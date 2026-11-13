---
name: plans
description: Roadmap, plan and progress-ledger files for multi-PR work goals - shape, ledger fields, checkpoints, delivery states, cross-plan blockers, reconciling a change and close-out.
kind: convention
domain: work
profile: core
applicability: work repositories
requires: employer context
provenance: house
---

# Plans for multi-PR work

Owns the planning files behind a work goal that spans several PRs. The employer tracker item is the live
backlog and status; these files hold design and recovery state and link that item. Git history is the
archive: delete a plan once its work is terminal.

## Files

- **Roadmap** `<EPIC>_ROADMAP.md`: an epic's tracker and cross-plan dependency map, alive until the epic
  ships. Each item carries a stable backticked `<epic>/<slug>` key and keeps its tick after its plan is
  deleted.
- **Plan** `<NAME>_PLAN.md`: the design and outstanding phases of one buildable item.
- **Ledger** `<NAME>_PROGRESS.md`, beside its plan: a compact snapshot of current truth, not a history. A
  plan may have one ledger per parallel workstream.
- A reference that spins off no phases keeps a bare stem.

One folder per epic. A plan never cites its roadmap; agents may read the roadmap to navigate.

## Plan shape

Each phase is independently shippable and ends green, stating what it changes, why and its verification
gate. A phase shipping a capability something else consumes pins its consumption contract: who calls it
and the exact shape returned. The consumer may wait for a later phase; the output contract may not. Where
prose leaves a mechanism open, show the deciding code, written to the standards of its target paths.
Phases map to PR slices under `work:delivery`.

## Ledger

Headers `Plan:`, `Roadmap:` and `Roadmap item: <epic>/<slug>`, then current sections: worktree, branch and
`PR:` (URL or `not opened`); state including uncommitted work to preserve; milestones with commit or PR
links; latest verification; `## Reviews` linking the `work:review` gate and open findings; decisions still
affecting execution; and `## Next Steps` with one resolved action followed by these four lines:

```text
Scope: whole plan through all remaining phases and terminal delivery.
Current slice: <the PR or phase in hand>
Remaining scope: <what stays open after it>
Done when: <the terminal state>
```

Keep an entry only if removing it could make a fresh agent act wrongly or repeat a failed approach. Stay
under 200 lines and 16 KB. The active delivery branch owns its plan and ledger; never edit one ledger in
two checkouts.

Update the ledger only at a material milestone, a blocker or handoff, a completed review, a terminal
transition or an unsafe context end, inside the substantive commit that carries it. Never make a
bookkeeping-only commit. Never write a merge as the next step before a review is recorded.

Use one state vocabulary: **implementation-blocked**, **implementable, delivery-gated**,
**delivery-ready**, **merge-ready**, **terminal**. Keep two dependency graphs, what local implementation
needs and what must land before delivery; a delivery gate blocks implementation only when the required
source, API or exact artifact is unavailable.

## Cross-plan blockers

A waiting plan never polls. It starts `## Next Steps` with:

```text
Blocked: <the exact unmet gate>
Blocked by: <owning _PROGRESS.md ledger or external owner>
Unblock action: <what must be done, by whom>
Resume when: <evidence that the gate opened>
```

Each ledger named in `Blocked by:` gains a `## Downstream handoffs` entry naming the waiting ledger, its
worktree and the gate. The owner updates the waiting ledger when it crosses the gate and cannot close
while a downstream handoff is undispatched. A gate only a person can open replaces the four lines with
`Paused: <who> - <action and observable resume condition>`. A fact belonging to a sibling plan goes to
that plan's owner, never into both ledgers.

## Reconcile a change across a roadmap

For a decision, dependency, release or upstream API change: inventory the roadmap and every live plan on
the default branch and active branches; classify each as `roadmap`, `plan`, `ledger` or `none` by real
dependency; stop if a target file is dirty under another change; update only the owning level; replace
stale assumptions rather than append history. This touches planning files only, never product code.

## Close-out

Close only when the whole lifecycle is terminal: every PR merged and any publication and sync complete.
Reconcile the tracker item and close it only after its own acceptance is verified. Then delete the plan
and ledger and tick the roadmap item in the final substantive commit or one docs-only close-out PR. Run
`git status --short` over the plans folder first: a closed plan must show `D`, never `A` or `??`.
Delete a superseded or rejected plan when that is decided; strike shipped phases of a partly done one.
