from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "tabular-regression-workflow"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def parse_front_matter(text: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert match, "SKILL.md must start with YAML front matter"
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def test_skill_package_structure_exists() -> None:
    assert SKILL_DIR.is_dir()
    assert (SKILL_DIR / "SKILL.md").is_file()
    assert (SKILL_DIR / "scripts" / "verify_outputs.py").is_file()
    assert (SKILL_DIR / "references" / "output-contract.md").is_file()


def test_skill_metadata_is_trigger_oriented() -> None:
    front_matter = parse_front_matter((SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))
    description = front_matter["description"]

    assert front_matter["name"] == "tabular-regression-workflow"
    assert "California Housing" in description
    assert "tabular regression workflow" in description
    assert "verify" in description
    assert "classification" in (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "time-series" in (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "AutoML" in (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")


def test_required_docs_and_references_exist() -> None:
    for path in [
        "docs/SKILL_GUIDE.md",
        "docs/WORKFLOW_GUIDE.md",
        "docs/SKILL_VALIDATION.md",
        "docs/DESIGN.md",
        "docs/HW7_IMPLEMENTATION_PLAN.md",
        "docs/VALIDATION.md",
        "WORKFLOW.md",
        "README.md",
        "AGENTS.md",
    ]:
        assert (ROOT / path).is_file(), path


def test_readme_links_documentation_hub() -> None:
    readme = read("README.md")
    for expected in [
        "WORKFLOW.md",
        "docs/WORKFLOW_GUIDE.md",
        "docs/SKILL_GUIDE.md",
        "docs/SKILL_VALIDATION.md",
        "docs/DESIGN.md",
        "docs/HW7_IMPLEMENTATION_PLAN.md",
        "docs/VALIDATION.md",
        ".agents/skills/tabular-regression-workflow/SKILL.md",
    ]:
        assert expected in readme


def test_workflow_references_guides_and_verifier() -> None:
    workflow = read("WORKFLOW.md")
    assert "docs/WORKFLOW_GUIDE.md" in workflow
    assert "docs/SKILL_GUIDE.md" in workflow
    assert "verify_outputs.py --config configs\\california_housing.json" in workflow
    assert "source of truth" not in workflow.lower() or "workflow" in workflow.lower()


def test_skill_guardrails_are_present() -> None:
    combined = "\n".join(
        [
            read("AGENTS.md"),
            read("README.md"),
            read("WORKFLOW.md"),
            (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"),
        ]
    )
    for phrase in [
        "Do not commit or push",
        "Do not add undeclared dependencies",
        "Do not claim coefficients prove causality",
        "Fresh-session",
    ]:
        assert phrase in combined
