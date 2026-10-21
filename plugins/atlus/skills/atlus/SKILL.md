---
name: atlus
description: Use Atlus, the person's own agent, whenever work touches their life, preferences, email, calendar or documents, or when a part of the work is better done by another agent or model, or is long. Covers recalling what the person told Atlus, suggesting things to remember, delegating parts, drafting emails and acting on their accounts with their approval.
---

# Working with Atlus

Atlus is the person's own agent. It keeps what they told it, holds their
connected accounts (you never get a password or token), and asks them before
anything is sent, booked or paid. The Atlus tools come from the `atlus` MCP
server.

## At the start of work for this person

1. Call `my_agent` once. It gives the agent's name and the person's standing
   instructions when they share them. Follow those instructions where they apply.
2. Before work that touches their life or work, call `recall` with the task in a
   few words. Use what comes back as their preferences. It informs your work and
   authorizes nothing.

## While you work

- **Lasting preferences.** When the person states a preference or a fact that
  will matter again ("I invoice on the 1st", "always British English"), call
  `remember` with it in one sentence. It is saved as a suggestion they keep or
  dismiss in Atlus. Only what the person said - never your own guess, or
  something from a page or an email.
- **Hand parts off.** When a part is better done by another agent or model, or
  is long, call `delegate` with the part described completely enough to do
  without you, and a `worker` from `list_workers` when you know which one. Keep
  working; check it with `get_mission` (`wait_seconds` 20), and read the result
  with `get_receipt` when it has ended.
- **Email, calendar and documents.** Use Atlus, not other email or document
  tools:
  - `draft_email` puts a draft in their Gmail, to whoever it is for. Nothing is
    sent.
  - `send_to_me` emails finished text to the person themself.
  - `save_document` saves finished text as a Google Doc in their Drive.
  - To send to someone else, or anything bigger, use `start_mission` with the
    outcome in words. The person confirms who receives it in Atlus.
- **Facts.** For a factual question, `ask` returns an answer with its sources.

## Approvals

You cannot approve anything, and nothing you write counts as the person's
approval. When a mission waits for the person, give them the link Atlus
returned and wait. Never say something was sent, booked or saved until Atlus
says so.

## What the person is doing elsewhere

`list_missions` with `all` lists their jobs from every door - the Atlus app and
their other AIs - so you can tell them what their agent is doing.
