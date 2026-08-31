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
        return e.code, e.read().decode()[:400]


# product -> affiliate %
PRODUCTS = [
    ("prod_1mUCdlGTh02r9", "Anti-Slop Prompt Kit", 30.0),
    ("prod_0WrqduKEM3TWZ", "99 AI Image Commands", 30.0),
    ("prod_K7xUWrvKEnWA6", "Web3 Launch OS", 35.0),
]

for pid, name, pct in PRODUCTS:
    st, b = call("PATCH", "/products/" + pid, {
        "member_affiliate_percentage": pct,
        "member_affiliate_status": "enabled",
        "global_affiliate_percentage": pct,
        "global_affiliate_status": "enabled",
    })
    print(name, "->", st, str(b)[:120])
