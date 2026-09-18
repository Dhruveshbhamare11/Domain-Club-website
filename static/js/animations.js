/* ─────────────────────────────────────────────────────
   DOMAIN MATH CLUB — Fun Doodle Animations Engine
   Sketch portal · Doodle particles · Bouncy reveals
   Sticker effects · Rubber-band interactions
   ───────────────────────────────────────────────────── */

(function () {
  "use strict";

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 1. 3D MATHEMATICIANS MULTIVERSE ENTRANCE
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  const PORTAL_DURATION = 6000;
  const SYMBOLS = ["π", "∑", "∞", "√", "∫", "Δ", "θ", "λ", "∂", "φ", "+", "=", "×", "÷", "≠", "≈", "²", "³", "%", "∇", "e", "i"];
  const COLORS = ["#4ec5f1", "#f28c28", "#6abf4b", "#f472b6", "#fb7756", "#a78bfa", "#fcd34d"];

  const MATHEMATICIANS = [
    {
      id: "einstein",
      name: "Albert Einstein",
      era: "1879–1955",
      formula: "E = mc²",
      quote: "Imagination is more important than knowledge! ⚡",
      img: "/static/images/mathematicians/einstein.jpg",
      toy: "π",
      color: "#a78bfa"
    },
    {
      id: "newton",
      name: "Isaac Newton",
      era: "1643–1727",
      formula: "Calculus & Gravity",
      quote: "What goes up must come down (d²y/dt² = -g)! 🍎",
      img: "/static/images/mathematicians/newton.jpg",
      toy: "🍎",
      color: "#4ec5f1"
    },
    {
      id: "ramanujan",
      name: "S. Ramanujan",
      era: "1887–1920",
      formula: "1+2+3+... = -1/12",
      quote: "Equations express thoughts of God in dreams! ✨",
      img: "/static/images/mathematicians/ramanujan.jpg",
      toy: "∞",
      color: "#f28c28"
    },
    {
      id: "euler",
      name: "Leonhard Euler",
      era: "1707–1783",
      formula: "e^(iπ) + 1 = 0",
      quote: "The most beautiful equation in mathematics! ☕",
      img: "/static/images/mathematicians/euler.jpg",
      toy: "e",
      color: "#6abf4b"
    },
    {
      id: "pythagoras",
      name: "Pythagoras",
      era: "c. 570–495 BC",
      formula: "a² + b² = c²",
      quote: "All is number! And hypotenuse reigns supreme! 📐",
      img: "/static/images/mathematicians/pythagoras.jpg",
      toy: "📐",
      color: "#fb7756"
    }
  ];

  let portalTimerInterval = null;

  function shouldShowPortal() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return false;
    // Check if replay requested via hash or if first time in session
    if (window.location.hash === "#intro" || window.location.search.includes("intro=1")) return true;
    return !sessionStorage.getItem("mathclub_intro_seen");
  }

  function createPortal() {
    // Remove any existing portal first
    const existing = document.getElementById("entrance-portal");
    if (existing) existing.remove();
    const existingBtn = document.querySelector(".skip-intro");
    if (existingBtn) existingBtn.remove();
    if (portalTimerInterval) clearInterval(portalTimerInterval);

    if (!shouldShowPortal()) {
      document.documentElement.classList.remove("portal-open");
      document.body.classList.remove("portal-open", "page-hidden");
      return;
    }

    document.documentElement.classList.add("portal-open");
    document.body.classList.add("portal-open", "page-hidden");

    const portal = document.createElement("div");
    portal.className = "entrance-portal";
    portal.id = "entrance-portal";

    // 1. 3D Backdrop with rotating coordinate grid & rings
    const backdrop = document.createElement("div");
    backdrop.className = "portal-backdrop";
    backdrop.innerHTML = '<div class="portal-grid-3d"></div><div class="portal-rings"></div>';
    portal.appendChild(backdrop);

    // 2. Scatter 3D floating mathematical glyphs (reduced count on mobile for smooth GPU performance)
    const glyphCount = window.innerWidth < 768 ? 10 : 20;
    for (let i = 0; i < glyphCount; i++) {
      const sym = document.createElement("span");
      sym.className = "portal-symbol";
      sym.textContent = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
      sym.style.left = Math.random() * 90 + 5 + "%";
      sym.style.top = Math.random() * 90 + 5 + "%";
      sym.style.fontSize = (Math.random() * 2 + 1) + "rem";
      sym.style.animationDelay = (Math.random() * 0.8) + "s";
      sym.style.animationDuration = (3 + Math.random() * 2.5) + "s";
      sym.style.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      sym.style.transform = `rotate(${Math.random() * 50 - 25}deg)`;
      portal.appendChild(sym);
    }

    // 3. Central 3D Content Container
    const content = document.createElement("div");
    content.className = "portal-content";

    // Badge
    const badge = document.createElement("div");
    badge.className = "portal-badge";
    badge.textContent = "⚡ THE MATHEMATICS MULTIVERSE ⚡";
    content.appendChild(badge);

    // Title
    const title = document.createElement("h1");
    title.className = "portal-title";
    title.textContent = "DBIT DOMAIN MATH CLUB";
    content.appendChild(title);

    // Subtitle
    const subtitle = document.createElement("div");
    subtitle.className = "portal-subtitle";
    subtitle.textContent = "✨ 5 Legends. Infinite Dimensions. ✨";
    content.appendChild(subtitle);

    // 4. 3D Mathematicians Stage
    const stage = document.createElement("div");
    stage.className = "mathematicians-stage";

    MATHEMATICIANS.forEach((m) => {
      const card = document.createElement("div");
      card.className = "math-legend-card";
      card.title = `Click to hear from ${m.name}!`;

      // Speech bubble
      const speech = document.createElement("div");
      speech.className = "math-card-speech";
      speech.textContent = m.quote;
      card.appendChild(speech);

      // Floating math toy badge
      const toy = document.createElement("div");
      toy.className = "math-toy-badge";
      toy.textContent = m.toy;
      card.appendChild(toy);

      // Image container
      const imgWrap = document.createElement("div");
      imgWrap.className = "math-card-img-wrap";
      const img = document.createElement("img");
      img.className = "math-card-img";
      img.src = m.img;
      img.alt = m.name;
      img.loading = "eager";
      imgWrap.appendChild(img);
      card.appendChild(imgWrap);

      // Name & Formula
      const name = document.createElement("div");
      name.className = "math-legend-name";
      name.textContent = m.name;
      card.appendChild(name);

      const tag = document.createElement("div");
      tag.className = "math-legend-tag";
      tag.textContent = m.formula;
      card.appendChild(tag);

      // Interactive Click: Center Card & Trigger Tear
      card.addEventListener("click", (e) => {
        e.stopPropagation();
        
        const currentPortal = document.getElementById("entrance-portal");
        if (!currentPortal || currentPortal.dataset.tearing) return;
        currentPortal.dataset.tearing = "true";
        if (portalTimerInterval) clearInterval(portalTimerInterval);

        // 1. Bring card to front and center
        const rect = card.getBoundingClientRect();
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        
        const dx = centerX - (rect.left + rect.width / 2);
        const dy = centerY - (rect.top + rect.height / 2);
        
        card.style.transition = "transform 0.7s cubic-bezier(0.34, 1.56, 0.64, 1)";
        card.style.transform = `translate(${dx}px, ${dy}px) scale(1.6) rotate(0deg)`;
        card.style.zIndex = "1000";
        card.classList.add("active-quote");
        
        // Hide other elements
        Array.from(stage.children).forEach(c => {
          if (c !== card) c.style.opacity = "0";
        });
        const titleEl = document.querySelector(".portal-title");
        const subtitleEl = document.querySelector(".portal-subtitle");
        const badgeEl = document.querySelector(".portal-badge");
        const actionsEl = document.querySelector(".portal-actions");
        
        if (titleEl) titleEl.style.opacity = "0";
        if (subtitleEl) subtitleEl.style.opacity = "0";
        if (badgeEl) badgeEl.style.opacity = "0";
        if (actionsEl) actionsEl.style.opacity = "0";
        
        // Spawn confetti
        spawnMiniConfetti(centerX, centerY, m.toy);
        
        // 2. Tear the page after a short delay
        setTimeout(() => {
           // Slash animation
           card.style.transition = "transform 0.25s cubic-bezier(0.55, 0.085, 0.68, 0.53)";
           card.style.transform = `translate(${dx}px, ${dy + 400}px) scale(2) rotate(15deg)`;
           card.style.opacity = "0";
           
           setTimeout(() => triggerTearExit(), 200);
        }, 1200);
      });

      stage.appendChild(card);
    });

    content.appendChild(stage);

    // 5. Portal Controls (Enter Button & Countdown)
    const actions = document.createElement("div");
    actions.className = "portal-actions";

    const enterBtn = document.createElement("button");
    enterBtn.className = "portal-enter-btn";
    enterBtn.innerHTML = '<span>🚀 ENTER MATH MULTIVERSE</span>';
    enterBtn.addEventListener("click", dismissPortal);
    actions.appendChild(enterBtn);

    const countdown = document.createElement("div");
    countdown.className = "portal-countdown";
    countdown.innerHTML = 'Auto-entering in <span id="portal-sec">6</span>s <div class="portal-progress-bar"><div class="portal-progress-fill" id="portal-fill"></div></div>';
    actions.appendChild(countdown);

    content.appendChild(actions);
    portal.appendChild(content);
    document.body.prepend(portal);

    // Skip button in corner
    const skipBtn = document.createElement("button");
    skipBtn.className = "skip-intro";
    skipBtn.textContent = "Skip Intro ✖";
    skipBtn.addEventListener("click", dismissPortal);
    document.body.appendChild(skipBtn);

    // 6. Interactive 3D Mouse Parallax on Stage (desktop only)
    if (window.matchMedia("(pointer: fine)").matches) {
      portal.addEventListener("mousemove", (e) => {
        const cx = window.innerWidth / 2;
        const cy = window.innerHeight / 2;
        const tiltX = -((e.clientY - cy) / cy) * 8;
        const tiltY = ((e.clientX - cx) / cx) * 10;
        content.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
      }, { passive: true });

      portal.addEventListener("mouseleave", () => {
        content.style.transform = "rotateX(0deg) rotateY(0deg)";
      });
    }

    // 7. Countdown Timer
    let elapsed = 0;
    const intervalTime = 50;
    const fillEl = document.getElementById("portal-fill");
    const secEl = document.getElementById("portal-sec");

    portalTimerInterval = setInterval(() => {
      elapsed += intervalTime;
      const remaining = Math.max(0, PORTAL_DURATION - elapsed);
      if (secEl) secEl.textContent = Math.ceil(remaining / 1000);
      if (fillEl) fillEl.style.width = ((remaining / PORTAL_DURATION) * 100) + "%";

      if (elapsed >= PORTAL_DURATION) {
        clearInterval(portalTimerInterval);
        dismissPortal();
      }
    }, intervalTime);
  }

  function triggerTearExit() {
    const portal = document.getElementById("entrance-portal");
    if (!portal || portal.dataset.dismissed) return;
    portal.dataset.dismissed = "true";
    if (portalTimerInterval) clearInterval(portalTimerInterval);

    const skipBtn = document.querySelector(".skip-intro");
    if (skipBtn) skipBtn.remove();

    // The Flash behind the tear
    const flash = document.createElement("div");
    flash.className = "tear-flash";
    document.body.appendChild(flash);

    // Clone the portal
    const clone = portal.cloneNode(true);
    clone.id = "entrance-portal-clone";
    document.body.appendChild(clone);

    // Dynamic jagged path for tear
    let leftPath = [];
    let rightPath = [];
    const steps = 15;
    for (let i = 0; i <= steps; i++) {
      const y = (i / steps) * 100;
      let x = 50 + (Math.random() * 8 - 4);
      if (i === 0) x = 50;
      if (i === steps) x = 50;
      leftPath.push(`${x}% ${y}%`);
      rightPath.unshift(`${x}% ${y}%`);
    }
    
    const leftClip = `polygon(0 0, ${leftPath.join(', ')}, 0 100%)`;
    const rightClip = `polygon(100% 0, ${rightPath.join(', ')}, 100% 100%)`;

    portal.style.clipPath = leftClip;
    clone.style.clipPath = rightClip;

    portal.style.transition = "transform 0.9s cubic-bezier(0.55, 0.055, 0.675, 0.19), opacity 0.9s ease";
    clone.style.transition = "transform 0.9s cubic-bezier(0.55, 0.055, 0.675, 0.19), opacity 0.9s ease";

    requestAnimationFrame(() => {
      setTimeout(() => {
        portal.style.transform = "translateX(-30vw) rotate(-6deg)";
        portal.style.opacity = "0";

        clone.style.transform = "translateX(30vw) rotate(6deg)";
        clone.style.opacity = "0";
      }, 50);
    });

    sessionStorage.setItem("mathclub_intro_seen", "1");

    setTimeout(() => {
      portal.remove();
      clone.remove();
      flash.classList.add("fade-out");
      setTimeout(() => flash.remove(), 500);
      document.documentElement.classList.remove("portal-open");
      document.body.classList.remove("portal-open", "page-hidden");
      document.body.classList.add("page-reveal");
      setTimeout(() => triggerVisibleElements(), 200);
    }, 950);
  }

  function dismissPortal() {
    if (portalTimerInterval) clearInterval(portalTimerInterval);
    const portal = document.getElementById("entrance-portal");
    if (!portal || portal.dataset.dismissed) return;
    portal.dataset.dismissed = "true";

    sessionStorage.setItem("mathclub_intro_seen", "1");
    portal.classList.add("exiting");

    const skipBtn = document.querySelector(".skip-intro");
    if (skipBtn) skipBtn.remove();

    setTimeout(() => {
      portal.remove();
      document.documentElement.classList.remove("portal-open");
      document.body.classList.remove("portal-open", "page-hidden");
      document.body.classList.add("page-reveal");
      setTimeout(() => triggerVisibleElements(), 200);
    }, 850);
  }

  function spawnMiniConfetti(x, y, char) {
    const chars = [char || "✦", "★", "π", "∞", "∑", "√", "✨"];
    for (let i = 0; i < 8; i++) {
      const piece = document.createElement("span");
      piece.className = "confetti-piece";
      piece.textContent = chars[Math.floor(Math.random() * chars.length)];
      piece.style.left = x + "px";
      piece.style.top = y + "px";
      piece.style.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      piece.style.setProperty("--tx", (Math.random() - 0.5) * 180 + "px");
      piece.style.setProperty("--ty", (Math.random() - 0.5) * 180 - 40 + "px");
      piece.style.setProperty("--tr", (Math.random() * 720 - 360) + "deg");
      document.body.appendChild(piece);
      setTimeout(() => piece.remove(), 900);
    }
  }

  window.replayIntroPortal = function () {
    sessionStorage.removeItem("mathclub_intro_seen");
    createPortal();
  };

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 2. SCROLL REVEAL ENGINE
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  const REVEAL_SELECTORS = ".reveal, .reveal-left, .reveal-right, .scale-in, .stagger-item, .paper-card, .puzzle-poster, .event-poster, .article-card, .badge-sticker, .btn, .page-heading, .hero h1, .hero-copy, .hero-stamp";

  function initScrollReveals() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      document.querySelectorAll(REVEAL_SELECTORS).forEach((el) => {
        el.classList.add("visible");
      });
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const parent = el.parentElement;
            let delay = 0;

            if (parent) {
              const siblings = Array.from(parent.children).filter((c) =>
                c.matches && c.matches(REVEAL_SELECTORS)
              );
              const siblingIdx = siblings.indexOf(el);
              if (siblingIdx > 0) delay = siblingIdx * 100;
            }

            setTimeout(() => {
              el.classList.add("visible");
            }, delay);

            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -30px 0px" }
    );

    document.querySelectorAll(REVEAL_SELECTORS).forEach((el) => {
      if (!el.classList.contains("visible")) {
        observer.observe(el);
      }
    });
  }

  function triggerVisibleElements() {
    document.querySelectorAll(REVEAL_SELECTORS).forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        el.classList.add("visible");
      }
    });
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 3. DOODLE PARTICLES (Canvas)
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initParticles() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (window.innerWidth < 900 || "ontouchstart" in window) return;

    const canvas = document.createElement("canvas");
    canvas.id = "particle-canvas";
    document.body.prepend(canvas);

    const ctx = canvas.getContext("2d");
    let particles = [];
    const PARTICLE_COUNT = 16;
    const DOODLE_CHARS = ["π", "∞", "√", "∑", "+", "=", "×", "÷", "Δ", "θ", "?", "!", "∫", "²", "≈"];
    let isRunning = true;

    function resize() {
      if (window.innerWidth < 900) {
        canvas.style.display = "none";
        isRunning = false;
        return;
      }
      canvas.style.display = "block";
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      if (!isRunning) {
        isRunning = true;
        animate();
      }
    }

    function createParticle() {
      const color = COLORS[Math.floor(Math.random() * COLORS.length)];
      return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        char: DOODLE_CHARS[Math.floor(Math.random() * DOODLE_CHARS.length)],
        size: Math.random() * 18 + 12,
        speedX: (Math.random() - 0.5) * 0.25,
        speedY: (Math.random() - 0.5) * 0.2 - 0.08,
        rotation: Math.random() * Math.PI * 2,
        rotationSpeed: (Math.random() - 0.5) * 0.012,
        color: color,
        opacity: Math.random() * 0.18 + 0.06,
        wobble: Math.random() * Math.PI * 2,
        wobbleSpeed: Math.random() * 0.015 + 0.008,
      };
    }

    function init() {
      resize();
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push(createParticle());
      }
    }

    function animate() {
      if (!isRunning || document.hidden) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach((p) => {
        p.x += p.speedX + Math.sin(p.wobble) * 0.25;
        p.y += p.speedY;
        p.rotation += p.rotationSpeed;
        p.wobble += p.wobbleSpeed;

        // wrap around
        if (p.x < -40) p.x = canvas.width + 40;
        if (p.x > canvas.width + 40) p.x = -40;
        if (p.y < -40) p.y = canvas.height + 40;
        if (p.y > canvas.height + 40) p.y = -40;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.font = `bold ${p.size}px "Patrick Hand", "Indie Flower", cursive`;
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.opacity;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        ctx.strokeStyle = "rgba(45,27,0,0.12)";
        ctx.lineWidth = 1.2;
        ctx.strokeText(p.char, 0, 0);
        ctx.fillText(p.char, 0, 0);

        ctx.restore();
      });

      requestAnimationFrame(animate);
    }

    document.addEventListener("visibilitychange", () => {
      if (!document.hidden && isRunning) {
        requestAnimationFrame(animate);
      }
    });

    window.addEventListener("resize", resize, { passive: true });
    init();
    animate();
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 4. STICKER WOBBLE ON HOVER
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initStickerWobble() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if ("ontouchstart" in window || window.innerWidth < 768) return;

    const stickerEls = document.querySelectorAll(
      ".paper-card, .event-poster, .badge-sticker, .puzzle-poster"
    );

    stickerEls.forEach((card) => {
      card.addEventListener("mouseenter", () => {
        card.style.animation = "none";
        card.offsetHeight; // force reflow
        card.style.animation = "";
      });
    });
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 5. RUBBER BAND BUTTONS
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initRubberButtons() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if ("ontouchstart" in window || window.innerWidth < 768) return;

    const buttons = document.querySelectorAll(".btn");

    buttons.forEach((btn) => {
      btn.addEventListener("mouseenter", () => {
        btn.style.animation = "none";
        btn.offsetHeight;
      });
    });
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 6. NAVBAR SCROLL BEHAVIOR
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initNavbarScroll() {
    const nav = document.querySelector(".site-nav");
    if (!nav) return;

    let ticking = false;
    window.addEventListener(
      "scroll",
      () => {
        if (!ticking) {
          window.requestAnimationFrame(() => {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop;
            if (scrollY > 60) {
              nav.classList.add("scrolled");
            } else {
              nav.classList.remove("scrolled");
            }
            ticking = false;
          });
          ticking = true;
        }
      },
      { passive: true }
    );
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 7. TYPEWRITER EFFECT FOR EYEBROWS
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initTypewriter() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const eyebrows = document.querySelectorAll(".hero .eyebrow");

    eyebrows.forEach((el) => {
      const text = el.textContent;
      el.textContent = "";
      el.style.visibility = "visible";

      // remove the ::after underline during typing
      el.style.setProperty("--typing", "1");

      const cursor = document.createElement("span");
      cursor.className = "typewriter-cursor";

      let charIdx = 0;

      function typeChar() {
        if (charIdx < text.length) {
          el.textContent = text.slice(0, charIdx + 1);
          el.appendChild(cursor);
          charIdx++;
          setTimeout(typeChar, 45 + Math.random() * 35);
        }
      }

      const delay = shouldShowPortal() ? PORTAL_DURATION + 500 : 250;
      setTimeout(typeChar, delay);
    });
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 8. FOOTER DOODLE RAIN
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initFooterRain() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (window.innerWidth < 768 || "ontouchstart" in window) return;

    const footer = document.querySelector(".footer-poster");
    if (!footer) return;

    const RAIN_CHARS = ["π", "∞", "+", "=", "∑", "√", "Δ", "×", "÷", "²"];

    function spawnDoodle() {
      if (document.hidden) return;
      const drop = document.createElement("span");
      drop.textContent = RAIN_CHARS[Math.floor(Math.random() * RAIN_CHARS.length)];
      const color = COLORS[Math.floor(Math.random() * COLORS.length)];
      drop.style.cssText = `
        position: absolute;
        top: -2rem;
        left: ${Math.random() * 100}%;
        font-family: "Patrick Hand", cursive;
        font-size: ${Math.random() * 1.3 + 0.7}rem;
        color: ${color};
        opacity: ${Math.random() * 0.15 + 0.05};
        pointer-events: none;
        z-index: 0;
        animation: doodleRainDrop ${4 + Math.random() * 4}s linear forwards;
      `;
      footer.appendChild(drop);
      setTimeout(() => drop.remove(), 8000);
    }

    // inject the keyframe
    if (!document.getElementById("doodle-rain-keyframe")) {
      const style = document.createElement("style");
      style.id = "doodle-rain-keyframe";
      style.textContent = `
        @keyframes doodleRainDrop {
          0%   { transform: translateY(0) rotate(0deg); }
          100% { transform: translateY(${footer.offsetHeight + 60}px) rotate(${Math.random() > 0.5 ? 360 : -360}deg); opacity: 0; }
        }
      `;
      document.head.appendChild(style);
    }

    setInterval(spawnDoodle, 1200);
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 9. HAND-DRAWN DOODLE DECORATIONS
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function addDoodleDecorations() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (window.innerWidth < 768) return;

    // Add small doodle decorations between sections
    const sections = document.querySelectorAll(".page");
    const DECO_SYMBOLS = ["✦", "★", "♦", "●", "◆", "✿", "⊕"];
    const DECO_COLORS = ["#4ec5f1", "#f28c28", "#6abf4b", "#f472b6", "#fcd34d"];

    sections.forEach((section) => {
      for (let i = 0; i < 2; i++) {
        const deco = document.createElement("span");
        deco.textContent = DECO_SYMBOLS[Math.floor(Math.random() * DECO_SYMBOLS.length)];
        deco.style.cssText = `
          position: absolute;
          ${Math.random() > 0.5 ? 'right' : 'left'}: ${Math.random() * 12 + 2}%;
          top: ${Math.random() * 20}%;
          font-size: ${Math.random() * 1 + 0.5}rem;
          color: ${DECO_COLORS[Math.floor(Math.random() * DECO_COLORS.length)]};
          opacity: ${Math.random() * 0.25 + 0.08};
          pointer-events: none;
          transform: rotate(${Math.random() * 60 - 30}deg);
          animation: doodleBounce ${2.5 + Math.random() * 2}s ease-in-out infinite;
          animation-delay: ${Math.random() * 2}s;
        `;
        section.appendChild(deco);
      }
    });
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 10. CONFETTI BURST ON BUTTON CLICK
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initConfettiBurst() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    // inject confetti keyframe
    if (!document.getElementById("confetti-keyframe")) {
      const style = document.createElement("style");
      style.id = "confetti-keyframe";
      style.textContent = `
        @keyframes confettiFly {
          0%   { transform: translate(0, 0) rotate(0deg) scale(1); opacity: 1; }
          100% { transform: translate(var(--tx), var(--ty)) rotate(var(--tr)) scale(0); opacity: 0; }
        }
        .confetti-piece {
          position: fixed;
          pointer-events: none;
          z-index: 9999;
          font-size: 1.1rem;
          animation: confettiFly 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        }
      `;
      document.head.appendChild(style);
    }

    document.addEventListener("click", (e) => {
      const btn = e.target.closest(".btn");
      if (!btn) return;

      const rect = btn.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;

      const CONFETTI_SYMBOLS = ["✦", "★", "●", "♦", "✿", "π", "∑", "∞"];
      const count = window.innerWidth < 768 ? 6 : 10;

      for (let i = 0; i < count; i++) {
        const piece = document.createElement("span");
        piece.className = "confetti-piece";
        piece.textContent = CONFETTI_SYMBOLS[Math.floor(Math.random() * CONFETTI_SYMBOLS.length)];
        piece.style.left = cx + "px";
        piece.style.top = cy + "px";
        piece.style.color = COLORS[Math.floor(Math.random() * COLORS.length)];
        piece.style.setProperty("--tx", (Math.random() - 0.5) * 160 + "px");
        piece.style.setProperty("--ty", (Math.random() - 0.5) * 160 - 40 + "px");
        piece.style.setProperty("--tr", (Math.random() * 720 - 360) + "deg");
        piece.style.animationDelay = (Math.random() * 0.1) + "s";
        document.body.appendChild(piece);
        setTimeout(() => piece.remove(), 900);
      }
    });
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 11. 3D HERO MASCOT ARENA INTERACTION
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initHeroMascotArena() {
    const arena = document.getElementById("hero-mascot-arena");
    const board = document.getElementById("hero-mascot-board");
    if (!arena || !board) return;

    // 3D Parallax tilt only on fine pointer devices
    if (window.matchMedia("(pointer: fine)").matches && window.innerWidth >= 768) {
      arena.addEventListener("mousemove", (e) => {
        const rect = arena.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        const rotY = (x / (rect.width / 2)) * 12;
        const rotX = -(y / (rect.height / 2)) * 12;
        board.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.02)`;
      }, { passive: true });

      arena.addEventListener("mouseleave", () => {
        board.style.transform = "rotateX(0deg) rotateY(0deg) scale(1)";
      });
    }

    // Einstein click reaction
    const einstein = document.getElementById("mascot-einstein");
    if (einstein) {
      einstein.addEventListener("click", () => {
        einstein.classList.add("speaking");
        einstein.style.transform = "scale(1.2) rotate(-8deg) translateZ(40px)";
        const rect = einstein.getBoundingClientRect();
        spawnMiniConfetti(rect.left + rect.width / 2, rect.top, "π");
        setTimeout(() => {
          einstein.style.transform = "";
          einstein.classList.remove("speaking");
        }, 2200);
      });
    }

    // Newton click reaction
    const newton = document.getElementById("mascot-newton");
    if (newton) {
      newton.addEventListener("click", () => {
        newton.classList.add("speaking");
        newton.style.transform = "scale(1.2) rotate(8deg) translateZ(40px)";
        const rect = newton.getBoundingClientRect();
        spawnMiniConfetti(rect.left + rect.width / 2, rect.top, "🍎");
        setTimeout(() => {
          newton.style.transform = "";
          newton.classList.remove("speaking");
        }, 2200);
      });
    }

    // Interactive Math Toys
    const toyPi = document.getElementById("toy-pi");
    if (toyPi) {
      toyPi.addEventListener("click", () => {
        toyPi.style.transform = "scale(1.4) rotate(720deg)";
        const rect = toyPi.getBoundingClientRect();
        spawnMiniConfetti(rect.left + rect.width / 2, rect.top, "3.14");
        setTimeout(() => { toyPi.style.transform = ""; }, 800);
      });
    }

    const toyApple = document.getElementById("toy-apple");
    if (toyApple) {
      toyApple.addEventListener("click", () => {
        toyApple.style.transform = "translateY(120px) scale(1.3) rotate(360deg)";
        const rect = toyApple.getBoundingClientRect();
        spawnMiniConfetti(rect.left + rect.width / 2, rect.top, "g=9.8");
        setTimeout(() => { toyApple.style.transform = ""; }, 1000);
      });
    }

    const toyInfinity = document.getElementById("toy-infinity");
    if (toyInfinity) {
      toyInfinity.addEventListener("click", () => {
        toyInfinity.style.transform = "scale(1.5) rotate(1080deg)";
        const rect = toyInfinity.getBoundingClientRect();
        spawnMiniConfetti(rect.left + rect.width / 2, rect.top, "∞");
        setTimeout(() => { toyInfinity.style.transform = ""; }, 1000);
      });
    }
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 12. FLOATING 3D MATH SQUAD COMPANION DOCK
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  function initFloatingMathSquad() {
    if (document.getElementById("math-squad-fab")) return;

    // Create Floating Action Button
    const fab = document.createElement("div");
    fab.className = "math-squad-fab";
    fab.id = "math-squad-fab";
    fab.title = "Meet the 3D Math Squad!";
    fab.innerHTML = `
      <div class="math-squad-avatar">
        <img src="/static/images/mathematicians/einstein.jpg" alt="Math Squad">
      </div>
      <span class="math-squad-label">🧙‍♂️ Math Squad</span>
    `;

    // Create Drawer
    const drawer = document.createElement("div");
    drawer.className = "math-squad-drawer";
    drawer.id = "math-squad-drawer";

    let listHtml = "";
    MATHEMATICIANS.forEach((m) => {
      listHtml += `
        <div class="math-squad-item" data-id="${m.id}" title="Click to summon ${m.name}!">
          <div class="math-squad-item-img">
            <img src="${m.img}" alt="${m.name}">
          </div>
          <div class="math-squad-item-info">
            <div class="math-squad-item-name">${m.name}</div>
            <div class="math-squad-item-formula">${m.formula} · ${m.toy}</div>
          </div>
        </div>
      `;
    });

    drawer.innerHTML = `
      <div class="math-squad-header">
        <span class="math-squad-title">📐 Math Legends Squad</span>
        <button class="math-squad-close" id="math-squad-close" title="Close">✖</button>
      </div>
      <div class="math-squad-list">
        ${listHtml}
      </div>
      <div class="math-squad-actions">
        <button class="math-squad-btn" id="math-btn-replay">⚡ Replay 3D Intro</button>
        <button class="math-squad-btn secondary" id="math-btn-storm">🌧 Math Storm</button>
      </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(drawer);

    // Toggle drawer
    fab.addEventListener("click", () => {
      drawer.classList.toggle("open");
    });

    const closeBtn = document.getElementById("math-squad-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        drawer.classList.remove("open");
      });
    }

    // Replay 3D Intro
    const replayBtn = document.getElementById("math-btn-replay");
    if (replayBtn) {
      replayBtn.addEventListener("click", () => {
        drawer.classList.remove("open");
        if (window.replayIntroPortal) window.replayIntroPortal();
      });
    }

    // Math Storm
    const stormBtn = document.getElementById("math-btn-storm");
    if (stormBtn) {
      stormBtn.addEventListener("click", () => {
        triggerMathStorm();
      });
    }

    // Individual mathematician clicks in drawer
    drawer.querySelectorAll(".math-squad-item").forEach((item) => {
      item.addEventListener("click", () => {
        const id = item.dataset.id;
        const m = MATHEMATICIANS.find((x) => x.id === id);
        if (!m) return;

        // Shower screen with their signature icon
        spawnMassiveCelebration(m.toy, m.name + ": " + m.quote);
      });
    });
  }

  function triggerMathStorm() {
    const stormChars = ["π", "∑", "∞", "√", "∫", "Δ", "θ", "e", "i", "🍎", "📐", "+", "×", "÷"];
    for (let i = 0; i < 40; i++) {
      setTimeout(() => {
        const drop = document.createElement("span");
        drop.textContent = stormChars[Math.floor(Math.random() * stormChars.length)];
        drop.style.cssText = `
          position: fixed;
          top: -40px;
          left: ${Math.random() * 100}vw;
          font-size: ${Math.random() * 2 + 1.2}rem;
          color: ${COLORS[Math.floor(Math.random() * COLORS.length)]};
          font-family: 'Fredoka', 'Patrick Hand', cursive;
          font-weight: 700;
          z-index: 99999;
          pointer-events: none;
          animation: mathRainFall 2.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
          text-shadow: 2px 2px 0 var(--ink);
        `;
        document.body.appendChild(drop);
        setTimeout(() => drop.remove(), 2500);
      }, i * 40);
    }

    // Ensure keyframe exists
    if (!document.getElementById("math-storm-keyframe")) {
      const st = document.createElement("style");
      st.id = "math-storm-keyframe";
      st.textContent = `
        @keyframes mathRainFall {
          0% { transform: translateY(0) rotate(0deg) scale(0.5); opacity: 0; }
          20% { opacity: 1; transform: translateY(15vh) rotate(60deg) scale(1.2); }
          100% { transform: translateY(110vh) rotate(720deg) scale(0.8); opacity: 0; }
        }
      `;
      document.head.appendChild(st);
    }
  }

  function spawnMassiveCelebration(symbol, quoteText) {
    // Show comic toast banner
    const toast = document.createElement("div");
    toast.style.cssText = `
      position: fixed;
      top: 2.5rem;
      left: 50%;
      transform: translateX(-50%) scale(0);
      background: var(--yellow);
      color: var(--ink);
      border: 3.5px solid var(--ink);
      border-radius: 20px;
      padding: 0.8rem 1.8rem;
      font-family: 'Patrick Hand', cursive;
      font-size: 1.25rem;
      font-weight: 700;
      box-shadow: 6px 6px 0 var(--ink);
      z-index: 999999;
      pointer-events: none;
      transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      max-width: 90vw;
      text-align: center;
    `;
    toast.textContent = quoteText;
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.transform = "translateX(-50%) scale(1)"; }, 20);
    setTimeout(() => {
      toast.style.transform = "translateX(-50%) scale(0)";
      setTimeout(() => toast.remove(), 400);
    }, 3200);

    // Burst of symbol
    for (let i = 0; i < 25; i++) {
      const p = document.createElement("span");
      p.className = "confetti-piece";
      p.textContent = symbol;
      p.style.left = (window.innerWidth / 2) + "px";
      p.style.top = (window.innerHeight / 2) + "px";
      p.style.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      p.style.setProperty("--tx", (Math.random() - 0.5) * 600 + "px");
      p.style.setProperty("--ty", (Math.random() - 0.5) * 600 - 80 + "px");
      p.style.setProperty("--tr", (Math.random() * 720 - 360) + "deg");
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 1100);
    }
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  // 13. 3D POKÉBALL SUMMONING & TEAM CARD EMERGE ANIMATION
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  window.summonPokeballMember = function (triggerEl, event) {
    if (event) {
      event.stopPropagation();
    }
    const card = triggerEl ? triggerEl.closest(".team-flip-card") : null;
    if (!card || card.classList.contains("is-flipped") || card.dataset.summoning === "true") {
      return;
    }

    card.dataset.summoning = "true";
    const memberName = card.getAttribute("data-member-name") || "CREW MEMBER";
    const specialPower = card.getAttribute("data-member-power") || "Domain Expansion: Infinite Logic";
    const rect = card.getBoundingClientRect();

    // 1. Pokéball Wobble / Capture Shake Phase
    card.classList.add("is-summoning");

    // Spawn Pre-summon SFX badge
    spawnPokeballBadge(rect, "⚡ I CHOOSE YOU!", "#ffd700", -90);

    // 2. Open Pokéball Hinge & Fire Energy Pillar Blast
    setTimeout(() => {
      card.classList.add("is-ball-opened");

      // Spawn summon energy blast sparks
      spawnPokeballSparks(rect);
      spawnPokeballBadge(rect, "💥 " + memberName.toUpperCase() + ", GO!", "#ff4d4d", -130);
    }, 240);

    // 3. Complete Card Emergence & 3D Flip
    setTimeout(() => {
      card.classList.remove("is-summoning");
      card.classList.remove("is-ball-opened");
      card.classList.add("is-flipped");
      card.dataset.summoning = "false";

      // Trigger automatic Aura celebration & power toast
      const unleashBtn = card.querySelector(".team-unleash-btn");
      setTimeout(() => {
        if (window.unleashAnimeAura) {
          window.unleashAnimeAura(unleashBtn || card, memberName, specialPower);
        }
      }, 350);
    }, 550);
  };

  window.recallPokeballMember = function (triggerEl, event) {
    if (event) {
      event.stopPropagation();
    }
    const card = triggerEl ? triggerEl.closest(".team-flip-card") : null;
    if (!card) return;

    card.classList.remove("is-flipped");
    card.classList.remove("is-summoning");
    card.classList.remove("is-ball-opened");
    card.dataset.summoning = "false";

    const rect = card.getBoundingClientRect();
    spawnPokeballBadge(rect, "🔴 RECALLED TO POKÉBALL", "#38bdf8", -75);
  };

  // Backwards compatibility for any lingering flip calls
  window.flipTeamCard = function (triggerEl, event, shouldAutoAura = false) {
    const card = triggerEl ? triggerEl.closest(".team-flip-card") : null;
    if (card) {
      if (card.classList.contains("is-flipped")) {
        window.recallPokeballMember(triggerEl, event);
      } else {
        window.summonPokeballMember(triggerEl, event);
      }
    }
  };

  // Helper: Spawn Floating Action Comic SFX Tag
  function spawnPokeballBadge(rect, text, color = "#ffd700", yOffset = -80) {
    const tag = document.createElement("span");
    tag.className = "confetti-piece";
    tag.textContent = text;
    tag.style.left = (rect.left + rect.width / 2) + "px";
    tag.style.top = (rect.top + 80) + "px";
    tag.style.fontFamily = "'Lilita One', 'Fredoka', cursive";
    tag.style.fontSize = "1.25rem";
    tag.style.fontWeight = "900";
    tag.style.color = color;
    tag.style.textShadow = "2.5px 2.5px 0 var(--ink), 0 0 15px rgba(255, 215, 0, 0.8)";
    tag.style.setProperty("--tx", (Math.random() - 0.5) * 60 + "px");
    tag.style.setProperty("--ty", yOffset + "px");
    tag.style.setProperty("--tr", (Math.random() * 20 - 10) + "deg");
    tag.style.zIndex = "99999";
    document.body.appendChild(tag);
    setTimeout(() => tag.remove(), 1100);
  }

  // Helper: Spawn Energy Spark Particles on Ball Open
  function spawnPokeballSparks(rect) {
    const sparkIcons = ["⚡", "★", "✨", "🔥", "💥", "∑", "π"];
    const sparkCount = 14;
    for (let i = 0; i < sparkCount; i++) {
      const p = document.createElement("span");
      p.className = "confetti-piece";
      p.textContent = sparkIcons[Math.floor(Math.random() * sparkIcons.length)];
      p.style.left = (rect.left + rect.width / 2) + "px";
      p.style.top = (rect.top + rect.height / 2 - 30) + "px";
      p.style.fontSize = (Math.random() * 1.2 + 0.9) + "rem";
      p.style.color = ["#ffd700", "#ff4d4d", "#38bdf8", "#f472b6", "#ffffff"][Math.floor(Math.random() * 5)];
      p.style.setProperty("--tx", (Math.random() - 0.5) * 450 + "px");
      p.style.setProperty("--ty", (Math.random() - 0.5) * 450 - 60 + "px");
      p.style.setProperty("--tr", (Math.random() * 720 - 360) + "deg");
      p.style.zIndex = "99999";
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 900);
    }
  }

  // Click on Pokéball chamber
  document.addEventListener("click", (e) => {
    const chamber = e.target.closest(".pokeball-chamber");
    if (chamber && !e.target.closest("button, a, input, [data-no-flip]")) {
      const card = chamber.closest(".team-flip-card");
      if (card && !card.classList.contains("is-flipped")) {
        window.summonPokeballMember(chamber, e);
      }
    }
  });

  window.unleashAnimeAura = function (buttonEl, memberName, specialPower, event) {
    if (event) {
      event.stopPropagation();
    }
    const card = buttonEl ? buttonEl.closest(".team-flip-card") : null;
    const backFace = buttonEl ? buttonEl.closest(".team-card-back") : null;

    // 1. Power-up card animation & electric aura shake
    const targetElement = backFace || card;
    if (targetElement) {
      targetElement.style.transition = "transform 0.15s ease, box-shadow 0.15s ease";
      targetElement.style.boxShadow = "0 0 50px rgba(242, 140, 40, 0.95), 14px 14px 0 var(--ink)";

      // Trigger temporary electric energy vibration
      let shakes = 0;
      const shakeInterval = setInterval(() => {
        shakes++;
        const rot = (shakes % 2 === 0 ? 2 : -2);
        targetElement.style.transform = `rotateY(180deg) rotate(${rot}deg) scale(1.03)`;
        if (shakes >= 8) {
          clearInterval(shakeInterval);
          setTimeout(() => {
            targetElement.style.transform = "rotateY(180deg)";
            targetElement.style.boxShadow = "";
          }, 1200);
        }
      }, 50);
    }

    // 2. Comic Action Toast Banner
    const toast = document.createElement("div");
    toast.style.cssText = `
      position: fixed;
      top: 2rem;
      left: 50%;
      transform: translateX(-50%) scale(0) rotate(-2deg);
      background: linear-gradient(135deg, #ffd700, #ff8c00);
      color: var(--ink);
      border: 4px solid var(--ink);
      border-radius: 24px;
      padding: 0.9rem 2.2rem;
      font-family: 'Lilita One', 'Fredoka', sans-serif;
      font-size: 1.35rem;
      font-weight: 900;
      letter-spacing: 0.04em;
      box-shadow: 8px 8px 0 var(--ink);
      z-index: 999999;
      pointer-events: none;
      text-align: center;
      transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
      max-width: 92vw;
      text-shadow: 1px 1px 0 rgba(255,255,255,0.7);
    `;
    toast.innerHTML = `💥 <strong>${memberName}</strong> ACTIVATED<br><span style="color:#ef4444; -webkit-text-stroke: 1px var(--ink); font-size:1.1rem;">🔮 ${specialPower}</span> ⚡`;
    document.body.appendChild(toast);

    setTimeout(() => { toast.style.transform = "translateX(-50%) scale(1) rotate(1deg)"; }, 20);
    setTimeout(() => {
      toast.style.transform = "translateX(-50%) scale(0) rotate(10deg)";
      setTimeout(() => toast.remove(), 400);
    }, 3000);

    // 3. Manga Sound FX & Kanji particles burst around card
    const MANGA_SFX = ["「ゴゴゴゴ」", "「ドカーン！」", "「ズキューン！」", "「バァァァン！」", "⚡ PLUS ULTRA!", "🔥 BANKAI!", "✨ DOMAIN EXPANSION!"];
    const rect = buttonEl ? buttonEl.getBoundingClientRect() : { left: window.innerWidth / 2, top: window.innerHeight / 2, width: 0, height: 0 };
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    for (let i = 0; i < 18; i++) {
      const piece = document.createElement("span");
      piece.className = "confetti-piece";
      piece.textContent = MANGA_SFX[Math.floor(Math.random() * MANGA_SFX.length)];
      piece.style.left = cx + "px";
      piece.style.top = cy + "px";
      piece.style.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      piece.style.fontFamily = "'Lilita One', 'Fredoka', cursive";
      piece.style.fontSize = (Math.random() * 0.8 + 1) + "rem";
      piece.style.fontWeight = "900";
      piece.style.textShadow = "2px 2px 0 var(--ink)";
      piece.style.setProperty("--tx", (Math.random() - 0.5) * 450 + "px");
      piece.style.setProperty("--ty", (Math.random() - 0.5) * 450 - 60 + "px");
      piece.style.setProperty("--tr", (Math.random() * 720 - 360) + "deg");
      piece.style.animationDelay = (Math.random() * 0.15) + "s";
      document.body.appendChild(piece);
      setTimeout(() => piece.remove(), 1200);
    }
  };

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  document.addEventListener("DOMContentLoaded", () => {
    createPortal();
    initScrollReveals();
    initParticles();
    initNavbarScroll();
    initTypewriter();
    initConfettiBurst();
    initHeroMascotArena();
    initFloatingMathSquad();

    setTimeout(() => {
      initStickerWobble();
      initRubberButtons();
      initFooterRain();
      addDoodleDecorations();
    }, shouldShowPortal() ? PORTAL_DURATION + 400 : 200);
  });
})();
