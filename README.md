# Work

Work is employer-neutral standards and generic assistance for Tommy to use at work. It is designed for
local, Git-ignored injection into projects at whichever company he works for. Employer plugins supply
company-specific tracker routes, context and authorization. Infonetica is the current employer-specific
layer, not a requirement for future Work use. Learning is a separate optional overlay, such as when
learning a new language.

## Authoring this repository

This `tj-agents/work` source repository and its worktrees are Tommy's explicitly designated personal
tooling projects, so they adopt `personal@tj-agents` for authoring. That source designation does not
travel with the published Work profile: an actual employer project consuming Work through local,
Git-ignored configuration remains non-Personal and must not select or inject Personal. See
[AGENTS.md](AGENTS.md) for the canonical authoring-scope policy.

Employer-agnostic communication and review entry points for work repositories. Authored
skills live in `.agents/work`; Template generates the Claude and Codex payloads from that source.

The sibling `teams` plugin, authored in `.agents/teams` and selected in every repo, ships `teams:message`: its typed `teams_message.py` checks a Teams draft, renders links, inline code and code blocks to HTML, and copies and verifies it.

`work:ask-person`, `work:ask-the-team` and `work:ask-infra` share `work:ask`: load the exact employer context identified at session start, read available recipient context, draft briefly, and hand over through `teams:message`, which checks Teams markdown and copies it through `cli:clip`. The team route exhausts requirements evidence before asking; the infrastructure route establishes the relevant capabilities. Chat drafts are never sent without explicit current-message authorization.

`work:draft-comment` and `work:respond-comments` provide review workflows. Pasteable review drafts are plain prose.

`work:confluence` writes Confluence pages as HTML with native pieces and Mermaid diagrams readable in dark mode, and verifies the stored and rendered result. It ships `render_mermaid.py`, which renders `.mmd` sources into the site's own Mermaid macro, copied from an existing page, with a fresh id each run.

The ask workflows were restored from recovered skill loads and feedback memories, then separated from employer-specific routing and provider procedures. Employer plugins supply that context; this repository contains no employer identities or private chat data.

Install only for work repositories through the employer plugin's repository-local installation procedure.
Enable `tj-agents/work`, `tj-agents/base`,
`tj-agents/engineering` and `tj-agents/machine` together. Do not enable this plugin at user scope.
Its version 3 tier requires the reserved `employer` fact established by employer detection.

After authored changes, run `pwsh .agents/sync-generated.ps1`, `pwsh .agents/sync-generated.ps1 -Check`, and `template:check`. Run `python -B .agents/tests/test_packaging.py` for packaging isolation and dependency checks.
