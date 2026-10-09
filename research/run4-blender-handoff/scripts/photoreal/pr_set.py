"""Environment and set dressing.

The biggest single tell that a food render is CG is that its glossy surfaces
reflect a black void with four bright rectangles in it. Real food is shot
inside a room. This module builds that room — a graded environment plus large
off-camera bounce panels — and dresses the surface the burger sits on, because
a featureless infinite plane gives the eye no scale to hold on to.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_boot  # must precede bpy
import bpy, bmesh, math, random
from mathutils import Vector
import pr_mat as M
import pr_geo as G

TAU = math.pi * 2.0


def world_gradient(strength=0.16):
    """A studio, not a void: warm above, near-black below, so every glossy
    surface has something graded to reflect."""
    w = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_WORLD':
            nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    el = ramp.color_ramp.elements
    el[0].position, el[0].color = 0.30, (0.004, 0.0035, 0.003, 1)
    el[1].position, el[1].color = 0.62, (0.085, 0.070, 0.055, 1)
    e = el.new(0.80); e.color = (0.190, 0.165, 0.140, 1)
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = strength
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    return w


def bounce_panels():
    """Large dull panels just outside the frame. They barely light anything;
    what they do is fill the reflections with soft shapes at different angles."""
    made = []
    spec = [
        ("PANEL_L", (-0.62, 0.05, 0.16), 0.9, 0.9, (0.55, 0.50, 0.46)),
        ("PANEL_R", (0.66, -0.06, 0.20), 0.9, 0.5, (0.60, 0.54, 0.48)),
        ("PANEL_TOP", (-0.05, -0.10, 0.70), 1.2, 0.35, (0.62, 0.58, 0.54)),
    ]
    for name, loc, size, power, col in spec:
        d = bpy.data.lights.new(name, 'AREA')
        d.shape = 'SQUARE'
        d.size = size
        d.energy = power
        d.color = col
        o = bpy.data.objects.new(name, d)
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (Vector((0, 0, 0.05)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        made.append(o)
    return made


def mat_board():
    """Dark oiled wood. Near-black so the brand's red and yellow still read,
    but with grain and a low sheen so it is obviously a surface, not a void."""
    m, nt, b = M._nt("MAT_board")
    tc = M._n(nt, "ShaderNodeTexCoord")
    mp = M._n(nt, "ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.0, 0.055, 1.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    grain = M._n(nt, "ShaderNodeTexNoise", Scale=26.0, Detail=9.0, Roughness=0.62)
    nt.links.new(mp.outputs["Vector"], grain.inputs["Vector"])
    pores = M._n(nt, "ShaderNodeTexNoise", Scale=420.0, Detail=5.0)
    nt.links.new(tc.outputs["Object"], pores.inputs["Vector"])
    c = M._ramp(nt, grain.outputs["Factor"], [(0.28, (0.0035, 0.0018, 0.0009, 1)),
                                              (0.55, (0.0130, 0.0070, 0.0032, 1)),
                                              (0.82, (0.0330, 0.0185, 0.0085, 1))])
    nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    rgh = M._ramp(nt, pores.outputs["Factor"], [(0.30, (0.22,) * 3 + (1,)),
                                                (0.75, (0.46,) * 3 + (1,))])
    nt.links.new(rgh.outputs["Color"], b.inputs["Roughness"])
    b.inputs["Specular IOR Level"].default_value = 0.55
    h = M._mix(nt, 0.4, grain.outputs["Factor"], pores.outputs["Factor"], "ADD")
    M._bump(nt, b, h, 0.28, 0.0009)
    return m


def board(size=0.9):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, -0.0004))
    g = bpy.context.active_object
    g.name = "board"
    M.assign(g, mat_board())
    return g


def crumbs(count=90, seed=17, r_in=0.062, r_out=0.20):
    """Crumbs, a few escaped sesame seeds and a scatter of crust flakes. Nothing
    sells scale like debris that is obviously smaller than the subject."""
    rnd = random.Random(seed)
    bm = bmesh.new()
    for _ in range(count):
        a = rnd.uniform(0, TAU)
        d = r_in + (r_out - r_in) * (rnd.random() ** 0.6)
        x, y = math.cos(a) * d, math.sin(a) * d
        s = rnd.uniform(0.0004, 0.0016)
        sm = bmesh.new()
        bmesh.ops.create_icosphere(sm, subdivisions=1, radius=1.0)
        for v in sm.verts:
            v.co.x *= s * rnd.uniform(0.7, 1.6)
            v.co.y *= s * rnd.uniform(0.7, 1.6)
            v.co.z *= s * rnd.uniform(0.35, 0.8)
            v.co += Vector((G.fbm(v.co * 900.0, 2),) * 3) * s * 0.35
        bmesh.ops.rotate(sm, verts=sm.verts,
                         matrix=__import__("mathutils").Matrix.Rotation(rnd.uniform(0, TAU), 3, 'Z'))
        bmesh.ops.translate(sm, vec=Vector((x, y, s * 0.3)), verts=sm.verts)
        tmp = bpy.data.meshes.new("crumb_tmp")
        sm.to_mesh(tmp); sm.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    me = bpy.data.meshes.new("crumbs")
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("crumbs", me)
    bpy.context.scene.collection.objects.link(ob)
    M.assign(ob, M.mat_bun())
    return ob
