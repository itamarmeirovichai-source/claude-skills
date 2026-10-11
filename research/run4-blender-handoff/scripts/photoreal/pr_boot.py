"""Point Blender at its own colour-management config before bpy is imported.

The pip `bpy` module ships datafiles/colormanagement/config.ocio but does not
set OCIO, so view_transform silently collapses to 'NONE' and every render comes
out as flat linear light — milky, desaturated, and unmistakably CG.
"""
import os, sys, glob

if "OCIO" not in os.environ:
    for base in sys.path + ["/usr/local/lib/python3.11/dist-packages"]:
        if not base:
            continue
        hits = glob.glob(os.path.join(base, "bpy", "*", "datafiles",
                                      "colormanagement", "config.ocio"))
        if hits:
            os.environ["OCIO"] = hits[0]
            break
