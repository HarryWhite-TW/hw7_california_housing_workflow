# Design Notes

## Design motivation

HW6 was dataset-specific: paths, target, and feature names were fixed to 50 Startups. HW7 separates configuration from execution so the same tested modules can run against California Housing and later compatible regression datasets.

## Responsibility boundaries

- `configs/`: dataset-specific decisions
- `src/config.py`: configuration validation and path resolution
- `src/data_io.py`: acquisition, loading, schema validation, dataset summary
- `src/modeling.py`: preprocessing pipeline, model training, metrics, coefficients
- `src/visualization.py`: deterministic image generation
- `src/reporting.py`: JSON, Markdown, and static-site results
- `src/workflow.py`: orchestration only
- `run_workflow.py`: user-facing command-line entry point
- `.agents/skills/`: Codex usage instructions, not business logic

## Why Pipeline + ColumnTransformer

The saved model must include preprocessing. This avoids a common failure where training uses one encoding process but later predictions use a different one.

## Why explicit feature configuration

Automatic column inference would be convenient but less transparent for a beginner assignment. Explicit features make the modeling contract visible, auditable, and easier to explain.

## Why the Skill stays thin

The Workflow is the source of truth. The Skill tells Codex when and how to execute and verify it. Duplicating Python logic inside the Skill would create two implementations that could drift apart.
