#!/usr/bin/env python3
"""Test of setup.py against a fake HOME: dry run writes nothing, apply is idempotent, keeps foreign settings and CLAUDE.md text, and the created Vault passes kb_verify.

Usage: python3 test_setup.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run(home, *args):
    env = {**os.environ, "HOME": home}
    return subprocess.run([sys.executable, os.path.join(HERE, "setup.py"), *args], env=env, capture_output=True, text=True)


for language in ("pt-BR", "en"):
    with tempfile.TemporaryDirectory() as home:
        claude = os.path.join(home, ".claude")
        os.makedirs(claude)
        json.dump({"theme": "auto", "permissions": {"deny": ["Bash(rm -rf *)"]}}, open(os.path.join(claude, "settings.json"), "w"))
        open(os.path.join(claude, "CLAUDE.md"), "w").write("# Mine\n\nKeep me.\n")
        vault = os.path.join(home, "vault")
        args = ["apply", "--language", language, "--vault", vault, "--areas", "issue,planning"]

        r = run(home, *args, "--dry-run")
        assert r.returncode == 0, r.stderr
        assert not os.path.exists(vault) and not os.path.exists(os.path.join(home, ".config")), "dry run wrote files"

        r = run(home, *args)
        assert r.returncode == 0, r.stderr
        settings = json.load(open(os.path.join(claude, "settings.json")))
        assert settings["theme"] == "auto" and settings["autoMemoryEnabled"] is False
        assert "Bash(rm -rf *)" in settings["permissions"]["deny"]
        md = open(os.path.join(claude, "CLAUDE.md")).read()
        assert md.startswith("# Mine\n\nKeep me.\n") and md.count("devflow:start") == 1
        assert f"@{vault}/devflow/conventions.md" in md
        config = json.load(open(os.path.join(home, ".config", "devflow", "config.json")))
        assert config["areas"] == ["issue", "knowledge", "planning"], config

        r = run(home, *args)
        assert "(nothing missing)" in r.stdout and r.stdout.count("(no change)") == 3, r.stdout
        assert open(os.path.join(claude, "CLAUDE.md")).read() == md

        r = run(home, "apply", "--language", language, "--vault", vault, "--areas", "issue")
        assert r.returncode == 0, r.stderr

        v = subprocess.run([sys.executable, os.path.join(HERE, "kb_verify.py"), "--base", vault], capture_output=True, text=True)
        assert v.returncode == 0, v.stdout
    print(f"ok {language}: dry run, apply, idempotence, foreign settings kept, vault verifies")
