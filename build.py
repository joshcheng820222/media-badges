#!/usr/bin/env python3
"""Build cleaned, self-hosted badges JSON from the two source configs."""
import json, re, os

RAW_BASE = "https://raw.githubusercontent.com/joshcheng820222/media-badges/refs/heads/master/icons"
ZW = re.compile(r'[​‌‍⁠⁣⁤]')

def clean(d, icon_map, fix_60fps=False):
    out_groups = d.get('groups', [])
    filters = []
    for x in d.get('filters', []):
        x = dict(x)
        # strip zero-width steganographic IDs from patterns
        x['pattern'] = ZW.sub('', x['pattern'])
        # collapse leftover empty alternation artifacts like |) -> )
        x['pattern'] = re.sub(r'\|\)', ')', x['pattern'])
        # rewrite icon URL to self-hosted
        u = x.get('imageURL', '')
        if u and u in icon_map:
            x['imageURL'] = f"{RAW_BASE}/{icon_map[u]}"
        # drop disabled filters
        if not x.get('isEnabled', True):
            continue
        if fix_60fps and x['id'] == 'b-xui3zm':
            x['pattern'] = r'(?i)(?<![0-9])(?:59\.94|60(?:\.0+)?)[ ._-]*(?:fps|hz)(?![A-Za-z0-9])'
        filters.append(x)
    return {'groups': out_groups, 'filters': filters}

icon_map = json.load(open('icon-map.json'))
sb = clean(json.load(open('sb.json')), icon_map)
xp = clean(json.load(open('xp.json')), icon_map, fix_60fps=True)
json.dump(sb, open('streambridge-badges.json', 'w'), ensure_ascii=False, indent=1)
json.dump(xp, open('xperience-badges.json', 'w'), ensure_ascii=False, indent=1)

# merged: xperience groups + streambridge groups (prefix ids to avoid collisions)
GMAP_SB = {g['id']: f"sb-{g['id']}" for g in sb['groups']}
merged_groups = [dict(g, id=g['id']) for g in xp['groups']]
for g in sb['groups']:
    merged_groups.append(dict(g, id=GMAP_SB[g['id']]))
merged_filters = [dict(f, id=f"xp-{f['id']}") for f in xp['filters']]
for f in sb['filters']:
    merged_filters.append(dict(f, id=f"sb-{f['id']}", groupId=GMAP_SB.get(f['groupId'], f['groupId'])))
merged = {'groups': merged_groups, 'filters': merged_filters}
json.dump(merged, open('badges.json', 'w'), ensure_ascii=False, indent=1)

for name, d in (('streambridge-badges.json', sb), ('xperience-badges.json', xp), ('badges.json', merged)):
    # validate all patterns compile
    bad = []
    for f in d['filters']:
        try:
            re.compile(f['pattern'])
        except re.error as e:
            bad.append((f['id'], str(e)))
    missing = [f['id'] for f in d['filters']
               if f.get('imageURL','').startswith(RAW_BASE)
               and not os.path.exists('icons/' + f['imageURL'].rsplit('/',1)[1])]
    print(f"{name}: {len(d['groups'])} groups, {len(d['filters'])} filters, bad-regex={len(bad)}, missing-icons={len(missing)}")
    for b in bad[:10]: print('  BAD:', b)
