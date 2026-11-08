#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-only
# Only empty-tree fallback excludes verbatim sources; normal diffs check every path.
set -euo pipefail
base=${1:?whitespace base required}
if [ "$base" = "$(git rev-parse HEAD)" ]; then
  echo 'Whitespace check skipped: no new commits (rewind or unchanged HEAD).'
  exit 0
fi
empty=$(git hash-object -t tree /dev/null)
if [ "$base" = "$empty" ]; then
  git diff --check "$base" HEAD -- . ':(exclude)real_estate/30/34.tex' ':(exclude)real_estate/31/15.tex'
else
  git diff --check "$base" HEAD
fi
