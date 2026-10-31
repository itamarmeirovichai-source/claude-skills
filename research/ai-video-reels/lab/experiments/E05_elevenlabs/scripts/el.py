"""Tiny proxy-auth helper (header injected by network secret; no key handled here)."""
import json, sys, urllib.request, urllib.parse, urllib.error
API = "https://api.elevenlabs.io"
def call(method, path, body=None, query=None, timeout=600, raw=False):
    url = API + path + ("?" + urllib.parse.urlencode(query, doseq=True) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    h = {"Accept": "*/*"}
    if body is not None: h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            b = r.read(); hd = dict(r.headers)
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_detail": (e.read() or b"")[:800].decode(errors="replace")}
    if raw: return b, hd
    try: return json.loads(b)
    except Exception: return b
