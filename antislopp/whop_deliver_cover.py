import json, os, urllib.request, urllib.error, time

KEY = os.getenv("WHOP_API_KEY", "")
BASE = "https://api.whop.com/api/v1"
PID = "prod_1mUCdlGTh02r9"
ZIP = os.getenv("DELIVERY_ZIP", "")
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
        return None, "create file " + str(st)
    fid = b.get("id")
    up = b.get("upload_url")
    if up:
        req = urllib.request.Request(up, data=data, headers={"Content-Type": ctype}, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                print("upload PUT", name, resp.status)
        except urllib.error.HTTPError as e:
            print("put err", name, e.code)
    for _ in range(12):
        st3, b3 = call("GET", "/files/" + fid)
        if (b3 or {}).get("upload_status") == "ready":
            print("ready", name, fid)
            return fid, None
        time.sleep(4)
    return fid, "not ready"


def main():
    if ZIP and os.path.exists(ZIP):
        print("uploading zip...")
        fid, err = upload("Anti-Slop-Prompt-Kit-v1.0.zip", ZIP, "application/zip")
        print("zip file id:", fid, err or "")
    if COVER and os.path.exists(COVER):
        print("uploading cover...")
        cid, err = upload("cover.png", COVER, "image/png")
        print("cover file id:", cid, err or "")
        if cid:
            st4, b4 = call("PATCH", "/products/" + PID, {"gallery_images": [{"id": cid}]})
            print("set gallery:", st4, str(b4)[:120])


if __name__ == "__main__":
    main()
