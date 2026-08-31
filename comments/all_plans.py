import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"


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


# list all products, then their plans
st, b = call("GET", "/products")
prods = b.get("data", b if isinstance(b, list) else [])
print("products count:", len(prods) if isinstance(prods, list) else str(prods)[:100])
for p in (prods if isinstance(prods, list) else []):
    title = p.get("title", "")
    if any(x in title for x in ["Anti-Slop", "99", "Commands", "Web3", "Launch"]):
        pid = p.get("id")
        acct = (p.get("account") or {})
        account_id = acct.get("id") if isinstance(acct, dict) else ""
        print("\nPRODUCT", pid, "|", title, "| acct", account_id)
        st2, b2 = call("GET", "/plans", {"account_id": account_id})
        data = b2.get("data", b2 if isinstance(b2, list) else [])
        if isinstance(data, list):
            for pl in data:
                if (pl.get("product_id") or "") == pid:
                    ip = (pl.get("initial_price") or {})
                    print("   plan", pl.get("id"), "| price", ip.get("amount"), ip.get("currency"), "| vis", pl.get("visibility"))
        else:
            print("   plans resp:", str(data)[:100])
