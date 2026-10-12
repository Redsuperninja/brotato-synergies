# Fixed Coop Synergies: notes for Claude

A Brotato mod (Godot 3.x GDScript, Godot Mod Loader 6.x) that gives all 64 characters an active skill
and groups them into factions that buff and nerf the team. Forked from hhoangg's `tato-Synergies`;
the mod lives in `mods-unpacked/Redsuperninja-FixedCoopSynergies/`. Read `README.md` ("How it works"),
`docs/dev/game-internals.md`, `docs/ROADMAP.md` and `docs/adr/` first (map: `docs/README.md`).

## How work is done
- Work is split across the specialized agents in `.claude/agents/`; see `docs/dev/workflow.md`.
- One roadmap item = one small local branch (`feat/|fix/|balance/|docs/|chore/`). Never commit to `main` directly.
- Any change to a skill, faction or stat number gets a `game-designer` pass.
  Any change to publishing, file writes, bundled assets or licences gets a `security-reviewer` pass.

## Hard rules
- Stats only go through the game's `TempStats` layer (`_apply_stat` in the controller). Never write a
  player's `current_stats`/`max_stats` or the persistent effects dict. Use the game's stat keys
  (`stat_percent_damage`, `xp_gain`, …); `tools/check_config.py` lists the valid ones.
- Before relying on game behaviour, read it: `python tools/game_source.py dump <path>` (output in the
  git-ignored `.game-src/`). Never commit game code or game assets; Brotato is © Blobfish.
- Anything a skill leaves behind (buff, zone, slow, summon) must be undone by wave end, and an
  enemy's speed or tint only changes through the `_enemy_mod` ledger.
- Faction nerfs never touch Harvesting, and never push a stat below 0 (they are clamped).
- Credit stays with the original author (hhoangg / byptah) in README, LICENSE, LICENSE-ASSETS and the
  Workshop text. The 64 skill icons are theirs (CC BY 4.0).
- `MOD_VERSION` in `config.gd` and `version_number` in `manifest.json` always match; bump on every change.
- Player-facing text ships in English and Vietnamese; add both, or flag the missing Vietnamese.
- Small files, no repetition: one job per file, reuse shared helpers. See `docs/dev/conventions.md`.
- Attribution: code is built by Claude, designed and reviewed by the owner (stated in `docs/dev/workflow.md`).
  Do NOT add `Co-Authored-By: Claude` trailers or "Generated with Claude Code" lines. PR descriptions end with
  exactly one line: "Built with Claude Code; designed and reviewed by @Redsuperninja."
- Commit to local branches by default. Push, open PRs, merge or publish to the Workshop only when the owner asks.
- Docs ship with the code, in the same branch: tick `docs/ROADMAP.md`, add a `CHANGELOG.md` line, update
  `docs/dev/` for any mechanism change and the README for anything a player or contributor sees.

## Commands
- Config checks: `python tools/check_config.py`
- GDScript parse check: `gdparse <file.gd>` (setup in `docs/dev/testing.md`)
- Build: `./build-zip.sh` (test build) or `BUILD_RELEASE=1 ./build-zip.sh` → `dist/Redsuperninja-FixedCoopSynergies.zip`
- In-game check: `docs/dev/testing.md`
