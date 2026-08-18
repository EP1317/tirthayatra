#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add Tier-2 city temples, new deity families, sthala stories, and family overrides."""

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


def T(**kw):
    return kw


NEW_DEITIES = {
    "murugan": {
        "slug": "murugan",
        "name": "Murugan / Kartikeya",
        "nameHi": "मुरुगन / कार्तिकेय",
        "sanskrit": "ॐ सरवण भव",
        "blurb": "Palani, Thiruchendur, Swamimalai, Marudhamalai, and Tamil–Kannada hill Murugan kshetras.",
        "lede": "Temples of Lord Murugan (Skanda, Subramanya, Kartikeya) — vel, peacock vahana, and six-faced wisdom.",
    },
    "surya": {
        "slug": "surya",
        "name": "Surya",
        "nameHi": "सूर्य देव",
        "sanskrit": "ॐ घृणि: सूर्य आदित्य",
        "blurb": "Konark, Deo, Modhera, and living solar shrines tied to Chhath and dawn arghya.",
        "lede": "Sun temples and Surya-narayana seats where dawn worship marks time and health.",
    },
    "shani": {
        "slug": "shani",
        "name": "Shani",
        "nameHi": "शनि देव",
        "sanskrit": "ॐ शं शनैश्चराय नमः",
        "blurb": "Shani Shingnapur, Shani temples, and Saturday graha-shanti pilgrimage.",
        "lede": "Shrines of Shani Dev — justice, patience, and Saturday oil-lamp devotion.",
    },
    "dattatreya": {
        "slug": "dattatreya",
        "name": "Dattatreya",
        "nameHi": "दत्तात्रेय",
        "sanskrit": "ॐ दिगंबरा दिगंबरा",
        "blurb": "Ganagapur, Narsobawadi, and avadhuta–guru seats of the trimurti ascetic.",
        "lede": "Temples remembering Dattatreya as the wandering guru of Brahma, Vishnu, and Shiva.",
    },
    "narasimha": {
        "slug": "narasimha",
        "name": "Narasimha",
        "nameHi": "नरसिंह",
        "sanskrit": "ॐ उग्रं वीरं महाविष्णुं",
        "blurb": "Ahobilam, Simhachalam, Yadagirigutta, and man-lion avatara kshetras.",
        "lede": "Narasimha temples where Vishnu appeared as the man-lion at twilight.",
    },
    "vitthal": {
        "slug": "vitthal",
        "name": "Vitthal / Vithoba",
        "nameHi": "विठ्ठल / विठोबा",
        "sanskrit": "पांडुरंग पांडुरंग",
        "blurb": "Pandharpur Wari, Dehu, and Maharashtra–Karnataka Varkari Vitthal seats.",
        "lede": "Vitthal temples of the Varkari path — standing Krishna with hands on hips.",
    },
    "bhairav": {
        "slug": "bhairav",
        "name": "Bhairav",
        "nameHi": "भैरव",
        "sanskrit": "ॐ भैरवाय नमः",
        "blurb": "Kal Bhairav of Ujjain, Kashi, and fierce Shiva guardian shrines.",
        "lede": "Bhairav temples — Shiva’s terrifying form guarding tirthas and cremation grounds.",
    },
    "lakshmi": {
        "slug": "lakshmi",
        "name": "Lakshmi",
        "nameHi": "लक्ष्मी जी",
        "sanskrit": "ॐ श्रीं महालक्ष्म्यै नमः",
        "blurb": "Kolhapur Mahalaxmi, Ashtalakshmi, and prosperity Goddess pilgrimage.",
        "lede": "Temples where Lakshmi is the primary or co-primary deity of darshan.",
    },
    "saraswati": {
        "slug": "saraswati",
        "name": "Saraswati",
        "nameHi": "सरस्वती जी",
        "sanskrit": "ॐ ऐं सरस्वत्यै नमः",
        "blurb": "Basar, Pushkar Saraswati, and learning-Goddess aksharabhyasam seats.",
        "lede": "Saraswati temples for education vows, Vasant Panchami, and first letters.",
    },
    "kali": {
        "slug": "kali",
        "name": "Kali",
        "nameHi": "काली माँ",
        "sanskrit": "ॐ क्रीं कालिकायै नमः",
        "blurb": "Kalighat, Dakshineswar, Kamakhya-adjacent Kali devotion, and Bengal Shakta seats.",
        "lede": "Kali temples of the dark Goddess — tongue, sword, and fierce compassion.",
    },
    "jagannath": {
        "slug": "jagannath",
        "name": "Jagannath",
        "nameHi": "जगन्नाथ",
        "sanskrit": "जय जगन्नाथ",
        "blurb": "Puri Rath Yatra, Ranchi, Agartala, and Odia–Bengali Jagannath culture.",
        "lede": "Jagannath temples with wooden deities, mahaprasad, and annual chariot festivals.",
    },
    "venkateswara": {
        "slug": "venkateswara",
        "name": "Venkateswara / Balaji",
        "nameHi": "वेंकटेश्वर / बालाजी",
        "sanskrit": "ॐ वेंकटेशाय नमः",
        "blurb": "Tirumala, Chilkur, and Balaji pilgrimage across South and diaspora search.",
        "lede": "Venkateswara temples — hill darshan, hundi vows, and Balaji grace.",
    },
    "annapurna": {
        "slug": "annapurna",
        "name": "Annapurna",
        "nameHi": "अन्नपूर्णा",
        "sanskrit": "ॐ अन्नपूर्णायै नमः",
        "blurb": "Kashi Annapurna, Horanadu, Indore, and food-Goddess annadanam seats.",
        "lede": "Annapurna temples where the Goddess feeds the world and devotees.",
    },
    "santoshi": {
        "slug": "santoshi",
        "name": "Santoshi Mata",
        "nameHi": "संतोषी माता",
        "sanskrit": "जय संतोषी माता",
        "blurb": "Friday vrata culture and modern Mother-Goddess temples across North India.",
        "lede": "Santoshi Mata shrines — contentment, Friday fast, and household vows.",
    },
}

# slug → deityFamilies (merge with existing, preserve order)
FAMILY_OVERRIDES: dict[str, list[str]] = {
    "palani-murugan": ["murugan", "devi"],
    "thiruchendur-murugan": ["murugan"],
    "kukke-subramanya": ["murugan", "ganesha"],
    "kataragama": ["murugan"],
    "shani-shingnapur": ["shani"],
    "konark-sun-temple": ["surya"],
    "sun-temple-deo": ["surya"],
    "ahobilam-narasimha": ["narasimha", "vishnu"],
    "yadagirigutta": ["narasimha", "vishnu"],
    "simhachalam": ["narasimha", "vishnu"],
    "pandharpur-vitthal": ["vitthal", "krishna", "vishnu"],
    "tirumala-venkateswara": ["venkateswara", "vishnu"],
    "chilkur-balaji": ["venkateswara", "vishnu"],
    "jagannath-puri": ["jagannath", "krishna", "vishnu", "devi"],
    "jagannath-agartala": ["jagannath", "krishna", "vishnu"],
    "jagannath-temple-ranchi": ["jagannath", "krishna", "vishnu"],
    "dakshineswar-kali": ["kali", "devi"],
    "kalighat": ["kali", "devi"],
    "kali-mata-patiala": ["kali", "devi"],
    "basara-gnana-saraswati": ["saraswati", "devi"],
    "mahalaxmi-kolhapur": ["lakshmi", "devi"],
    "kal-bhairav-ujjain": ["bhairav", "shiva"],
    "horanadu-annapoorneshwari": ["annapurna", "devi"],
    "sabarimala": ["ayyappa"],
}

AUTO_FAMILY_RULES: list[tuple[list[str], list[str]]] = [
    (["murugan", "subramanya", "kartikeya", "skanda", "palani", "thiruchendur"], ["murugan"]),
    (["surya", "sun temple", "sun god"], ["surya"]),
    (["shani", "shanishwar"], ["shani"]),
    (["narasimha", "simhachalam"], ["narasimha", "vishnu"]),
    (["vitthal", "vithoba", "pandharpur"], ["vitthal", "krishna"]),
    (["venkateswara", "tirumala", "balaji", "srinivasa"], ["venkateswara", "vishnu"]),
    (["jagannath"], ["jagannath", "krishna", "vishnu"]),
    (["dakshineswar", "kalighat", " kali ", "goddess kali"], ["kali", "devi"]),
    (["saraswati", "gnana saraswati", "basar"], ["saraswati", "devi"]),
    (["mahalaxmi", "mahalakshmi", "ambabai"], ["lakshmi", "devi"]),
    (["bhairav", "kal bhairav"], ["bhairav", "shiva"]),
    (["annapurn", "annapoorn"], ["annapurna", "devi"]),
    (["dattatreya", "dattatrey"], ["dattatreya"]),
    (["santoshi"], ["santoshi", "devi"]),
]

# Tier-2 city temples — idempotent via slug skip
NEW_TEMPLES = [
    # Indore
    T(slug="khajrana-ganesh-indore", name="Khajrana Ganesh Temple, Indore", deity="Lord Ganesha", location="Khajrana, Indore, Madhya Pradesh", state="Madhya Pradesh", glyph="ख", tier="famous", famousFor="Indore’s most visited Ganesh · high MP city search", summary="Khajrana Ganesh — Indore’s beloved Vinayaka with steady weekday queues.", mythology="Sthala tradition remembers a buried murti revealed to a devotee; the shrine grew into central India’s most searched urban Ganesh tirtha. Modak offerings and Annakut seasons pack the lanes.", lat=22.724, lng=75.857, mapQuery="Khajrana Ganesh Temple Indore", nearestRail="Indore Junction", nearestAirport="Indore", deityFamilies=["ganesha"], festivals=["Ganesh Chaturthi", "Angarki Chaturthi"]),
    T(slug="annapurna-temple-indore", name="Annapurna Temple, Indore", deity="Goddess Annapurna", location="Sudama Nagar, Indore, Madhya Pradesh", state="Madhya Pradesh", glyph="अ", tier="regional", famousFor="Indore Devi–Annapurna complex · regional Shakti search", summary="Annapurna Mandir — large Indore temple of the food-Goddess with adjacent shrines.", mythology="Built in Nagara style with multiple deities in the campus; Annapurna as nourisher anchors Indore’s Shakta map alongside Khajrana Ganesh.", lat=22.694, lng=75.867, mapQuery="Annapurna Temple Indore", nearestRail="Indore Junction", nearestAirport="Indore", deityFamilies=["annapurna", "devi"]),
    T(slug="kal-bhairav-indore", name="Kal Bhairav Temple, Indore", deity="Lord Kal Bhairav (Shiva)", location="Bhairav Garh, Indore, Madhya Pradesh", state="Madhya Pradesh", glyph="भ", tier="regional", famousFor="Indore’s guardian Bhairav · Sunday arati search", summary="Kal Bhairav — fierce Shiva guardian shrine of Indore’s old fort belt.", mythology="Bhairav guards the tirtha as kotwal of Shiva’s court; liquor prasad tradition here follows Malwa custom under temple rules.", lat=22.718, lng=75.848, mapQuery="Kal Bhairav Temple Indore", nearestRail="Indore Junction", nearestAirport="Indore", deityFamilies=["bhairav", "shiva"]),
    # Bhopal
    T(slug="lakshmi-narayan-birla-bhopal", name="Lakshmi Narayan Temple (Birla Mandir), Bhopal", deity="Lakshmi–Narayan (Vishnu)", location="Arera Hills, Bhopal, Madhya Pradesh", state="Madhya Pradesh", glyph="बि", tier="regional", famousFor="Bhopal hill Birla Mandir · city landmark search", summary="Birla Mandir Bhopal — white marble Lakshmi Narayan on Arera Hills overlooking the lakes.", mythology="Modern marble campus with epics in relief; pairs with Upper Lake tourism and Sunday family darshan.", lat=23.240, lng=77.400, mapQuery="Birla Mandir Bhopal", nearestRail="Bhopal Junction", nearestAirport="Bhopal", deityFamilies=["vishnu", "lakshmi"]),
    T(slug="gufa-mandir-bhopal", name="Gufa Mandir (Udayagiri), Bhopal", deity="Lord Shiva & Hanuman", location="Udayagiri, Bhopal, Madhya Pradesh", state="Madhya Pradesh", glyph="गु", tier="regional", famousFor="Cave temple on Udayagiri hill · Bhopal local search", summary="Gufa Mandir — rock-cut style cave shrine on Bhopal’s Udayagiri ridge.", mythology="Devotees climb to darshan in a grotto setting; Hanuman and Shiva share the sacred hill with ancient cave heritage nearby.", lat=23.233, lng=77.393, mapQuery="Gufa Mandir Bhopal Udayagiri", nearestRail="Bhopal Junction", nearestAirport="Bhopal", deityFamilies=["shiva", "hanuman"]),
    T(slug="iskcon-bhopal", name="ISKCON Temple, Bhopal", deity="Krishna–Radha (ISKCON)", location="Habibganj, Bhopal, Madhya Pradesh", state="Madhya Pradesh", glyph="इ", tier="regional", famousFor="Bhopal ISKCON kirtan · modern Vaishnava search", summary="ISKCON Bhopal — active Krishna temple with Sunday feast and youth satsang.", mythology="Gaudiya Vaishnava campus bringing Braj kirtan culture to Madhya Pradesh’s capital.", lat=23.220, lng=77.440, mapQuery="ISKCON Temple Bhopal", nearestRail="Habibganj", nearestAirport="Bhopal", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    # Nagpur
    T(slug="tekdi-ganesh-nagpur", name="Tekdi Ganesh Temple, Nagpur", deity="Lord Ganesha (Tekdi Ganapati)", location="Sitabuldi Hill, Nagpur, Maharashtra", state="Maharashtra", glyph="ते", tier="famous", famousFor="Nagpur’s hill Ganesh · top Vidarbha city search", summary="Tekdi Ganapati — Nagpur’s iconic hilltop Ganesha above the railway quarter.", mythology="The ‘tekdi’ (hill) Ganesh is the city’s wish-fulfilling Vinayaka; Angarki and Ganesh Chaturthi see lakhs on the climb.", lat=21.148, lng=79.088, mapQuery="Tekdi Ganesh Temple Nagpur", nearestRail="Nagpur Junction", nearestAirport="Nagpur", deityFamilies=["ganesha"]),
    T(slug="koradi-temple-nagpur", name="Shri Mahalakshmi Jagdamba Temple, Koradi", deity="Goddess Jagdamba (Mahalakshmi)", location="Koradi, Nagpur, Maharashtra", state="Maharashtra", glyph="को", tier="famous", famousFor="Navaratri lakhs · Koradi Devi regional mega-search", summary="Koradi Jagdamba — major Devi tirtha of Nagpur with huge Navaratri footfall.", mythology="Jagdamba as city mother of Vidarbha; Koradi’s annual fair is among Maharashtra’s largest Devi gatherings outside Kolhapur.", lat=21.247, lng=79.103, mapQuery="Koradi Temple Nagpur", nearestRail="Nagpur", nearestAirport="Nagpur", deityFamilies=["devi", "lakshmi"], festivals=["Navaratri", "Gudi Padwa"]),
    T(slug="swaminarayan-nagpur", name="Swaminarayan Temple, Nagpur", deity="Swaminarayan / NarNarayan (Vaishnava)", location="Dharampeth, Nagpur, Maharashtra", state="Maharashtra", glyph="स्व", tier="regional", famousFor="Marble Swaminarayan campus · Nagpur family search", summary="Swaminarayan Mandir Nagpur — ornate marble temple with cultural exhibition.", mythology="Swaminarayan sampradaya seva and annakut draw Gujarati–Marathi families across Vidarbha.", lat=21.145, lng=79.065, mapQuery="Swaminarayan Temple Nagpur", nearestRail="Nagpur Junction", nearestAirport="Nagpur", deityFamilies=["vishnu"], tags_extra=["modern-temples"]),
    # Coimbatore
    T(slug="perur-pateeswarar", name="Perur Patteeswarar Temple", deity="Lord Shiva (Patteeswarar)", location="Perur, Coimbatore, Tamil Nadu", state="Tamil Nadu", glyph="प", tier="famous", famousFor="Kongu Nadu Shiva · Coimbatore’s ancient patikam search", summary="Perur Patteeswarar — classic Chola-era Shiva temple west of Coimbatore.", mythology="Kongu sthala purana links Patteeswarar with Karaikkal Ammaiyar lore; the golden roof and prakaram murals anchor Coimbatore Shaivism.", lat=10.968, lng=76.912, mapQuery="Perur Patteeswarar Temple", nearestRail="Coimbatore Junction", nearestAirport="Coimbatore", deityFamilies=["shiva"]),
    T(slug="marudhamalai-murugan", name="Marudhamalai Murugan Temple", deity="Lord Murugan (Subramanya)", location="Marudhamalai, Coimbatore, Tamil Nadu", state="Tamil Nadu", glyph="म", tier="famous", famousFor="Hill Murugan above Coimbatore · high Tamil Nadu search", summary="Marudhamalai — forest-hill Murugan temple overlooking Coimbatore.", mythology="Murugan as youthful healer and commander; Thaipusam and Panguni Uttiram draw hill-climbing devotees from Kongu Nadu.", lat=11.046, lng=76.912, mapQuery="Marudhamalai Murugan Temple", nearestRail="Coimbatore", nearestAirport="Coimbatore", deityFamilies=["murugan"], festivals=["Thaipusam", "Skanda Shashti"]),
    T(slug="eachanari-vinayagar", name="Eachanari Vinayagar Temple", deity="Lord Ganesha (Eachanari Pillaiyar)", location="Eachanari, Coimbatore, Tamil Nadu", state="Tamil Nadu", glyph="ए", tier="regional", famousFor="Large Coimbatore Ganesh · highway pilgrim stop search", summary="Eachanari Vinayagar — tall Ganesha murti on the Pollachi road from Coimbatore.", mythology="Popular first-stop Vinayaka for vehicles and new ventures; modak abhishekam defines local vow culture.", lat=10.926, lng=76.954, mapQuery="Eachanari Vinayagar Temple", nearestRail="Coimbatore", nearestAirport="Coimbatore", deityFamilies=["ganesha"]),
    # Surat
    T(slug="ambaji-temple-surat", name="Ambaji Temple, Surat", deity="Goddess Amba (Ambaji)", location="Varachha, Surat, Gujarat", state="Gujarat", glyph="अ", tier="regional", famousFor="Surat’s busiest Devi · diamond-belt vow search", summary="Ambaji Mandir Surat — major city Devi shrine for Varachha and textile workers.", mythology="Amba as kuldevi of many Gujarati families; Navaratri transforms Surat’s temple quarter into a night market of devotion.", lat=21.210, lng=72.860, mapQuery="Ambaji Temple Surat", nearestRail="Surat", nearestAirport="Surat", deityFamilies=["devi"]),
    T(slug="iskcon-surat", name="ISKCON Temple, Surat", deity="Krishna–Radha (ISKCON)", location="Athwalines, Surat, Gujarat", state="Gujarat", glyph="इ", tier="regional", famousFor="Surat ISKCON feast · youth kirtan search", summary="ISKCON Surat — riverside Krishna temple with daily prasadam distribution.", mythology="Tapi-bank kirtan culture serves Surat’s migrant and business communities on Janmashtami and Sunday programs.", lat=21.170, lng=72.790, mapQuery="ISKCON Temple Surat", nearestRail="Surat", nearestAirport="Surat", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    T(slug="swaminarayan-surat", name="Swaminarayan Temple, Surat", deity="Swaminarayan (Vaishnava)", location="Adajan, Surat, Gujarat", state="Gujarat", glyph="स", tier="regional", famousFor="Surat marble mandir · family darshan search", summary="Swaminarayan Mandir Surat — large Adajan campus with ornate carving.", mythology="Swaminarayan bhakti anchors Surat’s Gujarati Hindu calendar alongside Ambaji and river ghats.", lat=21.200, lng=72.790, mapQuery="Swaminarayan Temple Surat Adajan", nearestRail="Surat", nearestAirport="Surat", deityFamilies=["vishnu"], tags_extra=["modern-temples"]),
    # Vadodara
    T(slug="eme-temple-vadodara", name="EME Temple (Dakshinamurty Temple), Vadodara", deity="Lord Dakshinamurty / Shiva (multi-faith dome)", location="EME Centre, Vadodara, Gujarat", state="Gujarat", glyph="ई", tier="famous", famousFor="Unique alloy dome · Vadodara architecture search", summary="EME Temple — geodesic ‘Dakshinamurty’ shrine built by the Military Engineers with symbols of many faiths.", mythology="A modern tirtha of harmony: Shiva as Dakshinamurty sits under a aluminium dome inlaid with scripture from several traditions.", lat=22.330, lng=73.180, mapQuery="EME Temple Vadodara", nearestRail="Vadodara Junction", nearestAirport="Vadodara", deityFamilies=["shiva"], tags_extra=["modern-temples"]),
    T(slug="kalika-mandir-vadodara", name="Kalika Mata Temple, Vadodara", deity="Goddess Kalika", location="Makarpura, Vadodara, Gujarat", state="Gujarat", glyph="का", tier="regional", famousFor="Navaratri garba hub · Vadodara Devi search", summary="Kalika Mata — city Devi temple tied to Vadodara’s Navaratri garba culture.", mythology="Kalika as fierce protector; festival nights link temple arati with public garba grounds across the city.", lat=22.240, lng=73.190, mapQuery="Kalika Mata Temple Vadodara", nearestRail="Vadodara Junction", nearestAirport="Vadodara", deityFamilies=["devi", "kali"]),
    T(slug="kirti-mandir-vadodara", name="Kirti Mandir, Vadodara", deity="Shiva linga & memorial shrines", location="Kirti Stambh, Vadodara, Gujarat", state="Gujarat", glyph="कि", tier="regional", famousFor="Gaekwad memorial temple · city heritage search", summary="Kirti Mandir — memorial complex with active Shiva worship near the old city.", mythology="Built in memory of the Gaekwad dynasty with murals of Maratha–Gujarat history; living Shiva puja continues for citizens.", lat=22.300, lng=73.200, mapQuery="Kirti Mandir Vadodara", nearestRail="Vadodara Junction", nearestAirport="Vadodara", deityFamilies=["shiva"]),
    # Lucknow
    T(slug="hanuman-setu-lucknow", name="Hanuman Setu Mandir, Lucknow", deity="Lord Hanuman", location="Daliganj, Lucknow, Uttar Pradesh", state="Uttar Pradesh", glyph="ह", tier="famous", famousFor="Lucknow’s mega Hanuman · Tuesday queue search", summary="Hanuman Setu — sprawling Hanuman temple complex on the Gomti bank.", mythology="Tuesday and Saturday crowds define Lucknow’s urban bhakti; the ‘setu’ name recalls Hanuman’s bridge seva to Rama.", lat=26.860, lng=80.920, mapQuery="Hanuman Setu Mandir Lucknow", nearestRail="Lucknow Charbagh", nearestAirport="Lucknow", deityFamilies=["hanuman", "rama"]),
    T(slug="chandrika-devi-lucknow", name="Chandrika Devi Temple, Lucknow", deity="Goddess Chandrika Devi", location="Aashiyana, Lucknow, Uttar Pradesh", state="Uttar Pradesh", glyph="च", tier="regional", famousFor="Gomti riverside Devi · Lucknow Shakti search", summary="Chandrika Devi — ancient riverside Devi shrine of Lucknow’s outskirts.", mythology="Sthala purana links the Goddess with Chandraketu lore; Navaratri and Mundan ceremonies draw families from Awadh.", lat=26.780, lng=80.920, mapQuery="Chandrika Devi Temple Lucknow", nearestRail="Lucknow", nearestAirport="Lucknow", deityFamilies=["devi"]),
    T(slug="lavkush-temple-lucknow", name="Lavkush Temple (Aliganj), Lucknow", deity="Lav–Kush & Sita (Ramayana)", location="Aliganj, Lucknow, Uttar Pradesh", state="Uttar Pradesh", glyph="ल", tier="regional", famousFor="Ramayana sons’ seat · Awadh heritage search", summary="Lavkush Mandir — Aliganj temple tied to Lav and Kush of Ramayana memory.", mythology="Local tradition places the ashram of Rama’s sons here; Ram Navami and Kartik fairs sustain Awadh’s epic geography.", lat=26.890, lng=80.940, mapQuery="Lavkush Temple Aliganj Lucknow", nearestRail="Lucknow", nearestAirport="Lucknow", deityFamilies=["rama"]),
    # Kanpur
    T(slug="jk-temple-kanpur", name="JK Temple (Radha Krishna), Kanpur", deity="Radha–Krishna", location="Sarvodaya Nagar, Kanpur, Uttar Pradesh", state="Uttar Pradesh", glyph="जे", tier="famous", famousFor="Kanpur’s landmark Krishna temple · industrial city search", summary="JK Temple — modern Radha Krishna mandir with five shrines under one shikhara.", mythology="Built by the JK Trust; the campus presents epics in sculpture while daily aarti serves Kanpur’s Vaishnava households.", lat=26.470, lng=80.330, mapQuery="JK Temple Kanpur", nearestRail="Kanpur Central", nearestAirport="Lucknow / Kanpur", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    T(slug="sheetla-devi-kanpur", name="Sheetla Devi Temple, Kanpur", deity="Goddess Sheetla", location="Bithoor Road area, Kanpur, Uttar Pradesh", state="Uttar Pradesh", glyph="शी", tier="regional", famousFor="Kanpur Devi vows · Sheetla Ashtami search", summary="Sheetla Devi — regional Goddess temple for pox-protection and child-health vows.", mythology="Sheetla worship peaks in Chaitra; Kanpur families invoke the cooling Goddess in summer epidemics memory.", lat=26.450, lng=80.350, mapQuery="Sheetla Devi Temple Kanpur", nearestRail="Kanpur Central", nearestAirport="Lucknow", deityFamilies=["devi"]),
    T(slug="hanuman-mandir-kanpur", name="Hanuman Mandir, Kanpur", deity="Lord Hanuman", location="P Road, Kanpur, Uttar Pradesh", state="Uttar Pradesh", glyph="ह", tier="regional", famousFor="Central Kanpur Hanuman · Tuesday footfall search", summary="P Road Hanuman — busy urban Hanuman shrine of Kanpur cantonment belt.", mythology="Hanuman as sankat-mochan for soldiers and traders; Tuesdays see continuous darshan lines.", lat=26.460, lng=80.350, mapQuery="Hanuman Mandir Kanpur", nearestRail="Kanpur Central", nearestAirport="Lucknow", deityFamilies=["hanuman"]),
    # Gwalior
    T(slug="teli-ka-mandir-gwalior", name="Teli ka Mandir, Gwalior Fort", deity="Lord Vishnu (tall shikhara temple)", location="Gwalior Fort, Gwalior, Madhya Pradesh", state="Madhya Pradesh", glyph="ते", tier="famous", famousFor="Fort’s tallest pre-Muslim temple · Gwalior heritage search", summary="Teli ka Mandir — 9th-century shikhara temple inside Gwalior Fort.", mythology="Unique blend of Nagara height with Valabhi elements; still revered amid fort museums and sound-and-light shows.", lat=26.230, lng=78.170, mapQuery="Teli ka Mandir Gwalior", nearestRail="Gwalior Junction", nearestAirport="Gwalior", deityFamilies=["vishnu"]),
    T(slug="sas-bahu-temples-gwalior", name="Sas-Bahu Temples, Gwalior", deity="Vishnu (Sahastrabahu) & Shiva", location="Gwalior Fort east, Gwalior, Madhya Pradesh", state="Madhya Pradesh", glyph="स", tier="famous", famousFor="Twin 11th-century temples · MP archaeology search", summary="Sas-Bahu — paired red-sandstone temples with intricate carving inside the fort.", mythology="Names derive from Sahastrabahu Vishnu and smaller companion shrine; living puja continues on festival days.", lat=26.232, lng=78.175, mapQuery="Sas Bahu Temple Gwalior", nearestRail="Gwalior Junction", nearestAirport="Gwalior", deityFamilies=["vishnu", "shiva"]),
    T(slug="bateshwar-temples-morena", name="Bateshwar Temple Group", deity="Lord Shiva (multiple shrines)", location="Bateshwar, Morena (near Gwalior), Madhya Pradesh", state="Madhya Pradesh", glyph="ब", tier="regional", famousFor="200+ restored shrines · Chambal heritage search", summary="Bateshwar — sprawling Shiva temple cluster on the Chambal ravines near Gwalior.", mythology="ASI-restored nagara shrines line the Yamuna–Chambal belt; Kartik Monday melas revive pilgrimage after conservation.", lat=26.420, lng=78.220, mapQuery="Bateshwar Temples Morena", nearestRail="Morena", nearestAirport="Gwalior", deityFamilies=["shiva"]),
    # Jabalpur
    T(slug="chausath-yogini-bhedaghat", name="Chausath Yogini Temple, Bhedaghat", deity="64 Yoginis & Shiva (Matrika tradition)", location="Bhedaghat, Jabalpur, Madhya Pradesh", state="Madhya Pradesh", glyph="च", tier="famous", famousFor="Circular yogini shrine · marble gorge tourism search", summary="Chausath Yogini — rare circular yogini temple above the Narmada marble gorge.", mythology="Yogini worship links tantric Shakta and Shaiva streams; paired with Dhuandhar falls and Narmada aarti.", lat=23.132, lng=79.801, mapQuery="Chausath Yogini Temple Bhedaghat", nearestRail="Jabalpur", nearestAirport="Jabalpur", deityFamilies=["devi", "shiva"]),
    T(slug="madan-mahal-jabalpur", name="Madan Mahal Fort Temple area, Jabalpur", deity="Lord Shiva (Gond-era shrine traditions)", location="Madan Mahal, Jabalpur, Madhya Pradesh", state="Madhya Pradesh", glyph="म", tier="regional", famousFor="Gond fort sacred hill · Jabalpur city search", summary="Madan Mahal hill — historic fort with living Shiva shrines above Jabalpur.", mythology="Gond queen Durgavati’s fort memory blends with Shaiva tirtha on the granite outcrop overlooking the city.", lat=23.160, lng=79.930, mapQuery="Madan Mahal Jabalpur", nearestRail="Jabalpur", nearestAirport="Jabalpur", deityFamilies=["shiva"]),
    T(slug="gwari-ghat-jabalpur", name="Gwari Ghat Narmada Temples, Jabalpur", deity="Lord Shiva & Narmada", location="Gwari Ghat, Jabalpur, Madhya Pradesh", state="Madhya Pradesh", glyph="ग", tier="regional", famousFor="Narmada aarti ghat · Jabalpur evening search", summary="Gwari Ghat — cluster of Shiva shrines for Narmada parikrama and aarti.", mythology="Narmada as mother river; kartik and somvar nights see lamp offerings from the ghat steps.", lat=23.145, lng=79.920, mapQuery="Gwari Ghat Jabalpur", nearestRail="Jabalpur", nearestAirport="Jabalpur", deityFamilies=["shiva"]),
    # Mangaluru
    T(slug="kadri-manjunatha-mangaluru", name="Kadri Manjunatha Temple, Mangaluru", deity="Lord Manjunatha (Shiva)", location="Kadri, Mangaluru, Karnataka", state="Karnataka", glyph="क", tier="famous", famousFor="Panchalinga hill Shiva · coastal Karnataka search", summary="Kadri Manjunatha — hill Shiva temple with bronze age lore on the Mangaluru ridge.", mythology="Shiva as Manjunatha with Parvati; the bronze Lokeshwara in the matha museum and Kadri caves deepen the tirtha.", lat=12.880, lng=74.860, mapQuery="Kadri Manjunatha Temple Mangalore", nearestRail="Mangaluru Central", nearestAirport="Mangaluru", deityFamilies=["shiva"]),
    T(slug="mangaladevi-mangaluru", name="Mangaladevi Temple, Mangaluru", deity="Goddess Mangaladevi", location="Bolar, Mangaluru, Karnataka", state="Karnataka", glyph="मं", tier="famous", famousFor="City namesake Goddess · Tulu Nadu Shakti search", summary="Mangaladevi — the Devi who gives Mangaluru its name.", mythology="Kuladevata of many Tulu families; the temple anchors coastal Karnataka’s Shakta calendar before Dharmasthala onward yatras.", lat=12.870, lng=74.840, mapQuery="Mangaladevi Temple Mangalore", nearestRail="Mangaluru", nearestAirport="Mangaluru", deityFamilies=["devi"]),
    T(slug="kudroli-gokarnanatha", name="Kudroli Gokarnanatha Temple, Mangaluru", deity="Lord Ganesha & Shiva (Gokarnanatha)", location="Kudroli, Mangaluru, Karnataka", state="Karnataka", glyph="ग", tier="famous", famousFor="Navaratri lights · social-reform temple search", summary="Kudroli Gokarnanatha — reform-era temple famous for dazzling Navaratri illumination.", mythology="Built by Narayana Guru’s disciple tradition in Kudroli; Ganesha–Shiva campus hosts one of Karnataka’s brightest festival light shows.", lat=12.880, lng=74.830, mapQuery="Kudroli Gokarnanatha Temple", nearestRail="Mangaluru", nearestAirport="Mangaluru", deityFamilies=["shiva", "ganesha"]),
    # Hubli-Dharwad
    T(slug="chandramouleshwara-unkal", name="Chandramouleshwara Temple, Unkal", deity="Lord Shiva (Chandramouleshwara)", location="Unkal, Hubballi, Karnataka", state="Karnataka", glyph="चं", tier="famous", famousFor="Chalukya Shiva by Unkal lake · Hubballi search", summary="Chandramouleshwara — Chalukya-era Shiva temple on the Unkal lake hub.", mythology="Twin Shiva lingas under a stone mantapa; sunset darshan with the lake is a Hubballi–Dharwad classic.", lat=15.380, lng=75.110, mapQuery="Chandramouleshwara Temple Unkal Hubli", nearestRail="Hubballi Junction", nearestAirport="Hubballi", deityFamilies=["shiva"]),
    T(slug="siddharoodha-math-hubli", name="Siddharoodha Math, Hubballi", deity="Lord Shiva (Samadhi of Siddharoodha Swami)", location="Hubballi, Karnataka", state="Karnataka", glyph="सि", tier="famous", famousFor="Lingayat math pilgrimage · North Karnataka search", summary="Siddharoodha Math — major Veerashaiva pilgrimage centre of Hubballi.", mythology="Samadhi of Siddharoodha Swami draws lakhs on car festival; annadanam and Lingayat bhakti define the twin cities.", lat=15.360, lng=75.120, mapQuery="Siddharoodha Math Hubli", nearestRail="Hubballi Junction", nearestAirport="Hubballi", deityFamilies=["shiva"]),
    T(slug="banashankari-hubli", name="Banashankari Temple, Hubballi", deity="Goddess Banashankari", location="Hubballi, Karnataka", state="Karnataka", glyph="ब", tier="regional", famousFor="Hubballi Devi · Friday vow search", summary="Banashankari — city Devi temple for Hubballi–Dharwad families.", mythology="Banashankari as forest Goddess adapted to urban Hubli; pairs with Unkal Shiva on weekend tirtha loops.", lat=15.350, lng=75.140, mapQuery="Banashankari Temple Hubli", nearestRail="Hubballi Junction", nearestAirport="Hubballi", deityFamilies=["devi"]),
    # Kozhikode
    T(slug="tali-mahadeva-kozhikode", name="Tali Mahadeva Temple, Kozhikode", deity="Lord Shiva (Tali Mahadeva)", location="Palayam, Kozhikode, Kerala", state="Kerala", glyph="त", tier="famous", famousFor="Zamorin-era Shiva · Malabar heritage search", summary="Tali Mahadeva — ancient Shiva temple of the Zamorin capital.", mythology="Revathy Pattathanam literary festival memory links the shrine to classical Kerala culture; Shiva as patron of Malabar courts.", lat=11.258, lng=75.780, mapQuery="Tali Mahadeva Temple Kozhikode", nearestRail="Kozhikode", nearestAirport="Kozhikode", deityFamilies=["shiva"]),
    T(slug="valayanad-devi-kozhikode", name="Valayanad Devi Temple, Kozhikode", deity="Goddess Valayanad Bhagavathy", location="Valayanad, Kozhikode, Kerala", state="Kerala", glyph="व", tier="regional", famousFor="Malabar Devi kshetram · Theyyam-adjacent search", summary="Valayanad Devi — important Shakta shrine north of Kozhikode city.", mythology="Goddess of the sword and trident in local memory; festival processions connect temple culture with Theyyam heartlands.", lat=11.320, lng=75.820, mapQuery="Valayanad Devi Temple", nearestRail="Kozhikode", nearestAirport="Kozhikode", deityFamilies=["devi"]),
    T(slug="varakkal-bhagavathi-kozhikode", name="Varakkal Bhagavathy Temple, Kozhikode", deity="Goddess Bhagavathy (Varakkal Amma)", location="West Hill, Kozhikode, Kerala", state="Kerala", glyph="व", tier="regional", famousFor="Sea-facing Devi · Kozhikode city search", summary="Varakkal Bhagavathy — cliff-side Devi temple overlooking the Arabian Sea.", mythology="Among 108 Durga kshetras cited in regional lore; Vavu Bali and Navaratri draw Malabar coastal families.", lat=11.260, lng=75.770, mapQuery="Varakkal Bhagavathy Temple Kozhikode", nearestRail="Kozhikode", nearestAirport="Kozhikode", deityFamilies=["devi"]),
    # Dehradun
    T(slug="tapkeshwar-mahadev-dehradun", name="Tapkeshwar Mahadev Temple, Dehradun", deity="Lord Shiva (Tapkeshwar)", location="Garhi Cantt, Dehradun, Uttarakhand", state="Uttarakhand", glyph="त", tier="famous", famousFor="Cave dripping lingam · Dehradun top search", summary="Tapkeshwar — Shiva lingam in a cave where water droplets fall on the deity.", mythology="Drona cave lore of the Mahabharata era; Shivaratri and monsoon streams define this forest tirtha.", lat=30.350, lng=78.030, mapQuery="Tapkeshwar Mahadev Dehradun", nearestRail="Dehradun", nearestAirport="Dehradun", deityFamilies=["shiva"]),
    T(slug="laxman-siddh-dehradun", name="Laxman Siddh Temple, Dehradun", deity="Laxman (Ramayana) & Shiva traditions", location="Dehradun, Uttarakhand", state="Uttarakhand", glyph="ल", tier="regional", famousFor="Ramayana siddh peeth · Doon valley search", summary="Laxman Siddh — forest ashram shrine linked to Laxman’s penance in Doon lore.", mythology="Local tradition places Laxman’s tapas here; simple forest darshan attracts Doon families on Sundays.", lat=30.280, lng=78.080, mapQuery="Laxman Siddh Temple Dehradun", nearestRail="Dehradun", nearestAirport="Dehradun", deityFamilies=["rama", "shiva"]),
    T(slug="shiv-mandir-forest-research-dehradun", name="Shiv Mandir, Forest Research Institute", deity="Lord Shiva", location="FRI campus, Dehradun, Uttarakhand", state="Uttarakhand", glyph="श", tier="regional", famousFor="FRI campus Shiva · heritage walk search", summary="Forest Research Institute Shiva temple — gothic-campus setting with active puja.", mythology="Colonial-era campus architecture frames a small living Shiva shrine used by FRI staff and Dehradun walkers.", lat=30.340, lng=78.010, mapQuery="Forest Research Institute Shiva Temple Dehradun", nearestRail="Dehradun", nearestAirport="Dehradun", deityFamilies=["shiva"]),
    # Haridwar
    T(slug="mansa-devi-haridwar", name="Mansa Devi Temple, Haridwar", deity="Goddess Mansa Devi", location="Bilwa Hill, Haridwar, Uttarakhand", state="Uttarakhand", glyph="म", tier="famous", famousFor="Cable-car Devi · Haridwar twin-hill search", summary="Mansa Devi — wish-fulfilling Goddess on Bilwa Parvat above Haridwar.", mythology="Devotees tie threads for boons; paired with Chandi Devi on the opposite hill for the classic Haridwar skyline yatra.", lat=29.958, lng=78.164, mapQuery="Mansa Devi Temple Haridwar", nearestRail="Haridwar Junction", nearestAirport="Dehradun", deityFamilies=["devi"]),
    T(slug="chandi-devi-haridwar", name="Chandi Devi Temple, Haridwar", deity="Goddess Chandi Devi", location="Neel Parvat, Haridwar, Uttarakhand", state="Uttarakhand", glyph="च", tier="famous", famousFor="Neel Parvat Shakti · Haridwar ropeway search", summary="Chandi Devi — hill temple where the Goddess slayed Chanda–Munda in tradition.", mythology="Skanda Purana memory places Chandi here after killing demons; Navaratri and Kumbh seasons intensify hill queues.", lat=29.936, lng=78.150, mapQuery="Chandi Devi Temple Haridwar", nearestRail="Haridwar Junction", nearestAirport="Dehradun", deityFamilies=["devi", "kali"]),
    T(slug="maya-devi-haridwar", name="Maya Devi Temple, Haridwar", deity="Goddess Maya Devi", location="Upper Road, Haridwar, Uttarakhand", state="Uttarakhand", glyph="मा", tier="famous", famousFor="One of Haridwar’s Siddh Peethas · ancient Devi search", summary="Maya Devi — historic Shakti seat predating much of modern Haridwar’s grid.", mythology="Counted among siddh peethas where heart and navel of Sati fell in varying lists; presides over the sacred core of Kankhal.", lat=29.945, lng=78.160, mapQuery="Maya Devi Temple Haridwar", nearestRail="Haridwar Junction", nearestAirport="Dehradun", deityFamilies=["devi"]),
    # Jodhpur
    T(slug="chamunda-mata-jodhpur", name="Chamunda Mata Temple, Jodhpur", deity="Goddess Chamunda", location="Mehrangarh Fort, Jodhpur, Rajasthan", state="Rajasthan", glyph="च", tier="famous", famousFor="Mehrangarh kuldevi · Jodhpur fort search", summary="Chamunda Mata — royal kuldevi shrine inside Mehrangarh Fort.", mythology="Rao Jodha shifted the Goddess here when the fort was built; Dussehra sees the idol carried to the city for public darshan.", lat=26.298, lng=73.019, mapQuery="Chamunda Mata Temple Mehrangarh", nearestRail="Jodhpur Junction", nearestAirport="Jodhpur", deityFamilies=["devi"]),
    T(slug="mandore-temples-jodhpur", name="Mandore Temples & Gardens", deity="Ravana temple & hero stones (Shaiva–folk)", location="Mandore, Jodhpur, Rajasthan", state="Rajasthan", glyph="म", tier="regional", famousFor="Ravana temple rarity · Jodhpur day-trip search", summary="Mandore — garden complex with unusual Ravana temple and Marwar hero memorials.", mythology="Marwar capital before Jodhpur; Ravana as son-in-law of Mandore in local folk memory makes this a curiosity tirtha.", lat=26.345, lng=73.028, mapQuery="Mandore Gardens Jodhpur", nearestRail="Jodhpur Junction", nearestAirport="Jodhpur", deityFamilies=["shiva"]),
    T(slug="kunj-bihari-jodhpur", name="Kunj Bihari Temple, Jodhpur", deity="Lord Krishna (Kunj Bihari)", location="Old city, Jodhpur, Rajasthan", state="Rajasthan", glyph="क", tier="regional", famousFor="Old city Krishna · blue-city search", summary="Kunj Bihari — ornate haveli-style Krishna temple in Jodhpur’s painted lanes.", mythology="Krishna as forest flirt of Vrindavan remembered in desert city; Janmashtami fills the old bazaar with bhajan.", lat=26.295, lng=73.025, mapQuery="Kunj Bihari Temple Jodhpur", nearestRail="Jodhpur Junction", nearestAirport="Jodhpur", deityFamilies=["krishna", "vishnu"]),
    # Kota
    T(slug="kansua-mahadev-kota", name="Kansua Shiva Temple, Kota", deity="Lord Shiva (Kansua Mahadev)", location="Kota, Rajasthan", state="Rajasthan", glyph="क", tier="regional", famousFor="Four-faced lingam · Kota Shivaratri search", summary="Kansua Mahadev — Shiva temple famed for a four-faced lingam in Kota.", mythology="Local lore claims a lingam that grew four faces; Shivaratri and Sawan Mondays anchor Kota’s Shaiva calendar.", lat=25.180, lng=75.840, mapQuery="Kansua Mahadev Temple Kota", nearestRail="Kota Junction", nearestAirport="Jaipur / Kota", deityFamilies=["shiva"]),
    T(slug="garadia-mahadev-kota", name="Garadia Mahadev Temple, Kota", deity="Lord Shiva (Garadia Mahadev)", location="Garadia, Kota, Rajasthan", state="Rajasthan", glyph="ग", tier="famous", famousFor="Chambal gorge cliff Shiva · viral travel search", summary="Garadia Mahadev — cliff-edge Shiva above the Chambal canyon near Kota.", mythology="Dramatic gorge viewpoint with a small Shiva shrine; monsoon greenery made this a social-media tirtha paired with wildlife tourism.", lat=25.050, lng=76.020, mapQuery="Garadia Mahadev Kota", nearestRail="Kota Junction", nearestAirport="Jaipur", deityFamilies=["shiva"]),
    T(slug="godavari-dham-kota", name="Godavari Dham, Kota", deity="Lord Hanuman", location="Kota, Rajasthan", state="Rajasthan", glyph="गो", tier="regional", famousFor="Large Hanuman campus · Kota Tuesday search", summary="Godavari Dham — spacious Hanuman temple complex popular with students.", mythology="Hanuman as sankat-mochan for Kota’s coaching-city youth; Tuesdays and Saturdays see long youthful queues.", lat=25.170, lng=75.860, mapQuery="Godavari Dham Kota", nearestRail="Kota Junction", nearestAirport="Jaipur", deityFamilies=["hanuman"]),
    # Gorakhpur
    T(slug="gorakhnath-temple-gorakhpur", name="Gorakhnath Temple, Gorakhpur", deity="Guru Gorakhnath (Nath tradition)", location="Gorakhpur, Uttar Pradesh", state="Uttar Pradesh", glyph="गो", tier="famous", famousFor="Nath peetham · eastern UP mega-search", summary="Gorakhnath Math — heart shrine of the Nath yogi tradition and Gorakhpur city.", mythology="Gorakhnath as immortal guru of the Nath panth; Makar Sankranti khichdi fair feeds lakhs and defines Purvanchal pilgrimage.", lat=26.760, lng=83.370, mapQuery="Gorakhnath Temple Gorakhpur", nearestRail="Gorakhpur Junction", nearestAirport="Gorakhpur", deityFamilies=["shiva"], festivals=["Makar Sankranti", "Navaratri"]),
    T(slug="geeta-press-gorakhpur", name="Lila Chitra Mandir (Gita Press), Gorakhpur", deity="Radha–Krishna & Ram darbar (exhibition shrines)", location="Gita Press campus, Gorakhpur, Uttar Pradesh", state="Uttar Pradesh", glyph="गी", tier="regional", famousFor="Gita Press pilgrimage · illustrated Ramayana search", summary="Gita Press Lila Chitra — visual Ramayana–Mahabharata gallery with shrine worship.", mythology="Pilgrims combine Gita Press book purchase with darshan of painted lilas; a cultural tirtha of Hindi belt devotion.", lat=26.780, lng=83.380, mapQuery="Gita Press Gorakhpur", nearestRail="Gorakhpur Junction", nearestAirport="Gorakhpur", deityFamilies=["krishna", "rama"]),
    T(slug="vishnu-mandir-gorakhpur", name="Vishnu Mandir, Gorakhpur", deity="Lord Vishnu", location="Golghar, Gorakhpur, Uttar Pradesh", state="Uttar Pradesh", glyph="व", tier="regional", famousFor="City Vishnu shrine · Gorakhpur local search", summary="Golghar Vishnu Mandir — established Vaishnava temple of Gorakhpur old city.", mythology="Ekadashi and Vaikuntha Ekadashi draw Purvanchal Vaishnavas after Gorakhnath darshan.", lat=26.750, lng=83.380, mapQuery="Vishnu Mandir Gorakhpur", nearestRail="Gorakhpur Junction", nearestAirport="Gorakhpur", deityFamilies=["vishnu"]),
    # Siliguri
    T(slug="iskcon-siliguri", name="ISKCON Temple, Siliguri", deity="Krishna–Radha (ISKCON)", location="Siliguri, West Bengal", state="West Bengal", glyph="इ", tier="regional", famousFor="North Bengal ISKCON · Siliguri family search", summary="ISKCON Siliguri — Krishna temple serving North Bengal and Sikkim gateway travellers.", mythology="Kirtan and prasadam for tea-belt workers and tourists en route to Darjeeling and Sikkim.", lat=26.720, lng=88.410, mapQuery="ISKCON Temple Siliguri", nearestRail="Siliguri Junction", nearestAirport="Bagdogra", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    T(slug="kali-mandir-siliguri", name="Kali Mandir, Siliguri", deity="Goddess Kali", location="Siliguri, West Bengal", state="West Bengal", glyph="का", tier="regional", famousFor="Siliguri city Kali · North Bengal Shakta search", summary="Kali Mandir — active Shakta shrine of Siliguri’s Bengali community.", mythology="Kali as fierce mother of the frontier city; Kali Puja and Amavasya arati define local calendar.", lat=26.710, lng=88.430, mapQuery="Kali Mandir Siliguri", nearestRail="Siliguri Junction", nearestAirport="Bagdogra", deityFamilies=["kali", "devi"]),
    T(slug="shiv-mandir-siliguri", name="Shiv Mandir, Siliguri", deity="Lord Shiva", location="Siliguri, West Bengal", state="West Bengal", glyph="श", tier="regional", famousFor="City centre Shiva · Siliguri Monday search", summary="Central Siliguri Shiva temple for local Hindi–Bengali devotees.", mythology="Urban Shaiva seat for traders and transport workers of the corridor town.", lat=26.730, lng=88.420, mapQuery="Shiv Mandir Siliguri", nearestRail="Siliguri Junction", nearestAirport="Bagdogra", deityFamilies=["shiva"]),
    # Tirunelveli
    T(slug="nellaiappar-tirunelveli", name="Nellaiappar Temple, Tirunelveli", deity="Lord Shiva (Nellaiappar) & Kanthimathi Amman", location="Tirunelveli, Tamil Nadu", state="Tamil Nadu", glyph="ने", tier="famous", famousFor="Tamirabarani Shiva · among TN’s great twin temples", summary="Nellaiappar–Kanthimathi — massive Shiva–Parvati complex on the Tamirabarani.", mythology="Sangam-era capital temple with musical pillars and golden lily tank; Shivaratri and Thaipoosam scale city life.", lat=8.714, lng=77.682, mapQuery="Nellaiappar Temple Tirunelveli", nearestRail="Tirunelveli Junction", nearestAirport="Tuticorin / Madurai", deityFamilies=["shiva", "devi"]),
    T(slug="gandhimathi-krishnapuram", name="Gandhimathi Amman Temple, Krishnapuram", deity="Goddess Gandhimathi Amman", location="Krishnapuram, Tirunelveli, Tamil Nadu", state="Tamil Nadu", glyph="ग", tier="regional", famousFor="Krishnapuram Amman · Tirunelveli rural search", summary="Gandhimathi Amman — powerful village Goddess shrine near Tirunelveli.", mythology="Amman festivals with fire-walk and kavadi draw Tirunelveli district agrarian communities.", lat=8.650, lng=77.720, mapQuery="Gandhimathi Amman Temple Krishnapuram", nearestRail="Tirunelveli", nearestAirport="Tuticorin", deityFamilies=["devi"]),
    T(slug="kurukkuthurai-murugan-tirunelveli", name="Kurukkuthurai Murugan Temple", deity="Lord Murugan", location="Kurukkuthurai, Tirunelveli, Tamil Nadu", state="Tamil Nadu", glyph="मु", tier="regional", famousFor="Tamirabarani riverside Murugan · Tirunelveli local yatra", summary="Kurukkuthurai Murugan — riverside Skanda shrine on the Tamirabarani near Tirunelveli town.", mythology="Devotees bathe in the Tamirabarani and climb to Murugan’s riverside abode; Skanda Shashti and Panguni processions keep Tirunelveli’s Murugan trail alive beside Nellaiappar.", lat=8.728, lng=77.708, mapQuery="Kurukkuthurai Murugan Temple Tirunelveli", nearestRail="Tirunelveli", nearestAirport="Tuticorin", deityFamilies=["murugan"]),
    # Kumbakonam
    T(slug="adi-kumbeswarar-kumbakonam", name="Adi Kumbeswarar Temple, Kumbakonam", deity="Lord Shiva (Adi Kumbeswarar)", location="Kumbakonam, Tamil Nadu", state="Tamil Nadu", glyph="कु", tier="famous", famousFor="Mahamaham tank Shiva · Kumbakonam namesake search", summary="Adi Kumbeswarar — the Shiva who gives Kumbakonam its sacred name.", mythology="Legend of the kumba (pot) of amrita spilling here; Mahamaham festival every 12 years is a South Indian kumbh-scale event.", lat=10.959, lng=79.374, mapQuery="Adi Kumbeswarar Temple Kumbakonam", nearestRail="Kumbakonam", nearestAirport="Tiruchirappalli", deityFamilies=["shiva"], festivals=["Mahamaham", "Maha Shivaratri"]),
    T(slug="sarangapani-kumbakonam", name="Sarangapani Temple, Kumbakonam", deity="Lord Vishnu (Sarangapani)", location="Kumbakonam, Tamil Nadu", state="Tamil Nadu", glyph="स", tier="famous", famousFor="Tallest Vaishnava gopuram in town · Divya Desam search", summary="Sarangapani — premier Vishnu temple of Kumbakonam with chariot festival.", mythology="Vishnu reclines as Sarangapani; Vaikunta Ekadashi and car festival anchor the Vaishnava half of temple-town yatra.", lat=10.961, lng=79.378, mapQuery="Sarangapani Temple Kumbakonam", nearestRail="Kumbakonam", nearestAirport="Tiruchirappalli", deityFamilies=["vishnu"]),
    T(slug="oppiliappan-kumbakonam", name="Oppiliappan Temple, Thirunageswaram", deity="Lord Vishnu (Oppiliappan)", location="Thirunageswaram, Kumbakonam, Tamil Nadu", state="Tamil Nadu", glyph="ओ", tier="famous", famousFor="Salt-free prasadam legend · Kumbakonam Divya Desam search", summary="Oppiliappan — Vishnu who accepts offerings without salt near Kumbakonam.", mythology="Wedding lore of Markandeya’s daughter with Vishnu; ‘uppu illadha’ prasadam tradition is famous across Tamil Nadu.", lat=10.972, lng=79.420, mapQuery="Oppiliappan Temple Thirunageswaram", nearestRail="Kumbakonam", nearestAirport="Tiruchirappalli", deityFamilies=["vishnu"]),
    # Salem
    T(slug="kailasanathar-salem", name="Kailasanathar Temple, Salem", deity="Lord Shiva (Kailasanathar)", location="Salem, Tamil Nadu", state="Tamil Nadu", glyph="क", tier="regional", famousFor="Fort-area Shiva · Salem city search", summary="Kailasanathar — historic Shiva temple of Salem old town.", mythology="Shaiva seat of the Kongu–Salem corridor; Annadhanam and Pradosham draw textile-city devotees.", lat=11.664, lng=78.146, mapQuery="Kailasanathar Temple Salem", nearestRail="Salem Junction", nearestAirport="Salem / Coimbatore", deityFamilies=["shiva"]),
    T(slug="sugavaneshwarar-salem", name="Sugavaneshwarar Temple, Salem", deity="Lord Shiva (Sugavaneshwarar)", location="Salem, Tamil Nadu", state="Tamil Nadu", glyph="सु", tier="regional", famousFor="Salem heritage Shiva · local pradosham search", summary="Sugavaneshwarar — Chola-era Shiva temple in Salem.", mythology="Name recalls sage Sugavan’s worship; stone architecture and living puja sustain Salem’s Shaiva identity.", lat=11.650, lng=78.150, mapQuery="Sugavaneshwarar Temple Salem", nearestRail="Salem Junction", nearestAirport="Salem", deityFamilies=["shiva"]),
    T(slug="periya-mariamman-salem", name="Periya Mariamman Temple, Salem", deity="Goddess Mariamman", location="Salem, Tamil Nadu", state="Tamil Nadu", glyph="प", tier="famous", famousFor="Fire-walk Amman · Salem festival search", summary="Periya Mariamman — major Amman temple with intense summer festival.", mythology="Mariamma as smallpox protector; fire-pit walking and lime pot rituals define Salem’s Shakta public culture.", lat=11.660, lng=78.160, mapQuery="Periya Mariamman Temple Salem", nearestRail="Salem Junction", nearestAirport="Salem", deityFamilies=["devi"]),
    # Erode
    T(slug="sangameswarar-bhavani", name="Sangameswarar Temple, Bhavani", deity="Lord Shiva (Sangameswarar)", location="Bhavani, Erode, Tamil Nadu", state="Tamil Nadu", glyph="सं", tier="famous", famousFor="Kooduthurai confluence Shiva · Erode district search", summary="Sangameswarar — Shiva at the Cauvery–Bhavani–Amudha sangam.", mythology="Triveni sangam lore like a Tamil Prayag; Aadi Perukku and Shivaratri draw confluence bathers to the temple ghat.", lat=11.450, lng=77.680, mapQuery="Sangameswarar Temple Bhavani", nearestRail="Erode / Bhavani", nearestAirport="Coimbatore", deityFamilies=["shiva"]),
    T(slug="thindal-murugan-erode", name="Thindal Murugan Temple, Erode", deity="Lord Murugan", location="Thindal, Erode, Tamil Nadu", state="Tamil Nadu", glyph="थ", tier="famous", famousFor="Hill Murugan above Erode · Thaipusam search", summary="Thindal Murugan — visible hill temple overlooking Erode city.", mythology="Murugan with valli–deivanai tradition; Thaipusam kavadi from Erode textile workers fills the hill road.", lat=11.330, lng=77.690, mapQuery="Thindal Murugan Temple Erode", nearestRail="Erode Junction", nearestAirport="Coimbatore", deityFamilies=["murugan"], festivals=["Thaipusam"]),
    T(slug="periya-mariamman-erode", name="Periya Mariamman Temple, Erode", deity="Goddess Mariamman", location="Erode, Tamil Nadu", state="Tamil Nadu", glyph="प", tier="regional", famousFor="Erode city Amman · Panguni festival search", summary="Periya Mariamman — central Amman shrine of Erode.", mythology="Procession through textile market streets during summer festival; Amman as guardian of Erode’s commerce and health.", lat=11.340, lng=77.720, mapQuery="Periya Mariamman Temple Erode", nearestRail="Erode Junction", nearestAirport="Coimbatore", deityFamilies=["devi"]),
    # Warangal (+2)
    T(slug="bhadrakali-warangal", name="Bhadrakali Temple, Warangal", deity="Goddess Bhadrakali", location="Warangal, Telangana", state="Telangana", glyph="भ", tier="famous", famousFor="Kakatiya-era Devi · Warangal city search", summary="Bhadrakali — hilltop Devi temple with lake view in Warangal.", mythology="Kakatiya kings patronised the Goddess; Bonalu and Navaratri revive Telangana’s Shakta public culture here.", lat=17.990, lng=79.590, mapQuery="Bhadrakali Temple Warangal", nearestRail="Warangal", nearestAirport="Hyderabad", deityFamilies=["devi", "kali"]),
    T(slug="padmakshi-warangal", name="Padmakshi Temple, Hanamkonda", deity="Goddess Padmakshi", location="Hanamkonda, Warangal, Telangana", state="Telangana", glyph="प", tier="regional", famousFor="Jain-Hindu heritage hill · Warangal search", summary="Padmakshi Gutta — hill temple with Jain and Shakta layers in Hanamkonda.", mythology="Annual jatara and bonalu connect Padmakshi to Warangal’s layered sacred geography beside Thousand Pillar temple.", lat=18.010, lng=79.560, mapQuery="Padmakshi Temple Warangal", nearestRail="Warangal", nearestAirport="Hyderabad", deityFamilies=["devi"]),
    # Vijayawada (+2)
    T(slug="undavalli-caves-vijayawada", name="Undavalli Cave Temples", deity="Lord Vishnu (Anantasayana) & Trimurti caves", location="Undavalli, Vijayawada, Andhra Pradesh", state="Andhra Pradesh", glyph="उ", tier="famous", famousFor="Rock-cut Anantasayana · Vijayawada day-trip search", summary="Undavalli caves — multi-storey rock temple with reclining Vishnu overlooking the Krishna river.", mythology="Gupta-era carving later layered with Vijayanagara patronage; river-view darshan pairs with Kanaka Durga hill.", lat=16.496, lng=80.581, mapQuery="Undavalli Caves Vijayawada", nearestRail="Vijayawada Junction", nearestAirport="Vijayawada", deityFamilies=["vishnu"]),
    T(slug="iskcon-vijayawada", name="ISKCON Temple, Vijayawada", deity="Krishna–Radha (ISKCON)", location="Gunadala, Vijayawada, Andhra Pradesh", state="Andhra Pradesh", glyph="इ", tier="regional", famousFor="Krishna hill temple · Vijayawada family search", summary="ISKCON Vijayawada — hilltop Krishna temple above the city.", mythology="Gaudiya kirtan and annadanam serve Andhra families after Kanaka Durga darshan on Krishna river ghats.", lat=16.520, lng=80.620, mapQuery="ISKCON Temple Vijayawada", nearestRail="Vijayawada Junction", nearestAirport="Vijayawada", deityFamilies=["krishna", "vishnu"], tags_extra=["modern-temples"]),
    # Visakhapatnam (+2)
    T(slug="sampath-vinayaka-vizag", name="Sampath Vinayaka Temple, Visakhapatnam", deity="Lord Ganesha (Sampath Vinayaka)", location="Asilmetta, Visakhapatnam, Andhra Pradesh", state="Andhra Pradesh", glyph="स", tier="famous", famousFor="City-centre Ganesh · Vizag Tuesday search", summary="Sampath Vinayaka — beloved urban Ganesh of Visakhapatnam.", mythology="Named from early sponsor family tradition; modak sales and vehicle blessings mark Vizag’s daily Vinayaka culture.", lat=17.720, lng=83.310, mapQuery="Sampath Vinayaka Temple Vizag", nearestRail="Visakhapatnam", nearestAirport="Visakhapatnam", deityFamilies=["ganesha"]),
    T(slug="kali-temple-vizag", name="Kali Temple, Visakhapatnam", deity="Goddess Kali", location="Jagadamba Junction, Visakhapatnam, Andhra Pradesh", state="Andhra Pradesh", glyph="का", tier="regional", famousFor="Jagadamba Kali · Vizag Shakta search", summary="Jagadamba Kali temple — city Shakta shrine near the RTC complex.", mythology="Kali worship adapted to port-city life; Amavasya and Navaratri arati draw Vizag’s Bengali and Telugu communities.", lat=17.710, lng=83.300, mapQuery="Kali Temple Visakhapatnam", nearestRail="Visakhapatnam", nearestAirport="Visakhapatnam", deityFamilies=["kali", "devi"]),
    # Madurai (+2)
    T(slug="koodal-azhagar-madurai", name="Koodal Azhagar Temple, Madurai", deity="Lord Vishnu (Koodal Azhagar)", location="Madurai, Tamil Nadu", state="Tamil Nadu", glyph="कू", tier="famous", famousFor="Madurai Vishnu in sitting posture · Divya Desam search", summary="Koodal Azhagar — ancient Vishnu temple in the heart of Madurai near Meenakshi.", mythology="Azhagar in sitting, standing, and reclining forms in one murti tradition; Chitrai festival links with Alagar Koyil procession.", lat=9.914, lng=78.119, mapQuery="Koodal Azhagar Temple Madurai", nearestRail="Madurai Junction", nearestAirport="Madurai", deityFamilies=["vishnu"]),
    T(slug="alagar-kovil-madurai", name="Alagar Kovil (Alagar Temple)", deity="Lord Vishnu (Kallalagar)", location="Alagar Koyil, Madurai, Tamil Nadu", state="Tamil Nadu", glyph="अ", tier="famous", famousFor="Chitrai festival procession · Madurai Vaishnava search", summary="Alagar Kovil — hill Vishnu temple whose Chitrai procession into Madurai is legendary.", mythology="Kallalagar descends to Solaimalai hill and enters the Vaigai in festival memory; among Tamil Nadu’s great temple processions.", lat=10.050, lng=78.210, mapQuery="Alagar Kovil Madurai", nearestRail="Madurai", nearestAirport="Madurai", deityFamilies=["vishnu"], festivals=["Chitrai Festival"]),
    T(slug="thiruparankundram-murugan", name="Thiruparankundram Murugan Temple", deity="Lord Murugan (Subramanya)", location="Thiruparankundram, Madurai, Tamil Nadu", state="Tamil Nadu", glyph="थ", tier="famous", famousFor="Rock-cut Murugan · Arupadai Veedu search", summary="Thiruparankundram — first of Murugan’s six abodes, carved in a hill near Madurai.", mythology="Murugan married Deivanai here after Surapadma battle in tradition; cave sanctum and hill sunset draw constant worship.", lat=9.890, lng=78.070, mapQuery="Thiruparankundram Murugan Temple", nearestRail="Madurai Junction", nearestAirport="Madurai", deityFamilies=["murugan"], festivals=["Skanda Shashti", "Thaipusam"]),
    # Mysuru (+2)
    T(slug="trinesvaraswamy-mysuru", name="Trinesvaraswamy Temple, Mysuru", deity="Lord Shiva (Trinesvaraswamy)", location="Mysuru Palace premises, Mysuru, Karnataka", state="Karnataka", glyph="त्र", tier="famous", famousFor="Palace-adjacent Shiva · Mysuru Dasara search", summary="Trinesvaraswamy — historic Shiva temple within the Mysuru palace complex.", mythology="Shiva as three-eyed lord watched over the Wodeyar kingdom; Dasara processions begin with palace deity honours.", lat=12.305, lng=76.655, mapQuery="Trinesvaraswamy Temple Mysore", nearestRail="Mysuru Junction", nearestAirport="Mysuru", deityFamilies=["shiva"]),
    T(slug="prasanna-krishnaswamy-mysuru", name="Prasanna Krishnaswamy Temple, Mysuru", deity="Lord Krishna (Prasanna Krishnaswamy)", location="Mysuru, Karnataka", state="Karnataka", glyph="प्र", tier="regional", famousFor="Wodeyar Krishna · Mysuru palace temple search", summary="Prasanna Krishnaswamy — Krishna temple established by Wodeyar queens.", mythology="Krishna with flute in a serene palace-quarter shrine; Janmashtami and Dasara evenings add music to darshan.", lat=12.303, lng=76.653, mapQuery="Prasanna Krishnaswamy Temple Mysore", nearestRail="Mysuru Junction", nearestAirport="Mysuru", deityFamilies=["krishna", "vishnu"]),
    # Kolhapur (+2)
    T(slug="jyotiba-temple-kolhapur", name="Jyotiba Temple, Kolhapur", deity="Lord Jyotiba (Shiva–Khandoba form)", location="Jyotiba hill, Kolhapur, Maharashtra", state="Maharashtra", glyph="ज", tier="famous", famousFor="Full-moon fair lakhs · Kolhapur hill search", summary="Jyotiba — hill shrine whose Chaitra Purnima fair is among Maharashtra’s largest.", mythology="Jyotiba as luminous form linked to Shiva and regional Khandoba streams; night torches on the hill are iconic.", lat=16.700, lng=74.150, mapQuery="Jyotiba Temple Kolhapur", nearestRail="Kolhapur", nearestAirport="Kolhapur / Goa", deityFamilies=["shiva"], festivals=["Chaitra Purnima"]),
    T(slug="kopeshwar-khidrapur", name="Kopeshwar Temple, Khidrapur", deity="Lord Shiva (Kopeshwar)", location="Khidrapur, Kolhapur district, Maharashtra", state="Maharashtra", glyph="को", tier="famous", famousFor="Chalukya–Hemadpanthi marvel · Krishna river search", summary="Kopeshwar — stunning mandapa with pillars and open-sky garbhagriha on the Krishna river.", mythology="12th-century temple architecture draws art pilgrims who also take darshan of the swayambhu Shiva.", lat=16.610, lng=74.530, mapQuery="Kopeshwar Temple Khidrapur", nearestRail="Kolhapur / Miraj", nearestAirport="Kolhapur", deityFamilies=["shiva"]),
    T(slug="temblai-devi-kolhapur", name="Temblai Devi Temple, Kolhapur", deity="Goddess Temblai", location="Temblai Hill, Kolhapur, Maharashtra", state="Maharashtra", glyph="ते", tier="regional", famousFor="Kolhapur ridge Devi · Navaratri search", summary="Temblai Devi — hill Goddess shrine overlooking Kolhapur basin.", mythology="Temblai as guardian of the plain beside Mahalaxmi; local Navaratri lamp trails circle the ridge.", lat=16.680, lng=74.210, mapQuery="Temblai Devi Temple Kolhapur", nearestRail="Kolhapur", nearestAirport="Kolhapur", deityFamilies=["devi"]),
    # Tirupati (+2)
    T(slug="padmavathi-tiruchanur", name="Padmavathi Temple, Tiruchanur", deity="Goddess Padmavathi (Alamelu Manga)", location="Tiruchanur, Tirupati, Andhra Pradesh", state="Andhra Pradesh", glyph="प", tier="famous", famousFor="Tirupati consort darshan · mandatory paired yatra search", summary="Padmavathi Ammavari Temple at Tiruchanur — consort of Venkateswara.", mythology="Pilgrimage etiquette visits Tiruchanur after Tirumala; Padmavathi’s lotus-origin lore completes Srinivasa kalyanam memory.", lat=13.612, lng=79.420, mapQuery="Padmavathi Temple Tiruchanur", nearestRail="Tirupati", nearestAirport="Tirupati", deityFamilies=["devi", "venkateswara", "lakshmi"], festivals=["Panchami Teertham", "Navaratri"]),
    T(slug="govindaraja-tirupati", name="Govindaraja Swamy Temple, Tirupati", deity="Lord Vishnu (Govindaraja)", location="Tirupati, Andhra Pradesh", state="Andhra Pradesh", glyph="गो", tier="famous", famousFor="Old Tirupati Vishnu · before Tirumala hill search", summary="Govindaraja Swamy — historic Vishnu temple in Tirupati town below the hills.", mythology="Chola-era Vaishnava centre predating Tirumala’s medieval rise; Brahmotsavam and Rath Yatra anchor town life.", lat=13.630, lng=79.420, mapQuery="Govindaraja Swamy Temple Tirupati", nearestRail="Tirupati", nearestAirport="Tirupati", deityFamilies=["vishnu", "venkateswara"]),
    # Nashik (+1)
    T(slug="kalaram-temple-nashik", name="Kalaram Temple, Nashik", deity="Lord Rama (Kalaram)", location="Panchvati, Nashik, Maharashtra", state="Maharashtra", glyph="क", tier="famous", famousFor="Black-stone Rama of Panchvati · Nashik Kumbh search", summary="Kalaram Mandir — black stone Rama–Sita–Laxman in Nashik’s Panchvati.", mythology="Ramayana geography of exile forest; Kumbh Mela crowds and daily Ram bhakti define Nashik’s sacred quarter.", lat=20.010, lng=73.790, mapQuery="Kalaram Temple Nashik", nearestRail="Nashik Road", nearestAirport="Nashik / Mumbai", deityFamilies=["rama"]),
    # Raipur (+2)
    T(slug="dudhadhari-math-raipur", name="Dudhadhari Math & Temple, Raipur", deity="Lord Rama (Dudhadhari tradition)", location="Raipur, Chhattisgarh", state="Chhattisgarh", glyph="द", tier="famous", famousFor="Raipur’s premier math · Chhattisgarh city search", summary="Dudhadhari Math — Rama-centred monastery with ornate temple architecture.", mythology="Named from dudh–hari devotion metaphor; Ram Navami and city festivals radiate from this old Raipur seat.", lat=21.240, lng=81.630, mapQuery="Dudhadhari Math Raipur", nearestRail="Raipur Junction", nearestAirport="Raipur", deityFamilies=["rama", "vishnu"]),
    T(slug="mahamaya-temple-raipur", name="Mahamaya Temple, Raipur", deity="Goddess Mahamaya", location="Raipur, Chhattisgarh", state="Chhattisgarh", glyph="म", tier="regional", famousFor="Raipur city Devi · Chhattisgarh capital search", summary="Mahamaya — active Devi temple of Raipur distinct from Ratanpur’s historic seat.", mythology="City Goddess for Chhattisgarh’s capital; Navaratri and Durga Puja crowds spill into Raipur’s new market areas.", lat=21.250, lng=81.640, mapQuery="Mahamaya Temple Raipur", nearestRail="Raipur Junction", nearestAirport="Raipur", deityFamilies=["devi"]),
]

NEW_STORY_SLUGS = [
    "khajrana-ganesh-indore",
    "gorakhnath-baba",
    "manasa-chandi-haridwar",
    "perur-pateeswarar",
    "marudhamalai-murugan",
    "nellaiappar-tirunelveli",
    "kumbeswarar-kumbakonam",
    "tekdi-ganesh-nagpur",
    "koradi-temple-story",
    "tapkeshwar-dehradun",
    "chamunda-jodhpur",
    "padmavathi-tiruchanur",
    "thiruparankundram-murugan",
    "jyotiba-kolhapur",
]


def expand_detail(short_en: str, short_hi: str, hook: str, hook_hi: str, why: str, why_hi: str, takeaway: str, title: str, title_hi: str) -> tuple[str, str]:
    """Build ~300-word narrative expansions without SEO boilerplate."""
    detail_en = (
        f"{short_en}\n\n"
        f"Elders at home often begin with the line: {hook} "
        f"The middle of the telling is where doubt and devotion meet — not to prove history like a court, "
        f"but to shape tomorrow's patience.\n\n"
        f"{short_en.split('.')[0] if short_en else title}. "
        f"Children ask why the shrine still matters; the answer is in the queue, the modak, the thread tied after a vow kept. "
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
        dict(
            slug="khajrana-ganesh-indore",
            title="Khajrana Ganesh and the buried murti",
            titleHi="खजराना गणेश और दबी मूर्ति",
            deity="ganesha",
            hook="A dream pointed to earth — and Indore found its Ganesh.",
            hookHi="स्वप्न ने धरती दिखाई — और इंदौर को अपना गणेश मिला।",
            whyRitual="Wednesday and Angarki Chaturthi modak offerings remember the revealed Vinayaka of Khajrana.",
            whyRitualHi="बुध और अंगारकी पर मोदक — खजराना के प्रकट विनायक की स्मृति।",
            storyEn="In nineteenth-century Indore, a devotee named Pandit Mangal Bhatt dreamed that a Ganesh murti lay buried where the city would later grow. Digging at Khajrana revealed a swayambhu Ganesh in the earth. The shrine began as a simple tent; today it is among central India's most visited Vinayaka seats. Modak and laddoo sellers line the lane because families believe the first obstacle-remover of the city listens to honest vows. The sthala does not claim a Puranic battle — it claims discovery, patience, and the faith of a town that kept digging.",
            storyHi="उन्नीसवीं सदी के इंदौर में मंगल भट्ट जी को स्वप्न आया — खजराना की धरती में गणेश विराजमान हैं। खुदाई से स्वयंभू मूर्ति प्रकट हुई। तंबू से शुरू हुआ मंदिर आज मध्य भारत के प्रमुख विनायक तीर्थों में है। मोदक–लड्डू की लकीर इसलिए — परिवार मानते हैं नगर का विघ्नहर्ता सच्ची मन्नत सुनता है। यह कथा युद्ध नहीं, खोज, धैर्य और नगर की श्रद्धा की है।",
            takeaway="Before a new venture, offer one modak at home remembering Khajrana — begin with gratitude, not haste.",
            relatedTemples=["khajrana-ganesh-indore", "eachanari-vinayagar", "tekdi-ganesh-nagpur"],
        ),
        dict(
            slug="gorakhnath-baba",
            title="Gorakhnath and the fire that never dies",
            titleHi="गोरक्षनाथ और अखंड धूनी",
            deity="shiva",
            hook="A yogi whose name guards a city — and a kitchen that feeds millions.",
            hookHi="एक योगी जिसका नाम नगर रखता है — और रसोई जो लाखों को भोजन देती है।",
            whyRitual="Makar Sankranti khichdi at Gorakhnath Math remembers the Nath tradition of sacred hospitality.",
            whyRitualHi="मकर संक्रांति की खिचड़ी — नाथ परंपरा की पावन अतिथि सेवा।",
            storyEn="Gorakhnath is remembered as the immortal guru of the Nath panth — disciple of Matsyendranath, teacher of Raja Bhartrihari and countless householders who sought yoga without leaving devotion. Purvanchal's great math at Gorakhpur bears his name; the eternal dhuni is tended day and night. On Makar Sankranti, khichdi cauldrons feed lakhs — not spectacle alone, but the Nath vow that no pilgrim should leave hungry. Shiva appears in this path as the adinath behind the guru; the city itself becomes a tirtha of discipline, breath, and shared meal.",
            storyHi="गोरक्षनाथ जी नाथ संप्रदाय के अमर गुरु — मत्स्येन्द्रनाथ के शिष्य, भर्तृहरि और अनगिनत गृहस्थों के उपदेशक। गोरखपुर की महान् मठ में अखंड धूनी; मकर संक्रांति पर खिचड़ी से लाखों का भोजन — केवल तमाशा नहीं, नाथ व्रत कि भूखा तीर्थी न लौटे। शिव यहाँ आदिनाथ; नगर अनुशासन, प्राण और अन्न का तीर्थ बन जाता है।",
            takeaway="On Sankranti, share a simple meal with a neighbour — Gorakhnath's math begins in the kitchen, not the podium.",
            relatedTemples=["gorakhnath-temple-gorakhpur"],
        ),
        dict(
            slug="manasa-chandi-haridwar",
            title="Mansa and Chandi — the two hills of Haridwar",
            titleHi="मनसा और चंडी — हरिद्वार की दो पहाड़ियाँ",
            deity="devi",
            hook="Two Goddesses on two hills — wishes on one side, courage on the other.",
            hookHi="दो पहाड़ियों पर दो देवियाँ — एक ओर मन्नत, दूसरी ओर साहस।",
            whyRitual="Haridwar yatris climb Bilwa and Neel Parvat tying threads at Mansa and ringing bells at Chandi.",
            whyRitualHi="तीर्थी बिल्व और नील पर्वत चढ़कर मनसा पर डोर बाँधते, चंडी की घंटी बजाते हैं।",
            storyEn="Haridwar's skyline is guarded by two Devi hills. Mansa Devi on Bilwa Parvat is the wish-granting mother — devotees tie threads when vows are made and return to untie them when boons arrive. Across the Ganga, Chandi Devi on Neel Parvat remembers the Goddess who destroyed Chanda and Munda; Skanda Purana memory places her victory here above the sacred city. Maya Devi in the old town forms a third Shakta anchor. Together they teach that pilgrimage is not one darshan but a conversation between fear, hope, and release.",
            storyHi="हरिद्वार की क्षितिज दो देवी पहाड़ियाँ रखती है। बिल्व पर मनसा मन्नत पूरी करती हैं — डोर बाँधकर लौटते हैं। गंगा के पार नील पर्वत पर चंडी चंड–मुंड वध की स्मृति; स्कंद पुराण इस विजय को यहीं मानता है। माया देवी तीसरा शाक्त anchor। तीर्थ एक दर्शन नहीं — भय, आशा, मोक्ष की बातचीत।",
            takeaway="Climb one hill in life slowly — Mansa teaches patience; Chandi teaches courage; both are needed.",
            relatedTemples=["mansa-devi-haridwar", "chandi-devi-haridwar", "maya-devi-haridwar"],
        ),
    ]
    # Append remaining stories in compact form
    more = [
        ("perur-pateeswarar", "Patteeswarar and Karaikkal Ammaiyar", "पट्टीश्वर और कारैक्कल अम्मैयार", "shiva",
         "A Chola roof of gold remembers a woman's walk on her hands to Shiva.", "सोने की छत — हाथों पर चलकर शिव तक पहुँचने वाली अम्मैयार की स्मृति।",
         "Perur's Patteeswarar temple holds Kongu Nadu's classic Shiva–devotee bond; Karaikkal Ammaiyar's lore ties ascetic love to family life refused without insult.",
         "पेरुर का पट्टीश्वर कोंगु नाडु का शिव–भक्त बंध; कारैक्कल अम्मैयार की कथा — अपमान रहित त्याग।",
         ["perur-pateeswarar"]),
        ("marudhamalai-murugan", "Murugan of the medicinal hill", "औषधि पर्वत का मुरुगन", "murugan",
         "On a forest hill near Coimbatore, Murugan is healer and commander.", "कोयंबटूर के वन पर्वत पर मुरुगन वैद्य भी, सेनापति भी।",
         "Marudhamalai's name recalls herbs; Murugan as youthful god receives kavadi after illness vows. Thaipusam fills the ghat road with spears and milk pots.",
         "मरुदमलै = औषधि; मुरुगन को रोग मुक्ति की मन्नत; थाइपूसम पर कावड़ी और दूध।",
         ["marudhamalai-murugan", "thiruparankundram-murugan"]),
        ("nellaiappar-tirunelveli", "Nellaiappar and the golden lily tank", "नेलैयप्पर और स्वर्ण कमल ताल", "shiva",
         "Where the Tamirabarani flows, Shiva and Kanthimathi share a city-sized temple.", "ताम्रपarni किनारे शिव–कंठिमathi का नगर-विशाल मंदिर।",
         "Musical pillars and the golden lotus tank make Nellaiappar a living concert of stone; Shivaratri here is the city's heartbeat.",
         "संगीत स्तंभ और स्वर्ण कमल ताल — शिवरात्रि नगर की धड़कन।",
         ["nellaiappar-tirunelveli"]),
        ("kumbeswarar-kumbakonam", "The pot that named Kumbakonam", "कलश जिसने कुंभकुणम नाम दिया", "shiva",
         "When the kumba of amrita tilted, Shiva stayed as Kumbeswarar.", "अमृत कलश झुका — शिव कुम्बेश्वर बनकर रहे।",
         "Mahamaham every twelve years turns the temple tank into a kumbh of the south; Adi Kumbeswarar is the axis.",
         "12 वर्ष में महामहाम — दक्षिण का कुmbh; आदि कुम्बेश्वर केंद्र।",
         ["adi-kumbeswarar-kumbakonam"]),
        ("tekdi-ganesh-nagpur", "Tekdi Ganapati above the rails", "रेल के ऊपर टेकड़ी गणपati", "ganesha",
         "Nagpur climbs a hill for the Ganesh who watches the diamond of India.", "भारत के हृदय में पहाड़ी चढ़कर गणesh darshan।",
         "Sitabuldi tekdi Ganesh receives vehicle blessings and exam vows; Tuesday queues define Vidarbha urban bhakti.",
         "वाहन और परीक्षा की मन्नत; मंगल की कतार विदarbha की पहचान।",
         ["tekdi-ganesh-nagpur"]),
        ("koradi-temple-story", "Jagdamba of Koradi", "कोरadi की जगदamba", "devi",
         "Navaratri at Koradi fills the horizon with lamps for Jagdamba.", "नवरात्रि पर कोरadi में जगदamba के दीप क्षितij भर देते हैं।",
         "Mahalakshmi Jagdamba of Koradi is mother of Vidarbha; the fair after Navami is among Maharashtra's largest Devi gatherings.",
         "विदarbha की माँ; नवमी के बाद का मेला महाराष्ट्र के बड़े शक्ति समागमों में।",
         ["koradi-temple-nagpur"]),
        ("tapkeshwar-dehradun", "Tapkeshwar — Shiva in the dripping cave", "टपकेश्वर — टप-टप लिंग की गुफा", "shiva",
         "Water falls on the lingam drop by drop in Drona's cave.", "द्रोण गुफा में लिंग पर बूँद-बूँद जल।",
         "Tapkeshwar Mahadev in Dehradun forest recalls ashram lore; Shivaratri lamps multiply in the dripping dark.",
         "देहरादून वन में अश्रम स्मृति; शिवरात्रि की ज्योति गुफा में।",
         ["tapkeshwar-mahadev-dehradun"]),
        ("chamunda-jodhpur", "Chamunda of Mehrangarh", "मेहरानगढ़ की चामुंडा", "devi",
         "The fort's kuldevi rides out on Dussehra — blue city, red sand.", "दशहरा पर कुलदेवी निकलती हैं — नीला शहर, लाल रेत।",
         "Rao Jodha moved Chamunda into Mehrangarh; her procession to the city is Jodhpur's sacred calendar peak.",
         "राव जोधा ने चामुंडा को किले में स्थापित; जुलूस नगर की मुख्य रीति।",
         ["chamunda-mata-jodhpur"]),
        ("padmavathi-tiruchanur", "Padmavathi and the lotus bride", "पadmavathi — कमल-वधू", "venkateswara",
         "Tirumala's yatra completes at Tiruchanur — the consort on the lotus.", "तिरुमala की यातra तiruchanur में — कमल पर consort।",
         "Padmavathi appeared from lotus in Srinivasa kalyanam memory; etiquette demands darshan here after Venkateswara hill.",
         "श्रीनिवास कalyanam में कमल से प्रकट; तirumala के बाद etiquette यहीं।",
         ["padmavathi-tiruchanur", "tirumala-venkateswara", "govindaraja-tirupati"]),
        ("thiruparankundram-murugan", "Murugan wed on the rock hill", "चट्टान पर्वत पर मुरुगन विवाह", "murugan",
         "First of the six abodes — cave sanctum, spear, sunset.", "छह स्थानों में पहला — गुफा, शूल, सूर्यास्त।",
         "After Surapadma's defeat, Murugan married Deivanai at Thiruparankundram; devotees climb for marriage blessings.",
         "सुरapadma पर विजय के बाद deivanai विवाह; vivah मन्नत।",
         ["thiruparankundram-murugan", "marudhamalai-murugan"]),
        ("jyotiba-kolhapur", "Jyotiba's torch on the full moon", "पurnima की जyotiba मशaal", "shiva",
         "Chaitra Purnima turns Jyotiba hill into a river of torches.", "चैत्र purnima — मशalon की नदी।",
         "Jyotiba as luminous Shiva–Khandoba form draws Maharashtra's largest hill fair after Kolhapur Mahalaxmi.",
         "kolhapur mahalaxmi के बाद महाराष्ट्र का बड़ा पर्वतीय mela।",
         ["jyotiba-temple-kolhapur", "mahalaxmi-kolhapur"]),
    ]
    for slug, title, title_hi, deity, hook, hook_hi, en, hi, temples in more:
        raw.append(dict(
            slug=slug, title=title, titleHi=title_hi, deity=deity,
            hook=hook, hookHi=hook_hi,
            whyRitual=f"Festival and vow customs at the related shrine remember this telling.",
            whyRitualHi="संबंधित मंदिर की रीति इस कथा को जीवित रखती है।",
            storyEn=en + " Pilgrims carry the story home as practice — lamp, queue, or fair day — not as debate.",
            storyHi=hi + " तीर्थी कथा को अभ्यास में ले जातe हैं — दीप, कतार, मेला — बहस नहीं।",
            takeaway="Read once slowly; tell the short version from memory to a child if one is listening.",
            relatedTemples=temples,
        ))
    out = []
    for r in raw:
        de, dh = expand_detail(
            r["storyEn"], r["storyHi"], r["hook"], r["hookHi"],
            r["whyRitual"], r["whyRitualHi"], r["takeaway"], r["title"], r["titleHi"],
        )
        out.append({
            **r,
            "readSeconds": 320,
            "tags": ["long-read", "first-timer", "family"],
            "storyDetailEn": de,
            "storyDetailHi": dh,
        })
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
        detail["mythologyDisclaimer"] = (
            "Mythological accounts are drawn from Puranic traditions and sthala-purana. "
            "Versions differ by region. For cultural understanding — not historical claim."
        )
    detail["lastUpdated"] = "2026-08-18"
    detail["country"] = detail.get("country") or "India"
    detail["tier"] = detail.get("tier") or "regional"
    if detail.get("lat") and detail.get("lng") and not detail.get("mapQuery"):
        detail["mapQuery"] = detail["name"]
    return detail


def merge_families(existing: list[str], new: list[str]) -> list[str]:
    out = list(existing or [])
    for f in new:
        if f not in out:
            out.append(f)
    return out


def apply_family_overrides(deity_keys: set[str]) -> int:
    updated = 0
    for path in sorted(TEMPLES.glob("*.json")):
        d = load_json(path)
        slug = d["slug"]
        text = " ".join([d.get("name", ""), d.get("deity", ""), d.get("summary", ""), d.get("mythology", "")]).lower()
        fams = list(d.get("deityFamilies") or [])
        if slug in FAMILY_OVERRIDES:
            fams = merge_families(fams, [f for f in FAMILY_OVERRIDES[slug] if f in deity_keys])
        else:
            for keys, add in AUTO_FAMILY_RULES:
                if any(k in text for k in keys):
                    fams = merge_families(fams, [f for f in add if f in deity_keys])
        fams = [f for f in fams if f in deity_keys][:4]
        if fams != d.get("deityFamilies"):
            d["deityFamilies"] = fams
            dump_json(path, d)
            updated += 1
    return updated


def add_deities() -> tuple[int, list[str]]:
    path = DATA / "deities.json"
    data = load_json(path)
    added = []
    for slug, entry in NEW_DEITIES.items():
        if slug not in data:
            data[slug] = entry
            added.append(slug)
    if added:
        dump_json(path, data)
    return len(data), added


def add_temples(deity_keys: set[str]) -> tuple[int, list[str]]:
    existing = {p.stem for p in TEMPLES.glob("*.json")}
    created = []
    for seed in NEW_TEMPLES:
        slug = seed["slug"]
        if slug in existing:
            continue
        tags_extra = seed.pop("tags_extra", None) or []
        tier = seed.pop("tier", "regional")
        fams = seed.pop("deityFamilies", None) or []
        fams = [f for f in fams if f in deity_keys]
        detail = base_detail(dict(seed))
        detail["tier"] = tier
        detail["deityFamilies"] = fams
        tags = list(detail.get("tags") or [])
        for t in tags_extra:
            if t not in tags:
                tags.append(t)
        detail["tags"] = tags
        detail = attach_portal(detail)
        detail = enrich_myth_fields(detail)
        if detail.get("lat") is None:
            raise SystemExit(f"Missing lat for {slug}")
        dump_json(TEMPLES / f"{slug}.json", detail)
        created.append(slug)
        existing.add(slug)
    return len(created), created


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
    rot = data.setdefault("dailyRotation", {})
    stories = rot.setdefault("story", [])
    n = 0
    for slug in story_slugs:
        if slug not in stories:
            stories.append(slug)
            n += 1
    if n:
        dump_json(path, data)
    return n


def city_counts() -> dict[str, int]:
    from collections import defaultdict

    index = load_json(DATA / "temples.json")
    city_keys = {
        "Indore": ["indore"],
        "Bhopal": ["bhopal"],
        "Nagpur": ["nagpur"],
        "Coimbatore": ["coimbatore"],
        "Surat": ["surat"],
        "Vadodara": ["vadodara", "baroda"],
        "Lucknow": ["lucknow"],
        "Kanpur": ["kanpur"],
        "Gwalior": ["gwalior", "morena", "bateshwar"],
        "Jabalpur": ["jabalpur", "bhedaghat"],
        "Mangaluru": ["mangaluru", "mangalore", "mangaluru"],
        "Hubli-Dharwad": ["hubballi", "hubli", "dharwad", "unkal"],
        "Kozhikode": ["kozhikode", "calicut"],
        "Dehradun": ["dehradun"],
        "Haridwar": ["haridwar"],
        "Jodhpur": ["jodhpur", "mandore"],
        "Kota": ["kota", "garadia"],
        "Gorakhpur": ["gorakhpur"],
        "Siliguri": ["siliguri"],
        "Tirunelveli": ["tirunelveli", "nellai", "krishnapuram"],
        "Kumbakonam": ["kumbakonam", "thirunageswaram"],
        "Salem": ["salem"],
        "Erode": ["erode", "bhavani", "thindal"],
        "Warangal": ["warangal", "hanamkonda"],
        "Vijayawada": ["vijayawada", "undavalli"],
        "Visakhapatnam": ["visakhapatnam", "vizag", "asilmetta"],
        "Madurai": ["madurai", "alagar", "thiruparankundram"],
        "Mysuru": ["mysuru", "mysore"],
        "Kolhapur": ["kolhapur", "khidrapur", "jyotiba"],
        "Tirupati": ["tirupati", "tiruchanur", "tirumala"],
        "Nashik": ["nashik", "panchvati", "trimbak"],
        "Raipur": ["raipur"],
    }
    counts = defaultdict(int)
    for t in index:
        loc = t.get("location", "").lower()
        for city, keys in city_keys.items():
            if any(k in loc for k in keys):
                counts[city] += 1
    return dict(counts)


def main() -> None:
    deity_count, new_deities = add_deities()
    deity_keys = set(load_json(DATA / "deities.json").keys())

    temples_added, temple_slugs = add_temples(deity_keys)
    families_updated = apply_family_overrides(deity_keys)

    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "assign_deities.py")])

    # Re-apply explicit overrides after assign_deities heuristics
    apply_family_overrides(deity_keys)
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])

    stories_added, story_slugs = add_stories()
    engagement_added = update_engagement(story_slugs)

    counts = city_counts()
    sample = {k: counts.get(k, 0) for k in sorted(counts)[:12]}

    print("=== add_tier2_deities_temples summary ===")
    print(f"Deities total: {deity_count} (+{len(new_deities)} new)")
    print(f"New deity slugs: {', '.join(new_deities) or '(none — already present)'}")
    print(f"Temples added: {temples_added}")
    print(f"Family overrides refreshed on {families_updated} detail files (first pass)")
    print(f"Stories added: {stories_added}")
    print(f"Engagement dailyRotation.story appended: {engagement_added}")
    print(f"Sample city temple counts: {sample}")
    if temple_slugs[:8]:
        print("Sample new temples:", ", ".join(temple_slugs[:8]), "...")


if __name__ == "__main__":
    main()

