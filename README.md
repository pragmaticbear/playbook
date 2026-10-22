# playbook

An [Agent Skill](https://agentskills.io/specification) that turns a repeated job into a reviewed, testable skill of its own. Expertise lives in the skill; acceptance lives outside the agent that does the work.

Works with Claude Code as `/playbook`, and with any agent that loads `SKILL.md` from a skills directory (Codex, OpenCode, Devin, and others).

## Install

Claude Code, global:

```bash
git clone https://github.com/OWNER/playbook ~/.claude/skills/playbook
```

Claude Code, one project:

```bash
git clone https://github.com/OWNER/playbook .claude/skills/playbook
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

## Layout

- `SKILL.md` — the skill itself
- `references/FRAMEWORK.md` — the full policy: lanes, risk tiers, gates, verification rules
- `references/example-website-change-review.md` — a worked example
- `templates/` — contract, skill, evaluation and evidence templates

## License

MIT
