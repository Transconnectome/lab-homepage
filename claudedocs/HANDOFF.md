# HANDOFF — SNU Connectome Lab 홈페이지 (Transconnectome/lab-homepage)

> 최종 갱신 **2026-09-12**. 이 문서부터 읽고 시작할 것.
> 🔴 정본 = `main` · `/home/juke/git/lab-homepage`. 워크트리는 하나뿐 (`git worktree list` 로 확인).
> 읽기 순서: 이 파일 → PR #14 진단 문서 `claudedocs/design-audit-ai-look_2026-09-11.md` (main 에는 아직 없음, PR 브랜치에만 있음) → `docs/research-content-review.md` (연구 콘텐츠 출처 결정 정본).
> 라이브: https://www.connectomelab.com/ (GitHub Pages, HTTPS 강제).

## 0. 한 줄 상태 ★

**사이트는 정상 배포 중이고 저장소는 깨끗하다. 열린 일은 하나 — PR #14 "AI가 만든 티" 진단 문서의 방향을 실제 코드로 구현하라는 사용자 지시(2026-09-12)가 착수 전에 중단됐다.**

- ✅ `main` == `origin/main` @ `4750d30`, 미커밋 0, 워크트리 1개 (2026-09-12 16:31 KST `/home/juke/.claude/skills/handoff-doc/scripts/snapshot.sh` 실측)
- ✅ HTTPS 인증서 발급·강제 완료 — `./scripts/cutover.sh --status` 2026-09-12 16:32 KST: "serving this build over a valid certificate"
- ✅ 마지막 배포 성공: Deploy to GitHub Pages, main, 2026-09-10 14:13 UTC (`gh run list` 실측)
- 🔴 PR #14 OPEN (브랜치 `claude/homepage-ai-design-refresh-wnqf3e`, 커밋 fe6fdc1, 문서 1파일 +161줄, 코드 변경 0, check.yml 통과) — 머지 여부는 사용자 결정
- 🔴 구현 미착수. 2026-09-12 세션은 PR 문서를 읽은 직후 사용자가 중단시키고 인계·커밋·푸시만 요청함. 이 세션의 코드 변경 0
- 🔴 구현 착수 전 결정 질문 5개(진단 문서 §6)에 답이 없음 — 사람 몫. 단 A단계는 결정 없이 가능(§4 ②)

## 1. 사실 표

| 항목 | 값 | 출처 |
|---|---|---|
| 저장소 | Transconnectome/lab-homepage (public) | `git remote -v` |
| 라이브 도메인 | www.connectomelab.com · DNS = GitHub Pages A 레코드 4개, CNAME 없음, apex 미설정 | `./scripts/cutover.sh --status` 2026-09-12 |
| 열린 PR | #14 만 (2026-09-12 16:31 KST `gh pr list`) | GitHub |
| 원격 브랜치 | `main`, `claude/homepage-ai-design-refresh-wnqf3e` 두 개뿐 | `git branch -r` |
| 스택 | Node 22 (>=22.12), Python 3.10+, Astro 7, React 18, Tailwind 3 (PostCSS) | package.json |
| 구성원 사진 | `public/assets/members/` 32파일 | `ls | wc -l` 2026-09-12 |

## 2. 사용자 지시·결정 (축자)

- **2026-09-12** 사용자: "https://github.com/Transconnectome/lab-homepage/pull/14 이거 작업해. 오빠 그 플러그 이용하고 병렬 서버에이전트 최대한 많이 이용해서 빠르게 작업해 봐" → 직후 "Git commit push and hand off doc generate" 로 중단. 즉 **PR #14 의 개선 방향을 병렬 서브에이전트로 구현**하라는 뜻이며, 구현은 아직 시작하지 않았다.
- **2026-09-10** 사용자 확인: 이 저장소는 main 에 직접 push 하는 것이 관행 (feature 브랜치 원칙보다 우선).
- **2026-09-09** 통합 결정: 유지 브랜치는 main 하나. 대안 분할형 연구 페이지 설계는 채택하지 않음. 연구 구조는 4개 이중언어 영역(Neuro-X 에 fMRI·EEG 파운데이션 모델 포함).
- **2026-08-22** 확정: 한국어가 루트(`/`), 영어는 `/en/`, 옛 `/ko/*` 는 리다이렉트로 유지. 모토 "Everything Connects to Everything Else"(양쪽 언어 모두 영문).
- **2026-08-21** 확정: PI 직함 **부교수**. Lab Guide 는 정적 FAQ 이지 온라인 모델이 아님. AI Ideas 는 "기계 생성 · 연구실 비보증" 표기 유지.
- 진단 문서 §3 "유지할 것"(2026-09-11 작성, 사용자 반박 없음): 종이색+잉크+청록 팔레트, 마루부리/Hahmlet/프리텐다드/Plex Mono 타이포와 `:lang(ko)` 규칙, 언어 라우팅, 구성원 사진·passions, 3D 연구 지도(위치만 낮춤), 접근성 작업.

## 3. 산출물 지도 · 인벤토리 ★

| 파일 | 내용 | 상태 |
|---|---|---|
| `claudedocs/HANDOFF.md` | 이 문서 | 정본 · 2026-09-12 |
| `claudedocs/design-audit-ai-look_2026-09-11.md` | "AI가 만든 티" 진단 + A~E 단계 + 결정 질문 5개 | 정본(방향) · PR #14 브랜치 fe6fdc1 · main 에는 아직 없음 |
| `docs/research-content-review.md` | 연구 콘텐츠 과학적 출처·리뷰 이력 | 정본 · 2026-09-10 갱신 |
| `claudedocs/homepage_evaluation_and_plan_2026-08-21.md` | 8/21 초기 평가·계획 | 🔴 stale — 9/9 통합·연구 페이지 개편 이전 기준. 이력 참고용 |
| `src/i18n/ui.ts` | 전 UI 문구(영/한) | 정본 · B단계 재작성 대상. 실측 2026-09-12: `rg -o '—'` 32건, `rg -o '→'` 10건 |
| `src/components/ai/AskLabAI.tsx` + `src/layouts/BaseLayout.astro` | 우하단 챗 버블(정적 FAQ 7개) | A단계 제거 대상 |
| `src/components/pages/` | 언어 인식 공유 페이지 컴포넌트(얇은 라우트 래퍼가 호출) | 정본 · C/D단계 대상 |
| `scripts/cutover.sh` | DNS·HTTPS 상태 점검 | 정본 · `--status` 만 쓸 것 |
| `scripts/sync_scholar.py` | OpenAlex 동기화(v3, kind 분류, 멤버 allowlist) | 정본 |
| `/home/juke/.claude/projects/-home-juke-git/memory/lab_homepage_redesign_project.md` | Claude 자동 메모리 | 2026-09-12 "남은 일" 갱신됨 |
| `dist/` | 빌드 출력(2026-09-10) | gitignore · 신뢰하지 말고 재빌드 |

이번 세션(2026-09-12) 산출물: 이 문서 1건. 그 외 파일 변경 없음 — "내 것 아님" 목록도 없음(워킹트리 깨끗).

## 4. 🔴 지금 막혀 있는 것 · 결정 대기 ★

### ① PR #14 머지 여부 — 사람(사용자)
문서 1개 추가뿐이라 머지 위험 없음. 머지하면 진단 문서가 main 에 들어와 다음 세션이 `git show` 없이 읽을 수 있다. 머지 안 해도 `git show origin/claude/homepage-ai-design-refresh-wnqf3e:claudedocs/design-audit-ai-look_2026-09-11.md` 로 읽힌다.

### ② 구현 방향 결정 질문 5개 — 사람(PI)
진단 문서 §6: (1) 첫 방문자 한 사람은 누구인가 (2) 이 연구실만의 이미지 한 장은 무엇인가 (3) 레이더·아이디어는 대외용인가 내부 도구인가 (4) PI 가 200자 소개를 직접 쓸 수 있는가 (5) 브로셔인가 날짜 찍힌 게시판인가.
**결정 없이 가능한 것(A단계)**: 챗 버블 제거→FAQ 를 합류 페이지로 이관, 홈 모델명 칩·이모지·컨페티 제거, 레이더/아이디어를 주 메뉴에서 푸터/소식 하단으로 강등. 문서가 "코드만으로 가능, 반나절"이라 명시.
**결정이 필요한 것**: B(문구 전면 재작성, PI 소개문 필요), C(홈 3막 재구성, 카드→목록), D(필터 UI 단순화), E(사진).

### ③ 사진 자료(E단계) — 사람
단체사진(홍천 리트릿), EEG 아트 전시, 실제 연구 그림. 사용자가 주기 전까지 회색 박스 자리를 두지 말고 사진 없는 레이아웃으로 만든다(문서 §4-5).

## 5. 다음 단계 ★

1. **사용자에게 두 가지 확인**: PR #14 머지할지 · §6 질문 중 (3) 레이더/아이디어 용도와 (4) PI 소개문 가능 여부. 답이 없으면 A단계부터 진행해도 된다(2026-09-12 지시가 이미 "작업해"이므로).
2. **A단계 구현 — 병렬 서브에이전트로, 파일 단위 분할**. 같은 파일을 두 에이전트가 동시에 고치면 조용히 데이터가 손실된다(실측 함정, §6). `src/i18n/ui.ts` 는 **한 에이전트만** 담당. 분할 예: (a) AskLabAI 제거 + FAQ 이관(합류 페이지) (b) 홈 모델명 칩·이모지 제거 (c) 논문 컨페티 제거 (d) 네비 강등(헤더/푸터). 코드 위치는 `rg -n 'AskLabAI|confetti|nav.radar|nav.ideas|🤖' src` 로 잡는다.
3. **검증**: `npm ci && npm test && npm run build && npm run test:site`, 그다음 1440×1000 / 390×844 스크린샷 육안 검수(언어 전환, 연구 지도 링크, 구성원·논문 필터, 레이더 Enter/Space). 빌드 검사는 16개 정식 페이지·/ko 리다이렉트·hreflang·내부 링크·로컬 에셋을 본다.
4. main 에 push → deploy.yml 자동 배포. push 전 `git diff` 검토, 명시적 경로만 stage, force-push 금지, origin/main 이 앞서면 통합 후 테스트·빌드 재실행.
5. **B단계**: PI 소개문 수령 후 `src/i18n/ui.ts` 와 페이지 헤더 재작성(줄표·화살표·수사적 질문·"X부터 Y까지"·대구법 제거, 구체 명사·숫자·연도로). 진단 문서 §4-3 표가 초안.
6. C/D/E 는 A·B 결과를 보고 사용자와 결정.
7. 잔여 콘텐츠 결정(2026-09-09 이월, 사람 몫): 구성원 신분·소속 날짜를 연구실 명부와 대조 · 한국어 구성원 학력/관심/passions 와 레이더 본문 번역 공급 · 유전체/멀티오믹스 축 공식 명칭과 현재 모집 여부 확인 · Communications Medicine 조기공개 논문의 Version of Record 재확인.

## 6. 함정 (실측된 것만) ★

### 사실 관계
- MBBN 은 Communications Biology 기록 하나만. 제목이 다른 arXiv 프리프린트는 `scripts/sync_scholar.py` 수동 병합 규칙으로 제외됨.
- NeuroMamba 와 DIVER-0 는 **워크숍 논문**(구성원 하이라이트 포함). BK 수상 주장은 근거 없어 삭제됨 — 되살리지 말 것.
- 4개 연구 영역은 영/한 항목이 반드시 짝을 이룬다(`npm test` 의 content contract 가 검사).
- `/ko/*` 레거시 라우트는 리다이렉트. "중복 페이지"라며 지우지 말 것.
- History 라우트는 소스는 있으나 의도적으로 비공개.
- Lab Guide 는 정적 FAQ 다. "실시간 AI" 로 표기하지 말 것. Ideas 는 기계 생성·비보증 표기 유지(위치는 바꿔도 됨 — 진단 문서 §4-4).
- 손으로 검토한 연구 산문은 생성기가 절대 덮어쓰지 않는다. 논문 갱신은 큐레이션된 기존 레코드를 보존한다.
- 뉴스 링크는 HTTP(S)만, 생성 본문은 plain text 로 이스케이프.

### 도구
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

**브라우저 검수**: 레이아웃·런타임 변경 후 1440×1000 / 390×844. 언어 전환, 연구 지도 링크, 구성원·논문 필터, Lab Guide, 레이더 요약의 키보드 Enter/Space.

## 8. 관련 메모리

- `/home/juke/.claude/projects/-home-juke-git/memory/lab_homepage_redesign_project.md` — 8/21~8/22 개편 이력(사진 추출 기법, DNS 컷오버, 이관 후 Actions 복구, 타이포 교훈). 2026-09-12 "남은 일" 갱신.
- `/home/juke/.claude/projects/-home-juke-git/memory/feedback_workflow_shared_file_race.md` — 병렬 편집 데이터 손실 함정 원본.
