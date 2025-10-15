# Quest Master - SEO Image Requirements

## 📸 Required Images for SEO

### 1. Open Graph Image (`og-image.png`)
**Purpose:** Shown when sharing on Facebook, LinkedIn, WhatsApp, Slack, Discord

**Specifications:**
- **Size:** 1200 x 630 pixels (exact)
- **Format:** PNG or JPG
- **File Size:** Under 5 MB (ideally under 500 KB)
- **Location:** `static/images/og-image.png`

**Content Suggestions:**
```
┌─────────────────────────────────────┐
│  ⚔️ Quest Master                    │
│                                     │
│  Turn Your Tasks Into               │
│  Epic Quests                        │
│                                     │
│  [Screenshot of app or character]   │
│                                     │
│  Free Gamified Task Manager         │
└─────────────────────────────────────┘
```

**Design Tips:**
- Use your brand colors: Orange (#d97706) and Purple (#7c3aed)
- Include your logo/emoji ⚔️
- Keep text to minimum (80 characters max)
- Use large, bold fonts (60px+ for headlines)
- Add a screenshot or character graphic
- Leave 10% margin on all sides (safe zone)

**Tools to Use:**
- [Canva](https://canva.com) - Use "Facebook Post" template (1200x630)
- [Figma](https://figma.com) - Free design tool
- Adobe Photoshop/Illustrator
- [Placid](https://placid.app) - Automated image generation

---

### 2. Twitter Card Image (`twitter-card.png`)
**Purpose:** Shown when sharing on Twitter/X

**Specifications:**
- **Size:** 1200 x 675 pixels (16:9 ratio)
- **Format:** PNG or JPG
- **File Size:** Under 5 MB
- **Location:** `static/images/twitter-card.png`

**Can Use Same Image:**
You can use the same image as Open Graph if you want to save time. Twitter will crop it to 16:9.

**Or Create Twitter-Specific:**
```
┌──────────────────────────────────────────┐
│  ⚔️ Quest Master | Gamified Tasks        │
│                                          │
│  [App screenshot or game interface]      │
│                                          │
│  Level Up Your Productivity 🎮           │
└──────────────────────────────────────────┘
```

---

### 3. Logo (`logo.png`)
**Purpose:** Used in structured data, search results, brand identity

**Specifications:**
- **Size:** 512 x 512 pixels (square)
- **Format:** PNG with transparent background
- **File Size:** Under 200 KB
- **Location:** `static/images/logo.png`

**Content:**
- Your Quest Master logo
- ⚔️ sword emoji or custom icon
- Clean, simple design
- Transparent background preferred
- Should work well at small sizes (16px)

**Design Ideas:**
```
Simple version:
  ⚔️  (Just the sword emoji enlarged)

Text version:
  ┌─────────┐
  │   ⚔️    │
  │  QUEST  │
  │ MASTER  │
  └─────────┘

Badge style:
  ┌─────────────┐
  │   ⚔️ QM     │  (QM = Quest Master)
  └─────────────┘
```

---

### 4. Screenshot (`screenshot.png`)
**Purpose:** Shows app interface in search results and directories

**Specifications:**
- **Size:** 1280 x 720 pixels minimum (can be larger)
- **Format:** PNG or JPG
- **File Size:** Under 2 MB
- **Location:** `static/images/screenshot.png`

**What to Capture:**
1. Open your Quest Master app
2. Make sure it looks good:
   - Character with some stats
   - 2-3 active quests visible
   - Nice stats/XP bars
   - Good color theme selected
3. Take a full browser screenshot
4. Crop to show just the app (remove browser UI)
5. Optional: Add a subtle border/shadow

**Tools for Screenshots:**
- Browser Developer Tools (F12 → Device Toolbar → Screenshot)
- [Shottr](https://shottr.cc/) (Mac, free)
- Windows Snipping Tool (Windows)
- [LightShot](https://prnt.sc/) (Cross-platform)
- [Screely](https://screely.com/) - Add browser mockup (online)

---

### 5. Favicon Files
**Purpose:** Browser tab icon, bookmarks, mobile home screen

**Specifications:**
- **favicon-16x16.png** (16 x 16 pixels)
- **favicon-32x32.png** (32 x 32 pixels)
- **apple-touch-icon.png** (180 x 180 pixels)
- **Format:** PNG
- **Location:** `static/` folder (root)

**Content:**
- Simplified version of your logo
- Must be recognizable at tiny sizes
- ⚔️ emoji works great as favicon
- Use solid background color (not transparent for favicon)

**Easy Generation:**
1. Go to [favicon.io](https://favicon.io/)
2. Choose method:
   - **From Text:** Type "⚔️" or "QM"
   - **From Image:** Upload your logo
   - **From Emoji:** Select ⚔️ sword emoji
3. Customize colors (use #d97706 background)
4. Download ZIP
5. Extract all files to `static/` folder

---

## 🎨 Quick Design Guide

### Color Palette (from your app):
- **Primary Orange:** #d97706 (RGB: 217, 119, 6)
- **Primary Purple:** #7c3aed (RGB: 124, 58, 237)
- **Dark Background:** #0f0c29 (RGB: 15, 12, 41)
- **Light Text:** #f1f5f9 (RGB: 241, 245, 249)
- **Accent Gray:** #94a3b8 (RGB: 148, 163, 184)

### Font Suggestions:
- Headlines: Segoe UI, Roboto, Inter (bold)
- Body: Segoe UI, Arial, Helvetica

### Design Principles:
1. **Contrast:** Use dark backgrounds with light text
2. **Simplicity:** Less is more - don't overcrowd
3. **Brand Colors:** Use orange and purple prominently
4. **Gaming Aesthetic:** Add RPG elements (swords, shields, stars)
5. **Clear Hierarchy:** Make key message stand out

---

## 📦 Canva Templates (Free)

You can use these Canva templates and customize them:

1. **For OG Image:**
   - Search: "Facebook Post" (1200x630)
   - Use "Gaming" or "App Promo" templates
   - Customize with your colors and text

2. **For Twitter Card:**
   - Search: "Twitter Post" (1200x675)
   - Or use "YouTube Thumbnail" template (same ratio)

3. **For Logo:**
   - Search: "Logo" (square)
   - Keep it simple and bold

---

## ✅ Image Checklist

Before uploading images, verify:

- [ ] Correct dimensions (check specs above)
- [ ] File size optimized (use TinyPNG.com to compress)
- [ ] Clear, readable text
- [ ] Brand colors used
- [ ] No copyright issues with graphics/fonts
- [ ] Saved in correct location (`static/images/`)
- [ ] Correct filenames (lowercase, no spaces)

---

## 🔧 Image Optimization Tools

Compress images before upload:
- [TinyPNG](https://tinypng.com/) - Best PNG compression
- [Squoosh](https://squoosh.app/) - Google's image optimizer
- [ImageOptim](https://imageoptim.com/) - Mac app
- [Compressor.io](https://compressor.io/) - Web-based

**Why optimize?**
- Faster page load = better SEO
- Better user experience
- Lower bandwidth costs
- Google prefers fast-loading images

---

## 📐 Quick Reference Table

| Image Type | Size | Format | Location | Max Size |
|------------|------|--------|----------|----------|
| OG Image | 1200×630 | PNG/JPG | `static/images/og-image.png` | 500 KB |
| Twitter Card | 1200×675 | PNG/JPG | `static/images/twitter-card.png` | 500 KB |
| Logo | 512×512 | PNG | `static/images/logo.png` | 200 KB |
| Screenshot | 1280×720+ | PNG/JPG | `static/images/screenshot.png` | 2 MB |
| Favicon 16 | 16×16 | PNG | `static/favicon-16x16.png` | 5 KB |
| Favicon 32 | 32×32 | PNG | `static/favicon-32x32.png` | 10 KB |
| Apple Touch | 180×180 | PNG | `static/apple-touch-icon.png` | 50 KB |

---

## 🎯 Priority Order

If you're short on time, create these first:

1. **Favicon** (5 min) - Use favicon.io with ⚔️ emoji
2. **Logo** (10 min) - Simple text + emoji
3. **OG Image** (15 min) - Most important for sharing
4. **Screenshot** (5 min) - Just capture your app
5. **Twitter Card** (optional) - Can reuse OG image

**Total time:** ~35 minutes with Canva

---

## 💡 Example Content

### OG Image Text Options:
- "Turn Tasks Into Epic Quests ⚔️"
- "Level Up Your Productivity 🎮"
- "Quest Master: Gamified Task Manager"
- "Make To-Do Lists Fun Again!"
- "RPG Productivity • Free Forever"

### Logo Text Options:
- "QM" (minimalist)
- "⚔️ Quest Master"
- "Quest Master" (full name)
- Just the ⚔️ emoji (simple)

Keep it simple and memorable!

---

## 🆘 Can't Design?

**Free Alternatives:**

1. **Use Emoji Only:**
   - OG Image: Large ⚔️ emoji + text on solid background
   - Logo: Just the ⚔️ emoji (works great!)
   - Favicon: ⚔️ emoji (use favicon.io)

2. **Use Screenshot Only:**
   - Take nice screenshots of your app
   - Add text overlay with free tools:
     - [Pablo by Buffer](https://pablo.buffer.com/)
     - [Crello](https://crello.com/)

3. **Hire on Fiverr:**
   - $5-20 for basic OG image + logo
   - Search: "social media graphics" or "og image design"

---

## ✨ You've Got This!

Remember: **Perfect is the enemy of good.** A simple image is better than no image. Even just a large ⚔️ emoji with your app name on a gradient background will work great!

Start simple, improve later. 🚀

