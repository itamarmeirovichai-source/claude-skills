"""Geometry for the photoreal Smash House burger.

Everything here is real mesh: a lathed brioche crown with embedded sesame seeds,
smash patties with lace edges, cheese that actually drapes over the patty rim,
beef bacon strips that bend, and caramelised onion built from strands.
Layer names come from the asset contract and must not change.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_boot  # must precede bpy
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, noise as bnoise

TAU = math.pi * 2.0


# ---------------------------------------------------------------- helpers
def fbm(v, octaves=4, lac=2.0, gain=0.5):
    """Fractal value noise on a Vector, in [-1, 1]-ish."""
    amp, freq, total = 1.0, 1.0, 0.0
    for _ in range(octaves):
        total += bnoise.noise(Vector(v) * freq) * amp
        freq *= lac
        amp *= gain
    return total


def new_obj(name, bm, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def solidify(ob, thickness, offset=-1.0):
    """Thicken an open shell. Uses the modifier, not bmesh.ops.solidify, which
    tears open grids into non-manifold garbage."""
    md = ob.modifiers.new("solid", 'SOLIDIFY')
    md.thickness = thickness
    md.offset = offset
    md.use_even_offset = False
    md.use_rim = True
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    old = ob.data
    ob.modifiers.remove(md)
    ob.data = me
    bpy.data.meshes.remove(old)
    for pgon in me.polygons:
        pgon.use_smooth = True
    return ob


def shade_auto_smooth(ob, angle=math.radians(52)):
    """Blender 5 dropped mesh.use_auto_smooth; a weighted-normal-free equivalent
    is an edge-split by angle baked as sharp edges."""
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > angle:
            e.smooth = False
    bm.to_mesh(me)
    bm.free()


def spin_profile(bm, profile, segments=72, close_bottom=True):
    """Lathe a list of (r, z) points around +Z. profile runs top-centre outward."""
    rings = []
    for (r, z) in profile:
        if r <= 1e-6:
            rings.append([bm.verts.new((0.0, 0.0, z))])
            continue
        ring = []
        for s in range(segments):
            a = TAU * s / segments
            ring.append(bm.verts.new((math.cos(a) * r, math.sin(a) * r, z)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        if len(a) == 1:
            for s in range(segments):
                bm.faces.new((a[0], b[s], b[(s + 1) % segments]))
        elif len(b) == 1:
            for s in range(segments):
                bm.faces.new((a[s], a[(s + 1) % segments], b[0]))
        else:
            for s in range(segments):
                t = (s + 1) % segments
                bm.faces.new((a[s], a[t], b[t], b[s]))
    if close_bottom and len(rings[-1]) > 1:
        bm.faces.new(list(reversed(rings[-1])))
    bm.normal_update()
    return rings


def displace(bm, amp, scale, seed=0.0, mask=None, octaves=4):
    """Push every vert along its normal by fbm noise."""
    bm.normal_update()
    off = Vector((seed * 13.7, seed * 7.3, seed * 4.1))
    for v in bm.verts:
        w = 1.0 if mask is None else mask(v)
        if w <= 0.0:
            continue
        n = v.normal.copy()
        if n.length < 1e-6:
            continue
        v.co += n.normalized() * (fbm(v.co * scale + off, octaves) * amp * w)


# ---------------------------------------------------------------- buns
CROWN_PROFILE = [
    (0.0000, 0.0425), (0.0090, 0.0422), (0.0175, 0.0412), (0.0255, 0.0395),
    (0.0325, 0.0370), (0.0390, 0.0336), (0.0445, 0.0292), (0.0490, 0.0240),
    (0.0524, 0.0182), (0.0546, 0.0122), (0.0556, 0.0064), (0.0553, 0.0022),
    (0.0530, 0.0002), (0.0300, 0.0000), (0.0000, 0.0000),
]
HEEL_PROFILE = [
    (0.0000, 0.0198), (0.0180, 0.0197), (0.0320, 0.0193), (0.0420, 0.0184),
    (0.0490, 0.0167), (0.0533, 0.0138), (0.0552, 0.0100), (0.0551, 0.0058),
    (0.0530, 0.0024), (0.0470, 0.0004), (0.0300, 0.0000), (0.0000, 0.0000),
]


def build_bun(name, profile, seed, crumb_amp=0.0016, sx=1.0, sz=1.0):
    bm = bmesh.new()
    spin_profile(bm, [(r * sx, z * sz) for (r, z) in profile], 80)
    # the bake: broad lobes plus a fine crumb, both fading out at the base
    def mask(v):
        up = min(1.0, max(0.0, (v.co.z - 0.001) / 0.006))
        # leave the apex alone, or the broad lobes build a peak like a hat
        apex = 1.0 - math.exp(-((math.hypot(v.co.x, v.co.y)) / 0.016) ** 2 * 1.4)
        return up * (0.25 + 0.75 * apex)
    displace(bm, 0.0038, 17.0, seed, mask, octaves=3)
    displace(bm, crumb_amp, 150.0, seed + 3.3, mask, octaves=3)
    ob = new_obj(name, bm)
    return ob


def sesame_seeds(crown, count=210, seed=7):
    """Real ellipsoid seeds sunk into the crown, joined into the bun mesh so the
    cut beat slices through them like the bread."""
    rnd = random.Random(seed)
    me = crown.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.normal_update()
    faces = [f for f in bm.faces if f.calc_center_median().z > 0.016]
    clusters = [rnd.choice(faces).calc_center_median() for _ in range(9)]
    out = bmesh.new()
    placed = []
    tries = 0
    while len(placed) < count and tries < count * 40:
        tries += 1
        f = rnd.choice(faces)
        if rnd.random() < 0.55:
            # bias towards a cluster centre so the seeds bunch the way they do
            # on a real bun instead of sitting on an even lattice
            c = rnd.choice(clusters)
            f = min(faces, key=lambda q: (q.calc_center_median() - c).length
                    + rnd.uniform(0.0, 0.020))
        # random barycentric point on the face
        vs = [v.co for v in f.verts]
        w = [rnd.random() for _ in vs]
        tot = sum(w) or 1.0
        p = Vector((0, 0, 0))
        for c, wi in zip(vs, w):
            p += c * (wi / tot)
        n = f.normal.normalized()
        if any((p - q).length < 0.0044 for q in placed):
            continue
        placed.append(p)
        sm = bmesh.new()
        bmesh.ops.create_uvsphere(sm, u_segments=12, v_segments=7, radius=1.0)
        sz = rnd.uniform(0.86, 1.14)
        for v in sm.verts:
            v.co.x *= 0.0020 * sz
            v.co.y *= 0.0014 * sz
            v.co.z *= 0.00070 * sz
        # orient: z -> surface normal, random spin around it
        z = n
        x = Vector((0, 0, 1)).cross(z)
        if x.length < 1e-5:
            x = Vector((1, 0, 0))
        x.normalize()
        y = z.cross(x)
        basis = Matrix((x, y, z)).transposed().to_4x4()
        spin = Matrix.Rotation(rnd.uniform(0, TAU), 4, 'Z')
        bmesh.ops.transform(sm, matrix=(basis @ spin).to_3x3().to_4x4(), verts=sm.verts)
        bmesh.ops.translate(sm, vec=p - n * 0.00030, verts=sm.verts)
        tmp = bpy.data.meshes.new("seed_tmp")
        sm.to_mesh(tmp)
        sm.free()
        out.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    for f in out.faces:
        f.smooth = True
    # keep the seeds as their own material slot
    seed_me = bpy.data.meshes.new(crown.name + "_seeds")
    out.to_mesh(seed_me)
    out.free()
    bm.free()
    ob = bpy.data.objects.new(crown.name + "_seeds", seed_me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


# ---------------------------------------------------------------- patty
def build_patty(name, z0, seed=0, r=0.0565, thick=0.0090, rings=30, seg=150):
    """A smash patty. The outline is torn, the top is craggy where the beef
    caught the flat-top, and the last 12% of the radius thins into the crisp
    lace skirt that is the whole point of a smash burger."""
    rnd = random.Random(seed)
    ph = rnd.uniform(0, TAU)

    def edge_r(a):
        d = Vector((math.cos(a + ph), math.sin(a + ph), 0.0))
        torn = 1.0 + 0.055 * fbm(d * 2.4, 3)
        lace = 0.038 * max(0.0, fbm(d * 7.5, 4))
        frill = 0.011 * max(0.0, fbm(d * 19.0, 3))
        return r * (torn + lace + frill)

    def crag(x, y, k):
        return (fbm(Vector((x, y, 0.4)) * 52.0, 4) * 0.0017
                + fbm(Vector((x, y, 2.1)) * 190.0, 3) * 0.0008) * k

    bm = bmesh.new()
    top, bot = [], []
    for i in range(rings + 1):
        t = i / rings
        tr, br = [], []
        if i == 0:
            tr.append(bm.verts.new((0, 0, z0 + thick * 0.94 + crag(0, 0, 1.0))))
            br.append(bm.verts.new((0, 0, z0)))
            top.append(tr)
            bot.append(br)
            continue
        for s in range(seg):
            a = TAU * s / seg
            R = edge_r(a) * t
            x, y = math.cos(a) * R, math.sin(a) * R
            # round the shoulder: the top surface curves down to meet the base
            # at the rim, so there is no cylinder wall to catch a grey highlight
            if t > 0.86:
                u = (t - 0.86) / 0.14
                shoulder = math.sqrt(max(0.0, 1.0 - u * u))
            else:
                shoulder = 1.0
            rim = math.exp(-((t - 0.74) / 0.14) ** 2) * 0.0012
            # never thinner than 40% — a knife edge cannot be lit convincingly
            th = thick * (0.40 + 0.60 * shoulder) + rim
            k = 1.0 + 0.35 * max(0.0, (t - 0.72) / 0.28)
            tr.append(bm.verts.new((x, y, z0 + th + crag(x, y, k))))
            br.append(bm.verts.new((x, y, z0 + crag(x, y, 0.30) * 0.4)))
        top.append(tr)
        bot.append(br)

    def bridge(rows, flip):
        for i in range(len(rows) - 1):
            a, b = rows[i], rows[i + 1]
            if len(a) == 1:
                for s in range(seg):
                    f = (a[0], b[s], b[(s + 1) % seg])
                    bm.faces.new(tuple(reversed(f)) if flip else f)
            else:
                for s in range(seg):
                    t2 = (s + 1) % seg
                    f = (a[s], a[t2], b[t2], b[s])
                    bm.faces.new(tuple(reversed(f)) if flip else f)

    bridge(top, False)
    bridge(bot, True)
    for s in range(seg):
        t2 = (s + 1) % seg
        bm.faces.new((top[-1][s], bot[-1][s], bot[-1][t2], top[-1][t2]))
    bm.normal_update()
    return new_obj(name, bm)


# ---------------------------------------------------------------- cheese
def build_cheese(name, z0, half=0.052, rot=0.0, seed=0, n=56,
                 flat_r=0.0400, drop=0.0140, thick=0.0028, drips=6):
    """Melted cheese is not a square slice sitting on a patty — it is a blanket
    that has slumped over the edge and run down in tongues. Built radially so
    the boundary can be irregular and the drips can reach different depths."""
    rnd = random.Random(seed)
    tg = [(rnd.uniform(0, TAU), rnd.uniform(0.008, 0.019), rnd.uniform(0.22, 0.46))
          for _ in range(drips)]
    seg, rings = 132, 30

    def rim(a):
        d = Vector((math.cos(a + rot), math.sin(a + rot), 0.0))
        return half * (0.96 + 0.075 * fbm(d * 2.8, 3) + 0.045 * fbm(d * 8.0, 3))

    def run(a):
        """extra fall, and how far past the rim this angle reaches"""
        extra = 0.0
        for (ang, depth, width) in tg:
            da = abs(((a - ang + math.pi) % TAU) - math.pi)
            extra += max(0.0, 1.0 - da / width) ** 1.7 * depth
        return extra

    bm = bmesh.new()
    rows = []
    for i in range(rings + 1):
        t = i / rings
        row = []
        if i == 0:
            row.append(bm.verts.new((0, 0, z0 + 0.0008)))
        else:
            for sdx in range(seg):
                a = TAU * sdx / seg
                R = rim(a) * t
                x, y = math.cos(a) * R, math.sin(a) * R
                over = max(0.0, (R - flat_r) / max(1e-5, rim(a) - flat_r))
                fall = (drop + run(a)) * over ** 1.9
                # the tongue narrows as it falls, like cheese pulling thin
                pull = 1.0 - 0.16 * over
                z = z0 + 0.0008 * (1.0 - t) - fall
                z += fbm(Vector((x, y, seed * 3.0)) * 55.0, 3) * 0.0009
                row.append(bm.verts.new((x * pull, y * pull, z)))
        rows.append(row)
    for i in range(rings):
        a, b = rows[i], rows[i + 1]
        if len(a) == 1:
            for sdx in range(seg):
                bm.faces.new((a[0], b[sdx], b[(sdx + 1) % seg]))
        else:
            for sdx in range(seg):
                t2 = (sdx + 1) % seg
                bm.faces.new((a[sdx], a[t2], b[t2], b[sdx]))
    bm.normal_update()
    return solidify(new_obj(name, bm), thick)


# ---------------------------------------------------------------- beef bacon
def build_bacon(name, z0, seed=0, strips=3):
    """Curled strips. Each strip is a ribbon swept along a wavy path with a
    fatty lighter edge built into the geometry so the material can find it."""
    rnd = random.Random(seed)
    bm = bmesh.new()
    for k in range(strips):
        a0 = TAU * k / strips + rnd.uniform(-0.25, 0.25)
        length, width = 0.076, 0.0180
        steps, across = 40, 5
        rows = []
        for i in range(steps + 1):
            t = i / steps
            s = (t - 0.5) * length
            # path bends across the burger and lifts at the ends (curl)
            bend = math.sin(t * math.pi * 1.8 + k) * 0.010
            lift = (abs(t - 0.5) * 2.0) ** 2.4 * 0.0038
            px = math.cos(a0) * s - math.sin(a0) * bend
            py = math.sin(a0) * s + math.cos(a0) * bend
            row = []
            for j in range(across + 1):
                w = (j / across - 0.5) * width
                wx = -math.sin(a0) * w
                wy = math.cos(a0) * w
                x, y = px + wx, py + wy
                ripple = math.sin(t * 22.0 + j * 0.7 + k) * 0.0012
                z = z0 + lift + ripple + fbm(Vector((x, y, k)) * 90.0, 3) * 0.0007
                row.append(bm.verts.new((x, y, z)))
            rows.append(row)
        for i in range(steps):
            for j in range(across):
                bm.faces.new((rows[i][j], rows[i][j + 1],
                              rows[i + 1][j + 1], rows[i + 1][j]))
    bm.normal_update()
    return solidify(new_obj(name, bm), 0.0046)


# ---------------------------------------------------------------- onion
def build_onion(name, z0, seed=0, strands=17):
    """Caramelised onion as a tangle of flattened strands."""
    rnd = random.Random(seed)
    bm = bmesh.new()
    for k in range(strands):
        a0 = rnd.uniform(0, TAU)
        rad = rnd.uniform(0.020, 0.050)
        span = rnd.uniform(1.1, 2.4)
        w = rnd.uniform(0.0050, 0.0090)
        zk = z0 + rnd.uniform(0.0, 0.0042)
        steps = 16
        rows = []
        for i in range(steps + 1):
            t = i / steps
            a = a0 + span * (t - 0.5)
            r = rad * (1.0 + 0.16 * math.sin(t * 5.0 + k))
            x, y = math.cos(a) * r, math.sin(a) * r
            z = zk + math.sin(t * 6.0 + k * 1.7) * 0.0016
            nx, ny = -math.sin(a), math.cos(a)
            rows.append([
                bm.verts.new((x - nx * w, y - ny * w, z - 0.0007)),
                bm.verts.new((x, y, z + 0.0009)),
                bm.verts.new((x + nx * w, y + ny * w, z - 0.0007)),
            ])
        for i in range(steps):
            for j in range(2):
                bm.faces.new((rows[i][j], rows[i][j + 1],
                              rows[i + 1][j + 1], rows[i + 1][j]))
    bm.normal_update()
    return solidify(new_obj(name, bm), 0.0022)


# ---------------------------------------------------------------- sauce
def build_sauce(name, z0, seed=0, r=0.0505, seg=120, rings=14):
    """A poured layer with an uneven edge and a few runs over the side."""
    rnd = random.Random(seed)
    ph = rnd.uniform(0, TAU)
    runs = [rnd.uniform(0, TAU) for _ in range(3)]

    def rim(a):
        base = 1.0 + 0.055 * fbm(Vector((math.cos(a + ph), math.sin(a + ph), 0)) * 2.6, 3)
        for g in runs:
            da = abs(((a - g + math.pi) % TAU) - math.pi)
            base += max(0.0, 1.0 - da / 0.26) ** 2 * 0.150
        return r * base

    bm = bmesh.new()
    rows = []
    for i in range(rings + 1):
        t = i / rings
        row = []
        if i == 0:
            row.append(bm.verts.new((0, 0, z0 + 0.0026)))
        else:
            for s in range(seg):
                a = TAU * s / seg
                R = rim(a) * t
                x, y = math.cos(a) * R, math.sin(a) * R
                z = z0 + 0.0026 * (1.0 - t ** 3) + fbm(Vector((x, y, 5.0)) * 70.0, 3) * 0.0004
                row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    for i in range(rings):
        a, b = rows[i], rows[i + 1]
        if len(a) == 1:
            for s in range(seg):
                bm.faces.new((a[0], b[s], b[(s + 1) % seg]))
        else:
            for s in range(seg):
                t2 = (s + 1) % seg
                bm.faces.new((a[s], a[t2], b[t2], b[s]))
    bm.normal_update()
    return solidify(new_obj(name, bm), 0.0013)
