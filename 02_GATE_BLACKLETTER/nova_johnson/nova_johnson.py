"""
NOVA JOHNSON  --  the Founding-Era Definition Agent for VERITAS
==============================================================

NOVA JOHNSON gives you the plain, founding-era meaning of a word.

The important thing about this version: NOVA JOHNSON does NOT think up
definitions. He cannot. He only reads what is actually in your
Definitions Library and repeats it back in a clean, orderly card. If a
word is not in your library, he says so plainly and stops -- he will
not invent one.

That is the whole point. The other tool you tested (Grok) wrote a
confident, official-looking definition for the word "equity" -- a word
that is NOT in your library at all -- and even gave it a fake
confidence score. NOVA JOHNSON, run on that same word, refuses. He is
built so that the failure Grok showed you cannot happen here.

You do not need to understand this file. You only start it (the START
HERE guide tells you how) and type words at it.
"""

from veritas_libraries import VeritasLibraries


def nova_card(lib, word):
    """Build the NOVA JOHNSON answer card for one word, using ONLY what
    the library actually contains. Invents nothing."""
    result = lib.resolve(word)
    clean_word = word.strip().lower()
    lines = []
    lines.append("-" * 58)
    lines.append(f"  NOVA JOHNSON  --  {clean_word}")
    lines.append("-" * 58)

    if result["status"] == "resolved":
        controlling = result["controlling"]

        lines.append("  Source status: FOUND in your loaded sources")
        lines.append("     (Johnson 1755 / Bailey 1721)")
        lines.append("     Honest note: your entries do not yet record WHICH of the")
        lines.append("     two dictionaries each definition came from, so NOVA JOHNSON")
        lines.append("     does not claim one. He will not guess it.")
        lines.append("")
        lines.append(f"  Founding-era definition: {controlling['definition']}")

        dictionary_etymology = controlling.get("etymology_note_from_dictionary", "")
        if dictionary_etymology:
            lines.append("")
            lines.append(f"  Etymology (as written in the dictionary entry): {dictionary_etymology}")

        # Corroboration only. Never establishes or overrides a meaning.
        root = result["corroboration"]["etymology"]
        if root:
            lines.append("")
            lines.append("  Root origin (support only -- never the deciding meaning):")
            lines.append(f"     {root.get('definition', '')}")
            if root.get("path"):
                lines.append(f"     Path: {root['path']}")

        if result["corroboration"]["historical_context"]:
            lines.append("")
            lines.append("  Historical use on file: yes.")
            lines.append("     (That belongs to the intent layer, not to NOVA JOHNSON.")
            lines.append("      He points at it; he does not use it as a definition.)")

        lines.append("")
        lines.append("  Applicable constitutional sense: NOT chosen by this agent.")
        lines.append("     Picking the sense that fits a clause is a judgment left to")
        lines.append("     you or a later agent. NOVA JOHNSON supplies the plain")
        lines.append("     meaning only.")
        lines.append("")
        lines.append("  Modern drift: not assessed here. That is another layer's job.")

    else:
        lines.append("  Source status: NOT FOUND in your loaded sources.")
        lines.append("")
        lines.append("  Founding-era definition: No verified definition found in")
        lines.append("  loaded sources.")
        lines.append("")

        root = result["corroboration"]["etymology"]
        if root:
            lines.append("  A root origin exists (support only -- it does NOT establish")
            lines.append(f"  a definition): {root.get('definition', '')}")
            lines.append("")
        if result["corroboration"]["historical_context"]:
            lines.append("  Historical use is on file, but with no controlling definition")
            lines.append("  this word still cannot be used. It must be sourced first.")
            lines.append("")

        lines.append("  NOVA JOHNSON will not invent a definition. To use this word,")
        lines.append("  add it to the Definitions Library from verified Johnson 1755 or")
        lines.append("  Bailey 1721 text.")

    lines.append("")
    return "\n".join(lines)


def main():
    print("=" * 58)
    print("  NOVA JOHNSON  --  Founding-Era Definition Agent")
    print("=" * 58)
    print()
    print("  I give you the plain founding-era meaning of a word,")
    print("  taken only from your loaded sources. If a word is not")
    print("  there, I say so. I do not invent.")
    print()

    lib = VeritasLibraries()
    status = lib.library_status()
    print(f"  Sources loaded: {status['definitions_word_count']} definitions, "
          f"{status['etymology_word_count']} word origins, "
          f"{status['historical_context_word_count']} historical notes.")
    print()

    print("  First, three examples -- including the word Grok faked:")
    print()
    for word in ["liberty", "shall", "equity"]:
        print(nova_card(lib, word))

    print("-" * 58)
    print("  Notice: 'equity' is refused, because it is not in your")
    print("  library. That is the agent working exactly as intended.")
    print("-" * 58)
    print()
    print("  Now you try. Type any word and press Enter.")
    print("  Type the word  done  to finish.")
    print()

    while True:
        try:
            word = input("  Word for NOVA JOHNSON: ").strip()
        except EOFError:
            break
        if not word:
            continue
        if word.lower() == "done":
            print()
            print("  NOVA JOHNSON rests.")
            break
        print()
        print(nova_card(lib, word))


if __name__ == "__main__":
    main()
