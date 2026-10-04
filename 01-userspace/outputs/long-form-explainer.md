---
id: OUT-EXPLAINER
type: note
title: Long-form explainer
status: proposed
owner: owner
updated: 2026-10-03
tags: [output-kind]
links: [IDX-01O, ADR-0004, OUT-BRIEF, OQ-003]
---

# OUT-EXPLAINER: Long-form explainer

Purpose: the idea with its argument visible, for a reader who will disagree with something in it and needs to be able to see what the vault actually holds.

## Word budget: 1200 to 3000 words

Long enough to carry an argument, its grounds, and its objections. Below the budget the argument is asserted; above it the document has stopped being one line of reasoning and become a collection of sections.

## Sections

1. **What is being claimed** - the position, stated precisely enough to be argued against.
2. **Why** - the reasoning, in the order the vault reached it, with the claims it rests on named as claims.
3. **How it is made** - the parts, boundaries, responsibilities, or sections the idea consists of, with what each is responsible for.
4. **What it depends on** - constraints fixed outside the idea, assumptions the vault is making, and what each would break if it were false.
5. **How it is judged** - the criteria the idea is measured against, and where it is checked.
6. **What could go wrong** - the risks, their signals, and the limits placed on them.
7. **What is not settled** - the open questions, what each blocks, and their due dates.
8. **Where the grounds come from** - the outside sources in plain terms: what was read, when, and what it is used for.

## Draws from

Every domain: `10-idea/`, `20-claims/`, `30-structure/`, `40-plan/`, `50-risk/`, `60-quality/`, `70-evidence/`, plus the decision records in `01-userspace/decisions/`.

## May claim

What the vault holds, with its standing named. An explainer that presents a `proposed` claim as settled is the failure this kind exists to avoid: a long document is read as authority.

## Must cite

Its kind and the notes it drew from, in frontmatter. Outside sources are described in the readable body - what was read, when it was published, and what it is used for - because a reader who cannot check a source cannot disagree with it usefully.

## Not for

A reader who needs to decide today: that is `OUT-BRIEF`. An explainer is written to be argued with, and a decision document written this long gets read selectively and misquoted.

## Evidence

The budget is stated, not measured: 1200 to 3000 words is the length at which a single line of reasoning can hold its grounds and its objections at once.

## Open issues

[OQ-003](../questions/oq-003-which-output-kinds-are-worth-generating.md) - whether this vault needs a long form at all, or a different long form, is unresolved until the idea is named.
