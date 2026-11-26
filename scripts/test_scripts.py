#!/usr/bin/env python3
"""Test of the scripts that build pages and catalogs: overview.py, draw_view.py, catalog.py and tools.py.

Usage: python3 test_scripts.py
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(HERE)


def run(script, *args, home=None):
    env = {**os.environ, **({"HOME": home} if home else {})}
    return subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True, env=env, timeout=120)


def data_block(page):
    return json.loads(re.search(r'<script type="application/json" id="data">\n(.*?)\n</script>', page, re.S).group(1).replace("<\\/", "</"))


with tempfile.TemporaryDirectory() as home:
    vault = os.path.join(home, "vault")
    os.makedirs(os.path.join(home, ".config", "devflow"))
    areas = json.load(open(os.path.join(PLUGIN, "components.json")))["areas"]
    on = [name for name in areas if name != "experimental"]
    json.dump({"language": "pt-BR", "vault": vault, "areas": on}, open(os.path.join(home, ".config", "devflow", "config.json"), "w"))

    # draw_view: fills the template, escapes </script>, keeps pairs
    data = {"title": "T", "diagrams": [{"title": "a", "mermaid": "flowchart LR\n  x[\"</script>\"]", "pair": "p"}, {"title": "b", "mermaid": "flowchart LR\n  y", "pair": "p"}]}
    json.dump(data, open(os.path.join(home, "d.json"), "w"))
    r = run("draw_view.py", os.path.join(home, "d.json"), os.path.join(home, "out", "d.html"))
    assert r.returncode == 0, r.stderr
    page = open(os.path.join(home, "out", "d.html")).read()
    assert page.count("</script>") == page.count("<script"), "an unescaped </script> broke the page"
    assert data_block(page) == data and "<title>T</title>" in page
    json.dump({"title": "empty", "diagrams": []}, open(os.path.join(home, "e.json"), "w"))
    assert run("draw_view.py", os.path.join(home, "e.json"), os.path.join(home, "e.html")).returncode != 0

    # overview: default path in the git-ignored issues/, both languages, every diagram, Areas state, contracts
    r = run("overview.py", home=home)
    assert r.returncode == 0, r.stderr
    page = open(os.path.join(vault, "issues", "overview.html")).read()
    pt = data_block(page)
    assert pt["title"] == "devflow: visão geral" and len(pt["diagrams"]) == 7, [d["title"] for d in pt["diagrams"]]
    areas_mermaid = pt["diagrams"][0]["mermaid"]
    assert "experimental<br/>(desligada)" in areas_mermaid, "experimental must show as off when it is off"
    for skill in areas["experimental"]["skills"]:
        assert f'"{skill}"]:::skip' in areas_mermaid, skill
    files = pt["diagrams"][-1]["mermaid"]
    assert "K_analyze --> D_Analysis" in files and "D_Investigation -.-> K_diagnose" in files and "K_refactor --> D_Task" in files, files
    r = run("overview.py", "--language", "en", "--out", os.path.join(home, "en.html"), home=home)
    assert r.returncode == 0 and data_block(open(os.path.join(home, "en.html")).read())["title"] == "devflow overview"
    assert run("overview.py", "--out", home=home).returncode == 2

    # catalog: lists every Area and skill, marks off Areas, skips maintenance backlog entries
    r = run("catalog.py", home=home)
    assert r.returncode == 0, r.stderr
    for name, area in areas.items():
        assert f"## {name}" in r.stdout, name
        for skill in area.get("skills", []):
            assert f"/devflow:{skill}" in r.stdout, skill
    assert "## experimental (off)" in r.stdout
    assert "(maintenance" not in r.stdout

    # tools: check reports shape and install instructions; project tools are never installed
    r = run("tools.py", "check", "stryker", home=home)
    report = json.loads(r.stdout)
    assert report["stryker"]["kind"] == "project" and "install" in report["stryker"] or report["stryker"]["installed"] is True
    r = run("tools.py", "install", "stryker", home=home)
    assert r.returncode != 0 and "does not install it" in r.stderr, r.stderr
    assert run("tools.py", "check", "nope", home=home).returncode != 0
    assert run("tools.py", "path", "stryker", home=home).returncode != 0

print("ok: draw_view fills and escapes; overview writes every diagram in both languages with Areas state and contracts; catalog lists Areas; tools never installs project tools")
