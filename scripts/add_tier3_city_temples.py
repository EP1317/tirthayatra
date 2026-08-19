#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add Tier-3 city temples, sthala stories, and deity-family wiring for TirthaYatra."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))
from sync_groups import base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")

TARGET_PER_CITY = 3


def T(**kw):
    return kw


# city_key → location matchers (lowercase substrings in location+name)
CITY_CONFIG: dict[str, dict] = {
    "Agra": {"terms": ["agra, uttar pradesh", ", agra,", "agra, up", "agra fort"], "exclude": ["prayagraj", "allahabad"]},
    "Ajmer": {"terms": ["ajmer"], "exclude": ["pushkar"]},
    "Aligarh": {"terms": ["aligarh"]},
    "Alwar": {"terms": ["alwar"]},
    "Bareilly": {"terms": ["bareilly"]},
    "Belagavi": {"terms": ["belgaum", "belagavi"]},
    "Bellary": {"terms": ["bellary", "ballari", "sandur"]},
    "Bhavnagar": {"terms": ["bhavnagar"]},
    "Bhuj": {"terms": ["bhuj"]},
    "Bidar": {"terms": ["bidar"]},
    "Bijapur": {"terms": ["bijapur", "vijayapura"]},
    "Bikaner": {"terms": ["bikaner", "deshnok"]},
    "Bhubaneswar": {"terms": ["bhubaneswar", "bhubaneshwar"]},
    "Chandigarh": {"terms": ["chandigarh", "panchkula", "mohali"]},
    "Cuttack": {"terms": ["cuttack", "dhabaleswar"]},
    "Darbhanga": {"terms": ["darbhanga"]},
    "Davangere": {"terms": ["davangere"]},
    "Eluru": {"terms": ["eluru"]},
    "Faridabad": {"terms": ["faridabad"]},
    "Gulbarga": {"terms": ["gulbarga", "kalaburagi"]},
    "Hassan": {"terms": ["hassan", "belur", "halebidu", "halebid"]},
    "Hisar": {"terms": ["hisar", "agroha", "banbhori"]},
    "Imphal": {"terms": ["imphal"]},
    "Jaipur": {"terms": ["jaipur"]},
    "Jamnagar": {"terms": ["jamnagar"]},
    "Jamshedpur": {"terms": ["jamshedpur"]},
    "Jhansi": {"terms": ["jhansi"]},
    "Junagadh": {"terms": ["junagadh", "girnar"]},
    "Kadapa": {"terms": ["kadapa", "cuddapah"]},
    "Kakinada": {"terms": ["kakinada", "pithapuram", "annavaram"]},
    "Kanchipuram": {"terms": ["kanchipuram", "kanchi"]},
    "Kochi": {"terms": ["kochi", "ernakulam", "chottanikkara", "thrikkakara"]},
    "Kollam": {"terms": ["kollam", "quilon"]},
    "Meerut": {"terms": ["meerut"]},
    "Muzaffarpur": {"terms": ["muzaffarpur"]},
    "Nagercoil": {"terms": ["nagercoil", "suchindram", "kanyakumari district"]},
    "Nellore": {"terms": ["nellore"]},
    "Palakkad": {"terms": ["palakkad", "kalpathy"]},
    "Panipat": {"terms": ["panipat"]},
    "Patiala": {"terms": ["patiala"]},
    "Puducherry": {"terms": ["puducherry", "pondicherry", "pondy"]},
    "Rajkot": {"terms": ["rajkot"]},
    "Sambalpur": {"terms": ["sambalpur"]},
    "Sangli": {"terms": ["sangli", "narsobawadi", "audumbar"]},
    "Satara": {"terms": ["satara", "chaphal", "ajinkyatara"]},
    "Shillong": {"terms": ["shillong", "meghalaya"]},
    "Shimla": {"terms": ["shimla", "hatkoti", "jakhoo", "tara devi"]},
    "Solapur": {"terms": ["solapur"]},
    "Thanjavur": {"terms": ["thanjavur", "tanjore"]},
    "Thrissur": {"terms": ["thrissur", "trichur", "guruvayur"]},
    "Trichy": {"terms": ["trichy", "tiruchirappalli", "srirangam", "thiruvanaikaval", "samayapuram", "rockfort"]},
    "Tiruppur": {"terms": ["tiruppur", "tirupur"]},
    "Tiruvannamalai": {"terms": ["tiruvannamalai", "arunachaleswarar"]},
    "Udupi": {"terms": ["udupi", "kollur"]},
    "Vellore": {"terms": ["vellore", "sripuram", "virinjipuram"]},
    "Ayodhya": {"terms": ["ayodhya", "faizabad"]},
}

FAMILY_OVERRIDES: dict[str, list[str]] = {
    "siddheshwar-solapur": ["shiva"],
    "alakhnath-bareilly": ["shiva"],
    "jalakandeswarar-vellore": ["shiva"],
    "sripuram-golden-temple": ["lakshmi", "vishnu"],
    "hasanamba-hassan": ["devi"],
    "chottanikkara-devi-kochi": ["devi"],
    "samaleswari-sambalpur": ["devi"],
    "narasimha-jharni-bidar": ["narasimha", "vishnu"],
    "takhteshwar-bhavnagar": ["shiva"],
    "brihadeeswarar-thanjavur": ["shiva"],
    "lingaraj-bhubaneswar": ["shiva"],
    "vadakkumnathan-thrissur": ["shiva"],
    "rockfort-uchhi-pillayar-trichy": ["ganesha", "murugan"],
    "augharnath-meerut": ["devi", "shiva"],
    "bala-hanuman-jamnagar": ["hanuman"],
    "mankameshwar-agra": ["shiva"],
    "ranganathaswamy-nellore": ["vishnu"],
    "ernakulathappan-kochi": ["shiva"],
    "thrikkakara-vamana-kochi": ["vishnu"],
    "nagaraja-nagercoil": ["devi", "vishnu"],
    "suchindram-temple": ["shiva", "vishnu", "devi"],
    "thanumalayan-suchindram": ["shiva", "vishnu"],
    "sharana-basaveshwara-gulbarga": ["shiva"],
    "kalpathy-viswanathaswamy": ["shiva"],
    "anandavalleeswaram-kollam": ["devi"],
    "devuni-kadapa-venkateswara": ["venkateswara", "vishnu"],
    "sukreeswarar-tiruppur": ["shiva"],
    "ajinkyatara-satara": ["devi"],
    "damodar-kund-junagadh": ["krishna", "vishnu"],
    "bhavnath-mahadev-junagadh": ["shiva"],
    "kapileshwar-belgaum": ["shiva"],
    "khodiyar-mandir-bhavnagar": ["devi"],
    "laxminath-bikaner": ["vishnu", "lakshmi"],
    "shiv-bari-bikaner": ["shiva"],
    "iskcon-chandigarh": ["krishna", "vishnu"],
    "mukteshwar-bhubaneswar": ["shiva"],
    "varadaraja-kanchipuram": ["vishnu"],
    "anantheshwara-udupi": ["shiva"],
    "chandramouleshwara-udupi": ["shiva"],
    "samayapuram-mariamman-trichy": ["devi"],
    "paramekkavu-bhagavathy-thrissur": ["devi"],
    "thiruvambady-krishna-thrissur": ["krishna", "vishnu"],
    "bangaru-kamakshi-thanjavur": ["devi"],
    "hanuman-garhi-ayodhya": ["hanuman", "rama"],
    "kali-bari-shimla": ["devi", "kali"],
    "tara-devi-shimla": ["devi"],
    "birla-mandir-jaipur": ["vishnu", "lakshmi"],
    "dhabaleswar-cuttack": ["shiva"],
    "bajrangbali-ajmer": ["hanuman"],
    "teerthdham-mangalayatan-aligarh": ["shiva", "vishnu"],
}

NEW_STORY_SLUGS = [
    "alakhnath-bareilly",
    "siddheshwar-solapur",
    "jalakandeswarar-vellore",
    "sripuram-golden-temple",
    "hasanamba-hassan",
    "chottanikkara-devi",
    "samaleswari-sambalpur",
    "narasimha-jharni-bidar",
    "cuttack-chandi",
    "takhteshwar-bhavnagar",
    "rockfort-uchhi-pillayar",
    "augharnath-meerut",
    "bala-hanuman-jamnagar",
    "vadakkumnathan-thrissur",
]

NEW_TEMPLES: list[dict] = [
    # —— Bareilly ——
    T(city="Bareilly", slug="alakhnath-bareilly", name="Alakhnath Temple, Bareilly", deity="Lord Shiva (Alakhnath)", location="Alakhnath, Bareilly, Uttar Pradesh", state="Uttar Pradesh", glyph="अ", tier="famous", famousFor="Nath panth seat · Bareilly’s premier Shiva search", summary="Alakhnath — historic Nath math Shiva temple anchoring Bareilly’s Shaiva map.", mythology="The Nath tradition’s Alakhnath math made Bareilly a yogi–Shaiva centre; Shivaratri and Monday abhishekam draw Purvanchal pilgrims.", lat=28.350, lng=79.420, mapQuery="Alakhnath Temple Bareilly", nearestRail="Bareilly Junction", nearestAirport="Bareilly / Lucknow", deityFamilies=["shiva"], festivals=["Maha Shivaratri", "Shravan Mondays"]),
    T(city="Bareilly", slug="trivati-nath-bareilly", name="Trivati Nath Temple, Bareilly", deity="Lord Shiva (Trivati Nath)", location="Bareilly, Uttar Pradesh", state="Uttar Pradesh", glyph="त्र", tier="regional", famousFor="City-centre Shiva · Bareilly local yatra", summary="Trivati Nath — active urban Shiva shrine of Bareilly old city.", mythology="Three-nath memory in the name ties local Shaiva devotion to Bareilly’s merchant lanes; Pradosham evenings see steady queues.", lat=28.367, lng=79.410, mapQuery="Trivati Nath Temple Bareilly", nearestRail="Bareilly Junction", nearestAirport="Bareilly", deityFamilies=["shiva"]),
    T(city="Bareilly", slug="doodheshwar-nath-bareilly", name="Doodheshwar Nath Temple, Bareilly", deity="Lord Shiva (Doodheshwar Nath)", location="Bareilly, Uttar Pradesh", state="Uttar Pradesh", glyph="दू", tier="regional", famousFor="Milk-abhishek Shiva · Bareilly Monday search", summary="Doodheshwar Nath — Shiva temple famed for milk offerings in Bareilly.", mythology="‘Doodh’ abhishek tradition marks this linga; families vow here before weddings and new shops in Rohilkhand.", lat=28.355, lng=79.405, mapQuery="Doodheshwar Nath Temple Bareilly", nearestRail="Bareilly Junction", nearestAirport="Bareilly", deityFamilies=["shiva"]),
    # —— Solapur ——
    T(city="Solapur", slug="siddheshwar-solapur", name="Siddheshwar Temple, Solapur", deity="Lord Shiva (Siddheshwar)", location="Solapur, Maharashtra", state="Maharashtra", glyph="सि", tier="famous", famousFor="Solapur’s essential Shiva · high Maharashtra search", summary="Siddheshwar — the Shiva temple that defines Solapur’s sacred geography.", mythology="Built around a swayambhu linga on the Siddheshwar tank; Makar Sankranti fair and Shivaratri transform the city into a pilgrimage camp.", lat=17.659, lng=75.906, mapQuery="Siddheshwar Temple Solapur", nearestRail="Solapur Junction", nearestAirport="Solapur / Pune", deityFamilies=["shiva"], festivals=["Makar Sankranti", "Maha Shivaratri"]),
    T(city="Solapur", slug="vitthal-rukmini-solapur", name="Vitthal–Rukmini Temple, Solapur", deity="Vitthal & Rukmini (Varkari)", location="Solapur, Maharashtra", state="Maharashtra", glyph="वि", tier="regional", famousFor="Solapur Varkari Vitthal · Ashadhi Ekadashi search", summary="Vitthal–Rukmini Mandir — Varkari bhakti seat in Solapur’s temple quarter.", mythology="Standing Krishna with hands on hips in Pandharpur style; wari-season processions link Solapur to Maharashtra’s Vitthal culture.", lat=17.665, lng=75.910, mapQuery="Vitthal Rukmini Temple Solapur", nearestRail="Solapur Junction", nearestAirport="Solapur", deityFamilies=["vitthal", "krishna"]),
    T(city="Solapur", slug="akkalkot-swami-solapur", name="Shri Swami Samarth Temple, Akkalkot", deity="Swami Samarth (Dattatreya tradition)", location="Akkalkot, Solapur district, Maharashtra", state="Maharashtra", glyph="अक", tier="famous", famousFor="Akkalkot peetham · Solapur district mega-search", summary="Akkalkot — samadhi shrine of Swami Samarth, major Dattatreya-line pilgrimage near Solapur.", mythology="Swami Samarth’s grace lore draws lakhs on Thursdays; the math’s annadanam and paduka darshan anchor Solapur district bhakti.", lat=17.520, lng=76.200, mapQuery="Swami Samarth Temple Akkalkot", nearestRail="Solapur / Akkalkot Road", nearestAirport="Solapur", deityFamilies=["dattatreya"]),
    # —— Vellore ——
    T(city="Vellore", slug="jalakandeswarar-vellore", name="Jalakandeswarar Temple, Vellore Fort", deity="Lord Shiva (Jalakandeswarar)", location="Vellore Fort, Vellore, Tamil Nadu", state="Tamil Nadu", glyph="ज", tier="famous", famousFor="Fort Shiva · Vellore heritage search", summary="Jalakandeswarar — Vijayanagara-era Shiva temple inside Vellore Fort.", mythology="Jalakanta (water-eyed) Shiva sits in a mandapa with ornate pillars; the fort moat setting makes this among Tamil Nadu’s most photographed Shaiva seats.", lat=12.920, lng=79.130, mapQuery="Jalakandeswarar Temple Vellore", nearestRail="Vellore Cantonment", nearestAirport="Chennai / Bengaluru", deityFamilies=["shiva"]),
    T(city="Vellore", slug="sripuram-golden-temple", name="Sri Lakshmi Narayani Golden Temple, Sripuram", deity="Goddess Lakshmi Narayani", location="Sripuram, Vellore, Tamil Nadu", state="Tamil Nadu", glyph="श्री", tier="famous", famousFor="Gold-coated Narayani · modern pilgrimage search", summary="Sripuram Golden Temple — Lakshmi Narayani in a star-shaped gold-covered path complex.", mythology="Devotees walk the star path reading wisdom inscriptions before darshan; the Narayani seva and annadanam define modern Vellore pilgrimage.", lat=12.870, lng=79.090, mapQuery="Sripuram Golden Temple Vellore", nearestRail="Katpadi / Vellore", nearestAirport="Chennai", deityFamilies=["lakshmi", "devi"], tags_extra=["modern-temples"]),
    T(city="Vellore", slug="virinjipuram-arunachaleswarar", name="Arunachaleswarar Temple, Virinjipuram", deity="Lord Shiva (Arunachaleswarar)", location="Virinjipuram, Vellore, Tamil Nadu", state="Tamil Nadu", glyph="वि", tier="regional", famousFor="Palar-river Shiva · Vellore local yatra", summary="Virinjipuram Arunachaleswarar — Chola-era Shiva on the Palar near Vellore.", mythology="Smaller cousin to Tiruvannamalai’s Arunachala memory; Pradosham and Shivaratri draw Vellore families on short tirtha loops.", lat=12.950, lng=79.180, mapQuery="Virinjipuram Arunachaleswarar Temple", nearestRail="Vellore", nearestAirport="Chennai", deityFamilies=["shiva"]),
    # —— Bhavnagar ——
    T(city="Bhavnagar", slug="takhteshwar-bhavnagar", name="Takhteshwar Mahadev Temple, Bhavnagar", deity="Lord Shiva (Takhteshwar Mahadev)", location="Takhteshwar Hill, Bhavnagar, Gujarat", state="Gujarat", glyph="त", tier="famous", famousFor="Hilltop Shiva · Bhavnagar city landmark search", summary="Takhteshwar Mahadev — white marble Shiva on a hill overlooking Bhavnagar and the Gulf of Khambhat.", mythology="Built by Maharaja Takhtsinhji; the climb and Gulf breeze make this the city’s signature Shaiva darshan.", lat=21.770, lng=72.150, mapQuery="Takhteshwar Temple Bhavnagar", nearestRail="Bhavnagar Terminus", nearestAirport="Bhavnagar", deityFamilies=["shiva"]),
    T(city="Bhavnagar", slug="khodiyar-mandir-bhavnagar", name="Khodiyar Mata Temple, Bhavnagar", deity="Goddess Khodiyar Mata", location="Bhavnagar, Gujarat", state="Gujarat", glyph="ख", tier="famous", famousFor="Khodiyar kuldevi · Saurashtra Devi search", summary="Khodiyar Mata — major kuldevi shrine for Rajput and Patel communities of Saurashtra.", mythology="Khodiyar’s crocodile-vahana lore is beloved in Gujarat; Navaratri and newborn naming vows pack the temple.", lat=21.765, lng=72.145, mapQuery="Khodiyar Mata Temple Bhavnagar", nearestRail="Bhavnagar", nearestAirport="Bhavnagar", deityFamilies=["devi"]),
    T(city="Bhavnagar", slug="swaminarayan-bhavnagar", name="BAPS Swaminarayan Mandir, Bhavnagar", deity="Swaminarayan (Vaishnava)", location="Bhavnagar, Gujarat", state="Gujarat", glyph="स्व", tier="regional", famousFor="Marble Swaminarayan campus · Bhavnagar family search", summary="BAPS Swaminarayan Mandir — ornate marble temple serving Bhavnagar’s Vaishnava households.", mythology="Swaminarayan annakut and youth satsang complement Takhteshwar and Khodiyar on city festival calendars.", lat=21.760, lng=72.140, mapQuery="Swaminarayan Mandir Bhavnagar", nearestRail="Bhavnagar", nearestAirport="Bhavnagar", deityFamilies=["vishnu"], tags_extra=["modern-temples"]),
    # —— Belagavi ——
    T(city="Belagavi", slug="kapileshwar-belgaum", name="Kapileshwar Temple, Belagavi", deity="Lord Shiva (Kapileshwar)", location="Belagavi (Belgaum), Karnataka", state="Karnataka", glyph="क", tier="famous", famousFor="Cave Shiva · Belgaum city search", summary="Kapileshwar — cave Shiva temple at the heart of Belagavi old town.", mythology="Linga in a natural cave setting; Monday and Shivaratri define North Karnataka’s border-city Shaiva rhythm.", lat=15.870, lng=74.505, mapQuery="Kapileshwar Temple Belgaum", nearestRail="Belagavi Junction", nearestAirport="Belagavi", deityFamilies=["shiva"]),
    T(city="Belagavi", slug="maruti-mandir-belgaum", name="Maruti Mandir, Belagavi", deity="Lord Hanuman (Maruti)", location="Belagavi (Belgaum), Karnataka", state="Karnataka", glyph="म", tier="regional", famousFor="Fort-area Hanuman · Belgaum Tuesday search", summary="Maruti Mandir — historic Hanuman shrine near Belagavi Fort.", mythology="Hanuman guards the old fort quarter; Tuesday and Saturday arati draw Kannada–Marathi families of the twin-city belt.", lat=15.865, lng=74.510, mapQuery="Maruti Mandir Belgaum", nearestRail="Belagavi Junction", nearestAirport="Belagavi", deityFamilies=["hanuman"]),
    T(city="Belagavi", slug="jambukeshwar-belgaum", name="Jambukeshwar Temple, Belagavi", deity="Lord Shiva (Jambukeshwar)", location="Belagavi (Belgaum), Karnataka", state="Karnataka", glyph="ज", tier="regional", famousFor="Ancient Shiva in Belgaum · regional Pradosham search", summary="Jambukeshwar — old Shiva temple complementing Kapileshwar on Belagavi yatra loops.", mythology="Local sthala links the shrine to sage Jamadagni lore; living puja sustains Belgaum’s Shaiva merchant community.", lat=15.875, lng=74.500, mapQuery="Jambukeshwar Temple Belgaum", nearestRail="Belagavi Junction", nearestAirport="Belagavi", deityFamilies=["shiva"]),
    # —— Meerut ——
    T(city="Meerut", slug="augharnath-meerut", name="Augarnath (Kalipaltan) Temple, Meerut", deity="Lord Shiva (Augarnath) & Kali traditions", location="Meerut Cantonment, Meerut, Uttar Pradesh", state="Uttar Pradesh", glyph="अ", tier="famous", famousFor="1857 uprising shrine memory · Meerut top search", summary="Augarnath Temple — historic Shiva seat linked with Meerut Cantonment and freedom-era memory.", mythology="Kalipaltan area Shiva temple remembered in 1857 narratives; Shivaratri and local melas sustain cantonment bhakti.", lat=28.990, lng=77.710, mapQuery="Augarnath Temple Meerut", nearestRail="Meerut City", nearestAirport="Delhi", deityFamilies=["shiva"]),
    T(city="Meerut", slug="suraj-kund-meerut", name="Suraj Kund Temple, Meerut", deity="Lord Surya & associated deities", location="Suraj Kund, Meerut, Uttar Pradesh", state="Uttar Pradesh", glyph="सू", tier="regional", famousFor="Ancient tank-temple · Meerut heritage search", summary="Suraj Kund — historic sacred tank with active temple worship in Meerut.", mythology="Pre-Muslim era tank tradition; Chhath and Sunday Surya arghya draw Meerut families to the old kund.", lat=28.980, lng=77.700, mapQuery="Suraj Kund Meerut", nearestRail="Meerut", nearestAirport="Delhi", deityFamilies=["surya"]),
    T(city="Meerut", slug="mansadev-mandir-meerut", name="Mansa Devi Temple, Meerut", deity="Goddess Mansa Devi", location="Meerut, Uttar Pradesh", state="Uttar Pradesh", glyph="म", tier="regional", famousFor="Meerut Devi vows · Navaratri search", summary="Mansa Devi Mandir — popular Shakta shrine for Meerut’s urban devotees.", mythology="Wish-tying and Mundan ceremonies mark family life; Navaratri transforms lanes near the shrine.", lat=28.985, lng=77.705, mapQuery="Mansa Devi Temple Meerut", nearestRail="Meerut", nearestAirport="Delhi", deityFamilies=["devi"]),
    # —— Jamnagar ——
    T(city="Jamnagar", slug="bala-hanuman-jamnagar", name="Bala Hanuman Temple, Jamnagar", deity="Lord Hanuman (Bala Hanuman)", location="Lakhota Lake, Jamnagar, Gujarat", state="Gujarat", glyph="ब", tier="famous", famousFor="Continuous Ram dhun since 1964 · Guinness-record search", summary="Bala Hanuman — lakeside temple famed for unbroken ‘Shri Ram Jai Ram’ chanting.", mythology="Devotees maintain akhand dhun day and night; the lake setting and world-record memory make this Jamnagar’s signature tirtha.", lat=22.470, lng=70.070, mapQuery="Bala Hanuman Temple Jamnagar", nearestRail="Jamnagar", nearestAirport="Jamnagar", deityFamilies=["hanuman", "rama"]),
    T(city="Jamnagar", slug="mota-ashapura-jamnagar", name="Mota Ashapura Mata Temple, Jamnagar", deity="Goddess Ashapura Mata", location="Jamnagar, Gujarat", state="Gujarat", glyph="आ", tier="regional", famousFor="Kutchi–Saurashtra kuldevi · Jamnagar Devi search", summary="Mota Ashapura — major Ashapura Mata shrine of Jamnagar district.", mythology="Ashapura as kuldevi of many Kutchi and Kathiawadi families; Navaratri and newborn blessings define local calendar.", lat=22.465, lng=70.065, mapQuery="Ashapura Mata Temple Jamnagar", nearestRail="Jamnagar", nearestAirport="Jamnagar", deityFamilies=["devi"]),
    T(city="Jamnagar", slug="shri-dwarkadhish-jamnagar", name="Shri Dwarkadhish Temple, Jamnagar", deity="Lord Krishna (Dwarkadhish)", location="Jamnagar, Gujarat", state="Gujarat", glyph="द्", tier="regional", famousFor="City Krishna temple · Jamnagar Janmashtami search", summary="Dwarkadhish Mandir — active Krishna shrine in Jamnagar’s old city.", mythology="Krishna as king of Dwarka remembered in Kathiawad port culture; Janmashtami and Annakut draw city-wide bhajan.", lat=22.475, lng=70.075, mapQuery="Dwarkadhish Temple Jamnagar", nearestRail="Jamnagar", nearestAirport="Jamnagar", deityFamilies=["krishna", "vishnu"]),
    # —— Nellore ——
    T(city="Nellore", slug="ranganathaswamy-nellore", name="Sri Ranganathaswamy Temple, Nellore", deity="Lord Ranganatha (Vishnu)", location="Nellore, Andhra Pradesh", state="Andhra Pradesh", glyph="र", tier="famous", famousFor="Penna river Ranganatha · Nellore premier search", summary="Ranganathaswamy — ancient reclining Vishnu temple of Nellore on the Penna.", mythology="Among Andhra’s important Vaishnava kshetras; Brahmotsavam and Vaikunta Ekadashi anchor Nellore district pilgrimage.", lat=14.440, lng=79.990, mapQuery="Ranganathaswamy Temple Nellore", nearestRail="Nellore Junction", nearestAirport="Tirupati / Chennai", deityFamilies=["vishnu"]),
    T(city="Nellore", slug="talpagiri-ranganath-nellore", name="Talpagiri Ranganatha Swamy Temple, Nellore", deity="Lord Ranganatha (Vishnu)", location="Talpagiri, Nellore, Andhra Pradesh", state="Andhra Pradesh", glyph="त", tier="famous", famousFor="Hill Ranganatha · Nellore Brahmotsavam search", summary="Talpagiri Ranganatha — hilltop Vishnu temple with Nellore’s grand chariot festival.", mythology="Ranganatha on the hill above the city; Rath Yatra season rivals coastal Andhra’s great Vaishnava processions.", lat=14.435, lng=79.985, mapQuery="Talpagiri Ranganatha Temple Nellore", nearestRail="Nellore", nearestAirport="Tirupati", deityFamilies=["vishnu"]),
    T(city="Nellore", slug="penchalakona-narasimha", name="Penchalakona Narasimha Temple", deity="Lord Narasimha", location="Penchalakona, Nellore district, Andhra Pradesh", state="Andhra Pradesh", glyph="न", tier="famous", famousFor="Forest Narasimha · Nellore district yatra search", summary="Penchalakona — Narasimha in forest hills east of Nellore.", mythology="Narasimha as forest healer; Narasimha Jayanti and weekend tirtha from Nellore city pack the ghat road.", lat=14.350, lng=79.850, mapQuery="Penchalakona Narasimha Temple", nearestRail="Nellore / Gudur", nearestAirport="Tirupati", deityFamilies=["narasimha", "vishnu"]),
    # —— Rajkot ——
    T(city="Rajkot", slug="ramnath-mandir-rajkot", name="Ramnath Mahadev Temple, Rajkot", deity="Lord Shiva (Ramnath Mahadev)", location="Rajkot, Gujarat", state="Gujarat", glyph="र", tier="famous", famousFor="City-centre Shiva · Rajkot Shivaratri search", summary="Ramnath Mahadev — historic Shiva temple at the heart of Rajkot.", mythology="Among Saurashtra’s old urban Shiva seats; Shravan and Shivaratri define Rajkot’s Shaiva calendar.", lat=22.300, lng=70.790, mapQuery="Ramnath Mahadev Temple Rajkot", nearestRail="Rajkot Junction", nearestAirport="Rajkot", deityFamilies=["shiva"]),
    T(city="Rajkot", slug="kailasgiri-mandir-rajkot", name="Kailasgiri Temple, Rajkot", deity="Lord Shiva (Kailasgiri)", location="Rajkot, Gujarat", state="Gujarat", glyph="क", tier="regional", famousFor="Hill Shiva · Rajkot family darshan search", summary="Kailasgiri — hilltop Shiva shrine overlooking Rajkot.", mythology="Kailasa memory in miniature; Monday climbers and Mahashivaratri lamps on the ridge.", lat=22.310, lng=70.800, mapQuery="Kailasgiri Temple Rajkot", nearestRail="Rajkot", nearestAirport="Rajkot", deityFamilies=["shiva"]),
    T(city="Rajkot", slug="swaminarayan-rajkot", name="Shree Swaminarayan Mandir, Rajkot", deity="Swaminarayan (Vaishnava)", location="Rajkot, Gujarat", state="Gujarat", glyph="स", tier="regional", famousFor="Rajkot marble mandir · Swaminarayan search", summary="Swaminarayan Mandir Rajkot — ornate Vaishnava campus in the city centre.", mythology="Swaminarayan sampradaya anchors Kathiawadi festival life alongside Ramnath Shiva.", lat=22.305, lng=70.795, mapQuery="Swaminarayan Mandir Rajkot", nearestRail="Rajkot Junction", nearestAirport="Rajkot", deityFamilies=["vishnu"], tags_extra=["modern-temples"]),
    # —— Hassan ——
    T(city="Hassan", slug="hasanamba-hassan", name="Hasanamba Temple, Hassan", deity="Goddess Hasanamba", location="Hassan, Karnataka", state="Karnataka", glyph="ह", tier="famous", famousFor="Opens once a year · Hassan district mega-search", summary="Hasanamba — the Goddess temple that opens only during Deepavali week.", mythology="Hasanamba ‘smiles’ once a year when the doors open; the rest of the year the sanctum stays sealed — among Karnataka’s most unique Devi traditions.", lat=13.010, lng=76.100, mapQuery="Hasanamba Temple Hassan", nearestRail="Hassan Junction", nearestAirport="Mangaluru / Bengaluru", deityFamilies=["devi"], festivals=["Deepavali week opening"]),
    T(city="Hassan", slug="chennakeshava-belur", name="Chennakeshava Temple, Belur", deity="Lord Vishnu (Chennakeshava)", location="Belur, Hassan district, Karnataka", state="Karnataka", glyph="चे", tier="famous", famousFor="Hoysala sculpture marvel · Belur heritage search", summary="Chennakeshava Belur — masterpiece Hoysala Vishnu temple with star-shaped platform.", mythology="Built by Hoysala Vishnuvardhana; living puja continues amid UNESCO-grade sculpture that defines Hassan district yatra.", lat=13.165, lng=75.865, mapQuery="Chennakeshava Temple Belur", nearestRail="Hassan", nearestAirport="Mangaluru", deityFamilies=["vishnu"]),
    T(city="Hassan", slug="hoysaleswara-halebidu", name="Hoysaleswara Temple, Halebidu", deity="Lord Shiva (Hoysaleswara)", location="Halebidu, Hassan district, Karnataka", state="Karnataka", glyph="हो", tier="famous", famousFor="Twin Hoysala Shiva · Halebidu art search", summary="Hoysaleswara — paired Shiva temples with unmatched Hoysala carving at Halebidu.", mythology="Former Dwarasamudra capital’s Shiva seat; art pilgrims and Monday devotees share the mandapa.", lat=13.215, lng=75.995, mapQuery="Hoysaleswara Temple Halebidu", nearestRail="Hassan", nearestAirport="Mangaluru", deityFamilies=["shiva"]),
    # —— Sambalpur ——
    T(city="Sambalpur", slug="samaleswari-sambalpur", name="Maa Samaleswari Temple, Sambalpur", deity="Goddess Samaleswari", location="Sambalpur, Odisha", state="Odisha", glyph="स", tier="famous", famousFor="Western Odisha presiding Devi · Nuakhai search", summary="Samaleswari — presiding Goddess of Sambalpur and Western Odisha.", mythology="Nuakhai festival begins with Her blessings; the temple anchors Sambalpur’s river-bank civic and spiritual life.", lat=21.470, lng=83.970, mapQuery="Samaleswari Temple Sambalpur", nearestRail="Sambalpur Junction", nearestAirport="Jharsuguda / Raipur", deityFamilies=["devi"], festivals=["Nuakhai", "Navaratri"]),
    T(city="Sambalpur", slug="budharaja-sambalpur", name="Budharaja Temple, Sambalpur", deity="Lord Shiva (Budharaja)", location="Budharaja Hill, Sambalpur, Odisha", state="Odisha", glyph="बु", tier="regional", famousFor="Hill Shiva above Sambalpur · local Shivaratri search", summary="Budharaja — forest-hill Shiva temple overlooking Sambalpur.", mythology="Climb through sal forest to the linga; Shivaratri and Shravan Mondays draw Western Odisha families.", lat=21.480, lng=83.980, mapQuery="Budharaja Temple Sambalpur", nearestRail="Sambalpur", nearestAirport="Jharsuguda", deityFamilies=["shiva"]),
    T(city="Sambalpur", slug="ghanteswari-sambalpur", name="Ghanteswari Temple, Chiplima", deity="Goddess Ghanteswari", location="Chiplima, Sambalpur district, Odisha", state="Odisha", glyph="घ", tier="regional", famousFor="Bell-lined Devi shrine · Mahanadi gorge search", summary="Ghanteswari — Devi temple famous for countless bells offered by devotees.", mythology="Devotees hang bells when vows are fulfilled; the Mahanadi gorge setting pairs with Hirakud tourism.", lat=21.420, lng=83.920, mapQuery="Ghanteswari Temple Chiplima", nearestRail="Sambalpur", nearestAirport="Jharsuguda", deityFamilies=["devi"]),
    # —— Bidar ——
    T(city="Bidar", slug="narasimha-jharni-bidar", name="Narasimha Jharni (Cave Temple), Bidar", deity="Lord Narasimha", location="Bidar, Karnataka", state="Karnataka", glyph="झ", tier="famous", famousFor="Wade-through cave Narasimha · Bidar essential search", summary="Narasimha Jharni — cave shrine where devotees wade through water to reach Narasimha.", mythology="Man-lion form in a underground stream cave; unique darshan ritual makes Bidar a Narasimha pilgrimage name across Deccan.", lat=17.910, lng=77.520, mapQuery="Narasimha Jharni Bidar", nearestRail="Bidar", nearestAirport="Hyderabad", deityFamilies=["narasimha", "vishnu"]),
    T(city="Bidar", slug="papnash-shiva-bidar", name="Papnash Shiva Temple, Bidar", deity="Lord Shiva (Papnash)", location="Papnash Hill, Bidar, Karnataka", state="Karnataka", glyph="प", tier="regional", famousFor="Sin-washing Shiva lore · Bidar tank search", summary="Papnash — Shiva temple with sacred tank on Bidar hill.", mythology="Sthala purana claims sins dissolve in the Papnash tank; Shivaratri draws Hyderabad–Bidar corridor pilgrims.", lat=17.920, lng=77.530, mapQuery="Papnash Shiva Temple Bidar", nearestRail="Bidar", nearestAirport="Hyderabad", deityFamilies=["shiva"]),
    T(city="Bidar", slug="veerabhadra-bidar", name="Veerabhadra Temple, Bidar", deity="Lord Veerabhadra (Shiva)", location="Bidar, Karnataka", state="Karnataka", glyph="वी", tier="regional", famousFor="Fierce Shiva form · Bidar fort-area search", summary="Veerabhadra — active Shiva temple in Bidar’s old city near the fort.", mythology="Veerabhadra as Shiva’s wrathful emanation; pairs with Narasimha Jharni on Bidar district tirtha circuits.", lat=17.918, lng=77.528, mapQuery="Veerabhadra Temple Bidar", nearestRail="Bidar", nearestAirport="Hyderabad", deityFamilies=["shiva", "bhairav"]),
    # —— Aligarh ——
    T(city="Aligarh", slug="teerthdham-mangalayatan-aligarh", name="Teerthdham Mangalayatan, Aligarh", deity="Jain–Hindu pilgrimage campus (Shiva & Vishnu shrines)", location="Aligarh–Agra Road, Aligarh, Uttar Pradesh", state="Uttar Pradesh", glyph="म", tier="regional", famousFor="Mangalayatan pilgrimage campus · Aligarh search", summary="Mangalayatan — large pilgrimage complex with active Hindu shrines on the Aligarh–Agra corridor.", mythology="Multi-shrine campus draws families for festival melas; Hindu sections include Shiva and Vishnu worship alongside the well-known Jain tirtha.", lat=27.950, lng=78.150, mapQuery="Teerthdham Mangalayatan Aligarh", nearestRail="Aligarh Junction", nearestAirport="Delhi / Agra", deityFamilies=["shiva", "vishnu"]),
    T(city="Aligarh", slug="kali-mandir-aligarh", name="Kali Mandir, Aligarh", deity="Goddess Kali", location="Aligarh, Uttar Pradesh", state="Uttar Pradesh", glyph="का", tier="regional", famousFor="Aligarh city Kali · Kali Puja search", summary="Kali Mandir — central Shakta shrine of Aligarh.", mythology="Kali Puja and Navaratri arati define Aligarh’s Bengali–Hindi Shakta community calendar.", lat=27.890, lng=78.080, mapQuery="Kali Mandir Aligarh", nearestRail="Aligarh Junction", nearestAirport="Delhi", deityFamilies=["kali", "devi"]),
    T(city="Aligarh", slug="shiva-mandir-aligarh", name="Shiva Mandir, Aligarh", deity="Lord Shiva", location="Aligarh, Uttar Pradesh", state="Uttar Pradesh", glyph="श", tier="regional", famousFor="Aligarh Monday Shiva · local search", summary="Shiva Mandir — busy urban linga shrine of Aligarh.", mythology="Monday abhishek and Shravan see steady queues from AMU-town and old city families.", lat=27.885, lng=78.075, mapQuery="Shiva Mandir Aligarh", nearestRail="Aligarh Junction", nearestAirport="Delhi", deityFamilies=["shiva"]),
    # —— Alwar ——
    T(city="Alwar", slug="bhartrihari-baba-alwar", name="Bhartrihari Temple, Alwar", deity="Yogi Bhartrihari & Shiva traditions", location="Alwar, Rajasthan", state="Rajasthan", glyph="भ", tier="regional", famousFor="Bhartrihari samadhi lore · Alwar heritage search", summary="Bhartrihari Temple — shrine linked to the poet–yogi Bhartrihari near Alwar.", mythology="Regional memory places Bhartrihari’s tapas in the Aravalli foothills; pilgrims combine with Siliserh and city palace walks.", lat=27.560, lng=76.610, mapQuery="Bhartrihari Temple Alwar", nearestRail="Alwar Junction", nearestAirport="Jaipur", deityFamilies=["shiva"]),
    T(city="Alwar", slug="moosi-maharani-alwar", name="Moosi Maharani Ki Chhatri, Alwar", deity="Shiva linga & memorial shrines", location="Alwar, Rajasthan", state="Rajasthan", glyph="मू", tier="regional", famousFor="Royal cenotaph with living Shiva · Alwar search", summary="Moosi Maharani Chhatri — ornate cenotaph complex with active Shiva worship.", mythology="Rajput memorial architecture frames a living linga; evening arti draws Alwar families.", lat=27.550, lng=76.600, mapQuery="Moosi Maharani Chhatri Alwar", nearestRail="Alwar Junction", nearestAirport="Jaipur", deityFamilies=["shiva"]),
    T(city="Alwar", slug="jai-samadhi-alwar", name="Jai Samadhi (Jaisamand) Temple area, Alwar", deity="Lord Shiva & regional deities", location="Alwar, Rajasthan", state="Rajasthan", glyph="ज", tier="regional", famousFor="Lake-temple Alwar · weekend tirtha search", summary="Jaisamand area temples — sacred seats near Alwar’s historic lake belt.", mythology="Aravalli lake shrines combine nature and darshan for Alwar district weekend yatras.", lat=27.540, lng=76.590, mapQuery="Jaisamand Alwar temple", nearestRail="Alwar Junction", nearestAirport="Jaipur", deityFamilies=["shiva"]),
    # —— Junagadh ——
    T(city="Junagadh", slug="damodar-kund-junagadh", name="Damodar Kund, Junagadh", deity="Lord Krishna (Damodar) & sacred tank", location="Junagadh, Gujarat", state="Gujarat", glyph="द", tier="famous", famousFor="Krishna kund · Junagadh old city search", summary="Damodar Kund — sacred tank and Krishna shrine in Junagadh’s old quarter.", mythology="Damodar name ties to Krishna; pilgrims bathe before Girnar yatra in living custom.", lat=21.520, lng=70.460, mapQuery="Damodar Kund Junagadh", nearestRail="Junagadh Junction", nearestAirport="Rajkot / Keshod", deityFamilies=["krishna", "vishnu"]),
    T(city="Junagadh", slug="bhavnath-mahadev-junagadh", name="Bhavnath Mahadev Temple, Girnar", deity="Lord Shiva (Bhavnath Mahadev)", location="Girnar foothills, Junagadh, Gujarat", state="Gujarat", glyph="भ", tier="famous", famousFor="Maha Shivaratri mela · Girnar base search", summary="Bhavnath Mahadev — Shiva at Girnar’s foot where Maha Shivaratri fair fills the hills.", mythology="Naga sadhus and lakh-strong Shivaratri gathering make Bhavnath among Gujarat’s great Shaiva melas before Girnar climb.", lat=21.515, lng=70.520, mapQuery="Bhavnath Mahadev Temple Girnar", nearestRail="Junagadh", nearestAirport="Rajkot", deityFamilies=["shiva"], festivals=["Maha Shivaratri"]),
    T(city="Junagadh", slug="ambaji-temple-junagadh", name="Ambaji Temple, Junagadh", deity="Goddess Amba", location="Junagadh, Gujarat", state="Gujarat", glyph="अ", tier="regional", famousFor="Junagadh Devi · Navaratri search", summary="Ambaji Mandir — city Devi shrine before Girnar ascent.", mythology="Amba as kuldevi for many Kathiawadi families; Navaratri garba nights radiate from the old city.", lat=21.525, lng=70.465, mapQuery="Ambaji Temple Junagadh", nearestRail="Junagadh Junction", nearestAirport="Rajkot", deityFamilies=["devi"]),
    # —— Satara ——
    T(city="Satara", slug="ajinkyatara-satara", name="Ajinkyatara Devi Temple, Satara", deity="Goddess Ajinkyatara (Yogeshwari)", location="Ajinkyatara Fort hill, Satara, Maharashtra", state="Maharashtra", glyph="अ", tier="famous", famousFor="Fort-hill Devi · Satara landmark search", summary="Ajinkyatara — Yogeshwari Devi on the fort hill above Satara town.", mythology="The fort Devi watches the Satara plain; Navaratri and full-moon climbs define city pilgrimage.", lat=17.680, lng=74.010, mapQuery="Ajinkyatara Temple Satara", nearestRail="Satara Road", nearestAirport="Pune", deityFamilies=["devi"]),
    T(city="Satara", slug="chaphal-samarth-mandir", name="Samarth Ramdas Swami Temple, Chaphal", deity="Lord Rama & Samarth Ramdas tradition", location="Chaphal, Satara district, Maharashtra", state="Maharashtra", glyph="च", tier="famous", famousFor="Samarth Ramdas birthplace · Satara district search", summary="Chaphal — birthplace shrine of Samarth Ramdas with Rama worship.", mythology="Ramdas’s bhakti shaped Shivaji-era Maharashtra; Hanuman and Rama darshan draw Sadhana seekers from Pune–Satara.", lat=17.580, lng=73.980, mapQuery="Samarth Ramdas Temple Chaphal", nearestRail="Satara", nearestAirport="Pune", deityFamilies=["rama", "hanuman"]),
    T(city="Satara", slug="yamai-devi-satara", name="Yamai Devi Temple, Aundh", deity="Goddess Yamai Devi", location="Aundh, Satara district, Maharashtra", state="Maharashtra", glyph="य", tier="regional", famousFor="Kuldevi of many Desh families · Satara search", summary="Yamai Devi Aundh — hill Devi shrine revered across Desh Maharashtra.", mythology="Yamai as family Goddess for numerous Maratha clans; annual jatra and Navaratri lamp trails on the hill.", lat=17.550, lng=74.050, mapQuery="Yamai Devi Temple Aundh Satara", nearestRail="Satara", nearestAirport="Pune", deityFamilies=["devi"]),
    # —— Kochi / Ernakulam (top-up) ——
    T(city="Kochi", slug="ernakulathappan-kochi", name="Ernakulathappan Temple, Ernakulam", deity="Lord Shiva (Ernakulathappan)", location="Ernakulam, Kochi, Kerala", state="Kerala", glyph="ए", tier="famous", famousFor="City namesake Shiva · Ernakulam search", summary="Ernakulathappan — the Shiva who gives Ernakulam its sacred name.", mythology="Shiva as patron of the merchant city; Shivaratri and Thiruvathira draw Kerala’s urban Shaiva crowds.", lat=9.970, lng=76.280, mapQuery="Ernakulathappan Temple Ernakulam", nearestRail="Ernakulam Junction", nearestAirport="Kochi", deityFamilies=["shiva"]),
    T(city="Kochi", slug="thrikkakara-vamana-kochi", name="Thrikkakara Vamana Moorthy Temple", deity="Lord Vamana (Vishnu)", location="Thrikkakara, Kochi, Kerala", state="Kerala", glyph="व", tier="famous", famousFor="Onam origin temple · Kerala Vamana search", summary="Thrikkakara — Vamana temple linked with Onam and Mahabali lore.", mythology="Tradition places Mahabali’s annual visit memory here; Onam feast and Vamana worship define Kerala’s harvest festival root.", lat=10.020, lng=76.320, mapQuery="Thrikkakara Vamana Temple", nearestRail="Ernakulam", nearestAirport="Kochi", deityFamilies=["vishnu"], festivals=["Onam"]),
    # —— Jamshedpur ——
    T(city="Jamshedpur", slug="bhuvaneshwari-jamshedpur", name="Bhuvaneshwari Temple, Jamshedpur", deity="Goddess Bhuvaneshwari", location="Jamshedpur, Jharkhand", state="Jharkhand", glyph="भू", tier="regional", famousFor="Jamshedpur city Devi · Jharkhand search", summary="Bhuvaneshwari Mandir — prominent Devi shrine of Jamshedpur.", mythology="Steel-city families vow at Bhuvaneshwari for health and prosperity; Navaratri fills Tata-town neighbourhoods.", lat=22.805, lng=86.185, mapQuery="Bhuvaneshwari Temple Jamshedpur", nearestRail="Tatanagar Junction", nearestAirport="Ranchi / Kolkata", deityFamilies=["devi"]),
    T(city="Jamshedpur", slug="digwadih-kali-jamshedpur", name="Kali Mandir, Digwadih", deity="Goddess Kali", location="Digwadih, Jamshedpur, Jharkhand", state="Jharkhand", glyph="का", tier="regional", famousFor="Digwadih Kali · Jamshedpur Shakta search", summary="Digwadih Kali Mandir — active Shakta seat in Jamshedpur’s industrial belt.", mythology="Kali Puja and Saturday arati draw Bengali–Hindi workers of the factory quarters.", lat=22.790, lng=86.200, mapQuery="Kali Mandir Digwadih Jamshedpur", nearestRail="Tatanagar", nearestAirport="Ranchi", deityFamilies=["kali", "devi"]),
    T(city="Jamshedpur", slug="sakchi-shiva-jamshedpur", name="Shiva Mandir, Sakchi", deity="Lord Shiva", location="Sakchi, Jamshedpur, Jharkhand", state="Jharkhand", glyph="श", tier="regional", famousFor="Sakchi Shiva · Jamshedpur Monday search", summary="Sakchi Shiva Mandir — central urban linga shrine of Jamshedpur.", mythology="Monday abhishek rhythm for Tata Steel town’s Hindi–Bengali devotees.", lat=22.800, lng=86.190, mapQuery="Shiva Mandir Sakchi Jamshedpur", nearestRail="Tatanagar Junction", nearestAirport="Ranchi", deityFamilies=["shiva"]),
    # —— Faridabad ——
    T(city="Faridabad", slug="iskcon-faridabad", name="ISKCON Temple, Faridabad", deity="Krishna–Radha (ISKCON)", location="Faridabad, Haryana", state="Haryana", glyph="इ", tier="regional", famousFor="Faridabad ISKCON · NCR Krishna search", summary="ISKCON Faridabad — Krishna temple serving NCR’s industrial suburb.", mythology="Sunday feast and Janmashtami draw Faridabad–Ballabhgarh families into Gaudiya kirtan culture.", lat=28.410, lng=77.320, mapQuery="ISKCON Temple Faridabad", nearestRail="Faridabad / Delhi", nearestAirport="Delhi", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    T(city="Faridabad", slug="shirdi-sai-faridabad", name="Shirdi Sai Baba Temple, Faridabad", deity="Sai Baba of Shirdi", location="Faridabad, Haryana", state="Haryana", glyph="स", tier="regional", famousFor="Faridabad Sai bhakti · Thursday search", summary="Sai Baba Mandir — popular Sai shrine in Faridabad.", mythology="Thursday oil lamp and annadanam seva anchor suburban NCR Sai devotion.", lat=28.400, lng=77.310, mapQuery="Sai Baba Temple Faridabad", nearestRail="Faridabad", nearestAirport="Delhi", deityFamilies=["sai"]),
    T(city="Faridabad", slug="baba-lakshman-das-faridabad", name="Baba Lakshman Das Temple, Faridabad", deity="Lord Hanuman & local saint traditions", location="Faridabad, Haryana", state="Haryana", glyph="ह", tier="regional", famousFor="Old Faridabad Hanuman · local mela search", summary="Baba Lakshman Das — Hanuman-focused shrine with fair-day crowds.", mythology="Tuesday and Saturday queues for Faridabad’s old-town Hanuman bhakti.", lat=28.395, lng=77.305, mapQuery="Hanuman Temple Faridabad", nearestRail="Faridabad", nearestAirport="Delhi", deityFamilies=["hanuman"]),
    # —— Gulbarga / Kalaburagi ——
    T(city="Gulbarga", slug="sharana-basaveshwara-gulbarga", name="Sharana Basaveshwara Temple, Gulbarga", deity="Basaveshwara (Lingayat Shiva–guru)", location="Gulbarga (Kalaburagi), Karnataka", state="Karnataka", glyph="श", tier="famous", famousFor="Sharana movement seat · Kalaburagi search", summary="Sharana Basaveshwara — premier Lingayat pilgrimage centre of Kalaburagi.", mythology="Basaveshwara’s vachana revolution memory; annual fair and Lingayat bhakti define Hyderabad–Karnataka spiritual life.", lat=17.330, lng=76.830, mapQuery="Sharana Basaveshwara Temple Gulbarga", nearestRail="Gulbarga / Kalaburagi", nearestAirport="Hyderabad", deityFamilies=["shiva"]),
    T(city="Gulbarga", slug="siddharoodha-math-gulbarga", name="Siddharoodha Math, Gulbarga", deity="Lord Shiva (Siddharoodha Swami samadhi)", location="Gulbarga (Kalaburagi), Karnataka", state="Karnataka", glyph="सि", tier="regional", famousFor="Veershaiva math · Gulbarga search", summary="Siddharoodha Math — Veerashaiva pilgrimage seat in Kalaburagi.", mythology="Samadhi tradition and annadanam draw North Karnataka devotees on festival days.", lat=17.335, lng=76.835, mapQuery="Siddharoodha Math Gulbarga", nearestRail="Gulbarga", nearestAirport="Hyderabad", deityFamilies=["shiva"]),
    T(city="Gulbarga", slug="venkateswara-gulbarga", name="Venkateswara Temple, Gulbarga", deity="Lord Venkateswara", location="Gulbarga (Kalaburagi), Karnataka", state="Karnataka", glyph="व", tier="regional", famousFor="Kalaburagi Balaji · Vaishnava search", summary="Venkateswara Mandir — active Balaji shrine in Gulbarga city.", mythology="Andhra–Karnataka border Balaji bhakti; Vaikunta Ekadashi and Saturday darshan for IT–farm belt families.", lat=17.340, lng=76.840, mapQuery="Venkateswara Temple Gulbarga", nearestRail="Gulbarga", nearestAirport="Hyderabad", deityFamilies=["venkateswara", "vishnu"]),
    # —— Palakkad ——
    T(city="Palakkad", slug="kalpathy-viswanathaswamy", name="Kalpathy Viswanathaswamy Temple", deity="Lord Shiva (Viswanathaswamy)", location="Kalpathy, Palakkad, Kerala", state="Kerala", glyph="क", tier="famous", famousFor="Tamil Brahmin agraharam Shiva · Palakkad search", summary="Kalpathy Viswanathaswamy — heritage Shiva temple in Palakkad’s agraharam.", mythology="Ratholsavam chariot festival and Tamil–Malayalam culture blend at this ancient Viswanatha seat.", lat=10.780, lng=76.660, mapQuery="Kalpathy Viswanathaswamy Temple", nearestRail="Palakkad Junction", nearestAirport="Coimbatore", deityFamilies=["shiva"], festivals=["Kalpathy Ratholsavam"]),
    T(city="Palakkad", slug="jainimedu-vishwanatha-palakkad", name="Jainimedu Vishwanatha Temple, Palakkad", deity="Lord Shiva (Vishwanatha)", location="Jainimedu, Palakkad, Kerala", state="Kerala", glyph="ज", tier="regional", famousFor="Palakkad city Shiva · local search", summary="Jainimedu Vishwanatha — active Shiva shrine in Palakkad town.", mythology="Urban Shaiva seat for Palakkad’s mixed Tamil–Malayalam devotee base.", lat=10.770, lng=76.650, mapQuery="Jainimedu Shiva Temple Palakkad", nearestRail="Palakkad Junction", nearestAirport="Coimbatore", deityFamilies=["shiva"]),
    T(city="Palakkad", slug="malampuzha-bhagavathi", name="Malampuzha Bhagavathi Temple", deity="Goddess Bhagavathi", location="Malampuzha, Palakkad, Kerala", state="Kerala", glyph="म", tier="regional", famousFor="Dam-side Devi · Palakkad tourism search", summary="Malampuzha Bhagavathi — Devi shrine near the famous dam gardens.", mythology="Tourism and tirtha combine; festival processions draw Palakkad district agrarian communities.", lat=10.830, lng=76.680, mapQuery="Malampuzha Bhagavathi Temple", nearestRail="Palakkad", nearestAirport="Coimbatore", deityFamilies=["devi"]),
    # —— Kollam ——
    T(city="Kollam", slug="anandavalleeswaram-kollam", name="Anandavalleeswaram Mahadeva Temple, Kollam", deity="Lord Shiva (Mahadeva) & Goddess Anandavalli", location="Anandavalleeswaram, Kollam, Kerala", state="Kerala", glyph="आ", tier="famous", famousFor="Twin Shiva–Devi · Kollam city search", summary="Anandavalleeswaram — ancient Shiva–Devi complex in Kollam.", mythology="Among Kerala’s old urban temple pairs; Shivaratri and Pooram season define Kollam’s sacred calendar.", lat=8.880, lng=76.590, mapQuery="Anandavalleeswaram Temple Kollam", nearestRail="Kollam Junction", nearestAirport="Trivandrum", deityFamilies=["shiva", "devi"]),
    T(city="Kollam", slug="ashtamudi-mahavishnu-kollam", name="Ashtamudi Mahavishnu Temple, Kollam", deity="Lord Vishnu (Mahavishnu)", location="Ashtamudi, Kollam, Kerala", state="Kerala", glyph="अ", tier="regional", famousFor="Backwater Vishnu · Kollam search", summary="Ashtamudi Mahavishnu — Vishnu shrine on Kollam’s backwater belt.", mythology="Boat-access darshan memory for fishermen and traders of the cashew coast.", lat=8.900, lng=76.600, mapQuery="Mahavishnu Temple Kollam", nearestRail="Kollam Junction", nearestAirport="Trivandrum", deityFamilies=["vishnu"]),
    T(city="Kollam", slug="puthenkulangara-devi-kollam", name="Puthenkulangara Devi Temple, Kollam", deity="Goddess Bhagavathi", location="Puthenkulangara, Kollam, Kerala", state="Kerala", glyph="प", tier="regional", famousFor="Theyyam-adjacent Devi · Kollam district search", summary="Puthenkulangara Bhagavathy — powerful Devi kshetram near Kollam.", mythology="Fire-walk and padayani-style festival memory draw coastal Shakta devotees.", lat=8.870, lng=76.580, mapQuery="Puthenkulangara Devi Temple Kollam", nearestRail="Kollam", nearestAirport="Trivandrum", deityFamilies=["devi"]),
    # —— Nagercoil ——
    T(city="Nagercoil", slug="nagaraja-nagercoil", name="Nagaraja Temple, Nagercoil", deity="Nagaraja (serpent lord) & Shiva–Vishnu traditions", location="Nagercoil, Tamil Nadu", state="Tamil Nadu", glyph="न", tier="famous", famousFor="Snake-deity kshetram · Kanyakumari district search", summary="Nagaraja Temple — unique serpent-deity shrine giving Nagercoil its name.", mythology="Naga worship with Tamil–Kerala border culture; Ayilyam days and milk offerings define the tirtha.", lat=8.180, lng=77.430, mapQuery="Nagaraja Temple Nagercoil", nearestRail="Nagercoil Junction", nearestAirport="Trivandrum", deityFamilies=["devi", "shiva"]),
    T(city="Nagercoil", slug="suchindram-temple", name="Thanumalayan Temple, Suchindram", deity="Trimurti — Shiva, Vishnu, Brahma (Sthanumalayan)", location="Suchindram, Nagercoil, Tamil Nadu", state="Tamil Nadu", glyph="स्थ", tier="famous", famousFor="Single idol three Gods · Suchindram search", summary="Thanumalayan — rare trimurti representation in one linga-form near Nagercoil.", mythology="Musical pillars and 22-foot Hanuman statue; among Kanyakumari district’s essential tirthas.", lat=8.150, lng=77.470, mapQuery="Thanumalayan Temple Suchindram", nearestRail="Nagercoil", nearestAirport="Trivandrum", deityFamilies=["shiva", "vishnu"]),
    T(city="Nagercoil", slug="kumari-amman-kanyakumari", name="Kumari Amman Temple, Kanyakumari", deity="Goddess Kumari Amman (Parvati)", location="Kanyakumari, Tamil Nadu", state="Tamil Nadu", glyph="कु", tier="famous", famousFor="Southern tip Shakti · sunrise darshan search", summary="Kumari Amman — Devi at India’s southern tip where three seas meet.", mythology="Parvati as eternal virgin Goddess; sunrise darshan and Navaratri draw national pilgrimage.", lat=8.080, lng=77.550, mapQuery="Kumari Amman Temple Kanyakumari", nearestRail="Kanyakumari", nearestAirport="Trivandrum", deityFamilies=["devi"]),
    # —— Bhuj ——
    T(city="Bhuj", slug="bhujia-fort-temple", name="Bhujia Fort Temple (Bhujia Mata), Bhuj", deity="Goddess Bhujia Mata", location="Bhujia Hill, Bhuj, Gujarat", state="Gujarat", glyph="भु", tier="famous", famousFor="Fort-hill Devi · Bhuj landmark search", summary="Bhujia Mata — hill fortress Goddess shrine above Bhuj.", mythology="Navaratri climbs and Kutchi kuldevi vows; the fort hill defines Bhuj skyline pilgrimage.", lat=23.260, lng=69.670, mapQuery="Bhujia Mata Temple Bhuj", nearestRail="Bhuj", nearestAirport="Bhuj", deityFamilies=["devi"]),
    T(city="Bhuj", slug="swaminarayan-bhuj", name="Shree Swaminarayan Mandir, Bhuj", deity="Swaminarayan (Vaishnava)", location="Bhuj, Gujarat", state="Gujarat", glyph="स", tier="famous", famousFor="Earthquake-rebuilt marble mandir · Kutch search", summary="Swaminarayan Mandir Bhuj — rebuilt ornate temple after 2001 earthquake.", mythology="Community rebuilt this marble campus as Kutch’s Vaishnava heart; Annakut and Janmashtami draw diaspora returnees.", lat=23.250, lng=69.660, mapQuery="Swaminarayan Mandir Bhuj", nearestRail="Bhuj", nearestAirport="Bhuj", deityFamilies=["vishnu"], tags_extra=["modern-temples"]),
    T(city="Bhuj", slug="ashapura-mata-mata-no-madh", name="Ashapura Mata Temple, Mata no Madh", deity="Goddess Ashapura Mata", location="Mata no Madh, Kutch (near Bhuj), Gujarat", state="Gujarat", glyph="आ", tier="famous", famousFor="Kutch kuldevi · Ashapura mega-search", summary="Ashapura Mata at Mata no Madh — principal kuldevi shrine of Kutch.", mythology="Ashapura as mother of Kutch; full-moon and Navaratri see lakhs from Gujarat and diaspora.", lat=23.400, lng=69.200, mapQuery="Ashapura Mata Mata no Madh", nearestRail="Bhuj / Gandhidham", nearestAirport="Bhuj", deityFamilies=["devi"]),
    # —— Darbhanga ——
    T(city="Darbhanga", slug="shyama-mai-darbhanga", name="Shyama Mai Temple, Darbhanga", deity="Goddess Shyama Mai (Kali form)", location="Darbhanga, Bihar", state="Bihar", glyph="श्", tier="famous", famousFor="Mithila Shakti · Darbhanga city search", summary="Shyama Mai — premier Devi temple of Darbhanga royal city.", mythology="Maithili Shakta tradition; Navaratri and Kali Puja transform Darbhanga’s old quarter.", lat=26.150, lng=85.900, mapQuery="Shyama Mai Temple Darbhanga", nearestRail="Darbhanga Junction", nearestAirport="Darbhanga / Patna", deityFamilies=["kali", "devi"]),
    T(city="Darbhanga", slug="ahilya-asthan-darbhanga", name="Ahilya Asthan, Kamtaul", deity="Goddess Sita (Ahilya redemption site)", location="Kamtaul, Darbhanga district, Bihar", state="Bihar", glyph="अ", tier="regional", famousFor="Ramayana Ahilya lore · Mithila search", summary="Ahilya Asthan — shrine linked with Ahilya’s redemption in Ramayana memory.", mythology="Local tradition marks the stone-turned-wife’s return to human form by Rama’s touch; draws Mithila Ramayana pilgrims.", lat=26.200, lng=85.950, mapQuery="Ahilya Asthan Kamtaul", nearestRail="Kamtaul", nearestAirport="Darbhanga", deityFamilies=["rama", "devi"]),
    T(city="Darbhanga", slug="kankali-mandir-darbhanga", name="Kankali Mandir, Darbhanga", deity="Goddess Kankali", location="Darbhanga, Bihar", state="Bihar", glyph="क", tier="regional", famousFor="Darbhanga Devi · local Navaratri search", summary="Kankali Mandir — active Devi shrine in Darbhanga.", mythology="Shakta vows for family health; pairs with Shyama Mai on Mithila tirtha loops.", lat=26.155, lng=85.905, mapQuery="Kankali Mandir Darbhanga", nearestRail="Darbhanga Junction", nearestAirport="Darbhanga", deityFamilies=["devi"]),
    # —— Davangere ——
    T(city="Davangere", slug="kunduwada-kere-davangere", name="Kunduwada Kere (Shiva) Temple, Davangere", deity="Lord Shiva", location="Kunduwada Kere, Davangere, Karnataka", state="Karnataka", glyph="कु", tier="regional", famousFor="Lake Shiva · Davangere search", summary="Kunduwada Kere Shiva — lakeside linga shrine of Davangere.", mythology="Tank and temple pair for Monday abhishek; Davangere’s textile-town devotees.", lat=14.470, lng=75.920, mapQuery="Kunduwada Kere Davangere", nearestRail="Davangere", nearestAirport="Hubballi", deityFamilies=["shiva"]),
    T(city="Davangere", slug="siddeshwara-davangere", name="Siddeshwara Temple, Davangere", deity="Lord Shiva (Siddeshwara)", location="Davangere, Karnataka", state="Karnataka", glyph="स", tier="regional", famousFor="City Shiva · Davangere Shivaratri search", summary="Siddeshwara — central Shiva temple of Davangere.", mythology="Shivaratri fair and Pradosham anchor Davangere district Shaivism.", lat=14.465, lng=75.925, mapQuery="Siddeshwara Temple Davangere", nearestRail="Davangere Junction", nearestAirport="Hubballi", deityFamilies=["shiva"]),
    T(city="Davangere", slug="anjaneya-davangere", name="Anjaneya Swamy Temple, Davangere", deity="Lord Hanuman", location="Davangere, Karnataka", state="Karnataka", glyph="ह", tier="regional", famousFor="Davangere Hanuman · Saturday search", summary="Anjaneya Swamy — prominent Hanuman shrine in Davangere.", mythology="Saturday sindoor arati for students and traders of the cotton city.", lat=14.460, lng=75.930, mapQuery="Anjaneya Temple Davangere", nearestRail="Davangere", nearestAirport="Hubballi", deityFamilies=["hanuman"]),
    # —— Bellary ——
    T(city="Bellary", slug="kote-anjaneya-bellary", name="Kote Anjaneya Temple, Bellary", deity="Lord Hanuman (Kote Anjaneya)", location="Bellary Fort area, Ballari, Karnataka", state="Karnataka", glyph="को", tier="famous", famousFor="Fort Hanuman · Ballari search", summary="Kote Anjaneya — Hanuman at Bellary Fort’s sacred quarter.", mythology="Hanuman guards the fort town; Tuesdays see extraordinary queues in mining-belt Ballari.", lat=15.150, lng=76.920, mapQuery="Kote Anjaneya Temple Bellary", nearestRail="Ballari Junction", nearestAirport="Hubballi / Bengaluru", deityFamilies=["hanuman"]),
    T(city="Bellary", slug="durgamma-bellary", name="Durgamma Temple, Bellary", deity="Goddess Durgamma", location="Ballari, Karnataka", state="Karnataka", glyph="दु", tier="regional", famousFor="Ballari Devi · Dasara search", summary="Durgamma — city Goddess temple of Ballari.", mythology="Dasara and village deity processions define Ballari Shakta public culture.", lat=15.145, lng=76.925, mapQuery="Durgamma Temple Bellary", nearestRail="Ballari Junction", nearestAirport="Hubballi", deityFamilies=["devi"]),
    T(city="Bellary", slug="kumaraswamy-sandur", name="Kumaraswamy Temple, Sandur", deity="Lord Murugan (Kumaraswamy)", location="Sandur, Ballari district, Karnataka", state="Karnataka", glyph="कु", tier="regional", famousFor="Hill Murugan near Ballari · Skanda search", summary="Sandur Kumaraswamy — hill Murugan temple near Ballari mining country.", mythology="Murugan as youthful commander; Thai Poosam kavadi from Ballari town.", lat=15.100, lng=76.550, mapQuery="Kumaraswamy Temple Sandur", nearestRail="Ballari / Toranagallu", nearestAirport="Hubballi", deityFamilies=["murugan"]),
    # —— Bijapur / Vijayapura ——
    T(city="Bijapur", slug="siddeshwar-bijapur", name="Siddeshwar Temple, Vijayapura", deity="Lord Shiva (Siddeshwar)", location="Vijayapura (Bijapur), Karnataka", state="Karnataka", glyph="सि", tier="regional", famousFor="Vijayapura city Shiva · Bijapur search", summary="Siddeshwar — active Shiva temple in Vijayapura old town.", mythology="Living Shaiva seat amid Adil Shahi heritage; Shivaratri draws Bijapur district farmers.", lat=16.830, lng=75.710, mapQuery="Siddeshwar Temple Bijapur", nearestRail="Vijayapura / Bijapur", nearestAirport="Hubballi / Solapur", deityFamilies=["shiva"]),
    T(city="Bijapur", slug="shivgiri-bijapur", name="Shivgiri Temple, Vijayapura", deity="Lord Shiva", location="Vijayapura (Bijapur), Karnataka", state="Karnataka", glyph="श", tier="regional", famousFor="Shivgiri hill Shiva · Bijapur local yatra", summary="Shivgiri — hill Shiva shrine on Vijayapura’s outskirts.", mythology="Short hill climb for Monday darshan; pairs with Gol Gumbaz tourism on culture circuits.", lat=16.840, lng=75.720, mapQuery="Shivgiri Temple Bijapur", nearestRail="Bijapur", nearestAirport="Hubballi", deityFamilies=["shiva"]),
    T(city="Bijapur", slug="umapati-bijapur", name="Umapati Temple, Vijayapura", deity="Lord Shiva (Umapati)", location="Vijayapura (Bijapur), Karnataka", state="Karnataka", glyph="उ", tier="regional", famousFor="Heritage Shiva · Vijayapura search", summary="Umapati Mandir — historic Shiva in Bijapur’s temple quarter.", mythology="Pre-Sultanate layer of Vijayapura’s sacred map; Monday puja continues for old-city families.", lat=16.825, lng=75.715, mapQuery="Umapati Temple Bijapur", nearestRail="Bijapur", nearestAirport="Hubballi", deityFamilies=["shiva"]),
    # —— Eluru ——
    T(city="Eluru", slug="dvaraka-tirumala-eluru", name="Sri Venkateswara Swamy Temple, Dvaraka Tirumala", deity="Lord Venkateswara", location="Dvaraka Tirumala, West Godavari (near Eluru), Andhra Pradesh", state="Andhra Pradesh", glyph="द्", tier="famous", famousFor="West Godavari Balaji · Eluru circuit search", summary="Dvaraka Tirumala — major Venkateswara hill temple near Eluru.", mythology="Called ‘Chinna Tirupati’ of coastal Andhra; Vaikunta Ekadashi and hair-offering vows draw Godavari delta pilgrims.", lat=16.820, lng=81.330, mapQuery="Dvaraka Tirumala Temple", nearestRail="Eluru / Bhimadole", nearestAirport="Rajahmundry / Vijayawada", deityFamilies=["venkateswara", "vishnu"]),
    T(city="Eluru", slug="ramalingeswara-eluru", name="Ramalingeswara Swamy Temple, Eluru", deity="Lord Shiva (Ramalingeswara)", location="Eluru, Andhra Pradesh", state="Andhra Pradesh", glyph="र", tier="regional", famousFor="Eluru city Shiva · Godavari search", summary="Ramalingeswara — central Shiva temple of Eluru town.", mythology="Godavari-belt Shaiva seat; Maha Shivaratri and Kartik Mondays for West Godavari families.", lat=16.710, lng=81.100, mapQuery="Ramalingeswara Temple Eluru", nearestRail="Eluru Junction", nearestAirport="Rajahmundry", deityFamilies=["shiva"]),
    T(city="Eluru", slug="pancharama-amareswara-eluru", name="Amareswara Temple, Amaravati (Pancharama)", deity="Lord Shiva (Amareswara)", location="Amaravati, near Eluru, Andhra Pradesh", state="Andhra Pradesh", glyph="अ", tier="famous", famousFor="Pancharama kshetram · Amaravati search", summary="Amareswara — one of Andhra’s five Pancharama Shiva temples near Eluru.", mythology="Pancharama tradition links five ancient Shivalingas; Amareswara draws Krishna–Godavari pilgrim circuits.", lat=16.570, lng=80.350, mapQuery="Amareswara Temple Amaravati", nearestRail="Guntur / Vijayawada", nearestAirport="Vijayawada", deityFamilies=["shiva"]),
    # —— Kadapa ——
    T(city="Kadapa", slug="devuni-kadapa-venkateswara", name="Devuni Kadapa Venkateswara Temple", deity="Lord Venkateswara", location="Kadapa (Cuddapah), Andhra Pradesh", state="Andhra Pradesh", glyph="व", tier="famous", famousFor="Kadapa Balaji · Rayalaseema search", summary="Devuni Kadapa Venkateswara — hill Balaji of Kadapa town.", mythology="Called ‘Tirupati’s little brother’ in Rayalaseema lore; Brahmotsavam and Saturday vows define Kadapa pilgrimage.", lat=14.470, lng=78.820, mapQuery="Devuni Kadapa Venkateswara Temple", nearestRail="Kadapa Junction", nearestAirport="Tirupati / Bengaluru", deityFamilies=["venkateswara", "vishnu"]),
    T(city="Kadapa", slug="veerabhadra-kadapa", name="Veerabhadra Temple, Kadapa", deity="Lord Veerabhadra (Shiva)", location="Kadapa (Cuddapah), Andhra Pradesh", state="Andhra Pradesh", glyph="वी", tier="regional", famousFor="Kadapa Shiva · local search", summary="Veerabhadra — fierce Shiva form temple in Kadapa.", mythology="Shravan and Shivaratri abhishek for Rayalaseema devotees.", lat=14.475, lng=78.825, mapQuery="Veerabhadra Temple Kadapa", nearestRail="Kadapa", nearestAirport="Tirupati", deityFamilies=["shiva", "bhairav"]),
    T(city="Kadapa", slug="kodanda-rama-kadapa", name="Kodanda Rama Temple, Vontimitta", deity="Lord Rama (Kodanda Rama)", location="Vontimitta, Kadapa district, Andhra Pradesh", state="Andhra Pradesh", glyph="को", tier="famous", famousFor="Single-stone Rama temple · Kadapa district search", summary="Vontimitta Kodanda Rama — ancient Rama temple carved from single stone.", mythology="Ramayana architecture marvel of Rayalaseema; Ram Navami draws district-wide bhakti.", lat=14.380, lng=79.020, mapQuery="Kodanda Rama Temple Vontimitta", nearestRail="Kadapa / Rajampet", nearestAirport="Tirupati", deityFamilies=["rama"]),
    # —— Tiruppur ——
    T(city="Tiruppur", slug="sukreeswarar-tiruppur", name="Sukreeswarar Temple, Tiruppur", deity="Lord Shiva (Sukreeswarar)", location="Tiruppur, Tamil Nadu", state="Tamil Nadu", glyph="सु", tier="regional", famousFor="Tiruppur city Shiva · textile-town search", summary="Sukreeswarar — historic Shiva temple in Tiruppur.", mythology="Sukreeva lore in sthala name; Shivaratri for Kongu textile workers.", lat=11.110, lng=77.340, mapQuery="Sukreeswarar Temple Tiruppur", nearestRail="Tiruppur", nearestAirport="Coimbatore", deityFamilies=["shiva"]),
    T(city="Tiruppur", slug="uthukuli-murugan-tiruppur", name="Uthukuli Murugan Temple", deity="Lord Murugan", location="Uthukuli, Tiruppur district, Tamil Nadu", state="Tamil Nadu", glyph="उ", tier="regional", famousFor="Tiruppur district Murugan · Thai Poosam search", summary="Uthukuli Murugan — hill Murugan near Tiruppur.", mythology="Kavadi season from textile belt; Murugan as guardian of export-industry town families.", lat=11.150, lng=77.400, mapQuery="Uthukuli Murugan Temple", nearestRail="Tiruppur", nearestAirport="Coimbatore", deityFamilies=["murugan"]),
    T(city="Tiruppur", slug="mariamman-tiruppur", name="Mariamman Temple, Tiruppur", deity="Goddess Mariamman", location="Tiruppur, Tamil Nadu", state="Tamil Nadu", glyph="म", tier="regional", famousFor="Tiruppur Amman · summer festival search", summary="Mariamman — city Amman temple with intense summer festival.", mythology="Fire-walk and lime-pot rituals for health vows; defines Tiruppur Shakta calendar.", lat=11.115, lng=77.345, mapQuery="Mariamman Temple Tiruppur", nearestRail="Tiruppur", nearestAirport="Coimbatore", deityFamilies=["devi"]),
    # —— Jhansi ——
    T(city="Jhansi", slug="durga-mandir-jhansi", name="Durga Mandir, Jhansi", deity="Goddess Durga", location="Jhansi, Uttar Pradesh", state="Uttar Pradesh", glyph="द", tier="regional", famousFor="Jhansi Devi · Bundelkhand search", summary="Durga Mandir — active Devi shrine in Jhansi city.", mythology="Navaratri and Durga Puja for Bundelkhand families; near Rani Mahal heritage quarter.", lat=25.450, lng=78.570, mapQuery="Durga Mandir Jhansi", nearestRail="Jhansi Junction", nearestAirport="Gwalior / Khajuraho", deityFamilies=["devi"]),
    T(city="Jhansi", slug="shiva-mandir-jhansi-nagar", name="Nagar Shiva Mandir, Jhansi", deity="Lord Shiva", location="Jhansi, Uttar Pradesh", state="Uttar Pradesh", glyph="श", tier="regional", famousFor="Jhansi Shiva · Monday search", summary="Nagar Shiva Mandir — urban linga shrine of Jhansi.", mythology="Monday abhishek rhythm for cantonment and city devotees.", lat=25.448, lng=78.575, mapQuery="Shiva Mandir Jhansi", nearestRail="Jhansi Junction", nearestAirport="Gwalior", deityFamilies=["shiva"]),
    T(city="Jhansi", slug="hanuman-mandir-jhansi", name="Hanuman Mandir, Jhansi", deity="Lord Hanuman", location="Jhansi, Uttar Pradesh", state="Uttar Pradesh", glyph="ह", tier="regional", famousFor="Jhansi Hanuman · Tuesday search", summary="Hanuman Mandir — popular Tuesday shrine in Jhansi.", mythology="Hanuman as sankat-mochan for Bundelkhand soldiers and traders.", lat=25.452, lng=78.568, mapQuery="Hanuman Mandir Jhansi", nearestRail="Jhansi Junction", nearestAirport="Gwalior", deityFamilies=["hanuman"]),
    # —— Agra (real Agra temples) ——
    T(city="Agra", slug="mankameshwar-agra", name="Mankameshwar Mahadev Temple, Agra", deity="Lord Shiva (Mankameshwar)", location="Agra, Uttar Pradesh", state="Uttar Pradesh", glyph="म", tier="famous", famousFor="Agra’s ancient Shiva · near Agra Fort search", summary="Mankameshwar — historic Shiva temple near Agra Fort and Jama Masjid quarter.", mythology="Wish-fulfilling Shiva of Mughal-era Agra; Shravan and Shivaratri draw Braj–Doab pilgrims who pair with Taj visits.", lat=27.180, lng=78.020, mapQuery="Mankameshwar Temple Agra", nearestRail="Agra Cantt", nearestAirport="Agra / Delhi", deityFamilies=["shiva"]),
    T(city="Agra", slug="balkeshwar-mahadev-agra", name="Balkeshwar Mahadev Temple, Agra", deity="Lord Shiva (Balkeshwar)", location="Agra, Uttar Pradesh", state="Uttar Pradesh", glyph="ब", tier="regional", famousFor="Yamuna-bank Shiva · Agra local search", summary="Balkeshwar Mahadev — Yamuna-side Shiva shrine of Agra.", mythology="River-bank Shaiva seat for Agra families; Monday and Shravan define local calendar.", lat=27.200, lng=78.010, mapQuery="Balkeshwar Mahadev Temple Agra", nearestRail="Agra Fort", nearestAirport="Agra", deityFamilies=["shiva"]),
    T(city="Agra", slug="kailash-mandir-agra", name="Kailash Temple, Agra", deity="Lord Shiva (Kailash)", location="Agra, Uttar Pradesh", state="Uttar Pradesh", glyph="क", tier="regional", famousFor="Agra Kailash Shiva · city search", summary="Kailash Mandir — active Shiva temple in Agra’s residential sacred map.", mythology="Kailasa memory in a Taj-city; Shivaratri lamp offerings from local merchants.", lat=27.190, lng=78.030, mapQuery="Kailash Temple Agra", nearestRail="Agra Cantt", nearestAirport="Agra", deityFamilies=["shiva"]),
    # —— Top-ups (cities with 1–2 existing) ——
    T(city="Ajmer", slug="bajrangbali-ajmer", name="Bajrangbali Mandir, Ajmer", deity="Lord Hanuman (Bajrangbali)", location="Ajmer, Rajasthan", state="Rajasthan", glyph="ब", tier="regional", famousFor="Ajmer Hanuman · Tuesday search", summary="Bajrangbali Mandir — busy Hanuman shrine in Ajmer city.", mythology="Tuesday queues for Rajasthani families who combine with Ana Sagar and dargah-area walks.", lat=26.450, lng=74.640, mapQuery="Bajrangbali Temple Ajmer", nearestRail="Ajmer Junction", nearestAirport="Jaipur / Kishangarh", deityFamilies=["hanuman"]),
    T(city="Bikaner", slug="laxminath-bikaner", name="Laxminath Temple, Bikaner", deity="Lord Vishnu (Laxminath) & Goddess Lakshmi", location="Bikaner, Rajasthan", state="Rajasthan", glyph="ल", tier="famous", famousFor="Bikaner fort-adjacent Vishnu · city search", summary="Laxminath — premier Vaishnava temple inside Bikaner’s old city near Junagarh.", mythology="Lakshmi–Narayana patron of Bikaner royals; Janmashtami and Diwali draw Marwar pilgrims.", lat=28.020, lng=73.310, mapQuery="Laxminath Temple Bikaner", nearestRail="Bikaner Junction", nearestAirport="Jodhpur / Bikaner", deityFamilies=["vishnu", "lakshmi"]),
    T(city="Bikaner", slug="shiv-bari-bikaner", name="Shiv Bari Temple, Bikaner", deity="Lord Shiva (Shiv Bari)", location="Bikaner, Rajasthan", state="Rajasthan", glyph="श", tier="regional", famousFor="Cenotaph Shiva · Bikaner search", summary="Shiv Bari — domed Shiva temple built by Maharaja Doongar Singh.", mythology="Marble Nandi and linga in a garden setting; Monday abhishek for Bikaner families after Karni Mata yatra.", lat=28.030, lng=73.320, mapQuery="Shiv Bari Temple Bikaner", nearestRail="Bikaner Junction", nearestAirport="Jodhpur", deityFamilies=["shiva"]),
    T(city="Chandigarh", slug="iskcon-chandigarh", name="ISKCON Temple, Chandigarh", deity="Krishna–Radha (ISKCON)", location="Chandigarh", state="Chandigarh", glyph="इ", tier="regional", famousFor="Chandigarh ISKCON · NCR-family search", summary="ISKCON Chandigarh — Krishna temple serving the planned city and Mohali belt.", mythology="Sunday feast and Janmashtami for Punjab–Haryana IT and government families.", lat=30.740, lng=76.780, mapQuery="ISKCON Temple Chandigarh", nearestRail="Chandigarh", nearestAirport="Chandigarh", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    T(city="Chandigarh", slug="kali-mandir-chandigarh", name="Kali Bari Mandir, Chandigarh", deity="Goddess Kali", location="Sector 47, Chandigarh", state="Chandigarh", glyph="का", tier="regional", famousFor="Chandigarh Kali Bari · Bengali–Punjabi Shakta search", summary="Kali Bari — Kali temple serving Chandigarh’s Bengali and wider Shakta community.", mythology="Kali Puja and Navaratri transform Sector 47 into a festival quarter.", lat=30.690, lng=76.770, mapQuery="Kali Bari Mandir Chandigarh", nearestRail="Chandigarh", nearestAirport="Chandigarh", deityFamilies=["kali", "devi"]),
    T(city="Cuttack", slug="dhabaleswar-cuttack", name="Dhabaleswar Temple, Cuttack", deity="Lord Shiva (Dhabaleswar)", location="Dhabaleswar Island, Cuttack, Odisha", state="Odisha", glyph="ध", tier="famous", famousFor="Suspension-bridge Shiva · Cuttack essential search", summary="Dhabaleswar — island Shiva temple reached by bridge over the Mahanadi.", mythology="Shivaratri and Kartik fair draw Cuttack’s signature river-island darshan.", lat=20.480, lng=85.880, mapQuery="Dhabaleswar Temple Cuttack", nearestRail="Cuttack", nearestAirport="Bhubaneswar", deityFamilies=["shiva"]),
    T(city="Cuttack", slug="gadagadia-ghata-cuttack", name="Gadagadia Ghata Temples, Cuttack", deity="Lord Shiva & river deities", location="Gadagadia Ghata, Cuttack, Odisha", state="Odisha", glyph="ग", tier="regional", famousFor="Mahanadi ghat Shiva · Cuttack search", summary="Gadagadia Ghata — sacred river-bank temple cluster of Old Cuttack.", mythology="Boita Bandana and Kartik bathers combine with ghat-side Shiva arati.", lat=20.460, lng=85.880, mapQuery="Gadagadia Ghata Cuttack", nearestRail="Cuttack Junction", nearestAirport="Bhubaneswar", deityFamilies=["shiva"]),
    T(city="Bhubaneswar", slug="mukteshwar-bhubaneswar", name="Mukteshwar Temple, Bhubaneswar", deity="Lord Shiva (Mukteshwar)", location="Bhubaneswar, Odisha", state="Odisha", glyph="मु", tier="famous", famousFor="Torana gateway marvel · Bhubaneswar heritage search", summary="Mukteshwar — 10th-century gem with ornate torana in Bhubaneswar temple city.", mythology="‘Gem of Odisha sculpture’ still receives living Shiva puja; pairs with Lingaraj on ekadashi walks.", lat=20.240, lng=85.840, mapQuery="Mukteshwar Temple Bhubaneswar", nearestRail="Bhubaneswar", nearestAirport="Bhubaneswar", deityFamilies=["shiva"]),
    T(city="Bhubaneswar", slug="rajarani-bhubaneswar", name="Rajarani Temple, Bhubaneswar", deity="Lord Shiva (Rajarani — no presiding deity, heritage Shiva seat)", location="Bhubaneswar, Odisha", state="Odisha", glyph="र", tier="famous", famousFor="Sandstone love-sculpture temple · Bhubaneswar search", summary="Rajarani — ornate 11th-century temple named for red-gold sandstone.", mythology="Though deity absent today, festival puja and classical music concerts keep Rajarani a living culture tirtha.", lat=20.250, lng=85.850, mapQuery="Rajarani Temple Bhubaneswar", nearestRail="Bhubaneswar", nearestAirport="Bhubaneswar", deityFamilies=["shiva"]),
    T(city="Thrissur", slug="vadakkumnathan-thrissur", name="Vadakkumnathan Temple, Thrissur", deity="Lord Shiva (Vadakkumnathan)", location="Thrissur, Kerala", state="Kerala", glyph="व", tier="famous", famousFor="Pooram ground Shiva · Thrissur essential search", summary="Vadakkumnathan — ancient Shiva temple whose maidan hosts Thrissur Pooram.", mythology="Shiva as northern lord of the city; Pooram fireworks and elephant pageantry radiate from this kshetram.", lat=10.527, lng=76.215, mapQuery="Vadakkumnathan Temple Thrissur", nearestRail="Thrissur", nearestAirport="Kochi", deityFamilies=["shiva"], festivals=["Thrissur Pooram"]),
    T(city="Thrissur", slug="thiruvambady-krishna-thrissur", name="Thiruvambady Sri Krishna Temple, Thrissur", deity="Lord Krishna", location="Thrissur, Kerala", state="Kerala", glyph="थ", tier="famous", famousFor="Pooram participant temple · Thrissur Krishna search", summary="Thiruvambady Krishna — Pooram’s southern elephant party anchor.", mythology="Krishna worship intertwined with Pooram rivalry and pageantry; among Kerala’s most photographed festival temples.", lat=10.520, lng=76.210, mapQuery="Thiruvambady Krishna Temple Thrissur", nearestRail="Thrissur", nearestAirport="Kochi", deityFamilies=["krishna", "vishnu"], festivals=["Thrissur Pooram"]),
    T(city="Thrissur", slug="paramekkavu-bhagavathy-thrissur", name="Paramekkavu Bhagavathy Temple, Thrissur", deity="Goddess Bhagavathy (Devi)", location="Thrissur, Kerala", state="Kerala", glyph="प", tier="famous", famousFor="Pooram northern party Devi · Thrissur search", summary="Paramekkavu Bhagavathy — Devi temple leading Pooram’s northern elephant line.", mythology="Devi as warlike mother in Pooram memory; festival season defines Thrissur civic identity.", lat=10.525, lng=76.220, mapQuery="Paramekkavu Bhagavathy Temple Thrissur", nearestRail="Thrissur", nearestAirport="Kochi", deityFamilies=["devi"], festivals=["Thrissur Pooram"]),
    T(city="Trichy", slug="rockfort-uchhi-pillayar-trichy", name="Ucchi Pillayar Temple (Rockfort), Tiruchirappalli", deity="Lord Ganesha (Ucchi Pillayar) & Rockfort Shiva", location="Rockfort, Tiruchirappalli, Tamil Nadu", state="Tamil Nadu", glyph="उ", tier="famous", famousFor="Rockfort climb Ganesha · Trichy landmark search", summary="Rockfort Ucchi Pillayar — hilltop Ganesha with fort Shiva above Trichy.", mythology="Ganesha atop the 83m rock; Vinayaka Chaturthi climbers and Srirangam yatri combine fort darshan.", lat=10.828, lng=78.697, mapQuery="Rockfort Ucchi Pillayar Temple Trichy", nearestRail="Tiruchirappalli Junction", nearestAirport="Tiruchirappalli", deityFamilies=["ganesha", "shiva"]),
    T(city="Trichy", slug="samayapuram-mariamman-trichy", name="Samayapuram Mariamman Temple", deity="Goddess Mariamman", location="Samayapuram, Tiruchirappalli, Tamil Nadu", state="Tamil Nadu", glyph="स", tier="famous", famousFor="Tamil Nadu Amman mega-tirtha · Trichy search", summary="Samayapuram Mariamman — among Tamil Nadu’s most visited Amman temples.", mythology="Pongal and Thai month see walking pilgrims from across the state; lemon and salt offerings mark vow culture.", lat=10.920, lng=78.750, mapQuery="Samayapuram Mariamman Temple", nearestRail="Tiruchirappalli", nearestAirport="Trichy", deityFamilies=["devi"]),
    T(city="Thanjavur", slug="bangaru-kamakshi-thanjavur", name="Bangaru Kamakshi Temple, Thanjavur", deity="Goddess Kamakshi (Bangaru)", location="Thanjavur, Tamil Nadu", state="Tamil Nadu", glyph="ब", tier="regional", famousFor="Thanjavur Kamakshi · near Brihadeeswarar search", summary="Bangaru Kamakshi — golden-named Devi shrine in Thanjavur old town.", mythology="Complements Brihadeeswarar on Chola capital yatra; Navaratri for Thanjavur silk and art families.", lat=10.785, lng=79.135, mapQuery="Bangaru Kamakshi Temple Thanjavur", nearestRail="Thanjavur Junction", nearestAirport="Tiruchirappalli", deityFamilies=["devi"]),
    T(city="Thanjavur", slug="abhirami-amman-thanjavur", name="Abhirami Amman Temple, Thanjavur", deity="Goddess Abhirami (Parvati)", location="Thanjavur, Tamil Nadu", state="Tamil Nadu", glyph="अ", tier="regional", famousFor="Abhirami bhakti lore · Thanjavur Devi search", summary="Abhirami Amman — Devi temple linked with Abhirami Bhattar tradition.", mythology="Tamil Shakta poetry memory; full-moon worship and Navaratri in the Brihadeeswarar quarter.", lat=10.790, lng=79.140, mapQuery="Abhirami Amman Temple Thanjavur", nearestRail="Thanjavur", nearestAirport="Trichy", deityFamilies=["devi"]),
    T(city="Kanchipuram", slug="varadaraja-kanchipuram", name="Varadaraja Perumal Temple, Kanchipuram", deity="Lord Vishnu (Varadaraja)", location="Kanchipuram, Tamil Nadu", state="Tamil Nadu", glyph="व", tier="famous", famousFor="Divya Desam elephant laddu · Kanchi Vaishnava search", summary="Varadaraja Perumal — major Vishnu temple of Kanchipuram with famous laddu prasadam.", mythology="Among 108 Divya Desams; Vaikunta Ekadashi and Garuda seva define Kanchi’s Vaishnava half.", lat=12.820, lng=79.715, mapQuery="Varadaraja Temple Kanchipuram", nearestRail="Kanchipuram", nearestAirport="Chennai", deityFamilies=["vishnu"]),
    T(city="Jaipur", slug="birla-mandir-jaipur", name="Birla Mandir (Lakshmi Narayan), Jaipur", deity="Lakshmi–Narayan (Vishnu)", location="Motilal Atal Road, Jaipur, Rajasthan", state="Rajasthan", glyph="बि", tier="famous", famousFor="White marble Jaipur Birla · city landmark search", summary="Birla Mandir Jaipur — white marble Lakshmi Narayan on the city ridge.", mythology="Modern marble campus with epics in relief; Diwali and Janmashtami draw Pink City families after Govind Dev darshan.", lat=26.890, lng=75.820, mapQuery="Birla Mandir Jaipur", nearestRail="Jaipur Junction", nearestAirport="Jaipur", deityFamilies=["vishnu", "lakshmi"], tags_extra=["modern-temples"]),
    T(city="Hisar", slug="shiv-mandir-hisar", name="Shiva Mandir, Hisar", deity="Lord Shiva", location="Hisar, Haryana", state="Haryana", glyph="श", tier="regional", famousFor="Hisar city Shiva · Monday search", summary="Shiva Mandir — active urban linga shrine of Hisar.", mythology="Monday abhishek for Haryana agricultural-belt families after Agroha and Banbhori yatra.", lat=29.150, lng=75.720, mapQuery="Shiva Mandir Hisar", nearestRail="Hisar Junction", nearestAirport="Delhi / Chandigarh", deityFamilies=["shiva"]),
    T(city="Shimla", slug="kali-bari-shimla", name="Kali Bari Temple, Shimla", deity="Goddess Kali (Shyamala)", location="Shimla, Himachal Pradesh", state="Himachal Pradesh", glyph="का", tier="famous", famousFor="Shimla namesake Devi · Mall Road search", summary="Kali Bari — Kali temple linked with Shimla’s name (Shyamala) memory.", mythology="Devotees climb from the Mall; Navaratri and Kali Puja in the hill capital.", lat=31.105, lng=77.175, mapQuery="Kali Bari Temple Shimla", nearestRail="Shimla / Kalka", nearestAirport="Shimla / Chandigarh", deityFamilies=["kali", "devi"]),
    T(city="Shimla", slug="tara-devi-shimla", name="Tara Devi Temple, Shimla", deity="Goddess Tara Devi", location="Tara Devi Hill, Shimla, Himachal Pradesh", state="Himachal Pradesh", glyph="त", tier="famous", famousFor="Ridge-top Devi · Shimla panorama search", summary="Tara Devi — hill Goddess temple overlooking Shimla and the valleys.", mythology="Full-moon and Navaratri climbs; pairs with Jakhoo Hanuman on ridge yatra loops.", lat=31.050, lng=77.120, mapQuery="Tara Devi Temple Shimla", nearestRail="Shimla", nearestAirport="Shimla", deityFamilies=["devi"]),
    T(city="Udupi", slug="anantheshwara-udupi", name="Anantheshwara Temple, Udupi", deity="Lord Shiva (Anantheshwara)", location="Udupi, Karnataka", state="Karnataka", glyph="अ", tier="famous", famousFor="Udupi Krishna’s Shiva anchor · Chandramouleshwara pair search", summary="Anantheshwara — ancient Shiva temple beside Krishna Matha in Udupi.", mythology="Madhwacharya tradition places Krishna worship in Shiva’s sanctum context; essential first stop on Udupi parikrama.", lat=13.340, lng=74.750, mapQuery="Anantheshwara Temple Udupi", nearestRail="Udupi", nearestAirport="Mangaluru", deityFamilies=["shiva"]),
    T(city="Udupi", slug="chandramouleshwara-udupi", name="Chandramouleshwara Temple, Udupi", deity="Lord Shiva (Chandramouleshwara)", location="Udupi, Karnataka", state="Karnataka", glyph="च", tier="famous", famousFor="Twin Shiva of Udupi · Krishna Matha circuit search", summary="Chandramouleshwara — Shiva with crescent crown beside Anantheshwara in Udupi.", mythology="Paired Shaiva seats before Krishna darshan; Monday abhishek on the parikrama route.", lat=13.341, lng=74.751, mapQuery="Chandramouleshwara Temple Udupi", nearestRail="Udupi", nearestAirport="Mangaluru", deityFamilies=["shiva"]),
    T(city="Ayodhya", slug="hanuman-garhi-ayodhya", name="Hanuman Garhi, Ayodhya", deity="Lord Hanuman", location="Ayodhya, Uttar Pradesh", state="Uttar Pradesh", glyph="ह", tier="famous", famousFor="Fort Hanuman · Ayodhya essential search", summary="Hanuman Garhi — hilltop Hanuman fort temple guarding Ayodhya.", mythology="Child Hanuman in lap of Mata Anjani iconography; Tuesday and Saturday define Ayodhya’s Hanuman bhakti before Ram Janmabhoomi darshan.", lat=26.795, lng=82.210, mapQuery="Hanuman Garhi Ayodhya", nearestRail="Ayodhya Junction", nearestAirport="Lucknow / Ayodhya", deityFamilies=["hanuman", "rama"]),
    T(city="Ayodhya", slug="nageshwarnath-ayodhya", name="Nageshwarnath Temple, Ayodhya", deity="Lord Shiva (Nageshwarnath)", location="Ayodhya, Uttar Pradesh", state="Uttar Pradesh", glyph="न", tier="regional", famousFor="Kush-era Shiva lore · Ayodhya search", summary="Nageshwarnath — ancient Shiva temple linked with Kush in Ramayana memory.", mythology="Legend attributes founding to Rama’s son Kush; Shivaratri on Ramayana trail after Saryu ghats.", lat=26.800, lng=82.205, mapQuery="Nageshwarnath Temple Ayodhya", nearestRail="Ayodhya Junction", nearestAirport="Ayodhya", deityFamilies=["shiva", "rama"]),
    T(city="Puducherry", slug="sri-gokilambal-thirukameshwar", name="Sri Gokilambal Thirukameshwar Temple, Villianur", deity="Lord Shiva (Thirukameshwar) & Gokilambal", location="Villianur, Puducherry", state="Puducherry", glyph="गो", tier="regional", famousFor="Car festival · Puducherry Shiva search", summary="Thirukameshwar Villianur — Shiva temple famous for annual chariot festival.", mythology="Tamil Shaiva culture in French-era Puducherry; car festival draws Pondicherry–Tamil Nadu border pilgrims.", lat=11.890, lng=79.740, mapQuery="Thirukameshwar Temple Villianur", nearestRail="Puducherry", nearestAirport="Chennai", deityFamilies=["shiva"]),
    T(city="Sangli", slug="ganapati-temple-sangli", name="Ganpati Temple, Sangli", deity="Lord Ganesha", location="Sangli, Maharashtra", state="Maharashtra", glyph="ग", tier="regional", famousFor="Sangli Ganesh · Ganesh Chaturthi search", summary="Ganpati Mandir — central Ganesh shrine of Sangli city.", mythology="Ganesh Chaturthi and Angarki Chaturthi for Krishna–Sangli sugar-belt families.", lat=16.860, lng=74.570, mapQuery="Ganpati Temple Sangli", nearestRail="Sangli", nearestAirport="Kolhapur / Pune", deityFamilies=["ganesha"]),
    T(city="Panipat", slug="shiva-mandir-panipat", name="Shiva Mandir, Panipat", deity="Lord Shiva", location="Panipat, Haryana", state="Haryana", glyph="श", tier="regional", famousFor="Panipat Shiva · Shravan search", summary="Shiva Mandir — active linga shrine in Panipat.", mythology="Monday abhishek for Haryana industrial-town devotees after Devi darshan.", lat=29.390, lng=76.970, mapQuery="Shiva Mandir Panipat", nearestRail="Panipat Junction", nearestAirport="Delhi", deityFamilies=["shiva"]),
    T(city="Panipat", slug="devi-temple-panipat", name="Devi Temple, Panipat", deity="Goddess Devi", location="Panipat, Haryana", state="Haryana", glyph="द", tier="regional", famousFor="Panipat Devi · Navaratri search", summary="Devi Mandir — Shakta shrine complementing Panipat’s historic battlefield town.", mythology="Navaratri and Mundan vows for Haryana families.", lat=29.385, lng=76.965, mapQuery="Devi Temple Panipat", nearestRail="Panipat Junction", nearestAirport="Delhi", deityFamilies=["devi"]),
    T(city="Muzaffarpur", slug="chandi-mata-muzaffarpur", name="Chandi Mata Temple, Muzaffarpur", deity="Goddess Chandi", location="Muzaffarpur, Bihar", state="Bihar", glyph="च", tier="regional", famousFor="Muzaffarpur Devi · Chhath-season search", summary="Chandi Mata — prominent Devi shrine of Muzaffarpur.", mythology="Navaratri and Chhath-season vows for litchi-belt families.", lat=26.120, lng=85.380, mapQuery="Chandi Mata Temple Muzaffarpur", nearestRail="Muzaffarpur Junction", nearestAirport="Patna / Darbhanga", deityFamilies=["devi"]),
    T(city="Muzaffarpur", slug="shiva-mandir-muzaffarpur", name="Shiva Mandir, Muzaffarpur", deity="Lord Shiva", location="Muzaffarpur, Bihar", state="Bihar", glyph="श", tier="regional", famousFor="Muzaffarpur Shiva · Monday search", summary="Shiva Mandir — urban linga shrine of Muzaffarpur.", mythology="Shravan Monday abhishek for North Bihar devotees.", lat=26.125, lng=85.385, mapQuery="Shiva Mandir Muzaffarpur", nearestRail="Muzaffarpur Junction", nearestAirport="Patna", deityFamilies=["shiva"]),
    T(city="Patiala", slug="mahamaya-bagh-patiala", name="Mahamaya Rajrajeshwari Temple, Patiala", deity="Goddess Rajrajeshwari (Mahamaya)", location="Patiala, Punjab", state="Punjab", glyph="म", tier="regional", famousFor="Patiala Devi · Navaratri search", summary="Mahamaya Bagh temple — Devi shrine in Patiala’s garden quarter.", mythology="Navaratri and Patiala royal-city heritage walks combine with Kali Mata darshan.", lat=30.340, lng=76.390, mapQuery="Mahamaya Temple Patiala", nearestRail="Patiala", nearestAirport="Chandigarh", deityFamilies=["devi"]),
    T(city="Patiala", slug="shiv-mandir-patiala", name="Shiva Mandir, Patiala", deity="Lord Shiva", location="Patiala, Punjab", state="Punjab", glyph="श", tier="regional", famousFor="Patiala Shiva · Shivaratri search", summary="Shiva Mandir — active linga shrine in Patiala.", mythology="Shivaratri for Punjabi families after Kali Mata visit.", lat=30.335, lng=76.385, mapQuery="Shiva Mandir Patiala", nearestRail="Patiala", nearestAirport="Chandigarh", deityFamilies=["shiva"]),
    T(city="Shillong", slug="kamakhya-shillong", name="Kamakhya Temple, Shillong", deity="Goddess Kamakhya (regional seat)", location="Shillong, Meghalaya", state="Meghalaya", glyph="क", tier="regional", famousFor="Shillong Shakta · Northeast search", summary="Kamakhya Mandir Shillong — Shakta shrine for Shillong’s Hindu community.", mythology="Assamese–Bengali Shakta culture transplanted to the hill capital; Ambubachi memory and Navaratri arati.", lat=25.570, lng=91.890, mapQuery="Kamakhya Temple Shillong", nearestRail="Guwahati", nearestAirport="Shillong / Guwahati", deityFamilies=["devi"]),
    T(city="Shillong", slug="bishen-narayan-shillong", name="Bishen Narayan Temple, Shillong", deity="Lord Vishnu (Bishen Narayan)", location="Shillong, Meghalaya", state="Meghalaya", glyph="ब", tier="regional", famousFor="Shillong Vaishnava · local search", summary="Bishen Narayan — Vishnu temple serving Shillong’s Hindu residents.", mythology="Janmashtami and Ekadashi for Northeast urban Vaishnava families.", lat=25.575, lng=91.885, mapQuery="Bishen Narayan Temple Shillong", nearestRail="Guwahati", nearestAirport="Shillong", deityFamilies=["vishnu"]),
    T(city="Imphal", slug="sanamahi-kongsang", name="Sanamahi Temple, Kongba", deity="Sanamahi (indigenous Meitei deity — Hindu-adjacent living tradition)", location="Imphal, Manipur", state="Manipur", glyph="स", tier="regional", famousFor="Meitei Sanamahi · Imphal search", summary="Sanamahi temple — sacred seat of indigenous Meitei tradition often visited alongside Govindajee.", mythology="Sanamahi as eternal guardian in Meitei cosmology; Cheiraoba and regional festivals maintain living worship.", lat=24.820, lng=93.950, mapQuery="Sanamahi Temple Imphal", nearestRail="Dimapur", nearestAirport="Imphal", deityFamilies=["devi"]),
    T(city="Imphal", slug="iskcon-imphal", name="ISKCON Temple, Imphal", deity="Krishna–Radha (ISKCON)", location="Imphal, Manipur", state="Manipur", glyph="इ", tier="regional", famousFor="Imphal Krishna · Northeast ISKCON search", summary="ISKCON Imphal — Krishna temple complementing Shree Govindajee Vaishnava heritage.", mythology="Gaudiya kirtan in the Manipur valley; Janmashtami draws Vaishnava families from the hill state.", lat=24.815, lng=93.945, mapQuery="ISKCON Temple Imphal", nearestRail="Dimapur", nearestAirport="Imphal", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    T(city="Kakinada", slug="sri-lakshmi-narasimha-kakinada", name="Lakshmi Narasimha Swamy Temple, Antarvedi", deity="Lord Narasimha & Lakshmi", location="Antarvedi, East Godavari (near Kakinada), Andhra Pradesh", state="Andhra Pradesh", glyph="न", tier="famous", famousFor="Godavari mouth Narasimha · Kakinada circuit search", summary="Antarvedi Narasimha — river-mouth Narasimha kshetram on Kakinada yatra.", mythology="Confluence of Godavari and sea; Narasimha Jayanti and boat darshan define coastal Andhra pilgrimage.", lat=16.330, lng=81.720, mapQuery="Antarvedi Narasimha Temple", nearestRail="Kakinada / Narasapur", nearestAirport="Rajahmundry", deityFamilies=["narasimha", "vishnu", "lakshmi"]),
]


def expand_detail(short_en: str, short_hi: str, hook: str, hook_hi: str, why: str, why_hi: str, takeaway: str, title: str, title_hi: str) -> tuple[str, str]:
    detail_en = (
        f"{short_en}\n\n"
        f"Elders at home often begin with the line: {hook} "
        f"The middle of the telling is where doubt and devotion meet — not to prove history like a court, "
        f"but to shape tomorrow's patience.\n\n"
        f"{short_en.split('.')[0] if short_en else title}. "
        f"Children ask why the shrine still matters; the answer is in the queue, the prasadam, the thread tied after a vow kept. "
        f"Regional tellings add names and dates that differ; receive cousin versions with respect.\n\n"
        f"What practice remembers: {why} "
        f"{takeaway}\n\n"
        f"This TirthaYatra retelling draws on widely cited sthala-purana and pilgrimage memory — "
        f"not a verbatim scripture quote, not affiliated with any temple trust."
    )
    detail_hi = (
        f"{short_hi}\n\n"
        f"घर में अक्सर इस पंक्ति से शुरुआत: {hook_hi} "
        f"कथा का मध्य वहाँ है जहाँ संशय और श्रद्धा मिलते हैं — अदालत सबूत नहीं, कल का धैर्य।\n\n"
        f"{short_hi.split('।')[0] if short_hi else title_hi}। "
        f"बच्चे पूछते हैं मंदिर आज क्यों; जवाब कतार, प्रसाद, मन्नत की डोर में है। "
        f"क्षेत्रीय कथाएँ भिन्न नाम देती हैं — सम्मान से सुनो।\n\n"
        f"रीति क्या याद रखती है: {why_hi} "
        f"{takeaway}\n\n"
        f"यह TirthaYatra की मूल पुनर्लेखन है — व्यापक तीर्थ-परंपरा स्मृति पर; शब्दशः शास्त्र नहीं।"
    )
    return detail_en, detail_hi


def build_stories() -> list[dict]:
    raw = [
        dict(slug="alakhnath-bareilly", title="Alakhnath and the Nath yogis of Bareilly", titleHi="अलकhnath और बरेली के नाथ योगी", deity="shiva",
             hook="A math on the Gangetic plain where Shiva and breath share one discipline.", hookHi="गंगा-मैदान पर math जहाँ शिव और प्राण एक अनुशासन हैं।",
             whyRitual="Shravan Monday abhishek at Alakhnath remembers Nath-Shaiva tapasya.", whyRitualHi="श्रavan सोमvar अभिषेक नाथ-शैव tapasya की स्मृति।",
             storyEn="Bareilly's Alakhnath temple grew from the Nath panth's wandering discipline into a city-defining Shiva seat. Gorakhnath's stream of yogis taught that the body itself could be a tirtha if breath and mantra aligned. The math's Shiva linga became Rohilkhand's anchor for Monday vows, Shivaratri lamps, and families seeking steadiness before life's crossings.",
             storyHi="बareilly का अलकhnath नाथ panth की wandering discipline से नगर-निर्धारक शिव tirtha बना। Gorakhnath की parampara ने शरीर को tirtha माना यदि प्राण और mantra मिलें। math का linga Rohilkhand के सोमvar, शिवरात्रि और जीवन-संक्रमण vows का anchor रहा।",
             takeaway="Before Monday abhishek, sit in silence one minute — Nath teaching begins in breath, not hurry.", relatedTemples=["alakhnath-bareilly", "trivati-nath-bareilly"]),
        dict(slug="siddheshwar-solapur", title="Siddheshwar and the tank that holds a city", titleHi="सिद्धेश्वर और tank जो नगर धारण करता है", deity="shiva",
             hook="A swayambhu linga beside still water — and Solapur gathers.", hookHi="still water के पास swayambhu linga — और Solapur इकट्ठा होता है।",
             whyRitual="Makar Sankranti fair at Siddheshwar tank marks harvest gratitude.", whyRitualHi="Makar Sankranti mela harvest gratitude की चिह्न।",
             storyEn="Solapur without Siddheshwar is hard to imagine. The linga rose beside the tank in local memory as self-manifest — not installed by kings alone but discovered by devotion. Makar Sankranti turns the water's edge into a temporary city of stalls, bhajan, and families who have returned for generations. Shiva here is not distant; He is the neighbour who receives milk, flowers, and whispered troubles every Monday.",
             storyHi="Siddheshwar के बिना Solapur कल्पना कठिन। tank के पास linga sthala memory में swayambhu उठा — केवल राज ne sthapna नहीं, bhakti ne khoj। Makar Sankranti pani ke kinare ko peedhi-dar-peedhi lautne wale parivar ka mela bana deta hai। Shiva yahan door nahi — har somvar doodh, phool aur fusfusate kasht lete hain।",
             takeaway="Offer one flower without a wish list — Siddheshwar teaches presence before bargaining.", relatedTemples=["siddheshwar-solapur"]),
        dict(slug="jalakandeswarar-vellore", title="Jalakandeswarar in the water-eyed fort", titleHi="जalakandeswarar — pani-nayan wale qile mein", deity="shiva",
             hook="Shiva whose eyes hold water — inside a Vijayanagara fort.", hookHi="Shiva jinki aankhon mein pani — Vijayanagara qile ke bhitar।",
             whyRitual="Fort Shiva darshan after moat parikrama on Shivaratri.", whyRitualHi="Shivaratri par moat parikrama ke baad fort Shiva darshan।",
             storyEn="Within Vellore Fort, Jalakandeswarar sits in sculpted stone that remembers a empire's pride and a God's calm. 'Jalakanta' — water in the eye — suggests Shiva who cooled cosmic fire in His throat now cools the devotee's restlessness. Pilgrims enter through fort gates where history books speak of battles; inside the mandapa, the story shifts to Pradosham bells and the patience of stone.",
             storyHi="Vellore qile mein Jalakandeswarar us sculpted patthar mein virajman hai jo samrajya ke garv aur Bhagwan ki shanti dono yaad dilata hai। 'Jalakanta' — aankh ka pani — woh Shiva jinhone kanth mein aag thandi ki, ab bhakt ki bechaini thandi karte hain। Qile ke darwazon se guzar kar mandapa mein katha Pradosham ki ghanti aur patthar ke dhairya par aa jati hai।",
             takeaway="Walk the fort slowly once — let architecture teach what haste forgets.", relatedTemples=["jalakandeswarar-vellore"]),
        dict(slug="sripuram-golden-temple", title="The star path to Lakshmi Narayani", titleHi="Lakshmi Narayani tak ka star path", deity="lakshmi",
             hook="Gold underfoot — but the walk asks for attention, not spectacle alone.", hookHi="Sone ka path — par chalne wale se dhyaan maangta hai, keval tamasha nahi।",
             whyRitual="Star-path parikrama before Narayani darshan trains slow gratitude.", whyRitualHi="Narayani darshan se pehle star-path parikrama dheere gratitude sikhati hai।",
             storyEn="Sripuram's Lakshmi Narayani temple asks devotees to walk a star-shaped path reading messages of compassion before reaching the golden sanctum. The gold cladding catches cameras, but elders say the real offering is the unhurried walk — each step a chance to loosen one grip on anxiety. Annadanam at the campus extends the Goddess's nourishment beyond the icon into shared meal.",
             storyHi="Sripuram ki Lakshmi Narayani mandir bhakton se star-path par chal kar karuna ke sandesh padhne ko kehti hai, phir golden garbhagriha। Sona camera khinchta hai, par buzurg kahte hain asli arpan bina jaldi ki chaal hai — har kadam ek chinta chhodne ka mauka। Annadanam campus par Devi ke poshan ko bhojan mein failata hai।",
             takeaway="Walk ten steps in silence at home — star path begins wherever you slow down.", relatedTemples=["sripuram-golden-temple"]),
        dict(slug="hasanamba-hassan", title="Hasanamba — the Goddess who opens once", titleHi="Hasanamba — woh Devi jo ek baar khulti hai", deity="devi",
             hook="Eleven months sealed — one week of darshan for a whole year’s longing.", hookHi="Gyarah mahine band — ek hafte ka darshan saal bhar ki lagan ke liye।",
             whyRitual="Deepavali-week opening is a lesson in patient longing.", whyRitualHi="Deepavali saptah ka khulna dhairya ki lagan sikhata hai।",
             storyEn="Hasanamba of Hassan is unlike most temples: for much of the year the sanctum stays closed, the Goddess 'smiling' only during Deepavali week when doors open and the district converges. The tradition teaches delayed gratification — devotion measured not in constant access but in the ache of waiting. When darshan finally arrives, the queue moves slowly because no one wants to waste a moment earned across months.",
             storyHi="Hassan ki Hasanamba adhiktar mandiron se alag: adhik samay garbhagriha band, Deepavali saptah mein 'muskurati' Devi jab zila ikattha hota hai। Parampara vilambit santosh sikhati hai — bhakti nirantar access mein nahi, intezar ke dard mein। Jab darshan aata hai, katar dheere chalti hai kyunki mahinon ki kamai pal barbaad nahi karni।",
             takeaway="Pick one desire and wait one week before acting — practice Hasanamba patience.", relatedTemples=["hasanamba-hassan"]),
        dict(slug="chottanikkara-devi", title="Chottanikkara — the Devi who walks with devotees", titleHi="Chottanikkara — Devi jo bhakton ke saath chalti hai", deity="devi",
             hook="Morning Saraswati, noon Lakshmi, evening Durga — one Goddess, three faces of care.", hookHi="Subah Saraswati, dopahar Lakshmi, shaam Durga — ek Devi, teen pehlu ki dekhbhal।",
             whyRitual="Guruthi pooja for mental peace remembers Devi's healing aspect.", whyRitualHi="Guruthi pooja man ki shanti ke liye Devi ke upchar ko yaad karti hai।",
             storyEn="Chottanikkara Bhagavathy near Kochi is beloved for a triple rhythm: worshippers understand the Devi as Saraswati at dawn, Mahalakshmi at noon, and Durga at dusk. Guruthi offerings address afflictions of the mind in a culture that speaks openly about spiritual healing. Festivals bring processions where the Goddess seems to walk among lanes — not frozen in stone alone but moving through community care.",
             storyHi="Kochi ke paas Chottanikkara Bhagavathy teen lay mein priya: subah Saraswati, dopahar Mahalakshmi, shaam Durga। Guruthi arpan man ke kasht par, jahan samuday mano-chikitsa khulkar bolta hai। Utsav mein juloos — Devi patthar mein frozen nahi, galiyon mein dekhbhal karke chalti hai।",
             takeaway="Name one fear aloud to a trusted person — Chottanikkara healing begins in honest speech.", relatedTemples=["chottanikkara-temple", "ernakulathappan-kochi"]),
        dict(slug="samaleswari-sambalpur", title="Samaleswari and the hunger of Western Odisha", titleHi="Samaleswari aur Paschim Odisha ki bhukh", deity="devi",
             hook="Before the first grain of Nuakhai, the Mother is fed.", hookHi="Nuakhai ka pehla anaaj se pehle, Ma ko bhojan।",
             whyRitual="Nuakhai begins with Samaleswari's offering — gratitude before eating.", whyRitualHi="Nuakhai Samaleswari arpan se — khane se pehle gratitude।",
             storyEn="Maa Samaleswari presides over Sambalpur as presiding Goddess of Western Odisha. Nuakhai — the new rice festival — does not begin in homes until Her share is offered at the temple. The ritual encodes agrarian ethics: no harvest pride before thanking the Mother who watched the fields through drought and rain. Navaratri nights fill the Mahanadi bank with lamp smoke and women's songs.",
             storyHi="Maa Samaleswari Paschim Odisha ki adhyaksha Devi, Sambalpur ki rakshika। Nuakhai ghar mein tab shuru jab mandir mein unka hissa chadh jaye। Riti kheti ki naitikta hai: Ma ko dhanyawad ke bina kshitij par garv nahi। Navaratri ki raat Mahanadi kinare diya aur geet se bhari।",
             takeaway="Before your next meal, offer the first spoon mentally to someone who fed you.", relatedTemples=["samaleswari-sambalpur"]),
        dict(slug="narasimha-jharni-bidar", title="Narasimha in the wading cave", titleHi="Narasimha — pani mein chal kar gufa tak", deity="narasimha",
             hook="You must wade through water to meet the man-lion.", hookHi="Man-lion se milne pani mein chalna padta hai।",
             whyRitual="Water-wading darshan remembers Narasimha appearing at threshold.", whyRitualHi="Pani se guzar kar darshan — Narasimha ka threshold par prakat hona।",
             storyEn="Bidar's Narasimha Jharni asks pilgrims to wade through a stream inside a cave before reaching the deity — body immersed before eyes meet the man-lion. The ritual mirrors Puranic memory: Narasimha appeared neither fully indoors nor outdoors, neither fully day nor night. Here, neither fully dry nor swimming — a threshold darshan. Devotees emerge with wet clothes and steady breath, having carried fear through water.",
             storyHi="Bidar ka Narasimha Jharni gufa ke andar dhara mein chal kar deity tak pahunchna chahta hai — aankhen milne se pehle sharir dooba। Riti Puranic smriti: Narasimha na andar na bahar, na din na raat। Yahan na sukha na tairna — threshold darshan। Bhakt geele kapde aur sthir saans ke saath nikalte hain, dar pani se guzar kar।",
             takeaway="Face one threshold task today — Jharni teaches courage is often wet and cold.", relatedTemples=["narasimha-jharni-bidar"]),
        dict(slug="cuttack-chandi", title="Cuttack Chandi on the Mahanadi", titleHi="Mahanadi par Cuttack Chandi", deity="devi",
             hook="The Goddess who named a city watches the river turn.", hookHi="Jis Devi ne shahar ka naam diya, woh nadi dekhti hai।",
             whyRitual="Durga Puja and Kali Puja at Chandi bind Cuttack's civic calendar.", whyRitualHi="Chandi par Durga-Kali Puja Cuttack ki nagar-riti bandhti hai।",
             storyEn="Cuttack Chandi Temple anchors Old Cuttack's identity — the Devi whose name the city carries in folk memory. Above the Mahanadi's bend, She receives Durga Puja crowds that spill from pandal to river ghat. Paired with Dhabaleswar island Shiva across the water, Cuttack's yatra teaches Shiva–Shakti balance in daily Odia life.",
             storyHi="Cuttack Chandi purane Cuttack ki pehchan — woh Devi jiska naam shahar mein। Mahanadi ke mod par Durga Puja ka samuday pani ke ghat tak failta hai। Paani ke us paar Dhabaleswar Shiva ke saath, Cuttack ki yatra Odia jeevan mein Shiva–Shakti santulan sikhati hai।",
             takeaway="Stand by water once this week — let river remind you movement is also prayer.", relatedTemples=["cuttack-chandi", "dhabaleswar-cuttack"]),
        dict(slug="takhteshwar-bhavnagar", title="Takhteshwar above the Gulf", titleHi="Khambhat ki khora par Takhteshwar", deity="shiva",
             hook="White marble Shiva watching ships cross the Gulf.", hookHi="Safed marble Shiva jahaj dekhte hue।",
             whyRitual="Hill climb before darshan — body effort offered to Shiva.", whyRitualHi="Darshan se pehle chadhna — sharir ka prayas Shiva ko arpan।",
             storyEn="Maharaja Takhtsinhji built this hilltop Shiva temple above Bhavnagar, where the Gulf of Khambhat meets Saurashtra's salt air. The climb is short but deliberate — each step a miniature pilgrimage. Monday abhishek mixes marble gleam with sea breeze; Shivaratri lamps appear like ships' lights on the horizon.",
             storyHi="Maharaja Takhtsinhji ne Bhavnagar ke upar yeh hilltop Shiva banwaya, jahan Khambhat ki khora aur Saurashtra ki namak hawa milti hai। Chadhna chhota par jaan-bujh kar — har kadam chhota tirtha। Somvar abhishek marble aur samudri hawa mein; Shivaratri ke diye kshitij par jahaj ki roshni jaise।",
             takeaway="Climb stairs slowly once today — offer the breath, not just the arrival.", relatedTemples=["takhteshwar-bhavnagar"]),
        dict(slug="rockfort-uchhi-pillayar", title="Ganesha on the rock above Trichy", titleHi="Trichy ke upar chattan par Ganesha", deity="ganesha",
             hook="Eighty-three metres up — Vinayaka before the view.", hookHi="Tirasi metre upar — drishya se pehle Vinayaka।",
             whyRitual="Climb Rockfort before Srirangam — Ganesha clears the path.", whyRitualHi="Srirangam se pehle Rockfort chadhna — Ganesha rasta saaf karta hai।",
             storyEn="Trichy's Rockfort holds Ucchi Pillayar — Ganesha at the summit where Pallava and Nayak fort walls remember centuries of rulers, yet the first queue is always for the elephant-faced God. Pilgrims climb breathless, remove shoes on hot stone, and whisper new beginnings. Below, the Cauvery plain spreads toward Srirangam; above, Ganesha listens.",
             storyHi="Trichy ka Rockfort Ucchi Pillayar rakhta hai — shikhar par Ganesha jahan Pallava-Nayak diwaron mein sadiyan, par pehli katar hamesha hathi-mukh wale Bhagwan ki। Bhakt saans phule chadhte hain, garam patthar par joota utaar kar nayi shuruaat fusfusate hain। Neeche Cauvery maidan Srirangam ki or; upar Ganesha sunta hai।",
             takeaway="Begin one hard task with 'Om Gam Ganapataye Namaha' — climb starts in the mind.", relatedTemples=["rockfort-uchhi-pillayar-trichy", "samayapuram-mariamman-trichy"]),
        dict(slug="augharnath-meerut", title="Augarnath and the cantonment Shiva", titleHi="Augarnath aur cantonment ka Shiva", deity="shiva",
             hook="A Shiva who watched soldiers march — and devotees still queue.", hookHi="Shiva jinhone sipahi dekhe — aur aaj bhi katar।",
             whyRitual="Shravan at Augarnath links freedom memory with Monday Shiva.", whyRitualHi="Augarnath par Shravan — swatantrata smriti aur somvar Shiva।",
             storyEn="Meerut's Augarnath Temple in the Kalipaltan quarter carries layered memory — Shaiva worship intertwined with 1857 uprising narratives locals honour without turning the shrine into a monument alone. Shiva remains approachable: milk on Mondays, bells on Shravan, families seeking steady ground in a city of armies and markets.",
             storyHi="Meerut ka Augarnath Kalipaltan mein parat dar par smriti rakhta hai — Shaiva pooja aur 1857 ki kathaon se juda, bina keval smarak banaye। Shiva sulabh: somvar doodh, shravan ghanti, fauj aur bazaar wale shahar mein sthir zameen dhoondhte parivar।",
             takeaway="Light one lamp for peace in your town — Augarnath remembers civic courage too.", relatedTemples=["augharnath-meerut"]),
        dict(slug="bala-hanuman-jamnagar", title="The unbroken Ram dhun of Jamnagar", titleHi="Jamnagar ki akhand Ram dhun", deity="hanuman",
             hook="Since 1964 — 'Shri Ram Jai Ram' without a gap.", hookHi="1964 se — 'Shri Ram Jai Ram' bina antar ke।",
             whyRitual="Listening beside the akhand dhun teaches patience and collective breath.", whyRitualHi="Akhand dhun ke paas baithna dhairya aur saanjha saans sikhata hai।",
             storyEn="Jamnagar's Bala Hanuman Temple on Lakhota Lake is famous worldwide for continuous chanting of 'Shri Ram Jai Ram Jai Jai Ram' — voices rotating day and night since 1964, recognised in record books yet meaningful first as local seva. Visitors sit on the lakeside steps not to break a record but to feel time soften. Hanuman here is not restless warrior alone but steady repeater of Rama's name.",
             storyHi="Jamnagar ka Bala Hanuman Lakhota tal par duniya bhar mein prasiddh — 'Shri Ram Jai Ram' 1964 se rat-din, record kitabon mein par pehle sthaniya seva। Log kinare baithte hain record todne nahi, samay dheela mahsus karne। Hanuman yahan keval bechain yodha nahi, Rama naam ke sthir japak।",
             takeaway="Chant Rama nama eleven times before sleep — small akhand begins at home.", relatedTemples=["bala-hanuman-jamnagar"]),
        dict(slug="vadakkumnathan-thrissur", title="Vadakkumnathan and the Pooram sky", titleHi="Vadakkumnathan aur Pooram ka aasman", deity="shiva",
             hook="Shiva who lends His ground for Kerala's loudest festival.", hookHi="Shiva jo apni bhoomi Kerala ke sabse tez utsav ko dete hain।",
             whyRitual="Pooram fireworks after Shiva's permission memory — celebration with restraint.", whyRitualHi="Pooram ke aatishbazi — utsav aur samman ka santulan।",
             storyEn="Vadakkumnathan — the northern lord Shiva of Thrissur — presides over a temple ground that becomes Kerala's most spectacular Pooram arena. Shiva does not ride an elephant here; He receives the festival's sound and colour as offering. The Devi temples of Thiruvambady and Paramekkavu parade in His witness — a civic theology where God holds space for community joy.",
             storyHi="Vadakkumnathan — Thrissur ke uttar disha ke Shiva — mandir ka maidan jahan Kerala ka sabse adbhut Pooram hota hai। Shiva yahan hathi par nahi; shor aur rang arpan sweekar karte hain। Thiruvambady aur Paramekkavu ki Devi juloos unki gawahi mein — samuday ke aanand ke liye Bhagwan jagah rakhte hain।",
             takeaway="Celebrate one local festival respectfully — Pooram teaches joy need not forget the sacred host.", relatedTemples=["vadakkumnathan-thrissur", "thiruvambady-krishna-thrissur", "paramekkavu-bhagavathy-thrissur"]),
    ]
    out = []
    for r in raw:
        de, dh = expand_detail(r["storyEn"], r["storyHi"], r["hook"], r["hookHi"], r["whyRitual"], r["whyRitualHi"], r["takeaway"], r["title"], r["titleHi"])
        out.append({**r, "readSeconds": 320, "tags": ["long-read", "first-timer", "family"], "storyDetailEn": de, "storyDetailHi": dh})
    return out


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
    detail["statePortal"] = {"name": portal["portalName"], "url": portal["portalUrl"], "slug": portal["slug"]}
    if detail.get("officialWebsite") in ("https://tourism.gov.in/", "", None):
        detail["officialWebsite"] = portal["portalUrl"]
    return detail


def enrich_myth_fields(detail: dict) -> dict:
    myth = detail.get("mythology", "")
    if not detail.get("mythologySignificance"):
        detail["mythologySignificance"] = myth + "\n\nPilgrimage literature treats this shrine as a living tirtha — verify custom with temple priests."
    if not detail.get("localBeliefs"):
        detail["localBeliefs"] = "Queue discipline, prasadam sharing, and festival vows shape belief as practice."
    if not detail.get("mythologyDisclaimer"):
        detail["mythologyDisclaimer"] = "Mythological accounts are drawn from Puranic traditions and sthala-purana. Versions differ by region."
    detail["lastUpdated"] = "2026-08-19"
    detail["country"] = detail.get("country") or "India"
    detail["tier"] = detail.get("tier") or "regional"
    return detail


def count_city(index: list[dict], city_key: str) -> int:
    cfg = CITY_CONFIG.get(city_key, {})
    terms = cfg.get("terms", [])
    exclude = cfg.get("exclude", [])
    n = 0
    for t in index:
        blob = (t.get("location", "") + " " + t.get("name", "")).lower()
        if exclude and any(ex in blob for ex in exclude):
            continue
        if any(term in blob for term in terms):
            n += 1
    return n


def city_at_target(index: list[dict], city_key: str) -> bool:
    return count_city(index, city_key) >= TARGET_PER_CITY


def apply_family_overrides(deity_keys: set[str]) -> int:
    updated = 0
    for path in sorted(TEMPLES.glob("*.json")):
        d = load_json(path)
        slug = d["slug"]
        if slug not in FAMILY_OVERRIDES:
            continue
        fams = [f for f in FAMILY_OVERRIDES[slug] if f in deity_keys]
        if fams and fams != d.get("deityFamilies"):
            d["deityFamilies"] = fams
            dump_json(path, d)
            updated += 1
    return updated


def add_temples(deity_keys: set[str]) -> tuple[int, list[str], list[str]]:
    existing_slugs = {p.stem for p in TEMPLES.glob("*.json")}
    index = load_json(DATA / "temples.json")
    created: list[str] = []
    skipped_city: list[str] = []
    for seed in NEW_TEMPLES:
        slug = seed["slug"]
        city = seed.get("city", "")
        if slug in existing_slugs:
            continue
        if city and city_at_target(index, city):
            if slug not in skipped_city:
                skipped_city.append(city)
            continue
        row = dict(seed)
        tags_extra = row.pop("tags_extra", None) or []
        row.pop("city", None)
        tier = row.pop("tier", "regional")
        fams = row.pop("deityFamilies", None) or []
        fams = [f for f in fams if f in deity_keys]
        if slug in FAMILY_OVERRIDES:
            fams = [f for f in FAMILY_OVERRIDES[slug] if f in deity_keys]
        detail = base_detail(row)
        detail["tier"] = tier
        detail["deityFamilies"] = fams
        tags = list(detail.get("tags") or [])
        for t in tags_extra:
            if t not in tags:
                tags.append(t)
        detail["tags"] = tags
        detail = attach_portal(enrich_myth_fields(detail))
        if detail.get("lat") is None:
            raise SystemExit(f"Missing lat for {slug}")
        dump_json(TEMPLES / f"{slug}.json", detail)
        created.append(slug)
        existing_slugs.add(slug)
        index.append({"slug": slug, "location": detail["location"], "name": detail["name"]})
    return len(created), created, skipped_city


def add_stories() -> tuple[int, list[str]]:
    path = DATA / "stories.json"
    data = load_json(path)
    existing = {s["slug"] for s in data.get("stories", [])}
    added = []
    for story in build_stories():
        if story["slug"] in existing:
            continue
        data["stories"].append(story)
        added.append(story["slug"])
        existing.add(story["slug"])
    if added:
        dump_json(path, data)
    return len(added), added


def update_engagement(story_slugs: list[str]) -> int:
    path = DATA / "engagement.json"
    data = load_json(path)
    stories = data.setdefault("dailyRotation", {}).setdefault("story", [])
    n = 0
    for slug in story_slugs:
        if slug not in stories:
            stories.append(slug)
            n += 1
    for slug in NEW_STORY_SLUGS:
        if slug not in stories:
            stories.append(slug)
            n += 1
    if n:
        dump_json(path, data)
    return n


def city_summary() -> dict[str, int]:
    index = load_json(DATA / "temples.json")
    return {city: count_city(index, city) for city in CITY_CONFIG}


def main() -> None:
    deity_keys = set(load_json(DATA / "deities.json").keys())
    temples_added, temple_slugs, skipped_cities = add_temples(deity_keys)
    families_updated = apply_family_overrides(deity_keys)
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])
    apply_family_overrides(deity_keys)
    stories_added, story_slugs = add_stories()
    engagement_added = update_engagement(story_slugs)
    counts = city_summary()
    at_target = sorted([c for c, n in counts.items() if n >= TARGET_PER_CITY])
    sample = {c: counts[c] for c in at_target[:20]}
    print("=== add_tier3_city_temples summary ===")
    print(f"Temples added: {temples_added}")
    print(f"Stories added: {stories_added}")
    print(f"Engagement dailyRotation.story appended: {engagement_added}")
    print(f"Family overrides applied on {families_updated} detail files (first pass)")
    print(f"Cities now at >={TARGET_PER_CITY} temples: {len(at_target)}")
    print(f"Sample counts: {sample}")
    if temple_slugs[:10]:
        print("Sample new slugs:", ", ".join(temple_slugs[:10]), "...")
    print(f"Cities covered (added temples for): {len(set(t.get('city') for t in NEW_TEMPLES if t['slug'] in temple_slugs))}")


if __name__ == "__main__":
    main()
