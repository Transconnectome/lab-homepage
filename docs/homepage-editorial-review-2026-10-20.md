# 홈페이지 설명·그림 보강 — 2026-10-20

> 최신 인계 상태: [HANDOFF](../claudedocs/HANDOFF.md)와 [검증 요약](verification/2026-10-20/README.md). 아래 검증 이력은 각 작성 시점의 기록이며 최종 Teamwork 감사는 아직 완료되지 않았다.

기존의 종이색·serif 제목·oxblood 강조와 연구 목적을 유지하면서, 첫 방문자가 실제 연구의 발견과 남은 문제를 읽고 자신의 질문으로 지원 준비를 시작하도록 로컬 화면을 보강했다. 성과·입학·지도·자원·진로를 보장하는 문구는 추가하지 않았다. 운영 배포와 원격 push는 수행하지 않았다.

## 개편 전후와 판단

| 개편 전 | 이번 반영 | 이유와 범위 |
|---|---|---|
| 오늘 질문 선택기와 네 질문 목록이 같은 질문·tagline을 연이어 반복 | 네 질문을 우선 표시하고 일일 선택기는 선택적으로 펼치는 짧은 구획으로 이동 | 네 축과 KST 선택·키보드 버튼·JavaScript 없는 링크를 보존하면서 중복 읽기 축소 |
| 홈에서는 질문과 방법 개요를 볼 수 있지만 실제 발견은 상세 페이지에서 찾아야 함 | 넓은 SwiFUN 사례와 평가 개념도, 아래 두 열린 열에 발달·경외 사례 | 동일 크기 카드나 수치 경쟁 대신 질문·비교·발견·한계·출처를 읽게 함 |
| MBBN A–C 그림은 출처와 인과 한계를 표시하지만 색과 분석 맥락이 설명되지 않음 | 주파수 분리의 목적, 빨강/파랑의 의미, 개인 진단의 한계 추가 | 원본 PNG와 A–C 발췌를 유지하고 그림이 무엇을 말하는지 설명 |
| 연구 상세를 읽은 뒤 지원 절차로 가는 직접 안내 부족 | 연구 페이지 끝에 질문 중심 합류 안내, 위에는 네 분야 본문 바로가기 | 전체 연구 지도·본문을 보존하면서 탐색과 다음 행동 연결 |
| 합류 안내에는 서류가 있으나 관심사를 문장으로 만드는 길잡이가 없음 | 질문 고르기 → 사례의 발견과 한계 읽기 → 다음 질문 적기 | 추가 제출 조건이 아닌 선택 안내라고 명시 |
| 320px People 5열에서 영문 이름이 단어 중간에서 나뉨 | 모바일 3열, 640px부터 5열, 대화면 10열 | 기존 초상·명부·링크를 유지하며 이름을 읽을 폭 확보 |

### 실제 문구 전후 예시

1. 그림 caption: “MBBN 모델에서 추정한 ADHD 관련 뇌 연결 패턴(그림 2A–C 발췌). 모델 분석 결과이며 질환의 인과기전을 입증하지 않습니다.” → “MBBN이 추정한 ADHD 관련 뇌 연결 패턴. 빨강은 비교 집단보다 높은 연결, 파랑은 낮은 연결을 나타냅니다. 그림 2A–C 발췌이며, 모델 분석 결과가 질환의 원인이나 개인의 진단을 뜻하지는 않습니다.” 색을 읽는 법과 해석의 경계를 함께 제공한다.
2. 홈의 기존 질문·tagline 아래에 발견 문장이 없던 상태 → “성인과 아동 자료에서 예측 지도와 실제 지도의 전체 유사도는 비교 모델 ConnTask보다 높았지만, 누구의 지도인지 구별하는 성능은 ConnTask가 더 좋았습니다.” 우세한 결과만 남기지 않고 평가 목적에 따른 차이를 드러낸다.
3. 지원 서류 목록으로 바로 가던 흐름 → “관심사를 정리하기 위한 선택 안내입니다. 추가 제출 과제가 아닙니다.”와 “무엇이 궁금하고 왜 중요한가요? 어떤 관측이나 비교가 도움이 될까요?” 기존 연구 관심 소개를 준비하는 방법을 제시하며 새 선발 요건을 만들지 않는다.

## 주장–출처–검토 범위

2026-10-20 근거 조사자가 아래 원자료의 해당 절·그림·방법·한계를 검토한 뒤 paired KO/EN 문안을 제안했고, 구현자는 그 문안을 보존해 통합했다. 이는 논문 재현이나 원자료 재분석이 아니다. 모든 논문·보충자료 전체를 읽었다는 주장이 아니다.

| 공개 주장 | 원자료·정확한 위치 | 설계·결과와 해석 경계 | 연구실 관계 |
|---|---|---|---|
| SwiFUN은 휴지기 fMRI에서 과제 활성 지도를 예측하며 지도 유사도와 개인 식별의 비교 우위가 다름 | [Kwon et al., Imaging Neuroscience (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12320000/), DOI 10.1162/imag_a_00440; §2.1 및 평가 방법, §3.1, Fig.2a/2d, Discussion limitations, Author Contributions | 성인 UKB·아동 ABCD; 전체 지도 유사도는 SwiFUN, 개인 식별은 ConnTask가 우세. 마음 읽기·보편적 전이·임상 검증으로 확대하지 않음 | Kwon 주 연구자; Cha 교신·지도 |
| 아동의 유전·뇌영상·인지·행동·환경 특징의 공동변화 분석; 학교·이웃 포함. 이 아동 표본에서 인지 관련 유전 점수와 큰 뇌 부피·표면적이 함께 높은 패턴 | [Joo et al., Nature Communications (2025)](https://www.nature.com/articles/s41467-025-63312-6); 결과는 Results Brain morphometry (sMRI), two-block CCA component 1, Fig.2; Methods SGCCA. 학교·이웃 관측의 포함은 별도 Methods Non-imaging measures; Discussion limitations; Contributions | 횡단 관찰의 다변량 집단 패턴. 학교·이웃이 해당 two-block 성분에 포함됐다는 뜻이 아님. 유전→뇌→행동의 인과 순서나 개인의 발달 궤적 아님. 선형 분석이며 주 분석은 European-ancestry 집단으로 일반화 제한. 분석별 분모가 달라 새 표본 수를 인용하지 않음 | Joo와 Cha 연구 구상 |
| VR 중 경험 보고·EEG 기록; 혼합 감정의 지속·강도와 경외 보고의 관계 | [Lee et al., Communications Psychology (2025)](https://www.nature.com/articles/s44271-025-00299-2); Methods Participants/Procedures/EEG; Results 첫 절 및 Fig.2; Discussion limitations; Contributions | 한국 청년 표본, 실시간 보고가 감정에 영향을 줄 수 있음. 치료 효과·보편적 감정 기제·DMN 주장 없음. 상세 본문의 한계 유지 | Lee와 Cha 구상; Lee 분석 주도 |
| MBBN의 ADHD 관련 연결 패턴 및 빨강/파랑 해설 | [Bae et al., Communications Biology (2026)](https://www.nature.com/articles/s42003-026-10011-7); Fig.2 caption, Results attribution, Methods frequency decomposition/analysis, Discussion limitations | 학습된 모델 attention의 분석. 빨강은 비교 집단보다 높은 연결, 파랑은 낮은 연결. A–C는 ADHD 관련, D–F는 ASD. 직접 축삭 추적·질환 원인·개인 진단 아님 | Bae 구상·구현·실험; Cha 지도 |

SwiFUN의 마지막 개인 고유성 질문과 참여 안내는 공개 결과를 읽는 편집적 질문이다. 공식 신규 과제·연구비·모집 계획으로 제시하지 않았다. QML을 포함한 네 연구축과 모든 연구 Markdown은 그대로 유지했으며 이번에 모든 기존 연구 주장을 새로 심사한 것은 아니다.

## 그림과 시각 설명의 출처

- **MBBN 실증 그림:** [원본 Figure 2](https://www.nature.com/articles/s42003-026-10011-7/figures/2), Bae et al., 2026, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). 저장 PNG 1234×2495, SHA-256 `98583e0cf7d7dde33444c311c0472362f04ac3c4147f71f714e967725a4f691d`. 원본 픽셀은 수정하지 않았다. 기존 정사각형 CSS의 A–C 발췌를 유지하고 화면 caption에 발췌·저자·출처·라이선스·해석 한계를 표시했다. 출판사 권한과 별도 크레딧 예외 없음은 근거 조사에서 재확인했다. [에셋 provenance](../public/assets/site/README.md).
- **SwiFUN 설명도:** 이번에 HTML/CSS로 작성한 연구 평가 개념도. 휴지기 fMRI → 모델 → 예측 지도와 실제 측정 지도 비교를 표현한다. 출처는 위 SwiFUN 연구다. 측정 데이터·성능 그래프가 아님을 화면에 명시했고 화살표는 처리 순서만 뜻한다. 합성 뇌영상·가짜 활성도·측정값을 만들지 않았다.
- **구성원 초상:** 기존 사진과 사용 범위를 유지했다. 이번에 새로운 사진·개인정보·동의 자료를 수집하지 않았고 새 동의 검증을 주장하지 않는다.
- **연구 지도:** 기존 [피질 표면 참고 그림 provenance](../public/assets/research/README.md)와 해부 참고/결과 구분을 유지했다. 경외 연구의 VR 영상 프레임은 재사용하지 않았다.

## 구현·검증과 증거

공통 Astro 페이지와 `src/data/researchStories.ts`를 사용해 한국어 루트와 영어 `/en/`에 동일한 과학적 범위와 실제 내부 이동 경로를 제공한다. 기존 타입·라우트·연구 지도·전체 본문·FAQ·최신 소식·논문 목록·생성 콘텐츠 경계를 유지한다. 현재 모집 여부와 CV·성적표·1–2단락 안내는 기존 정책 그대로다.

실행한 검증:

- `npm test`: radar/ideas/news/content contract 모두 통과.
- `npm run build`: Astro 정적 빌드 성공.
- `npm run test:site`: 16 bilingual pages, legacy redirects, local links/assets and fragments 통과.
- `RESEARCH_MAP_URL=http://127.0.0.1:4389 npm run test:research-map`: 11개 브라우저 계약 통과. 당시 실행은 설치된 Chromium을 `PLAYWRIGHT_CHROMIUM_EXECUTABLE` 환경 변수로 지정했다. 공개 명령에서는 실행 환경별 경로를 생략했다. 재현 환경의 Python Playwright·Chromium 준비는 [README의 Build & Preview](../README.md#build--preview)를 따른다. 사용자 지정 Chromium이 필요하면 해당 환경의 실행 파일 경로를 `PLAYWRIGHT_CHROMIUM_EXECUTABLE`로 설정한 뒤 실행한다.
- KO/EN 홈·연구·합류 × 320/390/1440px = 18개 실제 로컬 dev 렌더 관찰: 가로 넘침 0, pageerror 0, 미로딩 main 이미지 0. 홈 초상은 실제 로드 완료를 기다렸다. 초기 after capture의 smooth-scroll/sticky navbar 위치를 개선하기 위해 reduced-motion·즉시 top 이동으로 별도 `final-after` 캡처를 저장했다. 최초 캡처를 덮어쓰지 않았다.

증거 경로는 저장소 기준 `verification/teamwork-20261020/`다. BEFORE는 `survey_experience/report-before.json`과 `*-before.png`; AFTER는 `implementation/final-after/report-after.json` 및 `*-after.png`; 최초 after 관찰과 원시 로그는 `implementation/`에 보존한다. 코드의 초기 사용자 변경은 `survey_structure/initial-bytes/` 및 `initial-manifest.json`으로 별도 보존되어 있다. 검증 디렉터리는 로컬 실행 증거이며 운영 배포물이 아니다.

독립 편집 검토·새 발달 문장의 원문 검토·챌린저·감사는 이번 수정 기록 작성 시 **후속 판정 대기 중**이다. E2E는 독립 담당자가 작성한 Tier1–4 총 80개 사례를 구현자가 수정 없이 실행한다. 독립 작성과 구현자의 실행은 구분하며 실제 실행 결과는 아래 후속 기록과 [TEST_READY의 최신 추가 기록](../TEST_READY.md)을 따른다. 위 로컬 검사만으로 세계 최고 수준·지원 전환율·과학적 진실성·전체 보조공학·실사용 성능이 검증됐다고 주장하지 않는다.

재현은 저장소 루트에서 위 npm 명령을 실행하고, 개발 서버 `npm run dev -- --host 127.0.0.1 --port 4389`에 대해 `python3 verification/teamwork-20261020/implementation/capture_after.py`를 실행한다. **기존 증거를 보존하려면 스크립트의 OUT을 새 디렉터리로 지정한다.** 빌드/preview 검사 중에는 dist를 재빌드하지 않는다.

## 남은 판단과 갱신

PI의 구체적 확인 범위는 이번 세 사례를 대표 연구의 공개 소개로 선택한 편집 판단과 참여 안내의 공식 어조다. 논문으로 확인 가능한 비교·출처 확인을 PI에게 떠넘기지 않는다. 현재 모집/연구 자원/장학·지도 기회는 이번 작업으로 확인하지 않았다.

문구 갱신 시 `researchStories.ts`의 한영 쌍, 비교 대상·한계, 이 문서의 원자료 위치를 함께 갱신한다. 새 그림은 별도 권한과 provenance 검토 후 추가한다. 수동 연구 본문과 큐레이션 사례는 기존 논문·레이더·아이디어 자동화의 쓰기 대상이 아니며, 이를 자동 생성 산문으로 대체하지 않는다. 현재 상태의 기준 검토 인덱스는 [research-content-review.md](research-content-review.md) §21이다.


## 후속 수정과 검증 이력

- **내용:** 발달 사례에 인지 관련 유전 점수와 뇌 부피·표면적의 공동변화라는 실제 관측 결과를 한영 한 문장으로 추가했다. 학교·이웃의 Methods 범위와 two-block CCA 결과를 구분하고, 기존 인과 한계는 유지했다. 위 주장–출처 행에 정확한 위치·주 분석 조상집단·횡단적 한계를 보강했다.
- **접근성:** 합류 이메일에만 `max-w-full [overflow-wrap:anywhere]`를 적용했다. 기존 주소·mailto·encoded subject·기본 크기 버튼 폭을 유지했다. 공개 브라우저 명령에서는 실행 환경의 개인 설치 경로를 제거했다.
- **실행 완료:** `npm test`, `npm run build`, `npm run test:site` 통과. 최초 build는 종료 코드 143으로 중단됐고 한 차례 재실행에서 16페이지 빌드에 성공했다. 중단 원인은 확정하지 않았으며 원시 로그를 보존했다.
- **수정 후 브라우저:** KO/EN 합류·홈 × 320/390/1440px × 100%/200% root font-size의 **24조건 통과**. 문서 가로 넘침과 pageerror 0, 새 한영 문구 표시, 이메일 전체 텍스트·href·subject 보존, 키보드 Tab 도달과 가시적 초점, 지원 앵커 이동을 확인했다. 글자 확대는 브라우저 전체 zoom과 동일하지 않으며 Chromium 한 환경의 결과다. [원시 결과](../verification/teamwork-20261020/repair_worker/targeted-final/results.json).
- **E2E 이력:** 독립 작성자의 기존 28 PASS/2 FAIL과 56 PASS/4 FAIL은 그대로 보존한다. 수정 후 첫 실행은 서버 접속 실패로 5 PASS/25 FAIL, 다음 실행은 서버가 중도 종료돼 47 PASS/13 FAIL이었다. 자동 검사나 제품 결함이 모두 해소됐다는 뜻으로 바꾸지 않았다. 새 전경 TTY 서버에서 같은 80개 사례를 실행하며 [해당 원시 결과 디렉터리](../verification/teamwork-20261020/repair_worker/e2e-tty/)와 [TEST_READY](../TEST_READY.md)가 완료·실패·미실행 수를 제공한다. 원본 runner와 판정 조건은 바꾸지 않고 `--output`으로 별도 증거 경로만 지정했다.
- **새 화면:** [한국어 데스크톱 연구 지면](../verification/teamwork-20261020/repair_worker/clean-previews/ko-desktop-studies.png), [영어 데스크톱 연구 지면](../verification/teamwork-20261020/repair_worker/clean-previews/en-desktop-studies.png), [한국어 390px 홈](../verification/teamwork-20261020/repair_worker/targeted-final/ko-home-390-clean.png), [영어 390px 홈](../verification/teamwork-20261020/repair_worker/targeted-final/en-home-390-clean.png). 지연 이미지를 각각 실제 로드하고 초점을 해제한 뒤 캡처했다. 과거 화면·실패 로그·중간 캡처는 덮어쓰지 않았다.

브라우저 원시 기록과 실행 로그는 `verification/teamwork-20261020/repair_worker/`에 있다. 독립 suite의 재현은 실행 중인 preview에 `python3 verification/teamwork-20261020/e2e_track/run_e2e.py --url http://127.0.0.1:4390 --output verification/teamwork-20261020/repair_worker/e2e-new-run`을 사용한다. 지정 출력 경로는 아직 존재하지 않는 새 경로여야 한다. 과학 문장과 UI의 독립 검토는 실행자의 자동 검사와 별개이며 원격 push·배포는 수행하지 않았다.
