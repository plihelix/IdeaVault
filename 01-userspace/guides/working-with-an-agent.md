---
id: GUIDE-AGENT
type: note
title: Working With an Agent in This Vault
status: proposed
owner: owner
updated: 2026-10-03
tags: [userspace, guide, agents]
links: [GUIDE-NOTES, GUIDE-CHECKS, AGENTS, VLT-USERSPACE, STATUS-MODEL, IDX-01, IDX-TOOLS, OQ-001]
---

# Working With an Agent in This Vault

Purpose: get work done through an agent without losing the split that makes the vault trustworthy - the agent writes, you decide, and the record shows which was which.

## What the agent is told

[AGENTS.md](../../AGENTS.md) is the instruction sheet. It says what to read first, which folders the agent writes in, which four things it may write in your folder, which statuses it may set, and which commands it must run before it calls work finished. Point it at that file rather than re-explaining the mechanism in conversation: a rule stated in the vault survives the session, a rule stated in chat does not.

## What it does well here

- Triage. Inbox entries become notes in the folder that owns them, open questions, or a proposal to delete, with the trail written on the entry.
- Widening. Reading a claim and writing the constraints, assumptions, acceptance criteria, and risks it implies.
- Grounding. Turning a remembered fact into an `S-###` source card with URL and access date, then a `FND-###` finding when several cards point the same way.
- Housekeeping. Keeping the ID ledger, the decision ledger, the due dates, and the `updated:` dates honest, and running the checker until it reports 0.
- Generating. Writing a document in a declared kind, from named notes, against a word budget.

## What stays yours

Accepting anything. Answering an `OQ-###`. Deciding, declining, closing options. Choosing output kinds and what they mean. Reshaping the vault. Anything that costs money, deletes work, or reaches outside this machine.

If an agent's summary claims a decision you did not make, that is a defect in the vault, not a wording problem: say so and it writes the record of what was actually decided.

## How to brief it

Name the subject, the folder you expect the work to land in, and what you want to be able to read afterwards. Then two constraints that do most of the work:

- "Start by reading the folder's `_index.md` and the notes already in it; do not write a second note for something one already holds."
- "Finish only when `check`, `links`, and `adr` report 0, and commit with `commitmsg`."

Ask for the open questions explicitly. An agent that is not asked will smooth over what it does not know; an agent that is asked will write an `OQ-###` with a due date, which is the difference between a vault that hides its gaps and one that dates them.

## What to look at when it reports finished

1. `python3 _tools/vault.py status` - what changed, and whether anything reached `accepted` that should not have.
2. `python3 _tools/vault.py adr` - whether it recorded the decisions its work implied.
3. `python3 _tools/vault.py due --stale 14` - whether it left questions sitting past their dates.
4. The `owner:` field of one new note - your name in a content note, `vault` in a mechanism note. This is the field that keeps the split visible, and `check` derives it from the path.
5. `git log --stat` - whether the commit message names the folders and IDs it touched.

## Failure modes worth catching early

- A decision record written for a choice you never made. Reject it, and say what you actually decided.
- A new note for a subject an existing note already holds. Ask it to edit or supersede instead.
- A claim with a source it never wrote a card for. Ask for the card, or watch the claim become an `[INFERENCE]`.
- Notes filed in the wrong folder because it was convenient. The `owner` mismatch will show up in `check`; the fix is to move the note, not to bend the rule.
- A mechanism file edited without a decision record. `adr` will not catch it; your reading of the commit will.
