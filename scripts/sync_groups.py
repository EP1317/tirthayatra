#!/usr/bin/env python3
"""Sync temple tags from groups.json, seed missing temples, validate fixed counts."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES_DIR = DATA / "temples"

# Exact fixed memberships (source of truth for counts)
GROUPS = {
    "12-jyotirlinga": [
        "somnath",
        "mallikarjuna-srisailam",
        "mahakaleshwar-ujjain",
        "omkareshwar",
        "kedarnath",
        "bhimashankar",
        "kashi-vishwanath",
        "trimbakeshwar",
        "vaidyanath-deoghar",
        "nageshwar",
        "rameswaram",
        "grishneshwar",
    ],
    "char-dham": [
        "badrinath",
        "dwarka",
        "jagannath-puri",
        "rameswaram",
    ],
    "chota-char-dham": [
        "yamunotri",
        "gangotri",
        "kedarnath",
        "badrinath",
    ],
    "panch-kedar": [
        "kedarnath",
        "tungnath",
        "rudranath",
        "madhyamaheshwar",
        "kalpeshwar",
    ],
    "pancha-bhuta": [
        "ekambareswarar-kanchipuram",
        "thiruvanaikaval",
        "arunachaleswarar-tiruvannamalai",
        "srikalahasti",
        "nataraja-chidambaram",
    ],
    # Classic Maharashtra Ashtavinayak yatra order (Morgaon start)
    "ashtavinayak": [
        "moreshwar-morgaon",
        "siddhivinayak-siddhatek",
        "ballaleshwar-pali",
        "varadavinayak-mahad",
        "chintamani-theur",
        "girijatmaj-lenyadri",
        "vighnahar-ozar",
        "mahaganapati-ranjangaon",
    ],
    # Pithanirnaya-style 51 list (popular pilgrimage enumeration).
    # Shared complexes reuse the same slug (one detail file).
    "51-shakti-peeth": [
        "amarnath-shakti",
        "attahas",
        "bahula-ketugram",
        "bakreshwar",
        "jagannath-puri",  # Vimala Devi inside Jagannath complex
        "bhabanipur",
        "biraja-jajpur",
        "mithila-janakpur",
        "surkanda-devi",  # Head — Uttarakhand Siddha / popular 51-peetha seat
        "panchsagar-champawat",  # Lower teeth — Champawat (widely listed Himalayan peetha)
        "guhyeshwari",
        "muktinath",  # Gandaki / Muktinath peetha
        "saptashrungi",
        "hinglaj",
        "kalighat",
        "kamakhya",
        "kankalitala",
        "kanyakumari",
        "brajeshwari-kangra",
        "kiriteswari",
        "ratnavali",
        "bhramari-jalpaiguri",
        "manasa-manasarovar",
        "ugratara-mahishi",
        "manibandh-pushkar",
        "indrakshi-nainativu",
        "jayanti-nartiang",
        "jeshoreshwari",
        "jwalamukhi",
        "tara-tarini",
        "prabhas-chandrabhaga",
        "alopi-devi-prayagraj",
        "bhadrakali-kurukshetra",
        "sharada-maihar",
        "nandikeshwari-sainthia",
        "manikyamba-draksharama",
        "naina-devi",
        "shondesh-amarkantak",
        "mallikarjuna-srisailam",  # Bhramaramba at Srisailam complex
        "narayani-suchindram",
        "sugandha-shikarpur",
        "tripura-sundari",
        "ujani-mangalchandika",
        "vishalakshi-kashi",
        "vibhash-tamluk",
        "viraat-ambika",
        "katyayani-vrindavan",
        "tripuramalini-jalandhar",
        "vaidyanath-deoghar",  # heart peetha + Jyotirlinga complex
        "kamakshi-kanchipuram",
        "jogadya-kshirgram",
        "puruhutika-pithapuram",
    ],
}

OPEN_TAGS_KEEP = {
    "ramayana-trail",
    "mahabharata-sites",
    "beyond-india",
    "modern-temples",
}

LABELS = {
    "12-jyotirlinga": "12 Jyotirlinga",
    "51-shakti-peeth": "51 Shakti Peeth",
    "char-dham": "Char Dham",
    "chota-char-dham": "Chota Char Dham",
    "panch-kedar": "Panch Kedar",
    "pancha-bhuta": "Pancha Bhuta",
    "ashtavinayak": "Ashtavinayak",
    "ramayana-trail": "Ramayana Trail",
    "mahabharata-sites": "Mahabharata Sites",
    "beyond-india": "Beyond India",
    "modern-temples": "Modern Temples",
}

CIRCUITS = [
    {
        "slug": "12-jyotirlinga",
        "name": "12 Jyotirlinga",
        "shortName": "Jyotirlinga",
        "countLabel": "12 sacred lingas",
        "blurb": "All twelve Jyotirlingas — Somnath to Grishneshwar — one shared guide per shrine, even when a site also sits on another circuit.",
        "lede": "Complete set of twelve Jyotirlinga temples. Kedarnath also appears in Chota Char Dham and Panch Kedar — same page, same facts.",
        "sanskrit": "द्वादश ज्योतिर्लिङ्ग",
        "expected": 12,
    },
    {
        "slug": "51-shakti-peeth",
        "name": "51 Shakti Peeth",
        "shortName": "Shakti Peeth",
        "countLabel": "52 peethas",
        "blurb": "Shakti Peethas from the popular pilgrimage enumeration across India and neighbouring lands — including Himalayan seats such as Surkanda Devi and Champawat’s Panchsagar.",
        "lede": "Where tradition places Sati’s sacred fragments. Scriptural lists vary (often 51, 52, or 108); TirthaYatra’s circuit includes Surkanda Devi (head) and Panchsagar Champawat among the Himalayan peethas. Overlaps with Jyotirlinga / Char Dham complexes share the same temple guide.",
        "sanskrit": "एकपञ्चाशत् शक्तिपीठ",
        "expected": 52,
    },
    {
        "slug": "char-dham",
        "name": "Char Dham",
        "shortName": "Char Dham",
        "countLabel": "4 dhams",
        "blurb": "Adi Shankaracharya’s four cardinal dhams only: Badrinath, Dwarka, Puri, and Rameswaram — not the Uttarakhand Chota Char Dham.",
        "lede": "Exactly four seats. Kedarnath is not part of this circuit (see Chota Char Dham). Badrinath appears in both Char Dham and Chota Char Dham with the same guide.",
        "sanskrit": "चार धाम",
        "expected": 4,
    },
    {
        "slug": "chota-char-dham",
        "name": "Chota Char Dham",
        "shortName": "Chota Char Dham",
        "countLabel": "4 Himalayan dhams",
        "blurb": "Uttarakhand’s Yamunotri, Gangotri, Kedarnath, and Badrinath — the classic Himalayan Char Dham yatra.",
        "lede": "Do not confuse with Adi Shankaracharya’s pan-India Char Dham. This circuit is the seasonal Uttarakhand pilgrimage.",
        "sanskrit": "छोटा चार धाम",
        "expected": 4,
    },
    {
        "slug": "panch-kedar",
        "name": "Panch Kedar",
        "shortName": "Panch Kedar",
        "countLabel": "5 Kedars",
        "blurb": "Five Garhwal shrines of Shiva’s form after the Pandava legend — Kedarnath, Tungnath, Rudranath, Madhyamaheshwar, Kalpeshwar.",
        "lede": "Kedarnath is shared with Jyotirlinga and Chota Char Dham; the other four complete the Panch Kedar set.",
        "sanskrit": "पंच केदार",
        "expected": 5,
    },
    {
        "slug": "pancha-bhuta",
        "name": "Pancha Bhuta Sthalams",
        "shortName": "Pancha Bhuta",
        "countLabel": "5 elements",
        "blurb": "Earth, water, fire, air, and space — five South Indian Shiva temples of the elemental circuit.",
        "lede": "Complete five-temple set: Kanchipuram, Thiruvanaikaval, Tiruvannamalai, Srikalahasti, and Chidambaram.",
        "sanskrit": "पञ्चभूत स्थलम्",
        "expected": 5,
    },
    {
        "slug": "ashtavinayak",
        "name": "Ashtavinayak",
        "shortName": "Ashtavinayak",
        "countLabel": "8 Ganesha temples",
        "blurb": "Maharashtra’s eight sacred Ganesha temples — the classic Ashtavinayak yatra around Pune.",
        "lede": "Complete eight-temple set in traditional Morgaon-start order. Ideal 2–3 day road circuit from Pune.",
        "sanskrit": "अष्टविनायक",
        "expected": 8,
    },
    {
        "slug": "modern-temples",
        "name": "Modern Temples",
        "shortName": "Modern",
        "countLabel": "New-age shrines",
        "blurb": "Contemporary pilgrimage landmarks — Akshardham, ISKCON, and other living temples of the modern era.",
        "lede": "Open trail of newer or rebuilt sacred complexes that draw huge urban and international crowds.",
        "sanskrit": "आधुनिक मंदिर",
    },
    {
        "slug": "ramayana-trail",
        "name": "Ramayana Trail",
        "shortName": "Ramayana",
        "countLabel": "Epic sites",
        "blurb": "Temples and tirthas woven into Rama’s journey — growing trail, not a fixed count.",
        "lede": "Walk Ramayana geography through temples that preserve local memory of exile, devotion, and return.",
        "sanskrit": "रामायण पथ",
    },
    {
        "slug": "mahabharata-sites",
        "name": "Mahabharata Sites",
        "shortName": "Mahabharata",
        "countLabel": "Epic sites",
        "blurb": "Sites tied to the Mahabharata and Bhagavad Gita — open trail, not a fixed count.",
        "lede": "From Kurukshetra to Dwarka and quieter epic-linked tirthas.",
        "sanskrit": "महाभारत स्थल",
    },
    {
        "slug": "beyond-india",
        "name": "Beyond India",
        "shortName": "Beyond India",
        "countLabel": "Nepal · Sri Lanka · Kailash",
        "blurb": "Sacred sites beyond India’s borders linked by shared mythology.",
        "lede": "Nepal, Sri Lanka, and the Kailash–Manasarovar landscape.",
        "sanskrit": "अन्तर्राष्ट्रीय तीर्थ",
    },
]


def slugify_glyph(name: str) -> str:
    # first Devanagari-ish fallback: first letter of english name
    return (name.strip()[:1] or "ॐ").upper()


def base_detail(seed: dict) -> dict:
    name = seed["name"]
    loc = seed["location"]
    country = seed.get("country", "India")
    famous = seed.get("famousFor", name)
    mythology = seed.get(
        "mythology",
        f"{name} is a sacred tirtha at {loc}. Tradition links it to the wider fabric of Hindu pilgrimage and local sthala purana. Always verify current darshan rules on official channels.",
    )
    return {
        "slug": seed["slug"],
        "name": name,
        "deity": seed.get("deity", "Deity of the shrine"),
        "location": loc,
        "state": seed.get("state", ""),
        "country": country,
        "glyph": seed.get("glyph") or slugify_glyph(name),
        "tags": [],
        "tagLabels": [],
        "summary": seed.get("summary", f"Pilgrimage guide for {name} at {loc}."),
        "famousFor": famous,
        "mythology": mythology,
        "scriptureLinks": seed.get("scriptureLinks", ["Puranic / sthala tradition"]),
        "festivals": seed.get("festivals", ["Major local festival days", "Navaratri / Shiva-related observances as applicable"]),
        "bestTime": seed.get("bestTime", "October–March for most plains sites; confirm Himalayan seasonal windows separately."),
        "whatToCarry": seed.get("whatToCarry", "Modest clothes, ID proof, water, and offline maps."),
        "climate": seed.get("climate", "Varies by region — check seasonal weather before travel."),
        "nearestRail": seed.get("nearestRail", "See regional railhead; confirm current connectivity."),
        "nearestAirport": seed.get("nearestAirport", "Nearest major airport with road onward."),
        "accommodation": seed.get("accommodation", "Dharamshalas, trust guest houses, and private hotels near the shrine town."),
        "localFood": seed.get("localFood", "Simple vegetarian pilgrim meals and prasadam where offered."),
        "otherFood": seed.get("otherFood", "Wider options usually in the nearest city."),
        "localLanguage": seed.get("localLanguage", "Regional language and Hindi; English varies."),
        "dressCode": seed.get("dressCode", "Modest clothing; follow temple boards for traditional dress rules."),
        "darshanTimings": seed.get("darshanTimings", "Typically early morning to evening with ritual breaks — confirm locally."),
        "specialEntry": seed.get("specialEntry", "Special entry, if any, only via official temple counters."),
        "restrictions": seed.get("restrictions", "Follow phone, leather, and photography rules posted at the gate."),
        "lockers": seed.get("lockers", "Cloakrooms where available near the entrance."),
        "officialWebsite": seed.get("officialWebsite", "https://tourism.gov.in/"),
        "videoUrl": f"https://www.youtube.com/results?search_query={name.replace(' ', '+')}+temple",
        "videoNote": "Orientation videos only — verify timings on official sources.",
        "lat": seed.get("lat"),
        "lng": seed.get("lng"),
        "mapQuery": seed.get("mapQuery", name),
        "nearby": seed.get("nearby", []),
        "packages": seed.get("packages", [f"{name} day darshan", "Regional multi-temple circuit"]),
        "sources": seed.get(
            "sources",
            [
                "Temple trust / local administration notices",
                "State tourism materials",
                "Puranic / pilgrimage tradition (lists can vary by scripture)",
            ],
        ),
        "lastUpdated": "2026-07-30",
        "disclaimer": seed.get(
            "disclaimer",
            "Lists and ritual details can vary by tradition. Verify before travel.",
        ),
    }


# Seeds for temples we must create or enrich (missing files only created; existing kept & tag-synced)
SEEDS = {
    # —— Jyotirlinga missing ——
    "mallikarjuna-srisailam": {
        "slug": "mallikarjuna-srisailam",
        "name": "Mallikarjuna–Bhramaramba Temple, Srisailam",
        "deity": "Lord Shiva (Mallikarjuna) & Goddess Bhramaramba",
        "location": "Srisailam, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "glyph": "म",
        "famousFor": "Jyotirlinga + Shakti Peetha in one complex",
        "summary": "Srisailam hosts Mallikarjuna Jyotirlinga and Bhramaramba Devi — one complex counted in both the 12 Jyotirlinga and 51 Shakti Peeth circuits.",
        "mythology": "Mallikarjuna is one of the twelve Jyotirlingas. The same hill shrine venerates Bhramaramba, counted among the Shakti Peethas (neck). Pilgrims thus complete two major lists in a single darshan complex — facts stay on this one shared page.",
        "scriptureLinks": ["Shiva Purana", "Skanda Purana", "Shakti Peetha tradition"],
        "lat": 16.0742,
        "lng": 78.8681,
        "mapQuery": "Srisailam Mallikarjuna Temple",
        "nearestRail": "Markapur Road / Kurnool with road to Srisailam",
        "nearestAirport": "Hyderabad / Kurnool",
        "officialWebsite": "https://www.srisailamonline.com/",
        "dressCode": "Traditional modest dress preferred; follow temple notices.",
    },
    "mahakaleshwar-ujjain": {
        "slug": "mahakaleshwar-ujjain",
        "name": "Mahakaleshwar Temple",
        "deity": "Lord Shiva (Mahakaleshwar)",
        "location": "Ujjain, Madhya Pradesh",
        "state": "Madhya Pradesh",
        "glyph": "म",
        "famousFor": "South-facing Jyotirlinga & Bhasma Aarti",
        "summary": "One of the twelve Jyotirlingas in Ujjain — famed for the pre-dawn Bhasma Aarti.",
        "mythology": "Mahakaleshwar is the Jyotirlinga of Ujjain (Avanti), celebrated in the Shiva Purana. The lingam is traditionally described as south-facing (dakshinamurti). The city is also a Simhastha Kumbh seat.",
        "lat": 23.1828,
        "lng": 75.7682,
        "mapQuery": "Mahakaleshwar Temple Ujjain",
        "nearestRail": "Ujjain Junction",
        "nearestAirport": "Indore",
        "officialWebsite": "https://www.mahakaleshwar.templeinfo.in/",
        "festivals": ["Bhasma Aarti (daily pre-dawn)", "Maha Shivaratri", "Simhastha Kumbh years"],
    },
    "omkareshwar": {
        "slug": "omkareshwar",
        "name": "Omkareshwar Temple",
        "deity": "Lord Shiva (Omkareshwar / Mamleshwar)",
        "location": "Omkareshwar, Khandwa, Madhya Pradesh",
        "state": "Madhya Pradesh",
        "glyph": "ॐ",
        "famousFor": "Jyotirlinga on the Om-shaped Mandhata island",
        "summary": "Jyotirlinga on the Narmada’s Mandhata island, shaped like the sacred Om.",
        "mythology": "Omkareshwar and Mamleshwar form the Jyotirlinga tradition of the Narmada. The island’s Om-like shape and river parikrama are central to the pilgrimage experience.",
        "lat": 22.2455,
        "lng": 76.1510,
        "mapQuery": "Omkareshwar Temple",
        "nearestRail": "Omkareshwar Road / Khandwa",
        "nearestAirport": "Indore",
    },
    "bhimashankar": {
        "slug": "bhimashankar",
        "name": "Bhimashankar Temple",
        "deity": "Lord Shiva (Bhimashankar)",
        "location": "Pune district, Maharashtra",
        "state": "Maharashtra",
        "glyph": "भि",
        "famousFor": "Jyotirlinga in the Sahyadri forests",
        "summary": "Jyotirlinga in the Western Ghats near Pune, set in a wildlife sanctuary landscape.",
        "mythology": "Bhimashankar is counted among the twelve Jyotirlingas. Local legend links the name to Bhima and Shiva’s victory over the demon Tripurasura traditions of the region.",
        "lat": 19.0720,
        "lng": 73.5350,
        "mapQuery": "Bhimashankar Temple",
        "nearestRail": "Pune",
        "nearestAirport": "Pune",
        "bestTime": "October–February; monsoon is lush but slippery.",
    },
    "kashi-vishwanath": {
        "slug": "kashi-vishwanath",
        "name": "Kashi Vishwanath Temple",
        "deity": "Lord Shiva (Vishwanath)",
        "location": "Varanasi, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "का",
        "famousFor": "Jyotirlinga of Kashi & Ganga aarti city",
        "summary": "The Jyotirlinga of Varanasi — one of Hinduism’s most visited Shiva temples, beside the Ganga.",
        "mythology": "Kashi Vishwanath is the Jyotirlinga of the sacred city of light. Puranic tradition holds that dying in Kashi brings liberation; Vishwanath is the city’s spiritual axis.",
        "lat": 25.3109,
        "lng": 83.0107,
        "mapQuery": "Kashi Vishwanath Temple Varanasi",
        "nearestRail": "Varanasi Junction / Banaras",
        "nearestAirport": "Lal Bahadur Shastri Airport, Varanasi",
        "officialWebsite": "https://www.shrikashivishwanath.org/",
        "dressCode": "Modest dress; security screening; follow corridor rules in the expanded corridor complex.",
    },
    "trimbakeshwar": {
        "slug": "trimbakeshwar",
        "name": "Trimbakeshwar Temple",
        "deity": "Lord Shiva (Trimbakeshwar)",
        "location": "Trimbak, Nashik, Maharashtra",
        "state": "Maharashtra",
        "glyph": "त्रि",
        "famousFor": "Jyotirlinga near the Godavari source",
        "summary": "Jyotirlinga at Trimbak near Nashik, linked to the Godavari’s sacred geography.",
        "mythology": "Trimbakeshwar is the Jyotirlinga associated with the Brahmagiri / Godavari tradition. The lingam is distinctive in form and ritual practice.",
        "lat": 19.9320,
        "lng": 73.5307,
        "mapQuery": "Trimbakeshwar Temple Nashik",
        "nearestRail": "Nashik Road",
        "nearestAirport": "Nashik / Mumbai",
        "dressCode": "Traditional expectation for men often includes dhoti for sanctum — follow temple rules.",
    },
    "vaidyanath-deoghar": {
        "slug": "vaidyanath-deoghar",
        "name": "Baba Baidyanath Temple, Deoghar",
        "deity": "Lord Shiva (Vaidyanath) & Shakti peetha tradition",
        "location": "Deoghar, Jharkhand",
        "state": "Jharkhand",
        "glyph": "वै",
        "famousFor": "Jyotirlinga + Shakti Peetha complex",
        "summary": "Deoghar’s Baidyanath Dham is counted as a Jyotirlinga and also appears in the 51 Shakti Peeth list (heart) — one shared guide for both tags.",
        "mythology": "Baidyanath / Vaidyanath is widely accepted in pilgrimage practice as a Jyotirlinga. The same sacred complex is associated with a Shakti Peetha tradition (heart of Sati). Bol Bam kanwar yatra in Shravan draws huge crowds.",
        "scriptureLinks": ["Shiva Purana traditions", "Shakti Peetha lists", "Shravan kanwar tradition"],
        "lat": 24.4925,
        "lng": 86.6990,
        "mapQuery": "Baidyanath Temple Deoghar",
        "nearestRail": "Jasidih / Deoghar",
        "nearestAirport": "Deoghar / Ranchi",
        "festivals": ["Shravan Bol Bam", "Maha Shivaratri"],
    },
    "nageshwar": {
        "slug": "nageshwar",
        "name": "Nageshwar Jyotirlinga",
        "deity": "Lord Shiva (Nageshwar)",
        "location": "Near Dwarka, Gujarat",
        "state": "Gujarat",
        "glyph": "ना",
        "famousFor": "Jyotirlinga near Dwarka",
        "summary": "Jyotirlinga on the way to / near Dwarka — often combined with the Char Dham Dwarka visit.",
        "mythology": "Nageshwar is counted among the twelve Jyotirlingas. Pilgrims commonly pair it with Dwarkadhish on the same Gujarat coastal yatra.",
        "lat": 22.3365,
        "lng": 69.0860,
        "mapQuery": "Nageshwar Jyotirlinga Dwarka",
        "nearestRail": "Dwarka",
        "nearestAirport": "Jamnagar / Rajkot",
        "nearby": [
            {"name": "Dwarkadhish Temple", "slug": "dwarka", "note": "Same-trip Char Dham seat"},
            {"name": "Bet Dwarka", "slug": None, "note": "Boat shrine"},
        ],
    },
    "grishneshwar": {
        "slug": "grishneshwar",
        "name": "Grishneshwar Temple",
        "deity": "Lord Shiva (Grishneshwar)",
        "location": "Near Ellora, Aurangabad, Maharashtra",
        "state": "Maharashtra",
        "glyph": "घृ",
        "famousFor": "12th Jyotirlinga near Ellora caves",
        "summary": "The twelfth Jyotirlinga, beside the Ellora caves heritage landscape.",
        "mythology": "Grishneshwar (also Ghushmeshwar in some texts) completes many Jyotirlinga yatra lists. The shrine stands close to the UNESCO Ellora caves.",
        "lat": 20.0250,
        "lng": 75.1660,
        "mapQuery": "Grishneshwar Temple Ellora",
        "nearestRail": "Aurangabad",
        "nearestAirport": "Aurangabad",
    },
    # —— Char Dham missing ——
    "jagannath-puri": {
        "slug": "jagannath-puri",
        "name": "Jagannath Temple, Puri",
        "deity": "Lord Jagannath (with Balabhadra & Subhadra); Vimala Devi (Shakti Peetha)",
        "location": "Puri, Odisha",
        "state": "Odisha",
        "glyph": "ज",
        "famousFor": "Char Dham seat & Rath Yatra; Vimala Shakti Peetha inside",
        "summary": "Eastern Char Dham seat of Jagannath. The Vimala temple inside the same complex is counted as a Shakti Peetha — one shared page for both circuit tags.",
        "mythology": "Puri is Adi Shankaracharya’s eastern Char Dham. Lord Jagannath’s Rath Yatra is world-famous. Within the complex, Goddess Vimala is venerated as a Shakti Peetha (feet of Sati) — so Char Dham and Shakti Peeth pilgrims share this guide.",
        "lat": 19.8047,
        "lng": 85.8180,
        "mapQuery": "Jagannath Temple Puri",
        "nearestRail": "Puri",
        "nearestAirport": "Bhubaneswar",
        "officialWebsite": "https://www.shallowajagannath.nic.in/",
        "dressCode": "Strict entry rules historically for non-Hindus to the main temple — follow current official policy. Modest dress required.",
        "festivals": ["Rath Yatra", "Snana Yatra", "Kartika"],
    },
    # —— Chota Char Dham missing ——
    "yamunotri": {
        "slug": "yamunotri",
        "name": "Yamunotri Temple",
        "deity": "Goddess Yamuna",
        "location": "Uttarkashi district, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "य",
        "famousFor": "Source-region shrine of the Yamuna; Chota Char Dham",
        "summary": "First stop of the Uttarakhand Chota Char Dham — Yamunotri temple near the Yamuna’s sacred source region.",
        "mythology": "Yamunotri is the Devi shrine of the Yamuna in the Chota Char Dham circuit (Yamunotri–Gangotri–Kedarnath–Badrinath). It is not part of Adi Shankaracharya’s pan-India Char Dham.",
        "lat": 30.9987,
        "lng": 78.4627,
        "mapQuery": "Yamunotri Temple",
        "nearestRail": "Rishikesh / Dehradun then road to Janki Chatti + trek",
        "nearestAirport": "Dehradun",
        "officialWebsite": "https://badrinath-kedarnath.gov.in/",
        "bestTime": "May–June and September–October; closed in winter.",
    },
    "gangotri": {
        "slug": "gangotri",
        "name": "Gangotri Temple",
        "deity": "Goddess Ganga",
        "location": "Uttarkashi district, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "ग",
        "famousFor": "Ganga’s Himalayan shrine; Chota Char Dham",
        "summary": "Chota Char Dham shrine of Ganga at Gangotri, gateway toward Gaumukh glacier traditions.",
        "mythology": "Gangotri commemorates Ganga’s descent. It forms the second seat of the Uttarakhand Chota Char Dham with Yamunotri, Kedarnath, and Badrinath.",
        "lat": 30.9947,
        "lng": 78.9398,
        "mapQuery": "Gangotri Temple",
        "nearestRail": "Rishikesh then long road journey",
        "nearestAirport": "Dehradun",
        "officialWebsite": "https://badrinath-kedarnath.gov.in/",
        "bestTime": "May–June and September–October; closed in winter.",
    },
    # —— Panch Kedar missing ——
    "tungnath": {
        "slug": "tungnath",
        "name": "Tungnath Temple",
        "deity": "Lord Shiva (Tungnath)",
        "location": "Rudraprayag, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "तु",
        "famousFor": "Highest Shiva temple among Panch Kedar",
        "summary": "Second of the Panch Kedar — often called the highest Shiva temple, above Chopta.",
        "mythology": "In the Pandava–Shiva bull legend of Garhwal, Tungnath is where the arms of Shiva are worshipped. It forms Panch Kedar with Kedarnath, Rudranath, Madhyamaheshwar, and Kalpeshwar.",
        "lat": 30.4906,
        "lng": 79.2160,
        "mapQuery": "Tungnath Temple",
        "nearestRail": "Rishikesh",
        "nearestAirport": "Dehradun",
        "bestTime": "May–June, September–November",
    },
    "rudranath": {
        "slug": "rudranath",
        "name": "Rudranath Temple",
        "deity": "Lord Shiva (Rudranath)",
        "location": "Chamoli, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "रु",
        "famousFor": "Panch Kedar face-form shrine",
        "summary": "Third Panch Kedar temple — a demanding trek shrine where Shiva’s face is worshipped in tradition.",
        "mythology": "Rudranath is the Panch Kedar seat associated with Shiva’s face in the Garhwal Pandava legend.",
        "lat": 30.5330,
        "lng": 79.3330,
        "mapQuery": "Rudranath Temple",
        "nearestRail": "Rishikesh",
        "nearestAirport": "Dehradun",
        "bestTime": "May–June, September–October",
    },
    "madhyamaheshwar": {
        "slug": "madhyamaheshwar",
        "name": "Madhyamaheshwar Temple",
        "deity": "Lord Shiva (Madhyamaheshwar)",
        "location": "Garhwal, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "म",
        "famousFor": "Panch Kedar navel-form shrine",
        "summary": "Fourth Panch Kedar — associated with the navel of Shiva in local legend.",
        "mythology": "Madhyamaheshwar continues the Panch Kedar sequence of Shiva’s form distributed across Garhwal after the bull legend.",
        "lat": 30.6370,
        "lng": 79.2220,
        "mapQuery": "Madhyamaheshwar Temple",
        "nearestRail": "Rishikesh",
        "nearestAirport": "Dehradun",
    },
    "kalpeshwar": {
        "slug": "kalpeshwar",
        "name": "Kalpeshwar Temple",
        "deity": "Lord Shiva (Kalpeshwar)",
        "location": "Urgam Valley, Chamoli, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "क",
        "famousFor": "Panch Kedar hair-form; often open longer",
        "summary": "Fifth Panch Kedar — associated with Shiva’s hair/jata; relatively more accessible than some siblings.",
        "mythology": "Kalpeshwar completes the Panch Kedar set. Tradition links it to Shiva’s jata; many pilgrims note it remains accessible longer in the year than higher Kedars.",
        "lat": 30.5280,
        "lng": 79.4550,
        "mapQuery": "Kalpeshwar Temple",
        "nearestRail": "Rishikesh",
        "nearestAirport": "Dehradun",
    },
    # —— Pancha Bhuta missing ——
    "ekambareswarar-kanchipuram": {
        "slug": "ekambareswarar-kanchipuram",
        "name": "Ekambareswarar Temple",
        "deity": "Lord Shiva (Prithvi Lingam — Earth)",
        "location": "Kanchipuram, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "ए",
        "famousFor": "Earth element of Pancha Bhuta",
        "summary": "Prithvi (earth) Sthalam of the Pancha Bhuta circuit in temple city Kanchipuram.",
        "mythology": "Ekambareswarar represents the earth element. Legend of Parvati’s penance under the mango tree is central to the sthala purana.",
        "lat": 12.8475,
        "lng": 79.6997,
        "mapQuery": "Ekambareswarar Temple Kanchipuram",
        "nearestRail": "Kanchipuram",
        "nearestAirport": "Chennai",
        "dressCode": "South Indian temple norms — traditional attire often required for sanctum.",
    },
    "arunachaleswarar-tiruvannamalai": {
        "slug": "arunachaleswarar-tiruvannamalai",
        "name": "Arunachaleswarar Temple",
        "deity": "Lord Shiva (Agni Lingam — Fire)",
        "location": "Tiruvannamalai, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "अ",
        "famousFor": "Fire element & Karthigai Deepam",
        "summary": "Agni (fire) Sthalam — the Arunachala hill and temple of Tiruvannamalai.",
        "mythology": "Arunachaleswarar embodies the fire element. The Karthigai Deepam beacon on the hill is among South India’s great Shaiva festivals. Associated with Ramana Maharshi’s later fame in the town.",
        "lat": 12.2319,
        "lng": 79.0677,
        "mapQuery": "Arunachaleswarar Temple Tiruvannamalai",
        "nearestRail": "Tiruvannamalai",
        "nearestAirport": "Chennai / Puducherry",
        "festivals": ["Karthigai Deepam", "Maha Shivaratri"],
    },
    "srikalahasti": {
        "slug": "srikalahasti",
        "name": "Srikalahasteeswara Temple",
        "deity": "Lord Shiva (Vayu Lingam — Air)",
        "location": "Srikalahasti, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "glyph": "वा",
        "famousFor": "Air element of Pancha Bhuta",
        "summary": "Vayu (air) Sthalam of the elemental Shiva circuit, near Tirupati.",
        "mythology": "Srikalahasti represents the air element. The name recalls the spider (sri), snake (kala), and elephant (hasti) devotees of local legend.",
        "lat": 13.7497,
        "lng": 79.6983,
        "mapQuery": "Srikalahasti Temple",
        "nearestRail": "Srikalahasti / Renigunta",
        "nearestAirport": "Tirupati",
    },
    "nataraja-chidambaram": {
        "slug": "nataraja-chidambaram",
        "name": "Nataraja Temple, Chidambaram",
        "deity": "Lord Shiva as Nataraja (Akasha — Space)",
        "location": "Chidambaram, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "चि",
        "famousFor": "Space element & Chidambara Rahasyam",
        "summary": "Akasha (space) Sthalam — the great Nataraja temple of Chidambaram.",
        "mythology": "Chidambaram represents space among the Pancha Bhuta. The Chidambara Rahasyam and Nataraja’s cosmic dance are at the heart of its theology.",
        "lat": 11.3995,
        "lng": 79.6936,
        "mapQuery": "Nataraja Temple Chidambaram",
        "nearestRail": "Chidambaram",
        "nearestAirport": "Chennai / Trichy",
    },
}

# Compact Shakti Peeth seeds (name, location, state, country, body part, lat/lng approx)
SHAKTI_META = [
    ("amarnath-shakti", "Amarnath Shakti Peetha", "Goddess Mahamaya tradition", "Amarnath, Pahalgam", "Jammu and Kashmir", "India", "Throat (tradition varies)", 34.2197, 75.3700),
    ("attahas", "Attahas Shakti Peetha", "Goddess Phullara", "Labhpur, Birbhum", "West Bengal", "India", "Lips", 23.8260, 87.8180),
    ("bahula-ketugram", "Bahula Temple", "Goddess Bahula", "Ketugram, Purba Bardhaman", "West Bengal", "India", "Left arm", 23.7000, 87.9500),
    ("bakreshwar", "Bakreshwar Temple", "Mahishmardini tradition", "Bakreshwar, Birbhum", "West Bengal", "India", "Brow / between eyebrows", 23.8800, 87.3700),
    ("bhabanipur", "Bhabanipur Shakti Peetha", "Goddess Arpana tradition", "Sherpur region", "Rajshahi Division", "Bangladesh", "Left anklet", 24.6500, 89.4200),
    ("biraja-jajpur", "Biraja Temple", "Goddess Biraja", "Jajpur", "Odisha", "India", "Navel", 20.8500, 86.3300),
    ("mithila-janakpur", "Mithila Shakti Peetha, Janakpur", "Goddess of Mithila tradition", "Janakpur", "Madhesh Province", "Nepal", "Left shoulder", 26.7280, 85.9260),
    (
        "surkanda-devi",
        "Surkanda Devi Temple",
        "Goddess Surkanda Devi (Kali / Sati)",
        "Near Kanatal, Tehri Garhwal",
        "Uttarakhand",
        "India",
        "Head",
        30.4120,
        78.2880,
    ),
    (
        "panchsagar-champawat",
        "Panchsagar Shakti Peetha, Champawat",
        "Goddess Varahi / Panchsagar Devi",
        "Champawat",
        "Uttarakhand",
        "India",
        "Lower teeth",
        29.3360,
        80.0910,
    ),
    ("guhyeshwari", "Guhyeshwari Temple", "Goddess Guhyeshwari", "Near Pashupatinath, Kathmandu", "Bagmati Province", "Nepal", "Hips / knees", 27.7108, 85.3530),
    ("saptashrungi", "Saptashrungi Temple", "Goddess Saptashrungi", "Vani, Nashik", "Maharashtra", "India", "Chin", 20.3900, 73.9100),
    ("hinglaj", "Hinglaj Mata Temple", "Goddess Hingula", "Hinglaj, Lasbela", "Balochistan", "Pakistan", "Brahmarandhra (crown)", 25.5130, 65.5150),
    ("kalighat", "Kalighat Kali Temple", "Goddess Kali", "Kalighat, Kolkata", "West Bengal", "India", "Right toes", 22.5200, 88.3420),
    ("kankalitala", "Kankalitala Temple", "Goddess of Kankalitala", "Kankalitala, Birbhum", "West Bengal", "India", "Waist", 23.6800, 87.6800),
    ("kanyakumari", "Kanya Kumari Temple", "Goddess Kanya Kumari", "Kanyakumari", "Tamil Nadu", "India", "Back / spine (tradition)", 8.0883, 77.5385),
    ("brajeshwari-kangra", "Brajeshwari Temple", "Goddess Brajeshwari", "Kangra", "Himachal Pradesh", "India", "Left breast", 32.1000, 76.2700),
    ("kiriteswari", "Kiriteswari Temple", "Goddess Kiriteswari", "Kiritkona, Murshidabad", "West Bengal", "India", "Crown", 24.1800, 88.2700),
    ("ratnavali", "Ratnavali Shakti Peetha", "Goddess of Ratnavali", "Hooghly region", "West Bengal", "India", "Right shoulder", 22.9000, 88.3700),
    ("bhramari-jalpaiguri", "Bhramari Devi Peetha", "Goddess Bhramari", "Jalpaiguri region", "West Bengal", "India", "Left leg", 26.5200, 88.7300),
    ("manasa-manasarovar", "Manasa / Manasarovar Peetha", "Goddess Manasa tradition", "Lake Manasarovar", "Tibet Autonomous Region", "China", "Right hand", 30.6500, 81.4500),
    ("ugratara-mahishi", "Ugratara Temple, Mahishi", "Goddess Ugratara", "Mahishi, Saharsa", "Bihar", "India", "Left eye", 25.8800, 86.6000),
    ("manibandh-pushkar", "Manibandh / Gayatri Peetha", "Goddess Gayatri tradition", "Pushkar, Ajmer", "Rajasthan", "India", "Wrists", 26.4890, 74.5510),
    ("indrakshi-nainativu", "Indrakshi / Nagapooshani Peetha", "Goddess Indrakshi tradition", "Nainativu, Jaffna", "Northern Province", "Sri Lanka", "Anklets", 9.6160, 79.7740),
    ("jayanti-nartiang", "Jayanti Temple, Nartiang", "Goddess Jayanti", "Nartiang, Jaintia Hills", "Meghalaya", "India", "Left thigh", 25.3400, 92.2100),
    ("jeshoreshwari", "Jeshoreshwari Temple", "Goddess Jeshoreshwari", "Ishwaripur, Satkhira", "Khulna Division", "Bangladesh", "Palms and soles", 22.5600, 89.1000),
    ("jwalamukhi", "Jwalamukhi Temple", "Goddess Jwalamukhi", "Jwalamukhi, Kangra", "Himachal Pradesh", "India", "Tongue", 31.8750, 76.3240),
    ("tara-tarini", "Tara Tarini Temple", "Goddess Tara Tarini", "Near Berhampur, Ganjam", "Odisha", "India", "Breasts (Adi Shakti Peetha)", 19.4800, 84.6600),
    ("prabhas-chandrabhaga", "Chandrabhaga / Prabhas Devi Peetha", "Goddess of Prabhas", "Prabhas Patan, near Somnath", "Gujarat", "India", "Stomach", 20.8880, 70.4010),
    ("alopi-devi-prayagraj", "Alopi Devi Temple", "Goddess Alopi / Lalita tradition", "Prayagraj", "Uttar Pradesh", "India", "Fingers", 25.4358, 81.8463),
    ("bhadrakali-kurukshetra", "Bhadrakali Temple, Kurukshetra", "Goddess Bhadrakali", "Thanesar, Kurukshetra", "Haryana", "India", "Right ankle", 29.9695, 76.8280),
    ("sharada-maihar", "Sharada Devi Temple, Maihar", "Goddess Sharada", "Maihar, Satna", "Madhya Pradesh", "India", "Necklace (tradition varies)", 24.2650, 80.7550),
    ("nandikeshwari-sainthia", "Nandikeshwari Temple", "Goddess Nandikeshwari", "Sainthia, Birbhum", "West Bengal", "India", "Necklace ornament", 23.9500, 87.6800),
    ("manikyamba-draksharama", "Manikyamba Devi Temple", "Goddess Manikyamba", "Draksharama", "Andhra Pradesh", "India", "Cheek / navel (tradition varies)", 16.7900, 82.0600),
    ("naina-devi", "Naina Devi Temple", "Goddess Naina Devi", "Naina Devi, Bilaspur", "Himachal Pradesh", "India", "Eyes", 31.3900, 76.5500),
    ("shondesh-amarkantak", "Shondesh / Amarkantak Peetha", "Goddess of Amarkantak", "Amarkantak", "Madhya Pradesh", "India", "Right buttock", 22.6700, 81.7500),
    ("narayani-suchindram", "Narayani / Suchindram Peetha", "Goddess Narayani tradition", "Suchindram, Kanyakumari", "Tamil Nadu", "India", "Upper teeth", 8.1550, 77.4650),
    ("sugandha-shikarpur", "Sugandha Shakti Peetha", "Goddess Sugandha", "Shikarpur, Barisal region", "Barisal Division", "Bangladesh", "Nose", 22.7000, 90.2000),
    ("tripura-sundari", "Tripura Sundari Temple", "Goddess Tripura Sundari", "Udaipur, Gomati", "Tripura", "India", "Right foot", 23.5350, 91.4980),
    ("ujani-mangalchandika", "Mangal Chandika, Ujani", "Goddess Mangal Chandika", "Ujani, Purba Bardhaman", "West Bengal", "India", "Right wrist", 23.2500, 87.8700),
    ("vishalakshi-kashi", "Vishalakshi Temple", "Goddess Vishalakshi", "Varanasi", "Uttar Pradesh", "India", "Earring", 25.3100, 83.0140),
    ("vibhash-tamluk", "Vibhash / Kapalini Peetha", "Goddess Kapalini tradition", "Tamluk, Purba Medinipur", "West Bengal", "India", "Left ankle", 22.3000, 87.9200),
    ("viraat-ambika", "Viraat Ambika Peetha", "Goddess Ambika", "Bharatpur region", "Rajasthan", "India", "Left toes", 27.2200, 77.4900),
    ("katyayani-vrindavan", "Katyayani Temple, Vrindavan", "Goddess Katyayani", "Vrindavan, Mathura", "Uttar Pradesh", "India", "Hair / ringlets", 27.5800, 77.7000),
    ("tripuramalini-jalandhar", "Tripuramalini / Devi Talab", "Goddess Tripuramalini", "Jalandhar", "Punjab", "India", "Left breast", 31.3260, 75.5760),
    ("kamakshi-kanchipuram", "Kamakshi Amman Temple", "Goddess Kamakshi", "Kanchipuram", "Tamil Nadu", "India", "Navel / skeleton (tradition varies)", 12.8407, 79.7002),
    ("jogadya-kshirgram", "Jogadya Temple, Kshirgram", "Goddess Jogadya", "Kshirgram, Purba Bardhaman", "West Bengal", "India", "Right big toe", 23.4500, 87.9500),
    ("puruhutika-pithapuram", "Puruhutika Devi Temple", "Goddess Puruhutika", "Pithapuram, Kakinada", "Andhra Pradesh", "India", "Back / hip", 17.1160, 82.2540),
]


def invert_groups() -> dict[str, list[str]]:
    inv: dict[str, list[str]] = {}
    for g, slugs in GROUPS.items():
        for s in slugs:
            inv.setdefault(s, []).append(g)
    return inv


def ensure_shakti_seeds():
    for row in SHAKTI_META:
        slug, name, deity, loc, state, country, body, lat, lng = row
        if slug in SEEDS:
            continue
        SEEDS[slug] = {
            "slug": slug,
            "name": name,
            "deity": deity,
            "location": f"{loc}, {state}" if country == "India" else f"{loc}, {country}",
            "state": state,
            "country": country,
            "glyph": name[0],
            "famousFor": f"Shakti Peetha — {body}",
            "summary": f"{name} is counted among the 51 Shakti Peethas. Tradition associates this seat with the {body} of Sati.",
            "mythology": (
                f"According to the popular 51-peetha pilgrimage enumeration, {name} at {loc} "
                f"marks the place associated with the {body} of Goddess Sati. "
                f"Scriptural lists of peethas vary (51/52/108); we label this site consistently for navigation, "
                f"and advise verifying local tradition and current temple rules before travel."
            ),
            "scriptureLinks": ["Pithanirnaya / Shakti Peetha tradition", "Devi Purana cycles", "Local sthala lore"],
            "lat": lat,
            "lng": lng,
            "mapQuery": name,
        }


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_tags_on_detail(detail: dict, tags: list[str]) -> dict:
    # preserve open trail tags already on the temple
    open_existing = [t for t in detail.get("tags", []) if t in OPEN_TAGS_KEEP]
    # beyond-india auto if country not India
    if detail.get("country") and detail["country"] != "India":
        if "beyond-india" not in open_existing:
            open_existing.append("beyond-india")
    merged = []
    for t in tags + open_existing:
        if t not in merged:
            merged.append(t)
    detail["tags"] = merged
    detail["tagLabels"] = [LABELS[t] for t in merged if t in LABELS]
    return detail


def main():
    ensure_shakti_seeds()
    TEMPLES_DIR.mkdir(parents=True, exist_ok=True)

    # validate group sizes
    for g, slugs in GROUPS.items():
        if len(slugs) != len(set(slugs)):
            raise SystemExit(f"Duplicate in group {g}")
        expected = {
            "12-jyotirlinga": 12,
            "char-dham": 4,
            "chota-char-dham": 4,
            "panch-kedar": 5,
            "pancha-bhuta": 5,
            "ashtavinayak": 8,
            "51-shakti-peeth": 52,
        }[g]
        if len(slugs) != expected:
            raise SystemExit(f"{g} has {len(slugs)} != {expected}")

    inv = invert_groups()

    # existing details
    existing = {p.stem: load_json(p) for p in TEMPLES_DIR.glob("*.json")}

    # create missing from seeds
    created = []
    for slug, tags in inv.items():
        if slug in existing:
            continue
        if slug not in SEEDS:
            raise SystemExit(f"Missing seed for required temple: {slug}")
        detail = base_detail(SEEDS[slug])
        dump_json(TEMPLES_DIR / f"{slug}.json", detail)
        existing[slug] = detail
        created.append(slug)

    # Enrich shared-complex notes on important existing pages
    enrich = {
        "kedarnath": {
            "remove_tags_note": True,
        },
        "badrinath": {},
        "muktinath": {
            "mythology_append": " In Shakti Peetha lists this seat is also remembered as the Gandaki peetha — same shrine, shared guide.",
        },
        "rameswaram": {},
        "dwarka": {},
        "kamakhya": {},
        "thiruvanaikaval": {},
        "somnath": {},
    }

    # Sync tags for every temple that appears in groups OR exists
    all_slugs = sorted(set(existing) | set(inv))
    index = []
    for slug in all_slugs:
        path = TEMPLES_DIR / f"{slug}.json"
        detail = load_json(path) if path.exists() else None
        if detail is None:
            continue
        group_tags = inv.get(slug, [])
        detail = sync_tags_on_detail(detail, group_tags)

        # Fix Char Dham contamination: ensure kedarnath NOT in char-dham
        if slug == "kedarnath" and "char-dham" in detail["tags"]:
            detail["tags"] = [t for t in detail["tags"] if t != "char-dham"]
            detail["tagLabels"] = [LABELS[t] for t in detail["tags"] if t in LABELS]

        if slug == "muktinath" and "Gandaki" not in detail.get("mythology", ""):
            detail["mythology"] = detail.get("mythology", "") + enrich["muktinath"]["mythology_append"]

        # clarify badrinath belongs to both Char Dham systems
        if slug == "badrinath":
            if "Chota Char Dham" not in detail.get("mythology", ""):
                detail["mythology"] = (
                    detail.get("mythology", "")
                    + " Badrinath is unique in appearing in both Adi Shankaracharya’s Char Dham and the Uttarakhand Chota Char Dham — same temple page for both tags."
                )

        if slug == "kedarnath":
            # ensure mythology clarifies NOT Adi Shankara Char Dham
            note = "Kedarnath is part of the Uttarakhand Chota Char Dham and Panch Kedar, and is a Jyotirlinga — it is not one of Adi Shankaracharya’s four Char Dham seats (those are Badrinath, Dwarka, Puri, Rameswaram)."
            if "not one of Adi Shankaracharya" not in detail.get("mythology", ""):
                detail["mythology"] = detail.get("mythology", "") + " " + note

        dump_json(path, detail)

        index.append(
            {
                "slug": slug,
                "name": detail["name"],
                "deity": detail.get("deity", ""),
                "location": detail.get("location", ""),
                "state": detail.get("state", ""),
                "country": detail.get("country", "India"),
                "tier": detail.get("tier", "famous"),
                "glyph": detail.get("glyph", "ॐ"),
                "tags": detail["tags"],
                "tagLabels": detail["tagLabels"],
                "deityFamilies": detail.get("deityFamilies", []),
                "summary": detail.get("summary", ""),
                "famousFor": detail.get("famousFor", ""),
            }
        )

    # stable-ish order: fixed group temples first by circuit priority, then others
    priority = []
    for g in [
        "12-jyotirlinga",
        "char-dham",
        "chota-char-dham",
        "panch-kedar",
        "pancha-bhuta",
        "ashtavinayak",
        "51-shakti-peeth",
    ]:
        for s in GROUPS[g]:
            if s not in priority:
                priority.append(s)
    index.sort(key=lambda t: (priority.index(t["slug"]) if t["slug"] in priority else 999, t["name"]))

    dump_json(DATA / "temples.json", index)
    dump_json(DATA / "circuits.json", CIRCUITS)

    groups_out = {
        "fixed": {k: {"expected": len(v), "order": v} for k, v in GROUPS.items()},
        "open": {k: {"labelFlexible": True} for k in OPEN_TAGS_KEEP},
        "labels": LABELS,
    }
    dump_json(DATA / "groups.json", groups_out)

    # validate
    print("Created:", len(created), "temples")
    print("Total temples:", len(index))
    for g, slugs in GROUPS.items():
        have = [t["slug"] for t in index if g in t["tags"]]
        ok = set(have) == set(slugs) and len(have) == len(slugs)
        print(f"{g}: {len(have)}/{len(slugs)} {'OK' if ok else 'FAIL ' + str(sorted(set(slugs)^set(have)))}")
        if not ok:
            raise SystemExit(1)

    # char-dham must not include kedarnath
    char = [t["slug"] for t in index if "char-dham" in t["tags"]]
    assert "kedarnath" not in char, char
    assert set(char) == set(GROUPS["char-dham"]), char
    print("Char Dham members:", char)
    print("Sync complete.")


if __name__ == "__main__":
    main()
