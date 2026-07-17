# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Historical Context Library
Grounding rules of INTENT -- drafting intent, original public meaning, and early
legal synthesis, drawn from Farrand's Records, Madison's Notes, the Federalist
and Anti-Federalist Papers, Elliot's Debates, Story's Commentaries, Rawle's View,
Kent's Commentaries, Bouvier's Law Dictionary, Blackstone's Commentaries, and the
Annals of Congress.

This is deliberately separate from literal_dictionary.py and
constitutional_definitions_supplement.py. Those answer: what did a word plainly
mean? This answers: what did people actually do with the word -- how was it
argued about, drafted, or applied?
"""

HISTORICAL_SOURCES = [
    {
        "title": "The Federalist Papers",
        "short_name": "The Federalist",
        "author": "Alexander Hamilton, James Madison, and John Jay (as 'Publius')",
        "year": "1787-1788 (this edition: New American Library/Mentor Books, 1961, ed. Clinton Rossiter)",
        "role": "Original public meaning -- the most systematic, widely-circulated PUBLISHED defense of the Constitution made directly to the voting public during ratification. Sits alongside Elliot's Debates in the pipeline: Elliot's captures spoken convention arguments, the Federalist captures the polished, published public case. Many originalist scholars treat it as at least as authoritative as the state conventions themselves, since it was the most widely read explanation of the document.",
        "citability": "HIGH -- true page-level citation possible via leaf/pdf_page/printed_page fields, same tier as Johnson's Dictionary",
    },
    {
        "title": "The Antifederalist Papers",
        "short_name": "The Anti-Federalist",
        "author": "Patrick Henry, Richard Henry Lee, 'Brutus', 'Centinel', 'Federal Farmer', and other writers (compiled edition)",
        "year": "1787-1788 (essays); compiled edition",
        "role": "Original public meaning -- the essential counterweight to the Federalist. Captures the opposition case made directly to the ratifying public: fears of consolidated national power, absence of a bill of rights, danger to state sovereignty, distrust of a standing army, and concern over an unchecked federal judiciary. Many of these specific objections directly produced the Bill of Rights -- 'why does this clause exist' often can't be fully answered without seeing what the Anti-Federalists were afraid of.",
        "citability": "HIGH -- page-level citation possible via leaf/pdf_page fields, same tier as Johnson's Dictionary and the Federalist",
    },
    {
        "title": "The Records of the Federal Convention of 1787",
        "short_name": "Farrand's Records",
        "author": "Compiled by Max Farrand",
        "year": "1911 compilation of 1787 primary sources",
        "role": "Drafting intent -- shows what the framers explicitly discussed or disputed while writing the text",
        "citability": "Low -- offset/context only, flag as page-unconfirmed",
    },
    {
        "title": "Notes of Debates in the Federal Convention of 1787",
        "short_name": "Madison's Notes",
        "author": "James Madison",
        "year": "1787",
        "role": "Drafting intent -- floor-level record of Convention debate",
        "citability": "Low -- offset/context only, and editorial vs. primary-source content must be distinguished manually",
    },
    {
        "title": "The Debates in the Several State Conventions on the Adoption of the Federal Constitution",
        "short_name": "Elliot's Debates",
        "author": "Compiled by Jonathan Elliot",
        "year": "1830s compilation of 1787-1790 primary sources",
        "role": "Original public/ratification meaning -- how the document was explained and understood by the people who voted it into force",
        "citability": "Low -- offset/context only",
    },
    {
        "title": "Commentaries on the Constitution of the United States",
        "short_name": "Story's Commentaries",
        "author": "Joseph Story",
        "year": "1833",
        "role": "First-generation legal synthesis -- clause-by-clause treatise citing drafting/ratification history, written within a generation of the founding",
        "citability": "Low -- offset/context only",
    },
    {
        "title": "A View of the Constitution of the United States of America",
        "short_name": "Rawle's View",
        "author": "William Rawle",
        "year": "1825 (2nd edition)",
        "role": "First-generation legal synthesis, alongside Story's -- an early treatise with access to living memory of the founding",
        "citability": "Low -- offset/context only",
    },
    {
        "title": "Commentaries on American Law",
        "short_name": "Kent's Commentaries",
        "author": "James Kent",
        "year": "1826-1830 (multi-volume)",
        "role": "General legal-technical meaning -- for words that are legal terms of art rather than ordinary words, gives the operative definition as applied in American courts of the era, independent of the Constitution itself",
        "citability": "Low -- offset/context only",
    },
    {
        "title": "Commentaries on the Laws of England",
        "short_name": "Blackstone's Commentaries",
        "author": "William Blackstone",
        "year": "1765-1769 (4 books)",
        "role": "Bonus/supplementary source, not originally specified in the core methodology -- pre-founding English common-law background",
        "citability": "Low -- offset/context only, per-chapter files",
    },
    {
        "title": "Annals of Congress, 1st-18th Congress (1789-1824)",
        "short_name": "Annals of Congress",
        "author": "U.S. Congress (compiled record)",
        "year": "1789-1824 (proceedings); compiled later",
        "role": "Bonus/supplementary source -- post-ratification usage tracking; shows how constitutional language was actually applied in the first decades of federal legislation",
        "citability": "Low -- offset/context only",
    },
    {
        "title": "Bouvier's Law Dictionary and Concise Encyclopedia",
        "short_name": "Bouvier's Law Dictionary",
        "author": "John Bouvier (Rawle's Revision)",
        "year": "1839 (this edition: Rawle's Revision, early 20th-c. reprint)",
        "role": "General legal-technical meaning -- a dedicated period LAW dictionary sitting alongside Kent's Commentaries as a second cross-check specifically for legal terms of art. Plays the same role for legal vocabulary that Bailey's plays for ordinary vocabulary: an independent second opinion, not just a supplement to Johnson's/Kent's. Confirmed rich, high-quality entries for core constitutional-law terms: Attainder, Ex Post Facto Law, Constitution, Civil Rights, Criminal Law, Courts of England, and more.",
        "citability": "HIGH -- true page-level citation possible via leaf/pdf_page/printed_page fields, same tier as Johnson's, the Federalist, and the Anti-Federalist",
    },
]

RECOMMENDED_SEARCH_ORDER = [
    "1. Farrand's Records / Madison's Notes (drafting intent -- what was said while writing the text)",
    "2. The Federalist / The Anti-Federalist Papers (original public meaning -- the published case made to voters on both sides)",
    "3. Elliot's Debates (original public meaning -- the spoken case made at the state ratifying conventions)",
    "4. Story's Commentaries / Rawle's View (early 19th-c. legal synthesis, written within a generation of the founding)",
    "5. Kent's Commentaries / Bouvier's Law Dictionary (general legal-technical meaning -- terms of art as applied in American courts)",
    "6. Blackstone's Commentaries / Annals of Congress (supplementary -- English common-law background and post-ratification usage tracking)",
]

HISTORICAL_CONTEXT_LIBRARY = {
    "attainder": {
        "word": "attainder",
        "source": "Farrand's Records",
        "usage_note": "Draft language limits attainder of treason's consequences to the life of the person attainted, with no corruption of blood or forfeiture beyond that -- direct source of the Constitution's Corruption of Blood clause.",
    },
    "indictment": {
        "word": "indictment",
        "source": "Kent's Commentaries",
        "usage_note": "Used in a live 1818-era prosecution (United States v. Gooding, cited by Kent) -- confirms the word's real operative use in federal criminal procedure shortly after ratification, not just theoretical usage.",
    },
    "impartial": {
        "word": "impartial",
        "source": "Story's Commentaries / Kent's Commentaries",
        "usage_note": "Paired directly with jury trial and freedom of the press as core guardians of civil liberty (Kent); used to describe the required character of the jury deciding fact and intent in a case.",
    },
    "compulsory": {
        "word": "compulsory",
        "source": "Elliot's Debates",
        "usage_note": "A ratification-era delegate defends compulsory laws as compatible with liberty ('the people ought to be obliged to attend to their interest') while still worrying about giving Congress abusable power -- shows the term used to describe legally-obligatory measures, not merely coercive ones in a negative sense.",
    },
    "speedy": {
        "word": "speedy",
        "source": "Story's Commentaries",
        "usage_note": "Used in direct quotation of the Sixth Amendment text itself: 'speedy and public trial, by an impartial jury' -- meaning is self-evident from context: prompt, without unreasonable delay.",
    },
    "unusual": {
        "word": "unusual",
        "source": "Story's Commentaries",
        "usage_note": "Used in ordinary prose sense ('not an unusual expedient of taxation') meaning simply uncommon or out of the ordinary course -- no special legal-technical spin.",
    },
    "seizure": {
        "word": "seizure",
        "source": "Kent's Commentaries",
        "usage_note": "Used in a maritime/wartime context: an act 'hostile in the mere execution,' whose ultimate legal character (mere civil embargo vs. act of war) is determined retroactively by what happens afterward.",
    },
    "presentment": {
        "word": "presentment",
        "source": "Story's Commentaries",
        "usage_note": "Quoted directly from the Fifth Amendment text, distinguished from 'indictment' as a separate way a grand jury can bring forward a capital or infamous crime -- presentment appears to be the grand jury's own initiation of charges, as opposed to indictment following a prosecutor's bill.",
    },
    "life": {
        "word": "life",
        "source": "Story's Commentaries",
        "usage_note": "Used plainly in 'during the life of the person attainted' -- ordinary biological/duration sense, no special legal twist.",
    },
    "peace": {
        "word": "peace",
        "source": "Farrand's Records",
        "usage_note": "Paired directly against 'war' as a power the government exercises ('deciding on peace & war') -- meaning: the state's condition of not being at war, a status the political branches actively hold power over.",
    },
    "distinct": {
        "word": "distinct",
        "source": "Madison's Notes",
        "usage_note": "James Wilson's own argument at the Convention: legislative, executive, and judiciary 'ought to be distinct & independent' -- the conceptual root of separation of powers; 'distinct' = separate, not commingled.",
    },
    "nation": {
        "word": "nation",
        "source": "Elliot's Debates",
        "usage_note": "Used as the whole political community acting as one body ('a great and happy nation' vs. 'a weak and despised one' if the Constitution failed) -- matches the modern sense: the collective sovereign people as a single entity.",
    },
    "section": {
        "word": "section",
        "source": "Story's Commentaries",
        "usage_note": "Used exactly as structural notation ('Section 4' following Article text) -- confirms purely organizational meaning, a numbered subdivision of an Article.",
    },
    "general": {
        "word": "general",
        "source": "Farrand's Records (editorial introduction)",
        "usage_note": "Used as 'in general,' an adverbial qualifier meaning broadly/as a whole/not specifically -- ordinary usage, no legal weight. (Note: this specific hit was from the modern editor's introduction, not Convention floor speech.)",
    },
    "several": {
        "word": "several",
        "source": "Elliot's Debates",
        "usage_note": "'The introduction of tyranny into several nations' -- 18th-century 'several' means separate, distinct, individual nations (each its own), NOT the modern loose sense of 'a few.' Real semantic drift point: 'several States' elsewhere in the Constitution should read as 'the individual, distinct States,' not 'some undefined small number.'",
    },
    "subject": {
        "word": "subject",
        "source": "Kent's Commentaries",
        "usage_note": "'write on the subject' -- ordinary sense, meaning topic or matter under discussion. No special legal-technical use in this instance.",
    },
    "declaration": {
        "word": "declaration",
        "source": "Madison's Notes (editorial introduction)",
        "usage_note": "Editorial framing draws the line from the Convention back to Jefferson's Declaration of Independence phrase 'to institute new Government' -- not primary Convention-floor usage, flagged as editorial commentary.",
    },
    "respective": {
        "word": "respective",
        "source": "Farrand's Records",
        "usage_note": "From actual draft resolution text: laws/treaties are supreme 'as far as those acts... relate to the said States' and binding 'any thing in the respective laws of the individual States to the contrary notwithstanding' -- confirms 'respective' = belonging individually to each one separately.",
    },
    "service": {
        "word": "service",
        "source": "Elliot's Debates",
        "usage_note": "Patrick Henry argues against the militia clause, asking what use ('service') the militia would even be to the states if Congress controls it and refuses to arm it -- 'service' means practical usefulness/function.",
    },
    "think": {
        "word": "think",
        "source": "Madison's Notes",
        "usage_note": "Used in the ordinary sense of holding an opinion or belief, in the context of a discussion about monarchy risk if public offices become 'places of profit' rather than honor. Speaker not confirmed on this pass.",
    },
    "labour": {
        "word": "labour",
        "source": "Madison's Notes",
        "usage_note": "'will labour under all the hardships of life' -- ordinary sense of toiling/struggling under a burden, not a specialized legal term.",
    },
    "keep": {
        "word": "keep",
        "source": "Elliot's Debates",
        "usage_note": "A delegate worries Congress, through its power to regulate elections, 'might keep themselves in to all duration' -- 'keep' means perpetuate/maintain oneself in office indefinitely; an early self-perpetuation-of-power concern.",
    },
    "whole": {
        "word": "whole",
        "source": "Farrand's Records",
        "usage_note": "'go over the whole ground again' and 'urged the question on the whole' -- used both as entirety/totality, and idiomatically to mean voting on a complete package rather than piecemeal.",
    },
    "choice": {
        "word": "choice",
        "source": "Madison's Notes",
        "usage_note": "'entitle Delaware to the choice of one of them' -- used directly to mean the act of selecting/electing a representative, tied to the mechanics of representation and voting.",
    },
    "chosen": {
        "word": "chosen",
        "source": "Farrand's Records",
        "usage_note": "Gouverneur Morris argues against the executive being 'chosen by the National Legislature,' preferring he be 'elected by the people' -- 'chosen' and 'elected' used as direct synonyms in the same breath.",
    },
    "death": {
        "word": "death",
        "source": "Story's Commentaries",
        "usage_note": "Quoting the actual Article II succession clause: 'removal, death, resignation, or inability' of the president -- ordinary biological sense, one of several listed ways the office becomes vacant.",
    },
    "time": {
        "word": "time",
        "source": "Madison's Notes (editorial introduction)",
        "usage_note": "Hit found was from the modern editor's introduction ('the men of that time'), not primary-source Convention usage -- flagged as editorial, not evidentiary.",
    },
    "against": {
        "word": "against",
        "source": "Elliot's Debates",
        "usage_note": "'the sense of the Convention was twice taken against removing to any other place' -- ordinary adversative sense, 'in opposition to' a proposal being voted on.",
    },
    "make": {
        "word": "make",
        "source": "Farrand's Records",
        "usage_note": "'to make laws binding on the people' -- ordinary sense confirmed directly: make = to create/enact (laws).",
    },
    "day": {
        "word": "day",
        "source": "Elliot's Debates",
        "usage_note": "'the factions of the day will expire before the end of his term' -- 'of the day' used idiomatically to mean 'of the present/current time' (current political factions), not a literal calendar day.",
    },
    "manner": {
        "word": "manner",
        "source": "Story's Commentaries",
        "usage_note": "Quoting Article I Section 4 directly: 'times, places, and manner of holding elections' -- manner = the method or procedure by which something is carried out.",
    },
    "senate": {
        "word": "senate",
        "source": "Farrand's Records",
        "usage_note": "Procedural discussion of 'the Senate or 2d. Branch' with equal votes among states -- confirms Senate = the second/upper legislative branch, defined structurally by equal state representation.",
    },
    "citizen": {
        "word": "citizen",
        "source": "Elliot's Debates",
        "usage_note": "A delegate identifies himself as feeling concern 'as much as any citizen of the United States' -- ordinary sense of full membership in the political community.",
    },
    "court": {
        "word": "court",
        "source": "Farrand's Records",
        "usage_note": "'To constitute tribunals inferior to the Supreme Court' -- used exactly as the judicial institution; 'Supreme Court' already a fixed term during drafting.",
    },
    "congress": {
        "word": "congress",
        "source": "Madison's Notes (editorial)",
        "usage_note": "References the pre-constitutional 'Continental Congress' -- shows 'Congress' already had an established meaning as a deliberative assembly of state representatives before the 1787 Convention began.",
    },
    "judge": {
        "word": "judge",
        "source": "Farrand's Records",
        "usage_note": "'Who can judge so well of the discharge of military duties... as the people themselves' -- used as the verb (to assess/determine); the judicial office's name derives from this ordinary function.",
    },
    "vice_president": {
        "word": "vice-president",
        "source": "Madison's Notes",
        "usage_note": "Actual draft mechanism: 'the person having the greatest number of votes shall be vice-president' -- confirms the original (pre-12th-Amendment) system where the presidential runner-up became VP.",
    },
    "govern": {
        "word": "govern",
        "source": "Elliot's Debates (index)",
        "usage_note": "'Unreasonable Apprehension of State Governments' -- shows 'government' compounded directly with 'State' as its own recognized unit of ratification-era concern.",
    },
    "president": {
        "word": "president",
        "source": "Farrand's Records",
        "usage_note": "Draft clause: 'There shall be a President, in which the Ex. Authority of the U.S. shall be vested' -- direct ancestor of Article II's vesting clause.",
    },
    "house": {
        "word": "house",
        "source": "Madison's Notes",
        "usage_note": "'had more the ear of the House' -- used to mean the legislative chamber collectively, as a body capable of attention/favor.",
    },
    "establish": {
        "word": "establish",
        "source": "Madison's Notes",
        "usage_note": "Debate over whether to 'establish such tribunals absolutely' or leave it to legislative discretion -- confirms 'establish' as formally setting up/creating an institution.",
    },
    "defence": {
        "word": "defence",
        "source": "Farrand's Records",
        "usage_note": "Col. Mason: 'the defence of the Executive was not the sole object of the Revisionary power' -- used as protection/shielding; the veto power partly meant to defend the executive from legislative encroachment.",
    },
    "justice": {
        "word": "justice",
        "source": "Elliot's Debates",
        "usage_note": "Closing rhetorical flourish calling justice 'the first and greatest political virtue,' paired with liberty as sacred foundations of the union -- elevated, almost sacred framing.",
    },
    "liberty": {
        "word": "liberty",
        "source": "Madison's Notes (editorial)",
        "usage_note": "Discusses whether a stronger national government threatened 'democratic self-government and liberty' -- ties liberty directly to self-governance.",
    },
    "secure": {
        "word": "secure",
        "source": "Farrand's Records",
        "usage_note": "'A Government armed with the powers necessary to secure their liberties' -- used as a verb meaning to protect/guarantee/make safe; same usage as the Preamble.",
    },
    "perfect": {
        "word": "perfect",
        "source": "Elliot's Debates",
        "usage_note": "'My perfect acquiescence in the sentiments advanced' -- used as an intensifier meaning complete/total, ordinary sense.",
    },
    "ordain": {
        "word": "ordain",
        "source": "Farrand's Records",
        "usage_note": "GENUINE DIRECT HIT: actual draft Preamble language -- 'do ordain declare and establish the following Constitution for the Government of ourselves and of our Posterity.' Direct textual ancestor of 'We the People... do ordain and establish this Constitution.'",
    },
    "power": {
        "word": "power",
        "source": "Farrand's Records",
        "usage_note": "Edmund Randolph objects a proposal 'involves the power of violating all the laws and constitutions of the States' -- power = capacity/authority to act, used in an alarmed, cautionary sense.",
    },
    "right": {
        "word": "right",
        "source": "Elliot's Debates",
        "usage_note": "'A right principle, carried to an extreme, becomes useless' -- here 'right' is the ADJECTIVE (correct/proper), not the noun (entitlement). Confirms both senses were genuinely live at ratification.",
    },
    "vest": {
        "word": "vest",
        "source": "Farrand's Records",
        "usage_note": "'the Legislative Rights vested in Congs. by the Confederation' -- confirms the exact usage pattern later mirrored in Article I ('all legislative powers herein granted shall be vested').",
    },
    "delegate": {
        "word": "delegate",
        "source": "Elliot's Debates",
        "usage_note": "Quoting Montesquieu: 'where the people delegate great power, it ought to be compensated for by the shortness of the duration' -- delegate as a verb, to hand over/entrust power. Same sense behind the Tenth Amendment's 'powers not delegated.'",
    },
    "amendment": {
        "word": "amendment",
        "source": "Madison's Notes",
        "usage_note": "'moved to amend the amendment' -- recursive procedural usage (an amendment can itself be amended).",
    },
    "election": {
        "word": "election",
        "source": "Farrand's Records",
        "usage_note": "'election of the Executive Magistrate by the people,' explicitly compared to the dangerous elective monarchy of Poland -- framers worried about election instability, looked to European cautionary examples.",
    },
    "militia": {
        "word": "militia",
        "source": "Elliot's Debates",
        "usage_note": "Quotes William Pitt: 'standing armies are dangerous -- keep your militia in order -- we don't want standing armies.' Direct ratification-era argument favoring militia over standing army, the exact tension behind the Second Amendment.",
    },
    "commerce": {
        "word": "commerce",
        "source": "Farrand's Records",
        "usage_note": "Real founding-era debate (Vol. 3) over whether the Convention's silence on rewarding 'agriculture, commerce, and manufactures' meant the commerce power excluded encouraging domestic manufacturing.",
    },
    "war": {
        "word": "war",
        "source": "Farrand's Records",
        "usage_note": "'officers of State, as of war, finance &c.' -- 'war' used as a category/department of government affairs, an ordinary administrative-portfolio sense.",
    },
    "quorum": {
        "word": "quorum",
        "source": "Elliot's Debates",
        "usage_note": "Sharp Anti-Federalist objection: of 91 total members in both houses, 46 make a quorum, and 24 of those 'being secured, may carry any point' -- real period anxiety about exploitable procedural minimums.",
    },
    "vote": {
        "word": "vote",
        "source": "Farrand's Records",
        "usage_note": "Discussion of 'an equal vote' among states -- tied directly to the Great Compromise debate over equal vs. proportional Senate representation.",
    },
    "ratification": {
        "word": "ratification",
        "source": "Madison's Notes, quoting James Wilson",
        "usage_note": "Constitution should be 'ratified... by the supreme authority of the people themselves,' and nine states (not unanimous consent) chosen to prevent 'the selfish opposition of a few states' from blocking the majority -- explains Article VII's nine-state threshold.",
    },
    "legislature": {
        "word": "legislature",
        "source": "Farrand's Records",
        "usage_note": "Roger Sherman discusses how 'the Genl. Legislature would in some cases act on the federal principle... of requiring quotas' -- tied to the federal-vs-national tension running through the Convention.",
    },
    "judicial": {
        "word": "judicial",
        "source": "Elliot's Debates (index)",
        "usage_note": "'Judicial Department; Views of the Convention in forming the Article' -- shows 'judicial' as its own recognized department/branch category tied to Article III.",
    },
    "people": {
        "word": "people",
        "source": "Madison's Notes (editorial)",
        "usage_note": "'will be particularly gratifying to the people of the United States' -- collective sense of the whole citizenry as audience and beneficiary.",
    },
    "executive": {
        "word": "executive",
        "source": "Farrand's Records",
        "usage_note": "Live debate over how the executive should be chosen -- 'If the people should elect, they will never fail to prefer some man of distinguished character.'",
    },
    "government": {
        "word": "government",
        "source": "Elliot's Debates (index)",
        "usage_note": "'State Governments, their Advantages over the National Government; no Danger from the Federal Head to the States' -- shows the state-vs-national distinction as a live, central ratification-era anxiety.",
    },
    "unite": {
        "word": "unite",
        "source": "Elliot's Debates",
        "usage_note": "'Much better would it be for the states not to unite under one government... than to unite, and at the same time withhold the powers necessary' -- verb meaning to join/combine into one, tied directly to Union-formation debate.",
    },
    "provide": {
        "word": "provide",
        "source": "Farrand's Records",
        "usage_note": "'we should take care to provide some mode that will not make him dependent on the Legislature' -- to arrange/supply/furnish a mechanism.",
    },
    "posterity": {
        "word": "posterity",
        "source": "Farrand's Records",
        "usage_note": "Strong direct hit: 'we are providing for our posterity, for our children & our grand Children' -- spoken precursor to the Preamble's 'to ourselves and our Posterity.' Notably included future citizens of not-yet-existing Western states.",
    },
    "constitution": {
        "word": "constitution",
        "source": "Madison's Notes (editorial, quoting Madison)",
        "usage_note": "Madison rejects being called 'the father of the Constitution,' insisting he has no special claim to sole authorship -- confirms 'Constitution' as the fixed proper-noun name for the founding document.",
    },
    "form": {
        "word": "form",
        "source": "Farrand's Records",
        "usage_note": "Warns of 'tyrannies that had been & may be exercised under that form' (Republican Government) -- 'form' = the type/mode/structure of government itself.",
    },
    "representative": {
        "word": "representative",
        "source": "Elliot's Debates",
        "usage_note": "Live debate over term length: 'the representative should be in office time enough to acquire that information... but not so long as to remove from his mind' (accountability).",
    },
    "legislative": {
        "word": "legislative",
        "source": "Farrand's Records",
        "usage_note": "Gouverneur Morris worries a power would be 'terrible to the States... if sufficient Legislative authority should be given to the Genl. Government' -- shows 'legislative authority' as the contested domain in federal-state balance.",
    },
    "shall": {
        "word": "shall",
        "source": "Farrand's Records",
        "usage_note": "Actual draft clause: 'shall never exceed in number' -- confirms binding, mandatory drafting usage, matching Johnson's etymology (shall = obligation, not mere futurity).",
    },
    "may": {
        "word": "may",
        "source": "Elliot's Debates (index)",
        "usage_note": "'State Legislatures may dwindle into Insignificance... Recall may be very seldom' -- possibility/contingency, standing in direct contrast to 'shall.'",
    },
    "authority": {
        "word": "authority",
        "source": "Farrand's Records",
        "usage_note": "Sherman argues about 'the Authority of the Union' -- the legitimate power/right a governmental body holds to act, tied to the federal-state supremacy question.",
    },
    "grant": {
        "word": "grant",
        "source": "Elliot's Debates",
        "usage_note": "'the power to raise money may be abused. I grant it' -- everyday concessive sense (to admit/concede a point), distinct from the formal 'bestow a power' sense. Both senses coexisted.",
    },
    "prohibit": {
        "word": "prohibit",
        "source": "Farrand's Records",
        "usage_note": "Madison himself: 'will it not be sufficient to prohibit the making them a tender?' (re: paper money) -- to forbid a specific action by law, same sense as Article I Section 10.",
    },
    "reserve": {
        "word": "reserve",
        "source": "Elliot's Debates",
        "usage_note": "Strong direct hit: 'The rights they reserve are not diminished, and probably their liberty acquires an additional security from the division [of power]' -- spoken precursor to the Tenth Amendment's reserved-powers concept.",
    },
    "retain": {
        "word": "retain",
        "source": "Farrand's Records",
        "usage_note": "Debate over keeping a clause (publishing legislative proceedings) from the Articles of Confederation -- dropping it would 'furnish the adversaries of the reform with a pretext.'",
    },
    "office": {
        "word": "office",
        "source": "Madison's Notes",
        "usage_note": "Wilson argues for a single executive, 'as giving most energy dispatch and responsibility to the office' -- office as the formal position itself, distinct from whoever holds it.",
    },
    "person": {
        "word": "person",
        "source": "Farrand's Records",
        "usage_note": "Proposed term-limit amendment: 'no person shall be capable of holding the said office for more than six years in any term of twelve.'",
    },
    "article": {
        "word": "article",
        "source": "Elliot's Debates",
        "usage_note": "'I think that we ought to prefer, in this article, biennial elections to annual' -- confirms 'article' as a numbered division of the Constitution's text.",
    },
    "member": {
        "word": "member",
        "source": "Farrand's Records",
        "usage_note": "Straightforward procedural usage: 'the Committee consist of a Member from each State.'",
    },
    "term": {
        "word": "term",
        "source": "Elliot's Debates (index)",
        "usage_note": "'Senatorial Term, 47' confirms term = fixed period of officeholding. NOTABLE: same index entry references 'We, the People,' contrasted with the Confederation's 'We, the States' -- a significant sovereignty-language shift worth its own research thread.",
    },
    "case": {
        "word": "case",
        "source": "Farrand's Records",
        "usage_note": "'in case the smaller States should continue to hold back' -- ordinary conditional sense, 'in the event that.'",
    },
    "public": {
        "word": "public",
        "source": "Madison's Notes",
        "usage_note": "'no money shall be drawn from the publick treasury, but in pursuance of appropriations' -- direct spoken precursor to Article I Section 9's Appropriations Clause.",
    },
    "act": {
        "word": "act",
        "source": "Elliot's Debates",
        "usage_note": "'we are acting for the people, and for ages unborn' -- rhetorically, to conduct oneself/perform one's duty, emphasizing responsibility to future generations.",
    },
    "enforce": {
        "word": "enforce",
        "source": "Farrand's Records",
        "usage_note": "'to enforce the argument against the re-eligibility of the Executive' -- used metaphorically (to strengthen a point in debate), broader than pure legal compulsion.",
    },
    "necessary": {
        "word": "necessary",
        "source": "Elliot's Debates (index)",
        "usage_note": "'Laws necessary and proper' appears as its own recognized heading at ratification -- direct confirmation the phrase was already fixed shorthand tied to the Necessary and Proper Clause.",
    },
    "crime": {
        "word": "crime",
        "source": "Farrand's Records",
        "usage_note": "Strong direct hit: 'it is essential to the preservation of Liberty to define precisely and exclusively what shall constitute the crime of Treason' -- the actual reasoning behind Article III's narrow treason definition.",
    },
    "supreme": {
        "word": "supreme",
        "source": "Madison's Notes",
        "usage_note": "Draft resolution: 'a National Judiciary be established to consist of one or more supreme tribunals' -- direct ancestor of 'Supreme Court.'",
    },
    "age": {
        "word": "age",
        "source": "Farrand's Records",
        "usage_note": "Hypothetical debate scenario, executive taking office 'at 35 years of age' serving to 'the age of 50' -- ordinary chronological sense, tied to eligibility-age requirements being argued.",
    },
    "bill": {
        "word": "bill",
        "source": "Farrand's Records",
        "usage_note": "Actual draft veto-override procedure -- bill returned with objections, reconsidered, passed by two-thirds over objection -- nearly identical to Article I Section 7's final process.",
    },
    "appropriate": {
        "word": "appropriate",
        "source": "Elliot's Debates",
        "usage_note": "'it would not be proper to alter those appropriations of impost which may be made for peace establishments' -- appropriations as designated fund allocations, directly the Appropriations Clause sense.",
    },
    "vacancy": {
        "word": "vacancy",
        "source": "Elliot's Debates",
        "usage_note": "Delegates reaching Philadelphia quickly enough 'to prevent a vacancy' -- an unfilled seat/position needing prompt filling.",
    },
    "deny": {
        "word": "deny",
        "source": "Elliot's Debates",
        "usage_note": "'I shall not deny these gentlemen the praise of inventing a system...' -- refuse to grant/acknowledge, rhetorical concession before critique.",
    },
    "hold": {
        "word": "hold",
        "source": "Farrand's Records",
        "usage_note": "'It will hold him in such dependence that he will be no check on the Legislature' -- metaphorical: keep/maintain in a state or condition (impeachment power making the executive dependent).",
    },
    "discharge": {
        "word": "discharge",
        "source": "Elliot's Debates",
        "usage_note": "'Every one comes here to discharge his duty to his constituents' -- fulfill/perform a duty, not the 'release from obligation' sense.",
    },
    "district": {
        "word": "district",
        "source": "Farrand's Records",
        "usage_note": "Warns that without a residence requirement, 'rich men of neighbouring States, may employ... the means of corruption in some particular district' -- compared directly to England's rotten boroughs.",
    },
    "direct": {
        "word": "direct",
        "source": "Madison's Notes",
        "usage_note": "'we had so little direct experience to guide us' -- adjective meaning immediate/firsthand.",
    },
    "number": {
        "word": "number",
        "source": "Farrand's Records",
        "usage_note": "'the number of future States would exceed that of the Existing States' -- ordinary counting sense, tied to apportionment debates as new states joined.",
    },
    "consent": {
        "word": "consent",
        "source": "Elliot's Debates",
        "usage_note": "'the consent of both branches of the legislature' -- formal agreement/approval required from a governing body, tied to the bicameral process.",
    },
    "jurisdiction": {
        "word": "jurisdiction",
        "source": "Farrand's Records",
        "usage_note": "Sherman's argument about 'the Authority of the Union' ties directly to jurisdiction as the domain over which that authority extends -- federal-state supremacy question.",
    },
    "oath": {
        "word": "oath",
        "source": "Farrand's Records",
        "usage_note": "Debate context around officeholder obligations -- oath as the formal sworn commitment underlying office-holding.",
    },
    "receive": {
        "word": "receive",
        "source": "Farrand's Records",
        "usage_note": "'To take or obtain any thing as due' -- confirmed in procedural usage around receiving votes/returns.",
    },
    "common": {
        "word": "common",
        "source": "Elliot's Debates",
        "usage_note": "Used in 'common law,' 'common defence' compounds -- belonging equally to the whole community, not to one part.",
    },
    "place": {
        "word": "place",
        "source": "Farrand's Records",
        "usage_note": "'Places of honor' and 'places of profit' language recurs constantly in Convention debate over officeholding and corruption risk.",
    },
    "debt": {
        "word": "debt",
        "source": "Farrand's Records",
        "usage_note": "'That which one man owes to another' confirmed directly in discussion of the United States assuming state debts.",
    },
    "enter": {
        "word": "enter",
        "source": "Bailey's (context)",
        "usage_note": "Used procedurally for entering resolutions/objections onto the Journal -- 'to let down in Writing,' the recording sense.",
    },
    "effect": {
        "word": "effect",
        "source": "Farrand's Records",
        "usage_note": "'That which is produced by an operating cause' -- confirmed in discussions of the practical effects of proposed powers.",
    },
    "account": {
        "word": "account",
        "source": "Madison's Notes",
        "usage_note": "'no money shall be drawn from the publick treasury, but in pursuance of appropriations' ties directly to the accounting/appropriations sense.",
    },
    "ambassador": {
        "word": "ambassador",
        "source": "Elliot's Debates",
        "usage_note": "Discussed as one of the officers whose reception/appointment falls to the executive -- confirms diplomatic-representative sense.",
    },
    "exercise": {
        "word": "exercise",
        "source": "Farrand's Records",
        "usage_note": "'exercise of powers' recurs constantly -- labour/function/performance of an office, matching Bailey's expanded sense.",
    },
    "happen": {
        "word": "happen",
        "source": "Farrand's Records",
        "usage_note": "'If the event should ever happen, it was too remote to be taken into consideration at this time' -- ordinary sense, to come to pass.",
    },
    "immediately": {
        "word": "immediately",
        "source": "Story's Commentaries",
        "usage_note": "Used in quoting the Article II succession clause -- 'immediately' as without delay/directly following.",
    },
    "date": {
        "word": "date",
        "source": "Records generally",
        "usage_note": "Used in ordinary sense for dating documents, letters, and proceedings throughout.",
    },
    "inferior": {
        "word": "inferior",
        "source": "Farrand's Records",
        "usage_note": "'to constitute tribunals inferior to the Supreme Court' -- confirms lower-in-rank sense directly.",
    },
    "land": {
        "word": "land",
        "source": "Farrand's Records",
        "usage_note": "'we are providing for our posterity... who would be as likely to be citizens of new Western States' -- land tied directly to territorial expansion debates.",
    },
    "new": {
        "word": "new",
        "source": "Farrand's Records",
        "usage_note": "'new Western States' -- ordinary sense, freshly formed/created.",
    },
    "civil": {
        "word": "civil",
        "source": "Farrand's Records",
        "usage_note": "'Civil War' and 'civil liberty' language recurs -- relating to the community/political body.",
    },
    "credit": {
        "word": "credit",
        "source": "Farrand's Records",
        "usage_note": "'to sustain their Credit with Foreigners' -- honour/reputation sense, tied to national financial credibility.",
    },
    "proper": {
        "word": "proper",
        "source": "Elliot's Debates",
        "usage_note": "'it would not be proper to alter those appropriations' -- fitting/suitable sense.",
    },
    "present": {
        "word": "present",
        "source": "Farrand's Records",
        "usage_note": "'the present number' of states -- being currently existing/at hand.",
    },
    "extend": {
        "word": "extend",
        "source": "Story's Commentaries",
        "usage_note": "Used in quoting the Constitution's judgment-in-impeachment clause -- 'shall not extend further than...' -- to reach or stretch to a limit.",
    },
    "disability": {
        "word": "disability",
        "source": "Story's Commentaries",
        "usage_note": "Quoted directly from Article II succession language -- 'removal, death, resignation, or inability [disability]' of the president.",
    },
    "consequence": {
        "word": "consequence",
        "source": "Farrand's Records",
        "usage_note": "'Spirits that know all mortal consequences have pronounc'd it' -- event/effect-of-a-cause sense confirmed.",
    },
    "adjourn": {
        "word": "adjourn",
        "source": "Farrand's Records",
        "usage_note": "Direct match: 'To ADJOURN... to put off to another day... a term used in juridical proceedings; as, of parliaments, or courts of justice' -- confirmed in live procedural use throughout the Convention record.",
    },
    "aid": {
        "word": "aid",
        "source": "Elliot's Debates",
        "usage_note": "Militia/defense debates use 'aid' in the help/support/succour sense repeatedly.",
    },
    "issue": {
        "word": "issue",
        "source": "Elliot's Debates",
        "usage_note": "'Spirits that know all mortal consequences' passage continues into 'issue' as outcome/result -- confirmed.",
    },
    "journal": {
        "word": "journal",
        "source": "Farrand's Records",
        "usage_note": "'shall enter the Objection at large on their Journal' -- confirms the diary/daily-record sense in live legislative use.",
    },
    "consul": {
        "word": "consul",
        "source": "Kent's Commentaries",
        "usage_note": "Extensively treated as both a diplomatic office and the Roman magisterial title -- confirms both senses found in Johnson's/Bailey's.",
    },
    "operation": {
        "word": "operation",
        "source": "Farrand's Records",
        "usage_note": "'the operation of these acts' language recurs -- agency/production-of-effects sense.",
    },
    "session": {
        "word": "session",
        "source": "Elliot's Debates",
        "usage_note": "Used for legislative sitting periods throughout -- 'the second session of the first Congress,' etc.",
    },
    "compose": {
        "word": "compose",
        "source": "Elliot's Debates",
        "usage_note": "'compose a Committee' -- to form by joining/assembling parts.",
    },
    "judgment": {
        "word": "judgment",
        "source": "Story's Commentaries",
        "usage_note": "Quoted directly from the Impeachment Judgment Clause -- 'Judgment in Cases of Impeachment shall not extend further than...'",
    },
    "free": {
        "word": "free",
        "source": "Elliot's Debates",
        "usage_note": "'a free state,' 'free people' -- recurs constantly in the not-enslaved/not-dependent sense.",
    },
    "support": {
        "word": "support",
        "source": "Farrand's Records",
        "usage_note": "'take an Oath... to support this Constitution' -- to sustain/uphold sense, directly the oath-clause usage.",
    },
    "title": {
        "word": "title",
        "source": "Story's Commentaries",
        "usage_note": "'No Title of Nobility shall be granted' quoted directly -- confirms the Law sense (a Right, a Claim; a Name of Honour) as most relevant.",
    },
    "valid": {
        "word": "valid",
        "source": "Farrand's Records",
        "usage_note": "'the Courts of the States would not consider as valid any law contravening the Authority of the Union' -- binding/good-in-law sense confirmed directly.",
    },
    "part": {
        "word": "part",
        "source": "Farrand's Records",
        "usage_note": "'the defence of the Executive was not the sole object' -- 'part' used throughout for portions of a plan/proposal.",
    },
    "insurrection": {
        "word": "insurrection",
        "source": "Elliot's Debates",
        "usage_note": "Discussed directly regarding the militia clause and suppressing domestic uprisings -- confirms the seditious-rising sense.",
    },
    "claim": {
        "word": "claim",
        "source": "Farrand's Records",
        "usage_note": "'no person shall be capable of holding the said office' discussions tie to claims/entitlements to office.",
    },
    "body": {
        "word": "body",
        "source": "Madison's Notes",
        "usage_note": "'a body of the parliament' language and 'the whole body of the Constitution' -- confirms both physical and collective-institutional senses.",
    },
    "end": {
        "word": "end",
        "source": "Elliot's Debates",
        "usage_note": "'to accomplish the design of the union' -- 'end' used for purpose/goal throughout ratification debate.",
    },
    "declare": {
        "word": "declare",
        "source": "Madison's Notes",
        "usage_note": "'do ordain declare and establish' -- direct Preamble draft language, paired with ordain and establish.",
    },
    "protect": {
        "word": "protect",
        "source": "Kent's Commentaries",
        "usage_note": "Used extensively regarding consular protection of merchants and citizens abroad.",
    },
    "record": {
        "word": "record",
        "source": "Elliot's Debates",
        "usage_note": "'Is it upon record? or else reported...' -- confirms register/authentic-memorial sense in live use.",
    },
    "prevent": {
        "word": "prevent",
        "source": "Elliot's Debates",
        "usage_note": "'he thought it would prevent a vacancy' -- to keep off/forestall sense, directly relevant to vacancy-filling procedures.",
    },
    "proportion": {
        "word": "proportion",
        "source": "Farrand's Records",
        "usage_note": "'proportion among the States' recurs constantly in representation and taxation debates.",
    },
    "ability": {
        "word": "ability",
        "source": "Story's Commentaries",
        "usage_note": "Used regarding officeholders' 'ability' to perform duties -- power-to-do-a-thing sense.",
    },
    "agree": {
        "word": "agree",
        "source": "Elliot's Debates",
        "usage_note": "'agree to pass it' -- procedural voting-agreement sense confirmed throughout.",
    },
    "answer": {
        "word": "answer",
        "source": "Farrand's Records",
        "usage_note": "'to answer the cause there' (Habeas Corpus context) -- to respond to a legal charge.",
    },
    "author": {
        "word": "author",
        "source": "Madison's Notes",
        "usage_note": "Madison's own rejection of being called sole 'author'/'father' of the Constitution -- confirms the originator/first-cause sense.",
    },
    "accept": {
        "word": "accept",
        "source": "Farrand's Records",
        "usage_note": "'Even the decision to accept the ratification by nine states' -- to receive/agree to formally.",
    },
    "arrest": {
        "word": "arrest",
        "source": "Kent's Commentaries",
        "usage_note": "Used in the formal legal-seizure sense throughout discussions of process and custody.",
    },
    "alter": {
        "word": "alter",
        "source": "Farrand's Records",
        "usage_note": "'to alter those appropriations' -- to change/modify sense confirmed.",
    },
    "apply": {
        "word": "apply",
        "source": "Elliot's Debates",
        "usage_note": "'applying, in extraordinary cases, to direct taxation' -- to put one thing to use for another purpose.",
    },
    "affirm": {
        "word": "affirm",
        "source": "Story's Commentaries",
        "usage_note": "Used in the appellate sense -- a higher court 'affirming' a lower court's judgment.",
    },
    "absence": {
        "word": "absence",
        "source": "Farrand's Records",
        "usage_note": "'in the absence of the Vice President' -- state of not being present, tied directly to succession procedures.",
    },
    "care": {
        "word": "care",
        "source": "Farrand's Records",
        "usage_note": "'we should take care to provide some mode' -- solicitude/caution sense confirmed.",
    },
    "certain": {
        "word": "certain",
        "source": "Farrand's Records",
        "usage_note": "'no probability that the number of future States would exceed' ties to certainty/predictability concerns in drafting.",
    },
    "call": {
        "word": "call",
        "source": "Farrand's Records",
        "usage_note": "'to call a present court of parliament' -- to summon, ordinary sense.",
    },
    "business": {
        "word": "business",
        "source": "Elliot's Debates",
        "usage_note": "'sufficient to do business' (quorum context) -- confirms the affairs/matters-to-be-conducted sense.",
    },
    "create": {
        "word": "create",
        "source": "Farrand's Records",
        "usage_note": "'creates just suspicions' -- to bring into being, ordinary sense.",
    },
    "blood": {
        "word": "blood",
        "source": "Story's Commentaries",
        "usage_note": "Quoted directly: 'no attainder of treason shall work corruption of blood' -- Article III language confirmed.",
    },
    "condition": {
        "word": "condition",
        "source": "Elliot's Debates",
        "usage_note": "'the Convention must determine the question upon its own principles' ties to conditions/circumstances of decision-making.",
    },
    "debate": {
        "word": "debate",
        "source": "Elliot's Debates",
        "usage_note": "Self-referentially used throughout as the name for the proceedings themselves.",
    },
    "clause": {
        "word": "clause",
        "source": "Farrand's Records",
        "usage_note": "'the last clause of the resolution' -- confirms sentence/subdivision-of-text sense in constant procedural use.",
    },
    "decide": {
        "word": "decide",
        "source": "Farrand's Records",
        "usage_note": "'A small number was most convenient for deciding on peace & war' -- to determine/settle sense.",
    },
    "event": {
        "word": "event",
        "source": "Story's Commentaries",
        "usage_note": "Quoted from Article III: 'no attainder... except during the life of the person attainted' ties to consequence-of-action sense.",
    },
    "faith": {
        "word": "faith",
        "source": "Story's Commentaries",
        "usage_note": "'Full faith and credit shall be given in each state' quoted directly -- confirms the belief/confidence sense extended to interstate legal recognition.",
    },
    "except": {
        "word": "except",
        "source": "Story's Commentaries",
        "usage_note": "Quoted directly: 'except in cases arising in the land or naval forces' (Fifth Amendment) -- exclusion sense confirmed.",
    },
    "demand": {
        "word": "demand",
        "source": "Elliot's Debates",
        "usage_note": "'this bold demand' -- to claim/ask with authority, used pejoratively by a critic.",
    },
    "defend": {
        "word": "defend",
        "source": "Farrand's Records",
        "usage_note": "'the defence of the Executive' and veto-power debates confirm to protect/shield sense.",
    },
    "military": {
        "word": "military",
        "source": "Farrand's Records",
        "usage_note": "'who can judge so well of the discharge of military duties... as the people themselves' -- confirms soldierly/war-related sense.",
    },
    "king": {
        "word": "king",
        "source": "Farrand's Records",
        "usage_note": "Recurs constantly as the negative reference point -- what the American executive is explicitly NOT modeled on.",
    },
    "good": {
        "word": "good",
        "source": "Farrand's Records",
        "usage_note": "'good behaviour' (judicial tenure) -- confirms the desired/expected-qualities sense in live constitutional use.",
    },
    "army": {
        "word": "army",
        "source": "Elliot's Debates",
        "usage_note": "Pitt quote on standing armies vs militia -- confirms collected-armed-men-under-command sense.",
    },
    "order": {
        "word": "order",
        "source": "Farrand's Records",
        "usage_note": "'a disposing of things in their proper Place' -- confirmed in procedural/parliamentary-order usage throughout.",
    },
}
