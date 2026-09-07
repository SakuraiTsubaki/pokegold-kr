# GOLD KR 확장 엔진 — 원본 ROM 한계 및 최신 아키텍처

> 상태: CURRENT / Stage 0 프로토타입 설계를 대체하는 최신 기준

## 1. 기준 ROM

- 파일: `Pocket Monsters Geum (Korea).gbc`
- SHA-1: `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65`
- 크기: 2 MiB (`128 × 16 KiB ROM banks`)
- 카트리지: MBC3 + RTC + RAM + Battery
- SRAM: 32 KiB (`4 × 8 KiB`)
- 원본 ROM은 저장소에 포함하지 않는다.

## 2. 현재 데이터셋 목표

현재 데이터 기준:

- Species: 1025
- Battle Variety / Pokemon record: 1351
- Form record: 1579

이 숫자들은 **현재 등록 개수**이지 엔진 상한이 아니다. 10세대 이후 추가를 위해 런타임 ID 폭은 처음부터 16비트로 설계한다.

```text
Species ID : uint16
Variety ID : uint16
Form ID    : uint16
```

현재:

```text
SPECIES_NONE = 0
SPECIES_*    = 1..1025
VARIETY_*    = 1..1351
FORM_*       = 1..1579
```

미래 세대는 기존 ID를 재배치하지 않고 뒤에 append한다.

## 3. EGG 처리

원본 Gen II는 `0xFD = EGG`를 species 상수 공간에 두지만, 확장 엔진에서는 EGG를 species에서 분리한다.

```text
SPECIES_NONE = 0
SPECIES_*    = 1..
EGG          = 별도 개체 상태/flag
```

즉 최종 목표에서 `SPECIES_* ID == National Dex species number`를 유지한다.

## 4. 원본 ROM의 확실한 빈 공간

원본 128개 ROM bank를 실측한 결과 다음 24개 bank가 통째로 `00`이다.

```text
13 22 27 28 29 2C 2D 2F
34 35
58
63 67
6A 6B 6F
73 74 75 76 77
7C 7D 7E
```

합계:

- 24 banks
- 393,216 bytes
- 384 KiB

부분적으로 비어 있는 bank도 추가로 존재하지만, 이 영역은 링커 맵/실행 경로 검증 후 사용한다.

## 5. Species 확장의 실제 난점

원본의 `MON_SPECIES`는 1바이트이며 Pokémon 상수는 `01..FB` 251종을 전제로 한다.

관련 원본 소스:

- `constants/pokemon_constants.asm`
- `constants/pokemon_data_constants.asm`
- `home/pokemon.asm:GetBaseData`

따라서 아래를 16비트 안전 방식으로 변경해야 한다.

- party / box species access
- wild encounter records
- trainer party records
- evolution targets
- names
- base data
- cries
- sprites / palettes / icons
- Pokédex indexing
- breeding / daycare
- Hall of Fame
- link/trade compatibility layer

## 6. BaseData는 용량 병목이 아니다

원본 BaseData는 32 bytes/record이다.

```text
251  × 32 =  8,032 bytes
1351 × 32 = 43,232 bytes
증가량       35,200 bytes
```

따라서 1351 battle profile의 기본 스탯/타입/성비/성장률/알그룹 등의 고정 데이터는 현재 2 MiB ROM 안에서도 충분히 수용 가능하다.

## 7. BOXMON / SRAM 한계

원본 `BOXMON_STRUCT_LENGTH`는 32 bytes이며 한 박스 20마리, 총 14박스다.

원본 소스는 14개 박스가 정확히 2개의 SRAM bank에 걸쳐 배치된다고 명시한다.

따라서 구조체 자체를 마리당 여러 바이트 늘리는 방식은 피한다.

Gold/Silver 구조에는 `MON_POKERUS` 뒤, `MON_LEVEL` 앞에 `rb_skip 2`가 존재한다. 이 2바이트는 확장 메타데이터 저장 후보로 활용 가능하다.

목표:

- BOXMON 32-byte 크기는 가능한 한 유지
- 추가 정보는 예약 2바이트 + 외부 확장 테이블/압축 인덱스를 조합

## 8. 더 큰 병목: Move ID

원본은 한 포켓몬이 보유한 4개 move ID를 각각 1바이트로 저장한다.

원본 기술:

```text
00    = NO_MOVE
01-FB = 251 moves
FF    = 특수 상태값(CANNOT_MOVE 등)
```

현대 전체 기술을 넣으려면 move namespace 확장이 필요하다.

단순히 4개 move를 모두 uint16으로 바꾸면 BoxMon 하나당 +4 bytes가 필요해 SRAM 레이아웃을 크게 흔든다.

따라서 Move ID는 다음 중 하나의 압축/확장 계층이 필요하다.

- 8-bit local move dictionary + 16-bit master move ID
- extension bitfield / side table
- save-format versioned extended move slots

이 부분이 Species ID 확장보다 더 까다로운 핵심 설계 과제다.

## 9. Item ID 역시 8비트

`MON_ITEM`도 1바이트다. 현대 지닌도구/진화도구 전체를 지원하려면 item namespace 확장이 필요하다.

Species/Move/Item 중 실제 세이브 호환성 위험도는 대체로 다음과 같다.

```text
Species < Item < Move
```

특히 Move는 개체당 4개 필드를 사용하므로 가장 비용이 크다.

## 10. Pokédex

원본은 `wPokedexCaught` / `wPokedexSeen`을 `flag_array NUM_POKEMON`으로 저장한다.

251종:

```text
ceil(251/8) × 2 = 64 bytes
```

1025종:

```text
ceil(1025/8) × 2 = 258 bytes
```

증가량은 +194 bytes에 불과하므로 bitset 자체는 문제가 아니다.

다만 seen/caught 집계 및 UI에서 8비트 count/index를 쓰는 루틴은 16비트화해야 한다.

## 11. Form / Variety

원본 Gen II에는 범용 Form/Variety 시스템이 없다. Unown은 전용 예외 구현이다.

최종 계층:

```text
Species (National Dex identity)
  └─ Variety / Battle Profile
       └─ Form / Appearance record
```

- Species: 도감상의 종
- Variety: 능력치/타입/특성/배틀 규칙이 달라지는 프로필
- Form: 외형 차이까지 포함하는 표현 레코드

## 12. 현대 시스템 확장

원본에 필드 자체가 없는 요소는 기존 BaseData를 무작정 늘리지 않고 별도 확장 테이블에 둔다.

예:

- Ability
- Nature
- per-move Physical/Special/Status category
- modern EV model
- modern evolution methods
- regional/form mechanics
- future-generation metadata

## 13. ROM 용량 병목

1025 Species / 1351 battle profiles / 1579 form directory 자체는 작은 편이다.

최종 용량 병목은 다음이다.

1. front/back sprite data
2. form-specific graphics
3. move data + animations
4. Pokédex text
5. cries/audio

스프라이트는 버전/폼별로 추출한 뒤 **바이트 동일 자산을 deduplicate**하는 것을 기본 원칙으로 한다.

## 14. Mapper 확장 경로

현재:

```text
MBC3
2 MiB ROM
128 ROM banks
32 KiB SRAM
```

2 MiB가 부족해지면 첫 확장 후보는 MBC30 계열이다.

```text
MBC30 target
4 MiB ROM
256 ROM banks
최대 64 KiB SRAM 구조 검토
```

원본 `Bankswitch`는 bank 번호를 1바이트로 관리하므로 00..FF 256-bank 설계와 구조적으로 궁합이 좋다.

8 MiB MBC5까지 가면 9번째 ROM-bank bit가 필요하므로 bank API 자체를 더 크게 바꿔야 한다.

## 15. 현재 결론

원본의 진짜 하드캡은 단순한 "251 Pokémon"이 아니다.

```text
1) Species / Move / Item = 8-bit namespace
2) BOXMON = 32 bytes + 빡빡한 32 KiB SRAM
3) MBC3 = 2 MiB / 128 ROM banks
```

따라서 최종 엔진 목표는 다음으로 정의한다.

```text
Extensible 16-bit Pokémon Engine

- Species ID: 16-bit
- Variety ID: 16-bit
- Form ID: 16-bit
- current dataset: 1025 / 1351 / 1579
- future generations: append-only
- EGG: species namespace 밖의 state
- BOXMON size: 가능하면 32 bytes 유지
- Move/Item: 별도 확장 namespace 설계
- ROM: 2 MiB 우선, 필요 시 4 MiB MBC30
```

## 16. Stage 0 프로토타입과의 관계

초기 Stage 0 ROM/IPS는 `0xFC + ext16 species` sentinel 모델을 실험하기 위한 기반이다.

**현재 아키텍처에서는 이 sentinel 방식을 최종 설계로 채택하지 않는다.** Stage 0 파일은 재현 가능한 초기 실험 기록으로 보존하며, 앞으로의 소스 구현은 본 문서의 16비트 native ID 설계를 기준으로 진행한다.
