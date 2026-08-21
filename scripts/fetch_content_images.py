#!/usr/bin/env python3
"""
Download AdSense-safe Wikimedia Commons images for festivals & stories.

Licenses: Public domain, CC0, CC BY, CC BY-SA (same rules as temple fetch).
Prefer classic mythological paintings (Raja Ravi Varma / PD manuscripts)
and clear festival photographs.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import fetch_images as fi  # type: ignore

OUT_F = ROOT / "assets" / "festivals"
OUT_S = ROOT / "assets" / "stories"
OUT_D = ROOT / "assets" / "deities-art"
MEDIA_PATH = ROOT / "data" / "content-media.json"

# Verified / high-signal Commons filenames (prefer these before search)
FESTIVAL_FILES: dict[str, list[str]] = {
    "diwali": [
        "Diwali lamps in India 04.jpg",
        "Woman lighting the candles for the Festival of Lights in India (cropped).jpg",
        "Raja Ravi Varma, Goddess Lakshmi, 1896.jpg",
    ],
    "holi": [
        "Life in colour - Holi at Mathura.jpg",
        "Holi festival, Vrindavan, Mathura, Uttar Pradesh, India (2018).jpg",
        "Lathmar Holi 2022 in Nandgaon, Uttar Pradesh (edited).jpg",
    ],
    "janmashtami": [
        "Vasudeva carrying baby Krishna across the Yamuna.jpg",
        "Birth of Krishna.jpg",
        "Baby Krishna.jpg",
    ],
    "ganesh-chaturthi": [
        "Rebirth of Ganesha.jpg",
        "Ganesha Basohli miniature circa 1730.jpg",
    ],
    "navaratri": [
        "Durga by Raja Ravi Varma.jpg",
        "Goddess Durga by Raja Ravi Varma.jpg",
    ],
    "dussehra": [
        "Rama slays Ravana.jpg",
        "Ravana.jpg",
    ],
    "maha-shivaratri": [
        "Siva-parvati-by-raja-ravi-varma.jpg",
        "Shiva meditating.jpg",
    ],
    "ram-navami": [
        "Rama with Sita and Lakshmana.jpg",
        "Ram Darbar.jpg",
    ],
    "hanuman-jayanti": [
        "Hanuman Herb Mountain.jpg",
        "Chitrakathi Painting, Hanuman carrying Dronagiri, Maharashtra.jpg",
    ],
    "govardhan-puja": [
        "Krishna Holds Up Mount Govardhan to Shelter the Villagers of Braj, ca.1590–95, The Met.jpg",
        "Krishna Holding Mount Govardhan - Crop.jpg",
    ],
    "vasant-panchami": [
        "Saraswati.jpg",
        "Goddess Saraswati.jpg",
    ],
    "akshaya-tritiya": [
        "Raja Ravi Varma, Goddess Lakshmi, 1896.jpg",
        "Lakshmi, by Raja Ravi Varma, 1930s.jpg",
    ],
    "dhanteras": [
        "Raja Ravi Varma, Goddess Lakshmi, 1896.jpg",
    ],
    "rath-yatra": [
        "Rath Yatra Puri.jpg",
        "Jagannath Rath Yatra.jpg",
    ],
    "onam": [
        "Onam Pookalam.jpg",
        "Onam.jpg",
    ],
    "chhath-puja": [
        "Chhath Puja.jpg",
        "Chhath.jpg",
    ],
    "makar-sankranti": [
        "Makar Sankranti.jpg",
        "Kite flying.jpg",
    ],
    "shravan-sawan": [
        "Siva-parvati-by-raja-ravi-varma.jpg",
        "Shiva lingam.jpg",
    ],
    "nag-panchami": [
        "Naga.jpg",
        "Shiva with snake.jpg",
    ],
    "chaitra-navaratri": [
        "Durga by Raja Ravi Varma.jpg",
    ],
    "guru-purnima": [
        "Vyasa.jpg",
        "Veda Vyasa.jpg",
    ],
    "vat-savitri": [
        "Savitri and Satyavan.jpg",
        "Savitri.jpg",
    ],
}

FESTIVAL_SEARCH: dict[str, str] = {
    "diwali": "Diwali lamps India festival",
    "holi": "Holi Mathura Vrindavan festival colours",
    "janmashtami": "Krishna birth Janmashtami Vasudeva",
    "ganesh-chaturthi": "Ganesha painting mythology",
    "navaratri": "Durga Mahishasura Raja Ravi Varma",
    "dussehra": "Rama Ravana battle Ramayana painting",
    "maha-shivaratri": "Shiva Parvati Raja Ravi Varma",
    "raksha-bandhan": "Raksha Bandhan rakhi India",
    "ram-navami": "Rama Sita Lakshmana Hanuman painting",
    "hanuman-jayanti": "Hanuman mythology painting",
    "makar-sankranti": "Makar Sankranti kite India",
    "lohri": "Lohri bonfire Punjab",
    "pongal": "Pongal festival Tamil Nadu",
    "govardhan-puja": "Krishna Govardhan mountain painting",
    "chhath-puja": "Chhath Puja Bihar Surya",
    "karva-chauth": "Karva Chauth puja",
    "shravan-sawan": "Shiva lingam abhishek",
    "onam": "Onam pookalam Kerala",
    "rath-yatra": "Rath Yatra Puri Jagannath",
    "vasant-panchami": "Saraswati goddess painting",
    "akshaya-tritiya": "Lakshmi Raja Ravi Varma",
    "guru-purnima": "Vyasa sage painting",
    "dhanteras": "Lakshmi Diwali gold",
    "bhai-dooj": "Bhai Dooj Yamuna Yama",
    "gudi-padwa": "Gudi Padwa Maharashtra",
    "ugadi": "Ugadi festival",
    "nag-panchami": "Naga Panchami snake worship",
    "tulsi-vivah": "Tulsi Vivah",
    "chaitra-navaratri": "Durga goddess painting",
    "vaisakhi": "Vaisakhi Baisakhi",
    "kartik-purnima": "Kartik Purnima Dev Deepavali",
    "sharad-purnima": "Sharad Purnima full moon",
    "hartalika-teej": "Teej festival women",
    "vat-savitri": "Savitri Satyavan painting",
    "kanwar-yatra": "Kanwar Yatra Ganga",
    "santoshi-mata": "Santoshi Mata",
    "skanda-shashti": "Murugan Kartikeya",
    "thaipusam": "Thaipusam Murugan",
    "gangaur": "Gangaur Rajasthan",
    "sheetala-ashtami": "Sheetala Mata",
    "parashurama-jayanti": "Parashurama avatar",
}

STORY_FILES: dict[str, list[str]] = {
    "neelkanth-poison": [
        "Siva-parvati-by-raja-ravi-varma.jpg",
        "Neelkantheshwar mahadev.jpg",
    ],
    "prahlad-holika": [
        "Narasimha killed Hiranyakashipu.jpg",
        "Narasimha oil colour.jpg",
    ],
    "krishna-birth-night": [
        "Vasudeva carrying baby Krishna across the Yamuna.jpg",
        "Birth of Krishna.jpg",
    ],
    "durga-mahishasura": [
        "Durga by Raja Ravi Varma.jpg",
        "Goddess Durga by Raja Ravi Varma.jpg",
    ],
    "rama-homecoming-lamps": [
        "Rama returning to Ayodhya.jpg",
        "Ram Darbar.jpg",
    ],
    "ganesha-door-guardian": ["Rebirth of Ganesha.jpg"],
    "ganesha-elephant-head": ["Rebirth of Ganesha.jpg"],
    "krishna-govardhan": [
        "Krishna Holds Up Mount Govardhan to Shelter the Villagers of Braj, ca.1590–95, The Met.jpg",
        "Krishna Holding Mount Govardhan - Crop.jpg",
    ],
    "krishna-kaliya": ["Krishna Kaliya.jpg", "Kaliya mardan.jpg"],
    "bhagavad-gita-kurukshetra": [
        "Krishna and Arjuna on the chariot, Mahabharata, India.jpg",
        "Bhagavad Gita.jpg",
    ],
    "ganga-avatarana": ["Descent of Ganga.jpg", "Bhagiratha.jpg"],
    "vamana-bali": ["Vamana.jpg", "Vamana avatar.jpg"],
    "sudama-krishna": ["Sudama and Krishna.jpg"],
    "savitri-satyavan": ["Savitri and Satyavan.jpg"],
    "markandeya-shiva": ["Markandeya.jpg"],
    "hanuman-sanjeevani": [
        "Hanuman Herb Mountain.jpg",
        "Chitrakathi Painting, Hanuman carrying Dronagiri, Maharashtra.jpg",
    ],
    "narasimha-hiranyakashipu": [
        "Narasimha killed Hiranyakashipu.jpg",
        "Narasimha oil colour.jpg",
    ],
    "samudra-manthan-kurma": [
        "Sagar Manthan.jpg",
        "Samudra-Manthan-The-Churning-of-the-Ocean-of-Milk.jpg",
    ],
    "matsya-manu": ["Matsya.jpg", "Matsya avatar.jpg"],
    "varaha-earth": ["Varaha.jpg", "Varaha avatar.jpg"],
    "ravana-vadh-dharma": ["Rama slays Ravana.jpg"],
    "hanuman-lanka-agni": ["Hanuman burns Lanka.jpg", "Hanuman Herb Mountain.jpg"],
    "krishna-virat-roop": ["Vishvarupa.jpg", "Krishna Vishvarupa.jpg"],
    "lakshman-rekha": ["Lakshmana rekha.jpg", "Sita Ravana.jpg"],
    "shabari-rama": ["Shabari.jpg", "Rama and Shabari.jpg"],
    "ahalya-rama": ["Ahalya.jpg"],
    "draupadi-vastraharan-dharma": ["Draupadi.jpg"],
    "karna-danveer": ["Karna.jpg"],
    "bhishma-pratigya": ["Bhishma.jpg"],
    "abhimanyu-chakravyuh": ["Abhimanyu.jpg"],
    "eklavya-drona-thumb": ["Ekalavya.jpg"],
    # Devi-Devata birth / origin series
    "shiva-lingodbhava-origin": [
        "Siva-parvati-by-raja-ravi-varma.jpg",
        "Shiva.jpg",
        "Lingodbhava.jpg",
    ],
    "vishnu-ananta-shesha-origin": [
        "Vishnu.jpg",
        "Vishnu on Garuda.jpg",
        "Anantashayana Vishnu.jpg",
    ],
    "durga-born-from-tejas": [
        "Durga by Raja Ravi Varma.jpg",
        "Goddess Durga by Raja Ravi Varma.jpg",
    ],
    "ganesha-born-of-parvati": ["Rebirth of Ganesha.jpg", "Ganesha Basohli miniature circa 1730.jpg"],
    "rama-birth-ayodhya": [
        "Rama with Sita and Lakshmana.jpg",
        "Ram Darbar.jpg",
        "Birth of Rama.jpg",
    ],
    "hanuman-birth-anjana": [
        "Hanuman Herb Mountain.jpg",
        "Chitrakathi Painting, Hanuman carrying Dronagiri, Maharashtra.jpg",
    ],
    "murugan-skanda-birth": ["Murugan.jpg", "Kartikeya.jpg", "Kartikeya by Raja Ravi Varma.jpg"],
    "surya-aditya-origin": ["Surya.jpg", "Sun god Surya.jpg"],
    "shani-birth-chhaya": ["Shani.jpg", "Shani Dev.jpg"],
    "dattatreya-birth-anusuya": ["Dattatreya.jpg", "Lord Dattatreya.jpg"],
    "narasimha-pillar-appearance": [
        "Narasimha killed Hiranyakashipu.jpg",
        "Narasimha oil colour.jpg",
    ],
    "vitthal-vithoba-origin": ["Vithoba.jpg", "Vitthal.jpg", "Pandharpur.jpg"],
    "bhairav-kalabhairav-origin": ["Bhairava.jpg", "Kalabhairava.jpg", "Shiva.jpg"],
    "lakshmi-ocean-birth": [
        "Raja Ravi Varma, Goddess Lakshmi, 1896.jpg",
        "Lakshmi, by Raja Ravi Varma, 1930s.jpg",
        "Sagar Manthan.jpg",
    ],
    "saraswati-vak-origin": ["Saraswati.jpg", "Goddess Saraswati.jpg"],
    "kali-born-of-wrath": ["Kali.jpg", "Goddess Kali.jpg", "Kali by Raja Ravi Varma.jpg"],
    "jagannath-neelamadhav-origin": ["Jagannath.jpg", "Jagannath Balabhadra Subhadra.jpg"],
    "venkateswara-srinivasa-descent": ["Venkateswara.jpg", "Tirupati Balaji.jpg"],
    "annapurna-origin-kashi": ["Annapurna.jpg", "Goddess Annapurna.jpg"],
    "santoshi-mata-origin": ["Santoshi Mata.jpg", "Santoshi maa.jpg"],
    "brahma-lotus-birth": ["Brahma riding on his goose.jpg", "Brahma Pushkar.jpg", "Saraswati.jpg"],
    "mangal-graha-origin": ["Angaraka.jpg", "Mangala Graha.jpg"],
    # Family-relation series
    "shiva-parvati-divine-wedding": ["Siva-parvati-by-raja-ravi-varma.jpg", "Shiva Parvati.jpg"],
    "shiva-sons-ganesha-kartikeya": ["Rebirth of Ganesha.jpg", "Kartikeya.jpg"],
    "vishnu-lakshmi-eternal-pair": ["Vishnu.jpg", "Raja Ravi Varma, Goddess Lakshmi, 1896.jpg"],
    "lakshmi-as-vishnu-consort": ["Raja Ravi Varma, Goddess Lakshmi, 1896.jpg"],
    "krishna-yashoda-mother": ["Vasudeva carrying baby Krishna across the Yamuna.jpg", "Baby Krishna.jpg", "Krishna Holds Up Mount Govardhan to Shelter the Villagers of Braj, ca.1590–95, The Met.jpg"],
    "krishna-balarama-brother": ["Balarama.jpg", "Krishna Balarama.jpg"],
    "krishna-rukmini-wedding": ["Rukmini.jpg", "Krishna Rukmini.jpg", "Raja Ravi Varma Krishna.jpg"],
    "ganesha-siddhi-buddhi": ["Rebirth of Ganesha.jpg", "Ganesha Basohli miniature circa 1730.jpg"],
    "ganesha-shubh-labh-children": ["Rebirth of Ganesha.jpg"],
    "rama-lakshmana-brotherhood": ["Rama with Sita and Lakshmana.jpg", "Ram Darbar.jpg"],
    "rama-bharata-paduka": ["Bharata.jpg", "Rama Bharata.jpg", "Ram Darbar.jpg"],
    "sita-as-rama-consort": ["Rama with Sita and Lakshmana.jpg", "Ram Darbar.jpg"],
    "hanuman-kesari-anjana-parents": ["Hanuman Herb Mountain.jpg"],
    "murugan-valli-devasena": ["Murugan.jpg", "Kartikeya.jpg"],
    "murugan-ganesha-brothers": ["Kartikeya.jpg", "Rebirth of Ganesha.jpg"],
    "surya-sanjna-chhaya": ["Surya.jpg", "Sun god Surya.jpg"],
    "shani-and-surya-father": ["Shani Dev.jpg", "Surya.jpg"],
    "parvati-as-mother-of-ganesha": ["Siva-parvati-by-raja-ravi-varma.jpg", "Rebirth of Ganesha.jpg"],
    "kali-shiva-cremation-ground": ["Goddess Kali.jpg", "Siva-parvati-by-raja-ravi-varma.jpg"],
    "annapurna-shiva-household": ["Annapurna.jpg", "Siva-parvati-by-raja-ravi-varma.jpg"],
    "santoshi-ganesha-daughter": ["Worshiping goddess santoshi 02.jpg", "Rebirth of Ganesha.jpg"],
    "jagannath-balabhadra-subhadra": ["Jagannath.jpg", "Jagannath Balabhadra Subhadra.jpg"],
    "vitthal-rukmini-pandharpur": ["Pandharpur.jpg", "Vithoba.jpg"],
    "venkateswara-padmavati-consort": ["Venkateswara.jpg", "Tirupati Balaji.jpg"],
    "narasimha-lakshmi-prahlada": ["Narasimha killed Hiranyakashipu.jpg", "Narasimha oil colour.jpg"],
    "brahma-saraswati-knowledge": ["Brahma riding on his goose.jpg", "Saraswati.jpg", "Goddess Saraswati.jpg"],
    "saraswati-and-learning-family": ["Saraswati.jpg", "Goddess Saraswati.jpg"],
    "dattatreya-atri-anusuya-parents": ["Dattatreya.jpg"],
    "bhairav-bhairavi-consort": ["Bhairava.jpg", "Kalabhairava.jpg"],
    "ayyappa-foster-father-raja": ["Lord Ayyappa old painting.jpg", "Ayyappan.jpg"],
    "mangal-bhumi-family": ["Bhudevi.jpg", "Bhumi Devi.jpg", "Angaraka.jpg"],
}

STORY_SEARCH: dict[str, str] = {
    "neelkanth-poison": "Shiva Neelkantha poison mythology painting",
    "prahlad-holika": "Narasimha Hiranyakashipu Prahlada painting",
    "krishna-birth-night": "Vasudeva Krishna Yamuna birth painting",
    "durga-mahishasura": "Durga Mahishasura Raja Ravi Varma",
    "rama-homecoming-lamps": "Rama Ayodhya return Diwali painting",
    "ganesha-door-guardian": "Ganesha painting mythology",
    "ganesha-elephant-head": "Ganesha birth Parvati painting",
    "krishna-govardhan": "Krishna Govardhan mountain painting",
    "krishna-kaliya": "Krishna Kaliya serpent painting",
    "bhagavad-gita-kurukshetra": "Krishna Arjuna chariot Bhagavad Gita",
    "ganga-avatarana": "Descent of Ganga Bhagiratha painting",
    "vamana-bali": "Vamana avatar Bali painting",
    "sudama-krishna": "Sudama Krishna friendship painting",
    "savitri-satyavan": "Savitri Satyavan painting",
    "markandeya-shiva": "Markandeya Shiva painting",
    "hanuman-sanjeevani": "Hanuman carrying mountain herbs",
    "ram-setu-nal-neel": "Rama Setu bridge Lanka painting",
    "vali-sugriva-kishkindha": "Vali Sugriva Rama painting",
    "kaikeyi-dasharatha-boons": "Kaikeyi Dasharatha Rama exile",
    "sita-enters-earth": "Sita enters earth painting",
    "ravana-vadh-dharma": "Rama slays Ravana painting",
    "narasimha-hiranyakashipu": "Narasimha Hiranyakashipu painting",
    "samudra-manthan-kurma": "Samudra manthan churning ocean",
    "matsya-manu": "Matsya avatar Vishnu painting",
    "varaha-earth": "Varaha avatar earth painting",
    "draupadi-vastraharan-dharma": "Draupadi Mahabharata painting",
    "karna-danveer": "Karna Mahabharata painting",
    "bhishma-pratigya": "Bhishma Mahabharata painting",
    "abhimanyu-chakravyuh": "Abhimanyu Chakravyuha painting",
    "yaksha-prashna-yudhishthira": "Yudhishthira Pandavas painting",
    "eklavya-drona-thumb": "Ekalavya Drona painting",
    "barbarik-khatu-shyam": "Khatu Shyam Barbarika",
    "hanuman-lanka-agni": "Hanuman Lanka fire Ramayana",
    "shabari-rama": "Shabari Rama berries painting",
    "ahalya-rama": "Ahalya Rama painting",
    "lakshman-rekha": "Lakshmana rekha Sita Ravana",
    "krishna-makhan-chor": "Krishna butter Makhan chor painting",
    "krishna-virat-roop": "Vishvarupa Krishna cosmic form",
    "shiva-lingodbhava-origin": "Lingodbhava Shiva pillar of light painting",
    "vishnu-ananta-shesha-origin": "Vishnu Ananta Shesha reclining painting",
    "durga-born-from-tejas": "Durga goddess Raja Ravi Varma painting",
    "ganesha-born-of-parvati": "Parvati creates Ganesha painting",
    "rama-birth-ayodhya": "Birth of Rama Ayodhya painting",
    "hanuman-birth-anjana": "Hanuman Anjana birth mythology painting",
    "murugan-skanda-birth": "Kartikeya Murugan Skanda painting",
    "surya-aditya-origin": "Surya sun god chariot painting",
    "shani-birth-chhaya": "Shani Dev mythology painting",
    "dattatreya-birth-anusuya": "Dattatreya three heads painting",
    "narasimha-pillar-appearance": "Narasimha Hiranyakashipu pillar painting",
    "vitthal-vithoba-origin": "Vithoba Vitthal Pandharpur painting",
    "bhairav-kalabhairav-origin": "Bhairava Kalabhairava painting",
    "lakshmi-ocean-birth": "Lakshmi Samudra Manthan Raja Ravi Varma",
    "saraswati-vak-origin": "Saraswati goddess veena painting",
    "kali-born-of-wrath": "Goddess Kali mythology painting",
    "jagannath-neelamadhav-origin": "Jagannath Puri trinity painting",
    "venkateswara-srinivasa-descent": "Venkateswara Tirupati Balaji",
    "annapurna-origin-kashi": "Annapurna goddess painting",
    "santoshi-mata-origin": "Santoshi Mata goddess",
    "brahma-lotus-birth": "Brahma lotus Vishnu navel painting",
    "mangal-graha-origin": "Mangal Mars graha temple India",
    "shiva-parvati-divine-wedding": "Shiva Parvati wedding Raja Ravi Varma",
    "shiva-sons-ganesha-kartikeya": "Ganesha Kartikeya Shiva family painting",
    "vishnu-lakshmi-eternal-pair": "Vishnu Lakshmi painting mythology",
    "lakshmi-as-vishnu-consort": "Lakshmi Raja Ravi Varma",
    "krishna-yashoda-mother": "Yashoda Krishna butter painting",
    "krishna-balarama-brother": "Krishna Balarama brothers painting",
    "krishna-rukmini-wedding": "Krishna Rukmini wedding painting",
    "ganesha-siddhi-buddhi": "Ganesha Siddhi Buddhi painting",
    "ganesha-shubh-labh-children": "Ganesha mythology painting",
    "rama-lakshmana-brotherhood": "Rama Lakshmana forest painting",
    "rama-bharata-paduka": "Bharata Rama paduka painting",
    "sita-as-rama-consort": "Sita Rama painting mythology",
    "hanuman-kesari-anjana-parents": "Hanuman Anjana mythology painting",
    "murugan-valli-devasena": "Murugan Valli Devasena painting",
    "murugan-ganesha-brothers": "Murugan Ganesha brothers painting",
    "surya-sanjna-chhaya": "Surya sun god painting India",
    "shani-and-surya-father": "Shani Dev Surya mythology",
    "parvati-as-mother-of-ganesha": "Parvati Ganesha mother painting",
    "kali-shiva-cremation-ground": "Kali Shiva mythology painting",
    "annapurna-shiva-household": "Annapurna Shiva painting",
    "santoshi-ganesha-daughter": "Santoshi Mata goddess",
    "jagannath-balabhadra-subhadra": "Jagannath Balabhadra Subhadra",
    "vitthal-rukmini-pandharpur": "Vitthal Rukmini Pandharpur",
    "venkateswara-padmavati-consort": "Venkateswara Padmavati Tirupati",
    "narasimha-lakshmi-prahlada": "Narasimha Prahlada Lakshmi painting",
    "brahma-saraswati-knowledge": "Brahma Saraswati painting",
    "saraswati-and-learning-family": "Saraswati goddess students painting",
    "dattatreya-atri-anusuya-parents": "Dattatreya Anusuya painting",
    "bhairav-bhairavi-consort": "Bhairava Bhairavi painting",
    "ayyappa-foster-father-raja": "Ayyappa Sabarimala painting",
    "mangal-bhumi-family": "Mangal Mars graha India",
}

DEITY_FILES: dict[str, list[str]] = {
    "shiva": ["Siva-parvati-by-raja-ravi-varma.jpg", "Shiva.jpg"],
    "krishna": [
        "Krishna Holds Up Mount Govardhan to Shelter the Villagers of Braj, ca.1590–95, The Met.jpg",
        "Raja Ravi Varma Krishna.jpg",
    ],
    "devi": ["Durga by Raja Ravi Varma.jpg", "Goddess Durga by Raja Ravi Varma.jpg"],
    "rama": ["Rama with Sita and Lakshmana.jpg", "Ram Darbar.jpg"],
    "vishnu": ["Vishnu.jpg", "Vishnu on Garuda.jpg"],
    "ganesha": ["Rebirth of Ganesha.jpg"],
    "hanuman": ["Hanuman Herb Mountain.jpg"],
    "murugan": ["Murugan.jpg", "Kartikeya.jpg"],
    "surya": ["Surya.jpg", "Sun god Surya.jpg"],
    "lakshmi": ["Raja Ravi Varma, Goddess Lakshmi, 1896.jpg"],
    "narasimha": ["Narasimha oil colour.jpg", "Narasimha killed Hiranyakashipu.jpg"],
    "brahma": ["Brahma.jpg", "Brahma Pushkar.jpg"],
    "venkateswara": ["Venkateswara.jpg", "Tirupati Balaji.jpg"],
    "ayyappa": ["Ayyappa.jpg"],
    "sai": ["Sai Baba.jpg"],
}

DEITY_SEARCH: dict[str, str] = {
    "shiva": "Shiva Parvati Raja Ravi Varma painting",
    "krishna": "Krishna mythology painting India",
    "devi": "Durga goddess Raja Ravi Varma",
    "rama": "Rama Sita Lakshmana painting",
    "vishnu": "Vishnu deity painting India",
    "ganesha": "Ganesha mythology painting",
    "hanuman": "Hanuman mythology painting",
    "murugan": "Murugan Kartikeya painting",
    "surya": "Surya sun god painting",
    "lakshmi": "Lakshmi Raja Ravi Varma",
    "narasimha": "Narasimha avatar painting",
    "brahma": "Brahma deity painting",
    "venkateswara": "Venkateswara Tirupati",
    "ayyappa": "Ayyappa Sabarimala",
    "sai": "Sai Baba Shirdi",
}


def load_media() -> dict:
    if MEDIA_PATH.exists():
        return json.loads(MEDIA_PATH.read_text(encoding="utf-8"))
    return {"festivals": {}, "stories": {}, "deities": {}}


def save_media(data: dict) -> None:
    MEDIA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def has_local(bucket: dict, slug: str) -> bool:
    entry = bucket.get(slug) or {}
    local = entry.get("local")
    if not local:
        return False
    path = ROOT / local
    return path.exists() and path.stat().st_size > 2000


def pick(filenames: list[str], search: str | None) -> dict | None:
    tried: set[str] = set()
    for name in filenames:
        if name in tried:
            continue
        tried.add(name)
        time.sleep(0.55)
        try:
            info = fi.api_file_info(name)
        except Exception as ex:
            print("  ERR", name, ex)
            continue
        if info and not info.get("_rejected"):
            return info
        if info and info.get("_rejected"):
            print("  skip", name, info.get("license"), info.get("reason", ""))
    if not search:
        return None
    time.sleep(0.7)
    try:
        titles = fi.search_candidates(search, limit=10)
    except Exception as ex:
        print("  SEARCH FAIL", search, ex)
        return None
    for title in titles:
        if title in tried:
            continue
        tried.add(title)
        time.sleep(0.55)
        try:
            info = fi.api_file_info(title)
        except Exception:
            continue
        if info and not info.get("_rejected"):
            return info
        if info and info.get("_rejected"):
            print("  skip", title, info.get("license"), info.get("reason", ""))
    return None


def download(kind: str, slug: str, chosen: dict, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(urllib.parse.urlparse(chosen["url"]).path).suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".jpg"
    local = out_dir / f"{slug}{ext}"
    time.sleep(0.45)
    try:
        local.write_bytes(fi.get(chosen["url"]))
    except Exception:
        time.sleep(1.0)
        local.write_bytes(fi.get(chosen["full_url"]))
    if local.stat().st_size < 2000:
        local.unlink(missing_ok=True)
        raise RuntimeError("download too small")
    return {**chosen, "local": str(local.relative_to(ROOT)), "kind": kind}


def fill_bucket(
    label: str,
    items: list[tuple[str, list[str], str | None]],
    bucket: dict,
    out_dir: Path,
) -> tuple[int, list[str]]:
    added = 0
    failed: list[str] = []
    for slug, files, search in items:
        if has_local(bucket, slug):
            continue
        print(label, slug)
        chosen = pick(files, search)
        if not chosen:
            print("  NONE")
            failed.append(slug)
            continue
        try:
            bucket[slug] = download(label.lower(), slug, chosen, out_dir)
            added += 1
            print("  OK", chosen["filename"], chosen["license"])
            save_media({"festivals": media_ref["festivals"], "stories": media_ref["stories"], "deities": media_ref["deities"]})
        except Exception as ex:
            print("  FAIL", ex)
            failed.append(slug)
    return added, failed


# Mutable ref filled in main so mid-run saves work
media_ref: dict = {}


def main() -> None:
    global media_ref
    media = load_media()
    media.setdefault("festivals", {})
    media.setdefault("stories", {})
    media.setdefault("deities", {})
    media_ref = media

    guide = json.loads((ROOT / "data" / "festival-guide.json").read_text(encoding="utf-8"))
    stories = json.loads((ROOT / "data" / "stories.json").read_text(encoding="utf-8"))

    fest_items: list[tuple[str, list[str], str | None]] = []
    for fest in guide.get("festivals") or []:
        slug = fest["slug"]
        fest_items.append(
            (
                slug,
                FESTIVAL_FILES.get(slug, []),
                FESTIVAL_SEARCH.get(slug) or f"{fest.get('name', slug)} hindu festival mythology",
            )
        )

    # Priority stories (explicit map) first, then remaining with deity-based search
    story_items: list[tuple[str, list[str], str | None]] = []
    seen = set()
    for slug, files in STORY_FILES.items():
        story_items.append((slug, files, STORY_SEARCH.get(slug)))
        seen.add(slug)
    for slug, search in STORY_SEARCH.items():
        if slug in seen:
            continue
        story_items.append((slug, [], search))
        seen.add(slug)
    for st in stories.get("stories") or []:
        slug = st["slug"]
        if slug in seen:
            continue
        deity = st.get("deity") or ""
        title = st.get("title") or slug
        search = f"{title} {deity} hindu mythology painting"
        story_items.append((slug, [], search))
        seen.add(slug)

    deity_items = [
        (slug, DEITY_FILES.get(slug, []), DEITY_SEARCH.get(slug))
        for slug in sorted(set(DEITY_FILES) | set(DEITY_SEARCH))
    ]

    a1, f1 = fill_bucket("FESTIVAL", fest_items, media["festivals"], OUT_F)
    a2, f2 = fill_bucket("DEITY", deity_items, media["deities"], OUT_D)
    a3, f3 = fill_bucket("STORY", story_items, media["stories"], OUT_S)

    save_media(media)
    print(
        "done added",
        a1 + a2 + a3,
        "festivals",
        len(media["festivals"]),
        "deities",
        len(media["deities"]),
        "stories",
        len(media["stories"]),
        "failed",
        len(f1) + len(f2) + len(f3),
    )
    if f1:
        print("failed festivals", f1)
    if f2:
        print("failed deities", f2)
    if f3:
        print("failed stories sample", f3[:20])


if __name__ == "__main__":
    main()
