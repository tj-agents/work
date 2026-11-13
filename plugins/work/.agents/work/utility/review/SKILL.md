---
name: review
description: The recorded review for human-reviewed work PRs - one record per branch keyed to the reviewed head, findings and severity, fix then incremental review, and staged review for very large PRs.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context
provenance: house
---

# Recorded review

Owns the agent's own review record for a work PR before people review it: where it lives, its shape,
finding states and severity, how fixes are re-reviewed, and staged review of a very large PR. A pass is
its base and head SHAs plus their diff. Replies to human reviewers use `work:respond-comments`.

## One record per branch

Keep the record outside the tracked tree at `<git-common-dir>/reviews/<branch-slug>.md`, resolving the
directory with `git rev-parse --git-common-dir` and replacing `/` in the branch name with `-`. Every
pass, including a staged one, appends to that file. Never commit it.

```markdown
# Review - <branch>

**Status:** in-progress|complete
**Reviewed head:** <full-sha> (<ISO date>)
**Judgment:** pending|approved|changes-requested

## Pass <ISO date> - full|incremental|staged

Base: <full-sha>  Head: <full-sha>
**Pass judgment:** pending|approved|changes-requested

- [ ] **R1 - HIGH** - `path/file.py:42` - verified defect and the concrete fix
```

Set status and judgments to `in-progress` and `pending` before reviewing. When the pass completes, set
the status `complete`, both judgments, and move `Reviewed head` to the pass head. A first pass has no
reviewed head until it completes. Finding IDs stay unique across the file; a pass with no findings says
so under its heading.

The reviewing session is the only writer. Other reviewers and lenses return candidate findings; the
writer verifies each against the diff, removes duplicates and assigns severity.

## Findings

| State | Meaning |
| --- | --- |
| `[ ]` | open |
| `[~]` | fix or staged coverage in progress |
| `[x]` | resolved, with the fixing commit |
| `[wontfix]` | final, with its reason and any employer debt record per `work:delivery` |

| Severity | Meaning |
| --- | --- |
| `CRITICAL` | immediately exploitable security flaw, data loss or catastrophic outage |
| `HIGH` | likely correctness, security or boundary failure with material impact |
| `MEDIUM` | concrete defect with limited impact or reach |
| `LOW` | concrete rule violation or regression with small impact |

Every retained finding is actionable; keep confidence apart from severity. A diff touching auth, secrets,
permissions or untrusted input gets a security pass inside the same review.

## Fix, then review the increment

Fix the fixable part of a finding immediately; carry only a genuinely blocked remainder to its owner.
A finding stays on this branch unless evidence shows it pre-existed on the base, the change neither
exposes nor worsens it, and its repair is independent. Fixing may tick a finding and append its fix
commit; it never rewrites the original text, severity or a completed pass judgment.

New commits get an incremental pass over `<reviewed-head>..<new-head>`. When
`git diff --quiet <reviewed-head> <head>` succeeds the trees are identical and the head counts as
reviewed. Base movement alone needs another pass only when it touches the PR's paths; the merge queue
validates the combined tree.

The PR may be marked ready when the status is `complete`, the reviewed head equals the PR head (or an
identical tree), and no `[ ]` or `[~]` finding remains. Delete the record once the branch merges or is
retired and every finding is terminal.

## Staged review for very large PRs

Use staged review when one sitting cannot cover the diff, normally above 300 changed files or across
several substantial components.

1. Freeze the merge base and the anchor head; every stage reviews `<merge-base>..<anchor>`.
2. Partition only the changed paths into areas: each path in exactly one area, about 50-150 files or
   10k diff lines per area, shared contracts before their consumers, and a final `Everything else`.
3. Add `## Coverage` with one `- [ ] <area> - <N files> - <exact paths or glob>` line per area, and
   `## Cross-area notes`.
4. Review areas strictly in order, one per sitting: mark `[~]`, review, record findings, mark `[x]`.
   An interrupted `[~]` area is re-run from the anchor. A finding whose other half lies in a later area
   becomes a cross-area note naming that area.
5. Finalize after the last area: resolve every note, write a short summary, set judgments and status, and
   stamp `Reviewed head` at the anchor. Commits after the anchor get an ordinary incremental pass.

```text
Feature/Export reviewed at a1b2c3: R1 HIGH open -> changes-requested.
Fix commit d4e5f6 -> incremental pass a1b2c3..d4e5f6: R1 [x] d4e5f6 -> approved, reviewed head d4e5f6.
PR head d4e5f6 == reviewed head, no [ ] or [~] -> gh pr ready 201.
```
