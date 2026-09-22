document.documentElement.classList.add("js");
document.addEventListener("DOMContentLoaded", () => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* mobile menu */
  const menu = document.querySelector(".menu-btn");
  const links = document.querySelector(".navlinks");
  if (menu) menu.addEventListener("click", () => {
    links.style.display = links.style.display === "flex" ? "none" : "flex";
    links.style.flexDirection = "column";
    links.style.position = "absolute";
    links.style.top = "72px";
    links.style.right = "15px";
    links.style.padding = "16px";
    links.style.background = "#072b61";
    links.style.borderRadius = "14px";
  });

  document.querySelectorAll(".fade-up").forEach((el, i) => {
    el.style.animationDelay = `${Math.min(i * 60, 420)}ms`;
  });

  /* navbar shrink on scroll */
  const nav = document.querySelector(".navbar");
  const onScroll = () => nav && nav.classList.toggle("scrolled", scrollY > 20);
  onScroll(); addEventListener("scroll", onScroll, { passive: true });

  /* count-up for percentages */
  const count = (el) => {
    const m = el.textContent.match(/\d+/); if (!m) return;
    const end = +m[0], suffix = el.textContent.replace(m[0], "");
    if (reduce) return;
    const t0 = performance.now(), dur = 900;
    const tick = (t) => {
      const p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * e) + suffix;
      if (p < 1) requestAnimationFrame(tick); else el.classList.add("pop");
    };
    el.textContent = "0" + suffix; requestAnimationFrame(tick);
  };

  /* scroll reveal (staggered per group) */
  const targets = document.querySelectorAll(".card:not(.fade-up),.list-row,.feature:not(.fade-up),.question,.section-title,.page-head");
  targets.forEach((el) => {
    const sibs = [...el.parentElement.children].filter((c) => c.matches(".card,.list-row,.feature,.question"));
    el.style.setProperty("--d", Math.max(sibs.indexOf(el), 0) * 70 + "ms");
    el.classList.add("reveal");
  });
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add("in");
      en.target.querySelectorAll(".pct,.match-pct").forEach(count);
      io.unobserve(en.target);
    });
  }, { threshold: 0.12 });
  targets.forEach((el) => io.observe(el));
  document.querySelectorAll(".hero-card .pct").forEach(count);

  /* hero card tilt */
  const art = document.querySelector(".hero-art"), hc = document.querySelector(".hero-card");
  if (art && hc && !reduce) {
    art.addEventListener("mousemove", (e) => {
      const r = art.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      hc.style.animation = "none";
      hc.style.transform = `perspective(700px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg)`;
    });
    art.addEventListener("mouseleave", () => { hc.style.transform = ""; hc.style.animation = ""; });
  }

  /* button ripple */
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".btn"); if (!b || reduce) return;
    const r = b.getBoundingClientRect(), s = Math.max(r.width, r.height);
    const d = document.createElement("span"); d.className = "ripple";
    d.style.cssText = `width:${s}px;height:${s}px;left:${e.clientX - r.left - s / 2}px;top:${e.clientY - r.top - s / 2}px`;
    b.appendChild(d); setTimeout(() => d.remove(), 600);
  });

  /* quiz progress bar tracks answered questions */
  const bar = document.querySelector(".progress span");
  const qs = document.querySelectorAll(".question");
  if (bar && qs.length) {
    const upd = () => {
      const done = [...qs].filter((q) => q.querySelector("input:checked")).length;
      bar.style.width = (done / qs.length) * 100 + "%";
    };
    document.querySelector(".quiz-card").addEventListener("change", upd); upd();
  }
});
