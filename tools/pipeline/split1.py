# SPDX-License-Identifier: GPL-3.0-only
"""Split kordoc markdown of 1차 exam periods into questions -> JSON.
usage: split1.py <conv_dir> <round> <out_json>
"""
import re, sys, json, pathlib
sys.stdout.reconfigure(encoding="utf-8")

SUBJ = {  # normalized header -> (folder, canonical ko)
    '민법': 'civil_law', '경제원론': 'economics', '경제학원론': 'economics',
    '부동산학원론': 'real_estate', '부동산관계법규': 'appraisal_law', '감정평가관계법규': 'appraisal_law',
    '회계학': 'accounting', '영어': 'english',
}
CIRC = '①②③④⑤'

def norm_header(line):
    s = re.sub(r'[#<>〈〉《》【】\[\]\s*「」()（）]', '', line)
    s = re.sub(r'^(제?\d과목|\d교시)', '', s)
    return s

FOOTER_RES = [
    re.compile(r'^[A-Z]?\s*-\s*\d+\s*-\s*\d+$'),           # A-14-1
    re.compile(r'^-?\s*\[?\s*\d\s*교시\s*\]?\s*$'),          # -[1교시]
    re.compile(r'^\d\s*교시\s*\(?[A-Z]?\s*형?\)?\s*-?\s*\d*\s*-?\s*$'),
    re.compile(r'^-\s*\d+\s*-$'), re.compile(r'^\d+\s*/\s*\d+$'),
    re.compile(r'^[A-Z]형\s*-?\s*\d+\s*-?$'), re.compile(r'^\(?\s*[A-Z]\s*형\s*\)?$'),
    re.compile(r'^\d+\s*쪽$'), re.compile(r'^Page\s*\d+', re.I),
]

COVER_RE = re.compile(r'^#*\s*(시험시간|수험번호|성\s*명|교시\s+형별|감독자|\d+\s*분\s*$|※\s*답안카드)|수험번호.*성\s*명|^#*\s*[숔숕숖숗]')

def clean_line(ln):
    raw = ln.rstrip('\n')
    s = raw.strip()
    # kordoc list artifacts: "1. 4\. text" / "- ① text" / "  - ① text"
    s = re.sub(r'^(?:[-*+]\s+|\d+\.\s+)(?=\d{1,3}\\?\.\s)', '', s)
    s = re.sub(r'^\d+\.\s+(?=\d{1,3}\\\.)', '', s)
    s = re.sub(r'^[-*+]\s+(?=[①②③④⑤ㄱ-ㅎ㉠-㉭ⓐ-ⓩ(（<〈])', '', s)
    s = re.sub(r'^[-*+]\s+(?=\S)', '', s) if re.match(r'^[-*+]\s+[①②③④⑤]', raw.strip()) else s
    s = re.sub(r'^(\d{1,3})\\\.', r'\1.', s)
    s = re.sub(r'^(\d{1,3})\s*．\s*', r'\1. ', s)
    return s

def is_footer(s):
    return any(r.match(s) for r in FOOTER_RES)

def split_period(md, expect_start=1):
    lines = [clean_line(l) for l in md.split('\n')]
    qs = []; cur = None; subject = None; last = expect_start - 1; pending_subject = None
    i = 0
    in_html_table = False
    preamble = []; pending_pre = []
    for s in lines:
        if not in_html_table and '<table' in s: in_html_table = True
        if in_html_table:
            if cur: cur['lines'].append(s)
            if '</table>' in s: in_html_table = False
            continue
        if is_footer(s):
            continue
        h = norm_header(s)
        if len(s) < 40 and h in SUBJ and not re.match(r'^\d', s):
            pending_subject = h
            continue
        if COVER_RE.search(s):
            continue  # cover-page boxes (시험시간/수험번호/성명 …)
        s = re.sub(r'^#{1,6}\s*', '', s)
        s = clean_line(s)
        m = re.match(r'^(\d{1,3})\.\s*(.*)$', s)
        if m:
            n = int(m.group(1))
            rest = m.group(2)
            looks_q = (len(rest) > 8 and not re.match(r'^[\d,.%￦$]', rest) and not rest.startswith('①')
                       and re.search(r'\?|것은|고른|옳은|옳지', rest) is not None)
            gap = None
            ok = (n == last + 1) or (pending_subject and n in (1, last + 1)) or (cur is None and n == 1)
            if not ok and looks_q and n in (last + 2, last + 3):
                ok = True; gap = list(range(last + 1, n))
            if not ok and looks_q and n == 1 and last >= 38 and (last % 40 == 0 or last % 40 >= 38):
                ok = True; gap = 'restart'
            if ok:
                spre = None
                if pending_subject:
                    subject = pending_subject; pending_subject = None; spre = pending_pre; pending_pre = []
                elif gap == 'restart':
                    subject = None
                cur = {'number': n, 'subject_ko': subject, 'lines': [rest]}
                if spre: cur['subject_pre'] = spre
                if gap: cur['gap_before'] = gap
                qs.append(cur); last = n
                continue
        if pending_subject is not None:
            pending_pre.append(s)
        elif cur is not None:
            cur['lines'].append(s)
        else:
            preamble.append(s)
    return qs

def ORDER(r):
    if r == 19: return {1: ['민법', '부동산관계법규', '회계학'], 2: ['경제원론', '영어']}
    if r <= 26:
        p2 = ['부동산관계법규', '회계학'] if r in (25, 26) else ['회계학', '부동산관계법규']
        return {1: ['민법', '경제원론'], 2: p2}
    return {1: ['민법', '경제학원론', '부동산학원론'], 2: ['감정평가관계법규', '회계학']}

def main():
    conv = pathlib.Path(sys.argv[1]); rnd = sys.argv[2]; out = pathlib.Path(sys.argv[3])
    res = []
    for period in ('p1', 'p2'):
        f = conv / f'{period}.md'
        if not f.exists():
            continue
        md = f.read_text(encoding='utf-8', errors='replace')
        qs = split_period(md)
        # drop cover-page numbered items: unlabeled questions before the first labeled question no.1
        first_lab = next((i for i, q in enumerate(qs) if q['subject_ko'] and q['number'] == 1), None)
        if first_lab:
            qs = [q for i, q in enumerate(qs) if i >= first_lab or q['subject_ko']]
        # fill unlabeled blocks by the known subject order of the era
        order = ORDER(int(rnd))[int(period[1])]
        blocks = []
        for q in qs:
            if not blocks or q['number'] == 1 or (q['subject_ko'] and q['subject_ko'] != blocks[-1][0]):
                blocks.append([q['subject_ko'], []])
            blocks[-1][1].append(q)
        for bi, (sk, bq) in enumerate(blocks):
            if sk is None and bi < len(order):
                for q in bq:
                    q['subject_ko'] = order[bi]; q['subject_inferred'] = True
        for q in qs:
            q['period'] = int(period[1])
            # trailing blank cleanup
            while q['lines'] and not q['lines'][-1].strip(): q['lines'].pop()
        res.extend(qs)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding='utf-8')
    # quick report
    from collections import Counter
    c = Counter((q['period'], q['subject_ko']) for q in res)
    print(rnd, dict(c), 'total', len(res))

if __name__ == '__main__':
    main()
