#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""구조 검증 + 처리 현황 문서(docs/STATUS.md) 생성.

사용법 (저장소 루트에서):  python tools/validate.py [--write-status]
검사 항목
  - 각 과목·회차 폴더에 01.tex~40.tex 가 모두 있는지 (누락 번호 보고)
  - 메타데이터 줄(%% kapa:, %% source:, %% conversion:) 존재·형식
  - \\begin{question}{N} 번호와 메타데이터 number 일치
  - 선택지(choices) 항목 수 = 5 (선택지 표시가 문두에 포함된 유형은 예외 표시)
  - 정답 매크로 존재 및 answers/answers.csv 와 일치
  - review 상태(pending / proofread-*), 남은 flags, \\reviewflag 집계
종료 코드: 오류(error) 가 있으면 1, 경고만 있으면 0.
"""
import csv, json, pathlib, re, sys, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {'latex', 'tools', 'build', 'docs', 'skills', 'sources', 'answers', '.git', '.github'}
META = re.compile(r'^%% kapa: (.*)$', re.M)

def kv(s):
    return dict(x.split('=', 1) for x in s.split() if '=' in x)

def load_answers():
    f = ROOT / 'answers' / 'answers.csv'
    res = collections.defaultdict(list)
    if f.exists():
        for r in csv.DictReader(open(f, encoding='utf-8')):
            res[(int(r['round']), int(r['period']))].append(r)
    return res

def expected_answer(rows, block, seq):
    i = block * 40 + seq - 1
    return rows[i] if i < len(rows) else None

def markdown_tilde_errors():
    """Markdown 본문의 물결표(~)는 GitHub 에서 두 개가 한 줄에 있으면 취소선(~텍스트~)으로 렌더링된다.
    범위는 '–'(en dash)로 쓴다. 코드 스팬(`...`)과 코드 블록 안은 검사하지 않는다."""
    out = []
    for md in sorted(ROOT.rglob('*.md')):
        if {'.git', 'build'} & set(md.relative_to(ROOT).parts):
            continue
        fence = False
        for i, line in enumerate(md.read_text(encoding='utf-8').split('\n'), 1):
            if re.match(r'\s*(```|~~~)', line):
                fence = not fence; continue
            if fence:
                continue
            prose = re.sub(r'`+[^`]*`+', '', line)
            if '~' in prose:
                out.append(f'{md.relative_to(ROOT).as_posix()}:{i}: 범위 물결표 "~" 대신 "–" 를 쓴다(GitHub 취소선 방지)')
    return out

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write = '--write-status' in sys.argv
    subjects = json.loads((ROOT / 'subjects.json').read_text(encoding='utf-8'))['subjects']
    order_of = {}
    answers = load_answers()
    errors, warns = [], []
    table = []
    for sd in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name not in SKIP):
        for rd in sorted((d for d in sd.iterdir() if d.is_dir() and d.name.isdigit()), key=lambda d: int(d.name)):
            files = {int(f.stem): f for f in rd.glob('[0-9][0-9].tex') if f.stem != '00'}
            rnd = int(rd.name)
            missing = [n for n in range(1, 41) if n not in files]
            st = collections.Counter(); flags = collections.Counter(); rflags = 0; ans_bad = 0; nchoice_bad = 0
            for n, f in sorted(files.items()):
                t = f.read_text(encoding='utf-8')
                m = META.search(t)
                if not m:
                    errors.append(f'{f.relative_to(ROOT)}: missing %% kapa: line'); continue
                meta = kv(m.group(1))
                qn = re.search(r'\\begin\{question\}\{(\d+)\}', t)
                if not qn or meta.get('number') != qn.group(1):
                    errors.append(f'{f.relative_to(ROOT)}: question number mismatch ({meta.get("number")} vs {qn.group(1) if qn else None})')
                if '%% source:' not in t: errors.append(f'{f.relative_to(ROOT)}: missing %% source:')
                cm = re.search(r'^%% conversion: .*?review=(\S+?);\s*flags=(.*)$', t, re.M)
                if cm:
                    st['pending' if cm.group(1) == 'pending' else 'proofread'] += 1
                    for fl in cm.group(2).split(','):
                        fl = fl.strip().split(':')[0]
                        if fl and fl != 'none': flags[fl] += 1
                else:
                    warns.append(f'{f.relative_to(ROOT)}: no review status')
                rflags += t.count('\\reviewflag{')
                body = t.split('\\begin{choices}')
                if len(body) > 1:
                    # `\item[]` = column-header row of table-style choices, not a choice
                    items = len(re.findall(r'\\item(?!\[\])', body[1].split('\\end{choices}')[0]))
                    if items != 5:
                        nchoice_bad += 1; warns.append(f'{f.relative_to(ROOT)}: {items} choices')
                # answers
                a = re.search(r'\\answer\{([^}]*)\}|\\answerall|\\answerunknown', t)
                if not a:
                    errors.append(f'{f.relative_to(ROOT)}: no answer macro'); continue
                per = int(meta.get('period', 0))
                rows = answers.get((rnd, per), [])
                # block index = position of this subject in the period's subject order (from answers.csv subjects)
                blocks = [rows[i]['subject'] for i in range(0, len(rows), 40)]
                sk = meta.get('subject_ko', '')
                alias = {s['folder']: s['aliases'] for s in subjects}.get(sd.name, [])
                bi = next((i for i, b in enumerate(blocks) if re.sub(r'\s', '', b) in [re.sub(r'\s', '', x) for x in alias + [sk]]), None)
                exp = expected_answer(rows, bi, int(meta['seq'])) if bi is not None else None
                if exp is None:
                    warns.append(f'{f.relative_to(ROOT)}: no answer row to compare')
                else:
                    got = a.group(1).replace(',', '|') if a.group(1) is not None else ('1|2|3|4|5' if 'answerall' in a.group(0) else '?')
                    if got != exp['answer']:
                        ans_bad += 1; errors.append(f'{f.relative_to(ROOT)}: answer {got} != answers.csv {exp["answer"]}')
            table.append(dict(subject=sd.name, round=rnd, files=len(files), missing=missing, pending=st['pending'],
                              proofread=st['proofread'], flags=dict(flags), reviewflags=rflags, answer_mismatch=ans_bad, choice_count_warn=nchoice_bad))
            if missing: errors.append(f'{sd.name}/{rnd}: missing questions {missing}')
    errors += markdown_tilde_errors()
    print(f'errors: {len(errors)}  warnings: {len(warns)}')
    for e in errors[:50]: print('ERROR', e)
    for w in warns[:30]: print('WARN ', w)
    if write:
        ko = {s['folder']: s['name_ko'] for s in subjects}
        L = ['# 처리 현황 (자동 생성: `python tools/validate.py --write-status`)', '',
             '| 과목 | 회차 | 문항 파일 | 누락 | 교정 완료 | 자동 변환(미교정) | 정답 불일치 | 검토 표시(reviewflag) | 주요 flags |',
             '|---|---|---|---|---|---|---|---|---|']
        for r in table:
            top = ', '.join(f'{k}×{v}' for k, v in sorted(r['flags'].items(), key=lambda x: -x[1])[:4])
            L.append(f"| {ko.get(r['subject'], r['subject'])} | {r['round']} | {r['files']} | {','.join(map(str, r['missing'])) or '-'} | {r['proofread']} | {r['pending']} | {r['answer_mismatch']} | {r['reviewflags']} | {top or '-'} |")
        tot = lambda k: sum(r[k] for r in table)
        L += ['', f"합계: 문항 파일 {tot('files')}개, 교정 완료 {tot('proofread')}개, 자동 변환(미교정) {tot('pending')}개, 정답 불일치 {tot('answer_mismatch')}개, reviewflag {tot('reviewflags')}개", '',
              'flags 의미는 AGENTS.md 의 "flags 사전" 참고.']
        (ROOT / 'docs').mkdir(exist_ok=True)
        (ROOT / 'docs' / 'STATUS.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
        (ROOT / 'docs' / 'status.json').write_text(json.dumps(table, ensure_ascii=False, indent=1), encoding='utf-8')
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
