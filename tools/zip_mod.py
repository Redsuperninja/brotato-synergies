# Zip the mod folder the same way build-zip.sh does with `zip`, for machines without it (Git Bash on
# Windows ships no zip). Usage: python tools/zip_mod.py <repo_root> <out.zip> <mod_id>
import fnmatch
import os
import sys
import zipfile

EXCLUDE = ["*.DS_Store", "*.bak", "*/Frames/*", "*/Stylized VFX/*", "*.gif", "*.zip"]

root, out, mod_id = sys.argv[1], sys.argv[2], sys.argv[3]
base = os.path.join(root, "mods-unpacked", mod_id)
count = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for folder, _dirs, files in os.walk(base):
        for name in sorted(files):
            rel = os.path.relpath(os.path.join(folder, name), root).replace(os.sep, "/")
            if any(fnmatch.fnmatch(rel, pat) for pat in EXCLUDE):
                continue
            zf.write(os.path.join(root, rel), rel)
            count += 1
print("zip_mod: %d files" % count)
