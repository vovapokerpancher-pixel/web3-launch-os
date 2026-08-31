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
print("FIELDS:", sorted((b or {}).keys()))
# check for experiences/apps/files/content indicators
for k in ("experiences", "apps", "files", "delivery", "content"):
    if k in (b or {}):
        print("FIELD", k, "=", json.dumps(b[k], ensure_ascii=False)[:300])
# gallery
print("gallery count:", len((b or {}).get("gallery_images") or []))
# description download link
d = (b or {}).get("description", "")
print("desc has download link:", "fed7c598" in d)
