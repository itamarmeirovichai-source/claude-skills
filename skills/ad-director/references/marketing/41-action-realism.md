# 41 — Action realism checklist (read before writing any action/chase prompt)

Why this exists: the F09 heist was rejected by the owner as "not a real chase". The parachute opened at roof height, the car never turned, the landing was impossible, and everything happened in one camera move. The Dubai reel the owner keeps sending (DcDrXjXsLcU, see ch. 08 §1) is **not a one-take**: it has 9 shots with hard cuts, each from a different camera position, at 1080p. Action reads as real because of coverage plus physics, not because of one heroic move.

## 1. Genre decides the grammar
- **Product sensory films (pour, sip, spray):** one continuous take is the VXO signature.
- **Action, chase, stunt:** use **multi-shot coverage with hard cuts**, 6–10 shots in 30 s. One take only if a real camera rig could do it (chase car, FPV drone).
- **Never:** a camera that passes through glass, walls or cars. No impossible framing that a crew could not rig.

## 2. Physics gates (all must be true before generation)

| Event | Real-world rule to write into the prompt |
|---|---|
| BASE jump + parachute | Needs height: 150 m+ building. 2–4 s of visible freefall, *then* a pilot chute pulls the main canopy open with a jolt. The canopy is a rectangular ram-air wing. The jumper steers with toggles and lands into the wind with a flare and a run-out. |
| Landing in a moving car | Close to impossible; it reads as fake. Use instead: he lands on a rooftop or empty street and the car **skids to a stop** for him; or he lands **in the open truck bed** at matched low speed. |
| Car chase | Weight transfer, body roll, tyre smoke on hard turns, a handbrake turn into a side street, near-misses with traffic, a police car mirroring every turn, sirens doppler. |
| Police | Two or three cruisers. A realistic block (PIT attempt, roadblock) and a realistic escape (alley, wrong-way lane, tunnel). |
| Drinking | The level must drop; the throat moves; the same vessel throughout. |
| Speech | A voice only when lips are visible and synced, or when the mouth is off-screen. |

## 3. Coverage menu for a 30 s chase (pick 7–9)
1. Wide establishing aerial (drone) of the building/bank.
2. Medium of the hero at the edge, with a sound-first hook (alarm bell).
3. POV freefall, then the canopy jolt (helmet-cam style).
4. Ground-up wide of the canopy over the street.
5. Chase-car tracking at bumper height: the getaway car drifts round a corner, tyre smoke.
6. In-car 3/4 of the driver, mirror with police lights.
7. Low nose-on: police cruiser fishtails.
8. Pick-up beat: car skids to a stop, the hero vaults in, and it takes off.
9. Product payoff + punchline, locked-off.
10. End card.

## 4. Process gates
1. Write the shot list, then do a **physics read**: for each shot, ask "could a stunt crew film this?" If not, rewrite it.
2. Generate at 480p to test the blocking; only good takes go to 1080p.
3. **QC:** check every frame strip at 2 fps, the audio onset of each event, and whether each shot is cut on action.
4. Send nothing that fails a gate. Report what failed instead.
