---
id: IDX-30C
type: index
title: 30-structure/components - The Parts
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, structure]
links: [IDX-30, IDX-30I, ID-SCHEME, CON-VLT-001, OQ-002]
---

# 30-structure/components - The Parts

Purpose: one note per part of the idea, each saying what that part is responsible for, so that a reader can tell what the idea consists of without inferring it from a diagram.

## What belongs here

A `CMP-###` note for each part: `cmp-NNN-<topic>.md`, block 1-60, allocated with `python3 _tools/vault.py next CMP 30-structure`. A part may be a thing you build, a thing you already have, a person or body that carries a responsibility, a section of a written argument, or a category in a body of knowledge.

## What does not belong here

Boundaries: [interfaces/](../interfaces/_index.md). Obligations: `20-claims/`. Stages and roles: `40-plan/`. Anything that only organises notes is a folder, not a part.

## Rules for this folder

- One part per note. The note names the responsibility first, then the dependencies, then what the part is not.
- `## Depends on` lists the parts this one needs, by ID. `## Depended on by` lists what would break without it. A part with neither is not yet a part.
- Descriptive wording only: an obligation is a `REQ-###` elsewhere, cited here.
- A part that is really several parts gets a note each, and the parent note becomes an index of them.
- A part that turns out not to exist is `rejected`, with the reason, and the notes that depended on it are updated in the same commit.

## Catalogue

| ID | Part | Responsibility |
| --- | --- | --- |
| none yet | - | - |

## Evidence

None yet. A part that already exists outside this idea (a service, a publication, a person, an institution) cites the `S-###` card that establishes it.

## Open issues

[OQ-002](../../01-userspace/questions/oq-002-which-domains-does-this-idea-need.md) - whether parts here should be grouped by area or held flat depends on the idea, which is not named yet.
