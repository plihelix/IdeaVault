---
id: IDX-01
type: index
title: 01-userspace - The Owner's Folder
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, userspace]
links: [VLT-USERSPACE, IDX-01I, IDX-01Q, IDX-01D, IDX-01O, IDX-01G, HOME, ADR-0002, ADR-0004]
---

# 01-userspace - The Owner's Folder

Purpose: the part of the vault the owner writes in and reads directly - raw material going in, questions being answered, decisions being recorded, documents coming out, and the guides that explain the rest.

The contract this folder implements is defined once, in [00-vault/userspace.md](../00-vault/userspace.md). Nothing here repeats it; the sub-folder indexes below say what belongs in each drawer.

## Sub-folders

| Folder | Holds | Index |
| --- | --- | --- |
| `inbox/` | raw material with no home yet; ephemeral | [inbox/_index.md](inbox/_index.md) |
| `questions/` | `OQ-###` open questions with due dates | [questions/_index.md](questions/_index.md) |
| `decisions/` | `ADR-####` decision records and the ledger | [decisions/_index.md](decisions/_index.md) |
| `outputs/` | the output kinds the vault generates, and `issued/` instances | [outputs/_index.md](outputs/_index.md) |
| `guides/` | how to use this vault, written for the owner | [guides/_index.md](guides/_index.md) |

## Rules for this folder

- Notes here carry the owner's name in `owner:`, except each `_index.md`, which is mechanism and carries `vault`. The rule is path-derived, exactly as it is everywhere else: [conventions.md](../00-vault/conventions.md).
- An agent writes here only to record the owner's acts: a question the vault cannot answer, a decision the owner made or was offered, a generated document, a triage note on an inbox entry. It never decides here on the owner's behalf.
- The owner sets `accepted` here and everywhere else. Nothing in this folder reaches `accepted` on its own.
- A guide routes to a mechanism note; it never restates one. A restatement is a second rule, and second rules drift.
- Nothing in this folder is evidence for a claim about the idea. Evidence lives in `70-evidence/`. A decision records a choice; it does not prove a fact.

## Evidence

None, by design. This folder records the owner's statements, decisions, and requests, which are primary for what the vault is doing but are not evidence about the world. Where a decision rests on an outside fact, the decision record cites the `S-###` or `FND-###` note that holds it.

## Open issues

[OQ-001](questions/oq-001-what-idea-will-this-vault-hold.md) what idea this vault will hold, [OQ-002](questions/oq-002-which-domains-does-this-idea-need.md) which domains it needs, [OQ-003](questions/oq-003-which-output-kinds-are-worth-generating.md) which outputs are worth generating.
