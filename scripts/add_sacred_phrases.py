#!/usr/bin/env python3
"""
Add a sacred phrase / sloka / local saying to selected temples only —
where the line is meaningful to the deity, place, or living pilgrimage.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLES = ROOT / "data" / "temples"

# Only temples with a real, place-fitting line. Skip the rest.
# Fields: text (Devanagari/original), meaning (short English), optional source.
PHRASES: dict[str, dict[str, str]] = {
    "kedarnath": {
        "text": "ॐ नमः शिवाय",
        "meaning": "I bow to Shiva — the auspicious one",
        "source": "Universal Shaiva mantra; often on the lips of Kedarnath yatris",
    },
    "kashi-vishwanath": {
        "text": "काश्यां तु मरणान्मुक्तिः",
        "meaning": "In Kashi, even death becomes liberation",
        "source": "Classical Kashi mahatmya belief",
    },
    "somnath": {
        "text": "सोमनाथाय नमः",
        "meaning": "Salutation to Somnath — Lord of the Moon",
        "source": "From the Chandra–Soma penance tradition of this Jyotirlinga",
    },
    "mahakaleshwar-ujjain": {
        "text": "जय महाकाल",
        "meaning": "Victory to Mahakala — the Lord of Time",
        "source": "Living cry of Ujjain’s Shaiva devotees, especially at Bhasma Aarti",
    },
    "omkareshwar": {
        "text": "ॐ कार स्वरूपाय नमः",
        "meaning": "Salutation to the One whose form is Om",
        "source": "Echoes the Om-shaped Mandhata island of this Jyotirlinga",
    },
    "rameswaram": {
        "text": "श्री रामेश्वराय नमः",
        "meaning": "Salutation to Rameshwara — Shiva worshipped by Rama",
        "source": "Ramayana-linked consecration of the lingam on this shore",
    },
    "badrinath": {
        "text": "ॐ नमो भगवते वासुदेवाय",
        "meaning": "Om, salutation to the Blessed Vasudeva",
        "source": "Dwadasakshari mantra of Vaishnava Badri devotion",
    },
    "dwarka": {
        "text": "द्वारकाधीश की जय",
        "meaning": "Victory to the Lord of Dwarka",
        "source": "Living Gujarat pilgrim cry at Dwarkadhish",
    },
    "jagannath-puri": {
        "text": "जगन्नाथ स्वामी नयन-पथ-गामी भवतु मे",
        "meaning": "May Lord Jagannath stay upon the path of my eyes",
        "source": "Beloved Odia–Sanskrit prayer of Puri devotees",
    },
    "tirumala-venkateswara": {
        "text": "कलियुग वरदं वेंकटेशं",
        "meaning": "Venkatesha — the boon-giver of the Kali age",
        "source": "Classical Venkatachala mahatmya praise",
    },
    "kamakhya": {
        "text": "ॐ कामाख्यायै नमः",
        "meaning": "Om, salutation to Goddess Kamakhya",
        "source": "Mantra of Nilachal’s foremost Shakti Peetha",
    },
    "kalighat": {
        "text": "जय काली माँ",
        "meaning": "Victory to Mother Kali",
        "source": "Bengal’s living call at Kalighat",
    },
    "vaishno-devi": {
        "text": "जय माता दी",
        "meaning": "Victory to the Mother",
        "source": "North Indian pilgrim greeting of the Trikuta yatra",
    },
    "sabarimala": {
        "text": "स्वामिये शरणं अय्यप्पा",
        "meaning": "O Lord Ayyappa, you are my refuge",
        "source": "The defining chant of the Sabarimala vrata",
    },
    "guruvayur": {
        "text": "नारायणाय नमः",
        "meaning": "Salutation to Narayana",
        "source": "Heart-mantra of Guruvayurappan devotion in Kerala",
    },
    "pandharpur-vitthal": {
        "text": "विठ्ठल विठ्ठल",
        "meaning": "Vitthal! Vitthal! — the name that carries the wari",
        "source": "Warkari abhanga cry on the road to Pandharpur",
    },
    "khatushyam": {
        "text": "श्याम बाबा की जय",
        "meaning": "Victory to Shyam Baba",
        "source": "Rajasthan’s living call at Khatu",
    },
    "salasar-balaji": {
        "text": "जय हनुमान ज्ञान गुण सागर",
        "meaning": "Victory to Hanuman, ocean of wisdom and virtue",
        "source": "Opening of the Hanuman Chalisa — sung widely at Salasar",
    },
    "gangotri": {
        "text": "नमो गङ्गे",
        "meaning": "Salutation to Mother Ganga",
        "source": "River-goddess praise at her Himalayan shrine",
    },
    "yamunotri": {
        "text": "यमुनायै नमः",
        "meaning": "Salutation to Goddess Yamuna",
        "source": "Devi mantra of the Yamunotri dham",
    },
    "mount-kailash": {
        "text": "कैलासवासिने नमः",
        "meaning": "Salutation to the One who dwells on Kailasa",
        "source": "Shaiva praise of Shiva’s cosmic abode",
    },
    "pashupatinath": {
        "text": "ॐ पशुपतये नमः",
        "meaning": "Om, salutation to Pashupati — Lord of all beings",
        "source": "Classical name-mantra of Kathmandu’s great Shaiva seat",
    },
    "muktinath": {
        "text": "मुक्तिनाथाय नमः",
        "meaning": "Salutation to the Lord of Liberation",
        "source": "Name-theology of the Mustang mukti tirtha",
    },
    "kurukshetra-brahmasarovar": {
        "text": "धर्मक्षेत्रे कुरुक्षेत्रे",
        "meaning": "On the field of dharma, at Kurukshetra…",
        "source": "Opening words of the Bhagavad Gita (1.1)",
    },
    "chitrakoot-ramghat": {
        "text": "चित्रकूट के घाट घाट…",
        "meaning": "On every ghat of Chitrakoot…",
        "source": "Echo of Ramcharitmanas devotion to Rama’s forest home",
    },
    "arunachaleswarar-tiruvannamalai": {
        "text": "अरुणाचल शिवाय नमः",
        "meaning": "Salutation to Shiva of Arunachala — the hill of fire",
        "source": "Tamil Shaiva praise of the Agni Sthalam",
    },
    "nataraja-chidambaram": {
        "text": "नटराजाय नमः",
        "meaning": "Salutation to Nataraja — Lord of the cosmic dance",
        "source": "Heart of Chidambaram’s akasha (space) theology",
    },
    "thiruvanaikaval": {
        "text": "जम्बुकेश्वराय नमः",
        "meaning": "Salutation to Jambukeswara — Shiva of the water lingam",
        "source": "Name-mantra of the Appu (water) Pancha Bhuta Sthalam",
    },
    "ekambareswarar-kanchipuram": {
        "text": "एकाम्बरेशाय नमः",
        "meaning": "Salutation to Ekambareswara — Lord of the one mango tree",
        "source": "Sthala name of Kanchi’s earth-element Shiva",
    },
    "srikalahasti": {
        "text": "श्रीकालहस्तीश्वराय नमः",
        "meaning": "Salutation to Srikalahastiswara — Lord of spider, snake, and elephant",
        "source": "From the famous devotee-creatures legend of the Vayu Sthalam",
    },
    "mallikarjuna-srisailam": {
        "text": "श्रीशैलवासिन्यै नमः",
        "meaning": "Salutation to the Goddess who dwells on Srisailam",
        "source": "Paired with Mallikarjuna — Shiva–Shakti on one hill",
    },
    "vaidyanath-deoghar": {
        "text": "बैद्यनाथाय नमः",
        "meaning": "Salutation to Vaidyanath — the Lord who heals",
        "source": "Name-theology behind Deoghar’s Bol Bam vows",
    },
    "trimbakeshwar": {
        "text": "त्र्यम्बकं यजामहे",
        "meaning": "We worship the three-eyed One",
        "source": "Opening of the Mahamrityunjaya mantra — linked to Trimbak’s three-faced lingam",
    },
    "simhachalam": {
        "text": "नृसिंहाय नमः",
        "meaning": "Salutation to Narasimha — the man-lion Lord",
        "source": "Mantra of Simhachalam’s Varaha-Lakshmi-Narasimha form",
    },
    "kanaka-durga-vijayawada": {
        "text": "दुर्गां देवीं शरणमहं प्रपद्ये",
        "meaning": "I take refuge in Goddess Durga",
        "source": "Devi Mahatmya refuge-verse; fitting Indrakeeladri’s Kanaka Durga",
    },
    "chamundeshwari-mysuru": {
        "text": "जय चामुण्डेश्वरी",
        "meaning": "Victory to Chamundeshwari",
        "source": "Mysuru’s Dasara cry to the hill goddess",
    },
    "mookambika-kollur": {
        "text": "ॐ श्री मूकाम्बिकायै नमः",
        "meaning": "Om, salutation to Goddess Mookambika",
        "source": "Mantra of Kollur — sought for speech, learning, and arts",
    },
    "amarnath-shakti": {
        "text": "अमरनाथाय नमः",
        "meaning": "Salutation to Amarnath — the Immortal Lord",
        "source": "Name of the ice-lingam kshetra and its amar katha",
    },
    "bhadrachalam": {
        "text": "श्री रामाय नमः",
        "meaning": "Salutation to Lord Rama",
        "source": "Godavari-side Rama devotion of Bhadrachalam",
    },
    "tungnath": {
        "text": "केदाराय नमः",
        "meaning": "Salutation to Kedara — Shiva of the high meadows",
        "source": "Shared Shaiva call of the Panch Kedar circuit",
    },
    "moreshwar-morgaon": {
        "text": "ॐ गणेशाय नमः",
        "meaning": "Om, salutation to Lord Ganesha",
        "source": "Heart-mantra of the Ashtavinayak yatra",
    },
    "ayodhya-ram-mandir": {
        "text": "जय श्री राम",
        "meaning": "Victory to Lord Rama",
        "source": "Living pilgrim cry of Ayodhya",
    },
    "meenakshi-madurai": {
        "text": "मीनाक्ष्यै नमः",
        "meaning": "Salutation to Goddess Meenakshi",
        "source": "Name-mantra of Madurai’s divine queen",
    },
    "akshardham-delhi": {
        "text": "जय स्वामिनारायण",
        "meaning": "Victory to Swaminarayan",
        "source": "Living call of BAPS Akshardham devotion",
    },
    "iskcon-delhi": {
        "text": "हरे कृष्ण",
        "meaning": "Hare Krishna — the great mantra of the age",
        "source": "ISKCON congregational chant",
    },
    "siddhivinayak-mumbai": {
        "text": "श्री सिद्धिविनायकाय नमः",
        "meaning": "Salutation to Siddhivinayak",
        "source": "Mumbai’s Tuesday vow mantra",
    },
    "shirdi-sai": {
        "text": "सबका मालिक एक",
        "meaning": "The Lord of all is One",
        "source": "Shirdi Sai Baba’s teaching",
    },
    "padmanabhaswamy-thiruvananthapuram": {
        "text": "ॐ नमो नारायणाय",
        "meaning": "Om, salutation to Narayana",
        "source": "Vaishnava mantra at Padmanabha’s seat",
    },
}


def main() -> None:
    added = 0
    cleared = 0
    for path in sorted(TEMPLES.glob("*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        slug = d["slug"]
        if slug in PHRASES:
            d["sacredPhrase"] = PHRASES[slug]
            added += 1
        elif "sacredPhrase" in d:
            del d["sacredPhrase"]
            cleared += 1
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Sacred phrases on {added} temples (cleared {cleared} extras).")


if __name__ == "__main__":
    main()
