import json, os, urllib.request, urllib.error, time

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
PID = "prod_1mUCdlGTh02r9"
COVER = os.getenv("COVER_IMG", "")


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


def upload(name, path, ctype):
    data = open(path, "rb").read()
    st, b = call("POST", "/files", {"filename": name, "byte_size": len(data), "visibility": "public"})
    if st not in (200, 201):
        return None
    fid = b.get("id")
    up = b.get("upload_url")
    if up:
        req = urllib.request.Request(up, data=data, headers={"Content-Type": ctype}, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                print("PUT", name, resp.status)
        except urllib.error.HTTPError as e:
            print("put err", name, e.code)
    for _ in range(12):
        st3, b3 = call("GET", "/files/" + fid)
        if (b3 or {}).get("upload_status") == "ready":
            return fid
        time.sleep(4)
    return fid


def main():
    if COVER and os.path.exists(COVER):
        cid = upload("cover.png", COVER, "image/png")
        print("cover file id:", cid)
        if cid:
            st4, b4 = call("PATCH", "/products/" + PID, {"gallery_images": [{"id": cid}], "custom_cta": "get_access"})
            print("set gallery/cta:", st4, str(b4)[:160])
    # Confirm price is 0.99 (read plan)
    st, b = call("GET", "/products/" + PID)
    dp = (b or {}).get("default_plan") or {}
    print("price:", (dp.get("initial_price") or {}).get("amount"), "cur:", (dp.get("initial_price") or {}).get("currency"))
    print("gallery count:", len((b or {}).get("gallery_images") or []))


if __name__ == "__main__":
    main()
