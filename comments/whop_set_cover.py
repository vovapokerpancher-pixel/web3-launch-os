import json, os, urllib.request, urllib.error

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
PID = os.getenv("PRODUCT_ID", "prod_0WrqduKEM3TWZ")
IMG = os.getenv("COVER_IMG", "")


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
    if not IMG or not os.path.exists(IMG):
        print("COVER_IMG missing:", IMG)
        return
    data = open(IMG, "rb").read()
    print("img bytes:", len(data))
    st, b = call("POST", "/files", {"filename": "cover.png", "byte_size": len(data), "visibility": "public"})
    print("create file:", st, str(b)[:200])
    if st not in (200, 201):
        return
    fid = b.get("id")
    up = b.get("upload_url")
    if up:
        req = urllib.request.Request(up, data=data, headers={"Content-Type": "image/png"}, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                print("upload PUT:", resp.status)
        except urllib.error.HTTPError as e:
            print("put err:", e.code, e.read().decode()[:200])
    for _ in range(12):
        st3, b3 = call("GET", "/files/" + fid)
        s = (b3 or {}).get("upload_status")
        if s == "ready":
            print("file ready:", fid)
            break
        import time
        time.sleep(4)
    # update product gallery to just this cover
    st4, b4 = call("PATCH", "/products/" + PID, {"gallery_images": [{"id": fid}]})
    print("update gallery:", st4, str(b4)[:300])


if __name__ == "__main__":
    main()
