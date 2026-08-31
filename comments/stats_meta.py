import json, os, urllib.request, urllib.error, urllib.parse

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
ACCOUNT = "biz_UJGSjyMgbaNs5W"


def get(path, params=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    r = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + KEY,
        "Api-Version-Date": "2026-07-01",
    }, method="GET")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


# 1) Discover what metrics exist
st, b = get("/stats")
print("STATS_META:", st, str(b)[:400])
