# SILVER GitHub Autosync Policy

## Canonical implementation repository

`SakuraiTsubaki/pokegold-kr`

이 저장소가 한국판 Gold/Silver 디스어셈블리 및 실제 엔진 구현의 기준 저장소다.

## 자동 반영 대상

작업 중 생성되는 다음 안전한 산출물은 구현 단계가 끝날 때 GitHub에 반영한다.

- ASM/source changes
- constants / data / engine patches
- build/verification scripts
- manifests and hashes
- documentation
- IPS/BPS 등 차분 패치
- 테스트 및 분석 결과 중 구현에 직접 필요한 자료

## 업로드 금지

- 원본 상용 ROM 전체 바이너리
- 개조 ROM 전체 바이너리
- 사용자의 save/RTC/state 파일
- 저작권상 재배포하면 안 되는 원본 추출물

## 보조 저장소 역할

- `SakuraiTsubaki/Sakurai`: 여러 언어/리비전 간 비교, census, 분석 보고서
- `SakuraiTsubaki/Tsubaki`: sprites, graphics, palettes, fonts, icons, converted resources 등 재사용 가능한 작업 자산

SILVER 엔진 자체의 canonical source of truth는 항상 `pokegold-kr`로 둔다.
