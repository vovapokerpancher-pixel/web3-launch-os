import json, os, urllib.request
KEY = os.getenv("WHOP_API_KEY", "")
r = urllib.request.Request("https://api.whop.com/api/v1/products/prod_0WrqduKEM3TWZ", headers={
    "Authorization": "Bearer " + KEY,
    "Api-Version-Date": "2026-07-01",
})
with urllib.request.urlopen(r, timeout=60) as resp:
    d = json.loads(resp.read().decode())
desc = d.get("description", "")
print("description has download link:", "fed7c598-63d2-41d2-ab75-45af84a87407" in desc)
print("description tail:", desc[-160:])
