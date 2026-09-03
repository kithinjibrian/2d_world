# docs/incidents — Post-mortem reports

Written on demand, after something broke.

## Structure

1. Executive Summary — what broke, when, for how long, impact (max 100 words; **write it last**)
2. Timeline — chronological events with timestamps
3. Root Cause — the specific technical reason, not a symptom
4. Contributing Factors — what made this possible or worse
5. Resolution — what was done to restore service
6. Action Items — numbered, each with an owner and a due date
7. Lessons Learned — what the system or team will do differently

Every action item that is "the AI should have known X" becomes a rule in CLAUDE.md in the same
session. An incident that changes no rule will recur.

Filename: `YYYY-MM-DD-{slug}.md`
