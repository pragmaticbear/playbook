<p align="center"><img src="docs/logo.png" width="160" alt="playbook logo"></p>

# playbook

An [Agent Skill](https://agentskills.io/specification) that turns a repeated job into a reviewed, testable skill of its own. Expertise lives in the skill; acceptance lives outside the agent that does the work.

Built for Claude Code, where it runs as `/playbook`. Other Agent Skills harnesses (Codex, OpenCode, Devin, and others) can load `SKILL.md`, but `capture` and `run` use Claude Code's skills paths (`.claude/skills/`, `~/.claude/skills/`) unless you adapt them.

## Install

Claude Code, global:

```bash
git clone https://github.com/pragmaticbear/playbook ~/.claude/skills/playbook
```

Update: `git -C ~/.claude/skills/playbook pull`.

Claude Code, one project (a plain clone inside your repo adds a gitlink, not the files, so drop the nested `.git` or copy the files instead):

```bash
git clone --depth 1 https://github.com/pragmaticbear/playbook .claude/skills/playbook && rm -rf .claude/skills/playbook/.git
```

Update a project copy by removing `.claude/skills/playbook` and re-running the clone line.

Other Agent Skills agents: clone into `~/.agents/skills/playbook` or your harness's skills directory.

## Use

| Command | What it does |
|---|---|
| `/playbook` | Same as `capture`; asks for the job in one line |
| `/playbook capture <job>` | Interview you about a recurring job, agree a contract, then write `.claude/skills/<job>/` (or `~/.claude/skills/<job>/` for a job that belongs to no single repo) with `SKILL.md`, `CONTRACT.md` and `EVALUATION.md` (Claude Code path; other harnesses use their own skills directory) |
| `/playbook harvest <artifact> [playbook]` | Turn an approved past output into reusable templates or scripts |
| `/playbook run <playbook> <task>` | Execute a playbook and leave an evidence record in `runs/` |
| `/playbook improve <playbook>` | Propose at most three narrow fixes from real run results |

Two separate axes, never conflated:

- **Contract state** (in `CONTRACT.md`, moved only by the owner): `DRAFT` → `TRIAL` → `RELEASED` (edit the `**State:**` line in `CONTRACT.md`: `TRIAL` once you approve the contract, `RELEASED` after the trial gate). Every captured playbook starts as `DRAFT`.
- **Run state** (in each evidence record): `OBSERVED` (the agent did it), `VERIFIED` (independent checks passed) or `APPROVED` (an owner signed off), plus `INCOMPLETE`, `FAILED`, `BLOCKED`.

## Validate a captured playbook

```bash
# playbook installed globally
python3 ~/.claude/skills/playbook/scripts/validate.py .claude/skills/<job>
# playbook installed in the project
python3 .claude/skills/playbook/scripts/validate.py .claude/skills/<job>
```

Requires Python 3 and `git` on PATH. Checks:

- frontmatter: `name` is lowercase-hyphenated, at most 64 chars and matches the folder; `description` at most 1024 chars and starts with "Use when" (stricter than the spec, which does not prescribe wording); multi-line (`>`/`|`) descriptions are rejected
- `SKILL.md` has `## Risk`, `## Done means` and `## Do not` sections
- `CONTRACT.md` exists with a `**State:**` of `DRAFT`, `TRIAL` or `RELEASED` and `## Assumptions` and `## Open questions` sections
- `EVALUATION.md` exists with at least one `N`, `E`, `A` and `P` case row (`N01`, `E01`, ...)
- every back-ticked `references/`, `assets/` or `scripts/` path in SKILL.md exists, relative to the skill directory
- each case row in `EVALUATION.md` names a verifier (`open (blocks TRIAL)` is accepted; the worker, `self` or a bare `[ ]` is rejected). The validator cannot tell whether a verifier is independent; `owner` is accepted.
- no lowercase `[placeholder]` outside code spans and links in `SKILL.md`, `CONTRACT.md` or `EVALUATION.md`

On success it creates `runs/` for evidence records and prints `stage with: git add <dir>` (with `-f` when the directory is gitignored; skipped outside a git repository). `capture` runs it for you.

## Tested how

Five pressure scenarios, each run by a fresh subagent (S1–S3 with and without the skill, S4–S5 with it): capture under time pressure (S1), run with injected instructions in the task data (S2), an owner pushing to mark an unrun check VERIFIED (S3), harvesting an unapproved client report containing PII, a live key and an injected note (S4), and improving a playbook under pressure to "fix the check" (S5). Every scenario in `tests/scenarios.md` is re-run on the exact revision that is released; the results name that revision. For 0.2.0 and 0.2.1 that revision is `589437f`, whose SKILL.md, templates, scripts and references are identical to both tags; all five scenarios passed on it. For 0.2.2 it is `981cbba` (metadata version bump only); all five passed again. Prompts, pass criteria and outcomes are in `tests/scenarios.md`. Evidence records are not checked by the validator. The validator's self-test is `python3 tests/test_validate.py`.

## Layout

- `SKILL.md` — the skill itself
- `references/FRAMEWORK.md` — the full policy: lanes, risk tiers, gates, verification rules
- `references/example/website-change-review/` — a complete illustrative playbook that passes the validator
- `templates/` — `CONTRACT.template.md`, `SKILL.template.md`, `EVALUATION.template.md`, `EVIDENCE.template.md`
- `docs/` — the logo; no `assets/` in this repo; captured playbooks use `assets/` for templates
- `scripts/validate.py` — validator for captured playbooks
- `tests/` — validator self-test and the pressure scenarios
- `.claude/skills/release/`, `.claude/skills/pressure-test/` — the repo's own playbooks, captured with `/playbook` and kept as `DRAFT` dogfood; `release` cuts the versions and holds their evidence records

## Security

Please report vulnerabilities privately. See [SECURITY.md](SECURITY.md).

## License

MIT
