import re, sys, glob, json, random, os
HERE = os.path.dirname(os.path.abspath(__file__))
from collections import Counter

def parse_file(path):
    txt = open(path, encoding="utf-8").read()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", txt) if b.strip()]
    qs = []
    for b in blocks:
        lines = [l.rstrip() for l in b.split("\n")]
        if not lines[0].startswith("@"):
            raise ValueError(f"{path}: block without @: {lines[0][:60]}")
        head = lines[0][1:].split()
        lo = head[0]; keep = "k" in head[1:]
        q = {"lo": lo, "keep": keep, "stem": None, "correct": None, "wrong": [], "expl": None}
        for l in lines[1:]:
            if l.startswith("Q: "): q["stem"] = l[3:].strip()
            elif l.startswith("+ "):
                if q["correct"]: raise ValueError(f"{path}: two correct in {q['stem']}")
                q["correct"] = l[2:].strip()
            elif l.startswith("- "): q["wrong"].append(l[2:].strip())
            elif l.startswith("E: "): q["expl"] = l[3:].strip()
            else: raise ValueError(f"{path}: bad line '{l}' in {q['stem']}")
        if not (q["stem"] and q["correct"] and q["expl"] and len(q["wrong"]) == 3):
            raise ValueError(f"{path}: incomplete: {q}")
        if len(set([q["correct"]] + q["wrong"])) != 4:
            raise ValueError(f"{path}: duplicate options: {q['stem']}")
        qs.append(q)
    return qs

if __name__ == "__main__":
    allq = []
    for f in sorted(glob.glob(os.path.join(HERE, "t*.txt"))):
        qs = parse_file(f); allq += qs
        print(f, len(qs))
    c = Counter(q["lo"] for q in allq)
    topic = Counter(q["lo"].split(".")[0] for q in allq)
    print("TOTAL", len(allq))
    print(sorted(topic.items(), key=lambda x: int(x[0])))
    print(sorted(c.items(), key=lambda x: [int(p) for p in x[0].split(".")]))
    stems = Counter(q["stem"] for q in allq)
    d = [s for s, n in stems.items() if n > 1]
    if d: print("DUP STEMS:", d)
