@echo off
rem memar - the one command a person or an agent types to reach Memar.
rem
rem This shim exists because a Windows shell will not run a file that has no
rem known extension, and `memar` must be typeable without its extension. It
rem adds nothing: the Python file beside it does the routing, and the tools it
rem routes to declare their own interfaces.
rem
rem The reason is a property of how Windows resolves a bare name, not of
rem Python: cmd.exe appends each extension in PATHEXT to the name typed, and
rem CreateProcess below it appends .exe - so a file with no extension cannot
rem be named by either layer, while a shell that runs extensionless files
rem never consults PATHEXT, which is why the same file works under bash, Git
rem Bash, and every POSIX shell with no shim beside it.
rem
rem The alternatives are not free: adding .PY to PATHEXT works only if a file
rem named memar.py also exists, mutates the machine's environment from outside
rem the installer's control, and does nothing for bash; a symlink named
rem memar.exe does not work at all, because no current Python looks for a
rem script beside the name it was invoked under. What pip and uv do instead is
rem compile a real .exe at install time - that is the shape to expect once
rem this repository has an executable of its own, and until then this shim is
rem what stands in for it.

setlocal
set "MEMAR_LAUNCHER=%~dp0memar"
if not exist "%MEMAR_LAUNCHER%" (
    echo memar: the launcher is not beside this shim. Re-fetch Memar rather than working around it. 1>&2
    exit /b 2
)
python "%MEMAR_LAUNCHER%" %*
exit /b %ERRORLEVEL%
