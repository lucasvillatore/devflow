#!/usr/bin/env python3
"""Build a visual overview of devflow (Areas, flows, workspace files) as a zoomable page.

Usage: python3 overview.py [--out <file.html>] [--open]

The Areas come from components.json; the flows are described below. The page is written in the language
of ~/.config/devflow/config.json (en when missing), by default to <vault>/devflow/overview.html.
Standard library only.
"""
import json
import os
import subprocess
import sys
import tempfile

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLASSES = "\n".join([
    "  classDef ok fill:#d9f2e3,stroke:#1d7a46,color:#14301f",
    "  classDef info fill:#e8eefb,stroke:#2456c9,color:#14213d",
    "  classDef wait fill:#fbeedf,stroke:#b4570e,color:#3a2817,stroke-dasharray: 4 3",
    "  classDef skip fill:#eceef2,stroke:#5d6779,color:#1b2230,stroke-dasharray: 4 3",
    "  classDef file fill:#ffffff,stroke:#5d6779,color:#1b2230",
])

TEXT = {
    "en": {
        "title": "devflow overview",
        "subtitle": "Areas, the usual flows and the files skills exchange. Dashed orange: experimental. Dashed grey: optional step.",
        "required": "required", "off": "off", "none": "no skill yet", "hint": "Scroll to zoom, drag to move.",
        "areas": "Areas and skills",
        "areas_legend": ["Each yellow box is an Area; on its right, its skills (`/devflow:<name>`).", "Required Areas are always on; the others are turned on or off in `/devflow:setup`.", "Experimental skills are being tested and move to their real Area once validated."],
        "flows": {
            "bug": ("Bug with an unknown cause", ["pick-issue: assign, move to In Development, workspace", "analyze: map the code, findings by lens", "investigate-issue: red signal, facts, premise check", "diagnose: verdict (cause confirmed or probable)", "draw: the whole problem with zoom (optional)", "plan-issue: interview, Planning and Tasks", "implement each Task, close it (status done, box ticked)", "open-pr: PR with evidence, Jira to Code Review", "retro: lessons into guardrails, conventions, knowledge"]),
            "known": ("Known cause or simple task", ["pick-issue", "plan-issue", "implement each Task, close it", "open-pr"]),
            "noissue": ("Work without an Issue", ["workspace by name (e.g. vendor-service-update)", "analyze / investigate-issue / diagnose / draw", "plan-issue", "pick-issue KEY name: adopts the workspace if it becomes an Issue"]),
            "refactor": ("Refactoring", ["analyze (optional): findings and lenses", "refactor-plan: project, hot spots, border tests, Tasks; or 'healthy'", "refactor per Task: worth it? pin behavior, small steps, proof", "'it is ok': nothing to refactor (valid result)", "open-pr with the proof as evidence"]),
            "improve": ("Improving devflow itself", ["retro at the end of a session", "add-guardrail: hook or rule in ~/.claude", "Vault: convention or repository profile", "session in ~/dev/devflow: CLAUDE.md guides, grilling rounds", "backlog or commit"]),
        },
        "files": "Workspace files (contracts)",
        "files_legend": ["`<vault>/issues/<KEY or name>/`: skills never call each other; they write and read these files.", "Solid arrow: writes. Dashed arrow: reads.", "Files are found by their `type`, not by name (names follow your language)."],
        "labels": {"Issue": "index.md (Issue)", "Task": "Tasks (1 = Planning)", "Analysis": "Analysis", "Investigation": "Investigation", "Diagnosis": "Diagnosis", "Refactor": "Refactor record", "Retro": "Retro", "diagrams": "diagrams/ (pages)", "log": "log.md"},
    },
    "pt-BR": {
        "title": "devflow: visão geral",
        "subtitle": "Áreas, os fluxos de sempre e os arquivos que as skills trocam. Laranja tracejado: experimental. Cinza tracejado: passo opcional.",
        "required": "obrigatória", "off": "desligada", "none": "nenhuma skill ainda", "hint": "Role para dar zoom, arraste para mover.",
        "areas": "Áreas e skills",
        "areas_legend": ["Cada caixa amarela é uma Área; à direita, as skills dela (`/devflow:<nome>`).", "Áreas obrigatórias ficam sempre ligadas; as outras são ligadas ou desligadas no `/devflow:setup`.", "Skills experimentais estão em teste e vão para a Área de verdade quando validadas."],
        "flows": {
            "bug": ("Bug com causa desconhecida", ["pick-issue: atribui, move para In Development, cria o workspace", "analyze: mapa do código, achados por lente", "investigate-issue: sinal vermelho, fatos, checa a premissa", "diagnose: veredito (causa confirmada ou provável)", "draw: o problema inteiro com zoom (opcional)", "plan-issue: entrevista, planejamento e Tasks", "implementar cada Task e fechar (done, checkbox)", "open-pr: PR com evidências, Jira para Code Review", "retro: lições viram guardrail, convenção, conhecimento"]),
            "known": ("Causa conhecida ou tarefa simples", ["pick-issue", "plan-issue", "implementar cada Task e fechar", "open-pr"]),
            "noissue": ("Trabalho sem Issue", ["workspace por nome (ex.: vendor-service-update)", "analyze / investigate-issue / diagnose / draw", "plan-issue", "pick-issue CHAVE nome: adota o workspace se virar Issue"]),
            "refactor": ("Refatoração", ["analyze (opcional): achados e lentes", "refactor-plan: projeto, pontos quentes, testes de borda, Tasks; ou 'saudável'", "refactor por Task: vale a pena? fixa o comportamento, passos pequenos, prova", "'está ok': nada a refatorar (resultado válido)", "open-pr com a prova como evidência"]),
            "improve": ("Melhorar o próprio devflow", ["retro no fim da sessão", "add-guardrail: hook ou regra no ~/.claude", "Vault: convenção ou perfil do repo", "sessão em ~/dev/devflow: o CLAUDE.md guia, rodadas de grilling", "backlog ou commit"]),
        },
        "files": "Arquivos do workspace (contratos)",
        "files_legend": ["`<vault>/issues/<CHAVE ou nome>/`: as skills nunca chamam umas às outras; elas gravam e leem estes arquivos.", "Seta contínua: grava. Seta tracejada: lê.", "Os arquivos são achados pelo `type`, não pelo nome (os nomes seguem o seu idioma)."],
        "labels": {"Issue": "index.md (Issue)", "Task": "Tasks (1 = planejamento)", "Analysis": "Análise", "Investigation": "Investigação", "Diagnosis": "Diagnóstico", "Refactor": "Registro da refatoração", "Retro": "Retro", "diagrams": "diagramas/ (páginas)", "log": "log.md"},
    },
}

# Flow shapes: the class of each step (by index) and the edges beyond the straight chain.
FLOW_SHAPE = {
    "bug": {"classes": {1: "wait", 2: "wait", 3: "wait", 4: "skip", 6: "info", 8: "skip"}, "edges": [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (6, 7), (7, 8)]},
    "known": {"classes": {2: "info"}, "edges": [(0, 1), (1, 2), (2, 3)]},
    "noissue": {"classes": {1: "wait", 3: "skip"}, "edges": [(0, 1), (1, 2), (2, 3)]},
    "refactor": {"classes": {0: "skip", 1: "wait", 2: "wait", 3: "ok"}, "edges": [(0, 1), (1, 2), (2, 3, "dotted"), (2, 4)]},
    "improve": {"classes": {}, "edges": [(0, 1), (0, 2), (0, 3), (3, 4)]},
}

# Who writes (w) and reads (r) each workspace file.
CONTRACTS = {
    "pick-issue": {"w": ["Issue", "log"]},
    "plan-issue": {"w": ["Task", "log"], "r": ["Issue", "Analysis", "Investigation", "Diagnosis"]},
    "analyze": {"w": ["Analysis"]},
    "investigate-issue": {"w": ["Investigation"], "r": ["Issue", "Analysis"]},
    "diagnose": {"w": ["Diagnosis"], "r": ["Issue", "Analysis", "Investigation"]},
    "draw": {"w": ["diagrams"], "r": ["Analysis", "Investigation", "Diagnosis"]},
    "refactor-plan": {"w": ["Task", "log"]},
    "refactor": {"w": ["Refactor"], "r": ["Task", "Analysis"]},
    "open-pr": {"w": ["log"], "r": ["Issue", "Task", "Diagnosis", "Investigation", "Refactor"]},
    "retro": {"w": ["Retro"], "r": ["Investigation"]},
}


def config():
    try:
        with open(os.path.expanduser("~/.config/devflow/config.json"), encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def node(name):
    return "".join(c if c.isalnum() else "_" for c in name)


def label(text):
    return text.replace('"', "'")


def areas_diagram(t, active):
    with open(os.path.join(PLUGIN, "components.json"), encoding="utf-8") as handle:
        areas = json.load(handle)["areas"]
    lines = ["flowchart LR"]
    order = [n for n in ("base", "issue", "planning", "development", "delivery", "investigate", "knowledge", "experimental") if n in areas]
    order += [n for n in areas if n not in order]
    for name in order:
        area = areas[name]
        state = t["required"] if area.get("required") else ("" if name in active or name == "experimental" else t["off"])
        title = f"{name}<br/>({state})" if state else name
        lines.append(f'  A_{node(name)}["<b>{label(title)}</b>"]:::area')
        for skill in area.get("skills", []) or [t["none"]]:
            cls = ":::wait" if name == "experimental" else (":::skip" if name not in active and not area.get("required") else ":::info")
            lines.append(f'  S_{node(name)}_{node(skill)}["{label(skill)}"]{cls}')
            lines.append(f"  A_{node(name)} --- S_{node(name)}_{node(skill)}")
    return "\n".join(lines) + "\n" + CLASSES + "\n  classDef area fill:#fffbe6,stroke:#9a8a2a,color:#2a2410"


def flow_diagram(key, steps):
    shape = FLOW_SHAPE[key]
    lines = ["flowchart TD"]
    for i, step in enumerate(steps):
        cls = shape["classes"].get(i)
        lines.append(f'  F{i}["{label(step)}"]' + (f":::{cls}" if cls else ""))
    for edge in shape["edges"]:
        arrow = "-.->" if len(edge) > 2 else "-->"
        lines.append(f"  F{edge[0]} {arrow} F{edge[1]}")
    return "\n".join(lines) + "\n" + CLASSES


def files_diagram(t):
    lines = ["flowchart LR"]
    for kind, text in t["labels"].items():
        lines.append(f'  D_{kind}[("{label(text)}")]:::file')
    for skill, rw in CONTRACTS.items():
        cls = ":::wait" if skill in ("analyze", "investigate-issue", "diagnose", "draw", "refactor", "refactor-plan") else ":::info"
        lines.append(f'  K_{node(skill)}["{skill}"]{cls}')
        for kind in rw.get("w", []):
            lines.append(f"  K_{node(skill)} --> D_{kind}")
        for kind in rw.get("r", []):
            lines.append(f"  D_{kind} -.-> K_{node(skill)}")
    return "\n".join(lines) + "\n" + CLASSES


def main():
    cfg = config()
    t = TEXT.get(cfg.get("language"), TEXT["en"])
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    elif cfg.get("vault"):
        out = os.path.join(cfg["vault"], "devflow", "overview.html")
    else:
        sys.exit("no Vault configured: pass --out <file.html>")
    active = set(cfg.get("areas", []))
    diagrams = [{"title": t["areas"], "mermaid": areas_diagram(t, active), "legend": t["areas_legend"]}]
    for key, (title, steps) in t["flows"].items():
        diagrams.append({"title": title, "mermaid": flow_diagram(key, steps), "legend": []})
    diagrams.append({"title": t["files"], "mermaid": files_diagram(t), "legend": t["files_legend"]})
    data = {"title": t["title"], "subtitle": t["subtitle"], "hint": t["hint"], "diagrams": diagrams, "explanation": []}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False)
        path = handle.name
    command = [sys.executable, os.path.join(PLUGIN, "scripts", "draw_view.py"), path, out] + (["--open"] if "--open" in sys.argv else [])
    result = subprocess.run(command)
    os.unlink(path)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
