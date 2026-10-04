---
id: ADR-0004
type: decision
title: The vault issues standalone outputs in declared kinds
status: proposed
owner: owner
updated: 2026-10-03
tags: [decision, outputs]
links: [IDX-01O, IDX-01OI, OUT-ELEVATOR, OUT-BRIEF, OUT-EXPLAINER, IDX-TOOLS, VLT-USERSPACE, OQ-003]
---

# ADR-0004: The vault issues standalone outputs in declared kinds

Status: proposed, 2026-10-03.

## Context

The point of keeping a record is that it can be turned into something someone else can read: a short statement of the idea, a one-page brief, a long explainer, a plan section, a decision summary. If those documents are improvised each time, they drift from the record they came from, and nobody can tell which version agreed with which claims. The reference vault called these "products", which is one kind of thing an idea can be and collides with the idea itself in a vault whose subject is not a product.

## Decision

1. A **kind** is a declared shape the vault can generate: a note in `01-userspace/outputs/` with handle `OUT-<KIND>`, naming its sections, its word budget, and which folders it draws from.
2. An **issued instance** is one generated document of a kind, written to `01-userspace/outputs/issued/` with handle `ISS-<KIND>`, its issue date in frontmatter, and the notes it drew from named in its frontmatter `links:` rather than in its readable body.
3. An instance is generated from the notes that were `accepted` or `proposed` at issue time and says which. A claim still `proposed` is named as such inside the instance rather than smoothed over, and a `draft` note it rests on is marked as `draft`.
4. Word budgets are enforced by the tooling: `words` reports the length of a draft against its kind's budget, and `audit` reports every issued instance against its kind, along with placeholders and links to notes that no longer stand.
5. The three kinds shipped are `OUT-ELEVATOR` (60 to 120 words), `OUT-BRIEF` (350 to 600 words), and `OUT-EXPLAINER` (1200 to 3000 words). A kind is added by writing its note; a kind is retired by marking it `archived` and keeping its issued instances readable.

## Consequences

- An output is traceable: the instance names the notes it came from, and `audit` says when those notes have moved.
- Length is a property of the kind, not a preference of whoever generated the document, so the same kind produces comparable documents over time.
- Kinds are content-owned: the owner decides what shapes are worth generating, and the agent does not invent a kind to justify its own output.
- Three shipped kinds is a starting point, not a complete set: the useful kinds for a given idea are decided by [OQ-003](../questions/oq-003-which-output-kinds-are-worth-generating.md).

## Alternatives considered

- **Keep the reference vault's word "product".** Refused: for an idea that is a plan, a research position, or a body of knowledge, "product" is either wrong or a second name for the idea itself.
- **Generate outputs on request with no declared kind.** Refused: nothing then enforces length or sourcing, and the vault cannot tell a reader which output agreed with which claims.
- **Store outputs outside the vault.** Refused: an output nobody can trace back to the record is the point at which a record stops being useful.

## Affects

Written into [outputs/_index.md](../outputs/_index.md) and [outputs/issued/_index.md](../outputs/issued/_index.md); the three kind notes named above; the `words` and `audit` commands in [_tools/_index.md](../../_tools/_index.md).

## Evidence

No outside source is cited. The word budgets are stated limits chosen so that a reader can tell when a document has exceeded its purpose, not measurements.

## Revisit when

An issued instance is used in a way its kind does not describe, or `audit` reports instances whose kind nobody asked for.
