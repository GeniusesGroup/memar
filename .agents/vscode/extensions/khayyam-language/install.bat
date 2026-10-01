@echo off
setlocal
REM Installing the Khayyam Language extension for VS Code.
REM
REM The extension folder must be named <publisher>.<name>-<version>, the form the
REM editor's extension scanner and the marketplace use. The name is read from
REM package.json so it cannot drift from the manifest's own version.

echo Installing Khayyam Language Extension for VS Code...

where node >nul 2>nul
if errorlevel 1 (
    echo Node.js is required to compute the extension folder name from package.json.
    echo Expected folder name: geniusesgroup.khayyam-0.1.0
    echo   under %%USERPROFILE%%\.vscode\extensions
    exit /b 1
)

for /f "usebackq delims=" %%i in (`node -p "const p=require('./package.json');p.publisher.toLowerCase().replace(/\./g,'')+'.'+p.name.toLowerCase()+'-'+p.version"`) do set EXT_ID=%%i

set EXT_DIR=%USERPROFILE%\.vscode\extensions\%EXT_ID%

echo Extension id: %EXT_ID%
echo Target folder: %EXT_DIR%

mkdir "%EXT_DIR%" 2>nul
xcopy /E /Y /I . "%EXT_DIR%"
if errorlevel 1 (
    echo Copy failed.
    exit /b 1
)

echo.
echo Installation complete. Reload the window (Developer: Reload Window) to apply.
endlocal
pause
