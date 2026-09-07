# GOLD KR National Dex / Extended Pokémon Engine

이 디렉터리는 한글판 Pokémon Gold를 기반으로 한 확장 Pokémon 엔진 조사와 구현 기록을 관리한다.

## 현재 기준

- `GOLD_ROM_LIMITS_AND_ARCHITECTURE.md` — **최신 설계 문서**
- `GOLD_GITHUB_AUTOSYNC_POLICY.md` — 저장소 반영/저작권 바이너리 제외 정책

현재 엔진 목표:

```text
Species ID : uint16
Variety ID : uint16
Form ID    : uint16

현재 데이터셋: 1025 / 1351 / 1579
미래 세대: 기존 ID 유지 + append-only
```

## Stage 0

`stage0/`는 초기 `0xFC + ext16` sentinel 모델을 실제 ROM에서 검증하기 위한 프로토타입 기록이다.

이 방식은 **최종 아키텍처가 아니며**, 최신 구현은 native 16-bit ID 설계를 따른다.

## ROM 정책

원본 및 수정 ROM 바이너리는 이 저장소에 커밋하지 않는다. 패치, 소스, 스크립트, 매니페스트, 분석 자료만 관리한다.
