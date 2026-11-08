# AGENTS.md — 작업 가이드 (사람·AI 에이전트 공통)

이 저장소는 **비공개(private)** 로 유지하며 공개 전환은 저장소 관리자가 결정합니다. 수록 자료의 이용 조건은 전 회차
공공누리 제1유형(출처표시: 한국산업인력공단, Q-Net)이며 근거는 `NOTICE.md` 에 있습니다. 저장소 고유 작업물(LaTeX 변환·조판 코드, `tools/`, 문서)은 GPL-3.0-only(`LICENSE`)이며, 새 코드 파일에는 `SPDX-License-Identifier: GPL-3.0-only` 를 답니다. 새 회차를 추가해도 같은 조건과 출처표시를 따릅니다. 기본 브랜치에 직접 커밋하지 말고 작업 브랜치 + PR 로 반영합니다.

## 0. 원칙
1. **원본이 유일한 기준**입니다. 원본(Q-Net 시험지 PDF/HWP, 정답표)에 없는 내용·정답을 추정해서 채우지 않습니다.
   원본의 오탈자도 그대로 두고 필요하면 `% [원문 그대로]` 주석을 답니다.
2. 확인할 수 없는 부분은 문항 안에 `\reviewflag{사유}` 를 남기고 GitHub 이슈로 등록합니다.
3. 정답은 `answers/answers.csv` 가 기준입니다. 문항 파일의 정답 줄은 `tools/apply_answers.py` 로 생성하며 손으로 고치지 않습니다.
4. 토큰·비밀번호 등 비밀값을 커밋·로그·PR·이슈에 남기지 않습니다.

## 1. 자료 수집
- 기출문제 게시판: `cst00309`, 정답 게시판: `cst00310` (README 의 URL).
  목록은 `cst003.do?id=cst00301s01&gSite=L&gId=60&page=N&boardId=Q004&code=1008`(기출) / `code=1206`(정답) 으로 조회되고,
  상세는 `cst00302` 에 POST(artlSeq, boardId=Q004, code, menuType), 첨부는 `cst00302s01`(filePath, fileName, fileSeq, artlSeq) 로 받습니다.
  스크립트: `tools/pipeline/qnet_fetch.py` (목록·상세·첨부 일괄 다운로드, SHA-256 기록).
- 내려받은 파일은 저장소 밖의 빈 작업 폴더에 둡니다(신뢰할 수 없는 입력). ZIP 내부 파일명은 CP949 일 수 있습니다.
- 새 회차가 올라오면 `docs/SOURCES.md` 에 게시글 번호·파일명·SHA-256 을 추가합니다.

## 2. 변환

HWP 는 두 도구를 함께 씁니다: **kordoc**(본문·수식 추출, 수식이 LaTeX 로 나옴)과 **rhwp**(페이지 렌더링 → 원본 대조용 이미지, `export-tables` 로 표·표 형태 선택지 구조 확인). 2026-11 샘플 비교에서 rhwp `export-markdown` 은 수식이 HWP 수식 문법(`pi ^{e}`, `LEFT {`)으로 나오고 화면 줄바꿈이 섞여 본문 추출 기본 도구로는 kordoc 을 유지했습니다.

| 원본 형식 | 도구 | 비고 |
|---|---|---|
| HWP (제19~22, 24, 25, 30회 문제 / 대부분의 정답) | kordoc (`npx kordoc file.hwp -o out.md`) | 수식은 `$…$` LaTeX 로 나옴. 품질 높음 |
| 텍스트 PDF (제23, 26~29, 31, 35~37회) | kordoc `--no-tables` | 기본 모드는 2단 시험지에서 본문을 누락할 수 있음(제23회 확인). 표 구조는 사라지므로 원본 대조로 재구성 |
| 스캔 PDF (제32~34회) | kordoc `--no-tables --ocr` | OCR 오류(ㄱ→7, ㄷ→2, 한자 누락, 띄어쓰기) 많음 → **전수 교정 필수** |
| 정답표 | HWP 안의 그림(BMP) / 스캔 PDF | 사람·비전 모델 2인 독립 판독 후 대조 |

- 문항 분리: `tools/pipeline/split1.py <md 폴더> <회차> <out.json>` — 과목 머리글·번호 연속성으로 분리, 누락 번호는 `gap_before` 로 기록.
- LaTeX 생성: `tools/pipeline/gen1.py <작업폴더> <저장소> <회차> <split.json> <md 폴더> answers/answers.csv`
- 생성 직후 반드시 `python tools/apply_answers.py`, `python tools/validate.py`, `python tools/build.py <과목>/<회차>` 를 실행합니다.

## 3. 교정(원본 대조) 절차
1. 원본 페이지를 PNG 로 렌더링(130 dpi 이상)합니다. PDF 는 PyMuPDF, **HWP 는 rhwp**(`tools/pipeline/rhwp_pages.py`,
   <https://github.com/edwardkim/rhwp> v0.8.7, 릴리스 바이너리를 SHA256SUMS 로 검증 후 사용)로 렌더링합니다.
   rhwp 렌더링은 글꼴 차이로 쪽·단 배치가 원본과 다르고 꼬리말이 끝 줄과 겹칠 수 있으나 내용은 원본 그대로입니다.
2. 문항마다 확인: 번호 · 문두 · 선택지 5개(순서) · 지문/보기 상자 · 표(모든 칸) · 수식 · 그림 · 공통 지문.
3. 표기 규칙
   - 보기 상자(〈보기〉 제목) → `\begin{bogi} … \end{bogi}`, 제목 없는 테두리 지문 → `framedtext`
   - 표 → `tabular` (`{\small\centering\begin{tabular}{|c|c|}…\end{tabular}\par}`)
   - 밑줄 → `\uline{}`, 빈칸 → `\blank{}`, 수식 → `$…$`
   - 그림 → **TikZ/pgfplots 로 문항 파일 안에 재현하는 것이 원칙**입니다(그래프·도식·단순 도면). 모든 라벨·눈금 값·
     기호·점선/실선·교점 관계를 원본과 같게 그리고, 원본에 없는 정보는 넣지 않습니다. 재현 후 빌드한 PDF 를 원본과
     나란히 보고 확인하며 `flags` 에 `tikz` 를 적습니다.
     정확한 재현이 어려운 사진·지적도·복잡한 도면만 원본에서 잘라 `figures/NN-k.png` 로 두고
     `\qfigure[너비]{figures/NN-k.png}` 로 넣습니다(커밋 전 `python tools/optimize_figures.py` 로 용량 최적화).
     SVG 는 XeLaTeX 에서 직접 넣을 수 없어(컴파일마다 Inkscape 필요) 사용하지 않습니다.
   - LaTeX 특수문자 `% $ & # _ { }` 는 이스케이프
4. 교정을 마친 파일은 `%% conversion:` 줄의 `review=pending` 을 `review=proofread-<검토자>` 로 바꾸고
   `flags=` 는 남은 확인 사항만(없으면 `none`) 적습니다. `%% kapa:` · `%% source:` 줄은 바꾸지 않습니다.
5. 과목·회차 단위로 `python tools/build.py <과목>/<회차>` 컴파일, `python tools/validate.py` 통과 확인.
6. 원문 대조(자동): `python -I tools/pipeline/text_crosscheck.py . <원본텍스트폴더>` — 문항 파일의 한글 낱말이 원본 텍스트층(텍스트 PDF 는 PyMuPDF, HWP 는 rhwp `export-text`)에 실제로 있는지 확인합니다. 원본에 없는 낱말은 '원문 변경' 의심이므로 이미지로 확인합니다(TikZ 그림 라벨처럼 원래 텍스트층에 없는 글자는 정상). 원문 오탈자를 '교정'하지 않았는지 확인하는 데 씁니다.
7. HWP 회차는 rhwp 렌더링이 일부 글자(여는 따옴표 ‘ “ 등)를 빠뜨리거나 줄을 겹쳐 그리는 일이 있습니다. **렌더링에만 없는 글자는 원문 근거가 아닙니다** — 글자는 HWP 텍스트(rhwp `export-text`)로, 구조(상자·표·배치)는 이미지로 확인합니다.

## 4. 기여(PR) 절차
1. `git switch -c <type>/<요약>` (예: `fix/accounting-26-tables`, `data/round-38`)
2. 커밋 메시지: `<과목>/<회차>: <무엇을>` (예: `accounting/26: 41~45번 선택지 표 재구성`)
3. PR 본문: 범위(회차·과목·문항), 대조한 원본, 검증 결과(validate/build), 남은 문제와 관련 이슈.
   해결하지 못한 이슈는 `Refs #N` 으로 연결하고 **`Closes`/`Fixes` 는 실제로 해결한 이슈에만** 씁니다.
4. `python tools/validate.py --write-status` 로 `docs/STATUS.md` 를 갱신해 함께 커밋합니다.

## 5. 이슈·라벨
- 새 이슈 전에 기존 이슈를 검색합니다. 원인과 해결 방법이 같은 항목은 한 이슈로 묶되 회차·과목·문항을 표로 적습니다.
- 이슈 본문 필수 항목: 회차 · 과목 · 문항 번호 · 자료 출처(artlSeq/파일) · 문제 상황 · 수행한 확인 · 후속 조치.
- 라벨

| 라벨 | 용도 |
|---|---|
| `data:collection` | 자료 수집·정리 작업(PR) |
| `parse-error` | 파싱·OCR 오류, 깨진 문자·수식 |
| `missing-item` | 누락 문항·원본 자료 미확보 |
| `answer-check` | 정답 확인 필요(미확인·판독 불일치·정정) |
| `figure-check` | 그림 추출·재현 확인 필요 |
| `table-check` | 표 구조 재구성 필요 |
| `needs-review` | 원본 대조 검토 필요 |
| `license` | 저작권·이용 조건 확인 |
| `documentation` | 문서 (GitHub 기본 라벨) |

## 6. flags 사전 (`%% conversion:` 줄)
| flag | 의미 / 조치 |
|---|---|
| `tab-layout(table?)` | 원문에 열 정렬(표 또는 표 형태 선택지)이 있었을 가능성. 원본 대조 후 tabular 로 재구성 |
| `underlined-header(table?)` | 밑줄 친 열 머리(예: 부채요소/자본요소)가 감지됨. 선택지 표 재구성 필요 |
| `table` | HWP 표를 자동 변환함. 병합 칸·정렬 확인 |
| `figure` | 원본 그림을 추출해 포함함. 잘림·누락 확인. 스캔본은 페이지 일부일 수 있음 |
| `shared-prefix` / `post-content-moved-forward` | 앞 문항 뒤에 있던 지문·지시문을 이 문항 앞에 붙임. 귀속이 맞는지 확인 |
| `choices-reordered` | 2단 배치 선택지를 ①~⑤ 순서로 재정렬함 |
| `wrapped-choice-line` | 줄바꿈된 선택지 줄을 합침 |
| `inline-choice-markers` | ①~⑤ 가 문두(밑줄 어구 등) 안에 있는 유형. 선택지 목록 없음이 정상 |
| `missing-choice:…` / `no-choices` | 선택지 일부를 찾지 못함 → 원본 대조 필수 |
| `content-after-choices-unassigned` | 선택지 뒤 내용을 귀속하지 못함(보통 시험지 끝 안내문) |
| `dup-choice-marker` | 같은 선택지 기호가 두 번 나옴 → 확인 |
| `answer-table-number:N` | 정답표의 인쇄 번호(N)가 문제지 번호와 다름(번호 체계 차이, 정상) |
| `short-stem` | 문두가 매우 짧음 → 누락 확인 |
| `tikz` | 원본 그림을 TikZ/pgfplots 로 재현함(원본 대조 완료) |

## 버전과 변경 이력

변경은 `CHANGELOG.md` 의 `[Unreleased]` 에 기록한다. 버전 규칙과 새 회차 추가·릴리스 절차는 `docs/RELEASING.md` 에 있다.
- 새 회차는 MINOR, 정정은 PATCH, 폴더·메타데이터·매크로 변경은 호환성 깨짐이다.
