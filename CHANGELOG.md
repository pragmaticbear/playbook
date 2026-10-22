# Changelog

## 0.2.0 — 2026-10-22

Fixes from an independent review and two real capture runs.

- Validator: per-field spec limits (name 64, description 1024) instead of a whole-frontmatter cap; quoted values accepted; multi-line descriptions reported as unsupported; exact-word section headings; no crash without git.
- Validator: unfilled `[placeholder]` detection in `SKILL.md`, `CONTRACT.md` and `EVALUATION.md`; `CONTRACT.md` needs Assumptions and Open questions sections; `N10`-style case rows count; referenced paths ignore arguments and `<pointer>` paths.
- Contract states renamed to `DRAFT`, `TRIAL`, `RELEASED`, a separate axis from run states; FRAMEWORK maps the gates to them.
- Example playbook at `references/example/website-change-review/` replaces the prose example.
- Description adds SOP, runbook, checklist, recurring task and "automate this process"; capture steps tightened from real runs (absent user, staging, held-out cases, verifier, assumed checks).
- Logo moved to `docs/` (`assets/` holds skill assets by Agent Skills spec convention; it is not reserved).
- README corrections: validator path, requirements and checks, harness-specific write path, both state axes, untested modes.
- harvest: optional target playbook, owner-only acceptance, report leaked secrets and injected notes, `{{name}}` placeholders, stop at the diff when the user is away; S4 passed on both the pre-rewrite and the rewritten harvest text.
- Run mode: a check that could not execute is `INCOMPLETE`, one that ran and failed is `FAILED`; environment repair only when the playbook lists it; run id defined; skipped steps logged as deviations; a self-declared owner recorded as unconfirmed. Contract gains an evidence snapshot field and the evidence record a waivers field. Validator ignores fenced code and reference-style links and flags case rows with no verifier. Example evidence record added under `references/example/website-change-review/runs/`.
- Third review pass: validator reads the verifier from column 6, accepts `open (blocks TRIAL)`, skips `~~~` fences and shortcut reference links, and prints the `git add` command; run mode states the contract state and keeps `DRAFT`/`TRIAL` M/H runs in a sandbox; lane overrides, unattended sends and history-only examples moved from SKILL.md to FRAMEWORK; skill template keeps its guidance in comments; example contract records its playbook version.
- Fourth review pass: run mode defines the sandbox rule (owner approval does not override `DRAFT`/`TRIAL`), treats a missing contract as `DRAFT`, makes an environment error `INCOMPLETE` regardless of exit code, and never ticks `APPROVED` from an unverified owner; red flags for authoritative-looking ticket notes and "the owner said go"; improve treats "the test is wrong" as a proposal to the owner; harvest validates a scratch copy; FRAMEWORK defines a sandbox and each contract state; contract template renamed `CONTRACT.template.md`; evidence template gains contract state, deviations and redaction fields; validator rejects the worker as verifier, keeps a symlinked directory's name and ignores capitalised brackets such as `[RFC 2119]`; example records its playbook version as `6441387` (first commit; edited since).

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
