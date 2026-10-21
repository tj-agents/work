---
name: confluence
description: Write or update a Confluence page through the Atlassian connector — HTML body, native panels and layouts, Mermaid diagrams readable in light and dark mode, and checking the stored and rendered result. Use when creating, editing or fixing a Confluence page or a diagram on one.
kind: utility
domain: work
profile: core
applicability: work repositories
requires: available connectors
provenance: house
---

# Write a Confluence page

## Write where you were asked

Write straight into a page the user owns or was assigned. Confluence keeps every version, so the write is
reversible: no local draft, and no "should I publish?". Ask first only for someone else's page that nobody
assigned.

## HTML, never markdown

Read `getContentFormatGuide` for the tool you will call, then write with `contentFormat: html`. A markdown
body becomes a wall of text without any of the pieces below. Read pages in `html` too, so macros and ids
survive a round trip.

## Use the native pieces

| Piece | For |
| --- | --- |
| Info panel (`panel-info`) | the summary a reader can stop at |
| Note panel (`panel-note`) | a caveat or warning |
| Custom panel (`panel-custom`) | colour-coded boxes, such as two concepts compared |
| Expand (`<details>`) | detail most readers skip: option tables, glossary, change log |
| Two-column layout | two concepts side by side |
| Status lozenge | the state of a risk, option or deliverable |
| Decision list | decisions made and still open |
| Task list | prerequisites; open questions with owners |
| Table of contents macro | a page with more than a few sections |

Put parallel items in a table, not bullets of prose. Never draw ASCII art or a coloured table as a diagram.

## Diagrams: the organisation's standard, through the site's macro

Look for the organisation's diagram standard before drawing anything, and follow it. For Mermaid, read a page
that already shows a Mermaid diagram in `html` and save exactly one of its macro elements as `sample.html`.
Keep each diagram in `diagrams/NAME.mmd` beside the page, put `{{NAME}}` on its own line where it goes, and
render with this skill's script:

```powershell
python -B <this skill's directory>/render_mermaid.py page.html sample.html out.html
```

Each macro copies the sample's shape, with the diagram as its body, a fresh `macroId` and, where the sample
has one, a fresh `date`. The app caches its drawing by `macroId`, so new source under an old id keeps showing
the old diagram: re-render before every write and never reuse the output.

## Colours that work in dark mode

Dark mode lightens default text, so a pastel fill with no text colour is unreadable. Colour nodes only with
`classDef`, setting `fill`, `stroke` and `color` together, and name classes so they cannot clash with node ids.
Pair a bold fill with white text, or a bright fill with dark text:

```text
classDef done fill:<bold fill hex>,stroke:<darker hex>,color:#FFFFFF
```

Never `style X fill:<pastel>` on its own. Leave unstyled nodes to the theme.

## Live docs merge API writes

A page with subtype `live` shows its collaborative editor document, not the stored body the API reads.
An API write is merged into that document rather than replacing it, so a macro the write replaced stays
beside its replacement: every diagram re-write adds a duplicate. On a live page, write diagrams once, and
change or remove an existing one in the editor, never by another API write.

## Verify before claiming it is done

After every write, re-read the page in `html` and confirm the version advanced and still carries the change.
Then look at the rendered page, through browser automation or by asking the user, before saying a layout,
diagram or colour fix works. The stored source does not prove what renders. On a live page the API read
cannot see duplicates, so count the macros in the editor's DOM.
