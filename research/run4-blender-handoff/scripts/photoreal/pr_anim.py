"""The eight-beat choreography, as a pure function of scroll progress.

The website's rule is that every value on screen is a pure function of scroll
position, so scrubbing backwards is exact. The render has to obey the same rule
or the frames will not match the code that plays them: pose(p) never reads any
previous state.
"""
import math

BEATS = {
    "toss":    (0.00, 0.11),
    "bullet":  (0.11, 0.21),
    "closeup": (0.21, 0.31),
    "explode": (0.31, 0.50),
    "turn":    (0.50, 0.59),
    "smash":   (0.59, 0.69),
    "cut":     (0.69, 0.86),
    "slice":   (0.86, 1.00),
}

# bottom to top — the order the layers separate in
STACK = ["bun_bottom", "patty_lower", "cheese_lower", "patty_upper",
         "cheese_upper", "bacon_beef", "onion_caramelized", "sauce_chef",
         "bun_top"]


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def local(p, beat):
    a, b = BEATS[beat]
    return clamp((p - a) / (b - a))


def ease_out(t, k=3.0):
    return 1.0 - (1.0 - t) ** k


def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)


def ease_back_out(t, s=1.35):
    t -= 1.0
    return t * t * ((s + 1) * t + s) + 1.0


def d_part_half(part):
    """half-width added by the two halves parting"""
    return part


def pose(p):
    """Everything the renderer needs for one frame."""
    p = clamp(p)
    t_toss = local(p, "toss")
    t_bullet = local(p, "bullet")
    t_close = local(p, "closeup")
    t_expl = local(p, "explode")
    t_turn = local(p, "turn")
    t_smash = local(p, "smash")
    t_cut = local(p, "cut")
    t_slice = local(p, "slice")

    # --- the burger itself ---------------------------------------------------
    # rise: the hero drops in and settles
    rise = (1.0 - ease_back_out(t_toss)) * 0.085 if p < BEATS["toss"][1] else 0.0

    # explode: layers fan apart, then close again during the turn — the stack
    # has to be whole again before the smash lands on it
    spread = ease_out(t_expl, 2.2) * (1.0 - ease_in_out(t_turn))
    gap = 0.046 * spread

    # smash: the stack squashes and springs back a little
    hit = ease_in_out(t_smash)
    squash = 1.0 - 0.34 * math.sin(math.pi * min(1.0, t_smash * 1.35)) \
        if t_smash > 0 else 1.0
    bulge = 1.0 + (1.0 - squash) * 0.55

    # turn: the whole burger rotates to present its side to the knife
    spin = math.radians(-118.0) * ease_in_out(t_turn)
    # a slow drift through the first half keeps it alive
    drift = math.radians(16.0) * ease_in_out(clamp(p / 0.50))

    # Cut: the two halves swing open about the cut plane until both interior
    # faces point the same way, then slide apart across the screen. A small
    # book angle only ever shows one face — the other turns its crust to the
    # camera — so the halves go the whole ninety degrees, and the burger turns
    # with them so the camera does not have to orbit ninety degrees in one beat.
    open_amt = ease_out(t_cut, 2.4)
    part = 0.052 * open_amt + 0.040 * ease_in_out(t_slice)
    book = math.radians(90.0) * open_amt
    # The turn that brings both cut faces round to the lens. The sign is set by
    # which side of the plane each half keeps: bisect's "inner" is -X, so the
    # half the code calls left is the one holding x > 0. Turning the other way
    # showed the camera two crusts.
    reveal = math.radians(-90.0) * open_amt

    # --- camera --------------------------------------------------------------
    # keyframes: (p, distance, target z, elevation, azimuth, focal mm)
    # The lens widens through the explode. Holding 85 mm would need the camera
    # a metre and a half back to fit the fan, which loses every layer.
    KEYS = [
        (0.00, 0.62, 0.046, 26.0, -40.0, 80.0),
        (0.11, 0.54, 0.044, 18.0, -22.0, 85.0),
        (0.21, 0.50, 0.044, 12.0,  26.0, 90.0),
        (0.31, 0.46, 0.046,  6.0,  40.0, 82.0),
        (0.42, 0.66, 0.043,  9.0,  24.0, 50.0),
        (0.50, 0.78, 0.043, 11.0,  12.0, 44.0),
        (0.59, 0.58, 0.044,  7.0,  -6.0, 68.0),
        # the cut plane's normal sits at azimuth -12 after the half turn, so
        # the camera holds there: any further round and one half shows the
        # viewer its crust instead of its cross-section
        (0.69, 0.50, 0.040,  9.0, -12.0, 85.0),
        (0.86, 0.60, 0.042, 12.0, -12.0, 74.0),
        (1.00, 0.70, 0.044, 17.0, -16.0, 78.0),
    ]
    for i in range(len(KEYS) - 1):
        a, b = KEYS[i], KEYS[i + 1]
        if a[0] <= p <= b[0]:
            u = ease_in_out((p - a[0]) / (b[0] - a[0])) if b[0] > a[0] else 0.0
            cam = [a[j] + (b[j] - a[j]) * u for j in range(1, 6)]
            break
    else:
        cam = list(KEYS[-1][1:])

    # bullet time: the objects hold still while the camera keeps moving, so the
    # orbit gets an extra push that the burger does not see
    cam[3] += 34.0 * ease_in_out(t_bullet) * (1.0 - ease_in_out(t_close))

    # the smash kicks the camera
    if 0.0 < t_smash < 1.0:
        k = math.exp(-t_smash * 9.0) * (1.0 - ease_in_out(t_smash))
        cam[1] += 0.004 * math.sin(t_smash * 78.0) * k
        cam[2] += 1.6 * math.sin(t_smash * 61.0) * k

    # what the camera has to fit, in metres from the aim point
    fan_half = 4.0 * gap + 0.060
    wide_half = 0.064 + d_part_half(part)

    return dict(
        rise=rise, gap=gap, squash=squash, bulge=bulge,
        fan_half=fan_half, wide_half=wide_half, cam_focal=cam[4],
        spin=spin + drift + reveal, part=part, book=book,
        open_amt=open_amt, cut_active=p >= BEATS["cut"][0],
        explode_amt=spread,
        cam_dist=cam[0], cam_target_z=cam[1], cam_elev=cam[2], cam_azim=cam[3],
    )


def layer_offset(name, pose_d):
    """How far this layer has travelled from the closed stack."""
    i = STACK.index(name)
    centre = (len(STACK) - 1) / 2.0
    return (i - centre) * pose_d["gap"]
