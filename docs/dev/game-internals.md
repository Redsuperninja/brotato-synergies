# Brotato internals the mod relies on

Verified against Brotato 1.1.x's own scripts (read with `python tools/game_source.py dump <path>`).
Re-check after a game update; paths below are inside the game's pack.

## Stats

- A player's stat is `Utils.get_stat(hash, player_index)` = `RunData.get_stat` (items and level-ups, from
  the persistent effects dict) **+ `TempStats.get_stat`** + `LinkedStats.get_stat`, cached per player
  (`singletons/utils.gd`). Hashes come from `Keys.generate_hash("stat_…")`.
- The stat keys are the ones in `PlayerRunData.init_stats` (`singletons/player_run_data.gd`).
  **Damage % is `stat_percent_damage`** (weapons read it in `singletons/weapon_service.gd`) and
  **XP Gain is `xp_gain`**. `stat_damage` exists in `Keys` but nothing reads it.
- **`TempStats`** (`singletons/temp_stats.gd`) is the game's in-wave layer: `add_stat`/`remove_stat`
  reset the stat cache and mark the player dirty. `RunData._physics_process` then emits `stats_updated`,
  and `StatsManager.reload_stats` (`global/stats_manager.gd`) reloads the player, their weapons and
  their structures. The game calls `TempStats.reset()` at wave start (`main.gd` `_ready`), at wave end
  (after harvesting is paid) and at run start. `reset_player` swaps in a **new** Dictionary.
- `Player.update_player_stats()` (`entities/units/player/player.gd`) rebuilds `max_stats` and copies it
  into `current_stats`: `speed = base * (1 + capped stat_speed / 100)` (pixels per second),
  `armor = stat_armor`, `dodge = capped stat_dodge / 100` (**a 0–1 fraction**). When max HP rises it adds
  the difference to current HP; when it falls it does not clamp. Dodge is capped at 60 by default.
- Taking damage checks `randf() < current_stats.dodge`, so writing whole numbers there means 100%
  dodge, and subtracting them later means negative dodge. That was the old "negative stats" bug.

## Materials and harvesting

- `RunData.add_gold(value, player_index)` adds materials and emits `gold_changed` (HUD updates).
- Harvesting pays out once, at wave end (`main.gd` `manage_harvesting`):
  `harvesting_stat + bonuses`, so **negative Harvesting removes materials**. The harvesting timer also
  grows positive Harvesting permanently by the character's growth %.

## Enemies

- Enemy movement reads `current_stats.speed` (a `LiveStats`, `entities/units/unit/live_stats.gd`).
  The game doesn't restore it for us, so every change goes through the mod's `_enemy_mod` ledger.
- Bosses carry `health_increase_each_wave` of about 700+; normal enemies are under ~35.
