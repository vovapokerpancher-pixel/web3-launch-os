import json, os, urllib.request, urllib.error, urllib.parse

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
ZIP = os.getenv("DELIVERY_ZIP", "")   # path to the zip on the runner — set in workflow
PID = os.getenv("PRODUCT_ID", "prod_K7xUWrvKEnWA6")


def call(m, p, d=None, headers=None):
    b = json.dumps(d).encode() if d is not None else None
    h = {"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
         "Api-Version-Date": "2026-07-01"}
    if headers:
        h.update(headers)
    r = urllib.request.Request(BASE + p, data=b, headers=h, method=m)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


def main():
    if not ZIP or not os.path.exists(ZIP):
        print("DELIVERY_ZIP not set/not found:", ZIP)
        return
    data = open(ZIP, "rb").read()
    size = len(data)
    print("zip bytes:", size)

    # 1) create file (public so the download URL is stable + directly shareable)
    st, b = call("POST", "/files", {"filename": "Web3-Launch-OS-v1.0.zip", "byte_size": size, "visibility": "public"})
    print("create file:", st, str(b)[:300])
    if st not in (200, 201):
        return
    fid = b.get("id")
    upload_url = b.get("upload_url")
    headers = b.get("upload_headers") or {}
    print("file id:", fid)

    # 2) PUT bytes to presigned url
    if upload_url:
        h = {"Content-Type": "application/zip"}
        h.update(headers)
        req = urllib.request.Request(upload_url, data=data, headers=h, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                print("upload PUT:", resp.status)
        except urllib.error.HTTPError as e:
            print("upload PUT err:", e.code, e.read().decode()[:200])
            return

    # 3) confirm ready
    for _ in range(12):
        try:
            st3, b3 = call("GET", "/files/" + fid)
            status = (b3 or {}).get("upload_status")
            print("file status:", status)
            if status == "ready":
                print("FINAL url:", (b3 or {}).get("url"))
                print("FINAL id:", fid)
                break
        except Exception as e:
            print("poll err", str(e)[:80])
    # write a marker
    with open("delivery_result.json", "w", encoding="utf-8") as fh:
        json.dump({"file_id": fid, "product_id": PID}, fh)


if __name__ == "__main__":
    main()
