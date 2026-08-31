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


for label, path in [
    ("ACCOUNT_ME", "/accounts/me"),
    ("PRODUCTS", "/products"),
    ("COMPANY", "/company"),
    ("COMPANY_BALANCE", "/company/balance"),
    ("FILES", "/files"),
    ("PLANS", "/plans"),
]:
    st, b = call("GET", path)
    print(label, st, str(b)[:180])
