---
id: GUIDE-SHAPE
type: note
title: Reshaping the Vault Around Your Idea
status: proposed
owner: owner
updated: 2026-10-03
tags: [userspace, guide, shape]
links: [GUIDE-START, GUIDE-NOTES, VLT-SHAPE, VLT-USERSPACE, ID-SCHEME, IDX-00, ADR-0001, OQ-002]
---

# Reshaping the Vault Around Your Idea

Purpose: change the folders, namespaces, and output kinds when the shipped shape does not fit the idea - and do it as a recorded decision, so the change is legible afterwards.

The exact procedure, with the file to edit and the commands to run, is [00-vault/reshaping.md](../../00-vault/reshaping.md). This page is about the judgement around it: when to reshape, and what to keep stable.

## The shipped shape

Seven content domains - `10-idea/`, `20-claims/`, `30-structure/`, `40-plan/`, `50-risk/`, `60-quality/`, `70-evidence/` - plus `90-glossary/` and `99-archive/`, with `80-` left empty on purpose. That set is a reasonable first guess for an idea whose shape is not known yet, which is the state this template ships in.

It is not a classification of ideas. A research position may never need `30-structure/`. A plan may need `40-plan/` split into phases and owners. A body of knowledge may need a domain for the things it catalogues, and no domain for risks at all.

## Reshape when

- Material keeps landing in a folder whose index says it does not belong there.
- A folder's index has grown exceptions explaining why its own rules do not fit.
- A namespace runs out of numbers, or a namespace exists that nobody is allowed to allocate.
- Two folders hold the same kind of note and a reader has to guess which one owns it.
- The vault keeps producing documents in a shape nobody asked for.

Do not reshape because a name bothers you, or to mirror a taxonomy you read somewhere. A rename that changes no behaviour costs every link that pointed at the old path and buys nothing.

## What you decide, what the agent does

You decide: which domains this idea needs, which namespaces exist, which blocks they may allocate from, which output kinds are worth generating. Each of those is an `ADR-####` in `01-userspace/decisions/`, `proposed` until you accept it.

The agent carries it out: edits `00-vault/this-vault.json`, creates the folder and its `_index.md`, updates `HOME.md` and the affected indexes and guides, moves the notes, and runs `check`, `ids`, and `links` until they report 0.

## Shape changes that are cheap

- Adding a domain at the next free number (`80-` is free) with its own index.
- Adding a namespace with a fresh block, when the new kind of note is genuinely a new kind of statement.
- Adding an output kind.
- Splitting a folder that has grown two subjects, keeping every existing ID with the note that already held it.

## Shape changes that are expensive

- Renaming a domain: every relative link pointing at it has to be rewritten, and any guide that names it.
- Renumbering: not available. IDs are permanent, and a block is retired rather than reshuffled.
- Merging two domains: the retired index stays as an `archived` note pointing at the survivor.
- Changing the frontmatter contract, the status model, or the ownership split. Those are what make two notes comparable, so changing one is a decision about the vault itself, not about the idea.

## Half-finished reshapes, and how the checker catches them

| You forgot | What a report says |
| --- | --- |
| The folder's `_index.md` | `NN-folder/_index.md: missing folder instruction file` |
| The block in `this-vault.json` | `id ... outside the block for ...` |
| The folder in `spec_index_folders` | the claim-bearing sections are not required, so a spec index missing `## Evidence` goes unnoticed |
| A guide or index still naming the old folder | `links`: broken link |
| A namespace nobody was granted | `ids`: the prefix cross-listed against a folder that does not own it |

`check` after every shape change, then `ids`, then `links`. Three commands, and a shape change that survives all three is finished.
