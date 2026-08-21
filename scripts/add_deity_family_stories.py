#!/usr/bin/env python3
"""Append family-relation kathas (parents, spouse, children, siblings) for Devi-Devata hubs.

Original TirthaYatra retellings — AdSense-safe, not scripture reprints.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORIES_PATH = ROOT / "data" / "stories.json"


def story(
    *,
    slug: str,
    title: str,
    title_hi: str,
    deity: str,
    hook: str,
    hook_hi: str,
    story_en: str,
    story_hi: str,
    detail_en: str,
    detail_hi: str,
    why: str,
    why_hi: str,
    takeaway: str,
    devotion: list[str] | None = None,
    festivals: list[str] | None = None,
    temples: list[str] | None = None,
    tags: list[str] | None = None,
) -> dict:
    return {
        "slug": slug,
        "title": title,
        "titleHi": title_hi,
        "deity": deity,
        "tags": tags
        or ["family", "first-timer", "long-read", "ritual-why"],
        "readSeconds": 400,
        "hook": hook,
        "hookHi": hook_hi,
        "storyEn": story_en,
        "storyHi": story_hi,
        "storyDetailEn": detail_en,
        "storyDetailHi": detail_hi,
        "whyRitual": why,
        "whyRitualHi": why_hi,
        "takeaway": takeaway,
        "relatedDevotion": devotion or [],
        "relatedFestivals": festivals or [],
        "relatedTemples": temples or [],
    }


NEW: list[dict] = [
    # —— Shiva family ——
    story(
        slug="shiva-parvati-divine-wedding",
        title="Shiva and Parvati’s wedding — when tapasya became a household",
        title_hi="शिव–पार्वती विवाह — जब तपस्या ने गृहस्थ रूप लिया",
        deity="shiva",
        hook="The ascetic who wears ash accepted a bride who had won him with patience, not force.",
        hook_hi="भस्मधारी तपस्वी ने वह वधू स्वीकार की जिसने उन्हें बल से नहीं, धैर्य से जीता।",
        story_en=(
            "After Sati’s tragedy, Parvati’s long tapasya in the rains and forests softened Shiva’s "
            "withdrawn grief. Gods arranged a wedding that joined yoga and household — Himavan’s "
            "daughter as bride, Shiva as bridegroom with a wild barat of ganas. The marriage is "
            "not gossip; it is the teaching that love can live beside renunciation. Home shrines "
            "keep the couple together so devotion remembers both stillness and care."
        ),
        story_hi=(
            "सती की त्रासदी के बाद पार्वती की लंबी तपस्या ने शिव के एकांत शोक को कोमल किया। देवों ने "
            "योग और गृहस्थ जोड़ने वाला विवाह रचा — हिमवान-पुत्री वधू, गणों की बारात संग शिव वर। यह "
            "विवाह अफवाह नहीं; शिक्षा है कि प्रेम वैराग्य के साथ रह सकता है। घर की वेदी युगल इसलिए "
            "रखती है कि भक्ति स्थिरता और देखभाल दोनों याद रखे।"
        ),
        detail_en=(
            "First movement: grief that refuses easy replacement. Then the knot: Parvati’s vow "
            "proves steadfastness until the wedding becomes cosmic celebration.\n\n"
            "Sawan Mondays and Maha Shivaratri often honour this household of the divine. Read "
            "alongside Parvati’s tapasya story for her side of the effort.\n\n"
            "Regional wedding details differ; this is an original home retelling."
        ),
        detail_hi=(
            "पहला चरण: वह शोक जो सहज भरपाई नहीं मानता। फिर पार्वती का व्रत अटल सिद्ध होता है।\n\n"
            "सावन सोमवार और महाशिवरात्रि इस दिव्य गृहस्थ को याद करते हैं।"
        ),
        why="Couples often keep Shiva–Parvati together on the altar — a reminder that spiritual life can include marriage vows kept kindly.",
        why_hi="दंपति शिव–पार्वती को एक साथ रखते हैं — याद कि आध्यात्मिक जीवन में कोमल विवाह-वचन भी समा सकते हैं।",
        takeaway="Thank your spouse or a caring elder once today without asking for anything back.",
        devotion=["shiva-aarti", "shiva-chalisa", "sawan-somwar-vrat-katha", "mangala-gauri-vrat-katha"],
        festivals=["maha-shivaratri", "shravan-sawan"],
        temples=["kashi-vishwanath", "meenakshi-madurai", "trimbakeshwar"],
    ),
    story(
        slug="shiva-sons-ganesha-kartikeya",
        title="Ganesha and Kartikeya — Shiva–Parvati’s two sons, two paths",
        title_hi="गणेश और कार्तिकेय — शिव–पार्वती के दो पुत्र, दो मार्ग",
        deity="shiva",
        hook="One circles the parents; one races the world — both remain beloved.",
        hook_hi="एक माता-पिता की परिक्रमा करता, एक जगत् दौड़ता — दोनों प्रिय।",
        story_en=(
            "Popular family tellings place Ganesha and Kartikeya (Murugan/Skanda) as sons of "
            "Shiva and Parvati — different temperaments under one roof. The famous race around "
            "the world ends when Ganesha walks around his parents as the true world. Kartikeya’s "
            "spear guards the outer field; Ganesha guards the doorway of beginnings. Together "
            "they teach that a family can hold more than one kind of excellence."
        ),
        story_hi=(
            "लोककथाएँ गणेश और कार्तिकेय (मुरुगन/स्कंद) को शिव–पार्वती के पुत्र बताती हैं — एक छत "
            "नीचे भिन्न स्वभाव। प्रसिद्ध दौड़ तब खत्म होती है जब गणेश माता-पिता की परिक्रमा को ही "
            "जगत् मानते हैं। कार्तिकेय का वेल बाहरी क्षेत्र रखता, गणेश आरंभ का द्वार। साथ मिलकर "
            "सिखाते हैं — परिवार में एक से अधिक श्रेष्ठता समा सकती है।"
        ),
        detail_en=(
            "First movement: sibling comparison without cruelty. Then the knot: parents who "
            "bless both paths. Household note: do not force one child to copy another’s glory.\n\n"
            "Ganesh Chaturthi and Skanda Shashti honour each brother’s season."
        ),
        detail_hi=(
            "पहला चरण: बिना कटुता की तुलना। फिर माता-पिता दोनों मार्ग आशीर्वाद देते हैं।\n\n"
            "एक संतान को दूसरी की नकल पर मजबूर न करें।"
        ),
        why="When siblings quarrel at festival time, remember both sons received love without needing identical victories.",
        why_hi="त्योहार पर जब भाई-बहन झगड़ें, याद रखें दोनों पुत्रों को प्रेम मिला — एक जैसी जीत की शर्त पर नहीं।",
        takeaway="Praise one strength in a sibling or cousin that is different from yours.",
        devotion=["ganesha-aarti", "shiva-aarti", "murugan-aarti"],
        festivals=["ganesh-chaturthi", "skanda-shashti"],
        temples=["siddhivinayak-mumbai", "palani-murugan", "kashi-vishwanath"],
    ),
    # —— Vishnu / Lakshmi ——
    story(
        slug="vishnu-lakshmi-eternal-pair",
        title="Vishnu and Lakshmi — the eternal pair of care and grace",
        title_hi="विष्णु और लक्ष्मी — रक्षा और कृपा का नित्य युगल",
        deity="vishnu",
        hook="Wherever protection sits, prosperity prefers to sit beside it — if dharma stays awake.",
        hook_hi="जहाँ रक्षा बैठती है, समृद्धि साथ बैठना चाहती है — यदि धर्म जागा हो।",
        story_en=(
            "Lakshmi rising from the ocean chose Vishnu; icons show her at His chest or feet on "
            "Shesha’s rest. The pair is less romance novel, more household theology: care "
            "(Vishnu) and rightful abundance (Lakshmi) belong together. When temples separate "
            "them in processions, devotees still greet both — because a home that only chases "
            "wealth without protection, or only chants without generosity, feels incomplete."
        ),
        story_hi=(
            "सागर से उभरी लक्ष्मी ने विष्णु चुना; मूर्तियाँ उन्हें शेष-शय्या पर वक्ष या चरण पास "
            "दिखाती हैं। यह युगल प्रेम-उपन्यास कम, गृहस्थ धर्म अधिक है: रक्षा (विष्णु) और उचित "
            "समृद्धि (लक्ष्मी) साथ हैं। जब मंदिर यात्रा में अलग हों, भक्त दोनों को प्रणाम करते — "
            "क्योंकि केवल धन दौड़ या केवल जप बिना दान अधूरा लगता है।"
        ),
        detail_en=(
            "First movement: grace chooses righteousness. Then the knot: Kali Yuga noise that "
            "treats Lakshmi as ATM and Vishnu as insurance — reject that thinning.\n\n"
            "Diwali and Varalakshmi vrat keep the pair in seasonal focus."
        ),
        detail_hi=(
            "पहला चरण: कृपा धर्म चुनती है। फिर वह शोर जो लक्ष्मी को मशीन और विष्णु को बीमा बना दे — "
            "अस्वीकार करें।"
        ),
        why="Lighting a Diwali lamp for Lakshmi while keeping a Vishnu photo nearby restates the pair’s teaching.",
        why_hi="दीपावली पर लक्ष्मी के दीप संग विष्णु की तस्वीर पास रखना युगल की शिक्षा दोहराता है।",
        takeaway="Give one small gift or meal to someone before buying something new for yourself.",
        devotion=["vishnu-aarti", "lakshmi-aarti", "diwali-lakshmi-puja-katha"],
        festivals=["diwali", "akshaya-tritiya"],
        temples=["badrinath", "tirumala-venkateswara", "padmanabhaswamy-thiruvananthapuram"],
    ),
    story(
        slug="lakshmi-as-vishnu-consort",
        title="Lakshmi at home with Vishnu — why the Goddess keeps His company",
        title_hi="विष्णु संग लक्ष्मी — देवी उनका साथ क्यों रखती हैं",
        deity="lakshmi",
        hook="She does not chase every loud house — she stays where order and kindness last.",
        hook_hi="वे हर शोरगुल घर में नहीं दौड़तीं — जहाँ व्यवस्था और दया टिके, वहाँ रहती हैं।",
        story_en=(
            "From Lakshmi’s side, partnership with Vishnu means grace prefers steady dharma. "
            "Tales of her leaving prideful courts and returning when humility returns are folk "
            "ways of saying: prosperity is relational. Mahalakshmi temples and home Fridays "
            "invite her as mother and consort — never as a bribe machine. Clean floors and "
            "honest books are her love language."
        ),
        story_hi=(
            "लक्ष्मी की ओर से विष्णु-संग का अर्थ है — कृपा स्थिर धर्म चुनती है। अहंकारी सभा छोड़ने "
            "और नम्रता लौटने पर आने की लोककथाएँ कहती हैं: समृद्धि संबंध है। महालक्ष्मी मंदिर और "
            "शुक्रवार घर उन्हें माँ और संगिनी बुलाते हैं — रिश्वत मशीन नहीं। स्वच्छ फर्श और ईमानदार "
            "हिसाब उनकी प्रेम-भाषा हैं।"
        ),
        detail_en=(
            "First movement: choose where you want grace to feel welcome. Then the knot: "
            "anxiety shopping is not devotion.\n\n"
            "Keep AdSense-safe: no guaranteed riches — only disciplined invitation."
        ),
        detail_hi=(
            "पहला चरण: कृपा को कहाँ स्वागत चाहिए, चुनें। फिर खरीदारी की बेचैनी भक्ति नहीं।"
        ),
        why="Friday Lakshmi worship pairs well with a quick tidy of the prayer corner — hospitality for the consort-Mother.",
        why_hi="शुक्रवार लक्ष्मी पूजा संग पूजा-कोना साफ करना संगिनी-माँ की अतिथि-सेवा है।",
        takeaway="Tidy one shelf or account note today before lighting a lamp.",
        devotion=["lakshmi-aarti", "lakshmi-chalisa", "varalakshmi-vrat-katha"],
        festivals=["diwali", "dhanteras"],
        temples=["mahalaxmi-kolhapur", "mahalaxmi-mumbai"],
    ),
    # —— Krishna family ——
    story(
        slug="krishna-yashoda-mother",
        title="Yashoda and Krishna — the mother who tied the infinite with a rope",
        title_hi="यशोदा और कृष्ण — माँ जिसने अनंत को डोर से बाँधा",
        deity="krishna",
        hook="A butter-thief’s mischief met a mother’s scolding — and both were love.",
        hook_hi="मक्खन-चोर की शरारत माँ की डाँट से मिली — और दोनों प्रेम थे।",
        story_en=(
            "Devaki gave birth; Yashoda raised the child. In Gokul, Yashoda’s damodara-lila — "
            "trying to bind Krishna with rope that always fell short — became the icon of "
            "parental love facing infinity. She is the family heart of Braj: feeding, scolding, "
            "worrying, celebrating. Janmashtami cradles remember her arms as much as Mathura’s "
            "prison night."
        ),
        story_hi=(
            "देवकी ने जन्म दिया; यशोदा ने पाला। गोकुल में दामोदर-लीला — डोर से बाँधना जो बार-बार "
            "कम पड़ती — अनंत के सामने मातृत्व की प्रतिमा बनी। वे ब्रज का परिवार-हृदय हैं: खिलातीं, "
            "डाँटतीं, चिंतित होतीं, जश्न करतीं। जन्माष्टमी का पालना मथुरा की कारागार-रात जितना "
            "उनकी बाँहें भी याद करता है।"
        ),
        detail_en=(
            "First movement: foster love as real love. Then the knot: parents who need control "
            "learn playfulness instead.\n\n"
            "Keep a small rope or cradle symbol only if it helps tenderness — never as superstition theatre."
        ),
        detail_hi=(
            "पहला चरण: पालक प्रेम भी सच्चा प्रेम। फिर नियंत्रण की चाह खेल में बदलती है।"
        ),
        why="Janmashtami midnight aarti often rocks a cradle — invite Yashoda’s patience into your voice at home.",
        why_hi="जन्माष्टमी की अर्धरात्रि आरती पालना झुलाती है — घर की आवाज़ में यशोदा का धैर्य बुलाएँ।",
        takeaway="Speak one gentle sentence to a child or younger person instead of a sharp one.",
        devotion=["krishna-aarti", "krishna-chalisa", "janmashtami-vrat-katha"],
        festivals=["janmashtami", "govardhan-puja"],
        temples=["krishna-janmabhoomi-mathura", "banke-bihari-vrindavan", "guruvayur"],
    ),
    story(
        slug="krishna-balarama-brother",
        title="Balarama and Krishna — the elder brother with the plough",
        title_hi="बलराम और कृष्ण — हलधारी ज्येष्ठ भ्राता",
        deity="krishna",
        hook="Before the flute’s fame, there was an elder’s shoulder beside every adventure.",
        hook_hi="बाँसुरी की प्रसिद्धि से पहले, हर साहस के संग एक बड़े भाई का कंधा था।",
        story_en=(
            "Balarama — fair, plough-bearing, sometimes stern — walks as Krishna’s elder in "
            "many lila tellings: from childhood games to later counsel. He is strength that "
            "does not need the spotlight. Jagannath’s Balabhadra continues that brother-form "
            "in Puri’s wooden siblings. Sibling devotion here means loyalty without envy."
        ),
        story_hi=(
            "बलराम — गौर, हलधर, कभी कठोर — कई लीलाओं में कृष्ण के ज्येष्ठ हैं: बाल-खेल से सलाह "
            "तक। वे वह बल हैं जिसे मंच की जरूरत नहीं। पुरी में बलभद्र उसी भ्रातृ-रूप को दारुमय "
            "रखते हैं। यहाँ भाई-धर्म ईर्ष्या रहित निष्ठा है।"
        ),
        detail_en=(
            "First movement: the quiet power of standing beside. Then the knot: when brothers "
            "disagree, the story still holds affection.\n\n"
            "Rath Yatra’s three siblings make the family public."
        ),
        detail_hi=(
            "पहला चरण: साथ खड़े होने का शांत बल। फिर मतभेद में भी स्नेह टिकता है।"
        ),
        why="Seeing Balabhadra with Jagannath on the rath is a public reminder that brothers can share a path.",
        why_hi="रथ पर जगन्नाथ संग बलभद्र सार्वजनिक याद है — भाई एक पथ बाँट सकते हैं।",
        takeaway="Send a short appreciation message to a sibling or close friend who usually stays in the background.",
        devotion=["krishna-aarti", "vishnu-aarti"],
        festivals=["rath-yatra", "janmashtami"],
        temples=["jagannath-puri", "dwarka", "iskcon-vrindavan"],
    ),
    story(
        slug="krishna-rukmini-wedding",
        title="Rukmini’s letter — how Krishna took a bride by courage and consent",
        title_hi="रुक्मिणी का पत्र — कृष्ण ने साहस और सहमति से वधू कैसे पाई",
        deity="krishna",
        hook="A princess wrote for rescue — and love arrived as dharma on a chariot.",
        hook_hi="राजकुमारी ने रक्षा को पत्र लिखा — प्रेम रथ पर धर्म बनकर आया।",
        story_en=(
            "Rukmini, vowed to Krishna in her heart, sent a message when a forced wedding "
            "threatened. Krishna arrived, respected her choice, and the flight from Vidarbha "
            "became a wedding story of agency — not abduction-for-ego. Dwarka’s queenship "
            "and later Vitthal–Rukmini memory keep this consort bond alive: partnership chosen "
            "with clarity."
        ),
        story_hi=(
            "रुक्मिणी मन से कृष्ण को वरना चाहती थीं; जब जबरदस्ती विवाह सताया, संदेश भेजा। कृष्ण "
            "आए, उनकी इच्छा मानी, विदर्भ से गमन सहमति का विवाह-आख्यान बना — अहंकार-हरण नहीं। "
            "द्वारका की रानी-भाव और विठ्ठल–रुक्मिणी स्मृति यह दांपत्य जिलाए रखती है: स्पष्टता से "
            "चुना संग।"
        ),
        detail_en=(
            "First movement: a woman’s voice as sacred text. Then the knot: families that "
            "trade daughters as prizes fail this story’s test.\n\n"
            "AdSense-safe reading: celebrate consent and courage, not violence fantasy."
        ),
        detail_hi=(
            "पहला चरण: स्त्री की आवाज़ पवित्र पाठ। फिर जो परिवार पुत्री को पुरस्कार बनाएँ, वे इस "
            "कथा की परीक्षा में गिरते हैं।"
        ),
        why="Wedding-season prayers to Krishna–Rukmini can include a vow to respect a partner’s clear yes and no.",
        why_hi="कृष्ण–रुक्मिणी की विवाह-प्रार्थना में साथी के स्पष्ट हाँ-ना का सम्मान जोड़ें।",
        takeaway="Ask one genuine preference of your partner or friend today and honour it.",
        devotion=["krishna-aarti", "krishna-chalisa"],
        festivals=["janmashtami"],
        temples=["dwarka", "pandharpur-vitthal", "vitthal-rukmini-solapur"],
    ),
    # —— Ganesha family ——
    story(
        slug="ganesha-siddhi-buddhi",
        title="Siddhi and Buddhi — Ganesha’s consorts of achievement and wisdom",
        title_hi="सिद्धि और बुद्धि — गणेश की उपलब्धि और ज्ञान संगिनी",
        deity="ganesha",
        hook="Success without wisdom is noise; wisdom without effort is sleep — he keeps both near.",
        hook_hi="बिना बुद्धि की सफलता शोर है; बिना प्रयास की बुद्धि निद्रा — वे दोनों पास रखते हैं।",
        story_en=(
            "Many household icons seat Siddhi and Buddhi beside Ganesha — personifications of "
            "accomplishment and discernment. Whether read as wives in Purana lists or as "
            "qualities made visible, the family lesson is practical: begin work (Ganesha) with "
            "both skill-result and clear mind. Parents praying at Ganesh Chaturthi ask not only "
            "for ‘obstacles removed’ but for children who grow capable and thoughtful."
        ),
        story_hi=(
            "कई घरों की मूर्ति में गणेश संग सिद्धि और बुद्धि विराजती हैं — उपलब्धि और विवेक की "
            "मूर्तियाँ। पुराण-सूची में पत्नियाँ कहें या गुणों का रूप, परिवार-पाठ व्यवहारिक है: काम "
            "(गणेश) परिणाम-कौशल और स्वच्छ बुद्धि दोनों से शुरू हो। गणेश चतुर्थी पर माता-पिता केवल "
            "‘विघ्न हरो’ नहीं, सक्षम और विचारशील संतान माँगते हैं।"
        ),
        detail_en=(
            "First movement: pair results with judgment. Then the knot: hustle culture that "
            "forgets Buddhi.\n\n"
            "Some regions emphasise different consort names; hold the ethic, not the argument."
        ),
        detail_hi=(
            "पहला चरण: परिणाम संग विवेक। फिर वह भागदौड़ जो बुद्धि भुला दे।"
        ),
        why="When you offer modak, silently ask for one wise decision this week — Buddhi beside Siddhi.",
        why_hi="मोदक चढ़ाते समय इस सप्ताह एक विवेकपूर्ण निर्णय माँगें — सिद्धि संग बुद्धि।",
        takeaway="Before a big task, write one wise constraint you will respect (sleep, budget, or honesty).",
        devotion=["ganesha-aarti", "ganesha-chalisa", "ganesh-chaturthi-vrat-katha"],
        festivals=["ganesh-chaturthi"],
        temples=["siddhivinayak-mumbai", "dagdusheth-ganpati-pune"],
    ),
    story(
        slug="ganesha-shubh-labh-children",
        title="Shubh and Labh — the children who remind Ganesha’s household of good gain",
        title_hi="शुभ और लाभ — संतान जो गणेश-घर को अच्छे लाभ की याद दिलाते",
        deity="ganesha",
        hook="Auspiciousness and honest profit sit like children at the Lord’s feet.",
        hook_hi="मांगल्य और ईमानदार लाभ प्रभु के चरण पास बालकों-से बैठते हैं।",
        story_en=(
            "Folk and calendar art often shows Shubh and Labh as Ganesha’s sons — names that "
            "mean auspiciousness and gain. The family picture is a teaching aid for shops and "
            "homes: may earnings arrive with shubh (rightness), not only labh (numbers). Diwali "
            "account books and new ledgers bow here. Keep the ethic gentle — no miracle income "
            "promises, only orderly hope."
        ),
        story_hi=(
            "लोक और पंचांग-चित्र अक्सर शुभ-लाभ को गणेश-पुत्र दिखाते हैं। परिवार-चित्र दुकान-घर की "
            "शिक्षा है: कमाई शुभ (उचित) संग आए, केवल लाभ (अंक) नहीं। दीपावली बही इसी ओर झुकती है। "
            "नीति कोमल रखें — चमत्कारी आय की गारंटी नहीं, व्यवस्थित आशा।"
        ),
        detail_en=(
            "First movement: name your gains ethically. Then the knot: greed dressed as festival.\n\n"
            "AdSense-safe: educational family symbolism only."
        ),
        detail_hi=(
            "पहला चरण: लाभ को नैतिक नाम दें। फिर त्योहार बने लालच — सावधान।"
        ),
        why="Opening a new account book after Diwali can include a bow to Ganesha’s household — shubh before labh.",
        why_hi="दीपावली के बाद नई बही में गणेश-परिवार को प्रणाम — पहले शुभ, फिर लाभ।",
        takeaway="Label one financial goal with a fairness rule you will not break.",
        devotion=["ganesha-aarti", "lakshmi-aarti"],
        festivals=["diwali", "ganesh-chaturthi"],
        temples=["siddhivinayak-mumbai"],
    ),
    # —— Rama family ——
    story(
        slug="rama-lakshmana-brotherhood",
        title="Lakshmana’s vow — the brother who chose exile as love",
        title_hi="लक्ष्मण का संकल्प — भाई जिसने वनवास को प्रेम बनाया",
        deity="rama",
        hook="Not every hero walks alone — some greatness is a younger brother’s sleepless watch.",
        hook_hi="हर नायक अकेला नहीं चलता — कुछ महत्ता छोटे भाई की रात-जागनी है।",
        story_en=(
            "When Rama left for the forest, Lakshmana followed without a throne to gain — only "
            "service. He built huts, guarded nights, and spoke sharp when danger neared Sita. "
            "The brotherhood is the Ramayana’s everyday miracle: loyalty that does not negotiate "
            "comfort first. Sibling bonds at home can borrow this courage without copying epic anger."
        ),
        story_hi=(
            "जब राम वन गए, लक्ष्मण सिंहासन लोभ बिना साथ चले — केवल सेवा। पर्णकुटी रची, रात जागे, "
            "सीता संकट पर कठोर बोले। यह भ्रातृत्व रामायण का रोजमर्रा चमत्कार है: निष्ठा जो पहले "
            "आराम नहीं तौलती। घर के भाई-बहन इस साहस को उधार ले सकते हैं — महाकाव्य क्रोध की नकल बिना।"
        ),
        detail_en=(
            "First movement: choosing presence over privilege. Then the knot: service that "
            "must also rest — even Lakshmana’s story has limits humans should respect.\n\n"
            "Ram Navami families can honour brothers and chosen kin together."
        ),
        detail_hi=(
            "पहला चरण: सुविधा से अधिक उपस्थिति चुनना। फिर सेवा को भी विश्राम चाहिए।"
        ),
        why="Lighting a second lamp for Lakshmana beside Rama on Navami thanks the brotherhood that carried the exile.",
        why_hi="नवमी पर राम संग लक्ष्मण के लिए दूसरा दीप वनवास ढोने वाले भ्रातृत्व का धन्यवाद है।",
        takeaway="Offer practical help to a sibling or friend this week — one task, fully done.",
        devotion=["rama-aarti", "rama-chalisa", "ram-navami-vrat-katha"],
        festivals=["ram-navami", "dussehra"],
        temples=["kanak-bhawan-ayodhya", "ayodhya-ram-mandir", "orchha-ram-raja"],
    ),
    story(
        slug="rama-bharata-paduka",
        title="Bharata and the paduka — ruling as a brother’s trustee",
        title_hi="भरत और पादुका — भाई के न्यासी बनकर राज्य",
        deity="rama",
        hook="He could have taken the crown — he placed sandals on the throne instead.",
        hook_hi="वे मुकुट ले सकते थे — उन्होंने सिंहासन पर पादुका रखीं।",
        story_en=(
            "Bharata returned from his uncle’s home to find Rama exiled by a vow. Refusing to "
            "enjoy a kingdom stained by that sorrow, he installed Rama’s paduka on the throne "
            "and lived as a caretaker at Nandigram. The brotherhood here is justice with "
            "restraint — power held in trust. Families fighting over property can sit with this "
            "story before lawyers harden hearts."
        ),
        story_hi=(
            "भरत मामा घर से लौटे तो राम वनवास में मिले। उस शोक से रंगा राज्य भोगने से इनकार कर "
            "उन्होंने राम की पादुका सिंहासन पर रखीं, नंदीग्राम में न्यासी-से रहे। यहाँ भ्रातृत्व "
            "संयम-युक्त न्याय है — शक्ति विश्वास में। संपत्ति झगड़ते परिवार वकीलों से पहले इस कथा "
            "पास बैठ सकते हैं।"
        ),
        detail_en=(
            "First movement: refuse profit from a sibling’s pain. Then the knot: public duty "
            "without public bitterness.\n\n"
            "Ayodhya memory keeps Bharata beside Rama in the family of dharma."
        ),
        detail_hi=(
            "पहला चरण: भाई के दुःख से लाभ ठुकराना। फिर सार्वजनिक कर्तव्य बिना कटुता।"
        ),
        why="When inheritance talks begin, reading Bharata’s paduka episode once can cool the room.",
        why_hi="जब विरासत की बात चले, भरत-पादुका प्रसंग एक बार पढ़ना कमरा ठंडा कर सकता है।",
        takeaway="In one disagreement this week, ask: am I holding this in trust or in hunger?",
        devotion=["rama-aarti", "rama-chalisa"],
        festivals=["ram-navami", "diwali"],
        temples=["ayodhya-ram-mandir", "kanak-bhawan-ayodhya"],
    ),
    story(
        slug="sita-as-rama-consort",
        title="Sita beside Rama — strength, trial, and dignity of the consort",
        title_hi="राम संग सीता — संगिनी का बल, परीक्षा और गरिमा",
        deity="rama",
        hook="She chose the forest with him — and later chose the earth’s dignity when the world doubted.",
        hook_hi="उन्होंने संग वन चुना — और जब जगत् ने संदेह किया, पृथ्वी की गरिमा चुनी।",
        story_en=(
            "Sita is daughter of Janaka’s field, swayamvara bride, forest companion, captive who "
            "refused compromise, and mother who raised Lava–Kusha in Valmiki’s ashram in later "
            "tellings. As Rama’s consort she is not decoration; she is equal courage under "
            "different tests. Home reading should honour her agency — especially where older "
            "retellings turn harsh. Festival lamps of return still need her name."
        ),
        story_hi=(
            "सीता जनक-क्षेत्र की पुत्री, स्वयंवर वधू, वन-संगिनी, बंदी जिसने समझौता ठुकराया, और "
            "बाद की कथाओं में वाल्मीकि आश्रम में लव–कुश की माँ। राम की संगिनी वे श्रृंगार नहीं; "
            "भिन्न परीक्षाओं में समान साहस हैं। घर के पाठ में उनकी एजेंसी का सम्मान हो — जहाँ पुरानी "
            "कथाएँ कठोर हों। वापसी के दीपों में भी उनका नाम चाहिए।"
        ),
        detail_en=(
            "First movement: companionship as shared vow. Then the knot: public opinion versus "
            "inner truth — handle with care and compassion for readers.\n\n"
            "Companion pages cover swayamvara and earth-return; this page centres the consort bond."
        ),
        detail_hi=(
            "पहला चरण: संग एक साझा व्रत। फिर लोकमत बनाम आंतरिक सत्य — पाठकों के प्रति करुणा रखें।"
        ),
        why="Ram Navami and Vivah Panchami moods can include Sita’s name first in one aarti line — consort as equal presence.",
        why_hi="रामनवमी और विवाह पंचमी भाव में आरती की एक पंक्ति में पहले सीता नाम — संगिनी समान उपस्थिति।",
        takeaway="Speak of a woman in your family with the same respect you give epic heroes.",
        devotion=["rama-aarti", "rama-chalisa"],
        festivals=["ram-navami", "diwali"],
        temples=["kanak-bhawan-ayodhya", "mithila-janakpur", "sitamarhi-janaki"],
    ),
    # —— Hanuman ——
    story(
        slug="hanuman-kesari-anjana-parents",
        title="Kesari and Anjana — Hanuman’s parents in courage and prayer",
        title_hi="केसरी और अंजना — हनुमान के माता-पिता साहस और प्रार्थना में",
        deity="hanuman",
        hook="A vanara chief’s home and a mother’s vow raised the servant of Rama.",
        hook_hi="वानर नायक का घर और माँ का व्रत ने राम-सेवक को पाला।",
        story_en=(
            "Anjana’s penance and Kesari’s household frame Hanuman’s childhood in many tellings, "
            "with Vayu as divine grace in the birth. Parents here model two gifts: spiritual "
            "longing and sturdy belonging. Hanuman Jayanti is incomplete if it only praises leaps "
            "and forgets the home that shaped the leaper. Families can honour coaches and parents "
            "the same day."
        ),
        story_hi=(
            "अंजना की तपस्या और केसरी का गृह कई कथाओं में हनुमान का बचपन घेरते हैं, जन्म में वायु "
            "कृपा संग। माता-पिता दो वर देते: आध्यात्मिक तड़प और ठोस अपनापन। हनुमान जयंती अधूरी "
            "यदि केवल छलांग सराहे और घर भूले। परिवार उसी दिन गुरु-माता-पिता नमन कर सकते हैं।"
        ),
        detail_en=(
            "First movement: credit the roots. Then the knot: fame that orphans itself from gratitude.\n\n"
            "Read with the birth story for the full arc."
        ),
        detail_hi=(
            "पहला चरण: जड़ों का श्रेय। फिर प्रसिद्धि जो कृतज्ञता से कट जाए।"
        ),
        why="On Hanuman Jayanti, offer one pranam mentally to your parents or mentors before the Chalisa.",
        why_hi="हनुमान जयंती पर चालीसा से पहले माता-पिता या गुरु को मानसिक प्रणाम दें।",
        takeaway="Call or message a parent/mentor with one specific thanks.",
        devotion=["hanuman-chalisa", "hanuman-aarti", "hanuman-jayanti-vrat-katha"],
        festivals=["hanuman-jayanti"],
        temples=["hanuman-garhi-ayodhya", "salasar-balaji"],
    ),
    # —— Murugan ——
    story(
        slug="murugan-valli-devasena",
        title="Valli and Devasena — Murugan’s two consorts, two kinds of love",
        title_hi="वल्ली और देवसेना — मुरुगन की दो संगिनियाँ, दो प्रेम",
        deity="murugan",
        hook="One love grew in the millet fields; one arrived as a heavenly alliance — both kept.",
        hook_hi="एक प्रेम कोदो-खेत में बढ़ा; एक दिव्य संधि बनकर आया — दोनों रखे गए।",
        story_en=(
            "Tamil Murugan bhakti holds Devasena (Devayanai) and Valli as consorts — often read "
            "as celestial marriage and earthy courtship. Temples like Tiruttani and Palani keep "
            "their presence in festival drama. The family teaching is spacious: divine life can "
            "honour more than one rightful bond of care without turning love into contest."
        ),
        story_hi=(
            "तमिल मुरुगन भक्ति देवसेना (देवयानी) और वल्ली को संगिनी रखती है — स्वर्गीय विवाह और "
            "धरातली प्रेम-कथा। तिरुत्तनि और पलनी जैसे मंदिर उत्सव में उन्हें जिलाते। परिवार-शिक्षा "
            "विशाल है: दिव्य जीवन एक से अधिक उचित देखभाल-बंधन मान सकता है — प्रेम को होड़ बनाए बिना।"
        ),
        detail_en=(
            "First movement: different temperaments of devotion. Then the knot: modern readers "
            "should avoid weaponising the tale against real marriages.\n\n"
            "Skanda Shashti and Thai Poosam processions may feature the consorts."
        ),
        detail_hi=(
            "पहला चरण: भक्ति के भिन्न स्वभाव। फिर कथा को वास्तविक विवाह के खिलाफ हथियार न बनाएँ।"
        ),
        why="Offering two flowers — one for each consort — can be a simple temple or home gesture of inclusive love.",
        why_hi="दो फूल — प्रत्येक संगिनी हेतु — सरल मंदिर या घर संकेत हो सकता है।",
        takeaway="Appreciate two different kinds of care you receive (practical and emotional).",
        devotion=["murugan-aarti", "murugan-chalisa", "skanda-shashti-vrat-katha"],
        festivals=["skanda-shashti", "thaipusam"],
        temples=["palani-murugan", "tiruttani-murugan", "thiruparankundram-murugan"],
    ),
    story(
        slug="murugan-ganesha-brothers",
        title="Murugan and Ganesha as brothers — rivalry that ends in wisdom",
        title_hi="मुरुगन और गणेश भाई — स्पर्धा जो ज्ञान में खत्म होती",
        deity="murugan",
        hook="The world-race was never only about speed — it was about what you call ‘the world.’",
        hook_hi="जगत्-दौड़ केवल गति की नहीं थी — यह थी कि आप ‘जगत्’ किसे कहें।",
        story_en=(
            "From Murugan’s side, the sibling race with Ganesha stings and then softens: the "
            "younger brother’s clever circumambulation of parents wins the fruit, yet both "
            "remain worshipped. Brother-stories like this let families laugh at competition and "
            "then choose respect. Palani’s young renunciate mood and Ganesha’s doorway mood "
            "can share a home altar without quarrel."
        ),
        story_hi=(
            "मुरुगन की ओर से गणेश संग दौड़ चुभती फिर कोमल होती: छोटे भाई की माता-पिता परिक्रमा फल "
            "जीतती, फिर भी दोनों पूजे जाते। ऐसी भ्रातृ-कथा परिवार को स्पर्धा पर हँसा फिर सम्मान "
            "चुनने देती। पलनी का युवा संन्यास-भाव और गणेश का द्वार-भाव एक वेदी पर बिना झगड़े रह सकते।"
        ),
        detail_en=(
            "First movement: name the hurt of comparison. Then the knot: parents who bless both.\n\n"
            "Pair with the Shiva-family sons page for the parents’ view."
        ),
        detail_hi=(
            "पहला चरण: तुलना का दर्द नाम दें। फिर माता-पिता दोनों को आशीष दें।"
        ),
        why="During Skanda Shashti, a small nod to Ganesha at the door keeps brotherhood intact.",
        why_hi="स्कंद षष्ठी पर द्वार पर गणेश को छोटा प्रणाम भ्रातृत्व बचाए रखता है।",
        takeaway="Let a sibling or colleague win a small credit publicly this week.",
        devotion=["murugan-aarti", "ganesha-aarti"],
        festivals=["skanda-shashti", "ganesh-chaturthi"],
        temples=["palani-murugan", "siddhivinayak-mumbai"],
    ),
    # —— Surya / Shani ——
    story(
        slug="surya-sanjna-chhaya",
        title="Sanjna and Chhaya — Surya’s household of light and shadow",
        title_hi="संज्ञा और छाया — सूर्य का प्रकाश-छाया गृहस्थ",
        deity="surya",
        hook="Even the sun needed a shade — and from that shade a stern teacher was born.",
        hook_hi="सूर्य को भी छाया चाहिए थी — और उसी से कठोर शिक्षक जन्मा।",
        story_en=(
            "Tellings say Sanjna could not bear Surya’s full blaze and arranged Chhaya (shadow) "
            "in her place; from that household strand came children including Shani in popular "
            "lists. The family myth teaches pacing: light without relief burns. Chhath’s patient "
            "standing in water is a public echo — honour the sun, honour your limits."
        ),
        story_hi=(
            "कथा कहती है संज्ञा सूर्य का पूर्ण तेज नहीं सह सकीं, छाया को स्थान दिया; लोकसूची में "
            "उसी गृहस्थ से शनि आदि संतान। परिवार-मिथक लय सिखाता: बिना राहत प्रकाश जलाता है। छठ "
            "का जल में धैर्य सार्वजनिक गूँज है — सूर्य नमन, अपनी सीमा नमन।"
        ),
        detail_en=(
            "First movement: ask for sustainable brightness. Then the knot: do not shame rest.\n\n"
            "Links to Shani’s birth page for the child’s story."
        ),
        detail_hi=(
            "पहला चरण: टिकाऊ प्रकाश माँगें। फिर विश्राम को शर्म न दें।"
        ),
        why="After Surya arghya, sit in shade for a minute — ritual completion, not laziness.",
        why_hi="सूर्य अर्घ्य के बाद एक मिनट छाया में बैठें — अनुष्ठान पूर्णता, आलस्य नहीं।",
        takeaway="Schedule one real break today and keep it as faithfully as a prayer time.",
        devotion=["surya-aarti", "surya-chalisa", "shani-aarti"],
        festivals=["chhath-puja", "makar-sankranti"],
        temples=["konark-sun-temple", "sun-temple-deo", "shani-shingnapur"],
    ),
    story(
        slug="shani-and-surya-father",
        title="Shani and Surya — when a father’s blaze meets a son’s gaze",
        title_hi="शनि और सूर्य — पिता का तेज जब पुत्र की दृष्टि से मिलता",
        deity="shani",
        hook="Family tension can be cosmic — and still teach respect without hatred.",
        hook_hi="पारिवारिक तनाव ब्रह्मांडीय हो सकता है — फिर भी घृणा बिना सम्मान सिखाए।",
        story_en=(
            "Popular katha says infant Shani’s gaze troubled Surya — a stark image of father–son "
            "intensity. Devotees read it as karma’s seriousness, not permission for household "
            "cruelty. Saturday worship that remembers both Surya and Shani can become a practice "
            "of repairing harsh words between generations."
        ),
        story_hi=(
            "लोककथा कहती है शिशु शनि की दृष्टि से सूर्य व्यथित हुए — पिता–पुत्र तीव्रता की तीखी "
            "छवि। भक्त इसे कर्म की गंभीरता पढ़ें, घरेलू क्रूरता की अनुमति नहीं। शनिवार पूजा जो "
            "सूर्य और शनि दोनों याद करे, पीढ़ियों के बीच कठोर शब्दों की मरम्मत बन सकती है।"
        ),
        detail_en=(
            "First movement: intensity needs ethics. Then the knot: astrology fearmongering — reject it.\n\n"
            "AdSense-safe: character lessons only."
        ),
        detail_hi=(
            "पहला चरण: तीव्रता को नीति चाहिए। फिर ज्योतिष भय-व्यापार — अस्वीकार।"
        ),
        why="A Saturday lamp can include forgiveness for one sharp sentence spoken at home this month.",
        why_hi="शनिवार दीप में इस माह घर पर बोले एक तीखे वाक्य की क्षमा जोड़ें।",
        takeaway="Apologise once without defending yourself, if you spoke too harshly.",
        devotion=["shani-aarti", "shani-chalisa", "surya-aarti"],
        festivals=["makar-sankranti"],
        temples=["shani-shingnapur"],
    ),
    # —— Devi forms / Kali / Annapurna / Santoshi ——
    story(
        slug="parvati-as-mother-of-ganesha",
        title="Parvati as mother — the Goddess who made and remade her son",
        title_hi="माँ पार्वती — देवी जिन्होंने पुत्र रचा और संवारा",
        deity="devi",
        hook="Motherhood here is creator, protector, and mourner — then celebrant again.",
        hook_hi="यहाँ मातृत्व रचयिता, रक्षक और शोकसंतप्त है — फिर फिर उत्सवी।",
        story_en=(
            "From the Devi’s side, Ganesha’s shaping, loss, and elephant-headed restoration are "
            "a mother’s ordeal as much as a cosmic puzzle. Parvati’s anger and later joy teach "
            "that divine femininity includes fierce care. Navaratri homes that keep a small "
            "Ganesha near the Mother’s photo quietly admit this family bond."
        ),
        story_hi=(
            "देवी की ओर से गणेश का गढ़ना, हानि और गजमुख पुनरुद्धार माँ की परीक्षा भी है। पार्वती "
            "का रोष और बाद का आनंद सिखाता — दिव्य स्त्रीत्व में प्रचंड देखभाल है। नवरात्रि घर जो "
            "माँ की तस्वीर पास छोटा गणेश रखें, इस परिवार-बंधन को चुपचाप मानते हैं।"
        ),
        detail_en=(
            "First movement: a mother’s right to protect. Then the knot: rage that must return to care.\n\n"
            "Pair with Ganesha birth and elephant-head pages."
        ),
        detail_hi=(
            "पहला चरण: माँ का रक्षा अधिकार। फिर क्रोध जो देखभाल में लौटे।"
        ),
        why="During Navaratri, one evening can be ‘mother and child’ — aarti for Devi and a modak thought for Ganesha.",
        why_hi="नवरात्रि की एक संध्या ‘माँ और बालक’ हो — देवी आरती और गणेश हेतु मोदक-स्मृति।",
        takeaway="Do one protective kindness for a child or student in your circle.",
        devotion=["devi-aarti", "ganesha-aarti", "navaratri-vrat-katha"],
        festivals=["navaratri", "ganesh-chaturthi"],
        temples=["meenakshi-madurai", "vaishno-devi", "siddhivinayak-mumbai"],
    ),
    story(
        slug="kali-shiva-cremation-ground",
        title="Kali and Shiva — the wild consort dance of ego’s end",
        title_hi="काली और शिव — अहंकार-अंत का उग्र दांपत्य नृत्य",
        deity="kali",
        hook="Where polite society looks away, the Mother and the ash-smeared Lord keep company.",
        hook_hi="जहाँ सभ्य समाज मुँह मोड़ता, माँ और भस्मधारी प्रभु संग रहते।",
        story_en=(
            "Iconography of Kali with Shiva underfoot startles; bhakti reads it as ego subdued "
            "and time danced into stillness — a fierce consort theology. The ‘family’ here is "
            "not suburban; it is the truth that love can be terrifyingly honest. Kali Puja nights "
            "and Shiva’s cremation-ground imagery meet in that honesty."
        ),
        story_hi=(
            "शिव को चरण तले दिखाती काली प्रतिमा चौंकाती; भक्ति इसे अहंकार दमन और काल का नृत्य में "
            "स्थिर होना पढ़ती — उग्र दांपत्य। यहाँ ‘परिवार’ उपनगर नहीं; सत्य कि प्रेम डरावनी "
            "ईमानदारी हो सकता। काली पूजा रातें और श्मशान-शिव उसी ईमानदारी में मिलते।"
        ),
        detail_en=(
            "First movement: refuse decorative spirituality. Then the knot: do not romanticise harm.\n\n"
            "AdSense-safe: symbolic reading, no occult shock content."
        ),
        detail_hi=(
            "पहला चरण: सजावटी अध्यात्म ठुकराएँ। फिर हिंसा का रोमांस न करें।"
        ),
        why="A single lamp with both Kali and Shiva names can mark respect for fierce honesty in the heart.",
        why_hi="एक दीप पर काली और शिव दोनों नाम हृदय की उग्र ईमानदारी का सम्मान हो सकता है।",
        takeaway="Drop one polite falsehood you usually tell to look good.",
        devotion=["kali-aarti", "kali-chalisa", "shiva-aarti"],
        festivals=["navaratri", "maha-shivaratri"],
        temples=["kalighat", "dakshineswar-kali", "kashi-vishwanath"],
    ),
    story(
        slug="annapurna-shiva-household",
        title="Annapurna and Shiva — the kitchen that taught the yogi",
        title_hi="अन्नपूर्णा और शिव — रसोई जिसने योगी को सिखाया",
        deity="annapurna",
        hook="Husband and wife here argue about illusion — and dinner becomes philosophy.",
        hook_hi="यहाँ दंपति माया पर बहस करते — और रात्रिभोज दर्शन बन जाता।",
        story_en=(
            "When Shiva called the world’s food maya, Annapurna’s withdrawal and return with a "
            "ladle reframed their household: even yoga needs nourishment, even the Lord accepts "
            "anna from the Mother. Kashi’s Annapurna–Vishwanath neighbourhood keeps that married "
            "theology on the street. Home kitchens become shrines when no grain is insulted."
        ),
        story_hi=(
            "जब शिव ने अन्न को माया कहा, अन्नपूर्णा का हटना और करछुल संग लौटना गृहस्थ को नया अर्थ "
            "दिया: योग को भी पोषण चाहिए, प्रभु भी माँ से अन्न ग्रहण करते। काशी का अन्नपूर्णा–विश्वनाथ "
            "पड़ोस उस दांपत्य को गली में रखता। घर की रसोई तब मंदिर जब कोई कण अपमानित न हो।"
        ),
        detail_en=(
            "First movement: respect the cook. Then the knot: spiritual talk that skips feeding others.\n\n"
            "Pair with Annapurna origin page."
        ),
        detail_hi=(
            "पहला चरण: रसोईए का सम्मान। फिर वह अध्यात्म जो दूसरों को खिलाना छोड़ दे।"
        ),
        why="Cooked prasada offered first to Annapurna–Shiva photos turns dinner into a small wedding of care.",
        why_hi="पका प्रसाद पहले अन्नपूर्णा–शिव तस्वीर को — रात्रिभोज देखभाल का छोटा विवाह।",
        takeaway="Serve someone else first at the next meal you share.",
        devotion=["annapurna-aarti", "shiva-aarti"],
        festivals=["navaratri", "diwali"],
        temples=["annapurna-kashi", "kashi-vishwanath"],
    ),
    story(
        slug="santoshi-ganesha-daughter",
        title="Santoshi Mata and Ganesha’s family — contentment as a daughter’s gift",
        title_hi="संतोषी माता और गणेश-परिवार — संतोष पुत्री-दान सा",
        deity="santoshi",
        hook="Folk love calls her kin to Ganesha — so Friday vows feel like family visits.",
        hook_hi="लोक उन्हें गणेश-परिवार से जोड़ता — तो शुक्रवार व्रत परिवार-भेंट-सा लगता।",
        story_en=(
            "Popular Friday katha often places Santoshi Mata in Ganesha’s household circle — "
            "a daughterly presence of santosh. Whether or not older Puranas list her the same "
            "way, millions practice the bond: simple food, quiet story, refusal of pride. The "
            "family frame helps children understand contentment as a relative you welcome weekly."
        ),
        story_hi=(
            "लोक शुक्रवार कथा अक्सर संतोषी माता को गणेश-गृहस्थ से जोड़ती — संतोष की पुत्री-सी "
            "उपस्थिति। पुराने पुराण एक ही सूची दें या न दें, करोड़ों यह बंधन जीते: सादा भोजन, शांत "
            "कथा, अहंकार भोज से इनकार। परिवार-ढाँचा बच्चों को संतोष सगे रिश्तेदार-सा समझाता जिसे "
            "साप्ताहिक बुलाएँ।"
        ),
        detail_en=(
            "First movement: make virtues feel related. Then the knot: do not sell guaranteed miracles.\n\n"
            "Keep vrat competitive gossip out of the kitchen."
        ),
        detail_hi=(
            "पहला चरण: गुणों को रिश्तेदार-सा बनाएँ। फिर चमत्कार बेचना नहीं।"
        ),
        why="Friday Santoshi worship can include a tiny nod to Ganesha — family continuity of grace.",
        why_hi="शुक्रवार संतोषी पूजा में गणेश को छोटा प्रणाम — कृपा की पारिवारिक निरंतरता।",
        takeaway="Eat one simple meal without complaining or comparing.",
        devotion=["santoshi-chalisa", "santoshi-mata-vrat-katha", "ganesha-aarti"],
        festivals=["santoshi-mata"],
        temples=["santoshi-mata-jodhpur", "santoshi-mata-delhi"],
    ),
    # —— Jagannath / Vitthal / Venkateswara / Narasimha ——
    story(
        slug="jagannath-balabhadra-subhadra",
        title="Jagannath, Balabhadra, Subhadra — the sibling trinity of Puri",
        title_hi="जगन्नाथ, बलभद्र, सुभद्रा — पुरी का भ्रातृ-भगिनी त्रय",
        deity="jagannath",
        hook="Three wooden forms, one rath season — brotherhood and sisterhood on public wheels.",
        hook_hi="तीन दारु रूप, एक रथ मौसम — सार्वजनिक पहियों पर भ्रातृत्व और भगिनी-धर्म।",
        story_en=(
            "Puri’s theology places Jagannath with elder Balabhadra and sister Subhadra — a "
            "sibling set that rides together in Rath Yatra. The family is the point: God among "
            "kin, not a solitary monarch. Devotees jostling on Grand Road practice patience as "
            "sibling duty to strangers."
        ),
        story_hi=(
            "पुरी दर्शन जगन्नाथ को ज्येष्ठ बलभद्र और भगिनी सुभद्रा संग रखता — रथ यात्रा में साथ "
            "सवार भ्रातृ-सेट। परिवार ही मुद्दा: सगे-संग ईश्वर, अकेला सम्राट नहीं। बड़ी सड़क की "
            "भीड़ में भक्त अजनबियों के प्रति धैर्य को भगिनी-भ्रातृ धर्म सा जीते।"
        ),
        detail_en=(
            "First movement: holiness as shared. Then the knot: festival crush without care — avoid harm.\n\n"
            "Companion to origin and neem-murti pages."
        ),
        detail_hi=(
            "पहला चरण: पवित्रता साझा। फिर उत्सव भीड़ में हिंसा न हो।"
        ),
        why="Watching the three chariots is a yearly family portrait of the divine — notice who you pull along in life.",
        why_hi="तीन रथ देखना दिव्य परिवार चित्र है — जीवन में किसे संग खींचते, देखें।",
        takeaway="Include a sister, brother, or cousin in your next temple or prayer plan.",
        devotion=["krishna-aarti", "vishnu-aarti"],
        festivals=["rath-yatra"],
        temples=["jagannath-puri"],
    ),
    story(
        slug="vitthal-rukmini-pandharpur",
        title="Vitthal and Rukmini at Pandharpur — the waiting Lord and His queen",
        title_hi="पंढरपुर में विठ्ठल और रुक्मिणी — प्रतीक्षारत प्रभु और रानी",
        deity="vitthal",
        hook="Hands on hips, brick underfoot — and Rukmini’s shrine completing the household.",
        hook_hi="कमर पर हाथ, पाँव तले ईंट — और रुक्मिणी मंदिर गृहस्थ पूरा करता।",
        story_en=(
            "Vitthal’s brick-waiting for Pundalik pairs with Rukmini’s presence at Pandharpur — "
            "Krishna–Rukmini memory in Maharashtrian form. The family teaching: divine patience "
            "and consort dignity share the same pilgrim town. Abhang singers greet both so love "
            "does not erase duty, and duty does not erase love."
        ),
        story_hi=(
            "पुंडलिक हेतु विठ्ठल की ईंट-प्रतीक्षा पंढरपुर में रुक्मिणी उपस्थिति से जुड़ती — महाराष्ट्रीय "
            "रूप में कृष्ण–रुक्मिणी स्मृति। परिवार-पाठ: दिव्य धैर्य और संगिनी गरिमा एक तीर्थ बाँटते। "
            "अभंग दोनों को नमन करते ताकि प्रेम कर्तव्य न मिटाए, कर्तव्य प्रेम न मिटाए।"
        ),
        detail_en=(
            "First movement: complete the pair in darshan plans. Then the knot: rush that skips Rukmini.\n\n"
            "Pair with Vitthal origin and Krishna–Rukmini wedding pages."
        ),
        detail_hi=(
            "पहला चरण: दर्शन योजना में युगल पूरा करें। फिर जल्दबाजी जो रुक्मिणी छोड़ दे।"
        ),
        why="A Pandharpur vow can include gratitude to Rukmini — the household half of Vitthal’s patience.",
        why_hi="पंढरपुर संकल्प में रुक्मिणी कृतज्ञता जोड़ें — विठ्ठल धैर्य का गृहस्थ अध।",
        takeaway="Thank the person who waits for you patiently at home.",
        devotion=["vitthal-abhang-intro", "krishna-aarti"],
        festivals=["kartik-purnima"],
        temples=["pandharpur-vitthal"],
    ),
    story(
        slug="venkateswara-padmavati-consort",
        title="Padmavati and Venkateswara — the hill wedding that still draws vows",
        title_hi="पद्मावती और वेंकटेश्वर — पहाड़ी विवाह जो आज भी संकल्प खींचता",
        deity="venkateswara",
        hook="A goddess born of lotus met a Lord who borrowed for love — and the hill became home.",
        hook_hi="कमल से जन्मी देवी उस प्रभु से मिलीं जिन्होंने प्रेम हेतु ऋण लिया — पहाड़ी घर बनी।",
        story_en=(
            "From Venkateswara’s shrine outward, Padmavati at Tiruchanur completes the consort "
            "story of Srinivasa’s descent. Pilgrims often visit both — husband and wife of the "
            "hill theology. The family lesson for modern vows: celebrate marriage as shared "
            "responsibility, including debts of care you choose to repay with gratitude, not show."
        ),
        story_hi=(
            "वेंकटेश्वर मंदिर से पद्मावती तिरुचनूर श्रीनिवास अवतरण की संगिनी-कथा पूरी करती। यात्री "
            "अक्सर दोनों जाते — पहाड़ी धर्म का दंपति। आधुनिक संकल्पों हेतु पाठ: विवाह साझा "
            "जिम्मेदारी मनाएँ, देखभाल के ऋण कृतज्ञता से चुकाएँ, दिखावे से नहीं।"
        ),
        detail_en=(
            "First movement: plan darshan as a pair. Then the knot: commercial noise around offerings.\n\n"
            "Official temple guidance rules travel; this is home learning."
        ),
        detail_hi=(
            "पहला चरण: दर्शन युगल योजना। फिर अर्पण का शोर।"
        ),
        why="Couple vows at Tirumala season often name Padmavati — keep one mutual promise small enough to keep.",
        why_hi="तिरुमला मौसम के दंपति संकल्प में पद्मावती नाम — एक आपसी वचन इतना छोटा कि निभे।",
        takeaway="Write one shared household promise and date it.",
        devotion=["venkateswara-aarti", "lakshmi-aarti"],
        festivals=["diwali", "akshaya-tritiya"],
        temples=["tirumala-venkateswara", "padmavathi-tiruchanur"],
    ),
    story(
        slug="narasimha-lakshmi-prahlada",
        title="Lakshmi-Narasimha and Prahlada — fierce form, gentle devotee-son bond",
        title_hi="लक्ष्मी-नरसिंह और प्रह्लाद — उग्र रूप, कोमल भक्त-पुत्र बंधन",
        deity="narasimha",
        hook="After the pillar burst, compassion needed a mother’s calm and a child’s faith.",
        hook_hi="स्तंभ फूटने के बाद करुणा को माँ की शांति और बालक की श्रद्धा चाहिए थी।",
        story_en=(
            "Narasimha’s fury softens in tellings where Lakshmi’s presence or Prahlada’s embrace "
            "returns the Lord to grace. The ‘family’ is devotion itself: a child-like bhakta "
            "held against terror. Temples of Lakshmi-Narasimha keep the consort beside the "
            "man-lion so households remember protection without endless rage."
        ),
        story_hi=(
            "नरसिंह का रोष उन कथाओं में कोमल पड़ता जहाँ लक्ष्मी उपस्थिति या प्रह्लाद आलिंगन प्रभु "
            "को कृपा में लौटाते। ‘परिवार’ स्वयं भक्ति है: आतंक के विरुद्ध बाल-जैसा भक्त। "
            "लक्ष्मी-नरसिंह मंदिर संगिनी को नर-सिंह संग रखते ताकि घर रक्षा को याद रखें — अंतहीन "
            "क्रोध नहीं।"
        ),
        detail_en=(
            "First movement: anger that serves, then stops. Then the knot: celebrating violence.\n\n"
            "Holi’s Prahlada memory belongs here."
        ),
        detail_hi=(
            "पहला चरण: क्रोध सेवा करे, फिर रुके। फिर हिंसा उत्सव न बनें।"
        ),
        why="A Narasimha prayer can end with thanks for calm returning — Lakshmi’s gift after crisis.",
        why_hi="नरसिंह प्रार्थना अंत में शांति लौटने का धन्यवाद — संकट बाद लक्ष्मी का वर।",
        takeaway="After you feel angry, wait one song-length before sending a message.",
        devotion=["vishnu-aarti", "lakshmi-aarti"],
        festivals=["holi"],
        temples=["narasimha-jharni-bidar", "simhachalam", "yadagirigutta"],
    ),
    # —— Brahma / Saraswati / Dattatreya / Bhairav / Ayyappa / Mangal ——
    story(
        slug="brahma-saraswati-knowledge",
        title="Brahma and Saraswati — creation paired with sacred speech",
        title_hi="ब्रह्मा और सरस्वती — सृष्टि संग पवित्र वाणी",
        deity="brahma",
        hook="Making worlds is incomplete if words are careless — so learning sits beside the creator.",
        hook_hi="लोक रचना अधूरी यदि शब्द लापरवाह — इसलिए विद्या स्रष्टा संग बैठती।",
        story_en=(
            "Classical imagery pairs Brahma with Saraswati — veena and book beside the lotus-born "
            "creator. Whatever theological debates exist around the pair, the household ethic is "
            "clear: create carefully, speak carefully. Pushkar’s rare Brahma seat and Saraswati "
            "puja days keep that creative family in mind for students and makers."
        ),
        story_hi=(
            "शास्त्रीय छवि ब्रह्मा संग सरस्वती रखती — कमलज स्रष्टा पास वीणा-पुस्तक। युगल पर "
            "धर्मशास्त्र बहसें जो हों, गृहस्थ नीति स्पष्ट: सावधानी से रचो, सावधानी से बोलो। पुष्कर "
            "का दुर्लभ ब्रह्मा आसन और सरस्वती पूजा दिन विद्यार्थी-रचयिता हेतु वह रचना-परिवार जगाते।"
        ),
        detail_en=(
            "First movement: art and speech as responsibilities. Then the knot: ego of ‘I made this alone.’\n\n"
            "Keep discussion educational and respectful."
        ),
        detail_hi=(
            "पहला चरण: कला और वाणी जिम्मेदारी। फिर ‘मैंने अकेले रचा’ अहंकार।"
        ),
        why="Before a new project, a short Saraswati–Brahma remembrance asks for clean intention.",
        why_hi="नए प्रोजेक्ट से पहले सरस्वती–ब्रह्मा स्मरण स्वच्छ नीयत माँगता।",
        takeaway="Begin work only after one minute of silence to clarify intent.",
        devotion=["saraswati-aarti", "gayatri-aarti", "gayatri-chalisa"],
        festivals=["vasant-panchami", "guru-purnima"],
        temples=["brahma-temple-pushkar", "sringeri-sharada"],
    ),
    story(
        slug="saraswati-and-learning-family",
        title="Saraswati in the student’s family — parents, teachers, and the Goddess",
        title_hi="विद्यार्थी परिवार में सरस्वती — माता-पिता, गुरु और देवी",
        deity="saraswati",
        hook="Books become relatives when a mother-goddess sits among parents and gurus.",
        hook_hi="जब माँ-देवी माता-पिता और गुरु बीच बैठें, पुस्तकें सगे लगते।",
        story_en=(
            "Vasant Panchami scenes show children with parents placing pens at Saraswati’s feet — "
            "a family rite of learning. The Goddess joins the household as the relative who "
            "guards speech and study. Teachers become her hands; parents become her schedule. "
            "Keep ambition kind: marks matter less than truthful effort."
        ),
        story_hi=(
            "वसंत पंचमी दृश्य बच्चों को माता-पिता संग सरस्वती चरण पर कलम रखते दिखाते — विद्या का "
            "परिवार-अनुष्ठान। देवी घर में वाणी-अध्ययन की रक्षिका सगे जैसे जुड़तीं। गुरु उनके हाथ; "
            "माता-पिता उनकी समयसारिणी। महत्वाकांक्षा कोमल रखें: अंक से अधिक सत्य प्रयास।"
        ),
        detail_en=(
            "First movement: learning as shared family vow. Then the knot: pressure that steals joy.\n\n"
            "No miracle exam claims."
        ),
        detail_hi=(
            "पहला चरण: पढ़ाई साझा परिवार व्रत। फिर दबाव जो आनंद चुराए।"
        ),
        why="On Panchami, parents and children can bow together — one flower, one clean page.",
        why_hi="पंचमी पर माता-पिता और बच्चे साथ झुकें — एक फूल, एक स्वच्छ पृष्ठ।",
        takeaway="Study twenty focused minutes, then thank someone who taught you a skill.",
        devotion=["saraswati-aarti", "saraswati-chalisa"],
        festivals=["vasant-panchami"],
        temples=["sringeri-sharada", "sharada-maihar"],
    ),
    story(
        slug="dattatreya-atri-anusuya-parents",
        title="Atri and Anusuya — the parents who received the trinity as a child",
        title_hi="अत्रि और अनुसूया — माता-पिता जिन्होंने त्रिमूर्ति को बालक रूप पाया",
        deity="dattatreya",
        hook="A sage’s home became large enough for Brahma, Vishnu, and Shiva at once.",
        hook_hi="ऋषि का घर इतना विशाल हुआ कि ब्रह्मा, विष्णु, शिव एक साथ समा गए।",
        story_en=(
            "Dattatreya’s birth story is also a parents’ story: Atri’s tapasya and Anusuya’s "
            "tested hospitality. The family ethic is radical welcome grounded in purity of "
            "intent — not naivete. Guru Purnima can thank parents who made room for wisdom "
            "they did not fully understand yet."
        ),
        story_hi=(
            "दत्तात्रेय जन्म माता-पिता की कथा भी: अत्रि तप और अनुसूया की परीक्षित अतिथि-सेवा। "
            "परिवार-नीति है शुद्ध नीयत पर टिका उग्र स्वागत — भोलापन नहीं। गुरु पूर्णिमा उन "
            "माता-पिता का धन्यवाद हो सकती जिन्होंने उस ज्ञान हेतु जगह दी जिसे वे पूरी तरह तब "
            "नहीं समझते थे।"
        ),
        detail_en=(
            "First movement: hospitality as courage. Then the knot: tests that aim to shame — Anusuya transforms them.\n\n"
            "Pair with Dattatreya birth page."
        ),
        detail_hi=(
            "पहला चरण: अतिथि-सत्कार साहस। फिर वह परीक्षा जो शर्म Dilana चाहे — अनुसूया बदल देतीं।"
        ),
        why="Offer one meal to a guest or neighbour as Atri–Anusuya remembrance.",
        why_hi="अतिथि या पड़ोसी को एक भोजन अत्रि–अनुसूया स्मरण के रूप दें।",
        takeaway="Make your home one degree kinder to an unexpected visitor or call.",
        devotion=["vishnu-aarti", "shiva-aarti"],
        festivals=["guru-purnima"],
        temples=["maniknagar-datta", "narsobawadi-datta"],
    ),
    story(
        slug="bhairav-bhairavi-consort",
        title="Bhairav and Bhairavi — guardian partners of the threshold",
        title_hi="भैरव और भैरवी — देहरी के रक्षक युगल",
        deity="bhairav",
        hook="Fierce protection rarely walks alone — wisdom’s fierce form walks beside him.",
        hook_hi="उग्र रक्षा अकेली कम चलती — ज्ञान का उग्र रूप संग चलता।",
        story_en=(
            "Tantric and temple traditions often pair Bhairav with Bhairavi — consort energy of "
            "insight and boundary. For householders, the usable meaning is sober: courage plus "
            "clarity at life’s doors. Skip sensationalism; keep a lamp and a vow of truthful "
            "speech as the couple’s simplest rite."
        ),
        story_hi=(
            "तांत्रिक और मंदिर परंपराएँ भैरव संग भैरवी रखतीं — अंतर्दृष्टि और सीमा की संगिनी ऊर्जा। "
            "गृहस्थ हेतु उपयोगी अर्थ संयत: जीवन द्वार पर साहस प्लस स्पष्टता। सनसनी छोड़ें; दीपक "
            "और सत्य वाणी का वचन युगल का सरल अनुष्ठान।"
        ),
        detail_en=(
            "First movement: pair bravery with wisdom. Then the knot: fear marketing.\n\n"
            "AdSense-safe guardian devotion only."
        ),
        detail_hi=(
            "पहला चरण: साहस संग ज्ञान। फिर भय की बिक्री नहीं।"
        ),
        why="An evening doorway lamp can name both Bhairav and Bhairavi — protection with insight.",
        why_hi="संध्या देहरी दीप पर भैरव और भैरवी दोनों नाम — रक्षा संग अंतर्दृष्टि।",
        takeaway="Check one lock or boundary in your life (password, sleep time, or respectful no).",
        devotion=["bhairav-chalisa", "shiva-aarti"],
        festivals=["maha-shivaratri"],
        temples=["kal-bhairav-ujjain", "kaal-bhairav-kashi"],
    ),
    story(
        slug="ayyappa-foster-father-raja",
        title="Ayyappa and the king who raised him — foster father of Sabarimala’s Lord",
        title_hi="अय्यप्पा और पालक राजा — सबरीमाला स्वामी के पालक पिता",
        deity="ayyappa",
        hook="Hari–Hara’s child still needed a palace childhood and a father’s bewildered love.",
        hook_hi="हरि–हर बालक को भी राजभवन बचपन और पिता का अचंभित प्रेम चाहिए था।",
        story_en=(
            "Kerala tellings give Manikandan to a childless king’s household before the forest "
            "vows of Sabarimala. Foster fatherhood here is sacred: raising a divine child without "
            "fully owning him. Pilgrim fathers today can recognise themselves — love that prepares "
            "a son for a difficult dharma, then lets go."
        ),
        story_hi=(
            "केरल कथा मणिकंदन को निःसंतान राजा के घर देती सबरीमाला व्रत से पहले। पालक पितृत्व "
            "यहाँ पवित्र: दिव्य बालक पालना बिना पूर्ण स्वामित्व। आज के यात्री पिता स्वयं पहचान "
            "सकते — प्रेम जो पुत्र को कठिन धर्म हेतु तैयार करे, फिर छोड़ दे।"
        ),
        detail_en=(
            "First movement: raising without possessing. Then the knot: royal politics around the child.\n\n"
            "Pair with Ayyappa Manikandan origin."
        ),
        detail_hi=(
            "पहला चरण: बिना स्वामित्व पालना। फिर बालक गिर्द राजकारण।"
        ),
        why="Mandala season vows can include gratitude to parents and foster-guardians who shaped your discipline.",
        why_hi="मंडल मौसम संकल्प में माता-पिता और पालक-रक्षकों कृतज्ञता जोड़ें जिन्होंने अनुशासन गढ़ा।",
        takeaway="Thank someone who raised or mentored you without being your only ‘owner’ of success.",
        devotion=["ayyappa-aarti", "ayyappa-chalisa", "ayyappa-mandala-vrat-katha"],
        festivals=["makar-sankranti"],
        temples=["sabarimala"],
    ),
    story(
        slug="mangal-bhumi-family",
        title="Mangal and Mother Earth — courage born close to the ground",
        title_hi="मंगल और भूमि माँ — साहस जो धरती के पास जन्मा",
        deity="mangal",
        hook="A warrior planet’s folk kinship with Bhumi reminds us: bravery needs a home soil.",
        hook_hi="योद्धा ग्रह का भूमि संग लोक-नाता याद दिलाता: साहस को घर की मिट्टी चाहिए।",
        story_en=(
            "Some folk-astral tellings tie Mangal’s spark to earth and divine heat — a family "
            "metaphor of Bhumi and fiery will. Tuesday practices that plant, clean land, or "
            "help farmers honour that kinship better than superstition shopping. Courage without "
            "care for ground becomes mere aggression."
        ),
        story_hi=(
            "कुछ लोक-ज्योतिष मंगल चिंगारी को भूमि और दिव्य ऊष्मा से जोड़ते — भूमि और अग्नि-इच्छा "
            "का परिवार रूपक। मंगलवार जो पेड़ लगाए, भूमि साफ करे, किसान मदद करे, वह अंधविश्वास "
            "खरीद से बेहतर नाता है। बिना भूमि-देखभाल साहस केवल आक्रामकता।"
        ),
        detail_en=(
            "First movement: root bravery in care of place. Then the knot: Mars fear content online.\n\n"
            "AdSense-safe character reading."
        ),
        detail_hi=(
            "पहला चरण: साहस को स्थान-देखभाल में जड़ें। फिर ऑनलाइन मंगल-भय सामग्री नहीं।"
        ),
        why="A Tuesday can include watering a plant as Mangal–Bhumi family remembrance.",
        why_hi="मंगलवार को एक पौधा सींचना मंगल–भूमि परिवार स्मरण हो सकता।",
        takeaway="Do one small act that cares for land, floor, or shared public space.",
        devotion=["mangala-gauri-vrat-katha", "hanuman-chalisa"],
        festivals=["hanuman-jayanti"],
        temples=["mangal-dev-grah-amalner"],
    ),
]


def main() -> None:
    data = json.loads(STORIES_PATH.read_text(encoding="utf-8"))
    existing = {s["slug"] for s in data["stories"]}
    # Fix accidental typos in NEW before write
    for s in NEW:
        if "interTruth" in (s.get("storyDetailHi") or ""):
            s["storyDetailHi"] = s["storyDetailHi"].replace("interTruth", "आंतरिक सत्य")
        # clean takeaway field glitches
        if s["slug"] == "vitthal-rukmini-pandharpur":
            s["whyRitual"] = (
                "A Pandharpur vow can include gratitude to Rukmini — "
                "the household half of Vitthal’s patience."
            )
            s["whyRitualHi"] = (
                "पंढरपुर संकल्प में रुक्मिणी कृतज्ञता जोड़ें — विठ्ठल धैर्य का गृहस्थ अध।"
            )

    added = []
    skipped = []
    for s in NEW:
        if s["slug"] in existing:
            skipped.append(s["slug"])
            continue
        data["stories"].append(s)
        added.append(s["slug"])

    STORIES_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Added {len(added)} family stories:")
    for sl in added:
        print(" ", sl)
    if skipped:
        print("Skipped existing:", skipped)
    print("Total stories now:", len(data["stories"]))


if __name__ == "__main__":
    main()
