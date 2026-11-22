/* 벡터 DB 연구실 — 페이지 숫자의 원본 계산 (node code/analysis.js → data/results.json)
   페이지 안 실험은 같은 vlab.js로 브라우저에서 다시 계산한다. */
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const VL = require(path.join(ROOT, 'build', 'vlab.js'));
const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'corpus.json')));
d.lexicon = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'lexicon.json')));
VL.init(d);
const R = d.reviews, out = {};
const r3 = x => Math.round(x * 1000) / 1000;

/* 0. 데이터 요약 */
out.n = { reviews: R.length, sns: d.sns.length, kb: d.kb.length, ragq: d.ragq.length, lex: Object.keys(d.lexicon.lex).length, dims: d.lexicon.dims.length };
out.movies = d.movies.map(m => { const rs = R.filter(r => r.movie === m.id); return { id: m.id, title: m.title, genre: m.genre, n: rs.length, avg: r3(rs.reduce((s, r) => s + r.stars, 0) / rs.length) }; });
out.avg_all = r3(R.reduce((s, r) => s + r.stars, 0) / R.length);

/* 1. 리뷰 검색: LIKE 한 낱말 / 사람이 만든 동의어 사전 / 임베딩 (정답 수만큼 위에서 자름) */
out.search = d.searchq.map(q => {
  const L = VL.like(R, q.like), Di = VL.likeAny(R, q.dict), qv = VL.embed(q.q).v, rel = R.filter(r => VL.rel(r, q.asp)).length;
  const V = VL.topk(R, r => VL.cos(qv, r.vec), rel).map(x => x.it);
  const raw = VL.topk(R, r => VL.dot(qv, VL.embed(r.text).raw), rel).map(x => x.it);
  const f = x => ({ p: r3(x.p), r: r3(x.r), f1: r3(x.f1), n: x.n, tp: x.tp });
  return { id: q.id, q: q.q, rel, like: f(VL.prf(L, R, q.asp)), dict: f(VL.prf(Di, R, q.asp)), vec: f(VL.prf(V, R, q.asp)), dotraw: f(VL.prf(raw, R, q.asp)) };
});
const mean = (a, k) => r3(a.reduce((s, x) => s + x[k].f1, 0) / a.length);
out.search_mean = { like: mean(out.search, 'like'), dict: mean(out.search, 'dict'), vec: mean(out.search, 'vec'), dotraw: mean(out.search, 'dotraw') };
/* '재밌' LIKE의 함정: 부정어 리뷰가 섞인다 */
const funLike = VL.like(R, '재밌');
out.fun_like = { n: funLike.length, neg: funLike.filter(r => r.asp.fun === -1).length, missed: R.filter(r => r.asp.fun === 1 && r.text.indexOf('재밌') < 0).length };
const wasteLike = VL.like(R, '아깝');
out.waste_like = { n: wasteLike.length, actor: wasteLike.filter(r => r.text.indexOf('배우가 아깝') >= 0).length, notwaste: wasteLike.filter(r => r.text.indexOf('안 아깝') >= 0).length };

/* 2. 낱말 사이 코사인 */
const pairs = [['꿀잼', '재밌'], ['꿀잼', '노잼'], ['꿀잼', '무섭'], ['재밌', '감동'], ['OST', '노래'], ['돈값', '아깝'], ['결제', '환불']];
out.word_cos = pairs.map(p => ({ a: p[0], b: p[1], cos: r3(VL.cos(VL.wordVec(p[0]), VL.wordVec(p[1]))) }));
out.sent_cos = [['꿀잼', '재밌어요'], ['재밌어요', '안 재밌어요'], ['돈 아깝다', '돈이 하나도 안 아깝다'], ['진짜 무서워요', '하나도 안 무섭다']].map(p => ({ a: p[0], b: p[1], cos: r3(VL.cos(VL.embed(p[0]).v, VL.embed(p[1]).v)) }));

/* 3. 창고: 점 5,000개, IVF(서랍 64개)와 두 층 그래프 */
const P = VL.cloud(5000, 11, 9), Q = VL.cloud(60, 77, 9);
const ivf = VL.kmeans(P, 64, 3, 12);
out.ivf = [1, 2, 4, 8, 16].map(np => { let rc = 0, cmp = 0; Q.forEach(q => { const t = VL.exact(P, q, 10), s = VL.ivfSearch(P, ivf, q, 10, np); rc += VL.recall(s.ids, t); cmp += s.cmp; }); return { nprobe: np, recall: r3(rc / Q.length), cmp: Math.round(cmp / Q.length) }; });
const G = VL.graph(P, 8, 5);
out.graph = [10, 20, 40, 80].map(ef => { let rc = 0, cmp = 0; Q.forEach(q => { const t = VL.exact(P, q, 10), s = VL.graphSearch(P, G, q, 10, ef); rc += VL.recall(s.ids, t); cmp += s.cmp; }); return { ef, recall: r3(rc / Q.length), cmp: Math.round(cmp / Q.length) }; });
out.graph_top = G.topIds.length;
/* 고차원 확인: 교육용 24차원 리뷰 좌표 483개에 서랍 16개 */
{ const RVv = R.map(r => r.vec), Q24 = d.searchq.map(q => VL.embed(q.q).v).concat(d.sns.map(s => s.vec).filter(v => VL.norm(v) > 0).slice(0, 60));
  const iv = VL.kmeans(RVv, 16, 3, 12);
  out.ivf24 = { note: '같은 거리(동점)는 정답으로 침', n: RVv.length, q: Q24.length, lists: 16, rows: [1, 2, 4, 8].map(np => { let rc = 0, cmp = 0; Q24.forEach(q => { const t = VL.exact(RVv, q, 10), lim = VL.d2(RVv[t[9]], q) + 1e-9, s = VL.ivfSearch(RVv, iv, q, 10, np); rc += s.ids.filter(i => VL.d2(RVv[i], q) <= lim).length / 10; cmp += s.cmp; }); return { nprobe: np, recall: r3(rc / Q24.length), cmp: Math.round(cmp / Q24.length) }; }) }; }
out.storage = { n: 1e6, d: 768, gb: r3(1e6 * 768 * 4 / 1e9) };

/* 4. RAG: 쪼갠 크기 × 검색 방식 */
out.rag = [];
[80, 150, 250].forEach(size => { const ch = VL.chunk(d.kb, size, 0, true);
  [1, .5, 0].forEach(alpha => [1, 3].forEach(k => { const e = VL.ragEval(ch, { k, alpha, thr: .35, newest: true }); out.rag.push({ size, chunks: ch.length, alpha, k, acc: r3(e.acc), hit: r3(e.hit), hall: e.hall, tokens: e.tokens }); })); });
{ const ch = VL.chunk(d.kb, 150, 0, true);
  const v = VL.ragEval(ch, { k: 1, alpha: 1, thr: .35, newest: true }), h = VL.ragEval(ch, { k: 1, alpha: .3, thr: .35, newest: true });
  out.duel4 = { vec: r3(v.acc), hyb: r3(h.acc), vec_right: v.res.filter(x => x.right).length, hyb_right: h.res.filter(x => x.right).length,
    lp204_vec: v.res.find(x => x.q.q.indexOf('LP-204') === 0).hits[0].c.doc, lp204_hyb: h.res.find(x => x.q.q.indexOf('LP-204') === 0).hits[0].c.doc };
  /* 구버전 문서를 섞으면 */
  const old = VL.ragEval(ch, { k: 3, alpha: .5, thr: .35, newest: false }).res.find(x => x.q.doc === 'refund_v2' && x.q.key === '3일 이내');
  out.old_doc = { retrieved_old: old.hits.some(h => h.c.old), titles: old.hits.map(h => h.c.title) };
  const st = VL.ragEval(VL.chunk(d.kb, 250, 0, true), { k: 3, alpha: 1, thr: .35, newest: true }).res.find(x => x.q.q.indexOf('주가') >= 0);
  out.stock_q = { top: st.hits[0].c.title, s: r3(st.hits[0].s) };
}
/* LP-204 질문: 조각별 뜻 점수와 글자 점수 */
{ const ch = VL.chunk(d.kb, 150, 0, true), h = VL.retrieve(ch, 'LP-204 오류가 떠요', { k: 3, alpha: 1, newest: true });
  out.lp204 = h.slice(0, 2).map(x => ({ doc: x.c.doc, title: x.c.title, vec: r3(x.vec), bm: r3(x.bm) })); }
/* 작은 언어 모델: '<시작>' 다음 말 */
const bg = VL.bigram();
const nxt = w => Object.entries(bg[w] || {}).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, v]) => [k, v]);
out.bigram = { start: nxt('<시작>'), '진짜': nxt('진짜'), '연기': nxt('연기') };
out.bigram_tot = { '연기': Object.values(bg['연기'] || {}).reduce((a, b) => a + b, 0), '진짜': Object.values(bg['진짜'] || {}).reduce((a, b) => a + b, 0) };

/* 5. 사례: 영화끼리 닮음(리뷰 임베딩 평균), SNS 중복 광고, 새 이슈 */
const mv = d.movies.map(m => { const rs = R.filter(r => r.movie === m.id && r.stars >= 4), v = new Array(24).fill(0); rs.forEach(r => r.vec.forEach((x, i) => v[i] += x / rs.length)); return { id: m.id, title: m.title, v }; });
out.movie_sim = mv.map(a => ({ title: a.title, best: mv.filter(b => b.id !== a.id).map(b => [b.title, r3(VL.cos(a.v, b.v))]).sort((x, y) => y[1] - x[1])[0] }));
const pref = VL.embed('무섭고 반전 있는 영화').v;
out.pref_rank = mv.map(m => [m.title, r3(VL.cos(pref, m.v))]).sort((a, b) => b[1] - a[1]).slice(0, 3);
/* 광고 걸러내기: 신고된 광고 예시 3개(묶음마다 첫 문장)와 닮은 글을 걸러낸다 */
const S = d.sns, jac = (a, b) => { const A = new Set(VL.grams(a)), B = new Set(VL.grams(b)); let i = 0; A.forEach(x => { if (B.has(x)) i++; }); return i / (A.size + B.size - i || 1); };
const REP = require(path.join(ROOT, 'data', 'corpus.json')).sns && [1, 2, 3].map(g => d.sns.find(s => s.dup === g));
out.spam_reported = REP.map(s => s.id);
const pool = S.filter(s => REP.indexOf(s) < 0).map(s => ({ day: s.day, y: s.topic === 'promo', g: s.dup, jac: Math.max(...REP.map(r => jac(s.text, r.text))), cos: Math.max(...REP.map(r => VL.cos(s.vec, r.vec))) }));
const score = (arr, key, t) => { let tp = 0, fp = 0, fn = 0; arr.forEach(p => { const hit = p[key] >= t; if (hit && p.y) tp++; else if (hit) fp++; else if (p.y) fn++; }); const pr = tp / (tp + fp || 1), rc = tp / (tp + fn || 1); return { f1: r3(pr + rc ? 2 * pr * rc / (pr + rc) : 0), thr: r3(t), p: r3(pr), r: r3(rc), tp, fp, fn }; };
const tune = key => { let b = { f1: -1 }; for (let t = .05; t < 1.001; t += .01) { const x = score(pool.filter(p => p.day <= 7), key, t); if (x.f1 > b.f1) b = x; } return b; };
const wk2 = pool.filter(p => p.day >= 8);
out.spam = { week1: pool.filter(p => p.day <= 7).length, week2: wk2.length, promo2: wk2.filter(p => p.y).length, newstyle2: wk2.filter(p => p.g === 4).length,
  jac: Object.assign({ tuned: tune('jac').thr }, score(wk2, 'jac', tune('jac').thr)), cos: Object.assign({ tuned: tune('cos').thr }, score(wk2, 'cos', tune('cos').thr)) };
/* 새 이슈: 그날 글이 지난 글 모두와 닮지 않았으면(최대 코사인 < 0.6) '새 이야기' */
out.novel = []; for (let day = 2; day <= 14; day++) { const prev = S.filter(s => s.day < day && s.topic !== 'promo'), today = S.filter(s => s.day === day && s.topic !== 'promo');
  const nov = today.filter(s => Math.max(...prev.map(p => VL.cos(s.vec, p.vec))) < .6); out.novel.push({ day, n: today.length, novel: nov.length, issue: nov.filter(s => s.issue).length }); }
out.issue_by_day = Array.from({ length: 14 }, (_, i) => S.filter(s => s.day === i + 1 && s.issue).length);

/* 6장: 어텐션이 근거 조각에 얼마나 머무나 (교육용 좌표, 배율 β = 8) */
{ const ch = VL.chunk(d.kb, 150, 0, true), A = d.ragq.filter(q => q.doc);
  const focus = (k, beta) => { let tot = 0, hit = 0; A.forEach(q => { const h = VL.retrieve(ch, q.q, { k, alpha: .3, newest: true }), qv = VL.embed(q.q).v, toks = [];
      h.forEach(x => VL.tokens(x.c.text).forEach(w => toks.push({ v: VL.embed(w).v, gold: x.c.text.indexOf(q.key) >= 0 })));
      const w = VL.softmax(toks.map(t => VL.dot(qv, t.v)), beta); tot += toks.reduce((s0, t, i) => s0 + (t.gold ? w[i] : 0), 0); if (h.some(x => x.c.text.indexOf(q.key) >= 0)) hit++; });
    return { focus: r3(tot / A.length), hit, n: A.length }; };
  out.att = { k1: focus(1, 8), k2: focus(2, 8), k3: focus(3, 8), k5: focus(5, 8) };
  out.softmax_ex = VL.softmax([2, 1, 0], 1).map(r3); }
/* 7장: 여러 걸음 질문 — 벡터만 vs 그래프 */
{ const G = VL.graphPrep(JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'graph.json')))), ch = VL.chunk(d.kb, 150, 0, true);
  const fact = e => G.nodes[G.idx[e.s]].label + ' —' + e.p + '→ ' + G.nodes[G.idx[e.o]].label;
  const vec = k => { let ok = 0, c = 0; G.mq.forEach(q => { const h = VL.retrieve(ch, q.q, { k, alpha: .3, newest: true }); c += h.reduce((a, x) => a + x.c.text.length, 0); if (q.docs.every(x => h.some(y => y.c.doc === x))) ok++; }); return { ok, chars: Math.round(c / G.mq.length) }; };
  let gok = 0, gc = 0, gf = 0; G.mq.forEach(q => { const r = VL.graphRAG(G, q.q, { hops: 2 }); if (q.path.every(p => r.nodes.indexOf(G.idx[p]) >= 0)) gok++; gc += r.facts.map(fact).join(' / ').length; gf += r.facts.length; });
  out.graph7 = { nodes: G.nodes.length, edges: G.edges.length, mq: G.mq.length, classes: G.ont.length, vec2: vec(2), vec5: vec(5), graph: { ok: gok, chars: Math.round(gc / G.mq.length), facts: r3(gf / G.mq.length) } };
  /* 코사인 점수 분포: "재밌는 영화 리뷰" 정답과 오답 */
  const q = d.searchq[0], qv = VL.embed(q.q).v, rel = R.filter(r => VL.rel(r, q.asp)).map(r => VL.cos(qv, r.vec)), irr = R.filter(r => !VL.rel(r, q.asp)).map(r => VL.cos(qv, r.vec));
  const med = a => { const b = a.slice().sort((x, y) => x - y); return r3(b[Math.floor(b.length / 2)]); };
  out.cosdist = { rel_med: med(rel), irr_med: med(irr), rel_n: rel.length, irr_n: irr.length }; }
fs.writeFileSync(path.join(ROOT, 'data', 'results.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify({ search_mean: out.search_mean, fun_like: out.fun_like, waste_like: out.waste_like, word_cos: out.word_cos, sent_cos: out.sent_cos, ivf: out.ivf, graph: out.graph, duel4: out.duel4, old_doc: out.old_doc, stock: out.stock_q, spam: out.spam, novel: out.novel, movie_sim: out.movie_sim, pref: out.pref_rank, bigram: out.bigram }, null, 0));
