import json
FILM="9:16 vertical cinematic film still, editorial film grade, fine 35mm grain, real photograph. "
OTTO=("Image 1 is the identity reference: keep this exact man — long pale face, deep-set grey eyes, heavy dark brows, swept-back dark hair with silver temples, "
 "and his enormous charcoal-black waxed handlebar moustache with two mirror-symmetrical upturned Dali spirals that completely covers his mouth. Same black turtleneck, "
 "dark charcoal blazer, oxblood silk pocket square, brass director's viewfinder on a thin brass chain. Amused knowing eyes, never wide-eyed, mouth never visible. ")
CAN="Image 2 is the exact product: the slim brushed-gold AURUM can with the thin black band and AURUM lettering, unchanged and sharp. "
VEE="Image 3 is the woman: only her hand and ivory suit sleeve appear, with exactly ONE vintage silver stopwatch on a short silver chain. "
BAN=" No HDR, no oversaturation, no plastic skin, not a cartoon, mouth never visible, eyes never wide, no extra cans, no text besides AURUM."
ROOF="a luxurious rooftop terrace at golden hour high above a hazy golden city skyline, a white marble plinth with the AURUM can glowing in perfect sun, a helicopter in the distant sky"
K={
 "T0":(["otto","can"], FILM+CAN+"The view through a brass director's viewfinder: a circular vignette with soft black edges frames "+ROOF+"; the low sun sits at the right of the skyline; no people visible inside the circle."+BAN),
 "T1":(["otto","can"], FILM+OTTO+CAN+"Medium-wide: on "+ROOF+", he stands at the left holding the brass viewfinder up to one eye, framing the AURUM can on the plinth at frame right; low sun at right behind the skyline."+BAN),
 "T2":(["otto","can"], FILM+OTTO+CAN+"Same rooftop, same framing: he lowers the viewfinder and raises his right hand with two fingers pinched in the air as if moving the sun; the low sun now sits at the LEFT of the skyline, perfectly backlighting the AURUM can on the plinth; dry deadpan look."+BAN),
 "T3":(["otto","can"], FILM+OTTO+CAN+"High wide reveal: the entire rooftop, plinth, golden can and city skyline are a detailed TABLETOP MINIATURE diorama on a dark walnut desk in a dim film studio; the 'sun' is a brass desk lamp glowing over it; a coffee cup, pencils and a film slate beside the diorama show the real scale; a tiny figure of the moustached man stands on the miniature roof."+BAN),
 "T4":(["otto","can","vee"], FILM+CAN+VEE+"Same dim studio desk with the tabletop miniature city and brass desk lamp sun; a woman's hand in an ivory suit sleeve holds the silver stopwatch above the diorama, thumb on the crown, clicking it; beside the diorama a sleek desk monitor in portrait orientation glows, showing a finished golden cinematic product film of the gold AURUM can on a rooftop at sunset."+BAN),
 "T5":(["otto","can"], FILM+OTTO+CAN+"Macro close-up on the tabletop miniature roof: the tiny moustached man figure, perfectly detailed, lifts his tiny brass viewfinder toward the camera, one eyebrow raised; the tiny golden can on its plinth beside him; warm desk-lamp light, shallow depth of field, the glowing monitor soft in the background."+BAN),
}
R={"otto":"@file:ref/otto.png","can":"@file:ref/can.png","vee":"@file:ref/vee.png"}
jobs=[{"id":k,"model":"marketing-studio/image/flare","takes":1,"args":{"image_urls":[R[r] for r in refs],"aspect_ratio":"9:16","resolution":"2k","quality":"high","prompt":p}} for k,(refs,p) in K.items()]
json.dump({"jobs":jobs},open("plan_keys.json","w"),indent=1)
