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
print("count", len(data) if isinstance(data, list) else str(data)[:200])
if isinstance(data, list):
    for p in data:
        title = p.get("title") or ""
        if "Web3" in title or "Launch" in title:
            plan = (p.get("default_plan") or {})
            print(p.get("id"), "|", title, "|", p.get("created_at"), "|", p.get("visibility"), "| plan:", plan.get("id"))
