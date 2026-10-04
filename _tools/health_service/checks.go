package main

// Running a check means running one command of _tools/vault.py, so the rules that
// decide what is wrong live in the vault tooling and not here.

import (
	"bytes"
	"context"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// maxLines caps what one check sends so a long report stays a small message.
const maxLines = 60

var problemsLine = regexp.MustCompile(`^PROBLEMS: (\d+)\s*$`)
var numberLine = regexp.MustCompile(`^([A-Za-z0-9_]+)=(.*)$`)

func runCheck(ctx context.Context, cfg Config, check CheckConfig, today string) Result {
	args := append([]string{cfg.ScriptPath}, expandCommand(check.Command, today)...)
	cmd := exec.CommandContext(ctx, cfg.Runner, args...)
	cmd.Dir = cfg.VaultRoot
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	started := time.Now()
	runErr := cmd.Run()
	result := Result{
		Name:        check.Name,
		Label:       check.Label,
		Description: check.Description,
		Command:     check.Command,
		Interval:    check.Interval,
		RanAt:       started.UTC(),
		TookMS:      time.Since(started).Milliseconds(),
	}

	all := []string{}
	for _, line := range strings.Split(stdout.String(), "\n") {
		trimmed := strings.TrimRight(line, " \t\r")
		if trimmed == "" {
			continue
		}
		all = append(all, trimmed)
	}
	numbers := map[string]string{}
	for _, line := range all {
		if m := numberLine.FindStringSubmatch(line); m != nil {
			numbers[m[1]] = m[2]
		}
	}
	if len(numbers) > 0 {
		result.Numbers = numbers
	}

	if runErr != nil && ctx.Err() != nil {
		result.Status = "error"
		result.Summary = "the check ran past its time limit"
		result.Detail = strings.TrimSpace(stderr.String())
		result.ExitCode = -1
		return result
	}
	result.ExitCode = 0
	if cmd.ProcessState != nil {
		result.ExitCode = cmd.ProcessState.ExitCode()
	}

	problems, named := 0, false
	for i := len(all) - 1; i >= 0; i-- {
		if m := problemsLine.FindStringSubmatch(all[i]); m != nil {
			problems, _ = strconv.Atoi(m[1])
			named = true
			break
		}
	}
	failure := ""
	if runErr != nil {
		failure = runErr.Error()
	}
	switch {
	case cmd.ProcessState == nil:
		result.Status = "error"
		result.ExitCode = -1
		result.Summary = "the command could not be run"
		result.Detail = firstNonEmpty(failure, stderr.String(), lastLine(all))
	case result.ExitCode >= 2:
		result.Status = "error"
		result.Summary = "the vault tool could not carry out this check"
		result.Detail = firstNonEmpty(stderr.String(), lastLine(all))
		result.Problems = problems
	case !named:
		result.Status = "error"
		result.Summary = "the check gave no problems count (exit " + strconv.Itoa(result.ExitCode) + ")"
		result.Detail = firstNonEmpty(stderr.String(), lastLine(all))
	case problems > 0:
		result.Status = "attention"
		result.Problems = problems
		result.Summary = plural(problems, "thing to look at", "things to look at")
	default:
		result.Status = "ok"
		result.Problems = 0
		result.Summary = "nothing to fix"
	}
	result.Detail = strings.TrimSpace(result.Detail)
	result.Lines = all
	if len(all) > maxLines {
		result.More = len(all) - maxLines
		result.Lines = all[:maxLines]
	}
	return result
}

func firstNonEmpty(values ...string) string {
	for _, value := range values {
		if value != "" {
			return value
		}
	}
	return ""
}

func lastLine(lines []string) string {
	if len(lines) == 0 {
		return ""
	}
	return lines[len(lines)-1]
}

func plural(count int, one, many string) string {
	if count == 1 {
		return "1 " + one
	}
	return strconv.Itoa(count) + " " + many
}

