# 方案 A：哈希密码保护 —— 静态网站密码验证教程

## 这是什么？

想象你的联系方式是一扇**需要密码才能打开的门**。方案 A 就是这扇门——访问者必须输入正确的密码，才能看到门后的内容。

**方案 A 的原理：** 把密码的"指纹"（学名叫**哈希值**）存在网页代码里。当用户输入密码时，把输入的密码也转换成"指纹"，比对两个指纹是否相同。相同就放行，不同就拒绝。

> 打个比方：你有一把锁，锁芯的形状（哈希值）是公开写在前端代码里的。只有形状完全匹配的钥匙（正确的密码）才能打开。F12 能看到锁芯的形状，但**无法从形状反推出钥匙长什么样**。

---

## 安全程度

| 方面 | 说明 |
|------|------|
| 普通访客 | ✅ **防住了** —— 没有密码看不到隐藏内容 |
| 会按 F12 的人 | ⚠️ **防不住** —— 可以找到隐藏的内容区块，直接用代码显示出来 |
| 会按 F12 且有耐心的人 | ⚠️ **防不住** —— 可以找到哈希值，用工具离线暴力破解 |

**一句话总结：防君子不防小人。适合非敏感信息的简单保护。**

---

## 完整代码（复制即用）

### 第一步：生成密码哈希值

你需要先把你密码的 SHA-256 哈希值算出来。打开浏览器，按 F12 进入控制台（Console），粘贴以下代码并回车：

```javascript
// 把下面的 '你的密码' 改成你想要的密码，然后回车运行
async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

hashPassword('你的密码').then(hash => console.log('你的哈希值：', hash));
```

运行后控制台会输出一串像这样的字符：`6b3a55e0...`（64 个字符），**把这串字符复制保存好**。

### 第二步：创建受保护的 HTML 页面

新建一个 HTML 文件（比如 `secret.html`），复制下面的完整代码：

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>联系方式 - 需要密码</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f5f5f5;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      padding: 2.5rem;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      max-width: 420px;
      width: 100%;
      text-align: center;
    }
    .card h2 { margin-bottom: 0.5rem; font-size: 1.5rem; }
    .card p.sub { color: #888; margin-bottom: 1.5rem; font-size: 0.9rem; }
    .input-group {
      display: flex;
      gap: 0.5rem;
    }
    input[type="password"] {
      flex: 1;
      padding: 0.75rem 1rem;
      border: 2px solid #e0e0e0;
      border-radius: 8px;
      font-size: 1rem;
      outline: none;
      transition: border-color 0.2s;
    }
    input[type="password"]:focus { border-color: #4A90D9; }
    button {
      padding: 0.75rem 1.5rem;
      background: #4A90D9;
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.2s;
    }
    button:hover { background: #357ABD; }
    .error {
      color: #e74c3c;
      font-size: 0.85rem;
      margin-top: 0.75rem;
      display: none;
    }
    /* ✅ 受保护的内容默认隐藏 */
    #secretContent { display: none; }
    #secretContent h3 {
      font-size: 1.1rem;
      margin-bottom: 1rem;
      color: #333;
    }
    #secretContent .info {
      background: #f0f7ff;
      border-radius: 8px;
      padding: 1.25rem;
      text-align: left;
      line-height: 2;
    }
    #secretContent .info .label {
      font-weight: 600;
      color: #555;
    }
    #secretContent .info a {
      color: #4A90D9;
      text-decoration: none;
    }
    #secretContent .info a:hover { text-decoration: underline; }
    .lock-icon { font-size: 3rem; margin-bottom: 1rem; }
  </style>
</head>
<body>

<div class="card" id="passwordCard">
  <div class="lock-icon">🔐</div>
  <h2>联系方式</h2>
  <p class="sub">此页面需要密码才能访问</p>
  <div class="input-group">
    <input type="password" id="pwdInput" placeholder="请输入密码..." autocomplete="off">
    <button id="submitBtn">验证</button>
  </div>
  <p class="error" id="errorMsg">密码错误，请重试</p>
</div>

<!-- ✅ 这里是受保护的内容 —— 只有输入正确密码后才会显示 -->
<div class="card" id="secretContent">
  <h3>📬 期待与您联系</h3>
  <div class="info">
    <p><span class="label">📧 Email：</span><a href="mailto:yourname@example.com">yourname@example.com</a></p>
    <p><span class="label">💬 WhatsApp：</span>+852 1234 5678</p>
    <p><span class="label">📱 Telegram：</span>+86 138 0000 0000</p>
  </div>
</div>

<script>
(function() {
  'use strict';

  // ============================================
  // 🔑 把下面这串字符替换成你第一步生成的哈希值
  // ============================================
  var CORRECT_HASH = '6b3a55e0261b0304143f8059a95b27e3c3c9a56b28b3b7c4f1e2d3a4b5c6d7e8';
  // 👆 改这里！换掉这串假哈希值 👆
  // ============================================

  async function sha256(message) {
    var encoder = new TextEncoder();
    var data = encoder.encode(message);
    var hashBuffer = await crypto.subtle.digest('SHA-256', data);
    var hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(function(b) { return b.toString(16).padStart(2, '0'); }).join('');
  }

  function showError(msg) {
    var el = document.getElementById('errorMsg');
    el.textContent = msg;
    el.style.display = 'block';
  }

  function showSecret() {
    // 隐藏密码输入区，显示联系方式
    document.getElementById('passwordCard').style.display = 'none';
    document.getElementById('secretContent').style.display = 'block';
  }

  document.getElementById('submitBtn').addEventListener('click', function() {
    var input = document.getElementById('pwdInput').value;
    if (!input) {
      showError('请输入密码');
      return;
    }

    sha256(input).then(function(hash) {
      if (hash === CORRECT_HASH) {
        showSecret();
      } else {
        showError('密码错误，请重试');
      }
    });
  });

  // 支持回车键提交
  document.getElementById('pwdInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      document.getElementById('submitBtn').click();
    }
  });
})();
</script>

</body>
</html>
```

### 第三步：替换哈希值和联系方式

1. 找到代码中的 `CORRECT_HASH = '6b3a55e0...'`，把引号里的内容换成你第一步生成的哈希值
2. 找到 `<!-- ✅ 这里是受保护的内容 -->` 下面的部分，把邮箱、WhatsApp、Telegram 换成你自己的信息
3. 保存文件，用浏览器打开测试

---

## 如何修改密码？

1. 想好新密码
2. 回到第一步，用新密码生成新的哈希值
3. 在 HTML 文件中找到 `CORRECT_HASH`，替换成新的哈希值
4. 保存并重新部署

---

## 安全漏洞说明（重要！）

方案 A 有**两个已知弱点**，你必须了解：

### 漏洞 1：F12 开发者工具可以绕过

任何人都可以通过 F12 → Elements（元素）面板，找到 `id="secretContent"` 的 `<div>`，把 `style="display:none"` 删掉——内容就显示出来了。

**缓解措施：** 几乎没有。这是前端密码保护的固有限制。

### 漏洞 2：哈希值可以被离线破解

如果攻击者拿到了哈希值：
- 简单密码（如 `123456`）：**秒破**，攻击者用常见密码字典逐个试
- 中等密码（如 `damara2024`）：可能需要几个小时
- 强密码（如 `Xp9#mK2$zL8@qR5`）：几乎不可能在合理时间内破解

**缓解措施：使用长密码（12 位以上，含大小写字母、数字、特殊符号）。**

---

## 方案对比

| | 方案 A（哈希） | 方案 B（AES 加密） |
|------|------|------|
| 原理 | 比对密码"指纹" | 用密码解密内容 |
| F12 能看到隐藏内容吗？ | ✅ **能**（删除 `display:none` 即可） | ❌ **不能**（内容在源码里是乱码） |
| 实现难度 | 简单 | 稍复杂 |
| 适合场景 | 简单的访问控制，非敏感内容 | 需要更高安全性的场景 |

---

## 总结

- **用方案 A**：如果你只是想给访问加个门槛，不介意懂技术的人绕过
- **用方案 B**：如果你希望即使看源码也看不到真实内容

> 💡 **本教程对应的方案 B 完整教程请查看：[方案B-AES加密密码保护教程.md](./方案B-AES加密密码保护教程.md)**
