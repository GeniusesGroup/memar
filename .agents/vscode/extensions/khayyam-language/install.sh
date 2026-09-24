#!/bin/bash
echo "Installing Khayyam Language Extension for VS Code..."

# Path to the user's system extensions folder
EXT_DIR=~/.vscode/extensions/khayyam-language

# Create folder and copy files
mkdir -p "$EXT_DIR"
cp -r ./* "$EXT_DIR"

echo "Installation Complete! Please restart VS Code."
