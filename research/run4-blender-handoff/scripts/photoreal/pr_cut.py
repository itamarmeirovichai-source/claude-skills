"""Pre-split halves with real modelled interior faces.

A burger cut in half is the shot the whole site is built around, so the cross
section is modelled, not faked with a clipping plane: each layer is bisected at
x = 0, the hole is filled, the new faces are tagged at creation (their normals
lie near the cut, so classifying them afterwards by normal gets side faces
wrong) and given that layer's own interior material.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_boot  # must precede bpy
import bpy, bmesh, random
import pr_mat as M

# what each layer looks like on the inside. A single flat colour across all
# nine layers is what made the first attempt read as plastic.
INTERIOR = {
    "bun_bottom":        (0.620, 0.455, 0.250),
    "bun_top":           (0.650, 0.485, 0.275),
    "patty_lower":       (0.245, 0.072, 0.040),
    "patty_upper":       (0.245, 0.072, 0.040),
    "cheese_lower":      (0.780, 0.360, 0.055),
    "cheese_upper":      (0.780, 0.360, 0.055),
    "bacon_beef":        (0.180, 0.038, 0.020),
    "onion_caramelized": (0.300, 0.130, 0.032),
    "sauce_chef":        (0.420, 0.140, 0.035),
}


def interior_material(layer):
    name = "MAT_inside_" + layer
    m = bpy.data.materials.get(name)
    if m:
        return m
    m, nt, b = M._nt(name)
    col = INTERIOR[layer]
    n = M._noise(nt, 260.0, detail=8.0)
    c = M._ramp(nt, n.outputs["Factor"], [
        (0.28, tuple(v * 0.42 for v in col) + (1,)),
        (0.52, col + (1,)),
        (0.78, tuple(min(1.0, v * 1.45) for v in col) + (1,)),
    ])
    holes = M._n(nt, "ShaderNodeTexVoronoi", Scale=150.0, Randomness=1.0)
    nt.links.new(M._n(nt, "ShaderNodeTexCoord").outputs["Object"], holes.inputs["Vector"])
    pocket = M._ramp(nt, holes.outputs["Distance"], [(0.008, (0.0, 0.0, 0.0, 1)),
                                                     (0.075, (1.0, 1.0, 1.0, 1))])
    base = M._mix(nt, pocket.outputs["Color"],
                  tuple(v * 0.45 for v in col) + (1,), c.outputs["Color"])
    nt.links.new(base, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.42
    b.inputs["Subsurface Weight"].default_value = 0.18
    b.inputs["Subsurface Radius"].default_value = (0.010, 0.005, 0.003)
    b.inputs["Subsurface Scale"].default_value = 0.005
    b.inputs["Coat Weight"].default_value = 0.20
    b.inputs["Coat Roughness"].default_value = 0.16
    h = M._mix(nt, 0.45, n.outputs["Factor"], holes.outputs["Distance"], "ADD")
    M._bump(nt, b, h, 0.55, 0.0016)
    m.use_fake_user = True
    return m


def half_of(src, sign, parent, seed=11):
    """sign -1 keeps x < 0, sign +1 keeps x > 0.

    The cut face is filled with triangle_fill, not holes_fill: the boundary left
    by a bisect is several separate planar loops (the crust, the crumb cavity,
    a sesame seed caught by the blade), and holes_fill spans them all with one
    n-gon, which poke then fans into what looks like a folded paper fan.
    """
    rnd = random.Random(seed + (0 if sign < 0 else 97))
    bm = bmesh.new()
    bm.from_mesh(src.data)
    # create the tag layer first: adding a custom-data layer later invalidates
    # every BMFace reference already held in Python
    tag = bm.faces.layers.int.new("cut_face")
    res = bmesh.ops.bisect_plane(
        bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces),
        plane_co=(0.00007, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0),
        clear_outer=(sign > 0), clear_inner=(sign < 0))
    cut_edges = [e for e in res.get("geom_cut", []) if isinstance(e, bmesh.types.BMEdge)]
    if not cut_edges:
        bm.free()
        return None
    rim = {v for e in cut_edges for v in e.verts}
    filled = bmesh.ops.triangle_fill(bm, edges=cut_edges, use_beauty=True,
                                     normal=(1.0 if sign > 0 else -1.0, 0.0, 0.0))
    caps = [g for g in filled["geom"] if isinstance(g, bmesh.types.BMFace)]
    if not caps:
        bm.free()
        return None
    # Leave the cap flat. Poking it and jittering the new verts put a visible
    # radial crease pattern across the crumb — the material's bump does the
    # same job without drawing a wheel on every cut face.
    for f in caps:
        f[tag] = 1
    bm.normal_update()
    flags = [f[tag] for f in bm.faces]
    me = bpy.data.meshes.new("%s_%s" % (src.name, "R" if sign > 0 else "L"))
    bm.to_mesh(me)
    bm.free()
    me.materials.append(src.data.materials[0])
    me.materials.append(interior_material("bun_top" if src.name.endswith("_seeds")
                                          else src.name))
    for i, f in enumerate(me.polygons):
        cut = bool(flags[i]) if i < len(flags) else False
        f.material_index = 1 if cut else 0
        f.use_smooth = not cut
    ob = bpy.data.objects.new(me.name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = parent
    ob.location = src.location
    ob.rotation_euler = src.rotation_euler
    ob.scale = src.scale
    return ob


def build_halves(obs, root):
    """Returns (left_empty, right_empty, {name: [left_ob, right_ob]})."""
    out = {}
    empties = {}
    for sign, nm in ((-1, "burger_half_left"), (1, "burger_half_right")):
        e = bpy.data.objects.new(nm, None)
        bpy.context.scene.collection.objects.link(e)
        e.parent = root
        empties[sign] = e
    for name, src in obs.items():
        pair = []
        for sign in (-1, 1):
            h = half_of(src, sign, empties[sign])
            if h is not None:
                pair.append(h)
        out[name] = pair
    for e in empties.values():
        for c in e.children:
            c.hide_render = True
        e.hide_render = True
    return empties[-1], empties[1], out
