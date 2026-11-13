---
name: delivery
description: How work-project changes become human-reviewable PRs - slice size and splits, dependent stacks, draft then ready, merge queue and E2E tier, publish follow-up, debt PRs and employer records.
kind: policy
domain: work
profile: core
applicability: work repositories
requires: employer context, GitHub CLI
provenance: house
---

# Delivery in work projects

Owns the PR shape of work in an employer project, where people review every PR by hand: slice boundaries,
stacks, draft and ready, queue landing, publish follow-up, debt PRs and where employer problems are
recorded. The outcome, safety rules and exact-head merge stay with Core.

## One reviewable change per PR

Before implementing a large or multi-concern change, divide it into slices and give each its own PR. Every
slice lands green: it builds, keeps exposed behaviour working, preserves security invariants and carries
its tests. Keep an atomic schema, API and caller cutover in one slice rather than ship a broken
intermediate state. Extract tested preparatory refactors and independent infrastructure first. Record the
slice map (purpose, base or parent, dependency, expected size, verification) in the plan or PR body.

Measure against the actual base, counting uncommitted work too:

```bash
git diff --shortstat <base>...HEAD
git diff --numstat <base>...HEAD
```

Report generated files, lockfiles, docs and moves apart from substantive code and tests. Around 1,000
substantive changed lines or 40 substantive files, or a repository's stricter budget, requires a split
assessment before adding scope or requesting review; so does a smaller change spanning unrelated concerns.
An exception records its concrete reason and the rejected boundaries. "Same feature" or "already on this
branch" is not a reason.

Deliver sequentially by default: land the current slice, then branch the next from the fetched remote
default. A correction to an open slice goes to that slice's branch, not a new PR. An already oversized PR
keeps its head; split it only when smaller reviews outweigh rebuilding validated states.

## Stacks

Stack only when a child must proceed before its parent can land; record that reason in the slice map.

- Branch the child from the parent's current tip and open it against the parent:
  `gh pr create --draft --base <parent-branch>`.
- Review the child-only delta and validate the cumulative tree. Confirm CI runs for non-default bases.
- Land bottom-up. After the parent merges, confirm GitHub retargeted the child. After a squash merge,
  replay only the child's commits with `git rebase --onto origin/<default> <old-parent-tip> <child>` and
  rerun its checks.
- Never merge a child into an unmerged parent and call it landed. A parent edit means reconciling every
  descendant. Keep a stack as short as the active work needs.

## Draft, then ready

Open a draft at the first candidate that needs remote validation. Mark it ready with `gh pr ready` only
when its `work:review` record is complete for the PR head and exact-head CI is green; ready is not merge
authorization. Beyond Why and What, the body states what is not in the PR and a test plan separating what
was verified from what reviewers or CI must confirm. A visible UI change attaches `work:pr-screenshots`.

## Merge queue and E2E tier

Suites gated on `merge_group` report `skipping` on the PR; only the queue runs them. Run the full E2E tier
if and only if the diff can break behaviour that build, unit and integration tests cannot observe:

- a user-facing browser or UI flow;
- an HTTP, API or cross-service contract;
- a published package's public shape; or
- auth or routing behaviour visible only end to end.

Any trigger: remove every skip label and add the repository's full-tier label. No trigger: add the skip
label and remove the full-tier one; never run E2E "to be safe". Normalize labels before enqueueing, since
the queue reads them fresh. Prefer labels to commit trailers, which a blank line before an attribution
trailer silently drops.

Enqueue with `gh pr merge <n> --auto --match-head-commit <head>`. A queue rejects `--delete-branch`, so
delete the branch after it lands. Use `--admin` only when the user explicitly asks to skip the queue, for
a meta-only diff (Markdown, agent instructions, plans, docs; never CI workflows, package or project files,
lockfiles or migrations) or a wedged queue. A meta-only diff still gets a docs review. An ejection is a red
suite: fix the bug, push and re-enqueue; never force past it.

## Publish and version sync

Merging publishable source, as the repository's publish workflow path filter defines it, makes the merger
own the resulting sync. Find the run with `gh run list --commit <merge-sha>`, then the sync PR that run
created, never the newest by name. Follow it to merged. When it goes red, migrate the broken consumers in
that sync PR from its own checkout; never leave a red sync behind. A later unrelated publish that
supersedes it takes ownership. A published-contract rename is expand, republish, then sync, and is done
only when a repository-wide grep for the old identity returns zero.

## Debt

One PR per debt item. Bundle a second item only when it is small and mechanical, touches disjoint files
and neither depends on the other; give each item its own commit. An item that needs splitting leaves the
bundle and follows the slice rules above.

## Employer problem records

In a work project, the primary checkout's committed `.problem-records.json` (first entry of
`git worktree list --porcelain`) names the employer profile, for example
`{"schema_version":1,"provider":"<employer>:work-item"}`. A feature worktree's copy never overrides it.

| Operation | Employer skill |
| --- | --- |
| Read, list or view an item | `<employer>:work-item` |
| Record a new item | `<employer>:create-work-item` |
| Reconcile and carry out existing work | `<employer>:address-work-item` |

Employer evidence goes only to that employer's tracker: never Personal, a public repository or a Markdown
register. Creating an item needs the employer profile's creation decision; until it is given, keep the
facts in the current task and continue unaffected work. A missing or invalid selection, or an unavailable
profile, blocks recording; do not switch providers.

```text
Order export: 1,600 substantive lines across API and UI -> split assessment.
#201 Feature/ExportApi -> main: endpoint and tests, 700 lines; HTTP contract -> full E2E label.
#202 Feature/ExportUi -> Feature/ExportApi: page and tests, 900 lines; browser flow -> full E2E label.
#201 squash-merges -> git rebase --onto origin/main <old ExportApi tip> Feature/ExportUi, rerun checks.
#202 lands next; its publish run's sync PR is followed to merged.
```
