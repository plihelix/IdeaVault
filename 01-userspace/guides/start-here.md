---
id: GUIDE-START
type: note
title: Start Here
status: proposed
owner: owner
updated: 2026-10-03
tags: [userspace, guide]
links: [GUIDE-NOTES, GUIDE-SHAPE, GUIDE-AGENT, GUIDE-CHECKS, HOME, AGENTS, CON-VLT-001, ADR-0003, OQ-001, OQ-002, OQ-003]
---

# Start Here

Purpose: get this template into the shape of your vault, in about an hour, without reading every rule first.

## 1. Say whose vault this is

`00-vault/this-vault.json` is the one file that names this vault: its title, your name, and the ID blocks in use. Either edit it by hand, or run:

```
python3 _tools/vault.py instantiate <your-name> ["<Vault Title>"]
```

The command writes your name into `this-vault.json` and into the `owner:` field of every note that is not mechanism, so nothing is left holding the template's placeholder name. It also removes `README.md` and `assets/`: the repository's front page and the images that page shows are not notes, and the vault is not self-describing while they sit in it. Stage that removal and commit it with the rest.

## 2. Read the two entry pages

[HOME.md](../../HOME.md) says what the vault holds and what state it is in. [AGENTS.md](../../AGENTS.md) is the instruction sheet the agent works from; reading it tells you what the agent is allowed to do without asking.

## 3. Accept the mechanism, or amend it

Everything in `00-vault/` and the six decision records in `01-userspace/decisions/` are `proposed`, because accepting is your act and you have not read them yet. Work through them in this order: [conventions.md](../../00-vault/conventions.md), [id-scheme.md](../../00-vault/id-scheme.md), [status-model.md](../../00-vault/status-model.md), [userspace.md](../../00-vault/userspace.md), [requirement-language.md](../../00-vault/requirement-language.md), [reshaping.md](../../00-vault/reshaping.md).

For each one, either set `status: accepted` in its frontmatter, or leave it `proposed` and write a decision record saying what you want changed. Nothing else in the vault works until this step is settled, because every other note is written against these rules.

## 4. Write the idea down before it is good

Add a note in `10-idea/` saying what this vault is for, in the words you have now. A half-stated intention is a legitimate first note: name the parts you do not know as open questions instead of inventing answers.

[OQ-001](../questions/oq-001-what-idea-will-this-vault-hold.md), [OQ-002](../questions/oq-002-which-domains-does-this-idea-need.md) and [OQ-003](../questions/oq-003-which-output-kinds-are-worth-generating.md) are the vault's first work. Answer OQ-001 and the other two become answerable.

## 5. Drop the raw material in the inbox

Links, remarks, documents, fragments: one file each in `01-userspace/inbox/`, no tidying. Triage is the agent's job, and the agent will tell you where each thing landed.

## 6. Check that the vault is consistent

```
python3 _tools/vault.py check
python3 _tools/vault.py status
python3 _tools/vault.py links
```

Each ends with `PROBLEMS: 0`. A vault named in step 1 reports 0. A fresh clone reports exactly one problem, the front page, and step 1 removes it. Anything else in that first report means the template is wrong, and that is worth telling the agent before any of your own work goes in.

## 7. Commit

```
git add <the paths you touched>
python3 _tools/vault.py commitmsg "accept the mechanism and name the idea"
git commit -m "<the first line commitmsg printed>"
```

`git add` and `git commit` are separate commands, and the message comes from `commitmsg`, which reads the staged files.

## What the first week should produce

One note in `10-idea/` saying what the idea is. A handful of claims in `20-claims/` that you would defend if challenged. Enough source cards in `70-evidence/sources/` that the claims are not just your memory. And a decision record if you changed anything about the vault itself. If the first week produces only an inbox full of raw material and three answered questions, that is a normal first week.
