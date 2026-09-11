@echo off
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
 echo Node.js 20 or newer is required. Install Node.js, then open this file again.
 pause
 exit /b 1
)
echo Open http://127.0.0.1:4173 in your browser.
echo Run npm install once to install the engine for offline use.
node tools/serve.mjs
pause
