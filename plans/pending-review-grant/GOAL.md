# Goal — let draft-comment post a pending review without a permission prompt

## Defect

`draft-comment` allows posting findings into a pending GitHub review once Tommy approves the exact wording,
but nothing grants the call. Claude Code's auto-mode classifier refused `gh api -X POST
repos/<owner>/<repo>/pulls/<n>/reviews --input <payload>` as an unapproved external write (2026-10-08,
Infonetica/cris-preaward-app #878 and #873). A raw `gh api` grant cannot be the fix: the body is in a file,
so a rule cannot tell a pending review from a submitted one, and the skill forbids ever submitting.

## Required behaviour

1. A script in the `draft-comment` skill, e.g. `scripts/post_pending_review.py <owner/repo> <pr> <payload.json>`.
   It refuses a payload that carries `event` or anything else that submits, posts through `gh api`, verifies
   the response `state` is `PENDING`, and prints the review id and URL. If a pending review already exists,
   it fails with a clear message rather than adding to or replacing it.
2. `plugins/work/harness.json` `requires.permissions` grants exactly that script: `claude_allow` Bash and
   PowerShell forms with `${PLUGIN_ROOT}` templates, and a `codex_prefix_rules` entry with justification and
   `match` / `not_match`, following the existing grants in `tj-agents/core`'s `plugins/engineering/harness.json`.
3. `draft-comment/SKILL.md` "Handover and posting" names the script as the way to post, in the fewest words.

Takes effect once `tj-agents/core` branch `Fix/HarnessGrantsAcrossMarketplaces` makes the permission sync
read non-`base-agents` marketplaces. Do not work around that here.

## Authorization

Tommy's explicit request (2026-10-08). Covers editing, tests, commit, push and opening the PR. Merging is Tommy's.

## Checkout

`C:\Users\TommySeery\source\repos\tj-agents\work.worktrees\Fix-PendingReviewGrant`, branch
`Fix/PendingReviewGrant` off `origin/Feature/WorkCommunications` `b210013` (draft PR #1, the only branch
with `plugins/work/harness.json`). Open the PR against `Feature/WorkCommunications`.

## Next Steps

1. Implement 1–3 above, regenerate packaged copies with the repository's generation step, and add tests
   for the script's refusal of `event`, its PENDING check, and the grant's presence in the package.
2. Run the repository's tests, commit, push, open the PR. Do not merge.

Lane: L4 (specified implementation with code-level judgement).

## Progress

- 2026-10-08: goal written and Codex launched by the cris-preaward-app review session.
- 2026-10-08: implemented the pending-review helper, narrow package grants, skill handover, generated outputs, and regression coverage. `python -B -m unittest discover -s .agents/tests`, `pwsh -NoProfile -File .agents/sync-generated.ps1 -Check`, and `git diff --check` passed. Next: review, commit, push, and open the authorized PR; do not merge.
