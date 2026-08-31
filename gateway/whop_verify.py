"""
Verify the Web3 Launch OS product created in Whop (read-only).
Run inside GitHub Actions (US region). Prints product + plan + purchase URL.
"""
import json
import os
import urllib.request
import urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"


def call(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=body,
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "Api-Version-Date": "2026-07-01",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


def main():
    st, body = call("GET", "/products")
    products = body.get("data", body if isinstance(body, list) else [])
    print("products:", st, "count:", len(products) if isinstance(products, list) else str(products)[:200])
    if isinstance(products, list):
        for p in products:
            title = p.get("title")
            if "Web3" in title or "Launch" in title:
                show = {k: p.get(k) for k in ("id", "title", "route", "visibility", "marketplace_status", "headline")}
                print(show)
                dp = p.get("default_plan") or {}
                print("  plan:", dp.get("title"), dp.get("plan_type"), dp.get("initial_price", {}).get("amount"), "route:", p.get("route"))
                print("  purchase url: https://whop.com/products/" + str(p.get("route")))


if __name__ == "__main__":
    main()
