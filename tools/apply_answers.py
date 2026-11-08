#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""answers/answers.csv 의 정답을 각 문항 파일의 \\end{question} 뒤에 (다시) 기록한다.

사용법 (저장소 루트에서):  python tools/apply_answers.py [--check]
- 정답 매칭: (회차, 교시, 과목 블록 순서, 과목 내 순번 seq). 정답표의 번호 체계(과목별 1~40 재시작 등)가
  문제지와 달라도 과목 블록 순서와 순번으로 연결한다.
- 정답이 여러 개면 \\answer{a,b}, 5개 모두면 \\answerall + \\answernote, 행이 없거나 '?' 이면 \\answerunknown.
- --check : 파일을 바꾸지 않고 불일치만 보고 (종료 코드 1).
"""
import csv, json, pathlib, re, sys, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {'latex', 'tools', 'build', 'docs', 'skills', 'sources', 'answers'}

def answer_block(row):
    if row is None or not row['answer'].strip() or '?' in row['answer']:
        return '\\answerunknown'
    a = row['answer'].split('|')
    if len(a) == 5:
        return '\\answerall\n\\answernote{정답표에 1,2,3,4,5 모두 정답으로 표기(전원 정답)}'
    s = '\\answer{%s}' % ','.join(a)
    if len(a) > 1:
        s += '\n\\answernote{복수 정답(정답표 원문: %s)}' % ', '.join(a)
    return s

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    check = '--check' in sys.argv
    subjects = json.loads((ROOT / 'subjects.json').read_text(encoding='utf-8'))['subjects']
    alias = {s['folder']: [re.sub(r'\s', '', x) for x in s['aliases']] for s in subjects}
    rows = collections.defaultdict(list)
    for r in csv.DictReader(open(ROOT / 'answers' / 'answers.csv', encoding='utf-8')):
        rows[(int(r['round']), int(r['period']))].append(r)
    changed = bad = 0
    for f in sorted(ROOT.glob('*/[0-9]*/[0-9][0-9].tex')):
        if f.parts[-3] in SKIP or f.stem == '00':
            continue
        t = f.read_text(encoding='utf-8')
        m = re.search(r'^%% kapa: (.*)$', t, re.M)
        if not m: continue
        meta = dict(x.split('=', 1) for x in m.group(1).split() if '=' in x)
        if meta.get('exam') != '1': continue
        rr = rows.get((int(meta['round']), int(meta['period'])), [])
        blocks = [re.sub(r'\s', '', rr[i]['subject']) for i in range(0, len(rr), 40)]
        bi = next((i for i, b in enumerate(blocks) if b in alias.get(f.parts[-3], [])), None)
        seq = int(meta['seq'])
        row = rr[bi * 40 + seq - 1] if bi is not None and bi * 40 + seq - 1 < len(rr) else None
        want = answer_block(row)
        head, sep, tail = t.partition('\\end{question}')
        if not sep:
            print('NO \\end{question}:', f.relative_to(ROOT)); bad += 1; continue
        new = head + sep + '\n' + want + '\n'
        if new != t:
            if check:
                print('MISMATCH', f.relative_to(ROOT)); bad += 1
            else:
                f.write_text(new, encoding='utf-8'); changed += 1
    print('changed', changed, 'problems', bad)
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
