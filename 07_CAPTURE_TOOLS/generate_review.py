"""Generate a human-readable side-by-side review of the 62 needs_human_choice
words: the stored definition vs the retrieved 1773 text. Read-only; changes
nothing in the library."""
import json, re
from pathlib import Path

LIBDIR = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE/03_LIBRARIES")
lib = json.loads((LIBDIR / "VERITAS_definitions_library.json").read_text(encoding="utf-8"))

flagged = [e for e in lib["entries"]
           if e.get("verification_status") == "needs_human_choice"]
flagged.sort(key=lambda e: e["word"].lower())

CAP = 1400  # cap very long 1773 entries for readability

lines = []
lines.append("VERITAS 1773 REVIEW -- words where stored text and 1773 text DIFFER")
lines.append(f"{len(flagged)} words need your choice. Nothing here has been changed.")
lines.append("For each: choose  [S] keep stored   [J] adopt 1773   [B] keep both")
lines.append("=" * 78)
for i, e in enumerate(flagged, 1):
    r = e["retrieved_1773"]
    got = r["normalized_text"]
    if len(got) > CAP:
        got = got[:CAP].rstrip() + f"\n      ...[truncated; full text in library entry '{e['word']}' -> retrieved_1773]"
    lines.append("")
    lines.append(f"[{i:>2}/{len(flagged)}]  {e['word'].upper()}    ({r['part_of_speech']}, 1773)")
    lines.append("-" * 78)
    lines.append("  STORED (currently on file):")
    for ln in (e.get("definition", "") or "(empty)").split("\n"):
        lines.append("      " + ln)
    lines.append("")
    lines.append("  RETRIEVED 1773:")
    for ln in got.split("\n"):
        lines.append("      " + ln)
    lines.append("")
    lines.append("  YOUR CHOICE:  [ ] S keep stored   [ ] J adopt 1773   [ ] B keep both")
    lines.append("=" * 78)

out = LIBDIR / "johnson_1773_REVIEW_needs_choice.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {out} ({len(flagged)} words).")
# Print the first 3 as a preview
print("\n".join(lines[:0]))
preview_end = 0
shown = 0
for idx, ln in enumerate(lines):
    if ln.startswith("[") and "]" in ln[:8]:
        shown += 1
    if shown == 4:
        preview_end = idx
        break
print("\n".join(lines[4:preview_end if preview_end else 60]))
