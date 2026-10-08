# Memar
This project is developed with Memar's framework as follow to its method and mindset.

Load the Memar skill at the start of every session. Run `memar content path .agents/skills/memar/SKILL.md` and load the file it prints.

If `memar` is not defined on this system, Memar is not installed. Run the bootstrap for this platform from GitHub and follow the install script's output carefully:

```
powershell -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((irm https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1)))"   # Windows
sh -c "$(curl -fsSL https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh)" install.sh   # POSIX
```
