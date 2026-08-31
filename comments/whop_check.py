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


pid = "prod_0WrqduKEM3TWZ"
st, b = call("GET", "/products/" + pid)
print("title:", b.get("title"), "| route:", b.get("route"), "| vis:", b.get("visibility"), "| mkt:", b.get("marketplace_status"))
dp = b.get("default_plan") or {}
print("plan:", dp.get("title"), dp.get("plan_type"), dp.get("initial_price", {}).get("amount"), "currency", dp.get("initial_price", {}).get("currency"))
print("gallery_images:", len(b.get("gallery_images") or []))
for g in (b.get("gallery_images") or []):
    print("  gallery:", g.get("url"))
