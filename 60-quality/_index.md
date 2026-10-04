---
id: IDX-60
type: index
title: 60-quality - How The Idea Is Judged
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, quality]
links: [HOME, CON-VLT-001, ID-SCHEME, REQ-LANG, IDX-20, IDX-40, IDX-50, IDX-70, OQ-002]
---

# 60-quality - How The Idea Is Judged

Purpose: hold the points at which the idea is checked and can be stopped, and the numbers that say how it is doing. Without this folder, "it works" is whoever last looked.

## What belongs here

- `GATE-###` (1-30): a gate - a point where the idea is checked against named criteria and can be refused. A gate has an owner, a criterion, and a consequence for failing.
- `MET-###` (1-40): a metric - a number with a method, a unit, and a reason it was chosen. A metric exists to make a decision easier, or it is decoration.

## What does not belong here

The criteria themselves as obligations: those are `AC-###` in `20-claims/`, which a gate enforces. The stage a gate sits at: `40-plan/`. The risk a gate exists to catch: `50-risk/`. The measurement itself: a `FND-###` in `70-evidence/findings/`, which the metric cites.

## Rules for this folder

- A gate names what is refused when it fails, and who may let something through anyway. A gate with no consequence is advice.
- A gate cites the `AC-###` or `REQ-###` it enforces. A gate that enforces nothing is a ritual, and rituals get skipped.
- `GATE-*` and `MET-*` notes are licensed to carry normative wording in their criteria lines; the rest of the note writes indicatively.
- A metric states its unit, its method, its cadence, and what would make it misleading. A number without a method is not a metric.
- A metric nobody acts on is retired as `archived` with the reason, rather than kept running.
- A gate that has never been run is not evidence that the idea is sound: `audit` and the health page distinguish "ran and passed" from "has never run".

## Files

| File | ID | Role |
| --- | --- | --- |
| none yet | - | the first gate written here should be the one that could stop this week's work |

## Evidence

None yet. A criterion taken from outside - a standard, a rule, a published threshold - cites the `S-###` card that states it.

## Open issues

[OQ-002](../01-userspace/questions/oq-002-which-domains-does-this-idea-need.md) - some ideas need this folder to be the most-used folder in the vault, and some need one gate at most; which one this is stays unknown.
