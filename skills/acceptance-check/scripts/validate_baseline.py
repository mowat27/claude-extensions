#!/usr/bin/env python3
"""Validate baseline conditions: pnpm check and pnpm test pass."""

import subprocess
import sys
from pathlib import Path


def run_cmd(cmd: list[str], cwd: Path) -> tuple[bool, str]:
    """Run command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Command timed out after 300s"
    except Exception as e:
        return False, str(e)


def main(project_dir: str) -> int:
    """Run baseline validations."""
    cwd = Path(project_dir).resolve()

    if not cwd.exists():
        print(f"FAIL: Directory does not exist: {cwd}")
        return 1

    errors = []

    # Check 1: pnpm check (lint + typecheck)
    print("Running pnpm check...")
    success, output = run_cmd(["pnpm", "check"], cwd)
    if not success:
        errors.append(f"pnpm check failed:\n{output}")
        print("FAIL: pnpm check")
    else:
        print("PASS: pnpm check")

    # Check 2: pnpm test
    print("\nRunning pnpm test...")
    success, output = run_cmd(["pnpm", "test"], cwd)
    if not success:
        errors.append(f"pnpm test failed:\n{output}")
        print("FAIL: pnpm test")
    else:
        # Check for error patterns in output even if exit code is 0
        error_patterns = ["FAIL", "Error:", "error:", "failed"]
        has_errors = any(p in output for p in error_patterns if "0 failed" not in output.lower())
        if has_errors and "FAIL" in output:
            errors.append(f"pnpm test passed but output contains errors:\n{output}")
            print("FAIL: pnpm test (errors in output)")
        else:
            print("PASS: pnpm test")

    if errors:
        print("\n" + "=" * 50)
        print("BASELINE VALIDATION FAILED")
        print("=" * 50)
        for err in errors:
            print(f"\n{err}")
        return 1

    print("\n" + "=" * 50)
    print("BASELINE VALIDATION PASSED")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_baseline.py <project_dir>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
