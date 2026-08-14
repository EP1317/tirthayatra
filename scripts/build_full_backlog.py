#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build ALL remaining TirthaYatra content backlog items (idempotent)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES_DIR = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))
from sync_groups import base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")

DISCLAIMER_EN = (
    "This is an original TirthaYatra retelling drawn from widely cited Puranic, epic, and folk "
    "strands for learning and home devotion. It is not a verbatim scripture quotation, not a "
    "substitute for a guru or family priest, and not affiliated with any temple trust. Tellings differ; learn with humility."
)
DISCLAIMER_HI = (
    "यह TirthaYatra की मूल पुनर्लेखन है — पुराण, इतिहास, लोक परंपराओं से — घर भक्ति व सीख हेतु। "
    "शब्दशः शास्त्र नहीं; गुरु–पुजारी का स्थान नहीं लेती; किसी मंदिर ट्रस्ट से संबद्ध नहीं। कथाएँ भिन्न; विनम्रता से सीखें।"
)


def word_count(text: str) -> int:
    return len(text.split())


def read_seconds_from_detail(detail_en: str, minimum: int = 300) -> int:
    """~200 wpm reading pace for long detail."""
    secs = max(minimum, int(word_count(detail_en) / 200 * 60))
    return min(600, max(360, secs)) if minimum >= 360 else max(minimum, min(600, secs))


def craft_expansion_en(story: dict) -> str:
    title = story["title"]
    hook = story["hook"]
    why = story["whyRitual"]
    core = story["storyEn"]
    take = story["takeaway"]
    deity = story["deity"]
    tags = ", ".join(story.get("tags", []))
    extra = story.get("_detailExtraEn", "")
    return f"""{extra}When families gather for {deity} bhakti, the story of "{title}" often unfolds in layers. Elder tellings begin not with dates but with a question children ask after the short katha: what does this mean for our lamp, our festival plate, our quiet hour before sleep? Tags like {tags} on this page signal how pilgrims and householders search — ritual-why, festival memory, or first-timer entry.

The image that stays is the one named in the opening hook — {hook} In North Indian shrines, South Indian kathakaligals, Bengali pala gaan, and Gujarati home kathas, the emphasis shifts: some elders stress cosmic scale, others the domestic lesson. All agree the tale belongs to living devotion, not a single frozen text.

{why} Households repeat this when linking story to ritual so children understand that puja is memory, not habit alone.

The narrative heart, told slowly, runs like this: {core}

Some tellings add local colour — a river name, a hill, a saint's couplet — that does not appear in every Puranic redaction. That is normal. Puranic redactions, sthala-purana, grandmother's versions, and diaspora tellings do not always match line for line. Some regions omit a character; others add a folk verse. TirthaYatra respects that plurality — we do not claim one list or one temple tradition is the only true account.

For home practice, families adapt without diluting respect: {take} Light a lamp, read the short version on busy days, and return to this fuller telling when children ask "why again?" If your family custom differs, honour the priest or elder who guides you — this page is a companion, not a command.

{DISCLAIMER_EN}"""


def craft_expansion_hi(story: dict) -> str:
    title = story["titleHi"]
    hook = story["hookHi"]
    why = story["whyRitualHi"]
    core = story["storyHi"]
    take = story["takeaway"]
    deity = story["deity"]
    tags = ", ".join(story.get("tags", []))
    extra = story.get("_detailExtraHi", "")
    rel_f = ", ".join(story.get("relatedFestivals", [])[:3]) or "आपकी स्थानीय परंपरा"
    rel_t = ", ".join(story.get("relatedTemples", [])[:3]) or "नजदीकी मंदिर"
    return f"""{extra}जब परिवार {deity} भक्ति में इकट्ठा होता है, "{title}" की कथा अक्सर परतों में खुलती है। बुजुर्ग प्रश्न से शुरू करते हैं — छोटी कथा के बाद बच्चा पूछता है: हमारे दीप, व्रत थाली, या शांत घंटे का क्या अर्थ? {tags} जैसे विषय इस पृष्ठ की दिशा बताते हैं।

जो छवि रुकती है वह प्रारंभिक हुक में है — {hook} उत्तर भारत, दक्षिण भारत, बंगाल, गुजरात — हर जगह बल अलग: कोई ब्रह्मांडीय पैमाना, कोई गृह शिक्षा। सभी मानते — कथा जीवित भक्ति की है, जमी हुई एक पंक्ति नहीं।

{why} घर में रीति से कथा सुनाते समय यही दोहराया जाता — पूजा आदत नहीं, स्मृति है।

कथा का हृदय, धीरे सुनाने पर, ऐसा है: {core}

कई परिवार {rel_f} के दिनों में यह कथा पढ़ते हैं, और {rel_t} जैसे तीर्थों की यात्रा से जोड़ते हैं — भौगोलिक यात्रा और घर की कथा एक ही भक्ति में मिलती है। बच्चों के लिए एक पंक्ति हुक, एक पंक्ति सार लिखकर उत्सव कार्ड बनाना लोकप्रिय है; TirthaYatra का लंबा पाठ उसी कार्ड का विस्तार है।

कुछ कथाएँ स्थानीय रंग जोड़ती हैं — नदी, पहाड़, संत पंक्ति — जो हर पुराण में नहीं। यह सामान्य है। पुराण, स्थल-पुराण, दादी की कथा, प्रवासी संस्करण हमेशा मेल नहीं खाते। TirthaYatra उस विविधता का सम्मान करता है — एक सूची या एक मंदिर परंपरा ही सत्य, ऐसा दावा नहीं।

गृह अभ्यास में: {take} व्यस्त दिन छोटी कथा; जब बच्चा 'फिर क्यों?' पूछे तो यह विस्तार। परिवार रीति भिन्न हो तो गुरु–पुजारी का आदर — यह पृष्ठ साथी है, आदेश नहीं। संबंधित देवता, त्योहार, मंदिर सूचियाँ सामान्य मार्गदर्शन हैं — जो आपके घर में न हों, जबरदस्ती न जोड़ें। कुछ परिवार सोमवार या शुक्रवार एक निश्चित समय कथा-संध्या रखते हैं; अन्य केवल त्योहार पर — दोनों ठीक हैं। महत्वपूर्ण है कि कथा सुनी जाए, न कि दिखावा हो।

{DISCLAIMER_HI}"""


def filter_related(story: dict, temple_slugs: set[str], fest_slugs: set[str], dev_slugs: set[str]) -> dict:
    s = dict(story)
    s["relatedTemples"] = [x for x in s.get("relatedTemples", []) if x in temple_slugs]
    s["relatedFestivals"] = [x for x in s.get("relatedFestivals", []) if x in fest_slugs]
    s["relatedDevotion"] = [x for x in s.get("relatedDevotion", []) if x in dev_slugs]
    return s


def infer_deity_families(seed: dict) -> list[str]:
    text = " ".join(
        [seed.get("deity", ""), seed.get("name", ""), seed.get("summary", ""), seed.get("mythology", "")]
    ).lower()
    fams: list[str] = []
    checks = [
        ("hanuman", ["hanuman"]),
        ("ganesha", ["ganesha", "ganesh", "murugan", "subramanya", "kartikeya"]),
        ("rama", ["rama", "raghunath"]),
        ("krishna", ["krishna", "gopal", "govinda", "vitthal", "vithoba", "shrinath", "banke bihari", "iskcon"]),
        ("devi", ["goddess", "devi", "mata", "shakti", "amman", "murugan"]),
        ("shiva", ["shiva", "mahadev", "linga", "brihadeeswarar", "vishwanath", "amarnath"]),
        ("vishnu", ["vishnu", "venkateswara", "narasimha", "iskcon"]),
        ("sai", ["sai"]),
    ]
    for fam, keys in checks:
        if any(k in text for k in keys):
            if fam not in fams:
                fams.append(fam)
    if "murugan" in text or "subramanya" in text:
        if "ganesha" not in fams:
            fams.insert(0, "ganesha")
    return fams[:3] or ["shiva"]


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


def enrich_myth_fields(detail: dict) -> dict:
    myth = detail.get("mythology", "")
    if not detail.get("mythologySignificance"):
        detail["mythologySignificance"] = (
            myth
            + "\n\nPilgrimage literature treats this shrine as a tirtha — verify living custom with temple priests. "
            "Accounts here are TirthaYatra summaries of widely cited traditions, not verbatim scripture."
        )
    if not detail.get("localBeliefs"):
        detail["localBeliefs"] = (
            "Queue discipline, prasadam sharing, and festival vows shape belief as practice. "
            "First-time visitors often hear several local tellings — living conversation, not a single fixed text."
        )
    if not detail.get("mythologyDisclaimer"):
        detail["mythologyDisclaimer"] = (
            "Mythological accounts and local beliefs are drawn from Puranic traditions, epics, and widely recorded "
            "sthala-purana / pilgrimage lore. Versions differ by scripture, region, and temple tradition."
        )
    detail["lastUpdated"] = "2026-08-14"
    detail["country"] = detail.get("country") or "India"
    detail["tier"] = "famous"
    return detail


def T(**kw):
    return kw


# —— NEW STORIES (slug -> seed without detail; detail composed at runtime) ——
NEW_STORY_SEEDS = [
    T(
        slug="shiva-damaru",
        title="Why Shiva holds the damaru",
        titleHi="शिव जी डमरू क्यों बजाते हैं",
        readSeconds=420,
        deity="shiva",
        tags=["ritual-why", "long-read", "seo-gap", "first-timer"],
        hook="Two halves of a shell — rhythm that births the letters of sound.",
        hookHi="दो खोल — ध्वनि के वर्ण जन्म देने वाला लय।",
        whyRitual="Nataraja icons and Sawan kirtan remember Shiva’s damaru as the pulse of creation — sound before speech, beat before mantra.",
        whyRitualHi="नटराज मूर्ति और सावन कीर्तन डमरू को सृष्टि की धड़कन मानते — वाणी से पहले ध्वनि।",
        storyEn="Shiva as Nataraja dances the world into being; in one hand the damaru beats. One telling links each stroke to the emergence of Sanskrit letters — sound as the seed of language and mantra. Another strand simply hears the drum as the heartbeat of tapasya: steady, small, endless. Devotees do not need to decode every mythic syllable; they hear invitation — let worship begin with rhythm, not rush.",
        storyHi="नटराज शिव जगत नचाते; एक हाथ में डमरू। एक कथा हर प्रहार को संस्कृत वर्णों के उदय से जोड़ती — ध्वनि मंत्र की जड़। दूसरी धारा इसे तप की धड़कन मानती — स्थिर, छोटी, अनंत। भक्त को हर अक्षर समझना जरूरी नहीं; निमंत्रण सुनते — पूजा लय से, भागदौड़ से नहीं।",
        takeaway="Before aarti, tap a gentle rhythm on your knee — one minute of still beat.",
        relatedDevotion=["shiva-aarti", "lingashtakam", "shiva-chalisa"],
        relatedFestivals=["maha-shivaratri", "shravan-sawan"],
        relatedTemples=["kashi-vishwanath", "nataraja-chidambaram", "kedarnath"],
        _detailExtraEn="The damaru appears on Nataraja icons from Chidambaram to museum walls worldwide. ",
        _detailExtraHi="डमरू चिदंबरम के नटराज से संग्रहालय तक दिखता है। ",
    ),
    T(
        slug="shiva-bhasma",
        title="Why Shiva wears holy ash — vibhuti and tripundra",
        titleHi="शिव जी भस्म और त्रिपुंड क्यों धारण करते हैं",
        readSeconds=420,
        deity="shiva",
        tags=["ritual-why", "long-read", "seo-gap", "first-timer"],
        hook="What remains when fire finishes its work — worn as crown, not shame.",
        hookHi="जब अग्नि अपना कार्य पूर्ण करे — शर्म नहीं, मुकुट।",
        whyRitual="Tripundra ash on the forehead remembers impermanence and Shiva’s mastery over death — Maha Shivaratri and daily Shaiva puja mark three lines for the three gunas.",
        whyRitualHi="त्रिपुंड भस्म अनित्यता और मृत्यु पर विजय याद दिलाता — महाशिवरात्रि और दैनिक शैव पूजा में तीन रेखाएँ तीन गुण।",
        storyEn="Shaiva tradition remembers Shiva smeared with ash from cremation grounds — not morbid glamour but truth: bodies return to elements. Tripundra — three horizontal lines — maps sattva, rajas, tamas held in one awareness. Householders use vibhuti from sacred fire or temple prasad; some use sandal paste on other days. The teaching is not to romanticize death but to begin the day remembering what lasts beyond the body’s season.",
        storyHi="शैव परंपरा शिव को श्मशान भस्म से सुगंधित मानती — भय नहीं, सत्य: देह तत्व लौटती। त्रिपुंड — तीन क्षैतिज रेखाएँ — सत, रज, तम एक चेतना में। गृहस्थ वैभवी या मंदिर प्रसाद लगाते; अन्य दिन चंदन। शिक्षा: मृत्यु का रोमांस नहीं — देह के मौसम से पर जो रहता उसकी स्मृति।",
        takeaway="Apply a pinch of vibhuti or sandal with three calm lines — then begin work without vanity.",
        relatedDevotion=["shiva-aarti", "shiva-chalisa", "maha-shivaratri-vrat-katha"],
        relatedFestivals=["maha-shivaratri", "shravan-sawan"],
        relatedTemples=["kashi-vishwanath", "mahakaleshwar-ujjain", "somnath"],
    ),
    T(
        slug="hanuman-shiva-amsha",
        title="Is Hanuman an amsha of Shiva?",
        titleHi="क्या हनुमान शिव के अंश हैं?",
        readSeconds=450,
        deity="hanuman",
        tags=["ritual-why", "long-read", "seo-gap", "first-timer"],
        hook="Eleven Rudras, one wind-born servant — traditions answer differently, devotion stays one.",
        hookHi="ग्यारह रुद्र, एक वायु-जात सेवक — परंपराएँ भिन्न, भक्ति एक।",
        whyRitual="Hanuman Chalisa Tuesdays remember a servant whose strength is Shiva’s gift in some tellings, pure Rama-bhakti in others — both paths honour seva without debate at the lamp.",
        whyRitualHi="मंगलवार चालीसा सेवक की स्मृति — कहीं शिव का अंश, कहीं शुद्ध राम भक्त; दीप पर विवाद नहीं, सेवा।",
        storyEn="Popular North Indian katha sometimes calls Hanuman an eleventh Rudra or Shiva’s amsha sent to serve Rama. Other Ramayana retellings emphasize Vayu’s son alone — power born of wind and vow, not avatar math. Scholars note both streams; temples rarely force one answer at darshan. What householders keep: Hanuman’s strength is never arrogant; it bows to dharma. Whether read as Shiva’s spark or wind’s child, the moral is identical — power in service.",
        storyHi="उत्तर भारतीय कथा कभी हनुमान को ग्यारहवें रुद्र या शिवांश कहती — राम की सेवा हेतु। अन्य रामायण केवल वायु-पुत्र — वायु और व्रत की शक्ति। विद्वान दोनों धाराएँ नोट करते; मंदिर एक उत्तर थोपते नहीं। गृहस्थ रखते: बल अहंकारी नहीं, धर्म के आगे झुका। शिवांश या वायु-सुत — शिक्षा एक: शक्ति सेवा में।",
        takeaway="Read Hanuman Chalisa once without needing to win a theology argument.",
        relatedDevotion=["hanuman-chalisa", "hanuman-aarti", "rama-aarti"],
        relatedFestivals=["hanuman-jayanti", "ram-navami"],
        relatedTemples=["sankat-mochan-varanasi", "salasar-balaji", "prayagraj-hanuman"],
    ),
    T(
        slug="radha-krishna-vraja",
        title="Radha and Krishna — love in Vraja",
        titleHi="राधा–कृष्ण — व्रज की प्रेम कथा",
        readSeconds=480,
        deity="krishna",
        tags=["festival", "long-read", "seo-gap", "family"],
        hook="The flute that called the gopis — and the one name Krishna never forgot.",
        hookHi="बाँसुरी जिसने गोपियों को बुलाया — और वह नाम जो कृष्ण कभी भूले नहीं।",
        whyRitual="Janmashtami and Kartik in Braj remember Radha-Krishna as soul’s longing for the Divine — not gossip but madhurya bhakti sung in kirtan.",
        whyRitualHi="जन्माष्टमी और कार्तिक व्रज में राधा–कृष्ण को आत्मा की दिव्य लालसा — नinda नहीं, माधुर्य कीर्तन।",
        storyEn="Krishna’s youth in Vraja is remembered through Radha — the gopi whose devotion became theology. Some texts name her Shakti of Krishna; folk Braj makes every grove a stage for their rasa. Later Vaishnava acharyas debated hierarchy; villagers debated who stole butter first. For home katha, the gentle telling is: divine love can be personal without being possessive; Radha’s name at Janmashtami teaches children that bhakti has a feminine courage equal to any warrior’s.",
        storyHi="व्रज यौवन राधा से याद — गोपी जिसकी भक्ति theology बनी। कहीं कृष्ण की शक्ति; लोक व्रज हर कुंज को रास मंच। आचार्यों में वर्ण; गाँव में मक्खन चोरी। घर कथा: दिव्य प्रेम स्वामित्वहीन हो सकता; जन्माष्टमी पर राधा का नाम — स्त्री साहस योद्धा जैसा।",
        takeaway="Sing one Krishna naam with Radha’s name — honour both halves of Braj bhakti.",
        relatedDevotion=["krishna-aarti", "krishna-chalisa", "janmashtami-vrat-katha"],
        relatedFestivals=["janmashtami", "holi"],
        relatedTemples=["banke-bihari-vrindavan", "krishna-janmabhoomi-mathura", "prem-mandir-vrindavan"],
    ),
    T(
        slug="banke-bihari-appearance",
        title="Banke Bihari — how the Lord appeared to Swami Haridas",
        titleHi="बांके बिहारी — स्वामी हरिदास को प्रकट कथा",
        readSeconds=450,
        deity="krishna",
        tags=["temple-story", "long-read", "seo-gap", "first-timer"],
        hook="A saint’s song, a forest grove, and Krishna who chose to stay visible.",
        hookHi="संत का गीत, वन कुंज, और कृष्ण जो दृश्य रहने चुने।",
        whyRitual="Banke Bihari darshan in Vrindavan uses a curtain because the Lord is said to be too beautiful to bear — seva through song still fills the lane.",
        whyRitualHi="बांके बिहारी दर्शन पarda — प्रभु की सुंदरता सहन करने को; कीर्तन से लेन अब भी भरता।",
        storyEn="Swami Haridas, poet-saint of the Nidhivan tradition, is remembered as calling Krishna through ragas until the Lord appeared with Radha — Banke Bihari, bent in three places, playful and merciful. The image was established in Vrindavan; later seva grew into the temple crowds know today. Curtains during darshan recall intensity of presence, not secrecy. Pilgrims learn: music can be puja; the saint’s patience is part of the miracle.",
        storyHi="स्वामी हरidas — नidhivan संत — राग से कृष्ण बुलाते जब तक राधा सहित प्रभु प्रकट — बांके बिहारी, त्रिभंग, लीला और कृपा। चित्र वृंदावन में; सेवा मंदिर बनी। दर्शन पर पarda उपस्थिति की तीव्रता — रहस्य नहीं। तीर्थ: संगीत पूजा; संत की धैर्य चमत्कार का अंग।",
        takeaway="Play one bhajan softly before sleep — let sound be your curtain of reverence.",
        relatedDevotion=["krishna-aarti", "krishna-chalisa"],
        relatedFestivals=["janmashtami", "holi"],
        relatedTemples=["banke-bihari-vrindavan", "radha-vallabh-vrindavan"],
    ),
    T(
        slug="shrinathji-nathdwara",
        title="Shrinathji of Nathdwara — the Lord who traveled from Govardhan",
        titleHi="श्रीनाथजी — गोवर्धन से नाथद्वारा तक",
        readSeconds=480,
        deity="krishna",
        tags=["temple-story", "long-read", "seo-gap", "first-timer"],
        hook="A wagon, a hill’s child, and a Rajasthan town that became his home.",
        hookHi="बैलगाड़ी, गिरि का बालक, और राजस्थान नगर जो घर बना।",
        whyRitual="Pushti Marg seva remembers Shrinathji’s daily leelas — food, dress, and seasons as love language.",
        whyRitualHi="पुष्टि मार्ग सेवा श्रीनाथजी की दैनिक लीलाएँ — भोजन, वस्त्र, ऋतु प्रेम भाषा।",
        storyEn="When Mughal-era pressure threatened Braj icons, tradition says Shrinathji’s form traveled by cart toward Mewar until the wheels sank at Nathdwara — sign to stop. The town reorganized around haveli-style seva: waking the Lord, dressing, offering meals by clock and season. Diaspora Pushti families mirror timings abroad. The story is migration of devotion, not only migration of stone — Krishna as child-king cared for by community.",
        storyHi="मुghal दबाव में ब्रज मूर्ति खतरे में — कथा: श्रीनाथजी रथ से मेवाड़ की ओर, नाथद्वारा पर पहिया धंसे — रुकने का संकेत। नगर हवेली सेवा में: जगाना, श्रृंगार, भोग। प्रवासी पुष्टि परिवार विदेश में भी समय। कथा पत्थर की नहीं भक्ति की — बाल-स्वामी समुदाय की देखभाल।",
        takeaway="Offer one meal to Krishna’s photo before you eat — small haveli seva at home.",
        relatedDevotion=["krishna-aarti", "vishnu-aarti"],
        relatedFestivals=["janmashtami", "holi"],
        relatedTemples=["nathdwara-shrinathji", "banke-bihari-vrindavan"],
    ),
    T(
        slug="kalki-avatar",
        title="Kalki — the tenth avatar yet to come",
        titleHi="कल्कि — अंतिम अवतार की प्रतीक्षा",
        readSeconds=450,
        deity="vishnu",
        tags=["ritual-why", "long-read", "seo-gap", "first-timer"],
        hook="A white horse, a sword of dawn — hope at the edge of an age.",
        hookHi="श्वेत अश्व, भोर की तलवार — युग के छोर पर आशा।",
        whyRitual="Dashavatara lists end with Kalki — not fear-mongering but reminder that dharma will be restored when adharma peaks.",
        whyRitualHi="दशावतार कल्कि पर समाप्त — भय नहीं, अधर्म चरम पर धर्म पुनः स्थापित।",
        storyEn="Puranic futures describe Kalki arriving when virtue thins — Vishnu on a horse, ending corrupt age, opening renewal. Details vary by text; dates are never fixed for devotion. Households paint Dashavatara strips with an empty hope at the end: the story is unfinished because history is still being chosen. Teach children Kalki as responsibility now — act justly today rather than waiting for a cosmic cavalry.",
        storyHi="पुराण भविष्य: कल्कि जब सदाचार क्षीण — विष्णु अश्व पर, दूषित युग का अंत, नवीनता। विवरण पाठ भिन्न; भक्ति में तिथि नहीं। दशावतार चित्र अंत में आशा — कथा अधूरी क्योंकि इतिहास अभी लिखा जा रहा। बच्चों को: कल्कि आज न्याय — कल की घुड़सवारी की प्रतीक्षा नहीं।",
        takeaway="Do one act of fairness you postponed — be your age’s small restoration.",
        relatedDevotion=["vishnu-aarti", "vishnu-chalisa", "rama-aarti"],
        relatedFestivals=["ram-navami", "akshaya-tritiya"],
        relatedTemples=["srirangam-ranganathaswamy", "dwarka"],
    ),
    T(
        slug="buddha-dashavatara",
        title="Buddha in the Dashavatara list — a respectful note",
        titleHi="दशावतार में बुद्ध — सम्मानपूर्ण स्मरण",
        readSeconds=480,
        deity="vishnu",
        tags=["ritual-why", "long-read", "seo-gap", "first-timer"],
        hook="One name, many lists — Vishnu as teacher when pride masquerades as religion.",
        hookHi="एक नाम, अनेक सूचियाँ — जब अहंकार धर्म का वेश धरे।",
        whyRitual="Some Hindu calendars place Buddha as Vishnu’s ninth avatar against false sacrifice; Buddhists honor Shakyamuni separately — both deserve respect without conflation at the lamp.",
        whyRitualHi="कुछ हिंदू सूचियों में बुद्ध नौवें अवतार — झूठे यज्ञ के विरुद्ध; बौद्ध शाक्यमुनि अलग — दीप पर सम्मान, मिलावट नहीं।",
        storyEn="Medieval Bhagavata-influenced lists often include Buddha as Vishnu calming deluded ritualism — distinct from Gautama Buddha’s historical sangha. Other regions omit or reorder; Jayadeva’s Gita Govinda names Buddha; South Indian lists differ. TirthaYatra presents this as cultural literacy, not debate weapon. At home: teach that sacred history has many maps; kindness to neighbors of all paths is the shared floor.",
        storyHi="मध्यकालीन सूचियों में अक्सर बुद्ध — विष्णु रूप जो मिथ्या यज्ञ शांत करे — ऐतिहासिक बुद्ध से भिन्न। क्षेत्र अलग क्रम; जयदेव में बुद्ध; दक्षिण सूची भिन्न। TirthaYatra सांस्कृतिक ज्ञान, विवाद हथियार नहीं। घर: पवित्र इतिहास के अनेक मानचित्र; सभी मार्गों के प्रति दया общा भूमि।",
        takeaway="Explain two lists can coexist — then offer water to any thirsty guest.",
        relatedDevotion=["vishnu-aarti", "vishnu-chalisa"],
        relatedFestivals=["akshaya-tritiya", "guru-purnima"],
        relatedTemples=["srirangam-ranganathaswamy", "pashupatinath"],
    ),
    T(
        slug="vibhishana-surrender",
        title="Vibhishana — choosing Rama over blood",
        titleHi="विभीषण — रक्त से ऊपर राम का चुनाव",
        readSeconds=450,
        deity="rama",
        tags=["ritual-why", "long-read", "seo-gap", "family"],
        hook="Brother of a tyrant, crown of a just king — dharma over dynasty.",
        hookHi="अत्याचारी का भाई, न्याय राजा का मुकुट — वंश से ऊपर धर्म।",
        whyRitual="Dussehra remembers not only Rama’s victory but Vibhishana’s surrender — integrity when family goes wrong.",
        whyRitualHi="दशहरा केवल विजय नहीं — विभीषण की शरण, परिवार गलत हो तो भी धर्म।",
        storyEn="Vibhishana warned Ravana until warning failed; he crossed the sea to Rama’s camp, was mocked by some vanaras, yet Rama gave him refuge and later Lanka’s care. The Ramayana holds complexity: a rakshasa brother who chose truth. Diaspora tellings use him when discussing whistleblowing and exile. Moral for children: loyalty to righteousness can cost belonging — and still be right.",
        storyHi="विभीषण रावण को चेतावनी देते रहे; विफलता पर राम शरण; वानर उपहास; राम ने शरण दी, बाद में लंका का ध्यान। रामायण जटिल: राक्षस भाई सत्य चुनता। प्रवासी कथा: सच बोलने की कीमत। बच्चों को: धर्म की निष्ठा संबंध खो सकती — फिर भी सही।",
        takeaway="Stand for one truth kindly in a family conversation this week.",
        relatedDevotion=["rama-aarti", "rama-chalisa"],
        relatedFestivals=["dussehra", "ram-navami"],
        relatedTemples=["ayodhya-ram-mandir", "rameswaram"],
    ),
    T(
        slug="mandodari-lanka",
        title="Mandodari — voice of restraint in Lanka",
        titleHi="मंदोदरी — लंका में संयम की आवाज",
        readSeconds=420,
        deity="rama",
        tags=["long-read", "seo-gap", "family"],
        hook="Queen of a golden city, witness to a husband’s ruin — wisdom unheard until too late.",
        hookHi="स्वर्ण नगर की रानी, पति पतन की साक्षी — बुद्धि जो देर से सुनी गई।",
        whyRitual="Ramayana katha during Navaratri or Dussehra can include Mandodari — courage to speak truth inside power.",
        whyRitualHi="नवरात्रि–दशहरा कथा में मंदोदरी — सत्ता में सत्य बोलने का साहस।",
        storyEn="Mandodari is remembered as learned and righteous, urging Ravana to return Sita and avoid war. He did not listen; she remained, grieving yet dignified in most tellings. Her story is under-told beside Sita’s — yet it teaches spouses and ministers alike: counsel offered in love still matters even when rejected. No sensationalism — only the quiet cost of living beside unchecked ego.",
        storyHi="मंदोदरी विदुषी, धarmic — रावण से सीता लौटाने, युद्ध टालने कहतीं। नहीं सुना; शोकित पर गरिमा। सीता के साथ कम सुनी — फिर भी शिक्षा: प्रेम की सलाह अस्वीकार भी हो तो मूल्यवान। सनसनी नहीं — अहंकार के पास रहने की कीमत।",
        takeaway="Offer one honest counsel gently — without needing to win.",
        relatedDevotion=["rama-aarti", "rama-chalisa"],
        relatedFestivals=["dussehra", "navaratri"],
        relatedTemples=["ayodhya-ram-mandir", "rameswaram"],
    ),
    T(
        slug="draupadi-vastraharan-dharma",
        title="Draupadi’s appeal — dharma and divine protection",
        titleHi="द्रौपदी का आह्वान — धर्म और दिव्य रक्षा",
        readSeconds=480,
        deity="krishna",
        tags=["long-read", "seo-gap", "family"],
        hook="When court failed, she called Krishna — cloth that would not end.",
        hookHi="जब सभा विफल, कृष्ण को पुकारा — चीर जो समाप्त न हुआ।",
        whyRitual="Retellings focus on dharma’s failure in the Kuru court and Krishna’s response — dignity restored, not spectacle of harm.",
        whyRitualHi="कथाएँ कुरु सभा में धर्म पतन और कृष्ण की प्रतिक्रिया — गरिमा, हिंसा का नाटक नहीं।",
        storyEn="In the dice hall Draupadi asked whether a stake taken unrightfully could bind her; elders stayed silent. Her cry reached Krishna; tradition says endless garment protected her modesty while injustice was exposed. TirthaYatra tells this without graphic detail — emphasis on failed duty of kings and kinsmen, and on divine friendship that answers when institutions fail. Home lesson: protect the vulnerable; do not fetishize suffering.",
        storyHi="द्यूत सभा में द्रौपदी ने पूछा — अधर्म से जीती हुई दासी बंधन बाँध सकती? मौन बुजुर्ग। पुकार कृष्ण तक; परंपरा — अनंत वस्त्र, अन्याय उघाड़ा। TirthaYatra बिना graphic विवरण — राज–कुटुम्ब का कर्तव्य पतन, संस्था विफल हो तो मित्र भगवान। घर: दुर्बल की रक्षा; पीड़ा का उपभोग नहीं।",
        takeaway="If someone is humiliated nearby, intervene safely — be Krishna’s answer in small measure.",
        relatedDevotion=["krishna-aarti", "devi-aarti"],
        relatedFestivals=["raksha-bandhan", "navaratri"],
        relatedTemples=["dwarka", "guruvayur"],
    ),
    T(
        slug="karna-kunti",
        title="Karna and Kunti — sun-born son, delayed truth",
        titleHi="कर्ण और कुंती — सूर्य-पुत्र, विलंबित सत्य",
        readSeconds=480,
        deity="vishnu",
        tags=["long-read", "seo-gap", "family"],
        hook="Armour he would not remove, mother who spoke too late — fate woven in war.",
        hookHi="कवच जो उतारा नहीं, माँ जिसने देर से कहा — युद्ध में बुना भाग्य।",
        whyRitual="Mahabharata katha nights remember Karna’s generosity and tragic loyalty — ask children about fairness to outsiders.",
        whyRitualHi="महाभारत कथा रातें कर्ण की उदारता, दुखद निष्ठा — बाहरी के प्रति न्याय।",
        storyEn="Kunti revealed to Karna before Kurukshetra that he was her eldest; he promised not to kill Pandava brothers except Arjuna, yet stayed with Duryodhana’s debt of friendship. His kavach-kundal gift to Indra, his annadata fame — all frame a hero outside easy sides. The story warns: secrets kept for status ruin children; loyalty without dharma breaks kingdoms.",
        storyHi="कुंती कर्ण को युद्ध से पहले माँ साबित — पांडव न मारूँगा सिवाय अर्जुन; पर दुर्योधन ऋण में रहे। कवच–कुंडल दान, अन्नदाता — नायक सरल पक्ष से बाहर। चेतावनी: मान हेतु छिपा सत्य बच्चों को तोड़ता; धर्महीन निष्ठा राज्य तोड़ती।",
        takeaway="Tell one hidden truth kindly before it becomes a battlefield.",
        relatedDevotion=["surya-chalisa", "krishna-aarti"],
        relatedFestivals=["maha-shivaratri"],
        relatedTemples=["kurukshetra-jyotisar-kurukshetra" if False else "jyotisar-kurukshetra"],
    ),
    T(
        slug="abhimanyu-chakravyuh",
        title="Abhimanyu and the chakravyuha",
        titleHi="अभिमन्यु और चक्रव्यूह",
        readSeconds=450,
        deity="krishna",
        tags=["long-read", "seo-gap", "family"],
        hook="He knew how to enter, not exit — youth trapped by war’s geometry.",
        hookHi="प्रवेश जानता, न निकास — युद्ध की रेखाओं में फँसा युवा।",
        whyRitual="Mahabharata remembrance teaches courage and the cost of adults failing to teach fully.",
        whyRitualHi="महाभारत स्मृति — साहस और अधूरा शिक्षण का दाम।",
        storyEn="Abhimanyu learned breaking the chakravyuha formation in the womb by overhearing Krishna; exit strategy was never heard. In Kurukshetra he entered alone to save elders, fought until exhausted, and fell to unfair odds. The tale moves students and parents: brilliance without complete training is vulnerable; systems that send youth first are guilty. Tell it without glorifying war — honour the boy’s bravery and mourn the failure around him.",
        storyHi="अभिमन्यु ने गर्भ में चक्रव्यूह भेद सुना; निकास नहीं। कुरुक्षेत्र में अकेला प्रवेश, बचाने को; थककर अन्याय से गिरे। छात्र–अभिभावक: अधूरा ज्ञान असुरक्षित; युवा आगे धकेलना दोष। युद्ध महिमा नहीं — बालक वीरता, चारों ओर विफलता शोक।",
        takeaway="Teach someone a skill completely — include how to stop and retreat safely.",
        relatedDevotion=["krishna-aarti", "hanuman-chalisa"],
        relatedFestivals=["maha-shivaratri"],
        relatedTemples=["jyotisar-kurukshetra"],
    ),
    T(
        slug="sheetala-mata",
        title="Sheetala Mata — coolness against fever and rash",
        titleHi="शीतला माता — बुखार से शीतलता",
        readSeconds=420,
        deity="devi",
        tags=["festival", "long-read", "seo-gap", "family"],
        hook="Basoda kitchens cold, goddess on a donkey — spring mercy for children’s pox.",
        hookHi="बसोड़ा ठंडा भोजन, गधा वाहini — वसंत में बच्चों को शीतला कृपा।",
        whyRitual="Sheetala Ashtami and Basoda remember cooling foods and gentle care when smallpox and heat rashes once terrified villages.",
        whyRitualHi="शीतला अष्टमी, बसोड़ा — ठंडा भोजन, कोमल देखभाल जब चेचक भय था।",
        storyEn="Sheetala Mata rides a donkey, carries a broom and pot — symbols of sweeping illness and cooling water. Mothers offered stale-cooled food one day, prayed for children’s skin to heal, and shared remedies neighbor to neighbor. Modern medicine replaced pox; the festival remains as hygiene memory and Devi gratitude. Tell children: goddess stories once taught public health in sacred language.",
        storyHi="शीतला माता गधे पर, झाड़ू–कलश — रोग झाड़ना, जल शीतल करना। माताएँ एक दिन ठंडा भोजन, बच्चों की त्वचा हेतु प्रार्थना, पड़ोस में उपचार। आज चिकित्सा; उत्सव स्वच्छता स्मृति। बच्चों को: देवी कथा कभी सार्वजनिक स्वास्थ्य की भाषा थी।",
        takeaway="On a hot day, share cool water and check a neighbor child’s fever kindly.",
        relatedDevotion=["devi-aarti", "mansa-devi-aarti"],
        relatedFestivals=["sheetala-ashtami"],
        relatedTemples=["sheetla-mata-gurgaon", "sheetla-mata-ludhiana"],
    ),
    T(
        slug="manasa-behula",
        title="Manasa and Behula — faith across the snake’s test",
        titleHi="मनसा और बेहुला — सर्प परीक्षा पर विश्वास",
        readSeconds=480,
        deity="devi",
        tags=["long-read", "seo-gap", "family"],
        hook="A bride’s boat, a husband’s curse, and the goddess of serpents appeased by song.",
        hookHi="नाव पर दुलहन, पति शाप, और सर्प देवी जो गीत से प्रसन्न।",
        whyRitual="Manasa Puja in Bengal and Assam remembers Behula’s journey — devotion that refuses widowhood as fate.",
        whyRitualHi="बंगाल–असम मनसा पूजा बेहुला यात्रा — विधवा होने को भाग्य न मानना।",
        storyEn="Chand Saudagar’s pride offended Manasa; his son Lakshindar died of snakebite on wedding night. Behula sailed with his body, proving purity through trials until the goddess restored life. Mangal kavya singers spread the epic; villages learned coexistence with snakes and monsoon fear. Home telling: stubborn ego provokes suffering; faithful courage can rewrite endings without hate.",
        storyHi="चाँद सौदागर के अहंकार से मनसा नाराज; लक्षमिन्दर शादी की रात सर्पदंश; बेहुला शव संग नाव, परीक्षाएँ पार, देवी ने जीवन लौटाया। मंगलकाव्य गायक; सर्प–वर्षा सहजीवन। घर: अहंकार दुख; श्रद्धा साहस अंत बदल सकता — घृणा बिना।",
        takeaway="Learn one folk song of your region — carry story in melody.",
        relatedDevotion=["mansa-devi-aarti", "devi-aarti"],
        relatedFestivals=["nag-panchami"],
        relatedTemples=["hayagriva-madhava-hajo"],
    ),
    T(
        slug="chhinnamasta-meaning",
        title="Chhinnamasta — spiritual metaphor of self-giving",
        titleHi="छिन्नमस्ता — आत्म-त्याग का आध्यात्मिक प्रतीक",
        readSeconds=450,
        deity="devi",
        tags=["long-read", "seo-gap", "first-timer"],
        hook="Headless goddess feeding herself and devotees — not horror, but radical generosity symbol.",
        hookHi="शिरहीन देवी स्वयं और भक्त को पोषण — भय नहीं, पराकाष्ठा उदारता चिह्न।",
        whyRitual="Tantric and folk Shakti traditions read Chhinnamasta as life-force shared — interpreted only with teacher guidance, never sensationalized.",
        whyRitualHi="शाक्त परंपरा छिन्नमस्ता को जीवन-शक्ति साझा — गुरु मार्गदर्शन; सनसनी नहीं।",
        storyEn="Icons show the Goddess severing her own head so blood streams nourish companions — shocking at first glance, yet theologians read it as prana flowing without ego boundary. Rajrappa and Nepal traditions guard strict ritual context. TirthaYatra presents symbolic meaning only: sacrifice of pride to feed others; mothers who empty themselves for children see a fierce mirror. No gore fetish — ask a qualified guru before tantra practice.",
        storyHi="मूर्ति में देवी स्वशिर काटकर रक्त से साथी पोषती — पहली दृष्टि चौंकाए; तत्त्वज्ञ प्राण बिना अहंकार सीमा कहते। राजरप्पा, नेपाल — कठोर रीति। TirthaYatra केवल प्रतीक: अभिमान त्याग दूसरे को पोषे; माँ का प्रतिबिंब। रक्त आकर्षण नहीं; तंत्र गुरु बिना नहीं।",
        takeaway="Feed someone before yourself once — small practical Chhinnamasta without icon fear.",
        relatedDevotion=["devi-aarti", "kali-chalisa"],
        relatedFestivals=["navaratri"],
        relatedTemples=["rajrappa-chhinnamastika", "kamakhya"],
    ),
    T(
        slug="dattatreya-avatar",
        title="Dattatreya — the three-headed teacher",
        titleHi="दत्तात्रेय — त्रिमुख गुरु अवतार",
        readSeconds=450,
        deity="vishnu",
        tags=["long-read", "seo-gap", "first-timer"],
        hook="Brahma, Vishnu, Shiva in one form — wandering with dogs and lessons from nature.",
        hookHi="ब्रह्मा, विष्णु, शिव एक रूप — कुत्तों संग भ्रमण, प्रकृति से शिक्षा।",
        whyRitual="Dattatreya Jayanti in Maharashtra, Gujarat, and Andhra remembers guru who learned from twenty-four teachers including a child and a bee.",
        whyRitualHi="दत्त जयंती महाराष्ट्र–गुजरात–आंध्र — चौबीस गुरु, बालक और मधु मक्खी सहित।",
        storyEn="Anusuya’s austerity brought the trinity as one child Dattatreya; he later wandered as avadhuta, teaching that God speaks through humble things. Dogs following him upset polite society — lesson in loyalty outside status. Devotees at Girnar and Gangapur see him as living guru principle. Moral: learn from everything; ego is the only unteachable student.",
        storyHi="अनुसूया की तपस्या से त्रिमूर्ति एक पुत्र दत्तात्रेय; अवधूत बन भ्रमण — ईश्वर नम्र में बोलता। कुत्ते साथ — वर्ग विरोध; वफादारी शिक्षा। गिरनार, गंगापुर — जीवंत गुरु सिद्धांत। शिक्षा: सब से सीखो; अहंकार ही अशिक्ष्य।",
        takeaway="Notice one lesson today from an unexpected person or animal.",
        relatedDevotion=["vishnu-aarti", "shiva-aarti"],
        relatedFestivals=["guru-purnima"],
        relatedTemples=["girnar" if False else "somnath"],
    ),
    T(
        slug="sai-shirdi-origin",
        title="Sai Baba of Shirdi — who was the fakir-saint?",
        titleHi="शirdi के साईं बाबा — वह फकीर-संत कौन थे?",
        readSeconds=450,
        deity="sai",
        tags=["temple-story", "long-read", "seo-gap", "first-timer"],
        hook="No known birth, both mosque and dhwaja — mercy without label.",
        hookHi="जन्म अज्ञात, मसjid और ध्वज — बिना लेबल करुणा।",
        whyRitual="Thursday lamps and Sai Satcharitra reading remember a saint who fed the hungry and united Hindus and Muslims in shared seva.",
        whyRitualHi="गुरुवार दीप, सत्चरitra — भूखे को भोजन, हिंदू–मुस्लिम सेवा में एकता।",
        storyEn="Sai Baba appeared in Shirdi as a youth; villagers first feared, then loved his miracles of food and healing. He lived in masjid, named it Dwarkamai, kept dhuni fire. No crusade — only ‘Shraddha aur Saburi’, faith and patience. Posthumous temples spread worldwide; story stays humble: God wears whatever form reaches the lonely.",
        storyHi="साईं शirdi युवा रूप में; पहले भय, फिर चमत्कार–भोजन से प्रेम। मसjid में Dwarkamai, धuni। धर्म युद्ध नहीं — ‘श्रद्धा और सबूरी’। मृत्यु के बाद मंदिर विश्व; कथा विनम्र: ईश्वर अकेले तक पहुँचने का रूप धारण करता।",
        takeaway="Light one lamp Thursday; feed a stranger anonymously if you can.",
        relatedDevotion=["sai-baba-aarti", "sai-chalisa"],
        relatedFestivals=["guru-purnima"],
        relatedTemples=["shirdi-sai"],
    ),
    T(
        slug="vaishno-devi-appearance",
        title="Vaishno Devi — how the Goddess appeared in the Trikuta hills",
        titleHi="वैष्णो देवी — त्रिकुटा में देवी प्रकट कथा",
        readSeconds=480,
        deity="devi",
        tags=["temple-story", "long-read", "seo-gap", "first-timer"],
        hook="A bullock rider, a beheaded villain, and a cave that became yatra’s heart.",
        hookHi="बैलगाड़ी सवार, वध कंटक, और गुफा जो यात्रा का हृदय बनी।",
        whyRitual="Navaratri and New Year crowds climb Katra remembering Vaishnavi’s merge into rock after guiding Pandit Sridhar.",
        whyRitualHi="नवरात्रि, नव वर्ष कश्मीर चढ़ाई — वैष्णवी शिला में समा, श्रीधर को मार्ग दिखाया।",
        storyEn="Sridhar’s bhajan party invited a goddess in disguise; Bhairon Nath chased her; she beheaded him at Bhairon Ghati after warning. At the cave she assumed rock form — pindis worshipped today. Army and trust later organized the modern yatra; faith story stays local: Devi tests greed, rewards simple hospitality. Bhairon temple still closes the circuit — forgiveness included.",
        storyHi="श्रीधर के भजन में देवी अज्ञात रूप; भैरों नाथ पीछा; चेतावनी के बाद वध भैरों घाटी। गुफा में शिला रूप — आज पिंडी। सेना–ट्रस्ट ने आधुनिक यात्रा; स्थानीय: देवी लोभ परीक्षा, साधारण आतिथ्य पुरस्कार। भैरों मंदिर परिक्रमा — क्षमा सहित।",
        takeaway="Begin a small yatra vow with clean intent — not selfie, but seva.",
        relatedDevotion=["vaishno-devi-aarti", "vaishno-chalisa", "devi-aarti"],
        relatedFestivals=["navaratri", "chaitra-navaratri"],
        relatedTemples=["vaishno-devi"],
    ),
]

# Fix bad temple refs in seeds
for s in NEW_STORY_SEEDS:
    if s.get("relatedTemples") == ["kurukshetra-jyotisar-kurukshetra"]:
        s["relatedTemples"] = ["jyotisar-kurukshetra"]
    if s.get("relatedTemples") == ["girnar"]:
        s["relatedTemples"] = ["somnath", "shirdi-sai"]


NEW_TEMPLES = [
    T(
        slug="shani-shingnapur",
        name="Shani Shingnapur Temple",
        deity="Lord Shani (Saturn)",
        location="Shingnapur, Ahmednagar, Maharashtra",
        state="Maharashtra",
        glyph="श",
        famousFor="Open-air Shani shrine · no doors village legend · massive Saturday search",
        summary="Shani Shingnapur — Maharashtra's famous open-platform Shani temple where Saturn is worshipped without a conventional roofed sanctum.",
        mythology="Village tradition says a black stone emerged from the earth and was recognized as Shani; locals trust the deity as village guardian. The 'no locked doors' folk belief draws curious pilgrims alongside sincere Saturday graha-shanti vows.",
        lat=19.832,
        lng=74.481,
        mapQuery="Shani Shingnapur Temple Ahmednagar",
        nearestRail="Shirdi / Rahuri with road",
        nearestAirport="Aurangabad / Pune",
        officialWebsite="https://www.maharashtratourism.gov.in/",
        festivals=["Shani Amavasya", "Saturdays", "Mahashivratri nearby circuits"],
        tags_extra=["navagraha"],
    ),
    T(
        slug="amarnath-cave",
        name="Amarnath Cave Temple (Ice Lingam Yatra)",
        deity="Lord Shiva (Amarnath Ice Lingam)",
        location="Amarnath Cave, Pahalgam–Baltal route, Jammu and Kashmir",
        state="Jammu and Kashmir",
        glyph="अ",
        famousFor="Seasonal ice lingam yatra · among India's highest-search Himalayan pilgrimages",
        summary="Amarnath Cave — seasonal Shiva yatra to the self-forming ice lingam; distinct from the Amarnath Shakti Peeth naming elsewhere on Shakti lists.",
        mythology="Puranic memory places Shiva revealing immortality secrets to Parvati in this cave; the ice lingam waxes and wanes with season. Pilgrims trek via Pahalgam or Baltal under Shri Amarnathji Shrine Board arrangements.",
        lat=34.213,
        lng=75.513,
        mapQuery="Amarnath Cave Temple",
        nearestRail="Jammu Tawi with road onward",
        nearestAirport="Srinagar",
        officialWebsite="https://www.shriamarnathjishrine.com/",
        festivals=["Shravan Amarnath Yatra season", "Maha Shivaratri remembrance"],
        tags_extra=["himalayan-yatra"],
    ),
    T(
        slug="ahobilam-narasimha",
        name="Ahobilam Lakshmi Narasimha Temples",
        deity="Lord Narasimha (nine forms)",
        location="Ahobilam, Kurnool, Andhra Pradesh",
        state="Andhra Pradesh",
        glyph="अह",
        famousFor="Nava Narasimha forest temples · high AP Narasimha search",
        summary="Ahobilam — cluster of Narasimha shrines in the Nallamala hills linked to Prahlada lore.",
        mythology="Sthala tradition places Hiranyakashipu's realm and Narasimha's appearance across upper and lower Ahobilam. Pilgrims trek forest paths between nine forms; Ahobila Mutt holds a major Vaishnava seat.",
        lat=15.133,
        lng=78.716,
        mapQuery="Ahobilam Narasimha Temple",
        nearestRail="Jaggaiahpet / Nandyal with road",
        nearestAirport="Hyderabad / Tirupati",
        officialWebsite="https://www.aptemples.ap.gov.in/",
        festivals=["Narasimha Jayanti", "Brahmotsavam", "Dussehra"],
        tags_extra=["narasimha"],
    ),
    T(
        slug="palani-murugan",
        name="Arulmigu Dhandayuthapani Temple, Palani",
        deity="Lord Murugan (Dhandayuthapani / Kartikeya)",
        location="Palani, Dindigul, Tamil Nadu",
        state="Tamil Nadu",
        glyph="प",
        famousFor="Hill Murugan · Panchamritam · among TN's highest Murugan footfall",
        summary="Palani Murugan — hill temple of Dhandayuthapani, anchor of the Tamil Murugan circuit with Thaipusam and Skanda Shashti peaks.",
        mythology="Tradition remembers Murugan as renouncing worldly crown here, holding staff (danda) after Gnanapalam fruit dispute with Ganesha. Kavadi and tonsure vows define the climb.",
        lat=10.438,
        lng=77.517,
        mapQuery="Palani Murugan Temple",
        nearestRail="Palani",
        nearestAirport="Coimbatore / Madurai",
        officialWebsite="https://palani.org/",
        festivals=["Thaipusam", "Skanda Shashti", "Panguni Uthiram"],
        tags_extra=["murugan"],
    ),
    T(
        slug="thiruchendur-murugan",
        name="Arulmigu Subramaniaswamy Temple, Thiruchendur",
        deity="Lord Murugan (Subramanya)",
        location="Thiruchendur, Thoothukudi, Tamil Nadu",
        state="Tamil Nadu",
        glyph="त",
        famousFor="Seashore Murugan · Soora Samharam · Skanda Shashti crowds",
        summary="Thiruchendur — rare coastal Murugan temple where the Lord faces the sea after defeating Surapadma in lore.",
        mythology="Skanda Purana strands place Murugan's victory and temple by the Bay of Bengal. Soora Samharam processions draw massive Shashti footfall.",
        lat=8.497,
        lng=78.119,
        mapQuery="Thiruchendur Murugan Temple",
        nearestRail="Tiruchendur",
        nearestAirport="Tuticorin / Madurai",
        officialWebsite="https://thiruchendurmurugantemple.tnhrce.in/",
        festivals=["Skanda Shashti", "Thaipusam", "Vaikasi Visakam"],
        tags_extra=["murugan"],
    ),
    T(
        slug="brihadeeswarar-thanjavur",
        name="Brihadeeswarar Temple, Thanjavur",
        deity="Lord Shiva (Brihadeeswarar / Peruvudaiyar)",
        location="Thanjavur, Tamil Nadu",
        state="Tamil Nadu",
        glyph="बृ",
        famousFor="UNESCO Chola temple · Big Temple · Nandi scale",
        summary="Brihadeeswarar — Rajaraja Chola's granite masterpiece and living Shiva seat with one of India's largest Nandi icons.",
        mythology="Chola imperial worship fused architecture and Shaiva bhakti; the vimana's shadow legend and Nandi's size feed sthala memory. Still active under TN HR&CE with major Shivaratri abhishekam.",
        lat=10.783,
        lng=79.132,
        mapQuery="Brihadeeswarar Temple Thanjavur",
        nearestRail="Thanjavur Junction",
        nearestAirport="Tiruchirappalli",
        officialWebsite="https://www.tn.gov.in/department/18/hrce",
        festivals=["Maha Shivaratri", "Arudra Darshanam", "Pradosham"],
        tags_extra=["unesco", "chola-heritage"],
    ),
    T(
        slug="iskcon-vrindavan",
        name="ISKCON Krishna–Balaram Temple, Vrindavan",
        deity="Krishna–Balaram (ISKCON)",
        location="Raman Reti, Vrindavan, Uttar Pradesh",
        state="Uttar Pradesh",
        glyph="इ",
        famousFor="White marble Vrindavan ISKCON · global kirtan · Braj yatra hub",
        summary="ISKCON Vrindavan — Krishna–Balaram mandir with international kirtan, prasadam, and Braj pilgrimage anchor.",
        mythology="Built on Raman Reti lore where Krishna played; Gaudiya Vaishnava bhakti campus welcomes diaspora and domestic yatris for darshan, kirtan, and festival crowds on Janmashtami.",
        lat=27.568,
        lng=77.690,
        mapQuery="ISKCON Vrindavan Krishna Balaram Temple",
        nearestRail="Mathura Junction",
        nearestAirport="Delhi / Agra",
        officialWebsite="https://www.iskconvrindavan.com/",
        festivals=["Janmashtami", "Holi", "Kartik month kirtan"],
        tags_extra=["modern-temples", "iskcon"],
    ),
    T(
        slug="uttarkashi-vishwanath",
        name="Kashi Vishwanath Temple, Uttarkashi",
        deity="Lord Shiva (Vishwanath)",
        location="Uttarkashi, Uttarakhand",
        state="Uttarakhand",
        glyph="उ",
        famousFor="'Chhota Kashi' of Garhwal · Char Dham corridor Shiva search",
        summary="Uttarkashi Vishwanath — ancient Shiva temple on the Bhagirathi called the Kashi of the Himalayas.",
        mythology="Pilgrims en route to Yamunotri and Gangotri pause here; local belief mirrors Kashi's liberation promise in mountain form. Akhand Jyoti and Shivaratri draw Garhwal crowds.",
        lat=30.726,
        lng=78.434,
        mapQuery="Kashi Vishwanath Temple Uttarkashi",
        nearestRail="Rishikesh / Dehradun with road",
        nearestAirport="Dehradun",
        officialWebsite="https://uttarakhandtourism.gov.in/",
        festivals=["Maha Shivaratri", "Shravan Mondays", "Kartik"],
        tags_extra=["chota-kashi"],
    ),
    T(
        slug="srimukhalingam",
        name="Sri Mukhalingam Temple",
        deity="Lord Shiva (Mukhalingam)",
        location="Sri Mukhalingam, Srikakulam, Andhra Pradesh",
        state="Andhra Pradesh",
        glyph="मु",
        famousFor="9th-century Kalinga Shiva · Vamsadhara river heritage search",
        summary="Srimukhalingam — historic Kalinga-style Shiva temple complex on the Vamsadhara, thinner English web but steady regional tirtha.",
        mythology="Eastern Chalukya patronage left a multi-shrine complex; mukhalinga form and river ghats shape local Shaiva festivals. Pairs with Srikakulam coastal temple trails.",
        lat=18.867,
        lng=84.017,
        mapQuery="Sri Mukhalingam Temple Srikakulam",
        nearestRail="Palasa / Srikakulam Road",
        nearestAirport="Visakhapatnam",
        officialWebsite="https://www.aptemples.ap.gov.in/",
        festivals=["Maha Shivaratri", "Kartik", "Local Shivaratri mela"],
        tags_extra=["heritage"],
    ),
]


def fest_entry(**kw):
    return kw


NEW_FESTIVALS = [
    fest_entry(
        slug="skanda-shashti",
        name="Skanda Shashti",
        nameHi="स्कंद षष्ठी",
        importance="high",
        dateNames=["Skanda Shashti", "Kanda Shashti", "Soora Samharam"],
        summary="Sixth day of Kartik bright fortnight — Murugan's victory over Surapadma and courage for devotees.",
        summaryHi="कार्तिक शुक्ल षष्ठी — मुरुगन की विजय और भक्तों के लिए साहस।",
        meaningEn="Skanda Shashti honours Lord Murugan (Kartikeya) defeating the asura Surapadma. Tamil Nadu coastal temples like Thiruchendur stage Soora Samharam; six-day fasts and Kanda Sashti Kavasam recitation mark the week.",
        meaningHi="स्कंद षष्ठी भगवान मुरुगन (कार्तिकेय) की सुरपद्म पर विजय। तिरुचेंदूर में सूर समहारम; छः दिन व्रत, कंद षष्ठी कवच पाठ।",
        storyEn="Puranic battle strands describe Murugan receiving vel spear from Parvati, splitting Surapadma, and restoring devas. Folk tellings add six-day vigil and fasting broken on Shashti night with temple darshan.",
        storyHi="पुराण युद्ध में मुरुगन को पार्वती से वेल; सुरपद्म वध; देवता रक्षा। लोक में छः दिन जागरण–व्रत; षष्ठी रात दर्शन।",
        mythologyEn="The festival braids Shaiva–Shakta family lore (Shiva's son) with Tamil bhakti poetry and diaspora kavadi vows.",
        mythologyHi="उत्सव शिव–पुत्र और तमिल भक्ति काव्य, प्रवासी कावड़ी व्रत से जुड़ा।",
        deityStories=[
            {"deity": "Murugan / Kartikeya", "deityHi": "मुरुगन / कार्तिकेय", "en": "Six-faced commander whose vel ends injustice.", "hi": "षण्मुख सेनापति — वेल अन्याय का अंत।"},
        ],
        howCelebratedEn=["Six-day fast or partial fast with one meal (follow health)", "Read Kartikeya story; optional Kavasam intro verses", "Visit Murugan temple on Shashti if possible", "Break fast after evening darshan / arati"],
        howCelebratedHi=["छः दिन व्रत या एक ताल (स्वास्थ्य पहले)", "कार्तिकेय कथा; कवच प्रारंभ पंक्तियाँ", "षष्ठी को मुरुगन दर्शन", "संध्या आरती के बाद पारण"],
        diasporaEn="Singapore and Malaysia Thaipusam/Shashti crowds carry kavadi; apartment shrines use livestream from Palani or Thiruchendur.",
        diasporaHi="सिंगापुर–मलेशिया कावड़ी; फ्लैट में पलनी–तिरुचेंदूर लाइव।",
        regions=[{"region": "Tamil Nadu", "notes": "Thiruchendur Soora Samharam peak."}, {"region": "Diaspora", "notes": "Murugan temples worldwide."}],
        relatedDevotion=["murugan-kanda-intro", "devi-aarti"],
        relatedTemples=["thiruchendur-murugan", "palani-murugan", "meenakshi-madurai"],
    ),
    fest_entry(
        slug="thaipusam",
        name="Thaipusam",
        nameHi="थाइपूसम",
        importance="high",
        dateNames=["Thaipusam", "Thai Poosam"],
        summary="Tamil Thai month Purnima — Murugan devotion with kavadi, milk offerings, and vow fulfilment.",
        summaryHi="तमिल मास Thai की पूर्णिमा — कावड़ी, दूध अर्पण, व्रत पूर्ति।",
        meaningEn="Thaipusam marks the day Murugan received the vel from Parvati (in popular telling) or his victory day — observed with kavadi bearers, milk pots, and head-shaving vows.",
        meaningHi="थाइपूसम — मुरुगन को वेल प्राप्ति / विजय दिवस; कावड़ी, पाल कुड़म, मुंडन।",
        storyEn="Devotees carry physical burdens as symbolic sharing of Murugan's battle; Palani and Batu Caves (Malaysia) become global images of faith.",
        storyHi="भक्त शारीरिक बोझ मुरुगन युद्ध का प्रतीक मानते; पलनी, बatu गुफाएँ विश्व चित्र।",
        mythologyEn="Links to Skanda Purana battle motifs and Tamil saint poetry; not a North Indian calendar duplicate of Shashti though themes overlap.",
        mythologyHi="स्कंद पुराण और तमिल संत काव्य; उत्तर भारत की षष्ठी से अलग तिथि, विषय मिलते।",
        deityStories=[{"deity": "Murugan", "deityHi": "मुरुगन", "en": "Vel-bearing lord of disciplined courage.", "hi": "वेलधारी अनुशासित साहस के देव।"}],
        howCelebratedEn=["Prepare kavadi/milk offering with temple guidance", "Fast or sattvic diet before procession", "Chant Murugan names during walk", "Offer at hill Murugan shrine when safe"],
        howCelebratedHi=["मंदिर मार्गदर्शन से कावड़ी/पाल कुड़म", "यात्रा से पहले सात्विक आहार", "नाम जप", "पहाड़ी मुरुगन मंदिर अर्पण"],
        diasporaEn="Batu Caves Malaysia, Singapore Tank Road, and Sydney Murugan temples anchor diaspora Thaipusam.",
        diasporaHi="बatu गुफा, सिंगापुर, सिडनी — प्रवासी थाइपूसम।",
        regions=[{"region": "Tamil Nadu & Kerala", "notes": "Palani climb peaks."}, {"region": "Southeast Asia diaspora", "notes": "Major public processions."}],
        relatedDevotion=["murugan-kanda-intro"],
        relatedTemples=["palani-murugan", "thiruchendur-murugan"],
    ),
    fest_entry(
        slug="gangaur",
        name="Gangaur",
        nameHi="गणगौर",
        importance="high",
        dateNames=["Gangaur", "Gauri Tritiya"],
        summary="Rajasthan spring festival of Gauri–Shiva — clay idols, women’s songs, and marital bliss vows.",
        summaryHi="राजस्थान वसंत गauri–शिव उत्सव — मिट्टी प्रतिमा, महिला गीत, सौभाग्य।",
        meaningEn="Gangaur begins after Holi: women worship Gauri (Parvati) and Isar (Shiva) for happy marriage and harvest. Idols are crafted, carried in procession, then immersed.",
        meaningHi="होली के बाद गणगौर: गौरी–ईशर पूजा, सुखी वैवाहिक जीवन, फसल। प्रतिमा विसर्जन।",
        storyEn="Folk memory links Gauri’s visit to her parents’ home and Shiva following as guest — songs tease and bless couples.",
        storyHi="लोक में गौरी मायके, शिव अतिथि — गीतों में दंपति आशीर्वाद।",
        mythologyEn="Bridges Devi tapasya themes with desert water scarcity prayers.",
        mythologyHi="देवी तप और मरुस्थल जल प्रार्थना जोड़ता।",
        deityStories=[
            {"deity": "Gauri / Parvati", "deityHi": "गौरी / पार्वती", "en": "Mother of marital grace.", "hi": "वैवाहिक कृपा की माँ।"},
            {"deity": "Isar / Shiva", "deityHi": "ईशर / शिव", "en": "Ascetic husband who joins the folk procession.", "hi": "संयासी पति जो जुलूस में आते।"},
        ],
        howCelebratedEn=["Make or buy clay Gauri–Isar", "Daily evening songs until immersion", "Apply mehndi; share sweets", "Immerse on final day at water body"],
        howCelebratedHi=["मिट्टी गauri–ईशर", "विसर्जन तक संध्या गीत", "मेहँदी, मिष्ठान", "अंतिम दिन जल विसर्जन"],
        diasporaEn="Rajasthani diaspora in Gulf and US hosts community Gangaur with photo idols when clay is impractical.",
        diasporaHi="खाड़ी–अमेरिका में राजस्थानी समुदाय फोटो प्रतिमा से गणगौर।",
        regions=[{"region": "Rajasthan", "notes": "Jaipur royal procession famous."}, {"region": "Gujarat border", "notes": "Shared spring rites."}],
        relatedDevotion=["devi-aarti", "shiva-aarti"],
        relatedTemples=["pavagadh-kalika", "somnath"],
    ),
    fest_entry(
        slug="sheetala-ashtami",
        name="Sheetala Ashtami (Basoda)",
        nameHi="शीतला अष्टमी (बसोड़ा)",
        importance="high",
        dateNames=["Sheetala Ashtami", "Basoda", "Sheetla Ashtami"],
        summary="Spring Ashtami to Sheetala Mata — cold stale food offered, pox and heat ailments remembered.",
        summaryHi="वसंत अष्टमी शीतला माता — ठंडा भोजन, चेचक–गर्मी स्मृति।",
        meaningEn="Sheetala Ashtami follows Holi in many North Indian calendars. Fire is not lit; yesterday's food (basoda) is offered to the goddess who cools fevers.",
        meaningHi="होली के बाद अनेक उत्तर भारतीय पंचांग में शीतला अष्टमी। अग्नि नहीं; कल का भोजन (बसोड़ा) शीतला को।",
        storyEn="Linked to Sheetala Mata story — see TirthaYatra katha page. Villages once prayed when smallpox spread; today hygiene and Devi gratitude merge.",
        storyHi="शीतला माता कथा से जुड़ा — TirthaYatra पृष्ठ। गाँव में चेचक काल प्रार्थना; आज स्वच्छता और देवी कृतज्ञता।",
        mythologyEn="Cooling goddess on donkey with broom — sweeps disease, teaches rest and simple diet one day.",
        mythologyHi="गधे पर शीतला, झाड़ू — रोग झाड़, विश्राम और सरल आहार।",
        deityStories=[{"deity": "Sheetala Mata", "deityHi": "शीतला माता", "en": "Goddess of coolness and recovery.", "hi": "शीतलता और स्वस्थ recovery की देवी।"}],
        howCelebratedEn=["Cook day before; eat cold food on Ashtami", "Sheetala Mata puja and katha", "Avoid fresh cooking as custom allows", "Share food with neighbours"],
        howCelebratedHi=["पहले दिन पकाएँ; अष्टमी ठंडा भोजन", "शीतला पूजा–कथा", "रीति अनुसार अग्नि नहीं", "पड़ोस बाँटें"],
        diasporaEn="NCR and UK Punjabi/Haryanvi communities observe Basoda in apartments with fridge prasad.",
        diasporaHi="NCR, UK में बसोड़ा फ्रिज प्रसाद से।",
        regions=[{"region": "North & West India", "notes": "Strong in Haryana, UP, Rajasthan."}],
        relatedDevotion=["devi-aarti"],
        relatedTemples=["sheetla-mata-gurgaon", "sheetla-mata-ludhiana"],
    ),
    fest_entry(
        slug="sharad-purnima",
        name="Sharad Purnima (Kojagiri Purnima)",
        nameHi="शरद पूर्णिमा (कोजागिरी)",
        importance="high",
        dateNames=["Sharad Purnima", "Kojagiri Purnima", "Kheer Purnima"],
        summary="Autumn full moon — kheer under moonlight, Lakshmi vigil, and health-giving rays lore.",
        summaryHi="शरद पूर्णिमा — चंद्र प्रकाश में खीर, लक्ष्मी जागरण।",
        meaningEn="Ashwin Shukla Purnima: devotees keep kheer in moonlight, stay awake (kojagiri = who is awake), and honour Lakshmi–Radha–Krishna ras.",
        meaningHi="आश्विन शुक्ल पूर्णिमा: चंद्र में खीर, जागरण, लक्ष्मी–राधा–कृष्ण रास।",
        storyEn="Folk belief holds moon's nectar touches earth this night; Braj remembers Raas; Bengal links Lakshmi puja.",
        storyHi="लोक मानता चंद्र अमृत धरती छूता; ब्रज रास; बंगाल लक्ष्मी।",
        mythologyEn="Bridges harvest gratitude with Vaishnava moon love — not a substitute for Diwali but its poetic prelude in some regions.",
        mythologyHi="फसल कृतज्ञता और वैष्णव चंद्र प्रेम; दीपावली पूर्व संगीत क्षेत्रों में।",
        deityStories=[
            {"deity": "Lakshmi", "deityHi": "लक्ष्मी", "en": "Walks earth asking 'who is awake?'", "hi": "पृथ्वी पर 'कौन जाग रहा' पूछती।"},
            {"deity": "Krishna", "deityHi": "कृष्ण", "en": "Raas on Sharad Purnima in Braj memory.", "hi": "ब्रज में शरद रास स्मृति।"},
        ],
        howCelebratedEn=["Prepare kheer; place in moonlight", "Light lamps; Lakshmi aarti", "Stay up modestly with family kirtan", "Share sweet with neighbours"],
        howCelebratedHi=["खीर बनाएँ; चंद्र में रखें", "दीप, लक्ष्मी आरती", "परिवार कीर्तन से जागरण", "मिष्ठान बाँटें"],
        diasporaEn="Balcony moon sighting and LED 'moon' for high-rise diaspora when clouds block sky.",
        diasporaHi="बालकनी चंद्र; बादल में LED चंद्र प्रवासी।",
        regions=[{"region": "North & West", "notes": "Kojagiri parties."}, {"region": "Braj", "notes": "Raas lore."}],
        relatedDevotion=["lakshmi-aarti", "krishna-aarti"],
        relatedTemples=["banke-bihari-vrindavan", "tirumala-venkateswara"],
    ),
    fest_entry(
        slug="chaitra-navaratri",
        name="Chaitra Navaratri",
        nameHi="चैत्र नवरात्रि",
        importance="high",
        dateNames=["Chaitra Navaratri", "Vasant Navaratri", "Ram Navami season Navaratri"],
        summary="Spring nine nights of Devi — distinct calendar from Sharad Navaratri; ends toward Ram Navami.",
        summaryHi="वसंत की नौ रातें देवी — शरद से अलग; राम नवमी की ओर।",
        meaningEn="Chaitra Shukla Pratipada starts this Navaratri. Many fast nine days, worship Durga forms daily, and celebrate Ram Navami on Chaitra Navami within the same lunar month.",
        meaningHi="चैत्र शुक्ल प्रतिपदा से आरंभ। नौ दिन व्रत, प्रतिदिन दुर्गा स्वरूप; चैत्र नवमी राम नवमी।",
        storyEn="Same Mahishasura victory arc as autumn Navaratri but timed to spring renewal and Rama's birth season — reduces confusion when searching dates.",
        storyHi="शरद जैसी विजय कथा पर वसंत नवीनता और राम जन्म ऋतु — तिथि खोज में स्पष्टता।",
        mythologyEn="Nine forms (Navadurga) vary by region; follow local temple list.",
        mythologyHi="नवदुर्गा सूची क्षेत्र अनुसार; स्थानीय मंदिर देखें।",
        deityStories=[{"deity": "Durga / Navadurga", "deityHi": "दुर्गा / नवदुर्गा", "en": "Spring nine-night mother.", "hi": "वसंत नौ रात की माँ।"}],
        howCelebratedEn=["Ghatasthapana on day 1", "Daily Devi aarti and colour tradition if your family uses it", "Read Chaitra katha; plan Ram Navami", "Break fast on Navami with prasad"],
        howCelebratedHi=["प्रतिपदा घट स्थापना", "दैनिक देवी आरती", "चैत्र कथा; राम नवमी योजना", "नवमी पारण"],
        diasporaEn="Temples label 'Spring Navaratri' explicitly for diaspora calendars confused with October.",
        diasporaHi="प्रवासी मंदिर 'वसंत नवरात्रि' स्पष्ट लिखते।",
        regions=[{"region": "North India", "notes": "Ram Navami overlap."}, {"region": "Maharashtra", "notes": "Gudi Padwa same month start."}],
        relatedDevotion=["navaratri-vrat-katha", "devi-aarti", "rama-aarti"],
        relatedTemples=["vaishno-devi", "kamakhya", "chintpurni-temple"],
    ),
    fest_entry(
        slug="parashurama-jayanti",
        name="Parashurama Jayanti",
        nameHi="परशुराम जयंती",
        importance="medium",
        dateNames=["Parashurama Jayanti", "Parashuram Jayanti"],
        summary="Chaitra Shukla Tritiya birth of Vishnu's sixth avatar — axe, dharma, and Konkan–Kerala lore.",
        summaryHi="चैत्र शुक्ल तृतीया — विष्णु छठे अवतार का जन्म; परशु, धर्म, कोंकण–केरल।",
        meaningEn="Parashurama Jayanti remembers the brahmin warrior who corrected kshatriya tyranny. Akshaya Tritiya sometimes overlaps in popular calendars — confirm with your panchang.",
        meaningHi="परशुराम जयंती — ब्राह्मण योद्धा जिसने क्षत्रिय अत्याचार सुधारा। अक्षय तृतीया कभी मेल — पंचांग देखें।",
        storyEn="See TirthaYatra parashurama-avatar story for fuller telling. Homes avoid glorifying violence; they ask where skill must serve justice today.",
        storyHi="TirthaYatra parashurama-avatar कथा विस्तार। घर हिंसा महिमा नहीं — कौशल आज न्याय हेतु।",
        mythologyEn="Coastal India remembers Parashurama reclaiming land and training martial arts — regional lists vary.",
        mythologyHi="तट भारत भूमि और शस्त्र शिक्षा स्मृति — क्षेत्र अनुसार भिन्न।",
        deityStories=[{"deity": "Parashurama", "deityHi": "परशुराम", "en": "Vishnu avatar with axe of correction.", "hi": "परशु वाले सुधारक अवतार।"}],
        howCelebratedEn=["Read avatar story", "Vishnu aarti", "Donate to learning or teacher", "Visit trimbakeshwar region if on yatra"],
        howCelebratedHi=["अवतार कथा", "विष्णु आरती", "शिक्षा/गुरु दान", "त्र्यंबक यात्रा हो तो दर्शन"],
        diasporaEn="Vishnu mandirs mark Jayanti with short katha; families tie to spring cleaning of tools and kitchen.",
        diasporaHi="विष्णु मंदिर लघु कथा; वसंत में रसोई–औजार सफाई।",
        regions=[{"region": "Konkan & Kerala", "notes": "Strong local lore."}, {"region": "North India", "notes": "Jayanti puja at home."}],
        relatedDevotion=["vishnu-aarti", "vishnu-chalisa"],
        relatedTemples=["trimbakeshwar", "rameswaram"],
    ),
]


FESTIVAL_FIXED_DATES = [
    {"date": "2025-01-12", "name": "Thaipusam", "nameHi": "थाइपूसम", "importance": "high"},
    {"date": "2025-03-22", "name": "Sheetala Ashtami", "nameHi": "शीतला अष्टमी", "importance": "high"},
    {"date": "2025-03-30", "name": "Chaitra Navaratri begins", "nameHi": "चैत्र नवरात्रि आरंभ", "importance": "high"},
    {"date": "2025-04-01", "name": "Parashurama Jayanti", "nameHi": "परशुराम जयंती", "importance": "medium"},
    {"date": "2025-04-02", "name": "Gangaur (approx peak)", "nameHi": "गणगौर", "importance": "high"},
    {"date": "2025-10-07", "name": "Sharad Purnima", "nameHi": "शरद पूर्णिमा", "importance": "high"},
    {"date": "2025-10-28", "name": "Skanda Shashti", "nameHi": "स्कंद षष्ठी", "importance": "high"},
    {"date": "2026-01-31", "name": "Thaipusam", "nameHi": "थाइपूसम", "importance": "high"},
    {"date": "2026-03-11", "name": "Sheetala Ashtami", "nameHi": "शीतला अष्टमी", "importance": "high"},
    {"date": "2026-03-19", "name": "Chaitra Navaratri begins", "nameHi": "चैत्र नवरात्रि आरंभ", "importance": "high"},
    {"date": "2026-03-21", "name": "Parashurama Jayanti", "nameHi": "परशुराम जयंती", "importance": "medium"},
    {"date": "2026-03-22", "name": "Gangaur (approx peak)", "nameHi": "गणगौर", "importance": "high"},
    {"date": "2026-09-26", "name": "Sharad Purnima", "nameHi": "शरद पूर्णिमा", "importance": "high"},
    {"date": "2026-10-17", "name": "Skanda Shashti", "nameHi": "स्कंद षष्ठी", "importance": "high"},
    {"date": "2027-01-20", "name": "Thaipusam", "nameHi": "थाइपूसम", "importance": "high"},
    {"date": "2027-03-01", "name": "Sheetala Ashtami", "nameHi": "शीतला अष्टमी", "importance": "high"},
    {"date": "2027-03-09", "name": "Chaitra Navaratri begins", "nameHi": "चैत्र नवरात्रि आरंभ", "importance": "high"},
    {"date": "2027-03-11", "name": "Parashurama Jayanti", "nameHi": "परशुराम जयंती", "importance": "medium"},
    {"date": "2027-03-12", "name": "Gangaur (approx peak)", "nameHi": "गणगौर", "importance": "high"},
    {"date": "2027-10-15", "name": "Sharad Purnima", "nameHi": "शरद पूर्णिमा", "importance": "high"},
    {"date": "2027-10-06", "name": "Skanda Shashti", "nameHi": "स्कंद षष्ठी", "importance": "high"},
]


NEW_DEVOTION = [
    {
        "slug": "venkateswara-aarti",
        "type": "aarti",
        "deity": "vishnu",
        "title": "Venkateswara Aarti — Om Jai Lakshmi Ramana",
        "titleHi": "वेंकटेश्वर आरती — ॐ जय लक्ष्मी रमणा",
        "author": "Traditional",
        "when": "Tirupati darshan, Friday Vishnu puja, Balaji home shrines",
        "summary": "Traditional Govinda/Balaji aarti-style verses commonly sung at Tirupati and North Indian Vishnu temples.",
        "verses": [
            "ॐ जय लक्ष्मी रमणा, स्वामी जय लक्ष्मी रमणा।\nवेंकटेश्वर स्वामी, जय लक्ष्मी रमणा॥",
            "श्रीनिवास गोविंद, श्री वेंकटेश्वर।\nभक्त जनों के प्रभु, जय लक्ष्मी रमणा॥",
            "कमलाक्ष नायक, कमला संग वासी।\nवेदांत वेद्य, जय लक्ष्मी रमणा॥",
            "करुणा सागर, कृपा करो स्वामी।\nशरणागत वत्सल, जय लक्ष्मी रमणा॥",
            "ॐ जय लक्ष्मी रमणा, स्वामी जय लक्ष्मी रमणा॥\nगोविंदा गोविंदा, गोविंदा गोविंदा॥",
        ],
        "meaning": "Classic Balaji aarti invoking Srinivasa as Lakshmi's lord — mercy for surrendered devotees. Wording varies by temple; follow your local sangrah.",
        "relatedTemples": ["tirumala-venkateswara"],
        "completeText": True,
        "sangrahLabel": "वेंकटेश्वर / बालाजी",
        "audioNote": "Optional listen-along may be added later; confirm verses with your family or temple custom.",
    },
    {
        "slug": "annapurna-aarti",
        "type": "aarti",
        "deity": "devi",
        "title": "Annapurna Aarti — Annadatri Annapurna Bhavani",
        "titleHi": "अन्नपूर्णा आरती — अन्नदात्री अन्नपूर्णा भवानी",
        "author": "Traditional",
        "when": "Before meals, Devi Friday, Annapurna Jayanti, Kashi memory",
        "summary": "Traditional Annapurna praise — Goddess of food who feeds Shiva and the world.",
        "verses": [
            "जय अन्नपूर्णा माता, जय अन्नपूर्णा माता।\nअक्षय मुक्ति दात्री, जय अन्नपूर्णा माता॥",
            "शिव योगी तुम्हें माँगे, भिक्षा देती माँ।\nसंसार जीव जगाती, जय अन्नपूर्णा माता॥",
            "काशी में विराजमान, भक्तों को शक्ति दो।\nअन्नदान की महिमा, जय अन्नपूर्णा माता॥",
            "ॐ जय अन्नपूर्णा माता॥",
        ],
        "meaning": "Annapurna as mother who grants food and liberation-through-nourishment; pairs with the story of Shiva begging alms.",
        "relatedTemples": ["kashi-vishwanath", "horanadu-annapoorneshwari" if False else "kashi-vishwanath"],
        "completeText": True,
        "sangrahLabel": "अन्नपूर्णा माता",
        "audioNote": "Regional wording differs; follow Kashi or home Devi custom.",
    },
    {
        "slug": "murugan-kanda-intro",
        "type": "aarti",
        "deity": "ganesha",
        "title": "Kanda Sashti Kavasam — intro and opening",
        "titleHi": "कंद षष्ठी कवचम् — परिचय और प्रारंभ",
        "author": "Traditional Tamil devotion · TirthaYatra intro",
        "when": "Skanda Shashti week; morning listen or read before full path with teacher",
        "summary": "Original TirthaYatra introduction to the Kanda Sashti Kavasam tradition with widely known opening lines only — full Tamil path varies by edition and teacher.",
        "verses": [
            "Thiruppugazh–Kavasam tradition honours Murugan as Skanda, giver of the vel spear.\n\nOpening lines commonly sung (Tamil — transliteration for learning):\n\n'Vel Vel Vetri Vel' — Victory to the spear of Murugan.\n'Saravanabhava' — homage to the lord born in Saravana.\n\nFull Kavasam is long; learn from authentic Tamil Murugan teachers or temple classes — do not treat this page as a complete commercial text.",
        ],
        "meaning": "The Kavasam is armour-poetry for Murugan's protection during Shashti vows. TirthaYatra shares meaning and a few public-domain opening motifs; complete path requires living Tamil instruction.",
        "relatedTemples": ["palani-murugan", "thiruchendur-murugan"],
        "completeText": False,
        "sangrahLabel": "मुरुगन / स्कंद",
        "audioNote": "Seek full Kavasam from qualified Murugan bhakti sources in Tamil Nadu or diaspora temples.",
    },
    {
        "slug": "shani-aarti",
        "type": "aarti",
        "deity": "shiva",
        "title": "Shani Aarti — Jai Jai Shri Shani Deva",
        "titleHi": "शनि आरती — जय जय श्री शनि देव",
        "author": "Traditional",
        "when": "Shani Amavasya, Saturdays, Shani Shingnapur/Shani temples",
        "summary": "Traditional Shani Dev aarti — justice, patience, and graha shanti.",
        "verses": [
            "जय जय श्री शनि देवा, स्वामी जय श्री शनि देवा।\nनीलांजन समाभासं, रवि पुत्र नमोस्तुते॥",
            "काल के देवता, न्याय के धाम।\nदण्ड देते धीरे, कर्म फल स्वाम॥\nजय जय श्री शनि देवा॥",
            "शनि शिंगणापुर, शनि मंदिर में।\nभक्त जन प्रार्थना, शांति मन में॥\nजय जय श्री शनि देवा॥",
            "ॐ शं शनैश्चराय नमः॥\nजय जय श्री शनि देवा॥",
        ],
        "meaning": "Shani as slow, just Saturn — not to fear but to respect through honest work and Saturday lamp.",
        "relatedTemples": ["shani-shingnapur"],
        "completeText": True,
        "sangrahLabel": "शनि देव",
        "audioNote": "Pair with Shani Chalisa on Saturdays; confirm local temple custom.",
    },
    {
        "slug": "vitthal-abhang-intro",
        "type": "aarti",
        "deity": "krishna",
        "title": "Vitthal Abhang — Warkari intro",
        "titleHi": "विठ्ठल अभंग — वारकरी परिचय",
        "author": "Warkari tradition · TirthaYatra intro",
        "when": "Ashadhi/Kartiki Wari, Ekadashi, Pandharpur memory",
        "summary": "Original intro to Warkari abhang devotion with traditional public lines attributed to the saint tradition — learn full Marathi from authentic Warkari sources.",
        "verses": [
            "Warkari bhakti walks to Pandharpur singing abhangs — verses of Vitthal (Vithoba) as the Lord who stood on Pundalik's brick.\n\nLines attributed to Sant Tukaram tradition (meaning in English):\n'Vithoba, you stood waiting — teach me patience in seva.'\n\nMarathi originals vary by edition; visit Warkari kirtan or Varkari math to learn pronunciation and full abhang corpus.",
        ],
        "meaning": "Abhangs are Marathi devotional poems of the Vitthal–Rakhumai bhakti movement. TirthaYatra offers English meaning and encourages learning from living Warkari teachers, not republishing copyrighted modern editions.",
        "relatedTemples": ["pandharpur-vitthal"],
        "completeText": False,
        "sangrahLabel": "विठ्ठल / विटोबा",
        "audioNote": "Listen to Pandharpur wari kirtan recordings on YouTube from reputable Warkari channels.",
    },
]

# fix annapurna temple ref
for d in NEW_DEVOTION:
    if d["slug"] == "annapurna-aarti":
        d["relatedTemples"] = ["kashi-vishwanath"]
    if d["slug"] == "murugan-kanda-intro":
        d["deity"] = "shiva"


def prepare_story_for_write(story: dict) -> dict:
    """Attach composed details, strip internal keys."""
    s = dict(story)
    if not s.get("storyDetailEn"):
        s["storyDetailEn"] = craft_expansion_en(s)
    if not s.get("storyDetailHi"):
        s["storyDetailHi"] = craft_expansion_hi(s)
    new_slugs = {x["slug"] for x in NEW_STORY_SEEDS}
    min_rs = 360 if s.get("slug") in new_slugs else 300
    detail_secs = read_seconds_from_detail(s["storyDetailEn"], minimum=min_rs)
    s["readSeconds"] = max(s.get("readSeconds", 0), detail_secs)
    tags = list(s.get("tags") or [])
    if "long-read" not in tags:
        tags.append("long-read")
    s["tags"] = tags
    for k in ("_detailExtraEn", "_detailExtraHi"):
        s.pop(k, None)
    return s


def add_stories(data: dict, temple_slugs: set, fest_slugs: set, dev_slugs: set) -> tuple[list[str], int]:
    existing = {s["slug"] for s in data["stories"]}
    added = []
    expanded = 0
    for seed in NEW_STORY_SEEDS:
        if seed["slug"] in existing:
            continue
        story = prepare_story_for_write(filter_related(dict(seed), temple_slugs, fest_slugs, dev_slugs))
        data["stories"].append(story)
        added.append(story["slug"])
        existing.add(story["slug"])

    for i, story in enumerate(data["stories"]):
        if story.get("storyDetailEn"):
            if word_count(story.get("storyDetailHi", "")) >= 400:
                continue
            s = dict(story)
            s["storyDetailHi"] = craft_expansion_hi(s)
            data["stories"][i] = s
            expanded += 1
            continue
        updated = prepare_story_for_write(story)
        data["stories"][i] = updated
        expanded += 1

    return added, expanded


def add_temples() -> list[str]:
    existing = {p.stem for p in TEMPLES_DIR.glob("*.json")}
    created = []
    for seed in NEW_TEMPLES:
        slug = seed["slug"]
        if slug in existing:
            continue
        tags_extra = seed.pop("tags_extra", None) or []
        detail = base_detail(dict(seed))
        detail["deityFamilies"] = seed.get("deityFamilies") or infer_deity_families(seed)
        tags = list(detail.get("tags") or [])
        for t in tags_extra:
            if t not in tags:
                tags.append(t)
        detail["tags"] = tags
        detail = attach_portal(detail)
        detail = enrich_myth_fields(detail)
        if detail.get("lat") is None or detail.get("lng") is None:
            raise SystemExit(f"Missing coords for {slug}")
        dump_json(TEMPLES_DIR / f"{slug}.json", detail)
        created.append(slug)
        existing.add(slug)
    if created:
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "assign_deities.py")])
    return created


def add_festivals(fest_data: dict) -> list[str]:
    festivals = fest_data["festivals"]
    existing = {f["slug"] for f in festivals}
    added = []
    for entry in NEW_FESTIVALS:
        if entry["slug"] in existing:
            continue
        festivals.append(entry)
        added.append(entry["slug"])
        existing.add(entry["slug"])
    return added


def add_festival_dates(fest_json: dict) -> int:
    fixed = fest_json.setdefault("fixed", [])
    existing = {(x["date"], x["name"]) for x in fixed}
    n = 0
    for entry in FESTIVAL_FIXED_DATES:
        key = (entry["date"], entry["name"])
        if key in existing:
            continue
        fixed.append(entry)
        existing.add(key)
        n += 1
    fixed.sort(key=lambda x: x["date"])
    return n


def add_devotion(dev_data: dict, temple_slugs: set) -> list[str]:
    items = dev_data["items"]
    existing = {d["slug"] for d in items}
    added = []
    for entry in NEW_DEVOTION:
        if entry["slug"] in existing:
            continue
        e = dict(entry)
        e["relatedTemples"] = [t for t in e.get("relatedTemples", []) if t in temple_slugs]
        items.append(e)
        added.append(e["slug"])
        existing.add(e["slug"])
    return added


def update_engagement(added_stories: list[str], added_devotion: list[str]) -> None:
    engage = load_json(DATA / "engagement.json")
    rot = engage.setdefault("dailyRotation", {})
    for slug in added_stories:
        if slug not in rot.setdefault("story", []):
            rot["story"].append(slug)
    for slug in added_devotion:
        if slug not in rot.setdefault("aarti", []):
            rot["aarti"].append(slug)
    katha_map = {
        "murugan-kanda-intro": "murugan-kanda-intro",
    }
    for slug in added_devotion:
        if slug.endswith("-vrat-katha") or slug in katha_map:
            kslug = katha_map.get(slug, slug)
            if kslug not in rot.setdefault("katha", []):
                rot["katha"].append(kslug)
    dump_json(DATA / "engagement.json", engage)


def update_stories_lede(data: dict) -> None:
    data["section"]["lede"] = (
        "Short myth stories (about a minute) plus optional fuller bilingual tellings — "
        "the event, the deities, why the ritual remembers them, and home-practice meaning. "
        "Tap through for the long read when you have time."
    )
    if "ledeHi" in data["section"]:
        data["section"]["ledeHi"] = (
            "लगभग एक मिनट की छोटी कथाएँ और वैकल्पिक विस्तृत द्विभाषी वर्णन — "
            "घटना, देवता, रीति की स्मृति, और घर में अभ्यास। समय हो तो लंबी कथा पढ़ें।"
        )


def update_backlog(added_stories: list[str], added_temples: list[str], added_fests: list[str], added_dev: list[str]) -> None:
    backlog = load_json(DATA / "content-backlog.json")
    shipped = backlog.setdefault("shippedThisBatch", {})
    for key, items in (
        ("stories", added_stories),
        ("temples", added_temples),
        ("festivals", added_fests),
        ("devotion", added_dev),
    ):
        lst = shipped.setdefault(key, [])
        for s in items:
            if s not in lst:
                lst.append(s)

    # Mark priority lists done / clear
    priority = backlog.get("priority", {})
    for plist in list(priority.values()):
        if isinstance(plist, list):
            for item in plist:
                if isinstance(item, dict):
                    slug = item.get("slug", "")
                    item["status"] = "done"
                    item["shipped"] = (
                        slug in added_stories + added_temples + added_fests + added_dev
                        or slug.endswith("exists")
                        or "already" in slug
                        or "SKIP" in item.get("note", "")
                    )
    backlog["priority"] = {
        "P0_next_stories": [],
        "P0_temples_to_add": [],
        "P1_festivals_vrats": [],
        "P1_devotion": [],
        "note": "Batch shipped 2026-08-14 via build_full_backlog.py — see shippedThisBatch.",
    }
    backlog["updated"] = "2026-08-14"
    dump_json(DATA / "content-backlog.json", backlog)


def main() -> None:
    global PORTALS
    PORTALS = load_json(DATA / "state-portals.json")

    temple_index = load_json(DATA / "temples.json")
    temple_slugs = {t["slug"] for t in temple_index}
    fest_data = load_json(DATA / "festival-guide.json")
    fest_slugs = {f["slug"] for f in fest_data["festivals"]}
    dev_data = load_json(DATA / "devotion.json")
    dev_slugs = {d["slug"] for d in dev_data["items"]}

    created_temples = add_temples()
    temple_index = load_json(DATA / "temples.json")
    temple_slugs = {t["slug"] for t in temple_index}

    added_fests = add_festivals(fest_data)
    fest_slugs = {f["slug"] for f in fest_data["festivals"]}

    added_dev = add_devotion(dev_data, temple_slugs)
    dev_slugs = {d["slug"] for d in dev_data["items"]}

    stories_data = load_json(DATA / "stories.json")
    added_stories, expanded = add_stories(stories_data, temple_slugs, fest_slugs, dev_slugs)
    update_stories_lede(stories_data)
    dump_json(DATA / "stories.json", stories_data)

    dump_json(DATA / "festival-guide.json", fest_data)

    fest_json = load_json(DATA / "festivals.json")
    added_dates = add_festival_dates(fest_json)
    dump_json(DATA / "festivals.json", fest_json)

    dump_json(DATA / "devotion.json", dev_data)

    update_engagement(added_stories, added_dev)
    update_backlog(added_stories, created_temples, added_fests, added_dev)

    print("=== build_full_backlog.py summary ===")
    print(f"Stories added: {len(added_stories)} — {', '.join(added_stories) or '(none)'}")
    print(f"Stories expanded with storyDetail: {expanded}")
    print(f"Temples created: {len(created_temples)} — {', '.join(created_temples) or '(none)'}")
    print(f"Festivals added: {len(added_fests)} — {', '.join(added_fests) or '(none)'}")
    print(f"Festival fixed dates added: {added_dates}")
    print(f"Devotion items added: {len(added_dev)} — {', '.join(added_dev) or '(none)'}")
    print(f"Total stories now: {len(stories_data['stories'])}")
    print(f"Total temples now: {len(temple_index)}")


if __name__ == "__main__":
    main()
