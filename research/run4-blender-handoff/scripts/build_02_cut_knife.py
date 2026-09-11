"""Step 4-5: the pre-split halves with real modelled interior faces, the knife, the five toss burgers."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector
import smash_common as S

SRC, OUT = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=SRC)

base_interior = bpy.data.materials["MAT_cut_interior"]
rnd = random.Random(11)

def interior_for(layer_name):
    """One interior material per layer, so the cross-section actually reads as a burger."""
    name = "MAT_cut_" + layer_name
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = base_interior.copy()
        mat.name = name
        col = S.INTERIOR_COLORS[layer_name]
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        for node in mat.node_tree.nodes:
            if node.type == 'VALTORGB' and node.outputs[0].links and \
               node.outputs[0].links[0].to_socket.name == "Base Color":
                node.color_ramp.elements[0].color = tuple(c * 0.72 for c in col) + (1,)
                node.color_ramp.elements[1].color = tuple(min(1.0, c * 1.18) for c in col) + (1,)
                break
        else:
            bsdf.inputs["Base Color"].default_value = (*col, 1.0)
        mat.use_fake_user = True
    return mat

def half_of(src_ob, sign, parent, index):
    """Bisect a layer at x=0 and build a real interior face on the cut — never a flat boolean."""
    bm = bmesh.new()
    bm.from_mesh(src_ob.data)
    tag = bm.faces.layers.int.new("cut_face")   # tag at creation; normals lie near the cut
    res = bmesh.ops.bisect_plane(
        bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces),
        plane_co=(0, 0, 0), plane_no=(1.0, 0, 0),
        clear_outer=(sign > 0), clear_inner=(sign < 0))
    border = [e for e in bm.edges if len(e.link_faces) == 1]
    fill = bmesh.ops.holes_fill(bm, edges=border)
    for f in fill["faces"]:
        f[tag] = 1
    # the silhouette edge must stay clean, so remember it before subdividing
    rim_verts = {v for e in border for v in e.verts}
    # poke fans the cap into triangles around new INTERIOR verts, leaving the silhouette
    # rim untouched — subdividing the bevelled, non-planar boundary produced shards instead
    caps = list(fill["faces"])
    for _ in range(2):
        res_poke = bmesh.ops.poke(bm, faces=caps)
        caps = list(res_poke["faces"])
        for f in caps:
            f[tag] = 1
    bm.faces.ensure_lookup_table()
    # break the interior up so it reads as food, never as a flat boolean plane
    for f in bm.faces:
        if not f[tag]:
            continue
        for v in f.verts:
            if v in rim_verts:
                continue
            v.co.x += sign * rnd.uniform(0.00004, 0.00028)
            v.co.z += rnd.uniform(-0.00008, 0.00008)
    flags = [f[tag] for f in bm.faces]
    me = bpy.data.meshes.new("%s_%s" % (src_ob.name, "R" if sign > 0 else "L"))
    bm.to_mesh(me); bm.free()
    me.materials.append(src_ob.data.materials[0])
    interior = interior_for(src_ob.name)
    me.materials.append(interior)
    for i_f, f in enumerate(me.polygons):
        is_cut = bool(flags[i_f]) if i_f < len(flags) else False
        f.material_index = 1 if is_cut else 0
        f.use_smooth = not is_cut
    ob = bpy.data.objects.new(me.name, me)
    S.link(ob, "CUT")
    ob.parent = parent
    ob.location = src_ob.location
    ob["layer_index"] = index
    ob["rest_z"] = src_ob["rest_z"]
    return ob

halves = {}
for sign, name in ((-1, "burger_half_left"), (1, "burger_half_right")):
    empty = bpy.data.objects.new(name, None)
    S.link(empty, "CUT")
    empty.empty_display_size = 0.04
    halves[name] = empty
    for i, L in enumerate(S.LAYERS):
        half_of(bpy.data.objects[L["name"]], sign, empty, i)
    # a named marker for the cut face, so the glTF carries the contract name
    face_marker = bpy.data.objects.new(
        "cut_face_left" if sign < 0 else "cut_face_right", None)
    S.link(face_marker, "CUT")
    face_marker.parent = empty
    face_marker.empty_display_size = 0.03
    halves[name].hide_render = True
for ob in bpy.data.collections["CUT"].objects:
    ob.hide_render = True   # revealed by the animation step at the cut beat

# ------------------------------------------------------------------ knife
steel = S.make_material("MAT_knife_steel", (0.80, 0.83, 0.86), 0.14, metallic=1.0)
wood = S.make_material("MAT_knife_handle", (0.09, 0.065, 0.05), 0.62)

bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
for v in bm.verts:
    v.co.x *= 0.0016; v.co.y *= 0.20; v.co.z *= 0.055
# taper to a real edge at the bottom, or the glint has nothing to run along
for v in bm.verts:
    if v.co.z < 0:
        v.co.x *= 0.12
bmesh.ops.bevel(bm, geom=list(bm.edges) + list(bm.verts), offset=0.0004, segments=2, affect='EDGES')
blade = S.new_mesh_object("knife_blade", bm, "KNIFE")
S.assign(blade, steel)

bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
for v in bm.verts:
    v.co.x *= 0.009; v.co.y *= 0.075; v.co.z *= 0.017
bmesh.ops.bevel(bm, geom=list(bm.edges), offset=0.004, segments=3, affect='EDGES')
handle = S.new_mesh_object("knife_handle", bm, "KNIFE")
handle.location = (0, -0.135, 0)
S.assign(handle, wood)

knife = bpy.data.objects.new("knife", None)
S.link(knife, "KNIFE")
knife.empty_display_size = 0.05
blade.parent = knife
handle.parent = knife
for ob in (knife, blade, handle):
    ob.hide_render = True

# the glint: a narrow area light that sweeps the blade. Render-only, never exported.
gl = bpy.data.lights.new("knife_glint", type='AREA')
gl.shape = 'RECTANGLE'; gl.size = 0.006; gl.size_y = 0.30; gl.energy = 0.0
glint = bpy.data.objects.new("knife_glint", gl)
S.link(glint, "KNIFE")

# ------------------------------------------------------------------ five tossed burgers
hero_parent = bpy.data.objects.new(S.TOSS_NAMES[S.HERO_INDEX], None)
S.link(hero_parent, "HERO")
hero_parent.empty_display_size = 0.06
for L in S.LAYERS:
    bpy.data.objects[L["name"]].parent = hero_parent
bpy.data.objects["sesame_scatter"].parent = bpy.data.objects["bun_top"]

# the other four are only ever seen mid-air and blurred: one joined body each
bm = bmesh.new()
for L in S.LAYERS:
    src = bpy.data.objects[L["name"]]
    tmp = bmesh.new(); tmp.from_mesh(src.data)
    bmesh.ops.translate(tmp, verts=list(tmp.verts), vec=src.location)
    me = bpy.data.meshes.new("tmp"); tmp.to_mesh(me); tmp.free()
    bm.from_mesh(me); bpy.data.meshes.remove(me)
body = bpy.data.meshes.new("burger_toss_body")
bm.to_mesh(body); bm.free()
body.materials.append(bpy.data.materials["MAT_bun"])
for f in body.polygons:
    f.use_smooth = True

for i, name in enumerate(S.TOSS_NAMES):
    if i == S.HERO_INDEX:
        continue
    parent = bpy.data.objects.new(name, None)
    S.link(parent, "BEAT_01_TOSS")
    parent.empty_display_size = 0.06
    child = bpy.data.objects.new(name + "_body", body)
    S.link(child, "BEAT_01_TOSS")
    child.parent = parent

print("halves:", [o.name for o in bpy.data.collections["CUT"].objects if o.type == 'EMPTY'])
print("cut face polys left:",
      sum(1 for ob in bpy.data.collections["CUT"].objects if ob.type == 'MESH'
          for f in ob.data.polygons if f.material_index == 1))
print("toss burgers:", [o.name for o in bpy.data.objects if o.name in S.TOSS_NAMES])
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
