import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
PID = "prod_1mUCdlGTh02r9"


def call(m, p, d=None, params=None):
    b = json.dumps(d).encode() if d is not None else None
    url = BASE + p
    if params:
        url += "?" + "&".join("%s=%s" % (k, v) for k, v in params.items())
    r = urllib.request.Request(url, data=b, headers={
        "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json",
        "Api-Version-Date": "2026-07-01",
    }, method=m)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


# get product
st, b = call("GET", "/products/" + PID)
# find account id
acct = (b or {}).get("account") or {}
account_id = acct.get("id") if isinstance(acct, dict) else None
print("account_id:", account_id)

# list plans for the product to see all pricing variants
st2, b2 = call("GET", "/plans", {"account_id": account_id or "", "product_id": PID})
if st2 == 200:
    data = b2.get("data", b2 if isinstance(b2, list) else [])
    print("plans count:", len(data) if isinstance(data, list) else str(data)[:100])
    for p in (data if isinstance(data, list) else []):
        ip = (p.get("initial_price") or {})
        print("  plan", p.get("id"), "| type", p.get("plan_type"), "| price", ip.get("amount"), ip.get("currency"), "| vis", p.get("visibility"))
else:
    print("plans:", st2, str(b2)[:200])
