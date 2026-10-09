"""Low-sample test frames from beats 2, 4 and 7 — rendered to be looked at, not assumed."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
SRC, OUTDIR = sys.argv[-3], sys.argv[-2]
FRAMES = [int(x) for x in sys.argv[-1].split(",")]
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
sc.cycles.device = 'CPU'
sc.cycles.samples = int(os.environ.get("SAMPLES", "24"))
sc.cycles.adaptive_threshold = 0.05
sc.render.resolution_x = int(os.environ.get("RX", "640"))
sc.render.resolution_y = int(os.environ.get("RY", "360"))
sc.render.use_motion_blur = False
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_depth = '8'
os.makedirs(OUTDIR, exist_ok=True)
for f in FRAMES:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(OUTDIR, "test_%04d" % f)
    bpy.ops.render.render(write_still=True)
    print("rendered", f)
