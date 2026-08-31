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


pid = "prod_K7xUWrvKEnWA6"
st, b = call("GET", f"/products/{pid}")
print("full product keys:", list((b or {}).keys()))
# look for anything about experiences/apps/delivery/content
for k in (b or {}).keys():
    v = b.get(k)
    if isinstance(v, (list, dict)) and v:
        print("FIELD", k, "=", json.dumps(v, ensure_ascii=False)[:400])
