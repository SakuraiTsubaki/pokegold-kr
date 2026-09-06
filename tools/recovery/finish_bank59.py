#!/usr/bin/env python3
"""Stage-1 Bank $59 recovery indexer for Map Scripts 23."""
from pathlib import Path
import re, sys

FILES = [
    'maps/VermilionFishingSpeechHouse.asm',
    'maps/VermilionPokecenter1F.asm',
    'maps/VermilionPokecenter2FBeta.asm',
    'maps/PokemonFanClub.asm',
    'maps/VermilionMagnetTrainSpeechHouse.asm',
    'maps/VermilionMart.asm',
    'maps/VermilionDiglettsCaveSpeechHouse.asm',
    'maps/VermilionGym.asm',
    'maps/Route6SaffronGate.asm',
    'maps/Route6UndergroundPathEntrance.asm',
    'maps/RedsHouse1F.asm',
    'maps/RedsHouse2F.asm',
    'maps/BluesHouse.asm',
    'maps/OaksLab.asm',
]

def walk_file(root, rel, seen, order):
    if rel in seen:
        return
    seen.add(rel)
    src = (root / rel).read_text(encoding='utf-8')
    matches = list(re.finditer(r'(?m)^([A-Za-z_][A-Za-z0-9_]*):[^\n]*\n', src))
    for i, m in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(src)
        block = src[m.end():end]
        if re.search(r'(?m)^\ttext(?:_|\s)', block):
            order.append((rel, m.group(1)))
    for inc in re.findall(r'(?m)^INCLUDE\s+"([^"]+\.asm)"', src):
        if (root / inc).exists():
            walk_file(root, inc, seen, order)

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '.')
    seen=set(); order=[]
    for rel in FILES:
        walk_file(root, rel, seen, order)
    lines=['# Bank $59 / Map Scripts 23 assembler-order source index', f'# total text labels: {len(order)}', '', '## TEXT LABELS (assembler order)']
    lines += [f'{i:03d}\t{rel}\t{label}' for i,(rel,label) in enumerate(order,1)]
    lines += ['', '## RAW QUOTED DB/NEXT DATA']
    for rel in FILES:
        src=(root/rel).read_text(encoding='utf-8')
        for n,raw in enumerate(src.splitlines(),1):
            s=raw.strip()
            if ('db ' in s or s.startswith('next ')) and '"' in s:
                lines.append(f'{rel}:{n}\t{s}')
    out=root/'tools/recovery/bank59_source_index.txt'
    text='\n'.join(lines)+'\n'
    if not out.exists() or out.read_text(encoding='utf-8') != text:
        out.write_text(text,encoding='utf-8')
        print(f'wrote {out} with {len(order)} text labels')
    else:
        print(f'{out} already current ({len(order)} text labels)')

if __name__=='__main__':
    main()
