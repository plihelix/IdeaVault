---
id: IDX-70
type: index
title: 70-evidence - Grounding Outside The Vault
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, evidence]
links: [HOME, CON-VLT-001, ID-SCHEME, IDX-70S, IDX-70F, IDX-20, OQ-001]
---

# 70-evidence - Grounding Outside The Vault

Purpose: hold what the vault knows about the world that it did not invent: one card per outside source, and one finding per synthesis across cards. Every claim in the vault that is not the owner's own intention traces back through this folder.

## What belongs here

- `S-###` (1-100), in [sources/](sources/_index.md): one card per external source - URL or citation, publisher, publication date, access date, a short excerpt, and what the card is used for.
- `FND-###` (1-60), in [findings/](findings/_index.md): a synthesis across cards, with a confidence level and the cards it rests on.

## What does not belong here

The claims the evidence supports: `20-claims/`. The owner's own measurements and statements: written in the claim note, with the method named, and not dressed up as a source card. A decision: `01-userspace/decisions/`. A question: `01-userspace/questions/`.

## Rules for this folder

- A source is written as a card before it is quoted anywhere. A claim that quotes a source with no card is a claim nobody can re-check.
- A card records what the source says, in the source's own terms, in a short excerpt. Interpretation belongs in a finding.
- A source that benefits from the claim it supports is marked `confidence: low` and never carries a number alone.
- A number quoted from outside carries the source's method in the card, including what the source did not measure.
- A finding names the cards it rests on and what would change its conclusion. A finding resting on one low-confidence card says so.
- Cards age: `review:` is set to six months out for anything measured and twelve for anything quoted from a document. An out-of-date card is treated as `draft` whatever its recorded status.
- Evidence that contradicts a claim is written down too, and the claim cites it. A vault that only stores supporting sources is a justification, not a record.

## Files

| File | ID | Role |
| --- | --- | --- |
| [sources/_index.md](sources/_index.md) | IDX-70S | one card per outside source |
| [findings/_index.md](findings/_index.md) | IDX-70F | syntheses across cards |

## Evidence

This folder is the evidence. Its own discipline - card before quote, method with every number, contradiction kept - is stated in [conventions.md](../00-vault/conventions.md).

## Open issues

[OQ-001](../01-userspace/questions/oq-001-what-idea-will-this-vault-hold.md) - what counts as a credible source for this idea cannot be written down until the idea is known, and a generic statement about credibility would be ignored by everyone who read it.
