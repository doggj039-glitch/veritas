"""
veritas_reason.py — the grounded REASONING tier (Path B), folded into local VERITAS.

The offline agents can only QUOTE. This tier lets Claude REASON — but under a strict
contract so it can't fabricate founding-era meaning:

  • founding meaning comes ONLY from VERITAS's own tools (gate / concordance / agents),
    never from the model's memory;
  • modern law/data comes ONLY from web_search, cited and marked as modern/drift;
  • every answer is split into three labeled sections:
        FOUNDING  — record-cited (Johnson 1773 + founding usage + the cases)
        MODERN    — web-cited, marked modern
        ARGUMENT  — labeled inference (the reasoning, clearly flagged as such)

Design constraints honored: stdlib only (raw urllib — no SDK, so VERITAS stays
dependency-free and portable to the .exe / phone build); OFF by default ($0 until a
key is present); cost kept visible and low (prompt caching + a depth dial).

The three founding-evidence tools are INJECTED by the caller (veritas_server builds
them from the gate/concordance/agents), so this module stays decoupled and testable.
"""
import json, urllib.request, urllib.error

API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
WEB_SEARCH_TOOL = "web_search_20260209"   # dynamic-filtering web search (Sonnet 5 supports it)

# Sonnet 5 intro pricing (per 1M tokens) — through 2026-08-31; regular is $3/$15.
_PRICE = {"in": 2.00, "out": 10.00, "cache_write": 2.00 * 1.25, "cache_read": 2.00 * 0.10}
_WEB_SEARCH_USD = 0.01   # ~$10 / 1000 searches

# Depth dial: web-search budget + loop iterations. Evidence lookups are free (local);
# spend is driven by round-trips and web searches, so the dial is the cost control.
DEPTHS = {
    "quick":  {"web": 0, "iters": 3},
    "normal": {"web": 4, "iters": 5},
    "deep":   {"web": 8, "iters": 6},
}

SYSTEM = (
    "You are VERITAS's reasoning tier. You analyze constitutional questions by drift: "
    "what a word meant at the founding vs. what it means now. You may REASON and SYNTHESIZE, "
    "but you may NOT invent facts. Follow this contract exactly:\n"
    "1. FOUNDING-ERA MEANING comes ONLY from the founding tools (founding_meaning, "
    "founding_concordance, ask_founding_voice). NEVER state a founding-era definition, quote, "
    "or case from your own memory. If a tool has nothing, say the record is silent — do not fill it.\n"
    "2. MODERN law, data, and current cases come ONLY from web_search, and must be cited and "
    "marked as modern (i.e. drift away from the founding baseline).\n"
    "3. Structure EVERY answer as three clearly labeled sections:\n"
    "   FOUNDING — the founding-era meaning, each point tagged with its record source "
    "(Johnson 1773 / founding usage / the case).\n"
    "   MODERN — the current meaning/law, each point tagged with its web source, marked modern.\n"
    "   ARGUMENT — your reasoning about the drift between them, clearly labeled as inference "
    "(your analysis, not a sourced fact).\n"
    "Never invent quotes, case names, dates, or numbers. Quote verbatim from the tools. "
    "When founding and modern conflict, name the conflict — that gap IS the drift VERITAS measures."
)


def _tools(depth):
    """Tool schemas sent to the API: 3 custom founding tools + optional web_search."""
    t = [
        {"name": "founding_meaning",
         "description": "The founding-era meaning of a word: verbatim Johnson's 1773 definition "
                        "(controlling), later-dictionary drift, founding-era usage quotes, and the "
                        "Supreme Court cases that construed it. Call this for ANY founding-era meaning "
                        "— never state one from memory.",
         "input_schema": {"type": "object",
                          "properties": {"word": {"type": "string", "description": "the term to define"}},
                          "required": ["word"]}},
        {"name": "founding_concordance",
         "description": "Every occurrence of an English word (or a Strong's-style original) across the "
                        "founding-era corpus, with verbatim text and citations. Use to see how the "
                        "founders actually used a term.",
         "input_schema": {"type": "object",
                          "properties": {"word": {"type": "string"}},
                          "required": ["word"]}},
        {"name": "ask_founding_voice",
         "description": "Put a question to one grounded founding-era voice (federalist, antifederalist, "
                        "blackstone, story, montesquieu, rawle, sedgwick, lieber, convention, ratification). "
                        "Returns only what that voice's sources verbatim say, cited.",
         "input_schema": {"type": "object",
                          "properties": {"voice": {"type": "string"},
                                         "question": {"type": "string"}},
                          "required": ["voice", "question"]}},
    ]
    web = DEPTHS[depth]["web"]
    if web > 0:
        t.append({"type": WEB_SEARCH_TOOL, "name": "web_search", "max_uses": web})
    return t


def _mark_cache(tools, system_blocks):
    """Cache the stable prefix (tools + system) so each round trip re-reads it at ~0.1x."""
    if system_blocks:
        system_blocks[-1]["cache_control"] = {"type": "ephemeral"}
    return tools, system_blocks


def _post(key, body):
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode(),
        headers={"x-api-key": key, "anthropic-version": ANTHROPIC_VERSION,
                 "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def _estimate_cost(usage_totals):
    u = usage_totals
    c = (u["input"] * _PRICE["in"] + u["output"] * _PRICE["out"]
         + u["cache_write"] * _PRICE["cache_write"] + u["cache_read"] * _PRICE["cache_read"]) / 1_000_000
    c += u["web_searches"] * _WEB_SEARCH_USD
    return round(c, 4)


def research(question, key, tool_impls, model, depth="normal"):
    """Run the grounded agentic loop. `tool_impls` = {name: fn(input_dict)->str} for the
    three founding tools (web_search runs server-side). Returns {answer, sections, trace,
    usage, est_cost_usd, model, depth}. Never raises on tool errors — feeds them back."""
    if depth not in DEPTHS:
        depth = "normal"
    max_iters = DEPTHS[depth]["iters"]
    tools, system = _mark_cache(_tools(depth),
                                [{"type": "text", "text": SYSTEM}])
    messages = [{"role": "user", "content": question}]
    totals = {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "web_searches": 0}
    trace = []      # which founding tools/voices/searches were used (grounding provenance)
    final = ""

    for _ in range(max_iters):
        body = {"model": model, "max_tokens": 4096,
                "system": system, "tools": tools, "messages": messages,
                "thinking": {"type": "disabled"}}   # disabled = predictable low cost; evidence does the work
        try:
            resp = _post(key, body)
        except urllib.error.HTTPError as e:
            return {"error": "API error %s: %s" % (e.code, e.read().decode("utf-8", "ignore")[:300])}
        except Exception as e:
            return {"error": "Could not reach the API: %s" % e}

        u = resp.get("usage", {})
        totals["input"] += u.get("input_tokens", 0)
        totals["output"] += u.get("output_tokens", 0)
        totals["cache_write"] += u.get("cache_creation_input_tokens", 0)
        totals["cache_read"] += u.get("cache_read_input_tokens", 0)
        content = resp.get("content", [])
        stop = resp.get("stop_reason")

        # record grounding provenance from this turn
        for b in content:
            if b.get("type") == "tool_use":
                trace.append({"tool": b.get("name"), "input": b.get("input")})
            elif b.get("type") == "server_tool_use" and b.get("name") == "web_search":
                totals["web_searches"] += 1
                trace.append({"tool": "web_search", "input": b.get("input")})

        final = "".join(b.get("text", "") for b in content if b.get("type") == "text") or final

        if stop == "tool_use":
            messages.append({"role": "assistant", "content": content})
            results = []
            for b in content:
                if b.get("type") == "tool_use" and b.get("name") in tool_impls:
                    try:
                        out = tool_impls[b["name"]](b.get("input") or {})
                    except Exception as e:
                        out = "tool error: %s" % e
                    results.append({"type": "tool_result", "tool_use_id": b["id"],
                                    "content": out if isinstance(out, str) else json.dumps(out)})
            if results:
                messages.append({"role": "user", "content": results})
                continue
            break
        if stop == "pause_turn":                 # server web_search paused mid-loop — resume
            messages.append({"role": "assistant", "content": content})
            continue
        if stop == "refusal":
            return {"error": "The model declined this request.", "model": model, "depth": depth}
        break                                    # end_turn

    return {"answer": final, "sections": _split_sections(final), "trace": trace,
            "usage": totals, "est_cost_usd": _estimate_cost(totals),
            "model": model, "depth": depth}


def _split_sections(text):
    """Best-effort split into FOUNDING / MODERN / ARGUMENT for the 3-card UI. If the model
    didn't use the headers, the whole answer falls under 'answer' and the cards degrade."""
    import re
    out = {"founding": "", "modern": "", "argument": ""}
    keys = [("founding", r"FOUNDING"), ("modern", r"MODERN"), ("argument", r"ARGUMENT")]
    idx = []
    for name, pat in keys:
        m = re.search(r"(?im)^\s*#*\s*%s\b.*$" % pat, text)
        if m:
            idx.append((m.start(), m.end(), name))
    idx.sort()
    for i, (s, e, name) in enumerate(idx):
        end = idx[i + 1][0] if i + 1 < len(idx) else len(text)
        out[name] = text[e:end].strip()
    return out
