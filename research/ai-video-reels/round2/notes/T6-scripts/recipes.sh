#!/bin/bash
# T6 effect battery. Inputs: A.mp4 B.mp4 (1080x1920@30, 4s, with audio), music.wav, heebo.ttf
# usage: ./recipes.sh [name...]   -> out/<name>.mp4 + out/<name>.jpg (frame), results in results.tsv
cd "$(dirname "$0")"
LOOK=${LOOK:-A.mp4}
FF="ffmpeg -hide_banner -loglevel error -y"
ENC="-c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p"
W=1080; H=1920

# ---------- TRANSITIONS ----------
r_whip_real() { # A pans out fast to the left, B pans in (directional blur only during the 0.25s move)
$FF -i A.mp4 -i B.mp4 -filter_complex "
[0:v]trim=0:3.7,setpts=PTS-STARTPTS[a];[1:v]trim=0:3,setpts=PTS-STARTPTS[b];
[a][b]xfade=transition=slideleft:duration=0.25:offset=3.45,
avgblur=sizeX=80:sizeY=1:enable='between(t,3.40,3.75)',
avgblur=sizeX=30:sizeY=1:enable='between(t,3.33,3.82)'[v]" -map "[v]" $ENC out/whip_real.mp4; }

r_zoom_through() { # Premiere "zoom transition" [YT:G01V09CWTJY]: scale 100->300% over the 5 frames before the cut,
# B starts at 300% and eases back to 100% over 5 frames; shutter-angle motion blur ~ avgblur on those frames
$FF -i A.mp4 -i B.mp4 -filter_complex "
[0:v]trim=0:3,setpts=PTS-STARTPTS,
scale=w='iw*(1+2*pow(max(0,t-2.833)/0.167,2))':h=-2:eval=frame,crop=$W:$H,
avgblur=sizeX=18:sizeY=18:enable='gte(t,2.9)'[a];
[1:v]trim=0:3,setpts=PTS-STARTPTS,
scale=w='iw*(1+2*pow(max(0,1-t/0.167),2))':h=-2:eval=frame,crop=$W:$H,
avgblur=sizeX=18:sizeY=18:enable='lt(t,0.1)'[b];
[a][b]concat=n=2:v=1:a=0,fps=30,setsar=1[v]" -map "[v]" $ENC out/zoom_through.mp4; }

r_spin() { # spin transition: last 0.2s of A rotates out, B rotates in, motion-blurred
$FF -i A.mp4 -i B.mp4 -filter_complex "
[0:v]trim=0:3,setpts=PTS-STARTPTS,scale=2160:-2,rotate=a='if(gt(t,2.8),(t-2.8)/0.2*PI/4,0)':ow=$W:oh=$H:c=black[a];
[1:v]trim=0:3,setpts=PTS-STARTPTS,scale=2160:-2,rotate=a='if(lt(t,0.2),-(0.2-t)/0.2*PI/4,0)':ow=$W:oh=$H:c=black[b];
[a][b]concat=n=2:v=1:a=0,gblur=sigma=18:enable='between(t,2.78,3.22)'[v]" -map "[v]" $ENC out/spin.mp4; }

r_light_leak_trans() { # film-burn / light-leak transition: warm gradient blob in 'screen' over a 0.6s crossfade
$FF -i A.mp4 -i B.mp4 -f lavfi -i "gradients=s=${W}x${H}:c0=0xff6a00:c1=0xffd36b:c2=0x000000:c3=0xff2d55:nb_colors=4:speed=0.08:type=radial:d=7:r=30" -filter_complex "
[0:v][1:v]xfade=transition=fade:duration=0.6:offset=3.2,format=gbrp[x];
[2:v]format=gbrp,fade=t=in:st=2.9:d=0.3,fade=t=out:st=3.8:d=0.4,trim=0:6.8[lk];
[x][lk]blend=all_mode=screen,format=yuv420p[v]" -map "[v]" $ENC out/light_leak_trans.mp4; }

r_glitch_trans() { # 6-frame digital glitch cut (RGB split + block displacement + noise), CapCut "Glitch" look
$FF -i A.mp4 -i B.mp4 -filter_complex "
[0:v][1:v]xfade=transition=pixelize:duration=0.2:offset=3.4,
rgbashift=rh=-28:bh=28:rv=6:edge=wrap:enable='between(t,3.3,3.7)',
crop=iw:ih:x='if(between(t,3.3,3.7),mod(n*137,40),0)':y=0:exact=1,scale=$W:$H,
noise=alls=40:allf=t:enable='between(t,3.35,3.6)',
eq=contrast=1.3:saturation=1.6:enable='between(t,3.35,3.6)'[v]" -map "[v]" $ENC out/glitch_trans.mp4; }

r_flash_cuts_beats() { # white flash frames on a list of beat times (from beats.py)
B="1.0 1.5 2.0 2.5 3.0"; EN=$(for t in $B; do printf "between(t,%s,%s)+" $t $(python3 -c "print($t+0.066)"); done); EN=${EN%+}
$FF -i A.mp4 -filter_complex "[0:v]eq=brightness=0.6:contrast=0.6:enable='$EN'[v]" -map "[v]" $ENC out/flash_cuts_beats.mp4; }

# ---------- CAMERA / MOTION ----------
r_impact_shake() { # decaying shake on hits (punchier than constant shake): amp*exp(-decay*(t-hit))
HITS="0.5 2.0"; X=""; Y=""
for h in $HITS; do X="$X+gte(t,$h)*28*exp(-9*(t-$h))*sin(70*(t-$h))"; Y="$Y+gte(t,$h)*22*exp(-9*(t-$h))*cos(53*(t-$h))"; done
$FF -i A.mp4 -filter_complex "[0:v]scale=$((W+80)):$((H+80)),crop=$W:$H:x='40$X':y='40$Y'[v]" -map "[v]" $ENC out/impact_shake.mp4; }

r_handheld() { # subtle handheld drift (makes AI shots feel shot on camera): 2-4% motion, low freq
$FF -i A.mp4 -filter_complex "[0:v]scale=$((W*104/100)):-2,crop=$W:$H:x='(iw-ow)/2+18*sin(t*1.3)+9*sin(t*2.9+1)':y='(ih-oh)/2+14*sin(t*1.1+2)+7*sin(t*3.7)'[v]" -map "[v]" $ENC out/handheld.mp4; }

r_motion_blur() { # generic motion blur / smear for fast moves (hide AI morphing)
$FF -i A.mp4 -filter_complex "[0:v]tmix=frames=5:weights='1 2 3 2 1'[v]" -map "[v]" $ENC out/motion_blur.mp4; }

r_freeze_intro() { # freeze frame + zoom + desaturate + name tag ("character intro" / record-scratch)
$FF -i A.mp4 -filter_complex "
[0:v]trim=0:1.5,setpts=PTS-STARTPTS[a];
[0:v]trim=start_frame=45:end_frame=46,setpts=PTS-STARTPTS,loop=loop=45:size=1:start=0,
scale=w='iw*(1+0.12*min(1,n/8))':h=-2:eval=frame,crop=$W:$H,hue=s=0.2,
drawtext=fontfile=heebo.ttf:text='THE CLIENT':fontsize=110:fontcolor=white:borderw=8:x=(w-tw)/2:y=h*0.62:alpha='min(1,n/6)'[f];
[0:v]trim=1.5:4,setpts=PTS-STARTPTS[b];[a][f][b]concat=n=3:v=1:a=0[v]" -map "[v]" $ENC out/freeze_intro.mp4; }

r_slowmo_mci() { # real optical-flow slow motion of a 1s section (x3), only where needed (it is slow)
$FF -i A.mp4 -filter_complex "[0:v]trim=1:2,setpts=PTS-STARTPTS,minterpolate=fps=90:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=3*PTS,fps=30[v]" -map "[v]" $ENC out/slowmo_mci.mp4; }

r_boomerang() {
$FF -i A.mp4 -filter_complex "[0:v]trim=0:1.5,setpts=PTS-STARTPTS,split[f][r];[r]reverse[rv];[f][rv]concat=n=2:v=1:a=0,loop=loop=1:size=90[v]" -map "[v]" $ENC out/boomerang.mp4; }

r_echo_trails() { # light trails / echo (lagfun) - music-video & night-car look
$FF -i B.mp4 -filter_complex "[0:v]lagfun=decay=0.94[v]" -map "[v]" $ENC out/echo_trails.mp4; }

# ---------- GLITCH / RETRO ----------
r_rgb_pulse() { # chromatic aberration that pulses on beats (offset follows a decaying envelope via sendcmd-free trick: 3 fixed layers)
$FF -i A.mp4 -filter_complex "
[0:v]split=3[a][b][c];[b]rgbashift=rh=-10:bh=10[b2];[c]rgbashift=rh=-30:bh=30:rv=8:bv=-8[c2];
[a][b2]blend=all_expr='if(lt(mod(T,0.5),0.12),B,A)'[ab];
[ab][c2]blend=all_expr='if(lt(mod(T,0.5),0.05),B,A)',format=yuv420p[v]" -map "[v]" $ENC out/rgb_pulse.mp4; }

r_vhs() { # VHS / camcorder: low-res, chroma bleed, tracking noise band, scanlines, warm fade, date stamp
$FF -i A.mp4 -filter_complex "
[0:v]scale=360:-2,scale=$W:$H:flags=neighbor,chromashift=cbh=6:crh=-6,
gblur=sigma=1.2,noise=alls=18:allf=t,
eq=saturation=1.35:contrast=1.1:gamma=1.05,colorbalance=rs=0.08:bs=-0.06,
drawbox=x=0:y='mod(t*700,ih)':w=iw:h=40:color=white@0.12:t=fill,
geq=lum='lum(X,Y)*(0.86+0.14*mod(Y,4)/3)':cb='cb(X,Y)':cr='cr(X,Y)',
drawtext=fontfile=heebo.ttf:text='PLAY  OCT 05 2026':fontsize=48:fontcolor=white:x=60:y=120:shadowx=3:shadowy=3[v]" -map "[v]" $ENC out/vhs.mp4; }

r_datamosh_lite() { # pseudo-datamosh: blend motion residue of the next shot over the previous one
$FF -i A.mp4 -i B.mp4 -filter_complex "
[0:v]trim=0:2,setpts=PTS-STARTPTS,split[a][a0];[1:v]trim=0:2,setpts=PTS-STARTPTS,split[b1][b2];
[b2]tblend=all_mode=difference,eq=brightness=0.1:contrast=2[d];
[a][d]blend=all_mode=addition:all_opacity=0.7,trim=1.6:2,setpts=PTS-STARTPTS[mosh];
[a0]trim=0:1.6,setpts=PTS-STARTPTS[a1];
[a1][mosh][b1]concat=n=3:v=1:a=0[v]" -map "[v]" $ENC out/datamosh_lite.mp4; }

# ---------- LOOKS / COLOR ----------
r_grain_real() { # luma-dependent film grain (stronger in mids, survives IG better than per-pixel noise at size 1)
$FF -i $LOOK -f lavfi -i "color=c=gray:s=$((W/2))x$((H/2)):r=30:d=4" -filter_complex "
[1:v]format=gray,noise=alls=60:allf=t,scale=$W:$H:flags=bicubic,format=gbrp[g];
[0:v]format=gbrp[s];[s][g]blend=all_mode=overlay:all_opacity=0.35,format=yuv420p[v]" -map "[v]" $ENC out/grain_real.mp4; }

r_halation_bloom() { # bloom + red halation around highlights (35mm film / "cinematic" look)
$FF -i $LOOK -filter_complex "
[0:v]format=gbrp,split[a][b];[b]curves=all='0/0 0.7/0 1/1',gblur=sigma=25,colorchannelmixer=rr=1:gg=0.35:bb=0.15[glow];
[a][glow]blend=all_mode=screen:all_opacity=0.6,format=yuv420p[v]" -map "[v]" $ENC out/halation_bloom.mp4; }

r_cube_lut() { # python-generated teal&orange .cube (17^3), applied at 60% (mix) with lut3d
python3 - <<'PY'
N=17
with open('teal_orange.cube','w') as f:
    f.write('TITLE "teal_orange_T6"\nLUT_3D_SIZE %d\n'%N)
    for b in range(N):
        for g in range(N):
            for r in range(N):
                R,G,B=r/(N-1),g/(N-1),b/(N-1)
                L=0.2126*R+0.7152*G+0.0722*B
                s=lambda x: x*x*(3-2*x)
                c=0.5+ (s(L)-0.5)*1.0 - L + L  # keep luma
                sh=(1-L)**2; hi=L**2
                R2=R+0.06*hi-0.05*sh; G2=G+0.01*hi+0.02*sh; B2=B-0.07*hi+0.07*sh
                R2=0.06+0.9*R2; G2=0.06+0.9*G2; B2=0.06+0.9*B2   # lifted blacks, rolled highs
                f.write('%.5f %.5f %.5f\n'%tuple(min(1,max(0,x)) for x in (R2,G2,B2)))
PY
$FF -i $LOOK -filter_complex "[0:v]split[a][b];[b]lut3d=file=teal_orange.cube[l];[a][l]blend=all_mode=normal:all_opacity=0.6,format=yuv420p[v]" -map "[v]" $ENC out/cube_lut.mp4; }

r_curves_presets() { # ffmpeg built-in curves presets: vintage | cross_process | darker | lighter | increase_contrast | strong_contrast | medium_contrast | negative | color_negative
$FF -i $LOOK -filter_complex "[0:v]curves=preset=vintage,colortemperature=temperature=5200,vibrance=intensity=0.2[v]" -map "[v]" $ENC out/curves_presets.mp4; }

r_duotone() { # duotone / brand-colour grade (gray -> map shadows to navy, highlights to orange)
$FF -i $LOOK -filter_complex "[0:v]format=gray,format=gbrp,curves=r='0/0.05 1/1':g='0/0.08 1/0.6':b='0/0.3 1/0.2',format=yuv420p[v]" -map "[v]" $ENC out/duotone.mp4; }

# ---------- TEXT ----------
r_kinetic_he() { # Hebrew kinetic captions via ASS (libass+fribidi do RTL shaping) - pop, word highlight, slide, shake
cat > kin.ass <<'ASS'
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pop,Heebo,110,&H00FFFFFF,&H0000E5FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,9,4,5,60,60,0,1
Style: Kara,Heebo,84,&H00FFFFFF,&H0000E5FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,2,80,80,520,1
Style: Box,Heebo,64,&H00000000,&H00000000,&H0000E5FF,&H0000E5FF,-1,0,0,0,100,100,0,0,3,18,0,8,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:00.90,Pop,,0,0,0,,{\pos(540,900)\fscx40\fscy40\t(0,90,\fscx118\fscy118)\t(90,160,\fscx100\fscy100)}תראו את זה
Dialogue: 0,0:00:00.90,0:00:01.80,Pop,,0,0,0,,{\pos(540,900)\fscx40\fscy40\t(0,90,\fscx118\fscy118)\t(90,160,\fscx100\fscy100)\c&H0000E5FF&}בחינם!
Dialogue: 0,0:00:01.80,0:00:03.20,Kara,,0,0,0,,{\k35}יצרתי {\k35}את {\k30}זה {\k40}ב-Seedance‏ {\k40}2.5‏
Dialogue: 0,0:00:01.80,0:00:04.00,Box,,0,0,0,,{\move(1300,260,540,260,0,180)}הפרומפט בתגובות 👇
Dialogue: 0,0:00:03.20,0:00:04.00,Pop,,0,0,0,,{\pos(540,900)\t(0,400,\frz-4)\c&H004BFF2D&}מטורף
ASS
$FF -i A.mp4 -vf "ass=kin.ass:fontsdir=." $ENC out/kinetic_he.mp4; }

r_drawtext_he() { # drawtext fallback (NO bidi in drawtext 6.1 -> must pre-reverse with python-bidi / fribidi) - test shows the problem
$FF -i A.mp4 -vf "drawtext=fontfile=heebo.ttf:text='שלום עולם':fontsize=120:fontcolor=white:borderw=8:x=(w-tw)/2:y=h*0.3" $ENC out/drawtext_he.mp4; }

# ---------- AUDIO ----------
r_sfx_layer() { # layered transition SFX: pre-lap whoosh (starts 0.25s BEFORE the cut) + sub hit ON the cut + riser into the drop
CUT=2.0; DROP=3.5
$FF -i A.mp4 -i music.wav -filter_complex "
anoisesrc=d=0.6:c=pink:r=48000:a=0.8,highpass=f=400,lowpass=f=7000,volume='pow(sin(PI*t/0.6),3)*1.5':eval=frame,afade=t=out:st=0.45:d=0.15,adelay=$(python3 -c "print(int(($CUT-0.35)*1000))")|$(python3 -c "print(int(($CUT-0.35)*1000))")[wh];
aevalsrc='0.9*sin(2*PI*(45*t+(110/16)*(1-exp(-16*t))))*exp(-4*t)':s=48000:d=1,adelay=$(python3 -c "print(int($CUT*1000))")|$(python3 -c "print(int($CUT*1000))")[hit];
aevalsrc='0.3*sin(2*PI*(200*t+300*t*t))*pow(t/1.5,2)':s=48000:d=1.5,adelay=$(python3 -c "print(int(($DROP-1.5)*1000))")|$(python3 -c "print(int(($DROP-1.5)*1000))")[ris];
[1:a]volume=0.5[m];
[m][wh][hit][ris]amix=inputs=4:normalize=0:duration=first,atrim=0:4[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k out/sfx_layer.mp4; }

r_duck_eq() { # music ducked under voice (sidechain) + EQ notch 2-4kHz in music so speech cuts through
$FF -f lavfi -i "sine=f=300:d=6,volume='if(between(t,1,4),1,0)':eval=frame" -i music.wav -filter_complex "
[0:a]aformat=channel_layouts=stereo,asplit[v1][sc];
[1:a]atrim=0:6,aformat=channel_layouts=stereo,equalizer=f=3000:t=q:w=1:g=-4[m];
[m][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400:makeup=1[md];
[v1][md]amix=inputs=2:normalize=0[a]" -map "[a]" -c:a pcm_s16le out/duck_eq.wav; }

r_loudnorm2() { # two-pass loudnorm to -14 LUFS / -1 dBTP, then measure
J=$(ffmpeg -hide_banner -nostats -i out/sfx_layer.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
$FF -i out/sfx_layer.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:$MI:linear=true,aresample=48000" -c:v copy -c:a aac -b:a 256k out/loudnorm2.mp4
ffmpeg -hide_banner -nostats -i out/loudnorm2.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tr -s ' ' > out/loudnorm2.txt; }

r_export_ig() { # final export for Reels/TikTok/Shorts
$FF -i out/loudnorm2.mp4 -c:v libx264 -preset slow -crf 18 -profile:v high -level 4.2 -pix_fmt yuv420p -r 30 -g 60 -bf 2 \
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 256k -ar 48000 -movflags +faststart out/export_ig.mp4; }

ALL=$(declare -F | awk '{print $3}' | grep '^r_' | sed 's/^r_//')
[ $# -gt 0 ] && ALL="$*"
for n in $ALL; do
  s=$(date +%s.%N); err=$( { r_$n; } 2>&1 ); rc=$?
  e=$(python3 -c "print(round($(date +%s.%N)-$s,1))")
  f=out/$n.mp4; [ -f "$f" ] && $FF -ss 0.0 -i $f -vf "select='eq(n\,0)+eq(n\,30)+eq(n\,60)+eq(n\,95)',scale=270:-2,tile=4x1" -frames:v 1 -update 1 out/$n.jpg 2>/dev/null
  printf "%s\t%s\t%ss\t%s\n" "$n" "$rc" "$e" "$(echo "$err" | tail -2 | tr '\n' ' ' | cut -c1-200)" | tee -a results.tsv
done
