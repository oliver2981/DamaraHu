# 教程六：JavaScript 代码逐行解析

## 回顾

前五篇教程覆盖了 HTML、CSS、i18n 和部署。本篇从**纯粹的代码角度**，逐行解释 `shared.js` 和 `i18n-engine.js` 中的每一个编程概念、每一个 API 调用，以及它们为什么这么写。

---

## JS 文件清单

```
js/
├── i18n-data.js      ← 数据层：中英文翻译字典（纯数据，不包含逻辑）
├── i18n-engine.js    ← 引擎层：三个函数，负责把数据"翻译"成页面文字
└── shared.js         ← 控制层：所有页面共享的行为逻辑
```

加载顺序是 `i18n-data.js` → `i18n-engine.js` → `shared.js`。**顺序不能乱**——后面依赖前面定义的变量和函数。

---

## 第一部分：`shared.js` —— 外层结构

### 1.1 IIFE：立即执行函数

```javascript
(function() {
  // ... 所有代码 ...
})();
```

这叫做 **IIFE**（Immediately Invoked Function Expression，立即执行函数表达式）。

**拆解语法：**

```
(function() { ... })   ← 用括号包裹函数定义，使其成为一个"表达式"
                    ()  ← 第二个括号立即调用它
```

**为什么要这样写？**

JavaScript 中在顶层用 `var` 声明的变量会成为**全局变量**，污染全局命名空间。如果页面引入了其他第三方脚本，全局变量可能互相冲突。

```javascript
// ❌ 不用 IIFE
var currentPage = 'index';    // 全局变量，可能与其他脚本冲突
var observer = new IntersectionObserver(...);

// ✅ 用 IIFE
(function() {
  var currentPage = 'index';  // 局部变量，在函数外部不可见
  var observer = new IntersectionObserver(...);
})();
```

IIFE 创建了一个**函数作用域**，所有 `var` 变量都被关在里面，不会泄露到全局。

### 1.2 `'use strict'`：严格模式

```javascript
'use strict';
```

这是 JavaScript 的**严格模式**指令。它让浏览器以更严格的规则执行代码，帮你尽早暴露潜在的错误：

| 非严格模式（没有 `'use strict'`） | 严格模式 |
|---|---|
| 给未声明的变量赋值不会报错 | 直接抛出 `ReferenceError` |
| 函数参数重名不报错 | 抛出 `SyntaxError` |
| `this` 在普通函数中指向 `window` | `this` 为 `undefined` |

**一句话：** 严格模式让隐式的错误变成显式的报错，更容易发现 bug。

---

## 第二部分：Vercel Web Analytics 动态加载

```javascript
var analyticsScript = document.createElement('script');
analyticsScript.defer = true;
analyticsScript.src = 'https://cdn.vercel-insights.com/v1/script.js';
document.head.appendChild(analyticsScript);
```

这 4 行代码动态创建了一个 `<script>` 标签并注入到页面 `<head>` 中，等价于在 HTML 里写：

```html
<script defer src="https://cdn.vercel-insights.com/v1/script.js"></script>
```

### 逐行解析

**第 1 行：** `document.createElement('script')`

`document.createElement(tagName)` 创建一个指定标签名的 DOM 元素。此时它只存在于内存中，尚未插入页面。

```javascript
var div = document.createElement('div');   // 创建一个 <div>（在内存中）
var p = document.createElement('p');       // 创建一个 <p>（在内存中）
```

**第 2 行：** `analyticsScript.defer = true`

`defer` 属性告诉浏览器：「继续解析 HTML，等页面解析完成后再执行这个脚本」。

- 不加 `defer`：浏览器遇到脚本时**暂停解析**，下载并执行完再继续
- 加了 `defer`：脚本异步下载，等 HTML 解析完再按顺序执行

对于统计分析脚本，使用 `defer` 保证它不影响页面渲染性能。

**第 3 行：** `analyticsScript.src = 'https://cdn.vercel-insights.com/v1/script.js'`

设置脚本的源地址。注意此时脚本还**没有开始下载**——只有插入 DOM 后才会触发下载。

**第 4 行：** `document.head.appendChild(analyticsScript)`

将脚本元素添加到 `<head>` 中。**插入 DOM 后，浏览器才开始下载脚本。** `appendChild` 将元素添加为父元素的最后一个子节点。

### 为什么用 JS 动态注入而不是直接写 `<script>` 标签？

因为它只在 `shared.js` 中写一次，6 个页面就全部拥有了分析功能。如果直接写在 HTML 中，需要改 6 个文件。

---

## 第三部分：导航栏注入

### 3.1 检测当前页面

```javascript
var currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'index';
```

这行代码从浏览器地址栏提取当前页面名。拆解如下：

```
window.location.pathname   →  "/about.html"      （网址中域名后面的路径部分）
.split('/')                →  ["", "about.html"]  （用 / 切开成数组）
.pop()                     →  "about.html"        （取数组最后一个元素）
.replace('.html', '')      →  "about"            （去掉 .html 后缀）
|| 'index'                 →  如果是空字符串（首页 "/"），则取 "index"
```

| 网址 | `pathname` | `.pop()` 后 | 最终 `currentPage` |
|---|---|---|---|
| `https://xxx.com/` | `/` | `""` | `"index"` |
| `https://xxx.com/about.html` | `/about.html` | `"about.html"` | `"about"` |
| `https://xxx.com/education.html` | `/education.html` | `"education.html"` | `"education"` |

### 3.2 构建 HTML 字符串

```javascript
var navHTML = '<nav class="navbar">' +
  '<div class="navbar-inner">' +
    '<a href="/" class="nav-logo">Damara Hu</a>' +
    '<ul class="nav-links" id="navLinks">' +
      '<li><a href="/" data-i18n="nav.home" data-page="index">Home</a></li>' +
      // ... 更多链接
    '</ul>' +
    // ... 按钮
  '</div>' +
'</nav>';
```

**为什么要用 `+` 拼接字符串？** 因为 JavaScript 的字符串不能跨行（除非用 ES6 的模板字符串 `` ` ``），用 `+` 把多行连接成一个完整的字符串。

**`data-page` 属性的作用：** 给每个导航链接标记它对应的页面名（`"index"`, `"about"` 等），之后用来高亮当前页面的链接。

**`data-i18n` 属性的作用：** 给 i18n 引擎做标记。页面加载后，`updatePageText()` 会扫描所有带这个属性的元素，把占位英文替换成对应的中/英文。

### 3.3 注入到页面

```javascript
document.body.insertAdjacentHTML('afterbegin', navHTML);
```

`insertAdjacentHTML(position, text)` 不破坏现有 DOM 结构，直接把 HTML 字符串解析并插入到指定位置。

`position` 有 4 个选项：

```
<!-- beforebegin -->    ← 元素外部、前面
<div>
  <!-- afterbegin -->   ← 元素内部、第一个子节点之前
  （原有内容）
  <!-- beforeend -->    ← 元素内部、最后一个子节点之后
</div>
<!-- afterend -->       ← 元素外部、后面
```

`'afterbegin'` 把导航栏插入到 `<body>` 的最开头，所以它出现在所有页面内容之前。

---

## 第四部分：页脚注入

```javascript
var footerHTML = '<footer class="site-footer">' +
  '<div class="footer-inner">' +
    '<h4 class="footer-brand">Damara Hu</h4>' +
    '<p class="footer-tagline" data-i18n="home.hero.tagline">Student · Researcher · Creator</p>' +
    '<nav class="footer-links">' +
      '<a href="/" data-i18n="nav.home">Home</a>' +
      '<a href="/about.html" data-i18n="nav.about">About</a>' +
      // ... 更多链接
    '</nav>' +
    '<p class="footer-copyright" data-i18n="footer.copyright">© 2026 Damara Hu. All rights reserved.</p>' +
  '</div>' +
'</footer>';
```

### 页脚结构

```
┌─────────────────────────────────────┐
│           Damara Hu                  │  ← 品牌名
│    Student · Researcher · Creator    │  ← 标语（支持 i18n 翻译）
│                                     │
│   Home · About · Education · ...    │  ← 横向导航链接（以 · 分隔）
│                                     │
│  © 2026 Damara Hu. All rights ...   │  ← 版权信息（支持 i18n 翻译）
└─────────────────────────────────────┘
```

CSS 将整个 `.footer-inner` 设为 `text-align: center`，链接用 `flexbox` 水平排列并以 `·`（middle dot，`\00B7`）分隔，视觉上简洁统一。

对比旧版（曾经有一个三列布局，包含独立的 "Quick Links" 和 "Connect" 社交链接列），现在的设计更轻量、不会因内容高度不均而失衡。

### 注入位置

```javascript
document.body.insertAdjacentHTML('beforeend', footerHTML);
```

`'beforeend'` 把页脚插入到 `<body>` 的最末尾，所以它出现在所有页面内容之后。

---

## 第五部分：高亮当前页面的导航链接

```javascript
var navLinks = document.querySelectorAll('.nav-links a[data-page]');
for (var i = 0; i < navLinks.length; i++) {
  if (navLinks[i].getAttribute('data-page') === currentPage) {
    navLinks[i].classList.add('active');
  }
}
```

### 逐行解析

**`document.querySelectorAll('.nav-links a[data-page]')`**

CSS 选择器 `.nav-links a[data-page]` 的含义：

| 选择器部分 | 含义 | 匹配 |
|---|---|---|
| `.nav-links` | class 为 `nav-links` 的元素 | `<ul class="nav-links">` |
| ` ` (空格) | 后代选择器 | 在 `.nav-links` 内部查找 |
| `a` | `<a>` 标签 | 所有链接 |
| `[data-page]` | 属性选择器 | 带有 `data-page` 属性的元素 |

`querySelectorAll` 返回一个 **NodeList**（类似数组的节点列表），可以用 `for` 循环遍历。

**`getAttribute('data-page')`**

读取元素的 `data-page` 属性值。对比：

```javascript
element.getAttribute('data-page')   // 读取任意属性，返回字符串
element.dataset.page                // 专门读取 data-* 属性（data-page → .page）
```

两种写法等价，`getAttribute` 更直观，`dataset` 更简洁。

**`classList.add('active')`**

`classList` 是元素类名的操作接口：

```javascript
el.classList.add('active');      // 添加类名
el.classList.remove('active');   // 移除类名
el.classList.toggle('active');   // 有则移除，无则添加
el.classList.contains('active'); // 是否包含（返回 true/false）
```

CSS 中定义了 `.nav-links a.active { ... }`，加上 `active` 后该链接显示高亮样式。

---

## 第六部分：暗色模式

```javascript
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
```

### 逐行解析

**`document.getElementById('themeToggle')`**

通过 `id` 属性获取单个元素。与 `querySelector` 的区别：

| 方法 | 选择器类型 | 性能 | 返回 |
|---|---|---|---|
| `getElementById('x')` | 只能按 id | 最快 | 单个元素或 `null` |
| `querySelector('#x')` | 任意 CSS 选择器 | 稍慢 | 单个元素或 `null` |
| `querySelectorAll('.x')` | 任意 CSS 选择器 | 稍慢 | NodeList |

因为 id 在页面中是唯一的，用 `getElementById` 是最精确高效的方式。

**`document.documentElement`**

指向 `<html>` 根元素。暗色模式的实现原理是在 `<html>` 上添加/移除 `data-theme="dark"` 属性：

```html
<!-- 日间模式 -->
<html lang="zh">...</html>

<!-- 夜间模式 -->
<html lang="zh" data-theme="dark">...</html>
```

CSS 通过属性选择器覆盖颜色：

```css
:root {
  --bg: #FFFFFF;        /* 日间：白底 */
  --text: #1A1A2E;      /* 日间：深色字 */
}

[data-theme="dark"] {
  --bg: #1A1A2E;        /* 夜间：深色底 */
  --text: #E8E8F0;      /* 夜间：浅色字 */
}
```

所有元素的颜色都引用了 `var(--bg)`、`var(--text)` 等变量，切换主题时只需要改变变量值，全页面自动跟随——无需遍历每个元素。

**`setAttribute` vs `removeAttribute`**

```javascript
el.setAttribute('data-theme', 'dark');    // 设置属性：<html data-theme="dark">
el.removeAttribute('data-theme');          // 删除属性：<html>
el.hasAttribute('data-theme');            // 检查是否存在：返回 true 或 false
```

### 点击处理流程

```
用户点击按钮
    ↓
检查 <html> 是否有 data-theme 属性（当前是暗色还是亮色？）
    ↓
    ├── 当前暗色 → 调用 applyTheme(false) → 移除属性 → 变回亮色 → 存 'light'
    │
    └── 当前亮色 → 调用 applyTheme(true)  → 设置属性 → 变暗     → 存 'dark'
```

**`isDark ? 'light' : 'dark'`** 是三元运算符：`条件 ? 真时的值 : 假时的值`。这里保存的是**切换后**的状态。

---

## 第七部分：语言切换

```javascript
var savedLang = localStorage.getItem('lang') || 'zh';
document.documentElement.lang = savedLang;

document.getElementById('langToggle').addEventListener('click', function() {
  var newLang = document.documentElement.lang === 'zh' ? 'en' : 'zh';
  setLang(newLang);
  localStorage.setItem('lang', newLang);
});
```

### 逐行解析

**`localStorage.getItem('lang') || 'zh'`**

`||` 是逻辑「或」运算符。这里用作**默认值模式**：

```javascript
var savedLang = localStorage.getItem('lang') || 'zh';
//              ↑ 先取值                        ↑ 如果为假（null/空），用备选
```

- 用户第一次访问 → `localStorage.getItem('lang')` 返回 `null` → `null || 'zh'` → `'zh'`
- 用户之前选了英文 → 返回 `'en'` → `'en' || 'zh'` → `'en'`

**`document.documentElement.lang`**

设置 `<html lang="zh">` 或 `<html lang="en">`。这有两个作用：
1. 搜索引擎和浏览器能识别页面语言
2. `i18n-engine.js` 里的 `getText()` 读取这个值来决定用哪个语言字典

### 点击处理

```javascript
var newLang = document.documentElement.lang === 'zh' ? 'en' : 'zh';
```

中英文互相切换。只在两种语言之间翻转，简单可靠。

```javascript
setLang(newLang);
```

调用 `i18n-engine.js` 中定义的 `setLang()` 函数（详见第九部分），它会更新 `<html lang="...">`、存 localStorage、然后刷新全页面文字。

---

## 第八部分：移动端汉堡菜单

```javascript
var hamburger = document.getElementById('hamburger');
var navLinksContainer = document.getElementById('navLinks');
hamburger.addEventListener('click', function() {
  navLinksContainer.classList.toggle('open');
});
```

### 工作原理

1. 桌面端（宽度 > 768px）：CSS 中 `.nav-links` 正常显示为水平横排
2. 移动端（宽度 ≤ 768px）：CSS 中 `.nav-links` 默认隐藏（`display: none`），只有加上 `.open` 类才展开

```css
/* 移动端 */
@media (max-width: 768px) {
  .nav-links {
    display: none;               /* 默认隐藏 */
    flex-direction: column;      /* 纵排 */
  }
  .nav-links.open {
    display: flex;               /* 点击汉堡后展开 */
  }
}
```

**`classList.toggle('open')`**

```javascript
// 第一次点击：没有 open → 加上 open → 菜单展开
// 第二次点击：有 open   → 移除 open → 菜单收起
// 第三次点击：又没有了 → 加上 open → 菜单展开
// ...以此类推
```

不需要写 `if` 判断，`toggle` 自动处理「有则删，无则加」。

### 汉堡按钮的 HTML 结构

```html
<button class="hamburger" id="hamburger" aria-label="Menu">
  <span></span><span></span><span></span>    ← 三道横线
</button>
```

CSS 将三个 `<span>` 渲染为三道横线，点击时可能配合过渡动画变成 X 形状（取决于具体 CSS 实现）。`aria-label="Menu"` 为屏幕阅读器提供无障碍标签。

---

## 第九部分：`i18n-engine.js` —— 翻译引擎

这是全站中英文切换的核心。三个函数构成了一个完整的翻译管线。

### 9.1 `getText(key)` —— 查字典

```javascript
function getText(key) {
  var lang = document.documentElement.lang || 'zh';
  return (I18N[lang] && I18N[lang][key]) || key;
}
```

**执行流程：**

```
调用 getText('nav.home')
    ↓
读取 <html lang=""> → 得到 'zh' 或 'en'
    ↓
查找 I18N[lang][key]
    ├── 'zh' → I18N.zh['nav.home'] → '首页' ✓ 返回
    └── 'en' → I18N.en['nav.home'] → 'Home' ✓ 返回
    ↓
如果找不到翻译 → 返回原始 key 作为兜底（至少显示点什么）
```

**逻辑运算符详解：**

```javascript
return (I18N[lang] && I18N[lang][key]) || key;
//       ↑                            ↑
//       第一部分                      第二部分
```

- **第一部分 `I18N[lang] && I18N[lang][key]`：** 先检查语言字典是否存在，再取翻译值。如果字典不存在（比如新加了语言但忘了定义），`&&` 的**短路求值**让它在第一步就返回 `undefined`，不会因为访问 `undefined[key]` 而报错。
- **第二部分 `|| key`：** 如果翻译值为假（`undefined`、`null`、`""`），返回原始 key 作为兜底文字。

**短路求值（Short-circuit evaluation）：**

```javascript
A && B   // 如果 A 是假值，直接返回 A，不计算 B
A || B   // 如果 A 是真值，直接返回 A，不计算 B
```

### 9.2 `setLang(lang)` —— 切换语言

```javascript
function setLang(lang) {
  document.documentElement.lang = lang;
  localStorage.setItem('lang', lang);
  updatePageText();
}
```

**三步操作：**

| 步骤 | 代码 | 作用 |
|---|---|---|
| 1 | `document.documentElement.lang = lang` | 更新 `<html lang="">`，下次 `getText()` 会读新语言 |
| 2 | `localStorage.setItem('lang', lang)` | 保存到浏览器，下次访问自动恢复 |
| 3 | `updatePageText()` | 立刻刷新页面上所有 `data-i18n` 元素的文字 |

**顺序很重要：** 必须先更新 `lang`（步骤 1），再刷新文字（步骤 3）。因为 `updatePageText()` 内部调用 `getText()`，而 `getText()` 读取 `document.documentElement.lang` 来决定用哪个语言字典。

### 9.3 `updatePageText()` —— 刷新全页面文字

这个函数是翻译流程的终点——遍历 DOM 并把占位文字全部替换为翻译后的文字。

#### 第一遍：普通文本内容

```javascript
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
```

**`[data-i18n]` 选择器：** 找到页面上所有带 `data-i18n` 属性的元素。

**表单元素的特殊处理：** `<input>` 和 `<textarea>` 没有文字内容（它们的内容是 `value`），但可以用 `placeholder` 显示占位提示。所以对表单元素设置 `placeholder`，对普通元素设置 `textContent`。

```javascript
// 对 <p data-i18n="nav.home">Home</p>
// → p.textContent = '首页'

// 对 <input data-i18n="form.search" placeholder="Search">
// → input.placeholder = '搜索'
```

**为什么用 `textContent` 而不是 `innerHTML`？**

| 属性 | 行为 | 安全性 |
|---|---|---|
| `textContent` | 设置纯文字，HTML 标签会原样显示 | 安全，无 XSS 风险 |
| `innerHTML` | 解析并渲染 HTML 标签 | 如果内容来自用户输入则有 XSS 风险 |

因为翻译文本都是开发人员控制的，用 `textContent` 就足够了。

#### 第二遍：富文本内容（含 HTML 标签）

```javascript
var htmlElements = document.querySelectorAll('[data-i18n-html]');
for (var j = 0; j < htmlElements.length; j++) {
  var htmlKey = htmlElements[j].getAttribute('data-i18n-html');
  var htmlText = getText(htmlKey);
  if (htmlText) {
    htmlElements[j].innerHTML = htmlText;
  }
}
```

有些翻译内容包含 HTML 标签（如 `<li>`、`<strong>`），这时候不能设置 `textContent`（会把 `<li>` 当纯文字显示），需要用 `innerHTML` 来渲染。

项目中使用 `data-i18n-html` 的例子：

```javascript
'projects.research.0.desc': '<li><strong>研究过程：</strong>对姜黄素...</li>'
```

`data-i18n-html` 和 `data-i18n` 使用不同的属性名，让开发者明确标记哪些内容包含 HTML，降低 XSS 风险。

#### 第三遍：属性值

```javascript
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
```

这个功能用于翻译元素的**属性值**（而不是文本内容）。使用格式：

```html
<img data-i18n-attr="alt:about.hero.title, title:about.hero.title"
     alt="About Me" title="About Me" src="...">
```

**解析过程：**

```
"alt:about.hero.title, title:about.hero.title"
    ↓ split(',')
["alt:about.hero.title", " title:about.hero.title"]
    ↓ 遍历每个，split(':')
["alt", "about.hero.title"]
["title", "about.hero.title"]
    ↓
el.setAttribute('alt', getText('about.hero.title'))
el.setAttribute('title', getText('about.hero.title'))
```

**`kv.slice(1).join(':')` 的作用：** 因为 key 中可能包含冒号（虽然本项目不会），用 `slice(1)` 取第二部分及以后，用 `join(':')` 再拼回来。这是一个防御性写法，确保 key 中的冒号不会被误拆。

---

## 第十部分：`shared.js` —— 页面加载协调

### 10.1 调用 `updatePageText()`

```javascript
updatePageText();
```

这行代码在 `shared.js` 的中部被调用，时机非常关键：

```
① 注入导航栏 HTML → DOM 中出现新的 data-i18n 元素
② 注入页脚 HTML   → DOM 中出现新的 data-i18n 元素
③ 恢复 savedLang  → 设置 <html lang="zh/en">
④ 调用 updatePageText() → 所有 data-i18n 元素被翻译
```

必须在注入导航和页脚**之后**、恢复语言**之后**调用，否则新注入的导航和页脚还是英文占位文字。

### 10.2 `window.reobserveAnimations` —— 暴露全局方法

```javascript
window.reobserveAnimations = function() {
  var targets = document.querySelectorAll('.fade-in:not(.visible), .timeline-item:not(.visible)');
  for (var i = 0; i < targets.length; i++) {
    observer.observe(targets[i]);
  }
};
```

因为整个 `shared.js` 包裹在 IIFE 中，内部变量 `observer` 在外部不可见。但有些页面（如 `interests.html`）会动态加载新内容（图片、视频卡片），这些新内容也有 `.fade-in` 类，需要被 Observer 观察。

**`window.reobserveAnimations = ...`** 把内部函数暴露到全局对象 `window` 上，使得其他脚本可以调用：

```javascript
// 在 interests.html 动态加载图片后：
window.reobserveAnimations();  // 新图片也会淡入
```

**选择器 `:not(.visible)` 的含义：** 只观察**尚未**出现的元素。已经显示过的元素（有 `.visible` 类）不再重复观察，避免浪费。

---

## 第十一部分：IntersectionObserver 滚动动画

```javascript
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
```

### IntersectionObserver 是什么？

一个浏览器内置 API，用于监控元素是否进入了可见区域（viewport）。比传统的 `scroll` 事件监听效率高得多——浏览器在后台用优化过的算法判断，不会在每次滚动时都执行 JS。

### 构造函数参数

```javascript
new IntersectionObserver(callback, options)
```

**`callback`：** 当被观察元素的可见状态变化时调用。接收一个 `entries` 数组，每个 entry 代表一个被观察元素。

**`options`：**

| 属性 | 值 | 含义 |
|---|---|---|
| `threshold` | `0.15` | 元素 15% 进入视口时触发回调 |
| `rootMargin` | `'0px 0px -40px 0px'` | 视口检测区域的偏移量 |

`threshold: 0.15`：设置为 0 会在元素刚露出 1px 就触发（太快），设为 0.5 要一半才触发（太慢）。15% 是一个适中的值。

`rootMargin: '0px 0px -40px 0px'`：最后一个值 `-40px` 表示「视口底部向上收缩 40px」。这意味着元素必须"卷到"离底部至少 40px 以上才会触发。这个微调使得元素出现时不会在屏幕最底部——给读者一种「自然浮现」的感觉。

```
正常的视口底部  ─────────────────────
                                   ← -40px 收缩
有效的触发边界  ─────────────────────
                元素到达这条线才触发
```

### 回调函数逐行解析

```javascript
function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}
```

**`entry.target`：** 被观察的 DOM 元素。

**`entry.isIntersecting`：** 布尔值，元素是否与视口相交（是否进入了阈值范围）。

**`observer.unobserve(entry.target)`：** 元素出现后立即停止观察。因为淡入动画只需要触发一次——元素一出现就永远显示了，继续观察只是在浪费内存。

### 观察器的生命周期

```
页面加载
    ↓
querySelectorAll('.fade-in, .timeline-item')   → 找出所有待动画元素
    ↓
observer.observe(el) × N                       → 为每个元素设置"哨兵"
    ↓
用户向下滚动
    ↓
某元素 15% 进入视口 → 回调触发
    ↓
el.classList.add('visible')                    → CSS 过渡动画启动
observer.unobserve(el)                         → 哨兵撤离
    ↓
CSS transition 完成                            → 元素完全显现
```

### CSS 端的配合

```css
.fade-in {
  opacity: 0;                              /* 初始透明 */
  transform: translateY(24px);             /* 初始向下偏移 24px */
  transition: opacity 0.6s ease, transform 0.6s ease;  /* 过渡动画 */
}

.fade-in.visible {
  opacity: 1;                              /* 最终不透明 */
  transform: translateY(0);                /* 最终归位 */
}
```

JS 负责「何时加 `.visible`」，CSS 负责「加了之后怎么过渡」。

---

## 第十二部分：完整的页面加载时序

```
① 浏览器收到 HTML
        ↓
② 开始解析 HTML（从上到下）
        ↓
③ 遇到 <script src="js/i18n-data.js">
   暂停解析 → 下载并执行 → 定义全局变量 I18N（翻译字典）
        ↓
④ 遇到 <script src="js/i18n-engine.js">
   暂停解析 → 下载并执行 → 定义 getText() / setLang() / updatePageText()
        ↓
⑤ 遇到 <script src="js/shared.js">
   暂停解析 → 下载并执行 →
     a. 动态注入 Vercel Analytics 脚本
     b. 注入导航栏 HTML（到 <body> 顶部）
     c. 注入页脚 HTML（到 <body> 底部）
     d. 高亮当前页面对应的导航链接
     e. 从 localStorage 恢复暗色模式设置
     f. 绑定暗色模式按钮的点击事件
     g. 从 localStorage 恢复语言设置
     h. 绑定语言切换按钮的点击事件
     i. 调用 updatePageText() — 所有 data-i18n 替换为对应语言的文字
     j. 绑定移动端汉堡菜单的点击事件
     k. 为所有 .fade-in / .timeline-item 设置 IntersectionObserver
        ↓
⑥ 继续解析完剩余的 HTML
        ↓
⑦ CSS 加载完毕，首次渲染（用户看到页面）
        ↓
⑧ 用户滚动 → IntersectionObserver 触发 → 元素逐个淡入
```

**关键洞察：** 步骤 ③~⑤ 是**同步阻塞**的——浏览器必须暂停 HTML 解析来下载和执行脚本。这就是为什么脚本放在 `<body>` 底部的原因：等页面主要内容解析完再执行脚本，用户能更快看到内容。

---

## 总结：七个值得记住的编程模式

| # | 模式 | 代码 | 为什么用它 |
|---|------|------|-----------|
| 1 | **IIFE** | `(function(){...})()` | 避免全局变量污染，创建独立作用域 |
| 2 | **严格模式** | `'use strict'` | 让隐式错误变为显式报错 |
| 3 | **短路求值默认值** | `a || 'default'` | 简洁地提供备选值 |
| 4 | **classList.toggle** | `el.classList.toggle('open')` | 无脑切换状态，不需要 if 判断 |
| 5 | **data 属性解耦** | `data-*` + `getAttribute` | JS 逻辑和 HTML 结构松耦合 |
| 6 | **CSS 变量做主题** | `var(--bg)` + `[data-theme]` | 改一个属性，全站颜色跟随 |
| 7 | **Observer 代替 scroll** | `IntersectionObserver` | 高性能滚动检测，浏览器原生优化 |

---

> 本教程涵盖了 `shared.js` 和 `i18n-engine.js` 中的全部 JS 代码。建议对照实际文件逐行阅读，遇到不理解的 API 可以在 MDN（developer.mozilla.org）上查阅详细文档。
