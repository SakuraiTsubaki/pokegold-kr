#!/usr/bin/env python3
"""Stage-1 Bank $5A / Map Scripts 24 source indexer."""
from pathlib import Path
import re, sys

FILES = [
    'maps/PewterNidoranSpeechHouse.asm',
    'maps/PewterGym.asm',
    'maps/PewterMart.asm',
    'maps/PewterPokecenter1F.asm',
    'maps/PewterPokecenter2FBeta.asm',
    'maps/PewterSnoozeSpeechHouse.asm',
    'maps/IndigoPlateauPokecenter1F.asm',
    'maps/WillsRoom.asm',
    'maps/KogasRoom.asm',
    'maps/BrunosRoom.asm',
    'maps/KarensRoom.asm',
    'maps/LancesRoom.asm',
    'maps/HallOfFame.asm',
]

def text_labels(src):
    matches = list(re.finditer(r'(?m)^([A-Za-z_][A-Za-z0-9_]*):[^\n]*\n', src))
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(src)
        if re.search(r'(?m)^\ttext(?:_|\s)', src[m.end():end]):
            out.append(m.group(1))
    return out

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '.')
    lines = ['# Bank $5A / Map Scripts 24 assembler-order source index', '']
    total = 0
    for rel in FILES:
        src = (root / rel).read_text(encoding='utf-8')
        labels = text_labels(src)
        total += len(labels)
        lines.append(f'## {rel} ({len(labels)} text labels)')
        lines.extend(f'{label}' for label in labels)
        lines.append('RAW QUOTED DB/NEXT DATA:')
        for n, raw in enumerate(src.splitlines(), 1):
            s = raw.strip()
            if ('db ' in s or s.startswith('next ')) and '"' in s:
                lines.append(f'raw:{n}\t{s}')
        lines.append('')
    lines.insert(1, f'# total text labels: {total}')
    out = root / 'tools/recovery/bank5a_source_index.txt'
    text = '\n'.join(lines) + '\n'
    if not out.exists() or out.read_text(encoding='utf-8') != text:
        out.write_text(text, encoding='utf-8')
        print(f'wrote {out} with {total} text labels')
    else:
        print(f'{out} already current ({total} text labels)')

if __name__ == '__main__':
    main()
