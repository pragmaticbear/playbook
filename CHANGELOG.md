# Changelog

## 0.1.1 — 2026-10-22

Improve cycle from the first run records (`tests/scenarios.md`, "Improve cycle 1").

- Validator requires `## Risk`, `## Done means` and `## Do not` sections in a captured skill.
- Contract template no longer demands a git revision before the first commit.
- Red flag added: "just write it" approves a DRAFT, not the contract's assumptions.

## 0.1.0 — 2026-10-22

First public release.

- Four modes: capture, harvest, run, improve.
- `scripts/validate.py` checks a captured playbook (frontmatter, companion files, referenced paths) and scaffolds `runs/`.
- Pressure-tested with subagents; scenarios and outcomes in `tests/scenarios.md`.
