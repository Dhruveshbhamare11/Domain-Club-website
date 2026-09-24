document.documentElement.classList.add("js");

// 1. Mobile Menu Toggle with Auto-Prefetch
const toggle = document.querySelector("[data-nav-toggle]");
const menu = document.querySelector("[data-nav-menu]");
if (toggle && menu) {
  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    menu.classList.toggle("is-open", !expanded);

    // When menu opens, prefetch all menu destinations immediately
    if (!expanded) {
      prefetchNavLinks();
    }
  });

  // Close menu immediately on selecting a link
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      menu.classList.remove("is-open");
    });
  });
}

// 2. High-Speed Link Prefetch Engine (Instantaneous Page Transitions)
const prefetchedUrls = new Set();

function prefetchUrl(url) {
  if (!url || prefetchedUrls.has(url)) return;
  // Ignore external links, anchors, logout, admin, or files
  if (
    url.startsWith("http://") ||
    url.startsWith("https://") ||
    url.startsWith("#") ||
    url.includes("logout") ||
    url.includes("admin") ||
    url.includes("static") ||
    url.includes("media")
  ) {
    if (!url.startsWith(window.location.origin)) return;
  }

  prefetchedUrls.add(url);

  // Use standard prefetch link element
  const link = document.createElement("link");
  link.rel = "prefetch";
  link.href = url;
  link.as = "document";
  document.head.appendChild(link);
}

function prefetchNavLinks() {
  const navLinks = document.querySelectorAll(".nav-links a, .site-nav a");
  navLinks.forEach((a) => {
    const href = a.getAttribute("href");
    if (href && !href.startsWith("#") && !href.includes("logout") && !href.includes("admin")) {
      prefetchUrl(href);
    }
  });
}

// 3. Touchstart & Mouseover Prefetching: Trigger download before click
let hoverTimer = null;
document.addEventListener(
  "mouseover",
  (e) => {
    const link = e.target.closest("a");
    if (!link) return;
    const href = link.getAttribute("href");
    if (!href || href.startsWith("#") || href.includes("logout") || href.includes("admin")) return;

    hoverTimer = setTimeout(() => {
      prefetchUrl(href);
    }, 60);
  },
  { passive: true }
);

document.addEventListener(
  "mouseout",
  () => {
    if (hoverTimer) clearTimeout(hoverTimer);
  },
  { passive: true }
);

// Mobile touch: finger down triggers prefetch instantly
document.addEventListener(
  "touchstart",
  (e) => {
    const link = e.target.closest("a");
    if (!link) return;
    const href = link.getAttribute("href");
    if (href && !href.startsWith("#") && !href.includes("logout") && !href.includes("admin")) {
      prefetchUrl(href);
    }
  },
  { passive: true }
);



// 5. Rapid Visual Feedback on Link Navigation
const progressBar = document.createElement("div");
progressBar.id = "instant-progress-bar";
progressBar.style.cssText = `
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 0%;
  background: linear-gradient(90deg, #4ec5f1, #f28c28, #ffd700);
  z-index: 99999999;
  transition: width 0.25s ease, opacity 0.25s ease;
  pointer-events: none;
`;
document.body.appendChild(progressBar);

document.addEventListener("click", (e) => {
  const link = e.target.closest("a");
  if (!link) return;
  const href = link.getAttribute("href");
  if (
    !href ||
    href.startsWith("#") ||
    href.startsWith("javascript:") ||
    link.target === "_blank" ||
    e.ctrlKey ||
    e.metaKey ||
    e.shiftKey
  ) {
    return;
  }

  // Instant visual feedback for rapid user feel
  progressBar.style.width = "45%";
  progressBar.style.opacity = "1";
  setTimeout(() => {
    progressBar.style.width = "85%";
  }, 80);
});

window.addEventListener("pageshow", () => {
  progressBar.style.width = "100%";
  setTimeout(() => {
    progressBar.style.opacity = "0";
    setTimeout(() => {
      progressBar.style.width = "0%";
    }, 150);
  }, 100);
});
