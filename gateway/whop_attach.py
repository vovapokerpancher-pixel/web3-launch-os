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


# The uploaded Whop-hosted ZIP, ready and downloadable (verified HTTP 200).
fid = "file_YAEHLpBO0wi32"
pid = "prod_K7xUWrvKEnWA6"

# Attempt to attach the file to the product so buyers see it after purchase.
st, b = call("POST", f"/products/{pid}/files", {"file_id": fid, "title": "Web3 Launch OS package"})
print("attach file->product:", st, str(b)[:200])
