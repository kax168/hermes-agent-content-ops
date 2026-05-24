# Event-Aware Watch Layer

Community feedback pointed out that a pure cron workflow is only the baseline.
The better operating model is:

```text
cron schedule + watch layer + human-safe retry rules
```

Cron still owns the 07:00 and 18:00 publishing rhythm. The watch layer handles
events that should wake Hermes before or between those slots.

## Events

The public sample watches for local package signals:

- `topic_research.md`: source research changed, so the agent should re-check
  freshness and angle.
- `human_review.approved`: a human approved a queued item, so the agent may
  continue packaging.
- `wechat_api.failed`: a draft upload failed, so the agent should wake for a
  safe repair or retry.
- `article.md`, `article.html`, `article.json`: draft artifacts changed, so the
  package can be validated without necessarily waking the whole agent.

## Run

```bash
python3 scripts/watch_content_events.py path/to/content-package --out watch-report.json
```

The command prints a decision like:

```json
{
  "wakeAgent": true,
  "nextAction": "wake_agent",
  "events": []
}
```

This is intentionally conservative. It does not publish content. It only
decides whether the agent should wake and what kind of safe handoff should
happen next.

