# Project Standards

## Naming and layout

- Use stable, descriptive, machine-friendly paths.
- Preserve meaningful Korean target IDs, bank/section addresses, symbols, text/font identifiers, and original indices.
- Represent material release or revision differences in paths or metadata.
- Do not force another generation or another public disassembly's layout onto the Korean target.

## Source and generated material

Prefer editable source plus reproducible conversion over opaque output. Generated files should identify source and method. Keep scripts and tools required to regenerate important outputs.

## Deduplication and evidence

Deduplicate only with strong reproducible evidence. Separate confirmed observations from hypotheses; use `unknown` or `TBD` rather than inventing metadata.

## Structure

Keep one live structure. Do not recreate historical migration/version trees; Git history is the historical record.

## Repository safety

Do not commit retail or rebuilt playable ROM images, console keys, or equivalent complete game-image containers.
