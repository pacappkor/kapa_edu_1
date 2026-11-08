# kapa_edu_1 — 감정평가사 제1차 시험 기출문제 (LaTeX)

Q-Net(한국산업인력공단)에 공개된 **감정평가사 제1차 시험** 기출문제와 최종 정답을
과목별·회차별·문항별 LaTeX 조각 파일로 정리한 저장소입니다.

- 범위: 제19회(2008) – 제37회(2026), 19개 회차 · 3,520문항 (A형 기준)
- 정답: 회차별 **최종 정답**을 문항 파일과 `answers/answers.csv` 에 함께 기록
- 처리 현황: [`docs/STATUS.md`](docs/STATUS.md) (자동 생성) · 출처 목록: [`docs/SOURCES.md`](docs/SOURCES.md)
- 작업 절차(사람·에이전트 공통): [`AGENTS.md`](AGENTS.md) · 재사용 skill 초안: [`skills/kapa-past-exam/SKILL.md`](skills/kapa-past-exam/SKILL.md)

> ℹ️ 3,520문항 모두 원본(시험지 PDF/HWP 페이지 이미지)과 대조 교정을 마쳤습니다(`review=proofread-*`). 교정은 AI 에이전트가 수행했으며
> 사람의 표본 검수는 아직입니다(관련 이슈). 원문 오탈자는 고치지 않고 `% [원문 그대로]` 주석으로 표시합니다.

## 자료 출처와 이용 조건

| 자료 | 위치 |
|---|---|
| 기출문제 | Q-Net 감정평가사 › 기출문제 내려받기 <https://www.q-net.or.kr/cst003.do?id=cst00309&gSite=L&gId=60> |
| 최종 정답 | Q-Net 감정평가사 › 최종 정답 <https://www.q-net.or.kr/cst003.do?id=cst00310&gSite=L&gId=60> |

- 게시글 번호(artlSeq), 첨부파일명, SHA-256 은 `docs/SOURCES.md` 와 각 문항 파일의 `%% source:` 줄에 기록합니다.
- **이용 조건**: 문항·정답 내용은 전 회차 **공공누리 제1유형(출처표시)**, 이 저장소의 변환·조판 코드·도구·문서는 **[GPL-3.0](LICENSE)** — 출처: 한국산업인력공단, Q-Net. 자세한 내용과 적용 근거는 [`NOTICE.md`](NOTICE.md). Q-Net 공지는 2014년 자료부터 제1유형 개방을 밝히고 있으며, 2013년 이전(제19–24회) 자료에도 저장소 관리자 결정으로 같은 조건을 일괄 적용합니다. 저장소 공개 여부는 별도로 관리자가 결정합니다(현재 비공개).
- 원본 시험지 파일(PDF/HWP)은 용량 문제로 저장소에 넣지 않습니다. 필요하면 위 게시판에서 다시 내려받고 SHA-256 으로 확인하세요.

## 디렉터리 구조

```text
<subject>/<round>/NN.tex      문항 파일 (NN = 과목 내 순번 01~40)
<subject>/<round>/00.tex      (있을 때) 과목 공통 지시문 — 예: 회계학 앞의 ※ 안내문
<subject>/<round>/figures/    문항 그림 (NN-k.png) — TikZ 로 재현하지 못한 그림만(사진·지적도 등)
answers/answers.csv           최종 정답표 (정답의 기준 자료)
latex/kapa-exam.sty           공통 스타일 (문항·선택지·정답·보기 상자 매크로)
tools/build.py                회차·과목별 묶음 PDF 빌드 / 컴파일 검증
tools/validate.py             구조 검증 + docs/STATUS.md 생성
tools/optimize_figures.py     남은 PNG 그림 용량 최적화
tools/apply_answers.py        answers.csv → 문항 파일 정답 줄 반영
subjects.json                 폴더명 ↔ 과목명 대응표
docs/                         처리 현황, 출처 목록
skills/kapa-past-exam/        수집·변환·검증 절차 skill 초안
```

### 과목 폴더 대응표

| 폴더 | 과목 | 시험지 표기(회차) |
|---|---|---|
| `civil_law` | 민법 | 민법 (19–37) |
| `economics` | 경제학원론 | 경제원론 (19–26), 경제학원론 (27–37) |
| `real_estate` | 부동산학원론 | 부동산학원론 (27–37) — 제20–26회에는 시행되지 않음 |
| `appraisal_law` | 감정평가관계법규 | 부동산관계법규 (19–26), 감정평가관계법규 (27–37) |
| `accounting` | 회계학 | 회계학 (19–37) |
| `english` | 영어 | 영어 (19) — 제20회부터 공인어학성적으로 대체 |

각 문항 파일의 `subject_ko` 메타데이터에는 해당 회차 시험지에 인쇄된 과목명을 그대로 기록합니다.

## 문항 파일 규칙

```latex
%% kapa: exam=1 round=37 year=2026 period=1 form=A subject=civil_law subject_ko=민법 seq=1 number=1
%% source: Q-Net 감정평가사 기출문제 (cst00309) artlSeq=5258924 file=raw/1008/5258924/…1교시.pdf
%% conversion: kordoc 4.24.51 -> tools/gen1.py (auto); review=pending; flags=none
\begin{question}{1}
권리남용에 관한 설명으로 옳지 않은 것은? (다툼이 있으면 판례에 따름)
\begin{choices}
  \item …
  \item …
  \item …
  \item …
  \item …
\end{choices}
\end{question}
\answer{3}
```

- **파일명** `NN.tex` 는 과목 내 순번(01–40)입니다. 시험지에 인쇄된 번호(예: 2교시 회계학 41–80)는
  `\begin{question}{번호}` 와 메타데이터 `number` 에 보존합니다. 순번 = (인쇄 번호 − 1) mod 40 + 1.
- **프리앰블 없음**: 문항 파일은 조각(fragment)이며 `latex/kapa-exam.sty` 매크로만 사용합니다.
  다른 문서에 넣을 때는 `\usepackage{kapa-exam}` 후 `\subimport{<subject>/<round>/}{NN.tex}`(import 패키지)로
  포함합니다. 그림 경로가 문항 파일 기준 상대경로(`figures/…`)이므로 `\input` 대신 `\subimport` 를 사용합니다.
- **A형만** 정리합니다(A/B형 구분이 없는 회차는 해당 문제지 그대로).
- **공통 지문**(여러 문항에 걸친 지문·지시문)은 해당하는 각 문항 파일 맨 앞 `framedtext` 상자에 복제합니다.
- 메타데이터 `review` 값: `pending`(자동 변환, 원본 대조 전) / `proofread-<검토자>`(원본 이미지 대조 교정 완료).
  `flags` 는 자동 변환이 감지한 확인 필요 사항입니다(의미는 AGENTS.md 참고).

### 정답 표기 규칙

| 상황 | 표기 |
|---|---|
| 단일 정답 | `\answer{3}` |
| 복수 정답(정답 인정 번호 모두) | `\answer{2,5}` + `\answernote{복수 정답(정답표 원문: 2, 5)}` |
| 전원 정답(정답표에 1,2,3,4,5 표기) | `\answerall` + `\answernote{정답표에 1,2,3,4,5 모두 정답으로 표기(전원 정답)}` |
| 정답 미확인 | `\answerunknown` (추정 금지) |

- 기준 자료는 `answers/answers.csv` 입니다(열: round, period, form, subject, number, answer, note, verification, source_file).
  `number` 는 **정답표에 인쇄된 번호**입니다(제20–26회 일부는 과목마다 1–40 으로 다시 시작). 문항과의 연결은
  (회차, 교시, 과목 블록 순서, 순번)으로 하며 `tools/apply_answers.py` 가 이 규칙으로 문항 파일에 반영합니다.
- 최초/최종 정답이 함께 있는 경우 최종 정답을 사용합니다. Q-Net 정답 게시판에는 회차별로 최종 정답 파일
  하나씩만 게시되어 있습니다(제19–25회 파일명은 "정답", 제23회·제26회 이후는 "최종정답/최종 확정답안").
- `verification` 열: `2-reader`(서로 다른 두 판독자의 독립 판독 일치) / `reader+orchestrator`(1인 판독 + 총괄 대조) /
  `disputed->orchestrator-zoom-check`(판독 불일치 → 원본 확대 대조로 확정).

### 그림
- 그래프·도식·단순 도면은 문항 파일 안에 **TikZ/pgfplots** 로 재현합니다(라벨·눈금·선 모양을 원본과 동일하게, 원본 대조 후 `flags` 에 `tikz`).
- 정확한 재현이 어려운 그림만 `figures/NN-k.png` 로 두고 `\qfigure` 로 넣으며, `python tools/optimize_figures.py` 로 용량을 줄입니다. SVG 는 XeLaTeX 에서 직접 쓸 수 없어 사용하지 않습니다.

## 빌드 및 검토

필요: TeX Live 2024 이상(XeLaTeX, kotex, unfonts-core 글꼴 포함), Python 3.10+.

```bash
python tools/build.py                       # 전체 과목·회차 묶음 PDF (build/)
python tools/build.py civil_law/37          # 특정 과목·회차
python tools/build.py --noanswers economics # 정답 숨김
python tools/build.py --single civil_law/37/01.tex   # 문항 하나만
python tools/validate.py --write-status     # 구조 검증 + docs/STATUS.md 갱신
python tools/apply_answers.py --check       # 문항 파일 정답 = answers.csv 확인
```

검토할 때는 `build/` 의 PDF 와 원본 시험지를 나란히 놓고 문항 번호, 문두, 선택지, 표·그림, 정답을 대조합니다.
수정은 브랜치를 만들어 PR 로 올리고, 교정한 파일의 `review=` 값을 갱신합니다(자세한 절차는 AGENTS.md).

## 버전과 변경 이력

- 변경 내용: [CHANGELOG.md](CHANGELOG.md)
- 버전 규칙과 새 회차 추가 절차: [docs/RELEASING.md](docs/RELEASING.md)
  - 새 시험 회차를 추가하면 MINOR 를 올린다.
