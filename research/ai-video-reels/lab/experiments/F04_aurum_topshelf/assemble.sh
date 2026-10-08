#!/bin/bash
# AURUM "Top Shelf": 6 keyframe-matched shots -> one 30 s continuous take, with sound map + captions.
# usage: FONTS=/path/to/fontdir ./assemble.sh   (fontdir holds Instrument Serif .ttf)
# Timeline (s): A push 0-4 | B open 4-9 | C sip 9-14 | E float 14-20 (slowed 1.2x) | F land 20-25 | G pack 25-30
set -e
cd "$(dirname "$0")"
mkdir -p final
C=clips; F1=1/24
ffmpeg -v error -y \
 -i $C/A_push_t01.mp4 -i $C/B_open_t01.mp4 -i $C/C_sip_t01.mp4 \
 -i $C/E_float_k_t01.mp4 -i $C/F_land_t01.mp4 -i $C/G_pack_t01.mp4 -filter_complex "\
[0:v]setpts=PTS/1.25,trim=0:4,setpts=PTS-STARTPTS,fps=24[a];\
[1:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[b];\
[2:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[c];\
[3:v]trim=start=0.0417,setpts=1.2*(PTS-STARTPTS),minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1,trim=0:6,setpts=PTS-STARTPTS[e];\
[4:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[f];\
[5:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[g];\
[a][b][c][e][f][g]concat=n=6:v=1,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p[v]" \
 -map "[v]" -an -c:v libx264 -crf 16 -preset slow -t 30 final/_video.mp4

# Captions: lines in the locked voices + the AI disclosure super.
cat > final/captions.ass <<'EOF'
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Line,Instrument Serif,78,&H00F2F4F7,&H00000000,&H00101010,&H64000000,0,1,0,0,100,100,0,0,1,2,3,2,80,80,330,1
Style: Name,Instrument Serif,44,&H0060B8E6,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,2,0,1,1.5,2,2,80,80,430,1
Style: Super,Instrument Serif,34,&H99FFFFFF,&H00000000,&H00000000,&H00000000,0,1,0,0,100,100,1,0,1,0,1,3,0,48,60,1
Style: Tag,Instrument Serif,96,&H0060B8E6,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,4,0,1,2,3,8,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:30.00,Super,,0,0,0,,AI-generated film · VXO
Dialogue: 0,0:00:21.15,0:00:22.40,Name,,0,0,0,,OTTO
Dialogue: 0,0:00:21.15,0:00:22.40,Line,,0,0,0,,{\fad(120,120)}One more take?
Dialogue: 0,0:00:22.70,0:00:24.80,Name,,0,0,0,,VEE
Dialogue: 0,0:00:22.70,0:00:24.80,Line,,0,0,0,,{\fad(120,120)}It's perfect. Ship it.
Dialogue: 0,0:00:26.40,0:00:30.00,Tag,,0,0,0,,{\fad(300,0)}AURUM
Dialogue: 0,0:00:26.90,0:00:30.00,Line,,0,0,0,,{\fad(300,0)}Sparkling yuzu. Taste it from the top.
EOF

# Sound map. Music: build 0-13, 0.7 s of silence before the leap, dreamy tail under the float,
# 8 frames of silence on the glare cut, jazzy button (music 35.8 s) under the packshot.
A=audio
ffmpeg -v error -y -i final/_video.mp4 \
 -i $A/music.mp3 -i $A/music.mp3 -i $A/music.mp3 \
 -i $A/sfx_wind.mp3 -i $A/sfx_pop.mp3 -i $A/sfx_pour.mp3 -i $A/sfx_sip.mp3 \
 -i $A/sfx_whoosh.mp3 -i $A/sfx_thump.mp3 -i $A/sfx_set.mp3 -i $A/sfx_click.mp3 \
 -i $A/otto_onemore.mp3 -i $A/vee_ship.mp3 -i $A/otto_tag.mp3 -filter_complex "\
[1:a]atrim=0:13.3,asetpts=N/SR/TB,afade=t=in:d=0.6,afade=t=out:st=12.9:d=0.4,volume=0.8[m1];\
[2:a]atrim=14:20,asetpts=N/SR/TB,afade=t=in:d=0.3,afade=t=out:st=5.4:d=0.6,volume=0.95,adelay=14000:all=1[m2];\
[3:a]atrim=35.6:40.6,asetpts=N/SR/TB,afade=t=out:st=4.2:d=0.8,volume=0.75,adelay=25000:all=1[m3];\
[4:a]atrim=0:5,afade=t=in:d=0.4,afade=t=out:st=3.6:d=1.4,volume=0.55[wind];\
[5:a]volume=0.9,adelay=5600:all=1[pop];\
[6:a]atrim=0:3.2,afade=t=out:st=2.6:d=0.6,volume=0.7,adelay=7300:all=1[pour];\
[7:a]volume=0.8,adelay=11800:all=1[sip];\
[8:a]volume=0.7,adelay=14700:all=1[whoosh];\
[9:a]volume=1.0,adelay=20350:all=1[thump];\
[10:a]atrim=0:4.6,afade=t=in:d=0.3,afade=t=out:st=4:d=0.6,volume=0.3,adelay=20400:all=1[set];\
[11:a]volume=1.0,adelay=22450:all=1[click];\
[12:a]volume=1.1,adelay=21150:all=1[o1];\
[13:a]volume=1.1,adelay=22700:all=1[v1];\
[14:a]atempo=1.08,volume=1.1,adelay=25750:all=1[o2];\
[m1][m2][m3][wind][pop][pour][sip][whoosh][thump][set][click][o1][v1][o2]amix=inputs=14:duration=longest:normalize=0,atrim=0:30,alimiter=limit=0.9[a]" \
 -map 0:v -map "[a]" -vf "subtitles=final/captions.ass:fontsdir=${FONTS:-.}" \
 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -t 30 final/aurum_topshelf_30.mp4
rm -f final/_video.mp4
echo final/aurum_topshelf_30.mp4
