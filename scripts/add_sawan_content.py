#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Sawan / Shravan month pack: festival guides, stories, vrat kathas, aartis,
high-search temples, calendar dates, and engagement hooks.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))
from sync_groups import base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")


def save(name: str, data) -> None:
    path = DATA / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fest(**kw):
    return kw


def story(**kw):
    return kw


def devotion(**kw):
    return kw


# ── Festival guides ──────────────────────────────────────────────────────────

NEW_FESTIVALS = [
    fest(
        slug="shravan-sawan",
        name="Sawan / Shravan Month",
        nameHi="सावन / श्रावण मास",
        importance="high",
        dateNames=["Sawan", "Shravan", "Sawan Somwar", "Kanwar Yatra"],
        summary="The monsoon month of Shiva — Mondays, bel leaves, Ganga jal, and the living Bol Bam roads.",
        summaryHi="शिव का वर्षा मास — सोमवार व्रत, बेलपत्र, गंगाजल, और बोल बम की जीवंत राहें।",
        meaningEn=(
            "Sawan (Shravan) is among India’s most searched sacred months. In the rains, devotees "
            "turn to Shiva with water, milk, bilva leaves, and Monday fasts (Sawan Somwar). "
            "North India’s Kawariya / Bol Bam tradition — carrying Ganga water barefoot to "
            "Baidyanath, Basukinath, and countless village lingas — makes the month a moving "
            "pilgrimage. Regional calendars differ (Purnimanta vs Amanta), so always confirm "
            "local start and end dates."
        ),
        meaningHi=(
            "सावन (श्रावण) भारत के सर्वाधिक खोजे जाने वाले पवित्र मासों में है। वर्षा में भक्त "
            "शिव जी को जल, दूध, बिल्वपत्र और सोमवार व्रत से पूजते हैं। उत्तर भारत की कांवड़ / "
            "बोल बम परंपरा — गंगाजल पैदल बैद्यनाथ, बासुकीनाथ और गाँव-गाँव शिवलिंग तक — मास को "
            "चलती तीर्थयात्रा बनाती है। क्षेत्रीय पंचांग भिन्न हैं; स्थानीय आरंभ–समाप्ति अवश्य देखें।"
        ),
        storyEn=(
            "Popular memory links Sawan to Shiva as Neelkanth — the Lord who held the halahal "
            "poison so the worlds could live — and to Parvati Ji’s long tapasya for Mahadev. "
            "Monsoon water becomes abhishek; the bilva leaf becomes a whispered Om Namah Shivaya. "
            "Kawariyas say each step with the kanwar is itself a mantra. The month closes in many "
            "north Indian homes with Shravan Purnima — Raksha Bandhan — folding sibling protection "
            "into Shiva’s season of cooling grace."
        ),
        storyHi=(
            "लोकस्मृति सावन को नीलकंठ शिव से जोड़ती है — जिन्होंने हलाहल धारण कर लोक बचाए — और "
            "पार्वती जी की महादेव हेतु तपस्या से। वर्षा जल अभिषेक बनता है; बिल्वपत्र मंत्र। "
            "कांवड़िए कहते हैं — कांवड़ संग हर कदम ही जप है। अनेक उत्तर भारतीय घरों में मास "
            "श्रावण पूर्णिमा / रक्षाबंधन पर समेटता है — भाई–बहन रक्षा शिव की शीतल कृपा संग।"
        ),
        mythologyEn=(
            "Scriptural and folk strands meet: Samudra Manthan’s poison, Ganga resting in Shiva’s "
            "jata, and the belief that monsoon offerings cool the fierce heat of penance and ego. "
            "Pradosh evenings, Sawan Shivaratri, Nag Panchami, and Mangala Gauri Tuesdays punctuate "
            "the month. TirthaYatra pages retell these themes for home learning — not as temple edicts."
        ),
        mythologyHi=(
            "शास्त्र और लोक मिलते हैं: समुद्र मंथन का विष, जटा में गंगा, और विश्वास कि वर्षा अर्पण "
            "तप–अहंकार की उष्णता शीतल करता है। प्रदोष, सावन शिवरात्रि, नाग पंचमी, मंगला गौरी "
            "मंगलवार मास को बाँटते हैं। TirthaYatra घर की शिक्षा हेतु सार है — मंदिर आदेश नहीं।"
        ),
        deityStories=[
            {
                "deity": "Shiva",
                "deityHi": "शिव जी",
                "en": "Abhishek, bilva, Somwar vrat, and Bol Bam define living Shaiva Sawan.",
                "hi": "अभिषेक, बिल्व, सोमवार व्रत और बोल बम — जीवंत शैव सावन।",
            },
            {
                "deity": "Parvati / Gauri",
                "deityHi": "पार्वती / गौरी जी",
                "en": "Mangala Gauri and Hartalika Teej remember the Goddess’s steadfast vow for Shiva.",
                "hi": "मंगला गौरी और हरतालिका तीज — शिव हेतु देवी की अडिग प्रतिज्ञा।",
            },
            {
                "deity": "Ganga",
                "deityHi": "गंगा माता",
                "en": "Kawariyas lift Ganga jal as living prasadam for distant lingas.",
                "hi": "कांवड़िए गंगाजल को दूर शिवलिंगों का जीवंत प्रसाद मानकर उठाते हैं।",
            },
        ],
        howCelebratedEn=[
            "Keep Sawan Somwar (Monday) fast as health allows; offer water and bilva to Shiva",
            "Visit a Shiva temple or home linga; recite Om Jai Shiv Omkara / Shiva Chalisa",
            "If joining Kanwar Yatra: follow police routes, hydration, and temple queue rules",
            "Observe Nag Panchami, Pradosh, and Shravan Purnima / Rakhi per local panchang",
        ],
        howCelebratedHi=[
            "स्वास्थ्य अनुसार सावन सोमवार व्रत; शिव को जल–बिल्व अर्पण",
            "शिव मंदिर या घर शिवलिंग; ॐ जय शिव ओंकारा / शिव चालीसा",
            "कांवड़ यात्रा में पुलिस मार्ग, जलपान और कतार नियम मानें",
            "नाग पंचमी, प्रदोष, श्रावण पूर्णिमा / राखी — स्थानीय पंचांग से",
        ],
        diasporaEn=(
            "Abroad, temples run special Monday Rudrabhishek and livestream Sawan aartis. "
            "Homes keep a small copper kalash for abhishek and share bilva if available — or "
            "tulsi/water with the same intent when bilva is scarce."
        ),
        diasporaHi=(
            "विदेश में मंदिर विशेष सोमवार रुद्राभिषेक और सावन आरती लाइव रखते हैं। घर पर छोटे "
            "कलश से अभिषेक; बिल्व दुर्लभ हो तो तुलसी/जल उसी भाव से।"
        ),
        regions=[
            {"region": "North & East India", "notes": "Kanwar Yatra corridors — Sultanganj–Deoghar, Haridwar routes, UP–Bihar–Jharkhand."},
            {"region": "West & South India", "notes": "Amanta Shravan may fall later; temple abhishek and Somwar still central."},
            {"region": "Nepal", "notes": "Saun month draws huge crowds to Pashupatinath for special worship."},
            {"region": "Diaspora", "notes": "Monday temple programmes; home linga abhishek kits."},
        ],
        relatedDevotion=[
            "shiva-aarti",
            "shiva-chalisa",
            "lingashtakam",
            "sawan-somwar-vrat-katha",
            "mangala-gauri-vrat-katha",
            "ganga-aarti",
            "pradosh-vrat-katha",
        ],
        relatedTemples=[
            "vaidyanath-deoghar",
            "basukinath-temple",
            "ajgaibinath-sultanganj",
            "neelkanth-mahadev-rishikesh",
            "baba-garibnath-muzaffarpur",
            "pura-mahadev-baghpat",
            "kashi-vishwanath",
            "mahakaleshwar-ujjain",
            "kedarnath",
            "pashupatinath",
        ],
    ),
    fest(
        slug="nag-panchami",
        name="Nag Panchami",
        nameHi="नाग पंचमी",
        importance="high",
        dateNames=["Nag Panchami", "Naga Panchami"],
        summary="Shravan’s serpent day — milk, drawings, and honour for the Nagas bound to Shiva’s grace.",
        summaryHi="श्रावण की नाग तिथि — दूध, चित्रांकन, और शिव-नाग अनुग्रह का सम्मान।",
        meaningEn=(
            "Nag Panchami falls on Shravan Shukla Panchami in many regions. Families honour Naga "
            "deities with milk, flowers, and drawn serpent forms — seeking protection from fear "
            "and imbalance. Because Shiva is Nagabhushana (adorned with serpents), the day sits "
            "naturally inside Sawan’s Shaiva season."
        ),
        meaningHi=(
            "अनेक क्षेत्रों में नाग पंचमी श्रावण शुक्ल पंचमी को होती है। परिवार दूध–पुष्प और नाग "
            "चित्र से नाग देवताओं का सम्मान करते हैं। शिव नागभूषण हैं — अतः दिन सावन की शैव "
            "ऋतु में सहज बैठता है।"
        ),
        storyEn=(
            "Folk and Puranic tellings remember the Nagas as guardians of earth’s waters and "
            "treasures, and as beings wronged when humans forget kinship with wild life. One "
            "beloved strand recalls how devotion and restraint heal the wound between people and "
            "serpents. On this day many avoid digging earth or harming snakes, offering instead "
            "a quiet bowl of milk and a prayer for coexistence."
        ),
        storyHi=(
            "लोक–पुराण कथाएँ नागों को जल–निधि के रक्षक और उस संबंध की याद बताती हैं जो मनुष्य "
            "वन्य जीवन से भूल जाता है। प्रिय धारा कहती है — भक्ति और संयम घाव भरते हैं। इस दिन "
            "अनेक भूमि नहीं खोदते, सर्प नहीं सताते — दूध का कटोरा और सह-अस्तित्व की प्रार्थना।"
        ),
        mythologyEn=(
            "Vasuki of the ocean-churning, the serpents around Shiva’s neck, and regional Naga "
            "shrines feed the day’s imagery. TirthaYatra’s katha page is an original home retelling "
            "of these themes — confirm local custom with elders."
        ),
        mythologyHi=(
            "समुद्र मंथन के वासुकि, शिव की नाग-माला, और क्षेत्रीय नाग मंदिर दिन की छवि गढ़ते हैं। "
            "TirthaYatra कथा मूल घर-पुनर्कथन है — रीति बड़ों से पूछें।"
        ),
        deityStories=[
            {
                "deity": "Naga Devatas",
                "deityHi": "नाग देवता",
                "en": "Milk, flowers, and drawn naga forms are offered for protection and balance.",
                "hi": "रक्षा और संतुलन हेतु दूध, पुष्प, नाग चित्र अर्पण।",
            },
            {
                "deity": "Shiva",
                "deityHi": "शिव जी",
                "en": "As Nagabhushana, Shiva frames the day’s reverence inside Sawan worship.",
                "hi": "नागभूषण रूप में शिव इस दिन की श्रद्धा को सावन पूजा से जोड़ते हैं।",
            },
        ],
        howCelebratedEn=[
            "Morning puja of Naga image / anthill shrine as family custom allows",
            "Offer milk, flowers; avoid harming snakes; many skip ploughing/digging",
            "If it falls on Sawan Somwar (as in some years), combine with Shiva abhishek",
            "Read or hear the Nag Panchami katha at home",
        ],
        howCelebratedHi=[
            "परिवार रीति अनुसार नाग चित्र / रमे की पूजा",
            "दूध–पुष्प; सर्प न सताएँ; कई हल–खुदाई नहीं करते",
            "यदि सावन सोमवार पड़े तो शिव अभिषेक संग",
            "घर पर नाग पंचमी कथा सुनें/पढ़ें",
        ],
        diasporaEn="Temple halls draw naga motifs; apartments offer milk at a small picture altar and keep the day’s ahimsa intent.",
        diasporaHi="मंदिरों में नाग चित्र; फ्लैट में छोटे चित्र पर दूध और अहिंसा का भाव।",
        regions=[
            {"region": "North & West India", "notes": "Strong household observance in monsoon Shravan."},
            {"region": "South India", "notes": "Naga shrines and anthill worship have deep local forms."},
            {"region": "Diaspora", "notes": "Picture-altar puja; teach children coexistence, not fear."},
        ],
        relatedDevotion=["nag-panchami-vrat-katha", "shiva-aarti", "sawan-somwar-vrat-katha"],
        relatedTemples=["neelkanth-mahadev-rishikesh", "kukke-subramanya", "somnath", "kashi-vishwanath"],
    ),
    fest(
        slug="kanwar-yatra",
        name="Kanwar Yatra (Bol Bam)",
        nameHi="कांवड़ यात्रा (बोल बम)",
        importance="high",
        dateNames=["Kanwar Yatra", "Bol Bam", "Kawad Yatra", "Kawariya"],
        summary="Barefoot rivers of devotion — Ganga jal carried to Shiva in the rains of Sawan.",
        summaryHi="वर्षा में पैदल भक्ति की नदियाँ — सावन में शिव तक गंगाजल।",
        meaningEn=(
            "The Kanwar (Kawad) Yatra is the living heart of Sawan for millions. Devotees fetch "
            "Ganga water — famously from Sultanganj, Haridwar, Gaumukh routes, and other ghats — "
            "and carry it in decorated slings to offer at Baidyanath Deoghar, Basukinath, Kashi, "
            "and home-district Shiva temples. Chants of ‘Bol Bam’ pace the walk."
        ),
        meaningHi=(
            "कांवड़ यात्रा करोड़ों के लिए सावन का जीवंत हृदय है। भक्त गंगाजल — सुल्तानगंज, हरिद्वार "
            "आदि से — सजा कांवड़ में बैद्यनाथ देवघर, बासुकीनाथ, काशी और जिले के शिव मंदिरों तक "
            "ले जाते हैं। ‘बोल बम’ चलने की लय है।"
        ),
        storyEn=(
            "Tradition says the offering of unbroken Ganga jal to Shiva completes a vow of "
            "gratitude, healing, or penance. The kanwar must not touch the ground carelessly; "
            "fellow yatris help each other rest it on stands. The road becomes a temporary "
            "sangha — tea stalls, police corridors, first-aid tents, and midnight aarti. "
            "It is less a tourist trek than a moving vrata."
        ),
        storyHi=(
            "परंपरा कहती है — अविच्छिन्न गंगाजल शिव को चढ़ाना कृतज्ञता, आरोग्य या तप का व्रत पूरा "
            "करता है। कांवड़ लापरवाही से भूमि न छुए; साथी स्टैंड पर टिकाते हैं। सड़क अस्थायी संघ "
            "बनती है — चाय, पुलिस गलियारा, प्राथमिक चिकित्सा, मध्यरात्रि आरती। यह पर्यटन नहीं — "
            "चलता व्रत है।"
        ),
        mythologyEn=(
            "Mythic memory links the jal to Ganga’s descent through Shiva’s jata and to Neelkanth’s "
            "cooling grace. Historical scale of today’s yatra is modern and massive — plan with "
            "official advisories, not romance alone."
        ),
        mythologyHi=(
            "पौराणिक स्मृति जल को शिव जटा में गंगा अवतरण और नीलकंठ कृपा से जोड़ती है। आज की "
            "यात्रा का पैमाना आधुनिक और विशाल है — सरकारी सलाह से योजना करें।"
        ),
        deityStories=[
            {
                "deity": "Shiva (Baidyanath / local linga)",
                "deityHi": "शिव जी (बैद्यनाथ / स्थानीय लिंग)",
                "en": "The jal-abhishek at the destination is the vow’s seal.",
                "hi": "गंतव्य पर जलाभिषेक ही व्रत की मुहर है।",
            },
            {
                "deity": "Ganga",
                "deityHi": "गंगा माता",
                "en": "Source ghats are treated as the mother who travels with the kanwar.",
                "hi": "स्रोत घाट वह माता हैं जो कांवड़ संग चलती हैं।",
            },
        ],
        howCelebratedEn=[
            "Register / follow district police Kanwar routes where required",
            "Carry ORS, shoes that fit, reflective gear; rest the kanwar on proper stands",
            "Offer jal only at the vowed temple; accept prasadam without littering routes",
            "Read Sawan Somwar katha and Shiva aarti before or after the walk",
        ],
        howCelebratedHi=[
            "जहाँ जरूरी हो पुलिस कांवड़ मार्ग / पंजीकरण मानें",
            "ORS, ठीक जूते, रिफ्लेक्टिव; कांवड़ उचित स्टैंड पर",
            "जल केवल संकल्पित मंदिर पर; मार्ग स्वच्छ रखें",
            "यात्रा से पहले/बाद सावन सोमवार कथा और शिव आरती",
        ],
        diasporaEn="Diaspora devotees often sponsor jal-abhishek remotely at Deoghar or local Shiva temples, or walk a symbolic short kanwar to the nearest Ganga/temple tank.",
        diasporaHi="प्रवासी अक्सर देवघर/स्थानीय शिव मंदिर में जलाभिषेक करवाते हैं या निकट घाट तक प्रतीकात्मक कांवड़ ले जाते हैं।",
        regions=[
            {"region": "Bihar–Jharkhand", "notes": "Sultanganj → Deoghar / Basukinath classic corridor."},
            {"region": "Uttarakhand–UP–Delhi NCR", "notes": "Haridwar and other Ganga points; heavy monsoon traffic."},
            {"region": "All India", "notes": "Local district Shiva temples receive returning kanwars."},
        ],
        relatedDevotion=[
            "sawan-somwar-vrat-katha",
            "shiva-aarti",
            "ganga-aarti",
            "lingashtakam",
            "shiva-chalisa",
        ],
        relatedTemples=[
            "ajgaibinath-sultanganj",
            "vaidyanath-deoghar",
            "basukinath-temple",
            "baba-garibnath-muzaffarpur",
            "pura-mahadev-baghpat",
            "neelkanth-mahadev-rishikesh",
            "kashi-vishwanath",
        ],
    ),
]


# ── Stories ──────────────────────────────────────────────────────────────────

NEW_STORIES = [
    story(
        slug="bilva-leaf-shiva",
        title="Why the bilva leaf is offered to Shiva",
        titleHi="शिव जी को बिल्वपत्र क्यों चढ़ाते हैं",
        readSeconds=80,
        deity="shiva",
        tags=["ritual-why", "festival", "first-timer", "sawan"],
        hook="Three leaflets, one whisper of Om — the simplest gift of Sawan.",
        hookHi="तीन दल, एक ॐ का स्वर — सावन का सबसे सरल अर्पण।",
        whyRitual="Every Sawan Somwar and Shiva abhishek, bilva (bel) leaves are placed on the linga — a monsoon ritual searched across India and the diaspora.",
        whyRitualHi="हर सावन सोमवार और शिवाभिषेक पर बिल्वपत्र शिवलिंग पर रखा जाता है — भारत और प्रवास में खोजी जाने वाली वर्षा-रीति।",
        storyEn=(
            "Tradition says the bilva tree is dear to Shiva. Its triple leaf reminds devotees of "
            "the three eyes, the three gunas offered up, or the simple Trinity of creation–preservation–"
            "dissolution held in one cool green gift. In Sawan, when the rains soften stone and dust, "
            "people carry baskets of bel to temples. Some tell that even a single leaf offered with "
            "a steady mind outweighs elaborate wealth — because Shiva, the ascetic lord, receives "
            "what is pure more than what is priced. Children learn to wash the leaf, avoid torn ones "
            "if custom asks, and place it gently while saying Namah Shivaya. The myth is not botany "
            "alone; it is a monsoon lesson: cool the fierce with the simple."
        ),
        storyHi=(
            "परंपरा कहती है — बिल्व वृक्ष शिव को प्रिय है। तीन दल तीन नेत्र, तीन गुणों का समर्पण, "
            "या सृष्टि–स्थिति–संहार की एक शीतल हरित भेंट याद दिलाते हैं। सावन में जब वर्षा धूल "
            "धोती है, लोग बेल की टोकरियाँ मंदिर ले जाते हैं। कहा जाता है — स्थिर मन से एक पत्र "
            "भी भारी ऐश्वर्य से बढ़कर, क्योंकि तपस्वी शिव मूल्य नहीं शुद्धता देखते हैं। बच्चे "
            "पत्र धोते, रीति अनुसार फटा न चढ़ाएँ, नमः शिवाय कह धीरे रखें। कथा वनस्पति नहीं — "
            "वर्षा का पाठ: उग्र को सरल से शीतल करो।"
        ),
        takeaway="Offer one clean bilva leaf — or a sincere Namah Shivaya if leaves are scarce — on a Sawan Monday.",
        relatedDevotion=["shiva-aarti", "lingashtakam", "sawan-somwar-vrat-katha", "shiva-chalisa"],
        relatedFestivals=["shravan-sawan", "maha-shivaratri", "kanwar-yatra"],
        relatedTemples=["kashi-vishwanath", "mahakaleshwar-ujjain", "vaidyanath-deoghar", "neelkanth-mahadev-rishikesh"],
    ),
    story(
        slug="kanwar-ganga-shiva",
        title="The kanwar — why Ganga water walks to Shiva",
        titleHi="कांवड़ — गंगाजल शिव तक क्यों पैदल जाता है",
        readSeconds=90,
        deity="shiva",
        tags=["festival", "first-timer", "family", "sawan"],
        hook="A bamboo sling, two pots, and a road that turns into prayer.",
        hookHi="बाँस की कांवड़, दो गगरें, और प्रार्थना बनती सड़क।",
        whyRitual="Bol Bam / Kanwar Yatra is among India’s largest seasonal pilgrimages — searched every Sawan from Bihar to Haridwar corridors.",
        whyRitualHi="बोल बम / कांवड़ यात्रा भारत की विशालतम मौसमी यात्राओं में — हर सावन बिहार से हरिद्वार गलियारों तक खोजी जाती है।",
        storyEn=(
            "In living pilgrimage telling, the devotee becomes a moving river. Water drawn from "
            "Mother Ganga is carried so it does not ‘fall’ in pride — only in offering. The kanwar "
            "keeps two pots balanced; the yatri keeps anger and haste balanced. At the vow’s end, "
            "jal pours over the linga at Deoghar, Basukinath, Garibnath, Neelkanth, or a village "
            "shrine — and the heat of the year’s worries is imagined cooling like monsoon on stone. "
            "Mythic memory hears Ganga in Shiva’s jata and Neelkanth’s throat that once held fire. "
            "The story’s moral for home: if you cannot walk a hundred kilometres, walk one honest "
            "act of seva — carry water for someone thirsty, and whisper Bam."
        ),
        storyHi=(
            "जीवंत तीर्थकथा में भक्त चलती नदी बनता है। गंगा माता का जल ऐसे उठता है कि अहंकार से "
            "न गिरे — केवल अर्पण में। कांवड़ दो गगरें सँभालती; यात्री क्रोध और जल्दबाजी सँभालता। "
            "व्रत के अंत जल देवघर, बासुकीनाथ, गरीबनाथ, नीलकंठ या गाँव के लिंग पर उतरता — वर्ष भर "
            "की गर्मी पत्थर पर वर्षा-सी ठंडी कल्पित होती। पौराणिक स्मृति शिव जटा में गंगा और "
            "नीलकंठ कण्ठ सुनती है। घर का अर्थ: सौ कोस न चल सको तो एक ईमानदार सेवा चलो — प्यासे "
            "को जल दो, और बम कहो।"
        ),
        takeaway="This Sawan, offer water at a Shiva shrine — or fill a bottle for a roadside worker in Bam’s name.",
        relatedDevotion=["ganga-aarti", "shiva-aarti", "sawan-somwar-vrat-katha", "lingashtakam"],
        relatedFestivals=["kanwar-yatra", "shravan-sawan"],
        relatedTemples=[
            "ajgaibinath-sultanganj",
            "vaidyanath-deoghar",
            "basukinath-temple",
            "baba-garibnath-muzaffarpur",
            "neelkanth-mahadev-rishikesh",
        ],
    ),
    story(
        slug="parvati-sawan-tapasya",
        title="Parvati’s tapasya — the Goddess who won Shiva in the rains",
        titleHi="पार्वती जी की तपस्या — वर्षा में शिव को पाने वाली देवी",
        readSeconds=85,
        deity="devi",
        tags=["festival", "family", "first-timer", "sawan"],
        hook="Not ornaments first — ash, leaves, and unwavering Mondays of the heart.",
        hookHi="पहले आभूषण नहीं — भस्म, पत्र, और हृदय के अडिग सोमवार।",
        whyRitual="Sawan Somwar and Mangala Gauri vows remember Parvati Ji’s austerity for Shiva — among the most searched women’s vrats of the monsoon.",
        whyRitualHi="सावन सोमवार और मंगला गौरी व्रत पार्वती जी की तप याद करते हैं — वर्षा की सर्वाधिक खोजी स्त्री व्रतों में।",
        storyEn=(
            "After Sati’s fire, the Goddess returned as Parvati, daughter of the mountain, and "
            "chose tapasya over shortcuts. Tellings say she stood in heat and rain, ate sparingly, "
            "and held Shiva’s name when the world offered easier loves. Shiva, the yogi who had "
            "withdrawn into stillness, was moved not by display but by her steady truth. Their "
            "union becomes the icon of Grihastha and Yoga held together — fierce freedom and "
            "faithful partnership. In Sawan, when women keep Monday fasts or Tuesday Mangala Gauri "
            "worship, they retell this not as bargain but as courage: love that can wait without "
            "poisoning itself with envy."
        ),
        storyHi=(
            "सती की ज्वाला के बाद देवी पार्वती — पर्वतपुत्री — बनी और shortcut नहीं तप चुना। "
            "कथा कहती है — धूप–वर्षा में खड़ी रहीं, अल्प आहार, जब संसार सरल प्रेम दे शिव नाम "
            "थामे रहीं। योगी शिव प्रदर्शन नहीं, उनकी स्थिर सत्यता से द्रवित हुए। यह योग और "
            "गृहस्थ का संगम है — उग्र स्वतंत्रता और अडिग साझेदारी। सावन में सोमवार व्रत या "
            "मंगला गौरी पूजा करने वाली यह सौदा नहीं — साहस गाती हैं: प्रेम जो ईर्ष्या से विष "
            "न बनते हुए प्रतीक्षा करे।"
        ),
        takeaway="Keep one quiet Monday for Shiva–Parvati — fewer complaints, one sincere lamp.",
        relatedDevotion=["mangala-gauri-vrat-katha", "sawan-somwar-vrat-katha", "devi-aarti", "shiva-aarti"],
        relatedFestivals=["shravan-sawan", "hartalika-teej", "maha-shivaratri"],
        relatedTemples=["kedarnath", "kashi-vishwanath", "ambaji", "mansa-devi-panchkula"],
    ),
    story(
        slug="naga-shiva-ornament",
        title="Why Shiva wears the serpent",
        titleHi="शिव जी नाग क्यों धारण करते हैं",
        readSeconds=75,
        deity="shiva",
        tags=["ritual-why", "festival", "first-timer", "sawan"],
        hook="Fear becomes ornament when it rests at the Lord’s throat.",
        hookHi="भय आभूषण बन जाता है जब प्रभु के कण्ठ विश्राम करे।",
        whyRitual="Nag Panchami in Sawan and every Shiva image with a coiled naga point to this living icon — searched whenever monsoon snake-fear rises.",
        whyRitualHi="सावन की नाग पंचमी और नाग-मालाधारी शिव मूर्तियाँ इसी प्रतीक की ओर हैं — वर्षा में सर्पभय उठते ही खोजी जाती हैं।",
        storyEn=(
            "Artists place a serpent around Shiva’s neck — Vasuki or a nameless naga — not to "
            "frighten children but to teach mastery of panic. Poison and power sit close; Shiva "
            "is Neelkanth who held halahal without becoming hatred. On Nag Panchami, households "
            "offer milk and ask that wild fear turn into respect. The serpent is also kundalini "
            "imagery in some yogic readings — energy awake yet guided. For Sawan home puja, the "
            "lesson is gentle: do not crush what you fear; cool it with awareness, as monsoon "
            "cools stone."
        ),
        storyHi=(
            "कलाकार शिव कण्ठ पर नाग रखते हैं — वासुकि या अनाम — बच्चों को डराने नहीं, घबराहट "
            "पर विजय सिखाने। विष और शक्ति पास; शिव नीलकंठ जिन्होंने हलाहल धारा द्वेष बने बिना। "
            "नाग पंचमी पर घर दूध अर्पण कर प्रार्थना करते — जंगली भय सम्मान बने। योग में कभी यह "
            "कुण्डलिनी भी। सावन घर-पूजा का पाठ कोमल: जिसे डरते हो कुचलो नहीं; जागरूकता से शीतल "
            "करो, जैसे वर्षा पत्थर को।"
        ),
        takeaway="On Nag Panchami, teach a child one kind fact about snakes — and offer a drop of milk in prayer.",
        relatedDevotion=["nag-panchami-vrat-katha", "shiva-aarti", "pradosh-vrat-katha"],
        relatedFestivals=["nag-panchami", "shravan-sawan", "maha-shivaratri"],
        relatedTemples=["neelkanth-mahadev-rishikesh", "kukke-subramanya", "somnath", "kashi-vishwanath"],
    ),
    story(
        slug="rudraksha-tears-shiva",
        title="Rudraksha — the tears of Shiva",
        titleHi="रुद्राक्ष — शिव जी के अश्रु",
        readSeconds=70,
        deity="shiva",
        tags=["ritual-why", "festival", "sawan"],
        hook="A bead born of compassion — worn in Sawan as touchable prayer.",
        hookHi="करुणा से जन्मा मनका — सावन में छू सकने वाली प्रार्थना।",
        whyRitual="Rudraksha malas and abhishek are searched heavily in Shravan; Nepal’s Pashupatinath Saun season and Indian Jyotirlinga towns alike.",
        whyRitualHi="श्रावण में रुद्राक्ष माला और अभिषेक भारी खोजे जाते हैं — नेपाल पशुपति साउन और भारत के ज्योतिर्लिंग ठौर।",
        storyEn=(
            "One Puranic strand says rudraksha beads formed from Shiva’s tears of compassion "
            "for the world’s suffering. Wearers treat the mala as a mobile temple — each bead a "
            "count of Namah Shivaya. In Sawan, shops fill with strands; wise elders still say: "
            "the bead without conduct is only jewellery. The story returns you to Neelkanth’s "
            "heart — power that weeps for beings, not power that boasts."
        ),
        storyHi=(
            "एक पौराणिक धारा कहती है — जगत दुख देख शिव अश्रु रुद्राक्ष बने। धारण करने वाले माला "
            "को चलता मंदिर मानते — हर मनका नमः शिवाय। सावन में दुकानें भरतीं; बुजुर्ग कहते — "
            "आचार बिना मनका केवल गहना। कथा नीलकंठ हृदय लौटाती — प्राणियों हेतु अश्रु वाली शक्ति, "
            "डींग वाली नहीं।"
        ),
        takeaway="Touch a rudraksha or your throat and recite Om Namah Shivaya eleven times — tears become courage.",
        relatedDevotion=["shiva-chalisa", "shiva-aarti", "lingashtakam", "sawan-somwar-vrat-katha"],
        relatedFestivals=["shravan-sawan", "maha-shivaratri"],
        relatedTemples=["pashupatinath", "kedarnath", "kashi-vishwanath", "neelkanth-mahadev-rishikesh"],
    ),
]


# ── Devotion: aarti + vrat katha ─────────────────────────────────────────────

NEW_DEVOTION = [
    devotion(
        slug="lingashtakam",
        type="aarti",
        deity="shiva",
        sangrahLabel="लिंगाष्टकम्",
        title="Lingashtakam",
        titleHi="ब्रह्ममुरारि सुरार्चित लिङ्गम्",
        author="Traditional Sanskrit stotra",
        when="Sawan Mondays, Shiva abhishek, Pradosh, Maha Shivaratri",
        summary="Complete traditional eight-verse praise of the Shiva Linga — the most recited Sawan abhishek hymn after the aarti.",
        meaning="Lingashtakam glorifies the linga worshipped by Brahma and Vishnu, destroyer of suffering, adorned with bilva, and giver of devotion’s fruit. Ideal after jal-abhishek in Sawan.",
        relatedTemples=[
            "kashi-vishwanath",
            "mahakaleshwar-ujjain",
            "somnath",
            "vaidyanath-deoghar",
            "neelkanth-mahadev-rishikesh",
        ],
        completeText=True,
        verses=[
            "ब्रह्ममुरारि सुरार्चित लिङ्गं निरमलभासित शोभित लिङ्गम्।\nजन्मज दुःख विनाशक लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "देवमुनि प्रवरार्चित लिङ्गं कामदहं करुणाकर लिङ्गम्।\nरावण दर्प विनाशन लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "सर्व सुगन्ध सुलेपित लिङ्गं बुद्धि विवर्धन कारण लिङ्गम्।\nसिद्ध सुरासुर वन्दित लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "कनक महामणि भूषित लिङ्गं फनिपति वेष्टित शोभित लिङ्गम्।\nदक्ष सुयज्ञ विनाशन लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "कुङ्कुम चन्दन लेपित लिङ्गं पङ्कज हार सुशोभित लिङ्गम्।\nसञ्चित पाप विनाशन लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "देवगणार्चित सेवित लिङ्गं भावैर भक्ति भिरेव च लिङ्गम्।\nदिनकर कोटि प्रभाकर लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "अष्टदलोपरि वेष्टित लिङ्गं सर्व समुद्भव कारण लिङ्गम्।\nअष्ट दरिद्र विनाशन लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "सुरगुरु सुरवर पूजित लिङ्गं सुरवन पुष्प सदार्चित लिङ्गम्।\nपरात्परं परमात्मक लिङ्गं तत् प्रणमामि सदाशिव लिङ्गम्॥",
            "लिङ्गाष्टकमिदं पुण्यं यः पठेत् शिव सन्निधौ।\nशिवलोकमवाप्नोति शिवेन सह मोदते॥",
        ],
    ),
    devotion(
        slug="sawan-somwar-vrat-katha",
        type="vrat-katha",
        deity="shiva",
        sangrahLabel="सावन सोमवार व्रत",
        title="Sawan Somwar Vrat Katha",
        titleHi="सावन सोमवार व्रत कथा",
        author="Popular vow tradition · TirthaYatra original retelling",
        when="Mondays of Sawan / Shravan month (confirm local panchang)",
        summary="Original TirthaYatra retelling of the Monday Shiva vow of Sawan — Parvati’s tapasya, jal-abhishek, and the fruits of steady faith.",
        meaning=(
            "Sawan Somwar is the Monday fast and Shiva worship of the monsoon month. "
            "This page retells traditional themes for home learning — not a commercial katha book copy. "
            "Health first; partial fasts count when done with sincerity."
        ),
        relatedTemples=[
            "kashi-vishwanath",
            "mahakaleshwar-ujjain",
            "vaidyanath-deoghar",
            "neelkanth-mahadev-rishikesh",
            "baba-garibnath-muzaffarpur",
            "somnath",
        ],
        completeText=True,
        verses=[
            "॥ श्री गणेशाय नमः ॥\n॥ ॐ नमः शिवाय ॥\nसावन सोमवार व्रत कथा — श्रद्धा से पढ़ें। यह TirthaYatra का पारंपरिक भावों पर आधारित मौलिक पुनर्कथन है।",
            "श्रावण मास को सावन भी कहते हैं। इस मास के सोमवार शिव जी को विशेष प्रिय माने जाते हैं। भक्त जल, दूध, बिल्वपत्र और मंत्र जाप से शिवलिंग का अभिषेक करते हैं।",
            "लोक-परंपरा में कहा जाता है कि पार्वती जी ने शिव जी को पति रूप में पाने हेतु कठिन तप किया। वर्षा हो या धूप, उनका संकल्प नहीं टूटा। सावन के सोमवार उसी अडिग भक्ति की याद हैं।",
            "एक प्रचलित कथा-धारा में एक सुहागिनी / साधिका सोमवार व्रत से घर का संकट टालती है — जब तक वह अधीर होकर व्रत नहीं तोड़ती। अधूरे व्रत से विघ्न, पूर्ण श्रद्धा से शिव-कृपा — यही लोकशिक्षा है।",
            "दूसरी धारा नीलकंठ कथा से जुड़ती है। समुद्र मंथन का हलाहल विष शिव जी ने कण्ठ में धारण किया। सावन का शीतल जल उसी उग्रता को शांत अर्पण लगता है — भक्त अपने क्रोध-अहंकार का भी ‘विष’ उतारने की कामना करते हैं।",
            "व्रत विधि (परिवार रीति अनुसार): प्रातः स्नान-संकल्प। दिन भर सात्त्विक रहें — क्रोध, असत्य से दूर। सामर्थ्य हो तो उपवास या फलहार; स्वास्थ्य कमजोर हो तो दूध-फल संग नाम जप पर्याप्त।",
            "संध्या या प्रातः शिवलिंग / शिव-पार्वती चित्र पर जल चढ़ाएँ। बिल्वपत्र, धूप, दीप, सरल नैवेद्य। ‘ॐ नमः शिवाय’ या शिव चालीसा / ॐ जय शिव ओंकारा आरती करें।",
            "कांवड़ यात्रा वाले इसी मास गंगाजल ले शिव तक पैदल जाते हैं। घर बैठे भक्त भी एक लोटा जल श्रद्धा से चढ़ा सकते हैं — भाव यात्रा का सार है, दिखावा नहीं।",
            "व्रत पारण परिवार रीति से सायंकाल या अगली प्रातः करें। प्रसाद बाँटें। जो चारों सोमवार रखें, वे पूर्ण सावन सोमवार व्रत मानते हैं; एक सोमवार भी शुभारंभ है।",
            "फलश्रुति (श्रद्धा की भाषा में): मन की अशांति कम हो, घर में मधुरता आए, और शिव-पार्वती का आशीष संकल्प में बल दे — ऐसी कामना की जाती है।\n॥ हर हर महादेव · बोल बम ॥",
        ],
    ),
    devotion(
        slug="mangala-gauri-vrat-katha",
        type="vrat-katha",
        deity="devi",
        sangrahLabel="मंगला गौरी व्रत",
        title="Mangala Gauri Vrat Katha",
        titleHi="मंगला गौरी व्रत कथा",
        author="Popular vow tradition · TirthaYatra original retelling",
        when="Tuesdays of Sawan / Shravan (Mangala Gauri) — especially for married women; confirm local custom",
        summary="Original TirthaYatra retelling of the Sawan Tuesday Gauri vow — steadfast love, household grace, and Parvati’s blessing.",
        meaning="Mangala Gauri Vrat is observed on Tuesdays in Sawan in many regions, honouring Gauri–Parvati for marital harmony and courage. Original retelling for home puja learning.",
        relatedTemples=["ambaji", "mansa-devi-panchkula", "tuljapur-bhavani", "mahalaxmi-kolhapur", "kashi-vishwanath"],
        completeText=True,
        verses=[
            "॥ श्री गणेशाय नमः ॥\n॥ जय गौरी माता ॥\nमंगला गौरी व्रत कथा — TirthaYatra मौलिक पुनर्कथन।",
            "सावन के मंगलवार अनेक घरों में मंगला गौरी पूजा होती है। गौरी पार्वती जी का सौम्य रूप हैं — मंगल, सौभाग्य और अडिग प्रेम की देवी।",
            "कथा का हृदय पार्वती जी की तपस्या है। उन्होंने शिव जी को पाने के लिए आभूषण नहीं, तप चुना। मंगला गौरी व्रत उसी धैर्य की याद दिलाता है — जल्दबाजी नहीं, स्थिर श्रद्धा।",
            "लोककथाओं में एक स्त्री के संकट और गौरी कृपा से रक्षा का वर्णन आता है। विवरण क्षेत्र अनुसार बदलते हैं; शिक्षा एक है — सत्य, संयम और पति-परिवार के प्रति करुणा रखना।",
            "व्रत विधि: मंगलवार प्रातः स्नान। लाल/पीले वस्त्र रीति अनुसार। गौरी-गणेश या गौरी-शिव की स्थापना। हलदी, कुमकुम, फूल, मीठा नैवेद्य।",
            "दिन भर सात्त्विक व्रत — निर्जला तभी जब स्वास्थ्य अनुमति दे। सायंकाल आरती, कथा श्रवण, और सुहाग चिह्न रीति अनुसार अर्पण।",
            "अविवाहित भी भक्ति भाव से गौरी का स्मरण कर सकती हैं — व्रत का द्वार केवल एक अवस्था तक सीमित नहीं, भाव प्रधान है।",
            "सावन समाप्त होने पर कुछ परिवार उद्यापन / कथा-समाप्ति रीति रखते हैं। स्थानीय पुरोहित या बुजुर्ग रीति पूछें।",
            "फलश्रुति: घर में मंगलता, मन में धैर्य, और गौरी-शिव का आशीष — ऐसी प्रार्थना की जाती है।\n॥ जय मंगला गौरी माता ॥",
        ],
    ),
    devotion(
        slug="nag-panchami-vrat-katha",
        type="vrat-katha",
        deity="shiva",
        sangrahLabel="नाग पंचमी व्रत",
        title="Nag Panchami Vrat Katha",
        titleHi="नाग पंचमी व्रत कथा",
        author="Popular vow tradition · TirthaYatra original retelling",
        when="Shravan Shukla Panchami (Nag Panchami) — confirm city panchang",
        summary="Original TirthaYatra retelling of Nag Panchami — honouring Nagas, Shiva as Nagabhushana, and the vow of non-harm.",
        meaning="Nag Panchami katha themes: respect for serpent deities, milk offering, and coexistence. Original home retelling; regional stories differ.",
        relatedTemples=["neelkanth-mahadev-rishikesh", "kukke-subramanya", "somnath", "kashi-vishwanath"],
        completeText=True,
        verses=[
            "॥ श्री गणेशाय नमः ॥\n॥ नाग देवाय नमः ॥\nनाग पंचमी कथा — TirthaYatra मौलिक पुनर्कथन।",
            "श्रावण शुक्ल पंचमी को अनेक प्रदेश नाग पंचमी मानते हैं। नाग देवताओं को दूध, पुष्प और चित्र द्वारा सम्मान दिया जाता है।",
            "शिव जी नागभूषण हैं — कण्ठ पर नाग उनकी उग्रता पर विजय और भय के साक्षी हैं। इस दिन शैव भक्त शिव अभिषेक भी करते हैं, विशेष जब तिथि सावन सोमवार से मिले।",
            "लोककथाएँ बताती हैं कि जब मनुष्य अहंकार से पृथ्वी के रक्षकों को भूलता है, संकट आता है; जब श्रद्धा और अहिंसा लौटती है, कल्याण होता है। सर्प को क्रूरता से मारना इस दिन वर्जित माना जाता है।",
            "कुछ घर आटे या हल्दी से नाग चित्र बना पूजते हैं; कुछ वट/रमे पर दूध चढ़ाते हैं। रीति गाँव-गाँव भिन्न — बुजुर्गों की बात मानें।",
            "व्रत/पूजा: प्रातः स्नान। नाग चित्र या मंदिर दर्शन। दूध-पुष्प अर्पण। भूमि खुदाई और हल चलाना कई परंपराओं में आज नहीं करते।",
            "कथा सुनकर प्रसाद बाँटें। बच्चों को डराएँ नहीं — सिखाएँ कि जंगल के प्राणी भी सृष्टि के अंग हैं।",
            "फलश्रुति: भय शांत हो, घर सुरक्षित रहे, और नाग-शिव अनुग्रह से वर्षा ऋतु मंगलमय बीते — ऐसी कामना।\n॥ ॐ नमः शिवाय ॥",
        ],
    ),
]


# ── Temples ──────────────────────────────────────────────────────────────────

NEW_TEMPLES = [
    {
        "slug": "neelkanth-mahadev-rishikesh",
        "name": "Neelkanth Mahadev Temple, Rishikesh",
        "deity": "Lord Shiva (Neelkanth)",
        "location": "Neelkanth, near Rishikesh, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "नी",
        "famousFor": "Sawan Neelkanth yatra · poison-myth shrine above Rishikesh",
        "summary": "Hill shrine of Neelkanth Mahadev above Rishikesh — among Uttarakhand’s most searched Sawan Shiva temples.",
        "mythology": (
            "Named for Shiva as Neelkanth — the blue-throated Lord who held the halahal poison "
            "of the ocean-churning. Pilgrims climb or drive from Rishikesh for darshan, especially "
            "in Sawan when abhishek queues swell with monsoon devotion."
        ),
        "lat": 30.0786,
        "lng": 78.3411,
        "mapQuery": "Neelkanth Mahadev Temple Rishikesh",
        "nearestRail": "Rishikesh / Haridwar",
        "nearestAirport": "Dehradun (Jolly Grant)",
        "festivals": ["Sawan Somwar & Kanwar season", "Maha Shivaratri", "Nag Panchami"],
        "bestTime": "October–June for comfortable roads; Sawan is spiritually peak but monsoon-slippery.",
        "deityFamilies": ["shiva"],
        "officialWebsite": "https://uttarakhandtourism.gov.in/",
    },
    {
        "slug": "baba-garibnath-muzaffarpur",
        "name": "Baba Garibnath Temple, Muzaffarpur",
        "deity": "Lord Shiva (Garibnath)",
        "location": "Muzaffarpur, Bihar",
        "state": "Bihar",
        "glyph": "ग",
        "famousFor": "Bihar’s Sawan Bol Bam magnet · massive Kawariya footfall",
        "summary": "Muzaffarpur’s beloved Garibnath Shiva temple — a major Sawan Kanwar destination in north Bihar.",
        "mythology": (
            "Local devotion knows Garibnath as the compassionate Shiva of the poor (garib). "
            "In Sawan, Kawariyas throng for jal-abhishek; the temple becomes one of Bihar’s "
            "loudest Bol Bam centres outside the Deoghar corridor."
        ),
        "lat": 26.1197,
        "lng": 85.3910,
        "mapQuery": "Baba Garibnath Temple Muzaffarpur",
        "nearestRail": "Muzaffarpur Junction",
        "nearestAirport": "Patna / Darbhanga",
        "festivals": ["Sawan Kanwar / Bol Bam", "Maha Shivaratri", "Mondays year-round"],
        "bestTime": "October–March; Sawan has peak crowds and heat-rain mix — plan hydration.",
        "deityFamilies": ["shiva"],
        "officialWebsite": "https://tourism.bihar.gov.in/",
    },
    {
        "slug": "pura-mahadev-baghpat",
        "name": "Pura Mahadev Temple, Baghpat",
        "deity": "Lord Shiva (Pura Mahadev)",
        "location": "Pura Mahadev, Baghpat, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "पु",
        "famousFor": "West UP Kanwar route Shiva seat · huge Sawan search",
        "summary": "Historic Shiva temple on the west UP Kanwar belt near Baghpat — a major Sawan jal-abhishek stop.",
        "mythology": (
            "Pura Mahadev is counted among the important Shiva tirthas of the upper Doab. "
            "Sawan Kawariyas from Delhi–NCR and west UP corridors offer Ganga jal here; "
            "local lore ties the linga to ancient Mahadev worship on the Hindon–Yamuna plain."
        ),
        "lat": 28.9440,
        "lng": 77.2190,
        "mapQuery": "Pura Mahadev Temple Baghpat",
        "nearestRail": "Baghpat Road / Meerut",
        "nearestAirport": "Delhi (NCR)",
        "festivals": ["Sawan Kanwar season", "Maha Shivaratri", "Pradosh"],
        "bestTime": "October–March; Sawan is the pilgrimage peak — expect heavy security routes.",
        "deityFamilies": ["shiva"],
        "officialWebsite": "https://uptourism.gov.in/",
    },
]


def attach_portal(detail: dict) -> dict:
    state = detail.get("state", "")
    portal = PORTALS.get(state)
    if not portal:
        return detail
    sources = list(detail.get("sources", []))
    line = f"{portal['portalName']}: {portal['portalUrl']}"
    if line not in sources:
        sources = [line] + sources
    detail["sources"] = sources
    detail["statePortal"] = {
        "name": portal["portalName"],
        "url": portal["portalUrl"],
        "slug": portal["slug"],
    }
    if detail.get("officialWebsite") in ("https://tourism.gov.in/", "", None):
        detail["officialWebsite"] = portal["portalUrl"]
    return detail


def upsert_list(items: list, new_items: list, key: str = "slug") -> tuple[int, int]:
    by = {i[key]: i for i in items}
    added = updated = 0
    for n in new_items:
        if n[key] in by:
            by[n[key]].update(n)
            updated += 1
        else:
            items.append(n)
            added += 1
    return added, updated


def main() -> None:
    # Festivals
    guide = load_json(DATA / "festival-guide.json")
    a, u = upsert_list(guide["festivals"], NEW_FESTIVALS)
    # Refresh section lede mention
    sec = guide.get("section", {})
    lede = sec.get("lede", "")
    if "Sawan" not in lede and "Shravan" not in lede:
        sec["lede"] = (
            lede.rstrip(".")
            + ", plus Sawan/Shravan, Kanwar Yatra (Bol Bam), and Nag Panchami."
        )
        guide["section"] = sec
    save("festival-guide.json", guide)
    print(f"Festivals +{a} ~{u}")

    # Stories
    stories = load_json(DATA / "stories.json")
    a, u = upsert_list(stories["stories"], NEW_STORIES)
    save("stories.json", stories)
    print(f"Stories +{a} ~{u} (total {len(stories['stories'])})")

    # Devotion
    devotion_data = load_json(DATA / "devotion.json")
    a, u = upsert_list(devotion_data["items"], NEW_DEVOTION)
    # Update vrat lede
    vk = devotion_data.get("types", {}).get("vrat-katha", {})
    if vk and "Sawan" not in vk.get("lede", ""):
        vk["lede"] = (
            vk["lede"].rstrip(".")
            + ", Sawan Somwar, Mangala Gauri, and Nag Panchami."
        )
    at = devotion_data.get("types", {}).get("aarti", {})
    if at and "Lingashtakam" not in at.get("lede", ""):
        at["lede"] = at["lede"].rstrip(".") + ", and Lingashtakam for Shiva abhishek."
    save("devotion.json", devotion_data)
    print(f"Devotion +{a} ~{u}")

    # Calendar fixed dates (North India Purnimanta reference 2026; always verify)
    cal = load_json(DATA / "festivals.json")
    new_dates = [
        {
            "date": "2026-07-30",
            "name": "Sawan Begins (North India)",
            "nameHi": "सावन आरंभ (उत्तर भारत)",
            "importance": "high",
        },
        {
            "date": "2026-08-03",
            "name": "Sawan Somwar",
            "nameHi": "सावन सोमवार",
            "importance": "high",
        },
        {
            "date": "2026-08-10",
            "name": "Sawan Somwar",
            "nameHi": "सावन सोमवार",
            "importance": "high",
        },
        {
            "date": "2026-08-11",
            "name": "Sawan Shivaratri",
            "nameHi": "सावन शिवरात्रि",
            "importance": "high",
        },
        {
            "date": "2026-08-17",
            "name": "Nag Panchami / Sawan Somwar",
            "nameHi": "नाग पंचमी / सावन सोमवार",
            "importance": "high",
        },
        {
            "date": "2026-08-24",
            "name": "Sawan Somwar",
            "nameHi": "सावन सोमवार",
            "importance": "high",
        },
        {
            "date": "2026-08-28",
            "name": "Sawan Ends · Raksha Bandhan",
            "nameHi": "सावन समाप्ति · रक्षाबंधन",
            "importance": "high",
        },
    ]
    existing_dates = {(d["date"], d["name"]) for d in cal.get("fixed", [])}
    added_d = 0
    for d in new_dates:
        key = (d["date"], d["name"])
        # Allow updating Rakhi row note — skip exact dupes
        if key in existing_dates:
            continue
        # Avoid duplicate plain Raksha Bandhan on 2026-08-28
        if d["date"] == "2026-08-28" and any(
            x.get("date") == "2026-08-28" and "Raksha" in x.get("name", "") for x in cal["fixed"]
        ):
            # enrich existing rakhi entry name if plain
            for x in cal["fixed"]:
                if x.get("date") == "2026-08-28" and x.get("name") == "Raksha Bandhan":
                    x["name"] = "Raksha Bandhan · Sawan Purnima Ends"
                    x["nameHi"] = "रक्षाबंधन · सावन पूर्णिमा समाप्ति"
                    break
            continue
        cal["fixed"].append(d)
        added_d += 1
    cal["fixed"].sort(key=lambda x: x["date"])
    save("festivals.json", cal)
    print(f"Calendar dates +{added_d}")

    # Engagement hooks
    eng = load_json(DATA / "engagement.json")
    rot = eng.setdefault("dailyRotation", {})
    for key, slugs in {
        "aarti": ["lingashtakam", "shiva-aarti", "ganga-aarti"],
        "katha": [
            "sawan-somwar-vrat-katha",
            "mangala-gauri-vrat-katha",
            "nag-panchami-vrat-katha",
            "pradosh-vrat-katha",
            "maha-shivaratri-vrat-katha",
        ],
        "story": [
            "bilva-leaf-shiva",
            "kanwar-ganga-shiva",
            "parvati-sawan-tapasya",
            "naga-shiva-ornament",
            "rudraksha-tears-shiva",
            "neelkanth-poison",
            "ganga-avatarana",
        ],
    }.items():
        lst = rot.setdefault(key, [])
        for s in reversed(slugs):
            if s in lst:
                lst.remove(s)
            lst.insert(0, s)

    loved = eng.setdefault("socialProof", {}).setdefault("mostLoved", [])
    seasonal = {
        "type": "festival",
        "slug": "shravan-sawan",
        "label": "Sawan favourite",
        "blurb": "Mondays, bilva, and Bol Bam — Shiva’s monsoon month.",
    }
    loved = [x for x in loved if x.get("slug") != "shravan-sawan"]
    loved.insert(0, seasonal)
    eng["socialProof"]["mostLoved"] = loved[:8]

    challenges = eng.setdefault("challenges", [])
    if not any(c.get("id") == "sawan-somwar-4" for c in challenges):
        challenges.insert(
            0,
            {
                "id": "sawan-somwar-4",
                "title": "Sawan Somwar · four Mondays",
                "titleHi": "सावन सोमवार · चार सोमवार",
                "blurb": "Each Sawan Monday: jal + bilva (or water) for Shiva, aarti once, katha once. Health first.",
                "days": 4,
                "devotionSlug": "sawan-somwar-vrat-katha",
                "storySlug": "bilva-leaf-shiva",
            },
        )
    eng.setdefault("checklistPresets", {})["sawan"] = {
        "title": "My Sawan home checklist",
        "items": [
            "Note local Sawan start/end on a panchang",
            "Keep a copper/steel lota for Shiva abhishek",
            "Sawan Somwar: read katha + Om Jai Shiv Omkara",
            "Offer bilva or a sincere Namah Shivaya",
            "Optional: Ganga aarti listen / short kanwar seva",
            "Nag Panchami: milk offering + teach kindness about snakes",
            "Raksha Bandhan / Shravan Purnima closing thanks",
        ],
    }
    save("engagement.json", eng)
    print("Engagement updated")

    # Temples
    existing = {p.stem for p in TEMPLES.glob("*.json")}
    created = []
    for seed in NEW_TEMPLES:
        slug = seed["slug"]
        if slug in existing:
            print(" temple exists", slug)
            continue
        families = seed.pop("deityFamilies", ["shiva"])
        detail = base_detail(dict(seed))
        detail["deityFamilies"] = families
        detail["tier"] = "famous"
        detail["lastUpdated"] = "2026-08-11"
        detail["mythologySignificance"] = detail["mythology"] + (
            "\n\nPilgrimage literature treats this shrine as a Sawan tirtha — verify living custom "
            "with temple priests. Accounts here are TirthaYatra summaries of widely cited traditions."
        )
        detail["localBeliefs"] = (
            f"In Sawan, devotees throng {detail['name']} for jal-abhishek and Bol Bam vows. "
            "Queue discipline and monsoon safety are part of living belief as practice.\n\n"
            "Footfall notes are editorial signals from public pilgrimage reporting — not paid rankings."
        )
        detail["mythologyDisclaimer"] = (
            "Mythological accounts and local beliefs are drawn from Puranic traditions, epics, and "
            "widely recorded pilgrimage lore. Visitor figures are approximate. Verify with temple trusts."
        )
        detail = attach_portal(detail)
        dump_json(TEMPLES / f"{slug}.json", detail)
        created.append(slug)
        print(" + temple", slug)

    if created:
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "assign_deities.py")])
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "enrich_temple_content.py")])

    # Audio / video embeds for new devotion
    from add_devotion_audio import AUDIO  # type: ignore

    # extend map in devotion file via local apply
    EXTRA_AUDIO = {
        "lingashtakam": (None, "Lingashtakam full with lyrics"),
        "sawan-somwar-vrat-katha": (None, "Sawan Somwar Vrat Katha Hindi"),
        "mangala-gauri-vrat-katha": (None, "Mangala Gauri Vrat Katha Hindi"),
        "nag-panchami-vrat-katha": (None, "Nag Panchami Vrat Katha Hindi"),
    }
    # Patch add_devotion_audio AUDIO by writing into devotion items directly
    import urllib.parse

    devotion_data = load_json(DATA / "devotion.json")
    for item in devotion_data["items"]:
        slug = item["slug"]
        if slug not in EXTRA_AUDIO and slug not in AUDIO:
            continue
        vid, label = EXTRA_AUDIO.get(slug) or AUDIO.get(slug) or (None, item.get("title", slug))
        q = urllib.parse.quote(f"{item.get('titleHi', '')} {item.get('title', '')} full")
        search = f"https://www.youtube.com/results?search_query={q}"
        is_vrat = item.get("type") == "vrat-katha"
        if vid:
            item["audioUrl"] = f"https://www.youtube.com/embed/{vid}"
            item["audioWatchUrl"] = f"https://www.youtube.com/watch?v={vid}"
            item["audioLabel"] = label
        else:
            item["audioUrl"] = ""
            item["audioWatchUrl"] = search
            item["audioLabel"] = label
        item["audioNote"] = (
            "Popular YouTube recording to watch or listen while reading. Open on YouTube if the player does not load."
            if is_vrat
            else "Popular YouTube recording to listen while reading. Open on YouTube if the player does not load."
        )
    save("devotion.json", devotion_data)

    # Also update scripts/add_devotion_audio.py map for future runs
    audio_script = ROOT / "scripts" / "add_devotion_audio.py"
    text = audio_script.read_text(encoding="utf-8")
    if "sawan-somwar-vrat-katha" not in text:
        needle = '    "ahoi-ashtami-vrat-katha": ("8mGesAxcr_A", "Ahoi Ashtami Vrat Katha · Hindi"),\n}'
        insert = (
            '    "ahoi-ashtami-vrat-katha": ("8mGesAxcr_A", "Ahoi Ashtami Vrat Katha · Hindi"),\n'
            '    # Sawan / Shravan pack\n'
            '    "lingashtakam": (None, "Lingashtakam full with lyrics"),\n'
            '    "sawan-somwar-vrat-katha": (None, "Sawan Somwar Vrat Katha Hindi"),\n'
            '    "mangala-gauri-vrat-katha": (None, "Mangala Gauri Vrat Katha Hindi"),\n'
            '    "nag-panchami-vrat-katha": (None, "Nag Panchami Vrat Katha Hindi"),\n'
            "}"
        )
        if needle in text:
            audio_script.write_text(text.replace(needle, insert), encoding="utf-8")
            print("Updated add_devotion_audio.py map")

    print("Done. Created temples:", created)


if __name__ == "__main__":
    main()
