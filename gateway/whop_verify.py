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
if not isinstance(data, list):
    print("list not array", str(data)[:200])
    raise SystemExit

# Candidate IDs we created across runs (from logs).
candidates = ["prod_vCCczg2JZfudM", "prod_7RSQOQ0t6iwDo", "prod_5aAAYSbS9Z0fQ", "prod_MBlkJw0TRdplG"]
out = []
for pid in candidates:
    s, body = call("GET", "/products/" + pid)
    if s == 200:
        out.append({
            "id": body.get("id"),
            "title": body.get("title"),
            "visibility": body.get("visibility"),
            "route": body.get("route"),
            "created_at": body.get("created_at"),
            "marketplace": body.get("marketplace_status"),
            "default_plan": (body.get("default_plan") or {}).get("id"),
        })
    else:
        out.append({"id": pid, "status": s})

with open("my_candidates.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
