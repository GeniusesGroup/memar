#!/bin/sh
# For license and copyright information please see the LEGAL file in the code repository

# Put Memar on this machine.
#
#   ./install.sh                     install into ~/Memar
#   ./install.sh --path ~/Memar      install into a folder you name
#   ./install.sh --register ~/src/memar
#                                    use a Memar checkout you already have
#   ./install.sh --check /tmp/Memar  would a folder be refused? installs nothing
#   ./install.sh --project-path ~/work/app
#                                    also put Memar into that project
#
# What it does: makes sure git and Python are here, obtains a Memar checkout,
# and hands the run to Memar's installer, `memar install`, which puts Memar on
# this machine, into the project you name with --project-path, and into the AI agent
# apps on this machine. The folder you run it from is never read: with no
# --project-path, no project is written, and the run says so. Each step prints what it did. Running it again is safe and costs
# nothing.
#
# What you must do afterwards: this script prints one command this program can
# run at once, so it does not need a restart to load the skill, and you still
# restart your shell and your editor before they see `memar` on PATH, because a
# program already running when the variable was written does not read it.
#
# Options:
#   --path PATH      clone Memar into PATH and register it (default: ~/Memar, or
#                    the checkout this script is in)
#   --register PATH  register PATH as it is; it must be a Memar repository
#   --check PATH     say whether PATH would be refused as temporary, and stop
#   --project-path PATH
#                    put Memar into the project at PATH, a folder; it needs no
#                    earlier registration, and a project is never named by a word here
#   --help           print this text
#
# Exit status: 0 when MEMAR_ROOT points at a Memar repository, 1 otherwise.

# The rest of this file is addressed to whoever opens it, and --help stops at the
# blank line above. Everything below is why the run is shaped this way; a person
# installing Memar has no use for it, and printing it to them would make the help
# output a second copy of it that nobody maintains.
#
# This is the bootstrap, and the only file of Memar meant to be run on its own.
# It assumes nothing but a shell. Every other file here is written to be run
# from a Memar checkout, with its siblings on disk beside it, so this script's
# own job is to obtain that checkout and then run it from there.
#
# What it does, in order, printing each step:
#
#   1. Prerequisites — git and Python. If the platform offers a package manager
#      that has them, it installs them; if it does not, it says so and stops.
#   2. The architecture — Memar is a git checkout, so this step obtains one: a
#      `git clone --depth 1` of the repository into ~/Memar, a `git pull` of the
#      checkout already in a folder you named, or a checkout that is already here
#      and is used as it is. A run that named no folder fetches nothing when it
#      can find a checkout to run from, because whether Memar is already on this
#      machine is a question for the installer to ask against the record, and not
#      for this shell to answer from the copy of the variable this task holds.
#      No file of the architecture is fetched over the network and none is run
#      from memory, so a first run costs one clone and nothing else. A folder you
#      named that already holds something else is refused, and nothing is deleted.
#   3. The installer — `memar install`, run through the launcher of the checkout
#      step 2 settled on, with the rest of the architecture beside it. What it
#      decides and reports is declared by its own help; run `memar install
#      --help` for that interface.
#
# The launcher asks the daily update before every verb it routes, and the
# hand-off keeps it from starting one: MEMAR_NO_AUTO_UPDATE=1 is set for the
# installer's process alone. An update started mid-install would fetch into a
# checkout the install has not recorded yet — or into the one recorded before
# it — and refresh the skill copies and editor extensions the install is
# writing at the same moment.
#
# One mechanism decides where Memar lives: the MEMAR_ROOT environment variable,
# written at install time by the installer and read literally by everything. No
# per-OS location, no second resolution order, no fallback — this script decides
# where the checkout is, and never whether one is a Memar repository nor what the
# record of the variable says: both belong to the installer, which asks the
# modules that hold them.
#
# --check clones nothing, so it needs an architecture to ask: this script
# answers with the checkout it is in, or the one the variable names. A machine
# that has neither has no answer to give, and this script says so and stops.
#
# After a successful install this script prints one command the program that
# ran it can execute at once. That command is printed here, not written into a
# consuming project, because it is allowed to change.

set -eu

REPOSITORY_URL="https://github.com/GeniusesGroup/memar.git"
BOOTSTRAP_URL="https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh"
# Where the launcher the installer is reached through lives inside a checkout,
# and where this bootstrap lives inside one. The pair is what makes "the
# architecture is here" one question.
ARCHITECTURE_ENTRY="bundles/memar/memar"
BOOTSTRAP_ENTRY="install.sh"
# The folder a run with no arguments obtains the architecture into. The installer's
# own target module holds the same name, and the two are pinned to each other.
INSTALL_DIRNAME="Memar"


fail() {
    echo "error: $*" >&2
    exit 1
}

step() { echo "==> $*"; }
note() { echo "    $*"; }

# Read here, because obtaining the architecture needs the folder to obtain it
# into. The installer still decides what the words mean: it is handed one mode
# and one folder, and nothing else.
mode=""
target=""
project=""
expecting_value=""
for argument in "$@"; do
    if [ -n "$expecting_value" ]; then
        if [ "$expecting_value" = "project" ]; then project="$argument"; else target="$argument"; fi
        expecting_value=""
        continue
    fi
    case "$argument" in
        -h | --help)
            # The comment block at the top of this file, after the license
            # header and its blank line, is the documentation; print it rather
            # than keeping a second copy in the parser.
            [ -f "$0" ] ||
                fail "--help needs this file; fetch it from $BOOTSTRAP_URL and run it from there."
            awk 'help && /^#/ { sub(/^# ?/, ""); print; next } help { exit } /^$/ { help = 1 }' "$0"
            exit 0
            ;;
        --project-path)
            expecting_value="project"
            ;;
        --project-path=*)
            project="${argument#--project-path=}"
            ;;
        --project | --project=*)
            fail "this script is given a project's folder, not a name: use --project-path PATH"
            ;;
        --path)
            mode="install"
            expecting_value="yes"
            ;;
        --path=*)
            mode="install"
            target="${argument#--path=}"
            ;;
        --register)
            mode="register"
            expecting_value="yes"
            ;;
        --register=*)
            mode="register"
            target="${argument#--register=}"
            ;;
        --check)
            mode="check"
            expecting_value="yes"
            ;;
        --check=*)
            mode="check"
            target="${argument#--check=}"
            ;;
        *) fail "unknown argument '$argument'; try --help" ;;
    esac
done
[ -z "$expecting_value" ] ||
    fail "--path, --register, --check and --project-path each need a path; try --help"
# A run that named no folder installs into the default one; a check that named
# one asks about the one it named.
[ -n "$target" ] || target="$HOME/$INSTALL_DIRNAME"

on_windows() {
    case "$(uname -s 2>/dev/null || echo unknown)" in
        MINGW* | MSYS* | CYGWIN*) return 0 ;;
        *) return 1 ;;
    esac
}

# The places a Windows install of these lands, which PATH does not learn about
# until something restarts.
learn_windows_path() {
    on_windows || return 0
    for directory in \
        "/c/Program Files/Git/cmd" \
        "/c/Program Files/Git/bin" \
        "/c/Program Files/Python3" \
        "$LOCALAPPDATA/Programs/Python"; do
        if [ -d "$directory" ]; then
            case ":$PATH:" in
                *":$directory:"*) ;;
                *) PATH="$PATH:$directory" ;;
            esac
        fi
    done
    export PATH
}

# Each attempt is reported, and the next one is tried when it fails, so a machine
# with two package managers still ends up installed rather than told to give up.
attempt() {
    note "trying: $*"
    if "$@" >/dev/null 2>&1; then
        return 0
    fi
    note "that did not manage it"
    return 1
}

# --- 1. prerequisites ------------------------------------------------------

step "Prerequisites"

if command -v git >/dev/null 2>&1; then
    note "git: $(command -v git)"
elif on_windows; then
    attempt winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements ||
        attempt scoop install git ||
        attempt choco install git -y ||
        fail "\`git\` is not on PATH and this platform offers no way found here to install it. Install Git, then re-run. (A folder that already holds Memar needs no git: --register PATH.)"
    learn_windows_path
    command -v git >/dev/null 2>&1 ||
        fail "\`git\` was installed but is not on PATH in this shell. Open a new shell and re-run."
    note "git: $(command -v git)"
else
    attempt apt-get install -y git ||
        attempt dnf install -y git ||
        attempt pacman -S --noconfirm git ||
        attempt apk add git ||
        attempt brew install git ||
        attempt zypper -n install git ||
        fail "\`git\` is not on PATH and this platform offers no way found here to install it. Install Git, then re-run. (A folder that already holds Memar needs no git: --register PATH.)"
    command -v git >/dev/null 2>&1 ||
        fail "\`git\` was installed but is not on PATH in this shell. Open a new shell and re-run."
    note "git: $(command -v git)"
fi

find_python() {
    for candidate in python3 python py; do
        if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c pass >/dev/null 2>&1; then
            echo "$candidate"
            return 0
        fi
    done
    return 1
}

if PYTHON=$(find_python); then
    note "python: $(command -v "$PYTHON")"
elif on_windows; then
    attempt winget install --id Python.Python.3 -e --accept-package-agreements --accept-source-agreements ||
        attempt scoop install python ||
        attempt choco install python -y ||
        fail "Python 3 is not on PATH and this platform offers no way found here to install it. Install Python 3, then re-run."
    learn_windows_path
    PYTHON=$(find_python) ||
        fail "Python 3 was installed but is not on PATH in this shell. Open a new shell and re-run."
    note "python: $(command -v "$PYTHON")"
else
    attempt apt-get install -y python3 ||
        attempt dnf install -y python3 ||
        attempt pacman -S --noconfirm python ||
        attempt apk add python3 ||
        attempt brew install python3 ||
        attempt zypper -n install python3 ||
        fail "Python 3 is not on PATH and this platform offers no way found here to install it. Install Python 3, then re-run."
    PYTHON=$(find_python) ||
        fail "Python 3 was installed but is not on PATH in this shell. Open a new shell and re-run."
    note "python: $(command -v "$PYTHON")"
fi

# The folder, as the installer will read it: `~` and `$NAME` expanded by the same
# rule the installer applies, asked of the same interpreter, so the folder this
# script obtains and the folder the installer records cannot come to disagree.
absolute_path() {
    "$PYTHON" -c 'import os,sys;from pathlib import Path;print(Path(os.path.expandvars(sys.argv[1])).expanduser().absolute())' "$1"
}

# --- 2. the architecture ---------------------------------------------------

# The folder, named the way the installer will name it, because this step's own
# questions about it ("is a checkout there?") and the installer's have to be
# asked about one folder rather than two spellings of it.
target="$(absolute_path "$target")"

# The checkout this script is in, when it is a file in one: this file and the
# launcher beside it are how a checkout is recognized from the outside, and
# two levels up from the scripts folder is the repository root.
own_checkout=""
if [ -f "$0" ]; then
    here="$(dirname "$0")"
    if [ -f "$here/$BOOTSTRAP_ENTRY" ] && [ -f "$here/memar" ]; then
        own_checkout="$(cd "$here/../.." && pwd)"
    fi
fi

# The architecture is at ROOT when the launcher is inside it. Not the question
# whether ROOT is a Memar repository: that belongs to the installer.
holds_architecture() {
    [ -n "${1:-}" ] && [ -f "$1/$ARCHITECTURE_ENTRY" ]
}

# An architecture this run can name without obtaining one, for a mode that must
# not obtain: the checkout this script is in, or the one the variable names.
recorded="${MEMAR_ROOT:-}"
at_hand=""
if holds_architecture "$own_checkout"; then
    at_hand="$own_checkout"
elif holds_architecture "$recorded"; then
    at_hand="$recorded"
fi

obtain_it=""
step "The architecture"

case "$mode" in
    check)
        [ -n "$at_hand" ] ||
            fail "there is no Memar checkout on this machine to ask, and --check obtains nothing: run this script from a Memar checkout, or install Memar first. Nothing was installed and nothing was written."
        note "asked from the checkout at $at_hand"
        checkout="$at_hand"
        ;;
    register)
        checkout="$target"
        holds_architecture "$checkout" ||
            fail "$checkout holds no Memar checkout to run ($ARCHITECTURE_ENTRY is not in it). Nothing was changed and nothing was deleted."
        note "the checkout at $checkout, as it is"
        ;;
    install)
        checkout="$target"
        obtain_it="yes"
        ;;
    *)
        # Nothing was named, and nothing is fetched: whether Memar is already on
        # this machine is the installer's question, asked against the record, and
        # a shell reading this task's copy of the variable could answer it
        # differently from the record. So this step only needs a checkout to run
        # that question from, and a run that named a folder is the one that
        # fetches.
        if [ -n "$at_hand" ] && [ -z "$recorded" ]; then
            note "the checkout this script is in, at $at_hand"
            checkout="$at_hand"
        elif holds_architecture "$target"; then
            note "the checkout already at $target"
            checkout="$target"
        else
            note "cloning $REPOSITORY_URL"
            git clone --depth 1 "$REPOSITORY_URL" "$target" ||
                fail "\`git clone --depth 1 $REPOSITORY_URL $target\` failed. Nothing was deleted. If another install is running on this machine, wait for it and run this again."
            checkout="$target"
        fi
        ;;
esac

# A folder this run was told about is settled here: pulled when it holds a
# checkout, refused when it holds something else. A run that named no folder has
# settled nothing by fetching, and the installer below answers for it.
if [ -n "$obtain_it" ]; then
    if [ -d "$checkout/.git" ]; then
        note "updating the checkout at $checkout"
        git -C "$checkout" pull --ff-only ||
            fail "the update failed; the checkout at $checkout is unchanged."
    elif ! holds_architecture "$checkout"; then
        fail "$checkout already exists and holds no Memar checkout ($ARCHITECTURE_ENTRY is not in it). Nothing was changed and nothing was deleted. Name another folder with --path, or register a checkout you already have with --register."
    else
        note "$checkout holds Memar but is not a git checkout, so it cannot be updated"
    fi
fi

# --- 3. the installer ------------------------------------------------------

step "The installer"
note "run from the checkout at $checkout"

# The installer's own arguments, rebuilt: the mode this run settled on, and the
# folder it settled on. A run that named no folder is handed nothing, so the
# installer reports a Memar that is already here rather than recording again.
set --
case "$mode" in
    check)
        set -- --check "$target"
        ;;
    install | register)
        set -- --register "$checkout"
        ;;
esac
# The project is the folder the person named, handed on as an absolute path: the
# installer reads a path without any earlier registration, so a first run, with
# no record of projects yet, installs into it. It is never taken from the folder
# this script runs in.
if [ -n "$project" ] && [ "$mode" != "check" ]; then
    set -- "$@" --project-path "$(absolute_path "$project")"
fi
code=0
MEMAR_NO_AUTO_UPDATE=1 "$PYTHON" "$checkout/$ARCHITECTURE_ENTRY" install "$@" || code=$?
if [ "$code" -eq 0 ] && [ "$mode" != "check" ]; then
cat <<END
This program can go on without a restart. Load the skill by running the next line on its own:
"$PYTHON" "$checkout/$ARCHITECTURE_ENTRY" content path .agents/skills/memar/SKILL.md
END
fi
exit "$code"
