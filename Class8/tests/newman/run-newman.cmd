@echo off
setlocal

rem Always run from Class8 root so relative paths resolve correctly.
pushd "%~dp0\..\.."

set COLLECTION=tests\postman\products-crud.postman_collection.json
set ENVIRONMENT=tests\postman\class7-local.postman_environment.json
set REPORT=tests\reports\newman-report.json

if not exist tests\reports (
  mkdir tests\reports
)

echo Running Newman suite for 5 product endpoints...
newman run %COLLECTION% -e %ENVIRONMENT% -n 10 --delay-request 50 -r cli,json --reporter-json-export %REPORT%

if %ERRORLEVEL% NEQ 0 (
  echo Newman finished with failures.
  popd
  exit /b %ERRORLEVEL%
)

echo Newman run completed successfully.
echo JSON report saved to %REPORT%
popd
