# Read the installed game's own scripts so mod code can be checked against what Brotato really does.
# Lists the game's .pck and turns its compiled GDScript (.gdc, bytecode v13) back into readable text.
# Output goes to .game-src/ (git-ignored): Brotato's code is © Blobfish and must never be committed.
#
#   python tools/game_source.py list player              # list packed files whose path contains "player"
#   python tools/game_source.py dump singletons/temp_stats entities/units/player/player
#   python tools/game_source.py dump --all                # every script (~450 files)
#
# Set BROTATO_PCK if the game is not at the default Steam path.
import os
import struct
import sys

DEFAULT_PCK = r"C:\Program Files (x86)\Steam\steamapps\common\Brotato\Brotato.pck"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".game-src")

# Godot 3.x GDScriptTokenizer::Token order (bytecode version 13).
TOKENS = ("EMPTY IDENTIFIER CONSTANT self BUILT_IN_TYPE BUILT_IN_FUNC in == != < <= > >= and or not + - * / % "
          "<< >> = += -= *= /= %= <<= >>= &= |= ^= & | ^ ~ if elif else for while break continue pass return "
          "match func class class_name extends is onready tool static export setget const var as void enum "
          "preload assert yield signal breakpoint remote sync master slave puppet remotesync mastersync "
          "puppetsync [ ] { } ( ) , ; . ? : $ -> NEWLINE PI TAU _ INF NAN ERROR EOF CURSOR").split()
TYPES = ("null bool int float String Vector2 Rect2 Vector3 Transform2D Plane Quat AABB Basis Transform Color "
         "NodePath RID Object Dictionary Array PoolByteArray PoolIntArray PoolRealArray PoolStringArray "
         "PoolVector2Array PoolVector3Array PoolColorArray").split()
FUNCS = ("sin cos tan sinh cosh tanh asin acos atan atan2 sqrt fmod fposmod posmod floor ceil round abs sign "
         "pow log exp is_nan is_inf is_equal_approx is_zero_approx ease decimals step_decimals stepify lerp "
         "lerp_angle inverse_lerp range_lerp smoothstep move_toward dectime randomize randi randf rand_range "
         "seed rand_seed deg2rad rad2deg linear2db db2linear polar2cartesian cartesian2polar wrapi wrapf max "
         "min clamp nearest_po2 weakref funcref convert typeof type_exists char ord str print printt prints "
         "printerr printraw print_debug push_error push_warning var2str str2var var2bytes bytes2var range "
         "load inst2dict dict2inst validate_json parse_json to_json hash Color8 ColorN print_stack get_stack "
         "instance_from_id len is_instance_valid").split()
TIGHT = set(".()[],:")


def read_index(pck_path):
    f = open(pck_path, "rb")
    if f.read(4) != b"GDPC":
        sys.exit("not a Godot pack: %s" % pck_path)
    f.read(16 + 64)
    count = struct.unpack("<I", f.read(4))[0]
    entries = []
    for _ in range(count):
        n = struct.unpack("<I", f.read(4))[0]
        path = f.read(n).rstrip(b"\0").decode()
        offset, size = struct.unpack("<QQ", f.read(16))
        f.read(16)
        entries.append((path, offset, size))
    return f, entries


class Reader:
    def __init__(self, data):
        self.d, self.p = data, 0

    def u32(self):
        v = struct.unpack_from("<I", self.d, self.p)[0]
        self.p += 4
        return v

    def unpack(self, fmt):
        v = struct.unpack_from(fmt, self.d, self.p)
        self.p += struct.calcsize(fmt)
        return v

    def string(self, n):
        s = self.d[self.p:self.p + n].decode("utf8", "replace")
        self.p += n + (4 - n % 4) % 4
        return s

    def variant(self):
        head = self.u32()
        wide, kind = head >> 16 & 1, head & 0xFFFF
        if kind == 0:
            return "null"
        if kind == 1:
            return "true" if self.u32() else "false"
        if kind == 2:
            return str(self.unpack("<q" if wide else "<i")[0])
        if kind == 3:
            return repr(round(self.unpack("<d" if wide else "<f")[0], 6))
        if kind == 4:
            return repr(self.string(self.u32()))
        if kind == 5:
            return "Vector2(%g, %g)" % self.unpack("<2f")
        if kind == 7:
            return "Vector3(%g, %g, %g)" % self.unpack("<3f")
        if kind == 14:
            return "Color(%g, %g, %g, %g)" % self.unpack("<4f")
        if kind == 15:
            n = self.u32()
            names, subs = n & 0x7FFFFFFF, self.u32()
            self.u32()
            return "NodePath(%r)" % "/".join(self.string(self.u32()) for _ in range(names + subs))
        raise ValueError("unsupported constant type %d" % kind)


def detokenize(data):
    r = Reader(data)
    assert r.d[:4] == b"GDSC"
    r.p = 4
    r.u32()
    n_ids, n_consts, n_lines, n_tokens = r.u32(), r.u32(), r.u32(), r.u32()
    ids = []
    for _ in range(n_ids):
        n = r.u32()
        ids.append(bytes(b ^ 0xB6 for b in r.d[r.p:r.p + n]).split(b"\0")[0].decode())
        r.p += n
    consts = [r.variant() for _ in range(n_consts)]
    r.p += n_lines * 8
    lines, line = [], ""
    for _ in range(n_tokens):
        b = r.d[r.p]
        if b & 0x80:
            v = r.u32() & ~0x80
        else:
            v = b
            r.p += 1
        tok, arg = v & 0xFF, v >> 8
        name = TOKENS[tok] if tok < len(TOKENS) else "?%d" % tok
        if name == "NEWLINE":
            lines.append(line)
            line = "\t" * arg
            continue
        text = {"IDENTIFIER": lambda: ids[arg], "CONSTANT": lambda: consts[arg],
                "BUILT_IN_TYPE": lambda: TYPES[arg] if arg < len(TYPES) else "TYPE%d" % arg,
                "BUILT_IN_FUNC": lambda: FUNCS[arg] if arg < len(FUNCS) else "FUNC%d" % arg}.get(name, lambda: name)()
        if not line.strip() or text in TIGHT or line.endswith(("(", "[", ".", "$")):
            line += text
        else:
            line += " " + text
    lines.append(line)
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) < 2 or argv[0] not in ("list", "dump"):
        sys.exit("usage: game_source.py list <pattern...> | dump <pattern...> | dump --all")
    f, entries = read_index(os.environ.get("BROTATO_PCK", DEFAULT_PCK))
    patterns = argv[1:]
    for path, offset, size in entries:
        rel = path.replace("res://", "")
        if argv[0] == "list":
            if any(p in rel for p in patterns):
                print(rel, size)
            continue
        if not rel.endswith(".gdc"):
            continue
        if patterns != ["--all"] and not any(p + ".gdc" == rel or p in rel for p in patterns):
            continue
        f.seek(offset)
        dst = os.path.join(OUT_DIR, rel[:-1])   # .gdc -> .gd
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            open(dst, "w", encoding="utf8").write(detokenize(f.read(size)))
            print("wrote", os.path.relpath(dst))
        except Exception as e:   # one odd file shouldn't stop a bulk dump
            print("skipped %s: %s" % (rel, e))


if __name__ == "__main__":
    main(sys.argv[1:])
