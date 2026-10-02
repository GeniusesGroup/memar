# Memar
`MEMAR_ROOT` names the Memar checkout on this machine. If it is unset, run the bootstrap from Memar's repository — it makes sure git and Python are here, then installs Memar and writes that variable:

```
powershell -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((irm https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.ps1)))"   # Windows
sh -c "$(curl -fsSL https://raw.githubusercontent.com/GeniusesGroup/memar/main/.agents/scripts/install.sh)" install.sh   # POSIX
```

Then restart your program: a program of your own that is already running keeps the value it was started with, while the scripts in the checkout that variable names read the platform's record of it and see it at once. Load `.agents/skills/memar/SKILL.md` from the checkout that variable names, and use the scripts in its `.agents/scripts/`. To put Memar into another project, run `install-agents.py` from that checkout, in that project.
