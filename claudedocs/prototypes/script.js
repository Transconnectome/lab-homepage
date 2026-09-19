// Connectome Lab Responsive & Mobile Prototype Controller (A, B, C)

(function() {
  'use strict';

  // --- 1. Switcher Logic (A vs B vs C) ---
  const btnA = document.getElementById('btn-show-a');
  const btnB = document.getElementById('btn-show-b');
  const btnC = document.getElementById('btn-show-c');
  const btnD = document.getElementById('btn-show-d');
  const btnE = document.getElementById('btn-show-e');
  const btnF = document.getElementById('btn-show-f');
  const viewA = document.getElementById('view-option-a');
  const viewB = document.getElementById('view-option-b');
  const viewC = document.getElementById('view-option-c');
  const viewD = document.getElementById('view-option-d');
  const viewE = document.getElementById('view-option-e');
  const viewF = document.getElementById('view-option-f');
  const body = document.body;

  function switchView(opt) {
    [btnA, btnB, btnC, btnD, btnE, btnF].forEach(b => b && b.classList.remove('active'));
    [viewA, viewB, viewC, viewD, viewE, viewF].forEach(v => v && v.classList.remove('active'));

    if (opt === 'a') {
      btnA.classList.add('active');
      viewA.classList.add('active');
      body.style.background = '#080C14';
      if (typeof window.startCanvasAnimation === 'function') window.startCanvasAnimation();
    } else if (opt === 'b') {
      btnB.classList.add('active');
      viewB.classList.add('active');
      body.style.background = '#F8F9FA';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'c') {
      if (btnC) btnC.classList.add('active');
      if (viewC) viewC.classList.add('active');
      body.style.background = '#0B0F19';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'd') {
      if (btnD) btnD.classList.add('active');
      if (viewD) viewD.classList.add('active');
      body.style.background = '#0D0F14';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'e') {
      if (btnE) btnE.classList.add('active');
      if (viewE) viewE.classList.add('active');
      body.style.background = '#FAF8F5';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    } else if (opt === 'f') {
      if (btnF) btnF.classList.add('active');
      if (viewF) viewF.classList.add('active');
      body.style.background = '#F7F5F0';
      if (typeof window.stopCanvasAnimation === 'function') window.stopCanvasAnimation();
    }
  }

  if (btnA) btnA.addEventListener('click', () => switchView('a'));
  if (btnB) btnB.addEventListener('click', () => switchView('b'));
  if (btnC) btnC.addEventListener('click', () => switchView('c'));
  if (btnD) btnD.addEventListener('click', () => switchView('d'));
  if (btnE) btnE.addEventListener('click', () => switchView('e'));
  if (btnF) btnF.addEventListener('click', () => switchView('f'));

  window.addEventListener('keydown', (e) => {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if (e.key === '1') switchView('a');
    if (e.key === '2') switchView('b');
    if (e.key === '3') switchView('c');
    if (e.key === '4') switchView('d');
    if (e.key === '5') switchView('e');
    if (e.key === '6') switchView('f');
  });

  // --- 2. Option C Interactive Multi-Scale Layer Stage ---
  const scaleData = {
    'scale-2': {
      title: '4D Spatiotemporal Foundation Dynamics',
      desc: '수천 시간의 휴지기 및 자연주의 fMRI 시계열에서 신경망의 비선형 궤적을 4차원 트랜스포머(SwiFT)로 사전 학습하여 개인 뇌 식별 및 정신건강 바이오마커를 추출합니다.',
      spec1: 'SwiFT 4D / DIVER EEG',
      spec2: 'NeurIPS 2024 · ICLR 2024',
      tag: 'ACTIVE ATLAS: 4D SPATIOTEMPORAL fMRI',
      img: 'assets/mbbn-figure-2.png'
    },
    'scale-1': {
      title: 'Genomic Multi-Omics & Longitudinal Cohort',
      desc: 'ABCD 종단 코호트(N=11,875)를 기반으로 다유전자 위험 점수(PRS)와 가정·학교·이웃 환경 지표가 뇌 발달 궤적에 미치는 복합적 인과 경로를 규명합니다.',
      spec1: 'Polygenic Risk Scores (PRS)',
      spec2: 'N=11,875 ABCD Study',
      tag: 'ACTIVE ATLAS: MULTI-OMICS × COHORT',
      img: 'assets/mbbn-figure-2.png'
    },
    'scale-3': {
      title: 'Quantum Topology & Cortical Morphology',
      desc: 'Glasser 360 영역 기반 고해상도 피질 두께 데이터와 양자 상태 커널(Quantum State Kernels)을 결합하여 고전 알고리즘을 뛰어넘는 위상수학적 연결성을 탐색합니다.',
      spec1: 'Quantum Kernels / TDA',
      spec2: 'Glasser 360 Parcellation',
      tag: 'ACTIVE ATLAS: CORTICAL TOPOLOGY',
      img: 'assets/cortical-surface.png'
    },
    'scale-4': {
      title: 'Cognitive Dynamics, Awe & Aesthetic Science',
      desc: '인간이 예술, 자연, 내러티브에 몰입할 때 일어나는 "경외감(Awe)"의 신경 메커니즘과 기본모드신경망(DMN)의 다이내믹한 재조직 과정을 실시간으로 추적합니다.',
      spec1: 'Naturalistic fMRI / EEG',
      spec2: 'Awe & Emotional Dynamics',
      tag: 'ACTIVE ATLAS: AESTHETIC COGNITION',
      img: 'assets/cortical-surface.png'
    }
  };

  const scaleTabs = document.querySelectorAll('.opt-c-scale-tab');
  const stageImg = document.getElementById('opt-c-stage-img');
  const stageTag = document.getElementById('opt-c-stage-tag');
  const stageTitle = document.getElementById('opt-c-stage-title');
  const stageDesc = document.getElementById('opt-c-stage-desc');
  const stageSpec1 = document.getElementById('opt-c-spec-1');
  const stageSpec2 = document.getElementById('opt-c-spec-2');

  scaleTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      scaleTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const scaleKey = tab.getAttribute('data-scale');
      const data = scaleData[scaleKey];
      if (!data) return;

      if (stageImg) {
        stageImg.style.opacity = '0.3';
        setTimeout(() => {
          stageImg.src = data.img;
          stageImg.style.opacity = '1';
        }, 150);
      }
      if (stageTag) stageTag.textContent = data.tag;
      if (stageTitle) stageTitle.textContent = data.title;
      if (stageDesc) stageDesc.textContent = data.desc;
      if (stageSpec1) stageSpec1.textContent = data.spec1;
      if (stageSpec2) stageSpec2.textContent = data.spec2;
    });
  });

  // --- 3. Desktop Phone Simulator Toggle ---
  const btnResp = document.getElementById('btn-mode-responsive');
  const btnSim = document.getElementById('btn-mode-simulator');
  const wrapper = document.getElementById('main-viewport-wrapper');

  if (btnResp && btnSim && wrapper) {
    btnResp.addEventListener('click', () => {
      btnResp.classList.add('active');
      btnSim.classList.remove('active');
      const simContainer = document.getElementById('simulator-container');
      if (simContainer) {
        const phoneScreen = simContainer.querySelector('.phone-screen');
        while (phoneScreen.firstChild) {
          wrapper.appendChild(phoneScreen.firstChild);
        }
        simContainer.remove();
      }
      wrapper.style.display = 'block';
      if (window.resizeCanvas) window.resizeCanvas();
    });

    btnSim.addEventListener('click', () => {
      btnSim.classList.add('active');
      btnResp.classList.remove('active');
      if (document.getElementById('simulator-container')) return;

      const sim = document.createElement('div');
      sim.id = 'simulator-container';
      sim.innerHTML = `
        <div class="phone-frame">
          <div class="phone-notch"><div class="phone-camera"></div></div>
          <div class="phone-screen"></div>
        </div>
      `;
      document.body.appendChild(sim);
      const phoneScreen = sim.querySelector('.phone-screen');
      while (wrapper.firstChild) {
        phoneScreen.appendChild(wrapper.firstChild);
      }
      wrapper.style.display = 'none';
      if (window.resizeCanvas) window.resizeCanvas();
    });
  }

  // --- 4. Interactive Canvas Synaptic Graph with Touch Support ---
  const canvas = document.getElementById('neural-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    let animationFrameId;
    let isRunning = false;
    const mouse = { x: -1000, y: -1000, radius: 140 };

    function resize() {
      const parent = canvas.parentElement;
      if (!parent) return;
      const rect = parent.getBoundingClientRect();
      width = canvas.width = rect.width;
      height = canvas.height = rect.height;
    }

    window.addEventListener('resize', resize);
    window.resizeCanvas = resize;
    resize();

    window.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    });

    window.addEventListener('mouseleave', () => {
      mouse.x = -1000;
      mouse.y = -1000;
    });

    window.addEventListener('touchstart', (e) => {
      if (e.touches && e.touches[0]) {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.touches[0].clientX - rect.left;
        mouse.y = e.touches[0].clientY - rect.top;
      }
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
      if (e.touches && e.touches[0]) {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.touches[0].clientX - rect.left;
        mouse.y = e.touches[0].clientY - rect.top;
      }
    }, { passive: true });

    window.addEventListener('touchend', () => {
      mouse.x = -1000;
      mouse.y = -1000;
    });

    const NODE_COUNT = Math.min(50, Math.max(25, Math.floor(window.innerWidth / 24)));
    const nodes = [];

    for (let i = 0; i < NODE_COUNT; i++) {
      nodes.push({
        x: Math.random() * (width || 800),
        y: Math.random() * (height || 600),
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 1.8 + 1.2,
        baseAlpha: Math.random() * 0.5 + 0.3,
        pulse: Math.random() * Math.PI * 2
      });
    }

    function draw() {
      if (!isRunning) return;
      ctx.clearRect(0, 0, width, height);

      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i];
        n.x += n.vx;
        n.y += n.vy;
        n.pulse += 0.03;

        if (n.x < 0 || n.x > width) n.vx *= -1;
        if (n.y < 0 || n.y > height) n.vy *= -1;

        const dxMouse = mouse.x - n.x;
        const dyMouse = mouse.y - n.y;
        const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
        if (distMouse < mouse.radius) {
          const force = (1 - distMouse / mouse.radius) * 0.8;
          n.x += (dxMouse / distMouse) * force * 1.4;
          n.y += (dyMouse / distMouse) * force * 1.4;

          ctx.beginPath();
          ctx.moveTo(n.x, n.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(0, 242, 254, ${(1 - distMouse / mouse.radius) * 0.4})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }

        const currentAlpha = n.baseAlpha + Math.sin(n.pulse) * 0.2;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 242, 254, ${Math.max(0.1, currentAlpha)})`;
        ctx.shadowBlur = 6;
        ctx.shadowColor = '#00F2FE';
        ctx.fill();
        ctx.shadowBlur = 0;

        for (let j = i + 1; j < nodes.length; j++) {
          const m = nodes[j];
          const dx = n.x - m.x;
          const dy = n.y - m.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 110) {
            const alpha = (1 - dist / 110) * 0.22;
            ctx.beginPath();
            ctx.moveTo(n.x, n.y);
            ctx.lineTo(m.x, m.y);
            ctx.strokeStyle = `rgba(100, 150, 255, ${alpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }

      animationFrameId = requestAnimationFrame(draw);
    }

    window.startCanvasAnimation = function() {
      if (!isRunning) {
        isRunning = true;
        draw();
      }
    };

    window.stopCanvasAnimation = function() {
      isRunning = false;
      cancelAnimationFrame(animationFrameId);
    };

    window.startCanvasAnimation();
  }

  // --- 5. Option B Live Clock ---
  const clockEl = document.getElementById('live-utc-clock');
  function updateClock() {
    if (!clockEl) return;
    const now = new Date();
    const utcStr = now.toUTCString().split(' ')[4];
    clockEl.textContent = `UTC ${utcStr}`;
  }
  setInterval(updateClock, 1000);
  updateClock();

  // --- 6. Option A Pillar Cards ---
  const pillarCards = document.querySelectorAll('.opt-a-pillar-card');
  pillarCards.forEach(card => {
    card.addEventListener('click', () => {
      pillarCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
    });
  });

  // --- 7. BibTeX Instant Copy & Toast ---
  const toast = document.getElementById('toast');
  const bibData = {
    mbbn2025: `@article{lee2025multiscale,
  title={Multi-scale biological networks encode adolescent mental health dynamics},
  author={Lee, Ahhyun and Wang, Heehwan and Cha, Jiook},
  journal={Nature Communications},
  year={2025}
}`,
    natcomms25: `@article{lee2025multiscale,
  title={Multi-scale biological networks encode adolescent mental health dynamics},
  author={Lee, Ahhyun and Wang, Heehwan and Cha, Jiook},
  journal={Nature Communications},
  year={2025}
}`,
    neurips24: `@inproceedings{wang2024swift,
  title={SwiFT: Swin 4D fMRI Transformer for Spatiotemporal Brain Representation},
  author={Wang, Heehwan and Park, David Keetae and Cha, Jiook},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  year={2024}
}`
  };

  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2200);
  }

  document.querySelectorAll('.copy-bib-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const bibKey = btn.getAttribute('data-bib');
      const text = bibData[bibKey] || bibData['natcomms25'];
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          showToast('✓ BibTeX Copied to Clipboard');
        }).catch(() => {
          showToast('✓ BibTeX Copied');
        });
      } else {
        showToast('✓ BibTeX Copied');
      }
    });
  });


  // --- 8. Option D Interactive Dialectic Chamber & Prediction Error Slider ---
  const dPhaseData = {
    p1: {
      phase: 'PHASE I · ARCHITECTURE',
      badge: 'PHASE 01: THE BIOLOGICAL KEYS',
      title: '유한한 건반과 11,875개의 생애 악보',
      quote: '“피아노 건반의 수는 유한하지만, 시간 속에서 배열될 때 천문학적인 멜로디를 낳는다. 우리는 인간을 기계 부품으로 환원하지 않고, 그 건반의 물리학을 해독한다.”',
      desc: '인간의 뇌는 100조 개의 시냅스 연결망과 유전체(PRS)라는 생물학적 기저를 가지고 태어납니다. ABCD 연구의 11,875명 청소년 종단 뇌 영상과 다층적 생물학 네트워크는 환경과의 상호작용 속에서 고통과 회복탄력성이 어떻게 발현되는지를 추적합니다.',
      meta1: 'Nature Communications (2025)',
      meta2: 'Multi-scale Biological Networks',
      img: 'assets/mbbn-figure-2.png'
    },
    p2: {
      phase: 'PHASE II · PREPLAY DYNAMICS',
      badge: 'PHASE 02: THE 4D INTERNAL TRAJECTORY',
      title: '어둠 속에서 연주되는 사전 재생(Preplay)의 선율',
      quote: '“뇌는 세상의 자극이 들어오기 전에 이미 꿈속에서 가설의 궤적을 재생(Preplay)하고 있었다. 우리는 시간 축을 복원하여 이 자발적 멜로디를 포착한다.”',
      desc: '수천 시간의 fMRI 시계열에서 신경망의 비선형 궤적을 4차원 트랜스포머(SwiFT)로 사전 학습합니다. 뇌는 세상을 수동적으로 찍는 카메라가 아니라, 끊임없이 내부 모델을 세계에 쏘아 올리는 프로젝터입니다.',
      meta1: 'NeurIPS 2024 Spotlight',
      meta2: 'SwiFT 4D Transformer / DIVER EEG',
      img: 'assets/cortical-surface.png'
    },
    p3: {
      phase: 'PHASE III · THE FRACTURE',
      badge: 'PHASE 03: PREDICTION ERROR & SURPRISE',
      title: '가설이 박살 나는 순간, 배움의 화폐 획득',
      quote: '“오차가 발생하지 않는다면 뇌는 단 1바이트도 배우지 못한다. 내 가설과 세계가 어긋나 산산조각 나는 고통의 순간에만 정밀 신경망(Precision Brain)이 깨어난다.”',
      desc: '우리가 보는 현실은 통제된 환각(Controlled Hallucination)입니다. 행동을 통해 세계와 부딪히고, 오차가 발생할 때에만 뇌는 비로소 세계에 대한 지도를 업데이트합니다. 예측 오차 0은 학습의 종말이자 뇌의 퇴화입니다.',
      meta1: 'Predictive Processing Engine',
      meta2: 'Mismatch Negativity / Dopaminergic RPE',
      img: 'assets/mbbn-figure-2.png'
    },
    p4: {
      phase: 'PHASE IV · THE SUBLIME',
      badge: 'PHASE 04: TRANSCENDENT AWE & THE SOUL',
      title: '2×2=4를 넘어선 경외와 실존적 영혼',
      quote: '“인간은 피아노 건반이 아니다. 그러나 그 건반의 물리를 이해할 때 비로소 우리는 왜 인간이 예술에 전율하고, 타인의 슬픔에 울며, 숭고한 경외(Awe)에 도달하는지 알 수 있다.”',
      desc: '자연주의적 영화, 음악, 문학에 몰입할 때 일어나는 기본모드신경망(DMN)의 해체와 재조직을 실시간으로 추적합니다. 과학적 결정론의 가장 깊은 밑바닥에서 비로소 피어나는 인간 영혼의 찬란한 존엄성을 응시합니다.',
      meta1: 'Neuroaesthetics & Awe Dynamics',
      meta2: 'Naturalistic fMRI / DMN Topography',
      img: 'assets/cortical-surface.png'
    }
  };

  const dPhaseBtns = document.querySelectorAll('.opt-d-dialectic-btn');
  const dStageImg = document.getElementById('opt-d-stage-img');
  const dStageBadge = document.getElementById('opt-d-stage-badge');
  const dStagePhase = document.getElementById('opt-d-stage-phase');
  const dStageTitle = document.getElementById('opt-d-stage-title');
  const dStageQuote = document.getElementById('opt-d-stage-quote');
  const dStageDesc = document.getElementById('opt-d-stage-desc');
  const dStageMeta1 = document.getElementById('opt-d-stage-meta1');
  const dStageMeta2 = document.getElementById('opt-d-stage-meta2');

  dPhaseBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      dPhaseBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const phaseKey = btn.getAttribute('data-d-phase');
      const data = dPhaseData[phaseKey];
      if (!data) return;

      if (dStageImg) {
        dStageImg.style.opacity = '0.2';
        setTimeout(() => {
          dStageImg.src = data.img;
          dStageImg.style.opacity = '1';
        }, 150);
      }
      if (dStageBadge) dStageBadge.textContent = data.badge;
      if (dStagePhase) dStagePhase.textContent = data.phase;
      if (dStageTitle) dStageTitle.textContent = data.title;
      if (dStageQuote) dStageQuote.textContent = data.quote;
      if (dStageDesc) dStageDesc.textContent = data.desc;
      if (dStageMeta1) dStageMeta1.textContent = data.meta1;
      if (dStageMeta2) dStageMeta2.textContent = data.meta2;
    });
  });

  // Prediction Error Interactive Slider
  const errSlider = document.getElementById('opt-d-error-slider');
  const sliderValText = document.getElementById('opt-d-slider-val-text');
  const gymBadge = document.getElementById('opt-d-gym-badge');
  const gymTitle = document.getElementById('opt-d-gym-title');
  const gymQuote = document.getElementById('opt-d-gym-quote');
  const gymFactNeural = document.getElementById('opt-d-gym-fact-neural');
  const gymFactHuman = document.getElementById('opt-d-gym-fact-human');

  if (errSlider) {
    errSlider.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      if (val < 30) {
        sliderValText.textContent = `${val}% (안전한 맹신과 권태)`;
        gymBadge.textContent = 'PREDICTION ERROR = 0% · COGNITIVE STAGNATION';
        gymTitle.textContent = '안전한 독단: 배움 0 = 뇌의 퇴화';
        gymQuote.textContent = '“수정궁 안에서 모든 것이 계산되었을 때 인간은 권태로 죽어간다. 가설 없이 답만 받아쓰는 뇌는 단 1바이트도 업데이트되지 않는다.”';
        gymFactNeural.textContent = 'Precision Brain 0% 가동. 도파민성 예측오차 신호 침묵. 시냅스 가소성(LTP) 정체.';
        gymFactHuman.textContent = '도스토옙스키의 경고: 인간이 피아노 건반이나 톱니바퀴로 환원되어 자율적 질문을 멈춘 상태.';
      } else if (val <= 75) {
        sliderValText.textContent = `${val}% (최적의 불일치와 각성)`;
        gymBadge.textContent = `OPTIMAL PREDICTION ERROR · ${val}%`;
        gymTitle.textContent = '최적의 불일치: 배움의 화폐 획득';
        gymQuote.textContent = '“어둠 속에서 문 손잡이가 예상보다 5cm 옆에 있을 때, 그 어긋남의 순간 뇌는 가장 눈부시게 업데이트된다. 가설이 어긋나야만 뇌의 정밀 신경망(Precision Brain)이 깨어난다.”';
        gymFactNeural.textContent = '도파민성 예측오차(RPE) 급증. 80~90%의 침묵하던 Precision Brain 뉴런이 전면 동원되어 내부 지도를 재구성.';
        gymFactHuman.textContent = '질문을 던지는 행동만이 유일한 학습이다. 통제된 환각이 현실과 부딪혀 새로운 의식이 탄생하는 지점.';
      } else {
        sliderValText.textContent = `${val}% (존재론적 경외와 충격)`;
        gymBadge.textContent = `RADICAL PREDICTION ERROR · ${val}%`;
        gymTitle.textContent = '실존적 경외: 세계 모델의 전면적 해체';
        gymQuote.textContent = '“고통과 경외야말로 의식의 유일한 원천이다. 거대한 예술과 실존적 충격 앞에서 나의 낡은 자아가 산산조각 날 때 영혼은 비로소 자유로워진다.”';
        gymFactNeural.textContent = '기본모드신경망(DMN)의 탈동기화(Ego Dissolution). 전두-두정 주의 집중 네트워크의 전면적 재편.';
        gymFactHuman.textContent = '지하생활자의 절규와 초월. 2×2=4의 차가운 수식을 넘어선 인간 존엄과 숭고미의 경험.';
      }
    });
  }


  // --- 9. Option F Soft Interactive Filters ---
  const fFilterPills = document.querySelectorAll('.opt-f-filter-pill');
  const fAxisCards = document.querySelectorAll('.opt-f-axis-card');

  fFilterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      fFilterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const filter = pill.getAttribute('data-f-filter');
      fAxisCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-f-axis') === filter) {
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
          card.style.display = 'flex';
        } else {
          card.style.opacity = '0.35';
          card.style.transform = 'translateY(2px)';
          card.style.display = 'flex';
        }
      });
    });
  });

})();
