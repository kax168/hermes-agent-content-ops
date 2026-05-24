---
title: I Finished My Hermes Content Ops Agent With Tests, CI, and a Public Audit Trail
published: false
tags: githubchallenge, devchallenge, githubcopilot
---

*This is a submission for the [GitHub Finish-Up-A-Thon Challenge](https://dev.to/challenges/github-2026-05-21).*

![Hermes Agent Content Ops hero](https://raw.githubusercontent.com/kax168/hermes-agent-content-ops/main/assets/hero.png?v=3)

## What I Started

I started with **Hermes Agent Content Ops**, a real content-operations workflow for a Chinese WeChat Official Account.

The private version uses Hermes Agent to help run a two-post-a-day media workflow: topic research, article packaging, WeChat-safe HTML, local visual assets, draft-first WeChat delivery, and a Xiaohongshu pet-supplies review queue.

The first public repo was useful, but it was still mostly a challenge package. It had a README, diagrams, and sanitized sample scripts, but it did not have enough proof that the public artifact was finished and safe to maintain.

The unfinished parts were:

- no CI
- no tests
- no public audit command
- no before/after evidence inside the repo
- no explicit Copilot instructions for future assisted edits
- no repeatable quality gate for secret hygiene

## What I Shipped

For this finish-up pass, I turned the repo from a polished demo into a more complete public artifact.

I added:

- `content_ops/audit.py` for repeatable completion checks
- `scripts/run_finish_audit.py` to generate a Markdown audit report
- `tests/test_audit.py` for basic quality gates
- `.github/workflows/ci.yml` for GitHub Actions
- `.github/copilot-instructions.md` for future Copilot-assisted work
- `BEFORE_AFTER.md` to make the completion arc explicit
- `FINISH_UP_A_THON.md` to document what changed and why
- `WATCH_LAYER.md` and `content_ops/watch_layer.py` after a community comment pointed out that cron should not be the whole operating model

The public repo now has a way to answer: is the submission complete, inspectable, and safe to publish?

### Update after community feedback

After publishing the first version, Harpinder left a useful comment: the system should not rely only on cron. A real content operations agent should also have a watch layer that can wake on source changes, human review events, or safe retry conditions.

I agreed, so I added a lightweight event-aware layer:

- `content_ops/watch_layer.py`
- `scripts/watch_content_events.py`
- `WATCH_LAYER.md`
- `tests/test_watch_layer.py`
- `examples/watch-report.json`

Cron still owns the 07:00 and 18:00 rhythm, but the watch layer now models event-based wakeups for changed research, approved human review, and WeChat draft upload failures.

Example output:

```json
{
  "wakeAgent": true,
  "nextAction": "wake_agent",
  "events": [
    {
      "kind": "source_changed",
      "path": "topic_research.md",
      "reason": "topic research changed; agent should re-evaluate freshness and angle",
      "severity": "info"
    }
  ]
}
```

This made the project feel much less like "a cron script" and much more like an event-aware agent workflow.

## Before & After

Before:

- Strong project idea.
- Real private workflow behind it.
- Good README and visuals.
- Sanitized sample scripts.
- But no automated verification.

After:

- Public audit command.
- Unit tests.
- CI workflow.
- Secret-hygiene check.
- Before/after docs.
- Copilot-ready instructions.
- A generated completion report.
- Event-aware wakeups for source changes, human review approvals, and safe retries.

Run the audit:

```bash
python scripts/run_finish_audit.py
```

It writes:

```text
finish-audit-report.md
```

## Demo

Repository:

https://github.com/kax168/hermes-agent-content-ops

Core files added during the finish-up:

```text
content_ops/audit.py
scripts/run_finish_audit.py
tests/test_audit.py
.github/workflows/ci.yml
.github/copilot-instructions.md
BEFORE_AFTER.md
FINISH_UP_A_THON.md
```

The audit checks that the required public files exist, that the finish-up evidence exists, and that obvious credential tokens are not present in public source files.

## How GitHub Copilot Helped

The honest note: my local GitHub CLI exposed the `gh copilot` entry point, but the Copilot CLI binary was not installed in this environment when I attempted to invoke it. I did not want to pretend otherwise.

So I made the project **Copilot-ready** rather than writing a fake Copilot story.

The repo now includes `.github/copilot-instructions.md`, which tells future Copilot-assisted edits to:

- keep credentials out of the repo
- preserve draft-first publishing
- avoid live API calls in public samples
- keep Xiaohongshu review human-in-the-loop
- add tests or audit checks when changing the public package

I also added a concrete audit script and CI workflow, which are useful because Copilot works better when a repository has clear boundaries, tests, and a feedback loop.

If I continue this project with Copilot enabled, the next Copilot tasks are obvious: expand tests, add issue templates, strengthen the audit report, and refactor the sample scripts while preserving the safety boundaries.

## What I Learned

The hard part of finishing an agent project is not only making it run. It is making it inspectable.

Agent workflows touch schedules, APIs, credentials, generated content, and user intent. A public repo needs more than screenshots. It needs proof that the dangerous parts are fenced off and the useful parts are easy to understand.

This finish-up pass gave the project that missing layer: tests, CI, auditability, and a clear before/after story.
