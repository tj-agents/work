---
name: ask-person
description: Draft a short human chat or DM to a named person. Use for tell Kate, let X know, Message for Yan, draft a message, or wording for a colleague, including inside an investigation or other answer. Always load work:ask and clip the draft with machine:clip.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: employer context, available connectors
provenance: house
---

# Ask a person

Load `work:ask` before drafting and follow its employer lookup, recent context, voice, verified clipboard and sending rules.

Resolve the requested person through the available chat connector using employer context. Read the relevant recent exchange and use the recipient's own terminology. If the connector is unavailable, work from the supplied conversation without claiming a lookup. Ask for a recipient only when ambiguity prevents a useful draft.

Lead with the question or useful update. Include the concrete fact they need and at most one supporting reason; stop after a few sentences. A request to let someone know during another task still invokes this skill and still ends in `machine:clip`, not an inline Message for X block.

A requirement decision belongs to `work:ask-the-team`; a request requiring infrastructure authority belongs to `work:ask-infra`. Keep the recipient's draft specific to what they can answer or do. Acknowledge the verified clipboard copy in one or two lines.
