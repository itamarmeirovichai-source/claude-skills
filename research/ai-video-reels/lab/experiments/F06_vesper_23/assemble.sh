#!/bin/bash
# VESPER-2 "Keep the golden hour" (Vee, VXO spec): 5 Kling shots -> one 30 s take + sound map + captions.
# Timeline (s): A open 0-5 | B sunset time-lapse 5-15 | C spray 15-20 | D rewind 20-25 | E packshot 25-30
# usage: FONTS=/path/to/fontdir ./assemble.sh
set -e
cd "$(dirname "$0")"; mkdir -p final; C=clips
ffmpeg -v error -y -i $C/A_open_t01.mp4 -i $C/B_set_t01.mp4 -i $C/C_spray_t01.mp4 -i $C/D_rewind_t01.mp4 -i $C/E_pack_t01.mp4 -filter_complex "\
[0:v]trim=0:5,setpts=PTS-STARTPTS[a];\
[1:v]trim=start=0.0417:duration=10,setpts=PTS-STARTPTS[b];\
[2:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[c];\
[3:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[d];\
[4:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[e];\
[a][b][c][d][e]concat=n=5:v=1,fps=24,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p[v]" \
 -map "[v]" -an -c:v libx264 -crf 16 -preset slow -t 30 final/_video.mp4
cat > final/captions.ass <<'ASS'
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Line,Instrument Serif,78,&H00F2F4F7,&H00000000,&H00101010,&H64000000,0,1,0,0,100,100,0,0,1,2,3,2,80,80,330,1
Style: Name,Instrument Serif,44,&H0060B8E6,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,2,0,1,1.5,2,2,80,80,540,1
Style: Super,Instrument Serif,34,&H99FFFFFF,&H00000000,&H00000000,&H00000000,0,1,0,0,100,100,1,0,1,0,1,3,0,48,60,1
Style: Tag,Instrument Serif,110,&H0060B8E6,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,14,0,1,2,3,8,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:30.00,Super,,0,0,0,,AI-generated film · VXO spec
Dialogue: 0,0:00:02.40,0:00:05.90,Name,,0,0,0,,VEE
Dialogue: 0,0:00:02.40,0:00:05.90,Line,,0,0,0,,{\fad(120,120)}The sun's golden hour? Twenty minutes, tops.
Dialogue: 0,0:00:23.95,0:00:26.20,Name,,0,0,0,,VEE
Dialogue: 0,0:00:23.95,0:00:26.20,Line,,0,0,0,,{\fad(120,120)}Mine lasts all night.
Dialogue: 0,0:00:26.50,0:00:30.00,Tag,,0,0,0,,{\fad(300,0)}VESPER
Dialogue: 0,0:00:27.10,0:00:30.00,Line,,0,0,0,,{\fad(300,0)}Wear the golden hour.
ASS
A=audio
ffmpeg -v error -y -i final/_video.mp4 -i $A/music.mp3 -i $A/music.mp3 -i $A/sfx_city.mp3 -i $A/sfx_tick.mp3 -i $A/sfx_spray.mp3 -i $A/sfx_rewind.mp3 -i $A/sfx_click.mp3 \
 -i $A/vee_l1b.mp3 -i $A/vee_l2b.mp3 -i $A/vee_tag.mp3 -i $A/sfx_click.mp3 -filter_complex "\
[1:a]atrim=0:15.6,asetpts=N/SR/TB,afade=t=in:d=0.6,afade=t=out:st=15.0:d=0.6,volume=0.8[m1];\
[2:a]atrim=17.8:29.9,asetpts=N/SR/TB,afade=t=in:d=1.2,afade=t=out:st=8.6:d=1.4,volume=0.85,adelay=20200:all=1[m2];\
[3:a]afade=t=in:d=0.5,afade=t=out:st=6.5:d=1.5,volume=0.4[city];\
[4:a]afade=t=in:d=0.5,afade=t=out:st=7.6:d=0.4,volume=0.55,adelay=7000:all=1[tick];\
[5:a]volume=1.0,adelay=16700:all=1[spray];\
[6:a]volume=0.8,adelay=19900:all=1[rew];\
[7:a]volume=1.0,adelay=0:all=1[click0];\
[8:a]volume=1.1,adelay=2400:all=1[l1];\
[9:a]volume=1.1,adelay=23950:all=1[l2];\
[10:a]volume=1.1,adelay=26700:all=1[tag];\
[11:a]volume=1.0,adelay=23400:all=1[click1];\
[m1][m2][city][tick][spray][rew][click0][l1][l2][tag][click1]amix=inputs=11:duration=longest:normalize=0,atrim=0:30,alimiter=limit=0.9[a]" \
 -map 0:v -map "[a]" -vf "subtitles=final/captions.ass:fontsdir=${FONTS:-.}" \
 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -t 30 final/vesper_23_30.mp4
rm -f final/_video.mp4; echo final/vesper_23_30.mp4
