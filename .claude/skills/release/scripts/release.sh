#!/usr/bin/env bash
# Tag, push and publish vX.Y.Z of this repo from its CHANGELOG.md section.
# Usage: release.sh [--dry-run] X.Y.Z "tag message"
# Run without --dry-run only after the owner has said yes to the dry-run output.
set -euo pipefail
dry=; [ "${1:-}" = --dry-run ] && { dry=1; shift; }
ver=${1:?version X.Y.Z}; msg=${2:?tag message}; tag="v$ver"
cd "$(git rev-parse --show-toplevel)"
fail() { echo "ERROR $*" >&2; exit 1; }

[ "$(git rev-parse --abbrev-ref HEAD)" = main ] || fail "not on main"
[ -z "$(git status --porcelain)" ] || fail "working tree not clean"
git fetch -q origin
[ -z "$(git log --oneline origin/main..HEAD)" ] || fail "unpushed commits on main; push first"
git rev-parse -q --verify "refs/tags/$tag" >/dev/null && fail "tag $tag exists locally"
[ -z "$(git ls-remote --tags origin "$tag")" ] || fail "tag $tag exists on origin"
notes=$(awk -v v="$ver" '/^## /{p=($2==v)} p' CHANGELOG.md)
[ -n "$notes" ] || fail "no '## $ver' section in CHANGELOG.md"
python3 tests/test_validate.py >/dev/null || fail "tests/test_validate.py failed"  # assumed check, CONTRACT.md A4

echo "== $tag on $(git rev-parse --short HEAD); tag message: $msg"
echo "== release notes (CHANGELOG.md section, CONTRACT.md A2):"; echo "$notes"
if [ -n "$dry" ]; then
  echo "== dry run; would run: git tag -a $tag -m ...; git push origin $tag; gh release create $tag --title $tag --target main --notes ..."
  exit 0
fi
git tag -a "$tag" -m "$msg"
git push origin "$tag"
gh release create "$tag" --title "$tag" --target main --notes "$notes"
gh release view "$tag" --json url,tagName,isDraft,isPrerelease
