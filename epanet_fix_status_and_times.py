# epanet_fix_status_and_times.py
import re, io, sys, argparse

def load(p): 
    with open(p, "r", encoding="utf-8", errors="replace") as f: 
        return f.read()
def save(p, s): 
    with open(p, "w", encoding="utf-8") as f: 
        f.write(s)

SEC = re.compile(r'^\s*\[(.+?)\]\s*$', re.M)
ID  = re.compile(r'^\s*([^\s;]+)')

def split_sections(txt):
    marks=[]
    for m in SEC.finditer(txt):
        marks.append((m.group(1).upper(), m.start(), m.end()))
    out=[]
    for i,(nm,st,_)=enumerate(marks):
        en = marks[i+1][1] if i+1<len(marks) else len(txt)
        out.append((nm, st, en))
    return out

def get_block(txt, name):
    name=name.upper()
    for nm,st,en in split_sections(txt):
        if nm==name: return txt[st:en]
    return None

def upsert_block(txt, name, block_body):
    # write full section text given body lines (string)
    name=name.upper()
    new_sec = f'[{name}]\n{block_body.rstrip()}\n'
    buf=io.StringIO(); replaced=False
    for nm,st,en in split_sections(txt):
        seg = txt[st:en]
        if nm==name:
            buf.write(new_sec)
            replaced=True
        else:
            buf.write(seg)
    if not replaced:
        # drop it before [END] if present
        m_end = re.search(r'(?mi)^\s*\[END\]\s*$', txt)
        if m_end:
            return txt[:m_end.start()]+new_sec+txt[m_end.start():]
        else:
            return txt.rstrip()+"\n"+new_sec+"\n[END]\n"
    return buf.getvalue()

def body_only(block):
    # strip the leading [NAME] header line
    lines = block.splitlines()
    return "\n".join(lines[1:]) if lines else ""

def parse_link_ids(block):
    ids=[]
    for ln in body_only(block).splitlines():
        ls=ln.strip()
        if not ls or ls.startswith(";"): 
            continue
        m=ID.match(ls)
        if m: ids.append(m.group(1))
    return ids

def ensure_status_open(txt):
    lids=[]
    for sec in ("PIPES","VALVES","PUMPS"):
        blk = get_block(txt, sec)
        if blk: lids += parse_link_ids(blk)
    # all open
    lines=["; rebuilt by epanet_fix_status_and_times.py"]
    lines += [f"{lid} OPEN" for lid in lids]
    return upsert_block(txt, "STATUS", "\n".join(lines))

def ensure_times(txt):
    # sane defaults
    # Duration 24:00, Hydraulic Timestep 0:15, Pattern Timestep 1:00, Report Timestep 1:00
    body = (
        "; normalized by epanet_fix_status_and_times.py\n"
        "Duration            24:00\n"
        "Hydraulic Timestep  0:15\n"
        "Pattern Timestep    1:00\n"
        "Report Timestep     1:00\n"
        "Report Start        0:00\n"
        "Start ClockTime     12 am\n"
    )
    return upsert_block(txt, "TIMES", body)

def clamp_tanks(txt):
    blk = get_block(txt,"TANKS")
    if not blk: 
        return txt
    out=["[TANKS]"]
    for ln in body_only(blk).splitlines():
        raw=ln.rstrip("\n")
        if not raw.strip() or raw.lstrip().startswith(";"):
            out.append(raw); continue
        parts = raw.split()
        # expect: ID Elev Init Min Max Diam MinVol [VolCurve]
        if len(parts)>=7:
            try:
                elev=float(parts[1]); init=float(parts[2])
                mn=float(parts[3]); mx=float(parts[4])
            except:
                out.append(raw); continue
            # fix if init outside [mn, mx]
            if mx < mn: 
                mx, mn = mn, mx
            mid = (mn+mx)/2.0
            if not (mn <= init <= mx):
                parts[2] = f"{mid:.2f}"
                raw = " ".join(parts)
        out.append(raw)
    return upsert_block(txt,"TANKS","\n".join(out[1:]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", required=True)
    args = ap.parse_args()
    txt = load(args.inp)
    txt = ensure_status_open(txt)
    txt = ensure_times(txt)
    txt = clamp_tanks(txt)
    save(args.inp, txt)
    print("Patched:", args.inp, "→ STATUS OPEN, TIMES sane, TANK inits clamped.")

if __name__=="__main__":
    main()
