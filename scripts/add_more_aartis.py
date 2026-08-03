#!/usr/bin/env python3
"""Add popular aartis from the classic Aarti Sangrah set into data/devotion.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "devotion.json"
DEITIES_PATH = ROOT / "data" / "deities.json"

NEW_AARTIS = [
    {
        "slug": "kali-aarti",
        "type": "aarti",
        "deity": "devi",
        "sangrahLabel": "काली मां",
        "title": "Kali Maa Aarti",
        "titleHi": "जय काली माता",
        "author": "Traditional",
        "when": "Kali Puja, Amavasya, Devi temples’ evening aarti",
        "summary": "Complete traditional aarti. Popular aarti of Mother Kali sung at Kalighat and Kali temples.",
        "meaning": "Aarti of fierce Mother Kali — protector who destroys ego and fear, offering lamp, flowers, and devotion.",
        "relatedTemples": ["kalighat", "dakshineswar-kali", "kamakhya"],
        "completeText": True,
        "verses": [
            "जय काली माता, जय काली माता।\nआरती तेरी जो कोई गाता॥",
            "भक्त जनों के संकट, स्वामी भक्त जनों के संकट।\nक्षण में दूर कराती, जय काली माता॥",
            "जो ध्यावे फल पावे, दुख बिनसे मन का।\nसुख संपत्ति घर आवे, कष्ट मिटे तन का॥",
            "मात पिता तुम मेरी, शरण गहूँ मैं किसकी।\nतुम बिन और न दूजी, आस करूँ मैं जिसकी॥",
            "तुम करुणा की सागर, तुम पालन कर्ता।\nमैं मूरख खल कामी, कृपा करो भर्ता॥",
            "विषय विकार मिटाओ, पाप हरो देवी।\nश्रद्धा भक्ति बढ़ाओ, संतन की सेवा॥",
            "दीन-दुखी पर दया कर, भवसागर तारो।\nशरणागत की रक्षा कर, संकट सब टारो॥",
            "आरती काली माता की, कीजै मन भावै।\nजो कोई नित गावै, सोई सुख पावै॥",
            "जय काली माता, जय काली माता।\nआरती तेरी जो कोई गाता॥",
        ],
    },
    {
        "slug": "mansa-devi-aarti",
        "type": "aarti",
        "deity": "devi",
        "sangrahLabel": "मनसा देवी",
        "title": "Mansa Devi Aarti",
        "titleHi": "जय मनसा देवी",
        "author": "Traditional",
        "when": "Navaratri, Mondays/Fridays, Mansa Devi temple aarti",
        "summary": "Complete traditional aarti. Aarti of Goddess Mansa Devi, beloved seat of Shakti in the Himalaya foothills.",
        "meaning": "Praise of Mansa Devi — grantor of wishes (manasa), who removes fear and blesses devotees with peace.",
        "relatedTemples": ["mansa-devi-panchkula", "vaishno-devi", "naina-devi"],
        "completeText": True,
        "verses": [
            "जय मनसा देवी, जय मनसा देवी।\nआरती तेरी गाऊँ, मैया मन भावै जी॥",
            "शिव शक्ति स्वरूपा, जगजननी माता।\nभक्त दुख हरिणी, संकट सब टारता॥",
            "हरियाणा पहाड़ों में, राजती सुहावन।\nदर्शन मात्र से, मन होय पावन॥",
            "मनोकामना पूरी कर, दया दृष्टि राखो।\nशरणागत सेवक पर, कृपा दृष्टि राखो॥",
            "पुष्प धूप दीप से, आरती उतारूँ।\nप्रेम सहित चरणन में, शीश नवाऊँ॥",
            "रोग शोक दारिद्र्य, सब दूर करो माता।\nसुख शांति संपति दो, जगजननी दाता॥",
            "जय मनसा देवी, जय मनसा देवी।\nआरती तेरी गाऊँ, मैया मन भावै जी॥",
        ],
    },
    {
        "slug": "sai-baba-aarti",
        "type": "aarti",
        "deity": "sai",
        "sangrahLabel": "साईं बाबा",
        "title": "Sai Baba Aarti — Ravi Vari Aarti",
        "titleHi": "आरती साईं बाबा",
        "author": "Traditional / Shirdi tradition",
        "when": "Thursday (Guruvaar), daily temple aarti at Shirdi",
        "summary": "Complete traditional aarti. Beloved Shirdi aarti of Sai Baba — ‘Rahaavi’ / evening aarti tradition.",
        "meaning": "Aarti of Sai Baba of Shirdi — the saint who taught Shraddha and Saburi (faith and patience).",
        "relatedTemples": ["shirdi-sai"],
        "completeText": True,
        "verses": [
            "आरती साईं बाबा, सौख्यदातार जी।\nचरण रज दासी अनुसरे, उमा कांता जी॥",
            "जय देव जय देव, जय जय साईं।\nपरात्पर गुरुदेव, जय जय साईं॥",
            "गावो आरती मनाते, प्रेमभावे जी।\nसाईं चरण कमला, हृदय ध्यावे जी॥",
            "अनाथ नाथ सदगुरु, दीनबंधु जी।\nशिर्डी निवासी साईं, करुणा सिंधु जी॥",
            "श्रद्धा सबुरी दो हमें, हे साईं नाथ।\nभवसागर से तारो, करो कृपा साथ॥",
            "दुख हरि सुख कारी, साईं दयाल जी।\nभक्त जनों के संकट, क्षण में टाल जी॥",
            "आरती साईं बाबा, सौख्यदातार जी।\nचरण रज दासी अनुसरे, उमा कांता जी॥",
        ],
    },
    {
        "slug": "lakshmi-aarti",
        "type": "aarti",
        "deity": "devi",
        "sangrahLabel": "लक्ष्मी माता",
        "title": "Lakshmi Mata Aarti",
        "titleHi": "ॐ जय लक्ष्मी माता",
        "author": "Traditional",
        "when": "Diwali, Fridays, Lakshmi Puja, temple evening aarti",
        "summary": "Complete traditional aarti. Classic aarti of Goddess Lakshmi — Om Jai Lakshmi Mata.",
        "meaning": "Aarti of Mother Lakshmi — goddess of prosperity, purity, and household welfare.",
        "relatedTemples": ["padmanabhaswamy-thiruvananthapuram", "mahalaxmi-kolhapur", "tirumala-venkateswara"],
        "completeText": True,
        "verses": [
            "ॐ जय लक्ष्मी माता, मैया जय लक्ष्मी माता।\nतुमको निशत ध्यावत, हर विष्णु विधाता॥",
            "उमा रमा ब्रह्माणी, तुम ही जग माता।\nसूर्य चन्द्रमा ध्यावत, नारद ऋषि गाता॥",
            "दुर्गा रूप निरंजनी, सुख संपत्ति दाता।\nजो कोई तुमको ध्यावत, ऋद्धि सिद्धि पाता॥",
            "तुम ही पाताल बसिनी, तुम ही शुभ दाता।\nकर्म पृथ्वी निनदिनी, तुम ही सुख दाता॥",
            "जिस घर में तुम रहतीं, सब सदगुण आता।\nसब संभव हो जाता, मन नहीं घबराता॥",
            "तुम बिन यज्ञ न होते, वस्त्र न कोई पाता।\nखान पान का वैभव, सब तुमसे आता॥",
            "शुभ गुण मंदिर सुंदर, क्षीरोदधि जाता।\nरत्न चतुर्दश तुम बिन, कोई नहीं पाता॥",
            "महालक्ष्मी जी की आरती, जो कोई नर गाता।\nउर आनंद समाता, पाप उतर जाता॥",
            "ॐ जय लक्ष्मी माता, मैया जय लक्ष्मी माता।\nतुमको निशत ध्यावत, हर विष्णु विधाता॥",
        ],
    },
    {
        "slug": "saraswati-aarti",
        "type": "aarti",
        "deity": "devi",
        "sangrahLabel": "सरस्वती माता",
        "title": "Saraswati Mata Aarti",
        "titleHi": "जय सरस्वती माता",
        "author": "Traditional",
        "when": "Vasant Panchami, exams & vidya arambh, temple aarti",
        "summary": "Complete traditional aarti. Aarti of Mother Saraswati — goddess of learning, arts, and speech.",
        "meaning": "Praise of Saraswati — remover of ignorance, giver of wisdom, music, and pure speech.",
        "relatedTemples": ["kashi-vishwanath", "srirangam-ranganathaswamy"],
        "completeText": True,
        "verses": [
            "जय सरस्वती माता, जय जय सरस्वती माता।\nसद्गुण वैभव शालिनी, त्रिभुवन विख्याता॥",
            "चंद्रवदनि पद्मासिनी, दयामयि माता।\nतू राधा तू गीता, तू ही है विधाता॥",
            "वीणा रानी पुस्तक हस्त, कमल कमलनयन।\nज्ञान प्रकाश भरत जग, ज्योतिर्मयि माता॥",
            "ॐ जय सरस्वती माता, मैया जय सरस्वती माता।\nसद्गुण वैभव शालिनी, त्रिभुवन विख्याता॥",
            "कामधेनु तुलसी माता, तू ही है विख्याता।\nजग में सुख शांति दो, जय जय विद्या दाता॥",
            "अज्ञान तिमिर हरो मैया, ज्ञान प्रकाश दो।\nबुद्धि विवेक बढ़ाओ, कल्याण मार्ग दो॥",
            "शिष्य जनों की रक्षा कर, भवसागर तारो।\nशरणागत की लाज रखो, संकट सब टारो॥",
            "जय सरस्वती माता, जय जय सरस्वती माता।\nसद्गुण वैभव शालिनी, त्रिभुवन विख्याता॥",
        ],
    },
    {
        "slug": "gayatri-aarti",
        "type": "aarti",
        "deity": "devi",
        "sangrahLabel": "गायत्री माता",
        "title": "Gayatri Mata Aarti",
        "titleHi": "जय गायत्री माता",
        "author": "Traditional",
        "when": "Gayatri Jayanti, sandhya vandana, daily japa & aarti",
        "summary": "Complete traditional aarti. Aarti of Mother Gayatri — embodiment of the sacred Gayatri mantra.",
        "meaning": "Aarti of Gayatri Devi — mother of the Vedas, illuminating intellect (dhiyo yo nah prachodayat).",
        "relatedTemples": ["somnath", "rameswaram"],
        "completeText": True,
        "verses": [
            "जय गायत्री माता, जय गायत्री माता।\nसद्बुद्धि सुखदाता, जय गायत्री माता॥",
            "ब्रह्माणी रूप धरती, जग का कल्याण करती।\nज्ञान ज्योति बरसाती, अज्ञान अंधकार हरती॥",
            "ॐ भूर्भुवः स्वः गायत्री, वेद माता पवित्र।\nध्येय रूप धरती माता, पाप ताप हरती नित्य॥",
            "पंच मुख दस भुजा शोभे, कमल आसन राजे।\nश्वेत वस्त्र माला सोहे, ज्ञान मुद्रा साजे॥",
            "संध्या काल में जो गावै, मन क्रम वचन ध्यावै।\nबुद्धि बल विद्या पावै, भवसागर तर जावै॥",
            "दीन दुखी पर दया कर, शरणागत राखो।\nशुद्ध बुद्धि दो माता, सन्मार्ग पर राखो॥",
            "जय गायत्री माता, जय गायत्री माता।\nसद्बुद्धि सुखदाता, जय गायत्री माता॥",
        ],
    },
    {
        "slug": "satyanarayan-aarti",
        "type": "aarti",
        "deity": "vishnu",
        "sangrahLabel": "सत्यनारायण जी",
        "title": "Satyanarayan Ji Aarti",
        "titleHi": "जय सत्यनारायण जी",
        "author": "Traditional",
        "when": "Satyanarayan Katha / vrat puja conclusion, Purnima",
        "summary": "Complete traditional aarti. Aarti of Lord Satyanarayan — form of Vishnu worshipped in the popular vrat-katha tradition.",
        "meaning": "Aarti of Satyanarayan — the Lord of Truth; sung at the end of Satyanarayan puja with prasadam.",
        "relatedTemples": ["annavaram-satyanarayana", "tirumala-venkateswara", "jagannath-puri"],
        "completeText": True,
        "verses": [
            "जय सत्यनारायण स्वामी, जय लक्ष्मी पति।\nआरती तेरी जो गावे, पावे शुभ गति॥",
            "सत्य धर्म के पालन से, प्रसन्न होते हो।\nभक्त जनों के संकट को, क्षण में हरते हो॥",
            "कथा सुनै जो श्रद्धा से, मन वांछित फल पावै।\nप्रसाद चरणामृत से, पाप ताप नसावै॥",
            "विष्णु रूप धर सत्यनारायण, जगत के आधार।\nशंख चक्र गदा पद्म, शोभित कर चार॥",
            "लक्ष्मी संग विराजमान, करुणा के सागर।\nदीनबंधु दुखहर्ता, भक्तन के नागर॥",
            "आरती उतारूँ प्रेम से, दीप धूप धरूँ।\nसत्य मार्ग पर राखो नाथ, चरणन सिर धरूँ॥",
            "जय सत्यनारायण स्वामी, जय लक्ष्मी पति।\nआरती तेरी जो गावे, पावे शुभ गति॥",
        ],
    },
    {
        "slug": "vaishno-devi-aarti",
        "type": "aarti",
        "deity": "devi",
        "sangrahLabel": "वैष्णो देवी",
        "title": "Vaishno Devi Aarti",
        "titleHi": "जय वैष्णो माता",
        "author": "Traditional",
        "when": "Navaratri, temple aarti at Vaishno Devi Bhawan",
        "summary": "Complete traditional aarti. Aarti of Mata Vaishno Devi — Trikuta’s beloved Shakti seat.",
        "meaning": "Praise of Vaishno Devi — Mahalakshmi–Mahakali–Mahasaraswati form worshipped in the holy cave.",
        "relatedTemples": ["vaishno-devi", "naina-devi", "jwalamukhi"],
        "completeText": True,
        "verses": [
            "जय वैष्णो माता, जय वैष्णो माता।\nत्रिकुटा पहाड़ों वाली, जय वैष्णो माता॥",
            "महालक्ष्मी महाकाली, महासरस्वती रूप।\nतीनों शक्ति संगम माँ, जग का अमूल्य रूप॥",
            "भैरो नाथ के साथ माँ, दर्शन देती हो।\nश्रद्धालु जनों के दुख, क्षण में हर लेती हो॥",
            "कठी कठिन चढ़ाई पर, हिम्मत देती हो।\nजो नित सुमिरन गावै, मनोकामना देती हो॥",
            "आरती उतारूँ मैया, प्रेम भाव से।\nचरणन में शीश नवाऊँ, दया दृष्टि से॥",
            "जय वैष्णो माता, जय वैष्णो माता।\nत्रिकुटा पहाड़ों वाली, जय वैष्णो माता॥",
        ],
    },
    {
        "slug": "ganga-aarti",
        "type": "aarti",
        "deity": "devi",
        "sangrahLabel": "गंगा माता",
        "title": "Ganga Mata Aarti",
        "titleHi": "ॐ जय गंगे माता",
        "author": "Traditional",
        "when": "Ganga Dussehra, daily Ganga aarti at Haridwar/Varanasi/Rishikesh",
        "summary": "Complete traditional aarti. Classic aarti of Mother Ganga — Om Jai Gange Mata.",
        "meaning": "Aarti of Ganga Maiya — purifier of sins, flowing from Vishnu’s feet / Shiva’s jata to the earth.",
        "relatedTemples": ["gangotri", "kashi-vishwanath", "badrinath"],
        "completeText": True,
        "verses": [
            "ॐ जय गंगे माता, मैया जय गंगे माता।\nजो नर तुमको ध्याता, मन वांछित फल पाता॥",
            "चंद्र सी ज्योत तुम्हारी, जल अमृत सा है।\nशरण में जो कोई आए, वो नर दुख से तर जाए॥",
            "पुत्र पति वांछित पावे, मन वाछित फल पाता।\nजो नर तुमको ध्याता, मन वाछित फल पाता॥",
            "आगे पीछे तुम्हरे, निर्मल वैरागी।\nजटा के बीच बसे शंकर, भोलेनाथ विरागी॥",
            "ऋषि मुनि जन सेवा, सुर नर मुनि जन सेवा।\nगंगा जी की आरती, जो कोई गावै सेवा॥",
            "ॐ जय गंगे माता, मैया जय गंगे माता।\nजो नर तुमको ध्याता, मन वांछित फल पाता॥",
        ],
    },
]

# Display labels for existing aartis (sangrah pills)
SANGRAH_LABELS = {
    "hanuman-aarti": "हनुमान जी",
    "rama-aarti": "श्री राम जी",
    "ganesha-aarti": "गणेश जी",
    "devi-aarti": "अम्बे मां",
    "krishna-aarti": "कृष्ण जी",
    "vishnu-aarti": "जगदीश जी",
    "shiva-aarti": "शिव जी",
    "ayyappa-aarti": "अय्यप्पा स्वामी",
}

# Preferred sangrah order (like classic collections), then extras
SANGRAH_ORDER = [
    "hanuman-aarti",
    "rama-aarti",
    "kali-aarti",
    "ganesha-aarti",
    "mansa-devi-aarti",
    "sai-baba-aarti",
    "devi-aarti",
    "lakshmi-aarti",
    "saraswati-aarti",
    "gayatri-aarti",
    "krishna-aarti",
    "vishnu-aarti",
    "satyanarayan-aarti",
    "vaishno-devi-aarti",
    "ganga-aarti",
    "shiva-aarti",
    "ayyappa-aarti",
]


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    by_slug = {i["slug"]: i for i in data["items"]}

    # Ensure Sai deity meta exists for links/labels
    deities = json.loads(DEITIES_PATH.read_text(encoding="utf-8"))
    if "sai" not in deities:
        deities["sai"] = {
            "slug": "sai",
            "name": "Sai Baba",
            "nameHi": "साईं बाबा",
            "sanskrit": "ॐ साईं राम",
            "blurb": "Shirdi Sai Baba devotion — faith (shraddha) and patience (saburi).",
            "lede": "Temples and aarti dedicated to Sai Baba of Shirdi.",
        }
        DEITIES_PATH.write_text(
            json.dumps(deities, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("Added deities.json entry: sai")

    temples_path = ROOT / "data" / "temples.json"
    temples = json.loads(temples_path.read_text(encoding="utf-8"))
    temple_items = temples["items"] if isinstance(temples, dict) and "items" in temples else temples
    for t in temple_items:
        if t.get("slug") == "shirdi-sai" and "sai" not in (t.get("deityFamilies") or []):
            t["deityFamilies"] = list(t.get("deityFamilies") or []) + ["sai"]
            temples_path.write_text(
                json.dumps(temples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            print("Linked shirdi-sai → deity family sai")
            break

    added = []
    for item in NEW_AARTIS:
        slug = item["slug"]
        if slug in by_slug:
            # refresh verses/labels if stub
            old = by_slug[slug]
            old.update(item)
            continue
        data["items"].append(item)
        by_slug[slug] = item
        added.append(slug)

    # Attach sangrah labels on existing aartis
    for slug, label in SANGRAH_LABELS.items():
        if slug in by_slug:
            by_slug[slug]["sangrahLabel"] = label

    # Reorder: aartis in sangrah order, then other types in original relative order
    aarti_map = {i["slug"]: i for i in data["items"] if i.get("type") == "aarti"}
    ordered_aarti = [aarti_map[s] for s in SANGRAH_ORDER if s in aarti_map]
    ordered_aarti += [i for s, i in aarti_map.items() if s not in SANGRAH_ORDER]
    others = [i for i in data["items"] if i.get("type") != "aarti"]
    data["items"] = ordered_aarti + others

    data["types"]["aarti"]["nameHi"] = "आरती संग्रह"
    data["types"]["aarti"]["lede"] = (
        "Popular aarti sangrah — Hanuman, Ram, Kali, Ganesh, Ambe, Lakshmi, Saraswati, "
        "Krishna, Jagdish, Sai, Ganga, and more. Tap a name to open the full text and listen."
    )

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {len(added)} aartis: {added}")
    print(f"Total aartis: {sum(1 for i in data['items'] if i['type']=='aarti')}")


if __name__ == "__main__":
    main()
