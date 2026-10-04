---
id: OQ-003
type: open-question
title: Which output kinds are worth generating
status: draft
owner: owner
updated: 2026-10-03
tags: [open-question, outputs]
due: 2026-11-14
links: [ADR-0004, IDX-01O, OUT-ELEVATOR, OUT-BRIEF, OUT-EXPLAINER, OQ-001]
---

# OQ-003: Which output kinds are worth generating

Status: draft, open since 2026-10-03.

## Question

Which shapes is this idea actually going to be read in: the three shipped kinds, some of them, or kinds the vault has not declared yet?

## Blocks

The output set the vault maintains. A kind nobody generates is a rule with no use, and a kind that is needed but undeclared means the document gets improvised outside the vault, where nothing checks its length or its sourcing. It decides whether `OUT-ELEVATOR`, `OUT-BRIEF`, and `OUT-EXPLAINER` are kept, narrowed, or retired, and whether this idea needs a kind such as a plan section, a decision summary, a briefing note, a chapter outline, or a claim-by-claim dossier.

## Answered by

The owner, from what they actually need to hand to somebody. The agent may propose a kind after seeing a document written outside the vault, and writes the decision record.

## How it would be answered

Issue one instance of each shipped kind from whatever the vault holds, and read them against the use they were meant for. A kind whose instance is never handed to anyone is retired; a document the owner keeps writing by hand outside the vault is a kind waiting to be declared, with its sections and word budget written from the documents that already exist.

## Due

2026-11-14, set 2026-10-03, deliberately last: a kind chosen before there is anything to say in it is a format designed for its own sake.

## Answer

Nothing tried yet. The three shipped kinds are a starting guess about what a vault says out loud, with budgets stated so that a reader can tell when a document has outgrown its purpose.

## Evidence

None: the budgets are stated limits, not measurements, and the answer depends on use rather than on outside sources.

## Open issues

[OQ-001](oq-001-what-idea-will-this-vault-hold.md) must be answered first; [OQ-002](oq-002-which-domains-does-this-idea-need.md) decides which folders a kind may draw from.
