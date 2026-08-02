#!/usr/bin/env python3
"""Add more temples + attach official state portal links; then re-sync groups."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))
from sync_groups import SEEDS, base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")

NEW = [
    # Andhra Pradesh — aptemples.org / TTD ecosystem
    {
        "slug": "tirumala-venkateswara",
        "name": "Sri Venkateswara Temple, Tirumala",
        "deity": "Lord Venkateswara (Balaji)",
        "location": "Tirumala, Tirupati, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "country": "India",
        "glyph": "ति",
        "famousFor": "One of the world’s most visited Vishnu temples",
        "summary": "Tirumala Venkateswara — the foremost Andhra Pradesh pilgrimage, administered via TTD and listed among AP’s flagship temples.",
        "mythology": "Lord Venkateswara of Tirumala is venerated as Vishnu in Kaliyuga. The seven hills (Saptagiri) and centuries of royal patronage make Tirupati–Tirumala the spiritual centre of Andhra Pradesh pilgrimage. For official seva, tickets and timings, use Tirumala Tirupati Devasthanams and the AP Temples portal.",
        "scriptureLinks": ["Vaishnava tradition", "Varaha / Venkatachala mahatmya traditions"],
        "lat": 13.6833,
        "lng": 79.3472,
        "mapQuery": "Tirumala Venkateswara Temple",
        "nearestRail": "Tirupati",
        "nearestAirport": "Tirupati / Chennai",
        "officialWebsite": "https://www.tirumala.org/",
        "festivals": ["Brahmotsavam", "Vaikunta Ekadasi", "Ratha Sapthami"],
        "dressCode": "Traditional dress required for special entry/sevas — follow TTD rules.",
        "tags_extra": [],
    },
    {
        "slug": "simhachalam",
        "name": "Simhachalam Varaha Lakshmi Narasimha Temple",
        "deity": "Lord Varaha Lakshmi Narasimha",
        "location": "Simhachalam, Visakhapatnam, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "country": "India",
        "glyph": "सि",
        "famousFor": "Sandal-paste covered Narasimha; coastal AP pilgrimage",
        "summary": "Hill temple of Varaha Lakshmi Narasimha near Visakhapatnam — a major shrine highlighted across Andhra Pradesh temple circuits.",
        "mythology": "Simhachalam is dedicated to Narasimha in a rare combined form. For most of the year the deity is covered in sandal paste, revealed on Chandanotsavam. Refer AP Temples / local Devasthanam notices for current schedules.",
        "lat": 17.7665,
        "lng": 83.2506,
        "mapQuery": "Simhachalam Temple Visakhapatnam",
        "nearestRail": "Visakhapatnam",
        "nearestAirport": "Visakhapatnam",
        "officialWebsite": "https://www.aptemples.org/en-in/home",
        "festivals": ["Chandanotsavam", "Narasimha Jayanti"],
    },
    {
        "slug": "kanaka-durga-vijayawada",
        "name": "Kanaka Durga Temple, Vijayawada",
        "deity": "Goddess Kanaka Durga",
        "location": "Indrakeeladri, Vijayawada, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "country": "India",
        "glyph": "दु",
        "famousFor": "Hilltop Shakti shrine on the Krishna",
        "summary": "Kanaka Durga on Indrakeeladri Hill — Vijayawada’s principal Devi temple and a flagship Andhra Pradesh pilgrimage stop.",
        "mythology": "Tradition places Goddess Durga’s victory lore on Indrakeeladri. Dasara celebrations draw huge crowds. Cross-check timings on AP Temples / temple notices.",
        "lat": 16.5154,
        "lng": 80.6094,
        "mapQuery": "Kanaka Durga Temple Vijayawada",
        "nearestRail": "Vijayawada Junction",
        "nearestAirport": "Vijayawada / Gannavaram",
        "officialWebsite": "https://www.aptemples.org/en-in/home",
        "festivals": ["Dasara / Navaratri", "Varalakshmi Vratam season"],
    },
    {
        "slug": "annavaram-satyanarayana",
        "name": "Satyanarayana Swamy Temple, Annavaram",
        "deity": "Lord Satyanarayana / Veera Venkata Satyanarayana",
        "location": "Annavaram, Kakinada district, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "country": "India",
        "glyph": "अ",
        "famousFor": "Satyanarayana Vratham hill temple",
        "summary": "Annavaram is famed for Satyanarayana Swamy worship and family vrathams — a major coastal Andhra shrine.",
        "mythology": "The Ratnagiri hill temple of Annavaram is dedicated to Satyanarayana. Pilgrims widely perform Satyanarayana Vratham here.",
        "lat": 17.2820,
        "lng": 82.4010,
        "mapQuery": "Annavaram Satyanarayana Temple",
        "nearestRail": "Annavaram / Tuni",
        "nearestAirport": "Rajahmundry / Visakhapatnam",
        "officialWebsite": "https://www.aptemples.org/en-in/home",
    },
    {
        "slug": "kanipakam",
        "name": "Kanipakam Vinayaka Temple",
        "deity": "Lord Ganesha (Varasiddhi Vinayaka)",
        "location": "Kanipakam, Chittoor, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "country": "India",
        "glyph": "वि",
        "famousFor": "Self-manifest Ganesha shrine near Tirupati",
        "summary": "Kanipakam Vinayaka — popular AP Ganesha temple often combined with Tirupati yatra.",
        "mythology": "Local tradition describes a self-manifest (swayambhu) Vinayaka. Frequently visited on the Tirupati–Srikalahasti loop.",
        "lat": 13.2750,
        "lng": 79.0770,
        "mapQuery": "Kanipakam Temple",
        "nearestRail": "Chittoor / Tirupati",
        "nearestAirport": "Tirupati",
        "officialWebsite": "https://www.aptemples.org/en-in/home",
    },
    {
        "slug": "lepakshi-veerabhadra",
        "name": "Veerabhadra Temple, Lepakshi",
        "deity": "Lord Veerabhadra",
        "location": "Lepakshi, Anantapur, Andhra Pradesh",
        "state": "Andhra Pradesh",
        "country": "India",
        "glyph": "ले",
        "famousFor": "Vijayanagara murals & hanging pillar",
        "summary": "Lepakshi Veerabhadra temple — heritage Shaiva shrine famous for murals, the hanging pillar, and the monolithic Nandi.",
        "mythology": "Linked to Veerabhadra (fierce form of Shiva) and Vijayanagara patronage. Also woven into local Ramayana ‘Lepakshi’ lore of Jatayu.",
        "scriptureLinks": ["Shaiva tradition", "Local Ramayana Jatayu lore", "Vijayanagara history"],
        "lat": 13.8040,
        "lng": 77.6090,
        "mapQuery": "Lepakshi Veerabhadra Temple",
        "nearestRail": "Hindupur",
        "nearestAirport": "Bengaluru / Kadapa",
        "officialWebsite": "https://www.aptemples.org/en-in/home",
        "tags_extra": ["ramayana-trail"],
    },
    # Telangana
    {
        "slug": "yadagirigutta",
        "name": "Yadadri Lakshmi Narasimha Temple",
        "deity": "Lord Lakshmi Narasimha",
        "location": "Yadagirigutta, Yadadri Bhuvanagiri, Telangana",
        "state": "Telangana",
        "country": "India",
        "glyph": "य",
        "famousFor": "Rebuilt hill Narasimha temple of Telangana",
        "summary": "Yadadri (Yadagirigutta) — major Telangana Narasimha pilgrimage under state endowments oversight.",
        "mythology": "Narasimha is said to have appeared to the sage Yadarishi in the caves here. The modern reconstructed temple is a Telangana landmark.",
        "lat": 17.5860,
        "lng": 78.9440,
        "mapQuery": "Yadagirigutta Temple",
        "nearestRail": "Raigiri / Hyderabad region",
        "nearestAirport": "Hyderabad",
        "officialWebsite": "https://endowments.ts.nic.in/",
    },
    {
        "slug": "bhadrachalam",
        "name": "Sita Ramachandra Swamy Temple, Bhadrachalam",
        "deity": "Lord Rama",
        "location": "Bhadrachalam, Telangana",
        "state": "Telangana",
        "country": "India",
        "glyph": "भ",
        "famousFor": "Godavari-side Rama temple; Ramayana trail",
        "summary": "Bhadrachalam Rama temple on the Godavari — a key Telangana and Ramayana-trail pilgrimage.",
        "mythology": "Associated with Rama devotion and Godavari sacred geography; famous for Vaikunta Ekadasi and Sri Rama Navami celebrations.",
        "lat": 17.6680,
        "lng": 80.8880,
        "mapQuery": "Bhadrachalam Temple",
        "nearestRail": "Bhadrachalam Road",
        "nearestAirport": "Rajahmundry / Hyderabad",
        "officialWebsite": "https://endowments.ts.nic.in/",
        "tags_extra": ["ramayana-trail"],
    },
    {
        "slug": "vemulawada",
        "name": "Sri Raja Rajeshwara Temple, Vemulawada",
        "deity": "Lord Shiva (Raja Rajeshwara)",
        "location": "Vemulawada, Rajanna Sircilla, Telangana",
        "state": "Telangana",
        "country": "India",
        "glyph": "वे",
        "famousFor": "Prominent Telangana Shaiva shrine",
        "summary": "Vemulawada Raja Rajeshwara — one of Telangana’s foremost Shiva temples listed by the Endowments Department.",
        "mythology": "A major Shaiva centre of the Deccan with strong regional pilgrimage traditions and festival crowds.",
        "lat": 18.4670,
        "lng": 78.8680,
        "mapQuery": "Vemulawada Temple",
        "nearestRail": "Karimnagar region",
        "nearestAirport": "Hyderabad",
        "officialWebsite": "https://endowments.ts.nic.in/",
    },
    # Karnataka
    {
        "slug": "chamundeshwari-mysuru",
        "name": "Chamundeshwari Temple, Mysuru",
        "deity": "Goddess Chamundeshwari",
        "location": "Chamundi Hills, Mysuru, Karnataka",
        "state": "Karnataka",
        "country": "India",
        "glyph": "च",
        "famousFor": "Mysuru Dasara deity",
        "summary": "Chamundeshwari of Mysuru — hill shrine central to Karnataka’s Dasara tradition.",
        "mythology": "Goddess Chamunda’s victory over demon Mahishasura is celebrated in Mysuru lore; the hill temple overlooks the city.",
        "lat": 12.2726,
        "lng": 76.6707,
        "mapQuery": "Chamundeshwari Temple Mysore",
        "nearestRail": "Mysuru",
        "nearestAirport": "Mysuru / Bengaluru",
        "officialWebsite": "https://itms.kar.nic.in/hrcehome/index.php",
        "festivals": ["Mysuru Dasara", "Navaratri"],
    },
    {
        "slug": "murudeshwar",
        "name": "Murudeshwar Temple",
        "deity": "Lord Shiva",
        "location": "Murudeshwar, Uttara Kannada, Karnataka",
        "state": "Karnataka",
        "country": "India",
        "glyph": "मु",
        "famousFor": "Giant Shiva statue & sea-facing gopura",
        "summary": "Murudeshwar — coastal Karnataka Shiva temple famous for its towering statue and Arabian Sea setting.",
        "mythology": "Linked to the Ravana–Atmalinga legend cycle of coastal Karnataka Shaivism.",
        "lat": 14.0943,
        "lng": 74.4844,
        "mapQuery": "Murudeshwar Temple",
        "nearestRail": "Murdeshwar",
        "nearestAirport": "Mangaluru / Hubballi",
        "officialWebsite": "https://itms.kar.nic.in/hrcehome/index.php",
        "tags_extra": ["ramayana-trail"],
    },
    {
        "slug": "mookambika-kollur",
        "name": "Mookambika Temple, Kollur",
        "deity": "Goddess Mookambika",
        "location": "Kollur, Udupi, Karnataka",
        "state": "Karnataka",
        "country": "India",
        "glyph": "मू",
        "famousFor": "Powerful coastal Karnataka Devi temple",
        "summary": "Kollur Mookambika — major Shakti shrine of Karnataka’s coastal belt.",
        "mythology": "Associated with Adi Shankaracharya traditions and Devi worship; a classic Karnataka Devi yatra stop with Kerala pilgrim traffic too.",
        "lat": 13.8630,
        "lng": 74.8140,
        "mapQuery": "Mookambika Temple Kollur",
        "nearestRail": "Kundapura / Udupi",
        "nearestAirport": "Mangaluru",
        "officialWebsite": "https://itms.kar.nic.in/hrcehome/index.php",
    },
    # Kerala
    {
        "slug": "guruvayur",
        "name": "Guruvayur Sri Krishna Temple",
        "deity": "Lord Krishna (Guruvayurappan)",
        "location": "Guruvayur, Thrissur, Kerala",
        "state": "Kerala",
        "country": "India",
        "glyph": "गु",
        "famousFor": "Kerala’s foremost Krishna temple",
        "summary": "Guruvayurappan temple — among Kerala’s most important Vaishnava shrines, under Guruvayur Devaswom.",
        "mythology": "Guruvayur is dedicated to Krishna in a child-form tradition. Strict dress and entry customs apply — follow Devaswom rules.",
        "lat": 10.5943,
        "lng": 76.0395,
        "mapQuery": "Guruvayur Temple",
        "nearestRail": "Guruvayur / Thrissur",
        "nearestAirport": "Kochi",
        "officialWebsite": "https://www.guruvayurdevaswom.nic.in/",
        "dressCode": "Traditional Kerala temple dress code strictly enforced.",
    },
    {
        "slug": "sabarimala",
        "name": "Sabarimala Ayyappa Temple",
        "deity": "Lord Ayyappa",
        "location": "Sabarimala, Pathanamthitta, Kerala",
        "state": "Kerala",
        "country": "India",
        "glyph": "अ",
        "famousFor": "Seasonal hill pilgrimage of Ayyappa",
        "summary": "Sabarimala — Kerala’s great seasonal Ayyappa pilgrimage with unique vrata discipline.",
        "mythology": "Ayyappa of Sabarimala is central to Kerala’s forest-hill pilgrimage culture. Season, queue and vrata rules are regulated — follow Travancore Devaswom / official advisories only.",
        "lat": 9.4356,
        "lng": 77.0811,
        "mapQuery": "Sabarimala Temple",
        "nearestRail": "Chengannur / Kottayam then road",
        "nearestAirport": "Kochi / Madurai",
        "officialWebsite": "https://travancoredevaswomboard.org/",
        "bestTime": "Mandala–Makaravilakku season (approx Nov–Jan) and other notified openings.",
        "dressCode": "Black/blue traditional pilgrim attire and vrata norms — follow official rules.",
    },
    # Rajasthan
    {
        "slug": "khatushyam",
        "name": "Khatu Shyam Temple",
        "deity": "Shyam Baba (Barbarika tradition)",
        "location": "Khatu, Sikar, Rajasthan",
        "state": "Rajasthan",
        "country": "India",
        "glyph": "खा",
        "famousFor": "Huge Rajasthan pilgrimage for Shyam Baba",
        "summary": "Khatu Shyam — one of Rajasthan’s busiest pilgrimage temples, under popular Devasthan / trust administration patterns.",
        "mythology": "Linked to Barbarika (son of Ghatotkacha) from Mahabharata tradition, worshipped as Shyam. Falgun Mela is a major gathering.",
        "scriptureLinks": ["Mahabharata tradition", "Rajasthan folk-Vaishnava devotion"],
        "lat": 27.3640,
        "lng": 75.4030,
        "mapQuery": "Khatu Shyam Temple",
        "nearestRail": "Ringas / Jaipur",
        "nearestAirport": "Jaipur",
        "officialWebsite": "https://devasthan.rajasthan.gov.in/",
        "tags_extra": ["mahabharata-sites"],
        "festivals": ["Falgun Mela", "Ekadeshi days"],
    },
    {
        "slug": "salasar-balaji",
        "name": "Salasar Balaji Temple",
        "deity": "Lord Hanuman (Salasar Balaji)",
        "location": "Salasar, Churu, Rajasthan",
        "state": "Rajasthan",
        "country": "India",
        "glyph": "स",
        "famousFor": "Rajasthan Hanuman pilgrimage",
        "summary": "Salasar Balaji — major Hanuman shrine of Rajasthan’s Shekhawati pilgrimage belt.",
        "mythology": "A living Hanuman devotion centre of Rajasthan, often combined with Khatu Shyam on the same yatra.",
        "lat": 27.7270,
        "lng": 74.7170,
        "mapQuery": "Salasar Balaji Temple",
        "nearestRail": "Sujangarh / Jaipur",
        "nearestAirport": "Jaipur",
        "officialWebsite": "https://devasthan.rajasthan.gov.in/",
        "tags_extra": ["ramayana-trail"],
    },
    # Maharashtra extras
    {
        "slug": "tuljapur-bhavani",
        "name": "Tulja Bhavani Temple",
        "deity": "Goddess Bhavani",
        "location": "Tuljapur, Dharashiv, Maharashtra",
        "state": "Maharashtra",
        "country": "India",
        "glyph": "तु",
        "famousFor": "One of Maharashtra’s Shakti peeth-like Ambabai shrines",
        "summary": "Tulja Bhavani — among the foremost Devi temples of Maharashtra (Shakti tradition of the Deccan).",
        "mythology": "Goddess Bhavani of Tuljapur is central to Maratha and Deccan Shakti devotion; associated in popular memory with Chhatrapati Shivaji’s worship.",
        "lat": 18.0100,
        "lng": 76.0700,
        "mapQuery": "Tuljapur Bhavani Temple",
        "nearestRail": "Solapur / Osmanabad region",
        "nearestAirport": "Solapur / Aurangabad",
        "officialWebsite": "https://www.maharashtratourism.gov.in/",
    },
    {
        "slug": "pandharpur-vitthal",
        "name": "Vitthal-Rukmini Temple, Pandharpur",
        "deity": "Lord Vitthal (Vithoba) & Rukmini",
        "location": "Pandharpur, Maharashtra",
        "state": "Maharashtra",
        "country": "India",
        "glyph": "पं",
        "famousFor": "Warkari pilgrimage heartland",
        "summary": "Pandharpur Vitthal — the emotional centre of Maharashtra’s Warkari bhakti tradition.",
        "mythology": "Vitthal of Pandharpur is Krishna-Vishnu for the Warkari saints (Dnyaneshwar, Tukaram and others). Ashadhi and Kartiki Ekadashi processions are iconic.",
        "lat": 17.6745,
        "lng": 75.3237,
        "mapQuery": "Pandharpur Vitthal Temple",
        "nearestRail": "Pandharpur",
        "nearestAirport": "Pune / Solapur",
        "officialWebsite": "https://www.maharashtratourism.gov.in/",
        "festivals": ["Ashadhi Ekadashi", "Kartiki Ekadashi"],
    },
    # UP / famous extras
    {
        "slug": "vaishno-devi",
        "name": "Shri Mata Vaishno Devi",
        "deity": "Goddess Vaishno Devi",
        "location": "Trikuta Hills, Katra, Jammu",
        "state": "Jammu and Kashmir",
        "country": "India",
        "glyph": "वै",
        "famousFor": "Himalayan Devi yatra administered by shrine board",
        "summary": "Vaishno Devi — one of India’s largest Devi pilgrimages, administered by the Shrine Board.",
        "mythology": "Vaishno Devi is worshipped as a form of the Goddess on Trikuta hills. Official registration and track rules are mandatory in peak seasons.",
        "lat": 33.0300,
        "lng": 74.9490,
        "mapQuery": "Vaishno Devi Katra",
        "nearestRail": "Katra / Jammu Tawi",
        "nearestAirport": "Jammu",
        "officialWebsite": "https://www.maavaishnodevi.org/",
        "bestTime": "September–June; monsoon/winter advisories apply.",
    },
]


def attach_portal(detail: dict) -> dict:
    state = detail.get("state", "")
    portal = PORTALS.get(state)
    if not portal:
        return detail
    # keep temple-specific official site if already a trust URL; still record state portal in sources
    sources = detail.get("sources", [])
    line = f"{portal['portalName']}: {portal['portalUrl']}"
    if line not in sources:
        sources = [line] + list(sources)
    for a in portal.get("also", []):
        extra = f"{a['name']}: {a['url']}"
        if extra not in sources:
            sources.append(extra)
    detail["sources"] = sources
    detail["statePortal"] = {
        "name": portal["portalName"],
        "url": portal["portalUrl"],
        "slug": portal["slug"],
    }
    # If officialWebsite is generic tourism.gov.in, upgrade to state portal
    if detail.get("officialWebsite") in ("https://tourism.gov.in/", "", None):
        detail["officialWebsite"] = portal["portalUrl"]
    return detail


def main():
    created = []
    for seed in NEW:
        slug = seed["slug"]
        path = TEMPLES / f"{slug}.json"
        tags_extra = seed.pop("tags_extra", [])
        if path.exists():
            detail = load_json(path)
        else:
            detail = base_detail(seed)
            created.append(slug)
        # merge important fields
        for k, v in seed.items():
            if k == "slug":
                continue
            if k not in detail or not detail.get(k) or detail.get(k) in (
                "https://tourism.gov.in/",
                "See regional railhead; confirm current connectivity.",
            ):
                detail[k] = v
        # open tags
        tags = list(detail.get("tags", []))
        for t in tags_extra:
            if t not in tags:
                tags.append(t)
        detail["tags"] = tags
        detail = attach_portal(detail)
        dump_json(path, detail)

    # attach portals to ALL existing temples
    for path in TEMPLES.glob("*.json"):
        detail = load_json(path)
        detail = attach_portal(detail)
        dump_json(path, detail)

    print(f"Created/updated {len(NEW)} featured temples; new files: {created}")
    # re-run sync for index/tags (does not delete new temples)
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])


if __name__ == "__main__":
    main()
