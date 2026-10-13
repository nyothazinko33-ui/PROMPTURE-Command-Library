#!/usr/bin/env python3
"""Build PROMPTURE Command Library v2.4 single-file app (1556 commands, data update + fav migration)."""
import re, json, pathlib, io, base64, zipfile

HOME = pathlib.Path.home()
WS = HOME / 'workspace/prompture-command-library'
UPD = pathlib.Path('/tmp/data_update')

def parse_file(path, is_mm=False):
    t = pathlib.Path(path).read_text(encoding='utf-8')
    cmds = []
    cur = None
    for line in t.split('\n'):
        mh = re.match(r'^##\s+(.+?)\s*$', line)
        if mh:
            cur = re.sub(r'\s*\([^()]*\)\s*$', '', mh.group(1).strip()).strip()
            continue
        m = re.match(r'^(?:>\s*)?(\d{1,3})\.\s+(.*\S)\s*$', line)
        if m:
            cmds.append({'category': cur, 'num': int(m.group(1)),
                         'text': m.group(2).strip().replace('\\+', '+').replace('\\=', '=')})
        elif cmds and line.strip().startswith('>') and line.strip('> ').strip():
            cmds[-1]['text'] += ' ' + line.strip('> ').strip()
    return cmds

def find(pat):
    ms = [f for f in UPD.iterdir() if pat in f.name and f.suffix == '.md']
    assert len(ms) == 1, f"pattern {pat}: {ms}"
    return ms[0]

cmds = []
# PROMPTURE 220 (new EN + her MM)
en220 = parse_file(find('PROMPTURE_command_prompts__220_.md'))
mm220 = parse_file(find('220_#U1019'))
assert len(en220) == 220 and len(mm220) == 220
mm220_by = {c['num']: c['text'] for c in mm220}
for c in en220:
    cmds.append({'collection': 'prompture', 'category': c['category'], 'num': c['num'],
                 'text': c['text'], 'mm': mm220_by[c['num']]})
# STUDIO 890 (new EN + her MM V2)
en890 = parse_file(find('PROMPTURE_STUDIO_command_prompts__890_.md'))
mm890 = parse_file(find('890_#U1019'))
assert len(en890) == 890 and len(mm890) == 890
mm890_by = {c['num']: c['text'] for c in mm890}
for c in en890:
    cmds.append({'collection': 'studio', 'category': c['category'], 'num': c['num'],
                 'text': c['text'], 'mm': mm890_by[c['num']]})
# Outfit 400 (existing + translations_her)
otext = (HOME / 'workspace/user/files/PROMPTURE_STUDIO_outfit_revisions__400.md').read_text(encoding='utf-8')
cur = None
for line in otext.splitlines():
    mh = re.match(r'^##\s+(.+?)\s*$', line)
    if mh:
        cur = re.sub(r'\s*\([^()]*\)\s*$', '', mh.group(1).strip()).strip()
        continue
    m = re.match(r'^(\d+)\.\s+(.*\S)\s*$', line)
    if m:
        cmds.append({'collection': 'outfit', 'category': cur, 'num': int(m.group(1)), 'text': m.group(2).strip()})
tr = json.loads((WS / 'translations_her.json').read_text(encoding='utf-8'))
for c in cmds:
    if c['collection'] == 'outfit':
        c['mm'] = tr.get(f"outfit:{c['num']}", '')
# Mobile 46 (from casual mobile .md)
mb = (HOME / 'workspace/user/files/PROMPTURE_Casual_Mobile_Camera_Bank_COMMAND_Eng___Mm.md').read_text(encoding='utf-8')
titles = [m.start() for m in re.finditer(r'Casual Mobile Camera — Command Bank \(46\)', mb)]

def parse_text(t):
    out = []
    cur = None
    for line in t.split('\n'):
        mh = re.match(r'^##\s+(.+?)\s*$', line)
        if mh:
            cur = re.sub(r'\s*\([^()]*\)\s*$', '', mh.group(1).strip()).strip()
            continue
        m = re.match(r'^(?:>\s*)?(\d{1,2})\.\s+(.*\S)\s*$', line)
        if m and cur != '📱':
            out.append({'category': cur, 'num': int(m.group(1)),
                        'text': m.group(2).strip().replace('\\+', '+').replace('\\=', '=')})
        elif out and line.strip().startswith('>') and line.strip('> ').strip():
            out[-1]['text'] += ' ' + line.strip('> ').strip()
    return out

en_mob = parse_text(mb[titles[0]:titles[1]])
mm_mob = parse_text(mb[titles[1]:])
assert len(en_mob) == 46 and len(mm_mob) == 46
mm_mob_by = {c['num']: c['text'] for c in mm_mob}
for c in en_mob:
    cmds.append({'collection': 'mobile', 'category': c['category'], 'num': c['num'],
                 'text': c['text'], 'mm': mm_mob_by[c['num']]})
print("commands:", len(cmds))
assert len(cmds) == 1556

cat_order = {}
for c in cmds:
    cat_order.setdefault(c['collection'], [])
    if c['category'] not in cat_order[c['collection']]:
        cat_order[c['collection']].append(c['category'])
print("cats:", {k: len(v) for k, v in cat_order.items()})

# ---------- favorites migration map (old v2.3 index -> new v2.4 index) ----------
# old layout: prompture 0-199, studio 200-999, outfit 1000-1399, mobile 1400-1445
# new layout: prompture 0-219, studio 220-1109, outfit 1110-1509, mobile 1510-1555
old_cur = json.loads(re.search(r'const COMMANDS = (\[.*?\]);',
    pathlib.Path('/tmp/v23/index.html').read_text(encoding='utf-8'), re.S).group(1))
def norm(t): return re.sub(r'\s+', ' ', t.replace('\\+', '+').replace('\\=', '=')).strip()
new_by_text = {}
for i, c in enumerate(cmds):
    new_by_text.setdefault((c['collection'], norm(c['text'])), i)
moved_map = {}
for i, c in enumerate(old_cur):
    if c['collection'] == 'prompture' and 141 <= c['num'] <= 200:
        ni = new_by_text.get(('prompture', norm(c['text'])))
        assert ni is not None, f"unmapped old prompture #{c['num']}"
        moved_map[i] = ni
print("moved fav mappings:", len(moved_map))
mig_js = json.dumps(moved_map)

# ---------- logo ----------
from PIL import Image
src = HOME / 'workspace/user/media_library/image/75/75fdf2316aca005765273db9b6bc511d6f804bb586bc7e876c6b2db20156ab28.png'
im = Image.open(src)
h = im.copy(); h.thumbnail((256, 256), Image.LANCZOS)
buf = io.BytesIO(); h.convert('RGB').save(buf, 'JPEG', quality=82)
b64h = base64.b64encode(buf.getvalue()).decode()
w, hh = im.size
crop = im.crop((int(w*0.20), int(hh*0.12), int(w*0.80), int(hh*0.72)))
crop.thumbnail((64, 64), Image.LANCZOS)
buf2 = io.BytesIO(); crop.convert('RGB').save(buf2, 'PNG')
b64f = base64.b64encode(buf2.getvalue()).decode()

commands_json = json.dumps(cmds, ensure_ascii=False).replace('</', '<\\/')
catorder_json = json.dumps(cat_order, ensure_ascii=False)

# ---------- template ----------
tpl = open('/tmp/tpl_v23.txt', encoding='utf-8').read()

# counts & labels
tpl = tpl.replace('Command ၁၄၄၆ —', 'Command ၁၅၅၆ —')
tpl = tpl.replace('1446 commands —', '1556 commands —')
tpl = tpl.replace('🌟 အားလုံး (1446)', '🌟 အားလုံး (1556)')
tpl = tpl.replace('📝 PROMPTURE (200)', '📝 PROMPTURE (220)')
tpl = tpl.replace('🎨 STUDIO (800)', '🎨 STUDIO (890)')
tpl = tpl.replace("'+t.all+' (1446)", "'+t.all+' (1556)")
tpl = tpl.replace('>📝 PROMPTURE (200)<', '>📝 PROMPTURE (220)<')
tpl = tpl.replace('>🎨 STUDIO (800)<', '>🎨 STUDIO (890)<')
tpl = tpl.replace('PROMPTURE Command Library v2.3 · 1446 commands', 'PROMPTURE Command Library v2.4 · 1556 commands')

# favorites: v2 -> v3 with one-time migration
old_fav_load = "let favs=[]; try{ favs=JSON.parse(localStorage.getItem('prompture_cmd_favs_v2')||'[]'); }catch(e){ favs=[]; }"
new_fav_load = """const FAV_MOVED=__MOVED_MAP__;
function migrateFavs(old){ const m={}; for(let i=0;i<140;i++) m[i]=i;
  for(const k in FAV_MOVED) m[k]=FAV_MOVED[k];
  for(let i=200;i<1000;i++) m[i]=i+20; for(let i=1000;i<1400;i++) m[i]=i+110; for(let i=1400;i<1446;i++) m[i]=i+110;
  const out=[]; old.forEach(i=>{ if(m[i]!==undefined && out.indexOf(m[i])<0) out.push(m[i]); }); return out; }
let favs=[]; try{ const v3=localStorage.getItem('prompture_cmd_favs_v3');
  if(v3!==null){ favs=JSON.parse(v3); }
  else { favs=migrateFavs(JSON.parse(localStorage.getItem('prompture_cmd_favs_v2')||'[]'));
    try{ localStorage.setItem('prompture_cmd_favs_v3', JSON.stringify(favs)); }catch(e){} }
}catch(e){ favs=[]; }""".replace('__MOVED_MAP__', mig_js)
assert old_fav_load in tpl, "fav load pattern not found"
tpl = tpl.replace(old_fav_load, new_fav_load)
tpl = tpl.replace("localStorage.setItem('prompture_cmd_favs_v2'", "localStorage.setItem('prompture_cmd_favs_v3'")

html = tpl.replace('__COMMANDS__', commands_json)
html = html.replace('__CATORDER__', catorder_json)
html = html.replace('__LOGO__', b64h)
html = html.replace('__FAVICON__', b64f)
out = WS / 'index.html'
out.write_text(html, encoding='utf-8')
print("wrote", out.stat().st_size, "bytes")

zip_path = HOME / 'workspace/your_files/prompture-command-library-v2.4.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(out, 'index.html')
    z.write(WS / 'build_v2_4.py', 'build_v2_4.py')
print("zip:", zip_path, zip_path.stat().st_size, "bytes")
