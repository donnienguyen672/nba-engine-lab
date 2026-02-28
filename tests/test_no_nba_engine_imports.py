"""Guard test: ensure no imports from nba-engine (governed repo)."""

import os
import re


def test_no_nba_engine_imports():
    """Scan all .py files for forbidden imports from nba_engine."""
    root = os.path.join(os.path.dirname(__file__), "..")
    violations = []

    for dirpath, _, filenames in os.walk(root):
        # Skip hidden dirs and __pycache__
        if "/." in dirpath or "__pycache__" in dirpath:
            continue
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(dirpath, fname)
            with open(fpath, "r") as f:
                for i, line in enumerate(f, 1):
                    if re.search(r"(from|import)\s+nba_engine", line):
                        violations.append(f"{fpath}:{i}: {line.strip()}")

    assert violations == [], (
        f"Found {len(violations)} forbidden import(s) from nba_engine:\n"
        + "\n".join(violations)
    )
