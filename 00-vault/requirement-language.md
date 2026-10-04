---
id: REQ-LANG
type: note
title: Normative Language (RFC 2119 Usage)
status: proposed
owner: vault
updated: 2026-10-03
tags: [meta, language]
links: [CON-VLT-001, ID-SCHEME, STATUS-MODEL]
---

# Normative Language (RFC 2119 Usage)

Purpose: keep obligations unambiguous and testable, and keep the rest of the vault in plain indicative prose. Keywords follow RFC 2119 as used by IETF documents.

## Keyword set

`MUST`, `MUST NOT`, `REQUIRED`, `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, `RECOMMENDED`, `NOT RECOMMENDED`, `MAY`, `OPTIONAL`. `NEVER` stands for `MUST NOT`, `AVOID` for `SHOULD NOT`. Capitalised only when used normatively.

## Where they may appear

Only in a `REQ-*`, a `CON-*`, an `AC-*`, a `GATE-*`, a `STG-*`, and the Control line of a `CTL-*` entry - that is, in notes whose `type` is `requirement`, `constraint`, `acceptance-criteria`, `gate`, `stage`, or `control`. Everywhere else write indicatively: "the review step reads the ledger", not "the review step SHALL read the ledger". The checker enforces this by note type, so a note that wants normative wording has to be the kind of note that carries obligations, not a note that merely mentions one.

## Rules for a well-formed obligation

1. One obligation per statement. A sentence carrying two obligations is two statements.
2. Name the actor and the boundary: "the reviewer `MUST` reject an entry with no source", not "`MUST` reject".
3. State the observable condition, not the implementation: "`MUST` fail the gate when the count of unsourced claims rises" is testable; "`MUST` be rigorous" is not.
4. Every `REQ-*` names the `AC-*` that proves it, or is blocked on writing one.
5. A number carries its measurement method and, while unresolved, an `OQ-###`: "response time `MUST` stay under 2.0 s measured at the reader's side for a warm session `[BLOCKED: OQ-001]`".
6. `SHOULD` implies a recorded exception. If deviations are not going to be justified case by case, write `MUST` or drop the clause.
7. Do not write obligations about third parties you do not control. Their behaviour becomes an `ASM-*` or a `CON-*`, with a source card behind it.
8. An obligation must be answerable by someone who did not write it. If only the author knows what would satisfy it, it is a preference, not a `REQ-*`.

## Constraint, assumption, requirement

- `CON-*`: fixed outside the idea and not negotiable while the idea stands as it is - a budget, a law, a licence term, a device that already exists, a fact about the field. Requirements are derived from constraints; a constraint is never derived from a requirement.
- `ASM-*`: taken as true for now and falsifiable. Every assumption names the signal that would falsify it and the notes that break when it fails.
- `REQ-*`: an obligation the idea takes on - on a thing being built, a position being argued, a plan being carried out, or a body of knowledge being assembled.

Not every idea carries obligations. A settled body of knowledge may hold only `ASM-*` and `FND-*` notes; a half-stated intention may hold none yet. Absence is recorded as absence, not padded with invented requirements.

## Anti-patterns

- Statements that restate a preferred shape instead of the outcome ("the vault `MUST` use a folder per topic").
- Unbounded adjectives: robust, seamless, rigorous, comprehensive, world-class.
- Placeholder numbers presented as targets. Use `[BLOCKED: OQ-###]` instead.
- Normative claims about a product, a paper, or an institution, with no source card behind them.
- Obligations with no actor, so no observation can attribute a failure.
- Normative wording in a note that only describes: a finding, a guide, an index, or a generated document.
