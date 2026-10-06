@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run powershell -ExecutionPolicy Bypass -File environment\setup.ps1 first.
  exit /b 1
)
set "JUPYTER_PREFER_ENV_PATH=1"
".venv\Scripts\python.exe" -m jupyterlab --ServerApp.root_dir="%CD%" %*
