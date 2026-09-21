document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* =========================
     MOBILE MENU
  ========================= */
  const menu = document.querySelector(".menu-btn");
  const links = document.querySelector(".navlinks");

  if (menu && links) {
    menu.addEventListener("click", () => {
      links.classList.toggle("mobile-open");
      menu.classList.toggle("active");
    });

    // Close menu after clicking a link
    links.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        links.classList.remove("mobile-open");
        menu.classList.remove("active");
      });
    });
  }

  /* =========================
     FADE-UP STAGGER
  ========================= */
  document.querySelectorAll(".fade-up").forEach((el, i) => {
    el.style.animationDelay = `${Math.min(i * 60, 420)}ms`;
  });

  /* =========================
     NAVBAR SCROLL EFFECT
  ========================= */
  const nav = document.querySelector(".navbar");

  const onScroll = () => {
    if (!nav) return;
    nav.classList.toggle("scrolled", window.scrollY > 20);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* =========================
     COUNT-UP ANIMATION
  ========================= */
  const count = (el) => {
    if (el.dataset.counted === "true") return;

    const match = el.textContent.match(/\d+/);
    if (!match) return;

    const end = Number(match[0]);
    const suffix = el.textContent.replace(match[0], "");

    el.dataset.counted = "true";

    if (reduce) return;

    const start = performance.now();
    const duration = 900;

    const tick = (time) => {
      const progress = Math.min((time - start) / duration, 1);

      // Smooth ease-out
      const eased = 1 - Math.pow(1 - progress, 3);

      el.textContent = Math.round(end * eased) + suffix;

      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        el.classList.add("pop");
      }
    };

    el.textContent = "0" + suffix;
    requestAnimationFrame(tick);
  };

  /* =========================
     SCROLL REVEAL
  ========================= */
  const targets = document.querySelectorAll(
    ".card:not(.fade-up)," +
    ".list-row," +
    ".feature:not(.fade-up)," +
    ".question," +
    ".section-title," +
    ".page-head"
  );

  targets.forEach((el) => {
    const parent = el.parentElement;

    if (!parent) return;

    const siblings = [...parent.children].filter((child) =>
      child.matches(".card,.list-row,.feature,.question")
    );

    const index = siblings.indexOf(el);

    el.style.setProperty(
      "--d",
      `${Math.max(index, 0) * 70}ms`
    );

    el.classList.add("reveal");
  });

  if (!reduce && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          entry.target.classList.add("in");

          entry.target
            .querySelectorAll(".pct,.match-pct")
            .forEach(count);

          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12
      }
    );

    targets.forEach((el) => observer.observe(el));
  } else {
    targets.forEach((el) => el.classList.add("in"));
  }

  /* Hero percentage counters */
  document
    .querySelectorAll(".hero-card .pct")
    .forEach(count);

  /* =========================
     HERO 3D TILT
  ========================= */
  const art = document.querySelector(".hero-art");
  const heroCard = document.querySelector(".hero-card");

  if (art && heroCard && !reduce) {
    art.addEventListener("mousemove", (event) => {
      const rect = art.getBoundingClientRect();

      const x =
        (event.clientX - rect.left) / rect.width - 0.5;

      const y =
        (event.clientY - rect.top) / rect.height - 0.5;

      heroCard.style.animation = "none";

      heroCard.style.transform = `
        perspective(700px)
        rotateY(${x * 10}deg)
        rotateX(${-y * 10}deg)
        translateY(-4px)
      `;
    });

    art.addEventListener("mouseleave", () => {
      heroCard.style.transform = "";
      heroCard.style.animation = "";
    });
  }

  /* =========================
     BUTTON RIPPLE
  ========================= */
  document.addEventListener("click", (event) => {
    const button = event.target.closest(".btn");

    if (!button || reduce) return;

    const rect = button.getBoundingClientRect();

    const size = Math.max(
      rect.width,
      rect.height
    );

    const ripple = document.createElement("span");

    ripple.className = "ripple";

    ripple.style.width = `${size}px`;
    ripple.style.height = `${size}px`;

    ripple.style.left =
      `${event.clientX - rect.left - size / 2}px`;

    ripple.style.top =
      `${event.clientY - rect.top - size / 2}px`;

    button.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  });

  /* =========================
     QUIZ PROGRESS
  ========================= */
  const bar = document.querySelector(".progress span");
  const questions = document.querySelectorAll(".question");
  const quizCard = document.querySelector(".quiz-card");

  if (bar && questions.length && quizCard) {
    const updateProgress = () => {
      const answered = [...questions].filter(
        (question) =>
          question.querySelector("input:checked")
      ).length;

      const percentage =
        (answered / questions.length) * 100;

      bar.style.width = `${percentage}%`;
    };

    quizCard.addEventListener(
      "change",
      updateProgress
    );

    updateProgress();
  }

  /* =========================
     ACTIVE NAV LINK
  ========================= */
  const currentPath =
    window.location.pathname;

  document
    .querySelectorAll(".navlinks a")
    .forEach((link) => {
      const href = link.getAttribute("href");

      if (
        href &&
        href !== "/" &&
        currentPath.startsWith(href)
      ) {
        link.classList.add("active");
      }
    });

  /* =========================
     BUTTON LOADING EFFECT
  ========================= */
  document
    .querySelectorAll("form")
    .forEach((form) => {
      form.addEventListener("submit", () => {
        const button =
          form.querySelector(
            "button[type='submit'], .btn[type='submit']"
          );

        if (!button) return;

        button.classList.add("loading");

        const originalText =
          button.dataset.originalText ||
          button.textContent;

        button.dataset.originalText =
          originalText;

        button.textContent = "Processing...";
      });
    });

});