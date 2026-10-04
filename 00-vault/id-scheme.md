---
id: ID-SCHEME
type: note
title: ID Scheme
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta]
links: [CON-VLT-001, VLT-SHAPE, ADR-0001, ADR-0003]
---

# ID Scheme

Purpose: stable, collision-free handles so notes can refer to each other, so a claim can be traced from the note that asserts it to the evidence behind it, and so a vault about any kind of idea uses one vocabulary instead of a vocabulary borrowed from whoever built it.

## Namespaces

Every numbered namespace, its block, and the folder allowed to allocate from it live in `this-vault.json`. The names below are the shipped set; [reshaping.md](reshaping.md) says how to add or retire one.

| Prefix | Namespace | Block | Allocated by |
| --- | --- | --- | --- |
| `REQ-###` | a claim the idea takes on as an obligation: what it must satisfy, provide, or hold true | 1-60 | `20-claims/` |
| `CON-###` | constraint: fixed outside the idea and not negotiable while the idea stands as it is | 1-40 | `20-claims/` |
| `ASM-###` | assumption: treated as true, and falsifiable | 1-40 | `20-claims/` |
| `AC-###` | acceptance criterion: the observable test of a `REQ-*` | 1-100 | `20-claims/` |
| `CMP-###` | a part of the idea, whatever kind of thing that part is | 1-60 | `30-structure/` |
| `IF-###` | the boundary across which two parts meet | 1-40 | `30-structure/interfaces/` |
| `STG-###` | a stage of the work the idea implies | 1-30 | `40-plan/` |
| `ROLE-###` | a role that carries a stage or holds a decision | 1-20 | `40-plan/` |
| `RSK-###` | a way the idea could fail or be defeated | 1-40 | `50-risk/` |
| `CTL-###` | a control that limits a `RSK-*` | 1-60 | `50-risk/` |
| `GATE-###` | a gate: a point where the idea is checked and can be stopped | 1-30 | `60-quality/` |
| `MET-###` | a metric: a number that says how the idea is doing | 1-40 | `60-quality/` |
| `S-###` | a source card: one external source | 1-100 | `70-evidence/sources/` |
| `FND-###` | a finding: a synthesis across sources | 1-60 | `70-evidence/findings/` |
| `ADR-####` | a decision record | 1-60 | [ADR-0001](../01-userspace/decisions/adr-0001-the-template-holds-any-idea-in-generic-domains.md) starts it |
| `OQ-###` | an open question the idea cannot yet answer | 1-40 | [OQ-001](../01-userspace/questions/oq-001-what-idea-will-this-vault-hold.md) starts it |

## Handles

Handles are named, not numbered. They are allocated once, in the folder that owns them, and never reused.

| Handle | Meaning | Allocated in |
| --- | --- | --- |
| `IDX-NN` | a folder's instruction file | the folder itself |
| `IDX-<NN><L>` | a sub-folder's instruction file | the sub-folder |
| `<PREFIX>-REG` | a register holding many entries of one namespace | the folder owning the register |
| `<TAG>-<TOPIC>` | a descriptive note that is not part of a numbered namespace | the folder holding it |
| `OUT-<KIND>` | an output kind: a shape the vault can generate | [01-userspace/outputs/_index.md](../01-userspace/outputs/_index.md) |
| `ISS-<KIND>` | one generated instance of an output kind | [01-userspace/outputs/issued/_index.md](../01-userspace/outputs/issued/_index.md) |

## Allocation rules

- An ID is allocated by the folder that owns the namespace, never reused, never renumbered. Gaps are legal but are reported, because a gap usually means a note was deleted without being superseded.
- Numbers are allocated in creation order, not importance order. Each folder's block is recorded in `this-vault.json` and repeated in that folder's `_index.md` for the reader. A writer may not allocate outside the block recorded for their folder.
- `python3 _tools/vault.py next PREFIX [FOLDER]` gives the next free ID. Nobody invents an ID by hand, and no ID is invented twice.
- An ID lives in exactly one note. When a note splits, the ID stays with the surviving primary note and the new notes take fresh IDs.
- Cross-folder references use the ID, never a file path: files move, IDs do not.
- Renaming a note's title never changes its ID.
- When a namespace is retired, its block is retired with it and its numbers are never handed out again ([reshaping.md](reshaping.md)).

## Traceability chain

`REQ-*` → `AC-*` (how it is proven) → `GATE-*` (where it is enforced) → `CMP-*` and `IF-*` (what carries it) → `CTL-*` against `RSK-*` (why it exists) → `FND-*` → `S-*` (what grounds it outside the vault).

A `REQ-*` with no `AC-*` is untestable and cannot reach `accepted`. A claim with no `FND-*`, `S-*`, or named measurement behind it is a guess and says so in place.
