---
id: IDX-50
type: index
title: 50-risk - How The Idea Could Fail
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, risk]
links: [HOME, CON-VLT-001, ID-SCHEME, IDX-20, IDX-40, IDX-60, OQ-001]
---

# 50-risk - How The Idea Could Fail

Purpose: hold the ways this idea could fail, be defeated, or cause damage, and what limits each of them. A risk written down with its control is a decision; a risk held in someone's head is a surprise waiting to happen.

## What belongs here

- `RSK-###` (1-40): a way the idea fails or is defeated - a thing that could happen, with what it would cost and what would tell you it happened.
- `CTL-###` (1-60): a control that limits a named risk: what it does, what it costs, and how you would know it stopped working.

## What does not belong here

An unknown fact: that is an `ASM-###` in `20-claims/` or an `OQ-###`. A thing that is already fixed against you: that is a `CON-###`. A worry with no consequence: not a risk yet. A gate that would catch a failure: a `GATE-###` in `60-quality/`, cited by the risk.

## Rules for this folder

- A risk names its cause, its consequence, and the signal that would show it happening. "Complexity" is not a risk; "the boundary in `IF-###` drifts because nobody owns it, and the two sides stop agreeing" is.
- Severity and likelihood are written as words with a reason (`high: the only copy is one person's time`), not as a score copied from a template. A number needs a method, and a method needs a source.
- Every `RSK-###` names its controls, or says plainly that it has none and is accepted. An uncontrolled risk with no decision to accept it is an omission.
- A `CTL-###` is licensed to carry normative wording: what it enforces is written as an obligation. Everywhere else in this folder, write indicatively.
- A control that removes a risk does not delete it: the risk note becomes `archived` with the control named, so a reader can see the risk was considered.
- Risks to the vault's own mechanism (a rule nobody follows, a check nobody runs) belong in `00-vault/` as a decision record, not here.

## Files

| File | ID | Role |
| --- | --- | --- |
| none yet | - | the first risk written here should be the one that would end the idea |

## Evidence

None yet. A risk grounded in something that has already happened elsewhere cites the `S-###` card or `FND-###` finding that records it; an imagined risk says so in place.

## Open issues

[OQ-001](../01-userspace/questions/oq-001-what-idea-will-this-vault-hold.md) - with no idea named, every risk written here would be a generic risk about ideas in general, which is the kind of writing that makes a risk register ignorable.
