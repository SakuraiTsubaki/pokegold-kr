#!/usr/bin/env python3
from pathlib import Path
import argparse


def patch(repo: Path, apply: bool) -> int:
    changed = 0

    scripts = repo / "data/maps/scripts.asm"
    src = scripts.read_text(encoding="utf-8")
    old = src

    marker21 = '/*\nSECTION "Map Scripts 21", ROMX\n'
    active21 = 'SECTION "Map Scripts 21", ROMX\n'
    if marker21 in src:
        src = src.replace(marker21, active21, 1)

    marker22 = 'SECTION "Map Scripts 22", ROMX\n'
    commented22 = '/*\nSECTION "Map Scripts 22", ROMX\n'
    if marker22 in src and commented22 not in src:
        src = src.replace(marker22, commented22, 1)

    if src != old:
        changed += 1
        if apply:
            scripts.write_text(src, encoding="utf-8")
        print(("patched " if apply else "would patch ") + str(scripts.relative_to(repo)))

    layout = repo / "layout.link"
    src = layout.read_text(encoding="utf-8")
    old = src
    disabled = '; ROMX $56\n; \t"Map Scripts 21"'
    enabled = 'ROMX $56\n\t"Map Scripts 21"'
    if disabled in src:
        src = src.replace(disabled, enabled, 1)

    if src != old:
        changed += 1
        if apply:
            layout.write_text(src, encoding="utf-8")
        print(("patched " if apply else "would patch ") + str(layout.relative_to(repo)))

    print(f"Bank $56 enable: {changed} file(s) changed.")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    patch(Path(args.repo), args.apply)


if __name__ == "__main__":
    main()
