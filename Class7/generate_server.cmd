@echo off
REM Generate Flask backend stub from OpenAPI spec
openapi-generator-cli generate -i openapi.yaml -g python-flask -o generated-server
echo Done. Generated server is in generated-server/
