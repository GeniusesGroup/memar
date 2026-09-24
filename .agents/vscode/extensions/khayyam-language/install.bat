@echo off
echo Installing Khayyam Language Extension for VS Code...

:: Path to the user's system extensions folder
set EXT_DIR="%USERPROFILE%\.vscode\extensions\khayyam-language"

:: Create folder if it does not exist
mkdir %EXT_DIR% 2>nul

:: Copy all files in the current folder to the extensions path
xcopy /E /Y /I . %EXT_DIR%

echo.
echo Installation Complete! 
echo Please restart VS Code to apply the Khayyam syntax highlighting.
pause
