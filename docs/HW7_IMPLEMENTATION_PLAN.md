# HW7 California Housing Workflow + Lightweight Skill Plan

## Document status

- Status: Approved implementation baseline
- Owner: 駿弘
- Date: 2026-06-15
- Source project: `hw6_50_startups_crispdm`
- Primary requirement: Workflow first
- Optional enhancement: Lightweight repository-scoped Codex Skill
- Final presentation target: Public GitHub repository and GitHub Pages

## 1. Goal

Convert the repeatable parts of HW6 into a portable, configuration-driven regression workflow. Verify the workflow with the teacher-provided California Housing dataset and present the complete process, outputs, documentation, and optional Skill in GitHub.

## 2. Scope

### Required

- California Housing CSV acquisition
- Explicit configuration for target and features
- CRISP-DM-aligned processing
- Missing-value handling
- Categorical encoding
- Multiple linear regression
- Test split and cross-validation metrics
- Model artifact
- Visual gallery and all-in-one infographic
- Markdown report
- Smoke test
- GitHub Pages presentation

### Included as a lightweight extension

- Root `AGENTS.md` for Codex project rules
- Repository Skill under `.agents/skills/tabular-regression-workflow/SKILL.md`
- Skill delegates execution to the tested Workflow; it does not duplicate model logic

### Non-goals

- AutoML
- Classification
- Multiple-model tournament
- Hyperparameter search
- API/backend
- Database
- Streamlit
- React/Vite
- Docker/cloud deployment
- Plugin marketplace distribution

## 3. Milestones

### M0 — Planning and repository baseline

- Save this plan
- Establish project structure
- Add AGENTS and Workflow documentation

### M1 — Reusable workflow core

- JSON configuration
- Dataset validation and download
- Pipeline preprocessing
- Linear regression training
- Metrics and model saving

### M2 — Visual and report outputs

- Dataset overview
- Correlation heatmap
- Actual vs predicted
- Residual diagnostics
- Coefficient chart
- Metrics summary
- Homework infographic
- Workflow report

### M3 — Portability validation

- Synthetic-schema smoke fixture
- Automated pytest smoke test
- Single Windows entry command

### M4 — Skill and GitHub presentation

- Lightweight Skill
- Static site
- README
- GitHub Pages verification

## 4. Completion criteria

The project is complete when:

1. `python -m pytest` passes.
2. The real California Housing workflow runs from a clean environment.
3. Required output files exist and contain real data.
4. The saved model can accept the configured feature schema.
5. GitHub Pages displays real metrics and generated images.
6. A second user or device can follow README and reproduce the workflow.

## 5. Current limitation at baseline creation

The repository scaffolding and smoke workflow can be validated without internet. Full California Housing outputs require either internet access during execution or a local `data/housing.csv` copied from the teacher-provided source.
