/**
 * CareerLens UI — Premium Interactions
 * Powered by IntersectionObserver for scroll-triggered animations
 */
(function () {
  'use strict';

  // ----------------------------------------------------------
  // Mobile menu toggle
  // ----------------------------------------------------------
  const menuBtn = document.querySelector('[data-menu-btn]');
  const nav = document.querySelector('[data-nav]');

  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      const expanded = menuBtn.getAttribute('aria-expanded') === 'true';
      menuBtn.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('open');

      // Prevent body scroll when menu is open on mobile
      if (window.innerWidth <= 768) {
        document.body.style.overflow = nav.classList.contains('open') ? 'hidden' : '';
      }
    });

    // Close menu on nav link click (mobile)
    nav.querySelectorAll('.nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  // ----------------------------------------------------------
  // File input UX
  // ----------------------------------------------------------
  const resumeInput = document.querySelector('#resume');
  const fileName = document.querySelector('[data-file-name]');
  const fileDrop = document.querySelector('[data-file-drop]');

  if (resumeInput && fileName) {
    resumeInput.addEventListener('change', function () {
      const selectedFile = resumeInput.files && resumeInput.files[0];
      if (selectedFile) {
        fileName.textContent = selectedFile.name;
        if (fileDrop) {
          fileDrop.classList.add('has-file');
        }
      } else {
        fileName.textContent = 'Choose your resume';
        if (fileDrop) {
          fileDrop.classList.remove('has-file');
        }
      }
    });
  }

  // ----------------------------------------------------------
  // Scroll-triggered animations via IntersectionObserver
  // ----------------------------------------------------------
  function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.fade-in, .stagger, .scale-in');

    if (animatedElements.length === 0) return;

    // Respect reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      animatedElements.forEach(function (el) {
        el.classList.add('visible');
      });
      // Also reveal score values immediately
      document.querySelectorAll('.score-ring-value').forEach(function (el) {
        el.style.opacity = '1';
      });
      return;
    }

    // Use IntersectionObserver with rootMargin for slightly early trigger
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            // Add small staggered delay for cards within a grid
            const parent = entry.target.closest('.stagger');
            if (parent) {
              // The stagger is handled by CSS nth-child delays
              // Just make the parent visible to trigger all children
              parent.classList.add('visible');
              // Unobserve parent to prevent re-triggering
              observer.unobserve(parent);
            } else {
              entry.target.classList.add('visible');
              observer.unobserve(entry.target);
            }
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    // Observe standalone elements
    animatedElements.forEach(function (el) {
      // If it's inside a .stagger, observe the parent instead
      const staggerParent = el.closest('.stagger');
      if (staggerParent && staggerParent !== el) {
        if (!staggerParent._observed) {
          observer.observe(staggerParent);
          staggerParent._observed = true;
        }
      } else if (!el.closest('.stagger')) {
        observer.observe(el);
      }
    });
  }

  // ----------------------------------------------------------
  // Animated score ring values (counter animation)
  // ----------------------------------------------------------
  function animateCounters() {
    const scoreValues = document.querySelectorAll('.score-ring-value');
    if (scoreValues.length === 0) return;

    scoreValues.forEach(function (el) {
      const text = el.textContent.trim();
      const match = text.match(/^([\d.]+)\s*(\/10|%)?$/);
      if (!match) return;

      const target = parseFloat(match[1]);
      const unit = match[2] || '';
      const duration = 1500;
      const startTime = performance.now();

      // Set initial value to 0 before starting animation to avoid visual jump
      if (unit === '/10') {
        el.innerHTML = '0.0<span class="score-unit">/10</span>';
      } else {
        el.textContent = '0' + (unit || '');
      }

      // Show the element (it starts hidden to prevent flash of final value)
      el.style.opacity = '1';

      function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = eased * target;

        if (unit === '/10') {
          el.innerHTML = current.toFixed(1) + '<span class="score-unit">/10</span>';
        } else if (unit === '%') {
          el.innerHTML = Math.round(current) + '<span class="score-unit">%</span>';
        } else {
          el.textContent = Math.round(current) + unit;
        }

        if (progress < 1) {
          requestAnimationFrame(update);
        }
      }

      requestAnimationFrame(update);
    });
  }

  // ----------------------------------------------------------
  // Initialize on DOM ready
  // ----------------------------------------------------------
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initScrollAnimations();
      animateCounters();
    });
  } else {
    initScrollAnimations();
    animateCounters();
  }

  // ----------------------------------------------------------
  // Theme toggle (dark/light) with localStorage persistence
  // ----------------------------------------------------------
  var themeToggle = document.querySelector('[data-theme-toggle]');
  var themeSun = document.querySelector('[data-theme-sun]');
  var themeMoon = document.querySelector('[data-theme-moon]');
  var html = document.documentElement;
  var STORAGE_KEY = 'careerlens-theme';

  // Safely read/write localStorage (guards against private browsing exceptions)
  function storageGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function storageSet(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* noop */ }
  }

  function getPreferredTheme() {
    var stored = storageGet(STORAGE_KEY);
    if (stored === 'light' || stored === 'dark') return stored;
    // Respect OS preference
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function applyTheme(theme) {
    // Add transitioning class for smooth CSS transitions
    // (Transitions scoped to specific properties via CSS, not `all`)
    html.classList.add('theme-transitioning');

    if (theme === 'light') {
      html.setAttribute('data-theme', 'light');
      if (themeSun) themeSun.style.display = 'none';
      if (themeMoon) themeMoon.style.display = '';
      if (themeToggle) themeToggle.setAttribute('aria-label', 'Switch to dark theme');
    } else {
      html.removeAttribute('data-theme');
      if (themeSun) themeSun.style.display = '';
      if (themeMoon) themeMoon.style.display = 'none';
      if (themeToggle) themeToggle.setAttribute('aria-label', 'Switch to light theme');
    }

    storageSet(STORAGE_KEY, theme);

    // Remove transitioning class after animation completes
    setTimeout(function () {
      html.classList.remove('theme-transitioning');
    }, 350);
  }

  function toggleTheme() {
    var current = html.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    var next = current === 'light' ? 'dark' : 'light';
    applyTheme(next);
  }

  // Apply saved/preferred theme on load
  if (themeToggle) {
    applyTheme(getPreferredTheme());
    themeToggle.addEventListener('click', toggleTheme);
  }

  // Listen for OS theme changes (when no stored preference)
  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function (e) {
    if (!storageGet(STORAGE_KEY)) {
      applyTheme(e.matches ? 'light' : 'dark');
    }
  });

  // ----------------------------------------------------------
  // Smooth anchor scroll for same-page nav links
  // ----------------------------------------------------------
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = 80;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth',
        });
      }
    });
  });
})();
