# Redsuperninja-Synergies — Co-op Synergies (Brotato mod)

Turns Brotato co-op into a team game: per-character **active skills**, faction **affinities**
(buff + nerf when related characters team up), and a **role** read on every character.

A fork of Co-op Synergies (`tato-Synergies`) by **hhoangg (byptah)**, who designed the mod, its
skills and its icons: <https://github.com/hhoangg/brotato-synergies>. Fork maintained by
**Redsuperninja**. Don't enable both mods at once.

- `mod_main.gd` — ModLoader entry point; spawns the persistent controller.
- `config.gd` — every tunable and all content: skills, flavour text, factions.
- `lib/synergies_controller.gd` — the runtime: input, cooldowns, casting, buffs, factions.
- `lib/` — HUD, character-select card, Codex tab, settings, VFX.

See the repository README for how it works and how to build it.
