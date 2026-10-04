---
id: ADR-0005
type: decision
title: Tooling and the health demo travel with the vault
status: proposed
owner: owner
updated: 2026-10-03
tags: [decision, tooling]
links: [IDX-TOOLS, CON-VLT-001, ID-SCHEME, GUIDE-CHECKS, ADR-0003, OQ-002]
---

# ADR-0005: Tooling and the health demo travel with the vault

Status: proposed, 2026-10-03.

## Context

A vault whose rules live only in prose drifts: the rules are read differently by different people, and nobody notices until two notes disagree. The reference vault carried its rules in scripts that report file, line, and rule, plus a small service that runs those commands on a schedule and a page that shows the result. That is what made the reference vault dependable day to day. Whether that machinery belongs in a template - or is an accessory of one particular vault - is a decision the template has to state.

## Decision

1. The checker (`_tools/vault_scan.py`) and the command surface (`_tools/vault.py`) ship inside the vault, are mechanism, and are never cited as evidence.
2. The scripts read the vault's own configuration from `00-vault/this-vault.json` (ADR-0003) and resolve the vault root from their own location. Nothing in them names a person, a subject, or a folder set.
3. The health service and the dashboard ship alongside them, as the demonstration that the vault can be watched rather than re-read: the service runs the same commands a person would run, on intervals, and answers on one endpoint; the page renders that endpoint. Both are Go, both build with no network access, and both are optional to run.
4. Every report the tooling produces ends with a problem count, and the command a person is told to run is the command the service runs. There is no private check.
5. Binaries, caches, and generated output that is not a note are gitignored. `_tools/` holds no markdown except its own index.

## Consequences

- A fresh vault is checkable the moment it is instantiated, with nothing to install for the Python side.
- Rules can be changed only by changing the notes that state them and the script that enforces them in the same commit, which makes a rule change visible.
- The Go services add a build step for anyone who wants the dashboard; the checker works without them, and nothing in the vault depends on the service being up.
- The tooling is a maintenance cost: a rule the scripts cannot express stays a rule nobody enforces, and is written as such rather than pretended.

## Alternatives considered

- **Ship the prose rules only, and let each vault write its own checker.** Refused: an unenforced convention is a style, and the value of the reference vault came from the checks running on every change.
- **Write the services in Python too.** Refused: they already exist in Go, they build with the standard library, and rewriting working code to unify languages buys nothing the vault needs.
- **Keep the services outside the template as a separate demo repository.** Refused: the demo is how a new owner sees what the reports are for, and a template that ships half the machinery teaches the rules without the habit.

## Affects

Written into [_tools/_index.md](../../_tools/_index.md) and [checking-the-vault.md](../guides/checking-the-vault.md). The service ports and intervals live in `_tools/health_service/config.yaml`.

## Evidence

No outside source is cited: this is a decision about what ships with the vault.

## Revisit when

The dashboard stops being read, or a rule needs enforcement the scripts cannot express.
