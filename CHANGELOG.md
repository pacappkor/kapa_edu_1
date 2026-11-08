# 변경 이력 (CHANGELOG)

이 저장소의 모든 주요 변경을 기록한다.
- 형식: [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/)
- 버전: [유의적 버전](https://semver.org/lang/ko/)
- 버전 규칙과 릴리스 절차: [docs/RELEASING.md](docs/RELEASING.md)

새 변경은 먼저 `[Unreleased]` 에 쌓는다. 릴리스할 때 버전 제목으로 옮긴다.
새 시험 회차를 추가할 때는 `docs/RELEASING.md` 의 "새 회차 항목 템플릿"을 복사해 쓴다.

## [Unreleased]

### 변경
- `tlmgr search --file` 의 정규식 연산자인 `+` 도 실행 명령 대상에서 제외하고, 표준 LaTeX 로더 `RequirePackageWithOptions` 를 토큰 경계를 구분해 인식한다. 옵션 허용·유사 이름 제외와 실제 스타일의 기존 25개 파일 목록을 검증한다.
- 미등록 파일의 `tlmgr search` 실행 명령은 파일명이 `[A-Za-z0-9._-]+` 에 해당할 때만 표시한다. 그 외에는 파일명의 안전한 표현과 제공 패키지 조회 설명만 표시해 셸의 변수·명령 치환을 피한다. 공백·`$HOME`·백틱·괄호·한글 파일명의 회귀 테스트를 추가했다.
- 의존성을 TeX 토큰 단위로 읽어 제어 기호·주석·표시용 명령·옵션의 이스케이프된 중괄호를 구분한다. 누락 파일은 확인된 실제 TeX Live 패키지 설치 명령을, 미등록 파일은 안전한 파일명에 한해 실행 가능한 조회 명령을 안내한다. 실제 스타일의 25개 파일 순서와 오류 하위 테스트의 stderr 초기화를 검증한다.
- 한글 LaTeX 사전 검사가 모든 번들 글꼴(Latin Modern Roman 포함)과 스타일의 직접 패키지 의존성을 실행 시 파싱해 확인한다. 정상 설치는 kpsewhich 일괄 조회 한 번으로 검사하며, 필요하면 파일별 조회로 대체하고 호출당 10초 제한을 유지한다.
- 누락 파일별 TeX Live 설치 안내와 검사 파일 수를 출력하고, README 에 `kotex-utf` 및 전체 설치 해결책을 명시했다. 테스트는 검사 대상 함수를 공유하고 경로 경고 하위 테스트마다 stderr 를 초기화한다.

### 추가
- README 에 KTUG 기반 Windows 한글 LaTeX 환경 설정·경로 규칙·번들 글꼴 확인·문제 해결 안내를 추가했다.
- `tools/build.py` 에 UnBatang·UnDotum·kotex 사전 검사와 경로 경고, `--skip-preflight` 옵션을 추가했다. `python tools/test_build.py` 로 사전 검사 동작을 검증한다.

<!--
### 새 회차             ← 새 시험 문제 추가 (회차별 표: docs/RELEASING.md 템플릿)
### 정정                ← 문항 오탈자·표·그림·정답 정정 (파일, 내용, 근거)
### 추가
### 변경
### 삭제
### 호환성 깨짐         ← 폴더 구조·파일명·메타데이터 형식·LaTeX 매크로 변경
-->

### 정정
- 문서(Markdown)의 범위 표기 `~` 를 "–" 로 바꿨다. GitHub 는 한 줄에 물결표가 두 개 있으면 그 사이를 취소선으로 표시하기 때문이다(예: `제26~29, 35~37회`).
- `tools/validate.py` 가 Markdown 본문(코드 스팬·코드 블록 제외)의 `~` 를 오류로 잡는다.

## [v0.0.0] - 2026-11-08

최초 릴리스. 첫 PR(data/initial-import)이다.

### 새 회차
- 감정평가사 제1차 시험 기출문제 제19회(2008)–제37회(2026)
  - 범위: 3,520문항
  - 과목: 민법, 경제학원론, 부동산학원론, 감정평가관계법규, 회계학, 영어(제19회만 — 제20회부터 공인어학성적으로 대체)
  - 원본: Q-Net 기출문제 게시판(cst00309). 원본(PDF/HWP 페이지 이미지)과 대조 교정을 마쳤다(`review=proofread-*`)
- 최종 정답: 2인 판독 검증을 거친 `answers/answers.csv` 와 문항별 `\answer{}` (전원 정답·복수 정답 포함)

### 추가
- 문항 형식
  - 과목/회차/번호별 LaTeX 조각 파일
  - 공통 스타일 `latex/kapa-exam.sty`
  - 그림: TikZ 재작성(정확히 옮길 수 있는 경우), 나머지는 최적화한 이미지
- 도구 `tools/`
  - 수집: `pipeline/qnet_fetch.py`
  - 변환: kordoc·rhwp 기반 `pipeline/`
  - 원문 텍스트 대조: `pipeline/text_crosscheck.py`
  - 검증·현황표: `validate.py`
  - 빌드: `build.py`
- 문서
  - README, AGENTS, CLAUDE
  - `docs/STATUS.md`, `docs/SOURCES.md`
  - 작업 스킬 `skills/kapa-past-exam`
- 라이선스: 문항·정답 내용은 공공누리 제1유형(출처표시: 한국산업인력공단), 저장소 고유 작업물은 GPL-3.0-only (`NOTICE.md`)

### 검수
- 사람 검수를 대신해 독립 에이전트가 원본 페이지 이미지와 새 조판 PDF 를 문항별로 대조했다(이슈 #6). 기준은 학생이 같은 정보를 읽어낼 수 있는지이며, 표현 차이는 동일로 본다(예: 표시 무늬, 줄바꿈).
  - 표본 101문항: 제32–34회 전 과목 60문항, 직접 전사 8문항, 제23·26·37회 경제학원론 수식 문항 전부(33문항). 검수 모델은 교정에 쓰지 않은 모델이다.
  - 의미가 바뀐 오류는 없었다.
  - 원본에 없는 표시를 바로잡았다:
    - 제33회 감정평가관계법규·회계학의 "않은" 밑줄 18곳을 지웠다.
    - 제32회 경제학원론 60번의 밑줄 범위를 원본대로 고쳤다.
- 조판 정비:
  - 표 앞 문단 구분 98곳: 문두 끝 줄이 가운데 정렬되거나 표가 옆에 붙던 문제를 고쳤다.
  - 페이지 폭을 넘던 줄 5곳을 고쳤다.
  - 가운뎃점 ㆍ/․ 이 쉼표(、)처럼 보이던 문제를 고쳤다.
  - 결과: 전 과목 빌드 88/88, Overfull 5pt 초과 0

[Unreleased]: https://github.com/pacappkor/kapa_edu_1/compare/v0.0.0...HEAD
[v0.0.0]: https://github.com/pacappkor/kapa_edu_1/releases/tag/v0.0.0
