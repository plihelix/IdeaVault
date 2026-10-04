---
id: ADR-0006
type: decision
title: The repository ships a licence that survives instantiation
status: proposed
owner: owner
updated: 2026-10-03
tags: [decision, licensing]
links: [CON-VLT-001, ADR-0003, IDX-01D, GUIDE-START]
---

# ADR-0006: The repository ships a licence that survives instantiation

Status: proposed, 2026-10-03.

## Context

A template on a code forge is read before it is understood, and a reader who intends to use it needs to know what they are permitted to do with it. Without a licence file the default is all rights reserved, which means every potential user has to ask, and most will not. The template is also unusual in what it contains: scripts, mechanism notes that are the rules themselves, skeletons, guides, example notes, and a front page with images. A licence has to cover all of that, and it has to say clearly where the template's licence stops and the owner's own work begins. The removal of the front page at instantiation ([ADR-0003](adr-0003-one-instantiation-file-names-the-owner-and-the-id-blocks.md)) makes a second question unavoidable: which files are the repository's own, and therefore stay when the vault is named.

## Decision

1. `LICENCE` at the repository root carries the MIT licence, with the copyright holder named and dated. It is a plain text file with no extension, so a code forge recognises it and the vault's scanner, which governs markdown notes, does not treat it as a note.
2. The licence covers the template as shipped: the scripts in `_tools/`, the mechanism notes in `00-vault/`, the skeletons in `_templates/`, the guides, the example notes a fresh clone carries, and `README.md` with the images in `assets/`.
3. What an owner writes into a vault instantiated from the template is the owner's work, and the template never claims a share of the idea it was used to organise. The MIT text is kept word-for-word so a code forge can classify it, and that boundary is stated on the front page and in this record instead of being written into the licence body.
4. `LICENCE` is a repository file, not a note: no frontmatter, no ID, no owner, no status. It is not reported by `check`, and `instantiate` leaves it in place, because the terms under which the template was shared do not change when the vault is named.
5. Changing the licence is a decision record first and an edit second, in the same commit, so a reader can see when the terms changed and why.

## Consequences

- A reader can clone and use the template without asking, and the forge shows the terms on the repository page.
- The mechanism stays reusable, which is the point of publishing it: the rules are worth more applied than guarded.
- Keeping the licence text canonical is what makes a forge read it as MIT rather than as an unrecognised custom licence. The cost is that the boundary it describes lives in the front page and in this record, so those are the places that have to be kept true if the template ever ships material it did not author.
- MIT places no obligation on downstream vaults, so nothing in a private vault is forced into the open by using this template.
- The file is invisible to the checker. Its correctness is the owner's responsibility, which is the same treatment `.gitignore` already gets.

## Alternatives considered

- **Creative Commons Attribution 4.0.** Refused: it fits prose better than code, and it leaves the scripts, which are the part people actually run, licensed awkwardly.
- **Apache License 2.0.** Refused: the patent grant is worth having for a large project, and is not worth a second file (`NOTICE`) and a longer text for a template of this size.
- **CC0, dedicating the template to the public domain.** Refused: it removes the attribution that makes the mechanism traceable to this vault, and it gives up any ability to say whose work a vault built from the template is.
- **GNU GPL.** Refused: a copyleft template would put every vault built from it under terms the owner cannot apply to their own private idea, which is the opposite of what a vault is for.
- **No licence file, and let each user ask.** Refused: it is the current state of most templates, and it stops use rather than shaping it.

## Affects

Written into [00-vault/conventions.md](../../00-vault/conventions.md) as a filesystem rule, and into the front page (`README.md`), which previously told readers to add a licence themselves. [ADR-0003](adr-0003-one-instantiation-file-names-the-owner-and-the-id-blocks.md) is unchanged: it still governs what `instantiate` removes, and `LICENCE` is not on that list.

## Evidence

No outside source is cited. The decision rests on the owner's instruction to publish the template with terms attached, and on what a code forge does with a repository that carries no licence file.

## Revisit when

The template begins shipping material the vault did not author; or the mechanism is adopted somewhere that needs a patent grant; or the owner decides the mechanism notes should be shared on different terms from the scripts. The owner notices, because the change is theirs to accept.
