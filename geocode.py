#!/usr/bin/env python3
"""
Täidab data.js-is puuduvad koordinaadid (lat/lng = null) OpenStreetMapi Nominatimiga
ja kirjutab need faili püsivalt, nii et leht ei pea neid enam brauseris otsima.

Kasutus (oma arvutis, internetiühendusega):
    python3 geocode.py

Nominatimi reegel: max 1 päring sekundis. Tulemus kontrollitakse Tartu piirikasti vastu.
Vaata tulemus üle (nt openstreetmap.org-is), enne kui commit'id.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BOX = dict(s=58.28, n=58.46, w=26.55, e=26.90)
UA = "tartu-ringmajandus-kaart/1.0 (GitHub Pages projekt)"
PATH = "data.js"

src = open(PATH, encoding="utf-8").read()
m = re.match(r"\s*window\.POINTS\s*=\s*(\[.*\])\s*;\s*$", src, re.S)
if not m:
    sys.exit("data.js formaat ei sobi")
points = json.loads(m.group(1))


def geocode(address):
    q = re.sub(r"\s*\(.*?\)\s*", " ", address).strip() + ", Tartu"
    params = urllib.parse.urlencode({
        "format": "jsonv2", "limit": 3, "countrycodes": "ee", "accept-language": "et",
        "viewbox": f"{BOX['w']},{BOX['n']},{BOX['e']},{BOX['s']}", "bounded": 1, "q": q,
    })
    req = urllib.request.Request("https://nominatim.openstreetmap.org/search?" + params,
                                 headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        for hit in json.load(r):
            lat, lng = float(hit["lat"]), float(hit["lon"])
            if BOX["s"] <= lat <= BOX["n"] and BOX["w"] <= lng <= BOX["e"]:
                return lat, lng, hit.get("display_name", "")
    return None


changed = 0
for p in points:
    if p.get("lat") is not None:
        continue
    try:
        res = geocode(p["address"])
    except Exception as exc:
        print(f"VIGA  {p['name']}: {exc}")
        continue
    if res:
        p["lat"], p["lng"] = round(res[0], 6), round(res[1], 6)
        changed += 1
        print(f"OK    {p['name']}: {p['lat']}, {p['lng']}  ({res[2]})")
    else:
        print(f"PUUDUB {p['name']}: {p['address']}")
    time.sleep(1.1)

if changed:
    with open(PATH, "w", encoding="utf-8") as f:
        f.write("window.POINTS = " + json.dumps(points, ensure_ascii=False, indent=2) + ";\n")
    print(f"Kirjutasin {changed} koordinaati faili {PATH}")
else:
    print("Midagi ei muutunud")
