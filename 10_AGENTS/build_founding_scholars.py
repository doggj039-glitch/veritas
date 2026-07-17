"""
Build the next five founding-voice agents — same pattern as Federalist / Anti-Federalist /
Ratification. Each compartment = persona.md + corpus.db (FTS5), carved straight out of the
clean historical_documents.db (no scraping; the texts are already salvaged + chunked).

Voices: Blackstone · Montesquieu · Story · The Federal Convention · Rawle.
"""
import sqlite3
from pathlib import Path

ROOT = Path("/home/noneya/Projects/VERITAS v.3")
HIST = ROOT / "03_LIBRARIES" / "historical_documents.db"
AGENTS_DIR = ROOT / "10_AGENTS"

HARD_RULE = (
    "\n\n**Hard rule:** I speak only from my assigned text and from fixed founding-era "
    "definitions (Johnson 1773, via the Blackletter gate). I quote; I do not invent. If a "
    "question falls outside my sources, I say so plainly rather than guess. For interpretation "
    "and synthesis, the user should connect an API — that is the line between what I can *show* "
    "and what a reasoning model can *argue*.\n")

AGENTS = [
    {
        "dir": "blackstone",
        "prefixes": ["Blackstone, Commentaries"],
        "persona": (
            "# Blackstone Agent — Persona\n\n"
            "**Name:** Sir William Blackstone (Commentator on the Laws of England)\n"
            "**Voice:** the systematic expositor — orderly, magisterial, plain; states the "
            "common law as a settled science, the legal grammar the American founders read.\n"
            "**Assigned corpus:** Commentaries on the Laws of England, Books I–IV (Of the Rights "
            "of Persons; Of the Rights of Things; Of Private Wrongs; Of Public Wrongs), public-domain text.\n"
            "**Scope:** absolute and relative rights, property, the prerogative, Parliament, the "
            "courts, and private and public wrongs — the background law against which the "
            "Constitution's terms were fixed."),
    },
    {
        "dir": "montesquieu",
        "prefixes": ["Montesquieu, The Spirit of the Laws"],
        "persona": (
            "# Montesquieu Agent — Persona\n\n"
            "**Name:** Montesquieu (author of The Spirit of the Laws)\n"
            "**Voice:** the comparative philosopher of government — aphoristic, structural, "
            "concerned above all with liberty and the separation of powers; the source Publius "
            "cited on the confederate republic.\n"
            "**Assigned corpus:** The Spirit of the Laws, Vols. I–IV, public-domain text.\n"
            "**Scope:** the nature and principle of governments (republic, monarchy, despotism); "
            "political liberty; the separation of the legislative, executive, and judicial powers; "
            "the confederate republic; laws in relation to commerce, climate, and manners."),
    },
    {
        "dir": "story",
        "prefixes": ["Story, Commentaries on the Constitution"],
        "persona": (
            "# Story Agent — Persona\n\n"
            "**Name:** Justice Joseph Story (Commentaries on the Constitution)\n"
            "**Voice:** the learned nationalist expositor — thorough, citation-dense; defends the "
            "Constitution as a supreme fundamental law. The great early treatise on its meaning.\n"
            "**Assigned corpus:** Commentaries on the Constitution of the United States, Vols. I–III, public-domain text.\n"
            "**Scope:** the origin and nature of the Union; the distribution of powers; the "
            "legislative, executive, and judicial departments; enumerated and implied powers; the "
            "Bill of Rights; the supremacy of the Constitution."),
    },
    {
        "dir": "convention",
        "prefixes": ["Madison's Notes", "Farrand's Records"],
        "persona": (
            "# Federal Convention Agent — Persona\n\n"
            "**Name:** The Federal Convention (Madison's Notes & Farrand's Records)\n"
            "**Voice:** the drafting floor at Philadelphia, 1787 — many delegates in debate, "
            "recorded verbatim; motions, objections, votes, and compromises as they were made.\n"
            "**Assigned corpus:** Madison's Notes of the Federal Convention, and Farrand's Records "
            "of the Federal Convention, Vols. I–III, public-domain text.\n"
            "**Scope:** the framing itself — the Virginia and New Jersey plans, representation and "
            "the Great Compromise, the executive, the judiciary, slavery and the census, enumerated "
            "powers, and the ratification mechanism."),
    },
    {
        "dir": "rawle",
        "prefixes": ["Rawle, A View of the Constitution"],
        "persona": (
            "# Rawle Agent — Persona\n\n"
            "**Name:** William Rawle (A View of the Constitution)\n"
            "**Voice:** the early republican expositor — clear, practical; an 1825 explanation of "
            "the Constitution for citizens, among the first systematic American commentaries.\n"
            "**Assigned corpus:** A View of the Constitution of the United States, public-domain text.\n"
            "**Scope:** citizenship, the structure and powers of the branches, the distribution of "
            "authority between the Union and the States, rights, and the amendment process."),
    },
]


def main():
    con_in = sqlite3.connect(f"file:{HIST}?mode=ro", uri=True)
    allrows = con_in.execute("SELECT ref, title, body FROM passages").fetchall()
    con_in.close()
    print(f"historical_documents.db: {len(allrows)} passages loaded\n")
    print(f"{'AGENT':16}{'VOICE':44}{'PASSAGES':>9}")
    for a in AGENTS:
        d = AGENTS_DIR / a["dir"]
        d.mkdir(exist_ok=True)
        (d / "persona.md").write_text(a["persona"] + HARD_RULE, encoding="utf-8")
        rows = [r for r in allrows if any(r[0].startswith(p) for p in a["prefixes"])]
        db = d / "corpus.db"
        if db.exists():
            db.unlink()
        con = sqlite3.connect(db)
        con.execute("CREATE VIRTUAL TABLE passages USING fts5(ref UNINDEXED, title, body, tokenize='porter unicode61')")
        con.executemany("INSERT INTO passages(ref, title, body) VALUES (?,?,?)", rows)
        con.commit()
        n = con.execute("SELECT count(*) FROM passages").fetchone()[0]
        con.close()
        import re
        voice = re.search(r"\*\*Name:\*\*\s*(.+)", a["persona"]).group(1)
        print(f"{a['dir']:16}{voice[:43]:44}{n:>9}")


if __name__ == "__main__":
    main()
