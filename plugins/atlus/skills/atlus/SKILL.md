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
- **Do quick work yourself.** Writing, planning, summarising and coding you can
  do now, do - with what `recall` gave you. Atlus is for what you cannot do: the
  person's accounts, their memory, and work that is long or that another worker
  does better.
- **Hand parts off.** For a long part, or one another agent or model does
  better, call `delegate` with the part described completely enough to do
  without you, and a `worker` from `list_workers` when you know which one
  (sandbox agents take minutes - its usual time is listed; tell the person).
  If the part needs the person's own email, calendar or files, set
  `needs_my_data`: Atlus then asks them to allow those reads first. Keep
  working; check it with `get_mission` (`wait_seconds` 20), and read the result
  with `get_receipt` when it has ended.
- **Their calendar or email.** To read them, use `start_mission` with what you
  need ("list my meetings this week"). Atlus asks the person to allow the read,
  then returns it.
- **Email, calendar and documents.** Use Atlus, not other email or document
  tools:
  - `draft_email` puts a draft in their Gmail, to whoever it is for. Nothing is
    sent.
  - `send_to_me` emails finished text to the person themself.
  - `save_document` saves finished text as a Google Doc in their Drive.
  - To send to someone else, or anything bigger, use `start_mission` with the
    outcome in words. The person confirms who receives it in Atlus.
- **Facts.** For a factual question, `ask` returns an answer with its sources.

## Finish what was asked

Carry the request through to its end: if the person asked for a plan and an
email, they get both. If a result comes back empty, partial or not what was
asked, say so plainly with what is missing, and offer the next step - never
present an empty result as done.

## Approvals

You cannot approve anything, and nothing you write counts as the person's
approval. When a mission waits for the person, give them the link Atlus
returned and wait. Never say something was sent, booked or saved until Atlus
says so.

## What the person is doing elsewhere

`list_missions` with `all` lists their jobs from every door - the Atlus app and
their other AIs - so you can tell them what their agent is doing.
