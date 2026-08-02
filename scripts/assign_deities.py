#!/usr/bin/env python3
"""
Assign deityFamilies on every temple and add Krishna / Vishnu supporting temples
(Braj, Bet Dwarka, Nathdwara, Srirangam, etc.).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))
from sync_groups import base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")
DEITIES = load_json(DATA / "deities.json")

# Manual overrides win over heuristics (slug → families)
OVERRIDES: dict[str, list[str]] = {
    "dwarka": ["krishna", "vishnu"],
    "jagannath-puri": ["krishna", "vishnu", "devi"],  # Vimala peetha in complex
    "pandharpur-vitthal": ["krishna", "vishnu"],
    "khatushyam": ["krishna"],
    "guruvayur": ["krishna", "vishnu"],
    "udupi-krishna": ["krishna", "vishnu"],
    "govind-dev-ji-jaipur": ["krishna", "vishnu"],
    "tirumala-venkateswara": ["vishnu"],
    "badrinath": ["vishnu"],
    "padmanabhaswamy-thiruvananthapuram": ["vishnu"],
    "annavaram-satyanarayana": ["vishnu"],
    "yadagirigutta": ["vishnu"],
    "simhachalam": ["vishnu"],
    "mallikarjuna-srisailam": ["shiva", "devi"],
    "vaidyanath-deoghar": ["shiva", "devi"],
    "meenakshi-madurai": ["devi", "shiva"],
    "rameswaram": ["shiva", "rama"],  # Rama worshipped Shiva; Shaiva primary
    "bhadrachalam": ["rama", "vishnu"],
    "ayodhya-ram-mandir": ["rama", "vishnu"],
    "chitrakoot-ramghat": ["rama"],
    "seetha-amman-nuwara-eliya": ["rama", "devi"],
    "sabarimala": ["ayyappa"],
    "akshardham-delhi": ["vishnu"],  # Swaminarayan–Vaishnava stream
    "akshardham-gandhinagar": ["vishnu"],
    "shirdi-sai": [],  # multi-faith saint — skip deity browse
    "belur-math": [],
    "mount-kailash": ["shiva"],
    "pashupatinath": ["shiva"],
    "muktinath": ["vishnu", "devi"],
    "kurukshetra-brahmasarovar": ["krishna", "vishnu"],
    "katyayani-vrindavan": ["devi"],
    "gangotri": ["devi"],
    "yamunotri": ["devi"],
    # Guardrails against heuristic false positives
    "brajeshwari-kangra": ["devi"],  # name contains “braj” but is a Devi peetha
    "dakshineswar-kali": ["devi"],  # “Ramakrishna” must not imply Krishna temple
    "kanaka-durga-vijayawada": ["devi"],  # Krishna river ≠ Krishna deity
    "nageshwar": ["shiva"],  # Jyotirlinga near Dwarka, not a Krishna shrine
    "prabhas-chandrabhaga": ["devi"],
}

NEW = [
    {
        "slug": "bet-dwarka",
        "name": "Bet Dwarka (Beyt Dwarka)",
        "deity": "Lord Krishna (Dwarkadhish / Bet Dwarka)",
        "location": "Bet Dwarka island, Devbhoomi Dwarka, Gujarat",
        "state": "Gujarat",
        "country": "India",
        "glyph": "बे",
        "famousFor": "Island Krishna shrine of the Dwarka yatra",
        "summary": "Bet (Beyt) Dwarka — the island temple pilgrims traditionally combine with mainland Dwarkadhish.",
        "mythology": "Bet Dwarka is linked in pilgrimage memory to Krishna’s residence and to the wider Dwarka–Prabhas sacred coast. Boat access and island darshan complete many Gujarat Krishna yatras after the mainland Dwarkadhish temple.",
        "scriptureLinks": ["Bhagavata Purana", "Dwarka mahatmya / pilgrimage tradition"],
        "lat": 22.4490,
        "lng": 69.1200,
        "mapQuery": "Bet Dwarka Temple",
        "nearestRail": "Dwarka",
        "nearestAirport": "Jamnagar / Rajkot",
        "officialWebsite": "https://www.gujarattourism.com/",
        "festivals": ["Janmashtami", "Tulsi Vivah season"],
        "packages": ["Dwarka + Bet Dwarka day circuit", "Saurashtra Krishna yatra"],
        "deityFamilies": ["krishna", "vishnu"],
    },
    {
        "slug": "krishna-janmabhoomi-mathura",
        "name": "Krishna Janmabhoomi, Mathura",
        "deity": "Lord Krishna",
        "location": "Mathura, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "country": "India",
        "glyph": "कृ",
        "famousFor": "Traditional birthplace complex of Krishna in Mathura",
        "summary": "Krishna Janmabhoomi — the spiritual centre of Mathura in the Braj yatra.",
        "mythology": "Mathura is celebrated in the Bhagavata Purana as Krishna’s birthplace. The Janmabhoomi complex is the axis of Braj pilgrimage before devotees move on to Vrindavan, Gokul, and Barsana.",
        "scriptureLinks": ["Bhagavata Purana", "Braj mahatmya traditions"],
        "lat": 27.5046,
        "lng": 77.6690,
        "mapQuery": "Krishna Janmabhoomi Mathura",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "officialWebsite": "https://uptourism.gov.in/",
        "festivals": ["Janmashtami", "Holi of Braj"],
        "deityFamilies": ["krishna", "vishnu"],
    },
    {
        "slug": "radha-raman-vrindavan",
        "name": "Radha Raman Temple, Vrindavan",
        "deity": "Lord Krishna (Radha Raman)",
        "location": "Vrindavan, Mathura, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "country": "India",
        "glyph": "रा",
        "famousFor": "Self-manifest Krishna of Gopala Bhatta Goswami tradition",
        "summary": "Radha Raman — one of Vrindavan’s most revered classical Goswami temples.",
        "mythology": "Associated with Gopala Bhatta Goswami of the Gaudiya tradition; the small self-manifest deity is treasured for intimate darshan and unbroken seva lineage in Vrindavan.",
        "lat": 27.5835,
        "lng": 77.6965,
        "mapQuery": "Radha Raman Temple Vrindavan",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "officialWebsite": "https://uptourism.gov.in/",
        "festivals": ["Radha Raman Janmashtami", "Annkut"],
        "deityFamilies": ["krishna", "vishnu"],
    },
    {
        "slug": "radha-vallabh-vrindavan",
        "name": "Radha Vallabh Temple, Vrindavan",
        "deity": "Radha–Krishna (Radha Vallabh)",
        "location": "Vrindavan, Mathura, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "country": "India",
        "glyph": "व",
        "famousFor": "Radhavallabha sampradaya seat in Vrindavan",
        "summary": "Radha Vallabh — a major Vrindavan temple emphasising Radha’s primacy in Braj bhakti.",
        "mythology": "Centre of the Radhavallabha tradition founded by Hith Harivansh. Music, seva, and Radha-centred theology distinguish this shrine within Vrindavan’s dense sacred map.",
        "lat": 27.5820,
        "lng": 77.6980,
        "mapQuery": "Radha Vallabh Temple Vrindavan",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "officialWebsite": "https://uptourism.gov.in/",
        "deityFamilies": ["krishna", "vishnu"],
    },
    {
        "slug": "barsana-radha-rani",
        "name": "Radha Rani Temple, Barsana",
        "deity": "Goddess Radha (Radha Rani)",
        "location": "Barsana, Mathura district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "country": "India",
        "glyph": "रा",
        "famousFor": "Barsana — Radha’s village and Lathmar Holi",
        "summary": "Radha Rani of Barsana — the heart of Radha devotion in Braj.",
        "mythology": "Barsana is celebrated as Radha’s maternal home in Braj lore. The hill temple and Lathmar Holi make it essential on any Mathura–Vrindavan circuit.",
        "lat": 27.6480,
        "lng": 77.3770,
        "mapQuery": "Radha Rani Temple Barsana",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "officialWebsite": "https://uptourism.gov.in/",
        "festivals": ["Lathmar Holi", "Radhashtami"],
        "deityFamilies": ["krishna", "devi"],
    },
    {
        "slug": "nandgaon-nandbaba",
        "name": "Nand Baba Temple, Nandgaon",
        "deity": "Nanda Baba / Krishna childhood lore",
        "location": "Nandgaon, Mathura district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "country": "India",
        "glyph": "नं",
        "famousFor": "Nanda’s village opposite Barsana in Braj",
        "summary": "Nandgaon — paired with Barsana on the classic Braj parikrama.",
        "mythology": "Remembered as the village of Nanda, Krishna’s foster father. Pilgrims climb the hill for Nand Baba darshan and panoramic Braj views.",
        "lat": 27.7020,
        "lng": 77.3860,
        "mapQuery": "Nand Baba Temple Nandgaon",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "officialWebsite": "https://uptourism.gov.in/",
        "festivals": ["Nand Utsav", "Holi of Braj"],
        "deityFamilies": ["krishna"],
    },
    {
        "slug": "gokul-raman-reti",
        "name": "Gokul & Raman Reti (Braj)",
        "deity": "Lord Krishna (childhood Gokul lore)",
        "location": "Gokul / Raman Reti, Mathura district, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "country": "India",
        "glyph": "गो",
        "famousFor": "Krishna’s childhood landscape across the Yamuna from Mathura",
        "summary": "Gokul–Raman Reti — childhood Krishna geography of the Braj yatra.",
        "mythology": "Bhagavata tradition places Krishna’s early years in Gokul. Raman Reti and nearby shrines keep that childhood landscape alive for pilgrims after Mathura darshan.",
        "lat": 27.4390,
        "lng": 77.7200,
        "mapQuery": "Gokul Temple Mathura",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "officialWebsite": "https://uptourism.gov.in/",
        "deityFamilies": ["krishna"],
    },
    {
        "slug": "nathdwara-shrinathji",
        "name": "Shrinathji Temple, Nathdwara",
        "deity": "Shrinathji (Krishna as lifting Govardhan)",
        "location": "Nathdwara, Rajsamand, Rajasthan",
        "state": "Rajasthan",
        "country": "India",
        "glyph": "श्री",
        "famousFor": "Haveli of Shrinathji — major Pushtimarg Krishna seat",
        "summary": "Nathdwara’s Shrinathji — among India’s foremost Krishna pilgrimage towns.",
        "mythology": "Shrinathji is worshipped as Krishna lifting Govardhan. The image’s journey from Braj to Mewar and the haveli seva of the Pushtimarg define Nathdwara’s living theology.",
        "scriptureLinks": ["Bhagavata Purana", "Pushtimarg / Vallabha tradition"],
        "lat": 24.9380,
        "lng": 73.8220,
        "mapQuery": "Shrinathji Temple Nathdwara",
        "nearestRail": "Nathdwara / Udaipur",
        "nearestAirport": "Udaipur",
        "officialWebsite": "https://www.nathdwaratemple.org/",
        "festivals": ["Annkut", "Janmashtami", "Holi"],
        "deityFamilies": ["krishna", "vishnu"],
    },
    {
        "slug": "dakor-ranchhodrai",
        "name": "Ranchhodrai Temple, Dakor",
        "deity": "Lord Krishna (Ranchhodrai)",
        "location": "Dakor, Kheda district, Gujarat",
        "state": "Gujarat",
        "country": "India",
        "glyph": "रं",
        "famousFor": "Gujarat’s beloved Krishna temple after Dwarka",
        "summary": "Dakor Ranchhodrai — a major Gujarati Krishna pilgrimage often paired with Dwarka lore.",
        "mythology": "Ranchhodrai (‘one who left the battlefield’) is a form of Krishna. Local legend links the image’s arrival at Dakor with devoted Gujarati bhakti; full-moon days draw huge crowds.",
        "lat": 22.7520,
        "lng": 73.1500,
        "mapQuery": "Ranchhodrai Temple Dakor",
        "nearestRail": "Dakor / Nadiad",
        "nearestAirport": "Ahmedabad / Vadodara",
        "officialWebsite": "https://www.gujarattourism.com/",
        "festivals": ["Devpodhi Ekadashi / full-moon fairs", "Janmashtami"],
        "deityFamilies": ["krishna", "vishnu"],
    },
    {
        "slug": "srirangam-ranganathaswamy",
        "name": "Ranganathaswamy Temple, Srirangam",
        "deity": "Lord Ranganatha (Vishnu reclining on Ananta)",
        "location": "Srirangam, Tiruchirappalli, Tamil Nadu",
        "state": "Tamil Nadu",
        "country": "India",
        "glyph": "रं",
        "famousFor": "Among the largest living temple complexes; foremost South Indian Vishnu seat",
        "summary": "Srirangam Ranganatha — the island temple that anchors Tamil Vaishnava devotion.",
        "mythology": "Ranganatha reclines on Ananta in the Kaveri island kshetra praised across Alvar hymns and Sri Vaishnava tradition. Often paired with nearby Thiruvanaikaval on Trichy pilgrimages.",
        "scriptureLinks": ["Alvar / Divya Prabandham", "Sri Vaishnava Agamic tradition"],
        "lat": 10.8620,
        "lng": 78.6900,
        "mapQuery": "Srirangam Ranganathaswamy Temple",
        "nearestRail": "Srirangam / Tiruchirappalli",
        "nearestAirport": "Tiruchirappalli",
        "officialWebsite": "https://hrce.tn.gov.in/hrcehome/",
        "festivals": ["Vaikunta Ekadasi", "Brahmotsavam"],
        "dressCode": "Traditional dress preferred; follow temple notices.",
        "deityFamilies": ["vishnu"],
    },
    {
        "slug": "iskcon-mayapur",
        "name": "ISKCON Mayapur",
        "deity": "Radha–Madhava / Chaitanya traditions (ISKCON)",
        "location": "Mayapur, Nadia, West Bengal",
        "state": "West Bengal",
        "country": "India",
        "glyph": "म",
        "famousFor": "ISKCON world headquarters on the Ganga–Jalangi",
        "summary": "Mayapur — global ISKCON campus in the birth-region of Sri Chaitanya.",
        "mythology": "Mayapur is central to Gaudiya Vaishnava geography as the land of Chaitanya Mahaprabhu. The modern ISKCON temple town draws international Krishna devotees year-round.",
        "lat": 23.4240,
        "lng": 88.3910,
        "mapQuery": "ISKCON Mayapur",
        "nearestRail": "Krishnanagar / Navadwip region",
        "nearestAirport": "Kolkata",
        "officialWebsite": "https://www.mayapur.com/",
        "tags_extra": ["modern-temples"],
        "festivals": ["Gaura Purnima", "Janmashtami"],
        "deityFamilies": ["krishna", "vishnu"],
    },
    {
        "slug": "dwarkadhish-mathura",
        "name": "Dwarkadhish Temple, Mathura",
        "deity": "Lord Krishna (Dwarkadhish)",
        "location": "Mathura, Uttar Pradesh",
        "state": "Uttar Pradesh",
        "country": "India",
        "glyph": "द्वा",
        "famousFor": "Historic Krishna temple in Mathura city lanes",
        "summary": "Mathura’s Dwarkadhish temple — a classical city shrine on the Braj circuit.",
        "mythology": "Distinct from Gujarat’s Dwarka, this Mathura temple worships Krishna as Dwarkadhish and remains a busy lane-temple stop near the Janmabhoomi area.",
        "lat": 27.5055,
        "lng": 77.6735,
        "mapQuery": "Dwarkadhish Temple Mathura",
        "nearestRail": "Mathura Junction",
        "nearestAirport": "Agra / Delhi",
        "officialWebsite": "https://uptourism.gov.in/",
        "festivals": ["Janmashtami", "Holi"],
        "deityFamilies": ["krishna", "vishnu"],
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


def infer_families(d: dict) -> list[str]:
    slug = d["slug"]
    if slug in OVERRIDES:
        return list(OVERRIDES[slug])

    text = " ".join(
        [
            d.get("deity", ""),
            d.get("name", ""),
            d.get("famousFor", ""),
            " ".join(d.get("tags", [])),
        ]
    ).lower()

    families: list[str] = []

    def add(f: str) -> None:
        if f not in families:
            families.append(f)

    # Order matters for primary browsing feel
    if any(x in text for x in ["ayyappa", "sastha", "dharmasastha"]):
        add("ayyappa")
    if any(x in text for x in ["hanuman", "balaji temple", "sankat mochan", "salasar", "jakhoo", "mahavir mandir"]):
        # Salasar Balaji is Hanuman; Tirumala Balaji is Vishnu — handled by override
        if "venkateswara" not in text and "tirumala" not in text:
            add("hanuman")
    if any(x in text for x in ["rama", "ram mandir", "ramachandra", "sita ram", "rameswar"]):
        if "rameswar" in text or "rameshwar" in text:
            add("shiva")
        else:
            add("rama")
    if any(
        x in text
        for x in [
            "krishna",
            "radha",
            "vitthal",
            "vithoba",
            "jagannath",
            "banke bihari",
            "shrinath",
            "guruvayur",
            "govind",
            "shy am",
            "shyam",
            "dwarka",
            "iskcon",
            "ranchhod",
            "gokul",
            "braj",
            "vrindavan",
            "barbarika",
        ]
    ):
        add("krishna")
    if any(
        x in text
        for x in [
            "vishnu",
            "narayana",
            "narasimha",
            "lakshmi narasimha",
            "venkateswara",
            "balaji",
            "padmanabha",
            "ranganatha",
            "satyanarayana",
            "badri",
            "varaha",
            "swaminarayan",
            "tirumala",
        ]
    ):
        add("vishnu")
    if any(
        x in text
        for x in [
            "shiva",
            "shiv",
            "mahadev",
            "lingam",
            "jyotirlinga",
            "kedar",
            "bhairav",
            "nataraja",
            "sundareswar",
            "ekambareswar",
            "kalahasti",
            "somnath",
            "pashupati",
            "veerabhadra",
            "khandoba",
            "manguesh",
            "trimbak",
            "viswanath",
            "vishwanath",
            "mahakal",
            "omkareshwar",
            "grishneshwar",
            "bhimashankar",
            "nageshwar",
            "vaidyanath",
            "baidyanath",
            "mallikarjuna",
            "arunachala",
            "jambukeswar",
            "kapaleeshwar",
            "lingaraj",
            "raja rajeshwara",
            "murudeshwar",
        ]
    ) or "12-jyotirlinga" in d.get("tags", []) or "panch-kedar" in d.get("tags", []) or "pancha-bhuta" in d.get(
        "tags", []
    ):
        add("shiva")
    if any(
        x in text
        for x in [
            "devi",
            "goddess",
            "shakti",
            "durga",
            "kali",
            "lakshmi",
            "parvati",
            "meenakshi",
            "kamakhya",
            "vaishno",
            "ambaji",
            "mahalaxmi",
            "chamunda",
            "mookambika",
            "bhagavathy",
            "bhagavati",
            "katyayani",
            "tara ",
            "tripura",
            "naina",
            "jwala",
            "mansa",
            "hadimba",
            "danteshwari",
            "chhinnamasta",
            "shantadurga",
            "ganga",
            "yamuna",
            "peeth",
            "ambabai",
            "bhavani",
            "attukal",
            "kanaka durga",
        ]
    ) or "51-shakti-peeth" in d.get("tags", []):
        add("devi")
    if any(x in text for x in ["ganesha", "ganesh", "vinayaka", "ganapati", "ashtavinayak"]) or "ashtavinayak" in d.get(
        "tags", []
    ):
        add("ganesha")

    # Krishna pages are also browsable under Vishnu if only krishna matched from Vaishnava forms
    # Keep separate lists: do not auto-add vishnu for every krishna

    return families


def main() -> None:
    created = []
    for seed in NEW:
        slug = seed["slug"]
        path = TEMPLES / f"{slug}.json"
        tags_extra = seed.pop("tags_extra", [])
        deity_families = seed.pop("deityFamilies", None)
        if path.exists():
            detail = load_json(path)
            for k, v in seed.items():
                if k != "slug" and (k not in detail or not detail.get(k)):
                    detail[k] = v
        else:
            detail = base_detail(seed)
            created.append(slug)
        tags = list(detail.get("tags", []))
        for t in tags_extra:
            if t not in tags:
                tags.append(t)
        detail["tags"] = tags
        if deity_families is not None:
            detail["deityFamilies"] = deity_families
        detail = attach_portal(detail)
        dump_json(path, detail)

    # Assign / refresh deity families for all temples
    new_slugs = {s.get("slug") for s in NEW}
    # Re-read NEW deity families from files we just wrote
    counts: dict[str, int] = {k: 0 for k in DEITIES}
    unassigned = []
    for path in sorted(TEMPLES.glob("*.json")):
        d = load_json(path)
        slug = d["slug"]
        if slug in OVERRIDES:
            families = [f for f in OVERRIDES[slug] if f in DEITIES]
        elif slug in new_slugs and d.get("deityFamilies"):
            families = [f for f in d["deityFamilies"] if f in DEITIES]
        else:
            families = [f for f in infer_families(d) if f in DEITIES]
        d["deityFamilies"] = families
        if not families:
            unassigned.append(slug)
        for f in families:
            counts[f] = counts.get(f, 0) + 1
        dump_json(path, d)

    print(f"New temple files: {len(created)}")
    for s in created:
        print(" +", s)
    print("Deity family counts:")
    for k, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {n}")
    print(f"Unassigned (saint/multi/other): {len(unassigned)}")
    if unassigned[:20]:
        print(" ", ", ".join(unassigned[:20]))

    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "enrich_mythology.py")])


if __name__ == "__main__":
    main()
