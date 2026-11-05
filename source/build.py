import re, json, glob, random, hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__))
from collections import Counter
from parse import parse_file

TOPICS = {
 1: "Normal sleep, sleep disorders and the pathophysiology of SDB",
 2: "Diagnostic sleep testing in SDB",
 3: "Oral appliance therapy and other evidence-based treatments",
 4: "History, examination and imaging for patient selection",
 5: "Appliance selection, impressions, bite registration and fitting",
 6: "Assessing effectiveness and titrating the appliance",
 7: "Long-term follow-up of oral appliance therapy",
 8: "Paediatric sleep-disordered breathing",
 9: "Best-practice principles in dental sleep medicine",
 10: "Informed consent and management of side effects",
}
SHORT = {
 "1.1":"Health benefits of sleep","1.2":"Physiology of normal sleep","1.3":"Pathophysiology of SDB",
 "1.4":"Prevalence and comorbidities","1.5":"Risk factors, age and gender","1.6":"Signs and symptoms",
 "1.7":"Impact on the individual","1.8":"Impact on society","1.9":"Insomnia",
 "1.10":"Other respiratory sleep disorders","1.11":"Other non-respiratory sleep disorders","1.12":"Drugs and sleep",
 "2.1":"Normal PSG parameters","2.2":"Pathological PSG parameters","2.3":"Interpreting the PSG for treatment",
 "2.4":"Treatment efficacy on PSG","2.5":"Attended vs home studies","2.6":"MSLT and MWT","2.7":"Screening for SDB",
 "3.1":"History of OAT","3.2":"Mechanism of OAT","3.3":"OAT indications and contraindications",
 "3.4":"PAP therapies","3.5":"Surgical options","3.6":"Positional, weight loss, hygiene, CBT",
 "3.7":"Emerging therapies","3.8":"Combination therapies","3.9":"OAT vs other treatments",
 "3.10":"Mean disease alleviation","3.11":"Guidelines and evidence-based practice",
 "4.1":"DSM history, goals, expectations","4.2":"Medical history modifiers","4.3":"SDB and other sleep problems",
 "4.4":"Medical comorbidities","4.5":"Ethics and consent","4.6":"Multidisciplinary team",
 "4.7":"Sleep bruxism and SDB","4.8":"Pain and sleep",
 "5.1":"The 2015 clinical practice guideline","5.2":"Mechanism and predicting success","5.3":"Indications and contraindications",
 "5.4":"Designs, materials, fabrication","5.5":"Selecting the device","5.6":"Bite registration",
 "5.7":"Impression materials","5.8":"Laboratory request","5.9":"Delivery and fitting","5.10":"Home care instructions",
 "6.1":"Titration and the chief complaint","6.2":"Follow-up signs and symptoms","6.3":"Referral for objective testing",
 "6.4":"Treatment sleep study protocols","6.5":"Efficacy and limitations","6.6":"Adherence and compliance",
 "7.1":"Long-term modifiers","7.2":"Documenting the complaint over time","7.3":"Modification for progressive disease",
 "7.4":"The yearly review",
 "8.1":"Prevalence in children","8.2":"Aetiology and pathophysiology","8.3":"Signs and symptoms",
 "8.4":"Poor sleep in children","8.5":"Poor sleep in adolescents","8.6":"Paediatric screening",
 "8.7":"Paediatric treatment","8.8":"Children vs adults","8.9":"Syndromes and medical conditions","8.10":"Referral pathways",
 "9.1":"Diagnosis by a physician","9.2":"Record keeping","9.3":"Billing and item codes","9.4":"Ethics in DSM",
 "10.1":"Informed consent","10.2":"Side effect expectations","10.3":"Protrusion and craniofacial structures",
 "10.4":"Occlusal guide and exercises","10.5":"Managing side effects","10.6":"Suspending or abandoning OAT",
}
full = {}
for line in open(os.path.join(HERE, "lo_raw.txt"), encoding="utf-8"):
    code, title = line.rstrip("\n").split("|", 1)
    t = re.sub(r"\s+", " ", title).strip().rstrip(".")
    t = t.replace("Simulation", "Stimulation").replace("how its influences", "how it influences")
    full[code] = t

def typo(s):
    s = re.sub(r'"([^"]*)"', "\u201c\\1\u201d", s)
    s = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", s)
    s = re.sub(r"(\w)'", "\\1\u2019", s)
    return s

NUMRE = re.compile(r"^[~<>≥≤+\-−]?\s*(\d+(?:\.\d+)?)")
def numeric_key(opt):
    m = NUMRE.match(opt)
    return float(m.group(1)) if m else None

allq = []
for f in sorted(glob.glob(os.path.join(HERE, "t*.txt")), key=lambda p: (int(re.search(r"t(\d+)", p).group(1)), p)):
    allq += parse_file(f)

allq.sort(key=lambda q: [int(x) for x in q["lo"].split(".")])
out = []; per = Counter(); pos = Counter()
for q in allq:
    opts = [q["correct"]] + q["wrong"]
    keys = [numeric_key(o) for o in opts]
    if all(k is not None for k in keys):
        order = sorted(range(4), key=lambda i: (keys[i], i))
    elif q["keep"]:
        order = list(range(4))
    else:
        seed = int(hashlib.md5(q["stem"].encode()).hexdigest(), 16)
        order = list(range(4)); random.Random(seed).shuffle(order)
    new = [opts[i] for i in order]
    ans = order.index(0)
    pos[ans] += 1
    per[q["lo"]] += 1
    out.append({"id": f'{q["lo"]}.{per[q["lo"]]}', "lo": q["lo"], "s": typo(q["stem"]),
                "o": [typo(x) for x in new], "a": ans, "e": typo(q["expl"])})

los = [{"c": c, "t": SHORT[c], "f": typo(full[c]), "n": per[c]} for c in sorted(per, key=lambda x: [int(p) for p in x.split(".")])]
data = {"topics": [{"n": n, "t": t} for n, t in TOPICS.items()], "los": los, "q": out}
os.makedirs(os.path.join(HERE, "..", "data"), exist_ok=True)
json.dump(data, open(os.path.join(HERE, "..", "data", "questions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
compact = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
open(os.path.join(HERE, "..", "index.html"), "w", encoding="utf-8").write(tpl.replace("__DATA__", compact))
print(len(out), "questions; answer positions", dict(sorted(pos.items())))
print("missing LOs:", set(full) - set(per))
