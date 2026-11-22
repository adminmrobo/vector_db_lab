# 전체 다시 만들기: 데이터 → 숫자(results.json) → 페이지 7개 → 지식 색인·꾸러미 붙이기·점검
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(H)
subprocess.check_call([sys.executable, os.path.join(ROOT, 'code', 'make_data.py')])
subprocess.check_call([sys.executable, os.path.join(ROOT, 'code', 'lexicon.py')])
subprocess.check_call([sys.executable, os.path.join(ROOT, 'code', 'make_graph.py')])
subprocess.check_call(['node', os.path.join(ROOT, 'code', 'analysis.js')], stdout=subprocess.DEVNULL)
for p in ['p00', 'p01', 'p02', 'p03', 'p04', 'p05', 'p_ch6', 'p_ch7', 'p06']:
    subprocess.check_call([sys.executable, os.path.join(H, p + '.py')])
subprocess.check_call([sys.executable, os.path.join(H, 'kg_build.py')])
subprocess.check_call([sys.executable, os.path.join(H, 'make_docs.py')])
subprocess.check_call([sys.executable, os.path.join(H, 'make_teacher.py')])
