"""
Process the SECOND 1773 pass (the previously-not-found words) into the library.

DIFFERENT FROM process_1773.py IN ONE CRUCIAL WAY (Hard Rule 2):
  * process_1773.py rebuilds from the OLD pristine 209-word backup.
  * THIS script loads its base from the CURRENT 918-entry library snapshot
    (VERITAS_definitions_library.BACKUP-BEFORE-MISSED-WORDS-PASS.json, which is
    the exact state of the live library right before this pass), so the 709
    words added in the first run are preserved, not erased.

Reuses the SAME verify / normalize / mismatch-check logic from process_1773.py.

Reads:  03_LIBRARIES/johnson_missed_words_results.json
Base:   03_LIBRARIES/VERITAS_definitions_library.BACKUP-BEFORE-MISSED-WORDS-PASS.json
Writes: all FOUR active VERITAS_definitions_library.json copies (identically)
        03_LIBRARIES/johnson_missed_words_results.json  (enriched with disposition)
        03_LIBRARIES/johnson_missed_words_report.txt / .json

Root-retry note: a word recovered via a root form was already validated at scrape
time with headword_matches(root, ...). So the add-branch mismatch check is run
against the ROOT for those words (checking the inflected original would wrongly
reject legitimate recoveries like acts->act). Direct finds are checked against
the searched word itself.
"""
import json, hashlib
from pathlib import Path

from headword_check import headword_matches
from process_1773 import normalize_text, verify, combined

LIBDIR = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE/03_LIBRARIES")
GATE = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE/02_GATE_BLACKLETTER")
RESULTS = LIBDIR / "johnson_missed_words_results.json"
BASE = LIBDIR / "VERITAS_definitions_library.BACKUP-BEFORE-MISSED-WORDS-PASS.json"

LIB_COPIES = [
    LIBDIR / "VERITAS_definitions_library.json",
    GATE / "gate" / "VERITAS_definitions_library.json",
    GATE / "engine" / "VERITAS_definitions_library.json",
    GATE / "nova_johnson" / "VERITAS_definitions_library.json",
]


def main():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    lib = json.loads(BASE.read_text(encoding="utf-8"))
    entries = lib["entries"]
    entries_before = len(entries)
    index = {e["word"].lower(): i for i, e in enumerate(entries)}

    counts = {"verified": 0, "needs_human_choice": 0, "added": 0,
              "added_via_root": 0, "not_found": 0, "error": 0,
              "headword_mismatch": 0}
    verified_words, flagged_words, added_words = [], [], []
    added_via_root_words, not_found_words, error_words, mismatch_words = [], [], [], []

    for r in results:
        w = r["word"]
        wl = w.lower()

        if r["status"] == "error":
            counts["error"] += 1
            error_words.append(w)
            r["disposition"] = "error"
            continue
        if not r["found_1773"]:
            counts["not_found"] += 1
            not_found_words.append(w)
            r["disposition"] = "not_found"
            continue

        rows = r["entries"]
        via_root = bool(r.get("matched_via_root"))
        root_used = r.get("root_used")
        # A root recovery already passed headword_matches(root, ...) at scrape
        # time, so check the ROOT here; a direct find is checked against the word.
        check_word = root_used if via_root else w

        orig = combined(rows)
        norm = normalize_text(orig)
        pos = "; ".join(dict.fromkeys(e["part_of_speech"] for e in rows if e["part_of_speech"]))
        senses = [{"title": e["title"], "part_of_speech": e["part_of_speech"],
                   "original_text": e["definition_text"]} for e in rows]

        if wl in index:
            # Defensive: shouldn't happen (these were all not-found), but keep the
            # same verify behavior as the first pass if it somehow already exists.
            e = entries[index[wl]]
            status = verify(e.get("definition", ""), orig)
            e["verification_status"] = status
            e["retrieved_1773"] = {
                "source": "Johnson", "year": 1773, "part_of_speech": pos,
                "original_text": orig, "normalized_text": norm,
                "source_status": "site_transcription", "senses_1773": senses,
                "note": "Captured verbatim from johnsonsdictionaryonline.com (1773, 4th folio ed.); missed-words pass.",
            }
            if status == "verified_1773":
                counts["verified"] += 1; verified_words.append(w); r["disposition"] = "verified_1773"
            else:
                counts["needs_human_choice"] += 1; flagged_words.append(w); r["disposition"] = "needs_human_choice"
            continue

        # ADD path with SAFEGUARD 1 (headword mismatch check).
        matching_rows = [row for row in rows
                         if headword_matches(check_word, row.get("headword_label", ""))]
        dropped_rows = [row for row in rows
                        if not headword_matches(check_word, row.get("headword_label", ""))]

        if not matching_rows:
            counts["headword_mismatch"] += 1
            mismatch_words.append(w)
            r["disposition"] = "headword_mismatch"
            r["headword_mismatch_detail"] = [
                {"searched": w, "checked_against": check_word,
                 "returned_headword": row.get("headword_label", ""),
                 "title": row.get("title", "")} for row in rows]
            continue

        m_orig = combined(matching_rows)
        m_norm = normalize_text(m_orig)
        m_pos = "; ".join(dict.fromkeys(e["part_of_speech"] for e in matching_rows if e["part_of_speech"]))
        m_senses = [{"title": e["title"], "part_of_speech": e["part_of_speech"],
                     "original_text": e["definition_text"]} for e in matching_rows]
        n = len(matching_rows)
        note = (f"Captured verbatim from johnsonsdictionaryonline.com (1773, 4th folio ed.); "
                f"{n} sense-entr{'y' if n==1 else 'ies'}. New word from the missed-words (2nd) pass. "
                f"`definition` mirrors `normalized_text` (verbatim); no text was reworded.")
        if via_root:
            note += (f" Recovered via root-word retry: searched '{w}', matched Johnson's "
                     f"headword for root '{root_used}'.")
        if dropped_rows:
            dl = ", ".join(f"{row.get('headword_label','')!r} ({row.get('title','')})" for row in dropped_rows)
            note += f" Headword-mismatch safeguard dropped {len(dropped_rows)} non-matching row(s): {dl}."

        new_entry = {
            "word": w,
            "source": "Johnson",
            "year": 1773,
            "part_of_speech": m_pos,
            "original_text": m_orig,
            "normalized_text": m_norm,
            "source_status": "site_transcription",
            "verification_status": "verified_1773",
            "notes": note,
            "definition": m_norm,
            "senses_1773": m_senses,
        }
        if via_root:
            new_entry["matched_via_root"] = True
            new_entry["root_used"] = root_used
        entries.append(new_entry)
        index[wl] = len(entries) - 1
        counts["added"] += 1
        added_words.append(w)
        r["disposition"] = "added"
        if via_root:
            counts["added_via_root"] += 1
            added_via_root_words.append(w)

    lib["total_entries"] = len(entries)
    lib.setdefault("notes", [])
    if isinstance(lib["notes"], list):
        lib["notes"].append(
            "1773 missed-words (2nd) pass: "
            f"{counts['added']} added ({counts['added_via_root']} recovered via root-retry), "
            f"{counts['headword_mismatch']} blocked by headword-mismatch check, "
            f"{counts['not_found']} still not found. Verbatim transcription only.")

    payload = json.dumps(lib, ensure_ascii=False, indent=1)
    for p in LIB_COPIES:
        p.write_text(payload, encoding="utf-8")
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    report = {
        "summary": counts,
        "words_processed": len(results),
        "library_entries_before": entries_before,
        "library_entries_after": len(entries),
        "added_words": sorted(added_words),
        "added_via_root_words": sorted(added_via_root_words),
        "verified_words": sorted(verified_words),
        "needs_human_choice_words": sorted(flagged_words),
        "headword_mismatch_words": sorted(mismatch_words),
        "still_not_found_words": sorted(not_found_words),
        "error_words": sorted(error_words),
    }
    (LIBDIR / "johnson_missed_words_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    L = []
    L.append("VERITAS -- Johnson's 1773 MISSED-WORDS (2nd) pass")
    L.append("=" * 60)
    L.append(f"Words processed (the 496 first-run not-founds): {len(results)}")
    L.append("")
    L.append(f"  VERIFIED against 1773 (verified_1773):        {counts['verified']}")
    L.append(f"  MISMATCHES needing your choice:               {counts['needs_human_choice']}")
    L.append(f"  NEW words ADDED to the library:               {counts['added']}")
    L.append(f"     ...of those, RECOVERED VIA ROOT-RETRY:     {counts['added_via_root']}")
    L.append(f"  HEADWORD MISMATCHES (blocked, need manual):   {counts['headword_mismatch']}")
    L.append(f"  STILL NOT FOUND (no root recovered them):     {counts['not_found']}")
    if counts["error"]:
        L.append(f"  PAGE ERRORS:                                  {counts['error']}")
    L.append("")
    L.append(f"Library entries before: {entries_before}   after: {len(entries)}")
    L.append("")
    L.append(f"RECOVERED VIA ROOT-RETRY ({len(added_via_root_words)}) "
             f"-- inflected forms now sourced from Johnson's root headword:")
    if added_via_root_words:
        for i in range(0, len(sorted(added_via_root_words)), 10):
            L.append("  " + ", ".join(sorted(added_via_root_words)[i:i+10]))
    else:
        L.append("  (none)")
    L.append("")
    L.append(f"HEADWORD MISMATCHES BLOCKED ({len(mismatch_words)}) -- NOT added; manual lookup:")
    if mismatch_words:
        for i in range(0, len(sorted(mismatch_words)), 10):
            L.append("  " + ", ".join(sorted(mismatch_words)[i:i+10]))
    else:
        L.append("  (none)")
    L.append("")
    L.append(f"STILL NOT FOUND ({len(not_found_words)}) -- no root recovered them, never added:")
    if not_found_words:
        for i in range(0, len(sorted(not_found_words)), 10):
            L.append("  " + ", ".join(sorted(not_found_words)[i:i+10]))
    else:
        L.append("  (none)")
    L.append("")
    (LIBDIR / "johnson_missed_words_report.txt").write_text("\n".join(L), encoding="utf-8")

    print("\n".join(L))
    md5s = {hashlib.md5(p.read_bytes()).hexdigest() for p in LIB_COPIES}
    print("\nAll four copies identical:", len(md5s) == 1, "| md5:", md5s.pop()[:12])


if __name__ == "__main__":
    main()
