---
id: IDX-40
type: index
title: 40-plan - How The Idea Gets Realised
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, plan]
links: [HOME, CON-VLT-001, ID-SCHEME, IDX-30, IDX-50, IDX-60, OQ-002]
---

# 40-plan - How The Idea Gets Realised

Purpose: hold the order in which the idea is carried out and who carries each part of it, so that "the plan" is a set of dated notes rather than a story told differently in each conversation.

## What belongs here

- `STG-###` (1-30): a stage of the work, with what has to be true to enter it and what proves it was completed. A stage is a state of the idea, not a task.
- `ROLE-###` (1-20): a role that carries a stage or holds a decision. A role is a responsibility with a name, whether it belongs to one person, several, or a tool.
- The handoffs between stages, and the decisions a stage must produce before the next one can start.

## What does not belong here

Tasks, tickets, calendars, and time estimates: those are working arrangements, and this folder records the shape of the work, not its schedule. Parts of the idea: `30-structure/`. What proves a stage worked: a `GATE-###` in `60-quality/`. What could stop it: `50-risk/`.

## Rules for this folder

- Stages are numbered in the order they happen, and the numbers are never reused when the order changes: a stage that is skipped becomes `archived` with a line saying why.
- Every stage names its entry condition and its exit condition. The exit condition is a `GATE-###` or an `AC-###`, cited by ID, never a mood.
- A `STG-###` is one of the note kinds licensed to carry normative wording: what must be true to leave a stage is written as an obligation, and the checker permits it here.
- A `ROLE-###` names what it decides, not what it does. A role with no decisions is a workload, not a role.
- A stage nobody is responsible for is blocked, and the block is written as `blocked-by: OQ-###`, not left implicit.
- A plan that changes shape supersedes the old stage notes rather than editing them: what was planned is what the claims were written against.

## Files

| File | ID | Role |
| --- | --- | --- |
| none yet | - | the first stage written here should be the one you could start this week |

## Evidence

None yet. A stage that depends on an outside fact - something shipping on a date, a rule changing, a resource existing - cites the `S-###` card that says so, and the assumption goes in `20-claims/`.

## Open issues

[OQ-002](../01-userspace/questions/oq-002-which-domains-does-this-idea-need.md) - an idea that is a body of knowledge or a position needs no stages at all, and this folder should then stay empty rather than hold a ceremony.
