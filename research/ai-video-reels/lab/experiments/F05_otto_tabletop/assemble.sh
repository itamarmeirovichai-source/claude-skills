#!/bin/bash
# OTTO-1 "Tabletop city": 5 keyframe-matched Kling shots -> one 30 s continuous take + sound map + captions.
# Timeline (s): A out-of-viewfinder 0-5 | B sun drag 5-10 | C crane reveal 10-20 | D Vee click 20-25 | E tiny Otto 25-30
# usage: FONTS=/path/to/fontdir ./assemble.sh
set -e
cd "$(dirname "$0")"; mkdir -p final; C=clips
ffmpeg -v error -y -i $C/A_out_t01.mp4 -i $C/B_sun_t01.mp4 -i $C/C_reveal_t01.mp4 -i $C/D_click_t01.mp4 -i $C/E_tiny_t01.mp4 -filter_complex "\
[0:v]trim=0:5,setpts=PTS-STARTPTS[a];\
[1:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS[b];\
[2:v]trim=start=0.0417:duration=10,setpts=PTS-STARTPTS[c];\
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
Style: Name,Instrument Serif,44,&H0060B8E6,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,2,0,1,1.5,2,2,80,80,430,1
Style: Super,Instrument Serif,34,&H99FFFFFF,&H00000000,&H00000000,&H00000000,0,1,0,0,100,100,1,0,1,0,1,3,0,48,60,1
Style: Tag,Instrument Serif,120,&H00F2F4F7,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,12,0,1,2,3,8,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:30.00,Super,,0,0,0,,AI-generated film · VXO
Dialogue: 0,0:00:05.40,0:00:07.30,Name,,0,0,0,,OTTO
Dialogue: 0,0:00:05.40,0:00:07.30,Line,,0,0,0,,{\fad(120,120)}A little to the left.
Dialogue: 0,0:00:25.20,0:00:26.30,Name,,0,0,0,,OTTO
Dialogue: 0,0:00:25.20,0:00:26.30,Line,,0,0,0,,{\fad(120,120)}Perfect.
Dialogue: 0,0:00:26.40,0:00:30.00,Name,,0,0,0,,VEE
Dialogue: 0,0:00:26.40,0:00:30.00,Line,,0,0,0,,{\fad(150,0)}Big films. No crew. Thirty seconds.
Dialogue: 0,0:00:27.00,0:00:30.00,Tag,,0,0,0,,{\fad(300,0)}VXO
ASS
A=audio
# Score is epic until the reveal, then lowpassed and quiet: it "becomes" the sound of a tiny set.
ffmpeg -v error -y -i final/_video.mp4 -i $A/music.mp3 -i $A/music.mp3 -i $A/sfx_wind.mp3 -i $A/sfx_sun.mp3 -i $A/sfx_room.mp3 -i $A/sfx_click.mp3 \
 -i $A/otto_left.mp3 -i $A/otto_perfect.mp3 -i $A/vee_tag.mp3 -filter_complex "\
[1:a]atrim=0:17.6,asetpts=N/SR/TB,afade=t=in:d=0.5,afade=t=out:st=17.2:d=0.4,volume=0.85[m1];\
[2:a]atrim=17.4:30,asetpts=N/SR/TB,lowpass=f=1100,highpass=f=300,volume=0.35,afade=t=in:d=0.4,afade=t=out:st=11.6:d=1,adelay=17400:all=1[m2];\
[3:a]atrim=0:5,afade=t=out:st=3.5:d=1.5,volume=0.5[wind];\
[4:a]volume=0.7,adelay=6300:all=1[sun];\
[5:a]afade=t=in:d=1,volume=0.45,adelay=17500:all=1[room];\
[6:a]volume=1.0,adelay=21900:all=1[click];\
[7:a]volume=1.1,adelay=5400:all=1[o1];\
[8:a]volume=1.1,adelay=25200:all=1[o2];\
[9:a]volume=1.1,adelay=26400:all=1[v1];\
[m1][m2][wind][sun][room][click][o1][o2][v1]amix=inputs=9:duration=longest:normalize=0,atrim=0:30,alimiter=limit=0.9[a]" \
 -map 0:v -map "[a]" -vf "subtitles=final/captions.ass:fontsdir=${FONTS:-.}" \
 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -t 30 final/otto_tabletop_30.mp4
rm -f final/_video.mp4; echo final/otto_tabletop_30.mp4
