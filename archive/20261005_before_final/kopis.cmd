@echo off
setlocal
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
set "KOPIS_ROOT=%~dp0"
set "KOPIS_PYTHON=%USERPROFILE%\.cache\grad-notebook-venv\Scripts\python.exe"
if not exist "%KOPIS_PYTHON%" set "KOPIS_PYTHON=python"
"%KOPIS_PYTHON%" -u -c "import json,os,sys; from pathlib import Path; root=Path(os.environ['KOPIS_ROOT']); p=next(root.glob('notebooks/07_KOPIS_*.ipynb')); nb=json.loads(p.read_text(encoding='utf-8')); scope={'KOPIS_PROJECT_ROOT':str(root)}; [exec(compile(''.join(c['source']),str(p), 'exec'),scope) for c in nb['cells'] if c['cell_type']=='code' and 'kopis-runtime' in c.get('metadata',{}).get('tags',[])]; sys.exit(scope['kopis_cli_main'](sys.argv[1:]))" %*
exit /b %errorlevel%
