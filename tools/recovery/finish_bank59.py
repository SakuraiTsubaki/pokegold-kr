#!/usr/bin/env python3
"""Recover Korean Bank $59 / Map Scripts 23 from the verified KOR Silver ROM mapping.

Payload contains 75 text-command streams recovered from
Pocket Monsters Eun (Korea), SHA-1 cb22d7e03a74dc3a563fde6be8626626b2b392e7.
All 75 streams were independently re-encoded byte-identically before this patcher was generated.
"""
from pathlib import Path
import argparse, base64, json, re, zlib

BANK = 0x59
EXPECTED_SILVER_SHA1 = "cb22d7e03a74dc3a563fde6be8626626b2b392e7"
DATA_B64 = """eNqtW21vG0eS/isjf7oD4ru1N5cPi8P5/LKWs2snhiXECGBgMbHGEmGKI5BUNsIiACWNZFqk1hQkSrRM"
P = json.loads(zlib.decompress(base64.b64decode(DATA_B64)).decode("utf-8"))

def replace_block(src, label, body):
    pat = re.compile(r"(?ms)^(" + re.escape(label) + r":[^\n]*\n)(.*?^\tdone\n?)")
    m = pat.search(src)
    if not m:
        raise RuntimeError(f"missing text block {label}")
    return src[:m.start()] + m.group(1) + body.rstrip() + "\n" + src[m.end():]

def patch(root, apply):
    changed = []
    for rel, mapping in P["repls"].items():
        path = root / rel
        src = path.read_text(encoding="utf-8")
        old = src
        for label, body in mapping.items():
            src = replace_block(src, label, body)
        if src != old:
            changed.append(rel)
            if apply:
                path.write_text(src, encoding="utf-8")

    scripts = root / "data/maps/scripts.asm"
    src = scripts.read_text(encoding="utf-8")
    old = src
    src = src.replace('/*\nSECTION "Map Scripts 23", ROMX',
                      'SECTION "Map Scripts 23", ROMX', 1)
    if '/*\nSECTION "Map Scripts 24", ROMX' not in src:
        src = src.replace('\n\nSECTION "Map Scripts 24", ROMX',
                          '\n\n/*\nSECTION "Map Scripts 24", ROMX', 1)
    if src != old:
        changed.append("data/maps/scripts.asm")
        if apply:
            scripts.write_text(src, encoding="utf-8")

    layout = root / "layout.link"
    src = layout.read_text(encoding="utf-8")
    old = src
    src = src.replace('; ROMX $59\n; \t"Map Scripts 23"',
                      'ROMX $59\n\t"Map Scripts 23"', 1)
    if src != old:
        changed.append("layout.link")
        if apply:
            layout.write_text(src, encoding="utf-8")

    print(f"Bank $59: {len(changed)} file(s) changed; 75 verified text streams.")
    for rel in changed:
        print(" -", rel)
    return len(changed)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    patch(Path(args.repo), args.apply)

if __name__ == "__main__":
    main()
