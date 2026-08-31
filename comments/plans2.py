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


# list plans with pagination; the account_id comes from product's account
st, b = call("GET", "/products/" + PID)
acct = (b or {}).get("account") or {}
account_id = acct.get("id") if isinstance(acct, dict) else ""
print("account_id:", account_id)

# find all plans (try without product filter first)
st2, b2 = call("GET", "/plans", {"account_id": account_id})
print("plans list:", st2)
data = b2.get("data", b2 if isinstance(b2, list) else [])
if isinstance(data, list):
    # print only plans for our product
    for p in data:
        if (p.get("product_id") or "").startswith("prod_1mUCdl"):
            ip = (p.get("initial_price") or {})
            print("  plan", p.get("id"), "| product", p.get("product_id"), "| price", ip.get("amount"), ip.get("currency"), "| vis", p.get("visibility"))
    print("total plans:", len(data))
else:
    print(str(data)[:200])
