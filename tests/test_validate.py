"""Run: python3 tests/test_validate.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import check, gitignored, main  # noqa: E402

GOOD_SKILL = """---
name: good-job
description: Use when a release ticket asks for notes; not for hotfixes.
---
# Good job
## Risk and permitted actions
M. Allowed: read. Not allowed: send.
## Done means
`make check` passes; owner verifies.
## Do not
- Self-approve.
Read `references/rules.md` when unsure.
"""
CONTRACT = ("# Workflow contract: good-job\n- **State:** DRAFT\n- [ ] owner read it\n"
            "## Assumptions (need a yes)\n- see [rules](x)\n## Open questions (not guessed)\n- none\n")
EVAL = "| N01 | No | x | y | No | a |\n| E01 | Yes | x | y | Yes | a |\n| A01 | Yes | x | y | Yes | a |\n| P01 | Yes | x | y | Yes | a |\n"


def make(tmp, skill=GOOD_SKILL, contract=CONTRACT, evaluation=EVAL, refs=True):
    d = Path(tmp) / "good-job"
    d.mkdir()
    (d / "SKILL.md").write_text(skill)
    if contract is not None:
        (d / "CONTRACT.md").write_text(contract)
    if evaluation is not None:
        (d / "EVALUATION.md").write_text(evaluation)
    if refs:
        (d / "references").mkdir()
        (d / "references" / "rules.md").write_text("rules")
    return d


with tempfile.TemporaryDirectory() as t:
    assert check(make(t)) == []

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, skill=GOOD_SKILL.replace("Use when", "Performs the task. Use when")))
    assert any("Use when" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, skill=GOOD_SKILL.replace("good-job", "other-name")))
    assert any("!= directory" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, contract=None, evaluation=None))
    assert "missing CONTRACT.md" in errs and "missing EVALUATION.md" in errs, errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, contract="- **State:** done\n"))
    assert any("State" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, evaluation="| N01 | No | x | y | No | a |\n"))
    assert sum("case row" in e for e in errs) == 3, errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, refs=False))
    assert any("does not exist" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, skill=GOOD_SKILL.replace("references/rules.md", "scripts/[name].py")))
    assert any("placeholder path" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, skill=GOOD_SKILL.replace("## Done means", "## Outcome")))
    assert any("Done means" in e for e in errs), errs

for missing in ("## Risk and permitted actions", "## Do not"):
    with tempfile.TemporaryDirectory() as t:
        errs = check(make(t, skill=GOOD_SKILL.replace(missing, "## Notes")))
        assert any(missing.split()[1] in e and "section" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, skill=GOOD_SKILL.replace("## Risk and permitted actions", "## Risky business")))
    assert any("'## Risk'" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    long = "a" * 65
    errs = check(make(t, skill=GOOD_SKILL.replace("name: good-job", f"name: {long}")))
    assert any("max 64" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    desc = "Use when a release ticket asks for notes; not for hotfixes."
    assert check(make(t, skill=GOOD_SKILL.replace(desc, f'"{desc}"'))) == []

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, skill=GOOD_SKILL.replace("description: Use", "description: >\n  Use")))
    assert any("multi-line" in e for e in errs) and not any("Use when" in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, contract=CONTRACT + "- **Owner:** [person or role]\n"))
    assert errs == ["CONTRACT.md: unfilled placeholder [person or role]"], errs

with tempfile.TemporaryDirectory() as t:
    assert check(make(t, contract=CONTRACT + "- [x] done, `[not a placeholder]`\n")) == []

for heading in ("## Assumptions", "## Open questions"):
    with tempfile.TemporaryDirectory() as t:
        errs = check(make(t, contract=CONTRACT.replace(heading, "## Other")))
        assert any(heading in e for e in errs), errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, evaluation=EVAL.replace("N01", "N10")))
    assert errs == [], errs

with tempfile.TemporaryDirectory() as t:
    skill = GOOD_SKILL + "Run `scripts/<repo>/validate.py` from the repo.\n"
    assert check(make(t, skill=skill)) == []

with tempfile.TemporaryDirectory() as t:
    skill = GOOD_SKILL.replace("`references/rules.md`", "`references/rules.md --section X.Y`")
    assert check(make(t, skill=skill)) == []

with tempfile.TemporaryDirectory() as t:
    skill = GOOD_SKILL + "```bash\necho ${arr[idx]}\n```\nSee [spec][ref].\n\n[ref]: https://example.com\n"
    assert check(make(t, skill=skill)) == []

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, evaluation=EVAL.replace("| Yes | a |\n| A01", "| Yes | [ ] |\n| A01")))
    assert errs == ["EVALUATION.md: E01 has no verifier"], errs

with tempfile.TemporaryDirectory() as t:
    errs = check(make(t, evaluation=EVAL.replace("| No | a |\n| E01", "| No |\n| E01")))
    assert errs == ["EVALUATION.md: N01 has no verifier"], errs

with tempfile.TemporaryDirectory() as t:
    assert check(make(t, evaluation=EVAL.replace("| Yes | a |\n| A01", "| Yes | open (blocks TRIAL) |\n| A01"))) == []

with tempfile.TemporaryDirectory() as t:
    assert check(make(t, skill=GOOD_SKILL + "See [the spec].\n\n[the spec]: https://example.com\n")) == []

with tempfile.TemporaryDirectory() as t:
    assert check(make(t, skill=GOOD_SKILL + "~~~\nx = [name]\n~~~\n")) == []

with tempfile.TemporaryDirectory() as t:
    assert check(make(t, skill="\ufeff\n\n" + GOOD_SKILL)) == []

with tempfile.TemporaryDirectory() as t:  # git runs in the skill's repo, not the caller's cwd
    subprocess.run(["git", "init", "-q", t], check=True)
    (Path(t) / ".gitignore").write_text("good-job/\n")
    assert gitignored(make(t) / "SKILL.md")

with tempfile.TemporaryDirectory() as t:
    d = make(t)
    assert main(["validate.py", str(d)]) == 0 and (d / "runs" / ".gitkeep").exists()
    (d / "CONTRACT.md").unlink()
    assert main(["validate.py", str(d)]) == 1

example = Path(__file__).resolve().parents[1] / "references" / "example" / "website-change-review"
assert check(example) == [], check(example)

print("test_validate: all assertions passed")
