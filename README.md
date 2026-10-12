# Fixed Coop Synergies

> A fixed and rebalanced fork of [**Co-op Synergies**](https://github.com/hhoangg/brotato-synergies) by **hhoangg (byptah)**,
> who designed the mod, its 64 skills and its icons. This fork is maintained by **Redsuperninja**.
> Changes since the fork are listed in [CHANGELOG.md](CHANGELOG.md). Don't enable this fork and the
> original at the same time (the manifest marks them incompatible).

A [Brotato](https://store.steampowered.com/app/1942280/Brotato/) mod that turns co-op into a team
draft. Every one of the 64 characters gets its own active skill on a free button, characters that
share a theme form factions that grant the whole team a buff *and* a nerf when two or more of them
play together, and every character reads as a role (Carry, Caster, Tank, Support, Late, Skirmisher,
Flex) so a party becomes a composition instead of four unrelated runs happening in the same arena.

Godot 3.x GDScript mod for [Godot Mod Loader](https://github.com/GodotModding/godot-mod-loader) 6.x.
Mod id `Redsuperninja-FixedCoopSynergies` (namespace `Redsuperninja`), forked from `tato-Synergies` by hhoangg.

The original mod's companion site, **<https://brotato.byptah.com/synergies>**, lists skills and
factions as they are in the original. This fork's factions and numbers differ; `config.gd` is the
source of truth here.

---

## Features

**Active skills for all 64 characters.** Each character has a unique skill defined in
`config.gd`'s `SKILLS` table — the Engineer deploys a turret, the Ghost phases through the swarm,
the Creature leaves a curse cloud, the Lich chains lightning, and so on. Skills are built from 12
effect templates (`buff_self`, `buff_party`, `heal`, `aoe_self`, `aoe_cursor`, `shield`, `dash`,
`summon`, `cc`, `curse_cloud`, `heal_zone`, `greed`) plus optional riders — an on-cast damage burst,
knockback, charm, taunt, fire/arcane burn, chain lightning, fog clearing, material drops.

**Tiers and unlock cadence.** A skill unlocks at **level 6** (`UNLOCK_LEVEL`) and gains a tier every
**6 levels** (`UPGRADE_EVERY`), capped at **tier 5** (`MAX_TIER`) — so levels 6 / 12 / 18 / 24 / 30.
Every number in a skill scales as `value(T) = base + (T-1) * per_tier`.

**Cooldown classes.** The base cooldown is **45%** of the *current* wave's duration
(`COOLDOWN_WAVE_FRACTION`, read off the live `WaveTimer`, so it grows with the wave), multiplied by
the skill's `cooldown_class`: `fast` ×0.5 (~4 casts/wave), `normal` ×1.0 (~2/wave, the default),
`slow` ×1.6 (~1.2/wave). 15 skills are fast, 12 are slow, the rest normal.

**Endless scaling.** Fixed tier numbers go stale once enemies get tanky, so skill damage is
multiplied by a wave factor (+15%/wave, `SKILL_WAVE_DMG_GROWTH`; heals +12%) and by the caster's
Damage % with a tier-growing share (×1.0 at tier 1, +0.25 per tier → ×2.0 at tier 5), floored at 25%
so a negative-Damage build still hits (`SKILL_MIN_DMG_MULT`).

**Faction affinities.** 13 factions — Same Boat, Arcane, Machines, The Damned, Crown & Steel,
The Wild, Iron Fists, Hustlers, The Caretakers, Reckless, Late Bloomers, Drifters, All-Rounders.
**Every one of the 64 characters belongs to at least one.** Two or more members in the
run activates the faction's tier-2 bundle; three or more upgrades it to tier 3. Every bundle is a
**team buff plus a team nerf** (e.g. Arcane: +20% Elemental Damage, −6 Max HP), and some factions add
a named-pair bonus when two specific characters are both present (Mage + Apprentice, King + Knight,
Hunter + Ranger). Characters sit in more than one faction, so the draft has depth. Traits are applied
team-wide at each wave start and cleared at wave end.

A nerf only takes away what a player has: it never pushes a stat below 0 (Max HP never below 10,
`AFFINITY_NERF_FLOOR`), and no faction nerfs Harvesting, since negative Harvesting costs materials.

**How stats are applied.** Every skill buff and faction trait goes through the game's own `TempStats`
layer, the one its "while below half HP" items use. The game reloads the player, their weapons and
their structures from it, and resets it at the start and end of every wave, so nothing can leak into
the shop or a save. Harvesting from a skill lasts until the wave ends, because that is when it pays out.

**Roles.** Every character carries a role tag that drives its skill archetype and the colour coding
on the info cards: Carry (19), Late (9), Support (8), Tank (8), Skirmisher (8), Caster (7), Flex (5).

**In-game info.** A skill card is injected into the character-select and weapon-select description
panels (for every visible co-op panel, not just P1), a per-player HUD widget shows tier, a cooldown
radial and active-buff timers next to each life bar, and a fifth **CHARS** tab is injected into the
game's own Codex: an 8-column grid of every character with a detail pane showing its stats and its
Synergies skill.

**Localisation.** Skill names, flavour lines, stat names and faction labels ship in English and
Vietnamese; the UI picks the language from the game's locale and falls back to English.

---

## Install

1. Install [Godot Mod Loader](https://github.com/GodotModding/godot-mod-loader) for Brotato (the
   game must be started with mods enabled).
2. Subscribe to **Fixed Coop Synergies** on the Steam Workshop (the original Co-op Synergies is
   [item 3745283747](https://steamcommunity.com/sharedfiles/filedetails/?id=3745283747); use one or
   the other, not both).
3. Start Brotato, start a **Co-op** run, and make sure the **Synergies** toggle in the
   character-select Run Options panel is on (it is on by default).

Or install manually: build the zip (below) and drop it into your Brotato mods folder.

---

## Controls & settings

- **Space** (keyboard) or the **bottom face button** (controller — joypad button index 0, "A" on an
  Xbox-layout pad; Godot maps by position, not label) fires your skill. Configured as
  `Config.SKILL_KEY` / `Config.SKILL_BUTTON`.
- In co-op each player fires their own skill: the trigger is polled per input device, and the
  firing device is resolved to that player's co-op slot.
- Skills only fire **during a live wave** and never while paused, so the button never collides with
  shop/menu confirm.
- **Synergies on/off:** a `Synergies` check button is injected into the character-select **Run
  Options** panel, right under Co-op (it is only visible while Co-op is on). Default: on.
- Settings are stored in the mod's own file, `user://fixed_coop_synergies_settings.cfg` — the game's own
  save is never touched. There is a second, independent setting (`skills_solo`, default off) that
  enables skills in solo play; it is injected into **Options → Accessibility** and honoured **only in
  test builds** — a published release build never grants solo skills, since skills are a co-op
  feature by design.

---

## Building from source

Requirements: `bash` and `zip`. The optional icon/thumbnail tools in `tools/` need
[Bun](https://bun.sh) and `sharp`.

```bash
./build-zip.sh                    # → dist/Redsuperninja-FixedCoopSynergies.zip  (TEST build)
BUILD_RELEASE=1 ./build-zip.sh    # → dist/Redsuperninja-FixedCoopSynergies.zip  (RELEASE build)
```

`build-zip.sh` rewrites two constants in `config.gd` before zipping and restores the file afterwards
via an exit trap:

| | `TEST_MODE` | `ENABLE_IN_SOLO` |
|---|---|---|
| default (test) build | `true` | `true` |
| `BUILD_RELEASE=1` | `false` | `false` |

`TEST_MODE` is the flag the code actually reads: it drops the unlock level to 1, shortens the
cooldown to ~5% of the wave, lowers the faction activation threshold to 1 member, stretches buff
durations to 20s so you can read them in the pause screen, prints a once-a-second gating diagnostic,
and exposes the solo-skills toggle. `ENABLE_IN_SOLO` is currently only declared, not read at runtime.

The zip's internal layout is `mods-unpacked/Redsuperninja-FixedCoopSynergies/…`, which is what the ModLoader expects.
Only the Vivid spritesheets are bundled — the per-frame PNGs, preview gifs and unused packs are
excluded so the published zip stays lean.

Publishing to the Steam Workshop (maintainer only, needs [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD)
on PATH or `STEAMCMD=<path>`):

```bash
python tools/check_config.py            # must pass
./publish-steamcmd.sh <steam_account>   # release build + steamcmd upload of thumbnail.jpeg
```

Workshop metadata (title, description, changenote, item id, visibility) lives in `workshop_item.vdf`.
The first upload creates a **private** item (`"visibility" "2"`): paste the printed PublishedFileID
into `workshop_item.vdf`, subscribe, playtest, then set `"visibility" "0"` and run it again to go
public. `python tools/make_thumbnail.py` rebuilds `thumbnail.jpeg` from the original art.

---

## Local development loop

Brotato's shipped build loads mods **only** from the Steam Workshop content directory — it ignores a
local `mods/` or `mods-unpacked/` folder. So the fast loop overwrites the downloaded Workshop copy
in place:

```bash
WS_ITEM=<item id> ./sync-to-workshop.sh   # build-zip.sh (test build) + copy into the Workshop item folder
```

Prerequisites: the item must have been published once (privately is fine) and **subscribed** to in
Steam so its folder exists. The script knows the default Steam folder on macOS, Windows (Git Bash)
and Linux; override it with `WS_DIR=<path>`.

Then relaunch Brotato and read the log (`%APPDATA%\Brotato\logs\godot.log` on Windows,
`~/Library/Application Support/Brotato/logs/godot.log` on macOS) — the mod
prints `[Synergies] loaded Fixed Coop Synergies v<version>` on start, plus per-cast and per-stat lines. The version also
appears in the HUD watermark, so an in-game glance confirms which build is loaded.

Caveat: this overwrites Steam-managed files. Steam may revert them on "Verify integrity of game
files" or when the item updates server-side.

---

## Project layout

```
build-zip.sh              build the distributable zip (toggles TEST_MODE / ENABLE_IN_SOLO)
sync-to-workshop.sh       build + drop the zip into the local Steam Workshop folder
publish-steamcmd.sh       release build + Workshop upload via steamcmd
workshop_item.vdf         Workshop metadata (title, description, changenote, item id, visibility)
thumbnail.jpeg            Workshop preview, built from thumbnail.original.jpeg (hhoangg's art)
SKILL-ICON-PROMPTS.md     the image prompts used to generate the 64 skill icons
tools/
  circle-mask-icons.ts    cut generated icons to a transparent circle (Bun + sharp)
  make_thumbnail.py       put this fork's title on the preview art (Pillow)
  check_config.py         static checks on content, stat keys, versions and Workshop text
  game_source.py          read the game's own scripts into the git-ignored .game-src/
  zip_mod.py              zip fallback for build-zip.sh where `zip` is missing
mods-unpacked/Redsuperninja-FixedCoopSynergies/
  manifest.json           ModLoader manifest (id, version_number, ML 6.x compatibility)
  mod_main.gd             ModLoader entry point; spawns the persistent controller
  config.gd               ALL tunables + content: framework constants, roles, effect templates,
                          the 64-entry SKILLS table, flavour text, AFFINITIES, faction colours
  lib/
    synergies_controller.gd   the whole runtime: input polling, cooldowns, every cast template,
                              riders, affinities, buff bookkeeping, cross-mod API
    skill_hud.gd              in-run per-player widget (icon, tier, cooldown, buffs, affinities)
    charsel_panel.gd          skill + faction card injected into character/weapon select
    character_codex.gd        the "CHARS" tab injected into the game's Codex
    mod_settings.gd           persisted toggles (mod-owned ConfigFile in user://)
    settings_panel.gd         injects those toggles into the game's menus
    aoe_ring.gd beam.gd lightning.gd heal_aura.gd summon_turret.gd
    vfx/                      13 procedural effect scripts + sprite_vfx.gd (spritesheet player)
  assets/
    skills/<slug>.png         64 skill icons (256×256, transparent circle) — included
    vfx/                      third-party spritesheet pack — NOT included, see below
```

---

## How it works

**One persistent controller.** `mod_main.gd` installs no script extensions; it adds a single
`SynergiesController` node under `/root`. Everything else is that node polling and reacting each
frame, which keeps the mod out of the game's own class hierarchy and makes it easy to reason about
teardown — when a run ends, every buff, zone, freeze and timer is dropped in one place.

**The skill state machine.** Per frame, while a run is active and the system is enabled, the
controller reads whether a wave is live (from the scene's `WaveTimer`). On the first in-wave frame it
applies the faction traits and primes the input edge state (so the shop's "go" press isn't read as a
cast). It then ticks cooldowns and every active effect, polls the trigger and pushes a state snapshot
to the HUD. On the first out-of-wave frame it expires all buffs and clears lingering wave effects, so
nothing leaks into the shop or the next wave.

**Casting.** Input is **poll-based**: the controller reads the raw key/button *state* each frame and
fires on the rising edge, which is robust against flaky pad event delivery, and it never consumes the
event. A cast is gated on: run active, system enabled, not paused, in a wave, level ≥ unlock level,
cooldown at zero. `_cast_skill` then dispatches on the skill's `template` to the matching
`_cast_*` handler and applies the universal riders.

**Resolving a co-op place.** A "place" is a player slot index — `RunData.players_data` and
`CoopService.connected_players` use the same numbering. A `connected_players` entry is
`[device, PlayerType]`, and **the place is the entry's index**, not `entry[1]` (that field is the
controller brand: keyboard / Xbox / PlayStation / Switch). Keyboard input resolves to the entry whose
`PlayerType` is `KEYBOARD_AND_MOUSE`; pad input resolves by matching the remapped device id (Godot
hands out raw joypad ids, and the game remaps a pad on raw device 0 to `GAMEPAD_REMAPPED_DEVICE_ID`).
Getting this wrong cross-maps players — with two same-brand pads one player gets no skill at all —
so it is the single most bug-prone line in the mod.

**Applying stats.** Temp buffs go through `TempStats.add_stat(hash, amount, place)`, keyed by the
game's stat hash (`Keys.generate_hash`; use the game's own names, e.g. `stat_percent_damage` for
Damage and `xp_gain` for XP Gain). That resets the stat cache and marks the player dirty, so the game
reloads the player, weapons and structures next physics frame; the mod also calls
`update_player_stats()` right away. Never write `current_stats` directly: dodge there is a 0–1
fraction and speed is pixels, which is how the old version ended up with negative dodge. Each buff is
tracked in `_active_buffs` with its remaining time and undone once. Because the game wipes
`TempStats` at wave end (by swapping in a new table), each buff remembers the table it wrote to and
skips the undo when that table has been replaced. Faction traits use the same path with
`caster = -1` and an effectively-infinite duration, so they are excluded from the per-player HUD
timers and expire only when the wave ends.

**Enemy slows.** Freeze, slow zones and charm all register with one ledger (`_enemy_mod`): an enemy's
speed is its base times every active multiplier, and its tint is the newest source's. When the last
source ends, or the wave ends, it gets its base speed and tint back.

**The HUD** (`skill_hud.gd`) is a pure renderer on its own `CanvasLayer` — it draws whatever state
snapshot the controller pushes in and contains no game logic. Skill icons are raw mod PNGs, which
Godot cannot `load()` (they were never import-cooked), so they are read as bytes and decoded with
`Image.load_png_from_buffer`, cached per slug.

**UI injection.** The settings toggles, the character-select card and the Codex tab are all injected
into the game's own menus by watcher nodes that poll for the target container, build native-looking
controls in code (no `.tscn`), and re-inject when the menu is rebuilt. Node paths were verified
against the extracted game scenes and are kept as constants at the top of each file.

**Cross-mod API.** The controller exposes `get_synergies_state()` — a pure read returning whether
synergies were active this run and each player's character/skill — so another mod can call it via
`has_method` without a hard dependency.

---

## Third-party assets

The sprite-sheet effects use **Vivid Motion 23 — Universal Status Effects**, a third-party art pack.
**It is not included in this repository** (`.gitignore` excludes
`mods-unpacked/Redsuperninja-FixedCoopSynergies/assets/vfx/`) because this project has no right to redistribute it.

To build with those effects, obtain the pack yourself and place it at:

```
mods-unpacked/Redsuperninja-FixedCoopSynergies/assets/vfx/Vivid_Motion_23_ Universal_Status_Effects/
```

keeping the pack's own folder layout — the mod loads
`<Effect>Effect/Spritesheets/<Effect>Effect_Sheet_64x64.png` (a 4×4 grid of 64×64 frames) and
currently uses the Burn, Charm, Curse, Haste, Heal, Regen, Shield, Shock and Slow effects.

**Without the pack, nothing breaks.** `sprite_vfx.gd` fails to decode the missing sheet, frees itself
immediately, and those particular status-effect animations simply do not appear. All gameplay, all
13 procedural VFX scripts in `lib/vfx/`, the HUD and the menus are unaffected.

---

## Contributing

Bug reports, ideas and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Licence

- **Code:** MIT — see [LICENSE](LICENSE).
- **The mod's own art** (the 64 skill icons, the thumbnail): CC BY 4.0 — see
  [LICENSE-ASSETS](LICENSE-ASSETS).

Both licences let you fork, modify and redistribute this mod, commercially or not, as long as you
credit the original author (hhoangg / byptah, with a link back to
[the original repository](https://github.com/hhoangg/brotato-synergies)). The fork's own changes are
© Redsuperninja under the same licences.

Not covered by either licence: **Brotato** itself and anything extracted from it (sprites, sounds,
names, translations) — Brotato is © Blobfish; and the excluded third-party asset pack described
above, which remains under its own licence.

---

## Support the original author

The original mod was made for fun and given away free. If you enjoy it, hhoangg's
**<https://ko-fi.com/hhoangg>** is open.

---

## Credits & disclaimer

Original mod, skill design and skill icons by **hhoangg** (byptah). Fork maintained by
**Redsuperninja**. Built on [Godot Mod Loader](https://github.com/GodotModding/godot-mod-loader).

This is an unofficial, unaffiliated fan mod. It is not made by, endorsed by, or associated with
Blobfish, the developer of Brotato.
