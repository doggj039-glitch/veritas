// ==UserScript==
// @name         Constitution Word Database — Johnson's Dictionary Capture + Queue
// @namespace    constitution-word-db
// @version      9.0
// @description  Highlight a word + definition on Johnson's Dictionary Online, right-click, and save it into your Constitution word database. Includes a one-at-a-time priority queue panel and a full searchable word-list viewer. Fixes a bug where captures could be silently lost.
// @match        https://johnsonsdictionaryonline.com/*
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_registerMenuCommand
// @run-at       document-idle
// ==/UserScript==

(function () {
  'use strict';

  // ---------------------------------------------------------------------
  // 1. Your Constitution word list (1,075 words across 8 tiers), pre-loaded,
  //    already in priority order (Tier 1 = most important).
  // ---------------------------------------------------------------------
  const DB = {
  "metadata": {
    "source_document": "The United States Constitution (Preamble, 7 Articles, 27 Amendments)",
    "total_word_tokens": 7454,
    "total_unique_words": 1075,
    "tier_count": 8,
    "classification_method": "Contract-analysis framework: importance ranked by role in formation, parties, grant of authority, limitations, remedies, and default rules; remaining vocabulary classified by grammatical/lexical function so that no word is omitted.",
    "note": "definition fields intentionally left blank for manual completion; source_url points to Johnson's Dictionary Online (1755/1773) and is filled in automatically with the exact entry page once a definition is captured via the companion userscript. status: 'pending' | 'done' | 'unlisted'."
  },
  "tiers": {
    "1": {
      "tier_name": "Parties to the Contract",
      "description": "The named principals (We the People, the States) and agents/offices they create (Congress, President, Courts, etc.).",
      "word_count": 30,
      "words": [
        {
          "word": "states",
          "frequency": 127,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "president",
          "frequency": 110,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "united",
          "frequency": 84,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "state",
          "frequency": 80,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "congress",
          "frequency": 64,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "house",
          "frequency": 34,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "representatives",
          "frequency": 30,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "senate",
          "frequency": 29,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vice",
          "frequency": 26,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "constitution",
          "frequency": 25,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "citizens",
          "frequency": 18,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "electors",
          "frequency": 16,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "executive",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "legislature",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "senators",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vice-president",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "people",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "government",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "legislatures",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "senator",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "court",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "judicial",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "representative",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "citizen",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "courts",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "judges",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "america",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "elector",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "judge",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "legislative",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    },
    "2": {
      "tier_name": "Purpose & Consideration",
      "description": "Preamble language stating why the contract exists \u2014 the recital of consideration.",
      "word_count": 21,
      "words": [
        {
          "word": "provide",
          "frequency": 12,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "provided",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "union",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "establish",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "defence",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "justice",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "liberty",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "establishment",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "form",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "formed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ordain",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "promote",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "secure",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "welfare",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "blessings",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "established",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "insure",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "perfect",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "posterity",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "securing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tranquility",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    },
    "3": {
      "tier_name": "Operative Grant & Limitation Language",
      "description": "The core binding/prohibiting vocabulary that does the actual work of granting, denying, or reserving authority.",
      "word_count": 28,
      "words": [
        {
          "word": "shall",
          "frequency": 306,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "may",
          "frequency": 44,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "not",
          "frequency": 44,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "no",
          "frequency": 42,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "law",
          "frequency": 39,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "power",
          "frequency": 22,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "powers",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "right",
          "frequency": 14,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "laws",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "authority",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "grant",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prohibited",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vested",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "hereby",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "herein",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "authorized",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "granted",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "hereof",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "rights",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "cannot",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "delegated",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "granting",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "grants",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prohibiting",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reserved",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reserving",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "retained",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vest",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    },
    "4": {
      "tier_name": "Structural & Procedural Safeguards",
      "description": "Mechanisms for amending, checking, and operating the government (elections, amendment process, impeachment, taxation, etc.).",
      "word_count": 26,
      "words": [
        {
          "word": "amendment",
          "frequency": 35,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vote",
          "frequency": 16,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "majority",
          "frequency": 14,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "votes",
          "frequency": 14,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "election",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "militia",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ratified",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "voted",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "war",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "impeachment",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "jury",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tax",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "process",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "quorum",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ratification",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "amendments",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "conventions",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "elections",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "taxes",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "commerce",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "convention",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "taxed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "arms",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "impeachments",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ratifying",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "voting",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    },
    "5": {
      "tier_name": "Specific Protections & Prohibitions",
      "description": "Named individual rights and explicit prohibitions on government action (Bill of Rights-type terms).",
      "word_count": 37,
      "words": [
        {
          "word": "treason",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "assemble",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "property",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "punishment",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "attainder",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "due",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "witnesses",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ex",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "facto",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "indictment",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "speech",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "assembled",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "assembling",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bail",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "compulsory",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "confronted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "corpus",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "counsel",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "cruel",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "grand",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "habeas",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "impartial",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "jeopardy",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "petition",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "presentment",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "press",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "punishments",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "religion",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "religious",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "searched",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "searches",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "seized",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "seizures",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "speedy",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "unusual",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "warrants",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "witness",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    },
    "6": {
      "tier_name": "General Substantive & Procedural Vocabulary",
      "description": "All remaining content words (nouns, verbs, adjectives) that carry meaning but aren't uniquely tied to the core contract framework \u2014 the bulk of the document's working vocabulary.",
      "word_count": 769,
      "words": [
        {
          "word": "section",
          "frequency": 55,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "office",
          "frequency": 37,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "person",
          "frequency": 34,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "article",
          "frequency": 28,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "number",
          "frequency": 25,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "years",
          "frequency": 22,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "time",
          "frequency": 21,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "duties",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "several",
          "frequency": 16,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "persons",
          "frequency": 15,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "against",
          "frequency": 14,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "make",
          "frequency": 14,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "case",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "cases",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "public",
          "frequency": 12,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "day",
          "frequency": 11,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "manner",
          "frequency": 11,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "members",
          "frequency": 11,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "officers",
          "frequency": 11,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "term",
          "frequency": 11,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "consent",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "elected",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "more",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "whole",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "year",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "enforce",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "having",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "jurisdiction",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "legislation",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "made",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "necessary",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "act",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appropriate",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "choice",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "chosen",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "houses",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "subject",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vacancies",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "age",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appointed",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bill",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "denied",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "holding",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "respective",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "service",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "supreme",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "according",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "chuse",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "crime",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "death",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "declaration",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "direct",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "discharge",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "district",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "elect",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "equal",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "foreign",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "least",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "member",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "money",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "officer",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "rules",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "take",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "trial",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "written",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "abridged",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "acting",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appoint",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ballot",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "become",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "choose",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "coin",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "compensation",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "consist",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "days",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "debts",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "enter",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "enumeration",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fill",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "held",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "list",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "oath",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "party",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "place",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "pro",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "purpose",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "rebellion",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "receive",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "representation",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "services",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "session",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "speaker",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "taken",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tempore",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "account",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "affirmation",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ambassadors",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bound",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "committed",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "common",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "construed",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "convicted",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "date",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "different",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "directed",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "effect",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "entitled",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exercise",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "greatest",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "happen",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "hold",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "immediately",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "importation",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "imposts",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inferior",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inhabitant",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inoperative",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "issue",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "journal",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "land",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "lay",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "life",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "meeting",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ministers",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "new",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "numbers",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "pay",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "places",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "post",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prescribed",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "present",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "proceedings",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "proper",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "removal",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "resignation",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "seat",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "submission",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "terms",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "times",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "transmit",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "trust",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "two-thirds",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "unable",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "use",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "actual",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "adjourn",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "adjournment",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "aid",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appointments",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "attained",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bills",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "chusing",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "civil",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "class",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "composed",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "concurrence",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "consequence",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "consuls",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "credit",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "crimes",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "departments",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disability",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "duty",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "eligible",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "entered",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exceeding",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "expiration",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "extend",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "following",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "free",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "general",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "given",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "highest",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inability",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "insurrection",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "january",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "judgment",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "keep",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "labour",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "laid",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "like",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "male",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "meet",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "next",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "noon",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "objections",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "offices",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "open",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "part",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "peace",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "presented",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "principal",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "profit",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "purposes",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "qualifications",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "qualified",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "regulation",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "regulations",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "removed",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "require",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "required",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "said",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sign",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "support",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "territory",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "think",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "title",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "transmits",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "treasury",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "treaties",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "uniform",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "valid",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "acts",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "admit",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "adoption",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "advice",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "affect",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "affecting",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "application",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appointment",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "apportioned",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "approved",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "arising",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ascertained",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "assume",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "attendance",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ballots",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bear",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "becomes",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "begin",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "beginning",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "behaviour",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "body",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "born",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "branch",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "carolina",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "cause",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "census",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "certificates",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "certify",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "chief",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "claim",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "claims",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "collect",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "comfort",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "concur",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "confederation",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "constitute",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "constitutional",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "continuance",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "contrary",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "controversies",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "counted",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "criminal",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "danger",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "debt",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "declare",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "declaring",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "delivered",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "deny",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "department",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "deprived",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "determine",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "determined",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "devolve",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "devolved",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "diminished",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "discharged",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "distinct",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "divided",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "dollars",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "domestic",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "emolument",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "encreased",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "end",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "enemies",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "enjoy",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "equally",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "equity",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exceed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "excessive",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "excises",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exclusive",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "execute",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "execution",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exports",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fact",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "faithfully",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "felony",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fixed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "forces",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "give",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "high",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "immunities",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "imports",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "imposed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "incurred",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "indians",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "intoxicating",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "invasion",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "letters",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "liquors",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "lists",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "marque",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "measures",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "mentioned",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "most",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nations",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "naval",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "navy",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nays",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "needful",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nobility",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nominate",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "numerous",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "obligation",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "offences",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "order",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "particular",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "parts",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "pass",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "passed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "payment",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "period",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "presence",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prevent",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "previously",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prior",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "privileges",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "proportion",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "propose",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "proposed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "protect",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "punish",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "question",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "questioned",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "recess",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "records",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "regulate",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reprisal",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "requisite",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "respecting",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "resume",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "return",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "revenue",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sealed",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "servitude",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sitting",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sole",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "stated",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "subjects",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "temporary",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thing",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "three-fourths",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "transportation",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tried",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "twice",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "value",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "well",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "writs",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "yeas",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ability",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "abridge",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "abridging",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "absence",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "absent",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "absolutely",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "accept",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "acceptance",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "accusation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "accused",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "acted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "actually",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "adding",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "addition",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "adhering",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "admiralty",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "admitted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "affirm",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "agree",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "agreement",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "alliance",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "alone",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "alter",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "answer",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appellate",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "apply",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "apportionment",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appropriation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "appropriations",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "approve",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "armies",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "arming",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "army",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "arrest",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "arsenals",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "articles",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "arts",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "assistance",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "attainted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "authors",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bankruptcies",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "basis",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "belonging",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "best",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "beverage",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "blood",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "borrow",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bounties",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "breach",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "bribery",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "buildings",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "business",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "call",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "called",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "calling",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "capital",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "capitation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "captures",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "care",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "carrying",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "certain",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "cession",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "charged",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "choosing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "claiming",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "classes",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "clauses",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "clear",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "color",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "commander",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "commenced",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "commission",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "commissions",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "compact",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "compel",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "compelled",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "concerned",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "concurrent",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "condition",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "confession",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "confirmation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "connecticut",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "consideration",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "considered",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "constituting",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "constitutionally",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "continue",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "contracted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "contracts",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "controul",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "controversy",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "convene",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "convened",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "conviction",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "corruption",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "counterfeiting",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "counting",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "created",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "current",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "debate",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "december",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "decide",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "deem",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "defend",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "define",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "delaware",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "delay",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "delivery",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "demand",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "deprive",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "derived",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "describing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "desire",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "determines",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "died",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disabilities",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disagreement",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disapproved",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "discipline",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disciplining",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "discoveries",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disorderly",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disparage",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "dispose",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "disqualification",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "dock-yards",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "drawn",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "duly",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "effects",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "emancipation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "emit",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "emoluments",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "employed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "empower",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ended",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "engage",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "engaged",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "engagements",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "erected",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "erection",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "escaping",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "event",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ever",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "excepted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exceptions",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "executed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "executing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exist",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "existing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exists",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "expedient",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "expel",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "expenditures",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "expire",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exportation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "exported",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "extraordinary",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "failed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "failure",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "faith",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "favor",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "felonies",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fines",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fix",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fled",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "flee",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "follows",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "foregoing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "forfeiture",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "forts",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "found",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "freedom",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "full",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "georgia",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "giving",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "going",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "gold",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "good",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "governing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "grievances",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "guarantee",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "hampshire",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "heads",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "honor",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "hours",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "illegal",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "imminent",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "impairing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "included",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "incomes",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "indian",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ineligible",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "infamous",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inflicted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "information",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "informed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "infringed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inhabitants",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inspection",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "insurrections",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "intents",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "intervened",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "invaded",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "invasions",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "inventors",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "involuntary",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "jersey",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "junction",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "kind",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "king",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "lands",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "large",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "latter",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "levying",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "liable",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "limb",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "limitations",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "limited",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "longer",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "loss",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "magazines",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "maintain",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "manufacture",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "march",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "maritime",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "maryland",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "massachusetts",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "migration",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "miles",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "military",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "misdemeanors",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "mode",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "monday",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "name",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "names",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "natural",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "naturalization",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "naturalized",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nature",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "net",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "new-york",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "north",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nothing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "obligations",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "obliged",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "obtaining",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "occasions",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "october",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "offence",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "older",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "operative",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "opinion",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "organizing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "original",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "originate",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "originated",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "overt",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "owner",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "paid",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "papers",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "pardons",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "participation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "particularly",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "peaceably",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "penalties",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "pennsylvania",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "pensions",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "perform",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "piracies",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "plantations",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "poll",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "populous",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ports",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "possession",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "preference",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prejudice",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prescribe",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "preserve",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "preserved",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "preside",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "previous",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "primary",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prince",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "private",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "privilege",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "privileged",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "probable",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "proceed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "produce",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "progress",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "proposing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prosecuted",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "prosecutions",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "protection",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "proved",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "providence",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "provisions",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "publish",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "published",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "purchased",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "pursuance",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "put",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "qualification",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "qualify",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "quartered",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "race",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "raise",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "raising",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "re-examined",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reason",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "receipt",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "receipts",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "recommend",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reconsider",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reconsideration",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reconsidered",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "redress",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reduced",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "regard",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "regular",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "regulated",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "relating",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "remain",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "remainder",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "remove",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "repassed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "repealed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "repel",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reprieves",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "republican",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "reside",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "resident",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "resolution",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "respect",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "returned",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "returning",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "returns",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "revision",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "rhode-island",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "roads",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "rule",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "safety",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sale",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "science",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "seas",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "seats",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "secrecy",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sections",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "securities",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "security",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "selected",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sent",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sex",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ships",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "signed",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "silver",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "slave",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "slavery",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "smaller",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "soldier",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "solemnly",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "source",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "south",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "square",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "standard",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "statement",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "subsequent",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "successors",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sufficient",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "suffrage",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "suit",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "suits",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sundays",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "supported",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "suppress",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "suppressing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "suspended",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "swear",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tender",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "test",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "testimony",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "things",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tonnage",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "training",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "treaty",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tribes",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "tribunals",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "troops",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "try",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "unreasonable",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "useful",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vacancy",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vacated",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "validity",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "varying",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vessels",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "violated",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "violation",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "violence",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "virginia",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "void",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "water",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "way",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "weights",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "work",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "writ",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "writing",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "writings",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    },
    "7": {
      "tier_name": "Numerals, Ordinals & Roman-Numeral Fragments",
      "description": "Number words, ordinal words, and tokenizer artifacts from Roman numerals / ordinal suffixes (e.g., 'ii', 'nd', 'th').",
      "word_count": 44,
      "words": [
        {
          "word": "one",
          "frequency": 24,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "two",
          "frequency": 20,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "th",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thirds",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "three",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "first",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "eight",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "five",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "second",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "seven",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ten",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fourth",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "six",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "twenty-one",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "four",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "i",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "third",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thirty",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thousand",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "d",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fifth",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fourths",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "hundred",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nine",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ninth",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "sixth",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "twenty",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "eighteen",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "eighteenth",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "eighth",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fifths",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "forty-eight",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "fourteen",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ii",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "iii",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "iv",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nd",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "rd",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "seventh",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "st",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "twelfth",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "v",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vi",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "vii",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    },
    "8": {
      "tier_name": "Function / Grammatical Words",
      "description": "Closed-class words (articles, pronouns, prepositions, conjunctions, auxiliary verbs) that structure sentences but carry no independent contractual content.",
      "word_count": 120,
      "words": [
        {
          "word": "the",
          "frequency": 722,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "of",
          "frequency": 491,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "and",
          "frequency": 263,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "to",
          "frequency": 203,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "be",
          "frequency": 180,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "or",
          "frequency": 160,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "in",
          "frequency": 142,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "by",
          "frequency": 99,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "a",
          "frequency": 98,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "for",
          "frequency": 84,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "any",
          "frequency": 78,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "as",
          "frequency": 64,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "have",
          "frequency": 62,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "such",
          "frequency": 52,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "which",
          "frequency": 43,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "all",
          "frequency": 41,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "from",
          "frequency": 40,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "on",
          "frequency": 39,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "this",
          "frequency": 36,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "but",
          "frequency": 33,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "other",
          "frequency": 31,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "he",
          "frequency": 28,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "their",
          "frequency": 28,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "each",
          "frequency": 26,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "if",
          "frequency": 24,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "that",
          "frequency": 24,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "at",
          "frequency": 23,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thereof",
          "frequency": 22,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "it",
          "frequency": 20,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "they",
          "frequency": 20,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "within",
          "frequency": 20,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "his",
          "frequency": 18,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "an",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "been",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nor",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "under",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "with",
          "frequency": 17,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "same",
          "frequency": 16,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "when",
          "frequency": 16,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "who",
          "frequency": 16,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "them",
          "frequency": 15,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "during",
          "frequency": 14,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "unless",
          "frequency": 14,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "is",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "without",
          "frequency": 13,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "every",
          "frequency": 12,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "then",
          "frequency": 12,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "except",
          "frequency": 11,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "before",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "into",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "its",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "than",
          "frequency": 10,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "both",
          "frequency": 9,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "after",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "until",
          "frequency": 8,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "another",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "between",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "either",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "whenever",
          "frequency": 7,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "neither",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "those",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "upon",
          "frequency": 6,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "otherwise",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "whom",
          "frequency": 5,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "among",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "are",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "him",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "so",
          "frequency": 4,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "being",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "do",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "once",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "over",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "respectively",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "there",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "therein",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "throughout",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "up",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "was",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "wherein",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "will",
          "frequency": 3,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "accordingly",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "excluding",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "had",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "including",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "themselves",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "together",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "what",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "whatever",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "where",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "whereof",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "would",
          "frequency": 2,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "also",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "concerning",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "excepting",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "forth",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "further",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "has",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "himself",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "it's",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "just",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "likewise",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "my",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "nevertheless",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "notwithstanding",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "now",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "only",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "others",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "our",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "ourselves",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "out",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "own",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "should",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "some",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thereafter",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thereby",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "thereupon",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "we",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "were",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "whatsoever",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        },
        {
          "word": "whose",
          "frequency": 1,
          "definition": "",
          "source_url": "https://johnsonsdictionaryonline.com/index.php",
          "edition": "",
          "status": "pending"
        }
      ]
    }
  }
};

  const STORAGE_KEY = 'johnson_capture_db_v2';

  function loadDB() {
    const saved = GM_getValue(STORAGE_KEY, null);
    return saved ? JSON.parse(saved) : DB;
  }

  function saveDB(db) {
    GM_setValue(STORAGE_KEY, JSON.stringify(db));
  }

  let db = loadDB();

  // ---------------------------------------------------------------------
  // One-time cleanup: earlier versions could file a capture under the
  // wrong bucket (e.g. "Pre'sident" instead of "president") because of
  // Johnson's stress-mark apostrophes. Reconcile those now.
  // ---------------------------------------------------------------------
  (function migrateUncategorized() {
    if (!db.uncategorized || !db.uncategorized.length) return;
    const stillUnmatched = [];
    let recovered = 0;
    for (const rec of db.uncategorized) {
      const match = findWordEntry(rec.word);
      if (match && match.entry.status !== 'done') {
        match.entry.definition = rec.definition;
        match.entry.edition = rec.edition || '1755';
        match.entry.source_url = rec.source_url || match.entry.source_url;
        match.entry.status = 'done';
        recovered++;
      } else if (!match) {
        stillUnmatched.push(rec);
      }
      // if match already done, just drop the duplicate leftover record
    }
    if (recovered > 0) {
      db.uncategorized = stillUnmatched;
      saveDB(db);
      toast(`Recovered ${recovered} previously mis-filed word(s) into your list.`);
    }
  })();

  // ---------------------------------------------------------------------
  // 2. Flat, priority-ordered list of every word across all 8 tiers.
  // ---------------------------------------------------------------------
  function flatList() {
    const list = [];
    const tierKeys = Object.keys(db.tiers).sort((a, b) => Number(a) - Number(b));
    for (const tierKey of tierKeys) {
      const tier = db.tiers[tierKey];
      for (const entry of tier.words) {
        if (!entry.status) entry.status = entry.definition ? 'done' : 'pending';
        list.push({ entry, tierKey, tierName: tier.tier_name });
      }
    }
    return list;
  }

  function normalizeWord(w) {
    // Johnson's Dictionary marks stressed syllables with an apostrophe
    // (e.g. "Pre'sident") and sometimes hyphens between syllables.
    // Strip anything that isn't a plain letter so "Pre'sident" matches
    // the clean "president" entry already in the list.
    return w.trim().toLowerCase().replace(/[^a-z]/g, '');
  }

  function findWordEntry(word) {
    const target = normalizeWord(word);
    if (!target) return null;
    for (const item of flatList()) {
      if (normalizeWord(item.entry.word) === target) return item;
    }
    return null;
  }

  function getSkipped() {
    return GM_getValue('skipped_words', []);
  }
  function setSkipped(arr) {
    GM_setValue('skipped_words', arr);
  }

  function getCurrentQueueItem() {
    const list = flatList();
    const skipped = getSkipped();
    let idx = list.findIndex(item => item.entry.status === 'pending' && !skipped.includes(item.entry.word));
    let allSkipped = false;
    if (idx === -1) {
      // Every remaining pending word has been skipped — fall back to the
      // skipped ones so the queue isn't stuck empty.
      idx = list.findIndex(item => item.entry.status === 'pending');
      allSkipped = idx !== -1;
    }
    if (idx === -1) return { item: null, index: -1, total: list.length, allSkipped: false };
    return { item: list[idx], index: idx, total: list.length, allSkipped };
  }

  // ---------------------------------------------------------------------
  // 3. Parsing a highlighted selection into word + definition.
  // ---------------------------------------------------------------------
  function splitSelection(raw) {
    const text = raw.trim().replace(/\s+/g, ' ');
    const match = text.match(/^([A-Za-z'-]+)\.?\s*(.*)$/);
    if (match && match[2]) return { word: match[1], definition: match[2].trim() };
    return { word: '', definition: text };
  }

  // ---------------------------------------------------------------------
  // 4. Toast notification.
  // ---------------------------------------------------------------------
  function toast(message, isError) {
    const el = document.createElement('div');
    el.textContent = message;
    el.style.cssText = `
      position: fixed; bottom: 24px; right: 24px; z-index: 999999;
      background: ${isError ? '#7a1f1f' : '#1f3d2b'}; color: #f5f0e6;
      padding: 12px 18px; border-radius: 6px; font-family: Georgia, serif;
      font-size: 14px; max-width: 320px; box-shadow: 0 4px 14px rgba(0,0,0,0.3);
      transition: opacity 0.4s;
    `;
    document.body.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; }, 2200);
    setTimeout(() => { el.remove(); }, 2700);
  }

  // ---------------------------------------------------------------------
  // 5. Custom right-click capture menu.
  // ---------------------------------------------------------------------
  let menuEl = null;
  function removeMenu() { if (menuEl) { menuEl.remove(); menuEl = null; } }

  function showMenu(x, y, selectedText) {
    removeMenu();
    const { word, definition } = splitSelection(selectedText);
    const match = word ? findWordEntry(word) : null;

    menuEl = document.createElement('div');
    menuEl.style.cssText = `
      position: fixed; top: ${y}px; left: ${x}px; z-index: 999999;
      background: #fdfaf3; border: 1px solid #b8a888; border-radius: 6px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.25); font-family: Georgia, serif;
      font-size: 14px; color: #2b2418; min-width: 240px; overflow: hidden;
    `;

    const header = document.createElement('div');
    header.style.cssText = 'padding:10px 14px; background:#e9e0cc; font-weight:bold; border-bottom:1px solid #b8a888;';
    header.textContent = match ? `Match found: "${match.entry.word}"` : (word ? `New word: "${word}"` : 'Add to Word Database');
    menuEl.appendChild(header);

    function addOption(label, onClick) {
      const opt = document.createElement('div');
      opt.textContent = label;
      opt.style.cssText = 'padding:10px 14px; cursor:pointer;';
      opt.addEventListener('mouseenter', () => opt.style.background = '#e9e0cc');
      opt.addEventListener('mouseleave', () => opt.style.background = 'transparent');
      opt.addEventListener('click', onClick);
      menuEl.appendChild(opt);
    }

    addOption("➕ Add as Johnson's 1755 definition", () => saveCapture(word, definition, match, '1755', selectedText));
    addOption("➕ Add as Johnson's 1773 definition", () => saveCapture(word, definition, match, '1773', selectedText));
    addOption('✎ Edit word / definition before saving', () => promptEdit(word, definition, match, selectedText));
    addOption('✕ Cancel', removeMenu);

    document.body.appendChild(menuEl);
  }

  function promptEdit(word, definition, match, raw) {
    removeMenu();
    const newWord = window.prompt('Headword:', word || '');
    if (newWord === null) return;
    const newDef = window.prompt("Definition (Johnson's wording):", definition || raw);
    if (newDef === null) return;
    const edition = window.prompt('Edition — type 1755 or 1773:', '1755');
    if (edition === null) return;
    saveCapture(newWord, newDef, findWordEntry(newWord), edition.trim(), raw);
  }

  function saveCapture(word, definition, match, edition, raw) {
    removeMenu();
    if (!word) { toast('Could not detect a headword — try "Edit before saving".', true); return; }
    if (!definition) { toast('No definition text found in your selection.', true); return; }

    if (match) {
      match.entry.definition = definition;
      match.entry.edition = edition || '1755';
      match.entry.source_url = window.location.href;
      match.entry.status = 'done';
      removeFromSkipped(match.entry.word);
      toast(`Saved: "${word}" → Tier ${match.tierKey} (${match.tierName})`);
    } else {
      db.uncategorized = db.uncategorized || [];
      db.uncategorized.push({
        word, definition, edition: edition || '1755',
        source_url: window.location.href,
        captured_at: new Date().toISOString(), raw_selection: raw
      });
      toast(`Saved: "${word}" (not in your 1,075-word list — filed separately)`);
    }

    saveDB(db);
    refreshQueuePanel();
  }

  document.addEventListener('contextmenu', function (e) {
    const selection = window.getSelection().toString();
    if (selection && selection.trim().length > 0) {
      e.preventDefault();
      showMenu(e.clientX, e.clientY, selection);
    }
  });
  document.addEventListener('click', function (e) {
    if (menuEl && !menuEl.contains(e.target)) removeMenu();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') removeMenu();
  });

  // ---------------------------------------------------------------------
  // 6. Priority Queue Panel — one word at a time, copy button, no typing.
  // ---------------------------------------------------------------------
  let panelEl = null;
  let panelVisible = GM_getValue('panel_visible', true);

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        () => toast(`Copied "${text}" — paste it into the search box.`),
        () => fallbackCopy(text)
      );
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); toast(`Copied "${text}"`); }
    catch (e) { toast('Could not copy automatically — please select manually.', true); }
    ta.remove();
  }

  function markUnlisted(item) {
    item.entry.status = 'unlisted';
    item.entry.definition = '';
    removeFromSkipped(item.entry.word);
    saveDB(db);
    toast(`Marked "${item.entry.word}" as unlisted — needs further investigation.`);
    refreshQueuePanel();
  }

  function skipWord(item) {
    const skipped = getSkipped();
    if (!skipped.includes(item.entry.word)) {
      skipped.push(item.entry.word);
      setSkipped(skipped);
    }
    toast(`Skipped "${item.entry.word}" for now — it'll come back around later.`);
    refreshQueuePanel();
  }

  function removeFromSkipped(word) {
    const skipped = getSkipped().filter(w => w !== word);
    setSkipped(skipped);
  }

  function buildPanel() {
    if (panelEl) panelEl.remove();

    panelEl = document.createElement('div');
    panelEl.style.cssText = `
      position: fixed; bottom: 24px; left: 24px; z-index: 999998;
      background: #fdfaf3; border: 2px solid #6b5637; border-radius: 8px;
      box-shadow: 0 6px 24px rgba(0,0,0,0.3); font-family: Georgia, serif;
      color: #2b2418; width: 300px; padding: 14px 16px;
    `;
    panelEl.id = 'cwd-queue-panel';
    document.body.appendChild(panelEl);
    renderPanelContent();
  }

  function renderPanelContent() {
    if (!panelEl) return;
    panelEl.innerHTML = '';

    const { item, index, total, allSkipped } = getCurrentQueueItem();

    const closeBtn = document.createElement('div');
    closeBtn.textContent = '✕';
    closeBtn.style.cssText = 'position:absolute; top:6px; right:10px; cursor:pointer; font-size:13px; color:#7a6a4d;';
    closeBtn.addEventListener('click', () => {
      panelVisible = false;
      GM_setValue('panel_visible', false);
      panelEl.remove();
      panelEl = null;
    });
    panelEl.style.position = 'fixed';
    panelEl.appendChild(closeBtn);

    if (!item) {
      const done = document.createElement('div');
      done.style.cssText = 'font-weight:bold; text-align:center; padding:10px 0;';
      done.textContent = '🎉 All words are done or marked unlisted!';
      panelEl.appendChild(done);
      return;
    }

    const progress = document.createElement('div');
    progress.style.cssText = 'font-size:12px; color:#7a6a4d; margin-bottom:6px;';
    progress.textContent = `Word ${index + 1} of ${total} · Tier ${item.tierKey}: ${item.tierName}`;
    panelEl.appendChild(progress);

    if (allSkipped) {
      const note = document.createElement('div');
      note.style.cssText = 'font-size:11px; color:#7a1f1f; margin-bottom:8px;';
      note.textContent = "Everything left was skipped — showing skipped words again.";
      panelEl.appendChild(note);
    }

    const wordEl = document.createElement('div');
    wordEl.style.cssText = 'font-size:26px; font-weight:bold; margin:6px 0 12px 0; word-break: break-word;';
    wordEl.textContent = item.entry.word;
    panelEl.appendChild(wordEl);

    const copyBtn = document.createElement('button');
    copyBtn.textContent = '📋 Copy word';
    copyBtn.style.cssText = 'width:100%; padding:9px; margin-bottom:10px; background:#3a3226; color:#f5f0e6; border:none; border-radius:5px; cursor:pointer; font-size:14px; font-family: Georgia, serif;';
    copyBtn.addEventListener('click', () => copyToClipboard(item.entry.word));
    panelEl.appendChild(copyBtn);

    const pasteLabel = document.createElement('div');
    pasteLabel.style.cssText = 'font-size:12px; color:#3a3226; margin-bottom:4px;';
    pasteLabel.textContent = 'Paste the definition you copied from the page:';
    panelEl.appendChild(pasteLabel);

    const pasteBox = document.createElement('textarea');
    pasteBox.style.cssText = 'width:100%; min-height:70px; padding:8px; margin-bottom:8px; font-family: Georgia, serif; font-size:13px; border:1px solid #b8a888; border-radius:5px; box-sizing:border-box; resize:vertical;';
    pasteBox.placeholder = 'Paste here (Ctrl+V)';
    panelEl.appendChild(pasteBox);

    const saveBtn = document.createElement('button');
    saveBtn.textContent = '✓ Found & Saved — Next Word';
    saveBtn.style.cssText = 'width:100%; padding:12px; margin-bottom:8px; background:#1f3d2b; color:#f5f0e6; border:none; border-radius:5px; cursor:pointer; font-size:15px; font-weight:bold; font-family: Georgia, serif;';
    saveBtn.addEventListener('click', () => {
      const def = pasteBox.value.trim();
      if (!def) {
        toast('Paste the definition into the box first — nothing was saved.', true);
        return;
      }
      item.entry.definition = def;
      item.entry.status = 'done';
      item.entry.source_url = window.location.href;
      if (!item.entry.edition) item.entry.edition = '1755';
      removeFromSkipped(item.entry.word);
      saveDB(db);
      toast(`Saved "${item.entry.word}" with its definition. Next word.`);
      refreshQueuePanel();
    });
    panelEl.appendChild(saveBtn);

    const unlistedBtn = document.createElement('button');
    unlistedBtn.textContent = '⚠ Not found — needs further investigation';
    unlistedBtn.style.cssText = 'width:100%; padding:9px; background:#7a1f1f; color:#f5f0e6; border:none; border-radius:5px; cursor:pointer; font-size:13px; font-family: Georgia, serif;';
    unlistedBtn.addEventListener('click', () => markUnlisted(item));
    panelEl.appendChild(unlistedBtn);

    const listBtn = document.createElement('button');
    listBtn.textContent = '📜 View full word list';
    listBtn.style.cssText = 'width:100%; padding:8px; margin-bottom:8px; background:#3a3226; color:#f5f0e6; border:none; border-radius:5px; cursor:pointer; font-size:12px; font-family: Georgia, serif;';
    listBtn.addEventListener('click', openListViewer);
    panelEl.appendChild(listBtn);

    const hint = document.createElement('div');
    hint.style.cssText = 'font-size:11px; color:#7a6a4d; margin-top:10px; line-height:1.4;';
    hint.textContent = 'Paste the word into the search box above, find the entry, highlight word + definition, right-click, and save. This panel jumps to the next word automatically. Use "Next word" to skip one for now without losing your place.';
    panelEl.appendChild(hint);
  }

  function refreshQueuePanel() {
    if (panelVisible) renderPanelContent();
  }

  // ---------------------------------------------------------------------
  // 6b. Full Word List Viewer — see every word, its tier, its status,
  //     and fix any stuck entries by hand.
  // ---------------------------------------------------------------------
  let listModalEl = null;

  function statusColor(status) {
    if (status === 'done') return '#1f3d2b';
    if (status === 'unlisted') return '#7a1f1f';
    return '#7a6a4d';
  }
  function statusLabel(status) {
    if (status === 'done') return 'DONE';
    if (status === 'unlisted') return 'UNLISTED';
    return 'PENDING';
  }

  function openListViewer() {
    closeListViewer();

    listModalEl = document.createElement('div');
    listModalEl.style.cssText = `
      position: fixed; top: 5%; left: 50%; transform: translateX(-50%);
      width: 90%; max-width: 640px; height: 85%; z-index: 9999999;
      background: #fdfaf3; border: 2px solid #6b5637; border-radius: 8px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.4); font-family: Georgia, serif;
      color: #2b2418; display: flex; flex-direction: column; overflow: hidden;
    `;

    const header = document.createElement('div');
    header.style.cssText = 'padding:12px 16px; background:#e9e0cc; border-bottom:1px solid #b8a888; display:flex; justify-content:space-between; align-items:center;';
    const title = document.createElement('div');
    title.style.cssText = 'font-weight:bold; font-size:16px;';
    title.textContent = 'Full Word List';
    header.appendChild(title);
    const closeBtn = document.createElement('div');
    closeBtn.textContent = '✕';
    closeBtn.style.cssText = 'cursor:pointer; font-size:16px; padding:0 6px;';
    closeBtn.addEventListener('click', closeListViewer);
    header.appendChild(closeBtn);
    listModalEl.appendChild(header);

    const searchBar = document.createElement('div');
    searchBar.style.cssText = 'padding:10px 16px; border-bottom:1px solid #b8a888;';
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Search words...';
    searchInput.style.cssText = 'width:100%; padding:7px 10px; font-size:14px; border:1px solid #b8a888; border-radius:4px; font-family: Georgia, serif; box-sizing: border-box;';
    searchBar.appendChild(searchInput);
    listModalEl.appendChild(searchBar);

    const filterBar = document.createElement('div');
    filterBar.style.cssText = 'padding:0 16px 10px 16px; display:flex; gap:6px; border-bottom:1px solid #b8a888;';
    let activeFilter = 'all';
    const filters = [['all', 'All'], ['pending', 'Pending'], ['done', 'Done'], ['unlisted', 'Unlisted']];
    const filterBtns = {};
    filters.forEach(([key, label]) => {
      const b = document.createElement('button');
      b.textContent = label;
      b.style.cssText = 'padding:4px 10px; font-size:12px; border-radius:4px; border:1px solid #b8a888; cursor:pointer; background:' + (key === 'all' ? '#6b5637' : '#fdfaf3') + '; color:' + (key === 'all' ? '#f5f0e6' : '#2b2418') + ';';
      b.addEventListener('click', () => {
        activeFilter = key;
        Object.keys(filterBtns).forEach(k => {
          filterBtns[k].style.background = k === activeFilter ? '#6b5637' : '#fdfaf3';
          filterBtns[k].style.color = k === activeFilter ? '#f5f0e6' : '#2b2418';
        });
        renderRows();
      });
      filterBtns[key] = b;
      filterBar.appendChild(b);
    });
    listModalEl.appendChild(filterBar);

    const listBody = document.createElement('div');
    listBody.style.cssText = 'flex: 1; overflow-y: auto; padding: 8px 12px;';
    listModalEl.appendChild(listBody);

    function renderRows() {
      listBody.innerHTML = '';
      const q = searchInput.value.trim().toLowerCase();
      for (const item of flatList()) {
        if (activeFilter !== 'all' && item.entry.status !== activeFilter) continue;
        if (q && !item.entry.word.toLowerCase().includes(q)) continue;

        const row = document.createElement('div');
        row.style.cssText = 'display:flex; align-items:center; gap:8px; padding:8px 6px; border-bottom:1px solid #e9e0cc;';

        const badge = document.createElement('div');
        badge.textContent = statusLabel(item.entry.status);
        badge.style.cssText = `font-size:10px; font-weight:bold; color:#fff; background:${statusColor(item.entry.status)}; padding:2px 6px; border-radius:3px; min-width:62px; text-align:center;`;
        row.appendChild(badge);

        const wordCol = document.createElement('div');
        wordCol.style.cssText = 'flex:1; min-width:0;';
        const wordText = document.createElement('div');
        wordText.textContent = `${item.entry.word}  (Tier ${item.tierKey})`;
        wordText.style.cssText = 'font-weight:bold; font-size:14px;';
        wordCol.appendChild(wordText);
        if (item.entry.definition) {
          const defText = document.createElement('div');
          defText.textContent = item.entry.definition.length > 80 ? item.entry.definition.slice(0, 80) + '…' : item.entry.definition;
          defText.style.cssText = 'font-size:11px; color:#7a6a4d; margin-top:2px;';
          wordCol.appendChild(defText);
        }
        row.appendChild(wordCol);

        const actions = document.createElement('div');
        actions.style.cssText = 'display:flex; gap:4px; flex-shrink:0;';

        function tinyBtn(label, bg, onClick) {
          const b = document.createElement('button');
          b.textContent = label;
          b.style.cssText = `font-size:11px; padding:5px 7px; border:none; border-radius:4px; background:${bg}; color:#fff; cursor:pointer;`;
          b.addEventListener('click', onClick);
          return b;
        }

        actions.appendChild(tinyBtn('📋', '#3a3226', () => copyToClipboard(item.entry.word)));
        if (item.entry.status !== 'done') {
          actions.appendChild(tinyBtn('✓', '#1f3d2b', () => {
            const def = window.prompt(`Definition for "${item.entry.word}" (Johnson's wording):`, item.entry.definition || '');
            if (def === null || !def.trim()) return;
            item.entry.definition = def.trim();
            item.entry.status = 'done';
            item.entry.source_url = window.location.href;
            removeFromSkipped(item.entry.word);
            saveDB(db);
            toast(`Marked "${item.entry.word}" done.`);
            renderRows();
            refreshQueuePanel();
          }));
        }
        if (item.entry.status !== 'unlisted') {
          actions.appendChild(tinyBtn('⚠', '#7a1f1f', () => { markUnlisted(item); renderRows(); }));
        }
        if (item.entry.status !== 'pending') {
          actions.appendChild(tinyBtn('↺', '#7a6a4d', () => {
            item.entry.status = 'pending';
            saveDB(db);
            toast(`Reset "${item.entry.word}" to pending.`);
            renderRows();
            refreshQueuePanel();
          }));
        }

        row.appendChild(actions);
        listBody.appendChild(row);
      }
      if (!listBody.children.length) {
        const empty = document.createElement('div');
        empty.style.cssText = 'padding:20px; text-align:center; color:#7a6a4d; font-size:13px;';
        empty.textContent = 'No words match.';
        listBody.appendChild(empty);
      }
    }

    searchInput.addEventListener('input', renderRows);
    renderRows();

    document.body.appendChild(listModalEl);
  }

  function closeListViewer() {
    if (listModalEl) { listModalEl.remove(); listModalEl = null; }
  }


  // from storage — reloading here was the bug that lost captures: it swapped
  // out the in-memory db object out from under any capture that was still
  // in progress (word highlighted, menu open, not yet clicked), silently
  // discarding the save when it finally happened.
  setInterval(() => { refreshQueuePanel(); }, 2000);

  if (panelVisible) buildPanel();

  GM_registerMenuCommand('📜 View Full Word List', function () {
    openListViewer();
  });

  GM_registerMenuCommand('🔄 Clear skipped list (bring skipped words back to front)', function () {
    setSkipped([]);
    toast('Skip list cleared.');
    refreshQueuePanel();
  });

  GM_registerMenuCommand('👁 Show/Hide Queue Panel', function () {
    panelVisible = !panelVisible;
    GM_setValue('panel_visible', panelVisible);
    if (panelVisible) buildPanel(); else if (panelEl) { panelEl.remove(); panelEl = null; }
  });

  // ---------------------------------------------------------------------
  // 7. Download your file whenever you want.
  // ---------------------------------------------------------------------
  GM_registerMenuCommand('📥 Download my word database (JSON)', function () {
    const blob = new Blob([JSON.stringify(db, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'constitution_words_tiered.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    toast('Downloaded your word database.');
  });

  GM_registerMenuCommand('🔎 Show progress (done / unlisted / pending)', function () {
    let done = 0, unlisted = 0, pending = 0;
    for (const item of flatList()) {
      if (item.entry.status === 'done') done++;
      else if (item.entry.status === 'unlisted') unlisted++;
      else pending++;
    }
    const extra = (db.uncategorized || []).length;
    alert(`Done: ${done}\nUnlisted (needs research): ${unlisted}\nPending: ${pending}\n\nPlus ${extra} extra word(s) outside the list.`);
  });

})();
