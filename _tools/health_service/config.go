package main

// Configuration for the health service. The shape is the one config.yaml shows;
// an unknown key is an error rather than something quietly ignored.

import (
	"fmt"
	"os"
	"strings"
)

type CheckConfig struct {
	Name        string
	Label       string
	Description string
	Command     string
	Enabled     bool
	Interval    int // seconds between runs
}

type Config struct {
	Path         string
	VaultRoot    string
	ScriptPath   string
	Runner       string
	Tick         int
	Timeout      int
	Listen       string
	PushURL      string
	AllowOrigins []string
	HistoryKeep  int
	Interval     int
	Checks       []CheckConfig
}

// defaultChecks is the catalogue the service knows about. Every entry is a command
// of _tools/vault.py, so the rules live in one place: the vault tooling.
func defaultChecks() []CheckConfig {
	return []CheckConfig{
		{Name: "integrity", Label: "Note rules", Command: "check", Enabled: true, Interval: 30,
			Description: "Every note says what it is, when it was last changed, and follows the vault's writing rules."},
		{Name: "size", Label: "Vault size", Command: "metrics", Enabled: true, Interval: 60,
			Description: "How big the vault is: how many notes there are, how many are finished, how many are still drafts."},
		{Name: "numbering", Label: "Numbering", Command: "ids", Enabled: true, Interval: 120,
			Description: "Whether every note has its own number, and whether room is left to number new ones."},
		{Name: "links", Label: "Links between notes", Command: "links", Enabled: true, Interval: 60,
			Description: "Whether notes point at each other properly, and whether any note is cut off from the rest."},
		{Name: "open_questions", Label: "Open questions", Command: "oq", Enabled: true, Interval: 60,
			Description: "Questions the project has not answered yet."},
		{Name: "decisions", Label: "Decision records", Command: "adr", Enabled: true, Interval: 300,
			Description: "Records of choices the project has made, and whether each one is settled."},
		{Name: "due_dates", Label: "Overdue and expired", Command: "due --stale 14", Enabled: true, Interval: 60,
			Description: "A deadline that has passed, a review date that has come round, or a note nobody has revised in a fortnight."},
		{Name: "recent_edits", Label: "Edits since commit", Command: "changed {{today}}", Enabled: true, Interval: 60,
			Description: "Notes git reports as changed since the last commit, and any of them whose own 'last revised' date was not brought up to date."},
		{Name: "output_drafts", Label: "Generated outputs", Command: "audit", Enabled: true, Interval: 300,
			Description: "Documents the vault issued for someone outside it: whether each one holds to its kind's length, is registered, and stays free of internal wording."},
		{Name: "language", Label: "Prohibited words", Command: "noise", Enabled: true, Interval: 300,
			Description: "Words that do not belong in a document written for someone outside the vault, and rule-strength words (must, should, may) used in writing that has not earned them."},
	}
}

func defaultConfig() Config {
	return Config{
		Runner:       "python3",
		Tick:         5,
		Timeout:      120,
		Listen:       "127.0.0.1:8791",
		PushURL:      "",
		AllowOrigins: []string{"http://127.0.0.1:8081", "http://localhost:8081"},
		HistoryKeep:  20,
		Interval:     30,
		Checks:       defaultChecks(),
	}
}

func loadConfig(path string) (Config, error) {
	cfg := defaultConfig()
	cfg.Path = path
	if _, err := os.Stat(path); err != nil {
		if os.IsNotExist(err) {
			return cfg, nil // no file: the defaults above
		}
		return cfg, err
	}
	root, err := parseFile(path)
	if err != nil {
		return cfg, err
	}
	for _, key := range root.Keys {
		switch key {
		case "vault_root", "runner", "tick_seconds", "timeout_seconds", "listen",
			"push_url", "allow_origins", "history_keep", "interval_seconds", "checks":
		default:
			return cfg, fmt.Errorf("%s: unknown setting %q", path, key)
		}
	}
	if cfg.VaultRoot, err = textSetting(root, "vault_root", cfg.VaultRoot); err != nil {
		return cfg, err
	}
	if cfg.Runner, err = textSetting(root, "runner", cfg.Runner); err != nil {
		return cfg, err
	}
	if cfg.Listen, err = textSetting(root, "listen", cfg.Listen); err != nil {
		return cfg, err
	}
	if cfg.PushURL, err = textSetting(root, "push_url", cfg.PushURL); err != nil {
		return cfg, err
	}
	if cfg.Tick, err = numberSetting(root, "tick_seconds", cfg.Tick); err != nil {
		return cfg, err
	}
	if cfg.Timeout, err = numberSetting(root, "timeout_seconds", cfg.Timeout); err != nil {
		return cfg, err
	}
	if cfg.HistoryKeep, err = numberSetting(root, "history_keep", cfg.HistoryKeep); err != nil {
		return cfg, err
	}
	if cfg.Interval, err = numberSetting(root, "interval_seconds", cfg.Interval); err != nil {
		return cfg, err
	}
	if origins := root.Get("allow_origins"); origins != nil {
		cfg.AllowOrigins = origins.Texts()
	}
	if cfg.Tick < 1 {
		return cfg, fmt.Errorf("%s: tick_seconds must be at least 1", path)
	}
	if cfg.HistoryKeep < 1 {
		cfg.HistoryKeep = 1
	}
	if cfg.Runner == "" {
		return cfg, fmt.Errorf("%s: runner must name a program that runs the vault tool", path)
	}
	if node := root.Get("checks"); node != nil {
		cfg.Checks, err = loadChecks(node, cfg.Interval, path)
		if err != nil {
			return cfg, err
		}
	}
	if cfg.Tick <= 0 || cfg.Listen == "" {
		return cfg, fmt.Errorf("%s: listen and tick_seconds are required", path)
	}
	return cfg, nil
}

func loadChecks(node *Node, defaultInterval int, path string) ([]CheckConfig, error) {
	if node.Kind != List {
		return nil, fmt.Errorf("%s: checks must be a list", path)
	}
	known := map[string]CheckConfig{}
	for _, check := range defaultChecks() {
		known[check.Name] = check
	}
	out := make([]CheckConfig, 0, len(node.Items))
	seen := map[string]bool{}
	for _, item := range node.Items {
		if item.Kind != Mapping {
			return nil, fmt.Errorf("%s: every entry under checks must be a mapping", path)
		}
		for _, key := range item.Keys {
			switch key {
			case "name", "label", "command", "description", "enabled", "interval_seconds":
			default:
				return nil, fmt.Errorf("%s: unknown setting %q under checks", path, key)
			}
		}
		name := item.Get("name").Text()
		if name == "" {
			return nil, fmt.Errorf("%s: a checks entry needs a name", path)
		}
		if seen[name] {
			return nil, fmt.Errorf("%s: %s is listed twice under checks", path, name)
		}
		seen[name] = true
		check, knownName := known[name]
		if !knownName {
			// An entry the service does not know is allowed: it runs whatever
			// command the file gives it, which is how a new check is added.
			check = CheckConfig{Name: name, Label: name, Command: "", Enabled: true, Interval: defaultInterval}
		}
		if label := item.Get("label"); label != nil && label.Text() != "" {
			check.Label = label.Text()
		}
		if description := item.Get("description"); description != nil && description.Text() != "" {
			check.Description = description.Text()
		}
		if command := item.Get("command"); command != nil && command.Text() != "" {
			check.Command = command.Text()
		}
		enabled, err := item.Get("enabled").Bool(check.Enabled)
		if err != nil {
			return nil, fmt.Errorf("%s: %s: %w", path, name, err)
		}
		check.Enabled = enabled
		interval, err := item.Get("interval_seconds").Int(check.Interval)
		if err != nil {
			return nil, fmt.Errorf("%s: %s: %w", path, name, err)
		}
		if interval < 1 {
			interval = defaultInterval
		}
		check.Interval = interval
		if check.Command == "" {
			return nil, fmt.Errorf("%s: %s needs a command", path, name)
		}
		out = append(out, check)
	}
	if len(out) == 0 {
		return nil, fmt.Errorf("%s: checks is empty, so nothing would be watched", path)
	}
	return out, nil
}

func textSetting(root *Node, key string, fallback string) (string, error) {
	node := root.Get(key)
	if node == nil {
		return fallback, nil
	}
	if node.Kind != Scalar {
		return "", fmt.Errorf("%s must be a single value", key)
	}
	return node.Value, nil
}

func numberSetting(root *Node, key string, fallback int) (int, error) {
	value, err := root.Get(key).Int(fallback)
	if err != nil {
		return fallback, fmt.Errorf("%s: %w", key, err)
	}
	return value, nil
}

// expandCommand replaces {{today}} with the current date, so a check can ask for
// the notes edited on a particular day without the file knowing the date.
func expandCommand(command string, today string) []string {
	fields := strings.Fields(strings.ReplaceAll(command, "{{today}}", today))
	return fields
}
