// i18n engine — language functions. Content data is in js/i18n-data.js

function getText(key) {
  var lang = document.documentElement.lang || 'zh';
  return (I18N[lang] && I18N[lang][key]) || key;
}

function setLang(lang) {
  document.documentElement.lang = lang;
  localStorage.setItem('lang', lang);
  updatePageText();
}

function updatePageText() {
  // Text content
  var elements = document.querySelectorAll('[data-i18n]');
  for (var i = 0; i < elements.length; i++) {
    var key = elements[i].getAttribute('data-i18n');
    var text = getText(key);
    if (text) {
      if (elements[i].tagName === 'INPUT' || elements[i].tagName === 'TEXTAREA') {
        elements[i].placeholder = text;
      } else {
        elements[i].textContent = text;
      }
    }
  }

  // HTML content (for rich text with markup)
  var htmlElements = document.querySelectorAll('[data-i18n-html]');
  for (var j = 0; j < htmlElements.length; j++) {
    var htmlKey = htmlElements[j].getAttribute('data-i18n-html');
    var htmlText = getText(htmlKey);
    if (htmlText) {
      htmlElements[j].innerHTML = htmlText;
    }
  }

  // Attribute content (src, href, content)
  var attrElements = document.querySelectorAll('[data-i18n-attr]');
  for (var k = 0; k < attrElements.length; k++) {
    var el = attrElements[k];
    var spec = el.getAttribute('data-i18n-attr');
    var parts = spec.split(',');
    for (var p = 0; p < parts.length; p++) {
      var kv = parts[p].split(':');
      var attrName = kv[0].trim();
      var attrKey = kv.slice(1).join(':').trim();
      var val = getText(attrKey);
      if (val) {
        el.setAttribute(attrName, val);
      }
    }
  }
}
