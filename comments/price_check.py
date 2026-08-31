import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
PS = [
    ("Anti-Slop", "prod_1mUCdlGTh02r9", "plan_doZBudXDxzkM0", "1.00"),
    ("99 Commands", "prod_0WrqduKEM3TWZ", "plan_EB2ap9WdFPgVX", "2.69"),
    ("Web3 OS", "prod_K7xUWrvKEnWA6", "plan_EB2ap9WdFPgVX", "19.00"),
]


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


for name, pid, plan_id, want in PS:
    st, b = call("GET", "/plans/" + plan_id)
    if st == 200:
        ip = (b or {}).get("initial_price") or {}
        print(name, "| plan", plan_id, "| price", ip.get("amount"), "| vis", (b or {}).get("visibility"))
    else:
        print(name, "| GET plan", st, str(b)[:120])
