---
id: ADR-0003
type: decision
title: One instantiation file names the owner and the ID blocks
status: proposed
owner: owner
updated: 2026-10-03
tags: [decision, tooling, instantiation]
links: [ID-SCHEME, CON-VLT-001, VLT-USERSPACE, IDX-TOOLS, OQ-002]
---

# ADR-0003: One instantiation file names the owner and the ID blocks

Status: proposed, 2026-10-03.

## Context

A template cannot hardcode a person's name, and it cannot hardcode how many numbers a namespace may use: one idea needs sixty requirements, another needs four. In the reference vault both were written into the checker as constants, so the checker was a copy of one vault's decisions and every change to a block meant editing code. The template has to be instantiable by a person who is not editing Python.

## Decision

1. `00-vault/this-vault.json` is the single source of the vault's own facts: title, owner name, creation date, the namespaces with their blocks and digit widths, the folder-to-block allocations, and which folders are spec folders.
2. The checker loads it at start-up and reports a missing or malformed file as a problem. It carries no fallback constants: a vault whose configuration is unreadable is not a vault whose rules can be checked.
3. `python3 _tools/vault.py instantiate <name> ["<title>"]` sets the owner name in every content note, rewrites `this-vault.json`, and removes the repository's front page (`README.md`, and `assets/` with the images it shows), which ships with the template for a code forge and is not a note. Block edits are made in the JSON by the owner, or by the agent on the owner's instruction.
4. Editing a block never renumbers anything. A block is widened, or a namespace is added; numbers already issued keep their meaning, and a number no longer used stays unused.
5. The JSON is mechanism, is not a note, and is never cited as evidence.

## Consequences

- The tooling travels with the vault unchanged: nothing in `_tools/` names a person, a subject, or a folder set.
- A block change is a one-line edit in a data file, and the checker reports the new state on the next run.
- The owner's name appears in every content note, and renaming the owner is one command rather than a search-and-replace across the vault.
- A malformed `this-vault.json` stops `check` with a named problem instead of silently checking against the wrong rules.

## Alternatives considered

- **Keep the constants in the checker and edit them per vault.** Refused: the rules stated in `00-vault/` would no longer be the rules enforced, and a template whose configuration lives in code is a template you cannot use.
- **Put instantiation in frontmatter of a mechanism note.** Refused: frontmatter is a note's own metadata, and a note is the wrong place for values the whole toolchain reads on every run.
- **YAML instead of JSON.** Refused: YAML needs a parser the standard library does not have, and a template's tooling that needs an install is a template that breaks.

## Affects

Written into [id-scheme.md](../../00-vault/id-scheme.md) and [_tools/_index.md](../../_tools/_index.md); the checker and `vault.py` read this file. The instantiation command is step 1 of [start-here.md](../guides/start-here.md).

## Evidence

No outside source is cited: this is a decision about where the vault's own configuration lives.

## Revisit when

A vault needs per-folder rules the JSON cannot express, or two people need to instantiate the same template in one repository.
