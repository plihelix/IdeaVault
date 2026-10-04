---
id: IDX-01D
type: index
title: 01-userspace/decisions - Decision Records
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, userspace, decisions]
links: [IDX-01, VLT-USERSPACE, VLT-SHAPE, STATUS-MODEL, ID-SCHEME, ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006]
---

# 01-userspace/decisions - Decision Records

Purpose: record the choices that close an option, so that a reader six months from now can tell what was decided, what it replaced, and what it was decided on.

## What belongs here

An `ADR-####` for any act that closes an option a reader would otherwise consider open: adopting or amending the mechanism, choosing or retiring a domain or namespace, accepting a claim into the plan, committing to an output kind, declining a proposal, or setting a limit that binds later work.

## What does not belong here

A finding about the world: that is `FND-###` in `70-evidence/findings/`. A question: that is `OQ-###`. A preference that closes nothing: keep it in `10-idea/` as a `draft` note. A restatement of a rule: the rule lives in `00-vault/`.

## Rules for this folder

- Block in use: numbers 1 to 60, four digits, allocated with `python3 _tools/vault.py next ADR 01-userspace`. Never invented, never reused, never renumbered.
- File names: `adr-NNNN-<topic>.md`, the topic in the name so a folder listing reads as a history.
- Body sections, in order: `# ADR-NNNN: title`, a `Status:` line, `## Context`, `## Decision`, `## Consequences`, `## Alternatives considered`, `## Affects`, `## Evidence`, `## Revisit when`.
- The `Status:` line reads `Status: proposed`, `Status: accepted`, or `Status: rejected`, with the date. `python3 _tools/vault.py adr` reports an accepted decision that carries no `Status:` line, because acceptance is the owner's act and has to be dated somewhere a checker can read.
- The owner accepts a decision. An agent may draft one as `proposed` when the owner has clearly made the choice, and must not write a decision the owner has not made.
- A decision that replaces an older one names it: `supersedes: ADR-NNNN` in frontmatter, and the older note gains `superseded-by` plus a line pointing here. Nothing is deleted.
- A decision that reverses an `accepted` claim also updates the claim note's `status:` and its index entry, in the same commit.
- A decision about the shape of the vault is written here and carried out in `00-vault/this-vault.json`, following [00-vault/reshaping.md](../../00-vault/reshaping.md).

## Ledger

| ID | Decision | Status |
| --- | --- | --- |
| `ADR-0001` | the template holds any idea in generic domains | proposed |
| `ADR-0002` | userspace is where the human writes | proposed |
| `ADR-0003` | one instantiation file names the owner and the ID blocks | proposed |
| `ADR-0004` | the vault issues standalone outputs in declared kinds | proposed |
| `ADR-0005` | tooling and the health demo travel with the vault | proposed |
| `ADR-0006` | the repository ships a licence that survives instantiation | proposed |

`python3 _tools/vault.py adr` prints this ledger from the notes themselves, including supersession chains, so the table above is for readers and the command is for checking that the table is true.

## Evidence

The decisions in the ledger describe this template's own construction. Their evidence is the working reference vault they were modelled on and the mechanism notes they authorise; none of them rests on an outside source.

## Open issues

All six records are `proposed` until the owner accepts them. [OQ-002](../questions/oq-002-which-domains-does-this-idea-need.md) may reopen `ADR-0001` once the idea is known, and [OQ-003](../questions/oq-003-which-output-kinds-are-worth-generating.md) may reopen `ADR-0004`.
