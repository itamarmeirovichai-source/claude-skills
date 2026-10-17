"""Builds plan_train.json: 24 Qwen-Image-3 edits of the OTTO master for Soul ID training."""
import json
from pathlib import Path

ANCHOR = ("Image 1 is the identity reference: keep this exact man — long pale face, deep-set grey eyes, heavy dark brows, "
          "swept-back dark hair with silver temples, and his enormous charcoal-black waxed handlebar moustache with two "
          "mirror-symmetrical upturned Dali spirals that completely covers his mouth. Same tailored black turtleneck, dark "
          "charcoal blazer, oxblood silk pocket square, brass director's viewfinder on a thin brass chain. Relaxed brow, "
          "amused knowing eyes, never wide-eyed, never startled, mouth never visible.")
BAN = ("No HDR, no oversaturation, no beauty smoothing, no plastic or waxy skin, no rubber moustache, not a cartoon, "
       "not a costume, no text or logos.")
NEG = ("HDR, oversaturated, beauty smoothing, plastic skin, waxy skin, rubber moustache, fake moustache, cartoon, costume, "
       "text, logo, watermark, visible mouth, lips, teeth, wide eyes, startled, extra fingers, deformed hands, "
       "different person, different clothes")
BG = {
    "char": "Seamless charcoal paper backdrop with a warm brass-gold glow behind him; soft octabox key at 45 degrees camera-left, subtle rim light.",
    "grey": "Plain seamless mid-grey studio backdrop; soft, even, slightly cool daylight from a large window camera-right, gentle fill, no glow.",
    "stone": "Plain warm stone-beige seamless paper backdrop; soft natural top light with a gentle shadow side, low contrast, airy.",
}
TAIL = ("Real photograph, real unretouched skin with pores and fine lines, the moustache is real waxed hair with individual strands. "
        "Natural hands with five fingers. Editorial magazine portrait.")

# id, aspect, framing + angle + expression, background
SHOTS = [
    ("t01_front_amused",      "1:1", "Tight close-up of his face filling the frame from forehead to chin and moustache tips, facing the camera straight on, eyes into the lens, amused knowing look.", "char"),
    ("t02_34L_brow",          "1:1", "Tight close-up of his face, head turned three-quarters to his left (camera sees the right side of his face), eyes back to the lens, one brow slightly raised.", "grey"),
    ("t03_34R_thoughtful",    "1:1", "Tight close-up of his face, head turned three-quarters to his right (camera sees the left side of his face), eyes looking slightly off-camera, thoughtful and calm.", "stone"),
    ("t04_low_amused",        "1:1", "Tight close-up of his face from a slightly low camera angle looking up at him, chin a touch raised, dignified and amused.", "char"),
    ("t05_high_knowing",      "1:1", "Tight close-up of his face from a slightly high camera angle looking down at him, he glances up into the lens with a knowing look.", "grey"),
    ("t06_profileL",          "1:1", "Tight close-up, strict side profile facing left of frame, nose and the full upturned moustache spiral silhouetted, calm expression, eye looking ahead.", "char"),
    ("h07_front_brow",        "1:1", "Head-and-shoulders portrait, facing the camera, one eyebrow slightly raised, sharp amused eyes.", "grey"),
    ("h08_34L_amused",        "1:1", "Head-and-shoulders portrait, body and head turned three-quarters to his left, eyes back to the lens, amused.", "char"),
    ("h09_34R_amused",        "1:1", "Head-and-shoulders portrait, body and head turned three-quarters to his right, eyes back to the lens, warm amused look.", "stone"),
    ("h10_profileR",          "1:1", "Head-and-shoulders portrait, strict side profile facing right of frame, the full moustache spiral visible in silhouette, calm.", "grey"),
    ("h11_profileL",          "1:1", "Head-and-shoulders portrait, strict side profile facing left of frame, chin level, looking ahead thoughtfully.", "stone"),
    ("h12_viewfinder_eye",    "1:1", "Head-and-shoulders portrait, he holds the small brass director's viewfinder from his chain up to his right eye with one hand, looking through it at the camera, other eye relaxed; the chain still around his neck.", "char"),
    ("h13_thoughtful_34R",    "1:1", "Head-and-shoulders portrait, three-quarters to his right, he looks off to the side, deep in thought, one brow lowered slightly; hands out of frame.", "grey"),
    ("h14_low_brow",          "1:1", "Head-and-shoulders portrait from a slightly low camera angle, he looks down into the lens with one brow raised, confident.", "char"),
    ("w15_point_lens",        "3:4", "Waist-up portrait, facing the camera, he points his right index finger directly at the lens, amused knowing look.", "char"),
    ("w16_open_hand",         "3:4", "Waist-up portrait, body three-quarters to his left, he gestures with one open palm to the side as if presenting an idea, eyes to the lens, amused.", "grey"),
    ("w17_viewfinder_34R",    "3:4", "Waist-up portrait, body three-quarters to his right, he raises the brass director's viewfinder to one eye with his right hand, framing a shot, the chain hanging from it.", "stone"),
    ("w18_point_camleft",     "3:4", "Waist-up portrait, facing the camera, he points with his right arm outstretched toward camera-left, looking where he points, one brow raised.", "grey"),
    ("w19_arms_folded",       "3:4", "Waist-up portrait, facing the camera, arms folded across his chest, calm amused look into the lens.", "stone"),
    ("w20_frame_hands",       "3:4", "Waist-up portrait, he makes a director's frame with both hands, thumbs and index fingers forming a rectangle, held at chest height, eyes to the lens.", "char"),
    ("w21_high_amused",       "3:4", "Waist-up portrait from a slightly high camera angle, hands in his trouser pockets, he glances up at the lens, amused.", "char"),
    ("w22_profileR_look",     "3:4", "Waist-up portrait, side profile facing right of frame, he holds the brass viewfinder in his hand at chest height and looks down at it thoughtfully.", "grey"),
    ("f23_full_front",        "2:3", "Full-body portrait, standing upright facing the camera, feet slightly apart, hands relaxed at his sides; black tailored trousers and polished black shoes; whole body in frame with space above head and below feet.", "grey"),
    ("f24_full_34",           "2:3", "Full-body portrait, standing three-quarters to his left, one hand in his trouser pocket, looking at the lens, amused; black tailored trousers and polished black shoes; whole body in frame.", "char"),
]


def prompt_for(desc, bg):
    return (f"{ANCHOR} Create a new photograph of this same man. {desc} {BG[bg]} {TAIL} {BAN}")


jobs = []
for i, (jid, ar, desc, bg) in enumerate(SHOTS):
    jobs.append({"id": jid, "model": "alibaba/qwen-image-3/edit", "takes": 1, "args": {
        "prompt": prompt_for(desc, bg), "negative_prompt": NEG,
        "image_urls": ["@file:ref/master.png"], "resolution": "1k", "aspect_ratio": ar,
        "prompt_extend": False, "enable_thinking": False, "seed": 7100 + i}})
Path(__file__).with_name("plan_train.json").write_text(json.dumps(
    {"defaults": {"model": "alibaba/qwen-image-3/edit", "takes": 1}, "jobs": jobs}, indent=1, ensure_ascii=False))
print(len(jobs), "jobs")
