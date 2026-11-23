# ✨ PROMPTURE Command Library — v2.9 (PWA)

[![Version](https://img.shields.io/badge/version-2.9-gold.svg)](https://jarvishl.github.io/PROMPTURE-Command-Library/)
[![Commands](https://img.shields.io/badge/commands-4626-brightgreen.svg)](#-collection-breakdown)
[![PWA](https://img.shields.io/badge/PWA-100%25_Offline_Ready-blue.svg)](#-progressive-web-app-pwa-features)
[![Platform](https://img.shields.io/badge/platform-Web%20%7C%20iOS%20%7C%20Android%20%7C%20Desktop-orange.svg)](#-how-to-install-as-an-app)

A high-performance, mobile-first, and 100% offline-capable **Command & Prompt Engineering Library** designed for AI fashion photography, cinematic styling, and atelier garment generation (Midjourney, ChatGPT, Gemini, and Stable Diffusion).

GitHub Pages ပေါ်တွင် တင်ထားသော Zero-Dependency Single-Page Web Application ဖြစ်ပြီး **Command ပေါင်း ၄,၆၂၆ ခု** ကို မြန်မာ / English နှစ်ဘာသာဖြင့် အချိန်မရွေး လျင်မြန်စွာ ရှာဖွေ၊ ရွေးချယ်၊ ကူးယူ အသုံးပြုနိုင်ပါသည်။

---

## 📊 Collection Breakdown

| Icon | Collection | Commands | Target Workflow |
| :---: | :---| :---: | :---|
| 📝 | **PROMPTURE** | **220** | Prompt Generation, Layer Audits, Camera & Lighting |
| 🎨 | **PROMPTURE STUDIO** | **2,760** | Image Rendering, Relighting, Poses, Flashes & Inpainting |
| 👗 | **Outfit Revisions** | **600** | Garment Cuts, Traditional Wear, Fabric Realism & Physics |
| 📱 | **Mobile Camera** | **46** | 26mm Smartphone Aesthetics, Deep-DOF & Casual Realism |
| ✍️ | **K+P Generator** | **200** | HYBRID K+P Structured Prompt Construction |
| 📸 | **K+P Studio** | **500** | HYBRID K+P Studio Rendering & Body Fidelity Controls |
| 🪡 | **KANOTE SPEC** | **100** | Garment Specification, Measurements & Tailor Notes |
| 🧵 | **KANOTE FLAT** | **100** | Ghost-Mannequin, Hanger Staging & Technical Flats |
| 🎨 | **KANOTE BLUEPRINT** | **100** | Design Conception, Heritage Motifs & Guardrail Prompts |
| ⭐ | **Favorites** | *Dynamic* | User-Curated Saved Commands (Persisted via LocalStorage) |
| 🌟 | **TOTAL** | **4,626** | **All-in-One Fashion Production Suite** |

---

## 📱 Progressive Web App (PWA) Features

v2.9 မှစတင်၍ တကယ့် Native Mobile/Desktop App တစ်ခုသဖွယ် Install လုပ်၍ အသုံးပြုနိုင်ပါပြီ-

* 📶 **၁၀၀% Offline အသုံးပြုနိုင်ခြင်း:** Service Worker (`sw.js`) ကြောင့် အင်တာနက် လိုင်းမရှိချိန်၊ လေယာဉ်ပေါ်ရောက်နေချိန်တွင်ပင် Command ၄,၆၂၆ ခုလုံးကို ရှာဖွေ/ကူးယူနိုင်ခြင်း။
* 📲 **Standalone App Window:** Browser URL ဘားများ မပါဝင်ဘဲ ဖုန်း Screen ပြည့် သန့်ရှင်းစွာ ပွင့်လာခြင်း။
* ⚡ **Network-First Smart Cache:** အင်တာနက်ရှိချိန်တွင် GitHub ပေါ်မှ Update အသစ်များကို အလိုအလျောက် ရယူပြီး၊ လိုင်းမရှိချိန်တွင် ဒေသတွင်း Cache မှ ချောမွေ့စွာ ဖွင့်ပေးခြင်း။
* 💾 **နေရာချွေတာမှု:** ဖုန်း Memory ပေါ်တွင် 1~2 MB သာ သုံးစွဲပြီး အလွန်ပေါ့ပါးမြန်ဆန်ခြင်း။

---

## 🆕 Version Changelog

### v2.9 (Latest Release)
* 🔄 **Architecture & Category Restructuring:**
  * `🧵 Fabric Realism & Material Physics` (200 commands) ကို STUDIO မှ **👗 Outfit** သို့ ပြောင်းရွှေ့ပေါင်းစပ်ခဲ့သည်။
  * Outfit tab အရေအတွက် 400 မှ **600** သို့ တိုးတက်လာပြီး နံပါတ်စဉ် `#401` မှ `#600` သို့ ပြေပြစ်စွာ သတ်မှတ်ခဲ့သည်။
  * Outfit Category ထဲတွင် မူလ Fabric ၏ ဘေးကပ်လျက် (ဒုတိယနေရာ) ၌ နေရာချထားပေးသဖြင့် ပိတ်စဒီဇိုင်းပိုင်း ရှာဖွေရ ပိုမိုလွယ်ကူသွားသည်။
  * STUDIO tab ကို 2,960 မှ **2,760** သို့ ညှိယူပေးခဲ့ပြီး နံပါတ်စဉ် `#1` မှ `#2760` အထိ ကြားကွက်မရှိ ဆက်စပ်သွားသည်။
* 🚀 **PWA Integration:** `manifest.json`, `sw.js` (Smart Cache) နှင့် High-Resolution App Icons များကို ထည့်သွင်းပြီး installable app အဖြစ် အဆင့်မြှင့်တင်ခဲ့သည်။
* ⭐ **Favorites Migration (v5 → v6):** Index ရွှေ့ပြောင်းမှုများကြောင့် အသုံးပြုသူများ ယခင်က မှတ်သားထားသော Favorite ⭐ များ ပျောက်ဆုံးမှု မရှိစေရန် အလိုအလျောက် ရွှေ့ပြောင်းပေးသည့် Algorithm ထည့်သွင်းထားသည်။

### v2.8
* 📊 **1,000 New Studio Commands:** Fix & Repair (200), Fabric Realism (200), Flash & Film Aesthetics (200), Prop & Interaction (200), Output & Layouts (200) တို့ကို ထည့်သွင်းခဲ့သည်။ (3,626 → 4,626 commands)
* ⭐ **Favorites Migration (v4 → v5):** Addon 1000 ကြောင့် အနောက်ဘက် Index များအတွက် အလိုအလျောက် ရွှေ့ပြောင်းမှု စနစ်သစ်။

### v2.7
* 🎨 **Studio Master Overhaul:** STUDIO ကို 890 မှ 1,960 commands သို့ တိုးချဲ့ခဲ့သည်။
* ⭐ **Favorites Migration (v3 → v4):** စာသားတိုက်ဆိုင်စစ်ဆေးမှု Algorithm ဖြင့် Favorite များကို ကာကွယ်ပေးခဲ့သည်။

---

## 📲 How to Install as an App

### 📱 iPhone / iPad (Safari)
1. Safari Browser ဖြင့် [https://jarvishl.github.io/PROMPTURE-Command-Library/](https://jarvishl.github.io/PROMPTURE-Command-Library/) သို့ ဝင်ပါ။
2. အောက်ခြေရှိ **Share** ခလုတ် (⎋) ကို နှိပ်ပါ။
3. အောက်သို့ အနည်းငယ်ဆွဲချပြီး **"Add to Home Screen" (ပင်မစခရင်သို့ ထည့်ရန်)** ကို ရွေးချယ်ပါ။

### 📱 Android (Chrome)
1. Chrome Browser ဖြင့် ဖွင့်ပါ။
2. ညာဘက်ထိပ်ရှိ မီနူး အစက် ၃ စက် (⋮) ကို နှိပ်ပါ။
3. **"Install app"** သို့မဟုတ် **"Add to Home screen"** ကို နှိပ်ပါ။

### 🖥️ Desktop (Chrome / Edge)
1. ကွန်ပျူတာ Browser ဖြင့် ဖွင့်ပါ။
2. URL ရိုက်သည့် လိပ်စာဘား၏ ညာဘက်ထိပ်တွင် ပေါ်လာသော **"Install" (ကွန်ပျူတာပုံ Icon လေး)** ကို နှိပ်ပြီး ထည့်သွင်းပါ။

---

## 🛠️ Key Technical Highlights

* **Zero Dependency:** ပြင်ပ JavaScript Framework များ (React/Vue/JQuery) မပါဝင်ဘဲ Pure Vanilla JS & Modern CSS ဖြင့်သာ ရေးသားထားသဖြင့် အလွန်မြန်ဆန်သည်။
* **Single File Core:** အချက်အလက်များ၊ Logo နှင့် Favicon များအားလုံးကို Base64 ဖြင့် `index.html` ထဲတွင် တစ်ပါတည်း ထည့်သွင်းထားသဖြင့် Broken Link များ လုံးဝမဖြစ်ပေါ်နိုင်ပါ။
* **Bilingual Instant Search:** အင်္ဂလိပ် သို့မဟုတ် မြန်မာစာလုံး ရိုက်ရှာသည်နှင့် DOM ပေါ်တွင် ချက်ချင်း စစ်ထုတ်ပေးသည်။
* **Virtual Chunking / Infinite Scroll:** IntersectionObserver API ဖြင့် Command များကို အခု ၁၀၀ စီသာ ခွဲတင်ပေးသဖြင့် Memory စားသက်သာသည်။
* **Body Anchor Protection:** MODEL-001 ၏ အချိုးအစား (39/27/44, 157cm) မပျက်စီးစေရေးအတွက် Anti-Slimming Guardrail Command များကို စနစ်တကျ ထည့်သွင်းထားသည်။

---

## 📁 Repository Structure

```text
PROMPTURE-Command-Library/
├── index.html            # Main PWA Web Application (v2.9 · 4,626 Commands)
├── manifest.json         # PWA Web App Manifest (Standalone & Theme Config)
├── sw.js                 # Service Worker (Network-First Offline Caching)
├── icon-192.png          # App Icon (192x192 PNG)
├── icon-512.png          # App Icon (512x512 PNG)
├── build_v2_9.py         # Automation script for v2.9 restructuring
├── setup_pwa.py          # Automation script for PWA generation
└── README.md             # Project Documentation
