import React, { useState, useRef, useEffect } from 'react';
import { Send, X, BookOpen } from 'lucide-react';

type Lang = 'en' | 'ko';

interface ChatMessage {
  id: string;
  sender: 'guide' | 'user';
  text: string;
}

interface Props {
  lang?: Lang;
}

// A curated FAQ, matched by keyword. This is intentionally NOT presented as an
// AI assistant: the site is static (GitHub Pages), so there is no model behind it.
//
// Both languages are carried here because the guide is mounted on every page of
// both trees. It used to answer only in Korean, which left every English page
// with a Korean-only help widget.
type FaqKey = 'neuromamba' | 'diver0' | 'neurox' | 'qml' | 'admission' | 'culture' | 'pi';

const PRESET_KNOWLEDGE: Record<Lang, Record<FaqKey, string>> = {
  ko: {
    neuromamba: `**NeuroMamba**는 커넥톰 연구실이 개발한 **4D fMRI용 상태공간 파운데이션 모델**입니다 (NeurIPS 2025 Brain & Body 워크숍 Spotlight).

- **핵심 특징**: 트랜스포머 어텐션 대신 선택적 상태공간 모델(Mamba)을 써서 계산량이 입력 길이에 비례하게 하고, 뇌 바깥의 배경 토큰을 미리 걷어내 계산량을 거의 절반으로 줄였습니다.
- **결과**: UK Biobank·ABCD·HCP의 5만 명 넘는 전뇌 fMRI로 사전학습했고, HCP 성별 분류에서 SwiFT 논문이 보고한 정확도를 더 적은 파라미터로 넘어섰습니다. 다만 데이터 분할이 달라 직접 비교는 아닙니다. 다음 목표는 평가 과제를 인지 점수와 임상 진단 예측으로 넓히는 것입니다.`,

    diver0: `**DIVER-0**는 커넥톰 연구실이 제안한 **완전 채널 등변(Channel-Equivariant) EEG 파운데이션 모델**입니다 (ICML 2025 GenBio 워크숍 Spotlight).

- **문제**: 병원과 연구소마다 EEG 전극의 수와 배치가 달라, 한 데이터셋으로 학습한 모델을 다른 데이터셋에 그대로 쓰기 어렵습니다.
- **기술**: 채널 순열과 시간 이동에 대한 등변성(equivariance)을 아키텍처 안에 넣어, 사전학습 때 보지 못한 전극 배치에도 그대로 적용됩니다. 사전학습 데이터의 10%만으로도 경쟁력 있는 성능을 냈습니다.`,

    neurox: `**Neuro-X 프로젝트**는 커넥톰 연구실의 **뇌 파운데이션 모델** 프로그램입니다.

- **출발 가정**: LLM이 방대한 텍스트에서 언어의 구조를 익히듯, 대규모 뇌 데이터(fMRI, EEG, 확산 MRI)로 사전학습한 모델이 뇌 활동의 구조를 익힐 수 있다는 것입니다. 지금까지 fMRI 모델(SwiFT·NeuroMamba)과 EEG 모델(DIVER-0)을 만들었고, 이를 하나의 대규모 뇌 모델(Large Brain Model, LBM)로 모아 가는 것이 목표입니다.
- **이론적 토대**: György Buzsáki의 인사이드아웃(inside-out) 관점을 따라, 뇌를 스스로 행동 계획을 만들고 그 결과에서 배우는 예측 기계로 보고 신호 자체의 시공간 구조를 학습하게 합니다.`,

    qml: `커넥톰 연구실은 **양자 머신러닝(QML)**을 뇌·시계열 데이터에 접목하는 연구를 브룩헤이븐 국립연구소와 함께 진행하고 있습니다.

- **연구 주제**: ABCD·UK Biobank 휴지기 fMRI에 적용한 양자 시계열 트랜스포머(IEEE QCE 2025), 배런 플래토를 완화하는 멀티칩 앙상블 회로, 사전학습 EEG 인코더 위의 양자 아키텍처 탐색(Q-DIVER), 127큐비트 IBM Eagle에서의 10클래스 MNIST 실행.
- **인턴십**: 양자 컴퓨팅(Qiskit, PennyLane)과 뇌과학·AI에 열정이 있는 연구 인턴을 수시로 모집합니다. 양자역학 사전 지식은 필요하지 않습니다.`,

    admission: `**커넥톰 연구실 대학원 및 인턴 지원 안내**:

- **소속 트랙**: ① 서울대학교 심리학과 ② 협동과정 인공지능전공(IPAI) ③ 뇌인지과학과(BCS)
- **환영 배경**: 심리학, 인공지능, 컴퓨터공학, 통계학, 의학, 물리학, 생명과학 등 다양한 분야
- **지원 방법**: CV, 성적증명서, 관심 연구 분야 소개(1-2단락)를 connectome@snu.ac.kr 로 보내주세요. 검토 후 인터뷰를 안내해 드립니다.`,

    culture: `**커넥톰 연구실 문화**:

- 🏔️ **연구 해커톤**: 강원도 홍천 등에서 정기적으로 진행하는 며칠간의 집중 해커톤 (연구 몰입 + 요리와 게임).
- 🌍 **해외 연수**: 캐나다 MILA, 미국 브룩헤이븐 국립연구소(BNL) 등에 학생 연구원을 파견합니다.
- 🎨 **예술과 삶**: EEG 아트 전시(옵/신 페스티벌), 음악, 커피, 그리고 교수님의 칵테일까지 — 창의성은 삶의 즐거움에서 나온다고 믿습니다.`,

    pi: `**차지욱 교수 (Jiook Cha, PhD)**는 서울대학교 심리학과·인공지능협동과정·뇌인지과학과 부교수이자 커넥톰 연구실의 PI입니다.

- 미국 컬럼비아 대학교 아동청소년정신의학과 조교수와 데이터사이언스 연구소(DSI) 멤버를 역임했습니다.
- NIMH K01 커리어 개발상, NARSAD Young Investigator Award, 서울대 창의선도연구자 등을 수상했습니다.
- 연구 분야: 뇌 파운데이션 모델(Neuro-X), 동적 커넥톰, 계산정신의학, 유전체-뇌영상 융합, 양자 머신러닝.`,
  },

  en: {
    neuromamba: `**NeuroMamba** is the lab's **state-space foundation model for 4D fMRI** (Spotlight at the NeurIPS 2025 Brain & Body workshop).

- **What it does**: replaces the transformer's attention with a selective state-space model (Mamba), so compute grows in proportion to input length rather than its square, and discards non-brain background tokens before training, which cuts the cost almost in half.
- **Results**: pretrained on whole-brain fMRI from more than 50,000 people in UK Biobank, ABCD and HCP; after fine-tuning, a 3.1M-parameter model scored higher on HCP sex classification than the published SwiFT result (4.6M parameters), though on a different train/test split. Cognitive scores and clinical diagnoses are the next targets.`,

    diver0: `**DIVER-0** is the lab's **fully channel-equivariant EEG foundation model** (Spotlight at the ICML 2025 GenBio workshop).

- **The problem**: every clinic and lab uses a different number and layout of electrodes, so EEG datasets do not line up.
- **The approach**: build equivariance to channel permutation and to shifts in time into the architecture, so the model adapts to electrode layouts it never saw in pretraining. It reached competitive performance with only a tenth of the pretraining data.`,

    neurox: `**The Neuro-X Project** is the lab's **brain foundation model** program.

- **The premise**: as an LLM learns the structure of language from a large body of text, a model pretrained on large brain datasets (fMRI, EEG, diffusion MRI) should be able to learn the structure of brain activity. So far the lab has built fMRI models (SwiFT, NeuroMamba) and an EEG model (DIVER-0); the goal is to gather them into one Large Brain Model (LBM).
- **The theory**: György Buzsáki's inside-out view, which treats the brain as a prediction machine that generates its own action plans and learns from their consequences, so the models learn the spatiotemporal structure of the signal itself.`,

    qml: `The lab works on **quantum machine learning (QML)** for brain and time-series data, much of it with **Brookhaven National Laboratory**.

- **Current threads**: a Quantum Time-series Transformer applied to ABCD and UK Biobank resting-state fMRI (IEEE QCE 2025); multi-chip ensemble circuits that mitigate barren plateaus; quantum architecture search on a pretrained EEG encoder (Q-DIVER); and ten-class MNIST run end-to-end on a 127-qubit IBM Eagle processor.
- **Internships**: we recruit research interns interested in quantum computing (Qiskit, PennyLane) and brain AI year-round. No prior quantum background is required.`,

    admission: `**Applying to the lab — graduate study and internships**:

- **Three tracks**: ① Department of Psychology, SNU ② Interdisciplinary Program in AI (IPAI) ③ Department of Brain & Cognitive Sciences (BCS)
- **Backgrounds we welcome**: psychology, AI, computer science, statistics, medicine, physics, life sciences, and more
- **How to apply**: send a CV, transcripts, and one or two paragraphs on the research that draws you to connectome@snu.ac.kr. We follow up with an interview. International applicants are welcome to apply in English.`,

    culture: `**Life in the lab**:

- 🏔️ **Research hackathons**: multi-day deep-dive sprints in Hongcheon, Gangwon-do — research by day, cooking and games by night.
- 🌍 **Fellowships abroad**: students spend funded research terms at MILA (Montreal) and Brookhaven National Laboratory (New York).
- 🎨 **Art and life**: EEG art at the OB/Scene festival, music, coffee, and the PI's cocktails — we think creativity grows out of the pleasures of life.`,

    pi: `**Prof. Jiook Cha (차지욱, PhD)** is Associate Professor in the Department of Psychology, the Interdisciplinary Program in AI, and the Department of Brain & Cognitive Sciences at Seoul National University, and PI of the Connectome Lab.

- Previously Assistant Professor of Child & Adolescent Psychiatry at Columbia University and a member of its Data Science Institute.
- Awards include the NIMH K01 Career Development Award, a NARSAD Young Investigator Award, and SNU's Creative-Pioneering Researcher award.
- Research: brain foundation models (Neuro-X), dynamic connectomics, computational psychiatry, imaging genetics, and quantum machine learning.`,
  },
};

const FALLBACK: Record<Lang, string> = {
  ko: `이 안내는 연구실이 미리 작성한 FAQ에서 키워드로 찾아 보여드립니다. 아래 주제로 물어봐 주세요:

- **"NeuroMamba"** — 4D fMRI 파운데이션 모델
- **"DIVER-0"** — EEG 파운데이션 모델
- **"지원"** — 대학원·인턴 지원 방법
- **"양자"** — 양자 머신러닝 연구
- **"문화"** — 연구실 문화와 해외 연수
- **"교수"** — PI 소개

그 밖의 질문은 connectome@snu.ac.kr 로 이메일 주시면 사람이 답해 드립니다.`,

  en: `This guide looks your question up by keyword in a FAQ the lab wrote by hand. Try one of these:

- **"NeuroMamba"** — the 4D fMRI foundation model
- **"DIVER-0"** — the EEG foundation model
- **"apply"** — graduate study and internships
- **"quantum"** — quantum machine learning
- **"culture"** — lab life and fellowships abroad
- **"PI"** — about Prof. Jiook Cha

For anything else, email connectome@snu.ac.kr and a person will answer.`,
};

const UI: Record<Lang, Record<string, string>> = {
  ko: {
    launcher: 'Lab guide · 연구실 안내',
    title: 'Lab guide · 연구실 안내',
    subtitle: '큐레이션된 FAQ — 실시간 AI가 아닙니다',
    welcome:
      '안녕하세요! 커넥톰 연구실 안내입니다. 연구실이 미리 정리해 둔 FAQ에서 답을 찾아 보여드려요. 대표 연구(NeuroMamba, DIVER-0, Neuro-X), 대학원·인턴 지원, 연구실 문화에 대해 물어보세요.',
    placeholder: '예: 대학원 지원 방법',
    inputLabel: '연구실에 대해 물어보기',
    close: '안내 닫기',
    send: '질문 보내기',
  },
  en: {
    launcher: 'Lab guide',
    title: 'Lab guide',
    subtitle: 'A curated FAQ — not a live AI',
    welcome:
      "Hello! This is the Connectome Lab guide. I look answers up in a FAQ the lab wrote by hand. Ask about our main work (NeuroMamba, DIVER-0, Neuro-X), applying for graduate study or an internship, or what the lab is like.",
    placeholder: 'e.g. how do I apply?',
    inputLabel: 'Ask about the lab',
    close: 'Close guide',
    send: 'Send question',
  },
};

const SUGGESTIONS: Record<Lang, { label: string; query: string }[]> = {
  ko: [
    { label: '🧠 NeuroMamba', query: 'NeuroMamba가 무엇인가요?' },
    { label: '⚡ DIVER-0 (EEG)', query: 'DIVER-0 EEG 모델 설명해줘' },
    { label: '🎓 지원 안내', query: '대학원 지원 방법' },
    { label: '🎨 연구실 문화', query: '연구실 문화가 궁금해요' },
  ],
  en: [
    { label: '🧠 NeuroMamba', query: 'What is NeuroMamba?' },
    { label: '⚡ DIVER-0 (EEG)', query: 'Tell me about the DIVER-0 EEG model' },
    { label: '🎓 How to apply', query: 'How do I apply to the lab?' },
    { label: '🎨 Lab culture', query: "What is the lab's culture like?" },
  ],
};

// Minimal renderer for the **bold** markers used in the FAQ text.
function renderBold(text: string): React.ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
    part.startsWith('**') && part.endsWith('**') ? (
      <strong key={i}>{part.slice(2, -2)}</strong>
    ) : (
      <React.Fragment key={i}>{part}</React.Fragment>
    )
  );
}

// Keywords stay bilingual whatever the page language, so a Korean speaker on
// the English site (and the reverse) still reaches the right entry.
function findAnswer(query: string, lang: Lang): string {
  const lower = query.toLowerCase();
  const k = PRESET_KNOWLEDGE[lang];
  if (/(mamba|뉴로맘바|fmri)/.test(lower)) return k.neuromamba;
  if (/(diver|eeg|다이버)/.test(lower)) return k.diver0;
  if (/(neuro-x|lbm|파운데이션|foundation)/.test(lower)) return k.neurox;
  if (/(qml|양자|quantum)/.test(lower)) return k.qml;
  if (/(지원|인턴|입학|대학원|apply|admission|intern)/.test(lower)) return k.admission;
  if (/(문화|파티|해커톤|분위기|culture|life)/.test(lower)) return k.culture;
  if (/(차지욱|교수|\bpi\b|cha|professor)/.test(lower)) return k.pi;
  return FALLBACK[lang];
}

export default function AskLabAI({ lang = 'ko' }: Props) {
  const t = UI[lang];
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: 'welcome', sender: 'guide', text: t.welcome },
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query) return;
    setMessages((prev) => [
      ...prev,
      { id: `${Date.now()}-u`, sender: 'user', text: query },
      { id: `${Date.now()}-g`, sender: 'guide', text: findAnswer(query, lang) },
    ]);
    if (!textToSend) setInput('');
  };

  return (
    <>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 rounded-full bg-lab-700 hover:bg-lab-800 text-white font-semibold text-sm shadow-lg transition-colors"
        >
          <BookOpen className="w-4 h-4" aria-hidden="true" />
          <span>{t.launcher}</span>
        </button>
      )}

      {isOpen && (
        <div
          role="dialog"
          aria-label={t.title}
          className="fixed bottom-4 right-4 z-50 w-[95vw] sm:w-[420px] h-[560px] rounded-2xl bg-white border border-line flex flex-col shadow-2xl overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-300"
        >
          {/* Header */}
          <div className="px-5 py-4 bg-paper border-b border-line flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-lab-700 flex items-center justify-center text-white">
                <BookOpen className="w-4 h-4" aria-hidden="true" />
              </div>
              <div>
                <h3 className="font-semibold text-ink text-sm">{t.title}</h3>
                <p className="text-xs text-ink-faint">{t.subtitle}</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="w-7 h-7 rounded-full bg-white border border-line hover:bg-paper flex items-center justify-center text-ink-faint hover:text-ink transition-colors"
              aria-label={t.close}
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Suggestion chips */}
          <div className="px-4 py-2.5 bg-white border-b border-line overflow-x-auto flex gap-2">
            {SUGGESTIONS[lang].map((s) => (
              <button
                key={s.label}
                onClick={() => handleSend(s.query)}
                className="text-xs whitespace-nowrap px-2.5 py-1.5 rounded-full bg-paper hover:bg-lab-50 hover:text-lab-800 text-ink-soft border border-line transition-colors"
              >
                {s.label}
              </button>
            ))}
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3.5 text-sm bg-paper" aria-live="polite">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] p-3.5 rounded-xl leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-lab-700 text-white rounded-tr-sm'
                      : 'bg-white text-ink border border-line rounded-tl-sm'
                  }`}
                >
                  <div className="whitespace-pre-line">{renderBold(msg.text)}</div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="p-3 bg-white border-t border-line flex items-center gap-2"
          >
            <label htmlFor="lab-guide-input" className="sr-only">
              {t.inputLabel}
            </label>
            <input
              id="lab-guide-input"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={t.placeholder}
              className="flex-1 bg-paper border border-line rounded-lg px-3.5 py-2.5 text-sm text-ink placeholder-ink-faint focus:border-lab-600 transition-colors"
            />
            <button
              type="submit"
              disabled={!input.trim()}
              className="w-10 h-10 rounded-lg bg-lab-700 hover:bg-lab-800 disabled:opacity-40 text-white flex items-center justify-center transition-colors shrink-0"
              aria-label={t.send}
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
}
