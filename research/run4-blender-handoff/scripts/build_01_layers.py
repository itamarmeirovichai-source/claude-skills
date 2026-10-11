"""Step 1-3: project setup, the nine named burger layers, sesame, photoreal-intent materials."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector
import smash_common as S

OUT = sys.argv[-1]

sc = S.reset_scene()
for name in S.COLLECTIONS + ["HERO", "CUT", "KNIFE", "LIGHTS", "CAMERA"]:
    S.get_collection(name)

# ---------------------------------------------------------------- materials
M = {}
M["bun"] = S.make_material("MAT_bun", (0.52, 0.28, 0.12), 0.58,
                           subsurface_weight=0.12, subsurface_scale=0.005,
                           specular_ior_level=0.35)
M["patty"] = S.make_material("MAT_patty_seared", (0.14, 0.062, 0.035), 0.42,
                             specular_ior_level=0.42)
M["cheese"] = S.make_material("MAT_cheese_plant_based", (0.80, 0.55, 0.18), 0.35,
                              coat_weight=0.15, subsurface_weight=0.06,
                              subsurface_scale=0.004)
M["bacon"] = S.make_material("MAT_bacon_beef", (0.33, 0.048, 0.030), 0.30,
                             specular_ior_level=0.5)
M["onion"] = S.make_material("MAT_onion_caramelized", (0.42, 0.21, 0.05), 0.38,
                             subsurface_weight=0.18, subsurface_scale=0.003)
M["sauce"] = S.make_material("MAT_sauce_chef", (0.60, 0.24, 0.06), 0.17,
                             coat_weight=0.30, ior=1.45)
M["sesame"] = S.make_material("MAT_sesame", (0.86, 0.74, 0.50), 0.45,
                              subsurface_weight=0.25, subsurface_scale=0.001)
M["interior"] = S.make_material("MAT_cut_interior", (0.70, 0.39, 0.29), 0.45,
                                subsurface_weight=0.30, subsurface_scale=0.006)
MAT_FOR = {
    "bun_bottom": "bun", "bun_top": "bun",
    "patty_lower": "patty", "patty_upper": "patty",
    "cheese_lower": "cheese", "cheese_upper": "cheese",
    "bacon_beef": "bacon", "onion_caramelized": "onion", "sauce_chef": "sauce",
}

# procedural surface break-up, so nothing reads as a perfect machined cylinder
def add_detail(mat, scale=220.0, strength=0.0035, rough_lo=0.30, rough_hi=0.62,
               color_var=0.35):
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    coord = nt.nodes.new("ShaderNodeTexCoord")
    base = tuple(bsdf.inputs["Base Color"].default_value)[:3]
    # darken/lighten the albedo with the same noise: real food is never one flat colour
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = tuple(c * (1 - color_var) for c in base) + (1,)
    cr.color_ramp.elements[1].color = tuple(min(1.0, c * (1 + color_var * 0.55)) for c in base) + (1,)
    cn = nt.nodes.new("ShaderNodeTexNoise")
    cn.inputs["Scale"].default_value = scale * 0.45
    cn.inputs["Detail"].default_value = 12.0
    nt.links.new(coord.outputs["Object"], cn.inputs["Vector"])
    nt.links.new(cn.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], bsdf.inputs["Base Color"])
    tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = scale
    tex.inputs["Detail"].default_value = 9.0
    tex.inputs["Roughness"].default_value = 0.62
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.85
    bump.inputs["Distance"].default_value = strength
    nt.links.new(coord.outputs["Object"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (rough_lo,) * 3 + (1,)
    ramp.color_ramp.elements[1].color = (rough_hi,) * 3 + (1,)
    tex2 = nt.nodes.new("ShaderNodeTexNoise"); tex2.inputs["Scale"].default_value = scale * 0.22
    nt.links.new(coord.outputs["Object"], tex2.inputs["Vector"])
    nt.links.new(tex2.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])

for k in ("bun", "patty", "bacon", "onion", "interior"):
    add_detail(M[k])
# the interior material has no users until the cut step, so pin it or Blender drops it on save
M["interior"].use_fake_user = True
add_detail(M["cheese"], scale=120, strength=0.0015, rough_lo=0.28, rough_hi=0.44, color_var=0.18)
add_detail(M["sauce"], scale=170, strength=0.0010, rough_lo=0.10, rough_hi=0.26, color_var=0.20)

# ---------------------------------------------------------------- the nine layers
def dome_top(ob, dome=0.022):
    """Round the bun crown so it is a bun, not a disc."""
    me = ob.data
    zmax = max(v.co.z for v in me.vertices)
    R = max(math.hypot(v.co.x, v.co.y) for v in me.vertices)
    for v in me.vertices:
        if v.co.z > zmax - 1e-4:
            r = math.hypot(v.co.x, v.co.y) / R
            v.co.z += dome * math.sqrt(max(0.0, 1.0 - r * r))

def squash_sides(ob, amount=0.06, seed=1):
    """Real smashed layers are not perfect circles."""
    rnd = random.Random(seed)
    phase = rnd.uniform(0, 6.28)
    for v in ob.data.vertices:
        a = math.atan2(v.co.y, v.co.x)
        k = 1.0 + amount * (math.sin(a * 3 + phase) * 0.5 + math.sin(a * 5 - phase) * 0.3)
        v.co.x *= k; v.co.y *= k

z = 0.0
layer_objs = []
for i, L in enumerate(S.LAYERS):
    ob = S.cylinder(L["name"], L["r"], L["h"], "HERO")
    if L["name"] == "bun_top":
        dome_top(ob)
    squash_sides(ob, amount=0.07 if "patty" in L["name"] else 0.045, seed=i + 3)
    # origin stays at the layer's own centre; the object is positioned, not the mesh
    ob.location = (0.0, 0.0, z + L["h"] / 2.0)
    ob["rest_z"] = z + L["h"] / 2.0
    ob["layer_index"] = i
    S.assign(ob, M[MAT_FOR[L["name"]]])
    layer_objs.append(ob)
    z += L["h"]

bun_top = bpy.data.objects["bun_top"]

# ---------------------------------------------------------------- sesame
seed_parent = bpy.data.objects.new("sesame_scatter", None)
S.link(seed_parent, "HERO")
seed_parent.parent = bun_top
seed_parent.location = (0, 0, 0)

bm = bmesh.new()
bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=0.0022)
for v in bm.verts:
    v.co.z *= 0.45; v.co.x *= 1.35
seed_me = bpy.data.meshes.new("sesame_seed_mesh")
bm.to_mesh(seed_me); bm.free()
for f in seed_me.polygons:
    f.use_smooth = True
seed_me.materials.append(M["sesame"])

rnd = random.Random(7)
R, DOME = S.LAYERS[-1]["r"], 0.022
placed = 0
for n in range(150):
    a = rnd.uniform(0, 2 * math.pi)
    rr = math.sqrt(rnd.uniform(0, 1)) * 0.86
    x, y = math.cos(a) * rr * R, math.sin(a) * rr * R
    zz = S.LAYERS[-1]["h"] / 2.0 + DOME * math.sqrt(max(0.0, 1 - rr * rr)) - 0.0008
    if rr > 0.35 and rr < 0.5 and rnd.random() < 0.6:
        continue  # a deliberate bald patch — perfectly even sesame reads as CG
    if rnd.random() > 0.42:
        continue
    ob = bpy.data.objects.new("sesame_%02d" % placed, seed_me)
    S.link(ob, "HERO")
    ob.parent = seed_parent
    ob.location = (x, y, zz)
    ob.rotation_euler = (rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), rnd.uniform(0, 6.28))
    s = rnd.uniform(0.85, 1.2); ob.scale = (s, s, s)
    placed += 1

# thirty loose seeds that shake free during the toss
for i in range(30):
    ob = bpy.data.objects.new("seed_loose_%02d" % (i + 1), seed_me)
    S.link(ob, "BEAT_01_TOSS")
    ob.location = (rnd.uniform(-0.05, 0.05), rnd.uniform(-0.05, 0.05), S.STACK_H + 0.02)
    ob.hide_render = True  # enabled by the animation step

print("layers:", len(layer_objs), "| sesame on bun:", placed,
      "| stack height cm:", round(S.STACK_H * 100, 1))
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
