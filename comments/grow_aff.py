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


st, b = call("PATCH", "/products/prod_3qRek4SrZUdmk", {
    "member_affiliate_percentage": 30.0,
    "member_affiliate_status": "enabled",
    "global_affiliate_percentage": 30.0,
    "global_affiliate_status": "enabled",
})
print("affiliate:", st, str(b)[:120])
