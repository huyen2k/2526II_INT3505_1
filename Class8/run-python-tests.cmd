@echo off
setlocal

pushd "%~dp0"

if not exist ".venv" (
  echo Creating virtual environment...
  py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip >nul
python -m pip install -r requirements-test.txt

echo Running unit + integration tests...
python -m pytest tests\unit tests\integration -q
set TEST_EXIT_CODE=%ERRORLEVEL%

popd
exit /b %TEST_EXIT_CODE%
