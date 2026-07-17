# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
AI Integration Module
Connects to OpenAI and Google Gemini APIs for enhanced document analysis
accuracy, term verification, ambiguity resolution, and cross-reference
validation.
"""

import json
import os
import requests
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AIIntegration:
    """
    AI-powered document analysis enhancement.
    Supports OpenAI GPT-4 and Google Gemini for:
    - Legal term verification and disambiguation
    - Document findings accuracy review
    - Deflection/ambiguity detection enhancement
    - Cross-reference suggestions
    - Terminology consistency enforcement
    """

    # System prompts for general legal/research document analysis
    SYSTEM_PROMPTS = {
        "findings_review": (
            "You are an expert legal research analyst. You have broad knowledge of legal "
            "procedure, evidentiary standards, and document analysis. Your role is to:\n"
            "1. Verify the automated document findings for accuracy\n"
            "2. Identify any issues the automated system may have missed\n"
            "3. Validate the confidence/severity levels assigned to potential issues\n"
            "4. Suggest what kind of supporting authority would confirm or refute the finding\n"
            "5. Verify that terminology is used consistently throughout\n\n"
            "Be precise about what each finding does and does not establish. "
            "If the analysis contains errors, correct them and explain why."
        ),
        "term_verification": (
            "You are a legal terminology expert. Your role is to:\n"
            "1. Verify that legal terms are used correctly and consistently\n"
            "2. Identify any terms used inconsistently or ambiguously\n"
            "3. Distinguish between similar but distinct legal concepts\n"
            "4. Flag terminology that mixes conventions from different legal traditions inconsistently\n"
            "5. Ensure terminology aligns with the definitions already on record for the document\n\n"
            "Be precise. Identify the specific misuse and provide the correct usage with reasoning."
        ),
        "deflection_detection": (
            "You are an expert in analytical legal reasoning and rhetoric. Your role is to:\n"
            "1. Identify instances where language is used to deflect, obscure, or avoid addressing legal issues\n"
            "2. Detect ambiguity that could be exploited to create unreasonable doubt\n"
            "3. Flag equivocation, circular reasoning, or question-begging in legal arguments\n"
            "4. Identify weasel words and unsupported assertions\n"
            "5. Detect when legal tests or standards are described imprecisely to avoid their consequences\n"
            "6. Flag when the standard of proof or burden of proof is described incorrectly or imprecisely\n\n"
            "For each instance found, explain WHY it is deflection or ambiguity, what the precise "
            "position should be, and the potential consequence of the ambiguity."
        ),
        "cross_reference_validation": (
            "You are a legal research expert. Your role is to:\n"
            "1. Identify what kind of supporting authority (case law, statute, or rule) would be relevant to validate each finding\n"
            "2. Identify gaps where a finding lacks any supporting authority\n"
            "3. Suggest the type of source most likely to be on point for each issue identified\n"
            "4. Flag findings that may rest on outdated or superseded assumptions\n"
            "5. Suggest search terms that would help locate the most relevant supporting material\n\n"
            "Provide specific, actionable suggestions for what to look up and why it matters."
        ),
        "summary": (
            "You are an expert legal research analyst. Summarize the following document "
            "analysis in clear, precise language. Identify:\n"
            "1. The key issues found\n"
            "2. The strength of each finding\n"
            "3. The most appropriate next steps or remedies to consider\n"
            "4. Any critical gaps in the analysis\n\n"
            "Write for a legal professional. Be concise and authoritative."
        ),
    }

    def __init__(
        self,
        api_key=None,
        model="gpt-4",
        base_url=None,
        provider="openai",
        initial_history=None,
        analysis=None,
        reasoning=None,
        **kwargs
    ):
        self.provider = provider
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if self.provider == "gemini":
            self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
            if GEMINI_AVAILABLE and self.api_key:
                genai.configure(api_key=self.api_key)

        self.model = model
        self.base_url = base_url or "https://api.openai.com/v1"
        chosen_reasoning = reasoning if reasoning is not None else analysis
        if chosen_reasoning is None and "analysis" in kwargs:
            chosen_reasoning = kwargs.get("analysis")
        self.reasoning = self._normalize_reasoning(chosen_reasoning)
        self.session = requests.Session()
        if self.provider == "openai" and self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            })
        self.conversation_history = initial_history if isinstance(initial_history, list) else []
        self.cost_tracker = {"total_tokens": 0, "requests": 0}

    def is_configured(self):
        return bool(self.api_key)

    def _call_api(self, system_prompt, user_message, temperature=0.2, max_tokens=2000):
        """Make an API call to the configured provider."""
        if not self.is_configured():
            provider_name = "Gemini" if self.provider == "gemini" else "OpenAI"
            return {
                "error": f"{provider_name} API key not configured. Set appropriate environment variable or provide key in settings.",
                "content": None,
                "fallback": True,
            }

        if self.provider == "gemini":
            return self._call_gemini(system_prompt, user_message, temperature, max_tokens)
        else:
            return self._call_openai(system_prompt, user_message, temperature, max_tokens)

    def _call_openai(self, system_prompt, user_message, temperature, max_tokens):
        """Make an API call to OpenAI."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        endpoint_order = ["/responses", "/chat/completions"] if self._should_prefer_responses() else ["/chat/completions", "/responses"]
        last_http_error = None

        try:
            for endpoint in endpoint_order:
                payload = self._build_openai_payload(endpoint, messages, temperature, max_tokens)
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json=payload,
                    timeout=60,
                )
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    last_http_error = e
                    if response.status_code == 400:
                        continue
                    raise

                result = response.json()
                usage = result.get("usage", {})
                tokens_used = self._extract_token_usage(usage)
                self.cost_tracker["total_tokens"] += tokens_used
                self.cost_tracker["requests"] += 1
                content = self._extract_openai_text(result)

                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "provider": "openai",
                    "system_prompt_type": "custom",
                    "user_message_length": len(user_message),
                    "response_length": len(content),
                    "tokens_used": tokens_used,
                    "endpoint": endpoint,
                })

                return {"content": content, "error": None, "fallback": False}

            if last_http_error:
                return {
                    "error": f"OpenAI API error: {last_http_error.response.status_code} — {last_http_error.response.text[:200]}",
                    "content": None,
                    "fallback": True
                }
            return {"error": "OpenAI API error: request failed.", "content": None, "fallback": True}

        except requests.exceptions.Timeout:
            return {"error": "OpenAI API request timed out.", "content": None, "fallback": True}
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to OpenAI API.", "content": None, "fallback": True}
        except requests.exceptions.HTTPError as e:
            return {"error": f"OpenAI API error: {e.response.status_code} — {e.response.text[:200]}", "content": None, "fallback": True}
        except Exception as e:
            return {"error": f"Unexpected OpenAI error: {str(e)}", "content": None, "fallback": True}

    def _is_reasoning_model(self):
        model_lower = (self.model or "").lower()
        return model_lower.startswith("o") or model_lower.startswith("gpt-5")

    def _normalize_reasoning(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            v = value.strip().lower()
            if not v:
                return None
            return {"effort": v}
        if isinstance(value, dict):
            normalized = {}
            effort = value.get("effort") or value.get("analysis") or value.get("level")
            if isinstance(effort, str) and effort.strip():
                normalized["effort"] = effort.strip().lower()
            summary = value.get("summary")
            if isinstance(summary, str) and summary.strip():
                normalized["summary"] = summary.strip().lower()
            return normalized or None
        return None

    def _should_prefer_responses(self):
        return self.reasoning is not None or self._is_reasoning_model()

    def _build_openai_payload(self, endpoint, messages, temperature, max_tokens):
        if endpoint == "/responses":
            payload = {
                "model": self.model,
                "input": messages,
                "max_output_tokens": max_tokens,
            }
            if self.reasoning:
                payload["reasoning"] = self.reasoning
            if (not self._is_reasoning_model()) and temperature is not None:
                payload["temperature"] = temperature
            return payload

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        return payload

    def _extract_openai_text(self, result):
        if isinstance(result.get("output_text"), str):
            return result.get("output_text")

        if result.get("choices"):
            return result["choices"][0]["message"].get("content", "")

        parts = []
        for item in result.get("output", []) or []:
            if item.get("type") != "message":
                continue
            for content_item in item.get("content", []) or []:
                if content_item.get("type") == "output_text":
                    parts.append(content_item.get("text", ""))
                elif content_item.get("type") == "text":
                    parts.append(content_item.get("text", ""))
        return "\n".join([p for p in parts if p]).strip()

    def _extract_token_usage(self, usage):
        if not isinstance(usage, dict):
            return 0
        total = usage.get("total_tokens")
        if isinstance(total, int):
            return total
        input_tokens = usage.get("input_tokens", 0) or 0
        output_tokens = usage.get("output_tokens", 0) or 0
        if isinstance(input_tokens, int) and isinstance(output_tokens, int):
            return input_tokens + output_tokens
        return 0

    def _call_gemini(self, system_prompt, user_message, temperature, max_tokens):
        """Make an API call to Google Gemini."""
        if not GEMINI_AVAILABLE:
            return {"error": "google-generativeai library not installed.", "content": None, "fallback": True}

        try:
            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
                system_instruction=system_prompt
            )

            response = model.generate_content(user_message)
            content = response.text

            # Track usage (Gemini usage info is nested)
            self.cost_tracker["requests"] += 1
            # Token tracking for Gemini requires separate calls usually, putting 0 for now
            # or estimating if response provides it.

            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "provider": "gemini",
                "system_prompt_type": "custom",
                "user_message_length": len(user_message),
                "response_length": len(content),
                "tokens_used": 0,
            })

            return {"content": content, "error": None, "fallback": False}

        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}", "content": None, "fallback": True}

    def verify_findings(self, automated_results, document_excerpt):
        """
        Have AI verify and enhance the automated document findings.
        """
        # Prepare a focused excerpt (first 3000 chars to stay within token limits)
        excerpt = document_excerpt[:3000] if len(document_excerpt) > 3000 else document_excerpt

        terminology_summary = [
            {
                "term": issue.get("term"),
                "type": issue.get("type"),
                "count": issue.get("count"),
                "correct_form": issue.get("correct_form"),
            }
            for issue in (automated_results or {}).get("terminology_issues", [])[:10]
        ]
        deflection_summary = [
            {
                "pattern_type": issue.get("pattern_type"),
                "severity": issue.get("severity"),
                "count": issue.get("count"),
            }
            for issue in (automated_results or {}).get("deflection_issues", [])[:10]
        ]

        user_msg = (
            f"DOCUMENT EXCERPT:\n---\n{excerpt}\n---\n\n"
            f"AUTOMATED TERMINOLOGY FINDINGS:\n"
            f"{json.dumps(terminology_summary, indent=2)}\n\n"
            f"AUTOMATED DEFLECTION/AMBIGUITY FINDINGS:\n"
            f"{json.dumps(deflection_summary, indent=2)}\n\n"
            f"Please review this analysis for:\n"
            f"1. Accuracy — Are the findings correctly identified? Are any obvious issues missed?\n"
            f"2. Severity — Do you agree with the severity/confidence levels assigned?\n"
            f"3. Missing issues — What might the pattern-based system have missed?\n"
            f"4. Supporting authority — What kind of source would confirm or refute each finding?\n\n"
            f"Respond in structured JSON format with keys: 'verified_findings', 'missed_issues', "
            f"'severity_adjustments', 'suggested_sources', 'overall_assessment'."
        )

        return self._call_api(self.SYSTEM_PROMPTS["findings_review"], user_msg, temperature=0.15, max_tokens=2500)

    def verify_legal_terms(self, document_text, flagged_terms):
        """
        Have AI verify legal terminology usage and flag misuses.
        """
        excerpt = document_text[:3000] if len(document_text) > 3000 else document_text

        user_msg = (
            f"DOCUMENT EXCERPT:\n---\n{excerpt}\n---\n\n"
            f"FLAGGED TERMINOLOGY ISSUES (from automated scan):\n"
            f"{json.dumps(flagged_terms[:20], indent=2)}\n\n"
            f"Please review:\n"
            f"1. Are the flagged misuses correctly identified?\n"
            f"2. Are there additional terminology errors the automated system missed?\n"
            f"3. Are any terms used ambiguously — where the meaning could shift depending on interpretation?\n"
            f"4. Are there instances where a defined term is used inconsistently?\n\n"
            f"For each issue, provide: the term, the problematic usage, the correct usage, "
            f"and the reasoning supporting the correction."
        )

        return self._call_api(self.SYSTEM_PROMPTS["term_verification"], user_msg, temperature=0.15, max_tokens=2500)

    def detect_deflection(self, document_text, automated_deflections):
        """
        Have AI detect and analyze deflection, ambiguity, and obfuscation.
        """
        excerpt = document_text[:4000] if len(document_text) > 4000 else document_text

        user_msg = (
            f"DOCUMENT EXCERPT:\n---\n{excerpt}\n---\n\n"
            f"AUTOMATED DEFLECTION/AMBIGUITY FLAGS:\n"
            f"{json.dumps(automated_deflections[:15], indent=2)}\n\n"
            f"Please perform a deeper analysis of deflection and ambiguity in this document:\n"
            f"1. Review the automated flags — are they genuine concerns or false positives?\n"
            f"2. Identify any deflection techniques the pattern-matching system would miss:\n"
            f"   - Subtle reframing of the issue\n"
            f"   - Mischaracterization of the applicable standard or test\n"
            f"   - Inaccurate description of the burden of proof\n"
            f"   - Strategic ambiguity about who bears the burden of proof\n"
            f"   - Presenting a higher standard of proof than required\n"
            f"   - Conflating distinct legal concepts (e.g., 'detention' vs 'arrest')\n"
            f"3. Identify any places where the reasoning appears to avoid a necessary conclusion\n"
            f"4. Flag any instances where the document's language could be interpreted in multiple ways\n\n"
            f"For each finding, specify: the text at issue, the deflection/ambiguity type, "
            f"the precise position, the potential consequence, and a recommended clarification."
        )

        return self._call_api(self.SYSTEM_PROMPTS["deflection_detection"], user_msg, temperature=0.2, max_tokens=3000)

    def validate_cross_references(self, automated_results, document_text):
        """
        Have AI suggest and validate cross-reference research directions for the findings.
        """
        excerpt = document_text[:2000] if len(document_text) > 2000 else document_text

        issue_types = sorted(set(
            issue.get("type", "")
            for issue in (automated_results or {}).get("terminology_issues", [])
            if issue.get("type")
        ))

        user_msg = (
            f"DOCUMENT EXCERPT:\n---\n{excerpt}\n---\n\n"
            f"TERMINOLOGY ISSUE TYPES IDENTIFIED: {', '.join(issue_types) if issue_types else 'None'}\n\n"
            f"Please suggest, for each issue type identified, the kind of supporting authority "
            f"(case law, statute, rule, or secondary source) that would be most relevant to "
            f"confirm or refute it. For each suggestion, provide:\n"
            f"1. The type of source to look for\n"
            f"2. What it would need to establish to be relevant\n"
            f"3. Suggested search terms to locate it\n"
            f"4. Any reason to be cautious about an obvious-seeming source (e.g., it may be outdated)\n\n"
            f"Also note any statute or rule references already in the document that should be verified."
        )

        return self._call_api(self.SYSTEM_PROMPTS["cross_reference_validation"], user_msg, temperature=0.15, max_tokens=2500)

    def generate_summary(self, analysis_results):
        """
        Generate an AI-powered executive summary of the complete analysis.
        """
        user_msg = (
            f"COMPLETE ANALYSIS RESULTS:\n"
            f"{json.dumps(analysis_results, indent=2, default=str)[:5000]}\n\n"
            f"Please provide a concise executive summary covering:\n"
            f"1. Key issues found and their strength\n"
            f"2. Recommended next steps or remedies to consider\n"
            f"3. Critical next steps for the legal professional\n"
            f"4. Any significant risks or gaps in the analysis"
        )

        return self._call_api(self.SYSTEM_PROMPTS["summary"], user_msg, temperature=0.3, max_tokens=1500)

    def ask_custom_question(self, question, document_context=""):
        """
        Ask a custom legal research question with optional document context.
        """
        system = (
            "You are an expert legal research analyst. "
            "Answer the following question with precision, citing the type of authority, "
            "standard, or test that would be relevant, as applicable."
        )

        user_msg = question
        if document_context:
            user_msg = f"DOCUMENT CONTEXT:\n---\n{document_context[:2000]}\n---\n\nQUESTION:\n{question}"

        return self._call_api(system, user_msg, temperature=0.3, max_tokens=2000)

    def get_usage_stats(self):
        """Get API usage statistics."""
        return {
            "total_tokens": self.cost_tracker["total_tokens"],
            "total_requests": self.cost_tracker["requests"],
            "estimated_cost_usd": round(self.cost_tracker["total_tokens"] * 0.00003, 4),  # rough GPT-4 estimate
        }
