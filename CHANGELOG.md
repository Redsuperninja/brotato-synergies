# Changelog

This fork's changes. The original mod's history is in the git log up to commit `8a819ba` and on
[hhoangg/brotato-synergies](https://github.com/hhoangg/brotato-synergies).

## 0.40.0 — first release of Fixed Coop Synergies
- **Fork:** now its own mod, **Fixed Coop Synergies** (`Redsuperninja-FixedCoopSynergies`), by Redsuperninja, based on Co-op Synergies by
  hhoangg (byptah). Don't enable it together with the original (the mod list marks them incompatible).
  Its settings are saved separately.
- **Fixed: stats going negative.** Ending a buff could leave Dodge, Speed or Armor below where they
  started (Dodge at about -900%), and some buffs gave 100% Dodge while they lasted. Every skill buff and
  faction bonus now uses the game's own temporary-stat system, so it ends exactly where it started and
  can never carry into the shop or your save.
- **Fixed: Damage and XP Gain buffs did nothing**, and nor did Damage nerfs. They now work. Attack speed,
  crit, range and engineering buffs now reach your weapons and turrets too, not only the stat panel.
- **Fixed:** skill damage now scales with your Damage stat as intended (it read the wrong number before).
- **Factions:** every character now has at least one. New **Iron Fists** (Brawler, One-Armed, Dwarf,
  Ogre) and **All-Rounders** (Generalist, Well-Rounded, Multitasker, Vagabond); Ranger joins The Wild,
  Sick joins The Damned, Loud joins Reckless, Farmer joins Late Bloomers. New pair: Hunter + Ranger.
- **Faction nerfs never push a stat below 0**, are a little smaller, are spread across different stats
  (Caretakers now cost Attack Speed, Late Bloomers cost Speed), and never touch Harvesting.
- **Harvesting from a skill** lasts until the wave ends, because that's when Harvesting pays out.
- **Glutton's Devour** heals only Glutton, for more (25 → 65 HP across tiers, plus wave growth).
- **Fixed:** enemies hit by a freeze and a slow at the same time could stay frozen, slowed or tinted
  for the rest of the wave. **Fixed:** Saver's and Buccaneer's material drops never paid out.
  **Fixed:** Creature's curse cloud credited its damage to player 1.
- For developers: `./build-zip.sh` works on Windows, `tools/check_config.py` checks the content, and
  `tools/game_source.py` reads the game's own scripts for reference.
- New Workshop page and thumbnail; the first upload is private for playtesting. `publish-steamcmd.sh` and `sync-to-workshop.sh` (was `sync-to-mac.sh`) work on Windows, and publishing runs `tools/check_config.py` first.
