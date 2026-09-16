"""Render the scroll sequence.

Every frame is a pure function of scroll progress: the scene is rebuilt from
pose(p) each time and never accumulates state, so frame N is identical whether
the viewer arrived scrolling down or scrolling back up.

    python3 pr_render.py --variant desktop --start 0 --count 8 --samples 48
"""
import os, sys, json, math, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_boot  # must precede bpy
import bpy
from mathutils import Vector
import pr_scene as S
import pr_anim as A
import pr_cut as C

VARIANTS = {
    "desktop": dict(frames=108, res=(1440, 810), sensor='HORIZONTAL', dist_k=1.00),
    "mobile":  dict(frames=54,  res=(810, 1080), sensor='VERTICAL',  dist_k=1.02),
}

# where each layer's label points. Local to the layer, metres.
ANCHOR_R = 0.050


def aim_camera(cam, pose, dist_k=1.0):
    # follow the drop rather than framing for it: aiming at a fixed height
    # while the burger is 85 mm above it put the first frames half off the top
    target = Vector((0.0, 0.0, pose["cam_target_z"] + pose["rise"] * 0.88))
    e = math.radians(pose["cam_elev"])
    a = math.radians(pose["cam_azim"])
    cam.data.lens = pose["cam_focal"]
    d = pose["cam_dist"] * dist_k
    # Never let the subject leave the frame. The hand-set distance is a floor;
    # the real one is whatever it takes to fit the fan and the parted halves,
    # solved against this camera's actual field of view.
    need_v = pose["fan_half"] * 1.10 / math.tan(cam.data.angle_y * 0.5)
    need_h = pose["wide_half"] * 1.10 / math.tan(cam.data.angle_x * 0.5)
    d = max(d, need_v, need_h)
    pos = target + Vector((math.sin(a) * math.cos(e),
                           -math.cos(a) * math.cos(e),
                           math.sin(e))) * d
    cam.location = pos
    cam.rotation_euler = (target - pos).to_track_quat('-Z', 'Y').to_euler()
    cam.data.dof.focus_distance = (target - pos).length
    return pos


def apply_pose(obs, root, halves, cam, p, dist_k=1.0):
    d = A.pose(p)
    root.location = (0.0, 0.0, d["rise"])
    root.rotation_euler = (0.0, 0.0, d["spin"])
    root.scale = (d["bulge"], d["bulge"], d["squash"])

    cutting = d["cut_active"]
    for name, ob in obs.items():
        key = "bun_top" if name.endswith("_seeds") else name
        ob.location.z = ob["rest_z"] + (A.layer_offset(key, d) if key in A.STACK else 0.0)
        ob.hide_render = cutting

    left, right, pairs = halves
    for empty, sign in ((left, -1.0), (right, 1.0)):
        empty.hide_render = not cutting
        empty.location = (sign * d["part"], 0.0, 0.0)
        # both halves rotate to put their cut face on the same side
        empty.rotation_euler = (0.0, 0.0, sign * d["book"])
        for child in empty.children:
            child.hide_render = not cutting
            base = child.get("rest_z", 0.0)
            key = child.get("layer_name", "")
            if key.endswith("_seeds"):
                key = "bun_top"
            child.location.z = base + (A.layer_offset(key, d) if key in A.STACK else 0.0)
    aim_camera(cam, d, dist_k)
    return d


def label_anchors(scene, cam, obs, d):
    """Where each layer's label should sit on screen, in 0..1 view space."""
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    out = {}
    for name in A.STACK:
        ob = obs.get(name)
        if ob is None:
            continue
        world = ob.matrix_world @ Vector((ANCHOR_R, 0.0, 0.0))
        co = world_to_camera_view(scene, cam, world)
        out[name] = [round(co.x, 4), round(1.0 - co.y, 4),
                     1 if (0.0 <= co.x <= 1.0 and 0.0 <= co.y <= 1.0 and co.z > 0) else 0]
    out["_explode"] = round(d["explode_amt"], 4)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="desktop", choices=list(VARIANTS))
    ap.add_argument("--start", type=int, default=0, help="0-based frame index")
    ap.add_argument("--count", type=int, default=0, help="0 = to the end")
    ap.add_argument("--samples", type=int, default=56)
    ap.add_argument("--out", default="../../out/seq")
    ap.add_argument("--labels", default="")
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--only", default="", help="comma list of 1-based frame numbers")
    ap.add_argument("--poster", default="", help="also write this single still at p=0.26")
    ap.add_argument("--no-render", action="store_true",
                    help="compute the label track only — no Cycles, seconds not hours")
    a = ap.parse_args()

    V = VARIANTS[a.variant]
    obs, root, cam = S.build_scene(dressed=False)
    for name, ob in obs.items():
        ob["rest_z"] = ob.location.z
    halves = C.build_halves(obs, root)
    for name, pair in halves[2].items():
        for h in pair:
            h["rest_z"] = h.location.z
            h["layer_name"] = name

    sc = S.setup_render(V["res"][0], V["res"][1], a.samples)
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'WEBP'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.render.image_settings.quality = a.quality
    sc.view_settings.exposure = -0.15
    cam.data.sensor_fit = V["sensor"]

    outdir = os.path.abspath(os.path.join(a.out, a.variant))
    os.makedirs(outdir, exist_ok=True)

    n = V["frames"]
    last = n if a.count <= 0 else min(n, a.start + a.count)
    picked = [int(x) - 1 for x in a.only.split(",") if x.strip()] if a.only else None
    labels = {}
    t0 = time.time()
    for i in (picked if picked is not None else range(a.start, last)):
        p = i / float(n - 1)
        d = apply_pose(obs, root, halves, cam, p, V["dist_k"])
        labels["%04d" % (i + 1)] = label_anchors(sc, cam, obs, d)
        if a.no_render:
            continue
        sc.render.filepath = os.path.join(outdir, "smash_%04d" % (i + 1))
        bpy.ops.render.render(write_still=True)
        print("FRAME %d/%d p=%.4f  %.1fs" % (i + 1, n, p, time.time() - t0), flush=True)
    if a.poster and not a.no_render:
        apply_pose(obs, root, halves, cam, 0.26, V["dist_k"])
        os.makedirs(os.path.dirname(os.path.abspath(a.poster)), exist_ok=True)
        sc.render.image_settings.quality = 88
        sc.render.filepath = os.path.abspath(a.poster).replace(".webp", "")
        bpy.ops.render.render(write_still=True)
        print("WROTE poster", a.poster)

    if a.labels:
        os.makedirs(os.path.dirname(os.path.abspath(a.labels)), exist_ok=True)
        with open(a.labels, "w") as fh:
            json.dump({"variant": a.variant, "frames": n,
                       "res": V["res"], "anchors": labels}, fh, indent=1)
        print("WROTE", a.labels)
    print("TOTAL %.1fs for %d frames" % (time.time() - t0, last - a.start))


if __name__ == "__main__":
    main()
