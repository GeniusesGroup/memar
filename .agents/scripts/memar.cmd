@echo off
rem memar - the one command a person or an agent types to reach Memar.
rem
rem This shim exists because a Windows shell will not run a file that has no
rem known extension, and `memar` must be typeable without its extension. It
rem adds nothing: the Python file beside it does the routing, and the tools it
rem routes to declare their own interfaces. See .agents/scripts/README.md.

setlocal
set "MEMAR_LAUNCHER=%~dp0memar"
if not exist "%MEMAR_LAUNCHER%" (
    echo memar: the launcher is not beside this shim. Re-fetch Memar rather than working around it. 1>&2
    exit /b 2
)
python "%MEMAR_LAUNCHER%" %*
exit /b %ERRORLEVEL%
