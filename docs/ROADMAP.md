# Roadmap

## Done
- [x] **#1 Fork identity:** own mod id (`Redsuperninja-Synergies`), credit to hhoangg kept, marked
  incompatible with the original, Workshop item reset to create a new one.
- [x] **#2 Stats can't go negative:** buffs and faction traits through the game's TempStats (ADR 0001),
  real stat keys for Damage and XP, nerfs clamped at 0.
- [x] **#3 Every character has a faction:** Iron Fists and All-Rounders added; Ranger, Sick, Loud and
  Farmer joined existing factions; nerfs spread across stats.
- [x] **#4 Fixes found in review:** enemy slows/freezes no longer stick, material drops pay out, curse
  cloud damage credited to the caster, Glutton heals itself, Windows-friendly build.
- [x] **#5 Project practices:** agents, workflow, checks, pre-push hook, templates.

## Next
- [ ] **#6 Playtest v0.40.0** in co-op with the script in `docs/testing/` and fix what it finds.
- [ ] **#7 Publish the fork** to the Workshop (new item), then set `WS_ITEM` in `sync-to-mac.sh` and the
  item id in the README.
- [ ] **#8 Balance pass with real play data:** the Damage and XP buffs (and Damage nerfs) work now for
  the first time, so skills like Wounded, Baby and Multitasker hit harder than before.
- [ ] **#9 Vietnamese text** for the two new factions' descriptions and anything added since.
- [ ] **#10 Split `synergies_controller.gd`** (~2,750 lines) along its jobs: stats, enemy effects, casting.
