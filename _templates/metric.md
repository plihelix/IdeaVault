---
id: MET-000
type: metric
title: <<metric title>>
status: draft
owner: vault
updated: 2026-10-03
tags: [metric]
links: [GATE-000, REQ-000, FND-000, OQ-000]
---

# MET-000: <<metric title>>

Status: <<draft or proposed, with date>>.

Purpose: <<the number that says how the idea is doing, in one sentence, and the decision it makes easier>>.

## Metric

<<What is measured, in one sentence. A metric exists to make a decision easier, or it is decoration.>>

## Definition and unit

<<The exact quantity, its unit, and what counts as one instance of it. Two notes measuring near-identical things under one name is how a vault starts disagreeing with itself.>>

## Method

<<How it is obtained, from where, and what the method cannot see. A number with no method is not a metric.>>

## Cadence and history

<<How often it is taken, where the readings are kept, and how long a run of readings is needed before the number means anything.>>

## Threshold or target

<<The value that counts as acceptable, with its reason. A metric note is descriptive: an obligation attached to this number is written as a `REQ-###` in `20-claims/` and cited here. While the value is unresolved, write `[BLOCKED: OQ-###]` rather than inventing a target.>>

## Misleads how

<<What this number hides, and what would make it actively misleading. Every metric has this section, or it has not been thought about.>>

## Action

<<`GATE-###` or `ADR-####` that uses this number, and what is done when it moves. A metric nobody acts on is retired.>>

## Evidence

<<`FND-###` findings for a figure taken from outside, with the source's own method, or the measurement taken here.>>

## Open issues

<<`OQ-###` IDs about the threshold or the method.>>
