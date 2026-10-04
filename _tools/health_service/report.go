package main

// The store holds the newest result of every check, so a page reading the service
// sees the whole vault at once even though the checks run at different rates.

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"sort"
	"strings"
	"sync"
	"time"
)

type Result struct {
	Name        string            `json:"name"`
	Label       string            `json:"label"`
	Description string            `json:"description,omitempty"`
	Command     string            `json:"command"`
	Interval    int               `json:"interval_seconds"`
	Status      string            `json:"status"` // ok, attention, error
	Problems    int               `json:"problems"`
	Summary     string            `json:"summary"`
	Detail      string            `json:"detail,omitempty"`
	RanAt       time.Time         `json:"ran_at"`
	TookMS      int64             `json:"took_ms"`
	ExitCode    int               `json:"exit_code"`
	Lines       []string          `json:"lines,omitempty"`
	Numbers     map[string]string `json:"numbers,omitempty"`
	More        int               `json:"more_lines,omitempty"`
	History     []Round           `json:"history,omitempty"`
}

// Round is one finished run of one check: enough for a trend in a popup.
type Round struct {
	RanAt    time.Time `json:"ran_at"`
	Status   string    `json:"status"`
	Problems int       `json:"problems"`
	Summary  string    `json:"summary"`
	TookMS   int64     `json:"took_ms"`
}

// Snapshot is one reading of the vault: the newest result of every known check.
type Snapshot struct {
	Generated time.Time         `json:"generated"`
	Vault     string            `json:"vault"`
	Overall   string            `json:"overall"` // ok, attention, error, waiting
	Summary   string            `json:"summary"`
	Checks    []Result          `json:"checks"`
	Numbers   map[string]string `json:"numbers,omitempty"`
}

// Day is what a finished round keeps for the timeline: not a second copy of every
// report.
type Day struct {
	Generated time.Time `json:"generated"`
	Overall   string    `json:"overall"`
	Problems  int       `json:"problems"`
	Notable   []string  `json:"notable,omitempty"`
}

type Store struct {
	mu      sync.Mutex
	keep    int
	vault   string
	results map[string]Result
	rounds  map[string][]Round
	days    []Day
	updated time.Time // when the held state last changed, so a repeated poll reads the same body
}

func NewStore(keep int, vault string) *Store {
	return &Store{
		keep:    keep,
		vault:   vault,
		results: map[string]Result{},
		rounds:  map[string][]Round{},
		updated: time.Now().UTC(),
	}
}

// Add folds this round's results into the newest picture and returns it.
func (s *Store) Add(fresh []Result) *Snapshot {
	problems := 0
	now := time.Now().UTC()
	s.mu.Lock()
	for _, result := range fresh {
		s.results[result.Name] = result
		problems += result.Problems
		s.rounds[result.Name] = append([]Round{{
			RanAt:    result.RanAt,
			Status:   result.Status,
			Problems: result.Problems,
			Summary:  result.Summary,
			TookMS:   result.TookMS,
		}}, s.rounds[result.Name]...)
		if len(s.rounds[result.Name]) > s.keep {
			s.rounds[result.Name] = s.rounds[result.Name][:s.keep]
		}
	}
	s.updated = now
	snapshot := s.snapshotLocked()
	notable := []string{}
	for _, result := range fresh {
		if result.Status != "ok" {
			notable = append(notable, result.Label)
		}
	}
	s.days = append([]Day{{Generated: now, Overall: snapshot.Overall, Problems: problems, Notable: notable}}, s.days...)
	if len(s.days) > s.keep {
		s.days = s.days[:s.keep]
	}
	s.mu.Unlock()
	return snapshot
}

// Snapshot is the full held state, report lines included.
func (s *Store) Snapshot() *Snapshot {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.snapshotLocked()
}

// Brief is the same reading without the report text, so a page that only needs the
// tiles does not pull every report every time.
func (s *Store) Brief() *Snapshot {
	s.mu.Lock()
	defer s.mu.Unlock()
	snapshot := s.snapshotLocked()
	for index := range snapshot.Checks {
		snapshot.Checks[index].Lines = nil
		snapshot.Checks[index].Detail = ""
	}
	return snapshot
}

// Report returns one held check, report text included.
func (s *Store) Report(name string) (Result, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	result, ok := s.results[name]
	if !ok {
		return Result{}, false
	}
	result.History = append([]Round{}, s.rounds[name]...)
	return result, true
}

func (s *Store) Days() []Day {
	s.mu.Lock()
	defer s.mu.Unlock()
	out := make([]Day, len(s.days))
	copy(out, s.days)
	return out
}

func (s *Store) snapshotLocked() *Snapshot {
	checks := make([]Result, 0, len(s.results))
	numbers := map[string]string{}
	for _, result := range s.results {
		result.History = append([]Round{}, s.rounds[result.Name]...)
		checks = append(checks, result)
		for key, value := range result.Numbers {
			numbers[key] = value
		}
	}
	sort.Slice(checks, func(i, j int) bool { return checks[i].Name < checks[j].Name })
	overall, summary := summarize(checks)
	snapshot := &Snapshot{
		Generated: s.updated,
		Vault:     s.vault,
		Overall:   overall,
		Summary:   summary,
		Checks:    checks,
	}
	if len(numbers) > 0 {
		snapshot.Numbers = numbers
	}
	return snapshot
}

// summarize decides the one word the whole vault gets this reading.
func summarize(results []Result) (string, string) {
	var attention, failed []string
	for _, result := range results {
		switch result.Status {
		case "attention":
			attention = append(attention, result.Label)
		case "error":
			failed = append(failed, result.Label)
		}
	}
	switch {
	case len(results) == 0:
		return "waiting", "no check has run yet"
	case len(failed) > 0:
		return "error", "these checks could not finish: " + strings.Join(failed, ", ")
	case len(attention) > 0:
		return "attention", "these checks found something to look at: " + strings.Join(attention, ", ")
	}
	return "ok", "every check passed"
}

func pushSnapshot(url string, snapshot *Snapshot) error {
	body, err := json.Marshal(snapshot)
	if err != nil {
		return err
	}
	client := &http.Client{Timeout: 15 * time.Second}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return err
	}
	request.Header.Set("Content-Type", "application/json")
	response, err := client.Do(request)
	if err != nil {
		return err
	}
	defer response.Body.Close()
	if response.StatusCode >= 300 {
		return fmt.Errorf("%s answered %d", url, response.StatusCode)
	}
	return nil
}
