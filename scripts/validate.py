#!/usr/bin/env python3
"""Validate a captured playbook directory. Usage: validate.py <playbook-dir>

Checks SKILL.md frontmatter, required companion files, referenced paths,
unfilled placeholders and named verifiers, creates runs/ for evidence
records and prints how to stage the directory. Exit 1 on any error.
"""
import re
import subprocess
import sys
from pathlib import Path

STATES = ("DRAFT", "TRIAL", "RELEASED")
# [Something] that is not an inline or reference-style link, a link definition
# or an [x] checkbox; template placeholders start lowercase, so [RFC 2119] passes
PLACEHOLDER = re.compile(r"(?<!\])\[(?![xX]\])([a-z][^\]\n]*)\](?!\(|\[|:)")
NO_VERIFIER = {"", "[ ]", "tbd", "this agent", "the worker", "worker", "self", "agent"}


def frontmatter(text):
    m = re.match(r"\ufeff?\s*---\n(.*?)\n---\n", text, re.S)  # BOM, blank lines
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line[0].isspace():
            continue  # nested keys (e.g. metadata.version) are not checked
        k, _, v = line.partition(":")
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        fields[k.strip()] = v
    return fields


def placeholders(path):
    text = re.sub(r"```.*?```|~~~.*?~~~", "", path.read_text(), flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    defined = {m.lower() for m in re.findall(r"^\[([^\]]+)\]:", text, re.M)}  # [text] shortcut links
    return [f"{path.name}: unfilled placeholder [{m}]" for m in PLACEHOLDER.findall(text)
            if m.lower() not in defined]


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
        if len(name) > 64:
            errors.append(f"SKILL.md: name is {len(name)} chars, max 64")
        if name != d.absolute().name:  # not resolve(): a symlinked dir keeps the link's name
            errors.append(f"SKILL.md: name {name!r} != directory {d.absolute().name!r}")
        if re.fullmatch(r"[>|][-+]?", desc):
            errors.append("SKILL.md: multi-line descriptions are not supported by this validator")
        elif not desc.startswith("Use when"):
            errors.append("SKILL.md: description must start with 'Use when' (triggers only)")
        if len(desc) > 1024:
            errors.append(f"SKILL.md: description is {len(desc)} chars, max 1024")
    for req in ("CONTRACT.md", "EVALUATION.md"):
        if not (d / req).exists():
            errors.append(f"missing {req}")
    contract = d / "CONTRACT.md"
    if contract.exists():
        text = contract.read_text()
        m = re.search(r"\*\*State:\*\*\s*(.+)", text)
        state = m.group(1).strip() if m else ""
        if state not in STATES:
            errors.append(f"CONTRACT.md: **State:** must be one of {STATES}, got {state!r}")
        for heading in ("Assumptions", "Open questions"):
            if not re.search(rf"^##\s+{heading}(?!\w)", text, re.M | re.I):
                errors.append(f"CONTRACT.md: no '## {heading}' section")
    evaluation = d / "EVALUATION.md"
    if evaluation.exists():
        text = evaluation.read_text()
        for case in "NEAP":
            if not re.search(rf"^\|\s*{case}\d+", text, re.M):
                errors.append(f"EVALUATION.md: no {case}01-style case row (normal/edge/adversarial/protected-check; rows must start with `|`)")
        for row in re.findall(r"^\|\s*[NEAP]\d+.*$", text, re.M):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            # "open (blocks TRIAL)" is accepted; the template hint "[ ] or open (...)" is not
            if len(cells) < 6 or cells[5].lower() in NO_VERIFIER or cells[5].startswith("[ ]"):
                errors.append(f"EVALUATION.md: {cells[0]} has no verifier")
    for f in (skill, contract, evaluation):
        if f.exists():
            errors += placeholders(f)
    body = skill.read_text()
    for heading, why in (("Risk", "risk tier and allowed operations"),
                         ("Done means", "mandatory checks and verifier"),
                         ("Do not", "forbidden actions")):
        if not re.search(rf"^##\s+{heading}(?!\w)", body, re.M | re.I):
            errors.append(f"SKILL.md: no '## {heading}' section ({why})")
    for span in re.findall(r"`((?:references|assets|scripts)/[^`]+)`", body):
        ref = span.split()[0]  # `scripts/x.sh --flag` checks scripts/x.sh
        if "<" in ref or ">" in ref:
            continue  # a pointer such as <repo>/scripts/x.py, not a file here
        if "[" in ref:
            errors.append(f"SKILL.md: unfilled placeholder path {ref}")
        elif not (d / ref).exists():  # relative to the skill directory
            errors.append(f"SKILL.md: references {ref} which does not exist")
    return errors


def gitignored(path):
    """True/False, or None when the path is not inside a git repository."""
    path = path.resolve()
    try:  # run inside the skill's repo, wherever the validator is called from
        code = subprocess.run(["git", "check-ignore", "-q", str(path)],
                              capture_output=True, cwd=path.parent.parent).returncode
    except FileNotFoundError:  # no git on PATH
        return False
    return None if code == 128 else code == 0


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
        if not runs.exists():
            runs.mkdir()
            print(f"created {runs}/")
        (runs / ".gitkeep").touch()
        print(f"OK {d}: valid, runs/ ready")
        ignored = gitignored(d / "SKILL.md")
        if ignored is not None:  # None: not in a git repository, nothing to stage
            print(f"stage with: git add {'-f ' if ignored else ''}{d}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
