#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add popular temples for the next ~3 months (festivals, circuits, Devi–Devta).

Does NOT run sync_groups.py (that would wipe newer circuits in groups.json).
Rebuilds data/temples.json from detail files only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))

from sync_groups import base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")

CIRCUIT_LABELS = {
    "gujarat-char-dham": "Gujarat Char Dham",
    "braj-yatra": "Braj Yatra",
    "hanuman-trail": "Hanuman Trail",
    "krishna-lila-trail": "Krishna Lila",
    "murugan-trail": "Murugan Trail",
    "rama-kshaetra": "Rama Kshaetra",
    "narasimha-kshaetra": "Narasimha",
    "kerala-kshetram": "Kerala Kshetram",
    "rajasthan-tirtha": "Rajasthan",
    "myth-story-tirthas": "Story Tirthas",
    "dattatreya-trail": "Dattatreya",
    "sai-baba-trail": "Sai Baba",
    "modern-temples": "Modern Temples",
    "ramayana-trail": "Ramayana Trail",
    "51-shakti-peeth": "51 Shakti Peeth",
    "ashtavinayak": "Ashtavinayak",
}


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
            + "\n\nPilgrimage literature treats this shrine as a living tirtha — verify custom with temple priests."
        )
    if not detail.get("localBeliefs"):
        detail["localBeliefs"] = (
            "Queue discipline, prasadam sharing, and festival vows shape belief as practice."
        )
    if not detail.get("mythologyDisclaimer"):
        detail["mythologyDisclaimer"] = (
            "Mythological accounts are drawn from Puranic traditions and sthala-purana. "
            "Versions differ by region. For cultural understanding — not historical claim."
        )
    detail["lastUpdated"] = "2026-08-21"
    detail["country"] = detail.get("country") or "India"
    detail["tier"] = detail.get("tier") or "famous"
    if detail.get("lat") and detail.get("lng") and not detail.get("mapQuery"):
        detail["mapQuery"] = detail["name"]
    return detail


def apply_tags(detail: dict, circuit_slugs: list[str]) -> dict:
    tags = list(detail.get("tags") or [])
    labels = list(detail.get("tagLabels") or [])
    for c in circuit_slugs:
        if c not in tags:
            tags.append(c)
            labels.append(CIRCUIT_LABELS.get(c, c))
    detail["tags"] = tags
    detail["tagLabels"] = labels
    return detail


# Seasonal / circuit / Devi–Devta temples people actually visit Aug–Nov
NEW_TEMPLES = [
    # —— Ganesh Chaturthi ——
    {
        "slug": "dagdusheth-ganpati-pune",
        "name": "Shreemant Dagdusheth Halwai Ganpati, Pune",
        "deity": "Lord Ganesha (Dagdusheth)",
        "location": "Budhwar Peth, Pune, Maharashtra",
        "state": "Maharashtra",
        "glyph": "द",
        "famousFor": "Pune’s iconic public Ganeshotsav mandir",
        "summary": "Among Maharashtra’s most visited Ganesha temples — especially packed through Ganesh Chaturthi.",
        "mythology": "Founded by devotee Dagdusheth Halwai after personal loss, the shrine grew into a city-wide centre of Ganesh devotion. Public celebration here shaped modern urban Ganeshotsav culture while retaining daily worship.",
        "scriptureLinks": ["Ganesha Purana devotion", "Pune Ganeshotsav civic tradition"],
        "festivals": ["Ganesh Chaturthi", "Anant Chaturdashi visarjan season", "Maghi Ganesh days"],
        "lat": 18.5162,
        "lng": 73.8561,
        "mapQuery": "Dagdusheth Halwai Ganpati Temple Pune",
        "nearestRail": "Pune Junction",
        "nearestAirport": "Pune",
        "officialWebsite": "https://www.dagdushethganpati.com/",
        "deityFamilies": ["ganesha"],
        "tags_extra": [],
        "tier": "famous",
    },
    {
        "slug": "lalbaugcha-raja-mumbai",
        "name": "Lalbaugcha Raja, Mumbai",
        "deity": "Lord Ganesha (Lalbaugcha Raja)",
        "location": "Lalbaug, Mumbai, Maharashtra",
        "state": "Maharashtra",
        "glyph": "ला",
        "famousFor": "Mumbai’s legendary Ganeshotsav sarvajanik mandal",
        "summary": "Seasonal yet iconic — millions seek mannat darshan during Mumbai’s Ganesh festival fortnight.",
        "mythology": "Lalbaugcha Raja is a public Ganeshotsav murti tradition rather than an ancient stone temple. Its fame rests on vow fulfilment lore and the city’s collective festival bhakti.",
        "festivals": ["Ganesh Chaturthi", "Visarjan days"],
        "lat": 18.9902,
        "lng": 72.8377,
        "mapQuery": "Lalbaugcha Raja Mumbai",
        "nearestRail": "Currey Road / Softail / Mumbai Central area",
        "nearestAirport": "Mumbai",
        "deityFamilies": ["ganesha"],
        "tier": "famous",
        "bestTime": "Ganeshotsav fortnight (book queue time; mid-year humidity is high).",
        "darshanTimings": "Festival-season queues run day and night — follow mandal notices.",
    },
    {
        "slug": "kasba-ganapati-pune",
        "name": "Kasba Ganapati Temple, Pune",
        "deity": "Lord Ganesha (Kasba)",
        "location": "Kasba Peth, Pune, Maharashtra",
        "state": "Maharashtra",
        "glyph": "क",
        "famousFor": "Gram daivat of Pune — first honour in city Ganesh processions",
        "summary": "Pune’s gram-daivat Ganesha; historically first among the city’s public Ganesh mandals.",
        "mythology": "Kasba Ganapati is revered as the guardian deity of old Pune. Festival protocol often gives this shrine ceremonial precedence in city Ganeshotsav.",
        "festivals": ["Ganesh Chaturthi", "Local Pune Ganesh processions"],
        "lat": 18.5195,
        "lng": 73.8553,
        "mapQuery": "Kasba Ganapati Temple Pune",
        "nearestRail": "Pune Junction",
        "nearestAirport": "Pune",
        "deityFamilies": ["ganesha"],
        "tier": "famous",
    },
    {
        "slug": "mahalaxmi-mumbai",
        "name": "Mahalaxmi Temple, Mumbai",
        "deity": "Goddess Mahalakshmi (with Mahakali & Mahasaraswati)",
        "location": "Bhulabhai Desai Road, Mumbai, Maharashtra",
        "state": "Maharashtra",
        "glyph": "म",
        "famousFor": "Sea-facing Devi temple — Navaratri and Diwali crowds",
        "summary": "Mumbai’s primary Mahalaxmi shrine — especially busy in Navaratri and Diwali weeks.",
        "mythology": "Tradition links the temple to the recovery of Devi images from the sea and the blessing of the city’s causeway works. Mahalakshmi here is worshipped with companion forms of Mahakali and Mahasaraswati.",
        "festivals": ["Navaratri", "Diwali / Lakshmi Puja", "Fridays"],
        "lat": 18.9827,
        "lng": 72.8082,
        "mapQuery": "Mahalaxmi Temple Mumbai",
        "nearestRail": "Mahalaxmi",
        "nearestAirport": "Mumbai",
        "deityFamilies": ["lakshmi", "devi", "kali"],
        "tier": "famous",
    },
    # —— Navaratri / Devi ——
    {
        "slug": "vindhyavasini-vindhyachal",
        "name": "Vindhyavasini Devi Temple, Vindhyachal",
        "deity": "Goddess Vindhyavasini",
        "location": "Vindhyachal, Mirzapur, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "वि",
        "famousFor": "Major Navaratri Shakti seat of the Vindhya belt",
        "summary": "One of North India’s busiest Devi yatras in Sharad and Chaitra Navaratri — often paired with Ashtabhuja and Kali Khoh.",
        "mythology": "Vindhyavasini is praised as the goddess who dwells in the Vindhya hills. Local tradition binds her to Devi Mahatmya themes and the protection of the pilgrim road between Kashi and the plateau.",
        "scriptureLinks": ["Devi Mahatmya / Durga Saptashati themes", "Vindhya sthala tradition"],
        "festivals": ["Sharad Navaratri", "Chaitra Navaratri", "Fridays"],
        "lat": 25.1652,
        "lng": 82.5623,
        "mapQuery": "Vindhyavasini Temple Vindhyachal",
        "nearestRail": "Vindhyachal / Mirzapur",
        "nearestAirport": "Varanasi / Prayagraj",
        "deityFamilies": ["devi"],
        "tier": "famous",
        "packages": ["Vindhyachal Navaratri day yatra", "Kashi + Vindhyachal 2-day circuit"],
    },
    {
        "slug": "durga-kund-varanasi",
        "name": "Durga Mandir (Durga Kund), Varanasi",
        "deity": "Goddess Durga",
        "location": "Durga Kund, Varanasi, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "दु",
        "famousFor": "Red Durga temple and kund — Navaratri in Kashi",
        "summary": "Kashi’s celebrated Durga temple beside the kund — heavy Navaratri footfall with the city’s wider Shakti circuit.",
        "mythology": "The temple’s red-stone form and the adjacent kund are woven into Banaras Devi pilgrimage. Many families combine Durga Kund with Vishalakshi and Annapurna on Navaratri evenings.",
        "festivals": ["Sharad Navaratri", "Chaitra Navaratri", "Tuesdays / Fridays"],
        "lat": 25.2885,
        "lng": 82.9990,
        "mapQuery": "Durga Kund Temple Varanasi",
        "nearestRail": "Varanasi Junction / Banaras",
        "nearestAirport": "Varanasi",
        "deityFamilies": ["devi"],
        "tags_extra": ["myth-story-tirthas"],
        "tier": "famous",
    },
    {
        "slug": "annapurna-kashi",
        "name": "Annapurna Temple, Kashi",
        "deity": "Goddess Annapurna",
        "location": "Near Kashi Vishwanath corridor, Varanasi, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "अ",
        "famousFor": "Goddess of food beside Vishwanath — Annakut & Kartik devotion",
        "summary": "Annapurna of Kashi — the nourishing Devi paired with Vishwanath in Banaras theology.",
        "mythology": "Puranic narrative tells of Annapurna feeding Shiva when the world faced hunger — placing food and grace at the heart of Kashi’s sacred economy. Pilgrims still seek her blessing for household sufficiency.",
        "festivals": ["Annakut / Govardhan vicinity observances", "Navaratri", "Kartik"],
        "lat": 25.3107,
        "lng": 83.0107,
        "mapQuery": "Annapurna Temple Varanasi",
        "nearestRail": "Varanasi Junction",
        "nearestAirport": "Varanasi",
        "deityFamilies": ["annapurna", "devi", "shiva"],
        "tags_extra": ["myth-story-tirthas"],
        "tier": "famous",
    },
    {
        "slug": "tarapith",
        "name": "Tarapith Temple",
        "deity": "Goddess Tara (Tarapith)",
        "location": "Tarapith, Birbhum, West Bengal",
        "state": "West Bengal",
        "glyph": "ता",
        "famousFor": "Bengal’s fierce Tara peeth — Kali Puja / Amavasya crowds",
        "summary": "Major Shakta seat of Bengal; especially intense around Kali Puja and dark-night vows.",
        "mythology": "Tarapith venerates Tara in a cremation-ground adjacent Shakta landscape. Sages and householders alike narrate fierce grace that still draws overnight pilgrims.",
        "festivals": ["Kali Puja", "Amavasya nights", "Coinciding Sharad season travel"],
        "lat": 24.1110,
        "lng": 87.7960,
        "mapQuery": "Tarapith Temple Birbhum",
        "nearestRail": "Rampurhat",
        "nearestAirport": "Kolkata / Durgapur",
        "deityFamilies": ["kali", "devi"],
        "tier": "famous",
    },
    {
        "slug": "mahur-renuka-devi",
        "name": "Renuka Devi Temple, Mahur",
        "deity": "Goddess Renuka",
        "location": "Mahur, Nanded district, Maharashtra",
        "state": "Maharashtra",
        "glyph": "रे",
        "famousFor": "Maharashtra Shakti peetha of Renuka Mata",
        "summary": "Hill shrine of Renuka Devi — important for Navaratri and regional Shakti yatras in Marathwada.",
        "mythology": "Renuka, mother of Parashurama in epic memory, is worshipped here as a powerful mother goddess. The Mahur hill forms part of Maharashtra’s living Shakti geography.",
        "festivals": ["Navaratri", "Renuka Yatra days", "Fridays"],
        "lat": 19.8490,
        "lng": 77.9200,
        "mapQuery": "Renuka Devi Temple Mahur",
        "nearestRail": "Nanded / Kinwat region",
        "nearestAirport": "Nanded / Aurangabad",
        "deityFamilies": ["devi"],
        "tier": "famous",
    },
    # —— Kartik / Kashi–Haridwar ——
    {
        "slug": "har-ki-pauri-haridwar",
        "name": "Har Ki Pauri, Haridwar",
        "deity": "Ganga Devi · Har–Hara tirtha",
        "location": "Har Ki Pauri ghat, Haridwar, Uttarakhand",
        "state": "Uttarakhand",
        "glyph": "ह",
        "famousFor": "Evening Ganga aarti — Kartik & festival peak crowds",
        "summary": "Haridwar’s iconic ghat for Ganga aarti and snan — especially packed in Kartik and major bathing dates.",
        "mythology": "Called the footstep of Hari, the ghat is where heaven and earth meet in pilgrim imagination. Brahma Kund traditions and endless deepdaan shape Kartik nights.",
        "festivals": ["Kartik Purnima", "Ganga Dussehra", "Kanwar season (related basin)", "Daily evening aarti"],
        "lat": 29.9567,
        "lng": 78.1710,
        "mapQuery": "Har Ki Pauri Haridwar",
        "nearestRail": "Haridwar Junction",
        "nearestAirport": "Dehradun (Jolly Grant)",
        "deityFamilies": ["devi", "shiva", "vishnu"],
        "tags_extra": ["myth-story-tirthas"],
        "tier": "famous",
        "dressCode": "Modest clothes for ghat; follow police and trust cordons during peak aarti.",
    },
    {
        "slug": "kaal-bhairav-kashi",
        "name": "Kaal Bhairav Temple, Kashi",
        "deity": "Kaal Bhairav",
        "location": "Bharonath / Kaal Bhairav Mandir, Varanasi, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "भ",
        "famousFor": "Kotwal of Kashi — obligatory stop for many Vishwanath yatris",
        "summary": "The fierce guardian of Banaras; pilgrims often take Bhairav’s blessing before or after Vishwanath.",
        "mythology": "Kaal Bhairav is narrated as the police-chief (kotwal) of Kashi — Shiva’s terrifying form who keeps the city’s sacred order. Alcohol offering traditions are local and must be followed only as posted.",
        "festivals": ["Bhairavashtami", "Kartik visits", "Daily guardian darshan"],
        "lat": 25.3176,
        "lng": 83.0140,
        "mapQuery": "Kaal Bhairav Temple Varanasi",
        "nearestRail": "Varanasi Junction",
        "nearestAirport": "Varanasi",
        "deityFamilies": ["bhairav", "shiva"],
        "tags_extra": ["myth-story-tirthas"],
        "tier": "famous",
    },
    {
        "slug": "tulsi-manas-varanasi",
        "name": "Tulsi Manas Temple, Varanasi",
        "deity": "Lord Rama · Ramcharitmanas memory",
        "location": "Sankat Mochan Road area, Varanasi, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "glyph": "तु",
        "famousFor": "Marble Ramayana temple inscribed with Ramcharitmanas",
        "summary": "Modern yet deeply loved Rama shrine where Tulsidas’s Ramcharitmanas lines the walls — popular in Kartik and Ram Navami seasons.",
        "mythology": "Built in the twentieth century as a temple of the Manas, it keeps Tulsidas’s Avadhi epic in stone and song for Banaras pilgrims.",
        "festivals": ["Ram Navami", "Kartik", "Tulsi Jayanti observances", "Daily Manas path"],
        "lat": 25.2825,
        "lng": 82.9998,
        "mapQuery": "Tulsi Manas Temple Varanasi",
        "nearestRail": "Varanasi Junction",
        "nearestAirport": "Varanasi",
        "deityFamilies": ["rama", "vishnu"],
        "tags_extra": ["rama-kshaetra", "ramayana-trail", "modern-temples"],
        "tier": "famous",
    },
    # —— Murugan / Skanda Shashti ——
    {
        "slug": "tiruttani-murugan",
        "name": "Tiruttani Murugan Temple",
        "deity": "Lord Murugan (Tiruttani)",
        "location": "Tiruttani, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "தி",
        "famousFor": "One of the Arupadai Veedu — Skanda Shashti & wedding lore",
        "summary": "Hill Murugan shrine of the Six Abodes — key for Skanda Shashti and Tamil Kartikeya devotion.",
        "mythology": "Tiruttani is counted among Murugan’s six battle-abodes (Arupadai Veedu). Tradition remembers the Lord’s serenity after victory and divine marriage themes celebrated by devotees.",
        "festivals": ["Skanda Shashti", "Thai Poosam", "Panguni Uthiram"],
        "lat": 13.1750,
        "lng": 79.6110,
        "mapQuery": "Tiruttani Murugan Temple",
        "nearestRail": "Tiruttani",
        "nearestAirport": "Chennai",
        "deityFamilies": ["murugan", "shiva"],
        "tags_extra": ["murugan-trail"],
        "tier": "famous",
    },
    {
        "slug": "swamimalai-murugan",
        "name": "Swamimalai Murugan Temple",
        "deity": "Lord Murugan (Swaminatha)",
        "location": "Swamimalai, near Kumbakonam, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "சு",
        "famousFor": "Arupadai Veedu — Murugan as guru of Shiva",
        "summary": "Swaminatha temple where Murugan is worshipped as the teacher of Shiva — essential Skanda circuit stop.",
        "mythology": "Here Murugan is Swaminatha — the Lord who taught the meaning of pranava to Shiva. The stepped hill shrine is among the Six Abodes.",
        "festivals": ["Skanda Shashti", "Monthly Shashti", "Temple car festivals"],
        "lat": 10.9550,
        "lng": 79.3260,
        "mapQuery": "Swamimalai Murugan Temple",
        "nearestRail": "Kumbakonam / Sundaraperumal Kovil",
        "nearestAirport": "Tiruchirappalli",
        "deityFamilies": ["murugan", "shiva"],
        "tags_extra": ["murugan-trail"],
        "tier": "famous",
    },
    {
        "slug": "pazhamudircholai-murugan",
        "name": "Pazhamudircholai Murugan Temple",
        "deity": "Lord Murugan",
        "location": "Pazhamudircholai, near Madurai, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "ப",
        "famousFor": "Forest Arupadai Veedu above Madurai",
        "summary": "Wooded sixth abode of Murugan near Madurai — often combined with Meenakshi and Thiruparankundram.",
        "mythology": "Pazhamudircholai is the fruit-forest abode in the Six Abodes cycle. Classical Tamil devotion praises Murugan’s grace amid the hills above Madurai.",
        "festivals": ["Skanda Shashti", "Thai Poosam", "Panguni festivals"],
        "lat": 10.0420,
        "lng": 78.1730,
        "mapQuery": "Pazhamudircholai Murugan Temple",
        "nearestRail": "Madurai",
        "nearestAirport": "Madurai",
        "deityFamilies": ["murugan", "shiva"],
        "tags_extra": ["murugan-trail"],
        "tier": "famous",
    },
    # —— Krishna / modern ——
    {
        "slug": "parthasarathy-chennai",
        "name": "Parthasarathy Temple, Chennai",
        "deity": "Lord Krishna (Parthasarathy)",
        "location": "Triplicane, Chennai, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "பா",
        "famousFor": "Chennai’s historic Krishna as charioteer of Arjuna",
        "summary": "One of Chennai’s oldest Vishnu–Krishna temples — busy on Ekadashi, Janmashtami, and weekend city darshan.",
        "mythology": "Parthasarathy is Krishna as the charioteer of Arjuna (Partha). The Triplicane shrine anchors coastal Madras Vaishnava life.",
        "festivals": ["Janmashtami", "Vaikuntha Ekadashi", "Brahmotsavam"],
        "lat": 13.0545,
        "lng": 80.2780,
        "mapQuery": "Parthasarathy Temple Triplicane",
        "nearestRail": "Chennai Beach / Fort / Park Town area",
        "nearestAirport": "Chennai",
        "deityFamilies": ["krishna", "vishnu"],
        "tags_extra": ["krishna-lila-trail", "mahabharata-sites"],
        "tier": "famous",
    },
    {
        "slug": "iskcon-bangalore",
        "name": "ISKCON Temple, Bengaluru",
        "deity": "Krishna–Balaram (ISKCON)",
        "location": "Rajajinagar / Hare Krishna Hill, Bengaluru, Karnataka",
        "state": "Karnataka",
        "glyph": "इ",
        "famousFor": "Huge modern Krishna complex — Janmashtami & weekend crowds",
        "summary": "Bengaluru’s landmark ISKCON temple — a major urban Krishna pilgrimage through Janmashtami and Kartik.",
        "mythology": "Part of the global Gaudiya–ISKCON movement centred on Krishna bhakti. The hill complex combines temple, museum, and community prasadam culture.",
        "festivals": ["Janmashtami", "Kartik Damodara month", "Gaura Purnima"],
        "lat": 12.9912,
        "lng": 77.5512,
        "mapQuery": "ISKCON Temple Bangalore Rajajinagar",
        "nearestRail": "Bengaluru City / Yesvantpur",
        "nearestAirport": "Bengaluru",
        "deityFamilies": ["krishna", "vishnu"],
        "tags_extra": ["krishna-lila-trail", "modern-temples"],
        "tier": "famous",
    },
    {
        "slug": "iskcon-chennai",
        "name": "ISKCON Temple, Chennai",
        "deity": "Krishna–Radha (ISKCON)",
        "location": "East Coast Road / Injambakkam area, Chennai, Tamil Nadu",
        "state": "Tamil Nadu",
        "glyph": "இ",
        "famousFor": "Seaside ISKCON complex — Janmashtami city crowds",
        "summary": "Chennai ISKCON draws large Janmashtami and Sunday crowds with ocean-adjacent campus devotion.",
        "mythology": "Modern Krishna temple in the ISKCON lineage — chanting, prasadam, and festival drama for urban pilgrims.",
        "festivals": ["Janmashtami", "Kartik", "Ratha Yatra events"],
        "lat": 12.9485,
        "lng": 80.2590,
        "mapQuery": "ISKCON Temple Chennai ECR",
        "nearestRail": "Chennai suburban network",
        "nearestAirport": "Chennai",
        "deityFamilies": ["krishna", "vishnu"],
        "tags_extra": ["krishna-lila-trail", "modern-temples"],
        "tier": "famous",
    },
    # —— Rajasthan / circuits ——
    {
        "slug": "jagdish-temple-udaipur",
        "name": "Jagdish Temple, Udaipur",
        "deity": "Lord Vishnu (Jagdish / Jagannath form)",
        "location": "City Palace Road, Udaipur, Rajasthan",
        "state": "Rajasthan",
        "glyph": "ज",
        "famousFor": "Indo-Aryan Vishnu temple in Udaipur’s old city",
        "summary": "Udaipur’s central Jagdish temple — popular with lake-city travellers and Kartik–Diwali season visitors.",
        "mythology": "Built under Mewar patronage, Jagdish Temple places Vishnu at the heart of the palace-town’s sacred skyline.",
        "festivals": ["Janmashtami", "Diwali lights in the old city", "Daily aarti"],
        "lat": 24.5797,
        "lng": 73.6836,
        "mapQuery": "Jagdish Temple Udaipur",
        "nearestRail": "Udaipur City",
        "nearestAirport": "Udaipur",
        "deityFamilies": ["vishnu", "krishna"],
        "tags_extra": ["rajasthan-tirtha"],
        "tier": "famous",
    },
    {
        "slug": "ashapura-mata-nadol",
        "name": "Ashapura Mata Temple, Nadol",
        "deity": "Goddess Ashapura",
        "location": "Nadol, Pali district, Rajasthan",
        "state": "Rajasthan",
        "glyph": "आ",
        "famousFor": "Kuldevi of many western Rajasthan clans",
        "summary": "Historic Ashapura seat in Godwar — Navaratri family yatras from across Rajasthan–Gujarat.",
        "mythology": "Ashapura Mata is the hope-giving mother for many Rajput and merchant lineages. Navaratri fills Nadol with clan banners and vows.",
        "festivals": ["Navaratri", "Chaitra Navaratri", "Family kuldevi days"],
        "lat": 25.4080,
        "lng": 73.4550,
        "mapQuery": "Ashapura Mata Temple Nadol",
        "nearestRail": "Falna / Pali",
        "nearestAirport": "Udaipur / Jodhpur",
        "deityFamilies": ["devi"],
        "tags_extra": ["rajasthan-tirtha"],
        "tier": "regional",
    },
    {
        "slug": "sheetla-mata-mandir-jaipur",
        "name": "Sheetla Mata Temple, Jaipur region",
        "deity": "Goddess Sheetla",
        "location": "Near Chandpole / traditional Sheetla seats, Jaipur, Rajasthan",
        "state": "Rajasthan",
        "glyph": "शी",
        "famousFor": "Sheetla Ashtami & cooling-mother vows after Holi cycle; still visited in autumn family trips",
        "summary": "Jaipur-area Sheetla devotion popular with families seeking children’s health blessings.",
        "mythology": "Sheetla Mata is worshipped as the cooling mother who protects from feverish afflictions. Local lanes keep her Fridays and Ashtami vows alive.",
        "festivals": ["Sheetla Ashtami", "Fridays", "Navaratri-adjacent family visits"],
        "lat": 26.9260,
        "lng": 75.8235,
        "mapQuery": "Sheetla Mata Temple Jaipur",
        "nearestRail": "Jaipur",
        "nearestAirport": "Jaipur",
        "deityFamilies": ["devi"],
        "tags_extra": ["rajasthan-tirtha"],
        "tier": "regional",
    },
]


def rebuild_temples_index() -> int:
    """Rebuild temples.json from detail files without touching groups/circuits."""
    groups = load_json(DATA / "groups.json")
    priority: list[str] = []
    for g, meta in (groups.get("fixed") or {}).items():
        for s in meta.get("order") or []:
            if s not in priority:
                priority.append(s)

    index = []
    for path in sorted(TEMPLES.glob("*.json")):
        detail = load_json(path)
        slug = detail["slug"]
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
                "tags": detail.get("tags") or [],
                "tagLabels": detail.get("tagLabels") or [],
                "deityFamilies": detail.get("deityFamilies") or [],
                "summary": detail.get("summary", ""),
                "famousFor": detail.get("famousFor", ""),
            }
        )

    index.sort(
        key=lambda t: (
            priority.index(t["slug"]) if t["slug"] in priority else 9999,
            t["name"].casefold(),
        )
    )
    dump_json(DATA / "temples.json", index)
    return len(index)


def main() -> None:
    deity_keys = set(load_json(DATA / "deities.json").keys())
    existing = {p.stem for p in TEMPLES.glob("*.json")}
    created = []

    for seed in NEW_TEMPLES:
        seed = dict(seed)
        slug = seed["slug"]
        if slug in existing:
            print("skip existing", slug)
            continue
        tags_extra = seed.pop("tags_extra", None) or []
        tier = seed.pop("tier", "famous")
        fams = [f for f in (seed.pop("deityFamilies", None) or []) if f in deity_keys]
        detail = base_detail(seed)
        detail["tier"] = tier
        detail["deityFamilies"] = fams
        detail = apply_tags(detail, tags_extra)
        detail = attach_portal(detail)
        detail = enrich_myth_fields(detail)
        if detail.get("lat") is None or detail.get("lng") is None:
            raise SystemExit(f"Missing coordinates for {slug}")
        dump_json(TEMPLES / f"{slug}.json", detail)
        created.append(slug)
        existing.add(slug)

    # Tag popular existing temples into seasonal/open circuits where helpful
    open_boost = {
        "kanaka-durga-vijayawada": ["myth-story-tirthas"],
        "chamundeshwari-mysuru": ["myth-story-tirthas"],
        "kalkaji-mandir-delhi": ["myth-story-tirthas"],
        "neelkanth-mahadev-rishikesh": ["myth-story-tirthas"],
        "mansa-devi-haridwar": ["myth-story-tirthas"],
        "chandi-devi-haridwar": ["myth-story-tirthas"],
        "khatushyam": ["rajasthan-tirtha", "myth-story-tirthas"],
        "vaishno-devi": ["myth-story-tirthas"],
        "siddhivinayak-mumbai": [],  # keep as-is; already famous
    }
    boosted = 0
    for slug, circuits in open_boost.items():
        path = TEMPLES / f"{slug}.json"
        if not path.exists() or not circuits:
            continue
        d = load_json(path)
        before = list(d.get("tags") or [])
        d = apply_tags(d, circuits)
        if d.get("tags") != before:
            dump_json(path, d)
            boosted += 1

    total = rebuild_temples_index()
    print(f"Created {len(created)} temples: {', '.join(created)}")
    print(f"Boosted tags on {boosted} existing temples")
    print(f"temples.json entries: {total}")


if __name__ == "__main__":
    main()
