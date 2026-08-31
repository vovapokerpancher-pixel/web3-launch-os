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


pid = "prod_1mUCdlGTh02r9"
st, b = call("GET", "/products/" + pid)
print("STATUS:", st)
print("title:", (b or {}).get("title"))
print("visibility:", (b or {}).get("visibility"), "| marketplace:", (b or {}).get("marketplace_status"))
print("custom_cta:", (b or {}).get("custom_cta"))
# look for any redirect / post-purchase / welcome fields
for k, v in (b or {}).items():
    if any(x in k.lower() for x in ["redirect", "post_purchase", "welcome", "checkout", "success", "url"]):
        print("FIELD", k, "=", json.dumps(v, ensure_ascii=False)[:200])
dp = (b or {}).get("default_plan") or {}
print("default_plan:", json.dumps(dp, ensure_ascii=False)[:300])
