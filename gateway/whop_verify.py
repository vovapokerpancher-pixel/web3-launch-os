import json, os, urllib.request, urllib.error, re

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"


def call(m, p, d=None):
    b = json.dumps(d).encode() if d is not None else None
    r = urllib.request.Request(BASE + p, data=b, headers={
        "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json",
        "Api-Version-Date": "2026-07-01",
    }, method=m)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


st, b = call("GET", "/products")
data = b.get("data", b if isinstance(b, list) else [])
mine = []
other = []
if isinstance(data, list):
    for p in data:
        t = (p.get("title") or "").strip().lower()
        if "web3 launch os" in t:
            mine.append({"id": p.get("id"), "title": p.get("title"), "route": p.get("route"),
                         "created_at": p.get("created_at"), "marketplace": p.get("marketplace_status"),
                         "visibility": p.get("visibility")})
        else:
            other.append(p.get("id"))
with open("web3_ids.json", "w", encoding="utf-8") as fh:
    json.dump({"mine": mine, "other_count": len(other), "other_ids": other}, fh, ensure_ascii=False, indent=2)
print("Web3 Launch OS products:", len(mine))
for m in mine:
    print(m["id"], m["route"], m["created_at"][:19], m["marketplace"])
print("other count", len(other))
