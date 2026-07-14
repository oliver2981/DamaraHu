# 教程二：HTML 页面详解 —— 每个页面是怎么搭起来的

## 回顾

上一篇我们说了 HTML 就是房子的**结构**——决定「页面上有什么」。这篇我们把 6 个页面一个一个拆开来看。

---

## 所有页面的共同结构

打开任何一个 HTML 页面，你都会看到这样的大框架：

```html
<!DOCTYPE html>                           ← ① 文档声明：「我是 HTML5 网页」
<html lang="zh">                          ← ② 网页根元素：lang="zh" 表示默认中文
<head>                                    ← ③ 头部：给浏览器和搜索引擎看的
  <meta charset="UTF-8">                  ←     字符编码：支持中文
  <meta name="viewport" content="...">    ←     手机适配：让手机也能正常缩放
  <meta name="description" content="..."> ←     简介：搜索引擎展示用
  <title>...</title>                      ←     标签页标题
  <link rel="stylesheet" href="css/style.css"> ←  引入样式表
  <link rel="icon" href="...">            ←     网站小图标（favicon）
</head>
<body>                                    ← ④ 身体：真正显示在屏幕上的
  <main>...</main>                        ←     主要内容区
  <script src="js/i18n-data.js"></script> ← ⑤ 脚本：翻译数据
  <script src="js/i18n-engine.js"></script>←    翻译引擎
  <script src="js/shared.js"></script>    ←     导航栏+页脚+暗色模式
</body>
</html>
```

### 逐行解释

**① `<!DOCTYPE html>`**

这不是一个 HTML 标签。它是给浏览器的信号：「按最新标准来渲染我，别用老规矩」。没有它，旧版 IE 会进入「怪异模式」，页面可能变形。

**② `<html lang="zh">`**

`lang="zh"` 告诉浏览器和搜索引擎「这个页面主要是中文」，影响：
- 屏幕阅读器（盲人用的读屏软件）会用中文发音
- 搜索引擎会按中文页面索引
- 浏览器内置翻译功能会正确识别

**③ `<head>` 里的内容**

head 里的东西**一个都不会显示在页面上**，都是元信息：

```html
<meta charset="UTF-8">
```
没有这一行，中文会变乱码。`UTF-8` 是一种「万国码」，能表示全世界所有文字。

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
手机浏览器的关键配置。没有它，在手机上打开网站会缩小成一个「桌面缩略图」，字小得要放大才能看。有了它，浏览器会用适合手机屏幕的宽度来显示。

```html
<meta name="description" content="Damara Hu — Personal academic-style website...">
```
百度、Google 在搜索结果里展示的「简介文字」就来自这里。写得好能提高点击率。

```html
<link rel="stylesheet" href="css/style.css">
```
`rel="stylesheet"` 表示「引入的是一个样式表」，`href` 指定文件路径。

**④ `<body>` 里的内容**

body 是**页面真正可见的部分**。我们下文详细展开。

**⑤ 脚本加载顺序（重要！）**

```html
<script src="js/i18n-data.js"></script>    ← 一定要第一个：定义翻译字典
<script src="js/i18n-engine.js"></script>  ← 一定要第二个：定义翻译函数
<script src="js/shared.js"></script>       ← 一定要第三个：依赖前两个
```

浏览器从上到下执行脚本。如果把 `shared.js` 放到第一个，它调用 `setLang()` 时会报错——因为 `setLang` 还没被定义。

---

## 逐页拆解

### 1. 首页 `index.html`

**作用：** 访客看到的第一眼，引导他们进入子页面。

**结构：**

```
<main>
  ├── <section class="hero">        ← 大标题区：「你好，我是 Damara Hu」
  │     ├── <h1> 你好，我是 Damara Hu </h1>
  │     ├── <p> 终身学习者 · 创新者 </p>
  │     └── <a> 了解更多 </a> <a> 联系我 </a>   ← 两个按钮
  │
  └── <section class="section">     ← 4 张导航卡片
        ├── <a class="nav-card"> 关于我 </a>
        ├── <a class="nav-card"> 教育成长 </a>
        ├── <a class="nav-card"> 项目与研究 </a>
        └── <a class="nav-card"> 兴趣与生活 </a>
```

**关键代码讲解：**

```html
<span data-i18n="home.hero.greeting">你好，我是</span>
```

- `<span>` 是「行内容器」——不给文字换行，和 `<div>` 的区别就是 `<div>` 会换行
- `data-i18n="home.hero.greeting"` 是自定义属性。`data-` 开头的属性是 HTML5 允许我们自己定义的，浏览器不会理解它，但我们的 JS 代码会找到它并使用它

```html
<a href="about.html" class="btn btn-primary" data-i18n="home.hero.cta1">了解更多</a>
```

- `<a>` 是超链接标签
- `href="about.html"` 是点击后跳转的目标
- `class="btn btn-primary"` 是 CSS 类名——`btn` 定义按钮的基本样式，`btn-primary` 定义蓝色实心按钮的特定样式
- 多个 class 用空格隔开，一个标签可以有无数个 class

**为什么卡片用 `<a>` 而不是 `<div>`？**

因为卡片本身就是链接——点击后要跳转到对应页面。`<a>` 标签天然就是可点击的，整个卡片区域都能点击。如果用 `<div>`，还需要额外写 JS 来处理点击。

---

### 2. 关于我 `about.html`

**作用：** 头像、标签、个人故事、核心价值观。

**结构：**

```
<main>
  ├── <section class="page-hero">    ← 页面标题区
  ├── <section class="section">      ← 头像 + 三个标签
  │     ├── <img> 头像图片
  │     └── <span class="tag"> 创新者/学习者/探索者
  ├── <section class="section-alt">  ← 我的故事（灰色背景）
  └── <section class="section">      ← 核心价值观 4 张卡片
```

**关键代码：**

```html
<img src="assets/images/avatar.jpg" alt="Damara Hu"
     style="width:100%;height:100%;object-fit:cover;">
```

- `src`：图片文件路径
- `alt`：图片加载失败时显示的文字（也对盲人读屏器友好）
- `style="..."`：内联样式——只对这一个标签生效的 CSS。`object-fit: cover` 意思是「图片等比缩放，填满容器，超出部分裁剪掉」——这是让头像圆形容器不变形的关键

---

### 3. 教育成长 `education.html`

**作用：** 时间线展示教育经历 + 技能标签云。

**结构：**

```
<main>
  ├── <section class="page-hero">    ← 页面标题
  ├── <section class="section">      ← 时间线（3 个条目）
  └── <section class="section-alt">  ← 核心能力标签云
```

**时间线是怎么实现的？**

时间线在 HTML 里是三个 `<div class="timeline-item">` 排列：

```html
<div class="timeline">
  <div class="timeline-item">        ← 第 1 条
    <div class="timeline-year">2024.8 — 2025.11</div>
    <div class="timeline-dot"></div>       ← 那条线上的小圆点
    <div class="timeline-content">...</div>
  </div>
  <div class="timeline-item">        ← 第 2 条
    ...
  </div>
</div>
```

中间的竖线不是 HTML，是 **CSS 画的**：

```css
.timeline::before {
  content: '';              /* 伪元素——凭空创建了一个竖条 */
  position: absolute;       /* 绝对定位，脱离正常文档流 */
  left: 50%;                /* 放在正中间 */
  width: 2px;               /* 2 像素宽 */
  background: var(--primary); /* 蓝色 */
}
```

`::before` 叫做「伪元素」——它凭空创建了一个元素，不在 HTML 里。

**标签云的渲染：**

标签云数据存储为一个逗号分隔的字符串：

```javascript
'education.skills.tags': '环境与公共卫生管理, 生物信息学分析, GIS与区块链技术, ...'
```

页面里有一个内联脚本，用逗号把字符串切开，每个切开的小段生成一个 `<span class="tag">`：

```javascript
var tags = text.split(',');  // 用逗号切开字符串
tags.forEach(function(t) {
  var span = document.createElement('span');  // 创建一个新标签
  span.className = 'tag';                     // 给它 tag 类名
  span.textContent = t;                       // 填入文字
  el.appendChild(span);                       // 加到页面上
});
```

---

### 4. 项目与研究 `projects.html`

**作用：** 工作经历 + 7 个研究项目。

**结构：**

```
<main>
  ├── <section class="page-hero">
  ├── <section class="section">     ← 工作经历（2 张卡片）
  └── <section class="section-alt"> ← 研究项目（7 张卡片，灰色背景）
```

**工作经历的特殊属性：**

注意工作经历的描述用了不同的属性：

```html
<!-- ❌ 普通文本用 data-i18n -->
<p data-i18n="projects.work.0.title">Holcim China</p>

<!-- ✅ 带 HTML 标签的内容用 data-i18n-html -->
<ul data-i18n-html="projects.work.0.desc">
  <li>内容加载中...</li>
</ul>
```

`data-i18n-html` 和 `data-i18n` 的区别：

| 属性 | 用在什么地方 | JS 里的处理 |
|------|-------------|-----------|
| `data-i18n` | **纯文字**（标题、段落） | 用 `.textContent` 替换 |
| `data-i18n-html` | **带 HTML 标签的文字**（列表、加粗） | 用 `.innerHTML` 替换 |

为什么不能随便用 `innerHTML`？安全原因——如果是用户输入的内容，`innerHTML` 可能被注入恶意脚本。但这个项目的文字都是站长自己写的，所以安全。

**7 个项目的卡片网格：**

```html
<div class="card-grid">
  <div class="card fade-in">项目1</div>
  <div class="card fade-in">项目2</div>
  ...
</div>
```

`card-grid` 的 CSS 核心：

```css
.card-grid {
  display: grid;                                    /* 使用网格布局 */
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));  /* 自动列数 */
  gap: 1.5rem;                                      /* 卡片间距 */
}
```

这句 CSS 的意思：「自动计算一行能放几张卡片，每张卡片最少 300px 宽，多余空间大家平分。」

---

### 5. 兴趣与生活 `interests.html`

**作用：** 最复杂的页面——相册灯箱、音频播放列表、视频网格。

这个页面的特殊性在于：它有**三个内联 `<script>` 块**，而不是靠外部 JS 文件。

```
<script>
  /* 脚本1：灯箱功能（点击照片放大浏览） */      ← 在页面中间
</script>

<script src="js/i18n-data.js"></script>        ← 底部共享脚本
<script src="js/i18n-engine.js"></script>
<script src="js/shared.js"></script>

<script>
  /* 脚本2：动态加载音频/视频播放列表 */        ← 在共享脚本之后
</script>
```

**灯箱原理：**

```
点击缩略图 → 找到大图地址 → 把大图地址设给灯箱里的 <img> → 显示灯箱

关闭灯箱 → 把灯箱隐藏 → 恢复页面滚动
```

关键数据结构：

```javascript
var photoArray = [];  // 收集所有可浏览的图片地址

// 遍历每个 .photo-item
photoItems.forEach(function(item) {
  var img = item.querySelector('img');  // 找内部的 <img>
  if (img && img.src) {
    photoArray.push(img.src);  // 有真实图片就加到列表里
  }
});
```

**动态加载音频/视频：**

音频和视频不是写死在 HTML 里的，而是：

1. 页面加载时，JS 请求 `assets/audio/list.txt`
2. 读到文件名 `a thousand years.mp3`
3. 动态生成 `<audio>` 标签插入页面

这样新增音频/视频只需要在 `list.txt` 里加一行文件名，不用改 HTML。

---

### 6. 联系方式 `contact.html`

**作用：** 密码保护的联系信息——和普通用户验证交互。

这个页面有两个关键的 `<div>`：

```html
<div id="passwordCard">     ← 初始状态：显示密码输入框
  密码输入框 + 验证按钮
</div>

<div id="contactContent" style="display:none;">  ← 初始状态：隐藏
  邮箱 + WhatsApp + Telegram
</div>
```

初始状态下，`#passwordCard` 显示，`#contactContent` 隐藏（`display:none`）。

密码验证流程：

```
用户输入密码 → PBKDF2 搅拌 10 万次 → 得到解密密钥
→ 用 AES-256-GCM 尝试解密 Base64 密文
→ 解密成功 → 隐藏 #passwordCard，显示 #contactContent
→ 解密失败 → 显示「密码错误」
```

**错误密码不可能「碰巧猜对」**，因为 AES-GCM 带有认证标签——密码不对的话，认证标签校验会失败，解密操作直接报错。不是「解出乱码」而是「根本不给你解密」。

---

## 图解：一个页面从打开到显示完，发生了什么

以首页为例，当你在浏览器输入网址并回车：

```
0ms   浏览器请求 index.html
      ↓
50ms  服务器返回 HTML 文本
      ↓
     浏览器开始解析 HTML，从上到下逐行读取
      ↓
     遇到 <link rel="stylesheet" href="css/style.css">
      → 浏览器：「我先去下载样式表，你继续」
      → 异步下载，不阻塞 HTML 解析
      ↓
     遇到 <script src="js/i18n-data.js">
      → 浏览器：「等等！脚本要立刻执行」
      → 暂停 HTML 解析 → 下载并执行 i18n-data.js → 定义了 I18N 变量
      → 继续解析
      ↓
     遇到 <script src="js/i18n-engine.js">
      → 暂停 → 下载并执行 → 定义了 getText/setLang/updatePageText 函数
      → 继续解析
      ↓
     遇到 <script src="js/shared.js">
      → 暂停 → 下载并执行 →
        → 注入导航栏 HTML
        → 注入页脚 HTML
        → 设置暗色模式
        → 设置语言
        → 调用 updatePageText()：把所有 data-i18n 替换成真实文字
        → 设置 IntersectionObserver（滚动动画）
      → 继续解析
      ↓
100ms 解析完毕，页面完全显示
      ↓
      CSS 中的 fade-in 动画触发 → 卡片从透明到显现
```

---

## 下一步

现在你理解了每个页面的 HTML 结构和代码逻辑。下一篇我们将深入 CSS 样式系统，看看所有这些好看的视觉效果是怎么用代码画出来的。

**→ 继续阅读：[教程三：CSS 样式系统](./教程-03-CSS样式系统.md)**

---

> 📝 教程中展示的代码可能对敏感信息做了脱敏处理，不影响学习。
