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
print("title:", b.get("title"), "| vis:", b.get("visibility"), "| mkt:", b.get("marketplace_status"))
dp = b.get("default_plan") or {}
print("plan:", dp.get("plan_type"), dp.get("initial_price", {}).get("amount"), dp.get("initial_price", {}).get("currency"))
print("gallery count:", len(b.get("gallery_images") or []))
print("custom_cta:", b.get("custom_cta"))

# Test: can we PATCH price (plan) and cover? Try reading plan id to update price.
plan_id = dp.get("id")
print("plan_id:", plan_id)
if plan_id:
    st2, b2 = call("GET", "/plans?account_id=" + "" )  # placeholder to see shape
    print("plans query probe:", st2, str(b2)[:200])
