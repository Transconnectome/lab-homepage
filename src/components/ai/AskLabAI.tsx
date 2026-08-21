import React, { useState, useRef, useEffect } from 'react';
import { Send, X, BookOpen } from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'guide' | 'user';
  text: string;
}

// A curated FAQ, matched by keyword. This is intentionally NOT presented as an
// AI assistant: the site is static (GitHub Pages), so there is no model behind it.
const PRESET_KNOWLEDGE: Record<string, string> = {
  neuromamba: `**NeuroMamba**는 커넥톰 연구실이 개발한 **4D fMRI용 상태 공간 기반 파운데이션 모델**입니다 (NeurIPS 2025 워크숍 Spotlight).

- **핵심 특징**: 트랜스포머의 O(N²) 계산 복잡도를 선형 O(N)으로 줄여, 수천 타임스텝의 긴 4D 뇌영상 전체를 효율적으로 모델링합니다.
- **의의**: 대규모 fMRI 코호트에서 뇌 역동성을 사전학습하여 인지 기능 디코딩과 정신질환 예측에 활용됩니다.`,

  diver0: `**DIVER-0**는 커넥톰 연구실이 제안한 **완전 채널 동변(Channel-Equivariant) EEG 파운데이션 모델**입니다 (ICML 2025 워크숍 Spotlight).

- **문제 해결**: 병원·연구소마다 다른 EEG 전극 배치(8~256채널)로 인한 데이터 불일치 문제를 해결합니다.
- **기술**: 전극 위치를 연속 3D 좌표 포인트 클라우드로 취급하여 기하 대칭성을 보존하며 zero-shot 전이를 달성합니다.`,

  neurox: `**Neuro-X 프로젝트**는 차지욱 교수 연구팀이 주도하는 **대규모 뇌 파운데이션 모델(Large Brain Model)** 연구 이니셔티브입니다.

- **비전**: LLM이 언어를 학습하듯, 대규모 다중모달 뇌 데이터(fMRI, EEG, dMRI, 유전체)를 사전학습하여 마음과 행동의 신경 원리를 탐구합니다.
- **이론적 토대**: György Buzsáki의 'Inside-Out' 프레임워크를 기반으로 뇌의 능동적 예측과 시공간 역동성을 모델링합니다.`,

  qml: `커넥톰 연구실은 **양자 머신러닝(QML)**을 고차원 뇌 데이터에 접목하는 연구를 진행하고 있습니다.

- **연구 주제**: 파라미터화된 양자 회로(PQC)와 양자 커널을 활용한 뇌 연결성 분석, IBM 양자컴퓨터 기반 이미지 분류 등.
- **인턴십**: 양자 컴퓨팅(Qiskit, PennyLane)과 뇌과학·AI에 열정이 있는 연구 인턴을 수시로 모집합니다.`,

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
};

const FALLBACK = `이 안내는 연구실이 미리 작성한 FAQ에서 키워드로 찾아 보여드립니다. 아래 주제로 물어봐 주세요:

- **"NeuroMamba"** — 4D fMRI 파운데이션 모델
- **"DIVER-0"** — EEG 파운데이션 모델
- **"지원"** — 대학원·인턴 지원 방법
- **"양자"** — 양자 머신러닝 연구
- **"문화"** — 연구실 문화와 해외 연수
- **"교수"** — PI 소개

그 밖의 질문은 connectome@snu.ac.kr 로 이메일 주시면 사람이 답해 드립니다.`;

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

function findAnswer(query: string): string {
  const lower = query.toLowerCase();
  if (/(mamba|뉴로맘바|fmri)/.test(lower)) return PRESET_KNOWLEDGE.neuromamba;
  if (/(diver|eeg|다이버)/.test(lower)) return PRESET_KNOWLEDGE.diver0;
  if (/(neuro-x|lbm|파운데이션|foundation)/.test(lower)) return PRESET_KNOWLEDGE.neurox;
  if (/(qml|양자|quantum)/.test(lower)) return PRESET_KNOWLEDGE.qml;
  if (/(지원|인턴|입학|대학원|apply)/.test(lower)) return PRESET_KNOWLEDGE.admission;
  if (/(문화|파티|해커톤|분위기|culture)/.test(lower)) return PRESET_KNOWLEDGE.culture;
  if (/(차지욱|교수|pi)/.test(lower)) return PRESET_KNOWLEDGE.pi;
  return FALLBACK;
}

const SUGGESTIONS = [
  { label: '🧠 NeuroMamba', query: 'NeuroMamba가 무엇인가요?' },
  { label: '⚡ DIVER-0 (EEG)', query: 'DIVER-0 EEG 모델 설명해줘' },
  { label: '🎓 지원 안내', query: '대학원 지원 방법' },
  { label: '🎨 연구실 문화', query: '연구실 문화가 궁금해요' },
];

export default function AskLabAI() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'guide',
      text: '안녕하세요! 커넥톰 연구실 안내입니다. 연구실이 미리 정리해 둔 FAQ에서 답을 찾아 보여드려요. 대표 연구(NeuroMamba, DIVER-0, Neuro-X), 대학원·인턴 지원, 연구실 문화에 대해 물어보세요.',
    },
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
      { id: `${Date.now()}-g`, sender: 'guide', text: findAnswer(query) },
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
          <span>Lab guide · 연구실 안내</span>
        </button>
      )}

      {isOpen && (
        <div
          role="dialog"
          aria-label="Lab guide"
          className="fixed bottom-4 right-4 z-50 w-[95vw] sm:w-[420px] h-[560px] rounded-2xl bg-white border border-line flex flex-col shadow-2xl overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-300"
        >
          {/* Header */}
          <div className="px-5 py-4 bg-paper border-b border-line flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-lab-700 flex items-center justify-center text-white">
                <BookOpen className="w-4 h-4" aria-hidden="true" />
              </div>
              <div>
                <h3 className="font-semibold text-ink text-sm">Lab guide · 연구실 안내</h3>
                <p className="text-xs text-ink-faint">큐레이션된 FAQ — 실시간 AI가 아닙니다</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="w-7 h-7 rounded-full bg-white border border-line hover:bg-paper flex items-center justify-center text-ink-faint hover:text-ink transition-colors"
              aria-label="Close guide"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Suggestion chips */}
          <div className="px-4 py-2.5 bg-white border-b border-line overflow-x-auto flex gap-2">
            {SUGGESTIONS.map((s) => (
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
              Ask about the lab
            </label>
            <input
              id="lab-guide-input"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="예: 대학원 지원 방법"
              className="flex-1 bg-paper border border-line rounded-lg px-3.5 py-2.5 text-sm text-ink placeholder-ink-faint focus:border-lab-600 transition-colors"
            />
            <button
              type="submit"
              disabled={!input.trim()}
              className="w-10 h-10 rounded-lg bg-lab-700 hover:bg-lab-800 disabled:opacity-40 text-white flex items-center justify-center transition-colors shrink-0"
              aria-label="Send question"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
}
