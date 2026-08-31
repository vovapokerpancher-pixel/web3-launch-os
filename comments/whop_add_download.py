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


DESC = (
    "A cheatsheet of 99 AI image commands across 11 categories, plus 8 pro recipe "
    "combinations and 12 copy-paste example prompts. Compatible with ChatGPT Image 2.0. "
    "Includes 5 readable recap slides. Reference tool; results depend on the model.\n\n"
    "DOWNLOAD YOUR PACKAGE: " + DL + "\n"
    "If the link opens the next page after purchase, click the archive to download."
)


def main():
    st, b = call("PATCH", "/products/" + PID, {"description": DESC})
    print("update description:", st, str(b)[:200])
    if st in (200, 201):
        print("OK — download link added to product description.")


if __name__ == "__main__":
    main()
