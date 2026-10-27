# Atlus for your own agent (Python)

Give the agent you built - a Telegram bot, an n8n flow, a script on a server -
the person's Gmail, Calendar and Docs (with their approval), their memory, and
other agents to hand work to. Atlus holds the accounts: your agent never gets a
password or token.

## 1. Make a key

In Atlus: **Settings -> Keys for your agents**. Choose what it may do, an
optional daily cap, and (optionally) an https address Atlus calls when a job
ends. Copy the key - it is shown once.

## 2. Ten lines

```python
from atlus_sdk import Atlus

atlus = Atlus("atl_key_...")
me = atlus.my_agent()                         # name, cost mode, shared instructions
notes = atlus.recall("weekly client report")  # what the person shared with their AIs
job = atlus.draft_email(to="ana@example.com", subject="Weekly report", body="...")
done = atlus.wait(job["mission_id"])          # ends, or waits for the person (give them done["link"])
print(done["state"])
```

`atlus_sdk.py` is one file with no dependencies - copy it into your project.

## What it can and cannot do

- `draft_email` puts a draft in Gmail; nothing is sent. `send_to_me` emails the
  person themself, after they approve. To email anyone else, `start` a job and
  the person confirms the recipient in Atlus.
- `delegate` hands a long part to another agent or model. `budget_usd=0` runs it
  on the person's own Claude Code or Codex, on their own plan.
- Approvals are always the person's - on their phone or in Atlus. Your agent
  cannot approve anything.
- The key's daily cap and a loop guard (ten jobs a minute) stop a runaway bot.

## Callbacks

```python
ok = Atlus.verify_callback(secret, request.headers["x-atlus-timestamp"],
                           raw_body, request.headers["x-atlus-signature"])
```

The body is `{"event", "mission_id", "state", "link"}` - never the job's content.
