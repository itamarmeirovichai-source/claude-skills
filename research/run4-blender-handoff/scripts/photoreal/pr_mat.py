"""Materials for the photoreal burger.

Every surface is built from procedural nodes — no image textures, because the
build environment cannot download any. The point of each one is written above
it so the values can be argued with rather than guessed at again.
"""
import bpy


def _nt(name):
    m = bpy.data.materials.get(name)
    if m:
        return m, m.node_tree, m.node_tree.nodes["Principled BSDF"]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.use_fake_user = True
    nt = m.node_tree
    return m, nt, nt.nodes["Principled BSDF"]


def _n(nt, kind, **kw):
    n = nt.nodes.new(kind)
    for k, v in kw.items():
        if k in n.inputs:
            n.inputs[k].default_value = v
        else:
            setattr(n, k, v)
    return n


def _noise(nt, scale, detail=8.0, rough=0.55, w=0.0, distortion=0.0, coord="Object"):
    tc = _n(nt, "ShaderNodeTexCoord")
    ns = _n(nt, "ShaderNodeTexNoise", Scale=scale, Detail=detail,
            Roughness=rough, Distortion=distortion)
    nt.links.new(tc.outputs[coord], ns.inputs["Vector"])
    return ns


def _ramp(nt, src, stops):
    r = _n(nt, "ShaderNodeValToRGB")
    el = r.color_ramp.elements
    while len(el) > 1:
        el.remove(el[-1])
    el[0].position, el[0].color = stops[0]
    for pos, col in stops[1:]:
        e = el.new(pos)
        e.color = col
    nt.links.new(src, r.inputs["Factor"])
    return r


def _mix(nt, fac, a, b, blend="MIX"):
    m = _n(nt, "ShaderNodeMix", data_type="RGBA", blend_type=blend)
    if hasattr(fac, "node"):
        nt.links.new(fac, m.inputs["Factor"])
    else:
        m.inputs["Factor"].default_value = fac
    if hasattr(a, "bl_idname") or hasattr(a, "node"):
        nt.links.new(a, m.inputs[6])
    else:
        m.inputs[6].default_value = a
    if hasattr(b, "bl_idname") or hasattr(b, "node"):
        nt.links.new(b, m.inputs[7])
    else:
        m.inputs[7].default_value = b
    return m.outputs[2]


def _bump(nt, bsdf, height, strength=0.4, distance=0.002):
    b = _n(nt, "ShaderNodeBump", Strength=strength, Distance=distance)
    nt.links.new(height, b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], bsdf.inputs["Normal"])
    return b


# ------------------------------------------------------------------ bun
def mat_bun():
    """Brioche crust. One ramp drives the bake: half of it is height on the
    dome (the oven hits the top hardest), half is a broad blotch noise, so no
    two parts of the crust are the same golden."""
    m, nt, b = _nt("MAT_bun_crust")
    big = _noise(nt, 16.0, detail=6.0, rough=0.68, distortion=0.8)
    fine = _noise(nt, 520.0, detail=8.0, rough=0.62)
    pores = _n(nt, "ShaderNodeTexVoronoi", Scale=260.0, Randomness=1.0)
    nt.links.new(_n(nt, "ShaderNodeTexCoord").outputs["Object"], pores.inputs["Vector"])

    sep = _n(nt, "ShaderNodeSeparateXYZ")
    nt.links.new(_n(nt, "ShaderNodeTexCoord").outputs["Object"], sep.inputs["Vector"])
    bake = _n(nt, "ShaderNodeMapRange", **{"From Min": 0.0, "From Max": 0.040,
                                          "To Min": 0.20, "To Max": 0.86})
    nt.links.new(sep.outputs["Z"], bake.inputs["Value"])

    mixer = _n(nt, "ShaderNodeMix", data_type='FLOAT')
    mixer.inputs["Factor"].default_value = 0.52
    nt.links.new(bake.outputs["Result"], mixer.inputs[2])
    nt.links.new(big.outputs["Factor"], mixer.inputs[3])

    crust = _ramp(nt, mixer.outputs[0], [
        (0.16, (0.032, 0.010, 0.003, 1)),
        (0.34, (0.080, 0.027, 0.008, 1)),
        (0.50, (0.155, 0.060, 0.018, 1)),
        (0.66, (0.265, 0.120, 0.038, 1)),
        (0.86, (0.400, 0.210, 0.078, 1)),
    ])
    # the fine grain only lightens, never recolours
    lift = _n(nt, "ShaderNodeMix", data_type='RGBA', blend_type='OVERLAY')
    lift.inputs["Factor"].default_value = 0.12
    nt.links.new(crust.outputs["Color"], lift.inputs[6])
    nt.links.new(fine.outputs["Color"], lift.inputs[7])
    nt.links.new(lift.outputs[2], b.inputs["Base Color"])

    rgh = _ramp(nt, fine.outputs["Factor"], [(0.25, (0.26,) * 3 + (1,)),
                                             (0.75, (0.46,) * 3 + (1,))])
    nt.links.new(rgh.outputs["Color"], b.inputs["Roughness"])
    b.inputs["Subsurface Weight"].default_value = 0.07
    b.inputs["Subsurface Radius"].default_value = (0.008, 0.004, 0.002)
    b.inputs["Subsurface Scale"].default_value = 0.005
    b.inputs["Sheen Weight"].default_value = 0.06
    b.inputs["Sheen Roughness"].default_value = 0.40
    b.inputs["Specular IOR Level"].default_value = 0.62
    b.inputs["Coat Weight"].default_value = 0.08
    b.inputs["Coat Roughness"].default_value = 0.35

    h = _mix(nt, 0.45, fine.outputs["Factor"], pores.outputs["Distance"], "ADD")
    _bump(nt, b, h, strength=0.50, distance=0.0009)
    return m


def mat_sesame():
    m, nt, b = _nt("MAT_sesame")
    n = _noise(nt, 320.0, detail=4.0)
    c = _ramp(nt, n.outputs["Factor"], [(0.25, (0.185, 0.115, 0.050, 1)),
                                        (0.52, (0.360, 0.250, 0.125, 1)),
                                        (0.80, (0.560, 0.430, 0.245, 1))])
    nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.40
    b.inputs["Subsurface Weight"].default_value = 0.25
    b.inputs["Subsurface Radius"].default_value = (0.004, 0.003, 0.002)
    b.inputs["Subsurface Scale"].default_value = 0.003
    _bump(nt, b, n.outputs["Factor"], 0.2, 0.0004)
    return m


# ------------------------------------------------------------------ patty
def mat_patty():
    """Maillard crust. The read is: near-black char in the low spots, hot
    red-brown on the raised crags, and wet fat catching a hard specular."""
    m, nt, b = _nt("MAT_patty_crust")
    crag = _noise(nt, 120.0, detail=9.0, rough=0.62)
    char = _noise(nt, 26.0, detail=6.0, rough=0.55, distortion=0.6)
    fine = _noise(nt, 520.0, detail=4.0)
    cracks = _n(nt, "ShaderNodeTexVoronoi", Scale=70.0, Randomness=0.95,
                feature='DISTANCE_TO_EDGE')
    nt.links.new(_n(nt, "ShaderNodeTexCoord").outputs["Object"], cracks.inputs["Vector"])

    ramp = _ramp(nt, crag.outputs["Factor"], [
        (0.26, (0.020, 0.0070, 0.0030, 1)),
        (0.42, (0.055, 0.0200, 0.0080, 1)),
        (0.56, (0.125, 0.0480, 0.0190, 1)),
        (0.72, (0.235, 0.1000, 0.0400, 1)),
        (0.90, (0.390, 0.1950, 0.0820, 1)),
    ])
    # 0 = normal crust, 1 = a burnt patch
    charmask = _ramp(nt, char.outputs["Factor"], [(0.46, (0.0, 0.0, 0.0, 1)),
                                                  (0.63, (1.0, 1.0, 1.0, 1))])
    base = _mix(nt, charmask.outputs["Color"], ramp.outputs["Color"],
                (0.022, 0.009, 0.005, 1))
    nt.links.new(base, b.inputs["Base Color"])

    rgh = _ramp(nt, fine.outputs["Factor"], [(0.20, (0.34,) * 3 + (1,)),
                                             (0.55, (0.52,) * 3 + (1,)),
                                             (0.85, (0.72,) * 3 + (1,))])
    nt.links.new(rgh.outputs["Color"], b.inputs["Roughness"])
    b.inputs["Specular IOR Level"].default_value = 0.30
    b.inputs["Subsurface Weight"].default_value = 0.06
    b.inputs["Subsurface Radius"].default_value = (0.006, 0.002, 0.001)
    b.inputs["Subsurface Scale"].default_value = 0.004

    # grease sits in patches, not everywhere: a voronoi mask drives the clear
    # coat so some of the crust is wet and mirror-like and the rest is dry.
    wet = _n(nt, "ShaderNodeTexVoronoi", Scale=38.0, Randomness=1.0)
    nt.links.new(_n(nt, "ShaderNodeTexCoord").outputs["Object"], wet.inputs["Vector"])
    wetramp = _ramp(nt, wet.outputs["Distance"], [(0.05, (0.30, 0.30, 0.30, 1)),
                                                  (0.35, (0.01, 0.01, 0.01, 1))])
    nt.links.new(wetramp.outputs["Color"], b.inputs["Coat Weight"])
    b.inputs["Coat Roughness"].default_value = 0.14

    h = _mix(nt, 0.55, crag.outputs["Factor"], cracks.outputs["Distance"], "ADD")
    _bump(nt, b, h, strength=0.52, distance=0.0012)
    return m


def mat_patty_interior():
    """The cut face: a cooked grey-brown ring falling to a juicy centre."""
    m, nt, b = _nt("MAT_patty_interior")
    n = _noise(nt, 300.0, detail=8.0)
    c = _ramp(nt, n.outputs["Factor"], [
        (0.30, (0.28, 0.095, 0.060, 1)),
        (0.50, (0.44, 0.150, 0.095, 1)),
        (0.70, (0.56, 0.230, 0.150, 1)),
    ])
    nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.34
    b.inputs["Subsurface Weight"].default_value = 0.30
    b.inputs["Subsurface Radius"].default_value = (0.012, 0.004, 0.003)
    b.inputs["Subsurface Scale"].default_value = 0.006
    b.inputs["Coat Weight"].default_value = 0.15
    b.inputs["Coat Roughness"].default_value = 0.16
    _bump(nt, b, n.outputs["Factor"], 0.25, 0.0008)
    return m


def mat_crumb():
    """Bun crumb — pale, soft, full of holes."""
    m, nt, b = _nt("MAT_bun_crumb")
    holes = _n(nt, "ShaderNodeTexVoronoi", Scale=120.0, Randomness=1.0)
    nt.links.new(_n(nt, "ShaderNodeTexCoord").outputs["Object"], holes.inputs["Vector"])
    n = _noise(nt, 340.0, detail=6.0)
    c = _ramp(nt, holes.outputs["Distance"], [(0.02, (0.52, 0.43, 0.30, 1)),
                                              (0.20, (0.88, 0.79, 0.62, 1))])
    base = _mix(nt, n.outputs["Factor"], c.outputs["Color"], (0.93, 0.86, 0.70, 1))
    nt.links.new(base, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.78
    b.inputs["Subsurface Weight"].default_value = 0.35
    b.inputs["Subsurface Radius"].default_value = (0.014, 0.010, 0.007)
    b.inputs["Subsurface Scale"].default_value = 0.012
    _bump(nt, b, holes.outputs["Distance"], 0.45, 0.0015)
    return m


# ------------------------------------------------------------------ the rest
def mat_cheese():
    """Vegan cheese — this brand is kosher, so no dairy touches the beef."""
    m, nt, b = _nt("MAT_cheese_vegan")
    n = _noise(nt, 80.0, detail=5.0)
    c = _ramp(nt, n.outputs["Factor"], [(0.32, (0.520, 0.155, 0.010, 1)),
                                        (0.55, (0.740, 0.290, 0.032, 1)),
                                        (0.78, (0.930, 0.500, 0.100, 1))])
    nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    rgh = _ramp(nt, n.outputs["Factor"], [(0.3, (0.14,) * 3 + (1,)),
                                          (0.8, (0.30,) * 3 + (1,))])
    nt.links.new(rgh.outputs["Color"], b.inputs["Roughness"])
    b.inputs["Subsurface Weight"].default_value = 0.18
    b.inputs["Subsurface Radius"].default_value = (0.008, 0.004, 0.0015)
    b.inputs["Subsurface Scale"].default_value = 0.003
    b.inputs["Coat Weight"].default_value = 0.14
    b.inputs["Coat Roughness"].default_value = 0.10
    _bump(nt, b, n.outputs["Factor"], 0.18, 0.0009)
    return m


def mat_bacon():
    """Beef bacon: dark cured meat with pale rendered strips."""
    m, nt, b = _nt("MAT_bacon_beef")
    stripe = _n(nt, "ShaderNodeTexWave", Scale=26.0, Distortion=9.0, Detail=4.0)
    nt.links.new(_n(nt, "ShaderNodeTexCoord").outputs["Object"], stripe.inputs["Vector"])
    n = _noise(nt, 260.0, detail=6.0)
    c = _ramp(nt, stripe.outputs["Fac"], [
        (0.20, (0.055, 0.010, 0.006, 1)),
        (0.48, (0.140, 0.030, 0.016, 1)),
        (0.66, (0.300, 0.120, 0.062, 1)),
        (0.86, (0.460, 0.255, 0.140, 1)),
    ])
    base = _mix(nt, n.outputs["Factor"], c.outputs["Color"], (0.060, 0.016, 0.010, 1))
    nt.links.new(base, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.28
    b.inputs["Coat Weight"].default_value = 0.15
    b.inputs["Coat Roughness"].default_value = 0.18
    b.inputs["Subsurface Weight"].default_value = 0.12
    b.inputs["Subsurface Radius"].default_value = (0.006, 0.002, 0.001)
    b.inputs["Subsurface Scale"].default_value = 0.004
    _bump(nt, b, n.outputs["Factor"], 0.35, 0.0010)
    return m


def mat_onion():
    """Caramelised onion — amber, translucent, wet."""
    m, nt, b = _nt("MAT_onion_caramelized")
    n = _noise(nt, 150.0, detail=6.0)
    c = _ramp(nt, n.outputs["Factor"], [(0.30, (0.105, 0.036, 0.008, 1)),
                                        (0.55, (0.215, 0.085, 0.020, 1)),
                                        (0.80, (0.380, 0.180, 0.052, 1))])
    nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.16
    b.inputs["Subsurface Weight"].default_value = 0.55
    b.inputs["Subsurface Radius"].default_value = (0.012, 0.006, 0.002)
    b.inputs["Subsurface Scale"].default_value = 0.005
    b.inputs["Coat Weight"].default_value = 0.16
    b.inputs["Coat Roughness"].default_value = 0.10
    _bump(nt, b, n.outputs["Factor"], 0.30, 0.0008)
    return m


def mat_sauce():
    """Chef's sauce — the wettest thing in the frame."""
    m, nt, b = _nt("MAT_sauce_chef")
    n = _noise(nt, 90.0, detail=5.0)
    c = _ramp(nt, n.outputs["Factor"], [(0.35, (0.38, 0.105, 0.030, 1)),
                                        (0.65, (0.62, 0.210, 0.055, 1))])
    nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.10
    b.inputs["Coat Weight"].default_value = 0.28
    b.inputs["Coat Roughness"].default_value = 0.07
    b.inputs["Subsurface Weight"].default_value = 0.25
    b.inputs["Subsurface Radius"].default_value = (0.008, 0.003, 0.001)
    b.inputs["Subsurface Scale"].default_value = 0.004
    _bump(nt, b, n.outputs["Factor"], 0.12, 0.0006)
    return m


def mat_ground():
    """Dark slate. It must stay near-black so the brand's red and yellow read."""
    m, nt, b = _nt("MAT_ground")
    n = _noise(nt, 24.0, detail=6.0, rough=0.5)
    c = _ramp(nt, n.outputs["Factor"], [(0.35, (0.0040, 0.0038, 0.0037, 1)),
                                        (0.70, (0.0120, 0.0115, 0.0112, 1))])
    nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    rgh = _ramp(nt, n.outputs["Factor"], [(0.3, (0.34,) * 3 + (1,)),
                                          (0.8, (0.58,) * 3 + (1,))])
    nt.links.new(rgh.outputs["Color"], b.inputs["Roughness"])
    _bump(nt, b, n.outputs["Factor"], 0.08, 0.0008)
    return m


def assign(ob, mat, interior=None):
    ob.data.materials.clear()
    ob.data.materials.append(mat)
    if interior is not None:
        ob.data.materials.append(interior)
    return ob
