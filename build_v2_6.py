#!/usr/bin/env python3
"""Build PROMPTURE Command Library v2.6 from v2.5.4 index.html.

Adds 3 KANOTE tabs (SPEC / FLAT / BLUEPRINT, 100 commands each) as a pure
append: existing 2256 commands, order, and favorites indices are untouched.
Data swap happens inside the extracted script, then the script block is
swapped back into the page (single-file rebuild discipline).
Myanmar digits in the subtitle are built from unicode escapes, never typed.
"""
import json
import re
import sys

SRC = 'index.html'
FILES = [
    ('spec', 'kanote-spec-commands-100-with-mm.md'),
    ('flat', 'kanote-flat-commands-100-with-mm.md'),
    ('blueprint', 'kanote-blueprint-commands-100-with-mm.md'),
]
USER_FILES = '/home/hatch/workspace/user/files/'

MM_2256 = 'Command ' + ''.join(chr(c) for c in [0x1042, 0x1042, 0x1045, 0x1046])
MM_2556 = 'Command ' + ''.join(chr(c) for c in [0x1042, 0x1045, 0x1045, 0x1046])


def parse(path):
    text = open(path, encoding='utf-8').read()
    cats = []          # category names in file order
    entries = []       # (num, category, en, mm)
    cur = None
    lines = text.split('\n')
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
            mm_line = lines[i + 1] if i + 1 < len(lines) else ''
            mm = re.match(r'^   (.+)$', mm_line)
            assert mm, f'{path}:{num} missing MM line'
            entries.append((num, cur, en, mm.group(1)))
    nums = [e[0] for e in entries]
    assert nums == list(range(1, 101)), f'{path}: not sequential 1-100'
    assert len(entries) == 100, f'{path}: {len(entries)} entries'
    assert len(cats) == 8, f'{path}: {len(cats)} categories'
    for num, cat, en, mm in entries:
        assert '\u2028' not in en and '\u2029' not in en and '\u2028' not in mm and '\u2029' not in mm
    return cats, entries


def main():
    html = open(SRC, encoding='utf-8').read()
    m = re.search(r'<script>\n(.*?)\n</script>', html, re.S)
    assert m, 'script block not found'
    js = m.group(1)

    # Baseline checks
    old_cmds = re.search(r'COMMANDS = \[(.*?)\];\nconst CAT_ORDER', js, re.S).group(1)
    old_count = old_cmds.count('"collection"')
    assert old_count == 2256, f'baseline count {old_count}'
    assert 'v2.5.4' in html and 'mouse-event drag fallback' in js

    # Category collision check (exact string match against existing CAT_ORDER)
    old_cats = set(re.findall(r'"((?:[^"\\]|\\.)*)": \[', js))  # keys only, approx
    cat_order_body = re.search(r'CAT_ORDER = \{(.*?)\};\nconst COLL_NAME', js, re.S).group(1)
    existing_cats = set(re.findall(r'"([^"]+)"', cat_order_body))
    # existing_cats also includes collection keys; harmless for collision test
    new_entries_all = []
    cat_order_add = []
    collisions = []
    for coll, fname in FILES:
        cats, entries = parse(USER_FILES + fname)
        for c in cats:
            if c in existing_cats:
                collisions.append((coll, c))
        cat_order_add.append((coll, cats))
        for num, cat, en, mm in entries:
            new_entries_all.append({'collection': coll, 'category': cat,
                                    'num': num, 'text': en, 'mm': mm})
    print(f'parsed: {len(new_entries_all)} new entries')
    print(f'category collisions with existing tabs: {collisions}')

    # 1. Append to COMMANDS
    head, tail = js.split('];\nconst CAT_ORDER', 1)
    new_json = ', '.join(json.dumps(e, ensure_ascii=False) for e in new_entries_all)
    js = head + ', ' + new_json + '];\nconst CAT_ORDER' + tail

    # 2. CAT_ORDER: add 3 collections after kpstudio
    add = ', '.join(
        f'"{coll}": {json.dumps(cats, ensure_ascii=False)}'
        for coll, cats in cat_order_add)
    old_tail = '"]};\nconst COLL_NAME'
    assert old_tail in js
    js = js.replace(old_tail, '"], ' + add + '};\nconst COLL_NAME', 1)

    # 3. COLL_NAME: add 3 entries
    old_coll = "kpstudio:'📸 K+P Studio'}"
    assert old_coll in js
    js = js.replace(old_coll,
                    "kpstudio:'📸 K+P Studio', spec:'🪡 KANOTE SPEC', "
                    "flat:'🧵 KANOTE FLAT', blueprint:'🎨 KANOTE BLUEPRINT'}", 1)

    # 4. orderedCats: include new collections in all/fav view
    old_cols = "['prompture','studio','outfit','mobile','generator','kpstudio']"
    assert old_cols in js
    js = js.replace(old_cols,
                    "['prompture','studio','outfit','mobile','generator','kpstudio',"
                    "'spec','flat','blueprint']", 1)

    # 5. renderTabs: All count + 3 new buttons before fav
    assert "t.all+' (2256)</button>'" in js
    js = js.replace("t.all+' (2256)</button>'", "t.all+' (2556)</button>'", 1)
    fav_line = "'<button class=\"tab'+(coll==='fav'?' active':'')+'\" data-coll=\"fav\" id=\"favtab\">'"
    assert fav_line in js
    new_tabs = (
        "'<button class=\"tab'+(coll==='spec'?' active':'')+'\" data-coll=\"spec\">🪡 KANOTE SPEC (100)</button>'+\n    "
        "'<button class=\"tab'+(coll==='flat'?' active':'')+'\" data-coll=\"flat\">🧵 KANOTE FLAT (100)</button>'+\n    "
        "'<button class=\"tab'+(coll==='blueprint'?' active':'')+'\" data-coll=\"blueprint\">🎨 KANOTE BLUEPRINT (100)</button>'+\n    ")
    js = js.replace(fav_line, new_tabs + fav_line, 1)

    # 6. Subtitles
    assert "subtitle:'2256 commands" in js
    js = js.replace("subtitle:'2256 commands", "subtitle:'2556 commands", 1)
    assert MM_2256 in js
    js = js.replace(MM_2256, MM_2556, 1)

    # Swap script block back into the page
    html = html[:m.start(1)] + js + html[m.end(1):]

    # 7. Static HTML: tabs block, subtitle div, footer
    assert '🌟 အားလုံး (2256)' in html
    html = html.replace('🌟 အားလုံး (2256)', '🌟 အားလုံး (2556)', 1)
    fav_static = '<button class="tab" data-coll="fav" id="favtab">'
    assert fav_static in html
    static_tabs = (
        '    <button class="tab" data-coll="spec">🪡 KANOTE SPEC (100)</button>\n'
        '    <button class="tab" data-coll="flat">🧵 KANOTE FLAT (100)</button>\n'
        '    <button class="tab" data-coll="blueprint">🎨 KANOTE BLUEPRINT (100)</button>\n')
    html = html.replace(fav_static, static_tabs + fav_static, 1)
    assert MM_2256 in html
    html = html.replace(MM_2256, MM_2556, 1)
    assert 'PROMPTURE Command Library v2.5.4 · 2256 commands' in html
    html = html.replace('PROMPTURE Command Library v2.5.4 · 2256 commands',
                        'PROMPTURE Command Library v2.6 · 2556 commands', 1)

    open(SRC, 'w', encoding='utf-8').write(html)
    print('wrote', SRC)


if __name__ == '__main__':
    main()
