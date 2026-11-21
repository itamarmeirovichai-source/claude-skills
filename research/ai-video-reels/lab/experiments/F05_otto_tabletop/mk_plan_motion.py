import json
ID=("The moustached man keeps his exact identity: enormous charcoal waxed handlebar moustache with spiral tips covering his mouth (mouth never visible, eyes never wide), black turtleneck, charcoal blazer, oxblood pocket square, brass viewfinder. "
 "The gold AURUM can keeps its exact shape and label. Cinematic, real physics, one continuous camera move, no cuts. ")
M="kling-video/v3.0/pro/image-to-video"
S=[("A_out","T0","T1",5,"The camera pulls smoothly backward out of the circular brass viewfinder, revealing the man holding it to his eye on the golden rooftop beside the AURUM can on its plinth; a helicopter drifts across the sky."),
   ("B_sun","T1","T2",5,"He lowers the viewfinder, deadpan, raises two pinched fingers and drags the sun through the sky from right to left; the sun obediently glides across the skyline, the light on the can shifts to a perfect backlight; the helicopter turns away."),
   ("C_reveal","T2","T3",10,"Continuous slow crane move: the camera pulls back and rises higher and higher, and the rooftop, the man and the skyline turn out to be a detailed tabletop miniature diorama on a walnut desk in a dim film studio; the sun is revealed to be a brass desk lamp; a coffee cup and pencils show the real scale. Smooth constant speed, no cuts."),
   ("D_click","T3","T4",5,"The camera drifts slowly right along the desk; a woman's hand in an ivory sleeve enters from above holding a silver stopwatch and clicks it once over the diorama; the portrait monitor beside the miniature lights up playing a golden product film of the AURUM can."),
   ("E_tiny","T4","T5",5,"The camera pushes slowly in and down to the miniature roof: the tiny moustached man figure comes alive, lifts his tiny brass viewfinder to the camera and raises one eyebrow; warm desk-lamp light, shallow depth of field.")]
jobs=[{"id":i,"model":M,"takes":1,"args":{"image_url":f"@file:ref/{a}.png","last_image_url":f"@file:ref/{b}.png","duration":d,"cfg_scale":0.5,"sound":"off","prompt":ID+p}} for i,a,b,d,p in S]
json.dump({"jobs":jobs},open("plan_motion.json","w"),indent=1)
