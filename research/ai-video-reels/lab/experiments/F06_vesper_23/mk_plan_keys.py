import json
FILM="9:16 vertical cinematic film still, editorial film grade, fine 35mm grain, real photograph. "
VEE=("Image 1 is the identity reference: keep this exact woman — late 30s, angular face, high cheekbones, warm olive skin with real texture and a faint freckle cluster on the left cheekbone, "
 "strong straight dark brows, platinum-white close-cropped buzz cut, perfectly round oversized vermilion-tinted spectacles in thin gold wire frames. Same oversized ivory double-breasted suit, "
 "vermilion silk scarf knotted at the neck, exactly ONE vintage silver stopwatch on a short chain clipped to her lapel. Composed half-smile, direct quick eyes. ")
BOT="Image 2 is the exact product: the VESPER perfume bottle — faceted amber-gold glass cap, rectangular clear glass bottle of golden liquid, thin serif VESPER lettering — unchanged and sharp. "
BAN=" No HDR, no oversaturation, no beauty smoothing, no plastic skin, not a doll, no second stopwatch, no text besides VESPER."
ROOF="on a stone rooftop ledge high above a city skyline"
K={
 "V0":(FILM+VEE+BOT+"Close-up: the silver stopwatch clipped to her ivory lapel, its dial catching warm golden sunset light; beside it, out of focus, the VESPER bottle stands on the stone ledge glowing gold; the sun low on the horizon behind."+BAN),
 "V1":(FILM+VEE+BOT+"Medium shot from her three-quarter left side: she stands "+ROOF+" watching the low golden sun touch the horizon, face in warm gold light, half-smile; the VESPER bottle stands on the ledge beside her, glowing."+BAN),
 "V2":(FILM+VEE+BOT+"Same framing and same position "+ROOF+", but the sun has fully set: cool deep blue dusk light, city lights on; she glances down at the stopwatch on her lapel, unimpressed, one brow raised; the VESPER bottle on the ledge beside her, dim blue."+BAN),
 "V3":(FILM+VEE+BOT+"Same rooftop at blue dusk: she holds the VESPER bottle up at shoulder height and sprays it into the air; the fine perfume mist catches impossible warm golden light that glows in the blue dusk; deadpan confident expression."+BAN),
 "V4":(FILM+VEE+BOT+"Same rooftop: the sun has risen back above the horizon behind her, golden hour restored, warm gold light on her face; she holds the VESPER bottle in one hand and with the other thumb clicks the silver stopwatch on her lapel; dry satisfied half-smile."+BAN),
 "V5":(FILM+BOT+"Product hero: the VESPER bottle stands alone on the stone rooftop ledge, the sun sitting exactly on the horizon behind it, golden light pouring through the amber glass, city skyline soft; label sharp."+BAN),
}
jobs=[{"id":k,"model":"marketing-studio/image/flare","takes":1,"args":{"image_urls":["@file:ref/vee.png","@file:ref/vesper.png"] if k!="V5" else ["@file:ref/vesper.png"],"aspect_ratio":"9:16","resolution":"2k","quality":"high","prompt":p}} for k,p in K.items()]
json.dump({"jobs":jobs},open("plan_keys.json","w"),indent=1)
