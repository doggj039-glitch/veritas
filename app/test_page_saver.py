import sys, tempfile, datetime, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_cleaner, local_search

SAMPLE = """<html><head><title>Coinage Clause — Congress.gov</title>
<meta property="og:title" content="The Coinage Clause Explained"></head>
<body>
<nav class="menu"><a href="/a">Home</a><a href="/b">About</a><a href="/c">Login</a></nav>
<header id="masthead">SITE BANNER · SUBSCRIBE NOW</header>
<div class="advert">BUY GOLD TODAY — sponsored</div>
<script>var tracking=1; console.log('spy');</script>
<style>.x{color:red}</style>
<article>
<h1>The Coinage Clause</h1>
<p>The Congress shall have Power To coin Money, regulate the Value thereof, and of foreign Coin.</p>
<p>This power over currency was given to the federal legislature to ensure a uniform standard.</p>
</article>
<footer class="footer">© 2026 · Privacy · Terms · Share on social</footer>
</body></html>"""

print("=== STEP 3: clean_html drops menus/ads/scripts, keeps the article ===")
res = page_cleaner.clean_html(SAMPLE, "https://congress.gov/coinage")
t = res["text"].lower()
assert "coin money" in t, "lost the article body!"
assert "buy gold" not in t and "subscribe" not in t and "tracking" not in t and "console" not in t, "kept junk!"
assert res["title"] in ("The Coinage Clause Explained","Coinage Clause — Congress.gov"), res["title"]
print(f"  ok — title='{res['title']}', kept {res['kept_chars']} chars, junk stripped")

print("=== STEP 4: save_cleaned writes ONE provenance-stamped file ===")
tmp = Path(tempfile.mkdtemp())
p = page_cleaner.save_cleaned(res, "https://congress.gov/coinage", tmp)
head = p.read_text().splitlines()
assert p.name.startswith(datetime.date.today().isoformat()), p.name
assert head[0].startswith("TITLE:") and any(l.startswith("SOURCE URL:") for l in head) and any(l.startswith("DATE SAVED:") for l in head)
print(f"  ok — {p.name}\n       {head[0]}\n       {head[1]}\n       {head[2]}")

print("=== STEP 5: local_search finds it, returns URL + date ===")
out = local_search.search("how is money coined", tmp)
assert out["answered"], out
m = out["matches"][0]
assert m["url"] == "https://congress.gov/coinage", m
print(f"  ok — matched '{m['title']}' score={m['score']} url={m['url']} date={m['date']}")

print("=== STEP 6: no saved match -> plain message, NO api ===")
out2 = local_search.search("zebra migration patterns in antarctica", tmp)
assert out2["answered"] is False and out2["matches"] == [] and "No outside or paid service" in out2["message"]
print("  ok — " + out2["message"][:70] + "...")

print("=== GUARANTEE: local_search.py makes NO network/api call ===")
src = Path("local_search.py").read_text()
# check for real network/api PRIMITIVES (imports + calls), not doc words
bad = re.findall(r"(?m)^\s*(?:import|from)\s+(requests|urllib|http\.|socket|aiohttp)"
                 r"|anthropic|openai|\bapi_key\b|requests\.(?:get|post)|urlopen", src)
assert not bad, f"FOUND network/api primitive: {bad}"
print("  ok — no requests/urllib/http/socket import, no anthropic/openai, no outbound call")
print("\nALL HEADLESS TESTS PASSED (steps 3-6).")
