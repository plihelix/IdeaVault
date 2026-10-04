---
id: OUT-BRIEF
type: note
title: One-page brief
status: proposed
owner: owner
updated: 2026-10-03
tags: [output-kind]
links: [IDX-01O, ADR-0004, OUT-ELEVATOR, OQ-003]
---

# OUT-BRIEF: One-page brief

Purpose: the whole idea on one page, for a reader who will decide something from it and will not read anything longer.

## Word budget: 350 to 600 words

Long enough to state the idea and its grounds; short enough that a reader finishes it before forming an opinion. A brief that exceeds the budget has not compressed the idea, it has truncated it.

## Sections

1. **Statement** - the idea, in three or four sentences, with what it is not.
2. **Grounds** - the claims the idea depends on being true, each with how firmly the vault holds it.
3. **Shape** - the parts or sections the idea is made of, named plainly, no more than six.
4. **Plan of approach** - what happens first, what is decided before that, and what is deliberately not done yet.
5. **What could stop it** - the two or three risks the vault rates highest, each with what limits the vault has placed on it.
6. **Open questions** - the questions whose answers would change the brief, with their due dates.

## Draws from

`10-idea/`, `20-claims/`, `30-structure/`, `40-plan/`, `50-risk/`, `60-quality/`, `01-userspace/questions/`.

## May claim

What the vault holds as `accepted` without qualification. A `proposed` claim is written with its standing named, because a reader deciding something needs to know which grounds are firm and which are working positions.

## Must cite

Its kind and the notes it drew from, in frontmatter. Numbers appear with the reason they were chosen; a number with no method is left out rather than hedged.

## Not for

A reader who needs the argument rather than the conclusion: that is `OUT-EXPLAINER`. A brief is a decision document, not a summary for its own sake.

## Evidence

The budget is stated, not measured: 350 to 600 words is one printed page at a readable size, and a brief a reader has to turn over stops being a brief.

## Open issues

[OQ-003](../questions/oq-003-which-output-kinds-are-worth-generating.md) - which decisions this vault will need a brief for is not known yet.
