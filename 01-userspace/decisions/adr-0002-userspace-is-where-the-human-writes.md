---
id: ADR-0002
type: decision
title: Userspace is where the human writes
status: proposed
owner: owner
updated: 2026-10-03
tags: [decision, userspace]
links: [VLT-USERSPACE, CON-VLT-001, IDX-01, IDX-01I, IDX-01Q, IDX-01D, IDX-01O, GUIDE-START, OQ-002]
---

# ADR-0002: Userspace is where the human writes

Status: proposed, 2026-10-03.

## Context

The mechanism needs rules, and rules need an author. But the person who owns the idea should not have to learn the mechanism before writing down a thought, and should not have to read mechanism notes to find their own material. In the reference vault this split was carried by `owner`: mechanism notes owned by the vault, everything else by the person. That worked, and it left one thing unstated: where a person writes when they have not yet decided what the material is.

## Decision

1. `01-userspace/` is the folder the owner writes in and reads directly: `inbox/` for material that does not know where it belongs, `questions/` for what the vault cannot answer, `decisions/` for choices that close an option, `outputs/` for what the vault generates, `guides/` for how to use the vault.
2. Every note under `01-userspace/` is content-owned: `owner:` is the owner's name, including the guides, because a guide the owner edits is the owner's instruction.
3. The exception is the index files. Every `_index.md`, including the userspace ones, stays `owner: vault`: an index is the folder's instruction, and instructions are mechanism. The rule stays path-derived, with no special case in the checker.
4. The agent writes into userspace for three things only: to record what the owner decided or asked, to generate an output in a declared kind, and to update a status the owner named. A change to the mechanism is written by the agent only into `00-vault/`, and only after a decision record exists in `01-userspace/decisions/`.
5. `inbox/` notes carry a descriptive handle (`INB-<TOPIC>`), not a number: no namespace is allocated in the inbox, because triage is what allocates.

## Consequences

- The owner can write a note without knowing the rules: the inbox accepts it, and the agent files it into the domain that owns it.
- Guides are editable by the owner without breaking the mechanism's ownership rule, and a guide edit is a content change, so it is committed as one.
- Two files carry instructions in userspace (the index files) and they read as instructions, not as content: a reader who disagrees with an index changes it through a decision record.
- The checker needs no userspace special case, which keeps `owner:` a single derivation from path.

## Alternatives considered

- **Make userspace notes mechanism-owned.** Refused: the owner's own questions and decisions would then be the vault's assertions, and the vault would be citing itself.
- **Give userspace its own third `owner` value.** Refused: a third value splits one field into two ideas, and every rule that derives `owner` from path would need an exception.
- **Put guides in `00-vault/` with the mechanism.** Refused: a guide is read while working, by the person working, and a mechanism folder is where the agent goes to change rules.

## Affects

Written into [userspace.md](../../00-vault/userspace.md) and the userspace index files. It authorises the guide set in [guides/](../guides/_index.md) and the output contract decided by [ADR-0004](adr-0004-the-vault-issues-standalone-outputs-in-declared-kinds.md).

## Evidence

The reference vault's `owner` split, and the mechanism notes this record authorises. No outside source is cited.

## Revisit when

The owner writes enough material that the inbox route stops being the easy route, or a guide needs an instruction the index files refuse to carry.
