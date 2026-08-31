import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
VERSION = os.getenv("WHOP_API_VERSION", "2026-07-01")
DRY = os.getenv("DRY_RUN", "true").lower() != "false"


def call(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(BASE + path, data=body, headers={
        "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json",
        "Api-Version-Date": VERSION,
    }, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


PRODUCT = {
    "title": "Anti-Slop Prompt Kit",
    "headline": "Turn boring AI images into premium ones.",
    "description": (
        "A 3-line formula that fixes the most common AI image problem (slop) plus "
        "25 ready copy-paste prompt upgrades. See the honest before/after proof. "
        "Compatible with ChatGPT Image 2.0 and similar tools. Reference tool; "
        "results depend on the model."
    ),
    "custom_cta": "get_access",
    "labels": ["prompts", "ai", "image"],
    "default_plan": {
        "title": "Full Access",
        "plan_type": "one_time",
        "initial_price": {"amount": "0.99", "currency": "usd"},
        "renewal_price": {"amount": "0.00", "currency": "usd"},
        "unlimited_stock": True,
        "visibility": "visible",
    },
    "affiliate": {"member_affiliate_percentage": 30.0, "global_affiliate_percentage": 30.0},
}


def main():
    if not KEY:
        print("WHOP_API_KEY not set.", file=os.sys.stderr)
        raise SystemExit(2)
    if DRY:
        print("[DRY-RUN]")
        print(json.dumps(PRODUCT, ensure_ascii=False, indent=2))
        return
    st, body = call("POST", "/products", PRODUCT)
    print("create product:", st, str(body)[:500])
    if st in (200, 201):
        pid = body.get("id", body.get("data", {}).get("id"))
        print("product id:", pid, "route:", body.get("route"))
        with open("antislopp_created.json", "w", encoding="utf-8") as fh:
            json.dump({"id": pid, "route": body.get("route")}, fh)


if __name__ == "__main__":
    main()
