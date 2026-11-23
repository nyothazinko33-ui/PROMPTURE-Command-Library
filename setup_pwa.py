#!/usr/bin/env python3
"""Setup PWA (Progressive Web App) for PROMPTURE Command Library.

1. Backs up index.html -> index.html.before_pwa_bak
2. Generates TRUE-SIZE icons from the original 1254x1254 logo
   (icon-512.png, icon-192.png, icon-180.png) with PIL.
   NEVER uses the embedded 64x64 favicon as app icons — that was the
   v2.9 bug: both icon files were the same 64x64 JPEG, so the PWA
   install prompt failed and the home-screen icon was blurry.
   If the logo file is missing, existing icon files are left untouched.
3. Generates manifest.json (standalone, gold/black theme)
4. Generates sw.js (Service Worker with smart Network-First offline cache)
5. Patches index.html to link manifest, meta tags, and register sw.js
"""
import json
import os
import re
import shutil

HTML_FILE = 'index.html'
BACKUP_FILE = 'index.html.before_pwa_bak'
# Original gold book-and-quill logo (1254x1254 PNG). Keep this file next to
# the script, or edit the path below to where you keep it.
LOGO_FILE = 'logo-original-1254.png'

ICON_SIZES = (512, 192, 180)


def build_icons():
    """Generate true-size PNG icons from the original logo.

    Returns True when icons were written, False when skipped (logo missing).
    """
    if not os.path.exists(LOGO_FILE):
        print(f'[WARN] Logo not found ({LOGO_FILE}) — keeping existing icon files untouched.')
        print('[WARN] Do NOT use the embedded 64x64 favicon as app icons.')
        return False
    try:
        from PIL import Image
    except ImportError:
        print('[WARN] Pillow (PIL) is not installed — run: pip install pillow')
        print('[WARN] Keeping existing icon files untouched.')
        return False
    im = Image.open(LOGO_FILE)
    if im.mode == 'P':
        im = im.convert('RGBA')
    for size in ICON_SIZES:
        r = im.resize((size, size), Image.LANCZOS)
        r.save(f'icon-{size}.png', format='PNG', optimize=True)
        print(f'[OK] Generated icon-{size}.png ({size}x{size} PNG)')
    return True


def main():
    shutil.copy2(HTML_FILE, BACKUP_FILE)
    html = open(HTML_FILE, encoding='utf-8').read()

    # 1. True-size icons from the original logo (never the 64x64 favicon)
    build_icons()

    # 2. Generate manifest.json
    manifest = {
        "name": "PROMPTURE Command Library",
        "short_name": "PROMPTURE",
        "description": "PROMPTURE Command Library v2.9 · 4626 Commands",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#0f0e0c",
        "theme_color": "#d4af37",
        "orientation": "any",
        "icons": [
            {
                "src": "icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }
    open('manifest.json', 'w', encoding='utf-8').write(json.dumps(manifest, indent=2, ensure_ascii=False))
    print('[OK] Created manifest.json')

    # 3. Generate sw.js (Smart Network-First Service Worker)
    sw_code = """const CACHE_NAME = 'prompture-pwa-v2_9';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-180.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((k) => {
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      )
    )
  );
  self.clients.claim();
});

// Network-first with cache fallback (works 100% offline and auto-updates online)
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        const resClone = res.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
"""
    open('sw.js', 'w', encoding='utf-8').write(sw_code)
    print('[OK] Created sw.js (Service Worker)')

    # 4. Patch index.html
    # Insert manifest & meta tags in <head>
    head_tags = (
        '\n<link rel="manifest" href="manifest.json">\n'
        '<meta name="theme-color" content="#d4af37">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
        '<meta name="apple-mobile-web-app-title" content="PROMPTURE">\n'
        '<link rel="apple-touch-icon" href="icon-180.png">\n'
    )
    if '<link rel="manifest"' not in html:
        html = html.replace('<title>PROMPTURE Command Library</title>', '<title>PROMPTURE Command Library</title>' + head_tags, 1)

    # Insert Service Worker registration before closing </script>
    sw_register = """
// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  });
}
"""
    if 'navigator.serviceWorker' not in html:
        html = html.replace('applyTheme(); applyLang(); saveFavs();', 'applyTheme(); applyLang(); saveFavs();\n' + sw_register, 1)

    open(HTML_FILE, 'w', encoding='utf-8').write(html)
    print(f'[SUCCESS] PWA fully configured! (Backup at {BACKUP_FILE})')


if __name__ == '__main__':
    main()
