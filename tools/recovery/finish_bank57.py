#!/usr/bin/env python3
"""Stage-1 Bank $57 recovery indexer.
Generates a deterministic label/raw-string manifest for Map Scripts 22.
This file is replaced by the verified recovery patcher after ROM matching.
"""
from pathlib import Path
import re, sys

FILES = [
    'maps/GoldenrodGym.asm',
    'maps/GoldenrodBikeShop.asm',
    'maps/GoldenrodHappinessRater.asm',
    'maps/BillsFamilysHouse.asm',
    'maps/GoldenrodMagnetTrainStation.asm',
    'maps/GoldenrodFlowerShop.asm',
    'maps/GoldenrodPokecenter1F.asm',
    'maps/GoldenrodPPSpeechHouse.asm',
    'maps/GoldenrodNameRater.asm',
    'maps/GoldenrodDeptStore1F.asm',
    'maps/GoldenrodDeptStore2F.asm',
    'maps/GoldenrodDeptStore3F.asm',
    'maps/GoldenrodDeptStore4F.asm',
    'maps/GoldenrodDeptStore5F.asm',
    'maps/GoldenrodDeptStore6F.asm',
    'maps/GoldenrodDeptStoreElevator.asm',
    'maps/GoldenrodGameCorner.asm',
    'maps/IlexForestAzaleaGate.asm',
    'maps/Route34IlexForestGate.asm',
    'maps/DayCare.asm',
]

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '.')
    lines = ['# Bank $57 / Map Scripts 22 source index', '']
    total = 0
    for rel in FILES:
        src = (root / rel).read_text(encoding='utf-8')
        labels = []
        # A text data label is any top-level label whose block contains a text macro.
        matches = list(re.finditer(r'(?m)^([A-Za-z_][A-Za-z0-9_]*):[^\n]*\n', src))
        for i, m in enumerate(matches):
            end = matches[i+1].start() if i+1 < len(matches) else len(src)
            block = src[m.end():end]
            if re.search(r'(?m)^\ttext(?:_|\s)', block):
                labels.append(m.group(1))
        total += len(labels)
        lines.append(f'## {rel} ({len(labels)} text labels)')
        lines.extend(f'{n+1:03d}\t{label}' for n, label in enumerate(labels))
        lines.append('RAW QUOTED DB/NEXT DATA:')
        for n, raw in enumerate(src.splitlines(), 1):
            s = raw.strip()
            if ('db ' in s or s.startswith('next ')) and '"' in s:
                lines.append(f'raw:{n}\t{s}')
        lines.append('')
    lines.insert(1, f'# total text labels: {total}')
    out = root / 'tools/recovery/bank57_source_index.txt'
    text = '\n'.join(lines) + '\n'
    if not out.exists() or out.read_text(encoding='utf-8') != text:
        out.write_text(text, encoding='utf-8')
        print(f'wrote {out} with {total} text labels')
    else:
        print(f'{out} already current ({total} text labels)')

if __name__ == '__main__':
    main()
