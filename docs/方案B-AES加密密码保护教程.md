# 方案 B：AES 加密密码保护 —— 静态网站高安全性教程

## 这是什么？

方案 A 有个问题：**内容虽然不显示，但源码里是明晃晃写着的**。懂一点 HTML 的人按下 F12，删掉 `display:none` 就能看到所有内容。

方案 B 解决了这个问题：**你的联系方式在源代码里就是一堆乱码**。只有输入正确的密码，浏览器才会用密码作为"钥匙"把乱码翻译成人能看懂的内容。

> 打个比方：方案 A 是把信纸藏在抽屉里（找个会开抽屉的人就能看到）。**方案 B 是把信纸放在透明盒子里，但信纸上的字本身就是密文——不知道密码的人看到的就是一堆毫无意义的乱码。**

---

## 安全程度

| 方面 | 说明 |
|------|------|
| 普通访客 | ✅ **防住了** |
| 会按 F12 的人 | ✅ **防住了** —— 源码里全是乱码，没有 `display:none` 可删 |
| 懂调试断点的人 | ⚠️ **理论上能破** —— 在解密函数的返回值处打断点可以拿到明文 |
| 离线暴力破解 | ✅ **防住了** —— AES-256 + PBKDF2(100000次迭代) 极端耗时 |

**一句话总结：除非攻击者非常专业且愿意花大量时间，否则看不到你的真实内容。对个人网站来说完全够用。**

---

## 技术原理（白话版）

整个过程分为三步，每一步都有它的作用：

### 第一步：PBKDF2 —— 把密码变成"钥匙"

你不能直接用密码 `111479` 去加密，因为真实世界的密码太短、太弱。**PBKDF2** 会把你的密码反复搅拌 10 万次，产生一把 256 位的"真正的钥匙"。

> 为什么搅拌 10 万次？为了让暴力破解的人也搅拌 10 万次——**每次测试密码的成本提高了 10 万倍**。

### 第二步：AES-256-GCM —— 用钥匙加密内容

AES 是一个"加密保险箱"，GCM 模式还会贴一个防伪标签（认证标签）。如果有人篡改了密文，解密时浏览器会发现标签不对，直接报错。

### 第三步：把加密结果存进网页

加密后的内容 + 盐值（PBKDF2 需要的随机调料）+ IV（AES 需要的随机起始值）都用 Base64 编码存进 `<script>` 标签里。Base64 就是一堆看起来像乱码的字母数字，比如 `WmqB/WSJ/3HsyG...`。

---

## 完整工作流程

```
用户输入密码 "111479"
       │
       ▼
PBKDF2 搅拌 10 万次 ──────► 派生出 AES 解密密钥
       │
       ▼
用密钥尝试解密 Base64 密文
       │
       ├── 密码正确 ──► 解密成功 ──► 显示联系方式
       │
       └── 密码错误 ──► 解密失败 ──► 显示"密码错误"
```

**关键点：密码错误时，AES-GCM 的防伪标签会校验失败，整个解密操作直接报错——没有任何办法能"试"出正确密码。**

---

## 如何在你的项目中使用

### 前提条件

- 你的网站需要部署在 **HTTPS** 上（Vercel、GitHub Pages、Netlify 都自带 HTTPS）
- 不能是 `file://` 本地文件打开（浏览器安全策略限制）
- 本地开发可以用 `http://localhost`（浏览器对 localhost 有特殊豁免）

### 第一步：加密你的内容（在电脑上操作）

打开终端（Windows 按 Win+R 输入 `cmd`，Mac 打开 Terminal），粘贴以下命令：

> ⚠️ 如果你还没安装 Node.js，先去 [nodejs.org](https://nodejs.org) 下载安装 LTS 版本。

```bash
node -e "
const crypto = require('crypto');

// ============================================
// 🔑 在这里修改你的密码和联系方式
// ============================================
const password = '111479';  // 改成你的密码
const plaintext = JSON.stringify({
  subtitle: 'Looking forward to hearing from you',
  email: [
    'yourname@life.hkbu.edu.hk',   // 改成你的邮箱
    'yourname@qq.com',
    'yourname@163.com'
  ],
  whatsapp: '+852 69972219',       // 改成你的 WhatsApp
  telegram: [
    '+86 17345028816',             // 改成你的 Telegram
    '+852 69972219'
  ]
});
// ============================================

const salt = crypto.randomBytes(16);
const key = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
const iv = crypto.randomBytes(12);
const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
let encrypted = cipher.update(plaintext, 'utf8', 'base64');
encrypted += cipher.final('base64');
const authTag = cipher.getAuthTag();
const combined = Buffer.concat([Buffer.from(encrypted, 'base64'), authTag]);

console.log('=== 复制下面的三行，替换 HTML 中对应的值 ===');
console.log('SALT=' + salt.toString('base64'));
console.log('IV=' + iv.toString('base64'));
console.log('COMBINED=' + combined.toString('base64'));
"
```

运行后会输出三行：
```
SALT=xxxxxxxxxxxxxx
IV=xxxxxxxxxxxxxx
COMBINED=xxxxxxxxxxxxxx
```

**把这三行复制保存好，下一步要用。**

### 第二步：创建 HTML 页面

新建一个 `contact.html`（或任何你想要的名字），复制下面的完整代码：

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
    .decrypting {
      color: #888;
      font-size: 0.85rem;
      margin-top: 0.75rem;
      display: none;
    }
    #contactContent { display: none; }
    #contactContent .info {
      background: #f0f7ff;
      border-radius: 8px;
      padding: 1.25rem;
      text-align: left;
      line-height: 2;
    }
    #contactContent .info .label {
      font-weight: 600;
      color: #555;
    }
    #contactContent .info a {
      color: #4A90D9;
      text-decoration: none;
    }
    #contactContent .info a:hover { text-decoration: underline; }
    .contact-item {
      margin-bottom: 1.25rem;
      text-align: center;
    }
    .contact-item:last-child { margin-bottom: 0; }
    .contact-item .icon { font-size: 1.5rem; margin-bottom: 0.25rem; }
    .contact-item .type { font-weight: 600; margin-bottom: 0.25rem; }
    .contact-item .value { color: #666; font-size: 0.9rem; }
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
  <p class="decrypting" id="decryptingMsg">验证中...</p>
</div>

<div class="card" id="contactContent">
  <h3 id="subtitleDisplay" style="margin-bottom:1.25rem;"></h3>
  <div class="contact-item">
    <div class="icon">📧</div>
    <div class="type">Email</div>
    <div class="value" id="emailList"></div>
  </div>
  <div class="contact-item">
    <div class="icon">💬</div>
    <div class="type">WhatsApp</div>
    <div class="value" id="whatsappDisplay"></div>
  </div>
  <div class="contact-item">
    <div class="icon">📱</div>
    <div class="type">Telegram</div>
    <div class="value" id="telegramList"></div>
  </div>
</div>

<script>
(function() {
  'use strict';

  // ============================================
  // 🔑 把下面三行替换成你在第一步得到的值！
  // ============================================
  var SALT = Uint8Array.from(atob('sIeou0qwsQOYO4lVHqh18A=='), function(c) { return c.charCodeAt(0); });
  var IV   = Uint8Array.from(atob('SGnx0cRTVKFEXZaJ'),        function(c) { return c.charCodeAt(0); });
  var CIPHERTEXT = 'WmqB/WSJ/3HsyG/qJ5EJDPwyuAL7+hMqfAm+fZONLVc4VCl6AM3PJejnc4PfI3h3SZUodgVCkj5c1RIiviqYXZeG5lnjwBchobb0n4E/oneVgfSLQB8fYJysuSMMuoQWRHWXaWC92tBH/3CEI/skTCnhDLEskK3yWvcdpNVoZ2htQRg8r1sMfEY4uXi37bcOl+2HhvzR/v8XzUhWgchW4YJ4co6+EVl1sEdCVbBUchg/pVF0y6h3UFDbaBqwiZAAW8ZuFNjjgUgnYI/zes5zdLD2R2a7U1Qq91eIMw==';
  // ============================================

  function showError(msg) {
    document.getElementById('errorMsg').textContent = msg;
    document.getElementById('errorMsg').style.display = 'block';
    document.getElementById('decryptingMsg').style.display = 'none';
  }

  function showContact(data) {
    document.getElementById('passwordCard').style.display = 'none';

    var content = document.getElementById('contactContent');
    content.style.display = 'block';

    document.getElementById('subtitleDisplay').textContent = data.subtitle;

    var emailHtml = data.email.map(function(e) {
      return '<a href="mailto:' + e + '" style="display:block;margin:0.15rem 0;">' + e + '</a>';
    }).join('');
    document.getElementById('emailList').innerHTML = emailHtml;

    document.getElementById('whatsappDisplay').textContent = data.whatsapp;

    var teleHtml = data.telegram.map(function(t) {
      return '<span style="display:block;margin:0.15rem 0;">' + t + '</span>';
    }).join('');
    document.getElementById('telegramList').innerHTML = teleHtml;
  }

  function decryptWithPassword(password) {
    document.getElementById('errorMsg').style.display = 'none';
    document.getElementById('decryptingMsg').style.display = 'block';

    // PBKDF2: 把密码变成 AES 密钥（10万次迭代）
    crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey'])
      .then(function(baseKey) {
        return crypto.subtle.deriveKey(
          { name: 'PBKDF2', salt: SALT, iterations: 100000, hash: 'SHA-256' },
          baseKey,
          { name: 'AES-GCM', length: 256 },
          false,
          ['decrypt']
        );
      })
      // AES-GCM: 用密钥解密
      .then(function(aesKey) {
        var ciphertextBytes = Uint8Array.from(atob(CIPHERTEXT), function(c) { return c.charCodeAt(0); });
        return crypto.subtle.decrypt(
          { name: 'AES-GCM', iv: IV, tagLength: 128 },
          aesKey,
          ciphertextBytes
        );
      })
      // 解密成功 → 显示内容
      .then(function(plaintext) {
        document.getElementById('decryptingMsg').style.display = 'none';
        var data = JSON.parse(new TextDecoder().decode(plaintext));
        showContact(data);
      })
      // 解密失败 → 密码错误
      .catch(function() {
        showError('密码错误，请重试');
      });
  }

  // 点击按钮
  document.getElementById('submitBtn').addEventListener('click', function() {
    var pw = document.getElementById('pwdInput').value;
    if (!pw) { showError('请输入密码'); return; }
    decryptWithPassword(pw);
  });

  // 按回车键
  document.getElementById('pwdInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      var pw = document.getElementById('pwdInput').value;
      if (!pw) { showError('请输入密码'); return; }
      decryptWithPassword(pw);
    }
  });
})();
</script>

</body>
</html>
```

### 第三步：替换三行关键数据

在代码中找到这三行：

```javascript
var SALT = Uint8Array.from(atob('...'), ...);
var IV   = Uint8Array.from(atob('...'), ...);
var CIPHERTEXT = '...';
```

把 `'...'` 里的内容**依次替换**成第一步生成的三行对应的值：

| 第一步输出 | 替换代码中的 |
|-----------|-------------|
| `SALT=xxxxxxxx` | `var SALT = ...` 的 `atob('...')` |
| `IV=xxxxxxxx`   | `var IV = ...` 的 `atob('...')`   |
| `COMBINED=xxxxxxxx` | `var CIPHERTEXT = '...'` |

### 第四步：部署到服务器

把文件上传到你的网站服务器。**记住：必须通过 HTTPS 访问，否则 Web Crypto API 不会工作。**

Vercel、GitHub Pages、Netlify 都自动提供 HTTPS，直接推送即可。

---

## 如何修改密码或联系方式？

每次修改密码或联系方式，都需要**重新执行第一步**（因为密文会变），然后用新的 SALT、IV、COMBINED 替换 HTML 中的三行数据。

1. 修改第一步脚本中的密码和联系方式
2. 重新运行 `node -e "..."` 命令
3. 复制新的 SALT、IV、COMBINED
4. 替换 HTML 中对应的三行
5. 保存并重新部署

---

## 常见问题

### Q: 为什么我本地打开 `file://` 不能用？

浏览器对 `file://` 协议有限制，Web Crypto API 的 `crypto.subtle` 在非安全环境下不可用。解决方法：
- 用 VS Code 的 Live Server 插件（右键 → Open with Live Server）
- 或在终端运行 `npx serve .` 然后访问 `http://localhost:3000`
- 部署到 Vercel 后自动可用（自带 HTTPS）

### Q: 密码存在哪里？服务器上？

**密码不存储在任何地方。** 你的密码从来没有离开过你的电脑。加密时用的是本机 Node.js，解密时用的是访客浏览器。整个过程是：

- 你本地加密 → 生成密文 → 密文放进网页
- 访客输入密码 → 浏览器用密码尝试解密密文 → 成功则显示

密码只在**你的脑子里**和**访客输入框里**存在过。

### Q: 如果我忘了密码怎么办？

**没有办法找回。** 你需要重新走第一步加密流程，用新密码生成新的密文，替换 HTML。

### Q: AES-256 真的安全吗？

AES-256 是目前全球公认的对称加密标准，被银行、政府、军队广泛使用。按现有计算能力，暴力破解 AES-256 需要的时间比宇宙年龄还长。

真正的薄弱环节不是算法，而是**密码复杂度**。`111479` 这类纯数字 6 位密码任何人拿到 SALT 后都可以离线暴力破解（大概几分钟）。建议使用 12 位以上的混合字符密码。

---

## 方案对比

| | 方案 A（哈希） | **方案 B（AES 加密）** |
|------|------|------|
| 原理 | 比对密码"指纹" | 用密码解密内容 |
| F12 能看到内容吗？ | ✅ **能** | ❌ **不能**（源码里是乱码） |
| 可以离线暴力破解吗？ | ✅ 能（拿到哈希值即可） | ⚠️ 能，但 PBKDF2 10万次迭代极大增加了成本 |
| 实现难度 | 简单 | 稍复杂（需要 Node.js 加密一次） |
| 需要 HTTPS 吗？ | 不需要 | **需要**（浏览器限制） |
| 适合场景 | 简单门槛 | **敏感联系信息、私人内容** |

---

## 真实案例：DamaraHu 个人网站

本项目已使用方案 B 实现了联系方式页面。查看 `contact.html` 可以看到完整的集成实现——包括与现有网站 CSS 样式、i18n 国际化系统、导航栏和页脚的整合。

**访问方式：**
- 线上：`https://damarahu-personal-website.vercel.app/contact`
- 密码：`111479`

> 💡 **本教程对应的方案 A 完整教程请查看：[方案A-哈希密码保护教程.md](./方案A-哈希密码保护教程.md)**
