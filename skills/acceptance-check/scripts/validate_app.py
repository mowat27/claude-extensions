#!/usr/bin/env python3
"""Validate app runs: build, dev server, routes, and logging."""

import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError


PORT = 3030
DEV_TIMEOUT = 60  # seconds to wait for dev server


def kill_port(port: int) -> None:
    """Kill any process using the specified port."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
        )
        if result.stdout.strip():
            pids = result.stdout.strip().split("\n")
            for pid in pids:
                try:
                    os.kill(int(pid), 9)
                except (ProcessLookupError, ValueError):
                    pass
            print(f"Killed existing process(es) on port {port}")
    except Exception:
        pass


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 300) -> tuple[bool, str]:
    """Run command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"Command timed out after {timeout}s"
    except Exception as e:
        return False, str(e)


def check_url(url: str, retries: int = 3, delay: float = 1.0) -> tuple[bool, str]:
    """Check if URL responds successfully."""
    for i in range(retries):
        try:
            with urlopen(url, timeout=10) as resp:
                return resp.status == 200, f"Status: {resp.status}"
        except URLError as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                return False, str(e)
    return False, "Max retries exceeded"


def wait_for_server(url: str, timeout: int = DEV_TIMEOUT) -> bool:
    """Wait for server to be ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urlopen(url, timeout=5):
                return True
        except (URLError, TimeoutError, OSError):
            time.sleep(1)
    return False


def main(project_dir: str) -> int:
    """Run app validations."""
    cwd = Path(project_dir).resolve()

    # Debug: Print execution context
    print("=" * 50)
    print("EXECUTION CONTEXT DEBUG")
    print("=" * 50)
    print(f"Script location: {Path(__file__).resolve()}")
    print(f"Current working dir: {Path.cwd()}")
    print(f"Target project dir: {cwd}")
    print(f"Project dir exists: {cwd.exists()}")
    print(f"Python executable: {sys.executable}")
    print(f"PATH: {os.environ.get('PATH', 'NOT SET')[:200]}...")
    print(f"HOME: {os.environ.get('HOME', 'NOT SET')}")
    print(f"NODE_ENV: {os.environ.get('NODE_ENV', 'NOT SET')}")
    print(f"User: {os.environ.get('USER', 'NOT SET')}")

    # Check if pnpm is available
    try:
        pnpm_check = subprocess.run(["which", "pnpm"], capture_output=True, text=True)
        print(f"pnpm location: {pnpm_check.stdout.strip() or 'NOT FOUND'}")
    except Exception as e:
        print(f"pnpm check failed: {e}")

    # Check if node is available
    try:
        node_check = subprocess.run(["which", "node"], capture_output=True, text=True)
        print(f"node location: {node_check.stdout.strip() or 'NOT FOUND'}")
    except Exception as e:
        print(f"node check failed: {e}")

    print("=" * 50)

    if not cwd.exists():
        print(f"FAIL: Directory does not exist: {cwd}")
        return 1

    errors = []
    dev_process = None

    try:
        # Check 1: Start dev server on port 3030
        print(f"\nStarting dev server on port {PORT}...")
        kill_port(PORT)  # Clean up any stale processes
        dev_process = subprocess.Popen(
            ["pnpm", "dev", "--port", str(PORT)],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,  # Create new process group for clean shutdown
        )

        base_url = f"http://localhost:{PORT}"
        if not wait_for_server(base_url):
            errors.append(f"Dev server failed to start within {DEV_TIMEOUT}s")
            print("FAIL: dev server start")
        else:
            print("PASS: dev server started")

            # Check 2: Main route responds
            print("\nChecking main route...")
            success, msg = check_url(base_url)
            if not success:
                errors.append(f"Main route failed: {msg}")
                print(f"FAIL: main route ({msg})")
            else:
                print("PASS: main route")

            # Check 3: Health check route
            print("\nChecking health route...")
            health_url = f"{base_url}/api/health"
            success, msg = check_url(health_url)
            if not success:
                errors.append(f"Health route failed: {msg}")
                print(f"FAIL: health route ({msg})")
            else:
                print("PASS: health route")

        # Check 4: Logs exist (non-destructive check)
        print("\nChecking logs exist...")
        logs_dir = cwd / "logs"
        if not logs_dir.exists():
            errors.append("Logs directory does not exist")
            print("FAIL: logs directory missing")
        else:
            log_files = list(logs_dir.glob("*.log"))
            if not log_files:
                errors.append("No .log files found in logs/")
                print("FAIL: no log files")
            else:
                print(f"PASS: logs exist ({len(log_files)} file(s))")

    finally:
        # Clean up dev server and all child processes
        if dev_process:
            print("\nStopping dev server...")
            try:
                # Kill entire process group
                os.killpg(dev_process.pid, 15)  # SIGTERM
                dev_process.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    os.killpg(dev_process.pid, 9)  # SIGKILL
                except ProcessLookupError:
                    pass

    if errors:
        print("\n" + "=" * 50)
        print("APP VALIDATION FAILED")
        print("=" * 50)
        for err in errors:
            print(f"\n{err}")
        return 1

    print("\n" + "=" * 50)
    print("APP VALIDATION PASSED")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_app.py <project_dir>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
