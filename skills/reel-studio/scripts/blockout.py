"""Blender blockout generator for AI video (Seedance / Genjutsu / Runway V2V).

Builds a flat-colored "greybox" scene from a JSON spec, animates a camera,
and renders a vertical guide video. The color-coded blocks (cyan = water,
red = furniture, white = architecture, green = vegetation...) lock geometry,
layout and camera motion; the AI model then re-renders the look.

Usage:
  python3 blockout.py spec.json out.mp4 [--res 540x960] [--fps 24] [--preview]
Requires: pip install bpy==4.5.0 (Python 3.11), ffmpeg.
"""
import json, math, os, subprocess, sys, tempfile

import bpy
from mathutils import Vector

PALETTE = {  # semantic colors (Workbench flat shading)
    "architecture": (0.92, 0.92, 0.92), "floor": (0.80, 0.80, 0.82),
    "water": (0.55, 0.90, 0.85), "furniture": (0.85, 0.08, 0.08),
    "accent": (0.10, 0.25, 0.85), "vegetation": (0.25, 0.80, 0.20),
    "glass": (0.60, 0.75, 0.95), "ground": (0.75, 0.70, 0.55),
    "product": (1.00, 0.80, 0.00), "person": (0.95, 0.45, 0.10),
    "vehicle": (0.20, 0.20, 0.25), "sky": (0.85, 0.90, 0.98),
}


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1.0)
    return m


def add_object(o):
    kind = o.get("shape", "box")
    loc = o.get("loc", [0, 0, 0])
    size = o.get("size", [1, 1, 1])
    if kind == "box":
        bpy.ops.mesh.primitive_cube_add(location=loc)
        ob = bpy.context.object
        ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    elif kind == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=size[0] / 2, depth=size[2])
        ob = bpy.context.object
    elif kind == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=size[0] / 2)
        ob = bpy.context.object
    elif kind == "plane":
        bpy.ops.mesh.primitive_plane_add(location=loc)
        ob = bpy.context.object
        ob.scale = (size[0] / 2, size[1] / 2, 1)
    elif kind == "tree":  # trunk + crown
        bpy.ops.mesh.primitive_cylinder_add(location=(loc[0], loc[1], loc[2] + size[2] * 0.3),
                                            radius=size[0] * 0.08, depth=size[2] * 0.6)
        trunk = bpy.context.object
        trunk.data.materials.append(material("ground", PALETTE["ground"]))
        bpy.ops.mesh.primitive_uv_sphere_add(location=(loc[0], loc[1], loc[2] + size[2] * 0.75),
                                             radius=size[0] / 2)
        ob = bpy.context.object
    else:
        raise ValueError(f"unknown shape {kind}")
    ob.rotation_euler[2] = math.radians(o.get("rot_z", 0))
    role = o.get("role", "architecture")
    rgb = tuple(o["color"]) if "color" in o else PALETTE.get(role, PALETTE["architecture"])
    ob.data.materials.append(material(role, rgb))
    ob.name = o.get("name", role)
    return ob


def setup_camera(cam_spec, fps, seconds):
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = cam_spec.get("lens", 24)
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    target = bpy.data.objects.new("target", None)
    bpy.context.scene.collection.objects.link(target)
    tc = cam.constraints.new("TRACK_TO")
    tc.target = target
    tc.track_axis = "TRACK_NEGATIVE_Z"
    tc.up_axis = "UP_Y"
    keys = cam_spec["keys"]  # [{"t":0,"pos":[..],"look":[..]}, ...]
    for k in keys:
        f = 1 + round(k["t"] * fps)
        cam.location = Vector(k["pos"]); cam.keyframe_insert("location", frame=f)
        target.location = Vector(k["look"]); target.keyframe_insert("location", frame=f)
    for ob in (cam, target):  # smooth ease in/out
        if ob.animation_data and ob.animation_data.action:
            for fc in ob.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, 1 + round(seconds * fps)


def render(spec, out_mp4, res=(540, 960), fps=24, preview=False):
    reset()
    sc = bpy.context.scene
    for o in spec["objects"]:
        add_object(o)
    seconds = spec.get("seconds", 5)
    setup_camera(spec["camera"], fps, seconds)
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"; sh.color_type = "MATERIAL"
    sh.show_shadows = True; sh.show_cavity = True
    sh.background_type = "WORLD"
    sc.world = bpy.data.worlds.new("w")
    sc.world.color = PALETTE["sky"]
    sh.studio_light = "outdoor.sl" if "outdoor.sl" in [s.name for s in bpy.context.preferences.studio_lights] else sh.studio_light
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.fps = fps
    if preview:
        sc.frame_end = sc.frame_start  # single still
    tmp = tempfile.mkdtemp(prefix="blockout_")
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.join(tmp, "f_")
    bpy.ops.render.render(animation=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i",
                    os.path.join(tmp, "f_%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", out_mp4], check=True)
    return out_mp4


if __name__ == "__main__":
    args = sys.argv[1:]
    spec = json.load(open(args[0])); out = args[1]
    res = (540, 960); fps = 24; preview = "--preview" in args
    if "--res" in args:
        w, h = args[args.index("--res") + 1].split("x"); res = (int(w), int(h))
    if "--fps" in args:
        fps = int(args[args.index("--fps") + 1])
    print(render(spec, out, res, fps, preview))
