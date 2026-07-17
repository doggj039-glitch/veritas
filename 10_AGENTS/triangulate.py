"""
Triangulation: put ONE question to BOTH agents and show the two grounded,
verbatim perspectives side by side. Neither can bluff; the disagreement between
their sourced words is the evidence of what the founding generation contested.
Fully offline.
"""
import sys
from agent_core import AgentCompartment, team_ask, ROOT

# Lazy: importing this module must NOT open the 114 MB Record — only using it does.
_AGENTS = None
def _agents():
    global _AGENTS
    if _AGENTS is None:
        _AGENTS = [AgentCompartment(ROOT / "10_AGENTS" / n)
                   for n in ("federalist", "antifederalist")]
    return _AGENTS


def triangulate(question):
    bar = "═" * 74
    print(bar + f"\nQUESTION:  {question}\n" + bar)
    ans = team_ask(_agents(), question)          # lex once, both voices share it
    print("\n" + ans["federalist"])
    print("\n" + "·" * 74 + "\n")
    print(ans["antifederalist"])
    print("\n" + bar)


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Can a large republic safely protect liberty?"
    triangulate(q)
    for a in _agents():
        a.close()
