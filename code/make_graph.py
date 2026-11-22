# -*- coding: utf-8 -*-
"""7장용 가상 지식 그래프와 온톨로지 — 랩플릭스 안내 문서·영화 데이터에서 사람이 뽑은 사실(삼항)
모든 사실은 data/corpus.json의 랩플릭스 안내 문서와 영화 정보에 실제로 적힌 내용만 옮겼다(출처 문서 번호 doc).
사용: python3 code/make_graph.py → data/graph.json
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(ROOT, 'data', 'corpus.json'), encoding='utf-8'))

# 노드: id, 이름, 온톨로지 클래스, 다른 이름(동의어)
N = [
    ('basic', '베이직', '요금제', []), ('standard', '스탠다드', '요금제', []), ('premium', '프리미엄', '요금제', []),
    ('p9900', '월 9,900원', '가격', []), ('p13500', '월 13,500원', '가격', []), ('p17000', '월 17,000원', '가격', []), ('p4000', '월 4,000원', '가격', []),
    ('hd', 'HD', '화질', []), ('fhd', 'FHD', '화질', []), ('uhd', '4K', '화질', ['초고화질']),
    ('d1', '한 대', '동시 시청 수', []), ('d2', '두 대', '동시 시청 수', []), ('d4', '네 대', '동시 시청 수', []),
    ('dl', '다운로드', '기능', ['내려받기', '다운']), ('dl30', '30일 보관', '조건', []), ('dl48', '재생 후 48시간', '조건', []),
    ('student', '학생 할인', '할인', ['대학생 할인']), ('s30', '30% 할인', '조건', []), ('mail', '학교 이메일 인증', '조건', []),
    ('mbps5', '초당 5메가비트', '조건', []), ('mbps25', '초당 25메가비트', '조건', []),
    ('lp204', 'LP-204', '오류 코드', []), ('lp503', 'LP-503', '오류 코드', []), ('cardexp', '결제 수단 만료·한도 부족', '원인', []),
    ('maint', '서버 점검·접속 폭주', '원인', []), ('tue', '매주 화요일 새벽 2~4시', '일정', []),
    ('paymenu', '결제 수단 메뉴', '앱 메뉴', []), ('histmenu', '결제 내역 메뉴', '앱 메뉴', []), ('acctmenu', '내 계정 메뉴', '앱 메뉴', []),
    ('chat', '채팅 상담', '상담 창구', []), ('phone', '전화 상담', '상담 창구', []), ('weekend', '주말·공휴일', '일정', ['주말']), ('weekday', '평일 9시~18시', '일정', []),
    ('payissue', '결제 문제', '문의 유형', ['결제 오류']),
    ('refund2', '환불 규정 (현행)', '규정', ['환불']), ('refund1', '환불 규정 (구버전)', '규정', []), ('r3', '결제 후 3일 이내·미재생 전액', '조건', []), ('r7', '결제 후 7일 이내·미재생 전액', '조건', []),
    ('cancel', '구독 해지', '절차', ['해지']), ('keepwatch', '낸 기간 끝까지 시청', '조건', []),
    ('share', '계정 공유', '정책', ['같이 쓰기']), ('family', '같은 집 가족', '조건', []), ('extra', '추가 회원', '요금 항목', []),
    ('sub', '자막', '기능', []), ('vi', '베트남어 자막', '자막 언어', []),
]
# 사실: (주어, 관계, 목적어, 출처 문서)
E = [
    ('basic', '가격', 'p9900', 'plan'), ('standard', '가격', 'p13500', 'plan'), ('premium', '가격', 'p17000', 'plan'),
    ('basic', '지원 화질', 'hd', 'plan'), ('standard', '지원 화질', 'fhd', 'plan'), ('premium', '지원 화질', 'uhd', 'plan'),
    ('basic', '동시 시청', 'd1', 'plan'), ('standard', '동시 시청', 'd2', 'plan'), ('premium', '동시 시청', 'd4', 'plan'),
    ('standard', '가능 기능', 'dl', 'download'), ('premium', '가능 기능', 'dl', 'download'), ('dl', '조건', 'dl30', 'download'), ('dl', '조건', 'dl48', 'download'),
    ('student', '적용 요금제', 'standard', 'student'), ('student', '할인율', 's30', 'student'), ('student', '조건', 'mail', 'student'),
    ('hd', '필요 속도', 'mbps5', 'quality'), ('uhd', '필요 속도', 'mbps25', 'quality'),
    ('lp204', '원인', 'cardexp', 'err204'), ('lp204', '해결 메뉴', 'paymenu', 'err204'), ('lp204', '문의 유형', 'payissue', 'err204'),
    ('lp503', '원인', 'maint', 'err503'), ('maint', '일정', 'tue', 'err503'),
    ('payissue', '가장 빠른 창구', 'chat', 'support'), ('chat', '운영', 'weekend', 'support'), ('chat', '운영', 'weekday', 'support'), ('phone', '운영', 'weekday', 'support'),
    ('refund2', '조건', 'r3', 'refund_v2'), ('refund2', '신청 메뉴', 'histmenu', 'refund_v2'), ('refund2', '대체함', 'refund1', 'refund_v2'), ('refund1', '조건', 'r7', 'refund_v1'),
    ('cancel', '신청 메뉴', 'acctmenu', 'cancel'), ('cancel', '조건', 'keepwatch', 'cancel'),
    ('share', '조건', 'family', 'share'), ('share', '다른 집이면', 'extra', 'share'), ('extra', '가격', 'p4000', 'share'),
    ('sub', '지원 언어', 'vi', 'subtitle'),
]
# 여러 걸음 질문: 질문, 필요한 문서들, 답, 답에 이르는 길
MQ = [
    {'q': '4K로 보면서 다운로드도 되는 요금제는 한 달에 얼마야?', 'docs': ['plan', 'download'], 'ans': '프리미엄, 월 17,000원', 'path': ['uhd', 'premium', 'dl', 'p17000']},
    {'q': '학생 할인이 되는 요금제로는 동시에 몇 대까지 볼 수 있어?', 'docs': ['student', 'plan'], 'ans': '스탠다드라서 두 대', 'path': ['student', 'standard', 'd2']},
    {'q': 'LP-204 오류가 주말에 뜨면 어디에 물어봐야 빨라?', 'docs': ['err204', 'support'], 'ans': '결제 문제라 채팅 상담 (주말에도 운영)', 'path': ['lp204', 'payissue', 'chat', 'weekend']},
    {'q': '프리미엄 화질로 보려면 인터넷이 얼마나 빨라야 해?', 'docs': ['plan', 'quality'], 'ans': '프리미엄은 4K라 초당 25메가비트 이상', 'path': ['premium', 'uhd', 'mbps25']},
    {'q': '다운로드 되는 요금제 중 가장 싼 건 얼마야?', 'docs': ['download', 'plan'], 'ans': '스탠다드 월 13,500원', 'path': ['dl', 'standard', 'p13500']},
    {'q': '친구가 다른 집에서 내 계정으로 보면 한 달에 얼마가 더 붙어?', 'docs': ['share'], 'ans': '추가 회원 요금 월 4,000원', 'path': ['share', 'extra', 'p4000']},
]
# 온톨로지: 클래스 (이름, 부모)
ONT = [
    ('개념', None), ('서비스 요소', '개념'), ('요금제', '서비스 요소'), ('화질', '서비스 요소'), ('기능', '서비스 요소'), ('오류 코드', '서비스 요소'), ('앱 메뉴', '서비스 요소'), ('상담 창구', '서비스 요소'),
    ('조건과 값', '개념'), ('가격', '조건과 값'), ('동시 시청 수', '조건과 값'), ('조건', '조건과 값'), ('일정', '조건과 값'), ('원인', '조건과 값'), ('할인', '조건과 값'), ('요금 항목', '조건과 값'),
    ('문서와 규칙', '개념'), ('규정', '문서와 규칙'), ('정책', '문서와 규칙'), ('절차', '문서와 규칙'), ('문의 유형', '문서와 규칙'), ('자막 언어', '기능'),
    ('콘텐츠', '개념'), ('영화', '콘텐츠'), ('장르', '콘텐츠'), ('긴장감 장르', '장르'), ('가족 장르', '장르'), ('감성 장르', '장르'),
    ('SF', '감성 장르'), ('로맨스', '감성 장르'), ('공포', '긴장감 장르'), ('스릴러', '긴장감 장르'), ('미스터리', '긴장감 장르'), ('액션', '긴장감 장르'),
    ('코미디', '가족 장르'), ('애니메이션', '가족 장르'),
    ('평가 관점', '개념'),
]
ASPECT_ALT = {'fun': ['재밌', '재미있', '꿀잼', '존잼', '몰입', '시간 가는 줄'], 'moving': ['감동', '눈물', '울면서', '오열', '여운'], 'fear': ['무서', '무섭', '소름', '쫄깃', '긴장감'],
              'acting': ['연기', '배우', '캐릭터'], 'music': ['음악', 'OST', '노래'], 'story': ['스토리', '반전', '각본', '떡밥', '전개'], 'laugh': ['웃겨', '웃김', '터졌', '배꼽', '코미디'],
              'visual': ['영상미', '액션', 'CG', '화면', '때깔']}
# 데이터 품질 규칙 (온톨로지가 정한 약속)
RULES = [
    {'id': 'one_current', 'ko': '같은 규정의 현행 판은 하나뿐이어야 한다'},
    {'id': 'old_has_end', 'ko': '"대체함" 관계로 밀려난 판은 적용 종료일이 있어야 한다'},
    {'id': 'plan_price', 'ko': '모든 요금제는 가격이 정확히 하나여야 한다'},
]


def main():
    ids = {n[0] for n in N}
    for s, p, o, d in E:
        assert s in ids and o in ids, (s, o)
    kbids = {k['id'] for k in C['kb']}
    for s, p, o, d in E:
        assert d in kbids, d
    out = {'note': '랩플릭스 가상 안내 문서에서 사람이 뽑은 사실(삼항)과 설명용 온톨로지', 'nodes': [{'id': a, 'label': b, 'cls': c, 'alt': d} for a, b, c, d in N],
           'edges': [{'s': s, 'p': p, 'o': o, 'doc': d} for s, p, o, d in E], 'mq': MQ, 'ont': [{'c': a, 'parent': b} for a, b in ONT], 'aspect_alt': ASPECT_ALT, 'rules': RULES}
    json.dump(out, open(os.path.join(ROOT, 'data', 'graph.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('노드', len(N), '사실', len(E), '여러 걸음 질문', len(MQ), '클래스', len(ONT))


if __name__ == '__main__':
    main()
