<div align="center">

  <img src="static/images/domain_logo.png" alt="Domain Math Club Logo" width="120" height="120" style="border-radius: 50%; border: 3px solid #1c150c; box-shadow: 0 8px 25px rgba(0,0,0,0.2);">

  # 📐 Domain Math Club
  ### *Don Bosco Institute of Technology (DBIT)*

  [![Django](https://img.shields.io/badge/Django-6.1+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/)
  [![CSS3](https://img.shields.io/badge/CSS3-Custom_3D_Voxel-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
  [![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

  <p align="center">
    <strong>A high-engagement, cartoonistic, and gamified Mathematics Club web platform for curious problem solvers, alchemists, and engineering students.</strong>
  </p>

  <p align="center">
    <a href="#-key-features">Features</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-installation--setup">Quickstart</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-admin-panel">Admin Guide</a>
  </p>

</div>

---

## 🌟 Key Features

### 🌌 1. The 3D Mathematics Multiverse Portal
- **Interactive 3D Entrance**: Welcome portal with floating mathematical glyphs ($\pi, \sum, \infty, e, \int$), coordinate rings, and dynamic perspective parallax.
- **5 Cartoon Legends**: Meet animated versions of **Albert Einstein, Isaac Newton, Srinivasa Ramanujan, Leonhard Euler**, and **Pythagoras** with interactive soundbites and jokes.
- **Auto-enter Timer & Hyperspace Exit**: Smooth countdown progress bar with instant skip toggle.

### ⛏️ 2. Minecraft-Themed Leaderboard Realm
- **3D Pedestals of Glory**: Top 3 ranking problem solvers displayed on 3D Minecraft Pedestals (#1 Diamond/Emerald Throne with Golden Crown, #2 Gold Tier, #3 Copper Tier).
- **Interactive Hotbar Filter**: Instant live filtering for college branches (**COMPS**, **IT**, **EXTC**, **MECH**).
- **Anvil Search Engine**: Real-time student search bar styled like a Minecraft Chat/Anvil GUI.
- **Synthesized 8-Bit Audio**: In-browser Web Audio API sound effects (wood clicks, XP orb pickup chimes, level-up fanfares) with `🔊 AUDIO ON/OFF` toggle.

### ⚒️ 3. Minecraft Quest Board & Crafting Solver
- **Adventure Quest Board**: Wooden signboards with difficulty badges (`⚔️ ELITE QUEST` / `HARDCORE`) and reward previews.
- **Boss Health Bar Countdown**: Real-time redstone bar ticking down to puzzle close.
- **Crafting Table & Anvil Input**: Left column Ancient Enchanted Tome + Right column inventory crafting slot to forge answers.
- **Obsidian Lock & Truth Scroll**: Answers locked in obsidian with full mathematical solutions revealed upon expiration.

### 🎪 4. Polaroid Events & Photo Gallery
- **Polaroid Photo Cards**: Uploaded event photos rendered inside vintage polaroid frames with washi tape pins and calendar leaves.
- **Fullscreen Lightbox**: Dark-mode blurred modal on photo click with `Esc` key and tap-to-dismiss support.
- **Meta HUD**: Venue badges, time pins, and one-click registration buttons (`🚀 Register Now`).

### 📚 5. The Mathematical Chronicles & Cartoon Professors' Lounge
- **Multicolor Comic Typography**: Rainbow layered 3D display headings.
- **Professors' Lounge Observatory**: Interactive scientist cards with witty speech bubbles and bounce animations.
- **Editorial Paper Reader**: Optimized reading experience with paper-texture cards, quote callouts, and author signatures.

### 🎴 6. S-Rank Anime Team Guild
- **Poké-Capsule Summoning**: 3D animated Pokéballs that open into full revealed anime character companion cards with custom power levels and bounty tags.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Django 6.1+ (MVC/MVT Architecture) |
| **Frontend** | Vanilla JavaScript (ES6+), Web Audio API Synthesizer, CSS3 (3D Voxel/Grid Transforms) |
| **Styling** | Custom Responsive Design System, Tailwind CSS, Google Fonts (`Press Start 2P`, `VT323`, `Fredoka`, `Nunito`) |
| **Database** | SQLite (Dev) / PostgreSQL (Production) |
| **Storage** | Django Media Storage for event photos, team images, and blog covers |

---

## 📁 Architecture & Directory Structure

```text
Domain-club/
├── accounts/          # Student authentication, profiles, streaks, and rank caching
├── badges/            # Gamified achievements and mathematical unlockable badges
├── blog/              # Mathematical chronicles, essays, and editorial journal
├── config/            # Root project settings, URL routing, and WSGI/ASGI configs
├── core/              # Landing page, sitemaps, robots.txt, and team roster models
├── events/            # Events calendar, photo gallery, and registration engine
├── leaderboard/       # All-time & monthly leaderboard algorithms, winner plaques
├── media/             # Uploaded team portraits, event photos, and blog covers
├── puzzles/           # Weekly 24h numerical puzzle engine, submissions & validation
├── static/
│   ├── css/           # custom.css, minecraft_theme.css
│   ├── images/        # domain_logo.png, anime/, mathematicians/, minecraft/
│   └── js/            # animations.js, minecraft_effects.js, countdown.js, main.js
└── templates/         # Django HTML5 templates (base.html, partials, apps)
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Dhruveshbhamare11/Domain-Club-website.git
cd Domain-Club-website
```

### 2. Create and Activate Virtual Environment
```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` or use default development values:
```bash
cp .env.example .env
```

### 5. Apply Migrations & Create Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- 🏠 **Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🛡️ **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🛡️ Admin Panel & Content Management

Use the Django Admin at `/admin/` to manage:
- **Puzzles**: Add weekly questions, answers, solutions, and start/end times.
- **Events & Photos**: Upload conclave photos, venues, and registration links.
- **Blog Articles**: Publish student essays and mathematical proofs.
- **Team**: Manage team members, roles, branch years, and photos.

---

## 🤝 Contributing

Contributions, bug reports, and pull requests are warmly welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

<div align="center">
  <sub>Built with ❤️ and ☕ by <strong>Dhruvesh Bhamare</strong> & the <strong>DBIT Domain Math Club Squad</strong></sub>
</div>
