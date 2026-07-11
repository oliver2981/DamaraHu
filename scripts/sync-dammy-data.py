#!/usr/bin/env python3
"""
Dammy 个人网站 — 数据同步脚本

读取 dammy-data/ 下所有 .txt 文件，
自动更新 i18n.js、HTML 文件，
复制媒体文件到 assets/，
然后提交并部署。
"""

import os
import re
import shutil
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'dammy-data')
JS = os.path.join(BASE, 'js', 'i18n.js')

# ============================================================
# Step 1: Parse all data files
# ============================================================

def parse_txt(path):
    """Parse a simple key=value text file. Returns dict."""
    result = {}
    if not os.path.exists(path):
        return result
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            if '=' in line:
                key, _, value = line.partition('=')
                key = key.strip()
                value = value.strip()
                # Strip visual markers 【】
                value = value.replace('【', '').replace('】', '')
                if value:
                    result[key] = value
    return result

print('Reading dammy-data files...')

profile = parse_txt(os.path.join(DATA, 'profile.txt'))
about = parse_txt(os.path.join(DATA, 'about', 'bio.txt'))
education = parse_txt(os.path.join(DATA, 'education', 'timeline.txt'))
projects = parse_txt(os.path.join(DATA, 'projects', 'projects.txt'))
interests = parse_txt(os.path.join(DATA, 'interests', 'interests.txt'))
contact = parse_txt(os.path.join(DATA, 'contact', 'contact.txt'))

# ============================================================
# Step 2: Build i18n dict
# ============================================================

name = profile.get('NAME', 'Dammy')
tagline = profile.get('TAGLINE', 'Student · Researcher · Creator')
logo = profile.get('LOGO', 'Dammy')

def tag(name, zh, en):
    return f"'{name}': '{zh}'", f"'{name}': '{en}'"

def _clean(v):
    return v.replace('【', '').replace('】', '').strip()

def _parse_value(data, n):
    key = f'VALUE_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = raw.split('|', 1)
        return _clean(parts[0]), _clean(parts[1])
    return _clean(raw), _clean(raw)

def _parse_timeline(data, n):
    key = f'ITEM_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = [_clean(p) for p in raw.split('|', 2)]
        while len(parts) < 3:
            parts.append('')
        return parts[0], parts[1], parts[2]
    return _clean(raw), _clean(raw), _clean(raw)

def _parse_project(data, n):
    key = f'PROJECT_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = [_clean(p) for p in raw.split('|', 2)]
        while len(parts) < 3:
            parts.append('')
        return parts[0], parts[1]
    return _clean(raw), _clean(raw)

def _parse_interest(data, n):
    key = f'ITEM_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = [_clean(p) for p in raw.split('|', 2)]
        while len(parts) < 3:
            parts.append('')
        return parts[1], parts[2]
    return _clean(raw), _clean(raw)

def _replace_nth_playlist_item(html, n, title, artist, duration):
    pattern = re.compile(
        r'(<div class="playlist-item"[^>]*>.*?'
        r'<div class="playlist-title">)(.*?)(</div>\s*'
        r'<div class="playlist-artist">)(.*?)(</div>\s*'
        r'<span class="playlist-duration">)(.*?)(</span>)',
        re.DOTALL
    )
    matches = list(pattern.finditer(html))
    if n <= len(matches):
        m = matches[n - 1]
        replacement = m.group(1) + title + m.group(3) + artist + m.group(5) + duration + m.group(7)
        html = html[:m.start()] + replacement + html[m.end():]
    return html

# i18n entries as list of (zh_line, en_line)
entries = {
    'nav.home': ('首页', 'Home'),
    'nav.about': ('关于我', 'About'),
    'nav.education': ('教育成长', 'Education'),
    'nav.projects': ('项目与研究', 'Projects'),
    'nav.interests': ('兴趣与生活', 'Interests'),
    'nav.contact': ('联系方式', 'Contact'),
    'nav.langToggle': ('EN', '中文'),
    'nav.themeToggle': ('\U0001f319', '☀️'),

    'footer.quickLinks': ('快速导航', 'Quick Links'),
    'footer.connect': ('社交链接', 'Connect'),
    'footer.copyright': (f'© 2026 {name}. All rights reserved.', f'© 2026 {name}. All rights reserved.'),

    'home.hero.greeting': ('你好，我是', "Hi, I'm"),
    'home.hero.name': (name, name),
    'home.hero.tagline': (tagline, tagline),
    'home.hero.cta1': ('了解更多', 'Learn More'),
    'home.hero.cta2': ('联系我', 'Contact Me'),
    'home.navCards.title': ('探索我的世界', 'Explore My World'),
    'home.navCards.subtitle': ('像浏览一所大学一样，了解我的方方面面', 'Discover every facet — just like browsing a university website'),
    'home.cards.about.title': ('关于我', 'About Me'),
    'home.cards.about.desc': ('我的故事、价值观与身份认同', 'My story, values, and identity'),
    'home.cards.education.title': ('教育成长', 'Education'),
    'home.cards.education.desc': ('学术旅程与关键成长节点', 'Academic journey and key milestones'),
    'home.cards.projects.title': ('项目与研究', 'Projects & Research'),
    'home.cards.projects.desc': ('我做过的事情与研究方向', 'What I have built and explored'),
    'home.cards.interests.title': ('兴趣与生活', 'Interests & Life'),
    'home.cards.interests.desc': ('课堂之外，我的热爱所在', 'Beyond the classroom, what I love'),
    'home.cards.contact.title': ('联系方式', 'Contact'),
    'home.cards.contact.desc': ('期待与你取得联系', 'I would love to hear from you'),

    # About
    'about.hero.title': ('关于我', 'About Me'),
    'about.hero.subtitle': (about.get('SUBTITLE', '一个多重身份的探索者'), 'A Multi-Faceted Explorer'),
    'about.tags.student': (about.get('TAGS', '学生,创造者,探索者').split(',')[0].strip(), about.get('TAGS', 'Student,Creator,Explorer').split(',')[0].strip()),
    'about.tags.creator': (
        about.get('TAGS', '学生,创造者,探索者').split(',')[1].strip() if len(about.get('TAGS', '').split(',')) > 1 else '创造者',
        'Creator'),
    'about.tags.explorer': (
        about.get('TAGS', '学生,创造者,探索者').split(',')[2].strip() if len(about.get('TAGS', '').split(',')) > 2 else '探索者',
        'Explorer'),
    'about.story.heading': ('我的故事', 'My Story'),
    'about.story.text': (
        about.get('STORY', f'你好！我是 {name}。'),
        about.get('STORY', f'Hi! I\'m {name}.')),
    'about.values.heading': ('核心价值观', 'Core Values'),
    'about.values.curiosity.title': (_parse_value(about, 1)[0], _parse_value(about, 1)[0]),
    'about.values.curiosity.desc': (_parse_value(about, 1)[1], _parse_value(about, 1)[1]),
    'about.values.execution.title': (_parse_value(about, 2)[0], _parse_value(about, 2)[0]),
    'about.values.execution.desc': (_parse_value(about, 2)[1], _parse_value(about, 2)[1]),
    'about.values.resilience.title': (_parse_value(about, 3)[0], _parse_value(about, 3)[0]),
    'about.values.resilience.desc': (_parse_value(about, 3)[1], _parse_value(about, 3)[1]),
    'about.values.empathy.title': (_parse_value(about, 4)[0], _parse_value(about, 4)[0]),
    'about.values.empathy.desc': (_parse_value(about, 4)[1], _parse_value(about, 4)[1]),

    # Education
    'education.hero.title': ('教育成长', 'Education & Growth'),
    'education.hero.subtitle': (education.get('SUBTITLE', '每一步都算数'), 'Every Step Counts'),
    'education.skills.heading': ('核心技能', 'Core Skills'),
    'education.timeline.0.year': (_parse_timeline(education, 1)[0], _parse_timeline(education, 1)[0]),
    'education.timeline.0.title': (_parse_timeline(education, 1)[1], _parse_timeline(education, 1)[1]),
    'education.timeline.0.desc': (_parse_timeline(education, 1)[2], _parse_timeline(education, 1)[2]),
    'education.timeline.1.year': (_parse_timeline(education, 2)[0], _parse_timeline(education, 2)[0]),
    'education.timeline.1.title': (_parse_timeline(education, 2)[1], _parse_timeline(education, 2)[1]),
    'education.timeline.1.desc': (_parse_timeline(education, 2)[2], _parse_timeline(education, 2)[2]),
    'education.timeline.2.year': (_parse_timeline(education, 3)[0], _parse_timeline(education, 3)[0]),
    'education.timeline.2.title': (_parse_timeline(education, 3)[1], _parse_timeline(education, 3)[1]),
    'education.timeline.2.desc': (_parse_timeline(education, 3)[2], _parse_timeline(education, 3)[2]),

    # Projects
    'projects.hero.title': ('项目与研究', 'Projects & Research'),
    'projects.hero.subtitle': (projects.get('SUBTITLE', '做过的那些事'), 'Things I Have Built'),
    'projects.research.heading': ('研究兴趣', 'Research Interests'),
    'projects.item.0.title': (_parse_project(projects, 1)[0], _parse_project(projects, 1)[0]),
    'projects.item.0.desc': (_parse_project(projects, 1)[1], _parse_project(projects, 1)[1]),
    'projects.item.1.title': (_parse_project(projects, 2)[0], _parse_project(projects, 2)[0]),
    'projects.item.1.desc': (_parse_project(projects, 2)[1], _parse_project(projects, 2)[1]),
    'projects.item.2.title': (_parse_project(projects, 3)[0], _parse_project(projects, 3)[0]),
    'projects.item.2.desc': (_parse_project(projects, 3)[1], _parse_project(projects, 3)[1]),
    'projects.item.3.title': (_parse_project(projects, 4)[0], _parse_project(projects, 4)[0]),
    'projects.item.3.desc': (_parse_project(projects, 4)[1], _parse_project(projects, 4)[1]),

    # Interests
    'interests.hero.title': ('兴趣与生活', 'Interests & Life'),
    'interests.hero.subtitle': (interests.get('SUBTITLE', '课堂之外，生活之中'), 'Beyond the Classroom'),
    'interests.item.0.title': (_parse_interest(interests, 1)[0], _parse_interest(interests, 1)[0]),
    'interests.item.0.desc': (_parse_interest(interests, 1)[1], _parse_interest(interests, 1)[1]),
    'interests.item.1.title': (_parse_interest(interests, 2)[0], _parse_interest(interests, 2)[0]),
    'interests.item.1.desc': (_parse_interest(interests, 2)[1], _parse_interest(interests, 2)[1]),
    'interests.item.2.title': (_parse_interest(interests, 3)[0], _parse_interest(interests, 3)[0]),
    'interests.item.2.desc': (_parse_interest(interests, 3)[1], _parse_interest(interests, 3)[1]),
    'interests.item.3.title': (_parse_interest(interests, 4)[0], _parse_interest(interests, 4)[0]),
    'interests.item.3.desc': (_parse_interest(interests, 4)[1], _parse_interest(interests, 4)[1]),
    'interests.gallery.heading': ('生活剪影', 'Life Snapshots'),

    # Memories (now part of interests page)
    'memories.photos.title': ('照片墙', 'Photo Gallery'),
    'memories.photos.desc': ('用镜头定格我们的故事', 'Our stories captured in frames'),
    'memories.videos.title': ('视频集', 'Video Collection'),
    'memories.videos.desc': ('会动的画面，会说话的记忆', 'Moving pictures, living memories'),
    'memories.audio.title': ('为你选的歌', 'Songs for You'),
    'memories.audio.desc': ('每一首都是我想到你时会听的旋律', 'Every melody reminds me of you'),
    'memories.audio.notracks': ('即将上线，先期待一下~', 'Coming soon — stay tuned!'),

    # Contact
    'contact.hero.title': ('联系方式', 'Get in Touch'),
    'contact.hero.subtitle': (contact.get('SUBTITLE', '期待与你交流'), 'I would love to hear from you'),
    'contact.info.heading': ('找到我', 'Find Me'),
    'contact.form.heading': ('发送消息', 'Send a Message'),
    'contact.form.name': ('你的名字', 'Your Name'),
    'contact.form.email': ('你的邮箱', 'Your Email'),
    'contact.form.message': ('你想说的话...', 'Your message...'),
    'contact.form.submit': ('发送', 'Send'),
    'contact.form.success': ('消息已发送！感谢你的来信。', 'Message sent! Thank you for reaching out.'),
}

def _clean(v):
    return v.replace('【', '').replace('】', '').strip()

def _parse_value(data, n):
    key = f'VALUE_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = raw.split('|', 1)
        return _clean(parts[0]), _clean(parts[1])
    return _clean(raw), _clean(raw)

def _parse_timeline(data, n):
    key = f'ITEM_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = [_clean(p) for p in raw.split('|', 2)]
        while len(parts) < 3:
            parts.append('')
        return parts[0], parts[1], parts[2]
    return _clean(raw), _clean(raw), _clean(raw)

def _parse_project(data, n):
    key = f'PROJECT_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = [_clean(p) for p in raw.split('|', 2)]
        while len(parts) < 3:
            parts.append('')
        return parts[0], parts[1]
    return _clean(raw), _clean(raw)

def _parse_interest(data, n):
    key = f'ITEM_{n}'
    raw = data.get(key, '')
    if '|' in raw:
        parts = [_clean(p) for p in raw.split('|', 2)]
        while len(parts) < 3:
            parts.append('')
        return parts[1], parts[2]
    return _clean(raw), _clean(raw)

# ============================================================
# Step 3: Write i18n.js
# ============================================================

print('Generating i18n.js...')

# Build zh section
zh_lines = []
en_lines = []
for key in entries:
    zh_val, en_val = entries[key]
    # Escape single quotes in values
    zh_val = zh_val.replace("\\", "\\\\").replace("'", "\\'")
    en_val = en_val.replace("\\", "\\\\").replace("'", "\\'")
    zh_lines.append(f"    '{key}': '{zh_val}',")
    en_lines.append(f"    '{key}': '{en_val}',")

i18n_js = f'''const I18N = {{
  zh: {{
{chr(10).join(zh_lines)}
  }},

  en: {{
{chr(10).join(en_lines)}
  }}
}};

function getText(key) {{
  var lang = document.documentElement.lang || 'zh';
  return (I18N[lang] && I18N[lang][key]) || key;
}}

function setLang(lang) {{
  document.documentElement.lang = lang;
  localStorage.setItem('lang', lang);
  updatePageText();
}}

function updatePageText() {{
  var elements = document.querySelectorAll('[data-i18n]');
  for (var i = 0; i < elements.length; i++) {{
    var key = elements[i].getAttribute('data-i18n');
    var text = getText(key);
    if (text) {{
      if (elements[i].tagName === 'INPUT' || elements[i].tagName === 'TEXTAREA') {{
        elements[i].placeholder = text;
      }} else {{
        elements[i].textContent = text;
      }}
    }}
  }}
}}
'''

with open(JS, 'w', encoding='utf-8') as f:
    f.write(i18n_js)

print(f'  i18n.js written ({len(entries)} keys)')

# ============================================================
# Step 4: Update shared.js logo name
# ============================================================

shared_js = os.path.join(BASE, 'js', 'shared.js')
with open(shared_js, 'r', encoding='utf-8') as f:
    shared = f.read()

# Replace logo name in nav and footer
shared = re.sub(r"class=\"nav-logo\">[^<]+</a>", f'class="nav-logo">{logo}</a>', shared)
shared = re.sub(r"<h4>[^<]+</h4>\s*<p data-i18n=\"home.hero.tagline\"", f'<h4>{logo}</h4>\n        <p data-i18n="home.hero.tagline"', shared)

with open(shared_js, 'w', encoding='utf-8') as f:
    f.write(shared)

print('  shared.js updated (logo name)')

# ============================================================
# Step 5: Update contact.html links
# ============================================================

contact_html = os.path.join(BASE, 'contact.html')
if os.path.exists(contact_html):
    with open(contact_html, 'r', encoding='utf-8') as f:
        chtml = f.read()

    email = contact.get('EMAIL', 'hello@example.com')
    github = contact.get('GITHUB', 'https://github.com/')
    linkedin = contact.get('LINKEDIN', 'https://linkedin.com/')
    formspree = contact.get('FORMSPREE_ID', 'your-form-id')

    chtml = re.sub(r'mailto:[^\"]+', f'mailto:{email}', chtml)
    chtml = re.sub(r'github\.com/[^\"]*', github.split('://', 1)[-1] if '://' in github else github, chtml)
    chtml = re.sub(r'linkedin\.com/[^\"]*', linkedin.split('://', 1)[-1] if '://' in linkedin else linkedin, chtml)
    # Update the actual href values
    chtml = re.sub(r'href="https://github\.com/[^"]*"', f'href="{github}"', chtml)
    chtml = re.sub(r'href="https://linkedin\.com/[^"]*"', f'href="{linkedin}"', chtml)
    chtml = re.sub(r'formspree\.io/f/[^"]*', f'formspree.io/f/{formspree}' if formspree else 'formspree.io/f/your-form-id', chtml)

    with open(contact_html, 'w', encoding='utf-8') as f:
        f.write(chtml)
    print('  contact.html updated')

# ============================================================
# Step 6: Update interests.html song names
# ============================================================

interests_html = os.path.join(BASE, 'interests.html')
if os.path.exists(interests_html):
    with open(interests_html, 'r', encoding='utf-8') as f:
        ihtml = f.read()

    # Update song titles/artists in playlist
    for n in [1, 2, 3]:
        song_raw = interests.get(f'SONG_{n}', '')
        if '|' in song_raw:
            parts = [p.strip() for p in song_raw.split('|', 2)]
            title, artist = parts[0], parts[1] if len(parts) > 1 else ''
            duration = parts[2] if len(parts) > 2 else '0:00'
            # Replace the nth playlist item's title, artist, duration
            # Use a simple approach: replace in order
            ihtml = _replace_nth_playlist_item(ihtml, n, title, artist, duration)

    with open(interests_html, 'w', encoding='utf-8') as f:
        f.write(ihtml)
    print('  interests.html updated (song playlist)')

# ============================================================
# Step 7: Copy media files
# ============================================================

print('Copying media files...')

# Photos
photo_dir = os.path.join(DATA, 'photos')
asset_photo_dir = os.path.join(BASE, 'assets', 'images', 'memories')
os.makedirs(asset_photo_dir, exist_ok=True)
copied_photos = 0
for f in os.listdir(photo_dir):
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and not f.startswith('README'):
        src = os.path.join(photo_dir, f)
        dst = os.path.join(asset_photo_dir, f)
        shutil.copy2(src, dst)
        copied_photos += 1
        print(f'  photo: {f} -> assets/images/memories/')

# Avatar
avatar_src = os.path.join(DATA, 'about', 'avatar.jpg')
if not os.path.exists(avatar_src):
    avatar_src = os.path.join(DATA, 'about', 'avatar.png')
if os.path.exists(avatar_src):
    avatar_dir = os.path.join(BASE, 'assets', 'images')
    os.makedirs(avatar_dir, exist_ok=True)
    ext = os.path.splitext(avatar_src)[1]
    shutil.copy2(avatar_src, os.path.join(avatar_dir, f'avatar{ext}'))
    print(f'  avatar copied to assets/images/')

# Videos
video_dir = os.path.join(DATA, 'videos')
asset_video_dir = os.path.join(BASE, 'assets', 'videos')
os.makedirs(asset_video_dir, exist_ok=True)
copied_videos = 0
for f in os.listdir(video_dir):
    if f.lower().endswith(('.mp4', '.webm', '.mov')) and not f.startswith('README'):
        src = os.path.join(video_dir, f)
        dst = os.path.join(asset_video_dir, f)
        shutil.copy2(src, dst)
        copied_videos += 1
        print(f'  video: {f} -> assets/videos/')

# Audio
audio_dir = os.path.join(DATA, 'audio')
asset_audio_dir = os.path.join(BASE, 'assets', 'audio')
os.makedirs(asset_audio_dir, exist_ok=True)
copied_audio = 0
for f in os.listdir(audio_dir):
    if f.lower().endswith(('.mp3', '.ogg', '.wav', '.m4a')) and not f.startswith('README'):
        src = os.path.join(audio_dir, f)
        dst = os.path.join(asset_audio_dir, f)
        shutil.copy2(src, dst)
        copied_audio += 1
        print(f'  audio: {f} -> assets/audio/')

print(f'\nSummary: {len(entries)} i18n keys, {copied_photos} photos, {copied_videos} videos, {copied_audio} audio files')
print('Sync complete! Ready to commit and deploy.')
print('')
print('Files changed:')
print('  - js/i18n.js')
print('  - js/shared.js')
print('  - contact.html')
print('  - interests.html')
print('  - assets/images/memories/* (photos)')
print('  - assets/images/avatar.*')
print('  - assets/videos/*')
print('  - assets/audio/*')

