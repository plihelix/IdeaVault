---
id: IDX-30
type: index
title: 30-structure - The Parts And Their Boundaries
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, structure]
links: [HOME, CON-VLT-001, ID-SCHEME, IDX-30C, IDX-30I, IDX-20, IDX-40, OQ-002]
---

# 30-structure - The Parts And Their Boundaries

Purpose: say what the idea is made of and where its parts meet. "Parts" is deliberately broad: a component of a system, a section of an argument, a stage of a plan, a person in an arrangement, a term in a body of knowledge. What matters is that each part has a boundary, and the boundary is written down.

## What belongs here

- `CMP-###` (1-60), in [components/](components/_index.md): a part of the idea, with what it is responsible for and what it depends on.
- `IF-###` (1-40), in [interfaces/](interfaces/_index.md): the boundary across which two parts meet - what crosses it, in which direction, and what each side assumes about the other.

## What does not belong here

Why the parts are arranged this way: that is an argument, and an argument lives with the claims it supports in `20-claims/` or in a decision record. What will be built in what order: `40-plan/`. What could fail: `50-risk/`. Obligations the parts must satisfy: `20-claims/`, cited by ID.

## Rules for this folder

- A part is named by what it is responsible for, not by what it is called. Two parts with the same responsibility are one part.
- Every `CMP-###` names what it depends on and who depends on it. A part with neither is a placeholder.
- Every `IF-###` names both sides by ID, what crosses the boundary, and what each side assumes. A boundary nobody crosses is not a boundary.
- Structure notes are descriptive: no normative wording. An obligation a part must satisfy is a `REQ-###` in `20-claims/`, cited here.
- A diagram is drawn from these notes, and every node is labelled with its `CMP-###`. A diagram with nodes that exist nowhere is a second, contradicting structure.
- When the idea has no parts yet - an intention, a position, a plan not yet broken down - this folder stays empty and says so. Empty is a finding, not a gap.

## Files

| File | ID | Role |
| --- | --- | --- |
| [components/_index.md](components/_index.md) | IDX-30C | the parts |
| [interfaces/_index.md](interfaces/_index.md) | IDX-30I | the boundaries between parts |

## Evidence

None yet. A structure claim taken from outside - that a thing already exists, that a boundary is already fixed by someone else's design - cites a `70-evidence/` card.

## Open issues

[OQ-002](../01-userspace/questions/oq-002-which-domains-does-this-idea-need.md) - some ideas need this folder split further (a part per area, or a register per kind of part); whether this one does is not known yet.
