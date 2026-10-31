"""Train the Otto Soul ID (Higgsfield POST /v1/custom-references, model_version cinema).

Uses the QC-approved training images in train/ (w20 excluded: malformed hand frame).
Catalogue price: 40 credits ~ $2.50. Writes soulid.json (id, status, image count).
Run: HF_AUTH_VIA_PROXY=1 python3 train_soulid.py [--name NAME] [--exclude a,b]
"""
import argparse, json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "skills/ad-director/scripts"))
import hfgen  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--name", default="VEE (VXO producer) v1")
ap.add_argument("--dir", default="train")
ap.add_argument("--exclude", default="")
ap.add_argument("--out", default="soulid.json")
a = ap.parse_args()

skip = [s for s in a.exclude.split(",") if s]
imgs = [p for p in sorted((HERE / a.dir).glob("*.png")) if not any(p.name.startswith(s) for s in skip)]
ref = HERE / "ref/_none.png"
if ref.exists():
    imgs.insert(0, ref)
print(f"{len(imgs)} images -> uploading")
urls = [hfgen.upload(p) for p in imgs]
body = {"name": a.name, "model_version": "cinema",
        "input_images": [{"type": "image_url", "image_url": u} for u in urls]}
sub = hfgen._request("POST", hfgen.API + "/v1/custom-references", body)
rid = sub["id"]
print("submitted", rid, sub.get("status"))
st = sub
for _ in range(240):
    if st.get("status") in ("completed", "failed"):
        break
    time.sleep(15)
    st = hfgen._request("GET", f"{hfgen.API}/v1/custom-references/{rid}")
    print(st.get("status"))
rec = {"id": rid, "name": a.name, "model_version": "cinema", "status": st.get("status"),
       "images": [p.name for p in imgs], "est_usd": 2.50}
(HERE / a.out).write_text(json.dumps(rec, indent=1))
print(json.dumps(rec)[:400])
