---
name: pr-screenshots
description: Real screenshots for a work PR that changes UI - capture the running app after a real login, fix fresh-checkout setup gaps without touching shared state, and attach images inline.
kind: contract
domain: work
profile: core
applicability: work repositories
requires: employer context, GitHub CLI
provenance: house
---

# Screenshots on a UI PR

Owns the visual evidence a work PR that changes UI carries for its human reviewers: what to capture, how
to clear local setup gaps, and how to attach images so they render inline.

## Capture the real thing

Log in with real credentials against a running instance, not a mock or isolated component render, and
land on each route and state the PR changed. Show the specific change rendering: the populated state when
data exists, otherwise the empty state labelled as empty. Use the project's own run skill when it has one.

## Setup gaps are not feature bugs

A fresh checkout often lacks what CI and long-lived environments already have:

- environment-scoped config that exists for test or CI but not plain local runs, such as redirect URIs or
  allowed origins;
- machine-level secrets outside the checkout, which are one-time machine setup; and
- named local resources, such as a database volume, fixed port or lock file, that collide across
  concurrent checkouts.

Fix the gap instead of faking the screenshot; a repeatable gap is debt worth recording. Never reset
another checkout's shared state to unblock your own run; give yours an isolated copy.

## Attach inline

1. Push the images to a scratch branch in the same repository, never the PR branch, under one folder per
   PR number. The scratch branch never merges.
2. Only add files to that branch; never clear or replace what is already there.
3. Reference each image in a PR comment by its raw URL at that commit so it renders inline.

If the reviewer must open a link to see the picture, it is linked, not attached.

```text
PR #214 changes /orders (list and empty state).
Push orders-list.png and orders-empty.png to screenshots/pr-214/ on branch Chore/PrScreenshots.
Comment: ![Orders list](https://raw.githubusercontent.com/<owner>/<repo>/<sha>/screenshots/pr-214/orders-list.png)
         ![Orders, empty state](https://raw.githubusercontent.com/<owner>/<repo>/<sha>/screenshots/pr-214/orders-empty.png)
```
