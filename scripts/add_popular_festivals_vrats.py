#!/usr/bin/env python3
"""Add high-search festival guides + vrat kathas (original retellings)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    with open(ROOT / "data" / name, encoding="utf-8") as f:
        return json.load(f)


def save(name: str, data):
    with open(ROOT / "data" / name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def fest(
    slug,
    name,
    name_hi,
    date_names,
    summary,
    summary_hi,
    meaning_en,
    meaning_hi,
    story_en,
    story_hi,
    myth_en,
    myth_hi,
    deities,
    how_en,
    how_hi,
    diaspora_en,
    diaspora_hi,
    regions,
    related_devotion,
    related_temples,
    importance="high",
):
    return {
        "slug": slug,
        "name": name,
        "nameHi": name_hi,
        "importance": importance,
        "dateNames": date_names,
        "summary": summary,
        "summaryHi": summary_hi,
        "meaningEn": meaning_en,
        "meaningHi": meaning_hi,
        "storyEn": story_en,
        "storyHi": story_hi,
        "mythologyEn": myth_en,
        "mythologyHi": myth_hi,
        "deityStories": deities,
        "howCelebratedEn": how_en,
        "howCelebratedHi": how_hi,
        "diasporaEn": diaspora_en,
        "diasporaHi": diaspora_hi,
        "regions": regions,
        "relatedDevotion": related_devotion,
        "relatedTemples": related_temples,
    }


def vrat(
    slug,
    deity,
    title,
    title_hi,
    when,
    summary,
    verses,
    meaning,
    temples,
    sangrah,
    author="Popular vow tradition · TirthaYatra original retelling",
):
    return {
        "slug": slug,
        "type": "vrat-katha",
        "deity": deity,
        "title": title,
        "titleHi": title_hi,
        "author": author,
        "when": when,
        "summary": summary,
        "verses": verses,
        "meaning": meaning,
        "relatedTemples": temples,
        "completeText": True,
        "sangrahLabel": sangrah,
        "audioNote": "Optional listen-along video may be added later. Read the katha aloud at home; confirm ritual timing with your family custom or local temple.",
    }


NEW_FESTIVALS = [
    fest(
        "karva-chauth",
        "Karva Chauth",
        "करवा चौथ",
        ["Karva Chauth"],
        "A sunrise-to-moonrise fast of married love — sieve, moon, and a vow for a spouse’s long life.",
        "सूर्योदय से चंद्रोदय तक सौभाग्य व्रत — छलनी, चंद्रमा, और जीवनसाथी की दीर्घायु की कामना।",
        "Karva Chauth (Karaka Chaturthi) is among India’s most searched women’s vrats. Married women (and increasingly partners who join in solidarity) keep a day-long fast, often without water, until the moon is sighted. The evening ritual — viewing the moon through a sieve, offering arghya, and then breaking the fast — has become a cultural icon across North India and the diaspora.",
        "करवा चौथ भारत की सर्वाधिक खोजी जाने वाली स्त्री व्रतों में है। विवाहिताएँ प्रायः निर्जला व्रत रखती हैं और चंद्र दर्शन–अर्घ्य के बाद पारण करती हैं।",
        "Popular tellings weave two strands. One remembers Queen Veeravati, who broke her fast too early when a false moon was shown and saw calamity until the vow was completed with faith. Another strand links the day to Parvati Ji’s austerities for Shiva Ji, and to the karva (earthen pot) as a symbol of household continuity. The heart of the observance is not spectacle: it is a public, patient prayer that love should outlast fear.",
        "लोककथाओं में रानी वीरावती का उल्लेख है — अधूरे व्रत से संकट, पूर्ण श्रद्धा से रक्षा। दूसरी धारा पार्वती जी की शिव जी हेतु तप और करवा (मटकी) को गृह–सौभाग्य का चिह्न मानती है। व्रत का हृदय दिखावा नहीं — धैर्य और प्रेम की प्रार्थना है।",
        "Mythologically the vow sits near Kartik’s season of lamps and fidelity. The moon (Chandra) is treated as witness; the sieve reminds devotees to filter haste and illusion. Family priests emphasise that the katha is heard after puja, and that health comes before harshness — many modern households adapt the fast with medical guidance while keeping the prayer intact.",
        "पुराण–लोक परंपरा में यह व्रत कार्तिक की दीप–ऋतु और सौभाग्य से जुड़ता है। चंद्र साक्षी; छलनी अधीरता का निवारण। स्वास्थ्य पहले — कई घर चिकित्सकीय सलाह से व्रत ढालते हैं, भाव वही रखते हैं।",
        [
            {
                "deity": "Parvati & Shiva",
                "deityHi": "पार्वती जी और शिव जी",
                "en": "Parvati Ji’s tapasya for Shiva Ji is remembered as the archetype of steadfast partnership — strength that chooses devotion over ease.",
                "hi": "पार्वती जी की तपस्या अडिग साझेदारी का आदर्श है — सुविधा नहीं, भक्ति का बल।",
            },
            {
                "deity": "Chandra (Moon)",
                "deityHi": "चंद्र देव",
                "en": "Moonrise ends the fast; arghya to Chandra marks the vow’s completion under the night sky.",
                "hi": "चंद्रोदय पर व्रत पूरा; चंद्र अर्घ्य से नियम की पूर्ति।",
            },
        ],
        [
            "Wake early; set a sankalp; keep a sattvic day (nirjala or as advised)",
            "Evening Shiva–Parvati / Gauri puja; listen to Karva Chauth vrat katha",
            "Sight the moon through a sieve; offer arghya; break the fast with spouse’s care",
            "Exchange mehndi, bangles, and thalis as family custom allows",
        ],
        [
            "प्रातः संकल्प; यथाशक्ति व्रत",
            "संध्या गौरी–शिव पूजा; करवा चौथ व्रत कथा",
            "छलनी से चंद्र दर्शन, अर्घ्य, फिर पारण",
            "मेहँदी– downstreamूठी–थाली परिवार रीति से",
        ],
        "In the US, UK, Canada, Gulf, and Australia, temple associations host Karva Chauth evenings with collective moon-sighting apps and projected moonrise times. Apartment balconies replace open courtyards; the sieve and lamp still travel in hand luggage.",
        "अमेरिका, ब्रिटेन, कनाडा, खाड़ी और ऑस्ट्रेलिया में मंदिर संघ चंद्रोदय समय संग सामुदायिक कार्यक्रम रखते हैं। छलनी और दीपक प्रवासी थैली में भी यात्रा करते हैं।",
        [
            {"region": "North India & NCR", "notes": "Peak cultural observance; bazaars for mehndi and sargi."},
            {"region": "Global diaspora", "notes": "Temple halls; moonrise lookups by city; photo thalis."},
        ],
        ["karva-chauth-vrat-katha", "shiva-aarti", "devi-aarti"],
        ["vaishno-devi", "mansa-devi-panchkula", "kashi-vishwanath", "mahakaleshwar-ujjain"],
    ),
    fest(
        "chhath-puja",
        "Chhath Puja",
        "छठ पूजा",
        ["Chhath Puja"],
        "Four days of rigorous sun worship — clean rivers, standing arghya, and gratitude to Surya and Chhathi Maiya.",
        "चार दिन का कठोर सूर्य आराधना व्रत — स्वच्छ जल, खड़े अर्घ्य, सूर्य और छठी मैया का आभार।",
        "Chhath is one of India’s highest-intent search festivals after the Diwali cluster, especially in Bihar, Jharkhand, eastern Uttar Pradesh, and among migrant communities worldwide. Devotees thank Surya and Chhathi Maiya for life, children, and healed hardship through a multi-day discipline of purity, fasting, and riverbank arghya at sunset and sunrise.",
        "छठ दीपावली के बाद सर्वाधिक खोजी जाने वाली परंपराओं में है — बिहार, झारखंड, पूर्वी उत्तर प्रदेश और प्रवासी बस्तियों में। सूर्य और छठी मैया के प्रति आभार का बहु–दिवसीय व्रत।",
        "Tradition remembers Chhathi Maiya (often linked with Shashthi / forms of Prakriti) as guardian of children and childbirth, and Surya as the visible giver of prana. Epic memory also recalls Draupadi and the Pandavas turning to the Sun for relief in exile, and Rama’s line honouring Surya. The standing offering in water — body aligned to the setting and rising sun — is the festival’s unmistakable mythic posture: the devotee becomes a living axis between earth and light.",
        "परंपरा में छठी मैया बच्चों की रक्षिका और सूर्य प्राणदाता हैं। महाभारत स्मृति में द्रौपदी–पांडव सूर्य की शरण लेते हैं; राम वंश भी सूर्य का सम्मान करता है। जल में खड़े अर्घ्य — भक्त धरती और ज्योति के बीच अक्ष बनता है।",
        "Unlike many home pujas, Chhath’s mythology insists on ecological purity: the river or pond must be clean enough to stand in. Thekua and other naivedya are prepared without onion–garlic, and the vow’s severity (including periods without water) is framed as thanksgiving, not bargaining. Abroad, devotees recreate ghats at lakes and designated water bodies with municipal permission.",
        "छठ की कथा स्वच्छ जल पर टिकी है। ठेकुआ आदि नैवेद्य सात्त्विक; व्रत कठोर आभार है, सौदेबाजी नहीं। विदेश में झील–सरोवर पर अनुमति संग ‘घाट’ बनते हैं।",
        [
            {
                "deity": "Surya",
                "deityHi": "सूर्य देव",
                "en": "Sandhya and Usha arghya — sunset and sunrise offerings — place Surya at the centre of household gratitude.",
                "hi": "संध्या और उषा अर्घ्य — सूर्य परिवार के आभार के केंद्र।",
            },
            {
                "deity": "Chhathi Maiya",
                "deityHi": "छठी मैया",
                "en": "Invoked for children’s protection and the mother’s strength; her presence makes Chhath a family vow, not a solitary spectacle.",
                "hi": "संतान रक्षा और माँ की शक्ति के लिए — छठ परिवार का व्रत है।",
            },
        ],
        [
            "Follow the four-day arc: Nahay Khay, Kharna, Sandhya arghya, Usha arghya",
            "Keep the ghat and kitchen pure; prepare thekua and seasonal fruits as naivedya",
            "Stand in clean water for sunset and sunrise offerings; sing Chhath geet",
            "Read Chhath vrat katha; end with prasad shared in humility",
        ],
        [
            "चार दिन: नहाय खाय, खरना, संध्या अर्घ्य, उषा अर्घ्य",
            "घाट–रसोई शुद्ध; ठेकुआ और फल नैवेद्य",
            "स्वच्छ जल में सूर्यास्त–सूर्योदय अर्घ्य; छठ गीत",
            "छठ व्रत कथा; प्रसाद विनम्रता से बाँटें",
        ],
        "From New Jersey and Toronto lakesides to Dubai and Melbourne community parks, diaspora Chhath committees organise safety marshals, women’s changing tents, and eco-cleanup after arghya — a modern expression of the same purity myth.",
        "न्यू जर्सी–टोरंटो झीलों से दुबई–मेलबर्न तक प्रवासी छठ समितियाँ सुरक्षा और सफाई संग अर्घ्य कराती हैं — वही शुद्धता का आधुनिक रूप।",
        [
            {"region": "Bihar, Jharkhand, Purvanchal", "notes": "Heartland of Chhath; river and pond ghats."},
            {"region": "Delhi NCR & Mumbai migrant belts", "notes": "Large public ghats; heavy search traffic for timings."},
            {"region": "Global diaspora", "notes": "Lake/park permissions; community thekua kitchens."},
        ],
        ["chhath-vrat-katha", "ganga-aarti", "surya-overflowing-pot"],
        ["gangotri", "jagannath-puri", "ayodhya-ram-mandir", "mahavir-mandir-patna"],
    ),
    fest(
        "ram-navami",
        "Ram Navami",
        "राम नवमी",
        ["Ram Navami"],
        "The birth festival of Rama — Maryada Purushottama — with katha, fasting, and temple jhankis.",
        "maryada पुरुषोत्तम राम जी का जन्म उत्सव — कथा, व्रत और मंदिर झाँकियाँ।",
        "Ram Navami celebrates the birth of Rama Ji on Chaitra Shukla Navami. It is a peak search festival in India and a major diaspora temple day, linking home devotion to the Ramayana’s moral cosmos: truth, restraint, and compassionate kingship.",
        "राम नवमी चैत्र शुक्ल नवमी को राम जी के जन्म का पर्व है — भारत और प्रवासी मंदिरों में उच्च खोज वाला दिन।",
        "King Dasharatha of Ayodhya longed for heirs. Through the putrakameshti sacrifice, divine payasam was shared among Kausalya, Kaikeyi, and Sumitra. On Navami, Kausalya gave birth to Rama — Vishnu’s incarnation as the ideal human. The festival is less about royal pageantry than about remembering a life that chose dharma even when the forest was easier to refuse.",
        "अयोध्या नरेश दशरथ पुत्रकाम थे। पुत्रकामेष्टि से दिव्य पायस मिला। नवमी को कौसल्या के राम जी जन्मे — विष्णु जी का नर लीला रूप। पर्व राजसी ठाठ नहीं, उस जीवन का स्मरण है जिसने वन में भी धर्म नहीं छोड़ा।",
        "Vaishnava theology reads Rama as Maryada Purushottama — the Lord who accepts human limits to teach them. Temples recite Ramcharitmanas or Valmiki’s verses; many households keep a half-day or full-day fast and place a cradle for the infant Rama. The mythic map runs from Ayodhya’s joy to the later exile — Navami holds the beginning so devotees can walk the whole path with clearer eyes.",
        "वैष्णव दृष्टि में राम जी मर्यादा पुरुषोत्तम हैं। मंदिरों में रामचरितमानस/वाल्मीकि पाठ; घरों में व्रत और बाल राम का पालना। नवमी आरंभ की ज्योति है ताकि पूरी कथा समझ से चली जाए।",
        [
            {
                "deity": "Rama",
                "deityHi": "राम जी",
                "en": "Born at noon in many calendars’ telling — the hour of clarity — Rama embodies disciplined love for Sita Ji, Lakshmana Ji, and the people of Ayodhya.",
                "hi": "बहुत परंपराओं में मध्याह्न जन्म — स्पष्टता का क्षण। राम जी सीता जी, लक्ष्मण जी और प्रजा के प्रति अनुशासित प्रेम हैं।",
            },
            {
                "deity": "Sita & the Ayodhya household",
                "deityHi": "सीता जी और अयोध्या",
                "en": "Navami anticipates the household of dharma — not only a warrior’s birth, but a family’s vow to truth.",
                "hi": "नवमी केवल योद्धा जन्म नहीं — धर्म–परिवार की प्रतिज्ञा का आरंभ।",
            },
        ],
        [
            "Morning or noon abhishek / aarti for Rama; decorate a cradle",
            "Read Ram Navami vrat katha; chant Rama naam or aarti",
            "Keep a sattvic fast as health allows; share prasad",
            "Visit a Rama temple or join a community sundara kanda / bhajan",
        ],
        [
            "प्रातः/मध्याह्न अभिषेक–आरती; पालना सजाएँ",
            "राम नवमी व्रत कथा; राम नाम/आरती",
            "यथाशक्ति व्रत; प्रसाद बाँटें",
            "राम मंदिर या सामुदायिक भजन",
        ],
        "Ayodhya’s broadcast aarti and diaspora Rama temples (from the UK and US to the Caribbean and Fiji) make Navami a global Zoom-and-mandir day. Children enact birth scenes; elders emphasise maryada over loud argument.",
        "अयोध्या आरती और प्रवासी राम मंदिर नवमी को वैश्विक बनाते हैं। बच्चे जन्म झाँकी करते हैं; बड़े मर्यादा सिखाते हैं।",
        [
            {"region": "Ayodhya & North India", "notes": "Temple throngs; Ramayana path."},
            {"region": "Diaspora (UK, US, Caribbean, Fiji)", "notes": "Strong Rama temple culture; weekend cultural programmes."},
        ],
        ["ram-navami-vrat-katha", "rama-aarti", "rama-chalisa"],
        ["ayodhya-ram-mandir", "bhadrachalam", "rameswaram", "chitrakoot-ramghat"],
    ),
    fest(
        "hanuman-jayanti",
        "Hanuman Jayanti",
        "हनुमान जयंती",
        ["Hanuman Jayanti"],
        "The appearance day of Hanuman — strength as seva, courage as prayer.",
        "हनुमान जी का प्राकट्य दिवस — बल सेवा में, साहस प्रार्थना में।",
        "Hanuman Jayanti honours the birth or appearance of Hanuman Ji, the ideal devotee of Rama. Search interest spikes for Chalisa, Tuesday vows, and temple timings — in India and across overseas Hanuman mandirs.",
        "हनुमान जयंती पर हनुमान जी का स्मरण — चालीसा, मंगलवार व्रत और मंदिर समय की खोज भारत व विदेश दोनों में बढ़ती है।",
        "Anjana and Kesari received a boon; Vayu’s grace entered the child who would leap oceans for Rama’s work. Jayanti celebrates not brute force but buddhi and bhakti braided together — the servant who lifts mountains yet bows at Rama’s feet.",
        "अंजना–केसरी को वर मिला; पवन कृपा से बालक जन्मे जो राम कार्य हेतु सागर लाँघेंगे। जयंती बल की नहीं — बुद्धि और भक्ति की गाथा है।",
        "Regional calendars differ (Chaitra Purnima in much of North India; other tithis in some Deccan and Tamil traditions). Mythically Hanuman is Shiva’s amsha and Rama’s messenger — a bridge deity for households that keep both Shaiva and Vaishnava warmth.",
        "क्षेत्रीय तिथियाँ भिन्न हो सकती हैं। हनुमान जी शिव अंश और राम दूत — शैव–वैष्णव स्नेह के सेतु।",
        [
            {
                "deity": "Hanuman",
                "deityHi": "हनुमान जी",
                "en": "Sankat Mochan — remover of crisis — remembered through Chalisa, sindoor, and quiet courage.",
                "hi": "संकट मोचन — चालीसा, सिंदूर और शांत साहस से स्मरण।",
            },
            {
                "deity": "Rama",
                "deityHi": "राम जी",
                "en": "Hanuman’s strength always points back to Rama’s mission — devotion that refuses personal credit.",
                "hi": "हनुमान बल सदैव राम कार्य की ओर — कीर्ति नहीं, सेवा।",
            },
        ],
        [
            "Temple darshan; apply sindoor as custom allows",
            "Recite Hanuman Chalisa and aarti; read Hanuman Jayanti vrat katha",
            "Offer boondi, bananas, or panjiri; keep a Tuesday-style vow if desired",
            "Serve quietly — charity or help without announcement",
        ],
        [
            "मंदिर दर्शन; रीति अनुसार सिंदूर",
            "हनुमान चालीसा–आरती; जयंती व्रत कथा",
            "बूंदी/केला/पंजीरी; इच्छानुसार मंगलवार–सा व्रत",
            " चुपचाप सेवा–दान",
        ],
        "Overseas Hanuman temples run all-day Chalisa relays and children’s ‘bajrang’ plays. Many professionals keep a digital Chalisa streak that begins or renews on Jayanti.",
        "विदेशी हनुमान मंदिर चालीसा रिले और बाल नाटक रखते हैं। कई पेशेवर जयंती से डिजिटल चालीसा क्रम जोड़ते हैं।",
        [
            {"region": "North & West India", "notes": "Major Jayanti crowds at Sankat Mochan–style temples."},
            {"region": "Global diaspora", "notes": "Weekend Chalisa; open-ground hanuman jayanti melas."},
        ],
        ["hanuman-jayanti-vrat-katha", "hanuman-aarti", "hanuman-chalisa"],
        ["salasar-balaji", "sankat-mochan-varanasi", "jakhoo-hanuman-shimla", "mahavir-mandir-patna"],
    ),
    fest(
        "vasant-panchami",
        "Vasant Panchami",
        "वसंत पंचमी",
        ["Vasant Panchami"],
        "Spring’s yellow morning — Saraswati, learning, and the first hint of Holi’s season.",
        "पीला वसंत प्रभात — सरस्वती जी, विद्या, और होली–ऋतु का संकेत।",
        "Vasant Panchami (Sri Panchami) welcomes spring and worships Saraswati Ji, goddess of speech, music, and learning. It is heavily searched by students and parents for puja vidhi, and abroad for children’s ‘first pen’ ceremonies.",
        "वसंत पंचमी पर सरस्वती जी की पूजा — छात्र–अभिभावक पूजा विधि खोजते हैं; प्रवास में अक्षरारंभ समारोह लोकप्रिय हैं।",
        "On this tithi, many tellings say Saraswati’s grace makes the world eloquent — rivers of knowledge unfrozen after winter. Basant’s mustard fields colour the North yellow; devotees wear that hue as living metaphor for ripening insight. In some regions the day also marks early preparations toward Holi’s playful devotion to Krishna.",
        "इस तिथि सरस्वती कृपा से वाणी खिलती है। सरसों के पीले खेत उत्तरी भारत में ज्ञान के पकने का रूपक बनते हैं। कुछ क्षेत्रों में यह होली–कृष्ण लीला की तैयारी भी है।",
        "Saraswati is vac (speech) and vidya (disciplined knowing). Mythologically she is the river of clarity that keeps mantra and music from becoming noise. Books, instruments, and tools of study are placed near her image — a household pantheon of curiosity.",
        "सरस्वती वाक् और विद्या हैं — मंत्र व संगीत को शोर होने से बचाती स्पष्टता की नदी। पुस्तकें–वाद्य उसके पास रखकर घर जिज्ञासा का मंदिर बनाते हैं।",
        [
            {
                "deity": "Saraswati",
                "deityHi": "सरस्वती जी",
                "en": "Veena, white lotus, and swan — symbols of harmony, purity, and viveka (discernment).",
                "hi": "वीणा, श्वेत कमल, हंस — सामंजस्य, शुद्धता और विवेक।",
            }
        ],
        [
            "Wear yellow/cream if custom allows; offer yellow flowers and sweets",
            "Place books and instruments for Saraswati puja; do aksharabhyas for children",
            "Sing Saraswati aarti or vandana; begin a gentle study vow",
            "Avoid disrespect to books for the day — a simple household maryada",
        ],
        [
            "रीति से पीला/क्रीम वस्त्र; पीले फूल–मिठाई",
            "पुस्तक–वाद्य संग सरस्वती पूजा; बच्चों का अक्षरारंभ",
            "सरस्वती आरती/वंदना; हल्का विद्या व्रत",
            "दिन भर ग्रंथों का सम्मान",
        ],
        "Universities and Indian associations abroad host Basant cultural hours — kite crafts, yellow scarves, and student blessings before exam season.",
        "विदेशी विश्वविद्यालय और भारतीय संघ बसंत सांस्कृतिक कार्यक्रम रखते हैं — परीक्षा से पूर्व आशीष।",
        [
            {"region": "North & East India", "notes": "Strong Saraswati puja; yellow aesthetics."},
            {"region": "Diaspora campuses", "notes": "Student-led pujas and classical music evenings."},
        ],
        ["saraswati-aarti", "devi-aarti"],
        ["kamakhya", "meenakshi-madurai", "belur-math", "sharada-maihar"],
    ),
    fest(
        "akshaya-tritiya",
        "Akshaya Tritiya",
        "अक्षय तृतीया",
        ["Akshaya Tritiya"],
        "The ‘never-diminishing’ tithi — beginnings, dana, and legends of inexhaustible grace.",
        "अक्षय तिथि — शुभ आरंभ, दान, और अक्षय कृपा की कथाएँ।",
        "Akshaya Tritiya (Akti) is treated as a day when punya does not decay. It draws huge search volume for gold buying and wedding muhurats, but its older heart is dana, new ventures, and remembering myths of abundance that refuse greed.",
        "अक्षय तृतीया पर पुण्य अक्षय माना जाता है। सोना–विवाह खोज बढ़ती है, पर मूल भाव दान, शुभ आरंभ और लोभ–रहित समृद्धि की कथा है।",
        "Tellings link the day to the first manifestation of Ganga’s grace in some calendars, to Krishna and Sudama’s friendship of inexhaustible love, and to the Pandavas receiving the akshaya patra — a vessel that fed the righteous without end. ‘Akshaya’ means that which does not lessen: the myth warns that only what is shared stays.",
        "कथाएँ गंगा कृपा, कृष्ण–सुदामा की अक्षय प्रीति, और पांडवों के अक्षय पात्र से जुड़ती हैं — जो पात्र धर्मियों को अन्न देता रहा। अक्षय वही है जो बाँटने से घटता नहीं।",
        "Vedic–Puranic custom treats the tithi as favourable for sankalpa: starting study, business ledgers, temple donations, or water–food charity. Modern commerce amplified jewellery ads; dharmic teachers answer by recentring annadana and truthful beginnings.",
        "संकल्प का दिन — विद्या, व्यवसाय, मंदिर दान, अन्न–जल दान। आधुनिक विज्ञापन ने आभूषण बढ़ाया; धर्म शिक्षण अन्नदान और सत्य आरंभ पर लौटाता है।",
        [
            {
                "deity": "Krishna & Sudama",
                "deityHi": "कृष्ण जी और सुदामा",
                "en": "A fist of rice offered in love returns as lifelong grace — abundance measured by friendship, not price.",
                "hi": "मुट्ठी चावल का प्रेम अक्षय कृपा बना — मोल नहीं, मित्रता।",
            },
            {
                "deity": "Annapurna / Akshaya Patra",
                "deityHi": "अन्नपूर्णा / अक्षय पात्र",
                "en": "The inexhaustible vessel feeds dharma first — a myth against hoarding.",
                "hi": "अक्षय पात्र पहले धर्म को खिलाता है — संचय के अहंकार के विरुद्ध।",
            },
        ],
        [
            "Begin a worthy project or study vow; keep accounts clean",
            "Prefer dana (food, water, knowledge) alongside any purchases",
            "Vishnu / Krishna / Lakshmi puja as family custom",
            "Read Sudama–Krishna or akshaya patra stories with children",
        ],
        [
            "शुभ कार्य या विद्या संकल्प; हिसाब शुद्ध रखें",
            "खरीद के संग दान (अन्न–जल–ज्ञान) को प्राथमिकता",
            "विष्णु/कृष्ण/लक्ष्मी पूजा रीति से",
            "बच्चों को सुदामा–अक्षय पात्र कथा सुनाएँ",
        ],
        "Diaspora families often pair Akti with temple donations and scholarship funds rather than only jewellery — a search-friendly, values-forward framing for overseas guides.",
        "प्रवासी परिवार आभूषण से अधिक मंदिर दान और छात्रवृत्ति जोड़ते हैं — विदेश गाइडों के लिए मूल्य–केंद्रित रूप।",
        [
            {"region": "Pan-India", "notes": "Muhurat shopping + traditional dana."},
            {"region": "Diaspora", "notes": "Temple funds, gold ETFs vs. quiet charity — choices vary."},
        ],
        ["vishnu-aarti", "krishna-aarti", "lakshmi-aarti", "satyanarayan-vrat-katha"],
        ["tirumala-venkateswara", "dwarka", "jagannath-puri", "mahalaxmi-kolhapur"],
    ),
    fest(
        "guru-purnima",
        "Guru Purnima",
        "गुरु पूर्णिमा",
        ["Guru Purnima"],
        "Full moon of the teacher — Vyasa, living gurus, and gratitude for the lineage of knowledge.",
        "गुरु की पूर्णिमा — व्यास जी, सद्गुरु, और ज्ञान परंपरा का आभार।",
        "Guru Purnima (Vyasa Purnima) honours the teacher principle. It is widely searched by yoga students, classical artists, and temple communities in India and abroad who want a simple gratitude rite.",
        "गुरु पूर्णिमा शिक्षक–तत्त्व का पर्व — योग साधक, कलाकार और मंदिर समुदाय आभार विधि खोजते हैं।",
        "Sage Vyasa — arranger of the Vedas and narrator of the Mahabharata — is remembered on this full moon. The mythic claim is bold: knowledge that is ordered can be transmitted; chaos of memory becomes a river others can drink. Disciples offer paduka puja, fruit, or silent pranam to parents, teachers, and guides.",
        "वेद व्यवस्थापक और महाभारत कथाकार व्यास जी का स्मरण। ज्ञान व्यवस्थित हो तो परंपरा बनती है। शिष्य पदुका पूजा, फल या मौन प्रणाम से आभार करते हैं।",
        "In yogic lore the day also marks Shiva as Adi Guru teaching the saptarishis. Whether Shaiva or Vaishnava tinted, the mythology converges: without lineage, ego invents; with lineage, practice deepens.",
        "योग कथा में शिव आदिगुरु भी स्मृत। शैव हो या वैष्णव रंग — बिना परंपरा अहंकार गढ़ता है; परंपरा से साधना गहरी होती है।",
        [
            {
                "deity": "Vyasa",
                "deityHi": "व्यास जी",
                "en": "Compiler and storyteller — the archetype of the teacher who organises revelation for householders and renunciates alike.",
                "hi": "संकलक और कथाकार — गृहस्थ व संन्यासी दोनों हेतु ज्ञान व्यवस्थित करने वाले गुरु।",
            },
            {
                "deity": "Shiva as Adi Guru",
                "deityHi": "आदिगुरु शिव जी",
                "en": "In hatha and yoga traditions, the still teacher under the banyan who turns discipline into liberation.",
                "hi": "हठ–योग परंपरा में वटवृक्ष तले स्थिर गुरु — अनुशासन से मुक्ति।",
            },
        ],
        [
            "Offer gratitude to parents, teachers, and mentors (even with a message)",
            "Read a chapter of a sacred text or listen to a guru’s teaching",
            "Temple or home puja with simple flowers and silence",
            "Donate books or sponsor a student’s fees if you can",
        ],
        [
            "माता–पिता–गुरु का आभार",
            "ग्रंथ अध्याय या सत्संग श्रवण",
            "सरल पूजा और मौन",
            "पुस्तक दान या छात्र सहायता",
        ],
        "Yoga studios from New York to Singapore schedule Guru Purnima circles; Hindu student associations hold teacher-appreciation evenings with bhajans.",
        "न्यूयॉर्क से सिंगापुर तक योग स्टूडियो गुरु पूर्णिमा सत्संग रखते हैं; छात्र संघ आभार संध्याएँ करते हैं।",
        [
            {"region": "India ashrams & temples", "notes": "Paduka puja; Vyasa worship."},
            {"region": "Global yoga & Hindu students", "notes": "Gratitude circles; online guru darshan."},
        ],
        ["vishnu-aarti", "shiva-aarti"],
        ["badrinath", "kashi-vishwanath", "tirumala-venkateswara", "belur-math"],
    ),
    fest(
        "govardhan-puja",
        "Govardhan Puja",
        "गोवर्धन पूजा",
        ["Govardhan Puja"],
        "The day after Diwali — annakut mountains of food, and Krishna lifting the hill of care.",
        "दीपावली के अगले दिन — अन्नकूट का पर्वत और गोवर्धन उठाने वाली कृष्ण कथा।",
        "Govardhan Puja (Annakut) follows Diwali in many North Indian and Pushtimarg calendars. Devotees prepare vast vegetarian offerings shaped like a mountain and remember Krishna protecting Braj from Indra’s storm.",
        "गोवर्धन पूजा/अन्नकूट दीपावली के बाद — अन्न का पर्वत और इंद्र के गर्जन से ब्रज की रक्षा की कृष्ण कथा।",
        "When Braj worshipped Indra for rain, young Krishna asked why they ignored Govardhan — the hill that fed their cows. They offered to the hill instead. Indra’s pride sent floods; Krishna lifted Govardhan on a finger for seven days as umbrella. The myth turns theology toward ecological devotion: protect the land that protects you.",
        "ब्रज जब इंद्र यज्ञ करता, बाल कृष्ण ने पूछा — गोवर्धन क्यों न पूजें जो गौओं को पालता है? इंद्र का अहंकार वर्षा बना; कृष्ण ने सात दिन गोवर्धन उठाया। कथा भूमि–प्रेम की ओर मोड़ती है।",
        "Vaishnava homes build annakut — trays of grains, sweets, and vegetables. The ‘mountain’ is circumambulated; leftovers become community prasad. Abroad, temples recreate miniature Govardhan with fruit and rice.",
        "वैष्णव घर अन्नकूट सजाते हैं — परिक्रमा और सामुदायिक प्रसाद। विदेश में फल–चावल का छोटा गोवर्धन बनता है।",
        [
            {
                "deity": "Krishna–Govardhan",
                "deityHi": "कृष्ण जी–गोवर्धन",
                "en": "The lifted hill is both miracle and metaphor: divine care that shelters the humble.",
                "hi": "उठाया पर्वत चमत्कार और रूपक दोनों — विनम्र की छत्रछाया।",
            },
            {
                "deity": "Indra humbled",
                "deityHi": "इंद्र का अहंकार",
                "en": "Rain without gratitude becomes violence; the myth corrects transactional religion.",
                "hi": "बिना आभार वर्षा हिंसा बनती है — कथा लेन–देन धर्म को सुधारती है।",
            },
        ],
        [
            "Prepare annakut / chappan bhog as means allow",
            "Read the Govardhan story; offer to Krishna and share prasad",
            "Circumambulate the food-hill or a symbolic mound",
            "Thank farmers, cattle, and the ‘hills’ that feed your city",
        ],
        [
            "यथाशक्ति अन्नकूट/छप्पन भोग",
            "गोवर्धन कथा; कृष्ण अर्पण व प्रसाद",
            "अन्न–पर्वत की परिक्रमा",
            "किसान–गौ–भूमि का स्मरण",
        ],
        "Haveli and ISKCON temples abroad stage dramatic annakut displays the day after Diwali — a major Instagram and search moment for ‘Annakut 2026’ style queries.",
        "विदेशी हवेली और इस्कॉन मंदिर दीपावली के अगले दिन भव्य अन्नकूट लगाते हैं — खोज और सोशल दोनों में लोकप्रिय।",
        [
            {"region": "Braj, Gujarat, Rajasthan, North India", "notes": "Classic annakut culture."},
            {"region": "Diaspora Vaishnava temples", "notes": "Food-art Govardhan; volunteer kitchens."},
        ],
        ["krishna-aarti", "krishna-chalisa", "janmashtami-vrat-katha"],
        ["banke-bihari-vrindavan", "nathdwara-shrinathji", "dwarka", "iskcon-vrindavan"],
    ),
    fest(
        "rath-yatra",
        "Jagannath Rath Yatra",
        "जगन्नाथ रथ यात्रा",
        ["Jagannath Rath Yatra"],
        "When the Lord of the Universe rides a chariot — and the world pulls the rope together.",
        "जब जगन्नाथ रथ पर विराजते हैं — और संसार मिलकर रस्सी खींचता है।",
        "The Puri Rath Yatra is among Hinduism’s most visible public festivals and a growing diaspora search topic (from ISKCON raths to city parade permits). Jagannath, Balabhadra, and Subhadra leave the temple for the Gundicha yatra — god among the people.",
        "पुरी रथ यात्रा हिंदू जगत के सबसे दृश्य उत्सवों में है। जगन्नाथ, बलभद्र और सुभद्रा गुंडिचा यात्रा पर निकलते हैं — प्रभु जनों के बीच।",
        "Legends speak of Krishna–Jagannath’s form, of Subhadra and Balabhadra as companions, and of a deity who accepts incomplete, wooden, compassionate shapes so all castes may serve. Pulling the chariot is itself a mythic act: the devotee’s body becomes the vehicle of the divine progress.",
        "कथाएँ कृष्ण–जगन्नाथ रूप, सुभद्रा–बलभद्र संग, और उस विग्रह की हैं जो काष्ठ के करुण रूप में सबको सेवा का अधिकार देते हैं। रस्सी खींचना स्वयं कथा है — भक्त की देह दिव्य यात्रा का वाहन।",
        "Puranic and Odia traditions layer stories of Indradyumna, the unfinished murti, and the Lord’s yearly longing to visit the garden temple. The mythology democratises darshan: the street becomes the sanctum.",
        "इंद्रद्युम्न और अपूर्ण विग्रह की कथाएँ रथ को जन–दर्शन बनाती हैं — गली ही गर्भगृह।",
        [
            {
                "deity": "Jagannath",
                "deityHi": "जगन्नाथ जी",
                "en": "Lord of the Universe in a form that invites intimate, almost childlike love — and massive public seva.",
                "hi": "जगत के नाथ — आत्मीय प्रेम और विशाल जन सेवा दोनों आमंत्रित।",
            },
            {
                "deity": "Balabhadra & Subhadra",
                "deityHi": "बलभद्र और सुभद्रा",
                "en": "Sibling deities on companion chariots — the yatra as a family of the divine moving through the city.",
                "hi": "सह रथों पर सहोदर देव — नगर में चलता दिव्य परिवार।",
            },
        ],
        [
            "Follow Puri or local temple schedules; respect crowd and safety rules",
            "If abroad, join ISKCON / Odia association rath; volunteer for rope or prasad",
            "Sing Jagannath bhajans; read a short yatra katha at home",
            "Offer anna dana — the Lord’s festival is incomplete without feeding others",
        ],
        [
            "पुरी/स्थानीय समय देखें; सुरक्षा रखें",
            "विदेश में इस्कॉन/ओड़िया रथ में रस्सी या प्रसाद सेवा",
            "जगन्नाथ भजन; घर पर संक्षिप्त कथा",
            "अन्नदान — बिना भोजन यात्रा अधूनरी",
        ],
        "From New York Avenue raths to London and Melbourne parades, diaspora Rath Yatra is a top ‘Hindu festival abroad’ search companion to Diwali and Holi.",
        "न्यूयॉर्क से लंदन–मेलबर्न तक प्रवासी रथ यात्रा दीपावली–होली के संग विदेश खोजों में ऊँची है।",
        [
            {"region": "Puri, Odisha", "notes": "The archetypal yatra; global broadcast."},
            {"region": "ISKCON worldwide", "notes": "City chariot festivals; heavy volunteer culture."},
        ],
        ["vishnu-aarti", "krishna-aarti", "satyanarayan-vrat-katha"],
        ["jagannath-puri", "iskcon-mayapur", "iskcon-delhi", "iskcon-bengaluru"],
    ),
    fest(
        "onam",
        "Onam",
        "ओणम",
        ["Onam"],
        "Kerala’s harvest homecoming — King Mahabali’s visit, pookalam flowers, and the Onam sadya.",
        "केरल का फसल–स्वागत — राजा महाबली की वापसी, फूलों की पൂकलम, और ओणम सद्या।",
        "Onam is Kerala’s flagship festival and a major diaspora search term wherever Malayali communities gather. It commemorates the annual return of the just asura king Mahabali (Maveli) and the land’s abundance under his remembered reign.",
        "ओणम केरल का प्रमुख पर्व और मलयाली प्रवास की बड़ी खोज है — न्यायप्रिय राजा महाबली (मावेली) की वार्षिक वापसी और समृद्धि का स्मरण।",
        "Vamana, the dwarf Brahmin form of Vishnu, asked three steps of land from Mahabali. When the king offered his head for the third step, he was granted the boon to visit his people once a year. Onam is that visit: victory without humiliation — the Lord honours a devotee–king’s truthfulness.",
        "वामन रूपी विष्णु ने महाबली से तीन पग भूमि माँगी। तीसरे पग हेतु जब राजा ने मस्तक झुकाया, उन्हें वर्ष में एक बार प्रजा मिलने का वर मिला। ओणम वही भेंट है — सत्य के राजा का सम्मान।",
        "Flower carpets (pookalam), the vegetarian sadya on banana leaf, boat races, and pulikali dance dramatise a mythic golden age. The festival’s theology softens binary ‘asura = evil’: Mahabali is beloved precisely for dharma.",
        "पूकलम, केले के पत्ते पर सद्या, वल्लमकली — पौराणिक सुवर्ण युग का नाट्य। यहाँ असुर मात्र दुष्ट नहीं — महाबली धर्म हेतु प्रिय हैं।",
        [
            {
                "deity": "Vamana / Vishnu",
                "deityHi": "वामन / विष्णु जी",
                "en": "The small form that measures worlds — yet bows to the integrity of a generous king.",
                "hi": "छोटे रूप में लोक नापते हैं — फिर भी दानी राजा की सत्यता का सम्मान करते हैं।",
            },
            {
                "deity": "Mahabali",
                "deityHi": "महाबली",
                "en": "Not a villain in Kerala’s heart — a ruler whose yearly homecoming defines Onam joy.",
                "hi": "केरल के हृदय में खलनायक नहीं — जिसकी वार्षिक वापसी ओणम की खुशी है।",
            },
        ],
        [
            "Lay a pookalam; wear kasavu or festive Kerala attire",
            "Cook or share an Onam sadya; invite neighbours",
            "Tell children the Vamana–Mahabali story",
            "Join association Onam games, music, and charity drives",
        ],
        [
            "पूकलम; कासावु/उत्सव वस्त्र",
            "ओणम सद्या बनाएँ या साझा करें",
            "बच्चों को वामन–महाबली कथा सुनाएँ",
            "संघ खेल–संगीत–दान में जुड़ें",
        ],
        "Malayali associations from the Gulf to the US and UK host the year’s largest sadya halls — Onam often outranks other regional festivals in local ‘Indian event’ searches.",
        "खाड़ी से अमेरिका–ब्रिटेन तक मलयाली संघ विशाल सद्या हॉल भरते हैं — स्थानीय खोजों में ओणम अक्सर शीर्ष पर।",
        [
            {"region": "Kerala", "notes": "Ten-day Onam season; Thiruvonam climax."},
            {"region": "Gulf, US, UK, Singapore", "notes": "Huge association Onams; temple plus cultural centre."},
        ],
        ["vishnu-aarti", "vamana-bali"],
        ["padmanabhaswamy-thiruvananthapuram", "guruvayur", "sabarimala", "mookambika-kollur"],
    ),
    fest(
        "ugadi",
        "Ugadi",
        "युगादि",
        ["Ugadi"],
        "Telugu–Kannada New Year — bitter–sweet bevu–bella, and the reading of the year’s scroll.",
        "तेलुगु–कन्नड़ नववर्ष — बेवु–बेल्ला का कड़वा–मीठा और पंचांग श्रवण।",
        "Ugadi (Yugadi) marks the New Year for many Telugu and Kannada households, often falling with Gudi Padwa. Diaspora searches spike for ‘Ugadi pachadi recipe’ and temple special puja.",
        "युगादि तेलुगु–कन्नड़ नववर्ष — अक्सर गुड़ी पड़वा संग। प्रवास में पच्चड़ी रेसिपी और विशेष पूजा खोज बढ़ती है।",
        "The day is tied to Brahma’s creation rhythms and to the turning of the lunisolar year in Chaitra. Families taste Ugadi pachadi — neem and jaggery — so the tongue learns that a year holds bitter and sweet, and courage must meet both.",
        "दिन सृष्टि लय और चैत्र वर्षारंभ से जुड़ा। बेवु–बेल्ला चखकर जीभ सीखती है — वर्ष में तिक्त और मधुर दोनों आएँगे।",
        "Panchanga sravanam (hearing the year’s forecast) continues the mythic role of time-priests: not fatalism, but readiness. Vishnu and household deities receive special abhyanga and decoration.",
        "पंचांग श्रवण काल–पुरोहित की कथा जारी रखता है — भाग्यवाद नहीं, तैयारी। विष्णु व गृह देवता विशेष पूजा पाते हैं।",
        [
            {
                "deity": "Brahma & Kaala",
                "deityHi": "ब्रह्मा जी और काल",
                "en": "New Year as conscious entry into time — creation renewed in the household calendar.",
                "hi": "नववर्ष काल में सचेत प्रवेश — गृह कैलेंडर में सृष्टि का पुनःआरंभ।",
            },
            {
                "deity": "Vishnu",
                "deityHi": "विष्णु जी",
                "en": "Preserver of order through the year’s changes; many temples hold special Ugadi alankaram.",
                "hi": "वर्ष के परिवर्तन में व्यवस्था के पालक; मंदिरों में विशेष अलंकारम।",
            },
        ],
        [
            "Oil bath and fresh clothes; decorate the entrance",
            "Prepare Ugadi pachadi; share with neighbours",
            "Listen to panchanga sravanam at temple or online",
            "Set one ethical intention for the year",
        ],
        [
            "अभ्यंग स्नान–नये वस्त्र; तोरण",
            "युगादि पच्चड़ी; पड़ोस संग बाँटें",
            "पंचांग श्रवण",
            "वर्ष हेतु एक नैतिक संकल्प",
        ],
        "Telugu and Kannada sanghams abroad run Ugadi sabhas with classical music — a cornerstone ‘South Indian New Year’ search cluster alongside Puthandu and Vishu.",
        "तेलुगु–कन्नड़ संघ युगादि सभाएँ रखते हैं — पुत्तंडु–विषु के संग दक्षिण नववर्ष खोज का स्तंभ।",
        [
            {"region": "Andhra, Telangana, Karnataka", "notes": "Core Ugadi culture."},
            {"region": "US & Gulf Telugu belts", "notes": "Large sabhas; pachadi contests."},
        ],
        ["vishnu-aarti", "satyanarayan-vrat-katha"],
        ["tirumala-venkateswara", "kanaka-durga-vijayawada", "yadagirigutta", "udupi-krishna"],
    ),
    fest(
        "vaisakhi",
        "Vaisakhi / Vishu / Puthandu",
        "वैसाखी · विषु · पुत्तंडु",
        ["Vaisakhi / Vishu / Puthandu"],
        "April harvest new years — Baisakhi joy, Vishu kani, and Tamil Puthandu beginnings.",
        "अप्रैल फसल नववर्ष — बैसाखी आनंद, विषु कणि, और तमिल पुत्तंडु।",
        "Mid-April brings interleaved New Year / harvest festivals across North and South — heavily searched by diaspora families coordinating school leave and temple visits.",
        "अप्रैल मध्य उत्तरी–दक्षिणी नववर्ष/फसल पर्व — प्रवासी परिवार छुट्टी और मंदिर समय जोड़ते हुए खोजते हैं।",
        "Solar transition into Mesha (Aries) underpins many of these observances. Folklore and regional epics bless the first sight of auspicious objects (Vishu kani), the opening of new account books, and thanksgiving for wheat and rice harvests. Sikh history also marks Vaisakhi as a day of communal courage — neighbouring Hindu households often share the season’s melas in friendship.",
        "मेष संक्रांति कई रीतियों का आधार। विषु कणि की शुभ दृष्टि, नये खाते, फसल आभार। सिख इतिहास में वैसाखी साहस का दिन भी — पड़ोसी हिंदू परिवार मेले की मैत्री बाँटते हैं।",
        "The mythology is solar and agrarian: Surya’s clarity, Annapurna’s grain, and the ethical reset of a fiscal–ritual year. Diversity is the point — one sky, many kitchens.",
        "सौर–कृषि कथा — सूर्य स्पष्टता, अन्नपूर्णा का धान्य, नैतिक वर्षारंभ। एक आकाश, अनेक रसोई।",
        [
            {
                "deity": "Surya & Annapurna",
                "deityHi": "सूर्य और अन्नपूर्णा",
                "en": "Harvest thanks to light and food — the oldest festival grammar.",
                "hi": "प्रकाश और अन्न का आभार — सबसे पुरानी उत्सव भाषा।",
            }
        ],
        [
            "Temple visit; wear new clothes; share regional sweets",
            "Vishu: arrange kani (mirror, rice, fruit, gold, scripture) for first sight",
            "Puthandu / Baisakhi: family feast and community fair if available",
            "Donate grain or cook for someone who needs a meal",
        ],
        [
            "मंदिर; नये वस्त्र; क्षेत्रीय मिठाई",
            "विषु कणि सजावट",
            "पुत्तंडु/बैसाखी परिवार भोज–मेला",
            "अन्न दान या किसी को भोजन",
        ],
        "Gurdwara and Hindu temple complexes abroad often sit within the same April weekend calendar — practical guides should list both respectfully.",
        "विदेश में गुरुद्वारा और हिंदू मंदिर एक ही सप्ताहांत कैलेंडर में आते हैं — दोनों का सम्मान जरूरी।",
        [
            {"region": "Punjab & North", "notes": "Baisakhi harvest melas."},
            {"region": "Kerala & Tamil Nadu", "notes": "Vishu and Puthandu home rites."},
            {"region": "Diaspora", "notes": "Combined cultural association events."},
        ],
        ["ganga-aarti", "vishnu-aarti"],
        ["golden-temple-proxy", "guruvayur", "meenakshi-madurai", "tirumala-venkateswara"],
    ),
    fest(
        "dhanteras",
        "Dhanteras",
        "धनतेरस",
        ["Dhanteras"],
        "Diwali week begins — Dhanvantari’s pot of health, Lakshmi’s welcome, and mindful prosperity.",
        "दीपावली सप्ताहारंभ — धन्वंतरि का आरोग्य कलश, लक्ष्मी स्वागत, और सचेत समृद्धि।",
        "Dhanteras (Dhantrayodashi) opens the Diwali cluster and dominates pre-Diwali search charts for muhurat and shopping. Older dharma remembers Dhanvantari rising from the ocean with amrita and the physician’s art.",
        "धनतेरस दीपावली श्रृंखला खोलता है — मुहूर्त/खरीद खोजों में शीर्ष। प्राचीन स्मृति में समुद्र से धन्वंतरि अमृत–कलश संग emerg हुए।",
        "During the Samudra Manthan, Lord Dhanvantari appeared bearing the nectar pot — mythic source of Ayurveda. Homes light lamps for Yama in some customs (to push back untimely death) and buy metal utensils or coins as symbols of household stability. The story’s edge: wealth that ignores health is incomplete; the physician–god arrives before the night of lamps.",
        "समुद्र मंथन में धन्वंतरि अमृत कलश लेकर प्रकट हुए — आयुर्वेद की पौराणिक जड़। कुछ घर यम दीप जलाते हैं; धातु बर्तन/सिक्के स्थिरता के चिह्न। कथा कहती है — बिना आरोग्य धन अधूरा।",
        "Lakshmi–Kubera worship on this evening ties prosperity to orderly accounts. Ethical guides stress: do not let market frenzy erase dana and debt repayment.",
        "लक्ष्मी–कुबेर पूजा समृद्धि को व्यवस्थित हिसाब से जोड़ती है। बाजार हड़बड़ी दान और ऋण शुद्धि न मिटाए।",
        [
            {
                "deity": "Dhanvantari",
                "deityHi": "धन्वंतरि जी",
                "en": "Divine physician — pray for healers, medicines, and the body’s longevity before festive excess.",
                "hi": "दिव्य वैद्य — उत्सव से पहले आरोग्य और चिकित्सकों हेतु प्रार्थना।",
            },
            {
                "deity": "Lakshmi",
                "deityHi": "लक्ष्मी जी",
                "en": "Invited with clean thresholds and honest ledgers — prosperity as responsibility.",
                "hi": "स्वच्छ द्वार और सत्य खातों संग आमंत्रित — समृद्धि जिम्मेदारी है।",
            },
        ],
        [
            "Clean and light the entrance; optional Yama deepak as family custom",
            "Dhanvantari / Lakshmi puja; buy something useful for the home if you wish",
            "Prefer quality and need over panic shopping",
            "Set aside charity before festive spending",
        ],
        [
            "द्वार स्वच्छ–दीप; रीति से यम दीपक",
            "धन्वंतरि/लक्ष्मी पूजा; उपयोगी गृह वस्तु",
            "हड़बड़ी खरीद से बचें",
            "खर्च से पूर्व दान अंश",
        ],
        "Overseas Indians search ‘Dhanteras outside India’ for temple Lakshmi hours and bullion shop timings — pair with a short Dhanvantari prayer in community newsletters.",
        "प्रवासी ‘Dhanteras’ मंदिर समय और धातु खरीद खोजते हैं — न्यूज़लेटर में धन्वंतरि प्रार्थना जोड़ें।",
        [
            {"region": "Pan-India", "notes": "Market rush + home puja."},
            {"region": "Diaspora", "notes": "Temple evening aarti; symbolic coin puja."},
        ],
        ["lakshmi-aarti", "dhanteras"],
        ["mahalaxmi-kolhapur", "tirumala-venkateswara", "padmanabhaswamy-thiruvananthapuram", "kashi-vishwanath"],
    ),
    fest(
        "kartik-purnima",
        "Kartik Purnima",
        "कार्तिक पूर्णिमा",
        ["Kartik Purnima"],
        "The full moon of lamps — Tripura’s fall, Dev Deepavali on the ghats, and Kartik’s closing glory.",
        "दीपों की पूर्णिमा — त्रिपुरासुर वध, घाटों पर देव दीपावली, कार्तिक की शोभा।",
        "Kartik Purnima (Tripuri Purnima) is a top late-autumn pilgrimage and lamp-festival search, especially for Varanasi’s Dev Deepavali and sacred baths.",
        "कार्तिक पूर्णिमा देर पतझड़ की बड़ी खोज — काशी देव दीपावली और पुण्य स्नान।",
        "One central telling: Shiva destroyed the three flying cities of the Tripurasuras with a single arrow when they aligned — a myth of timing, focus, and the end of arrogance. Rivers and tanks glow with lamps as if the gods themselves were celebrating Diwali (Dev Deepavali).",
        "कथा: शिव जी ने त्रिपुरासुर के तीन उड़ते पुरों को एक बाण से तब भेदा जब वे एक रेखा में आए — समय, एकाग्रता, अहंकार का अंत। घाट दीपों से जगमगाते हैं मानो देव स्वयं दीपावली मना रहे हों।",
        "Kartik’s month already braids Vishnu’s awakening, Tulsi rites, and Surya vows; the Purnima gathers them into a luminous finale. Sikh tradition also marks Guru Nanak Jayanti on or near this full moon in many years — share public space with courtesy.",
        "कार्तिक में विष्णु जागरण, तुलसी और सूर्य व्रत पहले से हैं; पूर्णिमा उन्हें ज्योतिर्मय समापन देती है। कई वर्षों गुरु नानक जयंती निकट — सार्वजनिक शिष्टाचार रखें।",
        [
            {
                "deity": "Shiva–Tripurantaka",
                "deityHi": "त्रिपुरारी शिव जी",
                "en": "The archer of perfect moment — evil cities fall when ego’s orbits coincide.",
                "hi": "पूर्ण क्षण के धनुर्धर — अहंकार की कक्षाएँ मिलें तब ही गिरें।",
            },
            {
                "deity": "Ganga & the ghats",
                "deityHi": "गंगा जी और घाट",
                "en": "Dev Deepavali turns the river into a mirror of heaven’s lamps.",
                "hi": "देव दीपावली नदी को स्वर्गीय दीपों का दर्पण बनाती है।",
            },
        ],
        [
            "Light rows of diyas at home or on safe public ghats",
            "Take a holy bath if custom and health allow; recite Shiva or Vishnu names",
            "Offer deep dana; avoid littering water bodies",
            "Read a short Tripura story; keep Kartik vows gently closed",
        ],
        [
            "घर/सुरक्षित घाट पर दीप पंक्ति",
            "रीति–स्वास्थ्य अनुसार स्नान; शिव/विष्णु नाम",
            "दीप दान; जल प्रदूषण न करें",
            "त्रिपुर कथा; कार्तिक व्रत शांति से पूर्ण करें",
        ],
        "Travel searches for ‘Varanasi Dev Deepavali’ dominate abroad; temples overseas host lamp gardens as local echoes.",
        "‘वाराणसी देव दीपावली’ यात्रा खोज विदेश में ऊँची; प्रवासी मंदिर दीप उद्यान सजाते हैं।",
        [
            {"region": "Varanasi & river towns", "notes": "Dev Deepavali spectacle."},
            {"region": "Pan-India Kartik closings", "notes": "Temple lamp festivals."},
            {"region": "Diaspora", "notes": "Lamp gardens; cultural Kartik evenings."},
        ],
        ["shiva-aarti", "ganga-aarti", "vishnu-aarti"],
        ["kashi-vishwanath", "gangotri", "rameswaram", "pushkar-proxy"],
    ),
    fest(
        "hartalika-teej",
        "Hartalika Teej",
        "हरतालिका तीज",
        ["Hartalika Teej"],
        "Parvati’s monsoon vow — green bangles, night jagran, and a fast for Shiva’s grace.",
        "पार्वती जी का वर्षा व्रत — हरी चूड़ियाँ, रात्रि जागरण, शिव कृपा हेतु उपवास।",
        "Hartalika Teej is a major women’s festival search in North and West India (and among diaspora from those regions), centred on Parvati Ji’s austerity to obtain Shiva Ji as husband.",
        "हरतालिका तीज उत्तर–पश्चिम भारत की बड़ी स्त्री पर्व खोज — पार्वती जी की तपस्या से शिव जी वर रूप में।",
        "The name remembers ‘harit’ (abduction/withdrawal) and ‘aalika’ (friend): Parvati slipped away with a companion to forest tapasya when her penance was obstructed. Shiva tested and accepted her. Teej’s swings, green dress, and night stories reenact longing that matures into household shakti.",
        "‘हरत’ और सखी संग वन तप की कथा — बाधा आने पर पार्वती जी तप हेतु निकलीं; शिव ने परीक्षा कर स्वीकारा। झूला, हरा वस्त्र, रात्रि कथा — लौ लगन जो गृह शक्ति बने।",
        "Sister Teej festivals (Hariyali Teej, Kajari Teej) share monsoon mythology: earth greening as Parvati’s joy. Hartalika emphasises nirjala or fruit fasts and listening to the Teej katha with friends.",
        "हरियाली/कजरी तीज बहनें — वर्षा में धरती हरियाली पार्वती आनंद। हरतालिका में व्रत और सखियों संग कथा।",
        [
            {
                "deity": "Parvati",
                "deityHi": "पार्वती जी",
                "en": "The yogini who chooses Shiva — autonomy inside devotion.",
                "hi": "शिव चुनती योगिनी — भक्ति के भीतर स्वायत्तता।",
            },
            {
                "deity": "Shiva",
                "deityHi": "शिव जी",
                "en": "The ascetic husband won not by force but by Parvati’s unbroken tapas.",
                "hi": "तप से वर — बल से नहीं, अखंड साधना से।",
            },
        ],
        [
            "Dress in green/bridal colours as custom; gather with friends",
            "Keep the Teej fast wisely; night jagran with songs and katha",
            "Shiva–Parvati puja; offer seasonal fruits and mehndi",
            "Read Hartalika Teej vrat katha before breaking the fast",
        ],
        [
            "रीति से हरा/सुहाग रंग; सखी संग",
            "यथाशक्ति व्रत; रात्रि जागरण–गीत",
            "शिव–पार्वती पूजा; मेहँदी–फल",
            "पारण से पूर्व हरतालिका व्रत कथा",
        ],
        "Community centres in the US/UK host Teej mehndi nights — often the largest women-led Hindu cultural search around monsoon’s end.",
        "अमेरिका/ब्रिटेन में तीज मेहँदी रातें — वर्षा अंत की बड़ी महिला–नेतृत्व सांस्कृतिक खोज।",
        [
            {"region": "Rajasthan, UP, Bihar, MP, Maharashtra", "notes": "Strong Teej customs (forms vary)."},
            {"region": "Diaspora", "notes": "Mehndi + katha evenings in associations."},
        ],
        ["teej-vrat-katha", "shiva-aarti", "devi-aarti"],
        ["vaishno-devi", "ambaji", "mahakaleshwar-ujjain", "kashi-vishwanath"],
    ),
    fest(
        "vat-savitri",
        "Vat Savitri",
        "वट सावित्री",
        ["Vat Savitri", "Vat Purnima"],
        "Savitri’s victory over death — banyan threads, and a vow for a beloved’s life.",
        "सावित्री की मृत्यु पर विजय — वट सूत्र, और प्रिय के जीवन का व्रत।",
        "Vat Savitri / Vat Purnima is a classic women’s vrat with enduring search demand, retelling how Savitri followed Yama and won Satyavan back through wisdom and steadfast love.",
        "वट सावित्री/वट पूर्णिमा क्लासिक स्त्री व्रत — सावित्री यम के पीछे चलीं और विवेक से सत्यवान को वापस लाईं।",
        "Savitri chose Satyavan knowing his short life. On the fated day she walked with him to the forest; when Yama drew his soul, she followed with reasoned speech and unbroken loyalty until boons restored her husband’s life and lineage. Women tie threads around a banyan (vat) — the tree of shelter and long memory.",
        "सावित्री ने अल्पायु जानकर भी सत्यवान चुना। निर्धारित दिन वन में यम प्राण ले गए; वे तर्क और भक्ति से पीछे रहीं याब तक वर मिले। महिलाएँ वट पर धागे बाँधती हैं — आश्रय और दीर्घ स्मृति का वृक्ष।",
        "The mythology elevates buddhi-bhakti: love that can debate death without hatred. Regional tithi differs (Amavasya in parts of the North; Purnima in the West) — always confirm locally.",
        "कथा बुद्धि–भक्ति उठाती है — मृत्यु से द्वेष रहित संवाद। तिथि क्षेत्रानुसार भिन्न — स्थानीय पुष्टि करें।",
        [
            {
                "deity": "Savitri & Satyavan",
                "deityHi": "सावित्री और सत्यवान",
                "en": "Human heroes of the Mahabharata/Puranic stream — courage in marriage as spiritual practice.",
                "hi": "मानवीय नायक — विवाह में साहस ही साधना।",
            },
            {
                "deity": "Yama",
                "deityHi": "यम जी",
                "en": "Lord of order who yields not to force but to dharma spoken truly.",
                "hi": "व्यवस्था के देव — बल नहीं, सत्य धर्म से मानते हैं।",
            },
        ],
        [
            "Fast as health allows; worship the banyan or a symbolic tree/plant",
            "Tie sacred thread; listen to Vat Savitri vrat katha",
            "Offer fruits and water; pray for family longevity and integrity",
            "Share the story with younger women and men alike — wisdom is not gated",
        ],
        [
            "यथाशक्ति व्रत; वट या प्रतीक वृक्ष पूजा",
            "धागा बाँधें; वट सावित्री कथा सुनें",
            "फल–जल अर्पण; दीर्घायु–सत्यता की प्रार्थना",
            "कथा युवा पीढ़ी संग बाँटें",
        ],
        "Park banyans are rare abroad — devotees use potted trees, courtyard figs, or temple vat installations for the thread rite.",
        "विदेश में वट दुर्लभ — गमलों/मंदिर वट प्रतिस्थापन पर धागा रीति।",
        [
            {"region": "North India", "notes": "Often Vat Savitri on Jyeshtha Amavasya."},
            {"region": "Maharashtra & West", "notes": "Vat Purnima emphasis."},
            {"region": "Diaspora", "notes": "Symbolic tree + katha circles."},
        ],
        ["vat-savitri-vrat-katha", "devi-aarti"],
        ["mahalaxmi-kolhapur", "tuljapur-bhavani", "vaishno-devi", "ambaji"],
    ),
]

# Fix relatedDevotion typos / missing slugs patched after vrats exist
# Remove bad temple slug placeholders
for f in NEW_FESTIVALS:
    f["relatedTemples"] = [t for t in f["relatedTemples"] if t not in ("golden-temple-proxy", "pushkar-proxy")]
    if f["slug"] == "vaisakhi":
        f["relatedTemples"] = ["guruvayur", "meenakshi-madurai", "tirumala-venkateswara", "gangotri"]
    if f["slug"] == "kartik-purnima":
        f["relatedTemples"] = ["kashi-vishwanath", "gangotri", "rameswaram", "trimbakeshwar"]
    if f["slug"] == "dhanteras":
        # relatedDevotion had self slug by mistake
        f["relatedDevotion"] = ["lakshmi-aarti", "satyanarayan-vrat-katha", "ganesha-aarti"]
    if f["slug"] == "onam":
        f["relatedDevotion"] = ["vishnu-aarti", "ayyappa-aarti"]
    if f["slug"] == "chhath-puja":
        f["relatedDevotion"] = ["chhath-vrat-katha", "ganga-aarti"]
    if f["slug"] == "ram-navami":
        # fix summaryHi typo maryada
        f["summaryHi"] = "मर्यादा पुरुषोत्तम राम जी का जन्म उत्सव — कथा, व्रत और मंदिर झाँकियाँ।"


NEW_VRATS = [
    vrat(
        "karva-chauth-vrat-katha",
        "devi",
        "Karva Chauth Vrat Katha",
        "करवा चौथ व्रत कथा",
        "Karva Chauth (Kartik Krishna Chaturthi) — after evening puja, before moon arghya",
        "Original TirthaYatra retelling of the popular Karva Chauth vow-story themes for home listening — not a publisher’s copyrighted edition.",
        [
            "॥ श्री गणेशाय नमः ॥\n॥ श्री पार्वत्यै नमः ॥\nकरवा चौथ व्रत कथा — श्रद्धा से सुनें। यह तिर्थयात्रा की मौलिक पुनर्प्रस्तुति है; किसी मुद्रित पुस्तक की प्रतिलिपि नहीं।",
            "कार्तिक कृष्ण चतुर्थी को सुहागिनें सौभाग्य व्रत रखती हैं। दिन भर संयम, सायंकाल गौरी–शिव पूजा, फिर चंद्र दर्शन कर पारण — यही बाह्य विधि है। भीतर की कथा धैर्य और सत्य की है।",
            "एक प्रिय लोककथा में रानी वीरावती की सात भाई थीं। व्रत में तड़प देख उन्होंने पेड़ पर दीपक उठा कर झूठा चंद्र दिखाया। रानी ने अधूरा व्रत तोड़ा; समाचार आया स्वामी संकट में हैं।",
            "जब सच्ची तिथि और पूर्ण श्रद्धा से व्रत दोहराया गया — छलनी से चंद्र देख अर्घ्य दिया — तब संकट टला। कथा सिखाती है: व्रत प्रदर्शन नहीं, अनुशासन है; जल्दबाजी माया है।",
            "दूसरी धारा पार्वती जी की याद कराती है — जिन्होंने कठिन तप से शिव जी को वर रूप पाया। करवा (मटकी) गृह की निरंतरता का चिह्न बनी। सौभाग्य केवल आभूषण नहीं, जिम्मेदारी का नाम है।",
            "व्रत विधि (परिवार रीति से): प्रातः संकल्प, सात्त्विक दिन, सायंकाल पूजा। स्वास्थ्य दुर्बल हो तो चिकित्सक सलाह से फल–जल ग्रहण करें — भाव न टूटे।",
            "पूजा के बाद यह कथा सुनें। चंद्रोदय पर छलनी/आँचल से चंद्र देख जल अर्घ्य दें। स्वामी या परिवार के आशीष संग पारण करें। अकेले व्रत रखने वालों के लिए भी चंद्र साक्षी पर्याप्त है।",
            "फलश्रुति भाव: दीर्घायु की कामना के संग स्वयं में धैर्य, और संबंध में अहिंसक प्रेम बढ़े। जो व्रत डराव नहीं, स्नेह बनाए — वही करवा चौथ की सिद्धि।",
            "॥ जय पार्वती जी ॥ जय शिव जी ॥",
        ],
        "Karva Chauth remembers steadfast marital prayer through stories of Veeravati’s patience and Parvati Ji’s tapasya. Sight the moon, offer arghya, and keep health wiser than harshness.",
        ["vaishno-devi", "mansa-devi-panchkula", "kashi-vishwanath", "mahakaleshwar-ujjain"],
        "करवा चौथ",
    ),
    vrat(
        "chhath-vrat-katha",
        "devi",
        "Chhath Vrat Katha",
        "छठ व्रत कथा",
        "Chhath Puja — especially after Kharna and before Sandhya / Usha arghya",
        "Original TirthaYatra retelling of Chhath’s Surya–Chhathi Maiya vow themes for home and ghat learning.",
        [
            "॥ श्री सूर्याय नमः ॥\n॥ छठी मैया की जय ॥\nछठ व्रत कथा — शुद्ध मन से सुनें। तिर्थयात्रा की मौलिक कथा–पुनर्कथन; कॉपीराइट ग्रंथ की नकल नहीं।",
            "छठ सूर्य और छठी मैया का व्रत है। चार दिन — नहाय खाय, खरना, संध्या अर्घ्य, उषा अर्घ्य — शरीर को प्रकाश के सामने खड़ा करते हैं।",
            "कथा कहते हैं छठी मैया संतान और प्रसव की रक्षिका हैं। सूर्य दृश्य देव हैं — अन्न पकाने वाले, रोग हरने वाले। जो आभार से अर्घ्य देता है, वह लेन–देन नहीं, ऋण–स्वीकार करता है।",
            "महाभारत स्मृति में वनवास की कठिन घड़ी में द्रौपदी–पांडव सूर्य की शरण ले अन्न–शक्ति पाते हैं। राम वंश भी सूर्य का सम्मान करता है। छठ उसी आभार को घाट पर जीवंत करता है।",
            "विधि का हृदय शुद्ध जल है। प्रदूषित नदी में खड़ा होना व्रत का मजाक है — इसलिए घाट सफाई स्वयं धर्म है। ठेकुआ और फल नैवेद्य सात्त्विक रखें।",
            "संध्या को डूबते सूर्य को अर्घ्य; उषा को उगते सूर्य को। बीच का जागरण/उपवास परिवार क्षमता से। महिलाओं–पुरुषों दोनों की परंपरा क्षेत्रों में फल–फूल रही है।",
            "कथा का फल: संतान सुख, रोग शांति, और अहंकार का घटना — क्योंकि सूर्य के सामने राजा और निर्धन एक जैसे खड़े होते हैं।",
            "अर्घ्य के बाद प्रसाद विनम्रता से बाँटें। जो नहीं व्रत रख सके, वे घाट की सेवा–सफाई से पुण्य पा सकते हैं।",
            "॥ जय सूर्य देव ॥ जय छठी मैया ॥",
        ],
        "Chhath thanks Surya and Chhathi Maiya through rigorous purity and standing arghya. Keep the water clean; let gratitude, not transaction, lead the vow.",
        ["gangotri", "jagannath-puri", "ayodhya-ram-mandir", "mahavir-mandir-patna"],
        "छठ",
    ),
    vrat(
        "satyanarayan-vrat-katha",
        "vishnu",
        "Satyanarayan Vrat Katha",
        "सत्यनारायण व्रत कथा",
        "Any auspicious day — especially Purnima; after sankalp and before prasad",
        "Original TirthaYatra condensed retelling of the widely loved Satyanarayan vow themes (truth, promise-keeping, gratitude). Not a verbatim copy of any commercial katha book.",
        [
            "॥ श्री गणेशाय नमः ॥\n॥ श्री सत्यनारायणाय नमः ॥\nसत्यनारायण व्रत कथा — संक्षेप में, घर के लिए। यह मौलिक पुनर्प्रस्तुति है।",
            "भगवान विष्णु सत्यनारायण रूप में सत्य और वचन–पालन के रक्षक हैं। व्रत कोई एक त्योहार नहीं — जब भी गृहस्थ कृतज्ञता या संकट–निवृत्ति चाहे, कथा सुन श्रद्धा जगाता है।",
            "कथा–सूत्र १: एक निर्धन ब्राह्मण ने सत्यनारायण व्रत कर दैन्य पार किया। समृद्धि आने पर यदि अहंकार से कथा/प्रसाद उपेक्षित हो, तो संकट लौटता सिखाया गया — कृपा स्मरण चाहती है।",
            "कथा–सूत्र २: एक व्यापारी/राजा ने संकट में व्रत का संकल्प लिया, कार्य सिद्ध होने पर विलंब किया तो विस्मृति ने नया दुख जन्म दिया। वचन पूरा होते ही शांति आई। शिक्षा: संकल्प को अधूरा न छोड़ो।",
            "कथा–सूत्र ३: गर्वित पात्रों ने प्रसाद अवज्ञा से देखा तो मुखान्धकार/अपमान के रूपक आए; क्षमा और पुनः श्रद्धा से दृष्टि लौटी। सत्यनारायण दर्प नहीं, विनम्र सत्य चाहते हैं।",
            "ये धाराएँ स्कंद/रेवा आदि परंपराओं में विस्तार से गायी जाती हैं। यहाँ भाव केंद्र है — हम किसी एक प्रकाशक की पंक्ति नहीं दोहराते।",
            "व्रत विधि सार: गणेश–गौरी स्मरण, सत्यनारायण कलश/छवि, पंचामृत–फल–मिठाई का भोग, कथा श्रवण, आरती, फिर सबको प्रसाद। झूठ और क्रूर वचन उस दिन विशेष वर्जित भाव से।",
            "फलश्रुति भाव: सत्य में स्थिरता, परिवार में विश्वास, और पूरा किया हुआ वचन — यही लक्ष्मी का द्वार।",
            "॥ जय श्री सत्यनारायण जी ॥",
        ],
        "Satyanarayan puja celebrates Vishnu as guardian of truth and completed vows. Listen with family, share prasad, and let kept promises be the real offering.",
        ["tirumala-venkateswara", "jagannath-puri", "badrinath", "pandharpur-vitthal"],
        "सत्यनारायण",
    ),
    vrat(
        "teej-vrat-katha",
        "devi",
        "Hartalika Teej Vrat Katha",
        "हरतालिका तीज व्रत कथा",
        "Hartalika Teej — during night jagran or before concluding the fast",
        "Original TirthaYatra retelling of Parvati Ji’s Teej tapasya themes for home devotion.",
        [
            "॥ श्री गणेशाय नमः ॥\n॥ श्री पार्वत्यै शिवाय नमः ॥\nहरतालिका तीज कथा — तिर्थयात्रा मौलिक पुनर्प्रस्तुति।",
            "वर्षा ऋतु में धरती हरित होती है — पार्वती जी की लगन का रूपक। हरतालिका तीज पर सुहागिनें और कन्याएँ शिव–पार्वती की कथा गाती हैं।",
            "कथा: पार्वती जी शिव जी को पति रूप में पाना चाहती थीं। जब तप में बाधा आई, वे सखी संग वन चली गईं — ‘हरत’ होकर भी साधना नहीं छोड़ी।",
            "शिव जी ने योगी रूप में परीक्षा ली — वैभव का लोभ, भय, और विरक्ति के तर्क। पार्वती जी अटल रहीं। तब प्रसन्न होकर शिव ने उन्हें अर्धांगिनी स्वीकारा।",
            "तीज सिखाती है: प्रेम जबरदस्ती नहीं, तप और स्पष्ट संकल्प है। हरा वस्त्र, मेहँदी, झूला — बाहरी उत्सव; भीतरी बात अखंड श्रद्धा है।",
            "व्रत: यथाशक्ति निर्जला या फलाहार। रात्रि जागरण में कथा–गीत। प्रातः पूजा कर पारण। स्वास्थ्य की रक्षा भी पार्वती इच्छा है।",
            "॥ जय गौरी शंकर ॥",
        ],
        "Hartalika Teej retells Parvati Ji’s unwavering tapasya for Shiva Ji. Keep the fast wisely and let friendship (aalika) support devotion.",
        ["vaishno-devi", "ambaji", "mahakaleshwar-ujjain", "kashi-vishwanath"],
        "हरतालिका तीज",
    ),
    vrat(
        "vat-savitri-vrat-katha",
        "devi",
        "Vat Savitri Vrat Katha",
        "वट सावित्री व्रत कथा",
        "Vat Savitri / Vat Purnima — after tree worship, before concluding the vow",
        "Original TirthaYatra retelling of the Savitri–Satyavan vow story for home reading.",
        [
            "॥ श्री गणेशाय नमः ॥\nवट सावित्री व्रत कथा — मौलिक कथा–पुनर्कथन।",
            "राजकुमारी सावित्री ने सत्यवान को पति चुना — जानते हुए कि एक वर्ष में उनकी आयु पूर्ण होगी। यह अज्ञान नहीं, साहस था।",
            "निर्धारित दिन सत्यवान वन में मुर्छित हुए। यम जी प्राण लेकर चले। सावित्री पैदल पीछे रहीं — रोष नहीं, धर्म की बातें करते हुए।",
            "यम ने वर दिए: श्वसुर का राज्य और दृष्टि, वंश के पुत्र। सावित्री ने चतुराई से वरों की शृंखला ऐसी माँगी कि सत्यवान के बिना वर पूरे न हों। यम ने प्रसन्न हो प्राण लौटाए।",
            "कथा कहती है — प्रेम जो विवेक संग चले, मृत्यु का भी संवाद सुनता है। वट वृक्ष पर धागा दीर्घ आश्रय का चिह्न है।",
            "व्रत: वट/प्रतीक वृक्ष की परिक्रमा, कथा श्रवण, यथाशक्ति उपवास, परिवार दीर्घायु की प्रार्थना। तिथि क्षेत्रानुसार अमावस्या या पूर्णिमा — पंचांग देखें।",
            "॥ जय सावित्री माँ ॥",
        ],
        "Savitri follows Yama and wins Satyavan through wisdom and loyalty. Tie the banyan thread as a vow to shelter life with courage.",
        ["mahalaxmi-kolhapur", "tuljapur-bhavani", "vaishno-devi", "ambaji"],
        "वट सावित्री",
    ),
    vrat(
        "maha-shivaratri-vrat-katha",
        "shiva",
        "Maha Shivaratri Vrat Katha",
        "महाशिवरात्रि व्रत कथा",
        "Maha Shivaratri night — during jagran, between abhishek and aarti",
        "Original TirthaYatra retelling of major Shivaratri myth themes (Neelkanth, lingodbhava, devotion over sleep).",
        [
            "॥ श्री गणेशाय नमः ॥\n॥ ॐ नमः शिवाय ॥\nमहाशिवरात्रि व्रत कथा — तिर्थयात्रा मौलिक पुनर्प्रस्तुति।",
            "महाशिवरात्रि शिव जी की रात्रि है — जागरण, अभिषेक, बिल्वपत्र और मन को जगाए रखना।",
            "एक कथा नीलकंठ की: क्षीरसागर मंथन से हलाहल उठा। शिव जी ने विष कंठ में धर लोक बचाए। जागरण उसी करुणा का स्मरण है — नींद का त्याग दूसरों की रक्षा हेतु।",
            "दूसरी कथा लिंगोद्भव की: ब्रह्मा–विष्णु ने स्तंभ के आदि–अंत खोजे; अहंकार हारा, शिव अनंत ज्योति रहें। शिवरात्रि अहं की सीमा सिखाती है।",
            "लोक कथा में बहेलिया/शिकारी बिल्व और जल की बूँदें अनजाने अर्पित कर पुण्य पाता है — भाव जाने बिना भी शिव कृपा देखते हैं; जानकर तो और अधिक।",
            "व्रत: दिन संयम, रात्रि चार प्रहर पूजा यथाशक्ति, पंचाक्षर जप, आरती। प्रदोष कथा से जुड़ी नीलकंठ स्मृति यहाँ रात्रि भर फैलती है।",
            "फल: भय शांति, क्रोध शमन, और वह जागरूकता जो घर में करुणा बनाए।",
            "॥ हर हर महादेव ॥",
        ],
        "Maha Shivaratri gathers Neelkanth compassion, lingodbhava humility, and night-long remembrance. Stay awake in kindness; offer bilva and water with a steady mind.",
        ["kashi-vishwanath", "mahakaleshwar-ujjain", "somnath", "trimbakeshwar"],
        "महाशिवरात्रि",
    ),
    vrat(
        "ahoi-ashtami-vrat-katha",
        "devi",
        "Ahoi Ashtami Vrat Katha",
        "अहोई अष्टमी व्रत कथा",
        "Ahoi Ashtami — evening star/puja time as per local custom",
        "Original TirthaYatra retelling of the Ahoi Mata vow themes for children’s protection.",
        [
            "॥ श्री गणेशाय नमः ॥\nअहोई अष्टमी व्रत कथा — मौलिक पुनर्प्रस्तुति।",
            "कार्तिक में अहोई अष्टमी पर माताएँ संतान सुख हेतु व्रत रखती हैं। दीवार पर अहोई चित्र/कलश और सायंकाल तारा/पूजा रीति क्षेत्रानुसार भिन्न।",
            "लोककथा: एक माता ने अनजाने वन्य प्राणी के बच्चों को हानि पहुँचाई; पश्चाताप और अहोई माता की आराधना से संतान रक्षा का मार्ग खुला। शिक्षा — माता का व्रत करुणा से बड़ा है, हिंसा से नहीं।",
            "दूसरा भाव: अहोई पृथ्वी–माता की स्नेह छाया हैं। व्रत में क्रोध–हिंसा छोड़, बच्चों को सत्य और दया सिखाएँ — वही वास्तविक फल।",
            "विधि: यथाशक्ति उपवास, कथा श्रवण, संध्या पूजा, पारण। स्वास्थ्य साथ रखें।",
            "॥ जय अहोई माता ॥",
        ],
        "Ahoi Ashtami is a mother’s vow for children’s wellbeing. Let compassion — not fear — shape the fast and the storytelling.",
        ["mansa-devi-panchkula", "vaishno-devi", "ambaji", "mahalaxmi-kolhapur"],
        "अहोई अष्टमी",
    ),
]


def upsert_festivals(guide: dict) -> int:
    by_slug = {f["slug"]: i for i, f in enumerate(guide["festivals"])}
    added = 0
    for f in NEW_FESTIVALS:
        if f["slug"] in by_slug:
            guide["festivals"][by_slug[f["slug"]]] = f
        else:
            guide["festivals"].append(f)
            added += 1
    # Strengthen existing festival disclaimers via section (already present)
    return added


def upsert_vrats(devotion: dict) -> int:
    items = devotion["items"]
    by_slug = {it["slug"]: i for i, it in enumerate(items)}
    added = 0
    for v in NEW_VRATS:
        if v["slug"] in by_slug:
            # preserve audio if already present
            old = items[by_slug[v["slug"]]]
            for key in ("audioUrl", "audioWatchUrl", "audioLabel"):
                if old.get(key) and not v.get(key):
                    v[key] = old[key]
            items[by_slug[v["slug"]]] = v
        else:
            items.append(v)
            added += 1
    # Update type lede
    vt = devotion.get("types", {}).get("vrat-katha", {})
    vt["lede"] = (
        "Vow-stories for home puja — Karva Chauth, Chhath, Satyanarayan, Teej, Vat Savitri, "
        "Shivaratri, Ekadashi, Pradosh, Navaratri, Janmashtami, Ganesh Chaturthi, Ram Navami, "
        "Hanuman Jayanti, Ayyappa Mandala, and more. TirthaYatra pages use original retellings "
        "of traditional themes for learning; regional wording differs. Not a substitute for your "
        "family priest. Optional YouTube listens belong to their uploaders."
    )
    vt["blurb"] = "Vow-day stories retold for fasting days and home puja — AdSense-safe original summaries of traditional themes."
    devotion["types"]["vrat-katha"] = vt
    sec = devotion.get("section", {})
    sec["disclaimer"] = (
        "Aarti, Chalisa, and Vrat Katha pages are for devotion and cultural learning. "
        "Classical hymns remain with their traditions; TirthaYatra does not claim copyright over "
        "scripture. Many vrat katha pages are original TirthaYatra retellings of popular vow themes — "
        "not verbatim copies of commercial katha books. Audio/video players use public YouTube "
        "recordings when provided; TirthaYatra does not host media files. Confirm ritual timing "
        "with your panchang, family custom, or temple. Not a substitute for a guru or priest."
    )
    devotion["section"] = sec
    return added


def update_calendar(festivals: dict) -> None:
    fixed = festivals["fixed"]
    # Fix Chhath date (was wrongly on Kartik Purnima day) and add missing high-search dates
    def upsert(date, name, name_hi, importance="high"):
        for row in fixed:
            if row["name"] == name and row["date"].startswith(date[:4]):
                row["date"] = date
                row["nameHi"] = name_hi
                row["importance"] = importance
                return
        # also replace exact name any year if updating 2026 specifically
        for row in fixed:
            if row["name"] == name and row["date"].startswith("2026"):
                row["date"] = date
                row["nameHi"] = name_hi
                row["importance"] = importance
                return
        fixed.append({"date": date, "name": name, "nameHi": name_hi, "importance": importance})

    upsert("2026-03-19", "Ugadi", "युगादि", "high")
    upsert("2026-05-16", "Vat Savitri", "वट सावित्री", "high")
    upsert("2026-06-29", "Vat Purnima", "वट पूर्णिमा", "medium")
    upsert("2026-08-31", "Onam", "ओणम", "high")
    upsert("2026-09-13", "Hartalika Teej", "हरतालिका तीज", "high")
    upsert("2026-11-01", "Ahoi Ashtami", "अहोई अष्टमी", "medium")
    upsert("2026-11-06", "Dhanteras", "धनतेरस", "high")
    upsert("2026-11-15", "Chhath Puja", "छठ पूजा", "high")
    upsert("2026-11-24", "Kartik Purnima", "कार्तिक पूर्णिमा", "high")
    # Remove duplicate Chhath on 2026-11-24 if still present alongside Kartik
    festivals["fixed"] = [
        row
        for row in fixed
        if not (row.get("name") == "Chhath Puja" and row.get("date") == "2026-11-24")
    ]
    # Ensure Akshaya Tritiya note stays; optionally align to Apr 21
    for row in festivals["fixed"]:
        if row["name"] == "Akshaya Tritiya" and row["date"].startswith("2026"):
            row["date"] = "2026-04-21"
    festivals["disclaimer"] = festivals.get(
        "disclaimer",
        "Informational calendar only. Regional observance and tithi can differ — confirm with your local panchang or temple.",
    )


def update_engagement(eng: dict) -> None:
    rot = eng.setdefault("dailyRotation", {})
    katha = list(rot.get("katha", []))
    for slug in [
        "satyanarayan-vrat-katha",
        "karva-chauth-vrat-katha",
        "chhath-vrat-katha",
        "maha-shivaratri-vrat-katha",
        "teej-vrat-katha",
        "vat-savitri-vrat-katha",
        "hanuman-jayanti-vrat-katha",
    ]:
        if slug not in katha:
            katha.append(slug)
    rot["katha"] = katha
    presets = eng.setdefault("checklistPresets", {})
    presets.setdefault(
        "karva-chauth",
        {
            "title": "My Karva Chauth home checklist",
            "items": [
                "Sankalp + sattvic day",
                "Evening Gauri–Shiva puja",
                "Listen to Karva Chauth katha",
                "Moon arghya + gentle iftar",
            ],
        },
    )
    presets.setdefault(
        "chhath-puja",
        {
            "title": "My Chhath Puja checklist",
            "items": [
                "Prepare clean naivedya (thekua/fruits)",
                "Keep ghat/kitchen pure",
                "Sandhya arghya",
                "Usha arghya + share prasad",
            ],
        },
    )


def strengthen_festival_section(guide: dict) -> None:
    sec = guide.setdefault("section", {})
    sec["lede"] = (
        "Stories, mythology, dates, and how India and the diaspora celebrate — with related aarti, "
        "vrat katha, and temples. High-search festivals included: Karva Chauth, Chhath, Ram Navami, "
        "Hanuman Jayanti, Onam, Ugadi, Rath Yatra, Dhanteras, Kartik Purnima, Teej, Vat Savitri, and more."
    )
    sec["disclaimer"] = (
        "Exact tithi dates can shift by region and almanac. Confirm with your local temple or panchang "
        "before planning. Festival stories are TirthaYatra retellings of traditional Puranic and folk "
        "themes for learning and home devotion — not verbatim scripture, not affiliated with any temple "
        "trust, and not a substitute for a family priest. Do not republish as official religious edicts."
    )


def wire_existing_guides(guide: dict) -> None:
    """Attach new vrat links onto festivals that already existed."""
    extra = {
        "maha-shivaratri": ["maha-shivaratri-vrat-katha", "pradosh-vrat-katha", "shiva-aarti"],
        "diwali": ["lakshmi-aarti", "satyanarayan-vrat-katha", "ganesha-aarti"],
        "gudi-padwa": ["vishnu-aarti", "satyanarayan-vrat-katha"],
    }
    for f in guide["festivals"]:
        if f["slug"] in extra:
            rel = list(f.get("relatedDevotion") or [])
            for slug in extra[f["slug"]]:
                if slug not in rel:
                    rel.append(slug)
            f["relatedDevotion"] = rel


def main():
    guide = load("festival-guide.json")
    devotion = load("devotion.json")
    festivals = load("festivals.json")
    engagement = load("engagement.json")

    n_f = upsert_festivals(guide)
    strengthen_festival_section(guide)
    wire_existing_guides(guide)
    n_v = upsert_vrats(devotion)
    update_calendar(festivals)
    update_engagement(engagement)

    save("festival-guide.json", guide)
    save("devotion.json", devotion)
    save("festivals.json", festivals)
    save("engagement.json", engagement)

    print(f"Festival guides now: {len(guide['festivals'])} (new inserts ~{n_f})")
    print(f"Vrat kathas: {sum(1 for i in devotion['items'] if i.get('type')=='vrat-katha')} (new inserts ~{n_v})")
    print("Calendar 2026 names:", sorted({r['name'] for r in festivals['fixed'] if r['date'].startswith('2026')}))


if __name__ == "__main__":
    main()
