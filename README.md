# Atlus for Claude Code

Your own agent, inside Claude Code. Atlus knows what you told it, hands parts of
your work to the best agent or model (Codex, Hermes, your own Claude Code on
your computer), and acts on your email, calendar and documents only after you
approve.

## Install

In Claude Code:

```
/plugin marketplace add devsolanki001/atlus-plugins
/plugin install atlus@atlus
```

The first time Claude Code uses Atlus, it opens Atlus's sign-in. You choose
what Claude Code may do; you can disconnect it any time in Atlus under
Settings.

## What you get

- **It knows you.** Claude Code asks Atlus what you told it - your preferences,
  your work, the people you work with (names only; addresses stay in Atlus).
- **It remembers with your yes.** When you state a lasting preference, Claude
  Code suggests it to Atlus. Nothing is used until you keep it.
- **It hands work off.** `/atlus:delegate codex_device write the tests for parser.py`
  gives a part to another worker and keeps going.
- **It acts for you, safely.** Drafts go into your Gmail; sending, booking and
  paying always ask you first, in Atlus or on your phone. Claude Code never
  gets your passwords or tokens.
- **One view.** `/atlus:jobs` shows what your agent is doing from every door.

## What this plugin contains

A connection to `https://vonit.si/mcp`, one skill telling Claude Code when to
use Atlus, and two commands. No keys, no code that runs on your computer.

## For an agent you built yourself

[`sdk/python`](sdk/python): a one-file Python SDK - a key from Atlus, ten lines,
the person's accounts, memory and other agents, with their approval.
