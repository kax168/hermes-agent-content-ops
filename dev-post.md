---
title: I Built a Hermes Agent That Runs a Two-Post-a-Day AI Media Workflow
published: false
tags: hermesagentchallenge, devchallenge, agents
---

*This is a submission for the [Hermes Agent Challenge](https://dev.to/challenges/hermes-agent-2026-05-15).*

## What I Built

I built a Hermes-powered content operations system for a Chinese WeChat Official Account focused on AI tools, cross-border monetization, content going global, and practical AI workflows.

The goal was not to make a generic chatbot. I wanted Hermes to do the unglamorous operational work behind a real media account:

- research current topics before writing;
- pick a high-click-through topic that fits the account strategy;
- generate a polished WeChat article;
- create a theme-matched cover and visual structure;
- format everything as WeChat-safe HTML;
- upload the result into the WeChat Official Account draft box;
- run the whole thing twice per day on a schedule.

The account publishes one article at 7:00 AM and another at 6:00 PM. The morning slot favors practical tutorials and tool/workflow guides. The evening slot favors trend analysis, controversy, reviews, and case breakdowns.

I also added a second operational workflow: a daily Xiaohongshu research queue for pet-supplies affiliate videos. It prepares search targets and review files, but intentionally keeps the final approval human-in-the-loop because the acceptance criteria require audio and on-screen text judgment.

## Demo

The WeChat pipeline produces a complete local article package for each run:

```text
~/.hermes/wechat-mp/YYYY-MM-DD/morning/
  article.md
  article.html
  article.json
  topic_research.md
  image_plan.md
  cover.png
  cover_prompt.txt
```

The draft creation step uses the official WeChat API. A run only counts as successful if the API returns a real draft media ID. Otherwise, the generated package stays on disk for inspection and Hermes reports the failure.

The Xiaohongshu workflow produces a daily review queue:

```text
~/.hermes/xhs-pet-supplies-videos/YYYY-MM-DD/
  review_queue.txt
  approved_links_template.txt
```

Approved video links are appended to:

```text
~/.hermes/xhs-pet-supplies-videos/links.txt
```

The important design choice: Hermes automates the repeatable operational work, but it does not pretend to verify things it cannot safely verify. For videos, "no Chinese narration" and "no more than 10 Chinese characters on screen" need visual/audio review, so the system creates the queue and saves only manually approved links.

## Code

Repository: [github.com/kax168/hermes-agent-content-ops](https://github.com/kax168/hermes-agent-content-ops)

The private installation contains:

- a Hermes skill for WeChat Official Account operations;
- deterministic cron scripts for reliable scheduled execution;
- WeChat Official Account API integration;
- a content strategy file persisted under Hermes home;
- Xiaohongshu review-queue scripts;
- environment-based model/provider configuration.

Secrets are stored outside the repo in `~/.hermes/.env` and are never printed or committed.

### My Tech Stack

- Hermes Agent
- Hermes cron scheduler
- Python
- WeChat Official Account API
- Google News RSS and Hacker News search for topic discovery
- Configurable model provider for article generation
- WeChat-safe inline HTML/CSS
- Local PNG cover generation as a reliable fallback

## How I Used Hermes Agent

Hermes is the operating layer of the project, not just a model wrapper.

### 1. Persistent skills

I created a local Hermes skill called `wechat-official-account-operator`. It contains the account strategy, content rules, visual requirements, API safety defaults, output schema, and success criteria.

That mattered because the account has a strong editorial position:

- AI tool tutorials and reviews;
- global AI product news;
- AI agents and automation;
- cross-border monetization;
- GEO, AdSense, affiliate, independent sites, and content export;
- legal "freebie" and cost-saving AI tool tactics.

The skill keeps these rules close to the agent so each run is not starting from a blank prompt.

### 2. Scheduled autonomous work

Hermes cron runs two jobs every day:

- `0 7 * * *` for the morning article;
- `0 18 * * *` for the evening article.

This is where Hermes felt different from a normal chat interface. The system is not waiting for a human to ask, "Please write a post now." It wakes up, collects context, generates artifacts, calls an API, and leaves a concrete result.

### 3. Tool use and API execution

The WeChat pipeline performs several real steps:

1. Collect current topic candidates from web/news/community sources.
2. Generate a topic-research file with candidate topics, source links, heat signals, and final rationale.
3. Generate an article with a strong hook, practical value, risks, and CTA.
4. Render a polished WeChat-safe HTML layout instead of dumping plain Markdown.
5. Create a local cover image and visual plan.
6. Write a machine-readable `article.json`.
7. Upload the cover and article to WeChat through the official API.
8. Report the run status.

I added a strict "no simulation" rule: the run is not successful unless the local files exist and the WeChat API returns a real draft result.

### 4. Practical reliability over agent theater

One of the more interesting lessons was that a fully autonomous large-prompt agent run was not the most reliable way to handle scheduled publishing. Some agentic runs timed out or got stuck on browser/model calls.

So I changed the architecture: Hermes still owns the schedule, skills, memory, and operational workflow, but the daily execution path uses deterministic Python scripts for the fragile parts.

That hybrid design made the system more useful:

- the agent defines and evolves the workflow;
- scripts perform predictable API/file work;
- Hermes cron keeps it alive on a schedule;
- failures leave inspectable artifacts instead of vague chat logs.

### 5. Human-in-the-loop where judgment is required

The Xiaohongshu workflow is deliberately semi-automatic. It searches for pet-supplies affiliate video candidates and prepares a review queue, but final saving requires manual confirmation.

That is not a limitation I wanted to hide. It is a product decision. If the rule says "no Chinese narration" and "almost no Chinese on-screen text," then silently adding links without checking would produce bad data. Hermes is still useful because it removes the repetitive search/setup work while preserving the judgment step.

## What Makes This Useful

This project is small, but it is real. It has all the annoying parts of actual automation:

- credentials and API permissions;
- scheduled jobs;
- retries and timeouts;
- local artifacts for debugging;
- editorial constraints;
- platform-specific HTML limitations;
- safe publishing defaults;
- human review boundaries.

Hermes Agent was a good fit because the workflow needed memory, scheduling, tools, and persistence more than it needed a prettier chat response.

The result is an agentic system that can operate a narrow but real content pipeline: from topic discovery to WeChat draft creation, twice a day.

## What I Would Improve Next

I would like to add:

- a visual dashboard for scheduled run status;
- screenshot-based QA for WeChat article layout before upload;
- safer browser automation for Xiaohongshu candidate collection;
- automatic source-quality scoring;
- multi-platform repurposing from one article package to X/Twitter, LinkedIn, and short-video scripts.

The biggest takeaway: the best agent projects are often not magic demos. They are workflows where the agent keeps showing up, on schedule, doing the boring parts correctly.
