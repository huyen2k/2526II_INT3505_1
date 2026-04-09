@echo off
setlocal

set "ROOT=%~dp0"

echo ==================================================
echo OpenAPI Comparison demo launcher
echo Press Ctrl+C in each server window when you want to move to the next one.
echo ==================================================
echo.

echo [1/4] OpenAPI
pushd "%ROOT%openapi"
py -m pip install -r requirements.txt
py app.py
popd
echo.

echo [2/4] API Blueprint
pushd "%ROOT%api-blueprint"
py -m pip install -r requirements.txt
py app.py
popd
echo.

echo [3/4] RAML
pushd "%ROOT%raml"
py -m pip install -r requirements.txt
py app.py
popd
echo.

echo [4/4] TypeSpec
pushd "%ROOT%typespec"
py -m pip install -r requirements.txt
py app.py
popd
echo.

echo Done.
pause