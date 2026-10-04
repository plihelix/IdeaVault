package main

// Vault health polling service.
//
// Tooling, not a note: no frontmatter, no ID, never cited as evidence (ADR-0015).
//
// The service polls the vault on the schedule in config.yaml by running the
// commands of _tools/vault.py, keeps the newest result of every check in memory,
// and answers client requests out of that held state. A client can poll as often
// as it likes and gets the same cached reading; only this service's own clock
// touches the vault.
//
// Run: go run .            (from this folder)
//      go build -o vault-health && ./vault-health
//
// Exit code 0 = every check passed, 1 = something was named.

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"flag"
	"log"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"sync"
	"syscall"
	"time"
)

func main() {
	configFlag := flag.String("config", "", "config file (default: config.yaml beside this program)")
	vaultFlag := flag.String("vault", "", "vault root (default: found from this program's own location)")
	once := flag.Bool("once", false, "run every enabled check once, print it, and exit")
	flag.Parse()

	cfg, err := loadConfig(resolveConfigPath(*configFlag))
	if err != nil {
		log.Fatalf("config: %v", err)
	}
	root, err := findVaultRoot(*vaultFlag, cfg.VaultRoot)
	if err != nil {
		log.Fatalf("%v", err)
	}
	cfg.VaultRoot = root
	cfg.ScriptPath = filepath.Join(root, "_tools", "vault.py")

	watched := enabledChecks(cfg)
	store := NewStore(cfg.HistoryKeep, root)
	log.Printf("vault      %s", root)
	log.Printf("checks     %d of %d enabled", len(watched), len(cfg.Checks))
	log.Printf("answers on %s", cfg.Listen)
	if cfg.PushURL != "" {
		log.Printf("pushes to  %s", cfg.PushURL)
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	if *once {
		snapshot := store.Add(runRound(ctx, cfg, watched))
		printSnapshot(snapshot)
		if cfg.PushURL != "" {
			if err := pushSnapshot(cfg.PushURL, snapshot); err != nil {
				log.Printf("push failed: %v", err)
			}
		}
		if snapshot.Overall != "ok" {
			os.Exit(1)
		}
		return
	}

	server := &http.Server{
		Addr:              cfg.Listen,
		Handler:           newHandler(cfg, store),
		ReadHeaderTimeout: 10 * time.Second,
	}
	serverProblem := make(chan error, 1)
	go func() { serverProblem <- server.ListenAndServe() }()
	go runSchedule(ctx, cfg, watched, store)

	select {
	case <-ctx.Done():
		log.Printf("stopping")
	case err := <-serverProblem:
		if err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %v", err)
		}
	}
	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := server.Shutdown(shutdownCtx); err != nil {
		log.Printf("shutdown: %v", err)
	}
}

func enabledChecks(cfg Config) []CheckConfig {
	out := []CheckConfig{}
	for _, check := range cfg.Checks {
		if check.Enabled {
			out = append(out, check)
		}
	}
	return out
}

// runRound runs the due checks together, a few at a time, so one slow report
// cannot hold up the rest.
func runRound(ctx context.Context, cfg Config, checks []CheckConfig) []Result {
	today := time.Now().Format("2006-01-02")
	results := make([]Result, len(checks))
	limit := make(chan struct{}, 3)
	var group sync.WaitGroup
	for index, check := range checks {
		group.Add(1)
		go func(index int, check CheckConfig) {
			defer group.Done()
			limit <- struct{}{}
			defer func() { <-limit }()
			checkCtx, cancel := context.WithTimeout(ctx, time.Duration(cfg.Timeout)*time.Second)
			defer cancel()
			results[index] = runCheck(checkCtx, cfg, check, today)
		}(index, check)
	}
	group.Wait()
	return results
}

// runSchedule is the only thing that asks the vault anything. Each check gets its
// own clock; a round that is still running when the next is due is skipped rather
// than stacked.
func runSchedule(ctx context.Context, cfg Config, watched []CheckConfig, store *Store) {
	type timer struct {
		check CheckConfig
		due   time.Time
	}
	scheduled := make([]timer, 0, len(watched))
	for _, check := range watched {
		scheduled = append(scheduled, timer{check: check})
	}
	ticker := time.NewTicker(time.Duration(cfg.Tick) * time.Second)
	defer ticker.Stop()
	busy := false
	for {
		now := time.Now()
		due := []CheckConfig{}
		for index := range scheduled {
			if scheduled[index].due.After(now) {
				continue
			}
			due = append(due, scheduled[index].check)
			scheduled[index].due = now.Add(time.Duration(scheduled[index].check.Interval) * time.Second)
		}
		if len(due) > 0 && !busy {
			busy = true
			snapshot := store.Add(runRound(ctx, cfg, due))
			busy = false
			for _, result := range snapshot.Checks {
				if !containsName(due, result.Name) {
					continue
				}
				log.Printf("%-15s %-9s %s (%d ms)", result.Name, result.Status, result.Summary, result.TookMS)
			}
			if cfg.PushURL != "" {
				if err := pushSnapshot(cfg.PushURL, snapshot); err != nil {
					log.Printf("push to %s failed: %v", cfg.PushURL, err)
				}
			}
		}
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
		}
	}
}

func containsName(checks []CheckConfig, name string) bool {
	for _, check := range checks {
		if check.Name == name {
			return true
		}
	}
	return false
}

// newHandler answers only from the held state: no vault work happens here.
func newHandler(cfg Config, store *Store) http.Handler {
	origins := map[string]bool{}
	for _, origin := range cfg.AllowOrigins {
		origins[origin] = true
	}
	allowAll := origins["*"]

	writeJSON := func(w http.ResponseWriter, r *http.Request, value any) {
		origin := r.Header.Get("Origin")
		if origin != "" && (allowAll || origins[origin]) {
			w.Header().Set("Access-Control-Allow-Origin", origin)
			w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
			w.Header().Set("Access-Control-Allow-Headers", "If-None-Match")
			w.Header().Set("Access-Control-Expose-Headers", "ETag")
			w.Header().Set("Access-Control-Max-Age", "600")
			w.Header().Set("Vary", "Origin")
		}
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		if r.Method != http.MethodGet {
			http.Error(w, "GET only", http.StatusMethodNotAllowed)
			return
		}
		body, err := json.Marshal(value)
		if err != nil {
			http.Error(w, "could not encode the answer", http.StatusInternalServerError)
			return
		}
		sum := sha256.Sum256(body)
		etag := `"` + hex.EncodeToString(sum[:8]) + `"`
		w.Header().Set("ETag", etag)
		w.Header().Set("Cache-Control", "no-store")
		wanted := r.Header.Get("If-None-Match")
		if wanted == "" {
			wanted = r.URL.Query().Get("etag")
		}
		if wanted == etag {
			w.WriteHeader(http.StatusNotModified)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write(body)
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		w.Header().Set("Content-Type", "text/plain")
		w.Write([]byte("vault health service\n\n" +
			"GET /health          the newest reading of every check\n" +
			"GET /report?check=   the full report of one check\n" +
			"GET /health/history  the rounds it has kept\n\n" +
			"Answers come from memory. The vault is only touched on its own schedule.\n"))
	})
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, r, store.Brief())
	})
	mux.HandleFunc("/report", func(w http.ResponseWriter, r *http.Request) {
		name := r.URL.Query().Get("check")
		result, found := store.Report(name)
		if !found {
			http.Error(w, "no check called "+name, http.StatusNotFound)
			return
		}
		writeJSON(w, r, result)
	})
	mux.HandleFunc("/health/history", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, r, map[string]any{"rounds": store.Days()})
	})
	return mux
}

func printSnapshot(snapshot *Snapshot) {
	log.Printf("overall    %s: %s", snapshot.Overall, snapshot.Summary)
	for _, result := range snapshot.Checks {
		log.Printf("%-15s %-9s %s (%d ms)", result.Name, result.Status, result.Summary, result.TookMS)
	}
}

// resolveConfigPath looks beside the program first, then in the current folder.
func resolveConfigPath(flagValue string) string {
	if flagValue != "" {
		return flagValue
	}
	candidates := []string{}
	if exe, err := os.Executable(); err == nil {
		candidates = append(candidates, filepath.Join(filepath.Dir(exe), "config.yaml"))
	}
	if cwd, err := os.Getwd(); err == nil {
		candidates = append(candidates, filepath.Join(cwd, "config.yaml"))
	}
	for _, candidate := range candidates {
		if _, err := os.Stat(candidate); err == nil {
			return candidate
		}
	}
	return "config.yaml"
}

// findVaultRoot resolves the vault from this program's own location rather than
// the working directory: the folder that holds _tools/vault.py. go run builds in a
// temporary folder, so the current folder is tried as well.
func findVaultRoot(flags ...string) (string, error) {
	for _, given := range flags {
		if given == "" {
			continue
		}
		root, err := filepath.Abs(given)
		if err != nil {
			return "", err
		}
		if isVault(root) {
			return root, nil
		}
		return "", &vaultError{given}
	}
	starts := []string{}
	if exe, err := os.Executable(); err == nil {
		starts = append(starts, filepath.Dir(exe))
	}
	if cwd, err := os.Getwd(); err == nil {
		starts = append(starts, cwd)
	}
	for _, start := range starts {
		root := start
		for range 7 {
			if isVault(root) {
				return root, nil
			}
			parent := filepath.Dir(root)
			if parent == root {
				break
			}
			root = parent
		}
	}
	return "", &vaultError{""}
}

func isVault(candidate string) bool {
	info, err := os.Stat(filepath.Join(candidate, "_tools", "vault.py"))
	return err == nil && !info.IsDir()
}

type vaultError struct {
	given string
}

func (e *vaultError) Error() string {
	if e.given != "" {
		return e.given + " does not hold _tools/vault.py"
	}
	return "could not find the vault (a folder holding _tools/vault.py); pass -vault"
}
