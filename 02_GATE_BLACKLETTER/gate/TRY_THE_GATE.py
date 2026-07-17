"""
TRY THE GATE
============

This little program lets you watch the Blackletter gate decide words,
all by itself. It does NOT touch VERITAS. Nothing here changes any of
your other work. It only reads your three word collections and shows
you the gate letting good words through and stopping words that are
not sourced yet.

You do not need to understand any of the words in this file. You only
need to start it (the START HERE guide tells you exactly how) and watch.
"""

from veritas_libraries import VeritasLibraries


def show(lib, word):
    """Print, in plain words, what the gate decides about one word."""
    result = lib.resolve(word)
    print(f"  Word:  {word}")

    if result["status"] == "resolved":
        definition = result["controlling"]["definition"]
        print("     ->  LET THROUGH")
        print("     Reason: a founding-era definition is on file, so this word is sourced.")
        print(f"     Definition on file: {definition}")
    else:
        print("     ->  STOPPED   (the gate says: Void for Vagueness)")
        print("     Reason: there is NO founding-era definition on file for this word.")
        print("     The gate will not guess. This word must be sourced before it can be used.")

    # These two only SUPPORT a decision. They never make one on their own.
    has_origin = result["corroboration"]["etymology"] is not None
    has_history = len(result["corroboration"]["historical_context"]) > 0
    extras = []
    if has_origin:
        extras.append("word origin")
    if has_history:
        extras.append("historical use")
    if extras:
        print(f"     Extra support also found (does not decide anything): {', '.join(extras)}")
    print()


def main():
    print("=" * 60)
    print("  THE BLACKLETTER GATE  --  does it work?")
    print("=" * 60)
    print()
    print("  What you are about to see:")
    print("  The gate checks a word against your founding-era sources.")
    print("  If the word is sourced, the gate LETS IT THROUGH.")
    print("  If the word is not sourced, the gate STOPS it -- on purpose.")
    print()

    lib = VeritasLibraries()
    status = lib.library_status()
    print("  Your three word collections loaded:")
    print(f"    Plain definitions (Johnson 1755 / Bailey 1721): {status['definitions_word_count']} words")
    print(f"    Word origins:                                    {status['etymology_word_count']} words")
    print(f"    Historical use and intent:                       {status['historical_context_word_count']} words")
    print()

    print("-" * 60)
    print("  First, watch the gate decide a few words for you:")
    print("-" * 60)
    print()
    for word in ["senate", "liberty", "person", "indictment", "trial"]:
        show(lib, word)

    print("-" * 60)
    print("  Now you try it.")
    print("-" * 60)
    print("  Type any word and press Enter to see the gate decide.")
    print("  Type the word  done  and press Enter to finish.")
    print()

    while True:
        try:
            word = input("  Your word: ").strip()
        except EOFError:
            break
        if not word:
            continue
        if word.lower() == "done":
            print()
            print("  Finished. You just watched the gate work.")
            break
        print()
        show(lib, word)


if __name__ == "__main__":
    main()
