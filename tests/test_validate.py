"""Run: python3 tests/test_validate.py"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import check  # noqa: E402

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
CONTRACT = "# Workflow contract: good-job\n- **State:** DRAFT\n"
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

print("test_validate: all assertions passed")
