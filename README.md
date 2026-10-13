# ✨ PROMPTURE Command Library — v2.4

GitHub Pages ပေါ်တင်ထားတဲ့ static web app — **command ၁၅၅၆** ကို မြန်မာ / English နှစ်မျိုးလုံးနဲ့ ရှာဖွေ၊ ရွေးချယ်၊ ကူးယူနိုင်တယ်.

| Collection | Commands |
|---|---|
| 📝 PROMPTURE (prompt ထုတ်တဲ့ GPT/Gem အတွက်) | 220 |
| 🎨 PROMPTURE STUDIO (ပုံထုတ်တဲ့ GPT/Gem အတွက်) | 890 |
| 👗 Outfit Revisions (ဝတ်စုံပြင်ဆင်ချက်) | 400 |
| 📱 Mobile (ဖုန်းပုံစံ camera command များ) | 46 |
| **စုစုပေါင်း** | **1556** |

---

## 🆕 v2.4 မှာ ဘာတွေအသစ်ပါလဲ

- 📊 **Data update** — PROMPTURE 200→**220**, STUDIO 800→**890**
  - 🎥 PROMPTURE မှာ **Camera & Lighting** အခန်း တိုးချဲ့ (mobile-casual command အသစ် 20)
  - 🎨 STUDIO မှာ အသစ် 90: 📱 Casual Mobile Look 40 + 💡 Relight Only 25 + 📱 Full Recapture 25
- 🇲🇲 **ဘာသာပြန် အသစ်** — ညိုရဲ့ မြန်မာပြန်ဆိုချက် 1110 ခု အစားထိုးထည့်ပြီးသား
- ⭐ **Favorites auto-migration** — update တင်ပြီး ပထမအကြိမ်ဖွင့်ရင် သိမ်းထားတဲ့ ⭐ တွေ အသစ်နေရာကို **အလိုလျောက်ရွှေ့**ပေးမယ်

## 🆕 v2.3 မှာ ဘာတွေပါခဲ့လဲ

- 📱 **Mobile tab အသစ်** — Casual Mobile Camera Bank (46 commands) သီးခြား tab
- 🌟 အားလုံး → 1446 commands

## 🆕 v2.2 မှာ ဘာတွေပါခဲ့လဲ

- 🌐 **ဘာသာပြောင်း ခလုတ် (MM / ENG)** — ခေါင်းစဉ်ဘယ်ဘက်ထိပ်က စက်ဝိုင်းခလုတ် (🌙 နဲ့ အရွယ်တူ); နှိပ်တိုင်း မြန်မာ ↔ English ပြောင်း, ရွေးထားတာ မှတ်ထားမယ်
  - **MM mode** — card တွေ မြန်မာလို (အရင်အတိုင်း)
  - **ENG mode** — card + search bar + tab + စာသားတွေ အကုန် English
  - 🪟 Popup ကတော့ နှစ်မျိုးလုံး **EN + မြန်မာ** နှစ်ဘာသာ ဆက်ပြတယ်

## ✨ အခြေခံလုပ်ဆောင်ချက်များ

- 🔍 **Search** — မြန်မာ / English နှစ်မျိုးလုံး ရိုက်ရှာလို့ရ
- 📑 **Tabs** — 🌟 အားလုံး · 📝 PROMPTURE · 🎨 STUDIO · 👗 Outfit · 📱 Mobile · ⭐ အကြိုက်ဆုံး
- 📂 **Category filter** — 🔍 ဘေးက 📂 icon နှိပ်မှ ပွင့် (document အစဉ်လိုက်)
- 🧹 **Toolbar** — ၂ တန်းပါးပါးလေး; အောက်ဆွဲချရင် **ပုန်းသွား**မယ်, အပေါ်ဆွဲရင် ပြန်ပေါ်
- 🪟 **Popup** — ထိလိုက်ရင် English အရင်, မြန်မာ နောက် နှစ်ဘာသာ; 📋 = English မူရင်းသာ copy
- ⭐ **အကြိုက်ဆုံး** — 🤍 နှိပ်ရင် ❤️ ဖြစ်; ဖုန်း/browser ထဲမှာ သိမ်းထားတယ် (localStorage)
- 🌙 **Day / Night / System** — ခေါင်းစဉ်ညာဘက်က icon နှိပ်ပြီး ပြောင်း
- 🖼️ **Logo** — header မှာ PROMPTURE Command Library logo ပါတယ်

---

## 📁 ဖိုင်များ

| ဖိုင် | ရှင်းလင်းချက် |
|---|---|
| `index.html` | App တစ်ခုလုံး (command ၁၅၅၆ + logo + favicon အပါ) — GitHub ပေါ် တင်ရမယ့်ဖိုင် |
| `README.md` | ဒီဖိုင် |
| `build_v2_4.py` | App ပြန်ထုတ်တဲ့ script (developer အတွက်) |

> API key မလို, internet မလို (ပထမအကြိမ်ဖွင့်ပြီးရင်), server မလို — ဖိုင်တခုတည်းနဲ့ အလုပ်လုပ်။

---

## 🚀 GitHub Pages ပေါ် တင်နည်း / Update လုပ်နည်း

### ပထမအကြိမ် တင်မယ်ဆို
1. GitHub မှာ repo အသစ် ဆောက် — ဥပမာ `prompture-commands` (**Public**)
2. `index.html` ကို **Add file → Upload files** နဲ့ တင်
3. **Settings → Pages → Deploy from a branch** → `main` + `/ (root)` → **Save**
4. ၁–၂ မိနစ် စောင့်ပြီး ပေါ်လာတဲ့ link ကို ဖွင့်

### Version အသစ် update လုပ်မယ် (v2.4 လို)
1. Repo ထဲက `index.html` အဟောင်းကို ရွေး → **🗑️ Delete** (ဒါမှမဟုတ် အသစ်ကို အစားထိုး upload)
2. `index.html` အသစ်ကို **Upload** လုပ် → **Commit changes**
3. ၁–၂ မိနစ် စောင့်ပြီး hard refresh လုပ် — 📱 ဖုန်း: `⋮ → Reload` / 🖥️ ကွန်ပျူတာ: `Ctrl+Shift+R`
4. ⭐ အကြိုက်ဆုံးတွေ အလိုလျောက်ရွှေ့ပေးမယ် — ပထမအကြိမ်ဖွင့်ရင် ခဏစောင့်

---

## 📖 အသုံးပြုနည်း

1. 🔍 ရှာချင်တဲ့ စကားလုံး ရိုက် (မြန်မာ/English) — ဒါမှမဟုတ် tab / category နဲ့ ရွေး
2. 👆 ကြိုက်တဲ့ စာကြောင်းကို **ထိ** — popup ပွင့်လာမယ် (English + မြန်မာ)
3. 📋 နှိပ်ရင် **English command** copy ဖြစ်မယ် → ChatGPT / Gemini / PROMPTURE GPT မှာ **paste** လုပ်
4. 🤍 နှိပ်ရင် **အကြိုက်ဆုံး** ထဲ သိမ်း — ⭐ tab မှာ ပြန်ကြည့်

---

## ⚠️ မှတ်ချက်များ

- ⭐ အကြိုက်ဆုံးနဲ့ 🌙 Day/Night ရွေးချယ်မှုက **သုံးနေတဲ့ browser/ဖုန်းထဲမှာပဲ** သိမ်းထားတာ — ဖုန်းပြောင်းရင် ပြန်ရွေးရမယ်
- 📋 Copy က **English မူရင်းသာ** — GPT/Gem မှာ တိုက်ရိုက်သုံးလို့ရအောင်
- မြန်မာပြန်ဆိုချက် ၁၅၅၆ က Nyo Thazin Ko ရဲ့ ကိုယ်ပိုင်ဗားရှင်း (AI အကူအညီနဲ့)

---

*Made with 💛 for ညို — PROMPTURE Command Library v2.4*
