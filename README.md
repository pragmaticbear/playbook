<p align="center"><img src="docs/logo.png" width="160" alt="playbook logo"></p>

# playbook

An [Agent Skill](https://agentskills.io/specification) that turns a repeated job into a reviewed, testable skill of its own. Expertise lives in the skill; acceptance lives outside the agent that does the work.

Works with Claude Code as `/playbook`, and with any agent that loads `SKILL.md` from a skills directory (Codex, OpenCode, Devin, and others).

## Install

Claude Code, global:

```bash
git clone https://github.com/pragmaticbear/playbook ~/.claude/skills/playbook
```

Claude Code, one project:

```bash
git clone https://github.com/pragmaticbear/playbook .claude/skills/playbook
```

Other Agent Skills agents: clone into `~/.agents/skills/playbook` or your harness's skills directory.

## Use

| Command | What it does |
|---|---|
| `/playbook capture <job>` | Interview you about a recurring job, agree a contract, then write `.claude/skills/<job>/` with `SKILL.md`, `CONTRACT.md` and `EVALUATION.md` (Claude Code path; other harnesses use their own skills directory) |
| `/playbook harvest <artifact> [playbook]` | Turn an approved past output into reusable templates or scripts |
| `/playbook run <playbook> <task>` | Execute a playbook and leave an evidence record in `runs/` |
| `/playbook improve <playbook>` | Propose at most three narrow fixes from real run results |

Two separate axes, never conflated:

- **Contract state** (in `CONTRACT.md`, moved only by the owner): `DRAFT` → `TRIAL` → `RELEASED`. Every captured playbook starts as `DRAFT`.
- **Run state** (in each evidence record): `OBSERVED` (the agent did it), `VERIFIED` (independent checks passed) or `APPROVED` (an owner signed off), plus `INCOMPLETE`, `FAILED`, `BLOCKED`.

## Validate a captured playbook

```bash
python3 ~/.claude/skills/playbook/scripts/validate.py .claude/skills/<job>
```

Requires Python 3 and `git` on PATH. Checks:

- frontmatter: `name` is lowercase-hyphenated, at most 64 chars and matches the folder; `description` at most 1024 chars and starts with "Use when"
- `SKILL.md` has `## Risk`, `## Done means` and `## Do not` sections
- `CONTRACT.md` exists with a `**State:**` of `DRAFT`, `TRIAL` or `RELEASED` and `## Assumptions` and `## Open questions` sections
- `EVALUATION.md` exists with at least one `N`, `E`, `A` and `P` case row (`N01`, `E01`, ...)
- every referenced `references/`, `assets/` or `scripts/` path exists, relative to the skill directory
- no unfilled `[placeholder]` left in `SKILL.md`, `CONTRACT.md` or `EVALUATION.md`

On success it creates `runs/` for evidence records and warns if the directory is gitignored. `capture` runs it for you.

## Tested how

Four pressure scenarios, each run by a fresh subagent with and without the skill: capture under time pressure, run with injected instructions in the task data, an owner pushing to mark an unrun check VERIFIED, and harvesting an unapproved client report containing PII, a live key and an injected note (S4, passed). Prompts, pass criteria and outcomes for S1–S3 are in `tests/scenarios.md`. `improve` has not been scenario-tested yet. The validator's self-test is `python3 tests/test_validate.py`.

## Layout

- `SKILL.md` — the skill itself
- `references/FRAMEWORK.md` — the full policy: lanes, risk tiers, gates, verification rules
- `references/example/website-change-review/` — a complete captured playbook that passes the validator
- `templates/` — contract, skill, evaluation and evidence templates
- `scripts/validate.py` — validator for captured playbooks
- `tests/` — validator self-test and the pressure scenarios

## Security

Please report vulnerabilities privately. See [SECURITY.md](SECURITY.md).

## License

MIT
