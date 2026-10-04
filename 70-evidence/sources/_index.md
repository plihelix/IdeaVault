---
id: IDX-70S
type: index
title: 70-evidence/sources - Source Cards
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, evidence, sources]
links: [IDX-70, IDX-70F, CON-VLT-001, ID-SCHEME, OQ-001]
---

# 70-evidence/sources - Source Cards

Purpose: one card per outside source, so that a claim written two years from now can still be traced to where it came from and when it was read.

## What belongs here

An `S-###` card (block 1-100, file `s-NNN-<topic>.md`) for anything the vault did not observe itself: a document, a publication, a dataset, a product page, a specification, a law, a talk, a conversation with a named person, a piece of code someone else wrote.

## What does not belong here

A synthesis across sources: [findings/](../findings/_index.md). The owner's own measurement: written in the claim it supports, with the method named. A restatement of a claim the vault already holds.

## Rules for this folder

- Card fields, in order: what the source is, where it is (URL or full citation), who published it, when it was published, when it was accessed, what it says (a short excerpt in the source's own words), what this vault uses it for, and `confidence:` with a reason.
- Write the card before the claim quotes it. A claim citing a card that does not exist is reported as an undefined reference.
- An excerpt is short and verbatim enough to be recognisable. A card that paraphrases an entire document is a finding, not a card.
- A source that benefits from the claim it supports is `confidence: low`, and a number it carries is never the only source for that number.
- A card nobody cites is deleted rather than kept as a reading list.
- `review:` is set when the card ages: six months out for a measurement, twelve for a document.

## Catalogue

| ID | Source | Used for |
| --- | --- | --- |
| none yet | - | - |

## Evidence

A source card is the evidence at its lowest level: it records what was read and when. It does not assert that what was read is true.

## Open issues

[OQ-001](../../01-userspace/questions/oq-001-what-idea-will-this-vault-hold.md) - the standard of credibility for this idea's sources is not written down yet, because the idea is not named yet.
