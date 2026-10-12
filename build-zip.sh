#!/usr/bin/env bash
set -euo pipefail

# Build the Co-op Synergies mod into a distributable .zip.
# The zip's internal layout is mods-unpacked/<id>/...  — exactly what Brotato's ModLoader
# expects (it mounts the zip at res://). .DS_Store is excluded.
#
# Usage:  ./build-zip.sh
# Output: dist/Redsuperninja-FixedCoopSynergies.zip

MOD_ID="Redsuperninja-FixedCoopSynergies"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${SCRIPT_DIR}/dist"
OUT="${OUT_DIR}/${MOD_ID}.zip"
CONFIG="${SCRIPT_DIR}/mods-unpacked/${MOD_ID}/config.gd"

if [ ! -d "${SCRIPT_DIR}/mods-unpacked/${MOD_ID}" ]; then
  echo "error: mod not found at ${SCRIPT_DIR}/mods-unpacked/${MOD_ID}" >&2
  exit 1
fi

# --- Toggle TEST_MODE + ENABLE_IN_SOLO on/off (cleanup trap restores originals) ---
CONFIG_BAK="${CONFIG}.bak"
cp "${CONFIG}" "${CONFIG_BAK}"
cleanup() { mv "${CONFIG_BAK}" "${CONFIG}"; }
trap cleanup EXIT

# Detect if this is a publish build (invoked from publish-steamcmd.sh) or a test build
# Portable in-place edit: `sed -i ''` is macOS-only and GNU sed (Linux, Git Bash) rejects it.
set_config() { sed "$1" "${CONFIG}" > "${CONFIG}.tmp" && mv "${CONFIG}.tmp" "${CONFIG}"; }
if [ "${BUILD_RELEASE:-0}" = "1" ]; then
  set_config 's/const TEST_MODE := true/const TEST_MODE := false/'
  set_config 's/const ENABLE_IN_SOLO := true/const ENABLE_IN_SOLO := false/'
  echo "build-zip: RELEASE mode (TEST_MODE=false, ENABLE_IN_SOLO=false)"
else
  set_config 's/const TEST_MODE := false/const TEST_MODE := true/'
  set_config 's/const ENABLE_IN_SOLO := false/const ENABLE_IN_SOLO := true/'
  echo "build-zip: TEST mode (TEST_MODE=true, ENABLE_IN_SOLO=true)"
fi

mkdir -p "${OUT_DIR}"
rm -f "${OUT}"
# VFX assets: ship only the Vivid spritesheets the mod actually loads. Exclude the raw per-frame
# PNGs (*/Frames/*, we animate from the 4x4 sheets), the whole unused Stylized VFX pack, and any
# preview gifs/zips — keeps the published zip lean instead of carrying ~10MB of source art.
if command -v zip >/dev/null 2>&1; then
  ( cd "${SCRIPT_DIR}" && zip -r -q "${OUT}" "mods-unpacked/${MOD_ID}" \
      -x '*.DS_Store' -x '*.bak' \
      -x '*/Frames/*' \
      -x '*/Stylized VFX/*' \
      -x '*.gif' -x '*.zip' )
else
  # No `zip` (e.g. Git Bash on Windows): same layout and exclusions via Python.
  PY="$(command -v python3 || command -v python)"
  "${PY}" "${SCRIPT_DIR}/tools/zip_mod.py" "${SCRIPT_DIR}" "${OUT}" "${MOD_ID}"
fi

echo "Built: ${OUT}"
if command -v unzip >/dev/null 2>&1; then
  ICONS=$(unzip -l "${OUT}" | grep -c '\.png$' || true)
  echo "  bundled skill icons: ${ICONS}"
  echo "--- contents (must start with mods-unpacked/${MOD_ID}/) ---"
  unzip -l "${OUT}" | sed -n '3,8p'
fi
echo "Test locally: ./sync-to-workshop.sh (after publishing + subscribing once)."
