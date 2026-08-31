import json, os, urllib.request, urllib.error

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
rows = []
if isinstance(data, list):
    for p in data:
        rows.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "created_at": p.get("created_at"),
            "visibility": p.get("visibility"),
            "plan": (p.get("default_plan") or {}).get("id"),
            "marketplace": p.get("marketplace_status"),
        })
with open("products_dump.json", "w", encoding="utf-8") as fh:
    json.dump({"count": len(rows) if isinstance(data, list) else None, "products": rows}, fh, ensure_ascii=False, indent=2)
print("dumped", len(rows), "rows to products_dump.json")
