# Code and docs conventions: small files, no repetition

The mod is read by people and by AI agents. Small, focused files are faster for both. Every agent
follows these rules, and reviewers check them.

## Code

- **One job per file.** A script does one thing and its name says what. Aim for under ~300 lines for new
  files. `config.gd` (content) and `lib/synergies_controller.gd` (runtime) are already large: when you
  add a new template or system, put it in its own `lib/` script instead of growing them.
- **Don't repeat yourself.** Search for an existing helper before writing one. The shared ones:
  - stats: `_apply_stat`, `_grant_buff`, `_undo_buff`, `_player_stat`, `_scaled_stats`;
  - enemies: `_enemy_mod` / `_enemy_unmod`, `_enemies_near`, `_nearest_enemy`;
  - damage and healing: `_scaled_damage`, `_spawn_aoe_hitbox`, `_heal_player`;
  - materials: `_add_player_gold`; VFX: `_spawn_vfx`, `_spawn_sprite_vfx`, the `lib/vfx/` scripts.
- **Content is data.** Skills, factions, numbers and text live in `config.gd`, never in logic. A new
  tunable gets a `_per_tier` companion and a line in the header comment above `SKILLS`.
- **Game paths and keys are constants** at the top of the file, with a note on how they were verified.
- **Short functions with clear names** over comments explaining long ones. A file starts with a one-line
  comment saying what it's for.
- **Refactor as you go, in scope.** Tidy the code you touch. Large clean-ups go in their own `chore/` branch.

## Docs

- **One topic per file**, aim for under ~200 lines. **Say each fact once** and link to it.
- Players read the README and the Workshop page; playtesters read `docs/testing/`; developers and agents
  read `docs/dev/` (map: [docs/README.md](../README.md)).
- Player text has no code names and ships in English and Vietnamese.
