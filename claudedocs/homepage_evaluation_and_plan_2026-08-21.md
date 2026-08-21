# SNU Connectome Lab 홈페이지 종합 평가 및 수정·보강 계획

작성일: 2026-08-21 · 대상: `snuconnectome/lab-homepage` (Astro 신규 사이트) vs 현행 www.connectomelab.com (Google Sites)
근거: 레포 전수 감사 (Crossref·arXiv·OpenAlex·GitHub API·라이브 사이트 교차 검증) + 세계적 연구실 사이트 12곳 디자인 벤치마크

---

## 1. 구 사이트 참조 여부 — 참조했으나 이관률이 낮고, 일부는 왜곡됨

**참조한 증거**: 네비게이션 구조(History/Research/Team/Publications/Join≈Research Program), 뉴스 항목(OB/Scene 전시, ICML DIVER-0, Nature Comms), 연혁(홍천 해커톤, BNL/MILA 연수), 멤버 데이터 상당수가 구 사이트와 일치.

**이관 실패 목록** (라이브 사이트 스크레이핑으로 확정):

| 항목 | 구 사이트 | 신규 레포 | 누락률 |
|---|---|---|---|
| 대학원생 | 19명 | 14명 정확 + 2명 오류 | 5명 완전 누락 |
| 동문 | 12명 (진로 포함) | 1명 | 11명 누락 |
| 스태프 | 코디네이터 신정은 | 0 (스키마에 staff 카테고리 자체가 없음) | 100% |
| 논문 | 100+ (2012–2026) | 28편 (2025–26만) | OpenAlex 기준 181편 중 153편 부재 |
| 다빈치 모토 | "Study the science of art…" (정체성) | 없음 | — |
| 주소·전화 | Bldg 16 M512, 82-2-880-8618 | 없음 | — |
| 인턴 목록 | 2022–25 코호트 | 0 (undergrad 탭도 없음) | 100% |

**신원 오류 2건 (심각)**:
- `eunseo-yu.json` → 실제는 **Allison Eun Se You (유은서)**: 소속(심리→BCS), 학위(HKU 분자생물학), 관심사, 이메일 전부 틀림
- `bohui-lee.json` → 실제는 **Bohee Lee (이보희)**: 소속, 학력(Université Paris Cité), 관심사(EEG/ECoG) 전부 틀림

**누락 5명**: 한동엽, 김도원, 오경진, 이아현, 윤유진 — 그런데 레포의 다른 콘텐츠(DIVER-0 뉴스, 예술·과학 페이지, 논문 저자란)는 이들을 이름으로 인용하고 있어 **자기모순** 상태.

---

## 2. 종합 평가

### 강점
- **정보 구조 우수**: Astro 콘텐츠 컬렉션 + Zod 스키마, 타입 안전한 Git 기반 CMS — 올바른 아키텍처 선택
- **자동화 골격 실재**: `sync_scholar.py`는 실제 Jiook Cha OpenAlex ID 2개를 조회(181편 확인), Research Radar의 자동 생성 8건은 arXiv ID·제목까지 전부 실물로 검증됨(진짜 Gemini 파이프라인이 돌았음)
- 3D 뷰어는 three.js로 실제 구현, 배포 파이프라인(GitHub Pages) 정상

### 약점 ① 신뢰성·정직성 — 가장 심각, 배포 전 필수 수정
1. **"Ask Connectome AI"는 AI가 아님**: 7개 키워드 `includes()` 매처 + 600ms 가짜 딜레이 + "Connectome AI is thinking…" 애니메이션. 정적 GitHub Pages라 백엔드 자체가 불가능. "무엇이든 물어보세요" 문구와 README "in real-time" 주장은 허위 표시
2. **외부 학자를 랩 멤버로 표기**: `sync_scholar.py:89`가 성씨 부분일치("Cha","Lee","Kim"…)로 labMembers를 추출 → Chadi G. Abdallah, Lee A. Baugh, Jae-Jin Kim 등 **외부 공저자 12명이 랩 멤버로 청록색 강조 표시**. 제3자 학자의 소속을 공개 사이트에서 오표기하는 것 — 최우선 수정
3. **조작된 제목 2건**: 실제 arXiv 2502.12771·Nature Comms DOI에 존재하지 않는 제목을 붙임 (trends 2건). 실제 논문 제목과 불일치 확인됨. "10,000+ developing brains" 수치도 창작
4. **출처 없는 트렌드 1건**: `qml-biomedical-trends.json` — 저자 "SNU Connectome Lab QML Initiative", 링크는 404
5. **과장 배지**: NeurIPS·ICML **워크숍** 스포트라이트를 본회의 "NeurIPS 2025 Spotlight"처럼 표기
6. **저자 오류**: `nature-comms-2025.json`의 "Gwanwoo Kim" → 실제는 **Gakyung Kim**(동문); 같은 논문이 중복 등록(2개 파일, 같은 DOI); 잘린 저자 목록을 "et al." 없이 완전한 것처럼 렌더
7. **능력 과장**: "arXiv, PubMed, OpenAlex 크롤러" 주장 vs 실제는 arXiv만; "Self-Updating" 주장 vs 자동커밋이 배포를 트리거하지 못하는 구조
8. **PI 직급 불일치**: 레포 "Associate Professor/부교수" vs 라이브 사이트 "Assistant Professor" — **사용자 확인 필요**

### 약점 ② 디자인·인문학적 향기·사람의 온기 — 방향 자체가 목적과 어긋남
벤치마크 12곳(McGovern, Allen, Stanford HAI, MIT Media Lab, Kording, PennLINC, Sainsbury Wellcome, MPI CBS, Wu Tsai, RIKEN, IBS, Distill) 조사 결과:
- **12곳 전부 라이트 배경의 편집 디자인**. 다크 기본은 0곳. 가장 근접한 DeepMind조차 라이트 기본이며, "사람 얼굴이 없는 가장 차가운 사이트"로 평가됨 — 현 드래프트가 모방한 미학은 '연구실'이 아니라 '기업 제품 쇼룸'의 언어
- 현 사이트: **사진 0장** (public/에 CNAME·favicon뿐), PI 아바타는 깨진 이미지, 나머지는 이니셜
- 다빈치 모토("Study the science of art. Study the art of science.") — 랩의 인문적 정체성 — 가 완전히 소실
- `passions` 필드(오페라, 에스프레소, 막걸리, 민초…)처럼 온기를 담는 데이터는 이미 있으나 표현이 못 따라감
- 접근성: 본문 대부분 12px, `text-slate-500` 4.0:1·`text-slate-600` 2.3:1로 WCAG AA 미달, 한국어 웹폰트 미로딩(시스템 폰트 충돌), `prefers-reduced-motion` 부재, 상시 애니메이션 ~12개
- `lang="ko"`인데 본문 90%가 영어; research 본문은 영어 전용(한국어 없음)

**온기를 만드는 검증된 패턴** (벤치마크에서 관찰):
1. 랩 단체사진 히어로 (Kording)
2. 유머가 살아있는 동문 진로 테이블 — 온기+리크루팅 증거를 동시에 (Kording)
3. 연구를 저널리즘처럼: 논문 목록이 아닌 헤드라인 스토리 (McGovern/Allen)
4. 멤버 수상·졸업·펠로우십 축하 뉴스피드 (PennLINC)
5. 세리프 편집 타이포그래피의 문예적 층위 (Distill)
6. 절제된 '와우' 요소 하나 + 나머지는 고요하게 (Allen)
7. 참여자·아웃리치 콘텐츠 (MPI CBS)
8. "Living in Korea" 류 국제 학생 안내 (IBS 역방향 응용)

### 약점 ③ 콘텐츠 신선도·완결성
- 뉴스 최신이 2025-12 (8개월 정체), radar는 2026-08 — 대비가 오히려 방치 인상
- `/news` 라우트가 없어 뉴스 6건 중 3건은 도달 불가
- Join 페이지: "OPEN CALL FOR 2026"이 무근거·무기한; 구 사이트의 QML 인턴 공고(마감 2025-12-05)도 이미 만료 — 양쪽 다 스테일

### 약점 ④ 기술 부채
- `@tailwindcss/typography`·`tailwindcss-animate` 미설치인데 `prose`·`animate-in` 클래스 사용 → research/history 마크다운 전체가 무스타일, 애니메이션 무동작
- radar 워크플로의 자동커밋은 `GITHUB_TOKEN` 푸시라 deploy를 트리거 못함 + 커밋 전 빌드 검증 없음 → 깨진 JSON이 잠복했다가 남의 커밋에서 빌드 폭발
- OG 이미지 404 (전 페이지), `#top` 데드 앵커, NeuroMamba 코드 링크 404
- 3D 뷰어: 리사이즈 후 히트테스트 어긋남, 터치 기기에서 클릭 불능(안내 문구와 모순)
- `sync_scholar.py`: 페이지네이션 없음(최신 30편 한계), DOI 중복 제거 없음, 태그 휴리스틱 오분류("generation"→Genetics)
- Astro 6 마이그레이션 부채 (legacy content collections API)

---

## 3. 홈페이지의 목적 재정의 (평가 기준)

1. **대학원생·포닥 리크루팅** (국내+국제) — 최우선. 지원자가 보는 것: 멘토링 증거(동문 진로), 랩 문화(사진·스토리), 연구 수준(논문·코드)
2. **학술적 신뢰** — 공저자·협력자·심사자가 방문. 저자 표기 오류·과장 배지는 여기서 치명적
3. **연구 참여자·일반 대중** — 심리학과 소속 랩. 접근성과 한국어가 중요
4. **연구비 기관·기자** — 연구 스토리텔링

현 드래프트는 1번의 '기술 어필' 절반만 최적화했고, 온기·신뢰·접근성 축은 오히려 구 Google Sites보다 후퇴했다.

---

## 4. 수정·보강 계획

### Phase 0 — 신뢰성 응급처치 (배포 전 필수, ~반나절)
| # | 작업 | 파일 |
|---|---|---|
| 0-1 | labMembers를 성씨 휴리스틱 → `src/content/members/` 기반 allowlist로 교체 | `scripts/sync_scholar.py:89`, `PublicationFilter.tsx:186` |
| 0-2 | AskLabAI 정직화: "Lab FAQ / 빠른 안내"로 리네임, thinking 애니메이션·라이브 닷 제거, 큐레이션 FAQ임을 명시 (또는 Phase 4에서 진짜 백엔드) + Markdown 렌더링 | `AskLabAI.tsx` |
| 0-3 | 조작 제목 트렌드 2건 실제 제목으로 수정, 무출처 1건 삭제 | `trends/brain-llm-alignment.json`, `polygenic-nature-trends.json`, `qml-biomedical-trends.json` |
| 0-4 | 중복 논문 제거(같은 DOI 2파일), "Gwanwoo Kim"→Gakyung Kim, et al. 처리 추가 | `publications/nature-comms-2025.json` 등 |
| 0-5 | 워크숍 스포트라이트 배지 정정 ("NeurIPS 2025 Workshop Spotlight") | `neuromamba-2025.json`, `diver0-icml-2025.json`, `AskLabAI.tsx` |
| 0-6 | 신원 오류 2건 정정 (Allison Eun Se You, Bohee Lee) | `members/eunseo-yu.json`, `members/bohui-lee.json` |
| 0-7 | "arXiv/PubMed/OpenAlex 크롤러"·"Self-Updating"·"3D neural tractography" 문구를 실제 능력에 맞게 수정 | `README.md`, `radar/index.astro`, `index.astro` |
| 0-8 | 날짜 오류 수정 (Nature Comms 2025-09-26; AAAI/OHBM 2025) | news/history/publications |

### Phase 1 — 콘텐츠 완결 (~1일)
- 누락 대학원생 5명 추가 (한동엽·김도원·오경진·이아현·윤유진 — 라이브 사이트에 이메일·학력 있음)
- 동문 11명 추가 + **진로 테이블** (UCSD, UT Austin, Samsung Biologics, Rutgers, MSU, SNU BCS, SAIHST, BNL, MIT, Columbia…) — 온기+리크루팅 이중 효과
- `config.ts`에 `staff` 카테고리 추가 + 코디네이터 신정은 + MemberGrid에 staff/undergrad 탭
- `sync_scholar.py` 페이지네이션 + DOI dedup + 태그 개선 → 논문 181편 전체 (2012–2026), 연도 아카이브
- `/news` 라우트 신설, footer에 주소·전화 복원, `#top` 앵커·NeuroMamba 링크 수정
- Join 페이지: 무기한 "OPEN CALL" 대신 실제 모집 정보(사용자 제공 필요), 국제 지원자 섹션
- Maria Pak·이승주 재학/동문 상태 확인 반영

### Phase 2 — 디자인 재설계: "밝은 미술관, 어두운 상영실 하나" (~2-3일)
방향: 전면 재작성이 아니라 **토큰 교체 + 구조 유지** (Tailwind 유틸리티 치환 수준으로 전환 비용 최소화)
- **바탕**: `stone-50`(#FAF9F7 종이 질감) + `stone-900` 잉크. 청록은 버리지 않고 **액센트로 반전** (`cyan-700` 링크·데이터·호버)
- **다크는 한 섹션만**: 3D 브레인 뷰어 밴드를 `slate-950` 딥잉크 패널로 — 기술적 '와우'는 보존, 정서 기조는 온화하게. glass-blur·glow는 이 밴드 안에서만
- **타이포**: 디스플레이 Hahmlet(한글 세리프)+Fraunces / 본문 Pretendard(jsDelivr; 폴백 Noto Sans KR) / 캡션·코드 IBM Plex Mono. 본문 16px 기준, WCAG AA 준수, `prefers-reduced-motion` 추가
- **다빈치 모토를 정보 구조로 승격**: "The Art of Science"(세리프·스토리·사람·랩 라이프·한국어 에세이) ↔ "The Science of Art"(모노 캡션·인터랙티브 그림·코드·데이터) 두 레지스터 인터리브
- **사진**: 단체사진 히어로 + 멤버 헤드샷 + 현장 캔디드 (촬영은 사용자 준비; 그전까지 tractography를 수묵화풍 '과학적 예술' 일러스트로 대체), OG 이미지 제작
- `passions` 필드 렌더링(현재 사장된 education·linkedin 필드 포함), 멤버 카드에 온기 부여
- 언어 전략: 영어 기본 + 핵심 페이지(Home/People/Join/참여자) 한국어 — MPI 모델. `lang` 속성 정합화
- 구현 시 `frontend-design` 스킬 로드 + `@tailwindcss/typography`·`tailwindcss-animate` 설치

### Phase 3 — 자동화 안정화 (~반나절)
- radar 워크플로: 커밋 전 `npm ci && npm run build` 검증 게이트, PAT 또는 deploy job 직결(자동커밋→배포 단절 해소), concurrency 그룹, fork guard
- radar 출력에 `generatedBy` 필드 — LLM 생성 vs 폴백을 UI에서 구분 표기 (폴백을 "AI Executive Summary"로 팔지 않기)
- 3D 뷰어 리사이즈·터치 버그 수정, `astro check` CI 추가, sitemap/robots.txt

### Phase 4 — 차별화 콘텐츠 (선택, 지속)
- 플래그십 논문 1–2편의 Distill 스타일 인터랙티브 explainer (NeuroMamba 또는 DIVER-0) — 기술력과 인문적 소통을 동시에 증명
- 멤버 수상·졸업 축하 뉴스피드 정례화, "Living in Korea"(국제 지원자), 연구 참여자 안내 페이지
- AskLabAI를 진짜로 만들려면: 정적 호스팅 한계상 서버리스 프록시(Cloudflare Workers 등) 필요 — 별도 결정

### 배포 컷오버 주의
`public/CNAME`이 www.connectomelab.com을 선점하므로 **DNS를 전환하는 순간 구 사이트가 사라짐**. Phase 0–2 완료 + 콘텐츠 검수 후 의도적으로 전환할 것. 그전까지는 `snuconnectome.github.io` 프리뷰로 검수.

---

## 5. 사용자 확인 필요 사항
1. PI 직급: 부교수(레포) vs 조교수(구 사이트) — 어느 쪽이 현재인지
2. Maria Pak·이승주: 재학생인지 동문인지 (라이브 team/history 페이지가 상충)
3. 사진 자산: 단체사진·헤드샷 제공 가능 여부와 시점
4. 디자인 방향: "밝은 미술관 + 어두운 상영실" 하이브리드 승인 여부 (증거는 위 벤치마크)
5. 2026 모집 정보: Join 페이지에 실을 실제 공고 내용
6. BK Silver Award·NeurIPS 뉴스 2건: 구 사이트에 없는 항목 — 사실 확인

## 6. 검증 계획
- `npm ci && npm run build` (아직 미실행 — research/history의 async map 등 정적 분석만 된 구간 확인)
- `npm run preview`로 전 페이지 육안 검수 (특히 prose 스타일, 아바타, 모바일)
- Lighthouse 접근성·성능 측정 (본문 크기·대비·모션 수정 전후 비교)
- 링크 체커로 외부 링크 전수 확인
