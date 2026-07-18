(function() {
  'use strict';

  /* Auto-detect base path for GitHub Pages project sites */
  var basePath = (window.location.pathname.indexOf('/DamaraHu/') !== -1 || window.location.pathname.indexOf('/DamaraHu') !== -1 && window.location.pathname.endsWith('/DamaraHu')) ? '/DamaraHu' : '';

  /* === Nav HTML template === */
  var currentPage = window.location.pathname.replace(/\/$/, '').split('/').pop() || 'index';

  var navHTML = '<nav class="navbar">' +
    '<div class="navbar-inner">' +
      '<a href="' + basePath + '/" class="nav-logo">Damara Hu</a>' +
      '<ul class="nav-links" id="navLinks">' +
        '<li><a href="' + basePath + '/" data-i18n="nav.home" data-page="index">Home</a></li>' +
        '<li><a href="' + basePath + '/about" data-i18n="nav.about" data-page="about">About</a></li>' +
        '<li><a href="' + basePath + '/education" data-i18n="nav.education" data-page="education">Education</a></li>' +
        '<li><a href="' + basePath + '/projects" data-i18n="nav.projects" data-page="projects">Projects</a></li>' +
        '<li><a href="' + basePath + '/interests" data-i18n="nav.interests" data-page="interests">Interests</a></li>' +
        '<li><a href="' + basePath + '/contact" data-i18n="nav.contact" data-page="contact">Contact</a></li>' +
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
      '<h4 class="footer-brand">Damara Hu</h4>' +
      '<p class="footer-tagline" data-i18n="home.hero.tagline">Student · Researcher · Creator</p>' +
      '<nav class="footer-links">' +
        '<a href="' + basePath + '/" data-i18n="nav.home">Home</a>' +
        '<a href="' + basePath + '/about" data-i18n="nav.about">About</a>' +
        '<a href="' + basePath + '/education" data-i18n="nav.education">Education</a>' +
        '<a href="' + basePath + '/projects" data-i18n="nav.projects">Projects</a>' +
        '<a href="' + basePath + '/interests" data-i18n="nav.interests">Interests</a>' +
        '<a href="' + basePath + '/contact" data-i18n="nav.contact">Contact</a>' +
      '</nav>' +
      '<p class="footer-copyright" data-i18n="footer.copyright">© 2026 Damara Hu. All rights reserved.</p>' +
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
