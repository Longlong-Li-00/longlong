@echo off
setlocal

echo Generating site data...
python tools\generate_site_data.py
if errorlevel 1 (
  echo.
  echo Failed to generate site data.
  exit /b 1
)

echo.
echo Starting local server...
echo Open http://127.0.0.1:8020/index.html
echo Do not close this window while previewing.
echo Do not preview by double-clicking HTML files.
echo.

python -m http.server 8020
