#!/usr/bin/env python3
"""Add kathas where a rakshasa/asura gained a boon, then Bhagwan’s avatar/form ended the tyranny.

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
        or [
            "rakshasa",
            "boon-avatar",
            "first-timer",
            "long-read",
            "ritual-why",
            "family",
        ],
        "readSeconds": 420,
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
    story(
        slug="hiranyaksha-boon-varaha",
        title="Hiranyaksha’s boon and Varaha — when the Earth was lifted from the deep",
        title_hi="हिरण्याक्ष का वर और वराह — जब पृथ्वी गहरे से उठवाई गई",
        deity="vishnu",
        hook="A boon made him feel unkillable — until the Lord arrived as a boar no clause had named.",
        hook_hi="वर ने उसे अजेय-सा बनाया — तब तक प्रभु वराह बने जिन्हें किसी शर्त ने नाम नहीं दिया था।",
        story_en=(
            "Hiranyaksha’s austerity won fearsome protection from Brahma. Pride followed: he dragged "
            "the Earth into the cosmic waters and challenged the worlds. Vishnu took the Varaha "
            "avatar — the divine boar — entered the depths, defeated the asura, and raised Bhudevi "
            "on his tusks. The pattern is classic: a boon that seemed airtight met a form the "
            "asura never imagined."
        ),
        story_hi=(
            "हिरण्याक्ष की तपस्या ने ब्रह्मा से भयंकर रक्षा-वर पाया। अहंकार आया: पृथ्वी को "
            "कॉस्मिक जल में घसीटा, लोकों को ललकारा। विष्णु वराह अवतार बने — दिव्य शूकर — गहराई "
            "में गए, असुर हारा, भूमि को दाँतों पर उठाया। क्लासिक क्रम: जो वर अभेद्य लगा, वह रूप "
            "आया जिसकी असुर ने कल्पना नहीं की।"
        ),
        detail_en=(
            "First movement: tapasya that asks for safety becomes a tool of tyranny. Then the "
            "knot: dharma answers through an unexpected avatar.\n\n"
            "Companion to our Varaha-and-Earth page; here the boon’s arrogance is the centre.\n\n"
            "Regional details differ; this is an original home retelling."
        ),
        detail_hi=(
            "पहला चरण: सुरक्षा माँगती तपस्या अत्याचार का औजार बनती। फिर धर्म अप्रत्याशित अवतार से उत्तर देता।\n\n"
            "यह पृष्ठ वर-अहंकार पर केंद्रित है।"
        ),
        why="Varaha Jayanti moods remember that protection of Earth is sacred — keep one small eco-kind act with your prayer.",
        why_hi="वराह जयंती भाव याद दिलाता — पृथ्वी रक्षा पवित्र है; प्रार्थना संग एक छोटा पर्यावरण-उपकार रखें।",
        takeaway="Name one ‘boon’ of power you misuse (anger, status, money) and set a limit today.",
        devotion=["vishnu-aarti", "vishnu-chalisa"],
        festivals=["holi", "kartik-purnima"],
        temples=["tirumala-venkateswara", "badrinath", "ahobilam-narasimha"],
    ),
    story(
        slug="tarakasura-skanda-vadha",
        title="Tarakasura’s boon and Skanda — the war-god who closed the loophole",
        title_hi="तारकासुर का वर और स्कंद — योद्धा-देव जिसने छिद्र बंद किया",
        deity="murugan",
        hook="Only Shiva’s son could end him — so the universe waited for Skanda’s spear.",
        hook_hi="केवल शिव-पुत्र उसे समाप्त कर सकता था — जगत् स्कंद के वेल की प्रतीक्षा करता रहा।",
        story_en=(
            "Tarakasura gained a boon that he could be killed only by a son of Shiva — then "
            "terrorised the gods who waited for that birth. When Skanda / Kartikeya / Murugan "
            "rose as commander, the spear of Vel ended the asura’s claim. The story teaches that "
            "boons can delay justice; they cannot cancel it forever."
        ),
        story_hi=(
            "तारकासुर ने वर पाया कि केवल शिव-पुत्र उसे मार सके — फिर देवों को त्रस्त किया जो "
            "जन्म की प्रतीक्षा करते। जब स्कंद / कार्तिकेय / मुरुगन सेनापति उठे, वेल ने असुर का "
            "दावा समाप्त किया। कथा सिखाती: वर न्याय टाल सकते हैं; हमेशा रद्द नहीं कर सकते।"
        ),
        detail_en=(
            "First movement: a clever condition that looks like immortality. Then the knot: "
            "divine preparation through the child’s birth and training.\n\n"
            "Skanda Shashti retells this victory in many Tamil homes."
        ),
        detail_hi=(
            "पहला चरण: चतुर शर्त जो अमरता-सी लगे। फिर दिव्य तैयारी — बालक जन्म और प्रशिक्षण।\n\n"
            "स्कंद षष्ठी कई घरों में यह विजय दोहराती है।"
        ),
        why="Skanda Shashti remembers Taraka’s end — keep one vow of courage without cruelty.",
        why_hi="स्कंद षष्ठी तारक-अंत याद करती — बिना क्रूरता के साहस का एक व्रत रखें।",
        takeaway="Finish one hard duty you postponed because ‘conditions weren’t perfect.’",
        devotion=["murugan-aarti", "murugan-chalisa", "skanda-shashti-vrat-katha"],
        festivals=["skanda-shashti", "thaipusam"],
        temples=["palani-murugan", "thiruchendur-murugan", "swamimalai-murugan"],
    ),
    story(
        slug="bhasmasura-mohini",
        title="Bhasmasura’s boon and Mohini — when Shiva’s gift met Vishnu’s dance",
        title_hi="भस्मासुर का वर और मोहिनी — जब शिव-वर विष्णु-नृत्य से मिला",
        deity="vishnu",
        hook="He could turn anyone to ash with a touch — until he touched his own head.",
        hook_hi="स्पर्श से राख बना सकता था — तब तक जब तक अपने ही सिर को छुआ।",
        story_en=(
            "Bhasmasura pleased Shiva and won a terrible boon: whatever head he touched would "
            "burn to ash. He then chased even the giver. Vishnu as Mohini drew him into a "
            "dance-like mimicry until the asura placed his hand on his own head and ended "
            "himself. A boon without wisdom becomes a trap."
        ),
        story_hi=(
            "भस्मासुर ने शिव को प्रसन्न कर भयंकर वर पाया: जिस सिर को छुए, भस्म। फिर दाता को भी "
            "खदेड़ा। विष्णु मोहिनी रूप में नृत्य-अनुकरण में उलझाए — असुर ने अपना सिर छुआ और "
            "स्वयं समाप्त हुआ। बिना विवेक का वर फंदा बनता है।"
        ),
        detail_en=(
            "First movement: asking for power without asking for character. Then the knot: "
            "Hari–Hara cooperation in protecting the worlds.\n\n"
            "Keep the telling light and ethical — no cruelty-as-entertainment."
        ),
        detail_hi=(
            "पहला चरण: चरित्र बिना शक्ति माँगना। फिर हरि–हर सहयोग।\n\n"
            "कथा को हलका और नैतिक रखें।"
        ),
        why="A Vishnu or Shiva aarti can include a quiet line: ‘Let my strengths not burn my own house.’",
        why_hi="विष्णु या शिव आरती में शांत पंक्ति जोड़ें: ‘मेरा बल मेरे घर को न जलाए।’",
        takeaway="Drop one habit that ‘empowers’ you but harms people close to you.",
        devotion=["vishnu-aarti", "shiva-aarti", "vishnu-chalisa"],
        festivals=["maha-shivaratri", "holi"],
        temples=["rameswaram", "kashi-vishwanath", "padmanabhaswamy-thiruvananthapuram"],
    ),
    story(
        slug="madhu-kaitabha-vadha",
        title="Madhu and Kaitabha — twin asuras who rose from Vishnu’s sleep",
        title_hi="मधु और कैटभ — जुड़वाँ असुर जो विष्णु की निद्रा से उठे",
        deity="vishnu",
        hook="They stole the Vedas and mocked creation — until the Lord woke to restore order.",
        hook_hi="उन्होंने वेद चुराए, सृष्टि पर हँसे — तब तक प्रभु जागे और क्रम लौटाया।",
        story_en=(
            "From the ear-wax or sleep-energy of resting Vishnu, tellings say, Madhu and Kaitabha "
            "appeared, seized the Vedas, and threatened Brahma’s work. Vishnu awoke, battled, and "
            "through boon-cleverness and strength ended them — restoring sacred knowledge. The "
            "lesson: chaos can sprout even beside divinity; awakening answers it."
        ),
        story_hi=(
            "विश्राम करते विष्णु की निद्रा-ऊर्जा से, कथा कहती, मधु-कैटभ प्रकट हुए, वेद हर लिए, "
            "ब्रह्मा के कार्य को धमकाया। विष्णु जागे, युद्ध किया, वर-चतुराई और बल से अंत किया — "
            "ज्ञान लौटाया। शिक्षा: अराजकता दिव्यता पास भी उग सकती; जागरण उत्तर है।"
        ),
        detail_en=(
            "First movement: theft of knowledge as cosmic crime. Then the knot: Devi/Vishnu "
            "variants exist — hold the ethic of restored order.\n\n"
            "Home learning only; not a ritual prescription."
        ),
        detail_hi=(
            "पहला चरण: ज्ञान-हरण ब्रह्मांडीय अपराध। फिर देवी/विष्णु भेद — क्रम-बहाली की नीति रखें।"
        ),
        why="Before study, a short Vishnu remembrance can mean: return stolen focus to the book.",
        why_hi="पढ़ाई से पहले छोटी विष्णु स्मृति: चुराया ध्यान पुस्तक को लौटाएँ।",
        takeaway="Give twenty undistracted minutes to learning or prayer without your phone.",
        devotion=["vishnu-aarti", "vishnu-chalisa", "saraswati-aarti"],
        festivals=["vasant-panchami", "kartik-purnima"],
        temples=["badrinath", "srirangam-ranganathaswamy"],
    ),
    story(
        slug="andhakasura-shiva-vadha",
        title="Andhaka’s boon and Shiva — blindness, blood, and the end of envy",
        title_hi="अन्धक का वर और शिव — अंधकार, रक्त और ईर्ष्या का अंत",
        deity="shiva",
        hook="Born of darkness and pride, he sought what was never his — until Rudra’s justice closed in.",
        hook_hi="अंधकार और अहंकार से जन्मा, जो उसका नहीं था चाहा — रुद्र न्याय ने घेरा।",
        story_en=(
            "Andhaka, linked in tellings to Shiva’s own fierce play and later asura pride, gained "
            "strength through tapasya and boons, then desired Parvati and warred against the gods. "
            "Shiva’s battle ended the asura’s claim. Read ethically: envy dressed as devotion is "
            "still envy — and boons do not bless stolen love."
        ),
        story_hi=(
            "अन्धक, कथाओं में शिव के उग्र लीला-प्रसंग और बाद असुर-अहंकार से जुड़ा, तप-वर से बल "
            "पाकर पार्वती को चाहा, देवों से युद्ध किया। शिव-युद्ध ने दावा समाप्त किया। नैतिक पाठ: "
            "भक्ति वेष में ईर्ष्या फिर भी ईर्ष्या — वर चोरी प्रेम को आशीष नहीं।"
        ),
        detail_en=(
            "First movement: desire without reverence. Then the knot: fierce grace that protects "
            "the household of the divine.\n\n"
            "Keep AdSense-safe tone — no gore focus; character lesson first."
        ),
        detail_hi=(
            "पहला चरण: बिना श्रद्धा की चाह। फिर उग्र कृपा जो दिव्य गृहस्थ रक्षा करे।\n\n"
            "कथा चरित्र-शिक्षा प्रधान रखें।"
        ),
        why="Maha Shivaratri can include a vow against coveting another’s peace or partner.",
        why_hi="महाशिवरात्रि में दूसरों की शांति या साथी पर लालच के विरुद्ध व्रत जोड़ें।",
        takeaway="Congratulate someone today for a blessing you wished you had.",
        devotion=["shiva-aarti", "shiva-chalisa", "lingashtakam"],
        festivals=["maha-shivaratri"],
        temples=["mahakaleshwar-ujjain", "kashi-vishwanath", "trimbakeshwar"],
    ),
    story(
        slug="tripurasura-shiva-dahana",
        title="Tripura’s three cities and Shiva’s arrow — when boon-fortresses fell",
        title_hi="त्रिपुरा के तीन नगर और शिव-बाण — जब वर-दुर्ग गिरे",
        deity="shiva",
        hook="Three flying cities aligned for a moment — and one arrow of dharma was enough.",
        hook_hi="तीन उड़ते नगर एक क्षण में जुटे — धर्म का एक बाण काफी था।",
        story_en=(
            "The Tripura asuras won boons and built three nearly invincible cities. When those "
            "cities briefly aligned, Shiva as Tripurantaka released a single cosmic arrow and "
            "burned the fortresses of arrogance. Architecture of ego meets timing of grace."
        ),
        story_hi=(
            "त्रिपुरा असुरों ने वर पाकर तीन लगभग अजेय नगर बनाए। जब वे क्षणिक संरेखित हुए, शिव "
            "त्रिपुरान्तक ने एक ब्रह्मांडीय बाण चलाया — अहंकार के दुर्ग जले। अहंकार की वास्तुकला "
            "कृपा की समय-संगति से मिलती है।"
        ),
        detail_en=(
            "First movement: collective asura power behind ‘perfect’ defence. Then the knot: "
            "one right moment undoes years of pride.\n\n"
            "Chidambaram and other Shaiva centres keep Tripurantaka memory in iconography."
        ),
        detail_hi=(
            "पहला चरण: ‘पूर्ण’ रक्षा पीछे सामूहिक असुर बल। फिर एक सही क्षण वर्षों का अहंकार तोड़ता।"
        ),
        why="A Monday Shiva prayer can ask to burn one inner fortress — a grudge you keep flying.",
        why_hi="सोमवार शिव प्रार्थना में एक भीतरी दुर्ग जलाने को कहें — वह शिकायत जो उड़ाए रखते।",
        takeaway="Release one old argument you keep replaying in your head.",
        devotion=["shiva-aarti", "shiva-chalisa"],
        festivals=["maha-shivaratri"],
        temples=["nataraja-chidambaram", "kashi-vishwanath", "rameswaram"],
    ),
    story(
        slug="shumbha-nishumbha-devi-vadha",
        title="Shumbha and Nishumbha — the brother-asuras Durga brought down",
        title_hi="शुंभ-निशुंभ — भाई-असुर जिन्हें दुर्गा ने गिराया",
        deity="devi",
        hook="They wanted the Goddess as prize of war — she answered as warrior, not trophy.",
        hook_hi="उन्होंने देवी को युद्ध-पुरस्कार चाहा — वे योद्धा बनीं, ट्राफी नहीं।",
        story_en=(
            "Shumbha and Nishumbha, strengthened by tapasya and boons, sent armies and demands "
            "for Devi herself. Durga’s battle — with forms like Kali and Chamunda in the wider "
            "telling — ended the brothers’ tyranny. A boon cannot turn the Mother into property."
        ),
        story_hi=(
            "शुंभ-निशुंभ तप-वर से बल पाकर सेना और स्वयं देवी की माँग भेजी। दुर्गा-युद्ध — विस्तृत "
            "कथा में काली-चामुंडा रूप संग — भाई-अत्याचार का अंत। वर माँ को संपत्ति नहीं बना सकता।"
        ),
        detail_en=(
            "First movement: objectifying the sacred. Then the knot: Shakti who fights for dignity.\n\n"
            "Navaratri nights often include this arc after Mahisha."
        ),
        detail_hi=(
            "पहला चरण: पवित्र को वस्तु बनाना। फिर गरिमा हेतु लड़ती शक्ति।\n\n"
            "नवरात्रि में महिष के बाद यह प्रसंग आता।"
        ),
        why="Navaratri can include respect for women’s dignity as part of Devi worship — not only lamps.",
        why_hi="नवरात्रि में देवी पूजा संग स्त्री गरिमा सम्मान — केवल दीप नहीं।",
        takeaway="Speak one sentence today that defends someone’s dignity without shaming anyone.",
        devotion=["devi-aarti", "durga-chalisa", "navaratri-vrat-katha", "kali-aarti"],
        festivals=["navaratri", "dussehra"],
        temples=["vaishno-devi", "meenakshi-madurai", "kalighat"],
    ),
    story(
        slug="gajasura-shiva-vadha",
        title="Gajasura’s boon and Shiva — the elephant-demon who met Rudra",
        title_hi="गजासुर का वर और शिव — गज-असुर जो रुद्र से मिला",
        deity="shiva",
        hook="An elephant-form terror won divine favour — then lost it to arrogance against Shiva.",
        hook_hi="गज-रूप आतंक ने दिव्य कृपा पाई — फिर शिव के विरुद्ध अहंकार में खोई।",
        story_en=(
            "Gajasura’s tapasya brought a boon and elephantine might; pride turned him against "
            "the gods and toward Shiva. Rudra’s victory ends the asura — and some tellings link "
            "related motifs to fierce Shaiva icons. Power granted for sadhana must not become "
            "a stampede on dharma."
        ),
        story_hi=(
            "गजासुर की तपस्या ने वर और गज-बल दिया; अहंकार ने देवों और शिव की ओर मोड़ा। रुद्र "
            "विजय असुरांत — कुछ कथाएँ उग्र शैव प्रतिमाओं से जोड़तीं। साधना हेतु मिला बल धर्म पर "
            "भगदड़ नहीं बनना चाहिए।"
        ),
        detail_en=(
            "First movement: form and force mistaken for final truth. Then the knot: Shiva who "
            "stills chaos.\n\n"
            "Pair gently with Ganesha lore without confusing the two."
        ),
        detail_hi=(
            "पहला चरण: रूप-बल को अंतिम सत्य समझना। फिर शिव जो अराजकता थामते।\n\n"
            "गणेश कथा से भ्रमित न करें।"
        ),
        why="Shiva abhishek can include a prayer to keep strength gentle inside the home.",
        why_hi="शिव अभिषेक में प्रार्थना: घर के भीतर बल कोमल रहे।",
        takeaway="Use physical strength or loud voice once today only to help, not to dominate.",
        devotion=["shiva-aarti", "shiva-chalisa"],
        festivals=["maha-shivaratri", "shravan-sawan"],
        temples=["kashi-vishwanath", "mahakaleshwar-ujjain"],
    ),
    story(
        slug="kamsa-vadha-krishna",
        title="Kamsa’s end — the tyrant uncle who fell to the eighth child",
        title_hi="कंस वध — अत्याचारी मामा जो आठवें शिशु से गिरा",
        deity="krishna",
        hook="A prophecy was his prison — cruelty was his choice — Krishna was the answer.",
        hook_hi="भविष्यवाणी उसका कारागार — क्रूरता उसका चुनाव — कृष्ण उत्तर थे।",
        story_en=(
            "Kamsa, warned that Devaki’s eighth child would end him, chose murder and chains "
            "instead of change. After childhood lilas, Krishna returned to Mathura, refused the "
            "tyrant’s stage, and ended Kamsa’s rule. Not every villain needs a Brahma-boon; some "
            "need only fear and power. The avatar still arrives for the oppressed."
        ),
        story_hi=(
            "कंस, देवकी के आठवें शिशु से अंत की चेतावनी पाकर, बदलाव के बजाय हत्या और बेड़ियाँ "
            "चुनी। बाल-लीला बाद कृष्ण मथुरा लौटे, अत्याचारी मंच ठुकराया, कंस-राज्य समाप्त किया। "
            "हर खलनायक को ब्रह्मा-वर नहीं; कुछ को भय और सत्ता काफी। अवतार फिर भी पीड़ितों हेतु आता।"
        ),
        detail_en=(
            "First movement: trying to outrun destiny by harming kin. Then the knot: public "
            "justice in the wrestling arena of Mathura.\n\n"
            "Read with Krishna’s birth-night story for the full arc."
        ),
        detail_hi=(
            "पहला चरण: सगे हानि से भाग्य से भागना। फिर मथुरा अखाड़े का सार्वजनिक न्याय।"
        ),
        why="Janmashtami joy includes remembering Mathura’s liberation — celebrate without mocking anyone’s fear.",
        why_hi="जन्माष्टमी आनंद में मथुरा मुक्ति याद — किसी के भय का मजाक न उड़ाएँ।",
        takeaway="Stop one controlling behaviour you justify as ‘protecting the family.’",
        devotion=["krishna-aarti", "krishna-chalisa", "janmashtami-vrat-katha"],
        festivals=["janmashtami", "holi"],
        temples=["krishna-janmabhoomi-mathura", "dwarkadhish-mathura", "guruvayur"],
    ),
    story(
        slug="bakasura-krishna-vadha",
        title="Bakasura — the crane-demon Krishna tore open",
        title_hi="बकासुर — बगुला-असुर जिसे कृष्ण ने चीर दिया",
        deity="krishna",
        hook="A giant crane swallowed the cowherd boys — then met a child who was not prey.",
        hook_hi="विशाल बगुले ने ग्वाल बालक निगले — फिर ऐसे शिशु से मिला जो शिकार नहीं था।",
        story_en=(
            "Bakasura, a crane-formed asura serving Kamsa’s fear, swallowed Krishna and the "
            "boys. The child expanded, burned the demon’s throat, and split the beak of tyranny. "
            "Boon or order from a tyrant — the avatar protects play and pasture alike."
        ),
        story_hi=(
            "बकासुर, कंस-भय का बगुला-असुर, कृष्ण और बालकों को निगल गया। शिशु ने विस्तार किया, "
            "कंठ जलाया, अत्याचार चोंच चीर दी। वर हो या अत्याचारी आदेश — अवतार खेल और चरनी दोनों "
            "रक्षा करता।"
        ),
        detail_en=(
            "First movement: childhood threatened by monstrous appetite. Then the knot: "
            "effortless divinity inside a child’s body.\n\n"
            "Keep tone suitable for family reading."
        ),
        detail_hi=(
            "पहला चरण: राक्षसी भूख से खतरे में बचपन। फिर बाल-देह में सहज दिव्यता।\n\n"
            "परिवार-पाठ हेतु स्वर रखें।"
        ),
        why="A Janmashtami cradle song can thank the Lord who kept Braj’s children safe in the stories.",
        why_hi="जन्माष्टमी लोरी में प्रभु धन्यवाद जिन्होंने कथा में ब्रज बालक बचाए।",
        takeaway="Protect one quiet hour of children’s play or rest from adult stress today.",
        devotion=["krishna-aarti", "krishna-chalisa"],
        festivals=["janmashtami"],
        temples=["banke-bihari-vrindavan", "iskcon-vrindavan", "krishna-janmabhoomi-mathura"],
    ),
    story(
        slug="aghasura-krishna-vadha",
        title="Aghasura — the serpent who became a cave of death",
        title_hi="अघासुर — सर्प जो मृत्यु की गुफा बना",
        deity="krishna",
        hook="Friends walked into a smiling mouth of a snake — Krishna walked out with them alive.",
        hook_hi="मित्र सर्प के मुस्कान-मुख में चले — कृष्ण उन्हें जीवित निकाल लाए।",
        story_en=(
            "Aghasura stretched as a huge serpent-cave to swallow Braj’s boys at Kamsa’s will. "
            "Krishna entered, expanded, and ended the asura — freeing breath and friendship. "
            "Evil that disguises itself as a path still meets the avatar’s truth."
        ),
        story_hi=(
            "अघासुर विशाल सर्प-गुफा बन कंस-इच्छा से ब्रज बालक निगलने बढ़ा। कृष्ण घुसे, फैले, "
            "असुरांत — श्वास और मित्रता मुक्त। बुराई जो पथ बनकर छिपे, अवतार सत्य से मिलती।"
        ),
        detail_en=(
            "First movement: trust exploited by disguise. Then the knot: the Lord who risks entry to save.\n\n"
            "Family-safe wording; focus on rescue."
        ),
        detail_hi=(
            "पहला चरण: भेष से तोड़ा विश्वास। फिर प्रभु जो बचाने भीतर जाते।\n\n"
            "परिवार-सुरक्षित शब्द; रक्षा पर बल।"
        ),
        why="Thank friendship in your Krishna prayer — Aghasura stories are also about the boys walking together.",
        why_hi="कृष्ण प्रार्थना में मित्रता धन्यवाद — अघासुर कथा साथ चलते बालकों की भी है।",
        takeaway="Check on a friend who might be walking into a bad situation alone.",
        devotion=["krishna-aarti", "krishna-chalisa"],
        festivals=["janmashtami"],
        temples=["iskcon-vrindavan", "banke-bihari-vrindavan"],
    ),
    story(
        slug="keshi-vadha-krishna",
        title="Keshi — the horse-demon Krishna slew for Braj",
        title_hi="केशी वध — अश्व-असुर जिसे कृष्ण ने ब्रज हेतु मारा",
        deity="krishna",
        hook="A demonic horse charged the pastures — the flute-bearer became a warrior for a moment.",
        hook_hi="राक्षसी अश्व चरनी पर टूटा — बाँसुरीधारी क्षण भर योद्धा बने।",
        story_en=(
            "Keshi, a horse-asura sent in Kamsa’s campaign, attacked the cowherd world. Krishna "
            "met the charge and ended the demon — one of the lilas that earn him the name "
            "Keshava in popular memory. Tyranny outsources violence; the avatar answers in person."
        ),
        story_hi=(
            "केशी, कंस अभियान का अश्व-असुर, गोप-जगत् पर टूटा। कृष्ण ने मुकाबला कर असुरांत — "
            "लीला जिससे लोक में केशव नाम जुड़ता। अत्याचार हिंसा ठेके पर देता; अवतार स्वयं उत्तर देते।"
        ),
        detail_en=(
            "First movement: sudden terror in daily pasture life. Then the knot: calm courage.\n\n"
            "Connect to Janmashtami without graphic detail."
        ),
        detail_hi=(
            "पहला चरण: रोज चरनी में अचानक आतंक। फिर शांत साहस।"
        ),
        why="When you say ‘Keshava’ in aarti, remember protection of ordinary work and play.",
        why_hi="आरती में ‘केशव’ कहें तो साधारण काम-खेल की रक्षा याद करें।",
        takeaway="Defend one ordinary routine (meal, walk, prayer) from unnecessary chaos today.",
        devotion=["krishna-aarti", "krishna-chalisa"],
        festivals=["janmashtami"],
        temples=["krishna-janmabhoomi-mathura", "dwarka"],
    ),
    story(
        slug="jalandhara-vadha",
        title="Jalandhara’s boon and fall — pride born of the ocean’s fire",
        title_hi="जलंधर का वर और पतन — सागर-अग्नि से जन्मा अहंकार",
        deity="shiva",
        hook="A warrior born of blaze won the world — then lost it when dharma withdrew its shade.",
        hook_hi="ज्वाला से जन्मा योद्धा जगत् जीत बैठा — धर्म ने छाया हटाई तो हारा।",
        story_en=(
            "Jalandhara, born of fierce oceanic blaze in the telling, gained power and boons, "
            "challenged the gods, and even troubled Shiva’s household through arrogance. His end "
            "comes when divine strategy and strength remove the asura’s borrowed glory. Boons "
            "shine until character cracks."
        ),
        story_hi=(
            "जलंधर, कथा में उग्र सागरी ज्वाला से जन्मा, वर-बल पाकर देवों को ललकारा, अहंकार से "
            "शिव-गृहस्थ भी सताया। अंत तब जब दिव्य युक्ति-बल ने उधार की प्रभा हटाई। वर चमकते "
            "जब तक चरित्र न फटे।"
        ),
        detail_en=(
            "First movement: spectacular origin mistaken for permanent right to rule. Then the "
            "knot: Vishnu–Shiva strands in variants — keep humility as the ethic.\n\n"
            "AdSense-safe: no sensational scandal focus; pride lesson first."
        ),
        detail_hi=(
            "पहला चरण: भव्य उद्गम को स्थायी राज्याधिकार समझना। फिर नम्रता नीति।\n\n"
            "सनसनी नहीं; अहंकार-शिक्षा।"
        ),
        why="A Shiva evening lamp can ask: ‘Let my origin story never excuse my cruelty.’",
        why_hi="शिव संध्या दीप: ‘मेरा उद्गम मेरी क्रूरता का बहाना न बने।’",
        takeaway="Apologise for one proud sentence you said this week.",
        devotion=["shiva-aarti", "vishnu-aarti"],
        festivals=["maha-shivaratri"],
        temples=["rameswaram", "kashi-vishwanath", "somnath"],
    ),
    story(
        slug="mahishi-vadha-ayyappa",
        title="Mahishi’s boon and Ayyappa — why Hari–Hara’s child entered the forest",
        title_hi="महिषी का वर और अय्यप्पा — हरि–हर बालक वन में क्यों आए",
        deity="ayyappa",
        hook="A boon demanded a child of both Vishnu and Shiva — Sabarimala’s Lord was the answer.",
        hook_hi="वर ने विष्णु और शिव दोनों के बालक की माँग की — सबरीमाला स्वामी उत्तर बने।",
        story_en=(
            "Mahishi’s boon made her nearly unstoppable except by one born of Hari and Hara. "
            "Manikandan / Ayyappa fulfilled that condition, ended her tyranny, and chose the "
            "path of vows at Sabarimala. The rakshasa pattern here is clear: boon → terror → "
            "special avatar-like birth → restoration of order."
        ),
        story_hi=(
            "महिषी का वर उसे लगभग अजेय बनाता — केवल हरि–हर जन्मा उसे हराए। मणिकंदन / अय्यप्पा ने "
            "शर्त पूरी की, अत्याचारांत, सबरीमाला व्रत-पथ चुना। यहाँ राक्षस क्रम स्पष्ट: वर → आतंक "
            "→ विशेष जन्म → क्रम बहाली।"
        ),
        detail_en=(
            "First movement: a boon that looks like a puzzle only heaven can solve. Then the "
            "knot: the child who solves it and still chooses tapasya over throne.\n\n"
            "Companion to Ayyappa Manikandan origin; this page centres Mahishi’s vadha."
        ),
        detail_hi=(
            "पहला चरण: वर जो पहेली-सा लगे। फिर बालक जो हल करे और सिंहासन से अधिक तप चुने।\n\n"
            "यह पृष्ठ महिषी वध केंद्रित।"
        ),
        why="Mandala season vows remember that Ayyappa’s forest path began after restoring order — keep vows clean.",
        why_hi="मंडल व्रत याद: अय्यप्पा वन-पथ क्रम बहाली बाद — व्रत स्वच्छ रखें।",
        takeaway="Keep one small fast or digital fast this week in gratitude, not show.",
        devotion=["ayyappa-aarti", "ayyappa-chalisa", "ayyappa-mandala-vrat-katha"],
        festivals=["makar-sankranti"],
        temples=["sabarimala"],
    ),
    story(
        slug="dhenukasura-krishna-vadha",
        title="Dhenukasura — the ass-demon of the palm grove",
        title_hi="धेनुकासुर — ताड़-वन का गर्दभ-असुर",
        deity="krishna",
        hook="The grove of sweet fruit was guarded by terror — Balarama and Krishna opened it for Braj.",
        hook_hi="मीठे फल का वन आतंक से रक्षित था — बलराम-कृष्ण ने ब्रज हेतु खोला।",
        story_en=(
            "Dhenukasura, an ass-formed asura, held a palm grove so the cowherds could not taste "
            "its fruit. With Balarama, Krishna ended the demon’s grip — a small geography of "
            "freedom inside the larger war with Kamsa. Even ‘minor’ asuras show the same pattern: "
            "stolen commons, then the Lord’s recovery."
        ),
        story_hi=(
            "धेनुकासुर, गर्दभ-असुर, ताड़-वन रोकता ताकि गोप फल न चाखें। बलराम संग कृष्ण ने "
            "असुर-पकड़ तोड़ी — कंस-युद्ध के भीतर स्वतंत्रता का छोटा भूगोल। ‘छोटे’ असुर भी वही क्रम: "
            "साझा चोरी, फिर प्रभु वापसी।"
        ),
        detail_en=(
            "First movement: everyday joy blocked by fear. Then the knot: brothers restoring access.\n\n"
            "Gentle family tone."
        ),
        detail_hi=(
            "पहला चरण: भय से रुका रोज आनंद। फिर भाई पहुँच लौटाते।"
        ),
        why="Share fruit or sweets after Krishna aarti as a symbol of the opened grove.",
        why_hi="कृष्ण आरती बाद फल-मिष्ठान बाँटना खुले वन का संकेत।",
        takeaway="Share one resource you’ve been guarding too tightly at home.",
        devotion=["krishna-aarti", "vitthal-abhang-intro"],
        festivals=["janmashtami"],
        temples=["iskcon-vrindavan", "pandharpur-vitthal"],
    ),
]


def main() -> None:
    # fix any draft placeholders
    for s in NEW:
        fests = [f for f in (s.get("relatedFestivals") or []) if isinstance(f, str)]
        s["relatedFestivals"] = fests
        dev = [d for d in (s.get("relatedDevotion") or []) if isinstance(d, str) and d != "mohini"]
        if s["slug"] == "bhasmasura-mohini" and "vishnu-chalisa" not in dev:
            dev = ["vishnu-aarti", "shiva-aarti", "vishnu-chalisa"]
        s["relatedDevotion"] = dev

    data = json.loads(STORIES_PATH.read_text(encoding="utf-8"))
    existing = {s["slug"] for s in data["stories"]}
    added, skipped = [], []
    for s in NEW:
        if s["slug"] in existing:
            skipped.append(s["slug"])
            continue
        data["stories"].append(s)
        added.append(s["slug"])
    STORIES_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Added {len(added)} rakshasa/boon-avatar stories:")
    for sl in added:
        print(" ", sl)
    if skipped:
        print("Skipped:", skipped)
    print("Total:", len(data["stories"]))


if __name__ == "__main__":
    main()
