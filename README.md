# Pocket Monsters Gold (Korea) — Disassembly

![Status](https://img.shields.io/badge/status-initial_setup-lightgrey)
![Project](https://img.shields.io/badge/project-disassembly-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Disassembly and source-reconstruction project for **Pocket Monsters Gold (Korea)**.

## 🎯 Goals

- Reconstruct the Korean game code and data into readable, editable assembly/source form.
- Document ROM banks, code, data, text, graphics, audio, maps, scripts, and Korean-specific structures.
- Preserve exact Korean release identity, provenance, version differences, and reproducible verification.
- Build a clean foundation for long-term Korean Generation II reverse-engineering work.

## 🚧 Status

This repository is in its **initial setup** stage. Source reconstruction and documentation will be added progressively.

## 🗂️ Planned scope

- ROM, bank, section, and code analysis
- Korean text, character tables, fonts, and encoding
- Game data structures
- Scripts and event data
- Graphics and asset metadata
- Audio and resource formats
- Maps and world data
- Tools, notes, manifests, and verification data

## 📌 Repository policy

ROM images and redistributed ROM binaries are **not included**. The repository is intended for reconstructed source, extracted/recreated project data, tooling, analysis, and documentation.

## 🧭 Roadmap

- [ ] Establish baseline Korean version/revision inventory
- [ ] Map ROM banks, sections, text/font systems, and data structures
- [ ] Begin source reconstruction
- [ ] Document graphics, scripts, maps, audio, and formats
- [ ] Add build, matching, verification, and reproducibility workflow

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Project status](docs/PROJECT_STATUS.md) | Current stage, coverage, validation level, and next milestones |
| [Roadmap](docs/ROADMAP.md) | Recommended disassembly phases and long-term progression |
| [Version coverage](docs/VERSIONS.md) | Korean release/revision/build identity and hashes |
| [Research guide](docs/RESEARCH_GUIDE.md) | Evidence, confidence, and research-recording workflow |
| [Verification guide](docs/VERIFICATION.md) | Standards for Observed, Reproduced, and Matched results |
| [Repository structure](docs/REPOSITORY_STRUCTURE.md) | Intended long-term source, data, asset, tooling, and manifest layout |
| [Documentation hub](docs/README.md) | Entry point for code, text, format, asset, version, and verification notes |

## 🧱 Repository structure

As real project material is reconstructed, the repository may grow into areas such as `asm/`, `data/`, `text/`, `assets/`, `tools/`, `tests/`, and `manifests/`. Empty directory trees are not created only for appearance, and detailed layout should follow the verified Korean target architecture.

See [Repository Structure](docs/REPOSITORY_STRUCTURE.md) for the full organization policy.

## 🔬 Research and verification

Research findings should identify the exact Korean target version or revision and clearly separate hypotheses from observed, reproduced, or matched results.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules, evidence expectations, commit guidance, and pull-request requirements.
