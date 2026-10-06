param([string]$Python = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not $Python) { $Python = Join-Path $PSScriptRoot 'python\python.exe' }
& $Python -m venv --copies (Join-Path $projectRoot '.venv')
if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 environment creation failed.' }
& $venvPython -c "import sys; assert sys.version_info[:2] == (3, 12), 'Python 3.12 is required'"
if ($LASTEXITCODE -ne 0) { throw 'Incorrect Python version.' }
$wheelDirectory = Join-Path $PSScriptRoot 'wheels'
if (Test-Path -LiteralPath $wheelDirectory) {
    & $venvPython -m pip install --no-index --find-links $wheelDirectory -r (Join-Path $PSScriptRoot 'requirements-lock.txt')
} else {
    & $venvPython -m pip install -r (Join-Path $PSScriptRoot 'requirements-lock.txt')
}
if ($LASTEXITCODE -ne 0) { throw 'Package installation failed.' }
& $venvPython -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Package dependency check failed.' }
& $venvPython -m ipykernel install --prefix (Join-Path $projectRoot '.venv') --name python3 --display-name 'graduation-project (Python 3.12)'
if ($LASTEXITCODE -ne 0) { throw 'Kernel installation failed.' }
& (Join-Path $PSScriptRoot 'node\node.exe') --version
if ($LASTEXITCODE -ne 0) { throw 'The included Node runtime is missing or invalid.' }
Write-Host 'Ready. Run start-jupyter.cmd from the project root.'
