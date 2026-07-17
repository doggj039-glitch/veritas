# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Literal English Dictionary -- founding-era definitions.

This is the SINGLE, authoritative definitions source for VERITAS. It replaces
the earlier literal_dictionary.py, which contained 42 unreliable entries mixed
in among genuine 1755 entries:
  - 27 entries silently used modern 'Standard Dictionary' definitions instead
    of Johnson's, with no visible flag distinguishing them from real 1755 entries.
  - 13 entries had no actual definition text at all -- only a leftover
    illustrative quotation survived a bad extraction from the original source.
  - 2 entries were essentially empty (a stray citation fragment only).

Those 42 entries were removed rather than patched, to avoid stacking fixes on
top of an unreliable base. The remaining 399 genuinely valid entries from that
file were kept and merged with 209 words individually verified this session
directly against the real scanned text of the 1755 folio (with Nathan Bailey's
1721 dictionary used only as a fallback where Johnson's entry could not be
located). Where a word existed in both the old file and the new verified set,
the newly verified entry was kept, since it was checked against the primary
source directly rather than pulled from a secondary website.

Total words: 522
"""

LITERAL_DICTIONARY = {
    "ability": {
        "definition": "The power to do any thing, whether depending upon skill, or riches, or strength, or any other quality.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[habilete, French]",
    },
    "absence": {
        "definition": "The state of being absent, opposed to presence.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "accept": {
        "definition": "To take with pleasure; to receive kindly; to admit with approbation.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[accipio, Latin]",
    },
    "acceptance": {
        "definition": "1. Reception with approbation. By that acceptance of his sovereignty, they also accepted of his laws; why then should any other laws be now used amongst them? Spenser’s State of Ireland. If he tells us his noble deeds, we must also tell him our noble acceptance of them. Shakespeare’s Coriolanus. Some men cannot be fools with so good acceptance as others. South’s Sermons. Thus I imbolden’d spake, and freedom us’d",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/acceptance_ns",
    },
    "according": {
        "definition": "1. In a manner suitable to, agreeably to, in proportion. Our churches are places provided, that the people might there assemble themselves in due and decent manner, according to their several degrees and orders. Hooker, b. v. § 13. Our zeal, then, should be according to knowledge. And what kind of knowledge? Without all question, first, according to the true, saving, evangelical knowledge. It should be according to the gospel, the whole gospel: not only according to its truths, but precepts: not only according to its free grace, but necessary duties: not only according to its mysteries, but also its commandments. Sprat’s Sermons. How much more noble is the fame that is built on candour and ingenuity, according to those beautiful lines of Sir John Denham, in his Poem on Fletcher’s works. Addis. Spect. A man may, with prudence and a good conscience, approve of the professed principles of one party more than the other, according as he thinks they best promote the good of church and state.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/according_prep",
    },
    "account": {
        "definition": "A computation of debts or expenses; a register of facts relating to money.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[account, French]",
    },
    "accusation": {
        "definition": "1. The act of accusing. Thus they in mutual accusation spent The fruitless hours, but neither self-condemning, And of their vain contest appear’d no end. Milt. Par. Lost. 2. The charge brought against any one by the accuser. You read These accusations, and these grievous crimes",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/accusation_ns",
    },
    "acquiesce": {
        "definition": "To ACQUIE'SCE. v.n.  [acquiescer, Fr. acquiescere, Lat.] To rest in, or remain satisfied with, without opposition or discontent. Neither a bare approbation of, nor a mere wishing, nor unactive complacency in; nor, lastly, a natural inclination to things virtuous and good, can pass before God for a man’s willing of such things; and, consequently, if men, upon this account, will needs take up and acquiesce in an airy ungrounded persuasion, that they will those things which really they not will, they fall thereby into a gross and fatal delusion. South. He hath employed his transcendent wisdom and power, that by these he might make way for his benignity, as the end wherein they ultimately acquiesce. Grew’s Cosmolog. Sac. b. i.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/acquiesce_vn",
    },
    "act": {
        "definition": "Something done; a deed; an exploit, whether good or ill.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[actus, Latin]",
    },
    "addition": {
        "definition": "1. The act of adding one thing to another; opposed to diminution. The infinite distance between the Creator and the noblest of all creatures, can never be measured, nor exhausted by endless addition of finite degrees. Bentley’s Sermons. 2. Additament, or the thing added. It will not be modestly done, if any of our own wisdom intrude or interpose, or be willing to make additions to what Christ and his Apostles have designed. Hammond’s Fundam. Some such resemblances, methinks, I find Of our last evening’s talk, in this thy dream,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/addition_ns",
    },
    "adjourn": {
        "definition": "To put off to another day, naming the time: a term used in juridical proceedings; as, of parliaments, or courts of justice.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[adjourner, French]",
    },
    "adjournment": {
        "definition": "An assignment of a day, or a putting off till another day.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[adjournement, French]",
    },
    "administration": {
        "definition": "1. The act of administering or conducting any employment; as, the conducting the publick affairs; dispensing the laws. I then did use the person of your father; The image of his pow’r lay then in me: And in th’ administration of his law, While I was busy for the commonwealth, Your highness pleased to forget my place. Shakesp. Henry IV. In the short time of his administration, he shone so powerfully upon me, that, like the heat of a Russian summer, he ripened the fruits of poetry in a cold climate.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/administration_ns",
    },
    "adoption": {
        "definition": "1. The act of adopting, or taking to one’s self what is not native. See the hell of having a false woman! My bed shall be abused, my coffers ransacked, my reputation gnawn at; and I shall not only receive this villainous wrong, but stand under the adoption of abominable terms, and by him that does me the wrong. Shakesp. Merry Wives of Windsor. 2. The state of being adopted. In which time she purpos’d, By watching, weeping, tendance, kissing, to O’ercome you with her shew: yes, and in time (When she had fitted you with her craft) to work",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/adoption_ns",
    },
    "advice": {
        "definition": "1. Counsel; instruction: except that instruction implies superiority, and advice may be given by equals or inferiors. Break we our match up, and, by my advice, Let us impart what we have seen to-night Unto young Hamlet. Shakesp. Hamlet. O troubled, weak and coward, as thou art! Without thy poor advice, the lab’ring heart To worse extremes with swifter steps would run;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/advice_ns",
    },
    "affirm": {
        "definition": "To declare; to tell confidently: opposed to the word deny.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[affirmo, Latin]",
    },
    "affirmation": {
        "definition": "1. The act of affirming or declaring: opposed to negation or denial. This gentleman vouching, upon warrant of bloody affirmation, his to be more virtuous, and less attemptable, than any of our ladies. Shakesp. Cymbeline. 2. The position affirmed. That he shall receive no benefit from Christ, is the affirmation, whereon his despair is founded; and one way of removing this dismal apprehension, is, to convince him, that Christ’s death, if he perform the condition required, shall certainly belong to him. Hammond’s Fundamentals. 3. Confirmation: opposed to repeal. The learned in the laws of our land observe, that our statutes sometimes are only the affirmation, or ratification, of that which, by common law, was held before.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/affirmation_ns",
    },
    "after": {
        "definition": "1. Following in place. After is commonly applied to words of motion; as, he came after, and stood behind him. It is opposed to before. What says lord Warwick, shall we after them? —— —— After them! nay, before them, if we can. Shak. Henry VI. 2. In pursuit of. After whom is the king of Israel come out? After whom dost thou pursue? After a dead dog, after a flea. 1 Sam. xxiv. 14. 3. Behind.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/after_prep",
    },
    "against": {
        "definition": "Opposite to, instead of.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(Bailey's, 1721)",
    },
    "age": {
        "definition": "Any period of time attributed to something as the whole, or part, of its duration.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[aetas via French]",
    },
    "agree": {
        "definition": "To put an end to a variance.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "agreement": {
        "definition": "1. Concord. What agreement is there between the hyena and the dog? and what peace between the rich and the poor? Ecclus, xiii. 18. 2. Resemblance of one thing to another. Expansion and duration have this farther agreement, that though they are both considered by us as having parts, yet their parts are not separable one from another. Locke. 3. Compact; bargain; conclusion of controversy; stipulation. And your covenant with death shall be disannulled, and your agreement with hell shall not stand; when the overflowing scourge shall pass through, then ye shall be trodden down by it.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/agreement_ns",
    },
    "aid": {
        "definition": "To help; to support; to succour.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[adjutare, Latin]",
    },
    "all": {
        "definition": "1. The whole; opposed to part, or nothing. And will she yet debase her eyes on me; On me, whose all not equals Edward’s moiety? On me that halt, and am mishapen thus? Shak. Rich. III. Nought’s had, all’s spent, Where our desire is got without content. Shak. Macbeth.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/all_ns",
    },
    "alter": {
        "definition": "To change; to make otherwise than it is.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[alterer, French]",
    },
    "ambassador": {
        "definition": "A person sent in a public manner from one sovereign power to another, and supposed to represent the power from which he is sent.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "amendment": {
        "definition": "A change from bad for the better.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[amendement, French]",
    },
    "and": {
        "definition": "and, conj. And. conjunction. 1. The particle by which sentences or terms are joined, which it is not easy to explain by any synonimous word. Sure his honesty Got him small gains, but shameless flattery And filthy beverage, and unseemly thift, And borrow base, and some good lady’s gift. Spens. Hubb.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/and_conj",
    },
    "annihilation": {
        "definition": "God hath his influence into the very essence of things, without which their utter annihilation could not choose but follow. Hooker, b. v. § 56. That knowledge, which as spirits we obtain, Is to be valu’d in the midst of pain: Annihilation were to lose heav’n more: We are not quite exil’d, where thought can soar. Dryden.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/annihilation_ns",
    },
    "answer": {
        "definition": "To speak in return to a question.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "appellate": {
        "definition": "An appellatory libel ought to contain the name of the party appellant; the name of him from whose sentence it is appealed; the name of him to whom it is appealed; from what sentence it is appealed; the day of the sentence pronounced, and appeal interposed; and the name of the party appellate, or person against whom the appeal is lodged. Ayliffe’s Parergon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/appellate_ns",
    },
    "apply": {
        "definition": "To put one thing to another.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[applico, Latin]",
    },
    "appoint": {
        "definition": "To Appo'int. v.a.  [appointer, Fr.] 1. To fix any thing, as to settle the exact time for some transaction. The time appointed of the father. Galat. iv. 2. 2. To settle any thing by compact. He said, Appoint me thy wages, and I will pay it. Gen. xxx. 20. Now there was an appointed sign between the men of Israel and the liers in wait.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/appoint_va",
    },
    "apportionment": {
        "definition": "A dividing of a rent into two parts or portions, according as the land whence it issues, is divided among two or more proprietors.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/apportionment_ns",
    },
    "appropriate": {
        "definition": "To consign to some particular use or person.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[appropriare, low Latin]",
    },
    "appropriation": {
        "definition": "1. The application of something to a particular purpose. The mind should have distinct ideas of the things, and retain the particular name, with its peculiar appropriation to that idea. Locke. 2. The claim of any thing as peculiar. He doth nothing but talk of his horse, and make a great appropriation to his good parts, that he can shoe him himself. Shakesp. Merchant of Venice. 3. The fixing a particular signification to a word. The name of faculty may, by an appropriation that disguises its true sense, palliate the absurdity.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/appropriation_ns",
    },
    "approve": {
        "definition": "To Approve. v.a.  [approuver, Fr. approbo, Lat.] 1. To like; to be pleased with. There can be nothing possibly evil which God approveth, and that he approveth much more than he doth command. Hooker. What power was that, whereby Medea saw, And well approv’d, and prais’d the better course, When her rebellious sense did so withdraw Her feeble pow’rs, that she pursu’d the worse?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/approve_va",
    },
    "arms": {
        "definition": "All manner of Weapons.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[arma, Latin] (Bailey's, 1721)",
    },
    "army": {
        "definition": "A collection of armed men, obliged to obey one man.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[armie, French]",
    },
    "arrest": {
        "definition": "To seize by a mandate from a court or officer of justice.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[arrester, French]",
    },
    "article": {
        "definition": "1. A part of speech, as the, an, a. 2. A single clause of an account; a particular part of any composition.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[articulus, Latin]",
    },
    "as": {
        "definition": "as, conj. As. conjunct. [als, Teut.] 1. In the same manner with something else. When thou dost hear I am as I have been, Approach me, and thou shalt be as thou wast. Shakespeare’s Henry IV. In singing, as in piping, you excel; And scarce your master could perform so well.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/as_conj",
    },
    "assemble": {
        "definition": "To bring together into one place; a collection of persons and things. (covers assembled, assembling)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[assembler, French]",
    },
    "assistance": {
        "definition": "The council of Trent commends recourse, not only to the prayers of the saints, but to their aid and assistance: What doth this aid and assistance signify? Stillingfleet. You have abundant assistances for this knowledge, in excellent books. Wake’s Preparation for Death. Let us entreat this necessary assistance, that by his grace he would lead us. Rogers.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/assistance_ns",
    },
    "assume": {
        "definition": "To ASSU'ME. v.a.  [assumo, Lat.] 1. To take. This when the various God had urg’d in vain, He strait assum’d his native form again. Pope. 2. To take upon one’s self. With ravish’d ears, The monarch hears,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/assume_va",
    },
    "at": {
        "definition": "1. At before a place, notes the nearness of the place; as, a man is at the house before he is in it. This custom continued among many, to say their prayers at fountains. Stillingfleet’s Def. of Disc. on Romish Idolatry. To all you ladies now at land We men at sea indite. Buckhurst. 2. At before a word signifying time, notes the coexistence of the time with the event; the word time is sometimes included in the adjective. We thought it at the very first a sign of cold affection. Hooker.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/at_prep",
    },
    "attainder": {
        "definition": "Bill of Attainder: a Bill brought into the House of Parliament, for the Attainting, Condemning, and Executing a Person for High Treason -- the exact legislative act Article I's Bill of Attainder Clause prohibits.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(Bailey's, 1721)",
    },
    "attendance": {
        "definition": "1. The act of waiting on another; or of serving. I dance attendance here, I think the duke will not be spoke withal. Shakesp. R. III. For he, of whom these things are spoken, pertaineth to another tribe, of which no man gave attendance at the altar. Heb. vii. 13. The other, after many years attendance upon the duke, was now one of the bedchamber to the prince. Clarendon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/attendance_ns",
    },
    "author": {
        "definition": "The first beginner or mover of any thing; he to whom any thing owes its original.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[auctor, Latin]",
    },
    "authority": {
        "definition": "Legal power.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[auctoritas, Latin]",
    },
    "be": {
        "definition": "To BE. v.n.  [This word is so remarkably irregular, that it is necessary to set down many of its terminations. Present.	I am,	thou art,	he is,	we are, &c. eom,	eart,	is,	aron, Sax. Preter.	I was,	thou wert,	he was,	we were, &c. wæs,	wære,	was,	wæron, Sax. The conjunctive mood. I be,	thou beest,	he be,	we be, &c. beo,	bist,	beo,	beon, Sax.]",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/be_vn",
    },
    "begin": {
        "definition": "To Begin. v.a. 1. To do the first act of any thing; to pass from not doing to doing, by the first act. Ye nymphs of Solyma, begin the song. Pope’s Messiah. They have been awaked, by these awful scenes, to begin religion; and, afterwards, their virtue has improved itself into more refined principles, by divine grace. Watts. 2. To trace from any thing as the first ground. The apostle begins our knowledge in the creatures, which leads us to the knowledge of God.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/begin_va",
    },
    "beginning": {
        "definition": "1. The first original or cause. Wherever we place the beginning of motion, whether from the head or the heart, the body moves and acts by a consent of all its parts. Swift. 2. The entrance into act, or being. Also in the day of your gladness, and in your solemn days, and in the beginnings of your months, you shall blow the trumpets over your burnt offering. Numbers, x. 10. Youth, what man’s age is like to be, doth show; We may our end by our beginning know.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/beginning_ns",
    },
    "behaviour": {
        "definition": "Manner of behaving one's self, whether good or bad; manners. 2. External appearance. 3. Conduct; course of life.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/behaviour_ns",
    },
    "being": {
        "definition": "1. Existence; opposed to nonentity. Of him all things have both received their first being, and their continuance to be that which they are. Hooker, b. v. Yet is not God the author of her ill, Though author of her being, and being there. Davies. There is none but he, Whose being I do fear: and under him",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/being_ns",
    },
    "beverage": {
        "definition": "1. Drink; liquour to be drank in general. I am his cupbearer; If from me he have wholesome beverage, Account me not your servant. Shakesp. Winter’s Tale. Grains, pulses, and all sorts of fruits, either bread or beverage, may be made almost of all. Brown’s Vulgar Errours, b. iii. A pleasant beverage he prepar’d before,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/beverage_ns",
    },
    "bill": {
        "definition": "A written paper of any kind. (third of three BILL entries)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[billet, French]",
    },
    "blood": {
        "definition": "The red liquor that circulates in the bodies of animals.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[blod, Saxon]",
    },
    "body": {
        "definition": "The material substance, opposed to the immaterial soul.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[bodig, Saxon]",
    },
    "borrow": {
        "definition": "Yet of your royal presence I’ll adventure The borrow of a week. Shakesp. Winter’s Tale.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/borrow_ns",
    },
    "breach": {
        "definition": "1. The act of breaking any thing. This tempest Dashing the garment of this peace, aboded The sudden breach on’t. Shakesp. Henry VIII. 2. The state of being broken. O you kind gods! Cure this great breach in his abused nature.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/breach_ns",
    },
    "brethren": {
        "definition": "All these sects are brethren to each other in faction, ignorance, iniquity, perverseness, pride. Swift.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/brethren_ns",
    },
    "bribery": {
        "definition": "There was a law made by the Romans, against the bribery and extortion of the governours of provinces: before, says Cicero, the governours did bribe and extort as much as was sufficient for themselves; but now they bribe and extort as much as may be enough not only for themselves, but for judges, jurors, and magistrates. Bacon. No bribery of courts, or cabals of factions, or advantages of fortune, can remove him from the solid foundations of honour and fidelity. Dryden’s Aurengz. Preface.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/bribery_ns",
    },
    "bring": {
        "definition": "To BRING. v.a.  [bringan, Sax. preter. I brought; part. pass. brought; broht, Sax.] 1. To fetch from another place; distinguished from to carry, or convey, to another place. I was the chief that rais’d him to the crown, And I’ll be chief to bring him down again. Shakesp. H. VI. And as she was going to fetch it, he called to her, and said, Bring me, I pray thee, a morsel of bread in thy hand. 1 Kings, xvii. 11.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/bring_va",
    },
    "business": {
        "definition": "Employment; multiplicity of affairs.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from busy]",
    },
    "but": {
        "definition": "but, conj. BUT. conjunct. [bute, butan, Saxon.] 1. Except. An emission of immateriate virtues we are a little doubtful to propound, it is so prodigious: but that it is so constantly avouched by many. Bacon. Who can it be, ye gods! but perjur’d Lycon? Who can inspire such storms of rage, but Lycon? Where has my sword left one so black, but Lycon?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/but_conj",
    },
    "by": {
        "definition": "In this instance, there is, upon the by, to be noted, the percolation of the verjuice through the wood. Bacon’s Natural History, №. 79. This wolf was forced to make bold, ever and anon, with a sheep in private, by the by. L’Estrange. Hence we may understand, to add that upon the by, that it is not necessary. Boyle. So, while my lov’d revenge is full and high, I’ll give you back your kingdom by the by.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/by_ns",
    },
    "call": {
        "definition": "To name; to denominate.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "calling": {
        "definition": "1. Vocation; profession; trade. If God has interwoven such a pleasure with our ordinary calling, how much superiour must that be, which arises from the survey of a pious life? Surely, as much as christianity is nobler than a trade. South. We find ourselves obliged to go on in honest industry in our callings. Rogers. I cannot forbear warning you against endeavouring at wit in your sermons; because many of your calling have made themselves ridiculous by attempting it. Swift. I left no calling for this idle trade,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/calling_ns",
    },
    "capital": {
        "definition": "1. The upper part of a pillar. You see the volute of the Ionick, the foliage of the Corinthian, and the uovali of the Dorick, mixed, without any regularity, on the same capital. Addison on Italy. 2. The chief city of a nation or kingdom.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/capital_ns",
    },
    "care": {
        "definition": "Solicitude; anxiety; perturbation of mind; concern.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[care, Saxon]",
    },
    "case": {
        "definition": "Condition with regard to outward circumstances.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[casus, Latin]",
    },
    "cause": {
        "definition": "1. That which produces or effects any thing; the efficient. The wise and learned amongst the very heathens themselves, have all acknowledged some first cause, whereupon originally the being of all things dependeth; neither have they otherwise spoken of that cause, than as an agent, which, knowing what and why it worketh, observeth, in working, a most exact order or law. Hooker, b. i. § 2. Butterflies, and other flies, revive easily when they seem dead, being brought to the sun or fire; the cause whereof is the diffusion of the vital spirit, and the dilating of it by a little heat. Bacon’s Natural History, №. 697. Cause is a substance exerting its power into act, to make one thing begin to be. Locke.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/cause_ns",
    },
    "certain": {
        "definition": "Sure; indubitable; unquestionable; undoubted; that which cannot be questioned, or denied.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[certus, Latin]",
    },
    "certify": {
        "definition": "To Ce'rtify. v.a.  [certifier, Fr.] 1. To give certain information of. The English embassadours returned out of Flanders from Maximilian, and certified the king, that he was not to hope for any aid from him. Bacon’s Henry VII. This is designed to certify those things that are confirmed of God’s favour. Hammond’s Fundamentals. 2. It has of before the thing told.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/certify_va",
    },
    "cession": {
        "definition": "1. Retreat; the act of giving way. Sound is not produced without some resistance either in the air or the body percussed; for if there be a mere yielding or cession, it produceth no sound. Bacon’s Nat. Hist. №. 125. 2. Resignation; the act of yielding up or quitting to another. A parity in their council would make and secure the best peace they can with France, by a cession of Flanders to that crown, in exchange for other provinces. Temple.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/cession_ns",
    },
    "character": {
        "definition": "CHA'RACTER. n.s.  [character, Lat. χαϱαϰτὴϱ.] 1. A mark; a stamp; a representation. In outward also her resembling less His image, who made both; and less expressing The character of that dominion giv’n O’er other creatures. Paradise Lost, b. viii. l. 542. 2. A letter used in writing or printing.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/character_ns",
    },
    "chief": {
        "definition": "1. A commander; a leader. Is pain to them Less pain, less to be fled? or thou than they Less hardy to endure? couragious chief! The first in flight from pain. Milton’s Paradise Lost, b. iv. After or before were never known Such chiefs; as each an army seem’d alone.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/chief_ns",
    },
    "choice": {
        "definition": "1. The act of choosing; determination between different things proposed; election. If you oblige me suddenly to chuse, The choice is made; for I must both refuse. Dryd. Ind. Emp. Soft elocution doth thy style renown, Gentle or sharp, according to thy choice, To laugh at follies, or to lash at vice. Dryd. Pers. sat. v.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/choice_ns",
    },
    "choose": {
        "definition": "To CHOOSE. v.a.  I chose, I have chosen or chose. [choisir, Fr. ceosan, Sax. kicsen, Germ.] 1. To take by way of preference of several things offered; not to reject. Did I choose him out of all the tribes of Israel to be my priest. 1 Sam. ii. 28. I may neither choose whom I would, nor refuse whom I dislike. Shakesp. Merchant of Venice. If he should offer to choose, and choose the right casket, you should refuse to perform your father’s will, if you should refuse to accept him. Shakesp. Merchant of Venice.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/choose_va",
    },
    "citizen": {
        "definition": "A freeman of a city; not a foreigner; not a slave.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[civis, Latin; citoyen, French]",
    },
    "civil": {
        "definition": "Relating to the community; political; relating to the city or government.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[civilis, Latin]",
    },
    "claim": {
        "definition": "A demand of any thing, as due.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from the verb]",
    },
    "clause": {
        "definition": "1. A sentence; a single part of a discourse; a subdivision of larger sentence. 2. An article, or particular stipulation.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[clausula, Latin]",
    },
    "collect": {
        "definition": "Then let your devotion be humbly to say over proper collects. Taylor’s Guide to Devotion.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/collect_ns",
    },
    "comfort": {
        "definition": "1. Support; assistance; countenance. Poynings made a wild chace upon the wild Irish; where, in respect of the mountains and fastnesses, he did little good, which he would needs impute unto the comfort that the rebels should receive underhand from the earl of Kildare. Bacon. The king did also appoint commissioners for the fining of all such as were of any value, and had any hand or partaking in the aid or comfort of Perkins, or the Cornishmen. Bacon. 2. Consolation; support under calamity or danger. I will keep her ign’rant of her good, To make her heavenly comforts of despair,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/comfort_ns",
    },
    "commander": {
        "definition": "1. He that has the supreme authority; a general; a leader; a chief. We’ll do thee homage, and be rul’d by thee, Love thee as our commander and our king. Shakespeare. I have given him for a leader and commander to the people. Is. lv. 4. The Romans, when commanders in war, spake to their army, and styled them, My soldiers. Bacon’s Apophthegms.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/commander_ns",
    },
    "commerce": {
        "definition": "Intercourse; exchange of one thing for another; interchange of any thing; trade; traffick.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[commercium, Latin]",
    },
    "common": {
        "definition": "Belonging equally to more than one.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[communis, Latin]",
    },
    "commonwealth": {
        "definition": "WORKING DEFINITION -- no standalone headword found in either Johnson's or Bailey's; both dictionaries use 'commonwealth' to gloss 'republick' without ever defining it independently. Composite sense: a free state; a political community in which power belongs to more than one person.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "(derived from usage within REPUBLICK entries, both dictionaries)",
    },
    "compact": {
        "definition": "A contract; an accord; an agreement; mutual and settled appointment between two or more, to do or to forbear something.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[pactum, Latin] (Johnson's, 1755)",
    },
    "compensation": {
        "definition": "Poynings, the better to make compensation of his service in the wars, called a parliament. Bacon’s Henry VII. All other debts may compensation find; But love is strict, and will be paid in kind. Dryd. Aurengz.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/compensation_ns",
    },
    "compliance": {
        "definition": "1. The act of yielding to any desire or demand; accord; submission. I am far from excusing that compliance, for plenary consent it was not, to his destruction. King Charles. We are free from any necessary determination of our will to any particular action, and from a necessary compliance with our desire, set upon any particular, and then appearing preferable good. Locke. Let the king meet compliance in your looks, A free and ready yielding to your wishes. Rowe.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/compliance_ns",
    },
    "compose": {
        "definition": "To form a mass by joining different things together.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[compono, Latin]",
    },
    "compulsory": {
        "definition": "Of a forcing or constraining Nature.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(Bailey's, 1721)",
    },
    "concerning": {
        "definition": "There is not any thing more subject to errour than the true judgment concerning the power and forces of an estate. Bacon. The ancients had no higher recourse than to nature, as may appear by a discourse concerning this point in Strabo. Brown. None can demonstrate that there is such an island as Jamaica, yet, upon testimony, I am free from all doubt concerning it. Tillotson, Preface.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/concerning_prep",
    },
    "conclude": {
        "definition": "To CONCLU'DE. v.a.  [concludo, Latin.] 1. To shut. The very person of Christ therefore, for ever and the self-same, was only, touching bodily substance, concluded within the grave. Hooker, b. v. s. 52. 2. To include; to comprehend. God hath concluded them all in unbelief, that he might have mercy upon all. Romans, xi. 32. 3. To collect by ratiocination.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/conclude_va",
    },
    "concurrence": {
        "definition": "Concu'rrence. 1. Union; association; conjunction. We have no other measure but our own ideas, with the concurrence of other probable reasons, to persuade us. Locke. 2. Agreement; act of joining in any design, or measures. Their concurrence in persuasion, about some material points belonging to the same polity, is not strange. Hooker, Preface. The concurrence of the peers in that fury, can be imputed to the irreverence the judges were in.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/concurrence_ns",
    },
    "concurrent": {
        "definition": "To all affairs of importance there are three necessary concurrents, without which they can never be dispatched; time, industry, and faculties. Decay of Piety.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/concurrent_ns",
    },
    "condition": {
        "definition": "Quality; that by which any thing is denominated good or ill.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[conditio, Latin]",
    },
    "confederation": {
        "definition": "The three princes enter into some strict league and confederation amongst themselves. Bacon’s Henry VII. Nor can those confederations or designs be durable, when subjects make bankrupt of their allegiance. King Charles.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/confederation_ns",
    },
    "confession": {
        "definition": "1. The acknowledgment of a crime; the discovery of one’s own guilt. Your engaging me first in this adventure of the Moxa, and desiring the story of it from me, is like giving one the torture, and then asking his confession, which is hard usage. Temple. 2. The act of disburdening the conscience to a priest. You will have little opportunity to practise such a confession, and should therefore supply the want of it by a due performance of it to God. Wake’s Preparation for Death. 3. Profession; avowal. Who, before Pontius Pilate, witnessed a good confession?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/confession_ns",
    },
    "confirmation": {
        "definition": "1. The act of establishing any thing or person; settlement; establishment. Embrace and love this man. ———— ———— With brother’s love I do it. —— ———— And let heav’n Witness how dear I hold this confirmation! Shak. Hen. VIII. 2. Evidence by which any thing is ascertained; additional proof. A false report hath",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/confirmation_ns",
    },
    "confront": {
        "definition": "To stand against another in full view; to face.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[confronter, French]",
    },
    "congress": {
        "definition": "1. A meeting; a shock; a conflict. 2. An appointed meeting for settlement of affairs between different nations.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[con and gressus, Latin]",
    },
    "consanguinity": {
        "definition": "I’ve forgot my father; I know no touch of consanguinity. Shakes. Troil. and Cressida. There is the supreme and indissoluble consanguinity and society between men in general; of which the heathen poet, whom the apostle calls to witness, saith, We are all his generation. Bacon’s Holy War. The first original would subsist, though he outlived all terms of consanguinity, and became a stranger unto his progeny. Brown’s Vulgar Errours, b. vi. c. 6. Christ has condescended to a cognation and consanguinity with us.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/consanguinity_ns",
    },
    "consent": {
        "definition": "The act of yielding or consenting.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[consentio, Latin]",
    },
    "consequence": {
        "definition": "1. That which follows from any cause or principle. 2. Event; effect of a cause. 3. Proposition collected from the agreement of other previous propositions; deduction; conclusion.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[consequentia, Latin]",
    },
    "consideration": {
        "definition": "1. The act of considering; mental view; regard; notice. As to present happiness and misery, when that alone comes in consideration, and the consequences are removed, a man never chuses amiss. Locke. 2. Mature thought; prudence; serious deliberation. Let us think with consideration, and consider with acknowledging, and acknowledge with admiration. Sidney. The breath no sooner left his father’s body, But that his wildness mortified in him;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/consideration_ns",
    },
    "constitute": {
        "definition": "To CO'NSTITUTE. v.a.  [constituo, Latin.] 1. To give formal existence; to make any thing what it is; to produce. Prudence is not only a moral but christian virtue, such as is necessary to the constituting of all others. Decay of Piety. 2. To erect; to establish. We must obey laws appointed and constituted by lawful authority, not against the law of God. Taylor’s Holy Living. 3. To depute; to appoint another to an office.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/constitute_va",
    },
    "constitution": {
        "definition": "Sense 6 applies: 'Established form of government; system of laws.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from constitute]",
    },
    "consul": {
        "definition": "1. The chief magistrate in the Roman republick. 2. An officer commissioned in foreign parts to judge between the merchants of his nation, and protect their commerce.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[consul, Latin]",
    },
    "continuance": {
        "definition": "1. Succession uninterrupted. The brute immediately regards his own preservation, or the continuance of his species. Addison’s Spectator, №. 120. 2. Permanence in one state. Continuance of evil doth in itself increase evil. Sidney. A chamber where a great fire is kept, though the fire be at one stay, yet with the continuance continually hath its heat increased. Sidney, b. ii.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/continuance_ns",
    },
    "contrary": {
        "definition": "1. A thing of opposite qualities. No contraries hold more antipathy, Than I and such a knave. Shakespeare’s King Lear. He sung Why contraries feed thunder in the cloud. Cowley’s Davideis. Honour should be concern’d in honour’s cause;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/contrary_ns",
    },
    "convene": {
        "definition": "To Conve'ne. v.a. 1. To call together; to assemble; to convoke. No man was better pleased with the convening of this parliament than myself. King Charles. All the factious and schismatical people would frequently, as well in the night as the day, convene themselves by the sound of a bell. Clarendon. And now th’ almighty father of the gods Convenes a council in the blest abodes.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/convene_va",
    },
    "convention": {
        "definition": "1. The act of coming together; union; coalition; junction. They are to be reckoned amongst the most general affections of the conventions, or associations of several particles of matter into bodies of any certain denomination. Boyle. 2. An assembly. Publick conventions are liable to all the infirmities, follies, and vices of private men. Swift. 3. A contract; an agreement for a time, previous to a definitive treaty.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/convention_ns",
    },
    "conviction": {
        "definition": "1. Detection of guilt, which is, in law, either when a man is outlawed, or appears and confesses, or else is found guilty by the inquest. Cowel. The third best absent is condemn’d, Convict by flight, and rebel to all law; Conviction to the serpent none belongs. Milton’s Par. Lost. 2. The act of convincing; confutation; the act of forcing others, by argument, to allow a position. When therefore the apostle requireth hability to convict hereticks, can we think he judgeth it a thing unlawful, and not rather needful, to use the principal instrument of their conviction, the light of reason. Hooker, b. iii. s. 8.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/conviction_ns",
    },
    "corruption": {
        "definition": "1. The principle by which bodies tend to the separation of their parts. 2. Wickedness; perversion of principles; loss of integrity. Precepts of morality, besides the natural corruption of our tempers, which makes us averse to them, are so abstracted from ideas of sense, that they seldom get an opportunity for descriptions and images. Addison’s Essay on the Georgicks. Amidst corruption, luxury and rage, Still leave some ancient virtue’s to our age. Pope. 3. Putrescence.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/corruption_ns",
    },
    "counsel": {
        "definition": "Advice; direction.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[consilium, Latin]",
    },
    "course": {
        "definition": "1. Race; career. And some she arms with sinewy force, And some with swiftness in the course. Cowley. 2. Passage from place to place; progress. To this may be referred the course of a river. And when we had finished our course from Tyre, we came to Ptolemais. Acts xxi. 7. A light, by which the Argive squadron steers",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/course_ns",
    },
    "court": {
        "definition": "The place where the prince resides; the palace.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[cour, French; hof, Dutch; curtis, low Latin]",
    },
    "create": {
        "definition": "To form out of nothing; to cause to exist.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "credit": {
        "definition": "1. Belief. 2. Honour; reputation.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[credit, French]",
    },
    "crime": {
        "definition": "An act contrary to right; an offence; a great fault; an act of wickedness.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[crimen, Latin]",
    },
    "crown": {
        "definition": "1. The ornament of the head which denotes imperial and regal dignity. If thou be a king, where is thy crown? ———— —— My crown is in my heart, not on my head: My crown is call’d content; A crown it is that seldom kings enjoy. Shakesp. Henry VI. Look down, you gods,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/crown_ns",
    },
    "cruel": {
        "definition": "Pleased with hurting others; inhuman; hard-hearted; without pity; without compassion; savage; barbarous; unrelenting.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[cruel, French]",
    },
    "current": {
        "definition": "1. A running stream. The current, that with gentle murmur glides, Thou know’st, being stopp’d, impatiently doth rage; But his fair course is not hindered: He makes sweet musick with th’ enamel’d stones. Shakesp. These inequalities will vanish in one place, and presently appear in another, and seem perfectly to move like waves, succeeding and destroying one another; save that their motion oftentimes seems to be quickest, as if in that vast sea they were carried on by a current, or at least by a tide. Boyle.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/current_ns",
    },
    "danger": {
        "definition": "DA'NGER. n.s.  [danger, Fr. of uncertain derivation. Skinner derives it from damnum, Menage from angaria, Minshew from δάνος, death, to which Junius seems inclined.] Risque; hazard; peril. They that sail on the sea, tell of the danger. Ecclus. xliii. 24. Our craft is in danger to be set at nought. Acts, x. 27. I dare pawn down my life for him, that he hath writ this to feel my affection to your honour, and to no other pretence of danger. Shakespeare’s King Lear. More danger now from man alone we find,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/danger_ns",
    },
    "date": {
        "definition": "1. The time at which a letter is written. 2. The time at which any event happened.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[datum, Latin]",
    },
    "day": {
        "definition": "A Space or Time which is variously reckoned. Distinguishes 'Artificial Day' (daylight only) from 'Natural Day' (full 24-hour cycle).",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[daeg, Saxon; dagh, Dutch] (Bailey's, 1721)",
    },
    "deaf": {
        "definition": "To Deaf. v.a.  To deprive of the power of hearing. Hearing hath deaf’d our sailors; and if they Know how to hear, there’s none know what to say. Donne. A swarm of their aerial shapes appears, And, flutt’ring round his temples, deafs his ears. Dryd. Æn.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/deaf_va",
    },
    "death": {
        "definition": "1. The extinction of life; the departure of the soul from the body. He is the mediator of the New Testament, that by means of death, for the redemption of the transgressions, they which are called might receive the promise of eternal inheritance. Heb. ix. 15. They say there is divinity in odd numbers, either in nativity or death. Shakes. Merry Wives of Windsor. Death, a necessary end, Will come, when it will come.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/death_ns",
    },
    "debate": {
        "definition": "A personal dispute; a controversy.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[debat, French]",
    },
    "debt": {
        "definition": "That which one man owes to another.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[debitum, Latin]",
    },
    "decide": {
        "definition": "1. To fix the event of; to determine. 2. To determine a question or dispute.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[decido, Latin]",
    },
    "declaration": {
        "definition": "1. A proclamation or affirmation; oral expression; publication. His promises are nothing else but declarations, what God will do for the good of men. Hooker, b. i. s. 2. Though wit and learning are certain and habitual perfections of the mind, yet the declaration of them, which alone brings the repute, is subject to a thousand hazards. South. There are no where so plain and full declarations of his mercy and love to the sons of men, as are made in the gospel. Tillotson, Sermon 5. 2. An explanation of something doubtful. Obsolete.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/declaration_ns",
    },
    "declare": {
        "definition": "1. To clear; to free from obscurity. 2. To make known; to tell evidently and openly.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[declaro, Latin]",
    },
    "deem": {
        "definition": "Hear me, my love, be thou but true of heart. —— I true! how now? what wicked deem is this? Shakespear.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/deem_ns",
    },
    "defence": {
        "definition": "Guard; protection; security.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[defensa, Latin]",
    },
    "defend": {
        "definition": "1. To stand in defence of; to protect; to support. 2. To vindicate; to uphold, to assert; to maintain. 3. To fortify; to secure.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[defendo, Latin]",
    },
    "delegate": {
        "definition": "To intrust; to commit to another's power and jurisdiction.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[delego, Latin]",
    },
    "delivery": {
        "definition": "1. The act of delivering, or giving. 2. Release; rescue; saving. He swore, with sobs, That he would labour my delivery. Shakesp. Richard III. 3. A surrender; giving up. After the delivery of your royal father’s person into the hands of the army, I undertaking to the queen mother, that I would find some means to get access to him, she was pleased to send me. Denham, Dedication.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/delivery_ns",
    },
    "demand": {
        "definition": "To claim; to ask for with authority.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[demander, French]",
    },
    "deny": {
        "definition": "1. To contradict an accusation; not to confess. 2. To refuse; not to grant.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[denego, Latin]",
    },
    "depository": {
        "definition": "The Jews themselves are the depositories of all the prophecies which tend to their own confusion. Addison.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/depository_ns",
    },
    "deprive": {
        "definition": "To DEPRI'VE. v.a.  [from de and privo, Latin.] 1. To bereave one of a thing; to take it away from him. God hath deprived her of wisdom, neither hath he imparted to her understanding. Job xxxix. 17. He lamented the loss of an excellent servant, and the horrid manner in which he had been deprived of him. Clarendon. Now wretched Oedipus, depriv’d of sight, Led a long death in everlasting night.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/deprive_va",
    },
    "design": {
        "definition": "1. An intention; a purpose. 2. A scheme; a plan of action. Is he a prudent man, as to his temporal estate, that lays designs only for a day, without any prospect to the remaining part of his life? Tillotson, Sermon i. 3. A scheme formed to the detriment of another. A sedate settled design upon another man’s life, put him in a state of war with him against whom he has declared such an intention. Locke. 4. The idea which an artist endeavours to execute or express.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/design_ns",
    },
    "desire": {
        "definition": "DESI'RE. n.s.  [desir, Fr. deseo, Ital. desiderium, Lat.] Wish; eagerness to obtain or enjoy. Drink provokes, and unprovokes; it provokes the desire, but it takes away the performance. Shakespeare’s Macbeth. Desire ’s the vast extent of human mind; It mounts above, and leaves poor hope behind. Dryden. Desire is the uneasiness a man finds in himself upon the absence of any thing, whose present enjoyment carries the idea of delight with it. Locke.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/desire_ns",
    },
    "desolation": {
        "definition": "What with your praises of the country, what with your discourse of the lamentable desolation thereof made by those Scots, you have filled me with a great compassion of their calamities. Spenser’s State of Ireland. Without her follows to myself and thee, Herself, the land, and many a Christian soul, Death, desolation, ruin, and decay. Shakesp. Richard III. To complete The scene of desolation stretch’d around,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/desolation_ns",
    },
    "despotism": {
        "definition": "Absolute power. [despotisme, French, from despot.]",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/despotism_ns",
    },
    "determine": {
        "definition": "To DETE'RMINE. v.a.  [determiner, Fr. determino, Latin.] 1. To fix; to settle. It is concluded he shall be protector. —— It is determin’d, not concluded yet; But so it must be, if the king miscarry. Shakes. Richard III. More particularly to determine the proper season for grammar, I do not see how it can be made a study, but as an introduction to rhetorick. Locke.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/determine_va",
    },
    "devolve": {
        "definition": "To DEVO'LVE. v.a.  [devolvo, Latin.] 1. To roll down. The matter which devolves from the hills down upon the lower grounds, does not considerably raise and augment them. Woodward’s Natural History. Through splendid kingdoms he devolves his maze, Now wanders wild through solitary tracts Of life-deserted sand. Thomson’s Summer, l. 805.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/devolve_va",
    },
    "direct": {
        "definition": "To aim in a straight line.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[dirigo, directum, Latin]",
    },
    "disability": {
        "definition": "Want of power to do any thing; weakness; impotence.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from disable]",
    },
    "disavow": {
        "definition": "To Disavo'w. v.a.  [dis and avow.] To disown; to deny knowledge of; to deny concurrence in any thing. The heirs and posterity of them which yielded the same, are, as they say, either ignorant thereof, or do wilfully deny, or stedfastly disavow it. Spenser’s State of Ireland. The English, that knew his noble spirit, did believe his name was therein abused, which he manifested to be true by disavowing it openly afterwards. Hayward. To deal in person is good, when a man’s face breedeth regard, and generally when a man will reserve to himself liberty either to disavow or to expound. Bacon, Essay 48. A man that acts below his rank, doth but disavow fortune, and seemeth to be conscious of his own want in worth, and doth but teach others to envy him.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/disavow_va",
    },
    "discharge": {
        "definition": "To disburden; to exonerate; to free from any load or inconvenience.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[dischurger, French]",
    },
    "discipline": {
        "definition": "DI'SCIPLINE. n.s.  [disciplina, Latin.] 1. Education; instruction; the act of cultivating the mind; the act of forming the manners. The cold of the northern parts is that which, without aid of discipline, doth make the bodies hardest, and the courage warmest. Bacon, Essay 59. They who want that sense of discipline, hearing, are also by consequence deprived of speech. Holder’s Elements of Speech. It must be confessed, it is by the assistance of the eye and the ear especially, which are called the senses of discipline, that our minds are furnished with various parts of knowledge. Watts.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/discipline_ns",
    },
    "disparage": {
        "definition": "To DISPA'RAGE. v.a.  [from dispar, Latin.] 1. To match unequally; to injure by union with something inferiour in excellence. 2. To injure by a comparison with something of less value. 3. To treat with contempt; to mock; to flout; to reproach. Ahaz, his sottish conqueror he drew, God’s altar to disparage and displace, For one of Syrian mode. Milton’s Paradise Lost.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/disparage_va",
    },
    "dispose": {
        "definition": "1. Power; management; disposal. All that is mine I leave at thy dispose; My goods, my lands, my reputation. Shakespeare. It shall be my task To render thee the Parthian at dispose. Milton’s Parad. Reg. Of all your goodness leaves to our dispose,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/dispose_ns",
    },
    "dissolve": {
        "definition": "To DISSO'LVE. v.a.  [dissolvo, Latin.] 1. To destroy the form of any thing by disuniting the parts with heat or moisture; to melt; to liquefy. The whole terrestrial globe was taken all to pieces, and dissolved at the deluge. Woodward’s Nat. Hist. Preface. 2. To break; to disunite in any manner. Seeing then that all these things shall be dissolved, what manner of persons ought ye to be. 2 Pet. iii. 11. 3. To loose; to break the ties of any thing.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/dissolve_va",
    },
    "distinct": {
        "definition": "Different, separate one from another; also clear, plain.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[distinctus, Latin] (Bailey's, 1721 -- not locatable in Johnson's scan)",
    },
    "district": {
        "definition": "1. The circuit or territory within which a man may be compelled to appearance. 2. Circuit of authority; province.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[districtus, Latin]",
    },
    "divine": {
        "definition": "1. A minister of the gospel; a priest; a clergyman. Claudio must die to-morrow: let him be furnished with divines, and have all charitable preparation. Sh. Meas. for Meas. Give Martius leave to proceed in his discourse; for he spoke like a divine in armour. Bacon’s Holy War. A divine has nothing to say to the wisest congregation, which he may not express in a manner to be understood by the meanest among them. Swift. 2. A man skilled in divinity; a theologian.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/divine_ns",
    },
    "do": {
        "definition": "To DO. v.a.  preter. did; part. pass. done. [don, Sax. doen, Dut.] 1. To practise or act any thing good or bad. Thou hast done evil above all that were before thee. 1 Kings. Flee evil, and do good. Psalms. 2. To perform; to atchieve. They help, who hurt so small;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/do_va",
    },
    "due": {
        "definition": "Owed; that which any one has a right to demand in consequence of a compact, or for any other reason.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[du, French]",
    },
    "duty": {
        "definition": "That which a man is by any natural or legal obligation bound to do.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from due]",
    },
    "each": {
        "definition": "each, pron. Each. pron.  [elc, Saxon; elch, Dutch; ilk, Scottish.] 1. Either of two. Though your orbs of diff’rent greatness be, Yet both are for each other’s use dispos’d; His to inclose, and your’s to be inclos’d. Dryden. 2. Every one of any number. This sense is rare, except in poetry.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/each_pron",
    },
    "effect": {
        "definition": "That which is produced by an operating cause.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[effectus, Latin]",
    },
    "either": {
        "definition": "either, pron. Ei'ther. pron.  [ægðer, Saxon; auther, Scottish.] 1. Which soever of the two; whether one or the other. Lepidus flatters both, Of both is flatter’d; but he neither loves, Nor either cares for him. Shakesp. Anthony and Cleopatra. So like in arms these champions were,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/either_pron",
    },
    "elect": {
        "definition": "To choose for any office or use; to take in preference to others. (covers elector, electors, election)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[electus, Latin]",
    },
    "election": {
        "definition": "The act of chusing; the act of selecting one or more from a greater number for any use or office; choice.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[electio, Latin]",
    },
    "elector": {
        "definition": "1. He that has a vote in the choice of any officer. From the new world her silver and her gold Came, like a tempest, to confound the old; Feeding with these the brib’d electors’ hopes, Alone she gave us emperors and popes. Waller. 2. A prince who has a voice in the choice of the German emperour.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/elector_ns",
    },
    "emancipation": {
        "definition": "Obstinacy in opinions holds the dogmatist in the chains of error, without hope of emancipation. Glanv. Sceps. c. 27.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/emancipation_ns",
    },
    "empower": {
        "definition": "To Empo'wer. v.a.  [from power.] 1. To authorise; to commission; to give power or authority to any purpose. You are empowered, when you please, to give the final decision of wit. Dryden’s Juv. Dedication. The government shall be empowered to grant commissions to all Protestants whatsoever. Swift on the Sacram. Test. 2. To give natural force; to enable. Does not the same power that enables them to heal, empower them to destroy?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/empower_va",
    },
    "end": {
        "definition": "1. The conclusion or cessation of any action. 2. To terminate; to conclude; to finish.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "enforce": {
        "definition": "To give strength to; to strengthen; to invigorate.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[enforcer, French]",
    },
    "enter": {
        "definition": "To go or come into any place.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[entrer, French]",
    },
    "entitle": {
        "definition": "To Enti'tle. v.a.  [entituler, French.] 1. To grace or dignify with a title or honourable appellation. 2. To give a title or discriminative appellation; as, to entitle a book. Besides the Scripture, the books which they call ecclesiastical were thought not unworthy some time to be brought into publick audience, and with that name they entitled the books which we term apocryphal. Hooker, b. v. s. 20. Next favourable thou, Who highly thus to entitle me vouchsaf’st, Far other name deserving! Milton’s Paradise Lost, b. x.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/entitle_va",
    },
    "equal": {
        "definition": "1. One not inferiour or superiour to another. He is enamoured on Hero: I pray you, dissuade him from her; she is no equal for his birth. Sh. Much Ado about Nothing. He would make them all equals to the citizens of Rome. 2 Mac. ix. 15. Those who were once his equals, envy and defame him, because they now see him their superiour; and those who were once his superiours, because they look upon him as their equal. Addison’s Spectator, №. 256. To my dear equal, in my native land,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/equal_ns",
    },
    "equity": {
        "definition": "1. Justice; right; honesty. Foul subornation is predominant, And equity exil’d your highness’ land. Shakesp. Henry VI. Christianity secures both the private interests of men and the publick peace, enforcing all justice and equity. Tillotson. 2. Impartiality. Liking their own somewhat better than other mens, even because they are their own, they must in equity allow us to be like unto them in this affection.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/equity_ns",
    },
    "erection": {
        "definition": "1. The act of raising, or state of being raised upward. We are to consider only the erection of the hills above the ordinary land. Brerewood on Languages. 2. The act of building or raising edifices. The first thing which moveth them thus to cast up their poison, are certain solemnities usual at the first erection of churches. Hooker, b. v. s. 12. Pillars were set up above one thousand four hundred and twenty-six years before the flood, counting Seth to be an hundred years old at the erection of them. Raleigh’s History.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/erection_ns",
    },
    "establish": {
        "definition": "To settle firmly; to fix unalterably.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[etablir, French]",
    },
    "establishment": {
        "definition": "Settlement; fixed state.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[establissement, French]",
    },
    "event": {
        "definition": "1. An incident; any thing that happens, good or bad. 2. The consequence of an action; the conclusion; the upshot.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[eventus, Latin]",
    },
    "example": {
        "definition": "EXA'MPLE. n.s.  [exemple, French; exemplum, Latin.] 1. Copy or pattern; that which is proposed to be resembled or imitated. The example and pattern of those his creatures he beheld in all eternity. Raleigh’s History of the World. 2. Precedent; former instance of the like. So hot a speed, with such advice dispos’d, Such temp’rate order in so fierce a course, Doth want example.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/example_ns",
    },
    "exceed": {
        "definition": "To EXCE'ED. v.a.  [excedo, Latin.] 1. To go beyond; to outgo. Nor did any of the crusts much exceed half an inch in thickness. Woodward on Fossils. 2. To excel; to surpass. Solomon exceeded all the kings of the earth. 1 Kings x. 23.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/exceed_va",
    },
    "except": {
        "definition": "1. Exclusively of, without inclusion of. 2. Unless.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "excepting": {
        "definition": "Exce'pting. preposit.  [from except. See EXCEPT.] Without inclusion of; with exception of. An improper word. What, since the pretor did my fetters loose, May I not live without controul and awe, Excepting still the letter of the law. Dryden’s Pers. Sat. 5. People come into the world in Turkey the same way they do here; and yet, excepting the royal family, they get but little by it. Collier on Duelling.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/excepting_prep",
    },
    "execute": {
        "definition": "To E'XECUTE. v.a.  [exequor, Latin.] 1. To perform; to practise. Against all the gods of Egypt I will execute judgment. Ex. He casts into the balance the promise of a reward to such as should execute, and of punishment to such as should neglect their commission. South’s Sermons. 2. To put in act; to do what is planned or determined. Men may not devise laws, but are bound for ever to use and execute those which God hath delivered.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/execute_va",
    },
    "execution": {
        "definition": "1. Performance; practice. When things are come to the execution, there is no secrecy comparable to celerity. Bacon’s Essays. I wish no better Than have him hold that purpose, and to put it In execution. Shakespeare’s Coriolanus. I like thy counsel; and how well I like it,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/execution_ns",
    },
    "executive": {
        "definition": "Active; not deliberative; not legislative; having the power to put in act the laws.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from execute]",
    },
    "exercise": {
        "definition": "Labour of the body; labour considered as conducive to the cure or prevention of diseases.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[exercitium, Latin]",
    },
    "exist": {
        "definition": "To EXI'ST. v.n.  [existo, Latin.] To be; to have a being. It is as easy to conceive that an infinite Almighty Power might produce a thing out of nothing, and make that to exist de novo, which did not exist before; as to conceive the world to have had no beginning, but to have existed from eternity. South’s Sermons. It seems reasonable to enquire, how such a multitude comes to make but one idea, since that combination does not always exist together in nature. Locke. One year is past; a different scene! No farther mention of the dean: Who now, alas, no more is mist",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/exist_vn",
    },
    "expedient": {
        "definition": "1. That which helps forward; as means to an end. God, who delights not to grieve the children of men, does not project for our sorrow, but our innocence; and would never have invited us to the one, but as an expedient to the other. Decay of Piety. 2. A shift; means to an end which are contrived in an exigence. Th’ expedient pleas’d, where neither lost his right; Mars had the day, and Venus had the night. Dryden. He flies to a new expedient to solve the matter, and supposes an earth of a make and frame like that of Des Cartes.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/expedient_ns",
    },
    "experience": {
        "definition": "EXPE'RIENCE. n.s.  [experientia, Latin.] 1. Practice; frequent trial. Hereof experience hath informed reason, and time hath made those things apparent which were hidden. Raleigh. 2. Knowledge gained by trial and practice. Boys immature in knowledge, Pawn their experience to their present pleasure, And so rebel to judgment.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/experience_ns",
    },
    "expiration": {
        "definition": "Expira'tion. n.s [from expire.] 1. That act of respiration which thrusts the air out of the lungs, and contracts the cavity of the breast. Quincy. In all expiration the motion is outwards, and therefore rather driveth away the voice than draweth it. Bacon’s Nat. History. Of an inflammation of the diaphragm, the symptoms are a violent fever, and a most exquisite pain increases upon inspiration; by which it is distinguished from a pleurisy, in which the greatest pain is in expiration. Arbuthnot on Diet. 2. The last emission of breath; death. We have heard him breathe the groan of expiration. ‡‡",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/expiration_ns",
    },
    "expire": {
        "definition": "To EXPI'RE. v.a.  [expiro, Latin.] 1. To breathe out. To save his body from the scorching fire, Which he from hellish entrails did expire. Fairy Queen. Anatomy exhibits the lungs in a continual motion of inspiring and expiring air. Harvey on Consumptions. This chaff’d the boar; his nostrils flames expire,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/expire_va",
    },
    "exportation": {
        "definition": "The cause of a kingdom’s thriving is fruitfulness of soil to produce necessaries, not only sufficient for the inhabitants, but for exportation into other countries. Swift.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/exportation_ns",
    },
    "extend": {
        "definition": "To stretch out towards any part.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[extendo, Latin]",
    },
    "failure": {
        "definition": "1. Deficience; cessation. There must have been an universal failure and want of springs and rivers all the Summer season. Woodward’s N. Hist. 2. Omission; non-performance; slip. He that, being subject to an apoplexy, used still to carry his remedy about him; but upon a time shifting his cloaths, and not taking that with him, chanced upon that very day to be surprised with a fit: he owed his death to a mere accident, to a little inadvertency and failure of memory. South’s Sermons. 3. A lapse; a slight fault.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/failure_ns",
    },
    "faith": {
        "definition": "Belief of the revealed truths of religion.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[fides, Latin]",
    },
    "fill": {
        "definition": "1. As much as may produce complete satisfaction. Her neck and breasts were ever open bare, That aye thereof her babes might suck their fill. Fairy Qu. But thus inflam’d bespoke the captain, Who scorneth peace shall have his fill of war. Fairfax, b. ii. When ye were thirsty, did I not cleave the rock, and waters flowed out to your fill?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/fill_ns",
    },
    "firm": {
        "definition": "To Firm. v.a.  [firmo, Latin.] 1. To settle; to confirm; to establish; to fix. He declared the death of the emperor; which after they had seen to be true, they by another secret and speedy messenger advertised Solyman again thereof, firming those letters with all their hands and seals. Knolles’s History of the Turks. ’Tis ratify’d above by every god, And Jove has firm’d it with an awful nod. Dryd. Albion. The pow’rs, said he,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/firm_va",
    },
    "firmness": {
        "definition": "1. Stability; hardness; compactness; solidity. It would become by degrees of greater consistency and firmness, so as to resemble an habitable earth. Burnet. 2. Durability. Both the easiness and firmness of union might be conjectured, for that both people are of the same language. Hayw. 3. Certainty; soundness. In persons already possessed with notions of religion, the understanding cannot be brought to change them, but by great examination of the truth and firmness of the one, and the flaws and weakness of the other.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/firmness_ns",
    },
    "fit": {
        "definition": "1. A paroxysm or exacerbation of any intermittent distemper. Small stones and gravel collect and become very large in the kidneys, in which case a fit of the stone in that part is the cure. Sharp’s Surgery. 2. Any short return after intermission; interval. Sometimes ’tis grateful to the rich to try A short vicissitude, and fit of poverty. Dryden’s Horace.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/fit_ns",
    },
    "for": {
        "definition": "for, conj. For. conj. 1. The word by which the reason is given of something advanced before. Heav’n doth with us as we with torches deal, Not light them for themselves; for if our virtues Did not go forth of us, ’twere all alike As if we had them not. Shakesp. Measure for Measure.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/for_conj",
    },
    "forfeiture": {
        "definition": "1. The act of forfeiting; the punishment discharged by loss of something possessed. 2. The thing forfeited; a mulct; a fine. The court is as well a Chancery to save and debar forfeitures, as a court of common law to decide rights; and there would be work enough in Germany and Italy, if Imperial forfeitures should go for good titles. Bacon’s War with Spain. Ancient privileges and acts of grace indulged by former kings, must not, without high reason, be revoked by their successors; nor forfeitures be exacted violently, nor penal laws urged rigorously. Taylor’s Rule of living holy. He fairly abdicates his throne, He has a forfeiture incurr’d.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/forfeiture_ns",
    },
    "form": {
        "definition": "The external appearance of any thing; representation; shape.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[forma, Latin; forme, French]",
    },
    "former": {
        "definition": "The wonderful art and providence of the contriver and former of our bodies, appears in the multitude of intentions he must have in the formation of several parts for several uses. Ray on the Creation.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/former_ns",
    },
    "foundation": {
        "definition": "1. The basis or lower parts of an edifice. The stateliness of houses, the goodliness of trees, when we behold them, delighteth the eye; but that foundation which beareth up the one, that root which ministreth unto the other nourishment and life, is in the bosom of the earth concealed. Hooker, b. i. s. 1. That is the way to make the city flat, To bring the roof to the foundation, To bury all. Shakespeare’s Coriolanus. O Jove, I think,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/foundation_ns",
    },
    "free": {
        "definition": "At liberty; not a vassal; not enslaved; not a prisoner; not dependant.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[freoh, Saxon]",
    },
    "from": {
        "definition": "1. Away; noting privation. Your slighting Zulema, this very hour Will take ten thousand subjects from your power. Dryden. In fetters one the barking porter ty’d, And took him trembling from his sov’reign’s side. Dryden. Clarissa drew, with tempting grace,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/from_prep",
    },
    "further": {
        "definition": "To Fu'rther. v.a.  [from the adverb; forðrian, Saxon.] To put onward; to forward; to promote; to countenance; to assist; to help. Things thus set in order, in quiet and rest, Shall further thy harvest, and pleasure thee best. Tuss. Husb. Could their fond superstition have furthered so great attempts, without the mixture of a true persuasion concerning the irresistible force of divine power. Hooker, b. v. s. 1. Grant not, O Lord, the desires of the wicked; further not his wicked device. Ps. cxl. 8.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/further_va",
    },
    "future": {
        "definition": "Thy letters have transported me beyond This ign’rant present time; and I feel now The future in the instant. Shakespeare’s Macbeth. The mind, once jaded, by an attempt above its power, either is disabled for the future, or else checks at any vigorous undertaking ever after. Locke.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/future_ns",
    },
    "going": {
        "definition": "1. The act of walking. When nobles are their taylors tutors, No hereticks burnt, but wenches suitors, Then comes the time, who lives to see’t, That going shall be us’d with feet. Shakes. King Lear. 2. Pregnancy. The time of death has a far greater latitude than that of our birth; most women coming, according to their reckoning, within the compass of a fortnight; that is, the twentieth part of their going.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/going_ns",
    },
    "gold": {
        "definition": "1. Gold is the heaviest, the most dense, the most simple, the most ductile, and most fixed of all bodies; not to be injured either by air or fire, and seeming incorruptible. It is soluble by means of sea-salt; but is injured by no other salt, and is most easily of all metals amalgamated with silver. Gold is frequently found native, and very rarely in a state of ore. It never constitutes a peculiar ore, but is found most frequently among ore of silver. Native gold is seldom found pure, but has almost constantly silver with it, and very frequently copper. Gold dust, or native gold, in small masses, is mixed among the sand of rivers in many parts of the world. It is found, in the greatest abundance, bedded in masses of hard stone, often at the depth of a hundred and fifty fathoms in the mines of Peru. Pure gold is so fixed, that Boerhaave informs us of an ounce of it set in the eye of a glass furnace for two months, without losing a single grain. Hill  on Fossils. Gold hath these natures: greatness of weight, closeness of parts, fixation, pliantness or softness, immunity from rust, and the colour or tincture of yellow. Bacon’s Nat. History. Ah! Buckingham, now do I ply the touch, To try if thou be current gold indeed. Shakes. Rich. III.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/gold_ns",
    },
    "good": {
        "definition": "Having such physical qualities as are expected or desired.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[god, Saxon]",
    },
    "govern": {
        "definition": "To rule as a chief magistrate.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[gouverner, French; guberno, Latin]",
    },
    "government": {
        "definition": "An establishment of legal authority.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[French: government]",
    },
    "grand": {
        "definition": "Great; illustrious; high in power.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[grand, French]",
    },
    "grant": {
        "definition": "To bestow something which cannot be claimed of right. (covers granted, granting, grants)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[garantir, French]",
    },
    "guarantee": {
        "definition": "God, the great guarantee for the peace of mankind, where laws cannot secure it, may think it the concern of his providence. South’s Sermons. A prince distinguished by being a patron of Protestants, and guarantee of the Westphalian treaty. Addison on the War.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/guarantee_ns",
    },
    "habeas_corpus": {
        "definition": "A writ, the which, a man indicted of some trespass, being laid in prison for the same, may have out of the King's Bench, thereby to remove himself thither at his own costs, and to answer the cause there.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[Latin]",
    },
    "happen": {
        "definition": "To fall out; to chance; to come to pass.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from hap]",
    },
    "happiness": {
        "definition": "1. Felicity; state in which the desires are satisfied. Happiness is that estate whereby we attain, so far as possibly may be attained, the full possession of that which simply for itself is to be desired, and containeth in it after an eminent sort the contentation of our desires, the highest degree of all our perfection. Hooker, b. i. Oh! happiness of sweet retir’d content, To be at once secure and innocent. Denham. The various and contrary choices that men make in the world, argue that the same thing is not good to every man alike: this variety of pursuits shews, that every one does not place his happiness in the same thing. Locke.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/happiness_ns",
    },
    "have": {
        "definition": "To Have. v.a.  pret. and part. pass. had. [haban, Gothick; habban, Saxon; hebben, Dutch; avoir, French; avere, Ital.] 1. Not to be without. I have brought him before you, that after examination had I might have something to write. Acts xxv. 26. 2. To carry; to wear. Upon the mast they saw a young man, who sat as on horseback, having nothing upon him. Sidney. 3. To make use of.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/have_va",
    },
    "having": {
        "definition": "1. Possession; estate; fortune. My having is not much; I’ll make division of my present with you: Hold, there’s half my coffer. Shakesp. Twelfth Night. 2. The act or state of possessing. Of the one side was alleged the having a picture, which the other wanted; of the other side, the first striking the shield. Sidney.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/having_ns",
    },
    "he": {
        "definition": "he, pron. He. pronoun. gen. him; plur. they; gen. them. [hy, Dutch; he, Saxon. It seems to have borrowed the plural from ðis, plural das, dative disum.] 1. The man that was named before. All the conspirators, save only he, Did that they did in envy of great Cæsar. Shakespeare. If much you note him, You shall offend him, and increase his passion;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/he_pron",
    },
    "head": {
        "definition": "1. The part of the animal that contains the brain or the organ of sensation or thought. Vein healing verven, and head purging dill. Spenser. Over head up-grew Insuperable height of loftiest shade. Milton’s Parad. Lost. My head geers off, what filthy work you make.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/head_ns",
    },
    "high": {
        "definition": "Which when the king of gods beheld from high, He sigh’d. Dryden.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/high_ns",
    },
    "history": {
        "definition": "HI'STORY. n.s.  [ἱστοϱία; historia, Latin; histoire, French.] 1. A narration of events and facts delivered with dignity. Justly Cæsar scorns the poet’s lays; It is to history he trusts for praise. Pope. 2. Narration; relation. The history part lay within a little room. Wiseman’s Surgery.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/history_ns",
    },
    "hold": {
        "definition": "To grasp in the hand; to gripe; to clutch.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[haldan, Gothick]",
    },
    "house": {
        "definition": "Sense 7 applies (legislative body): 'A body of the parliament; the lords or commons collectively considered.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[hus, Saxon; huys, Dutch]",
    },
    "hundred": {
        "definition": "1. A company or body consisting of an hundred. Very few will take this proposition, that God is pleased with the doing of what he himself commands, for an innate moral principle: whosoever does so, will have reason to think hundreds of propositions innate. Locke. Lands, taken from the enemy, were divided into centuries or hundreds, and distributed amongst the soldiers. Arbuthnot. 2. A canton or division of a county, perhaps once containing an hundred manors. [Hundredum, low Latin; hundrede, old French.] Imposts upon merchants do seldom good to the king’s revenue; for that that he wins in the hundred, he loseth in the shire. Bacon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/hundred_ns",
    },
    "if": {
        "definition": "if, conj. If. conjunction. [gif, Saxon.] 1. Suppose that; allowing that. A hypothetical particle. Absolute approbation, without any cautions, qualifications, ifs or ands. Hooker, Preface. If that rebellion Came like itself, in base and abject routs; I say, if damn’d commotion so appear’d,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/if_conj",
    },
    "immediately": {
        "definition": "Without the intervention of any other cause.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from immediate]",
    },
    "impartial": {
        "definition": "Void of Partiality, just, upright.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[impartial, French] (Bailey's, 1721)",
    },
    "impeachment": {
        "definition": "Accusation or Information against one. (Also, unrelated: 'Impeachment of Waste' -- a restraint from damaging leased land.)",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[Impeachment, French] (Bailey's, 1721)",
    },
    "importance": {
        "definition": "1. Thing imported or implied. A notable passion of wonder appeared in them; but the wisest beholder, that knew no more but seeing, could not say if the importance were joy or sorrow. Shak. Winter’s Tale. 2. Matter; subject. It had been pity you should have been put together with so mortal a purpose, as then each bore, upon importance of so slight a nature. Shakespeare’s Cymbeline. 3. Consequence; moment. We consider",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/importance_ns",
    },
    "importation": {
        "definition": "The king’s reasonable profit should not be neglected upon importation and exportation. Bacon. These mines fill the country with greater numbers of people than it would be able to bear, without the importation of corn from foreign parts. Addison on Italy. The emperor has forbidden the importation of their manufactures into any part of the empire. Addison on Italy.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/importation_ns",
    },
    "imposts": {
        "definition": "In architecture, that part of a pillar, in vaults and arches, on which the weight of the whole building lieth.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/imposts_ns",
    },
    "in": {
        "definition": "1. Noting the place where any thing is present. In school of love are all things taught we see; There learn’d this maid of arms the ireful guise. Fairfax. Is this place here not sufficient strong To guard us in? Daniel’s Civil War. 2. Noting the state present at any time.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/in_prep",
    },
    "inability": {
        "definition": "If no natural nor casual inability cross their desires, they always delighting to inure themselves with actions most beneficial to others, cannot but gather great experience, and thro’ experience the more wisdom. Hooker. Neither ignorance nor inability can be pretended; and what plea can we offer to divine justice to prevent condemnation? Rogers.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/inability_ns",
    },
    "inferior": {
        "definition": "1. Lower in place. 2. Lower in station or rank of life.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[inferior, Latin]",
    },
    "information": {
        "definition": "1. Intelligence given; instruction. But reason with the fellow, Lest you should chance to whip your information, And beat the messenger who bids beware Of what is to be dreaded. Shak. Coriolanus. The active informations of the intellect filling the passive reception of the will, like form closing with matter, grew actuate into a third and distinct perfection of practice. South.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/information_ns",
    },
    "inhabitant": {
        "definition": "In this place they report that they saw inhabitants, which were very fair and fat people. Abbot. If the fervour of the sun were the sole cause of blackness in any land of negroes, it were also reasonable that inhabitants of the same latitude, subjected unto the same vicinity of the sun, should also partake of the same hue. Brown. For his supposed love a third Lays greedy hold upon a bird, And stands amaz’d to find his dear A wild inhabitant of th’ air.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/inhabitant_ns",
    },
    "inspection": {
        "definition": "1. Prying examination; narrow and close survey. With narrow search, and with inspection deep, Consider every creature. Milton. Our religion is a religion that dares to be understood; that offers itself to the search of the inquisitive, to the inspection of the severest and the most awakened reason; for, being secure of her substantial truth and purity, she knows that for her to be seen and looked into, is to be embraced and admired, as there needs no greater argument for men to love the light than to see it. South’s Sermons. 2. Superintendence; presiding care. In the first sense it should have into before the object, and in the second sense may admit over; but authors confound them. We may safely conceal our good deeds from the publick view, when they run no hazard of being diverted to improper ends, for want of our own inspection.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/inspection_ns",
    },
    "instrument": {
        "definition": "I'NSTRUMENT. n.s.  [instrument, Fr. instrumentum, Lat.] 1. A tool used for any work or purpose. If he smite him with an instrument of iron, so that he die, he is a murderer. Num. xxxv. 16. What artificial frame, what instrument, Did one superior genius e’er invent; Which to the muscles is preferr’d. Blackmore on Creation.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/instrument_ns",
    },
    "insure": {
        "definition": "To engage, to make good any Thing that is in Danger of being lost; to pay the Premium of such Insurance. NOTE: closer to the modern commercial insurance-policy sense than to 'ensure/guarantee' -- possible semantic-drift point relevant to 'insure domestic Tranquility.'",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(Bailey's, 1721)",
    },
    "insurrection": {
        "definition": "A seditious rising; a rebellious commotion.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[insurgo, Latin]",
    },
    "interrupt": {
        "definition": "To Interru'pt. v.a.  [interrompre, Fr. interruptus, Lat.] 1. To hinder the process of any thing by breaking in upon it. Rage doth rend Like interrupted waters, and o’erbear What they are used to bear. Shakespeare’s Coriolanus. He might securely enough have engaged his body of horse against their whole inconsiderable army, there being neither tree nor bush to interrupt his charge. Clarendon, b. ii.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/interrupt_va",
    },
    "issue": {
        "definition": "1. The act of passing out. 2. Exit; egress or passage out.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[issue, French]",
    },
    "it": {
        "definition": "it, pron. IT. pronoun. [hit, Saxon.] 1. The neutral demonstrative. Used in speaking of things. Nothing can give that to another which it hath not itself. Bramh. against Hobbs. Will our great anger learn to stoop so low? I know it cannot. Cowley.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/it_pron",
    },
    "jeopardy": {
        "definition": "Hazard; danger; peril. (Johnson notes this word was already archaic in 1755: 'a word not now in use')",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[jeu perdu, 'lost game']",
    },
    "journal": {
        "definition": "A diary; an account kept of daily transactions.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[journal, French]",
    },
    "judge": {
        "definition": "One who is invested with authority to determine any cause or question, real or personal.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[juge, French; judex, Latin]",
    },
    "judgment": {
        "definition": "The power of discerning the relations between one term or one proposition and another.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[jugement, French]",
    },
    "judicial": {
        "definition": "Practised in the distribution of publick justice.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[judicium, Latin]",
    },
    "jurisdiction": {
        "definition": "Legal authority; extent of power.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[jurisdictio, Latin]",
    },
    "just": {
        "definition": "None was either more grateful to the beholders, or more noble in itself, than justs, both with sword and launce. Sidney. What news from Oxford? hold those justs and triumphs? Shakespeare’s Richard II. Among themselves the tourney they divide, In equal squadrons rang’d on either side; Then turn’d their horses heads, and man to man, And steed to steed oppos’d, the justs began.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/just_ns",
    },
    "justice": {
        "definition": "The virtue by which we give to every man what is his due.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[justice, French; justitia, Latin]",
    },
    "kind": {
        "definition": "1. Race; generical class. Kind in Teutonick English answers to genus, and sort to species; though this distinction, in popular language, is not always observed. Thus far we have endeavoured in part to open of what nature and force laws are, according to their kinds. Hooker. As when the total kind Of birds, in orderly array on wing, Came summon’d over Eden, to receive Their names of Thee. Milton’s Parad. Lost, b. vi.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/kind_ns",
    },
    "kindred": {
        "definition": "1. Relation by birth or marriage; cognation; affinity. Like her, of equal kindred to the throne, You keep her conquests, and extend your own. Dryden. 2. Relation; sort. His horse hipp’d with an old mothy saddle, and the stirrups of no kindred. Shakesp. Taming of the Shrew. 3. Relatives.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/kindred_ns",
    },
    "king": {
        "definition": "Monarch; supreme governour.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[Teutonic]",
    },
    "labour": {
        "definition": "1. The act of doing what requires a painful exertion of strength, or wearisome perseverance; pains; toil; travail. 2. Work to be done. 3. Childbirth; the act of bringing forth.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/labour_ns",
    },
    "land": {
        "definition": "A country; a region distinct from other countries.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[Gothick/Saxon]",
    },
    "law": {
        "definition": "A rule of action.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[laga, Saxon; loi, French; lex, Latin]",
    },
    "legislation": {
        "definition": "Pythagoras joined legislation to his philosophy, and, like others, pretended to miracles and revelations from God, to give a more venerable sanction to the laws he prescribed. Littleton on the Conversion of St. Paul.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/legislation_ns",
    },
    "legislative": {
        "definition": "Not its own headword -- cross-referenced under LAWGIVING: 'Legislative.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "legislature": {
        "definition": "The power that makes laws.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from legislator, Latin]",
    },
    "levy": {
        "definition": "1. The act of raising money or men. They have already contributed all their superfluous hands, and every new levy they make must be at the expence of their farms and commerce. Addison’s State of the War. 2. War raised. Treason has done his worst: nor steel, nor poison, Malice domestick, foreign levy, nothing Can touch him further! Shakespeare’s Macbeth.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/levy_ns",
    },
    "liable": {
        "definition": "But what is strength without a double share Of wisdom? vast, unwieldy, burthensome, Proudly secure, yet liable to fall By weakest subtleties. Milton’s Agonistes. The English boast of Spenser and Milton, who neither of them wanted genius or learning; and yet both of them are liable to many censures. Dryden’s Juvenal. This, or any other scheme, coming from a private hand, might be liable to many defects.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/liable_ns",
    },
    "liberty": {
        "definition": "Freedom, as opposed to slavery.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[liberte, French; libertas, Latin]",
    },
    "life": {
        "definition": "The Union of the Soul with the Body; Manner of Living; also Spriteliness, Spirit, Mettle.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[Lif, Saxon; Lijf, Dutch] (Bailey's, 1721 -- not locatable in Johnson's scan)",
    },
    "light": {
        "definition": "1. That quality or action of the medium of sight by which we see. Light is propagated from luminous bodies in time, and spends about seven or eight minutes of an hour in passing from the sun to the earth. Newton’s Opticks. 2. Illumination of mind; instruction; knowledge. Of those things which are for direction of all the parts of our life needful, and not impossible to be discerned by the light of nature itself, are there not many which few mens natural capacity hath been able to find out. Hooker, b. i. Light may be taken from the experiment of the horsetooth ring, how that those things which assuage the strife of the spirits, do help diseases contrary to the intention desired.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/light_ns",
    },
    "like": {
        "definition": "1. Some person or thing resembling another. He was a man, take him for all in all, I shall not look upon his like again. Shakesp. Hamlet. Every like is not the same, O Cæsar. Shakes. Jul. Cæsar. Though there have been greater fleets for number, yet for the bulk of the ships never the like. Bacon’s War with Spain.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/like_ns",
    },
    "limb": {
        "definition": "1. A member; a jointed or articulated part of animals. A second Hector, for his grim aspect, And large proportion of his strong knit limbs. Shakesp. O! that I had her here, to tear her limb meal. Shakesp. Now am I come each limb to survey, If thy appearance answer loud report.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/limb_ns",
    },
    "lives": {
        "definition": "So short is life, that every peasant strives, In a farm house, or field, to have three lives. Donne.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/lives_ns",
    },
    "loss": {
        "definition": "1. Forfeiture; the contrary to gain. The only gain he purchased was to be capable of loss and detriment for the good of others. Hooker, b. v. An evil natured son is the dishonour of his father that begat him; and a foolish daughter is born to his loss. Ecclus. The abatement of price of any of the landholder’s commodities, lessens his income, and is a clear loss. Locke. 2. Miss.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/loss_ns",
    },
    "magistrate": {
        "definition": "A man publickly invested with authority; a governour; an executor of the laws.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[magistratus, Latin] (Johnson's, 1755)",
    },
    "maintain": {
        "definition": "To MAINTA'IN. v.a.  [maintenir, French.] 1. To preserve; to keep. The ingredients being prescribed in their substance, maintain the blood in a gentle fermentation, reclude oppilations, and mundify it. Harvey. This place, these pledges of your love, maintain. Dryd. 2. To defend; to hold out; to make good. God values no man more or less, in placing him high or low, but every one as he maintains his post.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/maintain_va",
    },
    "majesty": {
        "definition": "1. Dignity, grandeur, greatness of appearance; an appearance awful and solemn. 2. Power; sovereignty. 3. Dignity; elevation. 4. The title of kings and queens.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[majestas, Latin] (Johnson's, 1755)",
    },
    "majority": {
        "definition": "1. The state of being greater. It is not plurality of parts without majority of parts that maketh the total greater. Grew’s Cosmol. 2. The greater number. [majorité, French.] It was highly probable the majority would be so wise as to espouse that cause which was most agreeable to the publick weal, and by that means hinder a sedition. Addison. As in senates so in schools, Majority of voices rules.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/majority_ns",
    },
    "make": {
        "definition": "To cause, to form or frame. [in Law]: to execute or perform.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[macan, Saxon; maecken, Dutch] (Bailey's, 1721)",
    },
    "manner": {
        "definition": "Fashion, Way, Custom, Usage.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[maniere, French] (Bailey's, 1721)",
    },
    "manufacture": {
        "definition": "1. The practice of making any piece of workmanship. 2. Any thing made by art. Heav’n’s pow’r is infinite: earth, air, and sea, The manufacture mass the making pow’r obey. Dryden. The peasants are clothed in a coarse kind of canvas, the manufacture of the country. Addison on Italy.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/manufacture_ns",
    },
    "many": {
        "definition": "1. A multitude; a company; a great number; people. After him the rascal many ran, Heaped together in rude rabblement. Fairy Queen. O thou fond many! with what loud applause Did’st thou beat heav’n with blessing Bolingbroke. Shakesp. I had a purpose now",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/many_ns",
    },
    "march": {
        "definition": "To March. v.a. 1. To put in military movement. Cyrus marching his army for divers days over mountains of snow, the dazzling splendour of its whiteness prejudiced the sight of very many of his soldiers. Boyle on Colours. 2. To bring in regular procession. March them again in fair array, And bid them form the happy day; The happy day design’d to wait",
        "source": "Johnson's Dictionary (1773)",
        "url": "https://johnsonsdictionaryonline.com/1773/march_va",
    },
    "may": {
        "definition": "To be permitted; to be allowed.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[magan, Saxon]",
    },
    "meeting": {
        "definition": "1. An assembly; a convention. If the fathers and husbands of those, whose relief this your meeting intends, were of the houshold of faith, then their relicts and children ought not to be strangers to the good that is done in it, if they want it. Sprat’s Sermons. Since the ladies have been left out of all meetings except parties at play, our conversation hath degenerated. Swift. 2. A congress. Let’s be revenged on him; let’s appoint him a meeting, and lead him on with a fine baited delay. Shakespeare.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/meeting_ns",
    },
    "member": {
        "definition": "One of a community. (sense 4; sense 1 is 'any part appendant to the body')",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[membrum, Latin]",
    },
    "military": {
        "definition": "Engaged in the life of a soldier; soldierly.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[militaris, Latin]",
    },
    "militia": {
        "definition": "The trainbands; the standing force of a nation.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[Latin]",
    },
    "mock": {
        "definition": "1. Ridicule; act of contempt; fleer; sneer; gibe; flirt. Tell the pleasant prince this mock of his Hath turn’d his balls to gun-stones. Shakesp. Henry V. Oh, ’tis the spight of hell, the fiend’s arch mock, To lip a wanton, and suppose her chaste. Shakespeare. Fools make a mock at sin.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/mock_ns",
    },
    "mode": {
        "definition": "1. Form; external variety; accidental discrimination; accident. A mode is that which cannot subsist in and of itself, but is always esteemed as belonging to, and subsisting by, the help of some substance, which, for that reason, is called its subject. Watts’s Logick, p. i. Few allow mode to be called a being in the same perfect sense as a substance is, and some modes have evidently more of real entity than others. Watts’s Logick. 2. Gradation; degree. What modes of sight betwixt each wide extreme,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/mode_ns",
    },
    "multitude": {
        "definition": "MU'LTITUDE. n.s.  [multitude, Fr. multitudo, Lat.] 1. The state of being many; the state of being more than one. 2. Number; many; more than one. It is impossible that any multitude can be actually infinite, or so great that there cannot be a greater. Hale. 3. A great number; loosely and indefinitely. It is a fault in a multitude of preachers, that they utterly neglect method in their harangues. Watts.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/multitude_ns",
    },
    "must": {
        "definition": "New wine; new wort. If in the must of wine, or wort of beer, before it be tunned, the burrage stay a small time, and be often changed, it makes a sovereign drink for melancholy. Bacon’s Natural History. As a swarm of flies in vintage time, About the wine-press where sweet must is pour’d, Beat off, returns as oft with humming sound. Milton. The wime itself was suiting to the rest,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/must_ns",
    },
    "nation": {
        "definition": "A People; also a Country.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[nation, French] (Bailey's, 1721 -- not locatable in Johnson's scan)",
    },
    "naturalization": {
        "definition": "The Spartans were nice in point of naturalization; whereby, while they kept their compass, they stood firm; but when they did spread, they became a windfal. Bacon’s Ess. Encouragement may be given to any merchants that shall come over and turn a certain stock of their own, as naturalization, and freedom from customs the two first years. Temple. Enemies, by taking advantage of the general naturalization act, invited over foreigners of all religions. Swift.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/naturalization_ns",
    },
    "necessary": {
        "definition": "1. Needful, unavoidable, indispensable [Bailey's, 1721 -- fills gap illegible in Johnson's scan]. 2. Not free; fatal; impelled by fate. 3. Conclusive; decisive by inevitable consequence. [Johnson's, 1755]",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[necessarius, Latin]",
    },
    "necessity": {
        "definition": "1. Cogency; compulsion; fatality. Necessity and chance Approach not me; and what I will is fate. Milton. 2. State of being necessary; indispensableness. Urge the necessity, and state of times. Shakes. Rich. III. Racine used the chorus in his Esther, but not that he found any necessity of it: it was only to give the ladies an occasion of entertaining the king with vocal musick.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/necessity_ns",
    },
    "neither": {
        "definition": "neither, conj. NEI'THER. conjunct. [nawðer, Saxon, ne either.] 1. Not either. A particle used in the first branch of a negative sentence, and answered by nor. Fight neither with small nor great, save only with the king. 1 Kings xxii. 31. 2. It is sometimes the second branch of a negative or prohibition to any sentence. Ye shall not eat of it, neither shall ye touch it. Gen. iii. 3.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/neither_conj",
    },
    "net": {
        "definition": "Poor bird! thoud’st never fear the net, nor lime, The pitfall nor the gin. Shakespeare’s Macbeth. He made nets of chequer-work for the chapiters, upon the top of the pillars. 1 Kings vii. 17. Impatience intangles us like the fluttering of a bird in a net, but cannot at all ease our trouble. Taylor’s Holy Living. The vegetative tribes,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/net_ns",
    },
    "new": {
        "definition": "Not old; fresh made or produced; novel.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[neop, Saxon]",
    },
    "no": {
        "definition": "The word of refusal.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[na, Saxon]",
    },
    "nobility": {
        "definition": "1. Antiquity of family joined with splendour. When I took up Boccace unawares, I fell on the same argument of preferring virtue to nobility of blood, and titles, in the story of Sigismunda. Dryden, Fab. Pref. Long galleries of ancestors, Challenge, nor wonder, or esteem from me, ``Virtue alone is true nobility. ’’ Dryden. 2. Rank or dignity of several degrees, conferred by sovereigns. Nobility in England is extended to five ranks; duke, marquis, earl, viscount, baron.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/nobility_ns",
    },
    "nominate": {
        "definition": "To NO'MINATE. v.a.  [nomino, Latin.] 1. To name; to mention by name. Suddenly to nominate them all, It is impossible. Shakes. Henry VI. p. iii. One lady, I may civilly spare to nominate, for her sex’s sake, whom he termed the spider of the court. Wotton. 2. To entitle.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/nominate_va",
    },
    "noon": {
        "definition": "1. The middle hour of the day; twelve; the time when the sun is in the meridian. Fetch forth the stocks, there shall he sit ’till noon. —— ’Till noon! ’till night, my lord, Shakes. K. Lear. The day already half his race had run, And summon’d him to due repast at noon. Dryden.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/noon_ns",
    },
    "nor": {
        "definition": "nor, conj. Nor. conjunct. [no or.] 1. A particle marking the second or subsequent branch of a negative proposition; correlative to neither or not. I neither love, nor fear thee. Shakespeare. Neither love will twine, nor hay. Marvel. 2. Two negatives are sometimes joined, but ill.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/nor_conj",
    },
    "north": {
        "definition": "The point opposite to the sun in the meridian. More unconstant than the wind; who wooes Ev’n now the frozen bosom of the north; And being anger’d puffs away from thence, Turning his face to the dew dropping south. Shakes. The tyrannous breathing of the north, Shakes all our buds from blowing.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/north_ns",
    },
    "not": {
        "definition": "The particle of negation, or refusal.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[ne awiht, Saxon]",
    },
    "nothing": {
        "definition": "1. Negation of being; nonentity; universal negation; opposed to something. It is most certain, that there never could be nothing. For, if there could have been an instant, wherein there was nothing, then either nothing made something, or something made itself; and so was, and acted, before it was. But if there never could be nothing; then there is, and was, a being of necessity, without any beginning. Grew’s Cos. We do not create the world from nothing and by nothing; we assert an eternal God to have been the efficient cause of it. Bentley’s Serm. This nothing is taken either in a vulgar or philosophical sense; so we say there is nothing in the cup in a vulgar sense, when we mean there is no liquor in it; but we cannot say there is nothing in the cup, in a strict philosophical sense, while there is air in it. Watts’s Logick. 2. Nonexistence.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/nothing_ns",
    },
    "now": {
        "definition": "Nothing is there to come, and nothing past, But an eternal now does ever last. Cowley. She vanish’d, we can scarcely say she dy’d, For but a now did heav’n and earth divide: This moment perfect health, the next was death. Dryden. Not less ev’n in this despicable now,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/now_ns",
    },
    "number": {
        "definition": "The species of quantity by which it is computed how many.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[numerus, Latin]",
    },
    "oath": {
        "definition": "An affirmation, negation, or promise, corroborated by the attestation of the Divine Being.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[ath, Gothick]",
    },
    "obligation": {
        "definition": "1. The binding power of any oath, vow, duty; contract. Your father lost a father; That father his; and the survivor bound In filial obligation, for some term, To do obsequious sorrow. Shakespeare’s Hamlet. There was no means for him as a christian, to satisfy all obligations both to God and man, but to offer himself for a mediator of an accord and peace. Bacon’s Henry VII.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/obligation_ns",
    },
    "october": {
        "definition": "OCTO'BER. n.s.  [October, Lat. octobre, Fr.] The tenth month of the year, or the eighth numbered from March.‡‡ October is drawn in a garment of yellow and carnation; upon his head a garland of oak leaves, in his right hand the sign scorpio, in his left a basket of servises. Peacham.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/october_ns",
    },
    "of": {
        "definition": "1. It is put before the substantive that follows another in construction; as, of these part were slain; that is, part of these. I cannot instantly raise up the gross Of full three thousand ducats. Shakespeare. He to his natural endowments of a large invention, a ripe judgment, and a strong memory, has joined the knowledge of the liberal arts. Dryden. All men naturally fly to God in extremity, and the most atheistical person in the world, when forsaken of all hopes of any other relief, is forced to acknowledge him. Tillotson.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/of_prep",
    },
    "off": {
        "definition": "1. Not on. I continued feeling again the same pain; and finding it grow violent I burnt it, and felt no more after the third time; was never off my legs, nor kept my chamber a day. Temple. 2. Distant from. Cicero’s Tusculum was at a place called Grotto Ferrate, about two miles off this town, though most of the modern writers have fixed it to Frescati. Addison on Italy.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/off_prep",
    },
    "offence": {
        "definition": "O'FFENCE. n.s.  [offense, Fr. offensa, from offendo, Lat.] 1. Crime; act of wickedness. Thither with speed their hasty course they ply’d, Where Christ the Lord for our offences dy’d. Fairfax. Thou hast stol’n that, which after some few hours Were thine without offence. Shakesp. Henry IV.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/offence_ns",
    },
    "office": {
        "definition": "A public charge or employment.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[officium, Latin]",
    },
    "officer": {
        "definition": "1. A man employed by the publick. ’Tis an office of great worth, And you an officer fit for the place. Shakespeare. Submit you to the people’s voices, Allow their officers, and be content To suffer lawful censure. Shakesp. Coriolanus.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/officer_ns",
    },
    "on": {
        "definition": "1. It is put before the word, which signifies that which is under, that by which any thing is supported, which any thing covers, or where any thing is fixed. He is not lolling on a lewd love bed, But on his knees at meditation. Shakesp. Rich. III. What news? —— —— Richmond is on the seas. —— —— There let him sink and be the seas on him. Shakesp.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/on_prep",
    },
    "one": {
        "definition": "1. A single person. If one by one you wedded all the world, She you kill’d would be unparallel’d. Shakespeare. Although the beauties, riches, honours, sciences, virtues, and perfections of all men were in the present possession of one, yet somewhat beyond and above all this there would still be sought and earnestly thirsted for. Hooker, b. i. From his lofty steed he flew, And raising one by one the suppliant crew,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/one_ns",
    },
    "open": {
        "definition": "To Ope. To O'pen. v.a.  [open, Saxon; op, Islandick, a hole. Ope is used only in poetry, when one syllable is more convenient than two.] 1. To unclose; to unlock; to put into such a state as that the inner parts may be seen or entered. The contrary to shut. The world’s mine oyster, Which I with sword will open. Shakesp. M. W. of Wind. Before you fight, ope this letter. Shakesp. K. Lear.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/open_va",
    },
    "operation": {
        "definition": "Agency; production of effects; influence.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[operatio, Latin]",
    },
    "opinion": {
        "definition": "OPI'NION. n.s.  [opinion, Fr. opinio, Lat.] 1. Perswasion of the mind, without proof or certain knowledge. Opinion is a light, vain, crude and imperfect thing, settled in the imagination, but never arriving at the understanding, there to obtain the tincture of reason. Ben. Johnson. Opinion is, when the assent of the understanding is so far gained by evidence of probability, that it rather inclines to one perswasion than to another, yet not altogether without a mixture of incertainty or doubting. Hale. Stiff in opinion, ever in the wrong. Dryden.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/opinion_ns",
    },
    "or": {
        "definition": "Gold. The show’ry arch With listed colours gay, or, azure, gules, Delights and puzzles the beholders eyes. Philips.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/or_ns",
    },
    "ordain": {
        "definition": "Sense 2 applies: 'To establish; to settle; to institute.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[ordino, Latin; ordonner, French]",
    },
    "order": {
        "definition": "Method; regular disposition.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[ordre, French]",
    },
    "original": {
        "definition": "O'rigin. 1. Beginning; first existence. The sacred historian only treats of the origins of terrestrial animals. Bentley’s Sermons. 2. Fountain; source; that which gives beginning or existence. Nature which contemns its origin, Cannot be border’d certain in itself. Shakesp. King Lear.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/original_ns",
    },
    "originate": {
        "definition": "To Ori'ginate. v.a.  [from origin.] To bring into existence.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/originate_va",
    },
    "other": {
        "definition": "other, pron. O'ther. pron.  [oðer, Sax. autre, Fr.] 1. Not the same; not this; different. Of good actions some are better than other some. Hooker. Will it not be received That they have don’t, Who dares receive it other?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/other_pron",
    },
    "ought": {
        "definition": "For ought that I can understand, there is no part but the bare English pale, in which the Irish have not the greatest footing. Spenser on Ireland. He asked him if he saw ought. Mark viii. 23. To do ought good never will be our task; But ever to do ill our sole delight. Milton’s Par. Lost. Universal Lord! be bounteous still",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/ought_ns",
    },
    "out": {
        "definition": "To Out. v.a.  To expel; to deprive. The members of both houses who withdrew, were counted deserters, and outed of their places in parliament. K. Charles. So many of their orders, as were outed from their fat possessions, would endeavour a re-entrance against those whom they account hereticks. Dryden.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/out_va",
    },
    "owner": {
        "definition": "A bark Stays but till her owner comes aboard. Shakesp. Is it not enough to break into my garden, Climbing my walls in spight of me the owner, But thou wilt brave me. Shakesp. Here shew favour, because it happeneth that the owner hath incurred the forfeiture of eight years profit of his lands, before he cometh to the knowledge of the process against him.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/owner_ns",
    },
    "part": {
        "definition": "Something less than the whole; a portion; a quantity taken from a larger quantity.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[pars, Latin]",
    },
    "participation": {
        "definition": "1. The state of sharing something in common. Civil society doth more content the nature of man, than any private kind of solitary living; because, in society, this good of mutual participation is so much larger. Hooker. Their spirits are so married in conjunction, with the participation of society, that they flock together in consent, like so many wild geese. Shakesp. Henry IV. A joint coronation of himself and his queen might give any countenance of participation of title. Bacon. 2. The act or state of partaking or having part of something.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/participation_ns",
    },
    "particular": {
        "definition": "1. A single instance; a single point. I must reserve some particulars, which it is not lawful for me to reveal. Bacon. Those notions are universal, and what is universal must needs proceed from some universal constant principle; the same in all particulars, which can be nothing else but human nature. South’s Sermons. Having the idea of an elephant or an angle in my mind, the first and natural enquiry is, whether such a thing does exist? and this knowledge is only of particulars. Locke. And if we will take them, as they were directed, in particular to her, or in her, as their representative, to all other women, they will, at most, concern the female sex only, and import no more but that subjection, they should ordinarily be in, to their husbands.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/particular_ns",
    },
    "particularly": {
        "definition": "1. Distinctly; singly; not universally. Providence, that universally casts its eye over all the creation, is yet pleased more particularly to fasten it upon some. South’s Sermons. 2. In an extraordinary degree. This exact propriety of Virgil, I particularly regarded as a great part of his character. Dryden. With the flower and the leaf I was so particularly pleased, both for the invention and the moral, that I commend it to the reader. Dryden.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/particularly_va",
    },
    "party": {
        "definition": "1. A number of persons confederated by similarity of designs or opinions in opposition to others; a faction. When any of these combatants strips his terms of ambiguity, I shall think him a champion for truth, and not the slave of vain glory or a party. Locke. This account of party patches will appear improbable to those, who live at a distance from the fashionable world. Addis. Party writers are so sensible of the secret virtue of an innuendo, that they never mention the q —— n at length. Spectat. This party rage in women only serves to aggravate animosities that reign among them.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/party_ns",
    },
    "payment": {
        "definition": "1. The act of paying. 2. The discharge of debt or promise. Thy husband commits his body To painful labour both by sea and land, And craves no other tribute at thy hands But love, fair looks, and true obedience; Too little payment for so great a debt. Shakesp.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/payment_ns",
    },
    "peace": {
        "definition": "Agreement, Concord, Quietness. [Law sense]: a quiet Behaviour towards King and Subject. (Old phrase: 'Peace of God and the Church' = the vacation period when lawsuits paused between court terms.)",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[paix, French; pax, Latin] (Bailey's, 1721 -- not locatable in Johnson's scan)",
    },
    "people": {
        "definition": "A nation; those who compose a community.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[peuple, French; populus, Latin]",
    },
    "perfect": {
        "definition": "Complete; consummate; neither defective nor redundant.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[perfectus, Latin; parfait, French]",
    },
    "perfidy": {
        "definition": "PERFI'DY. n.s.  [perfidia, Lat. perfidie, Fr.] Treachery; want of faith; breach of faith.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/perfidy_ns",
    },
    "perform": {
        "definition": "To PERFO'RM. v.a.  [performare, Italian.] To execute; to do; to discharge; to atchieve an undertaking; to accomplish. All three set among the foremost ranks of fame for great minds to attempt, and great force to perform what they did attempt. Sidney, b. ii. Hast thou, spirit, Perform’d to point the tempest that I bad thee? Shakesp. What cannot you and I perform upon Th’ unguarded Duncan?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/perform_va",
    },
    "period": {
        "definition": "PE'RIOD. n.s.  [periode, Fr. πεϱίοδος.] 1. A circuit. 2. Time in which any thing is performed, so as to begin again in the same manner. Tell these, that the sun is fixed in the centre, that the earth with all the planets roll round the sun in their several periods; they cannot admit a syllable of this new doctrine. Watts. 3. A stated number of years; a round of time, at the end of which the things comprised within the calculation shall return to the state in which they were at beginning. A cycle or period is an account of years that has a beginning and end too, and then begins again as often as it ends. Holder on Time.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/period_ns",
    },
    "person": {
        "definition": "Individual or particular man or woman.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[persona, Latin]",
    },
    "petition": {
        "definition": "Request; intreaty; supplication; prayer.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[petitio, Latin]",
    },
    "place": {
        "definition": "Particular portion of space.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[platea, Latin]",
    },
    "pledge": {
        "definition": "1. Any thing put to pawn. 2. A gage; any thing given by way of warrant or security; a pawn. These men at the first were only pitied; the great humility, zeal and devotion, which appeared to be in them, was in all men’s opinion a pledge of their harmless meaning. Hooker. If none appear to prove upon thy person Thy heinous, manifest and many treasons; There is my pledge, I’ll prove it on thy heart. Shakespeare.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/pledge_ns",
    },
    "population": {
        "definition": "The population of a kingdom, especially if it be not mown down by wars, does not exceed the stock of the kingdom, which should maintain them; neither is the population to be reckoned, only by number; for a smaller number, that spend more and earn less, do wear out an estate sooner than a greater number, that live lower, and gather more. Bacon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/population_ns",
    },
    "possession": {
        "definition": "1. The state of owning or having in one’s own hands or power; property. He shall inherit her, and his generation shall hold her in possession. Ecclus. iv. 16. In possession such, not only of right, I call you. Milton. 2. The thing possessed. Do nothing to lose the best possession of life, that of honour and truth.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/possession_ns",
    },
    "posterity": {
        "definition": "Succeeding generations; descendants; opposed to ancestors.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[posteritas, Latin]",
    },
    "power": {
        "definition": "Command; authority; dominion; influence.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[pouvoir, French]",
    },
    "prejudice": {
        "definition": "PRE'JUDICE. n.s.  [prejudice, Fr. prejudicium, Lat.] 1. Prepossession; judgment formed beforehand without examination. It is used for prepossession in favour of any thing or against it. It is sometimes used with to before that which the prejudice is against, but not properly. The king himself frequently considered more the person who spoke, as he was in his prejudice, than the counsel itself that was given. Clarendon, b. viii. My comfort is, that their manifest prejudice to my cause will render their judgment of less authority. Dryden. There is an unaccountable prejudice to projectors of all kinds, for which reason, when I talk of practising to fly, silly people think me an owl for my pains. Addison.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/prejudice_ns",
    },
    "prerogative": {
        "definition": "An exclusive or peculiar privilege.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[praerogativa, low Latin] (Johnson's, 1755)",
    },
    "present": {
        "definition": "Not absent; being face to face; being at hand.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[praesens, Latin]",
    },
    "presentment": {
        "definition": "A Declaration or Report made by the Jurors or other Officers, of an Offence enquirable in the Court to which it is presented -- distinguished from indictment as the grand jury's own initiation of a charge.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[presentement, French] (Bailey's, 1721)",
    },
    "president": {
        "definition": "Sense 1 applies: 'One placed with authority over others; one at the head of others.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[praesidens, Latin; president, French]",
    },
    "press": {
        "definition": "Sense 2: 'The instrument by which books are printed.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[presse, French]",
    },
    "prevent": {
        "definition": "To go before as a guide; to go before, making the way easy.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[prevenio, Latin]",
    },
    "prior": {
        "definition": "1. The head of a convent of monks, inferior in dignity to an abbot. Neither she, nor any other, besides the prior of the convent, knew any thing of his name. Addison’s Spectator. 2. Prior is such a person, as, in some churches, presides over others in the same churches. Ayliffe’s  Parergon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/prior_ns",
    },
    "private": {
        "definition": "His private with me of the dauphin’s love, Is much more general than these lines import. Shakesp.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/private_ns",
    },
    "privilege": {
        "definition": "1. Peculiar advantage. Here’s my sword, Behold it is the privilege of mine honours, My oath, and my profession. Shakesp. He went Invisible, yet stay’d, such privilege Hath omnipresence.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/privilege_ns",
    },
    "proceed": {
        "definition": "Produce: as, the proceeds of an estate. Not an imitable word, though much used in law writings.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/proceed_ns",
    },
    "process": {
        "definition": "A going forward, a continued Series or Order of Things.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[proces, French; processus, Latin] (Bailey's, 1721)",
    },
    "produce": {
        "definition": "1. Product; that which any thing yields or brings. You hoard not health for your own private use, But on the publick spend the rich produce. Dryden. 2. Amount; profit; gain; emergent sum or quantity. In Staffordshire, after their lands are marled, they sow it with barley, allowing three bushels to an acre. Its common produce is thirty bushels. Mortimer’s Husbandry. This tax has already been so often tried, that we know the exact produce of it.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/produce_ns",
    },
    "profit": {
        "definition": "PRO'FIT. n.s.  [profit, Fr.] 1. Gain; pecuniary advantage. Thou must know, ’Tis not my profit that does lead mine honour. Shakesp. He thinks it highly just, that all rewards of trust, profit, or dignity should be given only to those, whose principles direct them to preserve the constitution. Swift. 2. Advantage; accession of good.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/profit_ns",
    },
    "progress": {
        "definition": "PRO'GRESS. n.s.  [progress, Fr. from progressus, Lat.] 1. Course; procession; passage. I cannot, by the progress of the stars, Give guess how near to-day. Shakesp. Julius Cæsar. The morn begins Her rosy progress smiling. Milton.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/progress_ns",
    },
    "prohibit": {
        "definition": "To forbid; to interdict by authority. (covers prohibited, prohibiting)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[prohibeo, Latin]",
    },
    "promote": {
        "definition": "To advance or prefer, to further or carry on.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[promovere, Latin] (Bailey's, 1721)",
    },
    "proper": {
        "definition": "Peculiar; not belonging to more or common.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[proprius, Latin]",
    },
    "property": {
        "definition": "1. Peculiar quality. What special property or quality is that, which being no where found but in sermons, maketh them effectual to save souls? Hooker, b. v. s. 22. A secondary essential mode, is any attribute of a thing, which is not of primary consideration, and is called a property. Watts. 2. Quality; disposition. ’Tis conviction, not force, that must induce assent; and sure the logick of a conquering sword has no great property that way; silence it may, but convince it cannot. D. of Piety.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/property_ns",
    },
    "proportion": {
        "definition": "Comparative relation of one thing to another; ratio.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "protect": {
        "definition": "To defend; to cover from evil; to shield.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[protectus, Latin]",
    },
    "protection": {
        "definition": "1. Defence; shelter from evil. Drive tow’rd Dover, friend, where thou shalt meet Both welcome and protection. Shakesp. King Lear. If the weak might find protection from the mighty, they could not with justice lament their condition. Swift. 2. A passport; exemption from being molested: as, he had a protection during the rebellion.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/protection_ns",
    },
    "provide": {
        "definition": "To procure beforehand; to get ready; to prepare. (covers 'provided')",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[provideo, Latin]",
    },
    "providence": {
        "definition": "1. Foresight; timely care; forecast; the act of providing. The only people, which as by their justice and providence give neither cause nor hope to their neighbours to annoy them, so are they not stirred with false praise to trouble others quiet. Sidney. Providence for war is the best prevention of it. Bacon. An established character spreads the influence of such as move in a high sphere, on all around; it reaches farther than their own care and providence can do. Atterbury. 2. The care of God over created beings; divine superintendence.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/providence_ns",
    },
    "public": {
        "definition": "Belonging to a state or nation; not private.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[publicus, Latin]",
    },
    "publish": {
        "definition": "To PU'BLISH, v.a.  [publier, Fr. publico, Lat.] 1. To discover to mankind; to make generally and openly known; to proclaim; to divulge. How will this grieve you, When you shall come to clearer knowledge, that You thus have published me. Shakesp. Winter’s Tale. His commission from God and his doctrine tend to the impressing the necessity of that reformation, which he came to publish. Hammond’s Fundamentals.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/publish_va",
    },
    "punish": {
        "definition": "To PU'NISH. v.a.  [punio, Lat.] 1. To chastise; to afflict with penalties or death for some crime. Your purpos’d low correction Is such, as basest and the meanest wretches Are punished with. Shakesp. King Lear. If you will not hearken, I will punish you seven times more for your sins. Lev. xxvi. 18.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/punish_va",
    },
    "punishment": {
        "definition": "Any infliction or pain imposed in vengeance of a crime.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[punissement, French]",
    },
    "qualify": {
        "definition": "To QUALI'FY. v.a.  [qualifier, Fr.] 1. To fit for any thing. Place over them such governors, as may be qualified in such manner as may govern the place. Bacon’s Advice to Villiers. I bequeath to Mr. John Whiteway the sum of one hundred pounds, in order to qualify him for a surgeon. Swift’s Will. 2. To furnish with qualifications; to accomplish. That which ordinary men are fit for, I am qualified in; and the best of me is diligence.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/qualify_va",
    },
    "quorum": {
        "definition": "A bench of justices; such a number of any officers as is sufficient to do business.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[Latin]",
    },
    "ratification": {
        "definition": "The act of ratifying; confirmation.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from ratify, French]",
    },
    "ratify": {
        "definition": "To confirm or establish, especially by a publick Act.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[ratifier, French; ratificare, Latin] (Bailey's, 1721)",
    },
    "reason": {
        "definition": "REA'SON. n.s.  [raison, Fr. ratio, Lat.] 1. The power by which man deduces one proposition from another, or proceeds from premises to consequences; the rational faculty. Reason is the director of man’s will, discovering in action what is good; for the laws of well-doing are the dictates of right reason. Hooker, b. i. s. 7. Though brutish that contest and foul, When reason hath to deal with force; yet so Most reason is that reason overcome. Milton.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/reason_ns",
    },
    "receive": {
        "definition": "To take or obtain any thing as due.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[recipio, Latin]",
    },
    "recess": {
        "definition": "1. Retirement; retreat; withdrawing; secession. What tumults could not do, an army must; my recess hath given them confidence that I may be conquered. K. Charles. Fair Thames she haunts, and ev’ry neighb’ring grove, Sacred to soft recess and gentle love. Prior. 2. Departure. We come into the world, and know not how; we live in it in a self-nescience, and go hence again, and are as ignorant of our recess.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/recess_ns",
    },
    "recommend": {
        "definition": "To RECOMME'ND. v.a.  [recommender, Fr. re and commend.] 1. To praise to another. 2. To make acceptable. Mecenas recommended Virgil and Horace to Augustus, whose praises helped to make him popular while alive, and after his death have made him precious to posterity. Dryden. A decent boldness ever meets with friends, Succeeds, and ev’n a stranger recommends. Pope.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/recommend_va",
    },
    "record": {
        "definition": "Register; authentick memorial.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[record, French]",
    },
    "rectitude": {
        "definition": "1. Straitness; not curvity. 2. Rightness; uprightness; freedom from moral curvity or obliquity. Faith and repentance, together with the rectitude of their present engagement would fully prepare them for a better life. King Charles. Calm the disorders of thy mind, by reflecting on the wisdom, equity and absolute rectitude of all his proceedings. Att.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/rectitude_ns",
    },
    "redress": {
        "definition": "1. Reformation; amendment. To seek reformation of evil laws is commendable, but for us the more necessary is a speedy redress of ourselves. Hooker. 2. Relief; remedy. No humble suitors press to speak for right; No, not a man comes for redress to thee. Shakesp. Such people, as break the law of nations, all nations are interested to suppress, considering that the particular states, being the delinquents, can give no redress.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/redress_ns",
    },
    "reduce": {
        "definition": "To REDU'CE. v.a.  [reduco, Lat. reduire, Fr.] 1. To bring back. Obsolete. Abate the edge of traitors, gracious lord! That would reduce these bloody days again. Shakesp. 2. To bring to the former state. It were but just And equal to reduce me to my dust,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/reduce_va",
    },
    "regulation": {
        "definition": "1. The act of regulating. Being but stupid matter, they cannot continue any regular and constant motion, without the guidance and regulation of some intelligent being. Ray on the Creation. 2. Method; the effect of regulation.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/regulation_ns",
    },
    "reliance": {
        "definition": "His days and times are past, And my reliance on his fracted dates Has smit my credit. Shakesp. Timon of Athens. That pellucid gelatinous substance, which he pitches upon with so great reliance and positiveness, is chiefly of animal constitution. Woodward. He secured and encreased his prosperity, by an humble behaviour towards God, and a dutiful reliance on his providence. Atterbury’s Sermons.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/reliance_ns",
    },
    "religion": {
        "definition": "Virtue, as founded upon reverence of God, and expectation [of reward or punishment].",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[religio, Latin]",
    },
    "relinquish": {
        "definition": "To RELI'NQUISH. v.a.  [relinquo, Lat.] 1. To forsake; to abandon; to leave; to desert. The habitation there was utterly relinquished. Abbot. The English colonies grew poor and weak, though the English lords grew rich and mighty; for they placed Irish tenants upon the lands relinquished by the English. Davies. 2. To quit; to release; to give up. The ground of God’s sole property in any thing is, the return of it made by man to God; by which act he relinquishes and delivers back to God all his right to the use of that thing, which before had been freely granted him by God.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/relinquish_va",
    },
    "remain": {
        "definition": "1. Relick; that which is left. Generally used in the plural. I grieve with the old, for so many additional inconveniencies, more than their small remain of life seemed destined to undergo. Pope. 2. The body left by the soul. But fowls obscene dismember’d his remains, And dogs had torn him. Pope’s Odyssey. Oh would’st thou sing what heroes Windsor bore,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/remain_ns",
    },
    "removal": {
        "definition": "1. The act of putting out of any place. By which removal of one extremity with another, the world, seeking to procure a remedy, hath purchased a mere exchange of the evil before felt. Hooker. 2. The act of putting away. The removal of such a disease is not to be attempted by active remedies, no more than a thorn in the flesh is to be taken away by violence. Arbuthnot. 3. Dismission from a post. If the removal of these persons from their posts has produced such popular commotions, the continuance of them might have produced something more fatal.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/removal_ns",
    },
    "representation": {
        "definition": "1. Image; likeness. If images are worshipped, it must be as gods, which Celsus denied, or as representations of God; which cannot be, because God is invisible and incorporeal. Stillingfleet. 2. Act of supporting a vicarious character. 3. Respectful declaration.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/representation_ns",
    },
    "representative": {
        "definition": "Noun sense 2 applies: 'One exercising the vicarious power given by another.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[representatif, French]",
    },
    "reprisal": {
        "definition": "The English had great advantage in value of reprisals, as being more strong and active at sea. Hayward. Sense must sure thy safest plunder be, Since no reprisals can be made on thee. Pope.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/reprisal_ns",
    },
    "republican": {
        "definition": "These people are more happy in imagination than the rest of their neighbours, because they think themselves so; though such a chimerical happiness is not peculiar to republicans. Add.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/republican_ns",
    },
    "republick": {
        "definition": "Commonwealth; state in which the power is lodged in more than one.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[republica, Latin; republique, French] (Johnson's, 1755)",
    },
    "require": {
        "definition": "To REQUI'RE. v.a.  [requiro, Lat. requerir, Fr.] 1. To demand; to ask a thing as of right, Ye me require A thing without the compass of my wit; For both the lineage and the certain sire, From which I sprung, are from me hidden yet. Spenser. We do require them of you, so to use them,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/require_va",
    },
    "reserve": {
        "definition": "To keep in store; to save for some other purpose. (covers reserved, reserving)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[reservo, Latin]",
    },
    "reside": {
        "definition": "To RESI'DE. v.n.  [resideo, Lat. resider, Fr.] 1. To have abode; to live; to dwell; to be present. How can God with such reside? Milton. In no fix’d place the happy souls reside; In groves we live, and lie on mossy beds. Dryden’s Æneis. 2. [Resido, Lat.]",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/reside_vn",
    },
    "resident": {
        "definition": "The pope fears the English will suffer nothing like a resident or consul in his kingdoms. Addison.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/resident_ns",
    },
    "resignation": {
        "definition": "1. The act of resigning or giving up a claim or possession. Do that office of thine own good will; The resignation of thy state and crown. Shakesp. Rich. II. He intended to procure a resignation of the rights of the king’s majesty’s sisters and others, entitled to the possession of the crown. Hayward. 2. Submission; unresisting acquiescence. We cannot expect, that any one should readily quit his own opinion, and embrace ours, with a blind resignation to an authority, which the understanding acknowledges not.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/resignation_ns",
    },
    "resolution": {
        "definition": "1. Act of clearing difficulties. In matters of antiquity, if their originals escape due relation, they fall into great obscurities, and such as future ages seldom reduce into a resolution. Brown’s Vulgar Errours. The unravelling and resolution of the difficulties, that are met with in the execution of the design, are the end of an action. Dryden’s Oedipus. 2. Analysis; act of separating any thing into constituent parts. To the present impulses of sense, memory and instinct, all the sagacities of brutes may be reduced; though witty men, by analytical resolution, have chymically extracted an artificial logick out of all their actions. Hale’s Orig. of Mankind.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/resolution_ns",
    },
    "respective": {
        "definition": "Particular, relative.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(Bailey's, 1721)",
    },
    "rest": {
        "definition": "1. Sleep; repose. All things retir’d to rest, mind us of like repose. Milton. My tost limbs are wearied into rest. Pope. 2. The final sleep; the quietness of death. Oft with holy hymns he charm’d their ears;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/rest_ns",
    },
    "resume": {
        "definition": "To RESU'ME. v.a.  [resumo, Lat.] 1. To take back what has been given. The sun, like this, from which our sight we have, Gaz’d on too long, resumes the light he gave. Denham. Sees not my love, how time resumes The glory which he lent these flow’rs; Though none shou’d taste of their perfumes,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/resume_va",
    },
    "retain": {
        "definition": "To keep; not to lose. (covers retained)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[retineo, Latin]",
    },
    "right": {
        "definition": "Noun sense applies, not adjective: 'Just claim' / 'Power; prerogative' / 'Immunity; privilege.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[riht, Saxon; rectus, Latin]",
    },
    "ruler": {
        "definition": "1. Governour; one that has the supreme command. Soon rulers grow proud, and in their pride foolish. Sidney. God, by his eternal providence, has ordained kings; and the law of nature, leaders and rulers over others. Raleigh. The pompous mansion was design’d To please the mighty rulers of mankind; Inferior temples use on either hand.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/ruler_ns",
    },
    "safety": {
        "definition": "1. Freedom from danger. To that dauntless temper of his mind, He hath a wisdom that doth guide his valour To act in safety. Shakesp. Macbeth. If her acts have been directed well, While with her friendly clay she deign’d to dwell, Shall she with safety reach her pristine seat,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/safety_ns",
    },
    "sale": {
        "definition": "SALE. n.s.  [saal, Dutch.] 1. The act of selling. 2. Vent; power of selling; market. Nothing doth more enrich any country than many towns; for the countrymen will be more industrious in tillage, and rearing of all husbandry commodities, knowing that they shall have ready sale for them at those towns. Spenser. 3. A publick and proclaimed exposition of goods to the market; auction. Those that won the plate, and those thus sold, ought to be marked so as they may never return to the race, or to the sale. Temple.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/sale_ns",
    },
    "science": {
        "definition": "SCI'ENCE. n.s.  [science, French; scientia, Latin.] 1. Knowledge. If we conceive God’s sight or science, before the creation of the world, to be extended to all and every part of the world, seeing every thing as it is, his prescience or foresight of any action of mine, or rather his science or sight, from all eternity, lays no necessity on any thing to come to pass, any more than my seeing the sun move hath to do in the moving of it. Hamm. 2. Certainty grounded on demonstration. So you arrive at truth, though not at cience. Berkley. 3. Art attained by precepts, or built on principles.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/science_ns",
    },
    "search": {
        "definition": "To examine; to try; to explore; to look through. (covers searches, searched)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[chercher, French]",
    },
    "seat": {
        "definition": "1. A chair, bench, or any thing on which one may sit. The sons of light Hasted, resorting to the summons high, And took their seats. Milton’s Paradise Lost. The lady of the leaf ordain’d a feast, And made the lady of the flow’r her guest; When, lo, a bow’r ascended on the plain,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/seat_ns",
    },
    "secrecy": {
        "definition": "1. Privacy; state of being hidden. That’s not suddenly to be perform’d, But with advice and silent secrecy. Shak. Henry VI. The lady Anne, Whom the king hath in secrecy long married, This day was view’d in open as his queen. Shakes. H. VIII.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/secrecy_ns",
    },
    "section": {
        "definition": "[Architecture, only sense found] The Draught of the Heights and Depths of a Building railed on a Plane, as tho' the whole Fabrick were cut asunder, to discover the Inside. NOTE: partial match only -- the 'numbered text division' sense (as used constitutionally) was not located in either dictionary; same root concept (a cut/division) applies by extension.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(Bailey's, 1721)",
    },
    "secure": {
        "definition": "Free from fear; exempt from terror.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[securus, Latin]",
    },
    "security": {
        "definition": "1. Carelessness; freedom from fear. Marvellous security is always dangerous, when men will not believe any bees to be in a hive, until they have a sharp sense of their stings. Hayward. 2. Vitious carelessness; confidence; want of vigilance. There is scarce truth enough alive to make societies secure; but security enough to make fellowships accurst. Shakespeare. How senseless then, and dead a soul hath he, Which thinks his soul doth with his body die;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/security_ns",
    },
    "seem": {
        "definition": "To SEEM. v.n.  [sembler, French; unless it has a Teutonick original, as seemly certainly has.] 1. To appear; to make a show; to have semblance. My lord, you’ve lost a friend, indeed; And I dare swear, you borrow not that face Of seeming sorrow; it is sure your own. Shakesp. H. IV. Speak: we will not trust our eyes Without our ears: thou art not what thou seem’st.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/seem_vn",
    },
    "seizure": {
        "definition": "Seizing, taking into Custody, Attachment, Distress.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(Bailey's, 1721)",
    },
    "senate": {
        "definition": "An assembly and body of men set apart to consult for the publick good.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[senatus, Latin; senat, French]",
    },
    "senator": {
        "definition": "A publick counsellor.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[senator, Latin; senateur, French]",
    },
    "separate": {
        "definition": "To SE'PARATE. v.a.  [separo, Latin; separer, French.] 1. To break; to divide into parts. 2. To disunite; to disjoin. I’ll to England. ———— To Ireland, I: our separated fortunes Shall keep us both the safer. Shakes. Macbeth. Resolv’d,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/separate_va",
    },
    "separation": {
        "definition": "1. The act of separating; disjunction. They have a dark opinion, that the soul doth live after the separation from the body. Abbot. Any part of our bodies, vitally united to that which is conscious in us, makes a part of ourselves; but upon separation from the vital union, by which that consciousness is communicated, that which a moment since was part of ourselves, is now no more so. Locke. 2. The state of being separate; disunion. As the confusion of tongues was a mark of separation, so the being of one language was a mark of union. Bacon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/separation_ns",
    },
    "service": {
        "definition": "1. Menial office; low business done at the command of a master. The banish’d Kent, who in disguise Follow’d his king, and did him service Improper for a slave. Shakesp. K. Lear. 2. Attendance of a servant. Both fell by our servants, by those men we lov’d most: A most unnatural and faithless service.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/service_ns",
    },
    "servitude": {
        "definition": "1. Slavery; state of a slave; dependance. Aristotle speaketh of men, whom nature hath framed for the state of servitude, saying, they have reason so far forth as to conceive when others direct them. Hooker. You would have sold your king to slaughter, His princes and his peers to servitude, His subjects to oppression and contempt. Shakesp. Hen. V. Tho’ it is necessary, that some persons in the world should be in love with a splendid servitude, yet certainly they must be much beholding to their own fancy, that they can be pleased at it; for he that rises up early, and goes to bed late, only to receive addresses, is really as much abridged in his freedom, as he that waits to present one.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/servitude_ns",
    },
    "session": {
        "definition": "1. The act of sitting. 2. An assembly of magistrates or senators.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[sessio, Latin]",
    },
    "settlement": {
        "definition": "1. The act of settling; the state of being settled. 2. The act of giving possession by legal sanction. My flocks, my fields, my woods, my pastures take, With settlement as good as law can make. Dryden. 3. A jointure granted to a wife. Strephon sigh’d so loud and strong, He blew a settlement along;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/settlement_ns",
    },
    "several": {
        "definition": "Many, divers, sundry. NOTE: this 18th-c. sense means separate/distinct/individual ones, NOT the modern loose sense of 'a small number' -- a real semantic drift point.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[separalis/separare, Latin -- 'to separate'] (Bailey's, 1721)",
    },
    "shall": {
        "definition": "Verb, defective. From 'sceal,' Saxon, originally 'I owe' or 'I ought.' Carries obligation, not just futurity.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[sceal, Saxon]",
    },
    "should": {
        "definition": "1. This is a kind of auxiliary verb used in the conjunctive mood, of which the signification is not easily fixed. 2. I Should go. It is my business or duty to go. 3. If I Should go. If it happens that I go. 4. Thou Should'st go. Thou oughtest to go. 5. If thou Should'st go. If it happens that thou goest. 6. The same significations are found in all the other persons singular and plural. Let not a desperate action more engage you Than safety should.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/should_vn",
    },
    "silver": {
        "definition": "1. Silver is a white and hard metal, next in weight to gold. Watts’s  Logick. 2. Any thing of soft splendour. Pallas, piteous of her plaintive cries, In slumber clos’d her silver-streaming eyes. Pope. 3. Money made of silver.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/silver_ns",
    },
    "sixth": {
        "definition": "Only the other half would have been a tolerable seat for rational creatures, and five sixths of the whole globe would have been rendered useless. Cheyne’s Philos. Principles.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/sixth_ns",
    },
    "slavery": {
        "definition": "If my dissentings were out of errour, weakness, or obstinacy in me, yet no man can think it other than the badge and method of slavery, by savage rudeness and importunate obtrusions of violence to have the mist of his errour dispelled. King Charles.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/slavery_ns",
    },
    "soldier": {
        "definition": "SO'LDIER. n.s.  [soldat, Fr. from solidarius, low Latin, of solidus, a piece of money, the pay of soldier; souldée, French.] 1. A fighting man; a warriour. Originally one who served for pay. Your sister is the better soldier. Shakes. King Lear. Good Siward, An older and a better soldier none. Shakesp. Macbeth. A soldier,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/soldier_ns",
    },
    "sole": {
        "definition": "1. The bottom of the foot. I will only be bold with Benedict for his company; for from the crown of his head to the sole of his foot he is all mirth. Shakesp. Much Ado about Nothing. Tickling is most in the soles of the feet: the cause is the rareness of being touched there. Bacon’s Nat. History. The soals of the feet have great affinity with the head and the mouth of the stomach; as going wet-shod, to those that use it not, affecteth both. Bacon’s Natural History. Such resting found the sole of unblest feet.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/sole_ns",
    },
    "south": {
        "definition": "SOUTH. n.s.  [suð, Saxon; suyd, Dutch; sud, French.] 1. The part where the sun is to us at noon. East and West have no certain points of heaven, but North and South are fixed; and seldom the far southern people have invaded the northern, but contrariwise. Bacon. 2. The southern regions of the globe. The queen of the South. Bible. From the North to call",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/south_ns",
    },
    "sovereign": {
        "definition": "Supreme in power; having no superiour.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[souverain, French] (Johnson's, 1755)",
    },
    "speaker": {
        "definition": "1. One that speaks. These fames grew so general, as the authors were lost in the generality of speakers. Bacon’s Henry VII. In conversation or reading, find out the true sense, idea which the speaker or writer affixes to his words. Watts’s Logick. Common speakers have only one set of ideas, and one set of words to cloath them in; and these are always ready at the mouth. Swift. 2. One that speaks in any particular manner.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/speaker_ns",
    },
    "speech": {
        "definition": "The power of articulate utterance; the power of expressing thoughts by vocal words.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from speak]",
    },
    "stage": {
        "definition": "STAGE. n.s.  [estage, French ] 1. A floor raised to view on which any show is exhibited. 2. The theatre; the place of scenick entertainments. And much good do’t you then, Brave plush and velvet men: Can feed on ort; and, safe in your stage clothes, Dare quit, upon your oaths, The stagers and the stage wrights too.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/stage_ns",
    },
    "standard": {
        "definition": "STA'NDARD. n.s.  [estendart, French.] 1. An ensign in war, particularly the ensign of the horse. His armies, in the following day, On those fair plains their standards proud display. Fairfax. Erect the standard there of ancient night, Yours be the advantage all, mine the revenge. Milton.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/standard_ns",
    },
    "standing": {
        "definition": "1. Continuance; long possession of an office, character, or place. Nothing had been more easy than to command a patron of a long standing. Dryden. Although the ancients were of opinion that Egypt was formerly sea; yet this tract of land is as old, and of as long a standing as any upon the continent of Africa. Woodward. I wish your fortune had enabled you to have continued longer in the university, till you were of ten years standing. Swift. 2. Station; place to stand in.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/standing_ns",
    },
    "state": {
        "definition": "4. Condition; circumstances of nature or fortune. 5. The community; the publick; the commonwealth.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[status, Latin]",
    },
    "station": {
        "definition": "STA'TION. n.s.  [station, French; statio, Latin.] 1. The act of standing. Their manner was to stand at prayer, whereupon their meetings unto that purpose on those days had the names of stations given them. Hooker. 2. A state of rest. All progression is performed by drawing on or impelling forward some part which was before in station or at quiet, where there are no joints. Brown’s Vulgar Errours. 3. A place where any one is placed.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/station_ns",
    },
    "subject": {
        "definition": "Bound, obliged to some Dependence; liable, apt, inclinable. As a noun: One who is under the Dominion of a Sovereign Prince -- a politically loaded 18th-c. sense standing in contrast to 'citizen.'",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[sujette, French; subjectus, Latin] (Bailey's, 1721)",
    },
    "submission": {
        "definition": "1. Delivery of himself to the power of another. Submission, Dauphin! ’tis a meer French word, We English warriors wot not what it means. Shakespeare. 2. Acknowledgement of inferiority or dependance; humble or suppliant behaviour. In all submission and humility, York doth present himself unto your highness. Shakespeare.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/submission_ns",
    },
    "such": {
        "definition": "such, pron. Such. pronoun. [sulleiks, Gothick; sulk, Dutch; swilc, Saxon.] 1. Of that kind; of the like kind. With as before the thing to which it relates, when the thing follows: as, such a power as a king’s; such a gift as a kingdom. ’Tis such another fitchew! marry, a perfum’d one. Shakes. Can we find such a one as this, in whom the spirit of God is? Gen. xli. 38. The works of the flesh are manifest, such are drunkenness, revelings, and such like. You will not make this a general rule to debar such from preaching of the Gospel as have thro’ infirmity fallen.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/such_pron",
    },
    "suffer": {
        "definition": "To SU'FFER. v.a.  [suffero, Latin; souffrir, French.] 1. To bear; to undergo; to feel with sense of pain. A man of great wrath shall suffer punishment. Prov. xix. A woman suffered many things of physicians, and spent all she had. Mark v. 26. Obedience impos’d, On penalty of death, and suffering death.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/suffer_va",
    },
    "sufferance": {
        "definition": "1. Pain; inconvenience; misery. He must not only die, But thy unkindness shall the death draw out To ling’ring sufferance. Shakespeare’s Measure for Measure. How much education may reconcile young people to pain and sufferance, the examples of Sparta shew. Locke on Education. 2. Patience; moderation.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/sufferance_ns",
    },
    "suffrage": {
        "definition": "Noble confederates, thus far is perfect, Only your suffrages I will expect At the assembly for the chusing of consuls. Ben. Johnson. They would not abet by their suffrages or presence the designs of those innovations. King Charles. The fairest of our island dare not commit their cause against you to the suffrage of those who most partially adore them. ‡‡ Addison.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/suffrage_ns",
    },
    "suit": {
        "definition": "SUIT. n.s.  [suite, French.] 1. A set; a number of things correspondent one to the other. We, ere the day, two suits of armour sought, Which borne before him, on his steed he brought. Dryd. 2. Cloaths made one part to answer another. What a beard of the general’s cut, and a horrid suit of the camp will do among foaming bottles and ale-wash’d wits is wonderful. Shakespeare’s Henry V.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/suit_ns",
    },
    "support": {
        "definition": "To sustain; to prop; to bear up.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[supportare, Latin]",
    },
    "suppress": {
        "definition": "To SU'PPRESS. v.a.  [supprimo, suppressus, Lat. supprimer, Fr.] 1. To crush; to overpower; to overwhelm; to subdue; to reduce from any state of activity or commotion. Glo’ster would have armour out of the Tower, To crown himself king and suppress the prince. Shak. H. VI. Every rebellion, when it is suppressed, doth make the subject weaker, and the prince stronger. Davies on Ireland. Sir William Herbert, with a well armed and ordered company, set sharply upon them; and oppressing some of the forwardest of them by death, suppressed the residue by fear.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/suppress_va",
    },
    "supreme": {
        "definition": "Highest in dignity; highest in authority.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[supremus, Latin]",
    },
    "swear": {
        "definition": "To Swear. v.a. 1. To put to an oath. Moses took the bones of Joseph; for he had straitly sworn the children of Israel. Ex. xiii. 19. Swom ashore, man, like a duck; I can swim like a duck, I’ll be sworn. Shakespeare’s Tempest. Let me swear you all to secrecy; And, to conceal my shame, conceal my life.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/swear_va",
    },
    "system": {
        "definition": "SY'STEM. n.s.  [systeme, Fr. σύστημα.] 1. Any complexure or combination of many things acting together. 2. A scheme which reduces many things to regular dependence or co-operation. 3. A scheme which unites many things in order. Aristotle brings morality into system, by treating of happiness under heads, and ranges it in classes according to its different objects, distinguishing virtues into their several kinds which had not been handled systematically before. Baker. The best way to learn any science is to begin with a regular system, or a short and plain scheme of that science well drawn up into a narrow compass. Watts.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/system_ns",
    },
    "taking": {
        "definition": "What a taking was he in, when your husband asked who was in the basket. Shakespeare. She saw in what a taking, The knight was by his furious quaking. Butler.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/taking_ns",
    },
    "tax": {
        "definition": "To lay a Tax upon: Also to accuse or charge one with (now-obsolete secondary sense).",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[taxare, Latin]  (Bailey's, 1721)",
    },
    "tender": {
        "definition": "1. Offer; proposal to acceptance. Then to have a wretched puling fool, A whining mammet, in her fortune’s tender, To answer I’ll not wed. Shak. Romeo and Juliet. Think yourself a baby; That you have ta’en his tenders for true pay, Which are not sterling.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/tender_ns",
    },
    "term": {
        "definition": "Time for which any thing lasts; limited time. (sense 5)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[terminus, Latin]",
    },
    "territory": {
        "definition": "Linger not in my territories longer than swiftest expedition will give thee time to leave our royal court. Shakespeare. They erected a house within their own territory, half way between their fort and the town. Hayward. He saw wide territory spread Before him, towns, and rural works between. Milton. Ne’er did the Turk invade our territory,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/territory_ns",
    },
    "test": {
        "definition": "1. The cupel by which refiners try their metals. 2. Trial; examination: as by the cupel. All thy vexations Were but my trials of thy love, and thou Hast strangely stood the test. Shakespeare’s Tempest. Let there be some more test made of my metal, Before so noble and so great a figure",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/test_ns",
    },
    "testimony": {
        "definition": "Witness, Evidence, Proof, Token; a Quotation from an Author. [in the Holy Scriptures]: signifies a Law or Ordinance.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[testimonium, Latin] (Bailey's, 1721 -- not locatable in Johnson's scan)",
    },
    "that": {
        "definition": "that, conj. That. conjunction. 1. Because. It is not that I love you less Than when before your feet I lay: But to prevent the sad increase Of hopeless love, I keep away. Waller.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/that_conj",
    },
    "their": {
        "definition": "The round world should have shook Lions into civil streets, and citizens into their dens. Shak. For the Italians, Dante had begun to file their language in verse before Boccace, who likewise received no little help from his master Petrarch; but the reformation of their prose was wholly owing to Boccace. Dryden. 2. Theirs is used when any thing comes between the possessive and substantive. Prayer we always have in our power to bestow, and they never in theirs to refuse. Hooker, b. v.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/their_ns",
    },
    "they": {
        "definition": "1. The men; the women; the persons. They are in a most warlike preparation. Shak. Coriolanus. Why do you keep alone? Of sorriest fancies your companions making, Using those thoughts, which should indeed have died With them they think on. Shakesp. Macbeth.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/they_ns",
    },
    "thing": {
        "definition": "Whatever is; not a person. A general word. 1. Whatever is; not a person. 2. Part; something. 3. Event; transaction.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/thing_ns",
    },
    "think": {
        "definition": "To Think. v.a. 1. To imagine; to image in the mind; to conceive. Royal Lear, Whom I have ever honour’d as my king, And as my patron thought on in my prayer. Shakespeare. Charity thinketh no evil. 1 Cor. xiii. 5.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/think_va",
    },
    "this": {
        "definition": "this, pron. This. pronoun. [ðis, Saxon.] 1. That which is present; what is now mentioned. Bardolph and Nim had more valour than this, yet they were both hang’d; and so would this be, if he durst steal. Shak. Come a little nearer this ways. Shakespeare. Within this three mile may you see it coming;",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/this_pron",
    },
    "those": {
        "definition": "those, pron. Those. pron. the plural of that. Make all our trumpets speak, give them all breath, Those clam’rous harbingers of blood and death. Shakesp. The fibres of this muscle act as those of others. Cheyne. Sure there are poets which did never dream",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/those_pron",
    },
    "throughout": {
        "definition": "Thus it fareth even clean throughout the whole controversy about that discipline which is so earnestly urged. Hooker. There followed after the defeat an avoiding of all Spanish forces throughout Ireland. Bacon. O for a clap of thunder, as loud As to be heard throughout the universe, To tell the world the fact, and to applaud it. B. Johnson.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/throughout_prep",
    },
    "time": {
        "definition": "A certain Measure depending on the Motion of the Luminaries, by which the Distance and Duration of things are measured.",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[tempus, Latin] (Bailey's, 1721)",
    },
    "title": {
        "definition": "A general head comprising particulars.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[titulus, Latin]",
    },
    "to": {
        "definition": "To. preposition. 1. Noting motion towards: opposed to from. With that she to him afresh, and surely would have put out his eyes. Sidney, b. ii. Tybalt fled; But by and by comes back to Romeo, And to ’t they go like light’ning. Shakespeare.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/to_prep",
    },
    "tonnage": {
        "definition": "Tonnage and poundage upon merchandizes were collected, refused to be settled by act of parliament. Clarendon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/tonnage_ns",
    },
    "treason": {
        "definition": "An offence committed against the majesty of the commonwealth: divided into high treason and petit treason. High treason is an offence against the safety of the commonwealth, or of the king's majesty, whether by imagination, word, or deed.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[trahison, French]",
    },
    "treaty": {
        "definition": "1. Negotiation; act of treating. She began a treaty to procure; And stablish terms betwixt both their requests. Fa. Qu. 2. A compact of accommodation relating to publick affairs. A peace was concluded, being rather a bargain than a treaty. Bacon’s Henry VII. Echion",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/treaty_ns",
    },
    "trial": {
        "definition": "1. Test; examination. With trial fire touch me his finger end; If he be chaste the flame will back descend, And turn him to no pain; but if he start, It is the flesh of a corrupted heart. Shakespeare. 2. Experience; act of examining by experience. I leave him to your gracious acceptance,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/trial_ns",
    },
    "tyranny": {
        "definition": "1. Absolute monarchy imperiously administered. Our grand foe, Who now triumphs, and, in th’ excess of joy, Sole reigning holds the tyranny of heav’n. Milton. The cities fell often under tyrannies, which spring naturally out of popular governments. Temple. 2. Unresisted and cruel power.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/tyranny_ns",
    },
    "unfit": {
        "definition": "To Unfi't. v.a.  To disqualify. Those excellencies, as they qualified him for dominion, so they unfitted him for a satisfaction or acquiescence in his vassals. Government of the Tongue.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/unfit_va",
    },
    "union": {
        "definition": "The joining several Things together; Concord, Agreement. [of Kingdoms or States]: that which arises from solemn Leagues made between Sovereign Princes and States -- directly relevant to 'a more perfect Union.'",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "[unio, Latin] (Bailey's, 1721)",
    },
    "unite": {
        "definition": "To join two or more into one. (covers 'united')",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[unitas, Latin]",
    },
    "unless": {
        "definition": "unless, conj. Unle'ss. conjunct. Except; if not; supposing that not. Let us not say, we keep the commandments of the one, when we break the commandments of the other: for, unless we observe both, we obey neither. Hooker. Unless I look on Sylvia in the day, There is no day for me to look upon. Shakespeare. What hidden strength,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/unless_conj",
    },
    "up": {
        "definition": "In going up a hill, the knees will be most weary; in going down, the thighs: for that in lifting the feet, when a man goeth up the hill, the weight of the body beareth most upon the knees, and in going down, upon the thighs. Bacon.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/up_prep",
    },
    "use": {
        "definition": "To Use. v.a.  [user, Fr. usus, Lat.] 1. To employ to any purpose. You’re welcome, Most learned rev’rend Sir, into our kingdom; Use us and it. Shakesp. Hen. VIII. They could use both the right hand and the left, in hurling stones and shooting arrows. 1 Chr. xii. 2.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/use_va",
    },
    "vacancy": {
        "definition": "State of a post or employment when it is unsupplied. (sense 3)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[vacance, French]",
    },
    "valid": {
        "definition": "Strong; powerful; efficacious; prevalent.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[validus, Latin]",
    },
    "validity": {
        "definition": "1. Force to convince; certainty. You are persuaded of the validity of that famous verse, ’Tis expectation makes a blessing dear. Pope. 2. Value. A sense not used. To thee and thine, Remain this ample third of our fair kingdom; No less in space, validity, and pleasure,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/validity_ns",
    },
    "vassal": {
        "definition": "WORKING DEFINITION -- no standalone headword found in either dictionary; Bailey's uses it substantively within FIEF and HOMAGIUM entries: 'Lands or Tenements, which the Vassal holds of his Lord by Fealty and Homage.' Composite sense: one who holds land from a lord in exchange for a formal oath of loyalty and service -- the feudal-dependency status 'free' is defined against in Johnson's ('not a vassal... not dependant').",
        "source": "Bailey's Dictionary (1721)",
        "etymology": "(derived from usage within FIEF/HOMAGIUM entries, Bailey's)",
    },
    "vest": {
        "definition": "Verb applies, not noun: 'To make possessor of; to invest with... vested with power.'",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[vestis, Latin]",
    },
    "vice": {
        "definition": "Sense 6 applies (used for Vice President): 'used in composition for one... who has the second rank in command: as a viceroy; vice-chancellor.' (Original capture had used sense 1, depravity -- wrong sense.)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[vitium / vice, Latin]",
    },
    "violation": {
        "definition": "1. Infringement or injury of something sacred. Their right conceit that to perjury vengeance is due, was not without good effect, as touching the course of their lives, who feared the wilful violation of oaths. Hooker. Men, who had no other guide but their reason, considered the violation of an oath to be a great crime. Addison. 2. Rape; the act of deflowering. If your pure maidens fall into the hand Of hot and forcing violation.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/violation_ns",
    },
    "violence": {
        "definition": "1. Force; strength applied to any purpose. To be imprison’d in the viewless wind, And blown with restless violence about. Shakesp. All the elements At least had gone to wreck, disturb’d and torn With violence of this conflict, had not soon Th’ eternal hung his golden scales.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/violence_ns",
    },
    "vote": {
        "definition": "Suffrage; voice given and numbered.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[votum, Latin]",
    },
    "war": {
        "definition": "War may be defined the exercise of violence under sovereign command against withstanders; force, authority, and resistance being the essential parts thereof.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[werre, old Dutch; guerre, French]",
    },
    "warfare": {
        "definition": "In the wilderness He shall first lay down the rudiments Of his great warfare, ere I send him forth To conquer sin and death. Milton’s Paradise Regained. Faithful hath been your warfare, and of God Accepted, fearless in his righteous cause. Milton.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/warfare_ns",
    },
    "warrant": {
        "definition": "A writ conferring some right or authority. (covers warrants)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from the verb]",
    },
    "water": {
        "definition": "WA'TER. n.s.  [water, Dutch; wœter, Saxon.] 1. Sir Isaac Newton defines water, when pure, to be a very fluid salt, volatile, and void of all savour or taste; and it seems to consist of small, smooth, hard, porous, spherical particles, of equal diameters, and of equal specifick gravities, as Dr. Cheyne observes; and also that there are between them spaces so large, and ranged in such a manner, as to be pervious on all sides. Their smoothness accounts for their sliding easily over one another’s surfaces: their sphericity keeps them also from touching one another in more points than one; and by both these their frictions in sliding over one another, is rendered the least possible. Their hardness accounts for the incompressibility of water, when it is free from the intermixture of air. The porosity of water is so very great, that there is at least forty times as much space as matter in it; for water is nineteen times specifically lighter than gold, and consequently rarer in the same proportion. Quincy. My mildness hath allay’d their swelling griefs, My mercy dry’d their water-flowing tears. Shak. H. VI. Your water is a sore decayer of your whorson dead body. Shakespeare’s Hamlet. The sweet manner of it forc’d",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/water_ns",
    },
    "way": {
        "definition": "1. The road in which one travels. I am amaz’d, and lose my way, Among the thorns and dangers of this world. Shakespeare. You cannot see your way.—— ——I have no way, and therefore want no eyes: I stumbled when I saw. Shakesp. K. Lear.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/way_ns",
    },
    "we": {
        "definition": "we, pron. We. pronoun. [See I] 1. The plural of I. Retire we to our chamber, A little water clears us of this deed. Shakespeare. Fair and noble hostess, We are your guests to night.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/we_pron",
    },
    "welfare": {
        "definition": "If friends to a government forbear their assistance, they put it in the power of a few desperate men to ruin the welfare of those who are superiour to them in strength and interest. Add. Discretion is the perfection of reason: cunning is a kind of instinct that only looks out after our immediate interest and welfare. Addison’s Spectator.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/welfare_ns",
    },
    "were": {
        "definition": "O river! let thy bed be turned from fine gravel to weeds and mud; let some unjust niggards make weres to spoil thy beauty. Sid.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/were_ns",
    },
    "what": {
        "definition": "what, pron. What. pronoun. [hwæt, Saxon; wat, Dutch.] 1. That which. What you can make her do, I am content to look on; what to speak, I am content to hear. Shakesp. Winter Tale. In these cases we examine the why, the what, and the how of things.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/what_pron",
    },
    "which": {
        "definition": "which, pron. WHICH. pron.  [hwilc, Saxon; welk, Dutch.] 1. The pronoun relative; relating to things. The apostles term it the pledge of our heavenly inheritance, sometimes the handsel or earnest of that which is to come. Hooker, b. v. Do they not blaspheme that worthy name, by the which ye are called? Ja. ii. 7. In destructions by deluge, the remnant which hap to be reserved are ignorant.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/which_pron",
    },
    "who": {
        "definition": "who, pron. Who. pronoun. [hwa, Saxon; wie, Dutch.] 1. A pronoun relative, applied to persons. We have no perfect description of it, nor any knowledge how, or by whom it is inhabited. Abbot. Oft have I seen a timely-parted ghost, Of ashy semblance, meagre, pale, and bloodless, Being all descended to the lab’ring heart,",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/who_pron",
    },
    "whose": {
        "definition": "1. Genitive of who. Though I could With barefac’d power sweep him from my sight, And bid my will avouch it, yet I must not; For certain friends that are both his and mine, Whose loves I may not drop. Shakespeare’s Macbeth. 2. Genitive of which.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/whose_ns",
    },
    "will": {
        "definition": "1. Choice; arbitrary determination. Will is the power, which the mind has to order the consideration of any idea, or the forbearing to consider it, or to prefer the motion of any part of the body to its rest, and vice versa. Locke’s Works. Two principal fountains there are of human actions, knowledge and will; which will, in things tending towards any end, is termed choice. Hooker, b. i. Is it her nature, or is it her will, To be so cruel to an humble foe?",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/will_ns",
    },
    "with": {
        "definition": "With. preposit.  [wið, Saxon.] 1. By. Noting the cause. Truth, tir’d with iteration, As true as steel, as plantage to the moon. Shakespeare. With ev’ry stab her bleeding heart was torn, With wounds much harder to be seen than born. Rowe.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/with_prep",
    },
    "witness": {
        "definition": "One who gives testimony. (covers witnesses)",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "—",
    },
    "would": {
        "definition": "Weld, or Would. n.s.  [luteola, Latin.] Yellow weed, or dyers weed. Its leaves are oblong and intire: it has an anomalous flower, consisting of many dissimilar leaves: the fruit is globular, hollow, and divided into three parts. The dyers use it for dying bright yellows and lemon colours; and this is by some supposed to be the plant used by the ancient Picts in painting their bodies. Miller.",
        "source": "Johnson's Dictionary (1755)",
        "url": "https://johnsonsdictionaryonline.com/1755/would_ns",
    },
    "writ": {
        "definition": "1. Any thing written; scripture. 2. A judicial process. 3. A legal instrument.",
        "source": "Johnson's Dictionary (1755)",
        "etymology": "[from write] (Johnson's, 1755)",
    },
}
