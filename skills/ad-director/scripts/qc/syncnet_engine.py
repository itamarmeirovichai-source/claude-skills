"""SyncNet (Chung & Zisserman, "Out of time: automated lip sync in the wild", ACCV-W 2016) offset estimator.

Re-implements the public syncnet_python evaluation (github.com/joonson/syncnet_python) so the
QC tool can use the original pretrained weights (syncnet_v2.model, ~54 MB, downloaded once from
the authors' site into ~/.cache/ad-director-qc). Needs torch (CPU is fine) and python_speech_features.

Protocol (same as the reference implementation):
  * video at 25 fps, face crop resized to 224x224 (BGR, 0-255), 5-frame windows;
  * 13 MFCCs at 100 Hz (20 audio steps per 5-frame window);
  * for every window, distance between lip and audio embeddings for shifts of -vshift..+vshift frames;
  * mean over windows -> min distance at the best shift; confidence = median(dist) - min(dist).
Typical values on real talking heads: confidence > 5 means the mouth is clearly driven by this audio;
< 2-3 means no reliable sync (mismatched audio, mouth hidden, or no speech).
"""
from __future__ import annotations

import numpy as np

try:
    import torch
    import torch.nn as nn
    from python_speech_features import mfcc as psf_mfcc
    AVAILABLE = True
except ImportError:  # pragma: no cover
    AVAILABLE = False

SYNCNET_URL = "https://www.robots.ox.ac.uk/~vgg/software/lipsync/data/syncnet_v2.model"


if AVAILABLE:
    class SyncNet(nn.Module):
        def __init__(self, fc: int = 1024):
            super().__init__()
            self.netcnnaud = nn.Sequential(
                nn.Conv2d(1, 64, (3, 3), (1, 1), (1, 1)), nn.BatchNorm2d(64), nn.ReLU(inplace=True),
                nn.MaxPool2d((1, 1), (1, 1)),
                nn.Conv2d(64, 192, (3, 3), (1, 1), (1, 1)), nn.BatchNorm2d(192), nn.ReLU(inplace=True),
                nn.MaxPool2d((3, 3), (1, 2)),
                nn.Conv2d(192, 384, (3, 3), padding=(1, 1)), nn.BatchNorm2d(384), nn.ReLU(inplace=True),
                nn.Conv2d(384, 256, (3, 3), padding=(1, 1)), nn.BatchNorm2d(256), nn.ReLU(inplace=True),
                nn.Conv2d(256, 256, (3, 3), padding=(1, 1)), nn.BatchNorm2d(256), nn.ReLU(inplace=True),
                nn.MaxPool2d((3, 3), (2, 2)),
                nn.Conv2d(256, 512, (5, 4), padding=(0, 0)), nn.BatchNorm2d(512), nn.ReLU(),
            )
            self.netfcaud = nn.Sequential(nn.Linear(512, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Linear(512, fc))
            self.netfclip = nn.Sequential(nn.Linear(512, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Linear(512, fc))
            self.netcnnlip = nn.Sequential(
                nn.Conv3d(3, 96, (5, 7, 7), (1, 2, 2), 0), nn.BatchNorm3d(96), nn.ReLU(inplace=True),
                nn.MaxPool3d((1, 3, 3), (1, 2, 2)),
                nn.Conv3d(96, 256, (1, 5, 5), (1, 2, 2), (0, 1, 1)), nn.BatchNorm3d(256), nn.ReLU(inplace=True),
                nn.MaxPool3d((1, 3, 3), (1, 2, 2), (0, 1, 1)),
                nn.Conv3d(256, 256, (1, 3, 3), padding=(0, 1, 1)), nn.BatchNorm3d(256), nn.ReLU(inplace=True),
                nn.Conv3d(256, 256, (1, 3, 3), padding=(0, 1, 1)), nn.BatchNorm3d(256), nn.ReLU(inplace=True),
                nn.Conv3d(256, 256, (1, 3, 3), padding=(0, 1, 1)), nn.BatchNorm3d(256), nn.ReLU(inplace=True),
                nn.MaxPool3d((1, 3, 3), (1, 2, 2)),
                nn.Conv3d(256, 512, (1, 6, 6), padding=0), nn.BatchNorm3d(512), nn.ReLU(inplace=True),
            )

        def forward_aud(self, x):
            m = self.netcnnaud(x)
            return self.netfcaud(m.view(m.size(0), -1))

        def forward_lip(self, x):
            m = self.netcnnlip(x)
            return self.netfclip(m.view(m.size(0), -1))


_MODEL = None


def load(weights_path: str):
    global _MODEL
    if _MODEL is None:
        net = SyncNet()
        sd = torch.load(weights_path, map_location="cpu", weights_only=True)  # plain tensors only
        net.load_state_dict(sd)
        net.eval()
        _MODEL = net
    return _MODEL


def face_crop(bgr: np.ndarray, box: list[float], crop_scale: float = 0.4) -> np.ndarray:
    """syncnet_python crop: square-ish window around the face box, padded, resized to 224."""
    import cv2
    x, y, w, h = box
    bs = max(w, h) / 2
    mx, my = x + w / 2, y + h / 2
    bsi = int(bs * (1 + 2 * crop_scale))
    pad = cv2.copyMakeBorder(bgr, bsi, bsi, bsi, bsi, cv2.BORDER_CONSTANT, value=(110, 110, 110))
    myp, mxp = my + bsi, mx + bsi
    face = pad[int(myp - bs):int(myp + bs * (1 + 2 * crop_scale)), int(mxp - bs * (1 + crop_scale)):int(mxp + bs * (1 + crop_scale))]
    return cv2.resize(face, (224, 224))


def evaluate(faces_bgr: list[np.ndarray], audio16k: np.ndarray, vshift: int = 15, batch: int = 20) -> dict:
    """faces_bgr: 224x224 crops at 25 fps. Returns offset (frames, + = audio leads, i.e. the mouth
    is late), per-shift mean distances, min distance and confidence, plus per-window best shifts."""
    net = load_cached()
    im = np.stack(faces_bgr, axis=3)[None].transpose(0, 3, 4, 1, 2).astype(np.float32)  # 1,3,T,224,224
    imtv = torch.from_numpy(im)
    pcm = np.clip(audio16k, -1, 1)
    feats = psf_mfcc((pcm * 32767).astype(np.int16), 16000)  # (N, 13) at 100 Hz
    cc = torch.from_numpy(feats.T[None, None].astype(np.float32))  # 1,1,13,N
    min_len = min(len(faces_bgr), int(np.floor(feats.shape[0] / 4)))
    last = min_len - 5
    if last < 2 * vshift + 1:
        vshift = max(2, (last - 1) // 2)
    im_feat, cc_feat = [], []
    with torch.no_grad():
        for i in range(0, max(0, last), batch):
            idx = range(i, min(last, i + batch))
            im_feat.append(net.forward_lip(torch.cat([imtv[:, :, v:v + 5] for v in idx], 0)))
            cc_feat.append(net.forward_aud(torch.cat([cc[:, :, :, v * 4:v * 4 + 20] for v in idx], 0)))
    if not im_feat:
        return {"ok": False, "reason": "clip too short for SyncNet (needs > 1 s)"}
    im_feat = torch.cat(im_feat, 0)
    cc_feat = torch.cat(cc_feat, 0)
    win = 2 * vshift + 1
    cc_pad = torch.nn.functional.pad(cc_feat, (0, 0, vshift, vshift))
    dists = torch.stack([torch.nn.functional.pairwise_distance(im_feat[[i]].repeat(win, 1), cc_pad[i:i + win])
                         for i in range(len(im_feat))], 1)  # win x T
    mdist = dists.mean(1)
    minval, minidx = torch.min(mdist, 0)
    offset = vshift - int(minidx)
    conf = float(torch.median(mdist) - minval)
    # per-window: best shift and its confidence (used for drift / dead-segment detection)
    per_win_best = (vshift - torch.argmin(dists, 0)).numpy()
    per_win_conf = (torch.median(dists, 0).values - torch.min(dists, 0).values).numpy()
    return {"ok": True, "offset_frames": offset, "min_dist": float(minval), "confidence": conf,
            "curve": mdist.numpy().tolist(), "vshift": vshift,
            "per_window_offset": per_win_best.tolist(), "per_window_conf": per_win_conf.tolist()}


def load_cached():
    from qclib import MODEL_DIR, MODEL_URLS, model_path
    MODEL_URLS.setdefault("syncnet_v2.model", SYNCNET_URL)
    p = model_path("syncnet_v2.model")
    if p is None:
        raise RuntimeError(f"SyncNet weights unavailable; put syncnet_v2.model in {MODEL_DIR}")
    return load(str(p))
