"""Render raw base colour with no lighting — the only honest way to judge an
albedo, because AgX plus a bright key can make almost anything look like clay."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_boot, bpy, argparse
import pr_scene as S

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="../../out/look/albedo.png")
ap.add_argument("--res", type=int, default=520)
a = ap.parse_args()

S.build_scene()
sc = S.setup_render(a.res, int(a.res * 9 / 16), 24)
sc.view_settings.view_transform = 'Standard'
sc.view_settings.exposure = 0.0
for m in bpy.data.materials:
    nt = getattr(m, "node_tree", None)
    if not nt or "Principled BSDF" not in nt.nodes:
        continue
    b, out = nt.nodes["Principled BSDF"], nt.nodes["Material Output"]
    em = nt.nodes.new("ShaderNodeEmission")
    src = b.inputs["Base Color"]
    if src.is_linked:
        nt.links.new(src.links[0].from_socket, em.inputs["Color"])
    else:
        em.inputs["Color"].default_value = src.default_value
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
sc.render.filepath = os.path.abspath(a.out)
bpy.ops.render.render(write_still=True)
print("WROTE", sc.render.filepath)
