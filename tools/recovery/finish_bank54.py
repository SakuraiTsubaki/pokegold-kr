#!/usr/bin/env python3
"""Apply the Korean Silver Bank $54 / Map Scripts 19 reconstruction to pokegold-kr.

Source ROM SHA-1: cb22d7e03a74dc3a563fde6be8626626b2b392e7
This script changes text/data source only; it never writes ROM bytes into the repository.
"""
from pathlib import Path
import argparse, hashlib, re

EXPECTED_ROM_SHA1 = 'cb22d7e03a74dc3a563fde6be8626626b2b392e7'
REPLACEMENTS = {'maps/CeruleanGymBadgeSpeechHouse.asm': {'CeruleanGymBadgeSpeechHousePokefanMText': 'CeruleanGymBadgeSpeechHousePokefanMText:\n\ttext "관동의 체육관 배지를 모으니?"\n\tdone'}, 'maps/CeruleanPoliceStation.asm': {'CeruleanPoliceStationFishingGuruText': 'CeruleanPoliceStationFishingGuruText:\n\ttext "수상한 녀석이"\n\tline "어슬렁거리고 있다는 이야기다!"\n\tpara "도둑놈이라면"\n\tline "내가 용서하지 않겠어!"\n\tdone', 'CeruleanPoliceStationPokefanFText': 'CeruleanPoliceStationPokefanFText:\n\ttext "예전에"\n\tline "도둑을 맞은 적이 있었어"\n\tdone', 'CeruleanDiglettText': 'CeruleanDiglettText:\n\ttext "디그다『디그 디그다"\n\tdone'}, 'maps/CeruleanTradeSpeechHouse.asm': {'CeruleanTradeSpeechHouseGrannyText': 'CeruleanTradeSpeechHouseGrannyText:\n\ttext "우리 영감은"\n\tpara "여러 사람들과 교환한"\n\tline "포켓몬들과"\n\tcont "행복하게 지내고 있단다"\n\tdone', 'CeruleanTradeSpeechHouseGrampsText': 'CeruleanTradeSpeechHouseGrampsText:\n\ttext "아-……"\n\tline "난- 행복하구나-"\n\tdone', 'CeruleanTradeSpeechHouseRhydonText': 'CeruleanTradeSpeechHouseRhydonText:\n\ttext "캥카『캥카 캥카!"\n\tdone', 'CeruleanTradeSpeechHouseZubatText': 'CeruleanTradeSpeechHouseZubatText:\n\ttext "주벳『주벳 주벳!"\n\tdone'}, 'maps/CeruleanPokecenter1F.asm': {'CeruleanPokecenter1FSuperNerdText': 'CeruleanPokecenter1FSuperNerdText:\n\ttext "동쪽으로 펼쳐져 있는"\n\tline "9번도로의 끝에"\n\tcont "발전소가 있단다"\n\tdone', 'CeruleanPokecenter1FGymGuideText': 'CeruleanPokecenter1FGymGuideText:\n\ttext "리니어 기차는 시속 550km!"\n\tline "관동과 성도를"\n\tcont "눈 깜짝할 사이에 왕복한다!"\n\tpara "이것으로 성도에서도"\n\tline "살기 쉽게 되었지!"\n\tdone'}, 'maps/CeruleanGym.asm': {'CeruleanGymGruntIntroText': 'CeruleanGymGruntIntroText:\n\ttext "오우! 쏘리!"\n\tline "유 상처 낫씽입니까?"\n\tcont "나는 베리 비지해요!"\n\tcont "유랑 천천히 토킹"\n\tcont "할 수 없어요!"\n\tcont "누군가에게 발견되면"\n\tcont "난 골란해지니까요!"\n\tdone', 'CeruleanGymGruntBigMistakeText': 'CeruleanGymGruntBigMistakeText:\n\ttext "……오- 노-!"\n\tline "이미 유에게 들켜버렸네요!"\n\tcont "빅 마이 미스테이크!"\n\tdone', 'CeruleanGymGruntByeText': 'CeruleanGymGruntByeText:\n\ttext "헤이 유!"\n\tline "이 일에대해 포겟 해야해!"\n\tcont "유는 아무것도 못 봤다"\n\tcont "듣지도 않고 모르는거다!"\n\tpara "바이 키드!"\n\tline "롱 굿바이!"\n\tdone', 'CeruleanGymNote1Text': 'CeruleanGymNote1Text:\n\ttext "잠시 외출합니다"\n\tline "…… 체육관 관장 이슬"\n\tdone', 'CeruleanGymNote2Text': 'CeruleanGymNote2Text:\n\ttext "이슬이가 없어서"\n\tline "놀러 다녀오겠습니다"\n\tcont "…… 체육관 트레이너 일동"\n\tdone', 'MistyIntroText': 'MistyIntroText:\n\ttext "이슬『왔구나!"\n\tline "방해꾼 나으리!"\n\tpara "성도의 체육관 배지를"\n\tline "많이 가지고 있어 보이지만"\n\tcont "나를 얕보다간 큰 코 다칠껄"\n\tpara "내 물타입의 포켓몬은"\n\tline "무척 강하다구!"\n\tdone', 'MistyWinLossText': 'MistyWinLossText:\n\ttext "이슬『꽤 하는군……"\n\tpara "너의 실력"\n\tline "마음을 비우고 받아들이지……"\n\tpara "자 이거"\n\tline "블루배지야!"\n\tdone', 'ReceivedCascadeBadgeText': 'ReceivedCascadeBadgeText:\n\ttext "<PLAYER>는(은) 이슬이로부터"\n\tline "블루배지를 얻었다!"\n\tdone', 'MistyFightDoneText': 'MistyFightDoneText:\n\ttext "이슬『강한 트레이너가"\n\tline "성도에는 많이 있니?"\n\tcont "너처럼"\n\tpara "나도 언젠가 여행을 떠나서"\n\tline "강한 트레이너랑 싸울꺼야!"\n\tdone', 'SwimmerfDianaSeenText': 'SwimmerfDianaSeenText:\n\ttext "미안 부재중이어서"\n\tline "그럼 바로 승부에 들어갈까!"\n\tdone', 'SwimmerfDianaBeatenText': 'SwimmerfDianaBeatenText:\n\ttext "아잉 몰라!"\n\tline "내가 졌어!"\n\tdone', 'SwimmerfDianaAfterBattleText': 'SwimmerfDianaAfterBattleText:\n\ttext "우아하게 헤엄치고 있습니다"\n\tdone', 'SwimmerfBrianaSeenText': 'SwimmerfBrianaSeenText:\n\ttext "나의 화려한"\n\tline "헤엄치기를 보고 놀라지마세요!"\n\tdone', 'SwimmerfBrianaBeatenText': 'SwimmerfBrianaBeatenText:\n\ttext "전혀 놀라지 않는군……"\n\tline "엄청 냉정하네……!"\n\tdone', 'SwimmerfBrianaAfterBattleText': 'SwimmerfBrianaAfterBattleText:\n\ttext "나를 쓰러뜨렸다고해서"\n\tline "안심하지 마라"\n\tcont "이슬이는 정말 강하니까!"\n\tdone', 'SwimmermParkerSeenText': 'SwimmermParkerSeenText:\n\ttext "어푸!"\n\tpara "먼저 내가 상대다!"\n\tline "덤벼라!"\n\tdone', 'SwimmermParkerBeatenText': 'SwimmermParkerBeatenText:\n\ttext "이럴리 없는데"\n\tdone', 'SwimmermParkerAfterBattleText': 'SwimmermParkerAfterBattleText:\n\ttext "이슬이는 요 근래 수년동안"\n\tline "점점 강해졌단다!"\n\tcont "방심하지말거라"\n\tcont "혼쭐이 날테니까!"\n\tdone', 'CeruleanGymGuideText': 'CeruleanGymGuideText:\n\ttext "야아-!"\n\tline "미래의 챔피언!"\n\tpara "이슬이가 없어서"\n\tline "우리들도 놀러 갔었단다"\n\tcont "와하하하핫!"\n\tdone', 'CeruleanGymGuideWinText': 'CeruleanGymGuideWinText:\n\ttext "역시 강하구나!"\n\tline "좋은 시합이었어!"\n\tdone'}, 'maps/CeruleanMart.asm': {'CeruleanMart_CooltrainerMText': 'CeruleanMart_CooltrainerMText:\n\ttext "블루시티의 호수공원으로 가는 도중"\n\tline "많은 트레이너가 있단다"\n\tpara "걸려들면 트레이너의"\n\tline "실력을 확인하고 있으니까"\n\tdone', 'CeruleanMart_CooltrainerFText': 'CeruleanMart_CooltrainerFText:\n\ttext "블루시티의 호수공원에 있는"\n\tline "트레이너들을 이긴 사람은"\n\tcont "이 마을에서 체육관 관장인"\n\tcont "이슬이 정도야!"\n\tdone'}, 'maps/Route10Pokecenter1F.asm': {'Route10Pokecenter1FGentlemanText': 'Route10Pokecenter1FGentlemanText:\n\ttext "동굴 가까이 있는"\n\tline "포켓몬 센터는 참 기쁘지"\n\tdone', 'Route10Pokecenter1FGymGuideText': 'Route10Pokecenter1FGymGuideText:\n\ttext "발전소의 소장이"\n\tline "강한 트레이너를 찾고 있어"\n\tpara "도둑에게 도둑맞은 물건을"\n\tline "찾아와 주길 바라는 것 같아"\n\tdone', 'Route10Pokecenter1FGymGuideText_ReturnedMachinePart': 'Route10Pokecenter1FGymGuideText_ReturnedMachinePart:\n\ttext "그러고보니 로켓단이"\n\tline "성도에서 부활했다고 하더군"\n\tcont "이미 망해버린 것 같지만"\n\tpara "전혀 몰랐었어!"\n\tdone', 'Route10Pokecenter1FCooltrainerFText': 'Route10Pokecenter1FCooltrainerFText:\n\ttext "건물의 지붕이 있는 것이"\n\tline "밖으로 나오는 것처럼 보이지?"\n\tcont "저기가 발전소야!"\n\tdone'}, 'maps/PowerPlant.asm': {'PowerPlantOfficer1AThiefBrokeInText': 'PowerPlantOfficer1AThiefBrokeInText:\n\ttext "발전소에"\n\tline "도둑이 들다니"\n\tcont "전대미문의 사건이다……"\n\tdone', 'PowerPlantOfficer1CeruleanShadyCharacterText': 'PowerPlantOfficer1CeruleanShadyCharacterText:\n\ttext "블루시티로부터"\n\tline "연락이 있었습니다!"\n\tpara "괴상한 남자가 길 한복판에서"\n\tline "어슬렁 거린다는 것이었습니다!"\n\tdone', 'PowerPlantOfficer1CouldIAskForYourCooperationText': 'PowerPlantOfficer1CouldIAskForYourCooperationText:\n\ttext "괜찮다면 너도"\n\tline "협력해주지 않겠니?"\n\tdone', 'PowerPlantOfficer1HaveToBeefUpSecurityText': 'PowerPlantOfficer1HaveToBeefUpSecurityText:\n\ttext "이제부터는 경비를"\n\tline "강화하지 않으면!"\n\tdone', 'PowerPlantGymGuide1SomeoneStoleAPartText': 'PowerPlantGymGuide1SomeoneStoleAPartText:\n\ttext "발전기의 부품이"\n\tline "어떤자에의해 도둑맞았다!"\n\tpara "부품이 없으면 신형의"\n\tline "발전기를 움직이게 할 수 없단다!"\n\tdone', 'PowerPlantGymGuide1GeneratorUpAndRunningText': 'PowerPlantGymGuide1GeneratorUpAndRunningText:\n\ttext "매일 많은 전기를"\n\tline "만들 수 있게 되었단다!"\n\tdone', 'PowerPlantGymGuide2PowerPlantUpAndRunningText': 'PowerPlantGymGuide2PowerPlantUpAndRunningText:\n\ttext "이곳은 이전에 무인"\n\tline "발전소였단다"\n\tpara "그러나 리니어 기차의"\n\tline "전력을 만들기위해"\n\tcont "다시 만들어진 것이다"\n\tdone', 'PowerPlantGymGuide2GeneratorIsRunningAgainText': 'PowerPlantGymGuide2GeneratorIsRunningAgainText:\n\ttext "무사히 발전기가"\n\tline "움직이게끔 되었단다!"\n\tdone', 'PowerPlantOfficer2ManagerHasBeenSadAndFuriousText': 'PowerPlantOfficer2ManagerHasBeenSadAndFuriousText:\n\ttext "이 앞은 발전실"\n\tline "소장님이 계시지만"\n\tcont "기계가 부서져서"\n\tcont "화를 내거나 슬퍼하기도 하고……"\n\tdone', 'PowerPlantOfficer2ManagerHasBeenCheerfulText': 'PowerPlantOfficer2ManagerHasBeenCheerfulText:\n\ttext "기계가 고쳐져서"\n\tline "소장님도 기운이 넘친다!"\n\tdone', 'PowerPlantGymGuide4MagnetTrainConsumesElectricityText': 'PowerPlantGymGuide4MagnetTrainConsumesElectricityText:\n\ttext "리니어 기차는 많은 전기를"\n\tline "사용하는 교통수단이니까"\n\tpara "신형 발전기가 움직이지 않으면"\n\tline "리니어 기차는 멈춘채로 끝이란다"\n\tdone', 'PowerPlantGymGuide4WeCanGetMagnetTrainRunningText': 'PowerPlantGymGuide4WeCanGetMagnetTrainRunningText:\n\ttext "이제 드디어 리니어 기차를"\n\tline "움직이게 할 수 있다!"\n\tdone', 'PowerPlantManagerWhoWouldRuinMyGeneratorText': 'PowerPlantManagerWhoWouldRuinMyGeneratorText:\n\ttext "소장『요 요 용서 못해!"\n\tpara "내가 많은 시간을 투자한"\n\tline "발전기를 고장내다니!"\n\tpara "붙잡히기만 하면"\n\tline "필살의 전자포로"\n\tcont "박살낼꺼야!!"\n\tdone', 'PowerPlantManagerIWontForgiveCulpritText': 'PowerPlantManagerIWontForgiveCulpritText:\n\ttext "소장『나는 용서할 수 없다!"\n\tline "범인이 울면서 싹싹 빌어도말야!"\n\tcont "크흑 크흑 크흐흑……!"\n\tdone', 'PowerPlantManagerThatsThePartText': 'PowerPlantManagerThatsThePartText:\n\ttext "소장『오 오 오 오옷!!"\n\tpara "그것은 나의 귀여운"\n\tline "발전기의 부품이 아닌가!"\n\tcont "자네가 찾아주었는가!"\n\tdone', 'PowerPlantManagerTakeThisTMText': 'PowerPlantManagerTakeThisTMText:\n\ttext "얘야!!"\n\tline "고맙단다!"\n\tcont "고마움의 표시로"\n\tcont "이 기술머신을 주마!"\n\tdone', 'PowerPlantManagerTM07IsZapCannonText': 'PowerPlantManagerTM07IsZapCannonText:\n\ttext "소장『기술머신07은"\n\tline "나의 필살 전자포!"\n\tcont "강력한 기술이란다!"\n\tpara "약간 명중률은 떨어지지만……"\n\tline "위력은 대단하단다!"\n\tdone', 'PowerPlantManagerMyBelovedGeneratorText': 'PowerPlantManagerMyBelovedGeneratorText:\n\ttext "소장『내 발전기!"\n\tline "점점 전기를 만들고 있다!"\n\tdone'}, 'maps/BillsHouse.asm': {'BillsGrandpaIntroText': 'BillsGrandpaIntroText:\n\ttext "응? 너"\n\tline "이수재에대해 알고있느냐?"\n\tcont "이수재는 내 손자란다!"\n\tpara "성도에서 컴퓨터…… 뭔가의"\n\tline "일을 하고있어서"\n\tcont "내가 집을 지키고 있단다!"\n\tdone', 'BillsGrandpaAskToSeeMonText': 'BillsGrandpaAskToSeeMonText:\n\ttext "그 포켓몬을 가지고 있다면"\n\tline "꼭 보여줬으면 좋겠는데……"\n\tdone', 'BillsGrandpaExcitedToSeeText': 'BillsGrandpaExcitedToSeeText:\n\ttext "오오 보여주려구!"\n\tline "고맙구나!"\n\tdone', 'BillsGrandpaYouDontHaveItTextText': 'BillsGrandpaYouDontHaveItTextText:\n\ttext "가지고있지 않느냐?"\n\tline "그거 유감이구나……"\n\tdone', 'BillsGrandpaTokenOfAppreciationText': 'BillsGrandpaTokenOfAppreciationText:\n\ttext "고맙구나!"\n\tpara "답례로 이것을 주마!"\n\tdone', 'BillsGrandpaComeAgainText': 'BillsGrandpaComeAgainText:\n\ttext "또 놀러오너라"\n\tdone', 'BillsGrandpaShownAllThePokemonText': 'BillsGrandpaShownAllThePokemonText:\n\ttext "귀여운 포켓몬을"\n\tline "많이 구경 잘 했다"\n\tcont "고맙구나!"\n\tpara "매우 즐거웠단다!"\n\tline "이야아 역시 오래살고 볼 일이야!"\n\tdone', 'BillsGrandpaWrongPokemonText': 'BillsGrandpaWrongPokemonText:\n\ttext "우-움……"\n\tpara "소문으로 들은 포켓몬은"\n\tline "그렇게 생기지 않은 것 같은데……"\n\tdone', 'BillsGrandpaLickitungText': 'BillsGrandpaLickitungText:\n\ttext "손자 이수재가 말했던"\n\tline "길다란 혀로 낼름! 하고"\n\tcont "핥는 포켓몬이 있다는 것 같은데"\n\tdone', 'BillsGrandpaOddishText': 'BillsGrandpaOddishText:\n\ttext "그래그래 손자에게 들었는데"\n\tline "둥글고 녹색에다가"\n\tcont "머리에 잎사귀가 나있는"\n\tcont "포켓몬이 있다고 하던데"\n\tdone', 'BillsGrandpaStaryuText': 'BillsGrandpaStaryuText:\n\ttext "몸에 빨간 구슬이 있는"\n\tline "바다의 포켓몬이 있지?"\n\tcont "별 모양을 하고있는 녀석"\n\tpara "밤이되면 나타난다고 하던데"\n\tline "내가 꼭 보고싶단다!"\n\tdone', 'BillsGrandpaGrowlitheText': 'BillsGrandpaGrowlitheText:\n\ttext "주인 트레이너에게 충직하고"\n\tline "짖는 특기가 있는 포켓몬이"\n\tcont "있다고 이수재에게 들었단다"\n\tdone', 'BillsGrandpaVulpixText': 'BillsGrandpaVulpixText:\n\ttext "6개의 꼬리를 가진"\n\tline "귀여운 포켓몬이 있다는데"\n\tpara "나도 한번 그 포켓몬을"\n\tline "안아보고 싶구나"\n\tdone', 'BillsGrandpaPichuText': 'BillsGrandpaPichuText:\n\ttext "인기 최고의 포켓몬이"\n\tline "있다는데!"\n\tpara "이렇게! 노란색 몸에"\n\tline "빨간 볼을 한 포켓몬이지"\n\tpara "그것이 진화하기 전의 모습을"\n\tline "한번 보고싶단다!"\n\tdone', 'BillsGrandpaShownPokemonText': 'BillsGrandpaShownPokemonText:\n\ttext "그것이 @"\n\ttext_ram wStringBuffer3\n\ttext "인가!"\n\tline "귀여운 포켓몬이로구나!"\n\tpara "좋은 것 구경 잘 했다"\n\tdone'}}

DYNAMIC_LABEL = "BillsGrandpaShownPokemonText"


def replace_top_level_label_block(text: str, label: str, block: str) -> str:
    pattern = re.compile(rf"(?ms)^{re.escape(label)}:\n.*?(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)")
    m = pattern.search(text)
    if not m:
        raise RuntimeError(f"label not found: {label}")
    return text[:m.start()] + block.rstrip() + "\n\n" + text[m.end():]


def activate_bank54(root: Path, apply: bool) -> list[str]:
    changed=[]
    for rel, label_map in REPLACEMENTS.items():
        p=root/rel
        text=p.read_text(encoding='utf-8')
        new=text
        for label, block in label_map.items():
            new=replace_top_level_label_block(new,label,block)
        if new != text:
            changed.append(rel)
            if apply: p.write_text(new,encoding='utf-8')

    p=root/'data/maps/scripts.asm'
    text=p.read_text(encoding='utf-8')
    new=text
    marker='/*\nSECTION "Map Scripts 19", ROMX'
    if marker in new:
        new=new.replace(marker,'SECTION "Map Scripts 19", ROMX',1)
    marker20='\n\nSECTION "Map Scripts 20", ROMX'
    if marker20 in new and '/*\nSECTION "Map Scripts 20", ROMX' not in new:
        new=new.replace(marker20,'\n\n/*\nSECTION "Map Scripts 20", ROMX',1)
    if new != text:
        changed.append('data/maps/scripts.asm')
        if apply: p.write_text(new,encoding='utf-8')

    p=root/'layout.link'
    text=p.read_text(encoding='utf-8')
    old='; ROMX $54\n; \t"Map Scripts 19"'
    new=text.replace(old,'ROMX $54\n\t"Map Scripts 19"',1)
    if new != text:
        changed.append('layout.link')
        if apply: p.write_text(new,encoding='utf-8')
    return changed


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('repo', type=Path, help='path to a Narishma-gb/pokegold-kr checkout')
    ap.add_argument('--apply', action='store_true', help='write changes (default: dry run)')
    ap.add_argument('--rom', type=Path, help='optional Korean Silver ROM for SHA-1 provenance check')
    ns=ap.parse_args()
    if ns.rom:
        sha=hashlib.sha1(ns.rom.read_bytes()).hexdigest()
        if sha != EXPECTED_ROM_SHA1:
            raise SystemExit(f'ROM SHA-1 mismatch: {sha} != {EXPECTED_ROM_SHA1}')
        print(f'ROM SHA-1 OK: {sha}')
    changed=activate_bank54(ns.repo, ns.apply)
    mode='APPLIED' if ns.apply else 'DRY-RUN'
    print(f'{mode}: {len(changed)} files would change' if not ns.apply else f'{mode}: {len(changed)} files changed')
    for x in changed: print(' -',x)

if __name__=='__main__':
    main()
