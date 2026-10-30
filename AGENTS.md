# work

Work is an employer-neutral work profile. This tooling repository, its primary checkout and every
worktree are work scope. Never select, require or inject `personal@tj-agents` or its generated policy
here. GitHub owner, publisher identity and checkout location do not establish personal-project scope.
Employer plugins own tracker choice and employer authorization; Work does not route records to Personal.

This repository uses the plugin layout `template:check` documents and enforces
(https://github.com/tj-agents/template). Authored skills live once under `.agents/<namespace>/skills/<subject>/SKILL.md`,
with each skill's scripts and templates beside it; related skills share a family folder, family first
(`state/client/` publishes `state-client`). `.agents/sync_generated.py`, `.agents/sync-generated.ps1`,
`.gitattributes`, `.gitignore`, `CLAUDE.md` and `.github/workflows/ci.yml` are vendored from the current Template.
Change them in Template, then run `template:update` to refresh them.

`.codex/skills/`, `.claude/skills/`, `.agents/INDEX.md`, both marketplace files and `plugins/*` are generated. Run
`pwsh .agents/sync-generated.ps1` after authored changes and require `pwsh .agents/sync-generated.ps1 -Check`
before delivery.

Work publishes one communication standard and six operations. Kind describes behavior; scripts and templates sit beside their owning skill.
