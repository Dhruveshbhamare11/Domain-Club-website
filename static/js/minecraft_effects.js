/**
 * MINECRAFT EFFECTS & SOUND ENGINE - DOMAIN MATHEMATICS CLUB
 * Pure Web Audio API 8-Bit Synthesizer, XP Particles, Sound Toggle & Hotbar Filters
 */

(function () {
  'use strict';

  // --- Audio Context & Sound State ---
  let audioCtx = null;
  let soundEnabled = localStorage.getItem('mc_sound_enabled') !== 'false'; // default true

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  // --- 8-Bit Web Audio Sound Synthesizers ---

  // 1. Classic Minecraft Button Click (Wood/Stone click)
  function playMcClick() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(320, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(140, ctx.currentTime + 0.04);
      
      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.04);
      
      osc.connect(gain);
      gain.connect(ctx.destination);
      
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    } catch (e) {
      console.warn('Audio error:', e);
    }
  }

  // 2. High-Pitched XP Orb Pickup Chime
  function playMcXp() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const notes = [1318.51, 1567.98, 1760.00]; // E6, G6, A6
      const pitch = notes[Math.floor(Math.random() * notes.length)];
      
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      
      osc.type = 'sine';
      osc.frequency.setValueAtTime(pitch, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(pitch * 1.25, ctx.currentTime + 0.12);
      
      gain.gain.setValueAtTime(0.35, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
      
      osc.connect(gain);
      gain.connect(ctx.destination);
      
      osc.start();
      osc.stop(ctx.currentTime + 0.16);
    } catch (e) {
      console.warn('Audio error:', e);
    }
  }

  // 3. Level Up / Triumphant Fanfare
  function playMcLevelUp() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const chords = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
      chords.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.type = 'square';
        osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.08);
        
        gain.gain.setValueAtTime(0.2, ctx.currentTime + idx * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.08 + 0.3);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        
        osc.start(ctx.currentTime + idx * 0.08);
        osc.stop(ctx.currentTime + idx * 0.08 + 0.35);
      });
    } catch (e) {
      console.warn('Audio error:', e);
    }
  }

  // 4. Anvil / Crafting Hammer Clink
  function playMcCraft() {
    if (!soundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + 0.18);
      
      gain.gain.setValueAtTime(0.4, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
      
      osc.connect(gain);
      gain.connect(ctx.destination);
      
      osc.start();
      osc.stop(ctx.currentTime + 0.22);
    } catch (e) {
      console.warn('Audio error:', e);
    }
  }

  // Expose sound API to window
  window.McAudio = {
    playClick: playMcClick,
    playXp: playMcXp,
    playLevelUp: playMcLevelUp,
    playCraft: playMcCraft,
    toggleSound: function () {
      soundEnabled = !soundEnabled;
      localStorage.setItem('mc_sound_enabled', soundEnabled ? 'true' : 'false');
      updateSoundButtonUI();
      if (soundEnabled) playMcXp();
      return soundEnabled;
    },
    isSoundEnabled: function () {
      return soundEnabled;
    }
  };

  function updateSoundButtonUI() {
    const btns = document.querySelectorAll('.mc-sound-toggle');
    btns.forEach(btn => {
      if (soundEnabled) {
        btn.classList.add('active');
        btn.innerHTML = '<span>🔊 AUDIO: ON</span>';
      } else {
        btn.classList.remove('active');
        btn.innerHTML = '<span>🔇 AUDIO: OFF</span>';
      }
    });
  }

  // --- XP Particle Sparkle Spawner ---
  function spawnXpParticle(x, y) {
    const orb = document.createElement('div');
    orb.className = 'mc-xp-orb-particle';
    orb.style.cssText = `
      position: fixed;
      left: ${x}px;
      top: ${y}px;
      width: 10px;
      height: 10px;
      background: radial-gradient(circle, #80ff00 30%, #55ff55 70%, transparent 100%);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      box-shadow: 0 0 10px #80ff00;
      transform: translate(-50%, -50%);
      transition: all 0.6s cubic-bezier(0.1, 0.8, 0.3, 1);
    `;
    document.body.appendChild(orb);

    const deltaX = (Math.random() - 0.5) * 80;
    const deltaY = -Math.random() * 60 - 20;

    requestAnimationFrame(() => {
      orb.style.transform = `translate(calc(-50% + ${deltaX}px), calc(-50% + ${deltaY}px)) scale(0.3)`;
      orb.style.opacity = '0';
    });

    setTimeout(() => {
      if (orb.parentNode) orb.parentNode.removeChild(orb);
    }, 650);
  }

  // --- DOM Initializations ---
  document.addEventListener('DOMContentLoaded', () => {
    updateSoundButtonUI();

    // Attach sound and particle to all Minecraft buttons and slots
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.mc-btn, .mc-hotbar-slot, .mc-rank-box, .mc-archive-card');
      if (btn) {
        playMcClick();
        const rect = btn.getBoundingClientRect();
        spawnXpParticle(e.clientX || (rect.left + rect.width / 2), e.clientY || (rect.top + rect.height / 2));
      }

      // Sound toggle button click
      const soundBtn = e.target.closest('.mc-sound-toggle');
      if (soundBtn) {
        window.McAudio.toggleSound();
      }
    });

    // Hover XP sparkle on Pedestals
    const pedestals = document.querySelectorAll('.mc-pedestal-card');
    pedestals.forEach(p => {
      p.addEventListener('mouseenter', () => {
        playMcXp();
      });
    });

    // --- Search & Hotbar Filter for Leaderboard ---
    const searchInput = document.getElementById('mc-student-search');
    const hotbarSlots = document.querySelectorAll('.mc-hotbar-slot');
    const tableRows = document.querySelectorAll('.mc-row-item');

    let currentBranchFilter = 'ALL';

    function filterLeaderboard() {
      const query = (searchInput ? searchInput.value : '').toLowerCase().trim();

      tableRows.forEach(row => {
        const name = (row.getAttribute('data-name') || '').toLowerCase();
        const branch = (row.getAttribute('data-branch') || '').toUpperCase();

        const matchesBranch = currentBranchFilter === 'ALL' || branch === currentBranchFilter;
        const matchesQuery = !query || name.includes(query) || branch.toLowerCase().includes(query);

        if (matchesBranch && matchesQuery) {
          row.style.display = 'grid';
        } else {
          row.style.display = 'none';
        }
      });
    }

    if (searchInput) {
      searchInput.addEventListener('input', filterLeaderboard);
    }

    hotbarSlots.forEach(slot => {
      slot.addEventListener('click', () => {
        hotbarSlots.forEach(s => s.classList.remove('active'));
        slot.classList.add('active');
        currentBranchFilter = slot.getAttribute('data-branch') || 'ALL';
        filterLeaderboard();
      });
    });
  });
})();
