# -*- coding: utf-8 -*-
"""교육용 24차원 임베딩 사전 — 사람이 뜻을 정한 작은 사전 (설명용)

실제 임베딩 모델(384~1,536차원)은 수십억 문장에서 이런 관계를 스스로 배운다.
이 사전은 '숫자 좌표가 뜻을 담는다'를 눈으로 보이게 하려고 사람이 직접 적은 것이다.
차원마다 이름이 있다는 점이 실제 모델과 가장 큰 차이다(실제 모델의 차원은 이름이 없다).
사용: python3 code/lexicon.py → data/lexicon.json
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIMS = ['좋고 나쁨', '재미', '감동', '공포·긴장', '웃음', '스토리', '연기', '영상·액션', '음악', '시간·길이', '돈값', '영화 일반',
        '음식', '날씨', '일·출퇴근', '홍보·이벤트', '요금·결제', '환불·해지', '계정·공유', '화질·재생', '자막·언어', '오류·장애', '다운로드', '고객센터']
C = {k: i for i, k in enumerate(['good', 'fun', 'moving', 'fear', 'laugh', 'story', 'acting', 'visual', 'music', 'length', 'value', 'movie',
                                 'food', 'weather', 'work', 'promo', 'pay', 'refund', 'account', 'quality', 'subtitle', 'error', 'download', 'support'])}

L = {}


def w(keys, **kv):
    for k in keys.split('|'):
        L[k] = {C[a]: b for a, b in kv.items()}


# ── 리뷰: 재미
w('재밌|재미있', fun=1, good=.7); w('재미없', fun=1, good=-.8); w('꿀잼|존잼', fun=1, good=.9); w('개꿀잼', fun=1, good=1)
w('노잼', fun=1, good=-.9); w('핵노잼', fun=1, good=-1); w('지루', fun=.9, good=-.7); w('하품', fun=.7, good=-.6); w('졸았|잤음', fun=.6, good=-.6)
w('몰입', fun=.9, good=.6); w('시간 가는 줄 몰랐', fun=1, good=.8); w('지루할 틈이 없', fun=1, good=.8); w('눈을 못 뗐', fun=.9, good=.8); w('보다가 껐', fun=.7, good=-.8)
# 감동
w('감동', moving=1, good=.5); w('눈물', moving=.9, good=.3); w('울면서', moving=.9, good=.4); w('오열', moving=1, good=.5); w('여운', moving=.8, good=.6)
w('따뜻', moving=.7, good=.6); w('먹먹', moving=.8, good=.3); w('신파', moving=.8, good=-.6); w('강요', moving=.2, good=-.6); w('억지', good=-.6); w('울리려고', moving=.7, good=-.2)
# 공포
w('무서|무섭', fear=1, good=.4); w('소름', fear=.7, good=.5); w('쫄깃', fear=.8, good=.5); w('긴장감', fear=.9, good=.4); w('긴장감이 없', fear=.8, good=-.6)
w('식은땀', fear=.8, good=.3); w('혼자 못 보겠', fear=1, good=.5); w('놀래키기만', fear=.6, good=-.6); w('공포', fear=.8, movie=.3)
# 웃음
w('터졌', laugh=1, good=.6); w('웃겨|웃김', laugh=1, good=.6); w('웃었', laugh=.9, good=.6); w('개웃김', laugh=1, good=.9); w('배꼽', laugh=.8, good=.6)
w('코미디', laugh=.8, movie=.3, good=.2); w('ㅋㅋ', laugh=.3, good=.2); w('썰렁', laugh=.8, good=-.7); w('개그|유머', laugh=.7); w('코드가 안 맞', good=-.6); w('애쓰는데', good=-.3)
# 스토리
w('스토리', story=1); w('반전', story=.9, good=.6); w('각본', story=1); w('훌륭', good=.8); w('떡밥', story=.9); w('회수', story=.3, good=.4); w('완벽', good=.8)
w('전개', story=.9); w('깔끔', good=.6); w('탄탄', story=.5, good=.8); w('엉성', story=.3, good=-.8); w('개연성', story=1); w('개연성이 없', story=1, good=-.9)
w('산으로', story=.4, good=-.7); w('결말', story=.8); w('허무', good=-.7); w('뻔한', story=.5, good=-.7); w('내용', story=.5)
# 연기
w('연기|연기력', acting=1); w('배우', acting=.9); w('발연기', acting=1, good=-.9); w('어색', good=-.7); w('국어책', acting=.7, good=-.8); w('캐릭터', acting=.6, story=.3)
w('살아있', good=.7); w('차력쇼', acting=.5, good=.8); w('인정', good=.6)
# 영상·액션
w('영상미', visual=1, good=.5); w('영상', visual=.9); w('화면', visual=.8, quality=.3); w('아름답', visual=.3, good=.7); w('액션', visual=1); w('시원', good=.6)
w('CG', visual=1); w('퀄리티', visual=.3, good=.4); w('때깔', visual=.9, good=.5); w('추격', visual=.8); w('압권', good=.9); w('조잡', good=-.8); w('정신없', good=-.6)
w('답답', good=-.6); w('어둡', visual=.3, good=-.3); w('예술', visual=.3, good=.8)
# 음악
w('OST|음악|배경음악', music=1); w('노래', music=.9); w('귀에 맴', music=.7, good=.5); w('시끄럽', music=.5, good=-.7); w('튄다', good=-.4); w('살린다', good=.6)
# 시간·길이
w('러닝타임', length=1, movie=.3); w('길다', length=.9, good=-.5); w('3시간', length=.8); w('늘어진', length=.8, good=-.7); w('질질', length=.9, good=-.8)
w('짧게 느껴', length=.8, good=.8); w('두 시간', length=.5); w('시간', length=.4)
# 돈값
w('돈', value=.7); w('아깝|아까운', value=1, good=-.8); w('날렸', value=1, good=-.9); w('환불하고 싶', value=.8, refund=.3, good=-.8); w('버렸', value=.8, good=-.8)
w('돈값', value=1, good=.8); w('티켓값', value=1, movie=.3, good=.6); w('N차', movie=.6, good=.8)
# 평가 일반
w('좋', good=.6); w('최고', good=.9); w('대박', good=.7); w('미쳤', good=.7); w('최악', good=-.9); w('별로', good=-.5); w('아쉽', good=-.6); w('추천', good=.6)
w('강추', good=.9); w('비추', good=-.9); w('다시 볼', good=.6); w('볼 만', good=.4); w('그냥 그랬', good=-.3); w('실망', good=-.8); w('대단', good=.7)
w('예쁘', good=.6); w('싫', good=-.7); w('지옥', good=-.8); w('떨린', good=-.2); w('칭찬', good=.6, work=.3); w('정말 훌륭', good=.9)
# 영화 일반
w('영화', movie=1); w('봤|보고 왔', movie=.6); w('관람', movie=.6); w('극장', movie=.8); w('티켓', movie=.5, value=.4); w('개봉', movie=.8); w('감독', movie=.7, story=.2)
for t in ['별빛정거장', '마지막퇴근', '붉은계단', '한강추격전', '봄날의편지', '주판왕의비밀', '바다로간초파리', '검은서버실']:
    w('#' + t, movie=1)
# ── SNS 일상
w('마라탕|김치찌개|치킨|떡볶이|라떼', food=1); w('맛집', food=1, good=.4); w('맛있', food=.8, good=.7); w('존맛', food=1, good=.9); w('카페', food=.7)
w('배고', food=.8); w('점심|저녁', food=.8); w('저녁 메뉴', food=1); w('신메뉴', food=.7)
w('비 와', weather=1, good=-.2); w('하늘', weather=.9); w('미세먼지', weather=1, good=-.5); w('추워', weather=.9); w('패딩', weather=.7); w('눈 온', weather=1)
w('첫눈', weather=1, good=.4); w('햇살', weather=.9, good=.4); w('날씨', weather=1); w('산책', weather=.5, good=.3); w('마스크', weather=.5)
w('출근', work=1); w('퇴근', work=.8); w('야근', work=1, good=-.5); w('회의', work=.9); w('발표', work=.8); w('팀장', work=.9); w('회사', work=.8); w('월요일', work=.6, good=-.2)
w('무료|공짜', promo=1, pay=.2); w('증정', promo=1); w('이벤트', promo=1); w('링크', promo=.8); w('클릭', promo=.8); w('쿠폰|기프티콘', promo=.9, food=.2)
w('커피', food=.7); w('DM', promo=.7); w('꿀팁', promo=.5, good=.3); w('시청', movie=.5, quality=.3); w('드려요|드림|받아가|받기|받는', promo=.6); w('팔로우', promo=.8); w('추첨', promo=.8); w('부업', promo=.9, work=.3); w('10만원', promo=.6, pay=.2); w('관람권|영화표', promo=.6, movie=.6)
# ── 랩플릭스 안내 문서
w('요금제', pay=1); w('요금', pay=.9); w('베이직|스탠다드', pay=.6); w('프리미엄', pay=.6, quality=.3); w('얼마', pay=.8); w('가격', pay=.7, value=.3); w('할인', pay=.9)
w('학생|대학생|대학원생', pay=.4, account=.3); w('인증', account=.6); w('이메일', account=.5); w('동시', account=.6); w('대에서', account=.4); w('두 명', account=.5)
w('화질', quality=1); w('HD|FHD', quality=.8); w('4K', quality=1); w('결제', pay=1); w('카드', pay=.8); w('한도', pay=.7); w('만료', pay=.4, error=.4)
w('환불', refund=1); w('돌려받', refund=1); w('일할', refund=.6, pay=.3); w('해지', refund=.9); w('구독', pay=.6, refund=.2); w('결제일', pay=.7)
w('계정', account=1); w('공유', account=.9); w('같이 써', account=.9); w('가족', account=.6); w('접속', account=.5, error=.2); w('추가 회원', account=.8, pay=.5)
w('프로필', account=.7); w('다운|내려받', download=1); w('저장', download=.5); w('휴대폰|태블릿', download=.3, quality=.3); w('48시간', download=.4); w('30일', download=.3)
w('며칠', download=.2, length=.3); w('자막', subtitle=1); w('언어', subtitle=.8); w('베트남어|영어|일본어|중국어|한국어', subtitle=.8); w('해설', subtitle=.5)
w('오류|에러', error=1); w('실패', error=.8, pay=.2); w('LP-', error=1); w('점검', error=.8); w('서버', error=.7); w('접속자', error=.5)
w('인터넷|속도', quality=.8); w('메가비트', quality=.9); w('빨라', quality=.4); w('데이터', quality=.5); w('느리', quality=.5, good=-.3); w('재생', quality=.6)
w('고객센터|상담', support=1); w('채팅', support=.8); w('전화', support=.7); w('문의', support=.8); w('공휴일', support=.5); w('평일', support=.4); w('운영', support=.3); w('신청', refund=.3, support=.3)

NEG_PRE = ['하나도 안 ', '안 ', '못 ']          # 다음 낱말의 '좋고 나쁨'을 뒤집는다
NEG_POST = ['지 않', '지 못']                  # 앞 낱말의 '좋고 나쁨'을 뒤집는다


def main():
    out = {'dims': DIMS, 'lex': {k: [[i, v] for i, v in sorted(d.items())] for k, d in L.items()}, 'negPre': NEG_PRE, 'negPost': NEG_POST,
           'note': '사람이 뜻을 정한 교육용 24차원 임베딩 사전. 실제 임베딩 모델은 데이터에서 스스로 배우며 차원에 이름이 없다.'}
    json.dump(out, open(os.path.join(ROOT, 'data', 'lexicon.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('낱말', len(L), '차원', len(DIMS))


if __name__ == '__main__':
    main()
