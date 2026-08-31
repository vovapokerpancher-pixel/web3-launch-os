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
# Get the product and investigate experiences/apps
st, b = call("GET", f"/products/{pid}")
print("product title:", b.get("title"), "| route:", b.get("route"))
# print keys that hint at apps/experiences/files
for k in b.keys():
    if "app" in k.lower() or "experienc" in k.lower() or "file" in k.lower() or "delivery" in k.lower() or "post" in k.lower():
        print("field:", k, "=", str(b.get(k))[:200])
print("metadata:", b.get("metadata"))
print("default_plan full:", json.dumps(b.get("default_plan"), ensure_ascii=False))
