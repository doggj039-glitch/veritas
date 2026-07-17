# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Legal Dictionary
Neutral, jurisdiction-general legal/research terminology, usage rules, and
deflection/ambiguity detection patterns. Contains no jurisdiction-specific
statutes, constitutional provisions, or case citations.
"""

LEGAL_DICTIONARY = {
    "evidence": {
        "definition": "Information presented to a decision-maker (such as a court or tribunal) to establish or disprove facts at issue in a proceeding. May be documentary, physical, or testimonial.",
        "source": "Standard Legal Terminology",
        "category": "evidence",
        "aliases": ["proof", "exhibits"],
        "misuses": ["evidences (as a verb meaning 'to prove')"],
        "preferred_form": "evidence",
    },
    "hearsay": {
        "definition": "A statement made outside of the current proceeding that is offered to prove the truth of the matter asserted. Generally inadmissible unless an exception applies.",
        "source": "Standard Legal Terminology",
        "category": "evidence",
        "aliases": ["secondhand statement"],
        "misuses": ["rumor (informal, imprecise)"],
        "preferred_form": "hearsay",
    },
    "admissibility": {
        "definition": "Whether evidence is permitted to be considered by a court or tribunal under the applicable rules of evidence.",
        "source": "Standard Legal Terminology",
        "category": "evidence",
        "aliases": ["admissible evidence"],
        "misuses": ["acceptability (imprecise)"],
        "preferred_form": "admissibility",
    },
    "burden_of_proof": {
        "definition": "The obligation to prove a disputed fact or set of facts. In most adversarial proceedings, the party making an allegation bears the burden of proving it.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["onus", "burden"],
        "misuses": ["burden of proof (used loosely to mean 'standard of proof')"],
        "preferred_form": "burden of proof",
    },
    "standard_of_proof": {
        "definition": "The degree of certainty required to satisfy the burden of proof. Common standards include 'beyond a reasonable doubt' (criminal) and 'balance of probabilities' / 'preponderance of the evidence' (civil).",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["evidentiary standard"],
        "misuses": ["burden of proof (distinct concept)"],
        "preferred_form": "standard of proof",
    },
    "reasonable_doubt": {
        "definition": "The standard of proof typically required in criminal proceedings: the trier of fact must be satisfied of guilt to a near-certainty, with no reasonable doubt remaining.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["beyond a reasonable doubt"],
        "misuses": ["beyond reasonable doubt", "beyond any doubt", "beyond all doubt"],
        "preferred_form": "beyond a reasonable doubt",
    },
    "balance_of_probabilities": {
        "definition": "The standard of proof typically required in civil proceedings: a fact is proven if it is more likely than not to be true.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["preponderance of the evidence", "more likely than not"],
        "misuses": ["beyond a reasonable doubt (wrong standard for civil matters)"],
        "preferred_form": "balance of probabilities",
    },
    "arrest": {
        "definition": "The act of taking or keeping a person in custody by legal authority, typically in connection with a criminal charge or suspected offence.",
        "source": "Standard Legal Terminology",
        "category": "criminal_procedure",
        "aliases": ["taken into custody", "placed under arrest"],
        "misuses": ["detainment"],
        "preferred_form": "arrest",
    },
    "detention": {
        "definition": "A restraint on a person's liberty by a state actor, whether physical or psychological, that falls short of a formal arrest. Includes brief investigative stops.",
        "source": "Standard Legal Terminology",
        "category": "criminal_procedure",
        "aliases": ["investigative detention", "being detained", "held for questioning"],
        "misuses": ["arrest (when no formal arrest occurred)", "custody (distinct concept)"],
        "preferred_form": "detention",
    },
    "custody": {
        "definition": "The state of being under the control or guardianship of an authority. Distinct from arrest and detention; commonly used to describe time spent in confinement before or after trial.",
        "source": "Standard Legal Terminology",
        "category": "criminal_procedure",
        "aliases": ["pre-trial custody", "remand", "in custody"],
        "misuses": ["holding", "jail time (informal)"],
        "preferred_form": "custody",
    },
    "bail": {
        "definition": "The conditional release of a person pending trial or further proceedings, typically subject to conditions intended to ensure attendance in court and public safety.",
        "source": "Standard Legal Terminology",
        "category": "criminal_procedure",
        "aliases": ["pre-trial release", "release on conditions"],
        "misuses": ["parole (post-conviction, distinct concept)"],
        "preferred_form": "bail",
    },
    "warrant": {
        "definition": "A document issued by a court or other authorized official authorizing a specific act, such as an arrest, search, or seizure.",
        "source": "Standard Legal Terminology",
        "category": "criminal_procedure",
        "aliases": ["search warrant", "arrest warrant"],
        "misuses": [],
        "preferred_form": "warrant",
    },
    "search_and_seizure": {
        "definition": "The act of a state authority examining a person, place, or thing (search) and taking possession of property (seizure), typically subject to legal limits intended to protect privacy interests.",
        "source": "Standard Legal Terminology",
        "category": "criminal_procedure",
        "aliases": ["search", "seizure"],
        "misuses": [],
        "preferred_form": "search and seizure",
    },
    "right_to_counsel": {
        "definition": "The right of a person who has been arrested or detained to consult with and be represented by legal counsel.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["right to a lawyer", "access to counsel"],
        "misuses": [],
        "preferred_form": "right to counsel",
    },
    "presumption_of_innocence": {
        "definition": "The principle that a person accused of an offence is presumed innocent until proven guilty according to law.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": [],
        "misuses": ["presumed guilty until proven innocent (reversed/incorrect framing)"],
        "preferred_form": "presumption of innocence",
    },
    "due_process": {
        "definition": "The principle that legal proceedings must follow fair, established procedures before a person's rights, liberty, or property can be affected by state action.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["procedural fairness", "fair process"],
        "misuses": [],
        "preferred_form": "due process",
    },
    "natural_justice": {
        "definition": "Common-law procedural fairness principles, generally encompassing the right to be heard and the right to an impartial decision-maker.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["rules of natural justice", "procedural fairness"],
        "misuses": [],
        "preferred_form": "natural justice",
    },
    "bias": {
        "definition": "A lack of impartiality on the part of a decision-maker. A reasonable apprehension of bias may be grounds to challenge a decision even without proof of actual bias.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["apprehension of bias", "reasonable apprehension of bias"],
        "misuses": ["appearance of impropriety (broader, distinct concept)"],
        "preferred_form": "reasonable apprehension of bias",
    },
    "disclosure": {
        "definition": "The obligation of a party (commonly the prosecution or a party to litigation) to provide relevant information and materials to the opposing party in advance of trial or hearing.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["discovery"],
        "misuses": [],
        "preferred_form": "disclosure",
    },
    "abuse_of_process": {
        "definition": "Conduct by a state authority or party that is so unfair or oppressive that it undermines the integrity of the judicial process, potentially warranting a remedy such as a stay of proceedings.",
        "source": "Standard Legal Terminology",
        "category": "procedural",
        "aliases": ["process abuse"],
        "misuses": ["unfair trial (imprecise)"],
        "preferred_form": "abuse of process",
    },
    "remedy": {
        "definition": "A means by which a court or tribunal addresses a proven violation of a right or legal obligation. Common remedies include damages, injunctions, declarations, and exclusion of evidence.",
        "source": "Standard Legal Terminology",
        "category": "remedies",
        "aliases": ["relief"],
        "misuses": ["compensation (narrower than remedy generally)"],
        "preferred_form": "remedy",
    },
    "exclusion_of_evidence": {
        "definition": "A remedy whereby evidence obtained through an unlawful or unfair process is excluded from consideration at trial.",
        "source": "Standard Legal Terminology",
        "category": "remedies",
        "aliases": ["suppression of evidence"],
        "misuses": ["throwing out evidence (informal)"],
        "preferred_form": "exclusion of evidence",
    },
    "stay_of_proceedings": {
        "definition": "A remedy that halts a legal proceeding, often used where continuing the proceeding would be fundamentally unfair or would undermine the integrity of the justice system.",
        "source": "Standard Legal Terminology",
        "category": "remedies",
        "aliases": ["stayed proceedings"],
        "misuses": ["dismissal (distinct concept)"],
        "preferred_form": "stay of proceedings",
    },
    "accused": {
        "definition": "A person formally charged with an offence, entitled to the presumption of innocence and applicable fair-trial protections.",
        "source": "Standard Legal Terminology",
        "category": "parties",
        "aliases": ["defendant (criminal context)"],
        "misuses": ["perpetrator (prejudges guilt)", "offender (implies conviction)"],
        "preferred_form": "accused",
    },
    "prosecution": {
        "definition": "The party that brings and pursues criminal charges against an accused person, bearing the burden of proving guilt.",
        "source": "Standard Legal Terminology",
        "category": "parties",
        "aliases": ["the prosecution", "prosecuting authority"],
        "misuses": ["the government (too general)"],
        "preferred_form": "the prosecution",
    },
    "peace_officer": {
        "definition": "A person legally authorized to exercise police-type powers, such as making arrests and enforcing the law, including police officers and certain other designated officials.",
        "source": "Standard Legal Terminology",
        "category": "parties",
        "aliases": ["police officer", "officer", "law enforcement officer"],
        "misuses": ["cop (informal)"],
        "preferred_form": "peace officer / police officer (context-dependent)",
    },
    "informant": {
        "definition": "A person who provides information to authorities, sometimes on a confidential basis, regarding suspected unlawful activity.",
        "source": "Standard Legal Terminology",
        "category": "parties",
        "aliases": ["confidential informant", "source"],
        "misuses": ["snitch (informal)", "tipster (informal)"],
        "preferred_form": "informant",
    },
    "negligence": {
        "definition": "A failure to exercise the standard of care that a reasonable person would exercise in similar circumstances, resulting in harm.",
        "source": "Standard Legal Terminology",
        "category": "civil",
        "aliases": [],
        "misuses": ["carelessness (informal, imprecise)"],
        "preferred_form": "negligence",
    },
    "damages": {
        "definition": "A monetary remedy awarded to compensate a party for loss or injury caused by another party's wrongful conduct.",
        "source": "Standard Legal Terminology",
        "category": "civil",
        "aliases": ["compensation"],
        "misuses": [],
        "preferred_form": "damages",
    },
    "injunction": {
        "definition": "A court order requiring a party to do or refrain from doing a specific act.",
        "source": "Standard Legal Terminology",
        "category": "civil",
        "aliases": ["restraining order (context-dependent)"],
        "misuses": [],
        "preferred_form": "injunction",
    },
    "jurisdiction": {
        "definition": "The authority of a court or tribunal to hear and decide a particular matter, often defined by geography, subject matter, or the parties involved.",
        "source": "Standard Legal Terminology",
        "category": "general",
        "aliases": [],
        "misuses": [],
        "preferred_form": "jurisdiction",
    },
    "precedent": {
        "definition": "A previously decided case that provides authority or guidance for resolving subsequent cases involving similar facts or legal issues.",
        "source": "Standard Legal Terminology",
        "category": "general",
        "aliases": ["case law", "judicial precedent"],
        "misuses": [],
        "preferred_form": "precedent",
    },
    "statute": {
        "definition": "A written law enacted by a legislative body.",
        "source": "Standard Legal Terminology",
        "category": "general",
        "aliases": ["legislation", "act"],
        "misuses": [],
        "preferred_form": "statute",
    },
}


TERMINOLOGY_RULES = {
    "judgment": {
        "correct": "judgment",
        "incorrect": ["judgement (non-standard in formal legal writing)"],
        "note": "In formal legal writing, 'judgment' (without the middle 'e') is the conventional spelling."
    },
    "court_reference": {
        "correct": "the court / the Court",
        "incorrect": ["The Court (mid-sentence, unless referring to a specific named court or defined term)"],
        "note": "Capitalize 'Court' when referring to a specific court by name or when used as a defined term; lowercase for generic references.",
    },
    "versus": {
        "correct": "v.",
        "incorrect": ["vs.", "vs", "versus (in a case citation)"],
        "note": "In case citations, the convention is 'v.' between party names (e.g., 'Smith v. Jones')."
    },
    "reasonable_doubt_phrase": {
        "correct": "beyond a reasonable doubt",
        "incorrect": ["beyond reasonable doubt", "beyond any doubt", "beyond all doubt", "beyond a shadow of a doubt"],
        "note": "The standard phrase requires the indefinite article 'a': 'beyond a reasonable doubt'."
    },
    "onus_phrase": {
        "correct": "burden of proof",
        "incorrect": ["onus of proof (redundant but commonly seen)"],
        "note": "'Burden of proof' or 'onus' are both acceptable; 'onus of proof' is redundant since onus already means burden."
    },
    "plaintiff_defendant": {
        "correct": "plaintiff / defendant (civil) or prosecution / accused (criminal)",
        "incorrect": ["defendant (in a criminal context, where 'accused' is the more precise term in many jurisdictions)"],
        "note": "Use 'plaintiff' and 'defendant' for civil matters; many jurisdictions prefer 'the prosecution' and 'the accused' for criminal matters."
    },
}


# ============================================================================
# DEFLECTION / AMBIGUITY PATTERNS
# Patterns that indicate deliberate vagueness, equivocation, or deflection
# ============================================================================

DEFLECTION_PATTERNS = {
    "vague_quantifiers": {
        "patterns": [
            r'\b(?:a number of|several|various|some|certain|numerous|multiple|a few|many)\b',
        ],
        "description": "Vague quantifiers that lack specificity. Legal documents should specify exact numbers or ranges where possible.",
        "severity": "medium",
        "suggestion": "Replace with specific numbers or defined ranges."
    },
    "hedging_language": {
        "patterns": [
            r'\b(?:maybe|perhaps|possibly|it seems|it appears|arguably|one might say|it could be argued)\b',
            r'\b(?:somewhat|rather|kind of|sort of|more or less|to some extent|in a way)\b',
        ],
        "description": "Hedging language that weakens assertions. While some hedging is appropriate in legal analysis, excessive hedging can indicate ambiguity or lack of confidence.",
        "severity": "medium",
        "suggestion": "Determine whether the assertion can be stated with greater certainty or requires qualification with a clearly identified standard."
    },
    "undefined_references": {
        "patterns": [
            r'\b(?:the aforementioned|the aforementioned|the above-mentioned|said [a-z]+|such [a-z]+)\b',
            r'\b(?:the following|hereinafter|herein|therein|wherein)\b(?!.*defined)',
        ],
        "description": "References to undefined antecedents. Ensure all references clearly identify their subject. 'Said' and 'such' are often used to avoid specificity.",
        "severity": "high",
        "suggestion": "Replace with specific defined terms or repeat the specific reference for clarity."
    },
    "passive_obfuscation": {
        "patterns": [
            r'\b(?:it was determined|it was decided|it was found|it was concluded|it is noted|it is submitted)\b',
            r'\bwas (?:found|determined|decided|concluded|noted|observed|considered)\b(?! by)',
        ],
        "description": "Passive constructions that omit the decision-maker. Legal documents should identify who made the decision, finding, or conclusion.",
        "severity": "high",
        "suggestion": "Identify the actor: 'The trial judge determined...', 'The court found...', 'The official decided...'"
    },
    "equivocation": {
        "patterns": [
            r'\b(?:on one hand|on the other hand|at the same time|be that as it may|nevertheless|notwithstanding)\b',
            r'\b(?:while it is true|although|albeit|inasmuch as)\b',
        ],
        "description": "Equivocal language that presents contradictory positions without resolution. While nuance is important, unresolved contradictions undermine clarity.",
        "severity": "medium",
        "suggestion": "Acknowledge both positions but clearly state which prevails and why, or articulate the framework for resolution."
    },
    "circular_references": {
        "patterns": [
            r'\b(?:as (?:noted|stated|mentioned|set out|described) (?:above|below|earlier|previously|elsewhere))(?:\s*,\s*(?:see|cf\.|compare)\s*\S+)?\b',
            r'\b(?:see\s+(?:above|below|supra|infra|ibid))\b',
        ],
        "description": "Cross-references without specificity. Ensure references identify the exact location (paragraph number, page, footnote).",
        "severity": "medium",
        "suggestion": "Specify the exact reference: 'as noted at paragraph 14', 'see supra, footnote 7', 'see below, Part III'."
    },
    "weasel_words": {
        "patterns": [
            r'\b(?:clearly|obviously|undoubtedly|certainly|unquestionably|self-evidently|patently|manifestly)\b',
            r'\b(?:it goes without saying|it is axiomatic|as is well known|as everyone knows)\b',
        ],
        "description": "Assertive language without supporting authority. If something is 'clear' or 'obvious,' cite the authority that makes it so. These terms often mask weak analysis.",
        "severity": "high",
        "suggestion": "Either remove the intensifier or replace it with supporting authority, e.g., 'As established in [source]...', 'Under [applicable provision]...'"
    },
    "undefined_terms": {
        "patterns": [
            r'\b(?:appropriate|reasonable|suitable|adequate|proper|sufficient|necessary)\b(?!\s+(?:and\s+)?(?:just|cause|grounds|doubt|notice|time|care|person|steps|precision|opportunity|means))',
        ],
        "description": "Context-dependent legal terms used without definition or contextual anchor. Terms like 'reasonable', 'appropriate', and 'necessary' have specific legal meanings that vary by context.",
        "severity": "high",
        "suggestion": "Define the applicable standard explicitly: 'reasonable' under what test? 'Necessary' according to what rule or exception?"
    },
    "legalese_obfuscation": {
        "patterns": [
            r'\b(?:notwithstanding|provided that|subject to|without prejudice to|save as|except as)\b.*(?:aforementioned|foregoing|hereinafter)\b',
            r'\b(?:ipse dixit|inter alia|mutatis mutandis|pendente lite|sub judice)\b',
        ],
        "description": "Excessive use of Latin maxims or archaic legal phrasing that obscures meaning. Plain language is preferred in modern legal writing.",
        "severity": "low",
        "suggestion": "Replace with plain English equivalents: 'inter alia' → 'among other things'; 'mutatis mutandis' → 'with the necessary changes'."
    },
}
