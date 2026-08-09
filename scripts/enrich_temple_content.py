#!/usr/bin/env python3
"""
Enrich thin temple pages (esp. 2026-08-09 batch) toward fuller template parity:
  - longer mythology / significance / local beliefs (via enrich_mythology helpers)
  - sacredPhrase where a deity-fitting line is clear
  - nearby temples by distance
  - state-aware practical fields + deity-aware festivals
Does not invent shrine-specific timings; keeps verify-locally wording.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from enrich_mythology import (  # noqa: E402
    CURATED,
    DISCLAIMER_NOTE,
    _ensure_depth,
    expand_generic,
)

TEMPLES = ROOT / "data" / "temples"
GENERIC_BEST = "October–March for most plains sites; confirm Himalayan seasonal windows separately."
GENERIC_CLIMATE = "Varies by region — check seasonal weather before travel."
GENERIC_FOOD = "Simple vegetarian pilgrim meals and prasadam where offered."
GENERIC_FEST = {
    "Major local festival days",
    "Navaratri / Shiva-related observances as applicable",
}

STATE_PROFILE: dict[str, dict[str, str]] = {
    "Andhra Pradesh": {
        "bestTime": "October–March for cooler plains weather; summers are hot.",
        "climate": "Tropical / hot plains; coastal humidity near the Bay of Bengal.",
        "localLanguage": "Telugu and Hindi; English at hotels and larger towns.",
        "localFood": "Andhra vegetarian meals, temple prasadam, and sattvic thalis near pilgrim towns.",
    },
    "Arunachal Pradesh": {
        "bestTime": "October–April; check road and weather advisories for hills.",
        "climate": "Subtropical to alpine by elevation; heavy monsoon mid-year.",
        "localLanguage": "Local languages, Hindi, and some English in towns.",
        "localFood": "Simple vegetarian options in pilgrimage pockets; carry snacks for remote stretches.",
    },
    "Assam": {
        "bestTime": "October–April; Ambubachi and monsoon months need extra planning.",
        "climate": "Humid subtropical; heavy monsoon mid-year.",
        "localLanguage": "Assamese, Hindi, and English in cities.",
        "localFood": "Assamese vegetarian thalis and temple prasadam where offered.",
    },
    "Bihar": {
        "bestTime": "October–March; summers are hot and humid.",
        "climate": "Hot plains climate; monsoon June–September.",
        "localLanguage": "Hindi, Bhojpuri/Maithili locally; English limited outside cities.",
        "localFood": "Bihari vegetarian meals, litti-chokha style plates, and temple prasadam.",
    },
    "Chhattisgarh": {
        "bestTime": "October–March for comfortable pilgrimage weather.",
        "climate": "Central Indian plains — hot summers, monsoon mid-year.",
        "localLanguage": "Hindi and Chhattisgarhi; English limited outside cities.",
        "localFood": "Simple vegetarian thalis and prasadam near major shrines.",
    },
    "Delhi": {
        "bestTime": "October–March; avoid extreme summer heat where possible.",
        "climate": "Semi-arid extremes — hot summers, cool winters, monsoon showers.",
        "localLanguage": "Hindi and English widely; other Indian languages common.",
        "localFood": "North Indian vegetarian fare and prasadam at large temples.",
    },
    "Goa": {
        "bestTime": "November–February for pleasant weather; monsoon is lush but wet.",
        "climate": "Coastal tropical — humid, heavy monsoon June–September.",
        "localLanguage": "Konkani, Marathi, Hindi, and English in tourist areas.",
        "localFood": "Goan vegetarian / sattvic options near temples; wider cuisine in towns.",
    },
    "Gujarat": {
        "bestTime": "October–March for cooler coastal and plains weather.",
        "climate": "Hot and dry inland; humid on the coast; monsoon mid-year.",
        "localLanguage": "Gujarati and Hindi; English at hotels and tourist desks.",
        "localFood": "Gujarati vegetarian thali, farsan, and temple prasadam.",
    },
    "Haryana": {
        "bestTime": "October–March; summers are hot on the plains.",
        "climate": "Hot semi-arid plains; monsoon mid-year.",
        "localLanguage": "Hindi and Haryanvi; English in cities.",
        "localFood": "North Indian vegetarian meals and temple prasadam.",
    },
    "Himachal Pradesh": {
        "bestTime": "March–June and September–November; winter snow can close high roads.",
        "climate": "Hill climate — cool summers, cold winters, monsoon landslides possible.",
        "localLanguage": "Hindi and Pahari dialects; English in tourist towns.",
        "localFood": "Simple hill vegetarian meals, siddu/paratha styles, and prasadam.",
    },
    "Jammu and Kashmir": {
        "bestTime": "April–June and September–October for most circuits; check seasonal closures.",
        "climate": "Alpine to subtropical by belt; winter snow and summer showers vary sharply.",
        "localLanguage": "Kashmiri, Dogri, Hindi, Urdu; English in tourist zones.",
        "localFood": "Vegetarian pilgrim meals near shrines; carry layers and snacks for high routes.",
    },
    "Jharkhand": {
        "bestTime": "October–March; Bol Bam season has its own crowd calendar.",
        "climate": "Plateau climate — hot summers, monsoon mid-year.",
        "localLanguage": "Hindi and regional languages; English limited outside cities.",
        "localFood": "Simple vegetarian thalis and temple prasadam in shrine towns.",
    },
    "Karnataka": {
        "bestTime": "October–March for plains; Western Ghats can be wet in monsoon.",
        "climate": "Varies from coastal humidity to Deccan heat; monsoon heavy in Ghats.",
        "localLanguage": "Kannada and Hindi; English in cities and tourist hubs.",
        "localFood": "Karnataka vegetarian meals, temple meals (anna dana) where offered, and prasadam.",
    },
    "Kerala": {
        "bestTime": "October–March for most circuits; monsoon is green but wet.",
        "climate": "Tropical coastal — humid year-round; heavy southwest monsoon.",
        "localLanguage": "Malayalam and English widely; Hindi understood in tourist belts.",
        "localFood": "Kerala vegetarian sadhya-style meals and temple prasadam (payasam, etc.).",
    },
    "Madhya Pradesh": {
        "bestTime": "October–March for comfortable plains weather.",
        "climate": "Hot summers, pleasant winters, monsoon mid-year.",
        "localLanguage": "Hindi; English in larger towns.",
        "localFood": "Central Indian vegetarian thalis and temple prasadam.",
    },
    "Maharashtra": {
        "bestTime": "October–February for cooler weather; monsoon green but slippery on ghats.",
        "climate": "Coastal humidity west; hotter Deccan inland; monsoon June–September.",
        "localLanguage": "Marathi and Hindi; English in cities.",
        "localFood": "Maharashtrian vegetarian meals, wari-style simple food, and prasadam.",
    },
    "Manipur": {
        "bestTime": "October–April; check local advisories for hills.",
        "climate": "Humid subtropical hills; heavy monsoon.",
        "localLanguage": "Meitei / local languages, Hindi, some English in Imphal.",
        "localFood": "Simple vegetarian options near urban temples; confirm local customs.",
    },
    "Meghalaya": {
        "bestTime": "October–April; monsoon is very wet.",
        "climate": "Cool humid hills; among India’s wettest monsoon belts.",
        "localLanguage": "Khasi / local languages, English, and Hindi in towns.",
        "localFood": "Simple vegetarian meals in Shillong and pilgrimage pockets.",
    },
    "Odisha": {
        "bestTime": "October–March; Rath Yatra and coastal heat need separate planning.",
        "climate": "Tropical coastal / plains — humid, monsoon mid-year.",
        "localLanguage": "Odia and Hindi; English in cities and Puri belt.",
        "localFood": "Odia vegetarian meals, temple mahaprasad where available, and sattvic thalis.",
    },
    "Puducherry": {
        "bestTime": "November–February for cooler coastal weather.",
        "climate": "Coastal tropical — humid; northeast monsoon peaks late year.",
        "localLanguage": "Tamil, French heritage pockets, English and Hindi in tourist areas.",
        "localFood": "South Indian vegetarian meals and temple prasadam.",
    },
    "Punjab": {
        "bestTime": "October–March; summers are hot on the plains.",
        "climate": "Hot summers, cool winters, monsoon mid-year.",
        "localLanguage": "Punjabi and Hindi; English in cities.",
        "localFood": "Punjabi vegetarian thalis and simple pilgrim meals near shrines.",
    },
    "Rajasthan": {
        "bestTime": "October–March; avoid peak summer heat on desert circuits.",
        "climate": "Arid to semi-arid — hot days, cooler winter nights.",
        "localLanguage": "Hindi and Rajasthani dialects; English in tourist towns.",
        "localFood": "Rajasthani vegetarian thalis, dal-baati style plates, and temple prasadam.",
    },
    "Sikkim": {
        "bestTime": "March–June and September–November; winter cold at altitude.",
        "climate": "Himalayan — cool, wet monsoon, cold winters.",
        "localLanguage": "Nepali, local languages, Hindi, and English in Gangtok.",
        "localFood": "Simple vegetarian meals in town; carry snacks for hill stretches.",
    },
    "Tamil Nadu": {
        "bestTime": "November–February for cooler weather; summers are hot.",
        "climate": "Tropical / hot plains; coastal humidity; northeast monsoon late year.",
        "localLanguage": "Tamil; English in cities and major temple towns.",
        "localFood": "Tamil vegetarian meals, temple prasadam, and sattvic thalis.",
    },
    "Telangana": {
        "bestTime": "October–March for cooler Deccan weather.",
        "climate": "Hot Deccan plateau; monsoon mid-year.",
        "localLanguage": "Telugu and Hindi; English in Hyderabad and larger towns.",
        "localFood": "Telangana / Hyderabadi vegetarian options and temple prasadam.",
    },
    "Tripura": {
        "bestTime": "October–March for comfortable weather.",
        "climate": "Humid subtropical; heavy monsoon mid-year.",
        "localLanguage": "Bengali, Kokborok, Hindi; English in Agartala.",
        "localFood": "Bengali-style vegetarian meals and temple prasadam near major shrines.",
    },
    "Uttar Pradesh": {
        "bestTime": "October–March; summers are hot on the plains.",
        "climate": "Gangetic plains — hot summers, cool winters, monsoon mid-year.",
        "localLanguage": "Hindi; English in cities and major tirthas.",
        "localFood": "North Indian vegetarian thalis, kachori-sabzi styles, and temple prasadam.",
    },
    "Uttarakhand": {
        "bestTime": "May–June and September–October for high dhams; plains milder October–March.",
        "climate": "Himalayan — cool to cold by altitude; monsoon landslide risk on hill roads.",
        "localLanguage": "Hindi and Garhwali/Kumaoni; English in tourist towns.",
        "localFood": "Simple hill vegetarian meals and prasadam; carry dry snacks on treks.",
    },
    "West Bengal": {
        "bestTime": "October–March; Durga Puja season is crowded and festive.",
        "climate": "Humid subtropical; heavy monsoon mid-year.",
        "localLanguage": "Bengali and Hindi; English in Kolkata and tourist zones.",
        "localFood": "Bengali vegetarian meals, sweets, and temple prasadam.",
    },
    "Nepal": {
        "bestTime": "October–March for most circuits; high passes need separate windows.",
        "climate": "Varies from Kathmandu valley mildness to high Himalayan cold.",
        "localLanguage": "Nepali and local languages; Hindi/English in tourist belts.",
        "localFood": "Simple vegetarian thalis near shrines; follow local customs.",
    },
}

# Place-fitting phrases for notable new / thin temples (only where the line is real).
EXTRA_PHRASES: dict[str, dict[str, str]] = {
    "konark-sun-temple": {
        "text": "सूर्याय नमः",
        "meaning": "Salutation to Surya — the Sun",
        "source": "Classical Surya mantra fitting Konark’s solar shrine",
    },
    "chilkur-balaji": {
        "text": "गोविंदा गोविंदा",
        "meaning": "Govinda! Govinda! — the living cry of Venkateswara devotees",
        "source": "South Indian Balaji pilgrim call, widely heard at Chilkur",
    },
    "dharmasthala-manjunatha": {
        "text": "ॐ नमः शिवाय",
        "meaning": "I bow to Shiva — the auspicious one",
        "source": "Shaiva mantra at Manjunatha’s Dharmasthala seat",
    },
    "karni-mata-deshnok": {
        "text": "जय करणी माता",
        "meaning": "Victory to Karni Mata",
        "source": "Rajasthan’s living call at Deshnok",
    },
    "kalkaji-mandir-delhi": {
        "text": "जय काली माँ",
        "meaning": "Victory to Mother Kali",
        "source": "Delhi’s everyday cry at Kalkaji",
    },
    "kheer-bhawani": {
        "text": "जय माता दी",
        "meaning": "Victory to the Mother",
        "source": "Kashmiri Devi devotion at Tulmul",
    },
    "chottanikkara-temple": {
        "text": "ॐ देव्यै नमः",
        "meaning": "Om, salutation to the Goddess",
        "source": "Kerala Devi mantra fitting Chottanikkara’s healing reputation",
    },
    "mundeshwari-devi": {
        "text": "ॐ दुर्गायै नमः",
        "meaning": "Om, salutation to Goddess Durga",
        "source": "Shaiva–Shakta praise at Bihar’s ancient Mundeshwari hill",
    },
    "manakula-vinayagar": {
        "text": "ॐ गणेशाय नमः",
        "meaning": "Om, salutation to Lord Ganesha",
        "source": "Heart-mantra of Pondicherry’s Manakula Vinayagar",
    },
    "bambleshwari-dongargarh": {
        "text": "जय माँ बम्लेश्वरी",
        "meaning": "Victory to Mother Bambleshwari",
        "source": "Chhattisgarh pilgrim cry at Dongargarh",
    },
    "parshuram-kund": {
        "text": "परशुरामाय नमः",
        "meaning": "Salutation to Parashurama",
        "source": "Name-mantra of the Lohit kund tradition",
    },
    "kukke-subramanya": {
        "text": "ॐ सरवणभवाय नमः",
        "meaning": "Om, salutation to Sharavanabhava (Subramanya)",
        "source": "Skanda mantra of Kukke Subramanya devotion",
    },
    "eklingji-udaipur": {
        "text": "ॐ नमः शिवाय",
        "meaning": "I bow to Shiva — the auspicious one",
        "source": "Shaiva mantra of Mewar’s Eklingji",
    },
    "raghunath-temple-jammu": {
        "text": "जय श्री राम",
        "meaning": "Victory to Lord Rama",
        "source": "Living call at Jammu’s Raghunath complex",
    },
    "shankaracharya-temple": {
        "text": "ॐ नमः शिवाय",
        "meaning": "I bow to Shiva — the auspicious one",
        "source": "Shaiva mantra on Srinagar’s Shankaracharya hill",
    },
    "ambalapuzha-krishna": {
        "text": "कृष्णाय वासुदेवाय",
        "meaning": "Salutation to Krishna Vasudeva",
        "source": "Classical Krishna mantra; fitting Ambalapuzha’s child-Krishna seat",
    },
    "saptashrungi": {
        "text": "जय माँ सप्तश्रृंगी",
        "meaning": "Victory to Mother Saptashrungi",
        "source": "Maharashtra’s hill-Devi pilgrim cry",
    },
    "ugratara-mahishi": {
        "text": "ॐ तारायै नमः",
        "meaning": "Om, salutation to Goddess Tara",
        "source": "Name-mantra of Assam’s Ugratara tradition",
    },
    "jhandewalan-devi": {
        "text": "जय माता दी",
        "meaning": "Victory to the Mother",
        "source": "Delhi’s living Devi call at Jhandewalan",
    },
    "chhatarpur-temple-delhi": {
        "text": "ॐ दुर्गायै नमः",
        "meaning": "Om, salutation to Goddess Durga",
        "source": "Devi mantra fitting Chhatarpur’s vast complex",
    },
    "iskcon-east-of-kailash": {
        "text": "हरे कृष्ण",
        "meaning": "Hare Krishna — the great mantra of the age",
        "source": "ISKCON congregational chant",
    },
    "sitamarhi-janaki": {
        "text": "सीतायै नमः",
        "meaning": "Salutation to Sita",
        "source": "Janaki devotion of Sitamarhi’s birthplace tradition",
    },
    "mithila-janakpur": {
        "text": "जानक्यै नमः",
        "meaning": "Salutation to Janaki (Sita)",
        "source": "Mithila’s living Janaki praise at Janakpur",
    },
    "mudwan-hanuman-ludhiana": {
        "text": "जय हनुमान ज्ञान गुण सागर",
        "meaning": "Victory to Hanuman, ocean of wisdom and virtue",
        "source": "Opening of the Hanuman Chalisa",
    },
    "hatkoti-temple": {
        "text": "ॐ दुर्गायै नमः",
        "meaning": "Om, salutation to Goddess Durga",
        "source": "Himachal Devi mantra at Hatkoti",
    },
    "brajeshwari-kangra": {
        "text": "जय माँ बृजेश्वरी",
        "meaning": "Victory to Mother Brajeshwari",
        "source": "Kangra valley’s peetha pilgrim cry",
    },
    "surkanda-devi": {
        "text": "जय माता दी",
        "meaning": "Victory to the Mother",
        "source": "Garhwal Devi call on the Surkanda ridge",
    },
    "maha-mrityunjay-nagaon": {
        "text": "त्र्यम्बकं यजामहे",
        "meaning": "We worship the three-eyed One",
        "source": "Mahamrityunjaya mantra — fitting this Mrityunjay seat",
    },
    "thawe-mandir": {
        "text": "जय माँ थावे वाली",
        "meaning": "Victory to Mother Thawewali",
        "source": "Bihar–Nepal belt pilgrim cry at Thawe",
    },
    "chandrahasini-devi": {
        "text": "जय माँ चन्द्रहासिनी",
        "meaning": "Victory to Mother Chandrahasini",
        "source": "Chhattisgarh’s living call at this riverside peetha",
    },
    "malinithan-arunachal": {
        "text": "ॐ शिवाय नमः",
        "meaning": "Om, salutation to Shiva",
        "source": "Shaiva praise linked to Malinithan’s sculptural pilgrimage",
    },
    "lingaraj-bhubaneswar": {
        "text": "ॐ नमः शिवाय",
        "meaning": "I bow to Shiva — the auspicious one",
        "source": "Shaiva mantra of Bhubaneswar’s Lingaraj",
    },
    "mukteshwar-bhubaneswar": {
        "text": "ॐ नमः शिवाय",
        "meaning": "I bow to Shiva — the auspicious one",
        "source": "Shaiva mantra of Mukteshwar’s ornate shrine",
    },
    "biraja-jaipur": {
        "text": "ॐ बिराजायै नमः",
        "meaning": "Om, salutation to Goddess Biraja",
        "source": "Odisha’s peetha mantra at Jajpur",
    },
    "tara-tarini": {
        "text": "जय तारा तारिणी",
        "meaning": "Victory to Tara-Tarini",
        "source": "Odisha’s twin-goddess pilgrim cry",
    },
    "sakshi-ganesha-tirupati": {
        "text": "ॐ गणेशाय नमः",
        "meaning": "Om, salutation to Lord Ganesha",
        "source": "Heart-mantra of the witness-Ganesha on the Tirumala path",
    },
    "kanipakam-vinayaka": {
        "text": "ॐ गणेशाय नमः",
        "meaning": "Om, salutation to Lord Ganesha",
        "source": "Mantra of Kanipakam’s self-manifest Vinayaka",
    },
    "annavaram-satyanarayana": {
        "text": "ॐ नमो भगवते सत्यनारायणाय",
        "meaning": "Om, salutation to Satyanarayana",
        "source": "Name-mantra of Annavaram’s hill shrine",
    },
    "srikurmam": {
        "text": "कूर्माय नमः",
        "meaning": "Salutation to Kurma — the tortoise form of Vishnu",
        "source": "Rare Kurma avatar theology of Srikurmam",
    },
    "basar-saraswati": {
        "text": "ॐ सरस्वत्यै नमः",
        "meaning": "Om, salutation to Goddess Saraswati",
        "source": "Vidya mantra of Basar’s Gnana Saraswati",
    },
    "bhadrachalam-seetharamachandra": {
        "text": "जय श्री राम",
        "meaning": "Victory to Lord Rama",
        "source": "Godavari-side Rama devotion (if page uses this slug)",
    },
    "yadadri-lakshmi-narasimha": {
        "text": "नृसिंहाय नमः",
        "meaning": "Salutation to Narasimha",
        "source": "Telangana’s hill Narasimha call",
    },
    "knoll-knoll": {},  # placeholder removed below
}

# Remove empty placeholder
EXTRA_PHRASES.pop("knoll-knoll", None)

FAMILY_PHRASE: dict[str, dict[str, str]] = {
    "shiva": {
        "text": "ॐ नमः शिवाय",
        "meaning": "I bow to Shiva — the auspicious one",
        "source": "Universal Shaiva mantra of this shrine’s living devotion",
    },
    "devi": {
        "text": "जय माता दी",
        "meaning": "Victory to the Mother",
        "source": "Common North Indian Devi pilgrim greeting at this seat",
    },
    "vishnu": {
        "text": "ॐ नमो नारायणाय",
        "meaning": "Om, salutation to Narayana",
        "source": "Classical Vaishnava mantra fitting this Vishnu seat",
    },
    "krishna": {
        "text": "हरे कृष्ण",
        "meaning": "Hare Krishna",
        "source": "Living Krishna-nama of this shrine’s devotion",
    },
    "rama": {
        "text": "जय श्री राम",
        "meaning": "Victory to Lord Rama",
        "source": "Living Rama pilgrim cry at this seat",
    },
    "hanuman": {
        "text": "जय हनुमान ज्ञान गुण सागर",
        "meaning": "Victory to Hanuman, ocean of wisdom and virtue",
        "source": "Opening of the Hanuman Chalisa — widely sung here",
    },
    "ganesha": {
        "text": "ॐ गणेशाय नमः",
        "meaning": "Om, salutation to Lord Ganesha",
        "source": "Heart-mantra of Ganesha devotion at this shrine",
    },
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def haversine_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def festivals_for(d: dict) -> list[str]:
    existing = list(d.get("festivals") or [])
    if existing and not (set(existing) <= GENERIC_FEST):
        return existing
    families = set(d.get("deityFamilies") or [])
    name = (d.get("name") or "").lower()
    deity = (d.get("deity") or "").lower()
    out: list[str] = []
    if "shiva" in families or "shiva" in deity:
        out += ["Maha Shivaratri", "Mondays / Pradosham where observed"]
    if "devi" in families or any(x in deity for x in ("devi", "durga", "kali", "mata", "ambika", "bhagavati")):
        out += ["Navaratri", "Local jatra / mela days"]
    if "krishna" in families or "krishna" in deity:
        out += ["Janmashtami", "Ekadashi observances"]
    if "rama" in families or "rama" in deity or "sita" in deity or "janaki" in deity:
        out += ["Ram Navami", "Vivaha / local Rama festival days"]
    if "hanuman" in families or "hanuman" in deity:
        out += ["Hanuman Jayanti", "Tuesdays / Saturdays where observed"]
    if "ganesha" in families or "ganesha" in deity or "vinayaka" in deity:
        out += ["Ganesh Chaturthi", "Sankashti Chaturthi"]
    if "vishnu" in families or "narasimha" in deity or "venkateswara" in deity or "balaji" in name:
        out += ["Vaikuntha Ekadashi", "Brahmotsavam / local utsavam where held"]
    if "subramanya" in deity or "kartikeya" in deity or "murugan" in deity:
        out += ["Skanda Shashti", "Thai Poosam / local Subramanya festivals"]
    if "surya" in deity or "sun" in name or "konark" in name:
        out = ["Chandrabhaga Mela / Magha Saptami traditions", "Local solar festival days"]
    # dedupe preserve order
    seen = set()
    clean = []
    for f in out:
        if f not in seen:
            seen.add(f)
            clean.append(f)
    if not clean:
        clean = ["Major local festival days", "Annual temple utsavam / jatra"]
    if len(clean) < 2:
        clean.append("Daily aarti and special alankara days")
    return clean[:4]


def practical_fields(d: dict) -> None:
    state = d.get("state") or ""
    profile = STATE_PROFILE.get(state, {})
    if d.get("bestTime") in (None, "", GENERIC_BEST) and profile.get("bestTime"):
        d["bestTime"] = profile["bestTime"]
    if d.get("climate") in (None, "", GENERIC_CLIMATE) and profile.get("climate"):
        d["climate"] = profile["climate"]
    if d.get("localFood") in (None, "", GENERIC_FOOD) and profile.get("localFood"):
        d["localFood"] = profile["localFood"]
    if profile.get("localLanguage") and (
        not d.get("localLanguage")
        or d.get("localLanguage") == "Regional language and Hindi; English varies."
    ):
        d["localLanguage"] = profile["localLanguage"]

    name = d.get("name", "the temple")
    if not d.get("accommodation") or "Dharamshalas, trust guest houses" in (d.get("accommodation") or ""):
        d["accommodation"] = (
            f"Dharamshalas, temple-trust guest houses, and private hotels near {name}. "
            "Book early for festival weeks; prefer official trust counters when available."
        )
    if not d.get("whatToCarry") or d.get("whatToCarry") == "Modest clothes, ID proof, water, and offline maps.":
        hill = state in {
            "Himachal Pradesh",
            "Uttarakhand",
            "Jammu and Kashmir",
            "Sikkim",
            "Arunachal Pradesh",
            "Meghalaya",
            "Nepal",
        }
        extra = "Warm layers and rain protection for hills. " if hill else "Sun cap and light cotton for hot plains. "
        d["whatToCarry"] = extra + "Modest clothes, ID proof, water, and offline maps."
    if not d.get("dressCode") or "Modest clothing; follow temple boards" in (d.get("dressCode") or ""):
        d["dressCode"] = (
            "Modest attire — shoulders and knees covered preferred. "
            "Follow temple boards for traditional dress, footwear, and phone rules."
        )
    if not d.get("darshanTimings") or "Typically early morning to evening with ritual breaks" in (
        d.get("darshanTimings") or ""
    ):
        d["darshanTimings"] = (
            "Typically early morning to evening with aarti and ritual breaks. "
            "Confirm same-day timings on the temple trust / endowment board notices."
        )
    if not d.get("otherFood") or d.get("otherFood") == "Wider options usually in the nearest city.":
        d["otherFood"] = (
            "Wider vegetarian and city cuisine usually in the nearest town; "
            "keep non-veg and alcohol away from temple precincts as posted."
        )


def opening_mythology(d: dict) -> str:
    """Readable lead paragraph (not a one-line stub)."""
    name = d.get("name", "This temple")
    deity = d.get("deity", "the presiding deity")
    loc = d.get("location", "this tirtha")
    famous = (d.get("famousFor") or "").strip()
    summary = (d.get("summary") or "").strip()
    seed = (d.get("mythology") or "").strip()

    lead = seed if len(seed) >= 180 else (summary if len(summary) >= 120 else "")
    if len(lead) < 180:
        fame = f", known especially for {famous}" if famous else ""
        lead = (
            f"{name} at {loc} is dedicated to {deity}{fame}. "
            f"Pilgrimage tradition places the shrine within India’s tirtha network — "
            f"a seat where vows, gratitude, and family kuladevi / ishta devotion gather. "
            f"Local sthala-purana and priestly teaching elaborate how {deity} blesses "
            f"those who arrive with sincere intent; festival days intensify these beliefs "
            f"through special alankara and community worship where practised."
        )
    # Keep a single paragraph for the mythology teaser field
    return re.sub(r"\s+", " ", lead.split("\n\n")[0]).strip()


def enrich_mythology_fields(d: dict) -> None:
    slug = d["slug"]
    if slug in CURATED:
        c = CURATED[slug]
        d["mythologySignificance"] = c["mythologySignificance"]
        d["localBeliefs"] = c["localBeliefs"]
        if c.get("scriptureLinks"):
            links = list(c["scriptureLinks"])
            if not any(DISCLAIMER_NOTE in s for s in links):
                links.append(DISCLAIMER_NOTE)
            d["scriptureLinks"] = links
    else:
        myth = (d.get("mythology") or "").strip()
        sig = (d.get("mythologySignificance") or "").strip()
        if len(sig) < 360 or len(myth) < 180 or "Footfall and search popularity" in (
            d.get("localBeliefs") or ""
        ):
            sig, local, scriptures = expand_generic(d)
            d["mythologySignificance"] = sig
            d["localBeliefs"] = local
            d["scriptureLinks"] = scriptures
    _ensure_depth(d)

    # Rebuild a strong opening; keep fuller significance body after it
    opening = opening_mythology(d)
    body = d.get("mythologySignificance") or ""
    parts = [p for p in body.split("\n\n") if p.strip()]
    # Drop old thin first paragraph if we replaced it
    if parts and len(parts[0]) < 180:
        parts = parts[1:]
    # Avoid duplicating the same opening
    rest = [p for p in parts if p.strip() != opening]
    d["mythology"] = opening
    d["mythologySignificance"] = "\n\n".join([opening] + rest)
    d["mythologyDisclaimer"] = (
        "Mythological accounts and local beliefs are drawn from Puranic traditions, epics, "
        "and widely recorded sthala-purana / pilgrimage lore. Versions differ by scripture, "
        "region, and temple tradition. This section is for cultural understanding — not a "
        "claim of historical fact, nor a substitute for guidance from temple priests or "
        "official trusts."
    )


def assign_phrase(d: dict) -> bool:
    if d.get("sacredPhrase") and d["sacredPhrase"].get("text"):
        return False
    slug = d["slug"]
    if slug in EXTRA_PHRASES:
        d["sacredPhrase"] = EXTRA_PHRASES[slug]
        return True
    families = d.get("deityFamilies") or []
    for fam in ("hanuman", "ganesha", "rama", "krishna", "devi", "vishnu", "shiva"):
        if fam in families and fam in FAMILY_PHRASE:
            # Prefer more specific for South Devi
            if fam == "devi" and (d.get("state") or "") in {
                "Tamil Nadu",
                "Kerala",
                "Karnataka",
                "Andhra Pradesh",
                "Telangana",
                "Puducherry",
                "Odisha",
                "West Bengal",
                "Assam",
            }:
                d["sacredPhrase"] = {
                    "text": "ॐ देव्यै नमः",
                    "meaning": "Om, salutation to the Goddess",
                    "source": f"Devi mantra fitting devotion at {d.get('name', 'this shrine')}",
                }
            else:
                d["sacredPhrase"] = dict(FAMILY_PHRASE[fam])
            return True
    # deity string heuristics
    deity = (d.get("deity") or "").lower()
    for key, fam in (
        ("hanuman", "hanuman"),
        ("ganesha", "ganesha"),
        ("vinayaka", "ganesha"),
        ("rama", "rama"),
        ("sita", "rama"),
        ("krishna", "krishna"),
        ("kali", "devi"),
        ("durga", "devi"),
        ("devi", "devi"),
        ("mata", "devi"),
        ("vishnu", "vishnu"),
        ("narasimha", "vishnu"),
        ("balaji", "vishnu"),
        ("shiva", "shiva"),
    ):
        if key in deity:
            d["sacredPhrase"] = dict(FAMILY_PHRASE[fam])
            return True
    return False


def build_nearby(all_temples: list[dict], d: dict, limit: int = 3) -> list[dict]:
    if d.get("nearby"):
        return d["nearby"]
    lat, lng = d.get("lat"), d.get("lng")
    if lat is None or lng is None:
        return []
    candidates = []
    for other in all_temples:
        if other["slug"] == d["slug"]:
            continue
        olat, olng = other.get("lat"), other.get("lng")
        if olat is None or olng is None:
            continue
        # Prefer same state, allow nearby cross-border within 120km
        same = other.get("state") == d.get("state")
        dist = haversine_km((lat, lng), (olat, olng))
        if not same and dist > 120:
            continue
        if dist > 280:
            continue
        candidates.append((dist, same, other))
    candidates.sort(key=lambda x: (0 if x[1] else 1, x[0]))
    out = []
    for dist, _same, other in candidates[:limit]:
        note = f"About {int(dist)} km away" if dist >= 1 else "Nearby in the same sacred belt"
        out.append({"name": other["name"], "slug": other["slug"], "note": note})
    return out


def packages_for(d: dict) -> list[str]:
    pkgs = list(d.get("packages") or [])
    generic = {
        f"{d.get('name')} day darshan",
        "Regional multi-temple circuit",
    }
    if pkgs and not set(pkgs) <= generic:
        return pkgs
    name = d.get("name", "Temple")
    nearby = d.get("nearby") or []
    out = [f"{name} — day darshan"]
    if nearby:
        n0 = nearby[0]["name"]
        out.append(f"{name} + {n0} — 2-day circuit")
    if len(nearby) > 1:
        out.append(f"Regional {d.get('state', '')} multi-temple circuit".strip())
    else:
        out.append(f"{d.get('state', 'Regional')} pilgrimage weekend".strip())
    return out[:3]


def needs_enrich(d: dict) -> bool:
    if len(d.get("mythology") or "") < 180:
        return True
    if len(d.get("mythologySignificance") or "") < 360:
        return True
    if not d.get("sacredPhrase"):
        return True
    if not d.get("nearby"):
        return True
    if d.get("bestTime") == GENERIC_BEST or d.get("climate") == GENERIC_CLIMATE:
        return True
    fests = set(d.get("festivals") or [])
    if fests and fests <= GENERIC_FEST:
        return True
    if d.get("lastUpdated") == "2026-08-09" and len(d.get("mythology") or "") < 220:
        return True
    return False


def main() -> None:
    paths = sorted(TEMPLES.glob("*.json"))
    all_temples = [load(p) for p in paths]
    by_slug = {t["slug"]: t for t in all_temples}

    myth_n = phrase_n = nearby_n = pract_n = fest_n = 0
    touched = 0

    for path in paths:
        d = by_slug[path.stem]
        if not needs_enrich(d):
            continue
        touched += 1

        before_myth = len(d.get("mythology") or "")
        enrich_mythology_fields(d)
        if len(d.get("mythology") or "") > before_myth:
            myth_n += 1

        if assign_phrase(d):
            phrase_n += 1

        before_nearby = bool(d.get("nearby"))
        d["nearby"] = build_nearby(all_temples, d)
        if d["nearby"] and not before_nearby:
            nearby_n += 1

        before_best = d.get("bestTime")
        practical_fields(d)
        if d.get("bestTime") != before_best or d.get("climate") != GENERIC_CLIMATE:
            pract_n += 1

        before_fest = list(d.get("festivals") or [])
        d["festivals"] = festivals_for(d)
        if d["festivals"] != before_fest:
            fest_n += 1

        d["packages"] = packages_for(d)
        d["lastUpdated"] = "2026-08-09"
        dump(path, d)
        # refresh in-memory for later nearby builders
        by_slug[d["slug"]] = d
        for i, t in enumerate(all_temples):
            if t["slug"] == d["slug"]:
                all_temples[i] = d
                break

    print(
        f"Touched {touched} temples | mythology↑ {myth_n} | phrases +{phrase_n} | "
        f"nearby +{nearby_n} | practical {pract_n} | festivals {fest_n}"
    )


if __name__ == "__main__":
    main()
