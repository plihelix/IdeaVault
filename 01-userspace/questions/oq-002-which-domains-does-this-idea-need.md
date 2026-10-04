---
id: OQ-002
type: open-question
title: Which domains does this idea need
status: draft
owner: owner
updated: 2026-10-03
tags: [open-question, shape]
due: 2026-10-31
links: [ADR-0001, VLT-SHAPE, IDX-90, ID-SCHEME, OQ-001]
---

# OQ-002: Which domains does this idea need

Status: draft, open since 2026-10-03.

## Question

Of the shipped domains - idea, claims, structure, plan, risk, quality, evidence - which does this idea actually need, which stay empty, and which one belongs in the free `80-` slot?

## Blocks

The shape of the vault, not its first content. A domain that this idea has no use for will be filled with material that does not belong to it, and a domain the idea needs that is missing will be filled in somewhere else. It blocks the decision of whether to split a namespace (a `REQ` register split two ways, for instance) and whether the idea needs a domain of its own rather than a folder inside an existing one. [ADR-0001](../decisions/adr-0001-the-template-holds-any-idea-in-generic-domains.md) points 1 and 2 are reopened by this answer.

## Answered by

The owner, with the agent proposing the change and writing the decision record. Reshaping is the owner's call: [reshaping.md](../../00-vault/reshaping.md).

## How it would be answered

Write the first dozen claims in `20-claims/` and the first parts or sections in `30-structure/`, then read where the material naturally landed. Where a folder's index had to be read twice to know where something goes, or material landed in a folder that says it does not belong there, the shape is wrong and is changed by a decision record.

## Due

2026-10-31, set 2026-10-03, deliberately after [OQ-001](oq-001-what-idea-will-this-vault-hold.md): a shape chosen before the subject is known is a taxonomy invented for its own sake.

## Answer

Nothing tried yet. The shipped set is a working default, and the free `80-` slot exists so that a needed domain can be added without renumbering.

## Evidence

None: the answer comes from the material the owner writes, not from outside.

## Open issues

[OQ-001](oq-001-what-idea-will-this-vault-hold.md) must be answered first.
