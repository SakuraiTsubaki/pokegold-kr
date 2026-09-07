# SILVER KR 확장 엔진 — 원본 ROM 한계 및 최신 아키텍처

> 상태: CURRENT
> 기준일: 2026-09-07

## 1. 기준 저장소 / ROM

이 문서는 `SakuraiTsubaki/pokegold-kr`의 한국판 Gold/Silver 디스어셈블리를 구현 기준으로 삼는다.

Silver 기준 원본 ROM은 저장소에 포함하지 않으며, 빌드 시 사용자가 보유한 base ROM을 사용한다.

## 2. 현재 데이터셋 목표

현재 PokéAPI 계층 기준:

- Species: 1025
- Pokémon / battle variety: 1351
- Pokémon Form records: 1579

이 세 숫자는 서로 더하는 슬롯 수가 아니라 계층 구조다.

```text
Species
  -> Variety / Battle Profile
      -> Form / Appearance Record
```

현재 개수는 엔진 최대치가 아니다. 10세대 이후는 기존 ID를 유지하고 뒤에 append한다.

## 3. ID 아키텍처

최종 목표:

```text
SPECIES_NONE = 0x0000
SPECIES_*    = 0x0001..
VARIANT_*    = 0x0001..
0xffff       = reserved invalid/sentinel
```

- Species ID: uint16
- Variant ID: uint16
- Form: 별도 form layer
- EGG: Species namespace 밖의 개체 상태/특수 처리

`SPECIES_*`는 가능한 한 National Dex 번호와 일치시키고, 새로운 세대는 재번호 없이 append한다.

## 4. 원본 8-bit Species 한계

원본 Gen II는 `MON_SPECIES`, `wCurSpecies`, 파티/박스의 빠른 species 목록, 야생/트레이너/진화/링크 등 다수 경로에서 species를 1 byte로 취급한다.

원본 Pokémon 상수는 251종을 `0x01..0xfb`에 배치하고 `0xfd`를 EGG로 사용한다.

따라서 무개조 원본의 실질 species 한계는 251이다.

단순히 BaseData 테이블만 늘려서는 확장되지 않는다. 모든 8-bit copy/index/compare 경로를 감사하고 확장 ID를 전달해야 한다.

## 5. BoxMon / SRAM

원본 BoxMon 구조는 32 bytes이며 Pokerus 뒤, Level 앞에 2 bytes의 unused 영역이 있다.

이 공간은 확장 ID/form metadata를 저장하는 후보로 사용할 수 있다.

중요 원칙:

- BoxMon 32-byte 크기는 가능한 한 유지한다.
- species 확장 때문에 박스 전체 SRAM 레이아웃을 키우는 방식은 피한다.
- 별도의 빠른 species list나 Hall of Fame, daycare 등에서 1-byte truncation이 발생하지 않도록 별도로 패치한다.

## 6. BaseData

원본 BaseData는 32 bytes/record이다.

```text
251  x 32 =  8,032 bytes
1025 x 32 = 32,800 bytes
1351 x 32 = 43,232 bytes
1579 x 32 = 50,528 bytes
```

따라서 battle parameter 고정 테이블 자체는 주된 용량 병목이 아니다.

문제는 원본 `GetBaseData`가 8-bit species index와 단일 bank 배치를 전제로 한다는 점이다. 멀티-bank + extended-ID lookup으로 변경한다.

## 7. Pokédex

원본 seen/caught는 `NUM_POKEMON` 크기의 bit array이다.

```text
251 species  -> 32 bytes per bitset
1025 species -> 129 bytes per bitset
```

비트맵 용량 자체는 작다. 문제는 WRAM/save 구조 위치, 카운트 루틴, UI index가 251-era 설계라는 점이다.

Seen/Caught와 관련 UI를 모두 16-bit-safe하게 일반화한다.

## 8. Move / Item은 별도 확장 과제

Species 확장과 별개로 원본 Move ID와 Item ID도 8-bit이다.

현 단계에서는 Silver 원본 엔진에 맞춘 포켓몬 파라미터를 우선 구현하고, 현대 전체 Move/Item namespace 확장은 별도 단계로 다룬다.

특히 BoxMon은 move 4개를 각각 1 byte로 저장하므로 모든 현대 기술을 단순 u16화하면 SRAM 비용이 크다.

## 9. 이름 길이

원본 국제판 기준 고정 길이는 다음과 같은 제약이 있다.

```text
MON_NAME_LENGTH           = 11
MOVE_NAME_LENGTH          = 13
ITEM_NAME_LENGTH          = 13
TRAINER_CLASS_NAME_LENGTH = 13
```

현대 공식명 전체를 그대로 표시하려면 이름 포인터/가변길이 렌더링 또는 언어별 확장 UI가 필요하다.

## 10. ROM 용량 / Mapper

Silver는 MBC3 + RTC 구조다.

- 일본 Silver 계열: 1 MiB / 64 banks
- 국제/한국 Silver 계열: 2 MiB / 128 banks
- SRAM: 32 KiB

MBC3를 그대로 유지하면 2 MiB ROM이 실질 상한이다.

8개 Silver ROM 비교에서 국제/한국 2 MiB 6개 빌드에 공통으로 완전히 0인 bank가 20개(320 KiB) 확인되었다.

일본 1 MiB 두 개까지 2 MiB로 zero-padding한 뒤 8개 모두에서 공통으로 비어 있는 bank는 11개(176 KiB)다.

파라미터 테이블은 이 공간에서 충분히 시작할 수 있지만, 1351 variety / 1579 form의 full front/back sprite, animation, palette, icon, cry까지 모두 넣는 시점에는 2 MiB가 병목이 될 가능성이 높다.

## 11. 그래픽 구조

그래픽은 Species ID 산술로 직접 찾지 않고 명시적 매핑으로 일반화한다.

```text
Species / Variant / Form
        -> GraphicSetID
        -> front/back
        -> palette
        -> icon
        -> animation/metadata
```

동일한 그래픽 자산은 deduplicate한다.

## 12. 10세대 이후 확장 규칙

현재 숫자:

```text
NUM_SPECIES  = 1025
NUM_VARIANTS = 1351
NUM_FORMS    = 1579
```

이 값들은 데이터 개수다.

엔진 ID 폭은 별도로 유지한다.

```text
Species ID : uint16
Variant ID : uint16
Form table : appendable
```

한번 배정된 ID는 절대 재배치하지 않는다.

## 13. 구현 순서

1. Species/Variant 16-bit ID API 정의
2. EGG를 Species namespace에서 분리
3. party / box / temp / battle species 전달 경로 확장
4. wild / trainer / evolution / daycare / Hall of Fame / link 경로 확장
5. BaseData multi-bank lookup
6. names / cries / icon / sprite / palette lookup 일반화
7. Pokédex seen/caught 저장과 UI 확장
8. 1025 Species / 1351 Variant 실제 데이터 주입
9. 1579 Form mapping 연결
10. 그래픽 실측 후 MBC3 2 MiB 유지 여부 재판정

## 14. 저장소 정책

- 원본 상용 ROM: 커밋 금지
- 개조 ROM 전체 바이너리: 커밋 금지
- 허용: 디스어셈블리 소스, ASM 수정, 문서, manifest, hash, 생성기, IPS/BPS 등 차분 패치, 검증 도구

실제 구현은 본 저장소의 기존 `constants/`, `data/`, `engine/`, `home/`, `ram/` 구조를 우선 사용한다.
