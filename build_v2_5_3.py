#!/usr/bin/env python3
"""Build PROMPTURE Command Library v2.5.3: replace K+P tab data with emoji-MM versions."""
import re, json, pathlib, zipfile

HOME = pathlib.Path.home()
WS = HOME / 'workspace/prompture-command-library'

def parse_kp(path, coll):
    t = pathlib.Path(path).read_text(encoding='utf-8')
    cmds = []
    cur = None
    lines = t.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        mh = re.match(r'^##\s+(.+?)\s*$', line)
        if mh:
            cur = re.sub(r'\s*\([^()]*\)\s*$', '', mh.group(1).strip()).strip()
            i += 1
            continue
        m = re.match(r'^(\d{1,3})\.\s+(\S.*?)\s*$', line)
        if m:
            en = re.sub(r'\*\*', '', m.group(2)).strip()
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            mm = lines[j].strip() if j < len(lines) else ''
            cmds.append({'collection': coll, 'category': cur, 'num': int(m.group(1)),
                         'text': en, 'mm': mm})
            i = j + 1
            continue
        i += 1
    return cmds

gen = parse_kp(HOME / 'workspace/user/files/hybrid-kp-prompt-generator-commands-200-with-mm-emoji_3_d2aq.md', 'generator')
stu = parse_kp(HOME / 'workspace/user/files/hybrid-kp-studio-commands-500-with-mm-emoji_4_ppbx.md', 'kpstudio')
assert len(gen) == 200 and len(stu) == 500
assert all(c['mm'].strip() for c in gen + stu)

html = (WS / 'index.html').read_text(encoding='utf-8')
script = re.search(r'<script>\n(.*?)\n</script>', html, re.S).group(1)
i = script.index('const COMMANDS = [')
j = script.index('const CAT_ORDER', i)
old_cmds = json.loads(script[i:j].split('=',1)[1].strip().rstrip(';').rstrip())
assert len(old_cmds) == 2256
base = [c for c in old_cmds if c['collection'] not in ('generator', 'kpstudio')]
assert len(base) == 1556
# verify EN + categories + order identical (only MM emoji added)
def norm(t): return re.sub(r'\s+', ' ', t).strip()
old_kp = [c for c in old_cmds if c['collection'] in ('generator', 'kpstudio')]
new_kp = gen + stu
assert len(old_kp) == len(new_kp) == 700
for o, n in zip(old_kp, new_kp):
    assert o['collection'] == n['collection'] and o['num'] == n['num'], (o, n)
    assert norm(o['text']) == norm(n['text']), f"EN changed: {o['num']}"
    assert o['category'] == n['category'], f"cat changed: {o['num']}"
cmds = base + new_kp
assert len(cmds) == 2256
# indices of old 1556 unchanged by construction
assert cmds[:1556] == base

commands_json = json.dumps(cmds, ensure_ascii=False).replace('</', '<\\/')
cat_order = json.loads(re.search(r'const CAT_ORDER = (\{.*?\});', script, re.S).group(1))
catorder_json = json.dumps(cat_order, ensure_ascii=False)

# swap data INSIDE script, then swap script block back
script = re.sub(r'const COMMANDS = \[.*?\];\nconst CAT_ORDER = \{.*?\};',
                lambda m: f'const COMMANDS = {commands_json};\nconst CAT_ORDER = {catorder_json};',
                script, count=1, flags=re.S)
html2 = re.sub(r'<script>\n.*?\n</script>',
                lambda m: '<script>\n' + script + '\n</script>',
                html, count=1, flags=re.S)
html2 = html2.replace('PROMPTURE Command Library v2.5.2 \u00b7 2256 commands', 'PROMPTURE Command Library v2.5.3 \u00b7 2256 commands')
assert 'v2.5.3' in html2
out = WS / 'index.html'
out.write_text(html2, encoding='utf-8')
print("wrote", out.stat().st_size, "bytes")

zip_path = HOME / 'workspace/your_files/prompture-command-library-v2.5.3.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(out, 'index.html')
    z.write(WS / 'build_v2_5_3.py', 'build_v2_5_3.py')
print("zip:", zip_path, zip_path.stat().st_size, "bytes")
