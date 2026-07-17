"""
Debates service — the backend the app's Debates window calls.

Loads the three grounded agent compartments (Federalist / Anti-Federalist /
Ratifying Conventions) and, for each topic, pulls their strongest verbatim,
cited passage. Headless; returns plain dicts/JSON so any front end (the Tkinter
app or the web mock-up) can render it. Also exposes triangulate(question) for
ad-hoc questions. Fully offline, grounded, no API.
"""
import re, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from agent_core import AgentCompartment, ROOT, _topical_terms

VOICES = [
    ("federalist", "Publius", "Federalist"),
    ("antifederalist", "the Anti-Federalist", "Anti-Federalist"),
    ("ratification", "the Ratifying Conventions", "Ratification Debates"),
]

TOPICS = [
    ("union", "The Value of Union", "union states strength advantage"),
    ("faction", "Faction & the Republic", "faction republic majority"),
    ("standing-army", "Standing Armies", "standing army peace military soldiers"),
    ("militia", "The Militia", "militia arms bear"),
    ("taxation", "The Power of Taxation", "taxation taxes revenue impost"),
    ("separation", "Separation of Powers", "separation powers departments"),
    ("representation", "Representation", "representation representatives election"),
    ("judiciary", "The Judiciary", "judiciary courts judges supreme"),
    ("bill-of-rights", "A Bill of Rights", "bill rights liberty declaration"),
]

_agents = None
def agents():
    global _agents
    if _agents is None:
        _agents = {key: AgentCompartment(ROOT / "10_AGENTS" / key) for key, _, _ in VOICES}
    return _agents


def _clean(s):
    s = re.sub(r"\s+", " ", s).strip(" .…-")
    return s


def _quote(agent, terms, k=1):
    hits, _ = agent.search(terms, k=3)
    out = []
    for _rid, _r, ref, title, snip in hits[:k]:
        out.append({"quote": _clean(snip)[:260], "cite": ref + (f" ({title[:40]})" if title else "")})
    return out


def topic_debate(topic_terms, per_voice=1):
    terms = _topical_terms(topic_terms)
    ags = agents()
    return {key: _quote(ags[key], terms, per_voice) for key, _, _ in VOICES}


def build_all():
    data = {"voices": [{"key": k, "voice": v, "label": lbl} for k, v, lbl in VOICES], "topics": []}
    for tid, label, terms in TOPICS:
        data["topics"].append({"id": tid, "label": label,
                               "voices": topic_debate(terms, per_voice=1)})
    return data


def triangulate(question):
    """Ad-hoc: one question to all three voices."""
    terms = _topical_terms(question)
    ags = agents()
    return {"question": question,
            "voices": {key: _quote(ags[key], terms, 1) for key, _, _ in VOICES}}


if __name__ == "__main__":
    data = build_all()
    out = Path(__file__).parent / "debates_data.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    filled = sum(1 for t in data["topics"] for v in t["voices"].values() if v)
    print(f"topics: {len(data['topics'])} | voice-slots filled: {filled}/{len(data['topics'])*3}")
    print(f"-> {out}")
    # show one
    t = data["topics"][2]
    print(f"\nsample — {t['label']}:")
    for k, v, lbl in VOICES:
        q = t["voices"][k]
        print(f"  {lbl}: " + (q[0]["quote"][:80] + " — " + q[0]["cite"] if q else "(none)"))
