"""Step 12: bake the real-time glTF pair, with the exact contract mesh names."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
import smash_common as S

SRC, OUTDIR = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
sc.frame_set(S.FRAME_START)
os.makedirs(OUTDIR, exist_ok=True)

def rest(ob, z=None):
    ob.animation_data_clear()
    ob.rotation_mode = 'XYZ'
    ob.location = (0.0, 0.0, ob.get("rest_z", 0.0) if z is None else z)
    ob.rotation_euler = (0, 0, 0)
    ob.scale = (1, 1, 1)

for name in S.TOSS_NAMES:
    rest(bpy.data.objects[name], 0.0)
for L in S.LAYERS:
    rest(bpy.data.objects[L["name"]])

def export(objs, path, draco=True):
    for o in bpy.data.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    kw = dict(filepath=path, export_format='GLB', use_selection=True,
              export_apply=True, export_animations=False, export_yup=True)
    if draco:
        kw.update(export_draco_mesh_compression_enable=True,
                  export_draco_mesh_compression_level=6)
    try:
        bpy.ops.export_scene.gltf(**kw)
        return True, draco
    except Exception as e:
        if draco:
            print("Draco unavailable (%s) — exporting uncompressed" % type(e).__name__)
            return export(objs, path, draco=False)
        print("export failed:", e)
        return False, False

layers = [bpy.data.objects[L["name"]] for L in S.LAYERS]
ok1, d1 = export(layers, os.path.join(OUTDIR, "hero.glb"))

# the contract names the halves and the cut faces as meshes, so build real meshes for them
def merge(children, name, only_tagged):
    bm = bmesh.new()
    for ch in children:
        me = ch.data
        att = me.attributes.get("cut_face")
        tmp = bmesh.new(); tmp.from_mesh(me)
        tmp.faces.ensure_lookup_table()
        if only_tagged is not None and att is not None:
            drop = [f for i, f in enumerate(tmp.faces)
                    if bool(att.data[i].value) != only_tagged]
            bmesh.ops.delete(tmp, geom=drop, context='FACES')
        bmesh.ops.translate(tmp, verts=list(tmp.verts), vec=ch.location)
        t = bpy.data.meshes.new("tmp"); tmp.to_mesh(t); tmp.free()
        bm.from_mesh(t); bpy.data.meshes.remove(t)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    S.link(ob, "CUT")
    return ob

exports = []
for side, empty_name in (("left", "burger_half_left"), ("right", "burger_half_right")):
    empty = bpy.data.objects[empty_name]
    kids = [o for o in empty.children if o.type == 'MESH']
    rest(empty, 0.0)
    # free the contract names from the empties FIRST, or Blender appends .001 to the meshes
    empty.name = empty_name + "_pivot"
    marker = bpy.data.objects.get("cut_face_" + side)
    if marker:
        marker.name = "cut_face_%s_pivot" % side
    whole = merge(kids, empty_name, None)
    face = merge(kids, "cut_face_" + side, True)
    exports += [whole, face]

for n in ("knife_blade", "knife_handle"):
    ob = bpy.data.objects[n]
    ob.animation_data_clear()
    exports.append(ob)
bpy.data.objects["knife"].animation_data_clear()
ok2, d2 = export(exports, os.path.join(OUTDIR, "halves.glb"))

for f in ("hero.glb", "halves.glb"):
    p = os.path.join(OUTDIR, f)
    if os.path.exists(p):
        print("%-12s %7.2f MB" % (f, os.path.getsize(p) / 1e6))
print("draco:", d1 and d2)
print("contract names exported:",
      [o.name for o in layers] + [o.name for o in exports])
