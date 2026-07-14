(function() {
  'use strict';

  /* === Vercel Web Analytics === */
  var analyticsScript = document.createElement('script');
  analyticsScript.defer = true;
  analyticsScript.src = 'https://cdn.vercel-insights.com/v1/script.js';
  document.head.appendChild(analyticsScript);

  /* === Nav HTML template === */
  var currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'index';

  var navHTML = '<nav class="navbar">' +
    '<div class="navbar-inner">' +
      '<a href="/" class="nav-logo">Damara Hu</a>' +
      '<ul class="nav-links" id="navLinks">' +
        '<li><a href="/" data-i18n="nav.home" data-page="index">Home</a></li>' +
        '<li><a href="/about.html" data-i18n="nav.about" data-page="about">About</a></li>' +
        '<li><a href="/education.html" data-i18n="nav.education" data-page="education">Education</a></li>' +
        '<li><a href="/projects.html" data-i18n="nav.projects" data-page="projects">Projects</a></li>' +
        '<li><a href="/interests.html" data-i18n="nav.interests" data-page="interests">Interests</a></li>' +
      '</ul>' +
      '<div class="nav-actions">' +
        '<button class="nav-btn" id="langToggle" data-i18n="nav.langToggle" aria-label="Switch language">EN</button>' +
        '<button class="nav-btn" id="themeToggle" data-i18n="nav.themeToggle" aria-label="Toggle dark mode">🌙</button>' +
        '<button class="hamburger" id="hamburger" aria-label="Menu">' +
          '<span></span><span></span><span></span>' +
        '</button>' +
      '</div>' +
    '</div>' +
  '</nav>';

  /* === Footer HTML template === */
  var footerHTML = '<footer class="site-footer">' +
    '<div class="footer-inner">' +
      '<div class="footer-col">' +
        '<h4>Damara Hu</h4>' +
        '<p data-i18n="home.hero.tagline">Student · Researcher · Creator</p>' +
      '</div>' +
      '<div class="footer-col">' +
        '<h4 data-i18n="footer.quickLinks">Quick Links</h4>' +
        '<p><a href="/" data-i18n="nav.home">Home</a></p>' +
        '<p><a href="/about.html" data-i18n="nav.about">About</a></p>' +
        '<p><a href="/education.html" data-i18n="nav.education">Education</a></p>' +
        '<p><a href="/projects.html" data-i18n="nav.projects">Projects</a></p>' +
        '<p><a href="/interests.html" data-i18n="nav.interests">Interests</a></p>' +
      '</div>' +
    '<div class="footer-bottom">' +
      '<p data-i18n="footer.copyright">© 2026 Damara Hu. All rights reserved.</p>' +
    '</div>' +
  '</footer>';

  /* === Inject === */
  document.body.insertAdjacentHTML('afterbegin', navHTML);
  document.body.insertAdjacentHTML('beforeend', footerHTML);

  /* === Active nav link === */
  var navLinks = document.querySelectorAll('.nav-links a[data-page]');
  for (var i = 0; i < navLinks.length; i++) {
    if (navLinks[i].getAttribute('data-page') === currentPage) {
      navLinks[i].classList.add('active');
    }
  }

  /* === Dark Mode === */
  var themeToggle = document.getElementById('themeToggle');
  function applyTheme(dark) {
    if (dark) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }
  var savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    applyTheme(true);
  }
  themeToggle.addEventListener('click', function() {
    var isDark = document.documentElement.hasAttribute('data-theme');
    applyTheme(!isDark);
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
  });

  /* === Language === */
  var savedLang = localStorage.getItem('lang') || 'zh';
  document.documentElement.lang = savedLang;

  document.getElementById('langToggle').addEventListener('click', function() {
    var newLang = document.documentElement.lang === 'zh' ? 'en' : 'zh';
    setLang(newLang);
    localStorage.setItem('lang', newLang);
  });

  /* Update text after nav/footer injection */
  updatePageText();

  /* === Mobile Menu === */
  var hamburger = document.getElementById('hamburger');
  var navLinksContainer = document.getElementById('navLinks');
  hamburger.addEventListener('click', function() {
    navLinksContainer.classList.toggle('open');
  });

  /* === Scroll Animations === */
  var observerOptions = { threshold: 0.15, rootMargin: '0px 0px -40px 0px' };

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  var animTargets = document.querySelectorAll('.fade-in, .timeline-item');
  for (var i = 0; i < animTargets.length; i++) {
    observer.observe(animTargets[i]);
  }

  /* Re-observe after dynamic content changes */
  window.reobserveAnimations = function() {
    var targets = document.querySelectorAll('.fade-in:not(.visible), .timeline-item:not(.visible)');
    for (var i = 0; i < targets.length; i++) {
      observer.observe(targets[i]);
    }
  };
})();
