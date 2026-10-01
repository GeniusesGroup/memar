#!/bin/bash
# Installing the Khayyam Language extension for VS Code.
#
# The extension folder must be named <publisher>.<name>-<version>, the form the
# editor's extension scanner and the marketplace use. The name is read from
# package.json so it cannot drift from the manifest's own version.

set -euo pipefail

echo "Installing Khayyam Language Extension for VS Code..."

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required to compute the extension folder name from package.json." >&2
  echo "Expected folder name: geniusesgroup.khayyam-0.1.0" >&2
  echo "  under \$HOME/.vscode/extensions" >&2
  exit 1
fi

EXT_ID="$(node -p "const p=require('./package.json');p.publisher.toLowerCase().replace(/\./g,'')+'.'+p.name.toLowerCase()+'-'+p.version")"
EXT_DIR="$HOME/.vscode/extensions/$EXT_ID"

echo "Extension id: $EXT_ID"
echo "Target folder: $EXT_DIR"

mkdir -p "$EXT_DIR"
cp -r ./* "$EXT_DIR"/

echo
echo "Installation complete. Reload the window (Developer: Reload Window) to apply."
