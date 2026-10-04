---
id: IDX-20
type: index
title: 20-claims - What The Idea Depends On Being True
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, claims]
links: [HOME, CON-VLT-001, ID-SCHEME, REQ-LANG, STATUS-MODEL, IDX-10, IDX-60, IDX-70, OQ-001, OQ-002]
---

# 20-claims - What The Idea Depends On Being True

Purpose: hold every statement the idea takes as binding - what it must satisfy, what is fixed outside it, what it assumes, and how each of those would be proven. Everything downstream (structure, plan, risks, gates, generated documents) is written against this folder.

## What belongs here

| Namespace | Block | Statement |
| --- | --- | --- |
| `REQ-###` | 1-60 | an obligation the idea takes on: what it must satisfy, provide, or hold true |
| `CON-###` | 1-40 | a constraint fixed outside the idea: a budget, a rule, a licence, an existing thing, a fact about the field |
| `ASM-###` | 1-40 | an assumption: treated as true, and named as falsifiable |
| `AC-###` | 1-100 | an acceptance criterion: the observable test of a `REQ-###` |

## What does not belong here

What the idea is (`10-idea/`), what it is made of (`30-structure/`), what will be done in what order (`40-plan/`), what could go wrong (`50-risk/`), where it is checked (`60-quality/`), and the facts themselves (`70-evidence/`). A claim cites evidence; it does not contain it.

## Two ways to hold a claim

- **One note per claim** (`req-014-<topic>.md`), when the claim has argument, alternatives, or a history worth reading. This is the default for anything that could be contested.
- **A register** - one file holding many entries of one namespace (`constraints.md`, `type: constraint`) - when the claims are short, parallel, and read as a list. Each entry keeps its own ID in a `###` block heading or an unbackticked table cell, which is how the checker sees it as defined.

A register's own handle (`CON-REG`) is never cited as one of its entries. In any other folder's table, write IDs in backticks so they read as references and not as definitions.

## Rules for this folder

- Normative wording is licensed here and nowhere else in this folder's neighbourhood: `REQ-*`, `CON-*`, `AC-*` may use `MUST` and `SHOULD`; `ASM-*` may not. The shape of a well-formed obligation is in [requirement-language.md](../00-vault/requirement-language.md), and `check` enforces the licensing by note type.
- A `REQ-###` with no `AC-###` is untestable and cannot reach `accepted`: mark it `blocked-by: OQ-###` with a question about how it would be proven.
- A `CON-###` cites a source card. A constraint with no source is an assumption wearing a constraint's clothes, and will be renegotiated by someone who does not know it was supposed to be fixed.
- An `ASM-###` names the signal that would falsify it and the notes that break when it fails.
- A number is written with its method and, while unresolved, its `OQ-###`. A target number with no measurement behind it is a wish.
- Claims are allocated with `python3 _tools/vault.py next REQ 20-claims` and stay inside the block above.

## Files

| File | ID | Role |
| --- | --- | --- |
| none yet | - | the first claims written here should be the ones you would defend if challenged |

## Evidence

None yet. A claim becomes grounded by citing a `FND-###` finding or an `S-###` source card, and the card is written before the claim quotes it.

## Open issues

[OQ-001](../01-userspace/questions/oq-001-what-idea-will-this-vault-hold.md) - a vault with no idea cannot have claims, and inventing them to fill this folder would be the fastest way to make the vault misleading.
