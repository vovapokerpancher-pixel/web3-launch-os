import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
PID = os.getenv("PRODUCT_ID", "prod_0WrqduKEM3TWZ")
ZIP = os.getenv("DELIVERY_ZIP", "")


def call(m, p, d=None, headers=None):
    b = json.dumps(d).encode() if d is not None else None
    hh = {"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "Api-Version-Date": "2026-07-01"}
    if headers:
        hh.update(headers)
    r = urllib.request.Request(BASE + p, data=b, headers=hh, method=m)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


def main():
    if not ZIP or not os.path.exists(ZIP):
        print("DELIVERY_ZIP missing:", ZIP)
        return
    data = open(ZIP, "rb").read()
    print("zip bytes:", len(data))
    st, b = call("POST", "/files", {"filename": "99-AI-Image-Commands-v1.0.zip", "byte_size": len(data), "visibility": "public"})
    print("create file:", st, str(b)[:200])
    if st not in (200, 201):
        return
    fid = b.get("id")
    upload_url = b.get("upload_url")
    print("file id:", fid)
    if upload_url:
        req = urllib.request.Request(upload_url, data=data, headers={"Content-Type": "application/zip"}, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                print("upload PUT:", resp.status)
        except urllib.error.HTTPError as e:
            print("put err:", e.code, e.read().decode()[:200])
    for _ in range(12):
        try:
            st3, b3 = call("GET", "/files/" + fid)
            s = (b3 or {}).get("upload_status")
            print("file status:", s)
            if s == "ready":
                print("FINAL url:", (b3 or {}).get("url"))
                print("FINAL id:", fid)
                break
        except Exception as e:
            print("poll", str(e)[:60])


if __name__ == "__main__":
    main()
