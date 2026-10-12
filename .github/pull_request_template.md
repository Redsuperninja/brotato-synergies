## What
<!-- Plain English: what does this change do for players? -->

## Why
<!-- What problem does it solve? -->

## How to test in-game
<!-- Characters, solo or co-op, devices, what to press, what the stat panel / godot.log should show. -->

## Roadmap item
<!-- e.g. #6 Playtest v0.40.0 -->

## Checklist
- [ ] Small and single-purpose
- [ ] `python tools/check_config.py` passes, `gdparse` clean on changed `.gd` files, `./build-zip.sh` builds
- [ ] `MOD_VERSION` and `manifest.json` bumped together; CHANGELOG line added
- [ ] No game code (`.game-src/`), game assets or the VFX pack committed; original author's credit intact
- [ ] game-designer pass (if any skill, faction or stat number changed)
- [ ] security-reviewer pass (if publishing, file writes, assets or licences changed)
