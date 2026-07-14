# 教程六：JavaScript 代码逐行解析

## 回顾

前五篇教程覆盖了 HTML、CSS、i18n 和部署。本篇以**逐行注释**的方式，解释三个 JS 文件中每一行代码的具体作用。

---

## JS 文件加载顺序

```
js/i18n-data.js    →  先加载：定义翻译数据
js/i18n-engine.js  →  第二：定义翻译函数（依赖 I18N 变量）
js/shared.js       →  第三：执行所有页面行为（依赖上面两个文件）
```

---

# 文件一：`js/i18n-data.js`

这个文件定义了一个全局变量 `I18N`，包含中文（`zh`）和英文（`en`）两套翻译字典。

## 第 1 行

```javascript
// AUTO-GENERATED from dammy-data/*.txt — DO NOT EDIT DIRECTLY
```

单行注释。告诉开发者这个文件是工具自动生成的，手动编辑会被覆盖。`//` 后面的所有文字都是注释，不影响程序运行。

## 第 2 行

```javascript
// To change content, edit the .txt files in dammy-data/ then run: node scripts/build.js
```

单行注释。指导开发者正确的修改流程：编辑原始数据文件 → 运行构建脚本。

## 第 3 行

```javascript
const I18N = {
```

声明一个常量 `I18N`，赋值为一个对象（Object）。`const` 表示这个变量不能被重新赋值（但对象内部的属性可以修改）。花括号 `{` 是对象的开始标记，直到第 207 行的 `}` 闭合。

## 第 4 行

```javascript
  zh: {
```

在 `I18N` 对象中创建一个属性 `zh`，值是一个新对象。`zh` 是中文（中文的 ISO 639-1 语言代码）。这个内层对象将包含所有中文翻译文本。

## 第 5~103 行（中文翻译数据，以第一组为例）

```javascript
    'about.hero.subtitle': '你好，我是胡美婧（Damara），一个内在真正有趣的灵魂',
```

- **键（key）**：`'about.hero.subtitle'` — 用点号 `.` 分隔的命名空间格式，表示「关于页面 > 主视觉区 > 副标题」
- **冒号 `:`**：分隔键和值
- **值（value）**：`'你好，我是胡美婧...'` — 中文翻译文本，用单引号包裹
- **逗号 `,`**：分隔对象中的不同属性

每一行格式相同：`'key': '翻译文本',`。点号命名空间便于组织——`about.hero.title`、`about.story.heading` 都属于 "about" 这个逻辑分组。

## 第 104 行

```javascript
  },
```

中文翻译对象的结束花括号，后面的逗号表示 `zh` 属性结束，接下来是下一个属性。

## 第 106 行

```javascript
  en: {
```

创建英文翻译对象，结构完全镜像 `zh`。每个 key 名称完全相同（如 `'about.hero.subtitle'`），但 value 是英文文本。

## 第 207 行

```javascript
};
```

`I18N` 对象的结束花括号，分号表示 `const I18N = {...}` 语句结束。

### 数据访问模式

```javascript
I18N.zh['about.hero.title']    // → '关于我'
I18N.en['about.hero.title']    // → 'About Me'
I18N['zh']['about.hero.title'] // → '关于我'（方括号等价写法）
```

---

# 文件二：`js/i18n-engine.js`

这个文件定义了三个全局函数：`getText()`、`setLang()`、`updatePageText()`。它们是全站中英文切换的核心。

## 第 1 行

```javascript
// i18n engine — language functions. Content data is in js/i18n-data.js
```

单行注释。概述该文件的用途：语言功能函数，翻译数据在另一个文件中。

## 第 3 行

```javascript
function getText(key) {
```

定义一个名为 `getText` 的函数，接收一个参数 `key`。

- `function` — JavaScript 声明函数的关键字
- `getText` — 函数名，动词开头表示它执行一个操作
- `(key)` — 形参列表，调用时传入的翻译键名会赋给 `key`
- `{` — 函数体的开始

## 第 4 行

```javascript
  var lang = document.documentElement.lang || 'zh';
```

- `var lang` — 声明一个局部变量 `lang`（只在函数内部可见）
- `document.documentElement` — 获取页面的 `<html>` 根元素
- `.lang` — 读取 `<html lang="...">` 属性值
- `|| 'zh'` — 如果 `.lang` 为空或未定义，默认使用 `'zh'` 作为后备
- 整行作用：**确定当前应该用哪种语言，默认为中文**

## 第 5 行

```javascript
  return (I18N[lang] && I18N[lang][key]) || key;
```

- `return` — 将右侧表达式的计算结果作为函数返回值
- `I18N[lang]` — 用当前语言（如 `'zh'`）作为 key 访问 `I18N` 对象，得到中文翻译字典
- `&&` — 逻辑「与」：如果左边为真，返回右边；如果左边为假，直接返回左边（短路求值，不会因为访问 `undefined` 的属性而报错）
- `I18N[lang][key]` — 在翻译字典中查找具体的翻译文本
- `|| key` — 如果左边为假（翻译不存在），返回原始的 key 作为兜底
- 整行作用：**从字典中取出翻译文本；找不到翻译时返回原始 key**

### 执行示例

```javascript
// 假设 lang = 'zh'，key = 'nav.home'
getText('nav.home')
  → lang = 'zh'
  → I18N['zh'] 存在 → 是 { 'nav.home': '首页', ... }
  → I18N['zh']['nav.home'] = '首页'
  → '首页' 为真 → return '首页'

// 假设 key = 'does.not.exist'
getText('does.not.exist')
  → I18N['zh']['does.not.exist'] = undefined
  → undefined || 'does.not.exist' → 'does.not.exist'
  → return 'does.not.exist'（至少页面会显示 key 而不是空白）
```

## 第 6 行

```javascript
}
```

函数体的结束花括号。`getText` 函数定义完毕。

## 第 8 行

```javascript
function setLang(lang) {
```

定义函数 `setLang`，接收一个参数 `lang`（传入 `'zh'` 或 `'en'`）。

## 第 9 行

```javascript
  document.documentElement.lang = lang;
```

将 `<html>` 元素的 `lang` 属性设置为传入的值。例如 `setLang('en')` 后，HTML 变成 `<html lang="en">`。这有两个效果：
1. 浏览器和搜索引擎知道页面语言变了
2. `getText()` 读取这个值来判断用哪个字典

## 第 10 行

```javascript
  localStorage.setItem('lang', lang);
```

将语言选择保存到浏览器的 `localStorage` 中。

- `localStorage` — 浏览器提供的持久化存储 API
- `.setItem(key, value)` — 以键值对形式存储数据
- `'lang'` — 存储的键名（自定义）
- `lang` — 存储的值，即传入的语言代码
- 作用：**用户下次打开页面时，能自动恢复之前选择的语言**

## 第 11 行

```javascript
  updatePageText();
```

调用 `updatePageText()` 函数（定义在第 14 行），立即刷新页面上所有元素的文字内容。

## 第 12 行

```javascript
}
```

`setLang` 函数的结束花括号。

## 第 14 行

```javascript
function updatePageText() {
```

定义函数 `updatePageText`，无参数。这是最核心的函数——遍历 DOM 并替换所有标记元素的文字。

## 第 15 行

```javascript
  // Text content
```

注释：以下代码处理「纯文本」更新。

## 第 16 行

```javascript
  var elements = document.querySelectorAll('[data-i18n]');
```

- `document.querySelectorAll()` — 在整个页面中查找匹配 CSS 选择器的所有元素
- `'[data-i18n]'` — CSS 属性选择器，匹配所有带有 `data-i18n` 属性的元素
- `var elements` — 将返回的 NodeList（类似数组的节点集合）存入变量
- 作用：**找到页面上所有需要翻译的文本元素**

例如：
```html
<p data-i18n="nav.home">Home</p>    ← 匹配
<a data-i18n="nav.about">About</a>  ← 匹配
<p class="normal">Hello</p>         ← 不匹配（没有 data-i18n 属性）
```

## 第 17 行

```javascript
  for (var i = 0; i < elements.length; i++) {
```

- `for (...)` — JavaScript 的计数循环语句
- `var i = 0` — 初始化计数器变量，从 0 开始
- `i < elements.length` — 循环条件：`i` 小于元素总数时继续，`elements.length` 是 NodeList 的元素数量
- `i++` — 每轮循环结束后 `i` 自增 1
- 作用：**遍历第 16 行找到的每一个元素**

## 第 18 行

```javascript
    var key = elements[i].getAttribute('data-i18n');
```

- `elements[i]` — 用索引 `i` 取出集合中的第 `i` 个元素（从 0 开始计数）
- `.getAttribute('data-i18n')` — 读取该元素的 `data-i18n` 属性值
- `var key` — 将属性值（翻译键名）存入变量 `key`
- 作用：**从 HTML 元素上提取翻译键名**

例如 `<p data-i18n="nav.home">Home</p>` → `key = 'nav.home'`

## 第 19 行

```javascript
    var text = getText(key);
```

调用 `getText()` 函数（第 3 行定义），传入翻译键名，获取对应的翻译文本。结果存入变量 `text`。

## 第 20 行

```javascript
    if (text) {
```

- `if (...)` — 条件判断语句
- `text` — 检查 `text` 是否为「真值」（不是 `null`、`undefined`、空字符串 `''`）
- 作用：**只有成功获取到翻译文本时才执行替换，避免把内容清空**

## 第 21 行

```javascript
      if (elements[i].tagName === 'INPUT' || elements[i].tagName === 'TEXTAREA') {
```

- `elements[i].tagName` — 当前元素的标签名（始终返回大写，如 `'INPUT'`、`'P'`）
- `=== 'INPUT'` — 严格相等比较，判断是否为 `<input>` 元素
- `||` — 逻辑「或」：只要满足其中一个条件即为真
- `=== 'TEXTAREA'` — 判断是否为 `<textarea>` 元素
- 作用：**判断当前元素是否为表单元素**

## 第 22 行

```javascript
        elements[i].placeholder = text;
```

- `.placeholder` — 表单元素的占位提示文字属性
- 将翻译文本设置为 `placeholder`（而非 `textContent`）
- 作用：**对于 `<input>` / `<textarea>`，翻译文本显示为占位提示**

因为表单元素的值由用户输入，不能覆盖；但可以用 `placeholder` 翻译提示文字。

## 第 23 行

```javascript
      } else {
```

`else` — 与第 21 行的 `if` 配对，处理「不是表单元素」的情况。

## 第 24 行

```javascript
        elements[i].textContent = text;
```

- `.textContent` — 元素内的纯文字内容（不会解析 HTML 标签）
- 将翻译文本设置为元素的文字内容
- 作用：**对于普通元素（`<p>`、`<a>`、`<h1>` 等），直接替换其显示的文本**

对比 `textContent` vs `innerHTML`：
```javascript
element.textContent = '<strong>Hi</strong>';  // 页面显示字面量：<strong>Hi</strong>
element.innerHTML = '<strong>Hi</strong>';    // 页面显示粗体：**Hi**
```
用 `textContent` 更安全，防止意外执行恶意 HTML。

## 第 25~27 行

```javascript
      }
    }
  }
```

三层花括号闭合：
1. 第 25 行：闭合第 21 行的 `if/else`
2. 第 26 行：闭合第 20 行的 `if (text)`
3. 第 27 行：闭合第 17 行的 `for` 循环

## 第 29 行

```javascript
  // HTML content (for rich text with markup)
```

注释：以下处理「富文本」——包含 HTML 标签的翻译内容。

## 第 30 行

```javascript
  var htmlElements = document.querySelectorAll('[data-i18n-html]');
```

- `'[data-i18n-html]'` — 属性选择器，匹配属性名为 `data-i18n-html` 的元素
- 作用：**找到所有需要替换为富文本（含 HTML）的元素**

```html
<div data-i18n-html="projects.research.0.desc">...</div>
```

## 第 31 行

```javascript
  for (var j = 0; j < htmlElements.length; j++) {
```

遍历所有富文本元素，用新计数器 `j`（避免与第 17 行的 `i` 冲突）。

## 第 32 行

```javascript
    var htmlKey = htmlElements[j].getAttribute('data-i18n-html');
```

读取当前元素的 `data-i18n-html` 属性值（翻译键名），存入变量 `htmlKey`。

## 第 33 行

```javascript
    var htmlText = getText(htmlKey);
```

调用 `getText()` 获取翻译文本，存入变量 `htmlText`。

## 第 34 行

```javascript
    if (htmlText) {
```

检查翻译文本是否存在。避免用 `null`/`undefined` 覆盖元素内容。

## 第 35 行

```javascript
      htmlElements[j].innerHTML = htmlText;
```

- `.innerHTML` — 元素的 HTML 内容（会解析并渲染 HTML 标签）
- 作用：**将包含 HTML 标签的翻译文本注入元素，浏览器会渲染这些标签**

例如：
```javascript
// htmlText = '<li><strong>研究过程：</strong>对姜黄素...</li>'
element.innerHTML = htmlText;
// 浏览器将 <li> 渲染为列表项，<strong> 渲染为粗体
```

## 第 36~37 行

```javascript
    }
  }
```

闭合第 34 行的 `if` 和第 31 行的 `for`。

## 第 39 行

```javascript
  // Attribute content (src, href, content)
```

注释：以下处理「属性」翻译——翻译元素的属性值而非文本内容。

## 第 40 行

```javascript
  var attrElements = document.querySelectorAll('[data-i18n-attr]');
```

找到所有带 `data-i18n-attr` 属性的元素。例如：
```html
<img data-i18n-attr="alt:about.hero.title" alt="About Me">
```

## 第 41 行

```javascript
  for (var k = 0; k < attrElements.length; k++) {
```

用计数器 `k` 遍历所有属性翻译元素。

## 第 42 行

```javascript
    var el = attrElements[k];
```

将当前元素存入变量 `el`，方便后续引用，避免反复写 `attrElements[k]`。

## 第 43 行

```javascript
    var spec = el.getAttribute('data-i18n-attr');
```

读取 `data-i18n-attr` 的属性值（翻译规则字符串），存入 `spec`。例如：
```
spec = "alt:about.hero.title, title:about.hero.title"
```

## 第 44 行

```javascript
    var parts = spec.split(',');
```

- `.split(',')` — 以逗号为分隔符，将字符串切割为数组
- `"alt:about.hero.title, title:about.hero.title".split(',')` → `["alt:about.hero.title", " title:about.hero.title"]`
- 作用：**一个元素可能需要翻译多个属性，先用逗号拆开**

## 第 45 行

```javascript
    for (var p = 0; p < parts.length; p++) {
```

遍历 `parts` 数组中的每一段。

## 第 46 行

```javascript
      var kv = parts[p].split(':');
```

- `parts[p]` — 当前段，如 `"alt:about.hero.title"`
- `.split(':')` — 以冒号切分，得到属性名和翻译 key
- `"alt:about.hero.title".split(':')` → `["alt", "about.hero.title"]`
- 存入变量 `kv`（key-value 的缩写）

## 第 47 行

```javascript
      var attrName = kv[0].trim();
```

- `kv[0]` — 数组第一个元素，即属性名（如 `"alt"` 或 `" title"`）
- `.trim()` — 去除字符串首尾的空白字符（空格、tab 等）
- 作用：**获取要设置的属性名（如 `alt`、`title`）**

`" alt".trim()` → `"alt"`

## 第 48 行

```javascript
      var attrKey = kv.slice(1).join(':').trim();
```

- `kv.slice(1)` — 从索引 1 开始截取数组的剩余部分（排除属性名）
- `.join(':')` — 用冒号重新拼接剩余部分（防止翻译 key 自身包含冒号时被误拆）
- `.trim()` — 去除首尾空白
- 作用：**安全地获取翻译键名**

```
输入："alt:about.hero.title"
kv = ["alt", "about.hero.title"]
kv.slice(1) → ["about.hero.title"]
.join(':') → "about.hero.title"
```

## 第 49 行

```javascript
      var val = getText(attrKey);
```

调用 `getText()` 获取翻译后的属性值。

## 第 50 行

```javascript
      if (val) {
```

检查翻译值是否存在。

## 第 51 行

```javascript
        el.setAttribute(attrName, val);
```

- `.setAttribute(name, value)` — 设置元素的指定属性值
- 例如：`el.setAttribute('alt', '关于我')` → `<img alt="关于我">`
- 作用：**将翻译后的文本写入目标属性**

## 第 52~55 行

```javascript
      }
    }
  }
}
```

四层闭合：
1. 第 52 行：闭合第 50 行的 `if (val)`
2. 第 53 行：闭合第 45 行的 `for`（`parts` 循环）
3. 第 54 行：闭合第 41 行的 `for`（`attrElements` 循环）
4. 第 55 行：闭合第 14 行的 `function updatePageText()`

---

# 文件三：`js/shared.js`

这是全站的「总控制器」，负责注入导航栏/页脚、暗色模式、语言切换、滚动动画等所有共享行为。

## 第 1 行

```javascript
(function() {
```

IIFE（立即执行函数表达式）的开头。

- 外层括号 `(` — 将 `function()` 从「函数声明」转为「函数表达式」
- `function()` — 定义一个匿名函数（没有函数名）
- `{` — 函数体的开始
- 作用：**创建一个独立的作用域，使得内部所有 `var` 变量不会泄露为全局变量**

### IIFE 语法拆解

```javascript
// 标准写法
(function() {
  // 代码
})();

// 拆解为两步理解：
// 步骤 1: (function() { ... })  — 把函数包在括号里，变成表达式
// 步骤 2: ()                    — 立即调用这个函数
```

## 第 2 行

```javascript
  'use strict';
```

启用 JavaScript 严格模式。

- 这是一个字符串字面量，放在作用域的最顶部
- 效果：未声明变量直接赋值会报错、函数参数不能重名、`this` 行为更规范
- 作用：**让浏览器以更严格的规则执行代码，尽早暴露潜在 bug**

```javascript
// 非严格模式（危险，但默默运行）
x = 5;  // 自动创建全局变量 x

// 严格模式
'use strict';
x = 5;  // → ReferenceError: x is not defined
```

## 第 4 行

```javascript
  /* === Vercel Web Analytics === */
```

块注释（`/* ... */`）。用于标记代码段落的开始，不执行。比 `//` 更适合做段落标题。

## 第 5 行

```javascript
  var analyticsScript = document.createElement('script');
```

- `document.createElement('script')` — 在内存中创建一个新的 `<script>` DOM 元素（尚未添加到页面）
- `var analyticsScript` — 将新创建的元素引用存入变量
- 作用：**准备一个脚本标签，用于加载 Vercel 统计分析**

## 第 6 行

```javascript
  analyticsScript.defer = true;
```

- `.defer` — 布尔属性，控制脚本的执行时机
- 设为 `true` 等价于 HTML 中写 `<script defer>`
- 效果：脚本异步下载，不阻塞页面解析；等 DOM 完全解析后才执行
- 作用：**统计分析脚本不干扰页面渲染**

`defer` vs `async` vs 无属性：

| 属性 | 下载 | 执行时机 | 执行顺序 |
|------|------|---------|---------|
| 无 | 阻塞解析 | 立即执行 | 按出现顺序 |
| `defer` | 不阻塞 | DOM 解析完后 | 按出现顺序 |
| `async` | 不阻塞 | 下载完立即执行 | 乱序 |

## 第 7 行

```javascript
  analyticsScript.src = 'https://cdn.vercel-insights.com/v1/script.js';
```

- `.src` — 脚本的 URL 来源
- 设置 URL 不会立即下载脚本——必须将元素插入 DOM 后才触发下载
- 作用：**指定要加载的 Vercel 统计分析脚本地址**

## 第 8 行

```javascript
  document.head.appendChild(analyticsScript);
```

- `document.head` — 页面的 `<head>` 元素
- `.appendChild(element)` — 将元素追加为指定父节点的最后一个子节点
- 作用：**将脚本元素插入 `<head>` 中，触发浏览器下载**

执行后等价于 HTML 中多了一行：
```html
<script defer src="https://cdn.vercel-insights.com/v1/script.js"></script>
```

## 第 10 行

```javascript
  /* === Nav HTML template === */
```

块注释：接下来的代码是导航栏的 HTML 模板。

## 第 11 行

```javascript
  var currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'index';
```

这行代码从浏览器地址栏提取当前页面名。逐步拆解：

### 第 1 步：`window.location.pathname`

```
window        → 全局对象，代表浏览器窗口
.location     → 当前页面的 URL 信息
.pathname     → URL 中域名后面的路径部分

https://damarahu.com/about.html#section
                  ↑_________________↑
                  这就是 pathname: '/about.html'
```

### 第 2 步：`.split('/')`

```
'/about.html'.split('/')  →  ['', 'about.html']
'/'         .split('/')  →  ['', '']
```

用斜杠 `/` 切开路径，返回数组。首页的路径是 `/`，切开后只有空字符串。

### 第 3 步：`.pop()`

```
['', 'about.html'].pop()  →  'about.html'
['', '']         .pop()  →  ''
```

移除并返回数组的最后一个元素（栈操作）。

### 第 4 步：`.replace('.html', '')`

```
'about.html'.replace('.html', '')  →  'about'
''         .replace('.html', '')  →  ''
```

将第一个参数的文本替换为第二个参数的值——这里相当于删除 `.html`。

### 第 5 步：`|| 'index'`

```
'about' || 'index'  →  'about'  （非空字符串是真值，直接返回）
''      || 'index'  →  'index'  （空字符串是假值，返回备选值）
```

逻辑「或」作为默认值 —— 首页路径最终变成空字符串，用 `'index'` 代替。

### 完整执行示例

| 网址路径 | split | pop | replace | 最终 |
|---|---|---|---|---|
| `/about.html` | `['', 'about.html']` | `'about.html'` | `'about'` | `'about'` |
| `/` | `['', '']` | `''` | `''` | `'index'` |
| `/education.html` | `['', 'education.html']` | `'education.html'` | `'education'` | `'education'` |

## 第 13 行

```javascript
  var navHTML = '<nav class="navbar">' +
```

- `var navHTML` — 声明变量，用于存储完整的导航栏 HTML 字符串
- `'<nav class="navbar">'` — 导航栏的开头标签
- `+` — 字符串连接运算符，连接多行
- 作用：**开始构建导航栏的 HTML，`+` 将后续行拼接成完整字符串**

## 第 14 行

```javascript
    '<div class="navbar-inner">' +
```

继续拼接字符串：导航栏内部容器 `<div>`，CSS 用它设置最大宽度和居中。

## 第 15 行

```javascript
      '<a href="/" class="nav-logo">Damara Hu</a>' +
```

- `<a href="/">` — 链接到首页（`/` 代表根路径）
- `class="nav-logo"` — CSS 类名，用于网站 Logo 的样式
- `Damara Hu` — 链接的文字内容
- 作用：**生成左上角的品牌 Logo 链接**

## 第 16 行

```javascript
      '<ul class="nav-links" id="navLinks">' +
```

- `<ul>` — 无序列表
- `class="nav-links"` — CSS 类名，控制导航链接的显示样式
- `id="navLinks"` — 唯一标识符，JS 中通过 `getElementById` 获取并控制移动端菜单展开/收起
- 作用：**生成导航链接列表的容器**

## 第 17 行

```javascript
        '<li><a href="/" data-i18n="nav.home" data-page="index">Home</a></li>' +
```

- `<li>` — 列表项
- `<a href="/">` — 指向首页的链接
- `data-i18n="nav.home"` — 标记这个元素需要 i18n 翻译，key 为 `nav.home`
- `data-page="index"` — 标记这个链接对应的页面标识符，用于高亮当前页面
- `Home` — 默认显示文字（英文兜底），会被 `updatePageText()` 替换为翻译文本
- 作用：**生成首页导航链接**

## 第 18~22 行

```javascript
        '<li><a href="/about.html" data-i18n="nav.about" data-page="about">About</a></li>' +
        '<li><a href="/education.html" data-i18n="nav.education" data-page="education">Education</a></li>' +
        '<li><a href="/projects.html" data-i18n="nav.projects" data-page="projects">Projects</a></li>' +
        '<li><a href="/interests.html" data-i18n="nav.interests" data-page="interests">Interests</a></li>' +
        '<li><a href="/contact.html" data-i18n="nav.contact" data-page="contact">Contact</a></li>' +
```

与第 17 行结构相同，生成其余 5 个页面的导航链接。每个链接都有三个关键属性：

| 属性 | 值示例 | 用途 |
|---|---|---|
| `href` | `/about.html` | 点击后跳转的目标页面 |
| `data-i18n` | `nav.about` | i18n 翻译键名，决定显示什么文字 |
| `data-page` | `about` | 页面标识符，与 `currentPage` 比较后决定是否高亮 |

## 第 23 行

```javascript
      '</ul>' +
```

闭合第 16 行开始的 `<ul>` 标签。

## 第 24 行

```javascript
      '<div class="nav-actions">' +
```

导航栏右侧的按钮容器。CSS 用这个类名将按钮组合在一起并对齐到右侧。

## 第 25 行

```javascript
        '<button class="nav-btn" id="langToggle" data-i18n="nav.langToggle" aria-label="Switch language">EN</button>' +
```

- `<button>` — 按钮元素（默认 `type="button"`，不会触发表单提交）
- `class="nav-btn"` — CSS 类名，控制按钮外观
- `id="langToggle"` — 唯一标识符，JS 通过这个 id 绑定点击事件
- `data-i18n="nav.langToggle"` — 翻译 key，按钮文字（EN/中文）支持 i18n
- `aria-label="Switch language"` — 无障碍标签，屏幕阅读器会朗读这个文本而非按钮内容
- `EN` — 默认显示文字
- 作用：**生成语言切换按钮（中 ↔ 英）**

## 第 26 行

```javascript
        '<button class="nav-btn" id="themeToggle" data-i18n="nav.themeToggle" aria-label="Toggle dark mode">🌙</button>' +
```

- `id="themeToggle"` — JS 通过这个 id 绑定暗色模式切换事件
- `🌙` — Unicode 月亮 emoji，默认显示（用户看到的按钮图标）
- 作用：**生成暗色/亮色模式切换按钮**

## 第 27~29 行

```javascript
        '<button class="hamburger" id="hamburger" aria-label="Menu">' +
          '<span></span><span></span><span></span>' +
        '</button>' +
```

- `class="hamburger"` — CSS 控制三道横线的样式
- `id="hamburger"` — JS 绑定移动端菜单展开/收起事件
- `aria-label="Menu"` — 无障碍标签
- 三个 `<span></span>` — 空标签，CSS 将它们渲染为三道水平横线（经典的汉堡菜单图标）
- 作用：**生成移动端汉堡菜单按钮（三道横线）**

## 第 30~32 行

```javascript
      '</div>' +
    '</div>' +
  '</nav>';
```

三层闭合：
1. `</div>` — 闭合 `nav-actions` 容器
2. `</div>` — 闭合 `navbar-inner` 容器
3. `</nav>` — 闭合导航栏，分号 `;` 表示 `var navHTML = ...` 赋值语句结束

## 第 34 行

```javascript
  /* === Footer HTML template === */
```

块注释：接下来的代码是页脚的 HTML 模板。

## 第 35 行

```javascript
  var footerHTML = '<footer class="site-footer">' +
```

- `var footerHTML` — 声明变量，存储完整的页脚 HTML 字符串
- `'<footer class="site-footer">'` — 页脚的 `<footer>` 语义标签
- `class="site-footer"` — CSS 类名，控制背景色、上边框、内边距
- `+` — 拼接后续行

## 第 36 行

```javascript
    '<div class="footer-inner">' +
```

页脚内容容器。CSS 设置 `max-width` + `margin: 0 auto` 实现居中，`text-align: center` 让内容水平居中。

## 第 37 行

```javascript
      '<h4 class="footer-brand">Damara Hu</h4>' +
```

- `<h4>` — 四级标题，语义上表示页脚标题
- `class="footer-brand"` — CSS 类名，控制字号和间距
- `Damara Hu` — 品牌名（不参与 i18n，始终显示原名）
- 作用：**页脚第一行：品牌名**

## 第 38 行

```javascript
      '<p class="footer-tagline" data-i18n="home.hero.tagline">Student · Researcher · Creator</p>' +
```

- `<p>` — 段落标签
- `class="footer-tagline"` — CSS 控制颜色和字号
- `data-i18n="home.hero.tagline"` — 翻译 key，与首页 Hero 区的标语使用同一个 key，保持一致性
- `Student · Researcher · Creator` — 默认英文兜底文字
- 作用：**页脚第二行：个人标语**

## 第 39 行

```javascript
      '<nav class="footer-links">' +
```

- `<nav>` — 导航语义标签（告诉搜索引擎这是一组导航链接）
- `class="footer-links"` — CSS 使用 `display: flex` 将链接横向排列，`justify-content: center` 居中
- 作用：**页脚链接区域的容器**

## 第 40~45 行

```javascript
        '<a href="/" data-i18n="nav.home">Home</a>' +
        '<a href="/about.html" data-i18n="nav.about">About</a>' +
        '<a href="/education.html" data-i18n="nav.education">Education</a>' +
        '<a href="/projects.html" data-i18n="nav.projects">Projects</a>' +
        '<a href="/interests.html" data-i18n="nav.interests">Interests</a>' +
        '<a href="/contact.html" data-i18n="nav.contact">Contact</a>' +
```

6 个页脚导航链接。每个 `<a>` 标签：
- `href` — 目标页面 URL
- `data-i18n` — 翻译 key（与顶部导航栏共用同一个 key，但通过不同的 CSS 类控制外观）
- 默认文字 — 英文兜底

CSS 中定义 `.footer-links a:not(:last-child)::after { content: '\00B7'; }` 在每个链接后面自动添加 `·` 分隔符（最后一个链接除外）。

## 第 46 行

```javascript
      '</nav>' +
```

闭合 `<nav class="footer-links">`。

## 第 47 行

```javascript
      '<p class="footer-copyright" data-i18n="footer.copyright">© 2026 Damara Hu. All rights reserved.</p>' +
```

- `class="footer-copyright"` — CSS 控制字号、颜色、上边框（用 `border-top` 做一条分隔线）
- `data-i18n="footer.copyright"` — 翻译 key
- `©` — HTML 实体，显示版权符号 `©`
- 作用：**页脚最后一行：版权声明**

## 第 48~49 行

```javascript
    '</div>' +
  '</footer>';
```

- `</div>` — 闭合 `footer-inner`
- `</footer>` — 闭合 `site-footer`，分号结束 `var footerHTML = ...` 赋值

## 第 51 行

```javascript
  /* === Inject === */
```

块注释：以下代码将上面构建好的 HTML 注入页面。

## 第 52 行

```javascript
  document.body.insertAdjacentHTML('afterbegin', navHTML);
```

- `document.body` — 页面的 `<body>` 元素
- `.insertAdjacentHTML(position, text)` — 将 HTML 字符串解析为 DOM 并插入到指定位置
- `'afterbegin'` — 插入位置：`<body>` 内部的最开头（紧跟 `<body>` 标签之后）
- `navHTML` — 要注入的导航栏 HTML 字符串
- 作用：**将导航栏插入到页面内容的最顶部**

```
<body>
  ← 'afterbegin' 插入位置：<nav> 出现在这里
  <main>...</main>  ← 原有页面内容
</body>
```

## 第 53 行

```javascript
  document.body.insertAdjacentHTML('beforeend', footerHTML);
```

- `'beforeend'` — 插入位置：`<body>` 内部的最末尾（`</body>` 标签之前）
- `footerHTML` — 要注入的页脚 HTML 字符串
- 作用：**将页脚插入到页面内容的最底部**

```
<body>
  <nav>...</nav>     ← 导航栏（afterbegin 插入的）
  <main>...</main>   ← 页面内容
  ← 'beforeend' 插入位置：<footer> 出现在这里，所有内容之后
</body>
```

## 第 55 行

```javascript
  /* === Active nav link === */
```

块注释：以下代码高亮当前页面的导航链接。

## 第 56 行

```javascript
  var navLinks = document.querySelectorAll('.nav-links a[data-page]');
```

- `document.querySelectorAll()` — 用 CSS 选择器查找所有匹配元素
- `'.nav-links a[data-page]'` — 选择器：
  - `.nav-links` — class 为 `nav-links` 的元素
  - （空格）— 在该元素内部查找
  - `a` — 所有 `<a>` 标签
  - `[data-page]` — 且必须有 `data-page` 属性
- 返回值：一个 NodeList（类数组的节点集合）
- 作用：**获取所有带有 data-page 属性的导航链接**

## 第 57 行

```javascript
  for (var i = 0; i < navLinks.length; i++) {
```

- `var i = 0` — 初始化计数器，从 0 开始
- `i < navLinks.length` — 循环条件：`i` 小于链接总数时继续
- `i++` — 每轮结束后 `i` 自增 1
- 作用：**遍历每一个导航链接**

## 第 58 行

```javascript
    if (navLinks[i].getAttribute('data-page') === currentPage) {
```

- `navLinks[i]` — 当前遍历到的链接元素
- `.getAttribute('data-page')` — 读取 `data-page` 属性值（如 `'about'`、`'index'`）
- `===` — 严格相等比较（值和类型都必须相同）
- `currentPage` — 第 11 行计算出的当前页面标识符
- 作用：**判断当前链接是否对应正在浏览的页面**

## 第 59 行

```javascript
      navLinks[i].classList.add('active');
```

- `.classList` — 元素的类名操作接口
- `.add('active')` — 向元素添加 `active` 类名
- 作用：**给当前页面的导航链接加上高亮样式**

CSS 中匹配的规则：
```css
.nav-links a.active {
  color: var(--primary);    /* 主色调 */
  font-weight: 600;         /* 加粗 */
}
```

## 第 60~61 行

```javascript
    }
  }
```

- 第 60 行：闭合 `if` 判断
- 第 61 行：闭合 `for` 循环

## 第 63 行

```javascript
  /* === Dark Mode === */
```

块注释：以下代码处理暗色模式。

## 第 64 行

```javascript
  var themeToggle = document.getElementById('themeToggle');
```

- `document.getElementById('themeToggle')` — 通过 id 获取暗色模式切换按钮
- 如果找到元素，返回 DOM 元素；如果找不到，返回 `null`
- 作用：**获取暗色模式按钮，为后续绑定事件做准备**

## 第 65~71 行

```javascript
  function applyTheme(dark) {
    if (dark) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }
```

这段代码定义了一个名为 `applyTheme` 的函数：

**第 65 行：** `function applyTheme(dark) {`
- 声明函数，接收一个布尔参数 `dark`
- `dark === true` → 设置暗色；`dark === false` → 设置为亮色

**第 66 行：** `if (dark) {`
- 判断 `dark` 是否为真值
- 真值：`true`、非零数字、非空字符串等
- 这里只传入 `true` 或 `false`，所以直接判断布尔值

**第 67 行：** `document.documentElement.setAttribute('data-theme', 'dark');`
- `document.documentElement` — `<html>` 根元素
- `.setAttribute('data-theme', 'dark')` — 设置属性 `data-theme="dark"`
- 效果：`<html data-theme="dark">`
- CSS 通过 `[data-theme="dark"]` 选择器覆盖 CSS 变量值

**第 68 行：** `} else {`
- 如果 `dark` 为假值（`false`）

**第 69 行：** `document.documentElement.removeAttribute('data-theme');`
- `.removeAttribute('data-theme')` — 移除 `data-theme` 属性
- 效果：`<html>`（无 `data-theme`，恢复亮色模式）

**第 70~71 行：** `}` `}`
- 闭合 `else` 和函数体

### 暗色模式的 CSS 配合

```css
/* 亮色模式（默认） */
:root {
  --bg: #FFFFFF;       /* 白底 */
  --text: #1A1A2E;     /* 深色文字 */
}

/* 暗色模式 */
[data-theme="dark"] {
  --bg: #1A1A2E;       /* 深色底 */
  --text: #E8E8F0;     /* 浅色文字 */
}
```

所有元素引用 `var(--bg)`、`var(--text)` 等变量，切换 `<html>` 上的属性后全站颜色自动跟随——不需要遍历元素逐个改颜色。

## 第 72 行

```javascript
  var savedTheme = localStorage.getItem('theme');
```

- `localStorage.getItem('theme')` — 从 localStorage 读取 key 为 `'theme'` 的值
- 如果用户之前选择过暗色模式，返回 `'dark'`
- 如果用户从未选过（或选了亮色后保存为 `'light'`），返回对应的值
- 首次访问时该 key 不存在，返回 `null`
- 作用：**读取用户之前保存的主题偏好**

## 第 73 行

```javascript
  if (savedTheme === 'dark') {
```

- `=== 'dark'` — 严格比较：存储的值是否等于字符串 `'dark'`
- 如果是首次访问（`null`），`null === 'dark'` 为 `false`，不进入 `if` 块，保持默认亮色
- 作用：**仅当用户之前明确选择了暗色模式时，恢复暗色**

## 第 74 行

```javascript
    applyTheme(true);
```

- 调用 `applyTheme`，传入 `true`
- 效果：在 `<html>` 上设置 `data-theme="dark"`
- 这行代码在页面加载时执行，所以用户看到的第一个画面就已经是暗色（如果之前选择了暗色）

## 第 75 行

```javascript
  }
```

闭合第 73 行的 `if`。

## 第 76 行

```javascript
  themeToggle.addEventListener('click', function() {
```

- `themeToggle` — 第 64 行获取的按钮元素
- `.addEventListener(event, callback)` — 绑定事件监听器
- `'click'` — 监听鼠标点击事件（也支持触屏的 tap）
- `function() {` — 匿名回调函数，点击时执行
- 作用：**当用户点击切换按钮时，执行花括号内的逻辑**

## 第 77 行

```javascript
    var isDark = document.documentElement.hasAttribute('data-theme');
```

- `document.documentElement.hasAttribute('data-theme')` — 检查 `<html>` 上是否有 `data-theme` 属性
- 返回布尔值：有属性 → `true`（当前是暗色）；无属性 → `false`（当前是亮色）
- 作用：**判断切换前是什么模式**

## 第 78 行

```javascript
    applyTheme(!isDark);
```

- `!isDark` — 逻辑「非」取反
- 如果当前暗色（`isDark = true`）→ `!true = false` → `applyTheme(false)` → 变为亮色
- 如果当前亮色（`isDark = false`）→ `!false = true` → `applyTheme(true)` → 变为暗色
- 作用：**切换到与当前相反的主题**

## 第 79 行

```javascript
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
```

- `localStorage.setItem('theme', ...)` — 保存主题选择到 localStorage
- `isDark ? 'light' : 'dark'` — 三元运算符：当前是暗色 → 存 `'light'`（切换后的状态）；当前是亮色 → 存 `'dark'`
- 作用：**保存切换后的主题状态，下次访问时自动恢复**

## 第 80 行

```javascript
  });
```

- `)` — 闭合 `addEventListener` 的右括号
- `;` — 语句结束
- `}` — 闭合匿名回调函数

## 第 82 行

```javascript
  /* === Language === */
```

块注释：以下代码处理中英文切换。

## 第 83 行

```javascript
  var savedLang = localStorage.getItem('lang') || 'zh';
```

- `localStorage.getItem('lang')` — 从 localStorage 读取语言设置
- `|| 'zh'` — 如果返回 `null`（首次访问），使用默认值 `'zh'`
- 作用：**读取用户之前的语言选择，首次访问默认中文**

## 第 84 行

```javascript
  document.documentElement.lang = savedLang;
```

- 设置 `<html lang="zh">` 或 `<html lang="en">`
- `i18n-engine.js` 中的 `getText()` 通过读取这个值来判断用哪个字典
- 作用：**将恢复/默认的语言应用到页面**

## 第 86 行

```javascript
  document.getElementById('langToggle').addEventListener('click', function() {
```

- `document.getElementById('langToggle')` — 获取语言切换按钮
- `.addEventListener('click', ...)` — 绑定点击事件
- 作用：**当用户点击语言按钮时，执行花括号内的切换逻辑**

## 第 87 行

```javascript
    var newLang = document.documentElement.lang === 'zh' ? 'en' : 'zh';
```

- `document.documentElement.lang === 'zh'` — 判断当前语言
- `? 'en' : 'zh'` — 如果当前是中文，新语言是英文；否则新语言是中文
- 作用：**计算切换后的语言（只有 zh↔en 两种，所以直接翻转）**

## 第 88 行

```javascript
    setLang(newLang);
```

- 调用 `i18n-engine.js` 中定义的 `setLang()` 函数
- `setLang` 会做三件事：更新 `<html lang="">` → 保存到 localStorage → 刷新页面所有文字
- 作用：**执行语言切换**

## 第 89 行

```javascript
    localStorage.setItem('lang', newLang);
```

实际上 `setLang()` 内部已经执行了 `localStorage.setItem('lang', lang)`（第 10 行），所以这行是多余的冗余操作。双重保险确保语言设置一定被保存。

## 第 90 行

```javascript
  });
```

闭合回调函数。

## 第 92 行

```javascript
  /* Update text after nav/footer injection */
```

注释：在注入导航栏和页脚之后，刷新所有 `data-i18n` 元素的文字。

## 第 93 行

```javascript
  updatePageText();
```

- 调用 `i18n-engine.js` 中的 `updatePageText()` 函数
- 此时导航栏和页脚已经注入 DOM（第 52~53 行），`<html lang>` 也已设置（第 84 行）
- 函数遍历所有 `[data-i18n]`、`[data-i18n-html]`、`[data-i18n-attr]` 元素并替换为翻译文本
- 作用：**首次加载时，将所有占位英文替换为当前语言的文字**

### 调用时机

```
① 注入 navHTML → DOM 中多了 6 个带 data-i18n 的链接
② 注入 footerHTML → DOM 中多了带 data-i18n 的页脚元素
③ 设置 <html lang="zh/en">
④ updatePageText() → 上面所有新元素的文字被翻译
```

如果没有这一步，导航栏和页脚会一直显示英文默认文字（Home、About...），不管用户选了什么语言。

## 第 95 行

```javascript
  /* === Mobile Menu === */
```

块注释：以下代码处理移动端汉堡菜单。

## 第 96 行

```javascript
  var hamburger = document.getElementById('hamburger');
```

- 获取汉堡菜单按钮元素（id 为 `hamburger`）
- 存入变量 `hamburger`

## 第 97 行

```javascript
  var navLinksContainer = document.getElementById('navLinks');
```

- 获取导航链接列表容器（id 为 `navLinks`，即 `<ul class="nav-links">`）
- 存入变量 `navLinksContainer`

## 第 98 行

```javascript
  hamburger.addEventListener('click', function() {
```

绑定点击事件到汉堡按钮。

## 第 99 行

```javascript
    navLinksContainer.classList.toggle('open');
```

- `.classList.toggle('open')` — 如果元素没有 `open` 类 → 添加；如果有 → 移除
- 作用：**点击汉堡按钮 → 菜单展开；再次点击 → 菜单收起**

CSS 配合：
```css
/* 移动端（≤768px） */
.nav-links {
  display: none;        /* 默认隐藏 */
}
.nav-links.open {
  display: flex;        /* 加上 open 类后展开 */
}
```

## 第 100~101 行

```javascript
  });
```

闭合回调函数。

## 第 103 行

```javascript
  /* === Scroll Animations === */
```

块注释：以下代码处理页面滚动时的淡入动画。

## 第 104 行

```javascript
  var observerOptions = { threshold: 0.15, rootMargin: '0px 0px -40px 0px' };
```

定义一个配置对象，传给 `IntersectionObserver` 构造函数：

- `threshold: 0.15` — 当目标元素 **15%** 进入视口（可见区域）时触发回调
  - `0` = 刚露出 1px 就触发（太突然）
  - `1` = 元素 100% 可见才触发（太慢，大元素可能永远进不来）
  - `0.15` = 适中的触发点

- `rootMargin: '0px 0px -40px 0px'` — 视口检测区域的外边距调整
  - 四个值分别对应：上、右、下、左（与 CSS margin/padding 的顺序相同）
  - `-40px` 在底部 → 视口底部向内收缩 40px
  - 效果：元素必须「卷到」离底部至少 40px 以上才触发，避免在最底部才出现（读者看到时元素已经在屏幕中间偏下，更自然）

## 第 105 行

```javascript
  var observer = new IntersectionObserver(function(entries) {
```

- `new IntersectionObserver(callback, options)` — 创建 IntersectionObserver 实例
- `function(entries)` — 回调函数，当被观察元素的可见性变化时触发
- `entries` — 一个数组，包含所有状态发生变化的被观察元素
- `observer` — 将实例存入变量，后面用来调用 `.observe()` 和 `.unobserve()`

IntersectionObserver 是浏览器原生 API，比传统的 `scroll` 事件监听效率高得多。它在后台线程中检测元素可见性，只在需要时才触发 JS 回调。

## 第 106 行

```javascript
    entries.forEach(function(entry) {
```

- `entries.forEach(fn)` — 遍历数组中每一个 entry
- `entry` — 单个观察条目，包含以下关键属性：
  - `entry.target` — 被观察的 DOM 元素
  - `entry.isIntersecting` — 布尔值，元素是否进入了检测区域
  - `entry.intersectionRatio` — 0~1，元素可见比例

## 第 107 行

```javascript
      if (entry.isIntersecting) {
```

- `entry.isIntersecting` — 元素是否与视口（或 rootMargin 调整后的区域）有交集
- 当元素滚入检测区域时，该值变为 `true`
- 作用：**判断元素是否进入了「应该显示」的范围**

## 第 108 行

```javascript
        entry.target.classList.add('visible');
```

- `entry.target` — 被观察的 DOM 元素（如某个 `.fade-in` 卡片）
- `.classList.add('visible')` — 添加 `visible` CSS 类
- 作用：**触发 CSS 过渡动画，元素从透明+偏移状态过渡到完全显示**

CSS 配合：
```css
.fade-in {
  opacity: 0;                            /* 初始：透明 */
  transform: translateY(24px);           /* 初始：向下偏移 24px */
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.fade-in.visible {
  opacity: 1;                            /* 最终：不透明 */
  transform: translateY(0);              /* 最终：回到原位 */
}
```

当 JS 添加 `.visible` 后，`opacity` 和 `transform` 会在 0.6 秒内平滑过渡。

## 第 109 行

```javascript
        observer.unobserve(entry.target);
```

- `.unobserve(element)` — 停止观察指定元素
- 元素出现后立即停止观察，因为淡入动画只需要触发一次
- 作用：**释放资源，防止内存泄漏**

如果不 `.unobserve()`，已显示的元素会一直被观察，滚动时持续触发判断——虽然实际不会有新变化（`.visible` 已经加上了），但消耗了不必要的计算和内存。

## 第 110~112 行

```javascript
      }
    });
  }, observerOptions);
```

- 第 110 行：闭合 `if (entry.isIntersecting)`
- 第 111 行：闭合 `entries.forEach()` 回调
- 第 112 行：
  - `}` — 闭合 `function(entries)` 回调
  - `, observerOptions` — 第二个参数，传入第 104 行的配置对象
  - `)` — 闭合 `new IntersectionObserver(...)` 构造函数
  - `;` — 语句结束

## 第 114 行

```javascript
  var animTargets = document.querySelectorAll('.fade-in, .timeline-item');
```

- CSS 选择器 `.fade-in, .timeline-item` — 匹配两类元素：
  - `.fade-in` — 所有带此类的元素（卡片、段落等）
  - `.timeline-item` — 教育页面的时间线条目
- 作用：**找出页面上所有需要滚动淡入动画的元素**

## 第 115~117 行

```javascript
  for (var i = 0; i < animTargets.length; i++) {
    observer.observe(animTargets[i]);
  }
```

- `for` 循环遍历每个动画目标元素
- `observer.observe(element)` — 让 Observer 开始监控该元素的可见性
- 作用：**为每个淡入元素设置「哨兵」——一旦它滚入可视区域，回调就触发**

## 第 119 行

```javascript
  /* Re-observe after dynamic content changes */
```

注释：以下代码提供一个公开方法，用于在动态添加内容后重新观察新元素。

## 第 120~125 行

```javascript
  window.reobserveAnimations = function() {
    var targets = document.querySelectorAll('.fade-in:not(.visible), .timeline-item:not(.visible)');
    for (var i = 0; i < targets.length; i++) {
      observer.observe(targets[i]);
    }
  };
```

**第 120 行：** `window.reobserveAnimations = function() {`
- `window.xxx = ...` — 在全局 `window` 对象上挂载一个方法，使其在 IIFE 外部可调用
- 因为 `observer` 变量在 IIFE 内部，外部代码无法直接访问
- 作用：**暴露一个全局函数，让其他页面脚本能触发重新观察**

**第 121 行：** `var targets = document.querySelectorAll('.fade-in:not(.visible), .timeline-item:not(.visible)');`
- `:not(.visible)` — CSS 伪类，排除已经带有 `.visible` 类的元素
- 只选择「尚未出现」的元素——已经显示过的元素不需要再观察
- 作用：**找出所有新添加的、还没有淡入的元素**

**第 122~124 行：**
- 遍历并 `observer.observe()` 每个新元素
- 作用：**为新内容设置哨兵**

**第 125 行：** `};`

使用示例（在 `interests.html` 中动态加载图片后）：
```javascript
// 动态插入新图片
gallery.innerHTML += '<img class="fade-in" src="...">';
// 让新图片也能淡入
window.reobserveAnimations();
```

## 第 126 行

```javascript
})();
```

- `)` — 闭合 IIFE 的匿名函数
- `()` — 立即调用该函数
- `;` — 语句结束

---

## 完整加载时序

```
浏览器请求 index.html
    ↓
解析 HTML（从上到下）
    ↓
遇到 <script src="js/i18n-data.js">     → 暂停解析 → 下载执行 → 全局变量 I18N 可用
    ↓
遇到 <script src="js/i18n-engine.js">   → 暂停解析 → 下载执行 → getText/setLang/updatePageText 可调用
    ↓
遇到 <script src="js/shared.js">        → 暂停解析 → 下载执行 →
    ├── 第 5~8 行：注入 Vercel Analytics 脚本到 <head>
    ├── 第 11 行：计算当前页面标识符 currentPage
    ├── 第 13~32 行：构建导航栏 HTML 字符串 navHTML
    ├── 第 35~49 行：构建页脚 HTML 字符串 footerHTML
    ├── 第 52 行：导航栏插入 <body> 顶部
    ├── 第 53 行：页脚插入 <body> 底部
    ├── 第 56~61 行：高亮当前页面对应的导航链接
    ├── 第 64~80 行：从 localStorage 恢复暗色模式 → 绑定切换按钮
    ├── 第 83~90 行：从 localStorage 恢复语言 → 绑定切换按钮
    ├── 第 93 行：调用 updatePageText() → 所有 data-i18n 替换为翻译文字
    ├── 第 96~101 行：绑定汉堡菜单点击事件
    └── 第 104~125 行：为所有 .fade-in 元素设置 IntersectionObserver
    ↓
HTML 解析完成 → CSS 渲染 → 用户看到完整页面
    ↓
用户向下滚动 → Observer 触发 → 元素逐个淡入
```

---

## 概念速查表

| 代码 | 类别 | 作用 |
|---|---|---|
| `(function(){...})()` | 设计模式 | 创建隔离作用域，避免全局变量污染 |
| `'use strict'` | 指令 | 启用严格模式，捕获隐性错误 |
| `document.createElement()` | DOM API | 在内存中创建新元素 |
| `document.head.appendChild()` | DOM API | 将元素添加到 `<head>` |
| `window.location.pathname` | BOM API | 获取 URL 路径部分 |
| `.split().pop().replace()` | 字符串 | 链式处理提取当前页面名 |
| `\|\|` | 运算符 | 提供默认值（短路求值） |
| `document.body.insertAdjacentHTML()` | DOM API | 将 HTML 字符串解析并插入页面 |
| `querySelectorAll()` | DOM API | 用 CSS 选择器查找多个元素 |
| `getAttribute()` | DOM API | 读取元素的属性值 |
| `classList.add()` | DOM API | 给元素添加 CSS 类 |
| `classList.toggle()` | DOM API | 切换 CSS 类（有则删，无则加） |
| `document.documentElement` | DOM API | 获取 `<html>` 根元素 |
| `localStorage.getItem()` | Web Storage | 读取持久化数据 |
| `localStorage.setItem()` | Web Storage | 保存持久化数据 |
| `addEventListener('click')` | DOM Event | 绑定点击事件处理器 |
| `IntersectionObserver` | 浏览器 API | 高性能检测元素可见性 |
| `observer.observe()` | Observer API | 开始监控元素可见性 |
| `observer.unobserve()` | Observer API | 停止监控元素（释放资源） |
| `textContent` | DOM 属性 | 设置元素纯文字内容 |
| `innerHTML` | DOM 属性 | 设置元素 HTML 内容（会解析标签） |
| `setAttribute()` | DOM API | 设置元素的属性值 |
| `window.xxx = fn` | 设计模式 | 在 IIFE 内部暴露方法到全局 |

---

> 本教程逐行解释了 `js/` 目录下三个文件的全部 JavaScript 代码。建议打开实际文件对照阅读，遇到不理解的 API 可在 [MDN Web Docs](https://developer.mozilla.org) 上搜索查阅详细文档和交互示例。
