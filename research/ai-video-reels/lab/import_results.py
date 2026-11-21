#!/usr/bin/env python3
"""Download finished Higgsfield outputs by request id (free: status GET + CDN download).

  python3 import_results.py takes.json [--out imported/]
takes.json: [{"experiment": "E01_models", "take": "T01_label_rotate__kling30pro#1", "request_id": "..."}]
Uses the same auth as hfgen (HF_KEY, or HF_AUTH_VIA_PROXY=1 with a network secret).
"""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "skills" / "ad-director" / "scripts"))
import hfgen as H  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("takes"); ap.add_argument("--out", default="imported")
a = ap.parse_args()
out = Path(a.out)
ok = 0
for t in json.loads(Path(a.takes).read_text()):
    rid = t.get("request_id")
    if not rid:
        continue
    st = H.status(rid)
    urls = H.outputs(st) if st.get("status") == "completed" else []
    for i, u in enumerate(urls):
        name = t["take"].replace("#", "_t") + (f"_{i}" if i else "") + H._ext(u, ".mp4" if "video" in st else ".png")
        H.download(u, out / t.get("experiment", "misc") / name)
        ok += 1
    print(f"{t.get('experiment','?'):<12} {t['take']:<40} {st.get('status')}  {len(urls)} file(s)")
print(f"downloaded {ok} file(s) -> {out}")
