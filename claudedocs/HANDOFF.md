# HANDOFF — SNU Connectome Lab 홈페이지 (Transconnectome/lab-homepage)

> 최종 갱신 **2026-09-12 16:58 KST**. 이 문서부터 읽고 시작할 것.
> 🔴 정본 = `main` · `/home/juke/git/lab-homepage`. 워크트리는 하나뿐 (`git worktree list` 로 확인).
> 읽기 순서: 이 파일 → PR #14 진단 문서 `claudedocs/design-audit-ai-look_2026-09-11.md` (PR #14 머지 완료, main에서 바로 읽을 수 있음) → `docs/research-content-review.md` (연구 콘텐츠 출처 결정 정본).
> 라이브: https://www.connectomelab.com/ (GitHub Pages, HTTPS 강제).

## 0. 한 줄 상태 ★

**PR #14 진단의 A단계를 구현·검증하고 main에 push했다. B~E단계는 PI의 방향 결정과 소재를 기다린다.**

- 구현 커밋: `315ec2c` — 전역 챗 버블 제거, FAQ 합류 페이지 이관, 홈 모델명 칩·장식 이모지·BibTeX 컨페티 제거, 레이더/아이디어 푸터 이관.
- PR #14 머지 후 `git fetch origin`과 `git merge --ff-only origin/main`으로 로컬 main을 `2c74021`까지 동기화했다(2026-09-12 16:57 KST). 이 인계 갱신은 그 뒤의 문서 커밋이다.
- `npm ci`, `npm test`, `npm run build`, `npm run test:site` 통과. 1440×1000 / 390×844 한·영 브라우저 검증과 스크린샷 육안 검수 완료(§3).
- 구현 자동 배포: [Actions 34681840345](https://github.com/Transconnectome/lab-homepage/actions/runs/34681840345) **성공**, 2026-09-12 16:53 KST 완료. 배포 작업의 `headSha`는 `315ec2c`다. 라이브 `/`, `/en/`, `/join`, `/en/join`, `/ideas`, `/en/ideas`의 HTTPS 200·주 메뉴·FAQ·출처도 직접 확인했다.
- PR #14는 **MERGED**. 사용자의 “머지해라” 승인에 따라 2026-09-12 16:57 KST 머지했다. 머지 커밋 `2c7402196bf8da9f3518b7b863efbcfc1caf9f33`, 변경은 진단 문서 한 파일뿐이다. A단계 구현 코드는 그대로 보존했다.
- 진단 §6의 PI 결정 질문 다섯 개를 전달했으며 아직 답변·이미지·소개문을 받지 않았다. B~E 구현 미착수.

## 1. 사실 표

| 항목 | 값 | 출처 |
|---|---|---|
| 저장소 | Transconnectome/lab-homepage (public) | `git remote -v` |
| 라이브 도메인 | www.connectomelab.com · DNS = GitHub Pages A 레코드 4개, CNAME 없음, apex 미설정 | `./scripts/cutover.sh --status` 2026-09-12 |
| 열린 PR | 없음 (2026-09-12 16:58 KST `gh pr list --state open`) | GitHub |
| 원격 브랜치 | `main`, `claude/homepage-ai-design-refresh-wnqf3e`, `claude/homepage-korean-font-check-dz4neo` | `git fetch origin` 후 `git branch -r`, 2026-09-12 16:52 KST |
| 스택 | Node 22 (>=22.12), Python 3.10+, Astro 7, React 18, Tailwind 3 (PostCSS) | package.json |
| 구성원 사진 | `public/assets/members/` 32파일 | `ls | wc -l` 2026-09-12 |

## 2. 사용자 지시·결정 (축자)

- **2026-09-12** 사용자: "https://github.com/Transconnectome/lab-homepage/pull/14 이거 작업해. 오빠 그 플러그 이용하고 병렬 서버에이전트 최대한 많이 이용해서 빠르게 작업해 봐" → 직후 "Git commit push and hand off doc generate" 로 중단. 이것은 직전 세션의 미착수 기록이다. **이번 재개 세션에서는 A단계 구현·검증·main push를 명시적으로 지시받아 완료했다.**
- **2026-09-10** 사용자 확인: 이 저장소는 main 에 직접 push 하는 것이 관행 (feature 브랜치 원칙보다 우선).
- **2026-09-09** 통합 결정: 유지 브랜치는 main 하나. 대안 분할형 연구 페이지 설계는 채택하지 않음. 연구 구조는 4개 이중언어 영역(Neuro-X 에 fMRI·EEG 파운데이션 모델 포함).
- **2026-08-22** 확정: 한국어가 루트(`/`), 영어는 `/en/`, 옛 `/ko/*` 는 리다이렉트로 유지. 모토 "Everything Connects to Everything Else"(양쪽 언어 모두 영문).
- **2026-08-21** 확정: PI 직함 **부교수**. Lab Guide 는 정적 FAQ 이지 온라인 모델이 아님. AI Ideas 는 "기계 생성 · 연구실 비보증" 표기 유지.
- 진단 문서 §3 "유지할 것"(2026-09-11 작성, 사용자 반박 없음): 종이색+잉크+청록 팔레트, 마루부리/Hahmlet/프리텐다드/Plex Mono 타이포와 `:lang(ko)` 규칙, 언어 라우팅, 구성원 사진·passions, 3D 연구 지도(위치만 낮춤), 접근성 작업.

## 3. 산출물 지도 · 인벤토리 ★

| 파일 | 내용 | 상태 |
|---|---|---|
| `claudedocs/HANDOFF.md` | 이 문서 | 정본 · 2026-09-12 |
| `claudedocs/design-audit-ai-look_2026-09-11.md` | "AI가 만든 티" 진단 + A~E 단계 + 결정 질문 5개 | 정본(방향) · PR #14 머지 완료 · main의 `2c74021`에 포함 |
| `docs/research-content-review.md` | 연구 콘텐츠 과학적 출처·리뷰 이력 | 정본 · 2026-09-10 갱신 |
| `claudedocs/homepage_evaluation_and_plan_2026-08-21.md` | 8/21 초기 평가·계획 | 🔴 stale — 9/9 통합·연구 페이지 개편 이전 기준. 이력 참고용 |
| `src/i18n/ui.ts` | 전 UI 문구(영/한) | 정본 · B단계 재작성 대상. 실측 2026-09-12: `rg -o '—'` 32건, `rg -o '→'` 10건 |
| `src/components/common/JoinFaq.astro` + `src/components/pages/JoinPage.astro` | 한·영 FAQ, native details/summary | A단계 이관 완료. AskLabAI 삭제, BaseLayout의 전역 island 제거 |
| `src/components/pages/` | 언어 인식 공유 페이지 컴포넌트(얇은 라우트 래퍼가 호출) | 정본 · C/D단계 대상 |
| `scripts/cutover.sh` | DNS·HTTPS 상태 점검 | 정본 · `--status` 만 쓸 것 |
| `scripts/sync_scholar.py` | OpenAlex 동기화(v3, kind 분류, 멤버 allowlist) | 정본 |
| `/home/juke/.claude/projects/-home-juke-git/memory/lab_homepage_redesign_project.md` | Claude 자동 메모리 | 2026-09-12 "남은 일" 갱신됨 |
| `dist/` | A단계 빌드 출력(2026-09-12 16:47 KST) | gitignore · 변경 후에는 재빌드 |

### A단계 구현과 검증 (2026-09-12)

- `JoinFaq.astro`: 기존 일곱 FAQ의 양쪽 언어 답변을 옮겼다. `219d42d:src/components/ai/AskLabAI.tsx`의 답변과 대조하여 장식 이모지 외에는 일치함을 확인했다. 과학적 주장을 새로 검증하거나 재작성한 작업은 아니다. 최초 진입 시 모두 접혀 있고, Enter/Space로 열린다. Astro가 본문을 이스케이프하며 클라이언트 JS가 필요 없다.
- `Navbar.astro` / `Footer.astro`: 주 메뉴는 연구·논문·구성원·소식, 별도 합류 링크. 레이더와 아이디어는 푸터의 **실험실 노트 / Lab notes**에 있다. 한·영 경로와 현재 페이지 표시를 보존했다.
- `FeaturedProjects.astro`: 홈의 로봇·모델명 칩을 없앴다. 작은 “AI가 생성한 요약”을 펼치면 정확한 모델명을 확인한다. **모델명은 기본 화면에서 숨겨졌으며 HTML·데이터에서 삭제된 것은 아니다.**
- `IdeasFilter.tsx`: 정확한 생성 모델은 카드 하단 작은 회색 글씨로 이관, 이미지 생성 출처의 이모지 제거. 기존 기계 생성·연구실 비보증 안내는 유지했다.
- `PublicationFilter.tsx`: 컨페티와 Spotlight 장식 이모지 제거. BibTeX 내용과 복사됨 피드백은 유지했다. `package.json`·잠금 파일에서 `canvas-confetti` 및 타입 패키지도 제거했다.
- `src/i18n/ui.ts`는 한 에이전트만 편집했다. FAQ·홈·메뉴는 파일 소유자를 나눠 병렬 구현했고, 다른 담당자가 FAQ/홈/의존성 변경을 독립 리뷰하여 **Proceed**로 판정했다.
- 실행: `npm ci` → `npm test` → `npm run build` → `npm run test:site` 모두 성공. 설치 감사 결과 취약점 0. 빌드 계약은 한·영 정식 페이지, 레거시 리다이렉트, 메타데이터, 내부 링크·앵커·로컬 에셋을 통과했다.
- 브라우저: 로컬 프로덕션 preview를 1440×1000 / 390×844로 검사했다. `/`, `/research`, `/publications`, `/team`, `/news`, `/radar`, `/ideas`, `/join`과 영어 대응 경로를 모두 확인했다. 한·영 × 두 크기 × 여덟 경로 = 32개 화면, 가로 넘침 없음, pageerror 없음.
- 상호작용: 실제 언어 전환·연구 지도 링크, 모바일 메뉴, 구성원 필터, 논문 검색·게재유형, **실제 클립보드의 BibTeX**와 컨페티 canvas 없음, FAQ·레이더·모델 출처의 Enter/Space, FAQ 전체 확장 후 모바일 넘침 없음까지 확인했다.
- 스크린샷은 별도 에이전트와 메인 에이전트가 육안 확인했다. A단계 회귀로 볼 잘림·겹침을 찾지 못했다. 기존 한글 레이더의 영어 본문·구성원 영어 학력은 이번 범위에서 유지했다.
- 로컬 검수 증거: `/tmp/lab-homepage-phase-a-review/`의 PNG와 `report.json`; 재현 스크립트 `/tmp/lab-homepage-phase-a-browser.py`, `/tmp/lab-homepage-phase-a-attribution.py`. **임시·로컬 자료이며 Git에 포함하지 않았다.** `report.json`은 `python3 -c 'import json; r=json.load(open("/tmp/lab-homepage-phase-a-review/report.json")); print(len(r["pages"]), len(r["interactions"]), r["errors"])'`로 재집계할 수 있다.
- 구현 커밋에는 위 코드·README·기존 콘텐츠 테스트의 FAQ 경로 수정만 포함했다. 세션 시작 시 사용자 미커밋 변경은 없었다. 타 브랜치를 수정·삭제하지 않았다.

## 4. 🔴 지금 막혀 있는 것 · 결정 대기 ★

### ① PR #14 — 머지 완료
사용자 승인 후 머지했다. 이제 `claudedocs/design-audit-ai-look_2026-09-11.md`를 main에서 바로 읽는다. B~E단계의 PI 결정은 별도로 남아 있다.

### ② 구현 방향 결정 질문 5개 — 사람(PI)
진단 문서 §6: (1) 첫 방문자 한 사람은 누구인가 (2) 이 연구실만의 이미지 한 장은 무엇인가 (3) 레이더·아이디어는 대외용인가 내부 도구인가 (4) PI 가 200자 소개를 직접 쓸 수 있는가 (5) 브로셔인가 날짜 찍힌 게시판인가.
**A단계는 완료**했다. 이후 단계로 범위를 넓히지 않았다.
**결정이 필요한 것**: B(문구 전면 재작성, PI 소개문 필요), C(홈 3막 재구성, 카드→목록), D(필터 UI 단순화), E(사진).

### ③ 사진 자료(E단계) — 사람
단체사진(홍천 리트릿), EEG 아트 전시, 실제 연구 그림. 사용자가 주기 전까지 회색 박스 자리를 두지 말고 사진 없는 레이아웃으로 만든다(문서 §4-5).

## 5. 다음 단계 ★

1. `git status --short --branch`, `git log --oneline -5`, `gh run list --workflow deploy.yml --limit 3`로 현재 상태부터 확인한다. **A단계 재구현은 필요 없다.**
2. PR #14는 이미 머지됐다. `claudedocs/design-audit-ai-look_2026-09-11.md`의 §6과 아래 PI 결정부터 이어간다.
3. 사용자에게 이미 전달한 PI 결정 다섯 개의 답을 받는다: **첫 방문자 우선 대상 / 대표 실제 이미지 / 레이더·아이디어의 대외·내부 용도 / PI의 약 200자 소개문 / 소개 중심 브로셔 대 최신 소식 중심 게시판**. 이번 세션에는 답변이 없었다.
4. **B단계**: PI 소개문을 받은 뒤 `src/i18n/ui.ts`와 페이지 헤더를 재작성한다. 진단 문서 §4-3 표는 초안이며, 인원·연도·모집 상태는 확인 전 사실처럼 추가하지 않는다.
5. **C/D/E**: 홈 세 막 재구성·카드/필터 단순화·사진 배치는 PI 결정 후 진행한다. 기존 팔레트·타이포·언어 라우팅·구성원 자산·연구 지도·접근성은 보존한다.
6. 잔여 콘텐츠 결정(2026-09-09 이월): 구성원 신분·소속 날짜를 연구실 명부와 대조 · 한국어 구성원 학력/관심/passions와 레이더 본문 번역 공급 · 유전체/멀티오믹스 축 공식 명칭과 현재 모집 여부 확인 · Communications Medicine 조기공개 논문의 Version of Record 재확인.

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

**브라우저 검수**: 레이아웃·런타임 변경 후 1440×1000 / 390×844. 언어 전환, 연구 지도 링크, 구성원·논문 필터·BibTeX 실제 복사, 합류 FAQ, 홈 모델 출처 펼침, 레이더 요약의 키보드 Enter/Space.

## 8. 관련 메모리

- `/home/juke/.claude/projects/-home-juke-git/memory/lab_homepage_redesign_project.md` — 8/21~8/22 개편 이력(사진 추출 기법, DNS 컷오버, 이관 후 Actions 복구, 타이포 교훈). 2026-09-12 "남은 일" 갱신.
- `/home/juke/.claude/projects/-home-juke-git/memory/feedback_workflow_shared_file_race.md` — 병렬 편집 데이터 손실 함정 원본.
