#!/usr/bin/env python3
"""devflow tools: check and install the external tools devflow skills use (registry: tools.json).

Usage:
  python3 tools.py check [<tool>...]     status of each tool, JSON; exit 3 when a requested tool is missing
  python3 tools.py install <tool>        install a devflow or user tool (never a project tool)
  python3 tools.py path <tool>           print the command to run a devflow tool

Kinds:
  devflow  installed by devflow in its own virtualenv (~/.local/share/devflow/tools), pinned version
  user     installed in the user's environment by a fixed command
  project  a dependency of the project: never installed here, only the instructions are printed
Standard library only.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV = os.path.join(os.path.expanduser("~"), ".local", "share", "devflow", "tools")


def registry():
    with open(os.path.join(ROOT, "tools.json"), encoding="utf-8") as handle:
        return json.load(handle)


def expand(value):
    if isinstance(value, list):
        return [v.replace("{venv}", VENV) for v in value]
    return value.replace("{venv}", VENV) if isinstance(value, str) else value


def available(tool):
    command = expand(tool.get("check"))
    if not command:
        return None
    if not (os.path.exists(command[0]) or shutil.which(command[0])):
        return False
    try:
        return subprocess.run(command, capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def how_to_install(name, tool):
    if tool["kind"] == "devflow":
        return f"python3 {os.path.join(ROOT, 'scripts', 'tools.py')} install {name}"
    return tool["install"]


def check(names):
    tools = registry()
    unknown = [n for n in names if n not in tools]
    if unknown:
        sys.exit(f"unknown tools: {', '.join(unknown)} (known: {', '.join(tools)})")
    report, missing = {}, False
    for name in names or tools:
        tool = tools[name]
        state = available(tool)
        report[name] = {"purpose": tool["purpose"], "kind": tool["kind"],
                        "installed": state if state is not None else "unknown (project build plugin)"}
        if state is not True:
            report[name]["install"] = how_to_install(name, tool)
            missing = missing or (state is False and bool(names))
    print(json.dumps(report, indent=2))
    sys.exit(3 if missing else 0)


def install(name):
    tools = registry()
    if name not in tools:
        sys.exit(f"unknown tool: {name}")
    tool = tools[name]
    if available(tool):
        print(f"{name}: already installed")
        return
    if tool["kind"] == "project":
        sys.exit(f"{name} is a project dependency; devflow does not install it. Run in the project, after the user agrees:\n  {tool['install']}")
    if tool["kind"] == "devflow":
        if not os.path.exists(os.path.join(VENV, "bin", "python")):
            subprocess.run([sys.executable, "-m", "venv", VENV], check=True)
        subprocess.run([os.path.join(VENV, "bin", "python"), "-m", "pip", "install", "--quiet", tool["pip"]], check=True)
    else:
        subprocess.run(tool["install_cmd"], check=True)
    if not available(tool):
        sys.exit(f"{name}: installed but the check still fails")
    print(f"{name}: installed")


def path(name):
    tool = registry().get(name)
    if not tool or tool["kind"] != "devflow":
        sys.exit(f"{name} is not a devflow tool")
    if not available(tool):
        sys.exit(f"{name} is not installed: {how_to_install(name, tool)}")
    print(expand(tool["run"]))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("check", "install", "path"):
        sys.exit(__doc__)
    command, names = sys.argv[1], sys.argv[2:]
    if command == "check":
        check(names)
    elif len(names) != 1:
        sys.exit(__doc__)
    elif command == "install":
        install(names[0])
    else:
        path(names[0])


if __name__ == "__main__":
    main()
