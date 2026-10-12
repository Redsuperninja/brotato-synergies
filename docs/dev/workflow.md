# How this project is built and managed

This fork of Co-op Synergies is built by a small team of **specialized AI agents** (Claude Code
subagents) with a human in charge. Each agent has one job, a written brief, and limited tools, so it's
always clear who did what and why. Agent briefs live in [`.claude/agents/`](../../.claude/agents).

## The team

| Agent | Job | Can edit code? | Model |
| --- | --- | --- | --- |
| `architect` | Breaks features into small PRs, keeps `docs/dev/`, ROADMAP and ADRs current | Docs only | Opus |
| `gdscript-engineer` | The mod's GDScript (controller, templates, HUD, menus) and build scripts | Yes | Sonnet |
| `game-designer` | Skills, factions, roles and every balance number; checks they hold up in co-op | Yes (`config.gd` + text) | Opus |
| `security-reviewer` | Reviews publishing, file writes, bundled assets, licences and credit | No, review only | Opus |
| `test-engineer` | Static checks, build checks, and in-game test scripts for the owner | Yes (checks, test docs) | Sonnet |
| `docs-writer` | Player text: README, Workshop page, flavour lines, EN + VI | Docs/text only | Haiku |
| `release-manager` | Branches, version sync, commits, changelog | Git only | Haiku |

Judgment-heavy work (planning, balance, release safety) gets the strongest model; routine coding and
checks a mid-size one; text and git chores the fastest. Agents read only what their task needs.

**Who does what:** the code is built by [Claude Code](https://claude.com/claude-code) (Anthropic) through
these agents. The design and all reviews come from the project owner, Redsuperninja. The original mod,
its skill design and its icons are by hhoangg (byptah). Agents commit to local branches only; the owner
decides what is pushed, merged and published to the Workshop.

## The loop for every change

1. **Plan:** `architect` picks the next [roadmap](../ROADMAP.md) item and writes a short task (goal, files,
   how to check it in-game).
2. **Build:** `gdscript-engineer` or `game-designer` implements it on a branch, with docs.
3. **Check:** `test-engineer` runs the checks ([testing.md](testing.md)) and writes the in-game test steps;
   `game-designer` reviews any number change; `security-reviewer` reviews publishing, files, assets or credit.
4. **Commit:** `release-manager` bumps the version, commits to the local branch (aim for < ~400 changed
   lines), ticks the roadmap box and adds a changelog line. Nothing is pushed.
5. **Owner review and playtest:** the owner runs the in-game steps, then decides when it's pushed, merged
   and published.

### Rules for `main`
- **Changes reach `main` only through a pull request.** The `.githooks/pre-push` hook refuses pushing to
  `main` or deleting it. Turn it on once per clone: `git config core.hooksPath .githooks`.
- PRs are squash-merged and their branches deleted after the merge.

## Rules every agent follows
- Small changes, one purpose each. Commit locally; the owner decides what gets pushed and published.
- Check game behaviour in the game's own scripts ([game-internals.md](game-internals.md)), never guess it.
  Never commit game code or assets.
- Small files, no repetition ([conventions.md](conventions.md)).
- Every PR explains *what* and *why* in words a player could follow, and how it was tested in-game.
- Big decisions get an ADR in `docs/adr/` (one page: context, decision, consequences).

## Using the agents yourself
In Claude Code, from this folder, ask for an agent by name:

> "Use the game-designer agent to rebalance the Hustlers faction."

> "Have the security-reviewer agent review this branch before I publish."
