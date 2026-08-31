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


st, b = call("GET", "/permissions")
print("PERMISSIONS:", st, str(b)[:500])

st2, b2 = call("GET", "/products/prod_1mUCdlGTh02r9/experiences")
print("EXPERIENCES:", st2, str(b2)[:200])

# Also check what the key can do on the account
st3, b3 = call("GET", "/accounts/me")
print("ACCOUNT:", st3, str(b3)[:200])
