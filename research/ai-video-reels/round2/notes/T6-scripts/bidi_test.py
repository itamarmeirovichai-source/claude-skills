import subprocess, sys, numpy as np
# tokens colored: R,G,B,Y,M,C ... ; report left->right order of colors
COL=[("R",(255,0,0)),("G",(0,255,0)),("B",(0,0,255)),("Y",(255,255,0)),("M",(255,0,255)),("C",(0,255,255)),("W",(255,255,255))]
def asscol(rgb): r,g,b=rgb; return f"&H00{b:02X}{g:02X}{r:02X}&"
def run(tokens, enc, prefix=""):
    txt=prefix+" ".join("{\\c"+asscol(COL[i][1])+"}"+t for i,t in enumerate(tokens))
    ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1600
PlayResY: 200

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Heebo,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,10,10,0,{enc}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.00,S,,0,0,0,,{txt}
"""
    open("b.ass","w").write(ass)
    raw=subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i","color=black:s=1600x200:d=1","-vf","ass=b.ass:fontsdir=.","-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    img=np.frombuffer(raw,np.uint8).reshape(200,1600,3).astype(int)
    pos=[]
    for i,t in enumerate(tokens):
        c=np.array(COL[i][1]); m=(np.abs(img-c).sum(axis=2)<60)
        xs=np.where(m.any(axis=0))[0]
        pos.append((xs.mean() if len(xs) else -1, t))
    return " | ".join(t for _,t in sorted(pos))
cases=[["יצרתי","את","זה","ב-Seedance","2.5","תוך","10 דקות!"],["המחיר:","99","₪","(במקום","199)"],["AI","זה","העתיד"],["ראשון","שני","שלישי"]]
for enc,pre in [(1,""),(-1,""),(1,"‏"),(-1,"‏")]:
    print(f"Encoding={enc} prefix={'RLM' if pre else 'none'}")
    for c in cases: print("   L->R:", run(c,enc,pre))
