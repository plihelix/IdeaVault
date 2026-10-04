---
id: IDX-TOOLS
type: index
title: _tools - The Checker, the Commands, and the Health Demo
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, tooling]
links: [CON-VLT-001, ID-SCHEME, STATUS-MODEL, REQ-LANG, VLT-USERSPACE, VLT-SHAPE, ADR-0003, ADR-0005, GUIDE-CHECKS]
---

# _tools - The Checker, the Commands, and the Health Demo

Purpose: make the vault's stated rules enforceable, and make the state of the vault readable without reading notes. Nothing in this folder is a note, and nothing here is ever cited as evidence.

## Files

| File | What it is |
| --- | --- |
| [vault_scan.py](vault_scan.py) | the integrity scan: every rule stated in `00-vault/`, applied to every markdown file |
| [vault.py](vault.py) | the command surface a person or an agent runs: reports, allocation, generation, commit messages |
| `health_service/` | the Go service that runs those commands on intervals and answers on one endpoint |
| `dashboard_server/` | the Go server and page that render that endpoint |

`_tools/` holds no markdown except this index: the scripts carry their own explanation in their docstrings, and a rule explained only in a script is a rule nobody can disagree with.

## Where the rules come from

`vault_scan.py` is the enforcement, `00-vault/` is the statement, and a disagreement between them is a defect in the script. The script ships no vault-specific constants: the namespaces, ID blocks, digit widths, per-folder allocations, spec folders, and the owner's name are read from [this-vault.json](../00-vault/this-vault.json) (ADR-0003). A missing or malformed instantiation file is reported as a problem, never checked against defaults.

## Commands

Run from the vault root: `python3 _tools/vault.py <command>`. Every report ends with `PROBLEMS: <n>`, and the command exits non-zero when that number is not 0.

| Command | What it answers |
| --- | --- |
| `check` | does every note satisfy the rules: frontmatter, `owner` by path, legal type and status, broken links, IDs outside their block, unlicensed normative wording, placeholders, duplicate definitions |
| `status` | what the vault holds, by status and type, with the problems |
| `metrics` | counts a person acts on: notes, claims, open questions, decisions, issued instances, instances over budget |
| `ids` | the state of every namespace: allocated numbers, gaps, and the block each namespace may use |
| `next <PREFIX> [folder]` | the next free ID in a block. The only way an ID is ever taken |
| `find <pattern>` | notes whose title, ID, or body matches |
| `links [note]` | what a note cites, and whether each citation resolves |
| `oq` | open questions with their due dates and what they block |
| `due [--stale N] [--date YYYY-MM-DD]` | what is overdue, and what nobody has touched for N days |
| `adr` | the decision records, their standing, and their superseding chains |
| `changed [date] [--staged]` | which notes changed, by git |
| `stamp [--changed] [--dry-run]` | set `updated:` to today on the notes git reports as changed |
| `words [note] [--sections]` | each instance's length against its kind's word budget, section by section |
| `noise [note]` | content terms that do not belong in a generated document |
| `audit` | every issued instance against its kind: budget, registration, banned terms, links to notes that no longer stand |
| `scaffold <type> "<title>" <folder>` | a filled skeleton from `_templates/<type>.md`, with the ID allocated and `owner` derived from the folder |
| `instantiate <name> ["<title>"]` | set the owner's name in every content note, rewrite `this-vault.json`, and remove the repository's front page (`README.md`, `assets/`) |
| `commitmsg "<subject>"` | the commit message for what is already staged: `<folder> + <folder>: <subject> (<IDs>)` |

## The health demo

`health_service/` runs the same commands a person would, on intervals, and answers on `/health` with one object per check. `dashboard_server/` serves a page that reads that endpoint. Both are Go, both build offline, and neither is required: the vault is checkable with `check` alone. Ports, intervals, and the vault root are configuration in `health_service/config.yaml`, not code.

## Rules for this folder

- Nothing here is cited as evidence, and no note depends on a script being present: the scripts enforce the rules stated in `00-vault/`, they do not create them.
- A rule change is written in the note that states it and in the script that enforces it, in the same commit.
- Scripts are Python standard library only, resolve the vault root from their own location, and are named in lowercase snake_case with no ID.
- Generated binaries, caches, and scratch output are gitignored. A tool that needs an install is a tool that will be skipped.
- Every report names file, line, and rule, and ends with `PROBLEMS: <n>`. A report that ends without a count is not a report.

## Evidence

The rules this tooling enforces are stated in [conventions.md](../00-vault/conventions.md), [id-scheme.md](../00-vault/id-scheme.md), [status-model.md](../00-vault/status-model.md), [requirement-language.md](../00-vault/requirement-language.md), [userspace.md](../00-vault/userspace.md), and [reshaping.md](../00-vault/reshaping.md). What ships here is decided by [ADR-0003](../01-userspace/decisions/adr-0003-one-instantiation-file-names-the-owner-and-the-id-blocks.md) and [ADR-0005](../01-userspace/decisions/adr-0005-tooling-and-the-health-demo-travel-with-the-vault.md).

## Open issues

None open here. Whether the dashboard stays read is tracked in [ADR-0005](../01-userspace/decisions/adr-0005-tooling-and-the-health-demo-travel-with-the-vault.md), not in this index.
