# Codex Finalization Task Packet

Use this after the project is copied to the user's computer and opened in Codex.

```text
You are working in the hw7_california_housing_workflow repository.

Goal:
Finish and verify the approved HW7 California Housing reusable regression Workflow, its lightweight repository Skill, and its GitHub Pages presentation.

Read first:
- AGENTS.md
- docs/HW7_IMPLEMENTATION_PLAN.md
- WORKFLOW.md
- configs/california_housing.json

Required work:
1. Inspect the existing implementation. Do not rebuild it with another framework.
2. Create and activate a local virtual environment only if needed.
3. Install requirements.txt.
4. Run python -m pytest and fix only relevant failures.
5. Ensure data/housing.csv exists. If absent, use the source_url in configs/california_housing.json.
6. Run python run_workflow.py --config configs/california_housing.json.
7. Inspect generated metrics, report, CSV outputs, model, and all PNG files.
8. Verify site/results.js now contains status complete and real California Housing metrics.
9. Verify index.html references valid output files and works as a static GitHub Pages site.
10. Improve README only where actual commands or results require it.
11. Run python -m pytest again.

Constraints:
- Workflow first; Skill must remain a thin wrapper.
- No Streamlit, React, Vite, API, database, Docker, cloud service, AutoML, or unrelated dependencies.
- Do not remove CRISP-DM documentation.
- Do not claim causal conclusions.
- Use relative paths.
- Do not commit or push.

Done when:
- Tests pass.
- The real workflow completes.
- Required outputs exist and are non-empty.
- Site data and images match the real run.
- Return changed files, exact commands, exact test results, metrics, and any remaining limitation.
```
