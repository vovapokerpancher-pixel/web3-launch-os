import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
DRY = os.getenv("DRY_RUN", "true").lower() != "false"
ACCOUNT = os.getenv("WHOP_ACCOUNT_ID", "biz_UJGSjyMgbaNs5W")


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


def main():
    if not KEY:
        print("WHOP_API_KEY not set.", file=os.sys.stderr)
        raise SystemExit(2)

    # 1) create the product
    product = {
        "title": "Growth Tracker",
        "headline": "See where your traffic becomes clicks.",
        "description": (
            "A light analytics tool that shows which of your landing pages get "
            "views and where visitors click your checkout link. Runs in your "
            "browser, no personal data, no external calls. Dashboard + JSON "
            "export. Reference tool; results depend on your setup."
        ),
        "custom_cta": "subscribe",
        "labels": ["analytics", "growth", "tools"],
    }
    if DRY:
        print("[DRY-RUN] product payload:", json.dumps(product, ensure_ascii=False))
        print("[DRY-RUN] would then POST /plans with plan_type=renewal, billing_period=30, renewal_price=5.00")
        return
    st, body = call("POST", "/products", product)
    print("create product:", st, str(body)[:300])
    if st not in (200, 201):
        return
    pid = body.get("id", body.get("data", {}).get("id"))
    print("product id:", pid, "route:", body.get("route"))

    # 2) create the RECURRING plan ($5/mo)
    plan = {
        "account_id": ACCOUNT,
        "product_id": pid,
        "plan_type": "renewal",
        "title": "Monthly",
        "currency": "usd",
        "initial_price": 5.00,
        "renewal_price": 5.00,
        "billing_period": 30,
        "unlimited_stock": True,
        "visibility": "visible",
        "release_method": "buy_now",
    }
    st2, b2 = call("POST", "/plans", plan)
    print("create plan:", st2, str(b2)[:300])
    if st2 in (200, 201):
        plan_id = b2.get("id", b2.get("data", {}).get("id"))
        print("plan id:", plan_id)
        with open("growth_created.json", "w", encoding="utf-8") as fh:
            json.dump({"product_id": pid, "plan_id": plan_id, "route": body.get("route")}, fh)

    # 3) publish product
    st3, b3 = call("POST", "/products/%s/publish" % pid, {})
    print("publish:", st3, str(b3)[:200])


if __name__ == "__main__":
    main()
