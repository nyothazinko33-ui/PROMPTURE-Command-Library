#!/usr/bin/env python3
"""Build PROMPTURE Command Library v2.7 from v2.6 index.html.

Replaces the STUDIO collection (890) with the QA-fixed MASTER 1960 file
(1960 commands, MASTER numbering, her latest MM + 9 QA fixes).
Other collections keep their entries and relative order; the studio block
grows in place, so every collection after it shifts +1070.
Favorites migrate one-time v3 -> v4 (same pattern as v2.4):
  prompture 0-219 identity; studio by text match to MASTER number;
  all later collections +1070.
Myanmar digits in subtitles are built from unicode escapes, never typed.
"""
import json
import re

SRC = 'index.html'
MASTER = '/home/hatch/workspace/your_files/PROMPTURE_STUDIO_command_prompts__MASTER_1960_with-mm_QA-fixed_.md'

MM_2556 = 'Command ' + ''.join(chr(c) for c in [0x1042, 0x1045, 0x1045, 0x1046])
MM_3626 = 'Command ' + ''.join(chr(c) for c in [0x1043, 0x1046, 0x1042, 0x1046])


def parse_master(path):
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    cats = []
    entries = []
    cur = None
    for i, line in enumerate(lines):
        m = re.match(r'^## (.+?) \(\d+–\d+\)$', line)
        if m:
            cur = m.group(1)
            cats.append(cur)
            continue
        m = re.match(r'^(\d+)\. (.+)$', line)
        if m:
            num = int(m.group(1))
            en = m.group(2)
            mm = re.match(r'^   (.+)$', lines[i + 1])
            assert mm, f'{path}:{num} missing MM line'
            assert '</script' not in en and '</script' not in mm.group(1)
            entries.append({'collection': 'studio', 'category': cur,
                            'num': num, 'text': en, 'mm': mm.group(1)})
    nums = [e['num'] for e in entries]
    assert nums == list(range(1, 1961)), 'master not sequential 1-1960'
    assert len(cats) == 14, f'{len(cats)} categories'
    return cats, entries


def main():
    html = open(SRC, encoding='utf-8').read()
    m = re.search(r'<script>\n(.*?)\n</script>', html, re.S)
    assert m, 'script block not found'
    js = m.group(1)

    # Baseline: v2.6, 2556 commands
    assert 'PROMPTURE Command Library v2.6' in html
    assert 'mouse-event drag fallback' in js
    old_cmds = json.loads(re.search(r'COMMANDS = (\[.*?\]);\nconst CAT_ORDER',
                                    js, re.S).group(1))
    assert len(old_cmds) == 2556, f'baseline {len(old_cmds)}'
    old_studio = old_cmds[220:1110]
    assert len(old_studio) == 890
    assert all(c['collection'] == 'studio' for c in old_studio)
    assert [c['collection'] for c in old_cmds[1110:]] != ['studio'] * 1446

    # New studio data from QA-fixed MASTER
    cats, new_studio = parse_master(MASTER)
    co = json.loads(re.search(r'CAT_ORDER = (\{.*?\});\nconst COLL_NAME',
                              js, re.S).group(1))
    assert co['studio'] == cats, f'CAT_ORDER studio mismatch: {co["studio"]} vs {cats}'
    print('studio categories match CAT_ORDER: OK')

    # Migration map: old studio index -> MASTER number (by exact text)
    by_text = {}
    for e in new_studio:
        assert e['text'] not in by_text, 'dup text in master: ' + e['text'][:60]
        by_text[e['text']] = e['num']
    fav_studio_v4 = []
    for c in old_studio:
        assert c['text'] in by_text, 'old studio text missing in master: ' + c['text'][:60]
        fav_studio_v4.append(by_text[c['text']])
    assert len(set(fav_studio_v4)) == 890, 'migration map not unique'
    print('migration map: 890/890 old studio entries matched by text')

    # New COMMANDS: prompture + new studio + everything after studio
    new_cmds = old_cmds[:220] + new_studio + old_cmds[1110:]
    assert len(new_cmds) == 3626, len(new_cmds)
    assert new_cmds[:220] == old_cmds[:220]
    assert new_cmds[2180:] == old_cmds[1110:]

    # 1. Replace COMMANDS array
    start = js.find('COMMANDS = [')
    end_marker = '];\nconst CAT_ORDER'
    end = js.find(end_marker, start)
    assert start >= 0 and end > start
    new_json = 'COMMANDS = [' + ', '.join(
        json.dumps(e, ensure_ascii=False) for e in new_cmds)  # js[end:] supplies the closing '];'
    js = js[:start] + new_json + js[end:]

    # 2. Insert v4 migration (before migrateFavs)
    mig = ('const FAV_STUDIO_V4=' + json.dumps(fav_studio_v4) + ';\n'
           'function migrateFavsV4(old){ const m={}; for(let i=0;i<220;i++) m[i]=i;\n'
           '  for(let i=0;i<890;i++) m[220+i]=219+FAV_STUDIO_V4[i];\n'
           '  for(let i=1110;i<2556;i++) m[i]=i+1070;\n'
           '  const out=[]; old.forEach(i=>{ if(m[i]!==undefined && out.indexOf(m[i])<0) out.push(m[i]); }); return out; }\n')
    anchor = 'function migrateFavs(old)'
    assert anchor in js
    js = js.replace(anchor, mig + anchor, 1)

    # 3. Load logic: v4, falling back to v3 (via v4 migration) then v2 chain
    old_load = ("let favs=[]; try{ const v3=localStorage.getItem('prompture_cmd_favs_v3');\n"
                "  if(v3!==null){ favs=JSON.parse(v3); }\n"
                "  else { favs=migrateFavs(JSON.parse(localStorage.getItem('prompture_cmd_favs_v2')||'[]'));\n"
                "    try{ localStorage.setItem('prompture_cmd_favs_v3', JSON.stringify(favs)); }catch(e){} }\n"
                "}catch(e){ favs=[]; }")
    new_load = ("let favs=[]; try{ const v4=localStorage.getItem('prompture_cmd_favs_v4');\n"
                "  if(v4!==null){ favs=JSON.parse(v4); }\n"
                "  else { const v3=localStorage.getItem('prompture_cmd_favs_v3');\n"
                "    if(v3!==null){ favs=migrateFavsV4(JSON.parse(v3)); }\n"
                "    else { favs=migrateFavsV4(migrateFavs(JSON.parse(localStorage.getItem('prompture_cmd_favs_v2')||'[]'))); }\n"
                "    try{ localStorage.setItem('prompture_cmd_favs_v4', JSON.stringify(favs)); }catch(e){} }\n"
                "}catch(e){ favs=[]; }")
    assert old_load in js, 'load block not found'
    js = js.replace(old_load, new_load, 1)

    # 4. saveFavs writes v4
    old_save = "function saveFavs(){ localStorage.setItem('prompture_cmd_favs_v3'"
    assert old_save in js
    js = js.replace(old_save,
                    "function saveFavs(){ localStorage.setItem('prompture_cmd_favs_v4'", 1)

    # 5. renderTabs counts
    assert "t.all+' (2556)</button>'" in js
    js = js.replace("t.all+' (2556)</button>'", "t.all+' (3626)</button>'", 1)
    assert "'\" data-coll=\"studio\">🎨 STUDIO (890)</button>'" in js
    js = js.replace("🎨 STUDIO (890)</button>'", "🎨 STUDIO (1960)</button>'", 1)

    # 6. Subtitles
    assert "subtitle:'2556 commands" in js
    js = js.replace("subtitle:'2556 commands", "subtitle:'3626 commands", 1)
    assert MM_2556 in js
    js = js.replace(MM_2556, MM_3626, 1)

    # Swap script block back
    html = html[:m.start(1)] + js + html[m.end(1):]

    # 7. Static HTML: tabs, subtitle, footer
    assert '🌟 အားလုံး (2556)' in html
    html = html.replace('🌟 အားလုံး (2556)', '🌟 အားလုံး (3626)', 1)
    assert '🎨 STUDIO (890)' in html
    html = html.replace('🎨 STUDIO (890)', '🎨 STUDIO (1960)', 1)
    assert MM_2556 in html
    html = html.replace(MM_2556, MM_3626, 1)
    assert 'PROMPTURE Command Library v2.6 · 2556 commands' in html
    html = html.replace('PROMPTURE Command Library v2.6 · 2556 commands',
                        'PROMPTURE Command Library v2.7 · 3626 commands', 1)

    open(SRC, 'w', encoding='utf-8').write(html)
    print('wrote', SRC)


if __name__ == '__main__':
    main()
