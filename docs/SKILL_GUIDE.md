# Repository Codex Skill Guide

## Skill Purpose

The repository-scoped `tabular-regression-workflow` skill teaches Codex how to select, run, verify, and safely adapt this project workflow. It does not replace the Python implementation. The workflow remains the source of truth.

## When To Use The Skill

Use the skill when a request mentions:

- California Housing workflow execution;
- generated metrics, charts, model artifacts, reports, or site data;
- validation of the current workflow outputs;
- reuse of the same tabular regression workflow with a compatible CSV;
- Codex automation for this repository.

## Workflow And Skill Relationship

| Layer | Responsibility | Used by |
| --- | --- | --- |
| Workflow | Executes deterministic analysis | Humans, CI, scripts, Codex |
| Skill | Guides Codex to select, run, and verify the workflow | Codex |
| Config | Defines dataset-specific schema | Workflow |
| Verification | Checks outputs and consistency | Humans, CI, Codex |

## Skill Package Structure

```text
.agents/skills/tabular-regression-workflow/
|-- SKILL.md
|-- references/
|   `-- output-contract.md
`-- scripts/
    `-- verify_outputs.py
```

## How Codex Should Use It

Codex should read the repository instructions, choose the configured Python interpreter, install only declared dependencies, run tests, run the workflow, execute the verifier, and report exact results. It should not commit, push, or redesign the analysis unless the user explicitly asks.

## Minimal Validation Prompt

```text
Use $tabular-regression-workflow to validate the current
California Housing workflow outputs.
Do not modify, commit, or push.
```

## Full Regeneration Prompt

```text
Regenerate and verify the configured California Housing regression
metrics, model, charts, report, and static site data.
Do not redesign the analysis.
```

## CSV Adaptation Prompt

```text
Use $tabular-regression-workflow to adapt the existing workflow to
my compatible tabular regression CSV. Create a new config, keep the
California Housing baseline intact, and verify the new outputs.
```

## Expected Behavior

The skill should produce:

- tested Python workflow execution;
- verified JSON, CSV, model, PNG, report, and site data;
- clear distinction between smoke results and real California Housing results;
- concise reporting of metrics and changed files.

## Safety Boundaries

- Do not add undeclared dependencies.
- Do not use AutoML.
- Do not add Streamlit, React, Vite, Docker, databases, APIs, or cloud services.
- Do not infer causality from coefficients.
- Do not commit or push without explicit approval.
- Claim fresh-session activation as complete only when `docs/SKILL_VALIDATION.md` records tested evidence.

## Troubleshooting

If `.venv` is missing, create it with a compatible Python and install `requirements.txt`. If the dataset is absent, use the configured `download_if_missing` behavior. If output verification fails, inspect the failing artifact before changing code.

## Versioning

The skill is repository-scoped and should evolve with `WORKFLOW.md`, `docs/WORKFLOW_GUIDE.md`, and the output contract. Any change to generated artifact names or metrics must update the verifier and contract test.

## Acceptance Criteria

- `SKILL.md` has valid front matter.
- `verify_outputs.py` exits with code 0 for the real baseline outputs.
- `tests/test_skill_contract.py` passes.
- `docs/SKILL_VALIDATION.md` records implementation validation, explicit activation, and implicit activation as passed after tested evidence exists.
