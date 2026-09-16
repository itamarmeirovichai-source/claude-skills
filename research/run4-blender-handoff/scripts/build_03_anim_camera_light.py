"""Steps 6-10: the continuous camera take, all 8 beats keyed, lighting, world, render settings,
and the label anchor track the website needs."""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import smash_common as S

SRC, OUT, LABELS_DIR = sys.argv[-3], sys.argv[-2], sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene

TOSS = [bpy.data.objects[n] for n in S.TOSS_NAMES]
HERO = TOSS[S.HERO_INDEX]
LAYER_OBJS = [bpy.data.objects[L["name"]] for L in S.LAYERS]
HALF_L = bpy.data.objects["burger_half_left"]
HALF_R = bpy.data.objects["burger_half_right"]
HALF_KIDS = [o for o in bpy.data.collections["CUT"].objects if o.type == 'MESH']
KNIFE = bpy.data.objects["knife"]
GLINT = bpy.data.objects["knife_glint"]
LOOSE = [bpy.data.objects["seed_loose_%02d" % (i + 1)] for i in range(30)]

GRAV = 9.8 * 0.30
TOSS_PARAMS = [dict(v0=2.03 + i * 0.055, phase=i * 0.06,
                    dx=(i - 2) * 0.075, dy=(0.04 if i % 2 else -0.04),
                    axis=Vector((S.noise1(i + 1), S.noise1(i + 5), 1.0)).normalized(),
                    w0=5.5 + i * 0.9) for i in range(5)]

# ------------------------------------------------------------------ camera
cam_data = bpy.data.cameras.new("cam_main")
cam_data.lens = 85.0            # ONE lens for the whole take: distance does the work, never zoom
cam_data.sensor_width = 36.0
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 2.4
cam = bpy.data.objects.new("cam_main", cam_data)
S.link(cam, "CAMERA")
sc.camera = cam

focus_tgt = bpy.data.objects.new("focus_target", None)
S.link(focus_tgt, "CAMERA")
focus_tgt.empty_display_size = 0.02
cam_data.dof.focus_object = focus_tgt

port_data = cam_data.copy(); port_data.name = "cam_main_portrait"; port_data.lens = 70.0
port_data.dof.focus_object = focus_tgt
cam_p = bpy.data.objects.new("cam_main_portrait", port_data)
S.link(cam_p, "CAMERA")

# (progress, distance in m, target height in m, camera rise above target, f-stop)
# distances come from the subject size each beat has to cover at an 85mm lens on a 36mm sensor
CAM_KEYS = [
    (0.00, 1.75, 0.06, 0.05, 11.0),
    (0.11, 1.70, 0.36, 0.02, 11.0),
    (0.21, 1.60, 0.38, 0.01, 8.0),
    (0.31, 0.34, 0.055, 0.02, 5.0),
    (0.50, 1.32, 0.058, 0.02, 7.1),
    (0.59, 1.32, 0.058, 0.02, 7.1),
    (0.69, 0.52, 0.055, 0.03, 7.1),
    (0.86, 0.62, 0.050, 0.02, 7.1),
    (1.00, 0.62, 0.050, 0.02, 7.1),
]

def _interp(p):
    for i in range(len(CAM_KEYS) - 1):
        a, b = CAM_KEYS[i], CAM_KEYS[i + 1]
        if a[0] <= p <= b[0]:
            t = 0.0 if b[0] == a[0] else (p - a[0]) / (b[0] - a[0])
            t = t * t * (3 - 2 * t)            # smoothstep, so no corner at a beat boundary
            return [a[k] + (b[k] - a[k]) * t for k in range(1, 5)]
    return list(CAM_KEYS[-1][1:])

def cam_state(p):
    """One continuous move: distance does the framing, the focal length never changes."""
    orbit = S.local(p, "bullet") * math.pi * 0.5
    smash_t = S.local(p, "smash")
    impact = S.ease_expo_in(min(1.0, max(0.0, (smash_t - 0.3) / 0.2)))
    recoil = min(1.0, max(0.0, (smash_t - 0.5) / 0.5))
    shake = impact * (1 - recoil)
    dist, tgt_z, rise, fstop = _interp(p)
    e = S.local(p, "explode")
    tgt_z += S.CENTER_I * 0.018 * S.ease_back_out(e) * 0.5   # follow the lifted stack
    pos = Vector((math.sin(orbit) * dist + S.noise1(p * 900) * 0.010 * shake,
                  -math.cos(orbit) * dist,
                  tgt_z + rise + S.noise1(p * 770) * 0.008 * shake))
    return pos, Vector((0.0, 0.0, tgt_z)), shake, fstop

def key_cam(ob, f, p, portrait=False):
    pos, tgt, shake, fstop = cam_state(p)
    ob.location = pos + (Vector((0, 0, 0.01)) if portrait else Vector())
    q = (pos - tgt).to_track_quat('Z', 'Y')
    e = q.to_euler()
    e.rotate_axis('Z', S.noise1(p * 610) * 0.02 * shake)
    ob.rotation_euler = e
    ob.keyframe_insert("location", frame=f)
    ob.keyframe_insert("rotation_euler", frame=f)
    # focus tracks an object, so it can never drift off the subject; the rack is the empty moving
    ob.data.dof.aperture_fstop = fstop
    ob.data.dof.keyframe_insert("aperture_fstop", frame=f)

# ------------------------------------------------------------------ per-frame state
def beat_state(p):
    t_toss = S.local(p, "toss"); settle = S.local(p, "closeup")
    e_raw = S.local(p, "explode"); smash_t = S.local(p, "smash")
    antic = min(1.0, max(0.0, smash_t / 0.3))
    impact = S.ease_expo_in(min(1.0, max(0.0, (smash_t - 0.3) / 0.2)))
    recoil = min(1.0, max(0.0, (smash_t - 0.5) / 0.5))
    t_cut = S.local(p, "cut")
    cutting = min(1.0, max(0.0, (t_cut - 0.15) / 0.35))
    opening = min(1.0, max(0.0, (t_cut - 0.55) / 0.45))
    return t_toss, settle, e_raw, smash_t, antic, impact, recoil, t_cut, cutting, opening

for f in range(S.FRAME_START, S.FRAME_END + 1):
    p = S.p_of(f)
    (t_toss, settle, e_raw, smash_t, antic, impact, recoil,
     t_cut, cutting, opening) = beat_state(p)
    shake = impact * (1 - recoil)
    split = cutting > 0.5
    # the bottom layers would otherwise explode straight through the griddle
    spread0 = S.ease_back_out(min(1.0, max(0.0, e_raw))) * (1 + antic * 0.08) * (1 - impact)
    lift = max(0.0, S.CENTER_I * 0.018 * spread0) + 0.004 * spread0

    key_cam(cam, f, p)
    key_cam(cam_p, f, p, portrait=True)
    # rack focus: sits on the blade edge as it enters, then pulls back onto the cut face
    rack = min(1.0, max(0.0, (t_cut - 0.15) / 0.35))
    focus_tgt.location = (0.0, -0.035 * (1 - rack), S.STACK_H / 2)
    focus_tgt.keyframe_insert("location", frame=f)

    # --- beat 1-3: the toss, the freeze, the settle ---
    for i, ob in enumerate(TOSS):
        d = TOSS_PARAMS[i]
        apex_t = d["v0"] / GRAV          # normalise so t=1 is this burger's apex, not past it
        tt = max(0.0, (t_toss - d["phase"]) / (1 - d["phase"])) * apex_t
        x = d["dx"] * tt
        y = d["dy"] * tt
        z = -0.42 + d["v0"] * tt - 0.5 * GRAV * tt * tt
        if i == S.HERO_INDEX:
            ob.location = (x * (1 - settle), y * (1 - settle), z * (1 - settle) + lift)
        else:
            ob.location = (x, y, z - settle * 1.2)
            ob.hide_render = settle > 0.95
            ob.keyframe_insert("hide_render", frame=f)
        ang = (d["w0"] / 2.4) * (1 - math.exp(-2.4 * (t_toss + settle)))
        if i == S.HERO_INDEX and settle > 0.85:
            ang *= (1 - (settle - 0.85) / 0.15)        # decays onto a camera-facing rest pose
        ob.rotation_mode = 'AXIS_ANGLE'
        ob.rotation_axis_angle = (ang, *d["axis"])
        ob.keyframe_insert("location", frame=f)
        ob.keyframe_insert("rotation_axis_angle", frame=f)

    # --- beat 4 + 6: explode, anticipate, slam ---
    for i, ob in enumerate(LAYER_OBJS):
        stag = min(1.0, max(0.0, (e_raw - i * 0.05) / (1 - i * 0.05)))
        spread = S.ease_back_out(stag) * (1 + antic * 0.08) * (1 - impact)
        ob.location = (0.0, 0.0, ob["rest_z"] + (i - S.CENTER_I) * 0.018 * spread)
        ob.rotation_euler = ((0.06 if i % 2 else -0.06) * spread, 0.0,
                             (-0.04 if i % 3 else 0.04) * spread)
        ob.keyframe_insert("location", frame=f)
        ob.keyframe_insert("rotation_euler", frame=f)

    # --- beat 5: half turn (stack axis is Z, so the turn is about Z) ---
    # --- beat 6: volume-preserving impact squash ---
    sy = 1 - 0.18 * shake
    sxy = 1 / math.sqrt(sy)
    HERO.rotation_mode = 'AXIS_ANGLE'
    HERO.scale = (sxy, sxy, sy)
    HERO.keyframe_insert("scale", frame=f)
    for i, ob in enumerate(LAYER_OBJS):
        under = min(1.0, max(0.0, 1 - abs(cutting - 0.5) * 4))
        ob.scale = (1.0, 1.0, 1 - 0.06 * under) if not split else (1, 1, 1)
        ob.keyframe_insert("scale", frame=f)

    # --- beat 7: the knife, the swap, the halves opening ---
    KNIFE.location = (0.0, 0.0, 0.34 - t_cut * 0.42)
    KNIFE.rotation_euler = (0.0, 0.22 - t_cut * 0.22, 0.0)
    KNIFE.hide_render = not (0.0 < t_cut < 0.95)
    KNIFE.keyframe_insert("location", frame=f)
    KNIFE.keyframe_insert("rotation_euler", frame=f)
    KNIFE.keyframe_insert("hide_render", frame=f)
    GLINT.location = (0.02, -0.10 + t_cut * 0.24, 0.30 - t_cut * 0.40)
    GLINT.data.energy = 12.0 if 0.05 < t_cut < 0.45 else 0.0
    GLINT.keyframe_insert("location", frame=f)
    GLINT.data.keyframe_insert("energy", frame=f)

    for ob in LAYER_OBJS:
        ob.hide_render = split
        ob.keyframe_insert("hide_render", frame=f)
    gap = opening * 0.020
    turn = math.radians(72) * opening
    # the right half's cut normal is -X and the left's is +X; these signs swing both
    # faces toward the lens at -Y. Reversed, one half turns its back to camera.
    HALF_R.location = (gap, -gap * 0.35, 0); HALF_R.rotation_euler = (0, 0, turn)
    HALF_L.location = (-gap, -gap * 0.35, 0); HALF_L.rotation_euler = (0, 0, -turn)
    for h in (HALF_L, HALF_R):
        h.keyframe_insert("location", frame=f)
        h.keyframe_insert("rotation_euler", frame=f)
    for ob in HALF_KIDS:
        ob.hide_render = not split
        ob.keyframe_insert("hide_render", frame=f)

    # --- loose sesame shaken free at the top of the toss ---
    for i, ob in enumerate(LOOSE):
        born = 0.45 + (i % 10) * 0.04
        a = max(0.0, (t_toss - born) / max(1e-3, 1 - born))
        ob.hide_render = not (0 < a < 1) or settle > 0.6
        ob.location = (S.noise1(i + 1) * 0.16 * a,
                       S.noise1(i + 9) * 0.16 * a,
                       0.05 + a * 0.30 - 2.2 * a * a * 0.30)
        ob.keyframe_insert("location", frame=f)
        ob.keyframe_insert("hide_render", frame=f)

def all_fcurves(act):
    """Blender 5.0 moved F-Curves into layered action slots; fall back to the legacy list."""
    if hasattr(act, "fcurves"):
        yield from act.fcurves
        return
    for layer in act.layers:
        for strip in layer.strips:
            for cb in getattr(strip, "channelbags", []):
                yield from cb.fcurves

# constant interpolation on visibility, linear elsewhere: the maths already carries the easing
for act in bpy.data.actions:
    for fc in all_fcurves(act):
        mode = 'CONSTANT' if 'hide_render' in fc.data_path else 'LINEAR'
        for kp in fc.keyframe_points:
            kp.interpolation = mode

# ------------------------------------------------------------------ lighting: food-commercial
def area(name, loc, rot, size, energy, color):
    d = bpy.data.lights.new(name, type='AREA'); d.size = size
    d.energy = energy; d.color = color
    ob = bpy.data.objects.new(name, d); S.link(ob, "LIGHTS")
    ob.location = loc; ob.rotation_euler = rot
    return ob

# KEY is behind and above: backlight is the whole language of food photography
area("KEY_back_left", (-0.40, 0.50, 0.55), (math.radians(52), 0, math.radians(-142)),
     0.55, 22.0, (1.0, 0.95, 0.88))
area("FILL_front_right", (0.50, -0.45, 0.16), (math.radians(80), 0, math.radians(48)),
     0.80, 1.1, (1.0, 0.97, 0.94))
area("RIM_brand_yellow", (0.26, 0.36, 0.48), (math.radians(58), 0, math.radians(150)),
     0.18, 4.5, (1.0, 0.92, 0.08))
area("KICK_brand_red", (0.52, 0.08, 0.04), (math.radians(90), 0, math.radians(80)),
     0.22, 2.2, (0.90, 0.07, 0.27))

world = bpy.data.worlds.new("SmashWorld"); sc.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.012, 0.010, 0.007, 1.0)   # near-black #13110C, linearised
bg.inputs[1].default_value = 1.0

# a matte dark surface so nothing floats: food sits in its ground
bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=2.0)
ground = S.new_mesh_object("ground_stone", bm, "LIGHTS")
ground.location = (0, 0, -0.0012)
S.assign(ground, S.make_material("MAT_ground_stone", (0.004, 0.0035, 0.0028), 0.92))

# ------------------------------------------------------------------ render settings
sc.render.engine = 'CYCLES'
sc.cycles.device = 'GPU'            # Metal on Apple Silicon
sc.cycles.samples = 512
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.01
sc.cycles.use_denoising = True
try:
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'      # OptiX is NVIDIA-only; this is the Mac path
except Exception:
    pass
sc.render.use_persistent_data = True   # it lives on render, not cycles
sc.render.use_motion_blur = True
sc.render.motion_blur_shutter = 0.5
sc.render.resolution_x, sc.render.resolution_y = S.RES_DESKTOP
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGB'
sc.render.image_settings.color_depth = '16'
sc.render.filepath = "//render/desktop/smash_"
sc.render.use_file_extension = True
for vt in ('AgX', 'Filmic', 'Standard'):
    try:
        sc.view_settings.view_transform = vt
        break
    except Exception:
        continue
sc.view_settings.look = 'None'

# ------------------------------------------------------------------ label anchor track
def export_labels(camera, res, path):
    frames = {}
    f_start = int(round(S.BEATS["explode"][0] * (S.FRAME_END - S.FRAME_START))) + S.FRAME_START
    f_end = int(round(S.BEATS["turn"][1] * (S.FRAME_END - S.FRAME_START))) + S.FRAME_START
    dg = bpy.context.evaluated_depsgraph_get()
    for f in range(f_start, f_end + 1):
        sc.frame_set(f)
        dg.update()
        entry = {}
        for L in S.LAYERS:
            ob = bpy.data.objects[L["name"]]
            world = ob.matrix_world.translation
            co = world_to_camera_view(sc, camera, world)
            entry[L["name"]] = [round(co.x, 4), round(1.0 - co.y, 4)]   # web origin is top-left
        frames[str(f)] = entry
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump({"resolution": list(res), "frames": frames}, open(path, "w"))
    return len(frames)

n1 = export_labels(cam, S.RES_DESKTOP, os.path.join(LABELS_DIR, "labels.desktop.json"))
n2 = export_labels(cam_p, S.RES_MOBILE, os.path.join(LABELS_DIR, "labels.mobile.json"))
sc.frame_set(S.FRAME_START)

print("keyed frames:", S.FRAME_END, "| actions:", len(bpy.data.actions))
print("label track frames:", n1, "desktop /", n2, "mobile")
print("view transform:", sc.view_settings.view_transform, "| engine:", sc.render.engine)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
