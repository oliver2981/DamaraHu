# 教程四：JavaScript 国际化与动态内容系统

## 回顾

JavaScript 是房子的**电路和水管**——让页面动起来。前两篇讲了 HTML（结构）和 CSS（装修），这篇讲 JS 怎么让这个网站**支持中英文切换、记住用户的偏好、动态加载内容**。

---

## JS 文件职责再梳理

```
js/
├── i18n-data.js     ← ① 翻译字典：一个巨大的数据对象，存储所有中英文文本
├── i18n-engine.js   ← ② 翻译引擎：提供 getText() / setLang() / updatePageText()
└── shared.js        ← ③ 总控制器：注入导航栏、页脚、暗色模式、语言切换、滚动动画
```

---

## 文件一：`i18n-data.js` —— 翻译字典

### 什么是 i18n？

**i18n** 是 **i**nternationalizatio**n** 的缩写——首字母 `i`、中间 18 个字母、尾字母 `n`。中文叫「国际化」，就是让网站支持多种语言。

### 数据结构

打开这个文件，你会看到一个大对象（Object）：

```javascript
const I18N = {
  zh: {                                   // 中文翻译
    'about.hero.title': '关于我',
    'about.hero.subtitle': '你好，我是胡美婧（Damara），...',
    'nav.home': '首页',
    // ... 100 多个 key
  },
  en: {                                   // 英文翻译
    'about.hero.title': 'About Me',
    'about.hero.subtitle': 'Hello, I\'m Meijing HU (Damara),...',
    'nav.home': 'Home',
    // ... 同样的 key，不同的 value
  }
};
```

### 什么是对象（Object）？

对象是 JavaScript 里最核心的数据结构。你可以把它想象成一本**字典**：

```
字典（Object）
  ├── 中文部分（zh）
  │     ├── 'about.hero.title' → '关于我'
  │     ├── 'about.hero.subtitle' → '你好，我是...'
  │     └── ...
  └── 英文部分（en）
        ├── 'about.hero.title' → 'About Me'
        ├── 'about.hero.subtitle' → 'Hello, I'm...'
        └── ...
```

用代码访问：

```javascript
I18N.zh['about.hero.title']     // → '关于我'
I18N.en['about.hero.title']     // → 'About Me'
```

### Key 的命名规则

所有的 key 都遵循 `页面.区域.元素` 的命名规则：

```
about.hero.title
  │    │    └── 这个区域里的什么元素
  │    └────── 页面的哪个区域
  └─────────── 哪个页面
```

比如 `projects.research.3.title` 就是「项目页 → 研究区域 → 第 4 个项目（从 0 开始数）→ 标题」。

数字索引从 0 开始，这是编程惯例。第 1 个是 0，第 2 个是 1，依此类推。

---

## 文件二：`i18n-engine.js` —— 翻译引擎

这个文件只有 56 行，却驱动了整个网站的语言切换。我们逐函数讲。

### `getText(key)` —— 查字典

```javascript
function getText(key) {
  var lang = document.documentElement.lang || 'zh';
  return (I18N[lang] && I18N[lang][key]) || key;
}
```

逐行解释：

```javascript
var lang = document.documentElement.lang || 'zh';
//     ↑         ↑                          ↑
//   变量名   读取 <html lang="...">     兜底值：如果是空的就用 'zh'

return (I18N[lang] && I18N[lang][key]) || key;
//       ↑            ↑              ↑    ↑
//    先找当前语言   再找这个key    都有值  否则返回 key 本身
//    的翻译表       对应的文字      就返回   (作为fallback)
```

例子：

```javascript
// 假设当前语言是 zh
getText('about.hero.title')
// → lang = 'zh'
// → I18N['zh'] 存在 ✓
// → I18N['zh']['about.hero.title'] = '关于我' ✓
// → 返回 '关于我'

// 如果 key 不存在
getText('nonexistent.key')
// → I18N['zh']['nonexistent.key'] = undefined ✗
// → 返回 'nonexistent.key'（把 key 本身当文字显示，方便开发时调试）
```

### `setLang(lang)` —— 切换语言

```javascript
function setLang(lang) {
  document.documentElement.lang = lang;  // ① 更新 <html lang="...">
  localStorage.setItem('lang', lang);    // ② 记在小本子上
  updatePageText();                      // ③ 立刻刷新所有页面文字
}
```

### `updatePageText()` —— 刷新所有文字

这是引擎里**最重要**的函数：

```javascript
function updatePageText() {
  // 步骤 1：处理纯文字
  var elements = document.querySelectorAll('[data-i18n]');
  for (var i = 0; i < elements.length; i++) {
    var key = elements[i].getAttribute('data-i18n');
    var text = getText(key);
    if (text) {
      elements[i].textContent = text;     // 替换文字内容
    }
  }

  // 步骤 2：处理带 HTML 标签的内容
  var htmlElements = document.querySelectorAll('[data-i18n-html]');
  for (var j = 0; j < htmlElements.length; j++) {
    var htmlKey = htmlElements[j].getAttribute('data-i18n-html');
    var htmlText = getText(htmlKey);
    if (htmlText) {
      htmlElements[j].innerHTML = htmlText;  // 替换 HTML 内容
    }
  }
}
```

**执行流程：**

```
① 找到页面上所有带 data-i18n 属性的元素
   ↓
② 一个一个处理：
    取出 data-i18n 的值（比如 "nav.home"）
    → 调用 getText("nav.home")
    → 查到当前语言的文字 "首页"
    → 把元素的文字内容替换成 "首页"
   ↓
③ 所有元素处理完 → 页面上的文字全部切换完毕
```

---

## 文件三：`shared.js` —— 总控制器

### 这个文件做了什么？

它是全站的「总管家」，在**每个页面**加载完毕后执行：

```
① 注入导航栏 HTML 到页面顶部
② 注入页脚 HTML 到页面底部
③ 高亮当前页面的导航链接
④ 设置暗色模式（从 localStorage 读取用户之前的偏好）
⑤ 设置语言（从 localStorage 读取用户之前的偏好）
⑥ 绑定语言切换按钮的事件
⑦ 绑定暗色模式切换按钮的事件
⑧ 设置移动端汉堡菜单
⑨ 设置滚动淡入动画（IntersectionObserver）
```

### 为什么导航栏和页脚用 JS 注入而不是直接写在 HTML 里？

因为 6 个页面共享完全一样的导航栏和页脚。如果写在 HTML 里：

- **修改导航栏** → 需要改 6 个文件 → 容易漏改、容易出错
- **新增一个页面** → 需要在新页面里手写导航栏 → 可能写错

用 JS 注入：

- **修改导航栏** → 只改 `shared.js` 一个文件 → 6 个页面自动更新
- **新增页面** → 只要引入 `shared.js` 即可

这就是 **DRY 原则**（Don't Repeat Yourself，不要重复自己）。

### 导航栏注入

```javascript
var navHTML =
  '<nav class="navbar">' +
    '<div class="navbar-inner">' +
      '<a href="/" class="nav-logo">Damara Hu</a>' +
      '<ul class="nav-links" id="navLinks">' +
        '<li><a href="/" data-i18n="nav.home" data-page="index">Home</a></li>' +
        '<li><a href="/about.html" data-i18n="nav.about" data-page="about">About</a></li>' +
        // ... 更多链接
      '</ul>' +
      '<button id="langToggle" data-i18n="nav.langToggle">EN</button>' +
      '<button id="themeToggle" data-i18n="nav.themeToggle">🌙</button>' +
    '</div>' +
  '</nav>';

document.body.insertAdjacentHTML('afterbegin', navHTML);
//       ↑                        ↑            ↑
//    找到 <body>              插入位置     要插入的 HTML 字符串
```

`insertAdjacentHTML('afterbegin', ...)` 意思是「在 `<body>` 的开始标签之后、其他内容之前插入」。所以导航栏会出现在页面最顶部。

### 高亮当前页面的导航链接

```javascript
var currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'index';
//  ↑             ↑                   ↑         ↑        ↑          ↑                ↑
// 存结果      当前网址的路径    用 / 切开    取最后一段  去掉 .html      如果空就让它是 'index'

// 例子：网址是 https://xxx.com/about.html
// pathname = '/about.html'
// split('/') = ['', 'about.html']
// pop() = 'about.html'
// replace('.html', '') = 'about'
// currentPage = 'about'

var navLinks = document.querySelectorAll('.nav-links a[data-page]');
for (var i = 0; i < navLinks.length; i++) {
  if (navLinks[i].getAttribute('data-page') === currentPage) {
    navLinks[i].classList.add('active');   // 给当前页的链接加高亮样式
  }
}
```

### 暗色模式实现

```javascript
var themeToggle = document.getElementById('themeToggle');

// 从 localStorage 读取之前的设置
var savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
  document.documentElement.setAttribute('data-theme', 'dark');
}

// 点击切换
themeToggle.addEventListener('click', function() {
  var isDark = document.documentElement.hasAttribute('data-theme');
  if (isDark) {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
  localStorage.setItem('theme', isDark ? 'light' : 'dark');
});
```

### 语言切换实现

```javascript
// 从 localStorage 读取之前的语言选择
var savedLang = localStorage.getItem('lang') || 'zh';
document.documentElement.lang = savedLang;

// 点击按钮切换
document.getElementById('langToggle').addEventListener('click', function() {
  var newLang = document.documentElement.lang === 'zh' ? 'en' : 'zh';
  setLang(newLang);  // 调用 i18n-engine.js 里的函数
});
```

### 滚动动画：IntersectionObserver

```javascript
var observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {                 // 元素进入可见区域
      entry.target.classList.add('visible');    // 加 .visible 类 → CSS 过渡动画启动
      observer.unobserve(entry.target);         // 已经进来了，不再观察
    }
  });
}, { threshold: 0.15 });                       // 15% 可见就算「进来了」

// 给所有带 .fade-in 或 .timeline-item 的元素安排「哨兵」
var animTargets = document.querySelectorAll('.fade-in, .timeline-item');
for (var i = 0; i < animTargets.length; i++) {
  observer.observe(animTargets[i]);
}
```

---

## `localStorage` —— 浏览器的「小本子」

这是一个非常重要的浏览器 API，让网站能记住用户的偏好：

| 操作 | 代码 | 比喻 |
|------|------|------|
| 存 | `localStorage.setItem('theme', 'dark')` | 在小本子上写「暗色模式」 |
| 取 | `localStorage.getItem('theme')` | 翻开小本子看看之前写的什么 |
| 删 | `localStorage.removeItem('theme')` | 擦掉这一行 |

**特点：**
- 数据存在用户的电脑上（不是服务器上）
- **关掉浏览器、重启电脑，数据还在**
- 每个网站的小本子是独立的（你的网站看不到百度写的数据）
- 最大容量约 5MB

本项目用了两个 key：

| Key | 存什么 | 在哪里设置 |
|-----|--------|-----------|
| `lang` | `'zh'` 或 `'en'` | 用户点语言切换按钮时 |
| `theme` | `'dark'` 或 `'light'` | 用户点暗色模式按钮时 |

---

## 页面加载的完整时序图

```
浏览器请求 index.html
         ↓
    HTML 解析开始
         ↓
    <link> 下载 style.css（异步，不阻塞）
         ↓
    <script> 下载并执行 i18n-data.js
         → 定义 I18N 全局变量
         ↓
    <script> 下载并执行 i18n-engine.js
         → 定义 getText()、setLang()、updatePageText()
         ↓
    <script> 下载并执行 shared.js
         → 注入导航栏和页脚 HTML
         → 读取 localStorage，恢复语言和主题
         → 调用 updatePageText()：所有 data-i18n 元素替换为真实文字
         → 设置 IntersectionObserver
         ↓
    HTML 解析完成
         ↓
    CSS 动画启动：fade-in 元素逐个显现
         ↓
    页面完全就绪
```

---

## 总结：四个核心设计原则

1. **内容与结构分离**：文字存在 `i18n-data.js` 里，HTML 只管结构和占位
2. **DRY（不重复）**：导航栏和页脚用 JS 注入一次，6 个页面共享
3. **渐进增强**：即使 JS 加载失败，页面结构依然完整（只是没有导航栏和翻译）
4. **持久化偏好**：用 `localStorage` 记住语言和主题选择

---

## 下一步

现在你已经理解了网站的全部技术细节。下一篇讲如何把这个项目部署到互联网上，让全世界都能访问。

**→ 继续阅读：[教程五：从零部署上线](./教程-05-从零部署上线.md)**

---

> 📝 本教程假设你已阅读前三篇教程。
