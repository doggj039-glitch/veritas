"""Build the filtered word list for the 1773 full run.
Rule: use the `word` column of blackletter_definition_audit_words.csv,
skip pure numbers, single letters, and US state names. Preserve order, dedupe."""
import csv, json, re
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE")
CSV = ROOT / "05_AUDIT" / "blackletter_definition_audit_words.csv"
OUT = ROOT / "03_LIBRARIES" / "johnson_1773_wordlist.json"

STATES = {s.lower() for s in [
    "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
    "Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa",
    "Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
    "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
    "New Hampshire","New Jersey","New Mexico","New York","North Carolina",
    "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
    "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
    "Virginia","Washington","West Virginia","Wisconsin","Wyoming",
    # also skip the multi-word states collapsed to a single token, just in case
    "newhampshire","newjersey","newmexico","newyork","northcarolina","northdakota",
    "rhodeisland","southcarolina","southdakota","westvirginia",
]}

kept, skipped = [], {"number": [], "single_letter": [], "state": [], "blank": [], "dup": []}
seen = set()

with open(CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        w = (row.get("word") or "").strip()
        low = w.lower()
        if not w:
            skipped["blank"].append(w); continue
        if re.fullmatch(r"\d+", w):
            skipped["number"].append(w); continue
        if len(w) == 1:
            skipped["single_letter"].append(w); continue
        if low in STATES:
            skipped["state"].append(w); continue
        if low in seen:
            skipped["dup"].append(w); continue
        seen.add(low)
        kept.append(w)

OUT.write_text(json.dumps(kept, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"TOTAL CSV data rows -> kept {len(kept)} words")
for k, v in skipped.items():
    if v:
        print(f"  skipped {k}: {len(v)}  e.g. {v[:12]}")
print(f"\nWord list written to {OUT}")
print("First 20:", kept[:20])
print("Last 20:", kept[-20:])
