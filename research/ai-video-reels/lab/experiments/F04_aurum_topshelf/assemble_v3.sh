#!/bin/bash
# AURUM "Top Shelf" v3: every sound placed on the measured frame of its action.
# Picture (s): A push 0-4 (x1.25) | B open+pour 4-9 | C raise 9-13 (x1.25) | D real drink 13-17.35 (x1.15) | E leap 17.35-22 (to full white) | F land 22-26 (skips 1 s of glare) | G set glass down + packshot 26-30 (x1.25)
# Events: tab pop 5.15 | pour 7.6 | gulp 16.0 | leap 18.55 | landing 22.25 | Vee's click 24.8 | glass on box 28.45
# usage: FONTS=/path/to/fontdir ./assemble_v3.sh
set -e
cd "$(dirname "$0")"; mkdir -p final; C=clips
N="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24"
ffmpeg -v error -y -i $C/A_push_t01.mp4 -i $C/B_open_t01.mp4 -i $C/C_sip2_t01.mp4 -i $C/D_drink_t01.mp4 -i $C/E_dive_t01.mp4 -i $C/F_land3_t01.mp4 -i $C/G_pack4_t01.mp4 -filter_complex "\
[0:v]setpts=PTS/1.25,trim=0:4,setpts=PTS-STARTPTS,$N[a];\
[1:v]trim=start=0.0417:duration=5,setpts=PTS-STARTPTS,$N[b];\
[2:v]trim=start=0.0417,setpts=(PTS-STARTPTS)/1.25,trim=0:4,setpts=PTS-STARTPTS,$N[c];\
[3:v]trim=start=0.0417,setpts=(PTS-STARTPTS)/1.15,trim=0:4.35,setpts=PTS-STARTPTS,$N[d];\
[4:v]trim=start=0.0417:duration=4.65,setpts=PTS-STARTPTS,$N[e];\
[5:v]trim=start=1.0:duration=4,setpts=PTS-STARTPTS,$N[f];\
[6:v]trim=start=0.0417,setpts=(PTS-STARTPTS)/1.25,trim=0:4,setpts=PTS-STARTPTS,$N[g];\
[a][b][c][d][e][f][g]concat=n=7:v=1,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 -preset slow -t 30 final/_video.mp4
cat > final/captions_v3.ass <<'ASS'
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Line,Instrument Serif,78,&H00F2F4F7,&H00000000,&H00101010,&H64000000,0,1,0,0,100,100,0,0,1,2,3,2,80,80,330,1
Style: Name,Instrument Serif,44,&H0060B8E6,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,2,0,1,1.5,2,2,80,80,450,1
Style: Top,Instrument Serif,70,&H00F2F4F7,&H00000000,&H00101010,&H64000000,0,1,0,0,100,100,0,0,1,2,3,8,80,80,230,1
Style: TopName,Instrument Serif,44,&H0060B8E6,&H00000000,&H00101010,&H64000000,0,0,0,0,100,100,2,0,1,1.5,2,8,80,80,170,1
Style: Super,Instrument Serif,34,&H99FFFFFF,&H00000000,&H00000000,&H00000000,0,1,0,0,100,100,1,0,1,0,1,3,0,48,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:30.00,Super,,0,0,0,,AI-generated film · VXO
Dialogue: 0,0:00:23.10,0:00:24.40,Name,,0,0,0,,OTTO
Dialogue: 0,0:00:23.10,0:00:24.40,Line,,0,0,0,,{\fad(120,120)}One more take?
Dialogue: 0,0:00:26.00,0:00:30.00,TopName,,0,0,0,,OTTO
Dialogue: 0,0:00:26.00,0:00:30.00,Top,,0,0,0,,{\fad(150,0)}AURUM. Sparkling yuzu. Taste it from the top.
ASS
A=audio
ffmpeg -v error -y -i final/_video.mp4 \
 -i $A/music_topic.mp3 -i $A/music_soar.mp3 -i $A/music.mp3 \
 -i $A/sfx_wind.mp3 -i $A/sfx_pop.mp3 -i $A/sfx_pour.mp3 -i $A/sfx_gulp.mp3 -i $A/sfx_whoosh.mp3 \
 -i $A/sfx_thump.mp3 -i $A/sfx_set.mp3 -i $A/sfx_click.mp3 -i $A/sfx_clink.mp3 \
 -i $A/otto_onemore.mp3 -i $A/otto_tag.mp3 -filter_complex "\
[1:a]atrim=0:17.75,asetpts=N/SR/TB,afade=t=in:d=0.4,afade=t=out:st=17.6:d=0.15,volume=0.85[m1];\
[2:a]atrim=0.6:4.1,asetpts=N/SR/TB,volume=3.2,afade=t=in:d=0.15,afade=t=out:st=3.4:d=0.1,adelay=18500:all=1[m2];\
[3:a]atrim=35.6:39.6,asetpts=N/SR/TB,afade=t=in:d=0.2,afade=t=out:st=3.2:d=0.8,volume=0.6,adelay=26000:all=1[m3];\
[4:a]atrim=0:5,afade=t=in:d=0.4,afade=t=out:st=3.4:d=1.4,volume=0.5[wind];\
[5:a]volume=0.9,adelay=5130:all=1[pop];\
[6:a]atrim=0:2.9,afade=t=out:st=2.3:d=0.6,volume=0.7,adelay=7470:all=1[pour];\
[7:a]volume=1.0,adelay=14970:all=1[gulp];\
[8:a]volume=0.7,adelay=18270:all=1[whoosh];\
[9:a]volume=1.0,adelay=22190:all=1[thump];\
[10:a]atrim=0:4,afade=t=in:d=0.3,afade=t=out:st=3.4:d=0.6,volume=0.3,adelay=22300:all=1[set];\
[11:a]volume=1.0,adelay=24680:all=1[click];\
[12:a]volume=0.8,adelay=28420:all=1[clink];\
[13:a]volume=1.1,adelay=23100:all=1[o1];\
[14:a]atempo=1.1,volume=1.1,adelay=26000:all=1[o2];\
[m1][m2][m3][wind][pop][pour][gulp][whoosh][thump][set][click][clink][o1][o2]amix=inputs=14:duration=longest:normalize=0,atrim=0:30,alimiter=limit=0.9[a]" \
 -map 0:v -map "[a]" -vf "subtitles=final/captions_v3.ass:fontsdir=${FONTS:-.}" \
 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -t 30 final/aurum_topshelf_30.mp4
rm -f final/_video.mp4; echo final/aurum_topshelf_30.mp4
