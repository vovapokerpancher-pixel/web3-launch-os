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
for p in (data if isinstance(data, list) else []):
    if (p.get("route") or "").startswith("web3-launch-os"):
        print("found:", p.get("id"), "| route:", p.get("route"), "| title:", p.get("title"))
        print("  keys:", list(p.keys()))
        # type/kind if present
        for k in ("type", "kind", "product_type", "content_type"):
            if k in p:
                print("  ", k, "=", p.get(k))
