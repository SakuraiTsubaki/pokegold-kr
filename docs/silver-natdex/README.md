# SILVER NatDex Expansion

이 디렉터리는 포켓몬스터 은 한국판 디스어셈블리를 기준으로 전국도감 확장 엔진을 구현하기 위한 문서와 재현 가능한 작업 기록을 보관한다.

## 현재 목표

- National Dex Species: 1025
- Battle Variety / PokéAPI Pokémon records: 1351
- Pokémon Form records: 1579
- Generation 10+: 기존 ID 재배치 없이 append-only 확장

## 구현 원칙

- `SPECIES_*`는 National Dex Species ID를 사용한다.
- EGG는 `SPECIES_*` 공간에서 분리한다.
- Species / Variety / Form은 서로 다른 계층으로 유지한다.
- Species와 Variety는 처음부터 16-bit 확장 구조를 기준으로 구현한다.
- 원본 32-byte BoxMon 구조는 가능한 한 유지한다.
- 원본 ROM이나 개조 ROM 전체 바이너리는 저장소에 커밋하지 않는다.

## 파일

- `SILVER_ROM_LIMITS_AND_ARCHITECTURE.md`: 원본 은 한국판 및 8개 Silver ROM 비교를 반영한 엔진 한계/확장 구조
- `SILVER_GITHUB_AUTOSYNC_POLICY.md`: 자동 GitHub 반영 규칙

실제 엔진 변경은 이 저장소의 `constants/`, `data/`, `engine/`, `home/`, `ram/` 등 기존 디스어셈블리 구조에 맞춰 반영한다.
