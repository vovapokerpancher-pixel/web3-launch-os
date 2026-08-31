import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
PID = os.getenv("PRODUCT_ID", "prod_0WrqduKEM3TWZ")
DL = "https://assets-2-prod.whop.com/public/uploads/2026-08-31/fed7c598-63d2-41d2-ab75-45af84a87407/application.zip"


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
    st, b = call("GET", "/products/" + PID)
    desc = (b or {}).get("description", "") or ""
    # remove the download line we added
    lines = [ln for ln in desc.splitlines() if DL not in ln]
    new_desc = "\n".join(lines)
    # remove any leftover empty leading/trailing newlines
    new_desc = new_desc.strip()
    print("OLD desc had link:", DL in desc)
    st2, b2 = call("PATCH", "/products/" + PID, {"description": new_desc})
    print("update description (removed link):", st2, str(b2)[:160])


if __name__ == "__main__":
    main()
