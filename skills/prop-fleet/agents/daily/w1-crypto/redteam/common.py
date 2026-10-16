import sys, os, pickle, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/claude-skills/skills/prop-fleet/agents/daily/w1-crypto")
import d3lib as L
S="/tmp/claude-0/-home-user-claude-skills/8eca21fd-129a-52ba-a3be-cd685444e0e4/scratchpad"
def data():
    p=f"{S}/redteam/data.pkl"
    if os.path.exists(p): return pickle.load(open(p,"rb"))
    d=L.load(f"{S}/data"); pickle.dump(d,open(p,"wb")); return d
