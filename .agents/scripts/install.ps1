<#
.SYNOPSIS
Put Memar on this machine, and record where it lives.

.DESCRIPTION
This is the bootstrap, and the only file of Memar meant to be run on its own.
It assumes nothing but PowerShell. Every other file in the folder is written to
be run from a Memar checkout, with its siblings on disk beside it, so this
script's own job is to obtain that checkout and then run it from there.

  Install (clone) Memar into a folder you name, or into Memar in your home:

      .agents\scripts\install.ps1                 # Memar in your home
      .agents\scripts\install.ps1 -Path C:\Memar

  Register a Memar folder that already exists, without moving or copying
  anything:

      .agents\scripts\install.ps1 -Register C:\Users\you\GeniusesGroup\memar

  Ask whether a folder would be refused, without installing anything:

      .agents\scripts\install.ps1 -Check C:\Temp\Memar

What it does, in order, printing each step:

  1. Prerequisites - git and Python. If the platform offers a package manager
     that has them, it installs them; if it does not, it says so and stops.
  2. The architecture - Memar is a git checkout, so this step obtains one: a
     `git clone --depth 1` of the repository into Memar in your home, a
     `git pull` of the checkout already in a folder you named, or a checkout that
     is already here and is used as it is. A run that named no folder fetches
     nothing when it can find a checkout to run from, because whether Memar is
     already on this machine is a question for the installer to ask against the
     record, and not for this script to answer from the copy of the variable this
     session holds. No file of the architecture is fetched over the network and
     none is run from memory, so a first run costs one clone and nothing else. A
     folder you named that already holds something else is refused, and nothing
     is deleted.
  3. The installer - install.py, run from the checkout step 2 settled on, with
     the rest of the architecture beside it. The installer is the only thing
     that decides anything about Memar, including whether Memar is already here:
     it reports an existing install and stops, reports a value that names no
     Memar repository and leaves it alone, refuses a folder under the temporary
     directory, and otherwise writes MEMAR_ROOT, makes the shortcut, and
     installs the editor extensions that checkout ships.

One mechanism decides where Memar lives: the MEMAR_ROOT environment variable,
written at install time by the installer and read literally by everything. No
per-OS location, no second resolution order, no fallback - this script decides
where the checkout is, and never whether one is a Memar repository nor what the
record of the variable says: both belong to the installer, which asks the
modules that hold them.

Memar is never installed into a temporary directory: a copy there is
machine-local and does not survive, and the installer refuses such a target.

-Check obtains nothing, so it needs an architecture to ask: this script answers
with the checkout it is in, or the one the variable names. A machine that has
neither has no answer to give, and this script says so and stops.

MEMAR_ROOT takes effect for programs started *after* it is written. Other
programs - your editor, your shell, this session's parent - must be restarted
before they see it: a running program does not read a new value. This script's
own output does not need restarting.

.PARAMETER Path
Clone Memar into this folder and register it. Default: Memar in your home
directory. A run that names no folder, run from a checkout, uses that checkout
instead of fetching one.

.PARAMETER Register
Register this existing folder instead of cloning. It must be a Memar
repository; anything else is refused, so MEMAR_ROOT is never pointed at an
arbitrary directory.

.PARAMETER Check
Say whether this folder would be refused as temporary, and stop. Nothing is
cloned and nothing is written.

.PARAMETER Help
Print this text.
#>
[CmdletBinding()]
param(
    [string]$Path,
    [string]$Register,
    [string]$Check,
    [switch]$Help
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepositoryUrl = "https://github.com/GeniusesGroup/memar.git"
$BootstrapUrl = "https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1"
# Where the installer lives inside a checkout, and where this bootstrap lives
# inside one. The pair is what makes "the architecture is here" one question.
$ArchitectureEntry = ".agents/scripts/install.py"
$BootstrapEntry = "install.ps1"
# The folder a run that named none obtains the architecture into. The installer's
# own target module holds the same name, and the two are pinned to each other.
$InstallDirname = "Memar"

function Write-Step([string]$Message) { Write-Output "==> $Message" }
function Write-Note([string]$Message) { Write-Output "    $Message" }
function Write-Err([string]$Message) {
    # Not Write-Error: $ErrorActionPreference = "Stop" would turn a deliberate
    # failure message into an exception the caller might swallow.
    [Console]::Error.WriteLine($Message)
}
function Fail([string]$Message) {
    Write-Err "error: $Message"
    exit 1
}

# Each attempt is reported, and the next one is tried when it fails, so a machine
# with two package managers still ends up installed rather than told to give up.
function Invoke-Attempt([scriptblock]$Attempt, [string]$Description) {
    Write-Note "trying: $Description"
    if (& $Attempt) { return $true }
    Write-Note "that did not manage it"
    return $false
}

# A package manager installs into the user or machine environment; this process
# does not learn that until something restarts, so read it back and adopt it.
function Update-ProcessPath {
    $parts = @()
    foreach ($name in @("Machine", "User")) {
        $value = [System.Environment]::GetEnvironmentVariable("PATH", $name)
        if ($value) { $parts += $value }
    }
    if ($parts.Count -gt 0) { $env:PATH = ($parts -join ";") }
}

function Find-Python {
    foreach ($candidate in @("python", "python3", "py")) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if (-not $command) { continue }
        # A name on PATH is not a Python: `py` on Windows and `python` on a POSIX
        # box can be something else entirely, so ask it to run something.
        & $candidate -c "pass" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { return $candidate }
    }
    return $null
}

if ($Help) {
    if (-not $PSCommandPath) {
        Fail "-Help needs this file; fetch it from $BootstrapUrl and run it from there."
    }
    # The comment-based help block at the top of this file is the documentation;
    # print it (minus the block delimiters) rather than maintaining a second copy.
    $text = Get-Content -LiteralPath $PSCommandPath
    $end = ($text | Select-String -Pattern "^#>" | Select-Object -First 1).LineNumber
    if (-not $end) { $end = 2 }
    $text[1..($end - 2)] | ForEach-Object { $_ -replace "^#\.", "." -replace "^# ?", "" } | Write-Host
    exit 0
}

if ($Path -and $Register) {
    Fail "give either -Path (clone into it) or -Register (use it as it is), not both."
}

# Read here, because obtaining the architecture needs the folder to obtain it
# into. The installer still decides what the words mean: it is handed one mode
# and one folder, and nothing else.
$Mode = ""
$Target = ""
if ($Check) { $Mode = "check"; $Target = $Check }
elseif ($Path) { $Mode = "install"; $Target = $Path }
elseif ($Register) { $Mode = "register"; $Target = $Register }
# A run that named no folder installs into the default one; a check that named
# one asks about the one it named.
if (-not $Target) { $Target = Join-Path $HOME $InstallDirname }

# --- 1. prerequisites ------------------------------------------------------

Write-Step "Prerequisites"

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Note "git: $((Get-Command git).Source)"
} else {
    $installed = Invoke-Attempt { winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements } "winget install Git.Git"
    if (-not $installed) { $installed = Invoke-Attempt { scoop install git } "scoop install git" }
    if (-not $installed) { $installed = Invoke-Attempt { choco install git -y } "choco install git" }
    if (-not $installed) {
        Fail "`git` is not on PATH and this platform offers no way found here to install it. Install Git, then re-run. (A folder that already holds Memar needs no git: -Register PATH.)"
    }
    Update-ProcessPath
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Fail "`git` was installed but is not on PATH in this session. Open a new terminal and re-run."
    }
    Write-Note "git: $((Get-Command git).Source)"
}

$python = Find-Python
if (-not $python) {
    $installed = Invoke-Attempt { winget install --id Python.Python.3 -e --accept-package-agreements --accept-source-agreements } "winget install Python.Python.3"
    if (-not $installed) { $installed = Invoke-Attempt { scoop install python } "scoop install python" }
    if (-not $installed) { $installed = Invoke-Attempt { choco install python -y } "choco install python" }
    if (-not $installed) {
        Fail "Python 3 is not on PATH and this platform offers no way found here to install it. Install Python 3, then re-run."
    }
    Update-ProcessPath
    $python = Find-Python
    if (-not $python) {
        Fail "Python 3 was installed but is not on PATH in this session. Open a new terminal and re-run."
    }
}
Write-Note "python: $((Get-Command $python).Source)"

# The folder, as the installer will read it: `~` and `$NAME` expanded by the same
# rule the installer applies, asked of the same interpreter, so the folder this
# script obtains and the folder the installer records cannot come to disagree.
function ConvertTo-AbsolutePath([string]$Value) {
    & $python -c 'import os,sys;from pathlib import Path;print(Path(os.path.expandvars(sys.argv[1])).expanduser().absolute())' $Value
}

# --- 2. the architecture ---------------------------------------------------

# The checkout this script is in, when it is a file in one: this file and the
# installer beside it are how a checkout is recognized from the outside, and
# two levels up from the scripts folder is the repository root.
$OwnCheckout = $null
if ($PSCommandPath) {
    $Here = Split-Path -Parent $PSCommandPath
    if ((Test-Path -LiteralPath (Join-Path $Here $BootstrapEntry) -PathType Leaf) -and
        (Test-Path -LiteralPath (Join-Path $Here "install.py") -PathType Leaf)) {
        $OwnCheckout = Split-Path -Parent (Split-Path -Parent $Here)
    }
}

# The architecture is at ROOT when the installer is inside it. Not the question
# whether ROOT is a Memar repository: that belongs to the installer.
function Test-Architecture([string]$Root) {
    if (-not $Root) { return $false }
    return Test-Path -LiteralPath (Join-Path $Root $ArchitectureEntry) -PathType Leaf
}

# An architecture this run can name without obtaining one, for a mode that must
# not obtain: the checkout this script is in, or the one the variable names.
$Recorded = $env:MEMAR_ROOT
$AtHand = $null
if (Test-Architecture $OwnCheckout) { $AtHand = $OwnCheckout }
elseif (Test-Architecture $Recorded) { $AtHand = $Recorded }

$Target = ConvertTo-AbsolutePath $Target
$ObtainIt = $false

Write-Step "The architecture"

switch ($Mode) {
    "check" {
        if (-not $AtHand) {
            Fail "there is no Memar checkout on this machine to ask, and -Check obtains nothing: run this script from a Memar checkout, or install Memar first. Nothing was installed and nothing was written."
        }
        Write-Note "asked from the checkout at $AtHand"
        $Checkout = $AtHand
    }
    "register" {
        if (-not (Test-Architecture $Target)) {
            Fail "$Target holds no Memar checkout to run ($ArchitectureEntry is not in it). Nothing was changed and nothing was deleted."
        }
        Write-Note "the checkout at $Target, as it is"
        $Checkout = $Target
    }
    "install" {
        $Checkout = $Target
        $ObtainIt = $true
    }
    default {
        # Nothing was named, and nothing is fetched: whether Memar is already on
        # this machine is the installer's question, asked against the record, and
        # a script reading this session's copy of the variable could answer it
        # differently from the record. So this step only needs a checkout to run
        # that question from, and a run that named a folder is the one that
        # fetches.
        if ($AtHand -and -not $Recorded) {
            Write-Note "the checkout this script is in, at $AtHand"
            $Checkout = $AtHand
        } elseif (Test-Architecture $Target) {
            Write-Note "the checkout already at $Target"
            $Checkout = $Target
        } else {
            Write-Note "cloning $RepositoryUrl"
            & git clone --depth 1 $RepositoryUrl $Target
            if ($LASTEXITCODE -ne 0) {
                Fail "`git clone --depth 1 $RepositoryUrl $Target` failed. Nothing was deleted. If another install is running on this machine, wait for it and run this again."
            }
            $Checkout = $Target
        }
    }
}

# A folder this run was told about is settled here: pulled when it holds a
# checkout, refused when it holds something else. A run that named no folder has
# settled nothing by fetching, and the installer below answers for it.
if ($ObtainIt) {
    if (Test-Path -LiteralPath (Join-Path $Checkout ".git")) {
        Write-Note "updating the checkout at $Checkout"
        & git -C $Checkout pull --ff-only
        if ($LASTEXITCODE -ne 0) {
            Fail "the update failed; the checkout at $Checkout is unchanged."
        }
    } elseif (Test-Architecture $Checkout) {
        Write-Note "$Checkout holds Memar but is not a git checkout, so it cannot be updated"
    } else {
        Fail "$Checkout already exists and holds no Memar checkout ($ArchitectureEntry is not in it). Nothing was changed and nothing was deleted. Name another folder with -Path, or register a checkout you already have with -Register."
    }
}

# --- 3. the installer ------------------------------------------------------

Write-Step "The installer"
Write-Note "run from the checkout at $Checkout"

# The installer's own arguments, rebuilt: the mode this run settled on, and the
# folder it settled on. A run that named no folder is handed nothing, so the
# installer reports a Memar that is already here rather than recording again.
$forwarded = @()
switch ($Mode) {
    "check" { $forwarded = @("--check", $Target) }
    { $_ -in @("install", "register") } { $forwarded = @("--register", $Checkout) }
}

& $python (Join-Path $Checkout $ArchitectureEntry) @forwarded
exit $LASTEXITCODE
