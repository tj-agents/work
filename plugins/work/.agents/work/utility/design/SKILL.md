---
name: design
description: The sections of an approach or design page for a work change - summary, background and plan diagrams, decisions with options, risks, running it, open questions, delivery and what was not verified.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context
provenance: house
---

# Design page

Owns the sections of an approach, design, spike or options page and what each carries. Load `docs:layout`
for page conventions and `docs:diagram` for every diagram; the medium's skill, such as `work:confluence`,
supplies its native pieces.

Put the page under the feature or area it changes, and follow that space's own conventions by link, such
as an options template, status vocabulary or diagram standard.

## Sections

1. Header table: work item, status, owner, reviewer, last updated.
2. **In 30 seconds**: problem, fix, done when. A lead who reads only this knows what and why.
3. Contents, two levels.
4. Background: today's flow as a diagram, naming every moving part a newcomer meets and why it exists.
5. The problem: what breaks without the change; why the obvious shortcut fails, collapsed.
6. The plan: a diagram of the mechanism, then a `Rule | Why` table.
7. Decisions, each marked decided or undecided, with options collapsed into `Option | Verdict | Why`
   (chosen, rejected, dropped) and what was given up.
8. What could go wrong: `# | Risk | What we do about it | Status` (covered, partly, open, check, manual,
   to do, unknown, accepted). Cover load on consumers, alerting, unknown subscribers, readiness of
   dependents, re-runs and partial failure, and writes that destroy good data.
9. Running it: prerequisites as a task list, steps per environment or tenant, order and rollback.
10. Open questions as a task list, each with an owner.
11. Delivery: `Change | What it does | State`.
12. Glossary and change log, each collapsed; every change to the approach gets a dated line.
13. A closing italic line saying what was not verified and when the code was read.

Use plain words, put jargon in the glossary, and give every moving part, rule and decision its why.

```text
# Order id unification          header: WI-123 | Proposed | Payments | Ana | 2 Nov 2026
In 30 seconds                   problem, fix, done when
1. Background                   sequenceDiagram of today
2. The problem                  shortcut, collapsed
3. The plan                     sequenceDiagram after + Rule | Why
4. Decisions                    Option | Verdict | Why, collapsed
5. What could go wrong          risk table with statuses
_Not verified: production row counts. Code read 2 Nov 2026._
```
