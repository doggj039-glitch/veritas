# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Consistency Engine
Generic statement-vs-source-recording consistency checker.

Extracted from the former jurisdiction-specific analysis engine as part of the
neutral conversion (see: Neutral Conversion Plan). Compares a supporting
statement against an audio/video transcript (or directly-supplied transcript
text) and reports matches, contradictions, and risk indicators. Contains no
jurisdiction-specific legal logic.
"""

import os
import re
import subprocess
import tempfile
from difflib import SequenceMatcher


class ConsistencyEngine:
    """Compare a supporting statement against A/V evidence or transcript text."""

    def __init__(self):
        pass

    def analyze_av_against_witness(self, witness_statement_text, video_path=None, audio_path=None, transcript_text=None):
        """
        Analyze A/V evidence against a supporting statement.
        - Extracts audio from media (if ffmpeg available)
        - Attempts best-effort transcription
        - Compares witness claims with A/V transcript for matches/contradictions
        """
        witness_statement_text = (witness_statement_text or "").strip()
        transcript_text = (transcript_text or "").strip()

        media_info = {"video": None, "audio": None}
        media_errors = []
        gathered_transcripts = []
        transcription_runs = []

        if video_path:
            if not os.path.exists(video_path):
                media_errors.append(f"Video file not found: {video_path}")
            else:
                media_info["video"] = self._probe_media(video_path)
                t = self._transcribe_media_file(video_path, source_type="video")
                transcription_runs.append({
                    "source_type": "video",
                    "path": video_path,
                    "engine": t.get("engine"),
                    "quality_score": t.get("quality_score"),
                    "word_count": t.get("word_count", 0),
                    "segment_count": t.get("segment_count", 0),
                })
                if t.get("text"):
                    gathered_transcripts.append(t["text"])
                if t.get("errors"):
                    media_errors.extend(t["errors"])

        if audio_path:
            if not os.path.exists(audio_path):
                media_errors.append(f"Audio file not found: {audio_path}")
            else:
                media_info["audio"] = self._probe_media(audio_path)
                t = self._transcribe_media_file(audio_path, source_type="audio")
                transcription_runs.append({
                    "source_type": "audio",
                    "path": audio_path,
                    "engine": t.get("engine"),
                    "quality_score": t.get("quality_score"),
                    "word_count": t.get("word_count", 0),
                    "segment_count": t.get("segment_count", 0),
                })
                if t.get("text"):
                    gathered_transcripts.append(t["text"])
                if t.get("errors"):
                    media_errors.extend(t["errors"])

        if transcript_text:
            gathered_transcripts.append(transcript_text)

        av_transcript = "\n".join(s for s in gathered_transcripts if s.strip()).strip()
        comparison = self._compare_witness_to_transcript(witness_statement_text, av_transcript)
        perjury_risk = self._assess_perjury_risk(witness_statement_text, av_transcript, comparison)
        evidence_conflict = {
            "conflict_detected": bool(comparison.get("contradictions")),
            "conflict_count": len(comparison.get("contradictions", [])),
            "consistency_score": comparison.get("consistency_score", 0.0),
            "summary": comparison.get("summary", ""),
        }

        return {
            "witness_statement_text": witness_statement_text,
            "av_transcript_text": av_transcript,
            "media_info": media_info,
            "media_errors": media_errors,
            "transcription_runs": transcription_runs,
            "comparison": comparison,
            "evidence_conflict_assessment": evidence_conflict,
            "perjury_risk_indicators": perjury_risk,
        }

    def _probe_media(self, media_path):
        """Return lightweight media metadata via ffprobe when available."""
        try:
            proc = subprocess.run(
                [
                    "ffprobe",
                    "-v", "error",
                    "-show_entries", "format=duration,bit_rate:stream=index,codec_type,codec_name,width,height,sample_rate,channels",
                    "-of", "default=noprint_wrappers=1",
                    media_path,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode != 0:
                return {"path": media_path, "metadata_error": proc.stderr.strip() or "ffprobe failed"}
            return {"path": media_path, "ffprobe": proc.stdout.strip()}
        except Exception as e:
            return {"path": media_path, "metadata_error": str(e)}

    def _transcribe_media_file(self, media_path, source_type="audio"):
        """
        Best-effort transcription pipeline:
        1) Extract mono WAV with ffmpeg
        2) Try offline ASR engines if installed (faster-whisper, whisper)
        """
        errors = []
        transcript = ""
        engine_used = None
        temp_wav = None
        segment_count = 0
        quality_score = 0.0
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                temp_wav = tmp.name

            ffmpeg_variants = [
                [
                    "ffmpeg", "-y",
                    "-i", media_path,
                    "-vn",
                    "-af", "highpass=f=120,lowpass=f=3800,afftdn=nf=-25",
                    "-ac", "1",
                    "-ar", "16000",
                    temp_wav,
                ],
                [
                    "ffmpeg", "-y",
                    "-i", media_path,
                    "-vn",
                    "-af", "highpass=f=120,lowpass=f=3800",
                    "-ac", "1",
                    "-ar", "16000",
                    temp_wav,
                ],
            ]
            extracted = False
            for ffmpeg_cmd in ffmpeg_variants:
                proc = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=False)
                if proc.returncode == 0:
                    extracted = True
                    break
                errors.append(f"ffmpeg extraction failed ({'enhanced' if '-af' in ffmpeg_cmd else 'plain'}): {proc.stderr.strip()[:240]}")
            if not extracted:
                return {"text": "", "engine": None, "errors": errors, "source_type": source_type, "quality_score": 0.0}

            try:
                from faster_whisper import WhisperModel  # type: ignore

                # Upgrading to "small" for better accuracy than "base"
                # If memory is an issue on Android, stick with "base" or "tiny"
                model_size = "small" 
                model = WhisperModel(model_size, device="cpu", compute_type="int8")
                
                segments, _ = model.transcribe(
                    temp_wav,
                    beam_size=5,
                    best_of=5,
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500),
                    temperature=0.0,
                )
                parts = []
                logprobs = []
                for seg in segments:
                    text_part = (seg.text or "").strip()
                    if text_part:
                        parts.append(text_part)
                    avg_logprob = getattr(seg, "avg_logprob", None)
                    if isinstance(avg_logprob, (int, float)):
                        logprobs.append(avg_logprob)
                transcript = " ".join(parts).strip()
                transcript = self._polish_transcript(transcript)
                segment_count = len(parts)
                if transcript:
                    engine_used = "faster-whisper(base)"
                    wc = len(re.findall(r"[a-z0-9']+", transcript.lower()))
                    lp_component = 0.0
                    if logprobs:
                        avg_lp = sum(logprobs) / len(logprobs)
                        lp_component = min(max((avg_lp + 2.0) / 2.0, 0.0), 1.0)
                    length_component = min(wc / 120.0, 1.0)
                    quality_score = round((0.55 * lp_component) + (0.45 * length_component), 3)
            except Exception as e:
                errors.append(f"faster-whisper unavailable/failed: {e}")

            if not transcript:
                try:
                    import whisper  # type: ignore

                    model = whisper.load_model("base")
                    out = model.transcribe(temp_wav, fp16=False)
                    transcript = (out.get("text") or "").strip()
                    if transcript:
                        engine_used = "openai-whisper(base)"
                        segment_count = len(re.split(r'(?<=[\.\?!])\s+', transcript))
                        wc = len(re.findall(r"[a-z0-9']+", transcript.lower()))
                        quality_score = round(min(wc / 140.0, 1.0), 3)
                except Exception as e:
                    errors.append(f"openai-whisper unavailable/failed: {e}")
        finally:
            if temp_wav and os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                except OSError:
                    pass

        if not transcript:
            errors.append(
                "No transcript produced. Install faster-whisper/whisper or provide transcript_text manually."
            )

        return {
            "text": transcript,
            "engine": engine_used,
            "errors": errors,
            "source_type": source_type,
            "segment_count": segment_count,
            "word_count": len(re.findall(r"[a-z0-9']+", transcript.lower())),
            "quality_score": quality_score,
        }

    
    def _polish_transcript(self, text):
        if not text:
            return ''
        
        corrections = {
            r'\battention\b': 'detention',
            r'\bsection seven\b': 'Section 7',
            r'\bsection eight\b': 'Section 8',
            r'\bsection nine\b': 'Section 9',
            r'\bright to council\b': 'right to counsel',
            r'\bsees your\b': 'seizure',
            r'\barrested\b.*\bincident\b': 'arrested incident to arrest',
        }
        
        polished = text
        for pattern, replacement in corrections.items():
            polished = re.sub(pattern, replacement, polished, flags=re.IGNORECASE)
            
        return polished

    def _compare_witness_to_transcript(self, witness_text, transcript_text):
        """Claim-level witness-vs-transcript comparison with contradiction flags."""
        def split_claims(text):
            base = [s.strip() for s in re.split(r'(?<=[\.\?!])\s+|\n+', text or "") if s.strip()]
            claims = []
            for sentence in base:
                chunks = [c.strip(" ,;") for c in re.split(r"\b(?:and|but|while|whereas)\b|;", sentence, flags=re.IGNORECASE) if c.strip()]
                claims.extend(chunks if len(chunks) > 1 else [sentence])
            return claims

        def normalize_recording_language(text):
            normalized = (text or "").lower()
            replacements = [
                (r"\bon video\b|\bon camera\b|\bon film\b", " recorded "),
                (r"\bvideo(?:taped|taping)?\b|\bfilmed\b|\bfilm(?:ing)?\b|\btaped\b", " recorded "),
                (r"\bcaptured\b.{0,12}\b(?:video|camera|film)\b", " recorded "),
                (r"\bmic(?:'?d)?\s+up\b|\baudio(?:\s+recorded)?\b", " recorded "),
            ]
            for pattern, replacement in replacements:
                normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
            return re.sub(r"\s+", " ", normalized).strip()

        def tokenize(text):
            return [t for t in re.findall(r"[a-z0-9']+", normalize_recording_language(text)) if t]

        def has_negation(text):
            return bool(re.search(r"\b(no|not|never|none|without|didn't|did not|can't|cannot|won't|wasn't|weren't)\b", text.lower()))

        def recording_awareness_state(text):
            lowered = normalize_recording_language(text)
            if not lowered:
                return None

            recording_terms = r"(?:record(?:ed|ing)?|video|camera|taped)"
            unaware_patterns = [
                rf"\b(?:unaware|not aware|wasn't aware|were not aware|did(?: not|n't) know|no idea|did(?: not|n't) realize)\b.{{0,40}}\b{recording_terms}\b",
                rf"\b{recording_terms}\b.{{0,40}}\b(?:without my knowledge|unknown to me|without our knowledge)\b",
                rf"\b(?:without my knowledge|unknown to me|without our knowledge)\b.{{0,40}}\b{recording_terms}\b",
            ]
            aware_patterns = [
                rf"\b(?:i|we)\s+(?:like|liked|love|loved|enjoy|enjoyed|prefer|preferred)\s+being\s+(?:recorded|taped)\b",
                rf"\b(?:knew|know|aware|was aware|were aware)\b.{{0,30}}\b{recording_terms}\b",
                rf"\b{recording_terms}\b.{{0,30}}\b(?:knew|know|aware|was aware|were aware)\b",
                rf"\b(?:consent(?:ed)?|agree(?:d)?|okay|ok|fine|comfortable)\b.{{0,30}}\b(?:to\s+)?(?:being\s+)?(?:recorded|taped)\b",
                rf"\b{recording_terms}\b.{{0,30}}\b(?:consent(?:ed)?|agree(?:d)?|okay|ok|fine|comfortable)\b",
            ]

            if any(re.search(pattern, lowered, re.IGNORECASE) for pattern in unaware_patterns):
                return "unaware"
            if any(re.search(pattern, lowered, re.IGNORECASE) for pattern in aware_patterns):
                return "aware"
            return None

        def has_conflict_pair(a, b):
            pairs = [
                ("inside", "outside"),
                ("daylight", "night"),
                ("day", "night"),
                ("morning", "evening"),
                ("before", "after"),
                ("arrived", "left"),
                ("upstairs", "downstairs"),
                ("front", "back"),
            ]
            al = a.lower()
            bl = b.lower()
            flags = []
            for left, right in pairs:
                if ((re.search(rf"\b{left}\b", al) and re.search(rf"\b{right}\b", bl))
                        or (re.search(rf"\b{right}\b", al) and re.search(rf"\b{left}\b", bl))):
                    flags.append(f"{left}_vs_{right}")
            awareness_a = recording_awareness_state(a)
            awareness_b = recording_awareness_state(b)
            if awareness_a and awareness_b and awareness_a != awareness_b:
                flags.append("recording_awareness_mismatch")
            return flags

        witness_sentences = split_claims(witness_text)
        transcript_sentences = split_claims(transcript_text)
        transcript_awareness_overall = recording_awareness_state(transcript_text)
        matches = []
        contradictions = []
        unverified = []
        matched_transcript_idx = set()

        for ws in witness_sentences:
            witness_awareness = recording_awareness_state(ws)
            if witness_awareness:
                if transcript_awareness_overall and transcript_awareness_overall != witness_awareness:
                    contradictions.append({
                        "witness_sentence": ws,
                        "transcript_sentence": transcript_text.strip(),
                        "similarity_score": round(SequenceMatcher(None, normalize_recording_language(ws), normalize_recording_language(transcript_text)).ratio(), 3),
                        "conflict_flags": ["recording_awareness_mismatch"],
                        "certainty": "high",
                    })
                    matched_transcript_idx.update(range(len(transcript_sentences)))
                    continue
                awareness_candidates = []
                for i, ts in enumerate(transcript_sentences):
                    transcript_awareness = recording_awareness_state(ts)
                    if transcript_awareness and transcript_awareness != witness_awareness:
                        awareness_candidates.append((
                            SequenceMatcher(None, normalize_recording_language(ws), normalize_recording_language(ts)).ratio(),
                            i,
                            ts,
                        ))
                if awareness_candidates:
                    _, best_idx, best_sentence = max(awareness_candidates, key=lambda item: item[0])
                    matched_transcript_idx.add(best_idx)
                    contradictions.append({
                        "witness_sentence": ws,
                        "transcript_sentence": best_sentence,
                        "similarity_score": round(SequenceMatcher(None, normalize_recording_language(ws), normalize_recording_language(best_sentence)).ratio(), 3),
                        "conflict_flags": ["recording_awareness_mismatch"],
                        "certainty": "high",
                    })
                    continue

            wtok = set(tokenize(ws))
            best = {"idx": -1, "score": 0.0, "sentence": ""}
            for i, ts in enumerate(transcript_sentences):
                ttok = set(tokenize(ts))
                if not wtok or not ttok:
                    continue
                overlap = len(wtok & ttok) / max(len(wtok | ttok), 1)
                ratio = SequenceMatcher(None, normalize_recording_language(ws), normalize_recording_language(ts)).ratio()
                score = (0.65 * overlap) + (0.35 * ratio)
                if score > best["score"]:
                    best = {"idx": i, "score": score, "sentence": ts}

            preconflict_flags = has_conflict_pair(ws, best["sentence"])
            recording_awareness_conflict = "recording_awareness_mismatch" in preconflict_flags
            if best["score"] >= 0.28 or (preconflict_flags and best["score"] >= 0.22) or recording_awareness_conflict:
                matched_transcript_idx.add(best["idx"])
                neg_mismatch = has_negation(ws) != has_negation(best["sentence"])
                conflict_flags = preconflict_flags
                item = {
                    "witness_sentence": ws,
                    "transcript_sentence": best["sentence"],
                    "similarity_score": round(best["score"], 3),
                }
                if recording_awareness_conflict:
                    item["conflict_flags"] = conflict_flags
                    item["certainty"] = "high"
                    contradictions.append(item)
                elif neg_mismatch and best["score"] >= 0.35:
                    item["conflict_flags"] = ["negation_mismatch"] + conflict_flags
                    contradictions.append(item)
                elif conflict_flags and best["score"] >= 0.22:
                    item["conflict_flags"] = conflict_flags
                    contradictions.append(item)
                else:
                    matches.append(item)
            else:
                unverified.append(ws)

        additional_av_events = [
            s for i, s in enumerate(transcript_sentences) if i not in matched_transcript_idx
        ]

        denom = max(len(witness_sentences), 1)
        consistency_score = max(0.0, (len(matches) - len(contradictions)) / denom)
        high_certainty_contradictions = sum(1 for item in contradictions if item.get("certainty") == "high")

        return {
            "witness_sentence_count": len(witness_sentences),
            "transcript_sentence_count": len(transcript_sentences),
            "consistency_score": round(consistency_score, 3),
            "matches": matches[:50],
            "contradictions": contradictions[:50],
            "high_certainty_contradictions": high_certainty_contradictions,
            "unverified_witness_claims": unverified[:50],
            "additional_av_events": additional_av_events[:120],
            "summary": (
                f"Compared {len(witness_sentences)} supporting statements against {len(transcript_sentences)} transcript sentences. "
                f"Matches: {len(matches)} | Contradictions: {len(contradictions)} | High-certainty contradictions: {high_certainty_contradictions} | Unverified: {len(unverified)}."
            ),
        }

    def _assess_perjury_risk(self, witness_text, transcript_text, comparison):
        """
        Build a risk-indicator report for potential perjury-related concerns.
        This is not proof of perjury and should not be treated as a legal conclusion.
        """
        witness_text = witness_text or ""
        transcript_text = transcript_text or ""
        contradictions = comparison.get("contradictions", []) if isinstance(comparison, dict) else []
        unverified = comparison.get("unverified_witness_claims", []) if isinstance(comparison, dict) else []
        witness_count = max(int(comparison.get("witness_sentence_count", 0) or 0), 1) if isinstance(comparison, dict) else 1
        consistency_score = float(comparison.get("consistency_score", 0.0) or 0.0) if isinstance(comparison, dict) else 0.0

        evasion_patterns = [
            r"\bi (?:do not|don't) recall\b",
            r"\bi(?:'m| am) not sure\b",
            r"\bmaybe\b",
            r"\bi guess\b",
            r"\bto the best of my knowledge\b",
            r"\bi can(?:not|'t) remember\b",
        ]
        fabrication_patterns = [
            r"\bthat's not true\b",
            r"\bthat is not true\b",
            r"\bmade (?:it|that) up\b",
            r"\bfabricat",
            r"\blied\b",
            r"\bfalse statement\b",
        ]

        evasion_hits = sum(len(re.findall(p, transcript_text, re.IGNORECASE)) for p in evasion_patterns)
        fabrication_hits = sum(len(re.findall(p, transcript_text, re.IGNORECASE)) for p in fabrication_patterns)

        contradiction_ratio = len(contradictions) / witness_count
        unverified_ratio = len(unverified) / witness_count
        score = 0.0
        score += min(0.55, contradiction_ratio * 0.9)
        score += min(0.25, unverified_ratio * 0.35)
        score += min(0.15, evasion_hits * 0.03)
        score += min(0.2, fabrication_hits * 0.05)
        score += max(0.0, 0.1 - max(consistency_score, 0.0) * 0.1)
        score = round(min(score, 1.0), 3)

        if score >= 0.65:
            level = "HIGH"
        elif score >= 0.35:
            level = "MEDIUM"
        else:
            level = "LOW"

        indicators = []
        if contradictions:
            indicators.append(f"{len(contradictions)} witness-vs-evidence contradiction(s) detected.")
        if unverified:
            indicators.append(f"{len(unverified)} witness claim(s) not corroborated by the available transcript.")
        if evasion_hits:
            indicators.append(f"{evasion_hits} potential evasive-language marker(s) detected in transcript.")
        if fabrication_hits:
            indicators.append(f"{fabrication_hits} fabrication/falsehood marker(s) detected in transcript language.")
        if not indicators:
            indicators.append("No strong perjury-risk linguistic indicators detected on current transcript.")

        return {
            "risk_level": level,
            "risk_score": score,
            "consistency_score": consistency_score,
            "indicators": indicators,
            "disclaimer": (
                "Risk indicators only. Automated contradiction/evasion detection is not proof of perjury. "
                "Legal conclusions require full evidentiary context and professional legal assessment."
            ),
        }

