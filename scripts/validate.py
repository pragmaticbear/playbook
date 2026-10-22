#!/usr/bin/env python3
"""Validate a captured playbook directory. Usage: validate.py <playbook-dir>

Checks SKILL.md frontmatter, required companion files, referenced paths,
and creates runs/ for evidence records. Exit 1 on any error.
"""
import re
import sys
from pathlib import Path

STATES = ("DRAFT", "APPROVED FOR TRIAL", "VERIFIED", "RELEASE APPROVED")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fields[k.strip()] = v.strip()
    fields["_raw"] = m.group(1)
    return fields


def check(d):
    d = Path(d)
    errors = []
    skill = d / "SKILL.md"
    if not skill.exists():
        return [f"missing {skill}"]
    fm = frontmatter(skill.read_text())
    if fm is None:
        errors.append("SKILL.md: no YAML frontmatter block")
    else:
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            errors.append(f"SKILL.md: name {name!r} must be lowercase letters, digits, hyphens")
        if name != d.resolve().name:
            errors.append(f"SKILL.md: name {name!r} != directory {d.resolve().name!r}")
        if not desc.startswith("Use when"):
            errors.append("SKILL.md: description must start with 'Use when' (triggers only)")
        if "[" in desc:
            errors.append("SKILL.md: description still has a [placeholder]")
        if len(fm["_raw"]) > 1024:
            errors.append(f"SKILL.md: frontmatter is {len(fm['_raw'])} chars, max 1024")
    for req in ("CONTRACT.md", "EVALUATION.md"):
        if not (d / req).exists():
            errors.append(f"missing {req}")
    contract = d / "CONTRACT.md"
    if contract.exists():
        m = re.search(r"\*\*State:\*\*\s*(.+)", contract.read_text())
        state = m.group(1).strip() if m else ""
        if state not in STATES:
            errors.append(f"CONTRACT.md: **State:** must be one of {STATES}, got {state!r}")
    evaluation = d / "EVALUATION.md"
    if evaluation.exists():
        text = evaluation.read_text()
        for case in ("N0", "E0", "A0", "P0"):
            if not re.search(rf"^\|\s*{case}\d", text, re.M):
                errors.append(f"EVALUATION.md: no {case}x case row (normal/edge/adversarial/protected-check)")
    body = skill.read_text()
    for heading, why in (("Risk", "risk tier and allowed operations"),
                         ("Done means", "mandatory checks and verifier"),
                         ("Do not", "forbidden actions")):
        if not re.search(rf"^##\s+{heading}", body, re.M | re.I):
            errors.append(f"SKILL.md: no '## {heading}' section ({why})")
    for ref in re.findall(r"`((?:references|assets|scripts)/[^`]+)`", body):
        if "[" in ref:
            errors.append(f"SKILL.md: unfilled placeholder path {ref}")
        elif not (d / ref).exists():
            errors.append(f"SKILL.md: references {ref} which does not exist")
    return errors


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    d = Path(argv[1])
    errors = check(d)
    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        runs = d / "runs"
        runs.mkdir(exist_ok=True)
        (runs / ".gitkeep").touch()
        print(f"OK {d}: valid, runs/ ready")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
