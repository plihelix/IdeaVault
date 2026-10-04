---
id: HOME
type: index
title: Untitled Idea Vault - Template
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta]
links: [AGENTS, IDX-00, IDX-01, CON-VLT-001, ID-SCHEME, STATUS-MODEL, REQ-LANG, VLT-USERSPACE, VLT-SHAPE, ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006, OQ-001, OQ-002, OQ-003]
---

# Untitled Idea Vault - Template

Purpose: a working vault, empty of any particular idea, that a person and an agent can fill with whatever the idea turns out to be: a half-stated intention, a design, a plan, a product, a research position, or a settled body of knowledge.

This page is the vault's own front door. It says what the vault is for, how it is arranged, and what state it is in. It holds no claim about any idea, because there is no idea here yet.

## What this vault is

A git repository of short, dated, ID-addressable notes, arranged in domains, with rules that a program can check. Three things make it a vault rather than a folder of markdown:

1. **Every note says what it is.** Frontmatter names its ID, kind, status, owner, last substantive edit, tags, and the notes it depends on.
2. **Every claim says what it rests on.** Anything grounded outside the vault cites a source card or a finding; anything ungrounded is marked in place and cannot be `accepted`.
3. **Every obligation is testable and every unknown is named.** A claim without a test is blocked on writing one; a blank is written as an open question with a due date, never left as a gap in the prose.

The mechanism is generic on purpose. It names no product, no technology, and no field: the shape an idea needs is decided after the idea is known, and recorded when it is decided ([reshaping.md](00-vault/reshaping.md)).

## How to start

Read [01-userspace/guides/start-here.md](01-userspace/guides/start-here.md). In short: name the vault and yourself in `00-vault/this-vault.json`, accept or amend the mechanism, write one sentence about the idea in `10-idea/`, and let the open questions be open.

## Where you write

`01-userspace/` is the human's folder: the inbox, the open questions, the decision records, the generated documents, and the guides. Everything else is the agent's working ground, which the human reads and accepts but does not edit. The boundary is defined in [00-vault/userspace.md](00-vault/userspace.md) and enforced by `check`.

## Folder map

| Folder | Contains | Owner |
| --- | --- | --- |
| `00-vault/` | the mechanism: conventions, ID scheme, status model, normative language, the userspace boundary, the reshaping procedure, and `this-vault.json` | vault |
| `01-userspace/` | `inbox/`, `questions/`, `decisions/`, `outputs/` with `outputs/issued/`, and `guides/` | the owner |
| `10-idea/` | the idea as it is currently understood: the statement, its shape, its scope, what it is not | the owner |
| `20-claims/` | what the idea depends on being true: obligations, constraints, assumptions, acceptance criteria | the owner |
| `30-structure/` | the parts of the idea and the boundaries between them | the owner |
| `40-plan/` | how the idea gets realised: stages, roles, handoffs | the owner |
| `50-risk/` | how the idea could fail or be defeated, and what limits that | the owner |
| `60-quality/` | how the idea is judged: gates, metrics | the owner |
| `70-evidence/` | external grounding: `sources/` and `findings/` | the owner |
| `80-` | deliberately empty: the next free number, for a domain this idea needs and the shipped seven do not cover | - |
| `90-glossary/` | the vault's working vocabulary, including the terms the idea invents | the owner |
| `99-archive/` | superseded and rejected notes, kept with their IDs | the owner |
| `_templates/` | note skeletons; the only place a fill-in marker is legal | vault |
| `_tools/` | the checker, the vault command library, the health service, and the health page | vault |

## Current state (2026-10-03)

- The mechanism is written and **`proposed`**: [conventions.md](00-vault/conventions.md), [id-scheme.md](00-vault/id-scheme.md), [status-model.md](00-vault/status-model.md), [requirement-language.md](00-vault/requirement-language.md), [userspace.md](00-vault/userspace.md), [reshaping.md](00-vault/reshaping.md). Nothing in this vault is `accepted` yet, because accepting is the owner's act and the owner has not read it yet.
- Six decision records describe the template's own choices and are `proposed` pending sign-off: [ADR-0001](01-userspace/decisions/adr-0001-the-template-holds-any-idea-in-generic-domains.md) generic domains, [ADR-0002](01-userspace/decisions/adr-0002-userspace-is-where-the-human-writes.md) the userspace boundary, [ADR-0003](01-userspace/decisions/adr-0003-one-instantiation-file-names-the-owner-and-the-id-blocks.md) instantiation, [ADR-0004](01-userspace/decisions/adr-0004-the-vault-issues-standalone-outputs-in-declared-kinds.md) generated outputs, [ADR-0005](01-userspace/decisions/adr-0005-tooling-and-the-health-demo-travel-with-the-vault.md) tooling and the health demo, [ADR-0006](01-userspace/decisions/adr-0006-the-repository-ships-a-licence-that-survives-instantiation.md) the licence that travels with the repository.
- Three open questions are the vault's first work: [OQ-001](01-userspace/questions/oq-001-what-idea-will-this-vault-hold.md) what idea this vault will hold, [OQ-002](01-userspace/questions/oq-002-which-domains-does-this-idea-need.md) which domains it needs, [OQ-003](01-userspace/questions/oq-003-which-output-kinds-are-worth-generating.md) which outputs are worth generating.
- No claims, no structure, no plan, no risks, no gates, no evidence: those folders hold their rules and nothing else, which is the honest state of a vault that has not been given an idea yet.

## Reading order

[01-userspace/guides/start-here.md](01-userspace/guides/start-here.md) → [00-vault/conventions.md](00-vault/conventions.md) → [00-vault/id-scheme.md](00-vault/id-scheme.md) → [00-vault/status-model.md](00-vault/status-model.md) → [00-vault/userspace.md](00-vault/userspace.md) → [01-userspace/guides/reshaping-the-vault.md](01-userspace/guides/reshaping-the-vault.md) → [AGENTS.md](AGENTS.md).

## Working agreement

- Discussion output lands in the folder that owns it, not in a chat log. A decision made verbally gets its `ADR-####` the same day.
- A superseded note keeps its ID and points at its replacement. An `accepted` note is never rewritten.
- Anything taken from outside becomes an `S-###` source card with URL and access date before it is quoted anywhere.
- Before a session's work is committed: `check`, `links`, and `changed` all report `PROBLEMS: 0`.
