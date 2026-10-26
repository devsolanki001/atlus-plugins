---
description: Hand a part of the work to another agent or model through Atlus
argument-hint: "[worker] <the part, in words>"
---

Hand this part of the work to another worker through Atlus: $ARGUMENTS

1. If the first word looks like a worker id, check it against `list_workers`
   and use it as `worker`; otherwise let Atlus choose.
2. Write the part out completely enough to be done without you - what to do,
   the files or context it needs, and what to hand back.
3. Call `delegate` with that `job` (and the `worker`).
4. Tell the person which worker has it and the link Atlus returned, then keep
   working. Follow it with `job` (`wait_seconds` 20); once it has ended, `job`
   returns the result - use it.
