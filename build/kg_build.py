# -*- coding: utf-8 -*-
"""페이지마다 kg.json · refs.json · meta.json을 만들고 retrofit.py로 #kg·#export를 붙인 뒤 check.py로 점검한다."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from lib import R, SERIES, SITE

DATE = '2026-11-22'
BB = os.path.join(HERE, 'backbone_ai.json')
V = lambda **k: dict({'title': True, 'author': True, 'year': True, 'container': True, 'pages': False, 'doi': False}, **k)
REFS = {
    'ahn2026vdb': {'type': 'dataset', 'title': '벡터 DB 연구실 가상 데이터 (영화 리뷰·SNS 글·랩플릭스 안내 문서·교육용 임베딩)', 'author': [{'family': '안', 'given': '상선'}], 'publisher': '(주)M-Robo',
                   'URL': 'https://github.com/adminmrobo/vector_db_lab', 'year': 2026, 'role': 'data', 'verified': V(), 'checkedBy': '이 저장소 code/make_data.py · code/lexicon.py', 'checkedSource': 'repo'},
    'ahn2026dbd': {'type': 'webpage', 'title': '데이터베이스 설계 (강좌 사이트)', 'author': [{'family': '안', 'given': '상선'}], 'publisher': '(주)M-Robo', 'URL': 'https://adminmrobo.github.io/data_base_design/',
                   'year': 2026, 'role': 'background', 'verified': V(), 'checkedBy': '사이트 확인 (2026-11-22)', 'checkedSource': 'web'},
    'ahn2026nlp': {'type': 'webpage', 'title': '인공지능과 자연어 데이터 분석 (강좌 사이트)', 'author': [{'family': '안', 'given': '상선'}], 'publisher': '(주)M-Robo', 'URL': 'https://adminmrobo.github.io/ai-nlp-data-analysis/',
                   'year': 2026, 'role': 'background', 'verified': V(), 'checkedBy': '사이트 확인 (2026-11-22)', 'checkedSource': 'web'},
    'manning2008ir': {'type': 'book', 'title': 'Introduction to Information Retrieval', 'author': [{'family': 'Manning', 'given': 'Christopher D.'}, {'family': 'Raghavan', 'given': 'Prabhakar'}, {'family': 'Schütze', 'given': 'Hinrich'}],
                      'publisher': 'Cambridge University Press', 'year': 2008, 'role': 'method', 'verified': V()},
    'mikolov2013efficient': {'type': 'article', 'title': 'Efficient Estimation of Word Representations in Vector Space', 'author': [{'family': 'Mikolov', 'given': 'Tomas'}, {'family': 'Chen', 'given': 'Kai'}, {'family': 'Corrado', 'given': 'Greg'}, {'family': 'Dean', 'given': 'Jeffrey'}],
                             'container-title': 'arXiv:1301.3781', 'year': 2013, 'role': 'method', 'verified': V()},
    'reimers2019sbert': {'type': 'paper-conference', 'title': 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks', 'author': [{'family': 'Reimers', 'given': 'Nils'}, {'family': 'Gurevych', 'given': 'Iryna'}],
                         'container-title': 'EMNLP-IJCNLP 2019', 'year': 2019, 'role': 'method', 'verified': V()},
    'jegou2011pq': {'type': 'article-journal', 'title': 'Product Quantization for Nearest Neighbor Search', 'author': [{'family': 'Jégou', 'given': 'Hervé'}, {'family': 'Douze', 'given': 'Matthijs'}, {'family': 'Schmid', 'given': 'Cordelia'}],
                    'container-title': 'IEEE Transactions on Pattern Analysis and Machine Intelligence', 'volume': '33', 'issue': '1', 'year': 2011, 'role': 'method', 'verified': V()},
    'malkov2020hnsw': {'type': 'article-journal', 'title': 'Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs', 'author': [{'family': 'Malkov', 'given': 'Yu. A.'}, {'family': 'Yashunin', 'given': 'D. A.'}],
                       'container-title': 'IEEE Transactions on Pattern Analysis and Machine Intelligence', 'volume': '42', 'issue': '4', 'year': 2020, 'role': 'method', 'verified': V()},
    'johnson2021faiss': {'type': 'article-journal', 'title': 'Billion-scale Similarity Search with GPUs', 'author': [{'family': 'Johnson', 'given': 'Jeff'}, {'family': 'Douze', 'given': 'Matthijs'}, {'family': 'Jégou', 'given': 'Hervé'}],
                         'container-title': 'IEEE Transactions on Big Data', 'volume': '7', 'issue': '3', 'year': 2021, 'role': 'method', 'verified': V()},
    'lewis2020rag': {'type': 'paper-conference', 'title': 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks', 'author': [{'family': 'Lewis', 'given': 'Patrick'}, {'family': 'Perez', 'given': 'Ethan'}, {'family': 'Piktus', 'given': 'Aleksandra'}],
                     'container-title': 'NeurIPS 2020', 'year': 2020, 'role': 'method', 'verified': V()},
    'robertson2009bm25': {'type': 'article-journal', 'title': 'The Probabilistic Relevance Framework: BM25 and Beyond', 'author': [{'family': 'Robertson', 'given': 'Stephen'}, {'family': 'Zaragoza', 'given': 'Hugo'}],
                          'container-title': 'Foundations and Trends in Information Retrieval', 'volume': '3', 'issue': '4', 'year': 2009, 'role': 'method', 'verified': V()},
    'radford2021clip': {'type': 'paper-conference', 'title': 'Learning Transferable Visual Models From Natural Language Supervision', 'author': [{'family': 'Radford', 'given': 'Alec'}, {'family': 'Kim', 'given': 'Jong Wook'}],
                        'container-title': 'ICML 2021', 'year': 2021, 'role': 'background', 'verified': V()},
    'morris2023inversion': {'type': 'paper-conference', 'title': 'Text Embeddings Reveal (Almost) As Much As Text', 'author': [{'family': 'Morris', 'given': 'John X.'}, {'family': 'Kuleshov', 'given': 'Volodymyr'}, {'family': 'Shmatikov', 'given': 'Vitaly'}, {'family': 'Rush', 'given': 'Alexander M.'}],
                            'container-title': 'EMNLP 2023', 'year': 2023, 'role': 'background', 'verified': V()},
    'spotify_annoy': {'type': 'software', 'title': 'Annoy: Approximate Nearest Neighbors Oh Yeah', 'author': [{'family': 'Spotify', 'given': ''}], 'publisher': 'GitHub', 'URL': 'https://github.com/spotify/annoy',
                      'role': 'background', 'verified': V(year=False), 'checkedBy': 'README Background 절 (2026-11-22 확인)', 'checkedSource': 'web'},
    'pgvector': {'type': 'software', 'title': 'pgvector: Open-source vector similarity search for Postgres', 'author': [{'family': 'Kane', 'given': 'Andrew'}], 'publisher': 'GitHub', 'URL': 'https://github.com/pgvector/pgvector',
                 'role': 'background', 'verified': V(year=False, author=False)},
}


def ref(rid):
    r = dict(REFS[rid]); y = r.pop('year', None); role = r.pop('role', 'background')
    ver = r.pop('verified'); cb = r.pop('checkedBy', '페이지 참고문헌 목록에서 옮김 (외부 대조 안 함)'); cs = r.pop('checkedSource', 'page')
    o = {'id': rid}; o.update(r)
    if y: o['issued'] = {'date-parts': [[y]]}
    o['lab'] = {'work': 'lab:work/' + rid, 'role': role, 'supports': [], 'locs': [], 'verified': ver, 'checkedBy': cb, 'checkedSource': cs}
    return o


T = 'lab:topic/'
QMAP = {}


def build_page(slug, number, title, about, refs, nodes, edges, quiz=None, qanchor=None):
    N, E = [], []
    for t in nodes:
        nid, typ, ko, en, anchor, lvl, dfn = t[:7]
        n = {'id': nid, 'type': typ, 'label': {'ko': ko, 'en': en}, 'page': slug, 'anchor': anchor, 'level': lvl, 'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': [], 'domain': ['ai']}
        if dfn: n['definition'] = {'ko': dfn}
        if len(t) > 7 and t[7]: n['source'] = [{'ref': t[7], 'loc': ''}]
        N.append(n)
    for rid in refs:
        a = REFS[rid]
        N.append({'id': 'lab:work/' + rid, 'type': 'Work', 'label': {'ko': '%s (%s) %s' % (a['author'][0]['family'] + (' 외' if len(a['author']) > 1 else ''), a.get('year') or 'n.d.', a.get('container-title') or a.get('publisher', '')), 'en': a['title']},
                  'page': slug, 'anchor': '#export', 'level': 2, 'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': []})
    for s, p, o, anchor in edges:
        E.append({'s': s, 'p': 'lab:' + p, 'o': o, 'anchor': anchor, 'confidence': 'high'})
    cited = set()
    for n in N:
        for sr in n.get('source', []):
            E.append({'s': n['id'], 'p': 'lab:assertedIn', 'o': 'lab:work/' + sr['ref'], 'anchor': n['anchor'], 'confidence': 'high'}); cited.add(sr['ref'])
    for rid in refs:
        if rid not in cited:
            E.append({'s': about[0], 'p': 'lab:explainedIn', 'o': 'lab:work/' + rid, 'anchor': '#export', 'confidence': 'high'})
    if quiz:
        for qid, items in quiz.items():
            sec = qanchor(qid)
            for k, q in enumerate(items):
                nid = 'lab:quiz/vdb-%s-%s-%d' % (number, qid, k + 1)
                N.append({'id': nid, 'type': 'QuizItem', 'label': {'ko': q['q'][:60], 'en': 'Quiz %s %s-%d' % (number, qid, k + 1)}, 'page': slug, 'anchor': sec, 'level': 2,
                          'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': []})
                E.append({'s': nid, 'p': 'lab:assesses', 'o': QMAP[qid], 'anchor': sec, 'confidence': 'high'})
    kg = {'version': '1.0', 'page': slug, 'nodes': N, 'edges': E}
    meta = {'title': title, 'number': number, 'series': SERIES, 'about': about, 'basedOn': refs, 'educationalLevel': '입문',
            'creator': [{'name': '안상선', 'role': 'author'}], 'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}], 'date': DATE, 'version': '1.0',
            'language': ['ko'], 'license': '', 'url': SITE + slug + '.html', 'registry': 'KG_00_registry 0.2', 'learningResourceType': 'interactive explainer', 'seeAlso': '', 'domain': ['ai'],
            'suggestedCitation': '안상선 (2026). %s. %s %s, v1.0.' % (title, SERIES, number)}
    return kg, [ref(r) for r in refs], meta


def pages():
    P = {}
    sm = R['search_mean']
    P['index'] = ('index', '0', '벡터 DB 연구실 — 목차', ['lab:concept/vector-database'], ['ahn2026vdb', 'ahn2026dbd', 'ahn2026nlp'], [
        ('lab:concept/vector-database', 'Concept', '벡터 데이터베이스', 'Vector database', '#first', 1, '뜻을 담은 좌표와 메타데이터를 저장하고 가까운 좌표를 빨리 찾는 데이터베이스'),
        ('lab:concept/relational-database', 'Concept', '관계형 데이터베이스', 'Relational database', '#first', 1, '행과 열의 표와 SQL'),
        ('lab:concept/embedding', 'Concept', '임베딩', 'Embedding', '#picture', 1, '뜻을 숫자 좌표로 바꾼 것'),
        ('lab:method/rag', 'Method', '검색 증강 생성 (RAG)', 'Retrieval-augmented generation', '#picture', 1, '찾은 근거를 붙여 LLM이 답하게 함'),
        ('lab:dataset/vdb-virtual', 'Dataset', '가상 영화 리뷰·SNS 글·랩플릭스 문서', 'Virtual reviews, SNS posts and help docs', '#data', 1, '이 연구실이 만든 설명용 데이터', 'ahn2026vdb'),
        ('lab:claim/vdb-duel-record', 'Claim', '대결 전적 3승 2패 — 단순한 방법도 큰 방법도 늘 이기지 않는다', 'Duel record 3-2', '#record', 2, ''),
        ('lab:question/where-meaning', 'Question', '리뷰와 SNS 글의 뜻은 어디에 어떻게 저장해야 찾을 수 있을까?', 'Where to store meaning?', '#first', 1, '')], [
        ('lab:concept/vector-database', 'broader', T + 'embedding-space', '#first'), ('lab:concept/relational-database', 'broader', T + 'deployment', '#first'),
        ('lab:concept/embedding', 'broader', T + 'word-embedding', '#picture'), ('lab:method/rag', 'broader', T + 'rag', '#picture'),
        ('lab:concept/vector-database', 'contrastsWith', 'lab:concept/relational-database', '#first'), ('lab:concept/embedding', 'prerequisiteOf', 'lab:concept/vector-database', '#picture'),
        ('lab:method/rag', 'derivedFrom', 'lab:concept/vector-database', '#picture'), ('lab:concept/vector-database', 'evaluatedOn', 'lab:dataset/vdb-virtual', '#data'),
        ('lab:claim/vdb-duel-record', 'supports', 'lab:concept/vector-database', '#record'), ('lab:question/where-meaning', 'addressedBy', 'lab:concept/vector-database', '#first')], None)

    import p01
    QMAP.update({'q11': 'lab:concept/relational-database', 'q12': 'lab:metric/precision-recall', 'q13': 'lab:limitation/rule-taxonomy', 'q14': 'lab:concept/nl-characteristics'})
    P['01'] = ('01_why_not_table', '1', '1장 · 표에 담기지 않는 말 — 관계형 DB의 한계와 자연어 데이터의 특징', ['lab:concept/relational-database', 'lab:concept/nl-characteristics'],
               ['ahn2026vdb', 'ahn2026dbd', 'ahn2026nlp', 'manning2008ir'], [
        ('lab:concept/relational-database', 'Concept', '관계형 데이터베이스', 'Relational database', '#s1', 1, '행과 열의 표, 키로 잇고 SQL로 묻는다', 'ahn2026dbd'),
        ('lab:concept/structured-data', 'Concept', '정형 데이터', 'Structured data', '#s1', 1, '정해진 항목에 담기는 데이터'),
        ('lab:concept/unstructured-data', 'Concept', '비정형 데이터', 'Unstructured data', '#s4', 1, '정해진 항목이 없는 데이터 — 문장·사진·소리'),
        ('lab:method/sql-like', 'Method', 'SQL LIKE 검색', 'SQL LIKE search', '#s2', 2, '글자 일부가 들어 있는지 찾는 조건'),
        ('lab:metric/precision-recall', 'Metric', '정밀도·재현율·F1', 'Precision, recall, F1', '#s2', 2, '헛걸음과 빠뜨림을 함께 보는 채점', 'manning2008ir'),
        ('lab:claim/like-low-recall', 'Claim', "LIKE '%%재밌%%'의 재현율 %.1f%% (정답 %d개 중 %d개)" % (R['search'][0]['like']['r'] * 100, R['search'][0]['rel'], R['search'][0]['like']['tp']), 'LIKE has low recall', '#s2', 2, '', 'ahn2026vdb'),
        ('lab:method/synonym-dictionary', 'Method', '사람이 만든 동의어 사전·태그 규칙', 'Hand-made synonym dictionary and tag rules', '#s3', 2, '말투를 사람이 목록으로 관리'),
        ('lab:limitation/rule-taxonomy', 'Limitation', '사람이 만든 체계는 새 말·새 주제에 늙는다', 'Hand-made taxonomies age', '#s3', 2, ''),
        ('lab:concept/nl-characteristics', 'Concept', '자연어 데이터의 아홉 가지 특징', 'Nine characteristics of natural language data', '#s4', 1, '비정형·맥락·변화·단위 없음·어순·사전에 없는 말·같은 뜻 다른 표현·잡음·다의어', 'ahn2026nlp'),
        ('lab:sim/v1-like', 'Simulation', 'LIKE 검색기', 'LIKE search lab', '#s2', 2, '')], [
        ('lab:concept/relational-database', 'broader', T + 'deployment', '#s1'), ('lab:concept/structured-data', 'broader', T + 'feature-engineering', '#s1'),
        ('lab:concept/unstructured-data', 'broader', T + 'tokenization', '#s4'), ('lab:method/sql-like', 'broader', T + 'rule-vs-learning', '#s2'),
        ('lab:metric/precision-recall', 'broader', T + 'precision-recall', '#s2'), ('lab:method/synonym-dictionary', 'broader', T + 'rule-vs-learning', '#s3'),
        ('lab:limitation/rule-taxonomy', 'broader', T + 'rule-vs-learning', '#s3'), ('lab:concept/nl-characteristics', 'broader', T + 'tokenization', '#s4'),
        ('lab:concept/relational-database', 'hasLimitation', 'lab:concept/unstructured-data', '#s4'), ('lab:method/sql-like', 'evaluatedBy', 'lab:metric/precision-recall', '#s2'),
        ('lab:claim/like-low-recall', 'supports', 'lab:method/sql-like', '#s2'), ('lab:method/synonym-dictionary', 'hasLimitation', 'lab:limitation/rule-taxonomy', '#s3'),
        ('lab:concept/structured-data', 'contrastsWith', 'lab:concept/unstructured-data', '#s4'), ('lab:concept/nl-characteristics', 'partOf', 'lab:concept/unstructured-data', '#s4'),
        ('lab:sim/v1-like', 'demonstratedBy', 'lab:method/sql-like', '#s2')], (p01.QUIZ, lambda q: '#s' + q[2]))

    import p02
    QMAP.update({'q21': 'lab:method/bag-of-words', 'q22': 'lab:concept/embedding', 'q23': 'lab:metric/cosine', 'q24': 'lab:method/semantic-search'})
    P['02'] = ('02_embedding', '2', '2장 · 말을 좌표로 — 임베딩과 유사도', ['lab:concept/embedding', 'lab:metric/cosine'],
               ['ahn2026vdb', 'mikolov2013efficient', 'reimers2019sbert', 'ahn2026nlp'], [
        ('lab:method/bag-of-words', 'Method', '낱말 세기 (BoW)', 'Bag of words', '#s1', 2, '낱말마다 자리 하나, 나온 횟수를 적음'),
        ('lab:concept/embedding', 'Concept', '임베딩 (뜻의 좌표)', 'Embedding', '#s2', 1, '뜻이 비슷하면 가까운 실수 좌표', 'mikolov2013efficient'),
        ('lab:concept/sentence-embedding', 'Concept', '문장 임베딩', 'Sentence embedding', '#s2', 2, '문장 전체를 좌표 하나로', 'reimers2019sbert'),
        ('lab:metric/cosine', 'Metric', '코사인 유사도', 'Cosine similarity', '#s3', 2, '두 화살표 사이 각도로 잰 닮음, −1~1'),
        ('lab:metric/euclid-dot', 'Metric', '유클리드 거리·내적', 'Euclidean distance and dot product', '#s3', 2, '끝점 거리, 자리끼리 곱의 합'),
        ('lab:method/semantic-search', 'Method', '의미 검색 (벡터 검색)', 'Semantic search', '#s4', 2, '질문 좌표와 가장 가까운 k개'),
        ('lab:claim/vector-f1', 'Claim', '여덟 가지 뜻 F1 평균: LIKE %.3f, 사전 %.3f, 좌표 %.3f' % (sm['like'], sm['dict'], sm['vec']), 'Mean F1 by method', '#s4', 2, '', 'ahn2026vdb'),
        ('lab:limitation/negation-sarcasm', 'Limitation', '부정어·비꼼은 좌표도 자주 놓친다', 'Negation and sarcasm', '#s4', 2, ''),
        ('lab:claim/cosine-beats-dot', 'Claim', '정규화 안 한 내적은 긴 리뷰를 올려 F1 평균 %.3f (코사인 %.3f)' % (sm['dotraw'], sm['vec']), 'Unnormalized dot favors long reviews', '#duel', 2, ''),
        ('lab:sim/v2-anatomy', 'Simulation', '임베딩 해부실 + 낱말 지도', 'Embedding anatomy lab', '#s2', 2, '')], [
        ('lab:method/bag-of-words', 'broader', T + 'word-embedding', '#s1'), ('lab:concept/embedding', 'broader', T + 'word-embedding', '#s2'), ('lab:concept/sentence-embedding', 'broader', T + 'embedding-space', '#s2'),
        ('lab:metric/cosine', 'broader', T + 'linear-algebra', '#s3'), ('lab:metric/euclid-dot', 'broader', T + 'linear-algebra', '#s3'), ('lab:method/semantic-search', 'broader', T + 'embedding-space', '#s4'),
        ('lab:limitation/negation-sarcasm', 'broader', T + 'embedding-space', '#s4'),
        ('lab:method/bag-of-words', 'hasLimitation', 'lab:limitation/negation-sarcasm', '#s1'), ('lab:concept/embedding', 'contrastsWith', 'lab:method/bag-of-words', '#s2'),
        ('lab:concept/sentence-embedding', 'partOf', 'lab:concept/embedding', '#s2'), ('lab:method/semantic-search', 'measuredBy', 'lab:metric/cosine', '#s4'),
        ('lab:metric/euclid-dot', 'contrastsWith', 'lab:metric/cosine', '#s3'), ('lab:claim/vector-f1', 'supports', 'lab:method/semantic-search', '#s4'),
        ('lab:method/semantic-search', 'hasLimitation', 'lab:limitation/negation-sarcasm', '#s4'), ('lab:claim/cosine-beats-dot', 'supports', 'lab:metric/cosine', '#duel'),
        ('lab:sim/v2-anatomy', 'demonstratedBy', 'lab:concept/embedding', '#s2')], (p02.QUIZ, lambda q: '#s' + q[2]))

    import p03
    ivf4 = [x for x in R['ivf'] if x['nprobe'] == 4][0]
    QMAP.update({'q31': 'lab:concept/vector-record', 'q32': 'lab:method/ivf', 'q33': 'lab:method/hnsw', 'q34': 'lab:method/metadata-filter', 'q35': 'lab:concept/hybrid-storage'})
    P['03'] = ('03_vector_store', '3', '3장 · 벡터 창고 — 벡터 DB의 저장·색인·검색', ['lab:concept/vector-database', 'lab:method/hnsw'],
               ['ahn2026vdb', 'jegou2011pq', 'malkov2020hnsw', 'johnson2021faiss', 'pgvector'], [
        ('lab:concept/vector-database', 'Concept', '벡터 데이터베이스', 'Vector database', '#s1', 1, '좌표·메타데이터·원문 레코드와 ANN 색인'),
        ('lab:concept/vector-record', 'Concept', '벡터 레코드와 저장 용량', 'Vector record and storage', '#s1', 2, '건수 × 차원 × 4바이트'),
        ('lab:method/quantization', 'Method', '양자화 (PQ)', 'Product quantization', '#s1', 3, '좌표를 적은 바이트로 압축', 'jegou2011pq'),
        ('lab:concept/ann', 'Concept', '근사 최근접 이웃 검색 (ANN)', 'Approximate nearest neighbor search', '#s2', 2, '재현율을 조금 내주고 속도를 얻음'),
        ('lab:method/ivf', 'Method', '서랍 색인 (IVF)', 'Inverted file index', '#s2', 2, '군집 서랍 몇 개만 열어 찾음', 'johnson2021faiss'),
        ('lab:method/hnsw', 'Method', '그래프 색인 (HNSW)', 'HNSW graph index', '#s3', 2, '위층 지름길, 아래층 이웃 길', 'malkov2020hnsw'),
        ('lab:method/metadata-filter', 'Method', '메타데이터 필터 (먼저/나중 거르기)', 'Metadata filtering', '#s4', 2, '좌표 검색에 표 조건을 함께'),
        ('lab:concept/hybrid-storage', 'Concept', '관계형 DB와 벡터 DB의 역할 나누기 (pgvector)', 'Relational + vector division of labor', '#s5', 2, '사실은 표, 뜻은 벡터', 'pgvector'),
        ('lab:claim/ivf-speed', 'Claim', '점 5,000개에서 IVF nprobe 4: 재현율 %.1f%%, 비교 %d번' % (ivf4['recall'] * 100, ivf4['cmp']), 'IVF trades little recall for speed', '#duel', 2, ''),
        ('lab:limitation/post-filter-short', 'Limitation', '찾은 뒤 거르기는 k개를 못 채울 수 있다', 'Post-filtering may return fewer than k', '#s4', 2, ''),
        ('lab:sim/v3-graph', 'Simulation', '길 찾기 그래프 실험장', 'HNSW path lab', '#s3', 2, '')], [
        ('lab:concept/vector-database', 'broader', T + 'embedding-space', '#s1'), ('lab:concept/vector-record', 'broader', T + 'deployment', '#s1'), ('lab:method/quantization', 'broader', T + 'deployment', '#s1'),
        ('lab:concept/ann', 'broader', T + 'knn', '#s2'), ('lab:method/ivf', 'broader', T + 'knn', '#s2'), ('lab:method/hnsw', 'broader', T + 'knn', '#s3'), ('lab:method/metadata-filter', 'broader', T + 'deployment', '#s4'),
        ('lab:concept/hybrid-storage', 'broader', T + 'deployment', '#s5'), ('lab:limitation/post-filter-short', 'broader', T + 'deployment', '#s4'),
        ('lab:concept/vector-record', 'partOf', 'lab:concept/vector-database', '#s1'), ('lab:method/ivf', 'partOf', 'lab:concept/ann', '#s2'), ('lab:method/hnsw', 'partOf', 'lab:concept/ann', '#s3'),
        ('lab:method/hnsw', 'contrastsWith', 'lab:method/ivf', '#s3'), ('lab:concept/ann', 'partOf', 'lab:concept/vector-database', '#s2'), ('lab:claim/ivf-speed', 'supports', 'lab:method/ivf', '#duel'),
        ('lab:method/metadata-filter', 'hasLimitation', 'lab:limitation/post-filter-short', '#s4'), ('lab:method/quantization', 'partOf', 'lab:concept/vector-record', '#s1'),
        ('lab:concept/hybrid-storage', 'relatedTo', 'lab:concept/vector-database', '#s5'), ('lab:sim/v3-graph', 'demonstratedBy', 'lab:method/hnsw', '#s3')], (p03.QUIZ, lambda q: '#s' + q[2]))

    import p04
    d4 = R['duel4']
    QMAP.update({'q41': 'lab:concept/llm', 'q42': 'lab:method/rag', 'q43': 'lab:method/chunking', 'q44': 'lab:method/hybrid-search', 'q45': 'lab:limitation/stale-docs'})
    P['04'] = ('04_llm_rag', '4', '4장 · 찾아서 답하는 AI — LLM과 RAG', ['lab:method/rag', 'lab:concept/llm'],
               ['ahn2026vdb', 'lewis2020rag', 'robertson2009bm25', 'ahn2026nlp'], [
        ('lab:concept/llm', 'Concept', '대형 언어 모델 (다음 말 잇기)', 'Large language model', '#s1', 1, '앞말이 주어졌을 때 다음 말의 확률로 문장을 이어 씀'),
        ('lab:limitation/hallucination', 'Limitation', '환각 — 모르는 것도 그럴듯하게 지어냄', 'Hallucination', '#s1', 2, ''),
        ('lab:method/rag', 'Method', '검색 증강 생성 (RAG)', 'Retrieval-augmented generation', '#s2', 1, '근거 조각을 찾아 붙이고 자료로만 답하게 함', 'lewis2020rag'),
        ('lab:method/chunking', 'Method', '청킹 (조각 크기·겹침)', 'Chunking', '#s3', 2, '문장 단위로 목표 글자 수까지 모음'),
        ('lab:method/bm25', 'Method', 'BM25 (글자 점수)', 'BM25', '#s4', 2, '낱말 일치 빈도와 드묾으로 점수', 'robertson2009bm25'),
        ('lab:method/hybrid-search', 'Method', '하이브리드 검색 (α × 뜻 + (1−α) × 글자)', 'Hybrid search', '#s4', 2, '뜻 점수와 글자 점수를 섞음'),
        ('lab:claim/hybrid-wins', 'Claim', 'k = 1에서 벡터만 %d개, 섞기(α 0.3) %d개 맞힘 (질문 %d개)' % (d4['vec_right'], d4['hyb_right'], R['n']['ragq']), 'Hybrid search answers more', '#duel', 2, '', 'ahn2026vdb'),
        ('lab:limitation/stale-docs', 'Limitation', '구버전 문서가 함께 찾아짐', 'Stale documents retrieved', '#s5', 2, ''),
        ('lab:method/date-filter', 'Method', '날짜·버전 필터와 출처 표시', 'Date filter and citations', '#s5', 2, ''),
        ('lab:sim/v4-rag', 'Simulation', 'RAG 시뮬레이터', 'RAG simulator', '#s2', 2, '')], [
        ('lab:concept/llm', 'broader', T + 'pretrained-lm', '#s1'), ('lab:limitation/hallucination', 'broader', T + 'pretrained-lm', '#s1'), ('lab:method/rag', 'broader', T + 'rag', '#s2'),
        ('lab:method/chunking', 'broader', T + 'rag', '#s3'), ('lab:method/bm25', 'broader', T + 'rag', '#s4'), ('lab:method/hybrid-search', 'broader', T + 'rag', '#s4'),
        ('lab:limitation/stale-docs', 'broader', T + 'rag', '#s5'), ('lab:method/date-filter', 'broader', T + 'rag', '#s5'),
        ('lab:concept/llm', 'hasLimitation', 'lab:limitation/hallucination', '#s1'), ('lab:limitation/hallucination', 'addressedBy', 'lab:method/rag', '#s2'),
        ('lab:method/chunking', 'partOf', 'lab:method/rag', '#s3'), ('lab:method/hybrid-search', 'partOf', 'lab:method/rag', '#s4'), ('lab:method/bm25', 'partOf', 'lab:method/hybrid-search', '#s4'),
        ('lab:claim/hybrid-wins', 'supports', 'lab:method/hybrid-search', '#duel'), ('lab:method/rag', 'hasLimitation', 'lab:limitation/stale-docs', '#s5'),
        ('lab:limitation/stale-docs', 'addressedBy', 'lab:method/date-filter', '#s5'), ('lab:sim/v4-rag', 'demonstratedBy', 'lab:method/rag', '#s2')], (p04.QUIZ, lambda q: '#s' + q[2]))

    import p05
    sp = R['spam']
    QMAP.update({'q51': 'lab:method/content-recommend', 'q52': 'lab:method/spam-novelty', 'q53': 'lab:method/chat-memory', 'q54': 'lab:method/adoption-check'})
    P['05'] = ('05_cases', '5', '5장 · 현장 사례 — 영화 추천, SNS 모니터링, 챗봇의 기억, 도입 판단', ['lab:method/content-recommend', 'lab:method/chat-memory'],
               ['ahn2026vdb', 'spotify_annoy', 'radford2021clip', 'morris2023inversion', 'pgvector'], [
        ('lab:method/content-recommend', 'Method', '리뷰 좌표 평균으로 하는 콘텐츠 추천', 'Content recommendation from review embeddings', '#s1', 2, '좋아한 이유의 좌표가 닮은 작품', 'spotify_annoy'),
        ('lab:limitation/cold-start', 'Limitation', '콜드 스타트', 'Cold start', '#s1', 2, ''),
        ('lab:method/spam-novelty', 'Method', '광고 걸러내기와 새 이야기 알림', 'Spam filtering and novelty alert', '#s2', 2, '닮음으로 거르고 다름으로 알림'),
        ('lab:claim/spam-f1', 'Claim', '둘째 주 광고 걸러내기 F1: 글자 겹침 %.3f, 좌표 %.3f' % (sp['jac']['f1'], sp['cos']['f1']), 'Embedding spam filter F1', '#duel', 2, '', 'ahn2026vdb'),
        ('lab:method/chat-memory', 'Method', '대화 기억 창고 (장기 기억)', 'Conversation memory store', '#s3', 2, '지난 대화를 좌표로 저장, 가까운 기억만 꺼냄'),
        ('lab:limitation/embedding-privacy', 'Limitation', '좌표에서 원문이 되살아날 수 있음 — 좌표도 원문처럼 보호', 'Embedding inversion risk', '#s4', 2, '', 'morris2023inversion'),
        ('lab:method/adoption-check', 'Method', '벡터 DB 도입 판단 다섯 질문', 'Adoption checklist', '#s4', 2, '질문 종류·데이터·규모·갱신·보안'),
        ('lab:concept/multimodal-embedding', 'Concept', '글과 그림을 같은 좌표에 (CLIP)', 'Multimodal embedding', '#sum', 3, '', 'radford2021clip'),
        ('lab:sim/v5-sns', 'Simulation', 'SNS 상황실', 'SNS monitoring lab', '#s2', 2, '')], [
        ('lab:method/content-recommend', 'broader', T + 'embedding-space', '#s1'), ('lab:limitation/cold-start', 'broader', T + 'embedding-space', '#s1'),
        ('lab:method/spam-novelty', 'broader', T + 'anomaly-detection', '#s2'), ('lab:method/chat-memory', 'broader', T + 'rag', '#s3'), ('lab:limitation/embedding-privacy', 'broader', T + 'privacy', '#s4'),
        ('lab:method/adoption-check', 'broader', T + 'deployment', '#s4'), ('lab:concept/multimodal-embedding', 'broader', T + 'contrastive', '#sum'),
        ('lab:method/content-recommend', 'hasLimitation', 'lab:limitation/cold-start', '#s1'), ('lab:claim/spam-f1', 'supports', 'lab:method/spam-novelty', '#duel'),
        ('lab:method/chat-memory', 'hasLimitation', 'lab:limitation/embedding-privacy', '#s3'), ('lab:method/adoption-check', 'raises', 'lab:limitation/embedding-privacy', '#s4'),
        ('lab:sim/v5-sns', 'demonstratedBy', 'lab:method/spam-novelty', '#s2')], (p05.QUIZ, lambda q: '#s' + q[2]))

    P['practice'] = ('practice/index', '6', '마지막 장 · 실전 연습장 — 랩플릭스 운영실', ['lab:sim/practice-rag'], ['ahn2026vdb'], [
        ('lab:sim/practice-search', 'Simulation', '리뷰 검색 창구', 'Review search desk', '#search', 2, '방식·개수·별점 조건으로 F1 맞추기'),
        ('lab:sim/practice-rag', 'Simulation', '고객센터 RAG 창구', 'RAG help desk', '#rag', 2, '조각·k·α·문턱·날짜 필터'),
        ('lab:sim/practice-sns', 'Simulation', 'SNS 상황실', 'SNS room', '#sns', 2, '광고 문턱·묶음 닮음·알림 기준'),
        ('lab:sim/practice-store', 'Simulation', '창고 관리실', 'Index room', '#store', 2, '전수·IVF·HNSW의 재현율과 비교 횟수'),
        ('lab:question/robust-setting', 'Question', '조건이 바뀌어도 고른 설정의 점수가 유지되나?', 'Is the setting robust?', '#close', 2, ''),
        ('lab:limitation/tradeoffs', 'Limitation', '한쪽을 얻으면 다른 쪽을 내주는 맞바꿈', 'Trade-offs', '#close', 2, '')], [
        ('lab:sim/practice-search', 'demonstratedBy', T + 'precision-recall', '#search'), ('lab:sim/practice-rag', 'demonstratedBy', T + 'rag', '#rag'),
        ('lab:sim/practice-sns', 'demonstratedBy', T + 'anomaly-detection', '#sns'), ('lab:sim/practice-store', 'demonstratedBy', T + 'knn', '#store'),
        ('lab:limitation/tradeoffs', 'broader', T + 'deployment', '#close'), ('lab:question/robust-setting', 'addressedBy', 'lab:sim/practice-search', '#close'),
        ('lab:question/robust-setting', 'addressedBy', 'lab:sim/practice-rag', '#close'), ('lab:question/robust-setting', 'addressedBy', 'lab:sim/practice-store', '#close'),
        ('lab:sim/practice-sns', 'raises', 'lab:limitation/tradeoffs', '#sns')], None)
    return P


def main():
    P = pages()
    report, newids = [], {}
    for key, (slug, number, title, about, refs, nodes, edges, qz) in P.items():
        quiz, qa = (qz if qz else (None, None))
        kg, rf, meta = build_page(slug, number, title, about, refs, nodes, edges, quiz, qa)
        if slug == 'practice/index': meta['url'] = SITE + 'practice/'
        if slug == 'index': meta['url'] = SITE
        for n in kg['nodes']:
            if n['type'] not in ('Work', 'QuizItem') and n['id'] not in newids:
                newids[n['id']] = {'label': n['label'], 'type': n['type'], 'first_page': slug}
        d = os.path.join(ROOT, 'kg', slug.replace('/index', '') if slug != 'index' else 'index')
        os.makedirs(d, exist_ok=True)
        for n, o in (('kg.json', kg), ('refs.json', rf), ('meta.json', meta)):
            json.dump(o, open(os.path.join(d, n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        html = os.path.join(ROOT, slug + '.html'); orig = html + '.orig'
        open(orig, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read())
        subprocess.check_call(['python3', os.path.join(HERE, 'retrofit.py'), orig, '--kg', os.path.join(d, 'kg.json'), '--refs', os.path.join(d, 'refs.json'),
                               '--meta', os.path.join(d, 'meta.json'), '--backbone', BB, '-o', html])
        rep = os.path.join(d, 'check_report.md')
        subprocess.call(['python3', os.path.join(HERE, 'check.py'), orig, html, '--backbone', BB, '--report', rep])
        os.remove(orig)
        report.append((slug, open(rep, encoding='utf-8').read()))
    json.dump({'series': 'vector_db_lab', 'date': DATE, 'new_ids': newids}, open(os.path.join(ROOT, 'KG_new_ids.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for s, r in report:
        print('=====', s); print(r[:900])


if __name__ == '__main__':
    main()
