#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add high-search Ramayana & Mahabharata temples + bilingual stories."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES_DIR = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))
from sync_groups import base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")
LABELS = {
    "ramayana-trail": "Ramayana Trail",
    "mahabharata-sites": "Mahabharata Sites",
}


def portal_for(state: str) -> dict:
    p = PORTALS.get(state) or {}
    return {
        "name": p.get("portalName", f"{state} tourism"),
        "url": p.get("portalUrl", "https://tourism.gov.in/"),
        "slug": p.get("slug", state.lower().replace(" ", "-")),
    }


def enrich(seed: dict) -> dict:
    detail = base_detail(seed)
    tags = list(seed.get("tags") or [])
    detail["tags"] = tags
    detail["tagLabels"] = [LABELS[t] for t in tags if t in LABELS]
    detail["deityFamilies"] = list(seed.get("deityFamilies") or [])
    detail["tier"] = seed.get("tier", "famous")
    detail["statePortal"] = portal_for(seed["state"])
    detail["officialWebsite"] = seed.get("officialWebsite") or detail["statePortal"]["url"]
    detail["sources"] = [
        f"{detail['statePortal']['name']}: {detail['statePortal']['url']}",
        "Temple trust / local administration notices",
        "State tourism materials",
        "Puranic / epic / pilgrimage tradition (lists can vary by scripture)",
    ]
    detail["lastUpdated"] = "2026-08-20"
    myth = detail["mythology"]
    detail["mythologySignificance"] = (
        myth
        + "\n\nClassical pilgrimage teaching places this tirtha within India’s epic geography. "
        "Epic, Puranic, and regional mahatmya literature — not a single uniform text — sustain "
        "this sacred memory."
    )
    detail["localBeliefs"] = (
        f"In popular pilgrimage memory, {seed['name']} is especially associated with {seed.get('famousFor', seed['name'])}. "
        "Guides and elders retell this identity to first-time visitors as the living reason the tirtha draws crowds.\n\n"
        "Local sthala-purana and priestly teaching elaborate how the deity blesses devotees who arrive with vows, "
        "gratitude, or grief. Festival days intensify these beliefs through processions, special alankara, and "
        "community feeding where practised."
    )
    detail["mythologyDisclaimer"] = (
        "Mythological accounts and local beliefs are drawn from Puranic traditions, epics, and widely recorded "
        "sthala-purana / pilgrimage lore. Versions differ by scripture, region, and temple tradition. This section "
        "is for cultural understanding — not a claim of historical fact, nor a substitute for guidance from temple "
        "priests or official trusts."
    )
    return detail


TEMPLES = [
    {
        "slug": "kanak-bhawan-ayodhya",
        "name": "Kanak Bhawan, Ayodhya",
        "deity": "Lord Rama & Goddess Sita",
        "location": "Ramkot, Ayodhya, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "क",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["rama", "vishnu"],
        "summary": "Kanak Bhawan — Ayodhya’s beloved Rama–Sita palace shrine, among the most searched Ramayana temples after Ram Mandir.",
        "famousFor": "Rama–Sita ‘palace’ temple · gold-leaf memory of Kaikeyi’s gift",
        "mythology": "Tradition remembers Kanak Bhawan as the palace gifted to Sita by Kaikeyi. Devotees flock here for intimate Rama–Sita darshan beside the Ram Janmabhoomi corridor — a living Ramayana domestic shrine within Ayodhya’s sacred core.",
        "festivals": ["Ram Navami", "Diwali", "Sita Vivah"],
        "lat": 26.7957,
        "lng": 82.2008,
        "mapQuery": "Kanak Bhawan Ayodhya",
        "nearestRail": "Ayodhya Cantt / Ayodhya Dham",
        "nearestAirport": "Ayodhya / Lucknow",
        "nearby": [
            {"name": "Ram Mandir, Ayodhya", "slug": "ayodhya-ram-mandir", "note": "Adjacent sacred core"},
            {"name": "Hanuman Garhi, Ayodhya", "slug": "hanuman-garhi-ayodhya", "note": "Short walk"},
        ],
    },
    {
        "slug": "shringverpur-prayagraj",
        "name": "Shringverpur, Prayagraj",
        "deity": "Lord Rama (exile crossing memory)",
        "location": "Shringverpur, Prayagraj district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "श्रृ",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["rama"],
        "summary": "Shringverpur — where Rama, Sita, and Lakshmana crossed the Ganga into exile; a core Ramayana Circuit stop.",
        "famousFor": "Ganga crossing of Rama’s vanvas · Nishadraj memory",
        "mythology": "Valmiki’s Ramayana places Rama’s farewell to Ayodhya’s river world at Shringverpur. Nishadraj Guha’s hospitality and the Ganga crossing open the vanvas path toward Chitrakoot — making this ghat among the most searched Ramayana geography sites after Ayodhya.",
        "festivals": ["Ram Navami", "Kartik Purnima"],
        "lat": 25.55,
        "lng": 81.65,
        "mapQuery": "Shringverpur Prayagraj",
        "nearestRail": "Prayagraj Junction",
        "nearestAirport": "Prayagraj / Lucknow",
        "nearby": [
            {"name": "Lete Hanuman Mandir, Prayagraj", "slug": "prayagraj-hanuman", "note": "City darshan"},
        ],
    },
    {
        "slug": "chitrakoot-kamadgiri",
        "name": "Kamadgiri, Chitrakoot",
        "deity": "Lord Rama (exile forest seat)",
        "location": "Kamadgiri Parikrama, Chitrakoot, Madhya Pradesh / Uttar Pradesh border",
        "state": "Madhya Pradesh",
        "glyph": "का",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["rama"],
        "summary": "Kamadgiri — the wish-fulfilling hill of Chitrakoot whose parikrama is the heart of Ramayana exile pilgrimage.",
        "famousFor": "Kamadgiri parikrama · Rama–Sita–Lakshmana forest years",
        "mythology": "Chitrakoot is where Rama, Sita, and Lakshmana spent formative exile years. Kamadgiri’s circuit gathers ghats, caves, and shrines into one of India’s most searched Ramayana forest landscapes — often paired with Ramghat and Gupta Godavari.",
        "festivals": ["Ram Navami", "Diwali"],
        "lat": 25.162,
        "lng": 80.86,
        "mapQuery": "Kamadgiri Chitrakoot",
        "nearestRail": "Chitrakoot Dham Karwi",
        "nearestAirport": "Prayagraj / Khajuraho",
        "nearby": [
            {"name": "Ramghat, Chitrakoot", "slug": "chitrakoot-ramghat", "note": "Riverfront"},
            {"name": "Gupta Godavari, Chitrakoot", "slug": "gupta-godavari-chitrakoot", "note": "Cave tirtha"},
        ],
    },
    {
        "slug": "gupta-godavari-chitrakoot",
        "name": "Gupta Godavari, Chitrakoot",
        "deity": "Lord Rama (cave tirtha)",
        "location": "Gupta Godavari caves, Chitrakoot, Madhya Pradesh",
        "state": "Madhya Pradesh",
        "glyph": "गु",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["rama"],
        "summary": "Gupta Godavari — paired caves of Chitrakoot tied to Rama’s exile and hidden Godavari lore.",
        "famousFor": "Twin caves · exile geography search favourite",
        "mythology": "Pilgrim lore links these cool twin caves to Rama’s forest life and a ‘hidden’ Godavari stream. Together with Kamadgiri and Ramghat, Gupta Godavari is among Chitrakoot’s most photographed and searched Ramayana stops.",
        "festivals": ["Ram Navami"],
        "lat": 25.148,
        "lng": 80.875,
        "mapQuery": "Gupta Godavari Chitrakoot",
        "nearestRail": "Chitrakoot Dham Karwi",
        "nearestAirport": "Prayagraj / Khajuraho",
        "nearby": [
            {"name": "Kamadgiri, Chitrakoot", "slug": "chitrakoot-kamadgiri", "note": "Parikrama hill"},
            {"name": "Ramghat, Chitrakoot", "slug": "chitrakoot-ramghat", "note": "Riverfront"},
        ],
    },
    {
        "slug": "sita-gufa-nashik",
        "name": "Sita Gufa, Nashik",
        "deity": "Goddess Sita / Lord Rama (Panchavati)",
        "location": "Panchavati, Nashik, Maharashtra",
        "state": "Maharashtra",
        "glyph": "सी",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["rama"],
        "summary": "Sita Gufa in Nashik’s Panchavati — cave shrine of Sita’s exile days beside Kalaram Mandir.",
        "famousFor": "Panchavati exile cave · Surpanakha geography",
        "mythology": "Nashik’s Panchavati is remembered as the forest hermitage where Surpanakha met Rama and Sita’s abduction plot began. Sita Gufa keeps that memory underground beside the famous black-stone Kalaram Temple — a high-search Ramayana pair during Nashik Kumbh and year-round.",
        "festivals": ["Ram Navami", "Nashik Kumbh years"],
        "lat": 20.007,
        "lng": 73.792,
        "mapQuery": "Sita Gufa Nashik",
        "nearestRail": "Nashik Road",
        "nearestAirport": "Nashik / Mumbai",
        "nearby": [
            {"name": "Kalaram Temple, Nashik", "slug": "kalaram-temple-nashik", "note": "Adjacent Panchavati"},
        ],
    },
    {
        "slug": "anjanadri-hampi",
        "name": "Anjanadri Hill, Hampi",
        "deity": "Lord Hanuman (Anjaneya birthplace tradition)",
        "location": "Anjanadri / Anegundi, Hampi region, Karnataka",
        "state": "Karnataka",
        "glyph": "अं",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["hanuman", "rama"],
        "summary": "Anjanadri — hill traditionally identified with Hanuman’s birthplace in Kishkindha, opposite Hampi.",
        "famousFor": "Hanuman birthplace · Kishkindha Ramayana geography",
        "mythology": "The Ramayana’s Kishkindha is widely mapped onto the boulder landscape of Hampi–Anegundi. Anjanadri’s steep climb to Anjaneya’s shrine is among India’s most searched Hanuman–Ramayana pilgrimage experiences — paired with Kodandarama Temple below.",
        "festivals": ["Hanuman Jayanti", "Ram Navami"],
        "lat": 15.354,
        "lng": 76.469,
        "mapQuery": "Anjanadri Hill Hampi",
        "nearestRail": "Hospet Junction",
        "nearestAirport": "Hubballi / Ballari",
        "nearby": [
            {"name": "Kodandarama Temple, Hampi", "slug": "kodandarama-hampi", "note": "Kishkindha riverside"},
        ],
    },
    {
        "slug": "kodandarama-hampi",
        "name": "Kodandarama Temple, Hampi",
        "deity": "Lord Rama (Kodanda / bow-bearing)",
        "location": "Hampi / Anegundi riverside, Karnataka",
        "state": "Karnataka",
        "glyph": "को",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["rama", "vishnu"],
        "summary": "Kodandarama Temple on the Tungabhadra — Ramayana Kishkindha shrine in the Hampi landscape.",
        "famousFor": "Rama of Kishkindha · Sugriva–Vali geography",
        "mythology": "Local Ramayana memory places Sugriva’s kingdom and Rama’s alliance in this boulder country. Kodandarama Temple and Anjanadri together form one of South India’s strongest searched Ramayana trail pairs.",
        "festivals": ["Ram Navami", "Vaikuntha Ekadashi"],
        "lat": 15.341,
        "lng": 76.462,
        "mapQuery": "Kodandarama Temple Hampi",
        "nearestRail": "Hospet Junction",
        "nearestAirport": "Hubballi / Ballari",
        "nearby": [
            {"name": "Anjanadri Hill, Hampi", "slug": "anjanadri-hampi", "note": "Hanuman hill"},
        ],
    },
    {
        "slug": "dhanushkodi-rama-setu",
        "name": "Dhanushkodi & Rama Setu viewpoint",
        "deity": "Lord Rama (Setubandha memory)",
        "location": "Dhanushkodi, Rameswaram tip, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "ध",
        "tags": ["ramayana-trail"],
        "deityFamilies": ["rama"],
        "summary": "Dhanushkodi — the land’s end facing Adam’s Bridge / Rama Setu, climax geography of the Ramayana’s Lanka march.",
        "famousFor": "Rama Setu viewpoint · Setubandha pilgrimage",
        "mythology": "After Ramanathaswamy darshan, pilgrims ride to Dhanushkodi where the sea opens toward the chain of shoals remembered as Rama Setu. It is among the most searched Ramayana landscape queries worldwide — epic memory meeting a living shoreline.",
        "festivals": ["Ram Navami", "Maha Shivaratri (with Rameswaram)"],
        "lat": 9.169,
        "lng": 79.416,
        "mapQuery": "Dhanushkodi Rameswaram",
        "nearestRail": "Rameswaram",
        "nearestAirport": "Madurai",
        "nearby": [
            {"name": "Ramanathaswamy Temple, Rameswaram", "slug": "rameswaram", "note": "Jyotirlinga + Char Dham"},
        ],
        "officialWebsite": "https://www.tamilnadutourism.tn.gov.in/",
    },
    {
        "slug": "bhishma-kund-kurukshetra",
        "name": "Bhishma Kund, Kurukshetra",
        "deity": "Bhishma / Lord Krishna (Mahabharata memory)",
        "location": "Narkatari / Bhishma Kund, Kurukshetra, Haryana",
        "state": "Haryana",
        "glyph": "भी",
        "tags": ["mahabharata-sites"],
        "deityFamilies": ["krishna", "vishnu"],
        "summary": "Bhishma Kund — tirtha marking Bhishma’s arrow-bed and Arjuna’s water gift in Kurukshetra’s Mahabharata circuit.",
        "famousFor": "Bhishma’s sharashayya · arrow-bed water spring",
        "mythology": "Epic memory places the wounded Bhishma on a bed of arrows at Kurukshetra. Tradition holds that Arjuna struck the earth to quench his thirst — remembered at Bhishma Kund. Together with Jyotisar and Brahma Sarovar, it ranks among the most searched Mahabharata pilgrimage stops.",
        "festivals": ["Gita Jayanti", "Ekadashi observances"],
        "lat": 29.965,
        "lng": 76.78,
        "mapQuery": "Bhishma Kund Kurukshetra",
        "nearestRail": "Kurukshetra Junction",
        "nearestAirport": "Chandigarh / Delhi",
        "nearby": [
            {"name": "Jyotisar, Kurukshetra", "slug": "jyotisar-kurukshetra", "note": "Gita site"},
            {"name": "Brahma Sarovar & Jyotisar", "slug": "kurukshetra-brahmasarovar", "note": "Sacred tank circuit"},
        ],
    },
    {
        "slug": "pandaveshwar-hastinapur",
        "name": "Pandaveshwar Temple, Hastinapur",
        "deity": "Lord Shiva (Pandava association) / Kuru capital memory",
        "location": "Hastinapur, Meerut district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "पा",
        "tags": ["mahabharata-sites"],
        "deityFamilies": ["shiva", "krishna"],
        "summary": "Pandaveshwar Temple in Hastinapur — living shrine in the remembered capital of the Kuru dynasty.",
        "famousFor": "Hastinapur capital geography · Pandava shrine",
        "mythology": "Hastinapur is the Mahabharata’s political heart — seat of Dhritarashtra, the Pandavas’ claim, and Draupadi’s trials. Pandaveshwar and nearby Karna / Draupadi-linked spots keep that capital memory alive for pilgrims searching ‘Mahabharata places you can still visit’.",
        "festivals": ["Maha Shivaratri", "Gita Jayanti season"],
        "lat": 29.156,
        "lng": 78.0,
        "mapQuery": "Pandaveshwar Temple Hastinapur",
        "nearestRail": "Meerut / Muzaffarnagar region",
        "nearestAirport": "Delhi",
        "nearby": [
            {"name": "Karna Temple, Hastinapur", "slug": "karna-temple-hastinapur", "note": "Same town"},
        ],
    },
    {
        "slug": "karna-temple-hastinapur",
        "name": "Karna Temple, Hastinapur",
        "deity": "Karna (Mahabharata hero memory)",
        "location": "Hastinapur, Meerut district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "क",
        "tags": ["mahabharata-sites"],
        "deityFamilies": ["krishna"],
        "summary": "Karna Temple at Hastinapur — shrine honouring the tragic dana-vira of the Mahabharata.",
        "famousFor": "Karna devotion · Hastinapur Mahabharata circuit",
        "mythology": "Karna’s life of generosity, loyalty, and tragic revelation is among YouTube’s most searched Mahabharata arcs. Hastinapur’s Karna shrine anchors that emotion in the Kuru capital landscape beside Pandaveshwar.",
        "festivals": ["Karna-related memorial days as locally observed"],
        "lat": 29.16,
        "lng": 78.005,
        "mapQuery": "Karna Temple Hastinapur",
        "nearestRail": "Meerut region",
        "nearestAirport": "Delhi",
        "nearby": [
            {"name": "Pandaveshwar Temple, Hastinapur", "slug": "pandaveshwar-hastinapur", "note": "Same town"},
        ],
    },
    {
        "slug": "barnawa-lakshagriha",
        "name": "Barnawa Lakshagriha site",
        "deity": "Pandava escape memory (Mahabharata)",
        "location": "Barnawa, Baghpat district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "ला",
        "tags": ["mahabharata-sites"],
        "deityFamilies": ["krishna"],
        "summary": "Barnawa — traditional site of the lac palace (Lakshagriha) fire-trap and the Pandavas’ escape tunnel lore.",
        "famousFor": "Lakshagriha · viral ‘Mahabharata places still exist’ stop",
        "mythology": "The Adi Parva’s lac-house plot — Duryodhana’s attempt to burn the Pandavas — is mapped by local tradition onto Barnawa. Tunnel and mound lore make it a favourite internet search among Mahabharata geography lists.",
        "festivals": ["Local memorial visits"],
        "lat": 29.12,
        "lng": 77.38,
        "mapQuery": "Barnawa Lakshagriha Baghpat",
        "nearestRail": "Meerut / Baghpat region",
        "nearestAirport": "Delhi",
        "nearby": [
            {"name": "Pandaveshwar Temple, Hastinapur", "slug": "pandaveshwar-hastinapur", "note": "Kuru capital day trip"},
        ],
    },
    {
        "slug": "govardhan-giriraj",
        "name": "Giriraj Govardhan",
        "deity": "Lord Krishna (Govardhan / Giriraj)",
        "location": "Govardhan, Mathura district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "गो",
        "tags": ["mahabharata-sites"],
        "deityFamilies": ["krishna", "vishnu"],
        "summary": "Govardhan Hill — where Krishna lifted Giriraj; among the world’s most searched Krishna–Mahabharata-era Braj tirthas.",
        "famousFor": "Govardhan Parikrama · Annakut / Giriraj puja",
        "mythology": "Krishna’s lifting of Govardhan to shelter Braj from Indra’s storm is a peak YouTube and festival search theme (Annakut / Govardhan Puja). The hill’s 21-km parikrama and shrines form living Mahabharata-era Krishna geography beside Mathura–Vrindavan.",
        "festivals": ["Govardhan Puja / Annakut", "Janmashtami", "Holika Dahan season"],
        "lat": 27.497,
        "lng": 77.462,
        "mapQuery": "Govardhan Giriraj Temple",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "nearby": [
            {"name": "Krishna Janmabhoomi, Mathura", "slug": "krishna-janmabhoomi-mathura", "note": "Birthplace city"},
            {"name": "Banke Bihari Temple, Vrindavan", "slug": "banke-bihari-vrindavan", "note": "Braj circuit"},
        ],
    },
]


STORIES = [
    {
        "slug": "kaikeyi-dasharatha-boons",
        "title": "Kaikeyi’s two boons — why Rama went to the forest",
        "titleHi": "कैकेयी के दो वर — राम वन क्यों गए",
        "hook": "The most searched Ramayana turning point: a mother’s boons, a father’s word, and fourteen years of exile.",
        "hookHi": "रामायण का सबसे खोजा जाने वाला मोड़: माँ के वर, पिता का वचन, और चौदह वर्ष का वनवास।",
        "storyEn": "On the eve of Rama’s coronation, Manthara stirs Kaikeyi’s fear. Kaikeyi claims two boons Dasharatha once promised: Bharata on the throne, and Rama banished for fourteen years. Bound by dharma to keep his word, the king consents in grief. Rama accepts exile without anger — honouring father over kingdom. Sita and Lakshmana insist on joining him. This single night explains Diwali’s lamps years later: the prince who left so that a promise would not break.",
        "storyHi": "राज्याभिषेक की पूर्वसंध्या पर मंथरा कैकेयी के भय को जगाती है। कैकेयी दशरथ से दो पुराने वर माँगती हैं: भरत का सिंहासन, और राम का चौदह वर्ष वनवास। वचन-पालन के धर्म से बँधे राजा शोक में स्वीकार करते हैं। राम बिना क्रोध वन स्वीकार करते हैं — राज्य से ऊपर पिता का मान। सीता और लक्ष्मण साथ चलने का आग्रह करते हैं। यही रात वर्षों बाद दीपावली के दीपों का अर्थ खोलती है: वह राजकुमार जो वचन न टूटने देने को चला गया।",
        "storyDetailEn": "Dasharatha’s tragic dilemma is the Ramayana’s moral engine. Love for Rama collides with satya — truth as kept vow. Kaikeyi is not a cartoon villain in deeper readings: she is a queen protecting her son’s future under court intrigue. Rama’s calm refusal to cling to power teaches grihastha dharma: duty can cost comfort.\n\nPilgrims who walk Ayodhya, Shringverpur, and Chitrakoot are walking the geography opened by these boons. For home reading, light a lamp remembering that exile began with a promise kept — not with hatred.",
        "storyDetailHi": "दशरथ की करुण दुविधा रामायण का नैतिक इंजन है। राम-प्रेम सत्य-वचन से टकराता है। गहरी पाठ में कैकेयी केवल खलनायिका नहीं — राजसभा षड्यंत्र में पुत्र का भविष्य बचाने वाली रानी हैं। राम का राज्य-मोह त्याग गृहस्थ धर्म सिखाता है: कर्तव्य सुख का मोल ले सकता है।\n\nअयोध्या, श्रृंगवेरपुर, चित्रकूट घूमने वाले इन्हीं वरों से खुली भूगोल पर चलते हैं। घर में दीप जलाकर याद करें — वनवास घृणा से नहीं, वचन रखने से शुरू हुआ।",
        "whyRitual": "Reading this katha before Ram Navami or Diwali frames why Rama’s return is celebrated with lamps.",
        "whyRitualHi": "राम नवमी या दीपावली से पहले यह कथा पढ़ें — राम की वापसी पर दीप क्यों जलते हैं, यही समझ आती है।",
        "takeaway": "Dharma sometimes means leaving the throne so a father’s word stays unbroken.",
        "relatedTemples": ["ayodhya-ram-mandir", "kanak-bhawan-ayodhya", "shringverpur-prayagraj", "chitrakoot-kamadgiri"],
        "relatedFestivals": ["ram-navami", "diwali"],
        "relatedDevotion": ["rama-aarti", "rama-chalisa"],
        "deity": "rama",
        "tags": ["ritual-why", "family", "long-read", "ramayana"],
        "readSeconds": 420,
    },
    {
        "slug": "surpanakha-panchavati",
        "title": "Surpanakha at Panchavati — the insult that led to Lanka",
        "titleHi": "पंचवटी में शूर्पणखा — वह अपमान जिससे लंका-युद्ध जन्मा",
        "hook": "One of YouTube’s favourite Ramayana scenes: desire, refusal, mutilation, and Ravana’s revenge plot.",
        "hookHi": "यूट्यूब की प्रिय रामायण दृश्य-श्रृंखला: चाह, इनकार, अंग-भंग, और रावण का प्रतिशोध।",
        "storyEn": "In Panchavati, Surpanakha — Ravana’s sister — approaches Rama in desire. Refused, she turns on Sita. Lakshmana wounds her nose and ears. Humiliated, she flies to Lanka and paints Sita’s beauty for Ravana. Desire for vengeance becomes abduction strategy. The golden deer, the Lakshmana rekha, and Sita’s capture all grow from this forest confrontation still mapped onto Nashik’s Panchavati.",
        "storyHi": "पंचवटी में रावण की बहन शूर्पणखा कामभाव से राम के पास आती हैं। अस्वीकार पर वे सीता पर झपटती हैं। लक्ष्मण नाक-कान काटते हैं। अपमानित होकर वे लंका जाती हैं और सीता-सौंदर्य रावण को सुनाती हैं। प्रतिशोध हरण-योजना बन जाता है। सोने का मृग, लक्ष्मण-रेखा, सीता-हरण — सब इसी वन-संघर्ष से उगते हैं, जिसे आज नासिक की पंचवटी पर मैप किया जाता है।",
        "storyDetailEn": "The episode teaches boundaries and consequences. Lakshmana’s defence of Sita is protective dharma; Surpanakha’s report weaponises desire into state violence. Modern pilgrims visit Kalaram Temple and Sita Gufa to stand inside that story’s geography.\n\nHome takeaway: small forest choices can open epic wars — speak and act with care around desire and honour.",
        "storyDetailHi": "यह प्रसंग सीमा और परिणाम सिखाता है। लक्ष्मण की सीता-रक्षा रक्षक धर्म है; शूर्पणखा का संदेश काम को राज्य-हिंसा बना देता है। आज श्रद्धालु कालाराम और सीता गुफा में उसी भूगोल में खड़े होते हैं।\n\nघर का पाठ: छोटे वन-निर्णय महायुद्ध खोल सकते हैं — इच्छा और मान के आसपास सावधानी से बोलें-चलें।",
        "whyRitual": "A short Panchavati reading before Nashik travel or Ramayana trail study.",
        "whyRitualHi": "नासिक यात्रा या रामायण-पथ अध्ययन से पहले छोटी पंचवटी कथा।",
        "takeaway": "One wounded pride in the forest became the path to Lanka.",
        "relatedTemples": ["sita-gufa-nashik", "kalaram-temple-nashik"],
        "relatedFestivals": ["ram-navami"],
        "relatedDevotion": ["rama-aarti"],
        "deity": "rama",
        "tags": ["ritual-why", "long-read", "ramayana"],
        "readSeconds": 400,
    },
    {
        "slug": "vali-sugriva-kishkindha",
        "title": "Vali and Sugriva — Rama’s alliance in Kishkindha",
        "titleHi": "वालि और सुग्रीव — किष्किन्धा में राम की मित्रता",
        "hook": "Brother against brother, a disputed kingdom, and Rama’s arrow that sealed the search for Sita.",
        "hookHi": "भाई के विरुद्ध भाई, विवादित राज्य, और राम का वह बाण जिसने सीता-खोज सुनिश्चित की।",
        "storyEn": "Exiled Sugriva meets Rama near Kishkindha. He promises vanara help to find Sita if Rama restores his throne from elder brother Vali. In the duel, Rama’s arrow fells Vali. Sugriva becomes king; Hanuman and the armies begin the great search that leads to Lanka and the Setu. Hampi–Anjanadri geography keeps this chapter alive for today’s pilgrims.",
        "storyHi": "निर्वासित सुग्रीव किष्किन्धा के पास राम से मिलते हैं। सीता खोज में वानर-सहायता का वचन देते हैं यदि राम ज्येष्ठ वालि से सिंहासन दिलवा दें। द्वंद्व में राम का बाण वालि को गिराता है। सुग्रीव राजा बनते हैं; हनुमान और सेनाएँ महान खोज शुरू करती हैं — लंका और सेतु तक। हम्पी–अंजनाद्रि आज भी इस अध्याय को जीवित रखते हैं।",
        "storyDetailEn": "Commentators debate Rama’s method; the epic frames it as restoring a wronged ally to enable dharma’s larger rescue. For home devotion, the lesson is alliance: even divine heroes need faithful friends. Climb Anjanadri remembering Hanuman’s birth lore in the same landscape.",
        "storyDetailHi": "टीकाकार राम की विधि पर विमर्श करते हैं; महाकाव्य इसे अधर्म-पीड़ित मित्र की बहाली और बड़े धर्म-उद्धार के द्वार के रूप में रखता है। घर की भक्ति में पाठ है मित्रता: दिव्य नायक को भी विश्वसनीय साथी चाहिए। अंजनाद्रि चढ़ते हनुमान-जन्म स्मृति याद करें।",
        "whyRitual": "Read before Hampi / Anjanadri visits or Hanuman Jayanti.",
        "whyRitualHi": "हम्पी / अंजनाद्रि यात्रा या हनुमान जयंती से पहले पढ़ें।",
        "takeaway": "Friendship restored a kingdom — and opened the road to Sita.",
        "relatedTemples": ["anjanadri-hampi", "kodandarama-hampi"],
        "relatedFestivals": ["hanuman-jayanti", "ram-navami"],
        "relatedDevotion": ["hanuman-chalisa", "hanuman-aarti"],
        "deity": "rama",
        "tags": ["ritual-why", "long-read", "ramayana"],
        "readSeconds": 400,
    },
    {
        "slug": "ram-setu-nal-neel",
        "title": "Ram Setu — Nala, Neela, and the bridge to Lanka",
        "titleHi": "राम सेतु — नल, नील और लंका का पुल",
        "hook": "The bridge everyone searches: stones that floated, faith that marched, and Dhanushkodi’s sea.",
        "hookHi": "सबके खोज का सेतु: तैरते पत्थर, चलती श्रद्धा, और धनुषकोडि का सागर।",
        "storyEn": "Stopped by the ocean, Rama’s army receives counsel. Vanara engineers Nala and Neela — sons of divine craftsmen in many tellings — lead Setubandha. Stones marked with Rama’s name are said to float. The bridge carries the host toward Lanka. At Rameswaram, Rama worships Shiva; at Dhanushkodi, pilgrims still face the shoals called Adam’s Bridge / Rama Setu.",
        "storyHi": "सागर रोकता है तो राम-सेना को सलाह मिलती है। वानर शिल्पी नल-नील — कई कथनों में दिव्य कारीगरों के पुत्र — सेतुबंध कराते हैं। राम-नाम अंकित पत्थर तैरने की कथा है। सेतु सेना को लंका ले जाता है। रामेश्वरम में राम शिव की आराधना करते हैं; धनुषकोडि पर यात्री आज भी राम सेतु कहे जाने वाले द्वीप-श्रृंखला की ओर देखते हैं।",
        "storyDetailEn": "Whether read as miracle, poetry, or sacred geography, Setubandha is collective seva: countless hands, one purpose. Pair this katha with Ramanathaswamy darshan and a respectful Dhanushkodi visit — verify weather and local rules.",
        "storyDetailHi": "चमत्कार, काव्य या पवित्र भूगोल — सेतुबंध सामूहिक सेवा है: असंख्य हाथ, एक उद्देश्य। इस कथा को रामनाथस्वामी दर्शन और धनुषकोडि की विनम्र यात्रा से जोड़ें — मौसम और स्थानीय नियम जाँचें।",
        "whyRitual": "Home reading before Rameswaram yatra or Setu documentaries.",
        "whyRitualHi": "रामेश्वरम यात्रा या सेतु वृत्तचित्र से पहले घर में पाठ।",
        "takeaway": "Faith built a road across water — together.",
        "relatedTemples": ["rameswaram", "dhanushkodi-rama-setu"],
        "relatedFestivals": ["ram-navami", "diwali"],
        "relatedDevotion": ["rama-aarti", "hanuman-chalisa"],
        "deity": "rama",
        "tags": ["ritual-why", "long-read", "ramayana", "first-timer"],
        "readSeconds": 420,
    },
    {
        "slug": "hanuman-sanjeevani",
        "title": "Hanuman and the Sanjeevani — lifeline of Lakshmana",
        "titleHi": "हनुमान और संजीवनी — लक्ष्मण की जीवन-रेखा",
        "hook": "The mountain-lifting leap every child knows — and every YouTube Ramayana clip retells.",
        "hookHi": "पर्वत उठाकर उड़ान — हर बच्चे की जानी कथा, हर रामायण क्लिप की प्रिय दृश्य।",
        "storyEn": "On the battlefield of Lanka, Lakshmana falls to Indrajit’s weapon. The only cure is Sanjeevani from a distant Himalayan herb mountain. Hanuman flies, cannot identify the plant, and lifts the whole peak. Physicians revive Lakshmana. Devotion becomes medicine; speed becomes seva. This is why Hanuman Chalisa readers still invoke him in family illness and crisis.",
        "storyHi": "लंका-युद्ध में इंद्रजीत के अस्त्र से लक्ष्मण गिरते हैं। उपचार है दूर हिमालय की संजीवनी। हनुमान उड़ते हैं, जड़ी न पहचानकर पूरा पर्वत उठा लाते हैं। वैद्य लक्ष्मण जिलाते हैं। भक्ति औषधि बनती है; गति सेवा। इसलिए हनुमान चालीसा पढ़ने वाले आज भी रोग और संकट में उन्हें पुकारते हैं।",
        "storyDetailEn": "The story pairs courage with care. Hanuman does not argue impossibility; he expands the solution. For home puja, recite a few Chalisa verses after this katha — remembering that seva sometimes means carrying more than you planned.",
        "storyDetailHi": "कथा साहस को देखभाल से जोड़ती है। हनुमान असंभव पर बहस नहीं करते — समाधान बड़ा करते हैं। घर की पूजा में कथा के बाद कुछ चालीसा पद — याद रहे, सेवा कभी-कभी योजना से अधिक उठाने जैसी होती है।",
        "whyRitual": "Read when someone at home is unwell, or on Hanuman Jayanti / Tuesdays.",
        "whyRitualHi": "घर में अस्वस्थता पर, या हनुमान जयंती / मंगलवार को पढ़ें।",
        "takeaway": "When the herb is unclear, bring the whole mountain of effort.",
        "relatedTemples": ["anjanadri-hampi", "hanuman-garhi-ayodhya", "rameswaram"],
        "relatedFestivals": ["hanuman-jayanti"],
        "relatedDevotion": ["hanuman-chalisa", "hanuman-aarti"],
        "deity": "hanuman",
        "tags": ["ritual-why", "family", "long-read", "ramayana"],
        "readSeconds": 400,
    },
    {
        "slug": "sita-enters-earth",
        "title": "Sita returns to Mother Earth — the final farewell",
        "titleHi": "सीता धरती में समाईं — अंतिम विदा",
        "hook": "One of the most emotional Ramayana searches: why Sita chose the earth over another trial.",
        "hookHi": "सबसे भावुक रामायण खोजों में से एक: सीता ने पुनः परीक्षा के स्थान पर धरती क्यों चुनी।",
        "storyEn": "After years in Valmiki’s ashram, Sita’s sons Lava and Kusha sing the Ramayana before Rama. Recognition follows; court and public ask again for proof of purity. Sita calls on Mother Earth, her own origin in many tellings. The ground opens; she returns to Bhudevi — ending the cycle of public trial. The scene remains among the most watched Ramayana moments on television and YouTube.",
        "storyHi": "वाल्मीकि आश्रम के वर्षों बाद लव-कुश राम के समक्ष रामायण गाते हैं। पहचान होती है; सभा पुनः पवित्रता का प्रमाण माँगती है। सीता अपनी उत्पत्ति माता भूमि को पुकारती हैं। धरती खुलती है; वे भूदेवी में लौटती हैं — सार्वजनिक परीक्षा का चक्र समाप्त। यह दृश्य टीवी और यूट्यूब की सबसे देखी रामायण क्षणों में है।",
        "storyDetailEn": "Read with care and humility. Traditions differ on emphasis; the emotional core is dignity after endurance. For home devotion, honour Sita’s strength — not gossip. Light a lamp for women’s silent courage in family life.",
        "storyDetailHi": "विनम्रता से पढ़ें। परंपराओं में बल अलग है; भाव-केंद्र है सहने के बाद गरिमा। घर की भक्ति में सीता के बल का सम्मान — अफवाह का नहीं। परिवार में मौन साहस के लिए दीप जलाएँ।",
        "whyRitual": "A reflective reading on Sita Navami or after Ramayana trail study.",
        "whyRitualHi": "सीता नवमी या रामायण अध्ययन के बाद चिंतन-पाठ।",
        "takeaway": "Sita’s last act chooses dignity over endless proof.",
        "relatedTemples": ["kanak-bhawan-ayodhya", "mithila-janakpur", "sitamarhi-janaki"],
        "relatedFestivals": ["ram-navami"],
        "relatedDevotion": ["rama-aarti"],
        "deity": "rama",
        "tags": ["ritual-why", "family", "long-read", "ramayana"],
        "readSeconds": 420,
    },
    {
        "slug": "sita-second-exile",
        "title": "Why Rama sent pregnant Sita away — dharma of the king",
        "titleHi": "गर्भवती सीता का वनवास — राजा का धर्म",
        "hook": "The hardest Ramayana question online: how could Rama exile Sita after winning her back?",
        "hookHi": "ऑनलाइन रामायण का कठिन प्रश्न: सीता को वापस पाकर राम उन्हें वन कैसे भेज सकते थे?",
        "storyEn": "After crowning, whispers in Ayodhya question Sita’s captivity in Lanka. Rama, torn between husband and king, chooses the harsher public dharma and asks Lakshmana to leave Sita near Valmiki’s ashram — though she is pregnant. She raises Lava and Kusha in the sage’s care. The episode is debated for centuries; TirthaYatra presents it as tradition’s painful teaching on leadership cost, not as a simple verdict.",
        "storyHi": "राज्याभिषेक के बाद अयोध्या में लंका-वास की अफवाहें उठती हैं। पति और राजा के बीच बँटे राम कठिन लोक-धर्म चुनते हैं और लक्ष्मण से गर्भवती सीता को वाल्मीकि आश्रम के पास छोड़ने को कहते हैं। लव-कुश ऋषि-छाया में पलते हैं। सदियों से विवादित प्रसंग; तीर्थयात्रा इसे नेतृत्व की कीमत की करुण शिक्षा के रूप में रखती है — सरल फैसला नहीं।",
        "storyDetailEn": "Many households skip this chapter with children; adults may read it to understand why later Sita–earth and Lava–Kusha episodes exist. Pair with respect for Sita temples at Janakpur and Sitamarhi.",
        "storyDetailHi": "कई घर बच्चों से यह अध्याय छोड़ते हैं; प्रौढ़ इसे लव-कुश और धरती-प्रवेश समझने को पढ़ सकते हैं। जनकपुर और सीतामढ़ी के सीता मंदिरों के सम्मान के साथ जोड़ें।",
        "whyRitual": "Adult reflective reading — not a children’s bedtime tale.",
        "whyRitualHi": "प्रौढ़ चिंतन-पाठ — बच्चों की सोने-कथा नहीं।",
        "takeaway": "Kingship in the epic sometimes breaks the heart that war could not.",
        "relatedTemples": ["ayodhya-ram-mandir", "kanak-bhawan-ayodhya", "lavkush-temple-lucknow", "mithila-janakpur"],
        "relatedFestivals": [],
        "relatedDevotion": ["rama-aarti"],
        "deity": "rama",
        "tags": ["ritual-why", "long-read", "ramayana"],
        "readSeconds": 430,
    },
    {
        "slug": "ravana-vadh-dharma",
        "title": "Ravana’s fall — when dharma defeated ten-headed pride",
        "titleHi": "रावण वध — जब धर्म ने दशानन के अहंकार को हराया",
        "hook": "The climax search: how Rama finally ended the Lanka war.",
        "hookHi": "चरमोत्कर्ष खोज: राम ने लंका-युद्ध का अंत कैसे किया।",
        "storyEn": "After days of war, fallen heroes, and Vibhishana’s counsel, Rama confronts Ravana. Brahmastra and divine weapons end the ten-headed king who abducted Sita and scorned dharma. Vibhishana is crowned. Sita’s agni-pariksha traditions follow in many tellings. Victory returns the path toward Ayodhya — and Diwali’s lamps.",
        "storyHi": "दिनों के युद्ध, वीर-पतन, विभीषण की सलाह के बाद राम रावण से भिड़ते हैं। ब्रह्मास्त्र और दिव्यास्त्र उस दशानन का अंत करते हैं जिसने सीता हरी और धर्म ठुकराया। विभीषण राजा बनते हैं। कई कथनों में सीता की अग्नि-परीक्षा। विजय अयोध्या-पथ और दीपावली के दीप खोलती है।",
        "storyDetailEn": "Ravana is also remembered as a great Shiva devotee — complexity the epic allows. Home lesson: knowledge without restraint becomes tyranny. Celebrate Diwali as return of light after such darkness.",
        "storyDetailHi": "रावण शिव-भक्त भी याद किए जाते हैं — महाकाव्य जटिलता देता है। घर का पाठ: संयमहीन ज्ञान अत्याचार बनता है। दीपावली ऐसे अंधकार के बाद लौटी ज्योति के रूप में मनाएँ।",
        "whyRitual": "Diwali / Dussehra reading with family.",
        "whyRitualHi": "दीपावली / दशहरा पर परिवार संग पाठ।",
        "takeaway": "Pride that steals another’s dignity falls — even if it knows the Vedas.",
        "relatedTemples": ["rameswaram", "dhanushkodi-rama-setu", "ayodhya-ram-mandir"],
        "relatedFestivals": ["dussehra", "diwali"],
        "relatedDevotion": ["rama-aarti", "hanuman-chalisa"],
        "deity": "rama",
        "tags": ["ritual-why", "family", "long-read", "ramayana"],
        "readSeconds": 400,
    },
    {
        "slug": "yaksha-prashna-yudhishthira",
        "title": "Yaksha Prashna — Yudhishthira’s answers at the lake",
        "titleHi": "यक्ष प्रश्न — झील पर युधिष्ठिर के उत्तर",
        "hook": "Mahabharata’s viral wisdom test: what is the greatest wonder?",
        "hookHi": "महाभारत की वायरल ज्ञान-परीक्षा: सबसे बड़ा आश्चर्य क्या है?",
        "storyEn": "In exile, the Pandavas’ brothers fall lifeless at a forbidden lake. A Yaksha demands answers. Yudhishthira alone replies with calm philosophy — including the famous wonder: humans see death everywhere yet live as if immortal. Offered one brother’s life, he chooses Nakula so both mothers keep a son. The Yaksha reveals himself as Dharma; all revive. This Aranya Parva scene floods YouTube shorts and classrooms alike.",
        "storyHi": "वनवास में पाण्डव बंधु निषिद्ध झील पर मृत गिरते हैं। यक्ष प्रश्न माँगता है। अकेले युधिष्ठिर शांत दर्शन से उत्तर देते हैं — प्रसिद्ध आश्चर्य सहित: मनुष्य मृत्यु देखकर भी अमर-सा जीता है। एक भाई का जीवन चुनने पर वे नकुल चुनते हैं ताकि दोनों माताओं का पुत्र बचे। यक्ष धर्म बनकर प्रकट होते हैं; सब जीवित होते हैं। अरण्य पर्व का यह दृश्य शॉर्ट्स और कक्षाओं में छाया रहता है।",
        "storyDetailEn": "Leadership here is fairness under loss. Pair with Kurukshetra visits: the same Yudhishthira later walks the battlefield of harder choices.",
        "storyDetailHi": "यहाँ नेतृत्व हानि में निष्पक्षता है। कुरुक्षेत्र यात्रा से जोड़ें: वही युधिष्ठिर बाद में कठिनतर युद्ध-धर्म चलते हैं।",
        "whyRitual": "Family discussion katha — especially with students.",
        "whyRitualHi": "पारिवारिक चर्चा-कथा — विशेषकर विद्यार्थियों संग।",
        "takeaway": "The greatest wonder is forgetting mortality; the greatest dharma is fairness.",
        "relatedTemples": ["jyotisar-kurukshetra", "kurukshetra-brahmasarovar", "bhishma-kund-kurukshetra"],
        "relatedFestivals": [],
        "relatedDevotion": [],
        "deity": "krishna",
        "tags": ["ritual-why", "family", "long-read", "mahabharata"],
        "readSeconds": 430,
    },
    {
        "slug": "eklavya-drona-thumb",
        "title": "Eklavya and Drona — the guru-dakshina of the thumb",
        "titleHi": "एकलव्य और द्रोण — अँगूठे की गुरु-दक्षिणा",
        "hook": "One of the most searched Mahabharata injustices: talent, exclusion, and a terrible fee.",
        "hookHi": "सबसे खोजी महाभारत अन्यायों में: प्रतिभा, बहिष्कार, और कठोर दक्षिणा।",
        "storyEn": "Eklavya, a forest prince, learns archery by making a clay image of Drona when refused formal entry. His skill surpasses the princes. Drona, protecting Arjuna’s primacy, asks Eklavya’s right thumb as guru-dakshina. Eklavya obeys. The story burns in modern debate on merit and gatekeeping — yet remains a core Mahabharata teaching on sacrifice, power, and cost.",
        "storyHi": "वनराज एकलव्य औपचारिक प्रवेश न मिलने पर द्रोण की मिट्टी-मूर्ति बनाकर धनुर्विद्या सीखते हैं। कौशल राजकुमारों से बढ़ जाता है। अर्जुन की प्रधानता बचाने को द्रोण गुरु-दक्षिणा में दायाँ अँगूठा माँगते हैं। एकलव्य देते हैं। आधुनिक बहस में योग्यता और द्वार-रक्षक व्यवस्था जलती है — फिर भी यह बलिदान, शक्ति और कीमत की केंद्रीय महाभारत शिक्षा है।",
        "storyDetailEn": "Read without simplifying into only villain/victim. The epic shows systems that wound even while producing heroes. Home reflection: honour teachers, but question cruelty done in a tradition’s name.",
        "storyDetailHi": "केवल खल/पीड़ित सरल न करें। महाकाव्य दिखाता है कि व्यवस्था नायक बनाते हुए भी घायल कर सकती है। घर का चिंतन: गुरु सम्मान, परंपरा के नाम पर क्रूरता पर प्रश्न।",
        "whyRitual": "Student-season or teacher-day reflective reading.",
        "whyRitualHi": "विद्यार्थी-काल या गुरु अवसर पर चिंतन-पाठ।",
        "takeaway": "Obedience without justice still leaves a scar the epic refuses to hide.",
        "relatedTemples": ["jyotisar-kurukshetra", "pandaveshwar-hastinapur"],
        "relatedFestivals": [],
        "relatedDevotion": [],
        "deity": "krishna",
        "tags": ["ritual-why", "long-read", "mahabharata"],
        "readSeconds": 420,
    },
    {
        "slug": "karna-danveer",
        "title": "Karna the giver — armour, earrings, and unbroken dana",
        "titleHi": "दानवीर कर्ण — कवच-कुण्डल और अटूट दान",
        "hook": "Why Karna trends forever: generosity that even gods tested.",
        "hookHi": "कर्ण क्यों सदा ट्रेंड करते हैं: वह दान जिसकी परीक्षा देव भी लेते हैं।",
        "storyEn": "Born of Kunti and Surya, raised by a charioteer, Karna becomes Duryodhana’s loyal friend and the war’s tragic pillar. Indra, disguised, begs his divine armour and earrings; Karna cuts them off as dana. Later he learns he is the Pandavas’ elder — yet keeps his word to Anga’s friend. Death finds him with chariot wheel stuck and curses heavy. Hastinapur still keeps a temple in his name.",
        "storyHi": "कुंती और सूर्य से जन्मे, सूत-पुत्र पालित कर्ण दुर्योधन के मित्र और युद्ध के करुण स्तंभ बनते हैं। इंद्र वेष में दिव्य कवच-कुण्डल माँगते हैं; कर्ण दान में काट देते हैं। बाद में पाण्डवों के ज्येष्ठ जानकर भी अंग-मित्र से वचन निभाते हैं। रथ-चक्र फँसा, शाप भारी — मृत्यु आती है। हस्तिनापुर आज भी उनके नाम का मंदिर रखता है।",
        "storyDetailEn": "Karna’s dana is not soft charity; it is identity. Pair with Kunti–Karna recognition stories already on TirthaYatra. Light a lamp for those who give while the world misnames them.",
        "storyDetailHi": "कर्ण का दान कोमल भीख नहीं — पहचान है। तीर्थयात्रा की कुंती–कर्ण कथा से जोड़ें। जिन्हें संसार गलत नाम देकर भी जो देते हैं, उनके लिए दीप।",
        "whyRitual": "Read on memorial days or when teaching generosity to children.",
        "whyRitualHi": "स्मृति दिवस या बच्चों को दान सिखाने पर पढ़ें।",
        "takeaway": "True giving continues even when the asker is destiny in disguise.",
        "relatedTemples": ["karna-temple-hastinapur", "pandaveshwar-hastinapur", "jyotisar-kurukshetra"],
        "relatedFestivals": [],
        "relatedDevotion": [],
        "deity": "krishna",
        "tags": ["ritual-why", "family", "long-read", "mahabharata"],
        "readSeconds": 420,
    },
    {
        "slug": "barbarik-khatu-shyam",
        "title": "Barbarik becomes Khatu Shyam — the head that watched the war",
        "titleHi": "बार्बरीक से खाटू श्याम — युद्ध देखने वाला मस्तक",
        "hook": "Rajasthan’s mega-search: how a grandson of Bhima became Shyam Baba of Khatu.",
        "hookHi": "राजस्थान की विशाल खोज: भीम के पौत्र कैसे खाटू के श्याम बाबा बने।",
        "storyEn": "Folk and Skanda Purana tradition tell of Barbarik — immensely powerful, sworn to aid the weaker side. Krishna tests him and asks for his head as charity before Kurukshetra, so the war’s balance holds. The severed head watches the battle from a hill. Later worshipped as Khatu Shyam, ‘Haare ka Sahara,’ he draws crores of seekers. Note: this cycle is popular devotion layered on Mahabharata memory, not Vyasa’s core critical text.",
        "storyHi": "लोक और स्कंद पुराण परंपरा में बार्बरीक — अमित शक्ति, दुर्बल पक्ष की सहायता का प्रण। कृष्ण परीक्षा लेते हैं और कुरुक्षेत्र से पहले मस्तक दान माँगते हैं ताकि युद्ध-संतुलन रहे। कटा सिर पहाड़ी से युद्ध देखता है। बाद में खाटू श्याम, ‘हारे का सहारा’ बनकर करोड़ों को खींचते हैं। नोट: यह लोक-भक्ति महाभारत-स्मृति पर परत है — व्यास की मूल आलोचनात्मक पाठ नहीं।",
        "storyDetailEn": "Visit Khatu with clear eyes: miracle stories vary. The ethical spark is surrender of ego-power for a larger dharma frame. Tuesday/Sunday crowds are intense — plan darshan patiently.",
        "storyDetailHi": "खाटू स्पष्ट दृष्टि से जाएँ: चमत्कार-कथाएँ बदलती हैं। नैतिक ज्योति है अहं-शक्ति का बड़े धर्म हेतु समर्पण। मंगल/रविवार भीड़ तीव्र — दर्शन धैर्य से योजना करें।",
        "whyRitual": "Before Khatu yatra or Shyam aarti at home.",
        "whyRitualHi": "खाटू यात्रा या घर में श्याम आरती से पहले।",
        "takeaway": "Even unmatched strength may be asked to watch — not to win alone.",
        "relatedTemples": ["khatushyam", "jyotisar-kurukshetra", "bhishma-kund-kurukshetra"],
        "relatedFestivals": [],
        "relatedDevotion": [],
        "deity": "krishna",
        "tags": ["ritual-why", "first-timer", "long-read", "mahabharata"],
        "readSeconds": 430,
    },
    {
        "slug": "lakshagriha-pandava-escape",
        "title": "Lakshagriha — the lac palace and the Pandavas’ escape",
        "titleHi": "लाक्षागृह — लाख का महल और पाण्डवों की सुरंग",
        "hook": "A top ‘Mahabharata places still exist’ story: fire trap, tunnel, and Barnawa’s mounds.",
        "hookHi": "‘महाभारत स्थल आज भी’ की शीर्ष कथा: अग्नि-जाल, सुरंग, और बरनवा के टीले।",
        "storyEn": "Duryodhana plots to burn the Pandavas in a lacquered palace. Warned by Vidura, they dig a tunnel and escape as flames rise — with a Nishada family tragedy entangled in many tellings. Local memory places this Lakshagriha at Barnawa near Baghpat. The escape sends the brothers toward Varanavata exile arcs and eventually Draupadi’s swayamvara.",
        "storyHi": "दुर्योधन पाण्डवों को लाख के महल में जलाने की योजना बनाता है। विदुर की चेतावनी पर वे सुरंग खोदकर आग में से निकलते हैं — कई कथनों में निषाद परिवार की करुण उलझन संग। लोकस्मृति लाक्षागृह को बागपत के बरनवा पर रखती है। यह पलायन वारणावत वन-कथाओं और द्रौपदी स्वयंवर तक ले जाता है।",
        "storyDetailEn": "Archaeology and faith differ; pilgrimage treats Barnawa as memory-landscape. Read as vigilance: trust advice that saves life even when royalty smiles.",
        "storyDetailHi": "पुरातत्त्व और श्रद्धा भिन्न हो सकते हैं; तीर्थ बरनवा को स्मृति-भूगोल मानता है। पाठ है सावधानी: जीवन बचाने वाली सलाह पर विश्वास — जब राजमुस्कान हो तब भी।",
        "whyRitual": "Before visiting Hastinapur–Barnawa Mahabharata circuit.",
        "whyRitualHi": "हस्तिनापुर–बरनवा महाभारत सर्किट से पहले।",
        "takeaway": "Not every palace built for you is safe — listen for Vidura’s whisper.",
        "relatedTemples": ["barnawa-lakshagriha", "pandaveshwar-hastinapur", "karna-temple-hastinapur"],
        "relatedFestivals": [],
        "relatedDevotion": [],
        "deity": "krishna",
        "tags": ["ritual-why", "long-read", "mahabharata", "first-timer"],
        "readSeconds": 400,
    },
    {
        "slug": "draupadi-swayamvar",
        "title": "Draupadi’s swayamvara — the bow that chose Arjuna",
        "titleHi": "द्रौपदी स्वयंवर — वह धनुष जिसने अर्जुन को चुना",
        "hook": "Matsya-yantra, a disguised hero, and the marriage that reshaped the Mahabharata.",
        "hookHi": "मत्स्य-यंत्र, वेषधारी वीर, और वह विवाह जिसने महाभारत बदल दी।",
        "storyEn": "King Drupada sets a fish-eye archery test for Draupadi’s hand. Princes fail. Arjuna, disguised as a Brahmin after Lakshagriha exile, strikes the target. Draupadi garlands him. Later Kunti’s words and divine design lead to the five-husband marriage central to the epic. Popular tellings also debate Karna’s role at the contest — versions differ.",
        "storyHi": "द्रुपद मछली-आँख धनुष-परीक्षा रखते हैं। राजकुमार असफल। लाक्षागृह के बाद ब्राह्मण वेष में अर्जुन लक्ष्य बेधते हैं। द्रौपदी वरमाला डालती हैं। कुंती के वचन और दिव्य विधान से पंच-पति विवाह महाकाव्य का केंद्र बनता है। लोककथा में कर्ण की भूमिका विवादित — पाठभेद हैं।",
        "storyDetailEn": "For home reading, focus on skill under disguise and the weight of spoken words (Kunti’s instruction). Avoid caste-insult simplifications; cite that critical editions vary.",
        "storyDetailHi": "घर के पाठ में वेष में कौशल और बोले वचन का भार (कुंती) रखें। जाति-अपमान सरलता से बचें; आलोचनात्मक संस्करण भिन्न हैं — यह बताएँ।",
        "whyRitual": "Festival of Draupadi / family epic reading nights.",
        "whyRitualHi": "द्रौपदी उत्सव / परिवार महाकाव्य पाठ की रात।",
        "takeaway": "A single arrow can rewrite alliances — and a mother’s sentence can bind five lives.",
        "relatedTemples": ["pandaveshwar-hastinapur", "jyotisar-kurukshetra"],
        "relatedFestivals": [],
        "relatedDevotion": [],
        "deity": "krishna",
        "tags": ["ritual-why", "family", "long-read", "mahabharata"],
        "readSeconds": 410,
    },
    {
        "slug": "gandhari-blindfold",
        "title": "Gandhari’s blindfold — sharing a husband’s dark world",
        "titleHi": "गांधारी की पट्टी — पति के अंधे संसार का साथ",
        "hook": "Why Gandhari covered her eyes — a top character search beyond the battlefield.",
        "hookHi": "गांधारी ने आँखें क्यों बाँधीं — युद्ध से परे चरित्र खोज।",
        "storyEn": "Gandhari of Gandhara marries blind Dhritarashtra. In a radical act of companionship, she blindfolds herself for life — choosing not to see what her husband cannot. She mothers the Kauravas, warns Duryodhana, and later curses Krishna after the war’s slaughter. Her blindfold is love, protest, and tragedy woven together.",
        "storyHi": "गांधार की गांधारी अंधे धृतराष्ट्र से ब्याहती हैं। सहचर्य के कठोर कर्म में वे जीवन भर आँखें बाँध लेती हैं — जो पति नहीं देखता, वे भी न देखें। कौरवों की माता, दुर्योधन को चेतावनी, युद्ध-संहार के बाद कृष्ण को शाप। उनकी पट्टी प्रेम, विरोध और त्रासदी एक साथ है।",
        "storyDetailEn": "A home conversation starter on empathy and agency. Pair with Hastinapur visits — capital of the household this choice shaped.",
        "storyDetailHi": "सहानुभूति और स्वायत्तता पर घर की बातचीत। हस्तिनापुर यात्रा से जोड़ें — उसी गृहस्थी की राजधानी।",
        "whyRitual": "Women’s discussion circles / Mahabharata character study.",
        "whyRitualHi": "महिला चर्चा मंडल / महाभारत चरित्र अध्ययन।",
        "takeaway": "Some vows illuminate; some darken a generation — Gandhari’s did both.",
        "relatedTemples": ["pandaveshwar-hastinapur", "jyotisar-kurukshetra"],
        "relatedFestivals": [],
        "relatedDevotion": [],
        "deity": "krishna",
        "tags": ["ritual-why", "family", "long-read", "mahabharata"],
        "readSeconds": 390,
    },
]


def upsert_index(index: list, meta: dict) -> None:
    for i, row in enumerate(index):
        if row["slug"] == meta["slug"]:
            index[i] = meta
            return
    index.append(meta)


def index_meta(seed: dict) -> dict:
    return {
        "slug": seed["slug"],
        "name": seed["name"],
        "deity": seed["deity"],
        "location": seed["location"],
        "state": seed["state"],
        "country": "India",
        "tier": seed.get("tier", "famous"),
        "glyph": seed.get("glyph", seed["name"][:1]),
        "tags": list(seed.get("tags") or []),
        "tagLabels": [LABELS[t] for t in (seed.get("tags") or []) if t in LABELS],
        "deityFamilies": list(seed.get("deityFamilies") or []),
        "summary": seed["summary"],
        "famousFor": seed["famousFor"],
    }


def tag_existing(slug: str, tag: str, index: list) -> None:
    path = TEMPLES_DIR / f"{slug}.json"
    if not path.exists():
        return
    detail = load_json(path)
    tags = list(detail.get("tags") or [])
    if tag not in tags:
        tags.append(tag)
    detail["tags"] = tags
    detail["tagLabels"] = [LABELS[t] for t in tags if t in LABELS] + [
        x for x in (detail.get("tagLabels") or []) if x not in LABELS.values()
    ]
    # rebuild labels cleanly
    from sync_groups import LABELS as ALL_LABELS  # type: ignore

    detail["tagLabels"] = [ALL_LABELS[t] for t in tags if t in ALL_LABELS]
    dump_json(path, detail)
    for row in index:
        if row["slug"] == slug:
            row["tags"] = tags
            row["tagLabels"] = detail["tagLabels"]
            break


def main() -> None:
    index = load_json(DATA / "temples.json")
    existing = {t["slug"] for t in index}

    added_t = []
    for seed in TEMPLES:
        meta = index_meta(seed)
        detail = enrich(seed)
        dump_json(TEMPLES_DIR / f"{seed['slug']}.json", detail)
        upsert_index(index, meta)
        if seed["slug"] not in existing:
            added_t.append(seed["slug"])
        existing.add(seed["slug"])

    # Strengthen circuit tags on key existing hubs
    for slug, tag in [
        ("kalaram-temple-nashik", "ramayana-trail"),
        ("chitrakoot-ramghat", "ramayana-trail"),
        ("jyotisar-kurukshetra", "mahabharata-sites"),
        ("bhadrakali-kurukshetra", "mahabharata-sites"),
        ("khatushyam", "mahabharata-sites"),
        ("rameswaram", "ramayana-trail"),
        ("lepakshi-veerabhadra", "ramayana-trail"),
    ]:
        tag_existing(slug, tag, index)

    dump_json(DATA / "temples.json", index)

    stories_doc = load_json(DATA / "stories.json")
    by_slug = {s["slug"]: s for s in stories_doc["stories"]}
    added_s = []
    for story in STORIES:
        if story["slug"] in by_slug:
            # update in place
            for i, s in enumerate(stories_doc["stories"]):
                if s["slug"] == story["slug"]:
                    stories_doc["stories"][i] = story
                    break
        else:
            stories_doc["stories"].append(story)
            added_s.append(story["slug"])
    dump_json(DATA / "stories.json", stories_doc)

    print(f"Temples written: {len(TEMPLES)} (new: {len(added_t)})")
    print(f"Stories written: {len(STORIES)} (new: {len(added_s)})")
    if added_t:
        print("New temples:", ", ".join(added_t))
    if added_s:
        print("New stories:", ", ".join(added_s))

    subprocess.check_call([sys.executable, str(ROOT / "build.py")], cwd=ROOT)


if __name__ == "__main__":
    main()
