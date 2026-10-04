---
id: IDX-30I
type: index
title: 30-structure/interfaces - The Boundaries
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, structure]
links: [IDX-30, IDX-30C, ID-SCHEME, CON-VLT-001, OQ-002]
---

# 30-structure/interfaces - The Boundaries

Purpose: one note per boundary, because a boundary is where an idea actually fails: each side assumes something about the other, and the assumption is usually unwritten.

## What belongs here

An `IF-###` note (block 1-40, allocated with `python3 _tools/vault.py next IF 30-structure`, file `if-NNN-<topic>.md`) for every place two parts meet: a handoff between stages, a boundary between this idea and something outside it, a document one side writes and the other reads, a decision one part makes that another part must live with.

## What does not belong here

A part's internal detail ([components/](../components/_index.md)). A constraint imposed from outside (`CON-###` in `20-claims/`) - though the interface note cites it. A stage handoff with no lasting boundary (`40-plan/`).

## Rules for this folder

- Name both sides by ID. A boundary with one named side is a plan, not an interface.
- State what crosses it and in which direction: a thing, a decision, a number, an obligation, a permission.
- State what each side assumes about the other, and link the `ASM-###` that carries each assumption. An interface with no named assumption has not been thought about yet.
- Descriptive wording: an obligation crossing the boundary is a `REQ-###` in `20-claims/`, cited here.
- A boundary nobody actually crosses is deleted as `rejected` with the reason, rather than kept as decoration.

## Catalogue

| ID | Boundary | Between |
| --- | --- | --- |
| none yet | - | - |

## Evidence

None yet. A boundary fixed by someone else's design - a format, a protocol, a rule, a contract - cites the `S-###` card that fixes it.

## Open issues

[OQ-002](../../01-userspace/questions/oq-002-which-domains-does-this-idea-need.md) - an idea that is a single undivided thing needs no interface notes at all, and this folder should then stay empty rather than hold invented boundaries.
