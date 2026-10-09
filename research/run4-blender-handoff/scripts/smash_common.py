"""Shared definitions for the Smash House Blender build.
Every name here comes from the asset contract and must not be changed."""
import bpy, bmesh, math
from mathutils import Vector

FPS = 30
FRAME_START, FRAME_END = 1, 248
RES_DESKTOP = (1920, 1080)
RES_MOBILE = (1080, 1440)

# progress ranges, identical to the website's BEATS table
BEATS = {
    "toss": (0.00, 0.11), "bullet": (0.11, 0.21), "closeup": (0.21, 0.31),
    "explode": (0.31, 0.50), "turn": (0.50, 0.59), "smash": (0.59, 0.69),
    "cut": (0.69, 0.86), "slice": (0.86, 1.00),
}
COLLECTIONS = ["BEAT_01_TOSS", "BEAT_02_BULLET", "BEAT_03_CLOSEUP", "BEAT_04_EXPLODE",
               "BEAT_05_TURN", "BEAT_06_SMASH", "BEAT_07_CUT", "BEAT_08_SLICE"]

# bottom to top; stack axis is +Z. radius/height in metres (a real burger is ~11cm across)
LAYERS = [
    dict(name="bun_bottom",        r=0.055, h=0.022, color=(0.62, 0.36, 0.17)),
    dict(name="patty_lower",       r=0.058, h=0.013, color=(0.16, 0.07, 0.04)),
    dict(name="cheese_lower",      r=0.056, h=0.004, color=(0.80, 0.55, 0.18)),
    dict(name="patty_upper",       r=0.058, h=0.013, color=(0.16, 0.07, 0.04)),
    dict(name="cheese_upper",      r=0.056, h=0.004, color=(0.80, 0.55, 0.18)),
    dict(name="bacon_beef",        r=0.052, h=0.005, color=(0.34, 0.05, 0.03)),
    dict(name="onion_caramelized", r=0.050, h=0.006, color=(0.42, 0.21, 0.05)),
    dict(name="sauce_chef",        r=0.051, h=0.003, color=(0.60, 0.24, 0.06)),
    dict(name="bun_top",           r=0.055, h=0.040, color=(0.68, 0.40, 0.19)),
]
# what each layer looks like INSIDE — this is the shot the whole site is built around,
# so a single flat interior colour across all nine layers is not acceptable
INTERIOR_COLORS = {
    "bun_bottom":        (0.86, 0.74, 0.55),
    "bun_top":           (0.88, 0.77, 0.58),
    "patty_lower":       (0.45, 0.14, 0.10),
    "patty_upper":       (0.45, 0.14, 0.10),
    "cheese_lower":      (0.86, 0.63, 0.22),
    "cheese_upper":      (0.86, 0.63, 0.22),
    "bacon_beef":        (0.38, 0.07, 0.05),
    "onion_caramelized": (0.55, 0.32, 0.10),
    "sauce_chef":        (0.62, 0.26, 0.07),
}

STACK_H = sum(L["h"] for L in LAYERS)
CENTER_I = (len(LAYERS) - 1) / 2.0
TOSS_NAMES = ["burger_toss_a", "burger_toss_b", "burger_toss_c",
              "burger_toss_d", "burger_toss_e"]
HERO_INDEX = 2  # burger_toss_c is the hero, per the contract


def p_of(frame):
    """Scroll progress for a frame — the single source of truth for every beat."""
    return (frame - FRAME_START) / float(FRAME_END - FRAME_START)


def local(p, beat):
    a, b = BEATS[beat]
    return min(1.0, max(0.0, (p - a) / (b - a)))


def ease_back_out(t, s=1.6):
    t -= 1.0
    return t * t * ((s + 1) * t + s) + 1.0


def ease_expo_in(t):
    return 0.0 if t <= 0 else pow(2, 10 * (t - 1))


def noise1(x):
    s = math.sin(x * 127.1) * 43758.5453
    return (s - math.floor(s)) - 0.5


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.length_unit = 'CENTIMETERS'
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = FRAME_START, FRAME_END
    return sc


def get_collection(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def link(obj, collection_name):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    get_collection(collection_name).objects.link(obj)


def new_mesh_object(name, bm, collection):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    link(ob, collection)
    return ob


def cylinder(name, radius, height, collection, segments=64, taper=0.97):
    """A layer cylinder whose origin sits at its own geometric centre."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                          radius1=radius, radius2=radius * taper, depth=height)
    rim = [e for e in bm.edges
           if len(e.link_faces) == 2
           and any(abs(f.normal.z) > 0.7 for f in e.link_faces)]
    bmesh.ops.bevel(bm, geom=rim, offset=min(height * 0.22, radius * 0.05),
                    segments=3, affect='EDGES')
    for f in bm.faces:
        f.smooth = True
    return new_mesh_object(name, bm, collection)


def set_input(bsdf, name, value):
    if name in bsdf.inputs:
        try:
            bsdf.inputs[name].default_value = value
            return True
        except Exception:
            pass
    return False


def make_material(name, base_color, roughness=0.5, **kw):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (*base_color, 1.0))
    set_input(bsdf, "Roughness", roughness)
    for k, v in kw.items():
        set_input(bsdf, k.replace("_", " ").title().replace("Ior", "IOR"), v)
    return mat


def assign(ob, mat):
    ob.data.materials.clear()
    ob.data.materials.append(mat)
