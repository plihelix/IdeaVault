---
id: GUIDE-CHECKS
type: note
title: Checking the Vault
status: proposed
owner: owner
updated: 2026-10-03
tags: [userspace, guide, checks]
links: [GUIDE-AGENT, IDX-TOOLS, CON-VLT-001, ID-SCHEME, STATUS-MODEL, VLT-SHAPE, IDX-01OI, OQ-002]
---

# Checking the Vault

Purpose: know, in about ten seconds, whether this vault is doing what its own rules say it does.

## The commands

Everything runs through one script, and every report ends with `PROBLEMS: <n>`:

```
python3 _tools/vault.py check        # every rule the scanner enforces
python3 _tools/vault.py status       # counts by status and type, ID headroom
python3 _tools/vault.py metrics      # the same facts as key=value lines
python3 _tools/vault.py ids          # the ID ledger: allocated, gaps, out-of-block
python3 _tools/vault.py links        # broken links, notes nothing links to
python3 _tools/vault.py adr          # the decision ledger and supersession chains
python3 _tools/vault.py oq           # open questions with due dates
python3 _tools/vault.py due          # due and review dates; --stale 14 for neglected ones
python3 _tools/vault.py changed      # notes git reports changed since a date
python3 _tools/vault.py audit        # generated instances: budget, banned terms, registration
```

Add `--root PATH` to point any of them at a different vault. `_tools/health_service/config.yaml` is the schedule the health service runs; `_tools/dashboard_server/` serves the page that shows the same reports.

## What `PROBLEMS: 0` proves

That the vault is internally consistent: every note has the fields it needs, every ID is defined once and inside its block, every relative link resolves, every folder has an index, no note is holding a placeholder, no note uses normative wording it is not the kind of note to carry, and the `owner:` field matches the note's position in the tree.

## What it does not prove

That the claims are true. That a requirement is worth having. That the evidence is current - a source card from last year passes every check. That the idea is any good. The checker verifies the record, not the world; `due --stale 14` and the `review:` dates exist because the world is the part that ages.

## Cadence

| When | Run |
| --- | --- |
| Before committing any session's work | `check`, `links`, `changed` |
| After a reshaping | `check`, `ids`, `links`, in that order |
| Weekly | `status`, `adr`, `oq`, `due --stale 14` |
| Before generating a document | `audit`, `words`, `noise` |
| Before accepting anything | read the note, then `links <ID>` to see what refers to it |

## Reading a problem line

A line names the file, the line number, and the rule. Fix the note, not the rule, unless the rule is what is wrong - in which case the change is a decision record in `01-userspace/decisions/` and an edit to `00-vault/`, not a quiet exception in a script.

Two lines look like defects and are not:

- `mentioned with no definition` for an ID written as a shape in prose. Real undefined references are worth fixing; a shape written as `REQ-###` is how prose talks about a namespace without naming a note.
- A gap in a block that has never been used. Gaps are reported because they usually mean a deleted note that was never superseded. An unused block is not a gap.

## The health page

```
cd _tools/health_service && go build -o vault-health . && ./vault-health -once
cd _tools/dashboard_server && go build -o dashboard . && ./dashboard -listen 127.0.0.1:8081
```

`vault-health -once` runs the scheduled checks once and prints them, which is the fastest way to see whether the vault is well without keeping a service running. The long-running service listens on `127.0.0.1:8791` and answers `/health`; the dashboard page reads it and renders the panels. Both bind to localhost only, and both are configured in `_tools/health_service/config.yaml`.

A check that has run and reported problems shows on the page with its problem count and its last run time. A check that has never run is not a green panel: it is an unchecked claim about the vault.
