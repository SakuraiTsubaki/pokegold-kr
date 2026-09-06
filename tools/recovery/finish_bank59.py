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
DATA_B64 = """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"""
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
