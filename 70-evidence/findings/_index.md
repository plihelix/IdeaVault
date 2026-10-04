---
id: IDX-70F
type: index
title: 70-evidence/findings - Findings
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, evidence, findings]
links: [IDX-70, IDX-70S, CON-VLT-001, ID-SCHEME, STATUS-MODEL, OQ-001]
---

# 70-evidence/findings - Findings

Purpose: hold what the vault concludes from its sources. A finding is where reading becomes a position, and it is the level a claim should cite.

## What belongs here

An `FND-###` note (block 1-60, file `fnd-NNN-<topic>.md`) for a conclusion that rests on source cards, on a measurement taken here, or on both: what was looked at, what it shows, how confident the vault is, and what would change the conclusion.

## What does not belong here

A single source's content: that is a card in [sources/](../sources/_index.md). A claim the idea takes on: `20-claims/`, which cites the finding. A decision: `01-userspace/decisions/`. A guess: a `draft` note in `10-idea/`, marked `[INFERENCE]`.

## Rules for this folder

- A finding names the cards it rests on by ID, or names the measurement and how it was taken. A finding with neither is an opinion filed in the wrong folder.
- `confidence:` is `high`, `medium`, or `low`, with a reason. High means independent sources agree or the measurement was taken here with a stated method.
- A finding that contradicts a claim in `20-claims/` is written anyway, and the claim cites it. Contradiction kept is the difference between evidence and justification.
- A finding is descriptive: no normative wording. What follows from a finding is written as a claim, a constraint, or a risk.
- A finding superseded by better evidence keeps its ID, gains `superseded-by`, and stays readable: the old conclusion is what the existing claims were written against.
- A finding nobody cites is deleted, not archived: an uncited conclusion is not yet part of the record.

## Catalogue

| ID | Finding | Confidence |
| --- | --- | --- |
| none yet | - | - |

## Evidence

A finding's evidence is the set of `S-###` cards or the named measurement listed in its own body. This index holds none: an index asserts nothing.

## Open issues

[OQ-001](../../01-userspace/questions/oq-001-what-idea-will-this-vault-hold.md) - the questions this vault will need answered, and therefore the findings it will need, are unknown until the idea is named.
