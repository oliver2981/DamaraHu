# 教程三：CSS 样式系统 —— 怎么用代码画出一套好看的皮肤

## 回顾

CSS 是房子的**装修**——决定东西长什么样。上一篇讲了 HTML 结构，这篇讲这个结构是怎么被「美化」成你看到的样子的。

---

## CSS 文件结构

打开 `css/style.css`，按顺序分为这几大块：

```
├── ① CSS 自定义属性（CSS 变量）    ← 全站的颜色、字体、间距等「设计参数」
├── ② Reset（重置）                ← 清除浏览器的默认样式
├── ③ 布局工具类                   ← container、section 等通用容器
├── ④ 导航栏                       ← 顶部固定导航条
├── ⑤ Hero 区域                    ← 大标题区
├── ⑥ 卡片系统                     ← 各种卡片样式
├── ⑦ 时间线                       ← 教育页面专用
├── ⑧ 标签                         ← 技能标签
├── ⑨ 表单                         ← 输入框、按钮
├── ⑩ 页脚                         ← 底部信息
├── ⑪ 动画                         ← 淡入效果
├── ⑫ 响应式                       ← 手机/平板适配
├── ⑬ 相册/灯箱                    ← 图片浏览
├── ⑭ 视频卡片                     ← 视频展示
└── ⑮ 音频播放列表                 ← 音乐播放
```

---

## 第一部分：CSS 变量 —— 设计系统的灵魂

```css
:root {
  --primary: #4A90D9;              /* 主色调：蓝色 */
  --primary-light: #EBF4FB;        /* 浅蓝：卡片背景 */
  --primary-dark: #2C5F8A;         /* 深蓝：按钮hover */
  --text: #1A1A2E;                 /* 文字颜色：深灰蓝 */
  --text-secondary: #5A5A7A;       /* 次要文字：中灰 */
  --bg: #FFFFFF;                   /* 背景色：白色 */
  --bg-alt: #F8F9FA;               /* 备用背景：极浅灰 */
  --card-shadow: 0 2px 8px rgba(0,0,0,0.06);    /* 卡片阴影 */
  --font-heading: Georgia, "Times New Roman", serif;  /* 标题字体 */
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --max-width: 1100px;             /* 内容最大宽度 */
  --radius: 8px;                   /* 圆角大小 */
}
```

### 为什么用变量而不是直接写死颜色？

对比两种写法：

```css
/* ❌ 硬编码：如果要换主色调，需要改 20 个地方 */
.btn { background: #4A90D9; }
.nav-links a:hover { color: #4A90D9; }
.tag { background: #EBF4FB; color: #2C5F8A; }
/* ... 还有 17 处 ... */

/* ✅ 用变量：换主色调只改一行 */
:root { --primary: #FF6B6B; }  /* 从蓝色变成红色，全站生效 */
```

这就是**设计系统（Design System）**的思想：把所有设计参数集中定义，改一处、处处更新。

### `:root` 是什么意思？

`:root` 是 CSS 选择器，选中 `<html>` 元素。变量定义在 `:root` 上，整个页面的任何元素都能使用它们。

### `var(--primary)` 怎么用？

```css
.btn-primary {
  background: var(--primary);  /* 使用 --primary 变量的值 */
}
```

---

## 第二部分：Reset —— 为什么需要清除默认样式

```css
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

### 什么是浏览器的默认样式？

每个浏览器都会给 HTML 标签加一些默认样式，比如：
- `<h1>` 默认有上下外边距
- `<ul>` 默认有左边距
- `<body>` 默认有 8px 外边距

但这些默认值**不同浏览器不一样**。Chrome 的 `<h1>` 可能间距 20px，Firefox 可能间距 21px。

所以设计规范的做法是：**先用 Reset 全部清零，再从零开始自己设置**。

### `box-sizing: border-box` 是什么？

这是最重要的 CSS 属性之一，用图解释：

```
没有 border-box：             有 border-box：
┌─────────────────┐          ┌─────────────────┐
│  padding 10px   │          │                 │
│  ┌─────────────┐│          │  content 180px  │
│  │ content     ││          │  (含 padding)   │
│  │ 200px 宽    ││          │                 │
│  └─────────────┘│          └─────────────────┘
│                 │          总宽度 = 200px（不变）
└─────────────────┘
总宽度 = 200 + 10 + 10 = 220px
```

没有 `border-box` 时，你设置了 `width: 200px`，加上 padding 后实际宽度会变成 220px，导致布局出错。有了 `border-box`，`width: 200px` 就是最终宽度，padding 从里面扣。**永远都在项目里加这一行。**

---

## 第三部分：导航栏

```css
.navbar {
  position: sticky;          /* 粘性定位——滚动时贴在顶部 */
  top: 0;                    /* 贴在页面最顶部 */
  z-index: 1000;             /* 层级最高——永远在最上面 */
  background: var(--bg);     /* 白色背景 */
  height: var(--nav-height); /* 64px 高 */
}
```

### `position: sticky` 是什么？

- `position: static`（默认）：元素跟着页面滚动
- `position: fixed`：元素固定在屏幕上，永远不动
- `position: sticky`：**两者的结合**——正常滚动时像 static，滚到顶后像 fixed

导航栏用 `sticky` 的好处：正常浏览时它占据自己的位置，滑到下面时它贴在顶部方便随时导航。

### `z-index: 1000` 是什么？

页面上的元素有「层叠顺序」。z-index 越大，层级越高，覆盖在更下层元素的上面。1000 基本能保证导航栏永远在最上面。

---

## 第四部分：响应式设计 —— 手机也能好看

```css
@media (max-width: 768px) {
  .nav-links {
    display: none;          /* 导航菜单隐藏 */
  }
  .nav-links.open {
    display: flex;          /* 点击汉堡按钮后才显示 */
  }
  .hamburger {
    display: flex;          /* 显示三横线按钮 */
  }
  .nav-cards {
    grid-template-columns: 1fr;  /* 卡片从 3 列变成 1 列 */
  }
}
```

### `@media` 是什么？

`@media` 是**条件样式**——「只有在某种条件下才应用这些样式」。

```css
@media (max-width: 768px) {  /* 条件：屏幕宽度 ≤ 768px */
  /* 这里的样式只在手机上生效 */
}
```

768px 是常见的「手机 vs 电脑」分界线：

| 屏幕宽度 | 设备 | 布局策略 |
|----------|------|----------|
| ≤ 768px | 手机 | 单列布局、汉堡菜单、字号缩小 |
| 769-1024px | 平板 | 双列布局 |
| > 1024px | 电脑 | 完整多列布局 |

### 响应式的核心思想

不是给手机和电脑写两套完全不同的代码，而是**同一套代码，根据不同屏幕宽度调整排列方式**。

---

## 第五部分：淡入动画

```css
.fade-in {
  opacity: 0;                           /* 初始状态：完全透明 */
  transform: translateY(24px);          /* 初始状态：向下偏移 24px */
  transition: opacity 0.6s ease, transform 0.6s ease;
  /*           属性    时长 缓动函数 */
}

.fade-in.visible {
  opacity: 1;                           /* 最终状态：完全不透明 */
  transform: translateY(0);             /* 最终状态：回到原位 */
}
```

### 动画流程

```
初始状态（.fade-in）：
  - 透明看不见（opacity: 0）
  - 向下偏移 24px

当元素滚动到屏幕可见区域：
  → JS 给它加上 .visible 类
  → CSS transition 在 0.6 秒内平滑过渡

结束状态（.fade-in.visible）：
  - 完全可见（opacity: 1）
  - 回到原位（translateY: 0）
```

### JS 怎么知道元素进入可见范围了？

```javascript
var observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {           // 元素进入视口了
      entry.target.classList.add('visible'); // 加 visible 类 → 触发动画
      observer.unobserve(entry.target);   // 只看一次，不再重复
    }
  });
});
```

`IntersectionObserver` 是浏览器自带的「哨兵」——帮你盯着元素有没有进入屏幕。

---

## 第六部分：暗色模式

```css
[data-theme="dark"] {
  --primary: #5BA0E8;          /* 暗色下主色调亮一点 */
  --text: #E8ECF1;             /* 文字变成浅色 */
  --bg: #0F1923;               /* 背景变成深色 */
  --bg-alt: #1A2735;           /* 次要背景也变深 */
}
```

暗色模式的巧妙之处：**只改 CSS 变量值，不改任何具体样式**。

因为所有的颜色都是用 `var(--bg)`、`var(--text)` 这样的变量引用的，所以改一次变量，全站所有用到这个变量的地方都自动更新。

JS 切换暗色模式的逻辑：

```javascript
themeToggle.addEventListener('click', function() {
  var isDark = document.documentElement.hasAttribute('data-theme');
  if (isDark) {
    document.documentElement.removeAttribute('data-theme');  // 移除 data-theme → 恢复亮色
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');  // 添加 data-theme="dark" → 暗色
  }
  localStorage.setItem('theme', isDark ? 'light' : 'dark');  // 记住选择
});
```

关键点：
- `data-theme` 是自定义属性，加在 `<html>` 标签上
- CSS 里 `[data-theme="dark"]` 是一个**属性选择器**——只对有 `data-theme="dark"` 属性的元素生效
- `localStorage` 记录选择，下次打开网站还是暗色

---

## 时间线：CSS 如何画出竖线和圆点

```css
/* 竖线 */
.timeline::before {
  content: '';                      /* 伪元素——凭空创建 */
  position: absolute;               /* 脱离文档流 */
  left: 50%;                        /* 水平居中 */
  top: 0;
  bottom: 0;
  width: 2px;                       /* 2 像素宽 */
  background: var(--primary);       /* 蓝色 */
  transform: translateX(-50%);      /* 修正偏移（让线的中心对齐，不是左边缘） */
}

/* 圆点 */
.timeline-dot {
  position: absolute;
  left: 50%;
  width: 14px;
  height: 14px;
  border-radius: 50%;              /* 50% 圆角 = 圆形 */
  background: var(--primary);
  border: 3px solid var(--bg);     /* 白色边框——制造空心效果 */
  transform: translateX(-50%);
  z-index: 1;                      /* 在竖线上面 */
}
```

### `translateX(-50%)` 为什么需要？

`left: 50%` 是把元素的**左边缘**放在中线上。但元素有宽度（14px），所以元素整体偏右了。`translateX(-50%)` 把元素往左移自身宽度的一半（7px），这样元素的**中心**刚好在中线上。

---

## 卡片悬浮效果

```css
.card {
  transition: transform var(--transition), box-shadow var(--transition);
  /*           属性     过渡时长/缓动    属性        过渡时长/缓动 */
}

.card:hover {
  transform: translateY(-4px);                     /* 上浮 4px */
  box-shadow: var(--card-shadow-hover);            /* 阴影加深 */
}
```

`transition` 是 CSS 最常用的特性——让状态变化「平滑过渡」，而不是瞬间切换。`var(--transition)` 展开就是 `0.3s ease`：300 毫秒、先快后慢。

---

## 下一步

现在你理解了 CSS 怎么画出了全站的外观——从变量的设计系统思想，到响应式布局、动画、暗色模式。下一篇我们将深入 JavaScript 系统，看国际化引擎和共享脚本是怎么运作的。

**→ 继续阅读：[教程四：JavaScript 国际化与动态内容](./教程-04-JavaScript国际化系统.md)**

---

> 📝 本教程假设你已阅读前两篇教程，或已有基础的 HTML/CSS 认知。
