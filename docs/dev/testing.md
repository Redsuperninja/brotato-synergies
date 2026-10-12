# Testing

There is no way to run the game's code outside the game, so checking has three layers. Run all three
before asking for a review.

## 1. Static checks (no game needed)

```bash
python tools/check_config.py
```

Checks that every character has a skill, an icon, flavour text and a faction; every stat key is one the
game tracks; nerfs are negative and never touch Harvesting; factions have a colour and a legend slot;
and the versions in `config.gd` and `manifest.json` match. Exit code 1 on any error.

**GDScript parse check.** One-time setup (a Godot 3 parser in its own virtual environment):

```bash
python -m venv .venv-tools
.venv-tools/Scripts/pip install "gdtoolkit==3.*" "setuptools<70"   # macOS/Linux: .venv-tools/bin/pip
```

Then `.venv-tools/Scripts/gdparse <file.gd>` for every script you changed. It catches syntax errors
(a single one stops the whole mod loading), not wrong names or types.

## 2. Build

```bash
./build-zip.sh                    # test build: TEST_MODE on
BUILD_RELEASE=1 ./build-zip.sh    # release build: TEST_MODE off
```

Both must succeed and leave `config.gd` unchanged. Without `zip` (Git Bash on Windows) the script uses
`tools/zip_mod.py` instead.

## 3. In-game pass (the owner)

Brotato loads Workshop mods only, so the build has to reach your Workshop folder (see the README's
"Local development loop"; on Windows it is
`C:\Program Files (x86)\Steam\steamapps\workshop\content\1942280\<item id>`). Use a **test build**:
skills unlock at level 1, cooldowns are short, factions activate with one member and buffs last 20s so
you can pause and read the stat panel.

Then read `%APPDATA%\Brotato\logs\godot.log`:
- `[Synergies] loaded v<version>` and no `SCRIPT ERROR` above it;
- a `CAST` line per cast, `[stat] pi=… +N` when a buff applies and the matching `-N` when it expires.

The step-by-step script for the current release is in [`../testing/`](../testing/).
