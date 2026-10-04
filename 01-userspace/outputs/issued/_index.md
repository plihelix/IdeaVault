---
id: IDX-01OI
type: index
title: 01-userspace/outputs/issued - Generated Instances
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, userspace, outputs]
links: [IDX-01O, OUT-ELEVATOR, OUT-BRIEF, OUT-EXPLAINER, ADR-0004]
---

# 01-userspace/outputs/issued - Generated Instances

Purpose: hold the documents this vault has actually issued, each generated from named notes in a declared kind, so that a document read by someone outside the vault can be traced back to what the vault believed when it was written.

## What belongs here

One file per issued instance, named `iss-<kind>-<topic>.md`, with `id: ISS-<KIND>` plus a date suffix when a kind is issued more than once (`ISS-ELEVATOR-2026-10-17`). Each instance links to its `OUT-<KIND>` kind note and to the notes it drew from.

## What does not belong here

Kind definitions - those are one folder up. Drafts of the idea itself. A document the owner wrote by hand, which is not generated and carries no `ISS-` handle.

## Rules for this folder

- An instance is generated on a date, from a stated set of notes, and the set is written in the note. A reader can then tell which claims the document was asserting.
- An instance draws from `accepted` and `proposed` notes. Anything drawn from a `draft` note is marked as draft in the body.
- An instance asserts nothing the vault has not already written somewhere else. A new claim in a generated document is written as a note first, then generated from.
- A shipped instance is not quietly rewritten. A revised version is a new instance with a new date, and the older one keeps its place.
- Every instance is registered in the table below; `audit` reports an instance that is not registered, out of its kind's word budget, or carrying a banned content term.
- `python3 _tools/vault.py words` reports each instance's word count against its budget, and `noise` reports banned terms.

## Instances

| ID | Kind | Generated | Words | Budget |
| --- | --- | --- | --- | --- |
| none yet | - | - | - | - |

## Evidence

An instance inherits its evidence from the notes it drew from, and lists them. It carries no evidence of its own: restating a claim does not strengthen it.

## Open issues

[OQ-003](../../questions/oq-003-which-output-kinds-are-worth-generating.md) - nothing has been issued yet, so no kind has been tested against what this idea will actually need to say.
