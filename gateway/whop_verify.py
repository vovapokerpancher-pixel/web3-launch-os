import json, os, urllib.request, urllib.error, sys

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


# 1) find the product by route
st, b = call("GET", "/products")
data = b.get("data", b if isinstance(b, list) else [])
target = None
if isinstance(data, list):
    for p in data:
        if (p.get("route") or "").startswith("web3-launch-os") or "web3" in (p.get("title") or "").lower():
            target = p
            break
print("found product:", (target or {}).get("id"), (target or {}).get("route") or "NONE")
if not target:
    # fallback: probe IDs we know
    for pid in ["prod_vCCczg2JZfudM", "prod_7RSQOQ0t6iwDo"]:
        s, bod = call("GET", "/products/" + pid)
        if s == 200:
            print("known product:", bod.get("id"), bod.get("route"))
    raise SystemExit

pid = target["id"]
print("product id:", pid, "route:", target.get("route"))

# 2) fetch product detail (apps/experience list if present)
st2, bod2 = call("GET", "/products/" + pid)
print("detail keys:", list((bod2 or {}).keys()))
print("visibility:", (bod2 or {}).get("visibility"), "marketplace:", (bod2 or {}).get("marketplace_status"))
print("default_plan:", (bod2 or {}).get("default_plan"))
