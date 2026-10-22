<p align="center"><img src="assets/logo.png" width="160" alt="playbook logo"></p>

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
| `/playbook capture <job>` | Interview you about a recurring job, agree a contract, then write `.claude/skills/<job>/` with `SKILL.md`, `CONTRACT.md` and `EVALUATION.md` |
| `/playbook harvest <artifact>` | Turn an approved past output into reusable templates or scripts |
| `/playbook run <playbook> <task>` | Execute a playbook and leave an evidence record in `runs/` |
| `/playbook improve <playbook>` | Propose at most three narrow fixes from real run results |

Every captured playbook starts as `DRAFT`. Work is reported as `OBSERVED` (the agent did it), `VERIFIED` (independent checks passed) or `APPROVED` (an owner signed off), never conflated.

## Validate a captured playbook

```bash
python3 scripts/validate.py .claude/skills/<job>
```

Checks the frontmatter (name matches the folder, description is triggers only), that `CONTRACT.md` and `EVALUATION.md` exist with a valid state and the four required case types, that every referenced `references/`, `assets/` or `scripts/` path exists, and creates `runs/` for evidence records. `capture` runs it for you.

## Tested how

Three pressure scenarios, each run by a fresh subagent with and without the skill: capture under time pressure, run with injected instructions in the task data, and an owner pushing to mark an unrun check VERIFIED. Prompts, pass criteria and outcomes are in `tests/scenarios.md`. The validator's self-test is `python3 tests/test_validate.py`.

## Layout

- `SKILL.md` — the skill itself
- `references/FRAMEWORK.md` — the full policy: lanes, risk tiers, gates, verification rules
- `references/example-website-change-review.md` — a worked example
- `templates/` — contract, skill, evaluation and evidence templates
- `scripts/validate.py` — validator for captured playbooks
- `tests/` — validator self-test and the pressure scenarios

## Security

Please report vulnerabilities privately. See [SECURITY.md](SECURITY.md).

## License

MIT
