# Static checks on config.gd and manifest.json that need no game: every character has a skill, an
# icon, flavour text and a faction; every stat key is one the game tracks; nerfs are negative and
# never touch Harvesting; versions match. Usage: python tools/check_config.py   (exit 1 on errors)
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "mods-unpacked", "Redsuperninja-Synergies")

# Keys in the game's per-player stat table (PlayerRunData.init_stats, Brotato 1.1.x). TempStats.add_stat
# only accepts these; anything else is ignored by the game.
GAME_STATS = {
    "stat_max_hp", "stat_armor", "stat_crit_chance", "stat_luck", "stat_attack_speed",
    "stat_elemental_damage", "stat_hp_regeneration", "stat_lifesteal", "stat_melee_damage",
    "stat_percent_damage", "stat_dodge", "stat_engineering", "stat_range", "stat_ranged_damage",
    "stat_speed", "stat_harvesting", "xp_gain",
}
TEMPLATES = {"buff_self", "buff_party", "heal", "aoe_self", "shield", "aoe_cursor", "dash", "summon",
             "cc", "curse_cloud", "heal_zone", "greed"}
COOLDOWN_CLASSES = {"fast", "normal", "slow"}

errors, warnings = [], []


class _Names(dict):
    """Eval namespace: any bare GDScript constant (ROLE_*, TMPL_*) resolves to its value or its name."""
    def __missing__(self, key):
        return CONSTS.get(key, key)


def strip_comments(src):
    out = []
    for line in src.split("\n"):
        in_str, cut = False, len(line)
        for i, ch in enumerate(line):
            if ch == '"' and (i == 0 or line[i - 1] != "\\"):
                in_str = not in_str
            elif ch == "#" and not in_str:
                cut = i
                break
        out.append(line[:cut])
    return "\n".join(out)


def const_block(src, name):
    start = src.index("const %s := " % name) + len("const %s := " % name)
    depth, i = 0, start
    while True:
        ch = src[i]
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
            if depth == 0:
                break
        elif ch == '"':
            i = src.index('"', i + 1)
        i += 1
    text = src[start:i + 1].replace("true", "True").replace("false", "False")
    return eval(text, {"__builtins__": {}}, _Names())


src = strip_comments(open(os.path.join(MOD, "config.gd"), encoding="utf8").read())
CONSTS = dict(re.findall(r'^const (\w+) := "([^"]*)"', src, re.M))
skills = const_block(src, "SKILLS")
flavor = const_block(src, "SKILL_FLAVOR")
affinities = const_block(src, "AFFINITIES")
colors = const_block(src, "AFFINITY_COLORS")
order = const_block(src, "AFFINITY_ORDER")
manifest = json.load(open(os.path.join(MOD, "manifest.json"), encoding="utf8"))


def check_stats(where, stats, sign=None):
    for k, v in stats.items():
        if k not in GAME_STATS:
            errors.append("%s: '%s' is not a stat the game tracks" % (where, k))
        if sign == "+" and v <= 0:
            errors.append("%s: buff %s=%s should be positive" % (where, k, v))
        if sign == "-" and v >= 0:
            errors.append("%s: nerf %s=%s should be negative" % (where, k, v))
        if sign == "-" and k == "stat_harvesting":
            errors.append("%s: Harvesting nerfs cost players materials every wave" % where)


faction_count = {slug: 0 for slug in skills}
for key, aff in affinities.items():
    for slug in aff["members"]:
        if slug not in skills:
            errors.append("faction %s: unknown member '%s'" % (key, slug))
        else:
            faction_count[slug] += 1
    if key not in colors:
        errors.append("faction %s: no AFFINITY_COLORS entry" % key)
    if key not in order:
        errors.append("faction %s: missing from AFFINITY_ORDER" % key)
    for t in aff["tiers"]:
        check_stats("faction %s tier %s buff" % (key, t["at"]), t.get("buff", {}), "+")
        check_stats("faction %s tier %s nerf" % (key, t["at"]), t.get("nerf", {}), "-")
    for p in aff.get("pairs", []):
        for slug in (p["a"], p["b"]):
            if slug not in aff["members"]:
                errors.append("faction %s: pair member '%s' is not in the faction" % (key, slug))
        check_stats("faction %s pair" % key, p.get("buff", {}), "+")

for slug, sk in skills.items():
    if sk.get("template") not in TEMPLATES:
        errors.append("skill %s: unknown template %r" % (slug, sk.get("template")))
    if sk.get("cooldown_class", "normal") not in COOLDOWN_CLASSES:
        errors.append("skill %s: unknown cooldown_class %r" % (slug, sk.get("cooldown_class")))
    check_stats("skill %s stats" % slug, sk.get("stats", {}), "+")
    check_stats("skill %s stats_per_tier" % slug, sk.get("stats_per_tier", {}))
    for k in sk.get("stats", {}):
        if k not in sk.get("stats_per_tier", {}):
            warnings.append("skill %s: '%s' has no stats_per_tier entry (flat across tiers)" % (slug, k))
    if not os.path.isfile(os.path.join(MOD, "assets", "skills", slug + ".png")):
        errors.append("skill %s: no icon assets/skills/%s.png" % (slug, slug))
    if not flavor.get(slug, {}).get("en"):
        errors.append("skill %s: no English flavour text" % slug)
    elif not flavor[slug].get("vi"):
        warnings.append("skill %s: no Vietnamese flavour text" % slug)
    if faction_count[slug] == 0:
        errors.append("character %s: not in any faction" % slug)

version = re.search(r'const MOD_VERSION := "([^"]+)"', open(os.path.join(MOD, "config.gd"), encoding="utf8").read())
if version is None or version.group(1) != manifest["version_number"]:
    errors.append("MOD_VERSION in config.gd does not match manifest.json version_number")
if "%s-%s" % (manifest["namespace"], manifest["name"]) != os.path.basename(MOD):
    errors.append("manifest namespace-name does not match the mod folder name")

for w in warnings:
    print("warning: " + w)
for e in errors:
    print("ERROR: " + e)
print("check_config: %d characters, %d factions, %d errors, %d warnings"
      % (len(skills), len(affinities), len(errors), len(warnings)))
sys.exit(1 if errors else 0)
