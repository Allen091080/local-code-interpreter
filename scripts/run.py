#!/usr/bin/env python3
"""
Local Code Interpreter — run.py
================================
Execute Python code or files locally and capture output.

Usage:
  python3 run.py --code "print('hello')"
  python3 run.py --file /path/to/script.py
  python3 run.py --code "..." --no-header
"""

import argparse
import sys
import os
import io
import traceback
import subprocess
from contextlib import redirect_stdout, redirect_stderr


def execute_code(code: str) -> dict:
    """Execute a string of Python code and capture stdout/stderr."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    result = {"stdout": "", "stderr": "", "error": None, "success": False}

    exec_globals = {"__name__": "__main__", "__builtins__": __builtins__}

    try:
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            exec(compile(code, "<string>", "exec"), exec_globals)
        result["success"] = True
    except Exception:
        result["error"] = traceback.format_exc()
    finally:
        result["stdout"] = stdout_buf.getvalue()
        result["stderr"] = stderr_buf.getvalue()

    return result


def execute_file(filepath: str) -> dict:
    """Execute a Python file as a subprocess."""
    try:
        proc = subprocess.run(
            [sys.executable, filepath],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return {
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode,
            "success": proc.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Execution timed out (120 s)",
            "returncode": -1,
            "success": False,
        }
    except Exception as exc:
        return {"stdout": "", "stderr": str(exc), "returncode": -1, "success": False}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local Python code executor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--code", "-c", type=str, help="Python code string to execute")
    group.add_argument("--file", "-f", type=str, help="Path to a Python file to execute")
    parser.add_argument("--no-header", action="store_true", help="Suppress separator output")
    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        result = execute_file(args.file)
    else:
        result = execute_code(args.code)

    if not args.no_header:
        print("=" * 50)
        print("Output")
        print("=" * 50)

    if result.get("stdout"):
        print(result["stdout"], end="")

    if result.get("stderr") and result["stderr"].strip():
        print("\n[stderr]", file=sys.stderr)
        print(result["stderr"], file=sys.stderr)

    if result.get("error"):
        print("\n[error]", file=sys.stderr)
        print(result["error"], file=sys.stderr)
        sys.exit(1)

    if not result.get("success") and result.get("returncode", 0) != 0:
        sys.exit(result.get("returncode", 1))


if __name__ == "__main__":
    main()
