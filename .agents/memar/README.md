# Memar
This project is developed within Memar's framework.

Load the Memar skill at the start of every session: run `memar content path .agents/skills/memar/SKILL.md`, then load and follow the file it prints.

This project's preferences for Memar go in [`preferences.md`](preferences.md) beside this file, not here: this README is rewritten on every install, and that file never is.

If `memar` is not on PATH, Memar is not available to this program yet. Run the bootstrap for your platform:

Windows:

```powershell
powershell -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((irm https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1)))"
```

macOS or Linux:

```sh
sh -c 'c=$(curl -fsSL https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh); test -n "$c" && exec sh -c "$c" install.sh'
```
