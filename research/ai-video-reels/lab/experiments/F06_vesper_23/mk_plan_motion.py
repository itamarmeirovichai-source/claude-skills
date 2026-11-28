import json
ID=("The woman keeps her exact identity: platinum buzz cut, round red-tinted spectacles in thin gold frames, olive skin with freckles, oversized ivory double-breasted suit, red silk scarf, exactly ONE silver stopwatch on a short chain clipped to her lapel. "
 "The VESPER perfume bottle keeps its exact shape and label. Cinematic, real physics, one continuous camera move, no cuts. ")
M="kling-video/v3.0/pro/image-to-video"
S=[("A_open","V0","V1",5,"The camera slowly pulls back and arcs to her left side as she turns her head to watch the low golden sun on the horizon; the VESPER bottle glows on the ledge beside her."),
   ("B_set","V1","V2",10,"Locked-off time-lapse of the sky only: she stays almost perfectly still while the sun sinks below the horizon, the golden light drains to cool deep blue dusk and the city lights switch on behind her; at the very end she glances down at the stopwatch on her lapel, unimpressed."),
   ("C_spray","V2","V3",5,"Deadpan, she picks up the VESPER bottle from the ledge, lifts it to shoulder height and sprays twice into the air; the fine mist catches an impossible warm golden glow in the blue dusk."),
   ("D_rewind","V3","V4",5,"Magic rewind: from the golden mist, the sky reverses in time — the sun rises back up above the horizon and warm golden light floods back over her and the city; she clicks the stopwatch on her lapel with her thumb, satisfied half-smile."),
   ("E_pack","V4","V5",5,"The camera glides smoothly off her shoulder and settles on the VESPER bottle standing on the stone ledge, the sun sitting exactly on the horizon behind it, golden light pouring through the glass.")]
jobs=[{"id":i,"model":M,"takes":1,"args":{"image_url":f"@file:ref/{a}.png","last_image_url":f"@file:ref/{b}.png","duration":d,"cfg_scale":0.5,"sound":"off","prompt":ID+p}} for i,a,b,d,p in S]
json.dump({"jobs":jobs},open("plan_motion.json","w"),indent=1)
