import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, X, Bot } from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'ai' | 'user';
  text: string;
  timestamp: string;
}

const PRESET_KNOWLEDGE: Record<string, string> = {
  neuromamba: `**NeuroMamba**는 서울대학교 커넥톰 연구실(최주빈 학생, 차지욱 교수 등)이 개발한 **4D fMRI용 상태 공간 기반 파운데이션 모델(State-Space Foundation Model)**입니다 (NeurIPS 2025 Spotlight 선정).

- **핵심 특징**: 기존 트랜스포머의 $O(N^2)$ 계산 복잡도를 선형 시간 복잡도($O(N)$)로 줄여, 수천 타임스텝의 긴 4D 뇌영상 전체를 손실 없이 효율적으로 모델링합니다.
- **의의**: 대규모 fMRI 코호트에서 뇌 역동성을 선험적으로 학습하여 다양한 인지 기능 디코딩 및 정신질환 예측에서 SOTA 성능을 입증했습니다.`,

  diver0: `**DIVER-0**는 커넥톰 연구실(한동엽, 이세빈 학생 등)이 제안한 **완전 채널 동변(Channel-Equivariant) EEG 파운데이션 모델**입니다 (ICML 2025 GenBio Spotlight 선정).

- **문제 해결**: 전 세계 병원 및 연구소마다 서로 다른 EEG 전극 배치(8~256채널)로 인해 발생하는 데이터 불일치 문제를 해결했습니다.
- **기술**: 전극 위치를 연속적인 3D 공간 좌표 포인트 클라우드로 취급하여 공간적 기하 대칭성을 보존하며 Zero-shot 전이를 달성했습니다.`,

  neurox: `**Neuro-X 프로젝트**는 차지욱 교수 연구팀이 주도하는 **대규모 뇌 파운데이션 모델(Large Brain Model, LBM)** 연구 이니셔티브입니다.

- **비전**: LLM이 언어를 이해하듯, 대규모 다중모달 뇌 데이터(fMRI, EEG, dMRI, 유전체)를 사전학습하여 마음과 행동의 보편적 신경 문법을 해독합니다.
- **이론적 토대**: György Buzsáki 교수의 'Inside-Out' 신경과학 프레임워크를 기반으로 뇌의 능동적 예측 및 시공간 역동성을 모델링합니다.`,

  qml: `커넥톰 연구실에서는 **양자 머신러닝(Quantum Machine Learning, QML)**을 고차원 뇌 커넥톰 데이터에 접목하는 선도적 연구를 진행하고 있습니다.

- **연구 주제**: 파라미터화된 양자 회로(PQC)와 양자 커널(Quantum Kernels)을 활용한 뇌 연결성 그래프 분류 및 복잡도 극복.
- **인턴십**: 양자 컴퓨팅(Qiskit, PennyLane)과 뇌과학/AI에 열정이 있는 학부 및 대학원 연구 인턴을 상시 모집하고 있습니다.`,

  admission: `**커넥톰 연구실 대학원 및 인턴 지원 안내**:

- **전공 트랙**:
  1. 서울대학교 심리학과 (대학원)
  2. 협동과정 인공지능 전공 (GSAI)
  3. 뇌인지과학과 (BCS)
- **우대 배경**: 컴퓨터공학, 인공지능, 통계학, 심리학, 의학, 물리학, 생명과학 등 다학제적 융합에 열정적인 학생
- **지원 방법**: 관심 연구 분야, CV, 성적증명서를 첨부하여 \`connectome@snu.ac.kr\`로 이메일을 보내주시면 친절히 상담해 드립니다.`,

  culture: `**커넥톰 연구실 문화 (Lab Culture)**:

- 🏔️ **연구 해커톤**: 강원도 홍천 소노펠리체 등에서 정기적으로 집중 4박 5일 해커톤 진행 (연구 몰입 + 요리/게임!).
- 🌍 **글로벌 해외 연수**: 캐나다 MILA 인공지능 연구소, 미국 브룩헤이븐 국립연구소(BNL) 등과 긴밀한 연구원 파견 및 공동 연구.
- 🍷 **예술과 삶의 즐거움**: 교수님의 시그니처 칵테일 바, 음악, 막걸리, 다학제 예술 전시(옵/신 포커스) 등 창의적이고 유쾌한 분위기!`
};

export default function AskLabAI() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'ai',
      text: '안녕하세요! 서울대학교 커넥톰 연구실(Connectome Lab)의 AI 도우미입니다. 연구실의 대표 연구(NeuroMamba, Neuro-X, DIVER-0), 유전체-뇌영상 연구, 양자 머신러닝(QML) 및 인턴/대학원 지원에 대해 무엇이든 물어보세요!',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSend = (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setIsTyping(true);

    // AI Response generation logic
    setTimeout(() => {
      let responseText = '';
      const lower = query.toLowerCase();

      if (lower.includes('mamba') || lower.includes('뉴로맘바') || lower.includes('fmri')) {
        responseText = PRESET_KNOWLEDGE.neuromamba;
      } else if (lower.includes('diver') || lower.includes('eeg') || lower.includes('다이버')) {
        responseText = PRESET_KNOWLEDGE.diver0;
      } else if (lower.includes('neuro-x') || lower.includes('lbm') || lower.includes('파운데이션') || lower.includes('foundation')) {
        responseText = PRESET_KNOWLEDGE.neurox;
      } else if (lower.includes('qml') || lower.includes('양자') || lower.includes('quantum')) {
        responseText = PRESET_KNOWLEDGE.qml;
      } else if (lower.includes('지원') || lower.includes('인턴') || lower.includes('입학') || lower.includes('대학원') || lower.includes('apply')) {
        responseText = PRESET_KNOWLEDGE.admission;
      } else if (lower.includes('문화') || lower.includes('파티') || lower.includes('해커톤') || lower.includes('분위기') || lower.includes('culture')) {
        responseText = PRESET_KNOWLEDGE.culture;
      } else if (lower.includes('차지욱') || lower.includes('교수') || lower.includes('pi')) {
        responseText = `**차지욱 교수 (Jiook Cha, PhD)**는 서울대학교 심리학과, 인공지능협동과정, 뇌인지과학과 부교수이자 커넥톰 연구실의 PI입니다.

- 미국 컬럼비아 대학교(Columbia University) 아동청소년정신의학과 조교수 및 데이터사이언스 연구소(DSI) 멤버를 역임했습니다.
- 미국 국립정신건강연구소(NIMH) K01 커리어 개발상, NARSAD Young Investigator Award, 서울대 창의선도연구자 등을 수상했습니다.
- 연구 분야: 대규모 뇌 파운데이션 모델(Neuro-X), 동적 커넥톰, 계산정신의학, 다중오믹스 유전체-뇌영상 융합, 양자 머신러닝.`;
      } else {
        responseText = `커넥톰 연구실에 대한 질문 감사합니다!
서울대 커넥톰랩(PI 차지욱)은 **대규모 뇌 파운데이션 모델(Neuro-X, NeuroMamba, DIVER-0)**, **다중오믹스 유전체와 뇌연결성(PRS & fMRI/dMRI)**, **양자 머신러닝(QML)** 등 최첨단 융합 뇌과학-AI 연구를 수행하고 있습니다.

더 자세한 정보는 다음 키워드로 질문해보세요:
- ▹ **"NeuroMamba가 무엇인가요?"**
- ▹ **"DIVER-0 EEG 모델 설명해줘"**
- ▹ **"인턴 및 대학원 지원 자격"**
- ▹ **"양자머신러닝(QML) 연구"**
- ▹ **"연구실 문화와 해외 연수"**`;
      }

      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: responseText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, aiMsg]);
      setIsTyping(false);
    }, 600);
  };

  return (
    <>
      {/* Floating Launcher Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 flex items-center gap-2.5 px-4 py-3 rounded-full bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 text-white font-medium text-sm shadow-xl hover:shadow-cyan-500/25 hover:scale-105 transition-all duration-300 border border-white/20"
        >
          <Sparkles className="w-4 h-4 animate-spin text-cyan-200" style={{ animationDuration: '6s' }} />
          <span>Ask Connectome AI</span>
        </button>
      )}

      {/* Chat Window Modal */}
      {isOpen && (
        <div className="fixed bottom-4 right-4 z-50 w-[95vw] sm:w-[420px] h-[580px] rounded-3xl glass-panel border border-cyan-500/30 flex flex-col shadow-2xl overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-300">
          {/* Header */}
          <div className="px-5 py-4 bg-slate-900/90 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-500 flex items-center justify-center text-white shadow-lg">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-white text-sm flex items-center gap-2">
                  Connectome AI Copilot
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                </h3>
                <p className="text-[11px] text-slate-400">SNU Connectome Lab Intelligence</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="w-7 h-7 rounded-full bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-400 hover:text-white transition text-xs"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Quick Suggestions Chips */}
          <div className="px-4 py-2 bg-slate-950/60 border-b border-slate-800/60 overflow-x-auto flex gap-2 no-scrollbar">
            <button
              onClick={() => handleSend('NeuroMamba fMRI 연구 알려줘')}
              className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-800/80 hover:bg-cyan-900/50 hover:text-cyan-300 text-slate-300 border border-slate-700 transition"
            >
              🧠 NeuroMamba
            </button>
            <button
              onClick={() => handleSend('DIVER-0 EEG 모델 설명해줘')}
              className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-800/80 hover:bg-cyan-900/50 hover:text-cyan-300 text-slate-300 border border-slate-700 transition"
            >
              ⚡ DIVER-0 (EEG)
            </button>
            <button
              onClick={() => handleSend('양자머신러닝(QML) 인턴십')}
              className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-800/80 hover:bg-cyan-900/50 hover:text-cyan-300 text-slate-300 border border-slate-700 transition"
            >
              ⚛️ QML 인턴십
            </button>
            <button
              onClick={() => handleSend('대학원 지원 방법')}
              className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-800/80 hover:bg-cyan-900/50 hover:text-cyan-300 text-slate-300 border border-slate-700 transition"
            >
              🎓 지원 안내
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3.5 text-xs">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-2.5 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.sender === 'ai' && (
                  <div className="w-6 h-6 rounded-lg bg-cyan-600/30 border border-cyan-500/40 flex items-center justify-center shrink-0 text-cyan-300 mt-0.5">
                    <Bot className="w-3.5 h-3.5" />
                  </div>
                )}
                <div
                  className={`max-w-[82%] p-3 rounded-2xl leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-tr-sm'
                      : 'bg-slate-800/90 text-slate-200 border border-slate-700/60 rounded-tl-sm shadow-md'
                  }`}
                >
                  <div className="whitespace-pre-line">{msg.text}</div>
                  <div
                    className={`text-[9px] mt-1 text-right ${
                      msg.sender === 'user' ? 'text-blue-200' : 'text-slate-500'
                    }`}
                  >
                    {msg.timestamp}
                  </div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex items-center gap-2 text-slate-400 text-xs pl-8">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                <span className="text-[11px] text-slate-500 ml-1">Connectome AI is thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="p-3 bg-slate-900/95 border-t border-slate-800 flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about research, papers, internships..."
              className="flex-1 bg-slate-950/80 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition"
            />
            <button
              type="submit"
              disabled={!input.trim()}
              className="w-8 h-8 rounded-xl bg-cyan-500 hover:bg-cyan-400 disabled:opacity-40 disabled:hover:bg-cyan-500 text-slate-950 flex items-center justify-center transition shrink-0"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
}
