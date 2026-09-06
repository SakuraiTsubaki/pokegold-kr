#!/usr/bin/env python3
"""Stage-1 Bank $57 recovery indexer.
Generate assembler-order text/raw-string manifest for Map Scripts 22,
following nested INCLUDEs exactly where they occur.
This is replaced by the verified recovery patcher after ROM matching.
"""
from pathlib import Path
import re, sys

FILES = [
    'maps/GoldenrodGym.asm', 'maps/GoldenrodBikeShop.asm',
    'maps/GoldenrodHappinessRater.asm', 'maps/BillsFamilysHouse.asm',
    'maps/GoldenrodMagnetTrainStation.asm', 'maps/GoldenrodFlowerShop.asm',
    'maps/GoldenrodPokecenter1F.asm', 'maps/GoldenrodPPSpeechHouse.asm',
    'maps/GoldenrodNameRater.asm', 'maps/GoldenrodDeptStore1F.asm',
    'maps/GoldenrodDeptStore2F.asm', 'maps/GoldenrodDeptStore3F.asm',
    'maps/GoldenrodDeptStore4F.asm', 'maps/GoldenrodDeptStore5F.asm',
    'maps/GoldenrodDeptStore6F.asm', 'maps/GoldenrodDeptStoreElevator.asm',
    'maps/GoldenrodGameCorner.asm', 'maps/IlexForestAzaleaGate.asm',
    'maps/Route34IlexForestGate.asm', 'maps/DayCare.asm',
]

LABEL_RE = re.compile(r'(?m)^([A-Za-z_][A-Za-z0-9_]*):[^\n]*\n')
INC_RE = re.compile(r'(?m)^INCLUDE\s+"([^"]+)"\s*$')
TEXT_RE = re.compile(r'(?m)^\ttext(?:_|\s)')

def scan_file(root, rel, out, raw, stack=()):
    if rel in stack:
        raise RuntimeError('recursive INCLUDE: ' + ' -> '.join(stack + (rel,)))
    src = (root / rel).read_text(encoding='utf-8')
    labels = list(LABEL_RE.finditer(src))
    includes = list(INC_RE.finditer(src))
    events = [(m.start(), 'label', m) for m in labels] + [(m.start(), 'include', m) for m in includes]
    events.sort(key=lambda x: x[0])
    for i, (pos, kind, m) in enumerate(events):
        end = events[i+1][0] if i + 1 < len(events) else len(src)
        if kind == 'label':
            block = src[m.end():end]
            if TEXT_RE.search(block):
                out.append((rel, m.group(1)))
        else:
            child = m.group(1)
            if (root / child).exists():
                scan_file(root, child, out, raw, stack + (rel,))
    for n, line in enumerate(src.splitlines(), 1):
        s = line.strip()
        if ('db ' in s or s.startswith('next ')) and '"' in s:
            raw.append((rel, n, s))

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '.')
    labels, raw = [], []
    for rel in FILES:
        scan_file(root, rel, labels, raw)
    lines = [
        '# Bank $57 / Map Scripts 22 assembler-order source index',
        f'# total text labels: {len(labels)}',
        '',
        '## TEXT LABELS (assembler order)',
    ]
    for i, (rel, label) in enumerate(labels, 1):
        lines.append(f'{i:03d}\t{rel}\t{label}')
    lines += ['', '## RAW QUOTED DB/NEXT DATA']
    for rel, n, s in raw:
        lines.append(f'{rel}:{n}\t{s}')
    lines.append('')
    out = root / 'tools/recovery/bank57_source_index.txt'
    text = '\n'.join(lines)
    if not out.exists() or out.read_text(encoding='utf-8') != text:
        out.write_text(text, encoding='utf-8')
        print(f'wrote {out} with {len(labels)} text labels and {len(raw)} raw quoted lines')
    else:
        print(f'{out} already current ({len(labels)} text labels, {len(raw)} raw quoted lines)')

if __name__ == '__main__':
    main()
