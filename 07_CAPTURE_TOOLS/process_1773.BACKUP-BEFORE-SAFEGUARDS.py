"""
Process the 1773 scrape into the VERITAS definitions library.

Reads:  03_LIBRARIES/johnson_1773_results.json   (raw scrape)
Base:   03_LIBRARIES/VERITAS_definitions_library.BACKUP-BEFORE-1773.json  (pristine)
Writes: all FOUR active VERITAS_definitions_library.json copies (identically)
        03_LIBRARIES/johnson_1773_results.json   (enriched with disposition)
        03_LIBRARIES/johnson_1773_report.txt      (plain-English report)
        03_LIBRARIES/johnson_1773_report.json     (structured report)

HARD RULES honoured:
  * Definition text is only ever the verbatim text captured from the site.
    Nothing is invented, paraphrased, or "cleaned up" beyond long-s / display
    normalisation, and even then the verbatim `original_text` is kept intact.
  * VERIFY: existing word -> if the stored gloss(es) appear verbatim inside the
    1773 text, mark verified_1773; otherwise KEEP BOTH and mark
    needs_human_choice. The script never overwrites a stored definition and
    never decides a genuine mismatch.
  * NOT_FOUND / error words never enter the library; they go to the report.
  * Reads from the pristine backup so re-running is safe and reproducible.
"""
import json, re, unicodedata
from pathlib import Path

LIBDIR = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE/03_LIBRARIES")
GATE = Path("/home/noneya/Projects/VERITAS_MASTER_MERGE/02_GATE_BLACKLETTER")
RESULTS = LIBDIR / "johnson_1773_results.json"
BACKUP = LIBDIR / "VERITAS_definitions_library.BACKUP-BEFORE-1773.json"

LIB_COPIES = [
    LIBDIR / "VERITAS_definitions_library.json",
    GATE / "gate" / "VERITAS_definitions_library.json",
    GATE / "engine" / "VERITAS_definitions_library.json",
    GATE / "nova_johnson" / "VERITAS_definitions_library.json",
]

# ----------------------------------------------------------------------------
def normalize_text(s: str) -> str:
    """normalized_text: long-s + obvious display artifacts only. NOTHING reworded."""
    if not s:
        return ""
    s = s.replace("ſ", "s")          # long s -> s
    s = s.replace("’", "'").replace("‘", "'")   # curly single quotes
    s = s.replace("“", '"').replace("”", '"')   # curly double quotes
    s = s.replace(" ", " ")          # non-breaking space
    s = s.replace("–", "-").replace("—", "--")  # en/em dash artifacts
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def match_key(s: str) -> str:
    """Aggressive normal form used ONLY for substance comparison (not stored)."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("ſ", "s")
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)     # drop all punctuation incl. sense numbers
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def split_senses(stored: str):
    """Split a stored definition into its numbered senses; if none, one sense."""
    parts = re.split(r"(?:^|\s)\d+\.\s+", stored.strip())
    parts = [p.strip() for p in parts if p.strip()]
    return parts if parts else [stored.strip()]


def verify(stored_def: str, retrieved_text: str):
    """Return 'verified_1773' iff every stored sense-gloss appears verbatim
    (normalised) inside the retrieved 1773 text; else 'needs_human_choice'."""
    if not stored_def or not stored_def.strip():
        return "needs_human_choice"      # nothing to verify against -> defer to human
    hay = match_key(retrieved_text)
    for sense in split_senses(stored_def):
        needle = match_key(sense)
        if needle and needle not in hay:
            return "needs_human_choice"
    return "verified_1773"


def combined(entries):
    """Combine multiple 1773 rows for one word, in order, verbatim."""
    return "\n\n".join(e["definition_text"] for e in entries)


# ----------------------------------------------------------------------------
def main():
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    lib = json.loads(BACKUP.read_text(encoding="utf-8"))
    entries = lib["entries"]
    index = {e["word"].lower(): i for i, e in enumerate(entries)}

    counts = {"verified": 0, "needs_human_choice": 0, "added": 0,
              "not_found": 0, "error": 0}
    verified_words, flagged_words, added_words = [], [], []
    not_found_words, error_words = [], []

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
        orig = combined(rows)
        norm = normalize_text(orig)
        pos = "; ".join(dict.fromkeys(e["part_of_speech"] for e in rows if e["part_of_speech"]))
        senses = [{"title": e["title"], "part_of_speech": e["part_of_speech"],
                   "original_text": e["definition_text"]} for e in rows]

        if wl in index:
            e = entries[index[wl]]
            status = verify(e.get("definition", ""), orig)
            e["verification_status"] = status
            e["retrieved_1773"] = {
                "source": "Johnson", "year": 1773, "part_of_speech": pos,
                "original_text": orig, "normalized_text": norm,
                "source_status": "site_transcription",
                "senses_1773": senses,
                "note": "Captured verbatim from johnsonsdictionaryonline.com (1773, 4th folio ed.).",
            }
            if status == "verified_1773":
                counts["verified"] += 1
                verified_words.append(w)
                r["disposition"] = "verified_1773"
            else:
                counts["needs_human_choice"] += 1
                flagged_words.append(w)
                r["disposition"] = "needs_human_choice"
                # KEEP BOTH: stored `definition` left intact; retrieved added above.
        else:
            n = len(rows)
            note = (f"Captured verbatim from johnsonsdictionaryonline.com (1773, 4th folio ed.); "
                    f"{n} sense-entr{'y' if n==1 else 'ies'}. New word, not previously in library. "
                    f"`definition` mirrors `normalized_text` (verbatim) so the gate/resolver "
                    f"can source this word; no text was reworded.")
            new_entry = {
                "word": w,
                "source": "Johnson",
                "year": 1773,
                "part_of_speech": pos,
                "original_text": orig,
                "normalized_text": norm,
                "source_status": "site_transcription",
                "verification_status": "verified_1773",
                "notes": note,
                # `definition` is required by the gate's resolver (entry.get("definition"));
                # set to the verbatim normalized 1773 text so new words are actually sourced.
                "definition": norm,
                "senses_1773": senses,
            }
            entries.append(new_entry)
            counts["added"] += 1
            added_words.append(w)
            r["disposition"] = "added"

    lib["total_entries"] = len(entries)
    lib.setdefault("notes", [])
    if isinstance(lib["notes"], list):
        lib["notes"].append(
            "1773 pass (4th folio ed.) applied from johnsonsdictionaryonline.com: "
            f"{counts['added']} words added, {counts['verified']} verified_1773, "
            f"{counts['needs_human_choice']} needs_human_choice. Verbatim transcription only.")

    # Write all four copies identically.
    payload = json.dumps(lib, ensure_ascii=False, indent=1)
    for path in LIB_COPIES:
        path.write_text(payload, encoding="utf-8")

    # Enriched results.json (everything).
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    # Structured report.
    report = {
        "summary": counts,
        "total_words_processed": len(results),
        "library_total_entries_after": len(entries),
        "verified_words": sorted(verified_words),
        "needs_human_choice_words": sorted(flagged_words),
        "added_words_count": len(added_words),
        "not_found_words": sorted(not_found_words),
        "error_words": sorted(error_words),
    }
    (LIBDIR / "johnson_1773_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    # Plain-English report.
    lines = []
    lines.append("VERITAS -- Johnson's Dictionary 1773 (4th folio ed.) pass")
    lines.append("=" * 60)
    lines.append(f"Words processed (from filtered list): {len(results)}")
    lines.append("")
    lines.append(f"  VERIFIED against 1773 (verified_1773):      {counts['verified']}")
    lines.append(f"  MISMATCHES needing your choice:             {counts['needs_human_choice']}")
    lines.append(f"  NEW words ADDED to the library:             {counts['added']}")
    lines.append(f"  NOT FOUND in 1773 (site returned nothing):  {counts['not_found']}")
    if counts["error"]:
        lines.append(f"  PAGE ERRORS (treated as not-in-library):    {counts['error']}")
    lines.append("")
    lines.append(f"Library entries before: 209   after: {len(entries)}")
    lines.append("")
    lines.append("WHAT THE STATUSES MEAN")
    lines.append("-" * 60)
    lines.append("verified_1773     : the stored gloss appears verbatim inside the")
    lines.append("                    retrieved 1773 entry (formatting/long-s aside).")
    lines.append("needs_human_choice: the stored text and the 1773 text differ. BOTH")
    lines.append("                    are kept; the stored definition was NOT changed.")
    lines.append("                    You decide which to keep -- see `retrieved_1773`")
    lines.append("                    on each such entry in the library.")
    lines.append("")
    if flagged_words:
        lines.append(f"WORDS NEEDING YOUR CHOICE ({len(flagged_words)}):")
        lines.append("  " + ", ".join(sorted(flagged_words)))
        lines.append("")
    lines.append(f"NOT-FOUND LIST ({len(not_found_words)}) -- never added to the library:")
    if not_found_words:
        for i in range(0, len(sorted(not_found_words)), 10):
            lines.append("  " + ", ".join(sorted(not_found_words)[i:i+10]))
    else:
        lines.append("  (none)")
    lines.append("")
    if error_words:
        lines.append(f"PAGE-ERROR LIST ({len(error_words)}) -- also not added:")
        lines.append("  " + ", ".join(sorted(error_words)))
        lines.append("")
    (LIBDIR / "johnson_1773_report.txt").write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print("\nReports written to 03_LIBRARIES/johnson_1773_report.txt and .json")


if __name__ == "__main__":
    main()
