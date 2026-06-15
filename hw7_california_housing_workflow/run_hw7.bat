@echo off
setlocal
cd /d "%~dp0"
python run_workflow.py --config configs\california_housing.json
if errorlevel 1 (
  echo.
  echo HW7 workflow failed. Review the error above.
  pause
  exit /b 1
)
echo.
echo HW7 workflow completed.
pause
