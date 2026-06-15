# AGENTS.md

## Project goal

Build and maintain a reusable, beginner-readable CRISP-DM regression workflow. The primary verified dataset is California Housing. The public repository must demonstrate both execution and learning value.

## Required commands

```powershell
python -m pip install -r requirements.txt
python -m pytest
python run_workflow.py --config configs/california_housing.json
```

## Engineering boundaries

- Keep `run_workflow.py` as the main entry point.
- Keep dataset-specific values in `configs/`, not hard-coded throughout modules.
- Use scikit-learn `Pipeline` and `ColumnTransformer` so preprocessing is saved with the model.
- Preserve missing-value handling and categorical encoding.
- Use relative repository paths unless a test intentionally passes an absolute temporary path.
- Do not add Streamlit, React, Vite, a database, an API server, Docker, or cloud services unless the user separately approves them.
- Do not replace the main linear regression model with AutoML.
- Do not claim that model coefficients prove causal relationships.
- Do not commit or push unless the user explicitly approves the final reviewed state.

## Validation before reporting completion

1. Run `python -m pytest`.
2. Delete or ignore temporary smoke outputs.
3. Run the real California Housing workflow when internet or `data/housing.csv` is available.
4. Confirm every file referenced by `index.html` exists.
5. Confirm `site/results.js` contains real workflow results rather than `not-run`.
6. Report exact commands and results.
