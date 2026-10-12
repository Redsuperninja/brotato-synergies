# ADR 0001: Skill buffs and faction traits go through the game's TempStats

**Status:** accepted (v0.40.0)

## Context

Up to v0.39.14 the mod applied a buff by adding to the persistent effects dict
(`RunData.get_player_effects`) and, for armor, speed, damage and dodge, also adding the raw number
straight into the player's `current_stats`/`max_stats`. In the game, dodge there is a 0–1 fraction and
speed is pixels per second, so after any stat recalculation undoing a buff left dodge around −9 and
speed off by the raw amount. Writing the effects dict didn't mark the player dirty, so weapons and
turrets never reloaded and attack speed, crit, range and engineering buffs did nothing. A missed undo
(run ended mid-wave) left the change in the save.

## Decision

All temporary stats use `TempStats.add_stat(hash, amount, player_index)`, the layer the game uses for
its own "while below half HP" items. The mod never writes `current_stats`/`max_stats` or the effects
dict; it calls `update_player_stats()` and clamps current HP under max. Each buff remembers the
`TempStats` table it wrote to; if the game has since reset it (wave end, new run), the undo is skipped
instead of subtracting from a fresh table. Faction nerfs are clamped so they never push a stat below 0.

## Consequences

- Stats can't go negative from the mod, and nothing can leak into the shop or a save.
- Every stat key must be in the game's stat table; `tools/check_config.py` enforces it.
- Stat gain modifiers (`gain_stat_*`) now apply to skill buffs, the same as to the game's own temp stats.
- Harvesting is only read at wave end, so skill Harvesting lasts until then (non-stacking per caster).
