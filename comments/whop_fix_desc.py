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
    # fetch current description (may have been edited by owner)
    st, b = call("GET", "/products/" + PID)
    desc = (b or {}).get("description", "") or ""
    if DL in desc:
        print("already present, no change.")
        return
    # append download line keeping existing text
    add = "\n\nDOWNLOAD YOUR PACKAGE (click to download):\n" + DL
    new_desc = desc + add
    st2, b2 = call("PATCH", "/products/" + PID, {"description": new_desc})
    print("update description:", st2, str(b2)[:200])


if __name__ == "__main__":
    main()
