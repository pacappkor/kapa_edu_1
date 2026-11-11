# kapa_edu_1 — 감정평가사 제1차 시험 기출문제 (LaTeX)

[![visitors](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pacappkor/kapa_edu_1/traffic/.traffic/badge-views.json)](https://github.com/pacappkor/kapa_edu_1)
[![clones](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pacappkor/kapa_edu_1/traffic/.traffic/badge-clones.json)](https://github.com/pacappkor/kapa_edu_1)

배지는 GitHub traffic 조회·clone 집계이며, 공개 전환 및 첫 집계 성공 전에는 표시되지 않을 수 있습니다.

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
- **이용 조건**: 제25–37회(2014–2026) 문항·최종 정답은 Q-Net 공지(artlSeq=5259147)에 따른 **공공누리 제1유형(출처표시)** 대상입니다. 제19–24회(2008–2013)는 한국산업인력공단이 Q-Net 에 공개한 공식 기출문제·정답 자료이며, 위 공지의 적용 범위에 포함되지 않습니다. 이 저장소는 해당 기간 자료에 별도의 이용허락을 부여하거나 공공누리 적용을 주장하지 않습니다. 저장소 고유의 변환·조판 코드·도구·문서는 **[GPL-3.0-only](LICENSE)** 입니다. 출처와 범위별 조건은 [`NOTICE.md`](NOTICE.md)를 확인하세요.
- **공개 정책**: 저장소는 관리자 결정에 따라 공개할 수 있습니다. 공개 여부와 관계없이 토큰·비밀번호 등 자격 증명은 절대 커밋하지 않습니다. 취약점 제보는 [`SECURITY.md`](SECURITY.md)를 따릅니다.
- **정확성 안내**: 수록 정답은 Q-Net 공식 최종 정답을 전사한 것이지만, 이 저장소는 공식 배포본이 아니며 변환·전사 오류가 있을 수 있습니다. 별도로 추가하는 해설은 공식 해설이 아니며, 정답 전사와 해설의 정확성을 보증하지 않습니다. 시험지·정답표 원본을 최종 기준으로 확인하세요.
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

## 개발 환경 (한글 LaTeX)

필요: **TeX Live 2024 이상 전체 설치**(XeLaTeX, kotex, unfonts-core 포함), **Python 3.10+**.
컴파일 엔진은 XeLaTeX 입니다.

### Windows 설치

[KTUG Windows TeX Live 안내](https://www.ktug.org/getting-started/windows-texlive/)
(준비·설치·글꼴 문서, 2026-11-08 확인)를 참고하세요.

1. winget 과 터미널을 준비하고, **한글·공백 없는 경로**(예: `C:\work\kapa_edu_1`)에 저장소를 복제합니다.
   폴더명·파일명에도 한글·공백을 피하세요. KTUG 안내에 따르면 프로그램에 따라 이런 경로에서 TeX Live 오류가 날 수 있습니다.
2. [TeX Live ISO (kakao 미러)](https://mirror.kakao.com/CTAN/systems/texlive/Images/texlive.iso)를 내려받아
   `install-tl-windows.bat` 를 실행하고 기본 전체 설치(full scheme)를 선택합니다.
3. 설치 후 TLShell 에서 저장소를 `https://mirror.kakao.com/CTAN/systems/texlive/tlnet` 으로 설정하고
   약 한 달에 한 번 업데이트합니다. Python 은 별도로 설치합니다.

이 저장소는 `kotex` + `fontspec` 과 **UnBatang·UnDotum** 을 사용합니다. 두 글꼴은 TeX Live 의
`unfonts-core` 패키지에 포함되므로 Windows 에 글꼴을 따로 설치할 필요가 없습니다.
UnBatang 에 없는 한자는 TeX Live `baekmuk` 패키지의 **Baekmuk Batang**(`batang.ttf`)으로 대체합니다. 본문 라틴 문자는 TeX Live `lm` 패키지의 **Latin Modern Roman** 입니다.
시스템 글꼴을 쓰려면 fontconfig 에 Windows 글꼴 폴더를 알려 주는 `genlocalconf` 설정이 필요하지만,
이 저장소의 번들 글꼴에는 필요하지 않습니다. KTUG 예제의 oblivoir·Noto 대신 기존 클래스·글꼴을 유지해 조판 결과를 보존합니다.

설치 확인(터미널): 아래 명령은 모든 글꼴과 kotex 를 확인합니다. `tools/build.py` 는 이들에 더해
`latex/kapa-exam.sty` 가 `RequirePackage`·`RequirePackageWithOptions`·`usepackage` 로 직접 로드하는 모든 패키지도 자동으로 검사하고 확인한 파일 수를 출력합니다.

```bash
kpsewhich UnBatang.ttf
kpsewhich UnDotum.ttf
kpsewhich batang.ttf
kpsewhich lmroman10-regular.otf
kpsewhich kotex.sty
xelatex --version
```

- `kotex.sty` 가 없으면 TeX Live 의 [`kotex-utf`](https://ctan.org/pkg/kotex-utf) 를 설치하세요.
  글꼴은 UnBatang·UnDotum → `unfonts-core`, Baekmuk Batang → `baekmuk`, Latin Modern Roman → `lm` 입니다.
  한꺼번에 설치: `tlmgr install kotex-utf unfonts-core baekmuk lm`.
- 다른 패키지가 누락되면 사전 검사가 파일별 실제 TeX Live 패키지 설치 명령을 안내합니다
  (예: `tlmgr install pgf`, `tlmgr install tools`, `tlmgr install graphics`).
  알려지지 않은 파일은 파일명이 `[A-Za-z0-9._-]+` 에 해당할 때만 실행 가능한 조회 명령(예: `tlmgr search --global --file /example.sty`)을 안내합니다.
  `+`·공백·`$HOME`·백틱·괄호·한글 등이 포함된 파일명은 실행 명령 대신 파일명과 `tlmgr search --global --file` 로 제공 패키지를 찾으라는 설명만 표시합니다.
  권장하는 전체 설치(full scheme, `tlmgr install scheme-full`)도 사용할 수 있습니다.
- 글꼴 캐시 문제는 `fc-cache -fv` 로 갱신하세요(TeX Live 의 bin 경로가 PATH 에 있어야 합니다).
- `tools/build.py` 는 컴파일 전에 `kpsewhich` 로 UnBatang·UnDotum·Baekmuk Batang·Latin Modern Roman·kotex 와 스타일의 모든 직접 패키지 의존성을 확인하고,
  저장소 절대 경로의 비 ASCII 문자·공백은 경고합니다. 검사를 생략하려면 `--skip-preflight` 를 사용합니다
  (XeLaTeX 의 PATH 확인은 유지). 사전 검사 테스트: `python tools/test_build.py`.

## 빌드 및 검토

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

## CI

GitHub Actions 는 PR, `main` 푸시, 수동 실행에서 Python 3.12 로 다음을 검사합니다.

- `python tools/validate.py --write-status`: 구조·정답 일치와 Markdown 본문 범위 표기 검사
- 생성한 `docs/STATUS.md` · `docs/status.json` 이 커밋된 내용과 같은지 확인
- `python tools/apply_answers.py --check`: 정답표와 문항 정답 동기화 확인
- `tools/**/test_*.py` 표준 unittest 탐색 및 패키지 구조·요약 기반 완료 확인
- `python -m py_compile tools/build.py`: 빌드 도구의 Python 구문 검사
- PR 기준 커밋과의 `git diff --check`: 변경 줄 공백 오류 검사

한 작업 안에서 변경 경로에 따라 검사를 선택하고 실행 요약에 표시합니다. Markdown 만 바뀌면
본문 검사를 포함한 구조 검증·현황표 확인만 실행하고, 문항·정답 변경은 구조·정답 검사를,
`latex/` 변경은 빌드 도구 구문 검사를 실행합니다. `tools/` · 워크플로·분류 불명 경로 변경,
PR 은 존재하는 기준 SHA, 일반 푸시는 조상인 `before` 를 사용합니다. 강제 푸시는 공통 조상을 사용하되 전체 검사합니다.
수동 실행·기준 누락·공통 조상 없음·변경 조회 실패도 전체 검사합니다. 공백 검사는 같은 기준을 사용하며 기준이 없으면 빈 트리, 수동 실행에 부모가 있으면 `HEAD^`, 부모 없는 HEAD 는 항상 빈 트리와 비교합니다.

외부 시험 자료 다운로드·비밀값·TeX 설치는 사용하지 않습니다. 빌드 도구에는 TeX 없는 생성 모드가 없어
PDF 컴파일·글꼴 검사·원본 대조는 로컬 검토 절차로 남깁니다.

### 표준 테스트 탐색과 위협 모델

저장소 루트에서 `python -I -B tools/ci_tests_supervise.py` 를 실행한다.
감독 실행기는 먼저 `python -I -B tools/ci_layout_check.py` 로 구조만 검사한다.
이 검사는 tools 코드를 import하지 않으며, `tools/**/test_*.py` 파일이 없거나
테스트 파일명이 unittest의 파일명 정규식에 맞지 않으면 실패한다.
패키지 폴더명은 Python 3.12·3.14의 표준 탐색처럼 식별자·예약어 여부를 검사하지 않는다
(`class`, `my-pkg`, `123abc`도 허용).
테스트 폴더에서 `tools/` 까지의 각 폴더에는 `__init__.py` 파일이 있어야 한다.

그다음 저장소 루트에서 다음 **표준 명령을 그대로** 별도 프로세스로 실행한다.

```sh
python -I -B -m unittest discover -s tools -t . -p "test_*.py" -v
```

Python 3.12·3.14에서 `-I` 와 함께 사용해도 unittest의 `-t .` 가 저장소 루트를
검색 경로에 추가하므로 tools 패키지를 탐색한다. 별도 로더, import 도달 관찰자,
import 캐시 조작, 완료 표지 없이 표준 unittest의 import·load_tests·skip 동작을 따른다.
테스트는 패키지 import 또는 테스트 파일 자체의 최소한의 형제 경로 설정을 사용한다.
`-B` 는 바이트코드 생성을 막으며 CI는 `PYTHONDONTWRITEBYTECODE=1` 도 설정한다.

stdout·stderr는 그대로 출력하되 판정에 필요한 경계 이전 stderr만 메모리에 보관한다.
성공하려면 종료 코드가 0이고, 외부 테스트 프로세스 종료 직후 이미 버퍼에 있는 stderr를
비차단으로 수집해 경계를 기록한다. 각 수집은 시작 시 대기 중인 바이트 수로 제한하여
계속 출력하는 하위 프로세스도 잠금을 무한히 점유하지 못하며 종료 후 10초 대기를 지킨다.
경계 이전 stderr의 마지막 `Ran N tests` 요약과 그 직후 비어 있지 않은 줄의 `OK` 또는
`OK (...)` 가 모두 있어야 한다. 이후 하위 프로세스 출력은 표시하되 판정에서는 제외한다.
N은 1 이상이어야 하며, 0이면 OK 줄에
`skipped=K` (K ≥ 1)가 있어야 한다. `os._exit(0)` 같은 우발적 조기 종료로 요약이
없거나, 빈 실행·실패 종료·마지막 OK 누락이면 원인을 표시하고 실패한다.

테스트 파일과 패키지 초기화 코드는 PR에서 검토하는 **신뢰된 코드**이며 임의의 코드를
실행할 수 있다. 이 검사는 패키지 구조와 출력 기반 완료 여부만 확인하는 것이지,
파일별 탐색 도달·모든 테스트의 실행을 증명하거나 샌드박스·악성 테스트 방어를 제공하지 않는다.
신뢰된 load_tests나 result.stop()의 동작도 표준 unittest에 맡긴다.
고의적인 출력 위조나 우회는 CI가 아니라 코드 리뷰에서 차단한다.

## 버전과 변경 이력

- 변경 내용: [CHANGELOG.md](CHANGELOG.md)
- 버전 규칙과 새 회차 추가 절차: [docs/RELEASING.md](docs/RELEASING.md)
  - 새 시험 회차를 추가하면 MINOR 를 올린다.
