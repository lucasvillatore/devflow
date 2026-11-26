#!/usr/bin/env python3
"""Test of kb_verify.py: builds a fake base with defects for each template language and checks every defect is reported.

Usage: python3 test_kb_verify.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(HERE)

CASES = {
    "pt-BR": {
        "files": {
            "Contextos de negócio/X/Yaml quebrado.md":
                "---\ntype: Regra de negócio\ntitle: A\ndescription: Regra do pedido: ruim\n"
                "status: rascunho\ntimestamp: 2026-01-15\n---\n# Regra\nx\n",
            "Contextos de negócio/X/Varios.md":
                "---\ntype: Regrinha\ntitle: B\ndescription: d\nstatus: pronto\ntimestamp: 2026-01-15\n---\n"
                "# Regra\nSe o prazo é zero, o sistema ignora. O worker manda o payload.\n"
                "Ver [x](Nao%20existe.md) e [y](Yaml%20quebrado.md#regra).\n# Citations\n",
            "Contextos de negócio/X/Sem exemplo.md":
                "---\ntype: Regra de negócio\ntitle: C\ndescription: d\nstatus: ativo\ntimestamp: 2026-01-15\n---\n# Regra\nx\n",
            "Contextos de negócio/X/index.md": "---\ntype: Termo\n---\n",
            "Contextos de negócio/X/Certo.md":
                "---\ntype: Regra de negócio\ntitle: D\ndescription: d\nstatus: ativo\ntimestamp: 2026-01-15\n---\n"
                "# Regra\nO prazo é sempre de pelo menos 1 dia.\n# Exemplo\nUm caso.\n",
            "issues/ABC-1/0-issue.md": "sem frontmatter\n",
        },
        "expected": [
            "type 'Regrinha' is not in the configuration",
            "status 'pronto' is not in the configuration",
            "forbidden section: # Citations",
            "broken link: Nao%20existe.md",
            "invalid YAML frontmatter",
            "index.md cannot have frontmatter",
            "Sem exemplo.md: missing required section of template 'Regra de negócio': # Exemplo",
            "forbidden phrase",
            "system term 'worker'",
            "system term 'payload'",
            "anchor link '#regra'",
        ],
        "clean": ["Certo.md", "issues/"],
    },
    "en": {
        "files": {
            "Business contexts/X/No example.md":
                "---\ntype: Business rule\ntitle: C\ndescription: d\nstatus: active\ntimestamp: 2026-01-15\n---\n# Rule\nx\n",
            "Business contexts/X/Draft journey.md":
                "---\ntype: Journey\ntitle: J\ndescription: d\nstatus: draft\ntimestamp: 2026-01-15\n---\n# Goal\nx\n",
            "Business contexts/X/Bad.md":
                "---\ntype: Business rule\ntitle: B\ndescription: d\nstatus: rascunho\ntimestamp: 2026-01-15\n---\n"
                "# Rule\nIf the time is zero, the system ignores it.\n# Example\nx\n",
            "devflow/projects/repo.md": "no frontmatter\n",
        },
        "expected": [
            "No example.md: missing required section of template 'Business rule': # Example",
            "status 'rascunho' is not in the configuration",
            "forbidden phrase",
        ],
        "clean": ["Draft journey.md", "devflow/"],
    },
}

for language, case in CASES.items():
    with tempfile.TemporaryDirectory() as base:
        shutil.copytree(os.path.join(PLUGIN, "templates", "kb", language, ".kb"), os.path.join(base, ".kb"))
        for rel, content in case["files"].items():
            path = os.path.join(base, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(content)
        r = subprocess.run([sys.executable, os.path.join(HERE, "kb_verify.py"), "--base", base],
                           capture_output=True, text=True)

    missing = [e for e in case["expected"] if e not in r.stdout]
    assert r.returncode == 1, f"{language}: expected exit code 1, got {r.returncode}\n{r.stdout}{r.stderr}"
    assert not missing, f"{language}: not reported: {missing}\n\n{r.stdout}"
    for clean in case["clean"]:
        assert clean not in r.stdout, f"{language}: reported a problem in {clean}:\n{r.stdout}"
    print(f"ok {language}: {len(case['expected'])} defects reported, clean files untouched")
