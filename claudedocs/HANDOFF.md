# HANDOFF — SNU Connectome Lab 홈페이지 (Transconnectome/lab-homepage)

> 최종 갱신 **2026-09-12 17:40 KST**. 이 문서부터 읽고 시작할 것.
> 정본 = `main` · `/home/juke/git/lab-homepage`. 작업 시 현재 상태는 `git status --short --branch`로 확인한다.
> 읽기 순서: 이 파일 → `claudedocs/design-audit-ai-look_2026-09-11.md` → `docs/research-content-review.md`.
> 공식 홈페이지: https://www.connectomelab.com/ · 영어: https://www.connectomelab.com/en/.

## 0. 현재 상태 ★

**PR #14 머지, A–E 개선안 구현·검증, 공식 홈페이지 배포와 운영 사이트 확인을 완료했다.**

- A 구현: `315ec2c`. 전역 챗 버블을 합류 FAQ로 이관하고 홈 모델명 칩·장식 이모지·BibTeX 컨페티를 제거했다. 레이더·아이디어는 푸터로 옮겼다.
- PR #14: **MERGED**, `2c7402196bf8da9f3518b7b863efbcfc1caf9f33`, 2026-09-12 16:57 KST. 진단 문서만 포함한 PR이며 main에서 바로 읽을 수 있다.
- B–E 구현: `ca2533f93b9368b7487f9787f2065eb867d3817d`. 홈 세 구획, 한·영 문구, 연구 목차와 지도 이관, 연도별 논문, 필터 단순화, 실제 연구 그림과 공유 이미지.
- `npm ci`, `npm test`, `npm run build`, `npm run test:site` 통과. 최종 소스 수정 후 테스트·빌드·사이트 계약을 다시 통과했다. 브라우저 32개 경우와 사진·폰트 보충 검사 통과(§3).
- 구현 배포 [Actions 34683679902](https://github.com/Transconnectome/lab-homepage/actions/runs/34683679902) 성공, 2026-09-12 17:36 KST 완료. 공식 사이트 전체 경로와 이미지·주요 동작 확인 완료(§4).

## 1. 실측 사실

| 항목 | 확인 결과 | 확인 방법 |
|---|---|---|
| 저장소 | public · Transconnectome/lab-homepage | Git remote / GitHub |
| 공식 Pages 등록 | `www.connectomelab.com`, workflow 배포, HTTPS 강제 | `gh api repos/Transconnectome/lab-homepage/pages` 2026-09-12 17:35 KST |
| 도메인 | www는 기존 GitHub Pages 등록 유지. apex는 DNS 미설정이므로 공유 이미지·메타데이터에 www 사용 | 기존 `scripts/cutover.sh --status` 실측 및 Pages API |
| 기준 브랜치 | main 직접 push, force push 금지 | 사용자 승인·원격 규칙 |
| 스택 | Node >=22.12, Astro 7, React 18, Tailwind 3, Python 3.10+ | package.json / .nvmrc |
| 기존 멤버 자산 | 원본 파일 보존, 홈에 현재 구성원 초상 10개 표시 | 컬렉션 선택 + 브라우저 로딩 확인 |

## 2. 이번 사용자 결정과 구현 판단 ★

2026-09-12 사용자: **“나와 있는 모든 작업을 다 완성하고 최종적으로 검증해서 새 홈페이지 등록하고 배포까지 완료해 줘”**.
이 지시로 A만 끝내고 기다리던 범위를 B–E와 운영 배포까지 넓혔다. 앞선 다섯 질문에 별도
답을 받았다고 기록하지 않는다. 사용자에게 다음 가정을 알리고 구현했다.

1. 우선 방문자는 예비 지원자와 연구자다. 연구실 소개·근황·사람·지원 경로를 바로 읽게 한다.
2. 실제 단체·현장 사진은 확보하지 못해 공개 논문의 진짜 연구 그림과 기존 구성원 초상을 사용한다.
3. 레이더·아이디어는 푸터에서 접근하는 공개 실험실 노트로 유지한다. 기계 생성·미검토·비보증 안내는 남긴다.
4. 소개문은 검토한 기존 연구 범위에 근거한 기관 소개다. PI가 직접 썼다고 표시하지 않는다.
5. 소개와 날짜가 있는 소식을 결합한다. 실제 기사 날짜와 서지 연도만 사용한다.

기존 확정 사항: 한국어 `/`, 영어 `/en/`, 옛 `/ko/*` 리다이렉트; 영문 모토 유지; PI 직함 부교수;
네 개 연구축과 언어별 앵커; 종이색·잉크·청록 팔레트와 한국어 타이포; 연구 지도의 개념도 표시.

## 3. 산출물과 검증 ★

| 단계 | 최종 결과 | 주요 파일 |
|---|---|---|
| A | 챗 버블 제거·정적 FAQ, 모델 칩·컨페티 제거, 보조 메뉴 푸터 이관 | JoinFaq, Navbar, Footer, PublicationFilter |
| B | 한·영 소개·제목·지원·문화 문구를 구체적으로 정리. 확인되지 않은 현재 모집·인터뷰·정기 지원 보장 제거 | `src/i18n/ui.ts`, JoinFaq, BaseLayout |
| C | 홈 소개+그림 / 소식 3개+주요 논문 3편 / 구성원 초상 10명+지원. 지도와 프로젝트는 연구 페이지로 이관 | HomePage, ResearchPage, FeaturedProjects |
| D | 연구 4개 세로 목차, 연도별 서지 목록, 네이티브 필터. 본문·저자·초록·출처 보존 | PublicationFilter, MemberGrid, IdeasFilter, ResearchRadarView |
| E | 실제 MBBN 논문 그림 A–C 발췌·출처·라이선스, 기존 초상. 1200×630 공유 이미지·메타데이터. 뉴스 삽화는 접힌 항목에 명시 | `public/assets/site/`, `src/data/siteMedia.ts`, `scripts/og-homepage.html` |

문서 정본:
- `docs/research-content-review.md` §13: 이번 문구·그림의 근거와 해석 범위. 기존 연구 Markdown을 새로 전면 심사했다는 주장은 하지 않는다.
- `public/assets/site/README.md`: 논문·원본 PNG·CC BY 4.0·패널 발췌·해시·공유 이미지 재현 절차.
- `README.md`: 최종 화면 구조, 언어·빌드·자동화·등록 도메인 안내.

### 자동 검사

- 순서: `npm ci && npm test && npm run build && npm run test:site`. 설치 취약점 0, 모든 테스트 통과.
- 최종 소스 수정 후 `npm test && npm run build && npm run test:site` 재실행 성공(2026-09-12 17:31 KST). 사이트 계약은 한·영 16페이지·옛 리다이렉트·메타데이터·내부 링크·앵커·로컬 에셋을 검사한다.
- 연구·구성원·논문 컬렉션 데이터와 3D 연구 의미 데이터는 변경하지 않았다. 뉴스 다섯 파일은 `**` 강조 위치만 바꿔 파싱 표식 노출을 고쳤다.
- 서브에이전트는 파일 단위로 소유권을 분리했다. `src/i18n/ui.ts`는 한 담당자만 편집했다.

### 실제 브라우저 검사

Chromium 프로덕션 preview에서 1440×1000 / 390×844, 한·영 각각 홈·연구·논문·구성원·소식·레이더·아이디어·합류를 검사했다.
`report.json` 기준 **32개 화면·32개 상호작용 묶음 통과, pageerror 0, 가로 넘침 0**.

- 홈 3구획·소식/논문 3개씩·초상 링크·실제 언어 전환·모바일 메뉴 Enter/Space.
- 연구 목차 4개·분야별 앵커·연구 지도의 활성화 후 키보드 선택과 해당 연구 이동·프로젝트 생성 출처 펼침.
- 논문 검색·연도·주제·유형, `?type=` 진입/새로고침, 프리프린트 포함/제외.
- 실제 클립보드에서 저널 `@article`, 학회 `@inproceedings`, 프리프린트 `@unpublished` 확인. 권한 실패를 주입해 “복사 실패” 안내도 검증. 컨페티 canvas 없음.
- 구성원 카테고리 선택과 전체 복귀, 레이더 검색·주제·요약 Enter/Space, 아이디어 필터와 본문 앞 미검토 안내.
- 합류 FAQ 7개 기본 접힘·키보드 조작·전체 확장 후 가로 넘침 없음.
- 사진 보충 검사: 양 언어·두 화면에서 초상 10개의 `complete && naturalWidth > 0` 확인 후 다시 캡처.
- CDP `CSS.getPlatformFontsForNode`: 한글 제목의 실제 MaruBuri 렌더 확인. 뉴스 양 언어에서 노출된 `**` 0. 공유 이미지 HTML 재현 성공.

독립 검토 지적을 반영했다: 행사 설명 범위 축소, 부정확한 논문 월 정렬 제거, 그림 A–C 전체가 보이는 프레임,
뉴스 강조 표식 수정. 다른 담당자가 데스크톱과 모바일 캡처를 실제로 보고 배포를 막는 겹침·잘림을 찾지 못했다.

로컬 증거(임시 파일, Git에는 넣지 않음):
- `/tmp/lab-homepage-final-review/report.json`, `assets-report.json`, 각 페이지 PNG. 초상은 `*-home-people-loaded.png`, 전체 홈은 `*-home-full-loaded.png`를 본다.
- 재현: `/tmp/lab-homepage-final-browser.py`, `/tmp/lab-homepage-final-assets.py`.
- 집계: `python3 -c 'import json; r=json.load(open("/tmp/lab-homepage-final-review/report.json")); print(len(r["pages"]), len(r["interactions"]), r["errors"])'`.
- 이전 A단계 검수는 `/tmp/lab-homepage-phase-a-review/`와 Git의 과거 HANDOFF에 남아 있다.

## 4. 배포 실측 ★

구현 push: `ca2533f93b9368b7487f9787f2065eb867d3817d` → `origin/main`.
사용자 승인 범위에서 기존 GitHub Pages workflow를 이용했다. 새 도메인 구매나 DNS 변경은 하지 않았다.

- [Actions 34683679902](https://github.com/Transconnectome/lab-homepage/actions/runs/34683679902): `headSha=ca2533f93b9368b7487f9787f2065eb867d3817d`, **success**, 2026-09-12 17:36:34 KST 배포 완료.
- CI에서도 `npm ci → npm test → npm run build → npm run test:site`를 모두 통과한 산출물을 배포했다.
- 운영 `/`, `/research`, `/publications`, `/team`, `/news`, `/radar`, `/ideas`, `/join` 및 영어 대응 경로: **16개 HTTPS 200**, 공식 canonical·새 OG·주 메뉴·푸터 확인.
- 실제 연구 그림과 새 OG 파일의 운영 SHA-256이 커밋한 로컬 파일과 일치한다.
- 운영 브라우저 두 크기·두 언어: 홈 3구획, 초상 10개 로딩, 실제 언어 전환, 논문 `?type=journal` 진입, FAQ 7개 확인. 가로 넘침·pageerror 없음.
- 운영 증거: `/tmp/lab-homepage-live-review/report.json`, `*-home-full.png`; 재현 `/tmp/lab-homepage-live-check.py`. 임시 로컬 파일이다.
- 이 HANDOFF는 구현 배포 이후 결과를 기록한 문서 커밋이다. 문서 커밋 자체의 SHA와 후속 workflow 상태는 `git log`와 `gh run list`로 확인한다.

## 5. 이후 운영

A–E 디자인 개편의 구현은 끝났다. 새 세션에서 재구현하거나 PR #14를 다시 머지하지 않는다.
현재 상태와 배포는 `git status --short --branch`, `git log --oneline -5`, `gh run list --workflow deploy.yml --limit 3`으로 확인한다.

연구실 명부·현재 모집·현재 소속의 변경은 운영자가 확인한 새 자료가 생길 때 갱신한다. 실제 단체·작업 현장
사진을 받으면 출처를 확인하고 현재 연구 그림을 대체할 수 있다. 구성원 한국어 학력/관심/passions와 레이더
본문은 원본 공급 언어를 유지한다. 공식 연구축 명칭과 과학적 결론을 디자인 작업에서 임의 변경하지 않는다.

## 6. 함정 (실측된 것만) ★

### 사실 관계
- MBBN 은 Communications Biology 기록 하나만. 제목이 다른 arXiv 프리프린트는 `scripts/sync_scholar.py` 수동 병합 규칙으로 제외됨.
- NeuroMamba 와 DIVER-0 는 **워크숍 논문**(구성원 하이라이트 포함). BK 수상 주장은 근거 없어 삭제됨 — 되살리지 말 것.
- 4개 연구 영역은 영/한 항목이 반드시 짝을 이룬다(`npm test` 의 content contract 가 검사).
- `/ko/*` 레거시 라우트는 리다이렉트. "중복 페이지"라며 지우지 말 것.
- History 라우트는 소스는 있으나 의도적으로 비공개.
- 합류 페이지 FAQ는 정적 수동 답변이다. 제거된 챗 위젯을 되살리지 말 것. Ideas는 기계 생성·비보증 표기를 유지한다(위치는 바꿔도 됨 — 진단 문서 §4-4).
- 손으로 검토한 연구 산문은 생성기가 절대 덮어쓰지 않는다. 논문 갱신은 큐레이션된 기존 레코드를 보존한다.
- 뉴스 링크는 HTTP(S)만, 생성 본문은 plain text 로 이스케이프.

### 도구
- 홈페이지 논문 `month`는 영문 월 이름과 미기재가 섞인다. `Number(month)`로 최신순을 만들지 않는다. 홈은 연도 내림차순·제목순으로 세 편을 선정하고 주요 논문으로 표시한다.
- 뉴스의 `**“제목”**가`, `**학회(CCN 2026)**에서`는 CommonMark에서 별표가 노출될 수 있다. 따옴표·괄호는 강조 밖에 두고 빌드된 본문을 확인한다.
- `loading="lazy"` 사진은 스크롤 직후 캡처하면 빈 자리로 찍힌다. `complete && naturalWidth > 0`을 기다린 뒤 육안 확인한다. CSS 숨김으로 오진하지 않는다.
- preview를 대상으로 브라우저 검사하는 동안 `dist/`를 재빌드하면 일시적인 404가 생긴다. 최종 빌드가 끝난 고정 트리로 검사한다.
- ⚠️ **같은 파일 병렬 편집 = 조용한 데이터 손실**. 병렬 스트림이 같은 설정 파일을 동시에 Edit 하면 한쪽이 사라지고 검증 단계에서만 드러남. 파일 단위로 소유자를 나눌 것.
- `GITHUB_TOKEN` push 는 deploy.yml 을 트리거하지 않는다. 그래서 research-radar.yml 은 자체 워크플로 안에서 빌드 검증 후 직접 배포한다.
- push 가 Actions run 을 만들지 않는 증상(2026-08-22 겪음): 워크플로 disable/enable 로는 안 풀림. **저장소 Actions permissions 를 enabled=false→true 로 토글**하면 즉시 복구.
- 한글 폰트 진단은 CDP `CSS.getPlatformFontsForNode` 만 믿을 것. getComputedStyle·document.fonts.check 는 거짓양성. 한글을 라틴 모노스페이스로 보내면 Noto Sans Mono CJK **JP** 로 렌더된다.
- 한글 `word-break: keep-all` + `overflow-wrap` 전역 유지. 한글에 라틴 자간 금지. MaruBuri 서브셋과 LICENSE 는 같이 움직인다.
- Playwright 는 ARM64 라 `--executable-path /home/juke/.cache/ms-playwright/chromium-1217/chrome-linux/chrome` 필수.
- Astro 7 preview 는 관리형 백그라운드 서버. 끝나면 `npm exec astro preview stop`.
- bash: `curl … | grep -q` + `set -o pipefail` 은 매치해도 실패로 판정(SIGPIPE). 버퍼링 후 `[[ "$s" == *pat* ]]`.
- CommonMark: `**볼드(병기)**조사` 는 파싱 실패 → 괄호를 볼드 밖으로.
- 폰트 용량은 콜드 캐시 단일 페이지로 잰다. 세션 누적 측정은 캐시 때문에 심하게 과소집계.
- 헤드리스 `claude -p`·cron·trinity 는 `env -u ANTHROPIC_API_KEY` 필요(셸 키가 비활성 org 소속).

## 7. 운영 참조 (2026-09-09 통합 시점 기준, 2026-09-12 실측으로 유효 확인)

**실행·검증**
```bash
npm ci
npm test            # radar buckets · ideas pipeline · news-from-issue · content contract
npm run build
npm run test:site   # 빌드 결과 16페이지·리다이렉트·메타·링크·에셋
npm run preview -- --host 127.0.0.1
npm audit --omit=dev
```
main 룰셋: 삭제·non-fast-forward 차단. secret scanning·push protection·취약점 알림 켜짐, 자동 의존성 PR 은 꺼짐.

**라우팅·구조**
- 한국어 `/`, 영어 `/en/`. 얇은 라우트 래퍼 → `src/components/pages/` 공유 컴포넌트.
- 콘텐츠 스키마 `src/content.config.ts`, glob 로더 `src/content/`. 마크다운은 render(entry). 컬렉션 ID = 파일명.
- 연구 앵커 ID: 한국어 baseSlug, 영어 entry.id. 내부 링크는 localePath().

**자동화**

| 워크플로 | 동작 |
|---|---|
| `.github/workflows/deploy.yml` | main push/수동: 최신 main 체크아웃 → 설치 → 오프라인 테스트 → 빌드 → 생성 라우트 검사 → 배포 |
| `.github/workflows/check.yml` | PR/수동에 같은 검사, 배포 없음 |
| `.github/workflows/research-radar.yml` | 주간/수동: publications·trends·ideas·project metadata 만 생성 → 로컬 커밋 → rebase → 최종 트리 검증 → push → 그 산출물 배포 |
| `.github/workflows/news-submission.yml` | 뉴스 이슈 → 이스케이프된 영/한 마크다운 초안 → Actions 아티팩트(30일). 사이트 쓰기·배포 없음. 관리자가 사실 검증 후 `src/content/news` 에 복사 |

Pages 쓰기 워크플로는 concurrency group `pages` 공유. 생성기는 OPENROUTER_API_KEY 가 있을 때만 LLM 사용(뉴스는 필수, 레이더는 초록 발췌로 폴백, 아이디어는 미생성).

**브라우저 검수**: 레이아웃·런타임 변경 후 1440×1000 / 390×844. 언어 전환, 연구 지도 링크, 구성원·논문 필터·BibTeX 실제 복사, 합류 FAQ, 연구 페이지의 프로젝트 모델 출처 펼침, 레이더 요약의 키보드 Enter/Space.

## 8. 관련 메모리

- `/home/juke/.claude/projects/-home-juke-git/memory/lab_homepage_redesign_project.md` — 8/21~8/22 개편 이력(사진 추출 기법, DNS 컷오버, 이관 후 Actions 복구, 타이포 교훈). 2026-09-12 "남은 일" 갱신.
- `/home/juke/.claude/projects/-home-juke-git/memory/feedback_workflow_shared_file_race.md` — 병렬 편집 데이터 손실 함정 원본.
