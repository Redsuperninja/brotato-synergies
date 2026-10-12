#!/usr/bin/env bash
set -euo pipefail

# Publish Fixed Coop Synergies to the Steam Workshop via SteamCMD — WITHOUT
# GodotWorkshopUtility, so the Workshop title from workshop_item.vdf sticks
# (GodotWorkshopUtility has no title field and force-sets the title to the mod id).
#
# FIRST RUN (new item): workshop_item.vdf has  "publishedfileid" "0"  -> steamcmd CREATES
# a new Workshop item and prints its id (PublishedFileID). Paste that id back into
# workshop_item.vdf's "publishedfileid" so every later run UPDATES that same item.
#
# VISIBILITY: workshop_item.vdf ships "visibility" "2" (private) so the first upload can be subscribed
# to and playtested before anyone else sees it. Set it to "0" (public) and run again to release.
#
# Prereqs:
#   - steamcmd: macOS `brew install --cask steamcmd`; Windows: download steamcmd.zip from Valve
#     (https://developer.valvesoftware.com/wiki/SteamCMD), unzip it, and put the folder on PATH or set
#     STEAMCMD=/c/path/to/steamcmd.exe
#   - the Steam account you log in with OWNS Brotato (and, after creation, owns this item)
#   - the preview image thumbnail.jpeg (python tools/make_thumbnail.py rebuilds it)
#
# Usage:
#   ./publish-steamcmd.sh <steam_account>
#   (the first login prompts for your password and Steam Guard code, interactively)

MOD_ID="Redsuperninja-FixedCoopSynergies"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST="${SCRIPT_DIR}/dist"
CONTENT="${DIST}/content"                       # the folder Steam uploads: must hold ONLY the zip
TEMPLATE="${SCRIPT_DIR}/workshop_item.vdf"
GENERATED="${DIST}/workshop_item.generated.vdf" # template with absolute paths filled in
PREVIEW="${SCRIPT_DIR}/thumbnail.jpeg"

STEAM_ACCOUNT="${1:-}"
if [ -z "${STEAM_ACCOUNT}" ]; then
  echo "usage: $0 <steam_account>" >&2
  exit 1
fi

STEAMCMD="${STEAMCMD:-$(command -v steamcmd || command -v steamcmd.exe || true)}"
if [ -z "${STEAMCMD}" ]; then
  echo "error: steamcmd not found. Install it (see the header of this script) or set STEAMCMD=<path>." >&2
  exit 1
fi
[ -f "${TEMPLATE}" ] || { echo "error: missing ${TEMPLATE}" >&2; exit 1; }
[ -f "${PREVIEW}" ]  || { echo "error: missing preview image ${PREVIEW} (run: python tools/make_thumbnail.py)" >&2; exit 1; }

# steamcmd.exe on Windows can't resolve Git Bash paths (/c/...): hand it C:/... instead (forward
# slashes need no escaping in the .vdf). Elsewhere paths pass through unchanged.
native_path() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else echo "$1"; fi; }

# 0) Refuse to upload content or a Workshop page that fails the static checks.
PY="$(command -v python3 || command -v python)"
"${PY}" "${SCRIPT_DIR}/tools/check_config.py" || { echo "error: tools/check_config.py failed; not uploading." >&2; exit 1; }

# 1) Build the mod zip (release mode: TEST_MODE=false).
BUILD_RELEASE=1 "${SCRIPT_DIR}/build-zip.sh" >/dev/null
[ -f "${DIST}/${MOD_ID}.zip" ] || { echo "error: build did not produce ${DIST}/${MOD_ID}.zip" >&2; exit 1; }

# 2) Stage a clean content folder containing ONLY the zip (ModLoader loads the zip at the
#    item root). steamcmd replaces the item's content with everything in contentfolder.
rm -rf "${CONTENT}"
mkdir -p "${CONTENT}"
cp "${DIST}/${MOD_ID}.zip" "${CONTENT}/"

# 3) Render the .vdf with ABSOLUTE paths (steamcmd resolves contentfolder/previewfile from
#    its own cwd, so relative paths are unreliable). '|' avoids clashing with '/' in paths.
sed -e "s|__CONTENTFOLDER__|$(native_path "${CONTENT}")|g" \
    -e "s|__PREVIEWFILE__|$(native_path "${PREVIEW}")|g" \
    "${TEMPLATE}" > "${GENERATED}"

echo "--- ${GENERATED} ---"
cat "${GENERATED}"
echo "------------------------------------------------------------"

if grep -q '"publishedfileid"[[:space:]]*"0"' "${GENERATED}"; then
  echo "NOTE: publishedfileid is 0 -> this CREATES a new Workshop item."
  echo "      After it succeeds, copy the printed PublishedFileID into ${TEMPLATE}."
fi

# 4) Upload. First login is interactive (Steam Guard). On success steamcmd prints the id.
echo "Uploading as Steam account '${STEAM_ACCOUNT}'…"
"${STEAMCMD}" +login "${STEAM_ACCOUNT}" +workshop_build_item "$(native_path "${GENERATED}")" +quit

echo "Done. If this was the first upload, paste the PublishedFileID into ${TEMPLATE}."
