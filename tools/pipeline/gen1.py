# SPDX-License-Identifier: GPL-3.0-only
"""Generate 1차 question .tex files from split JSON.
usage: gen1.py <qnet_dir> <repo_dir> <round> <split_json> <conv_dir> [answers_csv]
Writes <repo>/<subject>/<round>/NN.tex (+figures/), and appends flags to <qnet>/meta/flags1.jsonl
"""
import sys, re, json, csv, pathlib, shutil
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from mdtex import inline, parse_html_table, parse_gfm_table, grid_table_to_latex
from PIL import Image

SUBJ = {'민법': 'civil_law', '경제원론': 'economics', '경제학원론': 'economics', '부동산학원론': 'real_estate',
        '부동산관계법규': 'appraisal_law', '감정평가관계법규': 'appraisal_law', '회계학': 'accounting', '영어': 'english'}
CIRC = '①②③④⑤'
BS = chr(92)  # backslash

Q = pathlib.Path(sys.argv[1]); REPO = pathlib.Path(sys.argv[2]); RND = int(sys.argv[3])
qs = json.loads(pathlib.Path(sys.argv[4]).read_text(encoding='utf-8'))
CONV = pathlib.Path(sys.argv[5])
ANS = {}  # (period, block_index, seq) -> row ; blocks = consecutive 40-question subject groups in table order
if len(sys.argv) > 6 and pathlib.Path(sys.argv[6]).exists():
    rows = [r for r in csv.DictReader(open(sys.argv[6], encoding='utf-8-sig')) if int(r['round']) == RND]
    cnt = {}
    for row in rows:
        p = int(row['period']); k = cnt.get(p, 0); cnt[p] = k + 1
        ANS[(p, k // 40, k % 40 + 1)] = row
man = json.loads((Q / 'meta/manifest.json').read_text(encoding='utf-8'))
SRC = {(m['round'], m['part']): m for m in man if m['exam'] == 1}
YEAR = RND + 1989

def blocks_of(lines):
    """group lines into blocks: ('table', rows) / ('img', path) / ('para', text)"""
    out = []; i = 0
    while i < len(lines):
        s = lines[i]
        if '<table' in s:
            buf = []
            while i < len(lines):
                buf.append(lines[i])
                if '</table>' in lines[i]: break
                i += 1
            out.append(('table', parse_html_table('\n'.join(buf)))); i += 1; continue
        if s.strip().startswith('|') and s.strip().endswith('|'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                buf.append(lines[i]); i += 1
            out.append(('table', parse_gfm_table(buf))); continue
        m = re.fullmatch(r'\s*!\[[^\]]*\]\(([^)]+)\)\s*', s)
        if m:
            out.append(('img', m.group(1))); i += 1; continue
        if s.strip():
            out.append(('para', s.strip()))
        i += 1
    return out

def split_choices(text):
    """text containing ①..⑤ in order -> list of 5 strings or None"""
    pos = []; start = 0
    for c in CIRC:
        k = text.find(c, start)
        if k < 0: return None, pos
        pos.append(k); start = k + 1
    items = []
    for j, k in enumerate(pos):
        end = pos[j + 1] if j + 1 < len(pos) else len(text)
        items.append(text[k + 1:end].strip())
    return items, pos


def analyse(q):
    """-> dict(stem=blocks, choices=list|None, after=blocks, flags)"""
    flags = []
    bl = blocks_of(q['lines'])
    ci = next((i for i, b in enumerate(bl) if b[0] == 'para' and b[1].startswith('①')), None)
    if ci is None:
        allt = ' '.join(b[1] for b in bl if b[0] == 'para')
        if all(c in allt for c in CIRC): flags.append('inline-choice-markers')
        else: flags.append('no-choices')
        aft = []
        while len(bl) > 1 and bl[-1][0] == 'para' and bl[-1][1].startswith('※'):
            aft.insert(0, bl.pop())
        return dict(stem=bl, choices=None, after=aft, flags=flags, inline=True)
    stem = bl[:ci]; j = ci; texts = []; seen = set()
    while j < len(bl) and bl[j][0] == 'para' and len(seen) < 5:
        t = bl[j][1]
        if texts and not re.match(r'^[①②③④⑤]', t):
            texts[-1] += ' ' + t; flags.append('wrapped-choice-line')
        else:
            texts.append(t)
        seen |= set(re.findall(r'[①②③④⑤]', t)); j += 1
    after = bl[j:]
    pieces = {}
    for t in texts:
        for m in re.finditer(r'([①②③④⑤])([^①②③④⑤]*)', t):
            if m.group(1) in pieces: flags.append('dup-choice-marker')
            pieces[m.group(1)] = (pieces.get(m.group(1), '') + ' ' + m.group(2)).strip()
    choices = None
    if all(c in pieces for c in CIRC):
        choices = [pieces[c] for c in CIRC]
        order = ''.join(re.findall(r'[①②③④⑤]', ' '.join(texts)))
        if order != CIRC: flags.append('choices-reordered')
    else:
        flags.append('missing-choice:' + ''.join(c for c in CIRC if c not in pieces))
        stem = bl[:j]; after = bl[j:]
    stem_text = ''.join(b[1] for b in stem if b[0] == 'para')
    inline_mode = False
    if choices and len(re.sub(r'\s', '', stem_text)) < 8 and not any(b[0] != 'para' for b in stem):
        # passage whose segments are numbered ①..⑤ (e.g. underline grammar items): keep inline
        inline_mode = True; flags.append('inline-choice-markers')
        stem = bl[:j]; choices = None
    return dict(stem=stem, choices=choices, after=after, flags=flags, inline=inline_mode)

RANGE_RE = re.compile(r'(\d{1,3})\s*[~～\-–]\s*(\d{1,3})')

def render(a, prefix, figdir_rel, figdir, nn):
    flags = list(a['flags'])
    img_k = 0
    def emit(blocks):
        nonlocal img_k
        res = []
        for b in blocks:
            if b[0] == 'para':
                t = b[1]
                if '\t' in t: flags.append('tab-layout(table?)')
                if re.search(r'<u>[^<]{0,40}</u>\s*(<u>|\t)', t): flags.append('underlined-header(table?)')
                res.append((BS + 'quad ').join(inline(seg) for seg in t.split('\t')) + r' \par')
            elif b[0] == 'table':
                flags.append('table'); res.append(grid_table_to_latex(b[1]))
            elif b[0] == 'img':
                img_k += 1
                src = (CONV / b[1]).resolve()
                name = f'{nn}-{img_k}.png'
                figdir.mkdir(parents=True, exist_ok=True)
                try:
                    Image.open(src).save(figdir / name)
                except Exception:
                    flags.append(f'image-convert-failed:{src.name}'); continue
                flags.append('figure')
                res.append(r'\qfigure{%s/%s}' % (figdir_rel, name))
        return res
    parts = []
    if prefix:
        parts.append('% [공통 지문/지시문: 원문에서 여러 문항에 걸쳐 제시됨]')
        parts.append(BS + 'begin{framedtext}\n' + '\n'.join(emit(prefix)) + '\n' + BS + 'end{framedtext}')
        flags.append('shared-prefix')
    st = emit(a['stem'])
    if st and st[0].endswith(r' \par'): st[0] = st[0][:-5]
    parts += st
    if a['choices']:
        parts.append(BS + 'begin{choices}\n' + '\n'.join('  ' + BS + 'item ' + inline(c) for c in a['choices']) + '\n' + BS + 'end{choices}')
    stem_text = ''.join(b[1] for b in a['stem'] if b[0] == 'para')
    if len(re.sub(r'\s', '', stem_text)) < 8 and not a['inline']: flags.append('short-stem')
    return '\n'.join(parts), flags

def answer_tex(period, bi, seq, number):
    a = ANS.get((period, bi, seq))
    if not a or not a['answer'].strip() or '?' in a['answer']:
        return r'\answerunknown', ['answer-unknown']
    extra = []
    if int(a['number']) != number:
        extra.append(f'answer-table-number:{a["number"]}')
    ans = a['answer'].strip().split('|')
    note = a.get('note', '').strip()
    t = r'\answer{%s}' % ','.join(ans) if len(ans) < 5 else r'\answerall'
    if len(ans) >= 5: note = (note + ' ' if note else '') + '정답표 원문: ' + ', '.join(ans)
    if note: t += '\n' + r'\answernote{%s}' % inline(note)
    return t, extra

flags_all = []
by_subj = {}
for q in qs:
    by_subj.setdefault((q['period'], q['subject_ko']), []).append(q)
# pass 1: analyse, distribute post-choice content forward as shared prefixes
order = sorted(qs, key=lambda q: (q['period'], qs.index(q)))
ana = [analyse(q) for q in order]
prefix = [[] for _ in order]
for i, a in enumerate(ana):
    if not a['after']: continue
    txt = ' '.join(b[1] for b in a['after'] if b[0] == 'para')
    m = RANGE_RE.search(txt)
    targets = []
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        targets = [k for k in range(i + 1, len(order)) if order[k]['period'] == order[i]['period'] and lo <= order[k]['number'] <= hi]
    if not targets and i + 1 < len(order) and order[i + 1]['period'] == order[i]['period']:
        targets = [i + 1]
    if targets:
        for k in targets: prefix[k] = prefix[k] + a['after']
        a['flags'].append('post-content-moved-forward')
    else:
        a['flags'].append('content-after-choices-unassigned')
for (period, sko), lst in by_subj.items():
    folder = SUBJ.get(sko or '', 'unknown_subject')
    d = REPO / folder / str(RND)
    src = SRC.get((RND, f'p{period}'))
    srcline = f'%% source: Q-Net 감정평가사 기출문제 (cst00309) artlSeq={src["source"].split("/")[2] if src else "?"} file={src["source"] if src else "?"}'
    d.mkdir(parents=True, exist_ok=True)
    pre = lst[0].get('subject_pre') or []
    if any(x.strip() for x in pre):
        bl = blocks_of(pre)
        body = '\n'.join(inline(b[1]) + r' \par' for b in bl if b[0] == 'para')
        (d / '00.tex').write_text(
            f'%% kapa: exam=1 round={RND} year={YEAR} period={period} form=A subject={folder} subject_ko={sko} seq=0 kind=subject-instructions\n'
            + srcline + '\n%% 과목 공통 지시문(문항 앞에 제시된 안내). 묶음 PDF 에서 첫 문항 앞에 출력된다.\n'
            + BS + 'begin{framedtext}\n' + body + '\n' + BS + 'end{framedtext}\n', encoding='utf-8')
    bi = [k for k in by_subj if k[0] == period].index((period, sko))
    for q in lst:
        idx = (q['number'] - 1) % 40 + 1
        nn = f'{idx:02d}'
        k = order.index(q)
        body, flags = render(ana[k], prefix[k], 'figures', d / 'figures', nn)
        at, af = answer_tex(period, bi, idx, q['number'])
        flags += af
        head = [
            f'%% kapa: exam=1 round={RND} year={YEAR} period={period} form=A subject={folder} subject_ko={sko} seq={idx} number={q["number"]}',
            srcline,
            f'%% conversion: kordoc 4.24.51 -> tools/gen1.py (auto); review=pending; flags={",".join(sorted(set(flags))) or "none"}',
        ]
        tex = '\n'.join(head) + '\n' + (BS + 'begin{question}{%d}\n%s\n' + BS + 'end{question}\n%s\n') % (q['number'], body, at)
        (d / f'{nn}.tex').write_text(tex, encoding='utf-8')
        flags_all.append({'round': RND, 'period': period, 'subject': folder, 'seq': idx, 'number': q['number'], 'flags': sorted(set(flags))})

with open(Q / 'meta' / f'flags1_{RND}.json', 'w', encoding='utf-8') as f:
    json.dump(flags_all, f, ensure_ascii=False, indent=0)
from collections import Counter
c = Counter(fl.split(':')[0] for x in flags_all for fl in x['flags'])
print(RND, 'files', len(flags_all), dict(c))
