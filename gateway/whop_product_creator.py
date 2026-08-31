"""
Whop product creator — runs inside GitHub Actions (US runners) so the API call
comes from an allowed region. Official Whop Products API (verified against docs).

Flow (replaces simpler checkout example):
  POST /api/v1/products                    -> create product
  POST (product) then publish via /publish; pricing is a Plan:
     - A product has plans. We create a one_time plan at $19 and make it default
       so the public page shows a buyable plan.
  (Optional) attach hosted digital file.

Modes:
  - DRY_RUN (default): prints payloads; does NOT create anything.
  - DRY_RUN=false: actually creates (irreversible, external).

Env (from GitHub secrets):
  WHOP_API_KEY
  WHOP_API_VERSION  (default 2026-07-01)

SECURITY: key only from env. No secrets in code.
"""
import json
import os
import sys
import urllib.request
import urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
VERSION = os.getenv("WHOP_API_VERSION", "2026-07-01")
BASE = "https://api.whop.com/api/v1"
DRY = os.getenv("DRY_RUN", "true").lower() != "false"

# Publicly hosted deliverable (on this repo's GitHub Pages) — used as delivery link.
DELIVERY_URL = "https://vovapokerpancher-pixel.github.io/web3-launch-os/Web3-Launch-OS-v1.0.zip"
COVER_URL = "https://vovapokerpancher-pixel.github.io/web3-launch-os/assets/cover.png"

PRODUCT = {
    "title": "Web3 Launch OS",
    "headline": "The operating system for web3 traction.",
    "description": (
        "A repeatable system for founders and growth leads of small web3 projects "
        "(team <= 10): KPI calculator, 30-day content calendar, community SOP, "
        "campaign planner, objection library, 3 scenarios, and 5 n8n workflows. "
        "First value in under 20 minutes. Inspect the filled examples before you buy. "
        "Not financial advice; does not guarantee token price or revenue."
    ),
    "custom_cta": "get_access",
    "labels": ["web3", "growth", "template"],
    # one-time $19 plan
    "default_plan": {
        "title": "Full Access",
        "plan_type": "one_time",
        "initial_price": {"amount": "19.00", "currency": "usd"},
        "renewal_price": {"amount": "0.00", "currency": "usd"},
        "unlimited_stock": True,
        "visibility": "visible",
    },
    "affiliate": {"member_affiliate_percentage": 35.0, "global_affiliate_percentage": 35.0},
}


def call(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=body,
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "Api-Version-Date": VERSION,
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]


def main():
    if not KEY:
        print("WHOP_API_KEY not set.", file=sys.stderr)
        sys.exit(2)

    if DRY:
        print("[DRY-RUN] payload (no API call):")
        print(json.dumps(PRODUCT, ensure_ascii=False, indent=2))
        print("\nDelivery URL:", DELIVERY_URL)
        print("Set DRY_RUN=false to actually create.")
        return

    st, body = call("POST", "/products", PRODUCT)
    print("create product:", st, str(body)[:600])
    if st not in (200, 201):
        # fall back to reading what happened
        stl, bl = call("GET", "/products")
        print("existing products list status:", stl, str(bl)[:400])
        return
    pid = body.get("id", body.get("data", {}).get("id"))
    print("product id:", pid)

    # Some products require a logo before publish. Try setting logo_url via PATCH.
    stl, bl = call("PATCH", f"/products/{pid}", {"logo_url": COVER_URL})
    print("set logo via patch:", stl, str(bl)[:200])

    st2, b2 = call("POST", f"/products/{pid}/publish", {})
    print("publish:", st2, str(b2)[:400])


if __name__ == "__main__":
    main()
