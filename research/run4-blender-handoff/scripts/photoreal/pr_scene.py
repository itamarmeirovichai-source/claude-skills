"""Assemble, light and render the photoreal burger.

Run:  python3 pr_scene.py --still out/look_dev.png --res 960 --samples 64
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_boot  # must precede bpy
import bpy, math, sys, os, argparse
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_geo as G
import pr_mat as M
import pr_set as SET

# ---- the stack, bottom to top. Names are fixed by the asset contract. -------
Z_HEEL = 0.0000
Z_PATTY_L = 0.0168
Z_CHEESE_L = 0.0248
Z_PATTY_U = 0.0268
Z_CHEESE_U = 0.0348
Z_BACON = 0.0362
Z_ONION = 0.0392
Z_SAUCE = 0.0432
Z_CROWN = 0.0452

# Radii are staged deliberately: each patty is narrower than the cheese under
# the one above it, so every layer keeps an edge the camera can see. An ID-pass
# render of the first stack showed the upper patty hiding four layers at once.
R_PATTY_L = 0.0578
R_PATTY_U = 0.0525
HALF_CHEESE_L = 0.0615
HALF_CHEESE_U = 0.0580

LAYER_ORDER = ["bun_bottom", "patty_lower", "cheese_lower", "patty_upper",
               "cheese_upper", "bacon_beef", "onion_caramelized", "sauce_chef",
               "bun_top"]


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.scale_length = 1.0
    return sc


def build_burger():
    """Returns {layer name: object}. Every object's origin stays at the world
    origin so the site's exploded layout can move them on one axis."""
    obs = {}

    heel = G.build_bun("bun_bottom", G.HEEL_PROFILE, seed=2, crumb_amp=0.0009,
                       sx=0.965, sz=0.88)
    heel.location.z = Z_HEEL
    obs["bun_bottom"] = heel

    pl = G.build_patty("patty_lower", Z_PATTY_L, seed=11, r=R_PATTY_L, thick=0.0082)
    pu = G.build_patty("patty_upper", Z_PATTY_U, seed=29, r=R_PATTY_U, thick=0.0082)
    obs["patty_lower"], obs["patty_upper"] = pl, pu

    cl = G.build_cheese("cheese_lower", Z_CHEESE_L, rot=math.radians(24), seed=5,
                        drop=0.0095, half=HALF_CHEESE_L, flat_r=0.0450, drips=7)
    cu = G.build_cheese("cheese_upper", Z_CHEESE_U, rot=math.radians(-17), seed=8,
                        drop=0.0130, half=HALF_CHEESE_U, flat_r=0.0400, drips=9)
    obs["cheese_lower"], obs["cheese_upper"] = cl, cu

    obs["bacon_beef"] = G.build_bacon("bacon_beef", Z_BACON, seed=3)
    obs["onion_caramelized"] = G.build_onion("onion_caramelized", Z_ONION, seed=4)
    obs["sauce_chef"] = G.build_sauce("sauce_chef", Z_SAUCE, seed=6)

    crown = G.build_bun("bun_top", G.CROWN_PROFILE, seed=1, sx=0.985, sz=0.95)
    crown.location.z = Z_CROWN
    seeds = G.sesame_seeds(crown, count=130, seed=7)
    seeds.location.z = Z_CROWN
    obs["bun_top"] = crown
    obs["bun_top_seeds"] = seeds

    # materials
    bun, crumb = M.mat_bun(), M.mat_crumb()
    patty, patty_in = M.mat_patty(), M.mat_patty_interior()
    cheese, bacon = M.mat_cheese(), M.mat_bacon()
    onion, sauce = M.mat_onion(), M.mat_sauce()
    M.assign(heel, bun, crumb)
    M.assign(crown, bun, crumb)
    M.assign(seeds, M.mat_sesame())
    M.assign(pl, patty, patty_in)
    M.assign(pu, patty, patty_in)
    M.assign(cl, cheese)
    M.assign(cu, cheese)
    M.assign(obs["bacon_beef"], bacon)
    M.assign(obs["onion_caramelized"], onion)
    M.assign(obs["sauce_chef"], sauce)

    # nudge every layer off-centre and off-axis. A perfectly concentric stack
    # is the fastest way to tell a viewer they are looking at CG.
    SLIP = {
        "patty_lower":       (0.0018, -0.0012, 3.0),
        "cheese_lower":      (-0.0022, 0.0016, -7.0),
        "patty_upper":       (-0.0014, 0.0021, -5.0),
        "cheese_upper":      (0.0026, 0.0011, 11.0),
        "bacon_beef":        (0.0009, -0.0018, 6.0),
        "onion_caramelized": (-0.0011, -0.0009, -4.0),
        "sauce_chef":        (0.0013, 0.0007, 2.0),
        "bun_top":           (-0.0016, 0.0024, 9.0),
        "bun_top_seeds":     (-0.0016, 0.0024, 9.0),
    }
    for name, (dx, dy, rot) in SLIP.items():
        ob = obs.get(name)
        if not ob:
            continue
        ob.location.x += dx
        ob.location.y += dy
        ob.rotation_euler.z += math.radians(rot)
    # the crown settles under its own weight, so it is never a true dome
    crown.scale = (1.005, 0.982, 0.97)
    crown.rotation_euler.y += math.radians(1.6)
    seeds.scale = crown.scale
    seeds.rotation_euler.y = crown.rotation_euler.y

    for ob in obs.values():
        G.shade_auto_smooth(ob)

    root = bpy.data.objects.new("burger_hero", None)
    bpy.context.scene.collection.objects.link(root)
    for ob in obs.values():
        ob.parent = root
    return obs, root


def build_ground(dressed=True):
    if not dressed:
        bpy.ops.mesh.primitive_plane_add(size=3.0, location=(0, 0, -0.0004))
        g = bpy.context.active_object
        g.name = "ground"
        M.assign(g, M.mat_ground())
        return g
    g = SET.board(1.1)
    SET.crumbs()
    return g


def build_lights(dressed=False):
    """Studio food lighting: a big soft key from behind-left so the food glows
    at the edges, a hard strip for the top-rim glisten, a low fill to keep the
    shadows from going solid, and a warm kicker on the cheese drip."""
    made = []

    def area(name, loc, target, size, power, color, shape='SQUARE', sy=None):
        d = bpy.data.lights.new(name, 'AREA')
        d.shape = shape
        d.size = size
        if sy is not None:
            d.size_y = sy
        d.energy = power
        d.color = color
        o = bpy.data.objects.new(name, d)
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        dirv = (Vector(target) - Vector(loc))
        o.rotation_euler = dirv.to_track_quat('-Z', 'Y').to_euler()
        made.append(o)
        return o

    t = (0.0, 0.0, 0.046)
    # key: the big softbox back-left that puts the highlight along the top edge
    area("KEY", (-0.30, 0.34, 0.34), t, 0.80, 10.0, (1.0, 0.860, 0.680))
    # top: keeps the crown from going flat, and lights the sesame
    area("TOP", (0.02, 0.06, 0.52), (0.0, 0.0, 0.07), 0.80, 5.0, (1.0, 0.910, 0.820))
    # fill: stands in for the white bounce card just out of frame, camera right
    area("FILL", (0.42, -0.36, 0.14), t, 1.00, 4.6, (1.0, 0.885, 0.760))
    # rim: a hard strip directly behind for the wet glisten on cheese and sauce
    area("RIM", (0.06, 0.46, 0.20), t, 0.80, 4.2, (1.0, 0.955, 0.880),
         shape='RECTANGLE', sy=0.05)
    # kick: a small warm light low on the right, echoing the brand yellow
    area("KICK", (0.30, 0.03, 0.02), (0.0, 0.0, 0.028), 0.10, 1.4,
         (1.0, 0.70, 0.32))

    if not dressed:
        # with no floor there is no bounce from below, so put one in
        area("UNDER", (0.10, -0.16, -0.26), (0.0, 0.0, 0.030), 0.80, 1.6,
             (1.0, 0.86, 0.70))
    SET.world_gradient(0.16)
    made += SET.bounce_panels()
    return made


def build_camera(focal=85.0, dist=0.54, elev=24.0, azim=-34.0, fstop=11.0,
                 target=(0.0, 0.0, 0.042)):
    d = bpy.data.cameras.new("cam")
    d.lens = focal
    d.sensor_width = 36.0
    d.dof.use_dof = True
    d.dof.aperture_fstop = fstop
    cam = bpy.data.objects.new("camera", d)
    bpy.context.scene.collection.objects.link(cam)
    e, a = math.radians(elev), math.radians(azim)
    pos = Vector(target) + Vector((math.sin(a) * math.cos(e),
                                   -math.cos(a) * math.cos(e),
                                   math.sin(e))) * dist
    cam.location = pos
    cam.rotation_euler = (Vector(target) - pos).to_track_quat('-Z', 'Y').to_euler()
    d.dof.focus_distance = (Vector(target) - pos).length - 0.030
    bpy.context.scene.camera = cam
    return cam


def setup_render(res_x=1920, res_y=1080, samples=128, denoise=True):
    try:
        bpy.ops.preferences.addon_enable(module='cycles')
    except Exception:
        pass
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.012
    sc.cycles.max_bounces = 8
    sc.cycles.diffuse_bounces = 3
    sc.cycles.glossy_bounces = 4
    sc.cycles.transmission_bounces = 6
    sc.cycles.transparent_max_bounces = 4
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.use_denoising = denoise
    try:
        sc.cycles.denoiser = 'OPENIMAGEDENOISE'
        sc.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    except Exception:
        pass
    sc.render.use_persistent_data = True
    sc.render.resolution_x = res_x
    sc.render.resolution_y = res_y
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGB'
    vs = sc.view_settings
    try:
        vs.view_transform = 'AgX'
        vs.look = 'AgX - Punchy'
    except Exception:
        try:
            vs.view_transform = 'Filmic'
            vs.look = 'Medium High Contrast'
        except Exception:
            pass
    vs.exposure = 0.0
    vs.gamma = 1.0
    return sc


def build_scene(dressed=False, **cam_kw):
    """dressed=True puts the burger on a board for a hero still. The scroll
    sequence renders with a transparent film and no set at all: the burger is
    airborne for most of it, and the page supplies its own background — which
    also removes the brightest, flattest object in the frame."""
    reset()
    obs, root = build_burger()
    if dressed:
        build_ground()
    build_lights(dressed)
    cam = build_camera(**cam_kw)
    return obs, root, cam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", default="out/look_dev.png")
    ap.add_argument("--res", type=int, default=960)
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--focal", type=float, default=85.0)
    ap.add_argument("--dist", type=float, default=0.54)
    ap.add_argument("--elev", type=float, default=24.0)
    ap.add_argument("--azim", type=float, default=-34.0)
    ap.add_argument("--fstop", type=float, default=11.0)
    ap.add_argument("--exposure", type=float, default=-0.15)
    ap.add_argument("--blend", default="")
    ap.add_argument("--dressed", action="store_true")
    ap.add_argument("--alpha", action="store_true")
    a = ap.parse_args()

    build_scene(dressed=a.dressed, focal=a.focal, dist=a.dist, elev=a.elev,
                azim=a.azim, fstop=a.fstop)
    sc = setup_render(a.res, int(a.res * 9 / 16), a.samples)
    sc.view_settings.exposure = a.exposure
    if a.alpha:
        sc.render.film_transparent = True
        sc.render.image_settings.color_mode = 'RGBA'
    os.makedirs(os.path.dirname(os.path.abspath(a.still)), exist_ok=True)
    sc.render.filepath = os.path.abspath(a.still)
    if a.blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.blend))
    import time
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER_SECONDS %.1f" % (time.time() - t0))
    print("WROTE", sc.render.filepath)


if __name__ == "__main__":
    main()
