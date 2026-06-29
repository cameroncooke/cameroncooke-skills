#!/usr/bin/env python3
"""Report the effective PR state without mutating the git index."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        env=GIT_ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def git_stdout(args: list[str], *, check: bool = True) -> str:
    return git(args, check=check).stdout


def repo_root() -> Path:
    return Path(git_stdout(["rev-parse", "--show-toplevel"]).strip())


def base_point(base: str) -> str:
    result = git(["merge-base", "HEAD", base], check=False)
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else base


def split_lines(output: str) -> list[str]:
    return [line for line in output.splitlines() if line]


def line_count(path: Path) -> int | None:
    data = path.read_bytes()
    if b"\0" in data[:8192]:
        return None
    return len(data.decode("utf-8", errors="replace").splitlines())


def tracked_numstat(point: str) -> list[dict[str, Any]]:
    rows = []
    for line in split_lines(git_stdout(["diff", "--numstat", point])):
        additions, deletions, path = line.split("\t", 2)
        rows.append({"path": path, "additions": additions, "deletions": deletions, "source": "tracked"})
    return rows


def untracked_numstat(root: Path, files: list[str]) -> list[dict[str, Any]]:
    rows = []
    for rel_path in files:
        count = line_count(root / rel_path)
        rows.append(
            {
                "path": rel_path,
                "additions": "-" if count is None else str(count),
                "deletions": "0" if count is not None else "-",
                "source": "untracked",
            }
        )
    return rows


def totals(rows: list[dict[str, Any]]) -> dict[str, int]:
    additions = 0
    deletions = 0
    binary_files = 0
    for row in rows:
        if row["additions"] == "-" or row["deletions"] == "-":
            binary_files += 1
            continue
        additions += int(row["additions"])
        deletions += int(row["deletions"])
    return {"additions": additions, "deletions": deletions, "footprint": additions + deletions, "binary_files": binary_files}


def untracked_diff(root: Path, rel_path: str) -> str:
    path = root / rel_path
    data = path.read_bytes()
    header = f"diff --git a/{rel_path} b/{rel_path}\nnew file mode 100644\n"
    if b"\0" in data[:8192]:
        return f"{header}Binary files /dev/null and b/{rel_path} differ\n"
    text = data.decode("utf-8", errors="replace").splitlines(keepends=True)
    diff = difflib.unified_diff([], text, fromfile="/dev/null", tofile=f"b/{rel_path}", lineterm="")
    return header + "".join(line if line.endswith("\n") else f"{line}\n" for line in diff)


def build_state(base: str) -> dict[str, Any]:
    root = repo_root()
    point = base_point(base)
    tracked_files = split_lines(git_stdout(["diff", "--name-only", point]))
    untracked_files = split_lines(git_stdout(["ls-files", "--others", "--exclude-standard"]))
    rows = tracked_numstat(point) + untracked_numstat(root, untracked_files)
    return {
        "repo_root": str(root),
        "base": base,
        "base_point": point,
        "tracked_files": tracked_files,
        "untracked_files": untracked_files,
        "changed_files": tracked_files + untracked_files,
        "numstat": rows,
        "totals": totals(rows),
    }


def print_summary(state: dict[str, Any]) -> None:
    print(f"repo_root: {state['repo_root']}")
    print(f"base: {state['base']}")
    print(f"base_point: {state['base_point']}")
    print(f"tracked_files: {len(state['tracked_files'])}")
    print(f"untracked_files: {len(state['untracked_files'])}")
    print(f"changed_files: {len(state['changed_files'])}")
    print(
        "footprint: "
        f"+{state['totals']['additions']} -{state['totals']['deletions']} "
        f"total={state['totals']['footprint']} binary={state['totals']['binary_files']}"
    )
    print("\nchanged files:")
    for path in state["changed_files"]:
        print(path)
    print("\nother formats:")
    print("  --format diff     print the complete effective code diff")
    print("  --format numstat  print changed-line metrics")
    print("  --format json     print structured state")


def print_numstat(state: dict[str, Any]) -> None:
    for row in state["numstat"]:
        print(f"{row['additions']}\t{row['deletions']}\t{row['path']}")


def print_diff(state: dict[str, Any]) -> None:
    sys.stdout.write(git_stdout(["diff", state["base_point"]]))
    root = Path(state["repo_root"])
    for rel_path in state["untracked_files"]:
        sys.stdout.write(untracked_diff(root, rel_path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Report effective PR state as one final diff against base.")
    parser.add_argument("--base", required=True, help="Production base branch or ref, e.g. origin/main")
    parser.add_argument("--format", choices=["summary", "json", "numstat", "diff"], default="summary")
    args = parser.parse_args()

    state = build_state(args.base)
    if args.format == "summary":
        print_summary(state)
    elif args.format == "json":
        print(json.dumps(state, indent=2, sort_keys=True))
    elif args.format == "numstat":
        print_numstat(state)
    elif args.format == "diff":
        print_diff(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
