#!/usr/bin/env python3
"""Append birth/origin kathas for each Devi-Devata (skip if a strong origin story already exists).

Original TirthaYatra retellings — not scripture reprints. Images via content-media / fetch.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORIES_PATH = ROOT / "data" / "stories.json"

# Already covered by strong birth/origin pages — do not duplicate.
SKIP_DEITIES = {
    "krishna",  # krishna-birth-night
    "ayyappa",  # ayyappa-manikandan
    "sai",  # sai-shirdi-origin
}


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
        or ["origin", "first-timer", "family", "long-read", "ritual-why"],
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
        slug="shiva-lingodbhava-origin",
        title="Lingodbhava — when Shiva appeared as a pillar of light",
        title_hi="लिंगोद्भव — जब शिव ज्योति-स्तंभ बने",
        deity="shiva",
        hook="Brahma sought the top, Vishnu the root — neither found an end to the flame.",
        hook_hi="ब्रह्मा ने शिखर खोजा, विष्णु ने मूल — ज्योति का अंत किसी को न मिला।",
        story_en=(
            "A well-known Shaiva telling begins with a dispute: who is first among the gods? "
            "From that argument rose an endless pillar of fire — Lingodbhava. Vishnu took the form "
            "of a boar and dug downward; Brahma rose as a swan toward the tip. Neither found a limit. "
            "Where ego ended, worship of the formless-and-formed linga began. Temples later carved "
            "this scene so devotees remember: Shiva is not a contest prize — He is the axis that "
            "holds seeking itself."
        ),
        story_hi=(
            "एक प्रसिद्ध शैव कथा विवाद से आरंभ होती है — देवों में प्रथम कौन? उसी से अनंत अग्नि-स्तंभ "
            "उठा — लिंगोद्भव। विष्णु वराह रूप में नीचे गए, ब्रह्मा हंस बनकर ऊपर। अंत किसी को न मिला। "
            "अहंकार जहाँ थमा, वहाँ निराकार-साकार लिंग की पूजा जन्मी। मंदिरों में यह दृश्य इसलिए "
            "उकेरा जाता है कि याद रहे — शिव जी पुरस्कार नहीं, खोज का आधार हैं।"
        ),
        detail_en=(
            "Read slowly: the story is less about winning a debate and more about the shock of "
            "limitlessness. In many South Indian temple gopurams and sanctum niches, Lingodbhava "
            "shows the flaming pillar with Vishnu and Brahma searching. Devotees are invited to "
            "feel small in a healing way — not crushed, but quieted.\n\n"
            "First movement: pride asks for rank. Then the knot tightens: endless light refuses "
            "measurement. Household note: when you touch water to a Shiva linga at home, you are "
            "not “proving” a theology; you are practicing humility before what cannot be finished "
            "in one glance.\n\n"
            "Variants differ on dialogue and sequence. TirthaYatra retells the shared mood for "
            "home learning — confirm local custom with your family priest if you observe a "
            "specific temple rite."
        ),
        detail_hi=(
            "धीरे पढ़ें: यह कथा जीत की नहीं, सीमाहीनता के आश्चर्य की है। दक्षिण के कई मंदिरों में "
            "लिंगोद्भव मूर्ति अग्नि-स्तंभ और खोजते ब्रह्मा-विष्णु दिखाती है। भक्त को छोटा महसूस होना "
            "यहाँ आघात नहीं — शांति है।\n\n"
            "पहला चरण: अहंकार पद माँगता है। फिर गाँठ कसती है: अनंत ज्योति माप नहीं मानती। घर का "
            "नोट: लिंग पर जल चढ़ाते समय आप सिद्धांत सिद्ध नहीं कर रहे — एक दृष्टि में न समा सकने "
            "के सामने नम्रता अभ्यास कर रहे हैं।\n\n"
            "परंपराओं में संवाद भिन्न हो सकते हैं। यह मूल भाव की मौलिक कथा है।"
        ),
        why=(
            "Maha Shivaratri and Monday sawan abhishek echo this mood: pour water, sit still, "
            "and let the linga remind you that devotion outlasts argument."
        ),
        why_hi=(
            "महाशिवरात्रि और सोमवार सावन अभिषेक इसी भाव को दोहराते हैं — जल चढ़ाएँ, स्थिर बैठें, "
            "लिंग याद दिलाए कि भक्ति विवाद से बड़ी है।"
        ),
        takeaway="Offer one calm jal-abhishek today without rushing to the next chore.",
        devotion=["shiva-aarti", "shiva-chalisa", "lingashtakam", "sawan-somwar-vrat-katha"],
        festivals=["maha-shivaratri", "shravan-sawan"],
        temples=["kashi-vishwanath", "mahakaleshwar-ujjain", "rameswaram", "trimbakeshwar"],
    ),
    story(
        slug="vishnu-ananta-shesha-origin",
        title="Vishnu on Ananta — the ocean where protection begins",
        title_hi="अनंत शेष पर विष्णु — जहाँ रक्षा का आरंभ है",
        deity="vishnu",
        hook="Before many avatars, the image that steadies hearts is rest upon the endless serpent.",
        hook_hi="अवतारों से पहले, मन को स्थिर करने वाली छवि — अनंत नाग पर विश्राम।",
        story_en=(
            "Vaishnava imagination often begins not with battle but with rest: Vishnu reclining on "
            "Ananta Shesha upon the ocean of milk, Lakshmi at His feet, Brahma rising from the lotus "
            "of His navel. This is not “laziness” — it is the teaching that the universe is held "
            "inside a calm that never panics. From that stillness, whenever dharma tilts, an avatar "
            "steps into history. Home altars keep this form so the first prayer is trust, not fear."
        ),
        story_hi=(
            "वैष्णव कल्पना अक्सर युद्ध से नहीं, विश्राम से शुरू होती है: क्षीरसागर पर अनंत शेष शय्या "
            "पर विष्णु, चरणों में लक्ष्मी, नाभि-कमल से ब्रह्मा। यह आलस्य नहीं — शिक्षा है कि सृष्टि "
            "उस शांति में टिकी है जो घबराती नहीं। जब धर्म झुकता है, उसी शांति से अवतार इतिहास में "
            "आते हैं। घर की वेदी यह रूप इसलिए रखती है कि पहली प्रार्थना विश्वास हो, भय नहीं।"
        ),
        detail_en=(
            "First movement: the cosmic ocean as a metaphor for what cannot be owned. Then the "
            "knot: creation (Brahma’s lotus) and preservation (Vishnu’s rest) are one household of "
            "meaning. Lakshmi’s presence teaches that prosperity belongs with righteousness, not "
            "with restless grabbing.\n\n"
            "Temples from Badrinath to Padmanabhaswamy keep related moods of the reclining or "
            "seated Lord. Read this as an origin of Vaishnava feeling — the sense that someone is "
            "already watching the world with care — rather than a single historical “birthday.”\n\n"
            "Variants and iconography differ by region. This is an original short retelling for "
            "home devotion."
        ),
        detail_hi=(
            "पहला चरण: क्षीरसागर उस वस्तु का रूपक जिसे स्वामित्व में नहीं बाँधा जा सकता। फिर गाँठ: "
            "सृष्टि (ब्रह्मा का कमल) और पालन (विष्णु का विश्राम) एक ही अर्थ-घर हैं। लक्ष्मी याद "
            "दिलाती हैं — समृद्धि धर्म के साथ है, बेचैन हथियाने के साथ नहीं।\n\n"
            "बद्रीनाथ से पद्मनाभस्वामी तक मंदिर इसी विश्राम-भाव की छवियाँ रखते हैं। इसे वैष्णव "
            "अनुभूति का उद्गम समझें — यह कि कोई जगत की देखभाल पहले से कर रहा है।"
        ),
        why="Vishnu aarti and Ekadashi quiet the week so the mind can rest like Shesha’s coils — steady, not sleepy.",
        why_hi="विष्णु आरती और एकादशी सप्ताह को शांत करती हैं ताकि मन शेष की कुंडली-सा स्थिर रहे — सुस्त नहीं।",
        takeaway="Sit for two quiet minutes before Vishnu’s photo — no requests, only thanks.",
        devotion=["vishnu-aarti", "vishnu-chalisa", "satyanarayan-aarti", "ekadashi-vrat-katha"],
        festivals=["kartik-purnima", "onam"],
        temples=["badrinath", "padmanabhaswamy-thiruvananthapuram", "dwarka", "srirangam-ranganathaswamy"],
    ),
    story(
        slug="durga-born-from-tejas",
        title="How Durga rose from the gods’ combined radiance",
        title_hi="दुर्गा कैसे देव-तेज से प्रकट हुईं",
        deity="devi",
        hook="One asura laughed at every god — until their lights became one Mother.",
        hook_hi="एक असुर हर देव पर हँसा — तब तक, जब तक उनकी ज्योतियाँ एक माँ न बन गईं।",
        story_en=(
            "When Mahishasura’s boon made him nearly unstoppable, the gods did not invent a new "
            "weapon first — they offered their tejas, their brilliance. From that gathered light "
            "Durga appeared: many-armed, calm-eyed, riding the lion, carrying what each deity "
            "could give. Her “birth” is cooperation made visible. The war that follows is famous; "
            "the origin lesson is quieter — courage is shared before it is swung."
        ),
        story_hi=(
            "जब महिषासुर का वर उसे लगभग अजेय बनाता है, देव पहले नया शस्त्र नहीं गढ़ते — अपना तेज "
            "अर्पित करते हैं। उसी एकत्र ज्योति से दुर्गा प्रकट होती हैं: अनेक भुजाएँ, शांत दृष्टि, "
            "सिंह पर सवार, हर देव का दान धारण किए। उनका “जन्म” सहयोग का साकार रूप है। आगे का युद्ध "
            "प्रसिद्ध है; उद्गम की शिक्षा शांत है — साहस पहले बाँटा जाता है, फिर चलाया जाता है।"
        ),
        detail_en=(
            "First movement: crisis exposes that no single power is enough. Then the knot tightens: "
            "ego among the gods softens into offering. Durga’s form teaches householders that "
            "strength can be collective without becoming chaotic.\n\n"
            "Navaratri evenings retell this origin beside the slaying of Mahisha. Keep both "
            "halves: the Mother who arrives because many hearts opened, and the Mother who "
            "protects when fear grows loud.\n\n"
            "Regional tellings vary. This is TirthaYatra’s original home-learning retelling."
        ),
        detail_hi=(
            "पहला चरण: संकट बताता है कि एक अकेला बल काफी नहीं। फिर अहंकार अर्पण में पिघलता है। "
            "दुर्गा का रूप सिखाता है — शक्ति सामूहिक हो सकती है बिना अव्यवस्थित हुए।\n\n"
            "नवरात्रि की संध्याएँ इस उद्गम को महिषवध के साथ याद करती हैं। दोनों याद रखें।"
        ),
        why="Navaratri and Chaitra Navaratri begin with calling the Mother who was born of shared light — invite unity at home before grand rituals.",
        why_hi="नवरात्रि और चैत्र नवरात्रि उसी माँ को बुलाती हैं जो साझा ज्योति से जन्मीं — बड़े अनुष्ठान से पहले घर में एकता निमंत्रित करें।",
        takeaway="Before evening lamps, thank one person who shared strength with you this week.",
        devotion=["devi-aarti", "durga-chalisa", "navaratri-vrat-katha", "durga-aarti-jagdamba"],
        festivals=["navaratri", "chaitra-navaratri", "dussehra"],
        temples=["vaishno-devi", "meenakshi-madurai", "vindhyavasini-vindhyachal", "kalighat"],
    ),
    story(
        slug="ganesha-born-of-parvati",
        title="How Parvati shaped Ganesha from love and turmeric",
        title_hi="पार्वती ने प्रेम और हल्दी से गणेश को कैसे रचा",
        deity="ganesha",
        hook="A door needed a guardian — and a mother’s wish became a son.",
        hook_hi="द्वार को रक्षक चाहिए था — और माँ की इच्छा पुत्र बन गई।",
        story_en=(
            "Before the elephant head became the famous sign, many tellings begin at a quieter "
            "moment: Parvati, wishing privacy for her bath, shaped a boy from the body’s purity "
            "and turmeric-paste and breathed life into him. She set him at the door as a loyal "
            "guard. What follows — Shiva’s arrival, the clash, the elephant head — is told "
            "elsewhere. This origin asks a softer question: what do we create when we need "
            "safety, and how carefully do we honor what love has made?"
        ),
        story_hi=(
            "हाथी के सिर की प्रसिद्ध छाप से पहले कई कथाएँ शांत क्षण से शुरू होती हैं: पार्वती स्नान "
            "की एकांत चाह में शरीर की शुद्धता और हल्दी-लेप से बालक गढ़ती हैं, प्राण देती हैं, द्वार "
            "पर प्रहरी बैठाती हैं। आगे — शिव का आगमन, संघर्ष, गजमुख — और कथा में है। यह उद्गम "
            "कोमल प्रश्न पूछता है: सुरक्षा चाहकर हम क्या रचते हैं, और प्रेम की रचना का सम्मान कैसे "
            "करते हैं?"
        ),
        detail_en=(
            "First movement: a mother’s rightful boundary. Then the knot: guardianship without "
            "introduction leads to tragedy — and later, restoration. The birth scene itself is "
            "tender: creativity as care.\n\n"
            "Ganesh Chaturthi celebrates both making and welcoming the son of Parvati. At home, "
            "shaping or installing a murti can echo that first shaping — done with clean hands "
            "and a calm vow, not haste.\n\n"
            "Tellings differ on materials and sequence. Read alongside our elephant-head story "
            "for the fuller arc."
        ),
        detail_hi=(
            "पहला चरण: माँ की उचित सीमा। फिर गाँठ: बिना परिचय के प्रहरी-धर्म दुःख लाता है — और "
            "बाद में पुनरुद्धार। जन्म-दृश्य कोमल है: रचना ही देखभाल है।\n\n"
            "गणेश चतुर्थी निर्माण और स्वागत दोनों मनाती है। घर में मूर्ति स्थापित करते समय उसी "
            "शांत संकल्प की याद रखें।"
        ),
        why="Ganesh Chaturthi and door-prayers remember the child Parvati made before the world knew his fame.",
        why_hi="गणेश चतुर्थी और द्वार-प्रार्थना उसी बालक को याद करती हैं जिसे जगत् की प्रसिद्धि से पहले पार्वती ने रचा।",
        takeaway="Place Ganesha near your main door today and greet him once before leaving home.",
        devotion=["ganesha-aarti", "ganesha-chalisa", "ganesh-chaturthi-vrat-katha"],
        festivals=["ganesh-chaturthi"],
        temples=["siddhivinayak-mumbai", "dagdusheth-ganpati-pune", "rockfort-uchhi-pillayar-trichy"],
    ),
    story(
        slug="rama-birth-ayodhya",
        title="Rama’s birth in Ayodhya — the yajna that opened a palace",
        title_hi="अयोध्या में राम का जन्म — यज्ञ जिसने राजभवन खोला",
        deity="rama",
        hook="A king’s longing, a sage’s fire, and four sons who arrived as answers.",
        hook_hi="राजा की तड़प, ऋषि की अग्नि, और चार पुत्र जो उत्तर बनकर आए।",
        story_en=(
            "Dasharatha of Ayodhya longed for heirs. With sage guidance he performed a putrakameshti "
            "yajna; from the sacred fire came a blessing shared among Kausalya, Kaikeyi, and Sumitra. "
            "On a bright Chaitra day Rama was born to Kausalya — joy that later would teach the "
            "world about duty. His brothers Lakshmana, Bharata, and Shatrughna completed the gift. "
            "Ram Navami keeps that palace morning alive: not only a prince’s birthday, but the "
            "feeling that dharma can enter a home as a child."
        ),
        story_hi=(
            "अयोध्या के दशरथ पुत्र चाहते थे। ऋषि-मार्गदर्शन में पुत्रकामेष्टि यज्ञ हुआ; अग्नि से "
            "आशीष कौसल्या, कैकेयी और सुमित्रा में बँटा। चैत्र की उज्ज्वल तिथि पर कौसल्या से राम "
            "जन्मे — आनंद जो आगे जगत् को कर्तव्य सिखाएगा। लक्ष्मण, भरत, शत्रुघ्न ने वर को पूरा "
            "किया। रामनवमी उसी राजभवन की सुबह जिलाती है: केवल राजकुमार का जन्मदिन नहीं — यह भाव "
            "कि धर्म घर में बालक बनकर आ सकता है।"
        ),
        detail_en=(
            "First movement: longing that turns toward sacred effort, not only politics. Then "
            "the knot of later years — exile, vows, return — remains for other stories. Here, "
            "stay with the cradle: a city learning to celebrate responsibility as affection.\n\n"
            "Ayodhya temples and Ram Navami processions retell this birth with lamps and chanting. "
            "At home, reading a short Rama aarti on Navami can be enough if travel is not possible.\n\n"
            "Epic details vary by telling. This is an original concise retelling for families."
        ),
        detail_hi=(
            "पहला चरण: तड़प जो केवल राजनीति नहीं, पवित्र प्रयास की ओर मुड़ती है। बाद के वनवास "
            "की गाँठ अन्य कथाओं में है। यहाँ पालने के पास ठहरें।\n\n"
            "अयोध्या और रामनवमी इस जन्म को दीप-गान से दोहराते हैं। घर पर छोटी राम आरती भी पर्याप्त हो सकती है।"
        ),
        why="Ram Navami remembers the morning Ayodhya received Rama — keep one lamp and one clean corner for that joy.",
        why_hi="रामनवमी अयोध्या की उस सुबह को याद करती है जब राम आए — उस आनंद के लिए एक दीप और एक स्वच्छ कोना रखें।",
        takeaway="On your next Monday or Navami, read one page of Rama’s childhood praise aloud.",
        devotion=["rama-aarti", "rama-chalisa", "ram-navami-vrat-katha"],
        festivals=["ram-navami", "dussehra"],
        temples=["kanak-bhawan-ayodhya", "ayodhya-ram-mandir", "orchha-ram-raja"],
    ),
    story(
        slug="hanuman-birth-anjana",
        title="Hanuman’s birth — Anjana’s prayer and the wind’s gift",
        title_hi="हनुमान का जन्म — अंजना की प्रार्थना और पवन का वर",
        deity="hanuman",
        hook="A child of vow and wind — restless at first, then the world’s greatest servant.",
        hook_hi="व्रत और वायु का बालक — पहले चंचल, फिर जगत् का सबसे बड़ा सेवक।",
        story_en=(
            "Anjana’s penance and Vayu’s grace meet in the birth of Hanuman. Popular tellings say "
            "the wind-god carried a portion of divine pudding from Dasharatha’s yajna to Anjana, "
            "and the child who arrived was strength wrapped in mischief — leaping at the sun, "
            "learning through curse and blessing to become Rama’s messenger. Hanuman Jayanti "
            "honours that origin: power that learns to kneel in love."
        ),
        story_hi=(
            "अंजना की तपस्या और वायु की कृपा हनुमान के जन्म में मिलती हैं। प्रसिद्ध कथा कहती है "
            "पवन ने दशरथ-यज्ञ के प्रसाद का अंश अंजना तक पहुँचाया; आया बालक बल और शरारत का संगम "
            "था — सूर्य को छूने को उछला, शाप-वर से सीखा, राम का दूत बना। हनुमान जयंती उसी उद्गम "
            "को नमन करती है: शक्ति जो प्रेम में झुकना सीखे।"
        ),
        detail_en=(
            "First movement: a mother’s prayer answered as responsibility, not spectacle. Then "
            "the knot of youthful haste — and teachers who reshape it into seva. Some traditions "
            "also speak of Shiva’s amsha; devotion does not need one exclusive formula.\n\n"
            "Temples from Ayodhya’s Hanuman Garhi to Salasar keep the birth-joy alive beside the "
            "warrior’s courage. At home, Chalisa on Jayanti mornings is a simple origin rite.\n\n"
            "This is an original household retelling; local katha may add regional colour."
        ),
        detail_hi=(
            "पहला चरण: माँ की प्रार्थना का उत्तर जिम्मेदारी है, तमाशा नहीं। फिर बाल-जल्दबाजी की "
            "गाँठ — और गुरु जो उसे सेवा बना देते हैं। कुछ परंपराएँ शिव-अंश भी कहती हैं; भक्ति को "
            "एक ही सूत्र की ज़िद नहीं।\n\n"
            "जयंती की सुबह चालीसा घर का सरल उद्गम-अनुष्ठान हो सकता है।"
        ),
        why="Hanuman Jayanti returns to Anjana’s answered prayer — begin with gratitude, then strength.",
        why_hi="हनुमान जयंती अंजना की सुनी गई प्रार्थना पर लौटती है — पहले कृतज्ञता, फिर बल।",
        takeaway="Read five chaupais of Hanuman Chalisa standing, as if greeting a newborn hero.",
        devotion=["hanuman-chalisa", "hanuman-aarti", "hanuman-jayanti-vrat-katha"],
        festivals=["hanuman-jayanti", "ram-navami"],
        temples=["hanuman-garhi-ayodhya", "salasar-balaji", "sankat-mochan-varanasi"],
    ),
    story(
        slug="murugan-skanda-birth",
        title="Skanda’s birth — six sparks, six faces, one commander",
        title_hi="स्कंद का जन्म — छह चिंगारियाँ, छह मुख, एक सेनापति",
        deity="murugan",
        hook="Shiva’s fire became too bright for one womb — the Krittikas raised a war-god of love.",
        hook_hi="शिव की अग्नि एक गर्भ के लिए तीव्र थी — कृत्तिकाओं ने प्रेम का योद्धा पाला।",
        story_en=(
            "When the asura Taraka threatened the worlds, a commander was needed who could carry "
            "divine fire. Shaiva-Skanda tellings say sparks from Shiva were borne by Agni and Ganga, "
            "then nursed by the six Krittikas — hence six faces, Shanmukha. The child grew into "
            "Murugan / Kartikeya, spear in hand, peacock as vahana. His birth festival moods live "
            "in Skanda Shashti and Thai Poosam: courage trained by many mothers."
        ),
        story_hi=(
            "जब तारकासुर लोकों को संकट में डालता, ऐसा सेनापति चाहिए था जो दिव्य अग्नि उठा सके। "
            "शैव-स्कंद कथा कहती है शिव की चिंगारियाँ अग्नि और गंगा से होती कृत्तिकाओं तक पहुँचीं — "
            "अतः षट्मुख। बालक मुरुगन / कार्तिकेय बना, वेल और मयूर संग। स्कंद षष्ठी और थाईपूसम "
            "उसी जन्म-भाव को जिलाते हैं: साहस जिसे कई माताओं ने सिखाया।"
        ),
        detail_en=(
            "First movement: a cosmic emergency answered by shared caregiving. Then the knot: "
            "the boy must choose duty over endless play — and does so with grace.\n\n"
            "Palani, Tiruchendur, and other arupadai veedu temples keep Skanda’s presence vivid. "
            "North Indian Kartikeya shrines and South Indian Murugan bhakti are one family of "
            "feeling.\n\n"
            "Details of the sparks’ journey vary. This retelling is for home learning."
        ),
        detail_hi=(
            "पहला चरण: संकट का उत्तर साझा लालन-पालन से। फिर बालक को खेल से कर्तव्य चुनना होता है।\n\n"
            "पलनी और तिरुचेंदूर् जैसे क्षेत्र स्कंद की उपस्थिति जगाए रखते हैं।"
        ),
        why="Skanda Shashti and Thai Poosam honour the birth of the spear-bearing child — keep one small vow of courage.",
        why_hi="स्कंद षष्ठी और थाईपूसम वेलधारी बालक के जन्म को नमन करते हैं — साहस का एक छोटा व्रत रखें।",
        takeaway="Offer a red flower or a simple lamp to Murugan and name one fear you will face kindly.",
        devotion=["murugan-aarti", "murugan-chalisa", "murugan-kanda-intro", "skanda-shashti-vrat-katha"],
        festivals=["skanda-shashti", "thaipusam"],
        temples=["palani-murugan", "thiruchendur-murugan", "swamimalai-murugan", "tiruttani-murugan"],
    ),
    story(
        slug="surya-aditya-origin",
        title="Surya’s origin — the eye of the world that teaches rhythm",
        title_hi="सूर्य का उद्गम — जगत् का नेत्र जो लय सिखाता है",
        deity="surya",
        hook="Before clocks, people learned time by greeting the rising Aditya.",
        hook_hi="घड़ी से पहले लोग समय उगते आदित्य को प्रणाम करके सीखते थे।",
        story_en=(
            "Puranic streams describe Surya as Aditya — brilliance born of cosmic order, riding "
            "a chariot of seven horses, seeing every field and rooftop. His “origin” for householders "
            "is less a private birthday and more a daily rebirth at dawn. Chhath and Makar Sankranti "
            "keep that origin public: thank the light that ripens grain and steadies health without "
            "asking for drama."
        ),
        story_hi=(
            "पौराणिक धाराएँ सूर्य को आदित्य कहती हैं — ब्रह्मांडीय क्रम की ज्योति, सात अश्वों का "
            "रथ, हर खेत-छत को देखते। गृहस्थ के लिए उनका “उद्गम” निजी जन्मदिन कम, प्रतिदिन उषा का "
            "पुनर्जन्म अधिक है। छठ और मकर संक्रांति इसे सार्वजनिक रखती हैं: उस प्रकाश का धन्यवाद "
            "जो अन्न पकाए और स्वास्थ्य थामे — तमाशा माँगे बिना।"
        ),
        detail_en=(
            "First movement: light as gift, not possession. Then the knot: pride that stares at "
            "the sun without humility is warned in many folk tales — look with reverence, through "
            "water or prayer, not arrogance.\n\n"
            "Konark’s stone wheels and temple Surya shrines make the chariot visible. At home, "
            "arghya with water is a miniature origin rite each morning.\n\n"
            "Astronomical and mythic languages differ; both can inspire gratitude."
        ),
        detail_hi=(
            "पहला चरण: प्रकाश दान है, संपत्ति नहीं। फिर अहंकार की गाँठ — सूर्य को घमंड से न घूरें।\n\n"
            "घर में जल से अर्घ्य प्रतिदिन का छोटा उद्गम-अनुष्ठान है।"
        ),
        why="Chhath Puja and Makar Sankranti return to Surya’s public origin — offer water facing east with a calm mind.",
        why_hi="छठ और मकर संक्रांति सूर्य के सार्वजनिक उद्गम पर लौटती हैं — पूर्व मुख जल अर्पित करें, मन शांत रखें।",
        takeaway="At sunrise tomorrow, step outside for thirty seconds and thank the light aloud.",
        devotion=["surya-aarti", "surya-chalisa"],
        festivals=["chhath-puja", "makar-sankranti", "pongal"],
        temples=["konark-sun-temple", "sun-temple-deo", "suraj-kund-meerut"],
    ),
    story(
        slug="shani-birth-chhaya",
        title="Shani’s birth — Chhaya’s child and the lesson of slow justice",
        title_hi="शनि का जन्म — छाया का पुत्र और धीमे न्याय की शिक्षा",
        deity="shani",
        hook="Not every birth is soft light — some arrive to teach patience under shadow.",
        hook_hi="हर जन्म कोमल प्रकाश नहीं — कुछ छाया में धैर्य सिखाने आते हैं।",
        story_en=(
            "Folk-Puranic tellings say Shani was born to Surya through Chhaya — Shadow — when "
            "Sanjna could not bear the sun’s full blaze. The child’s gaze was so intense that "
            "even his father felt its weight. Shani’s origin story is not cruelty for sport; it "
            "is the idea that actions ripen in time. Devotees approach him with honesty and "
            "steady charity, especially on Saturdays."
        ),
        story_hi=(
            "लोक-पौराणिक कथा कहती है शनि सूर्य से छाया (छाये) के माध्यम से जन्मे — जब संज्ञा पूर्ण "
            "तेज नहीं सह सकीं। बालक की दृष्टि ऐसी कि पिता को भी उसका भार छू गया। शनि की उद्गम-कथा "
            "क्रूर खेल नहीं; यह भाव है कि कर्म समय में पकते हैं। भक्त शनिवार को ईमानदारी और स्थिर "
            "दान से उनके निकट जाते हैं।"
        ),
        detail_en=(
            "First movement: even light needs shade to become livable. Then the knot: justice "
            "that is only swift can be shallow; Shani’s mood is thoroughness.\n\n"
            "Shingnapur and other Shani temples teach fearlessness through truthfulness — not "
            "superstition shopping. At home, a simple oil lamp and a promise to correct one "
            "habit can honour this origin.\n\n"
            "Astrological claims vary; TirthaYatra keeps the ethical core for AdSense-safe home learning."
        ),
        detail_hi=(
            "पहला चरण: प्रकाश को भी जीने लायक बनाने छाया चाहिए। फिर गाँठ: केवल तीव्र न्याय छिछला "
            "हो सकता है; शनि का भाव पूर्णता है।\n\n"
            "घर में एक दीपक और एक बुरी आदत सुधारने का वचन पर्याप्त सम्मान हो सकता है।"
        ),
        why="Saturday Shani worship remembers the child of shadow — keep vows small, honest, and kept.",
        why_hi="शनिवार की शनि पूजा छाया-पुत्र को याद करती है — व्रत छोटे, सच, और निभाए हुए रखें।",
        takeaway="Give a small, quiet donation this Saturday without announcing it.",
        devotion=["shani-aarti", "shani-chalisa"],
        festivals=["makar-sankranti"],
        temples=["shani-shingnapur"],
    ),
    story(
        slug="dattatreya-birth-anusuya",
        title="Dattatreya’s birth — Anusuya’s chastity and the trinity as one child",
        title_hi="दत्तात्रेय का जन्म — अनुसूया की पतिव्रता और त्रिमूर्ति बालक",
        deity="dattatreya",
        hook="Three guests tested a sage’s wife — and left as one guru in her arms.",
        hook_hi="तीन अतिथि ने पत्नी की परीक्षा ली — और एक गुरु बनकर गोद में छोड़ गए।",
        story_en=(
            "Anusuya’s purity and Atri’s tapasya drew Brahma, Vishnu, and Shiva in disguise. "
            "Her wise hospitality transformed their test into blessing: the trinity was born "
            "to her as Dattatreya — one child, three heads in iconography, walking later with "
            "dogs and nature as teachers. His birth story is the origin of a wandering guru "
            "ideal: wisdom without pride of caste costume."
        ),
        story_hi=(
            "अनुसूया की पवित्रता और अत्रि की तपस्या ने ब्रह्मा-विष्णु-शिव को वेश में खींचा। उनकी "
            "समझदार अतिथि-सेवा ने परीक्षा को आशीष बना दिया: त्रिमूर्ति दत्तात्रेय रूप में जन्मे — "
            "एक बालक, मूर्ति में तीन मुख, आगे कुत्तों और प्रकृति को गुरु बनाकर विचरते। यह जन्म "
            "घूमते गुरु-आदर्श का उद्गम है: बिन अहंकार की प्रज्ञा।"
        ),
        detail_en=(
            "First movement: hospitality as spiritual intelligence. Then the knot: society "
            "startles at an avadhuta who learns from animals — and must soften judgment.\n\n"
            "Datta temples and Guru Purnima moods keep this birth alive. At home, thanking "
            "three ordinary teachers in one day echoes the trinity gift.\n\n"
            "Companion piece to our earlier Dattatreya avatar essay; here the focus is the birth itself."
        ),
        detail_hi=(
            "पहला चरण: अतिथि-सत्कार आध्यात्मिक बुद्धि है। फिर समाज अवधूत पर चौंकता है — और निर्णय "
            "कोमल करना सीखे।\n\n"
            "यहाँ केंद्र जन्म है; अवतार-विचार अलग निबंध में है।"
        ),
        why="Guru Purnima can include Dattatreya’s birth gratitude — honour teachers who arrived in unexpected form.",
        why_hi="गुरु पूर्णिमा में दत्तात्रेय जन्म की कृतज्ञता जोड़ें — अप्रत्याशित रूप में आए गुरु का सम्मान।",
        takeaway="Name three people or books that taught you this year and thank them silently.",
        devotion=["vishnu-aarti", "shiva-aarti"],
        festivals=["guru-purnima"],
        temples=["maniknagar-datta", "narsobawadi-datta"],
    ),
    story(
        slug="narasimha-pillar-appearance",
        title="Narasimha’s appearance — the Lord who stepped out of a pillar",
        title_hi="नरसिंह का प्रादुर्भाव — स्तंभ से निकले भगवान",
        deity="narasimha",
        hook="Neither day nor night, neither indoor nor outdoor — protection found a loophole of love.",
        hook_hi="न दिन न रात, न घर न बाहर — रक्षा ने प्रेम की दरार खोज ली।",
        story_en=(
            "Hiranyakashipu’s boon tried to fence God out of every category. Prahlada’s faith "
            "pointed to a palace pillar; from that wood and stone Narasimha burst forth — man-lion, "
            "at twilight, on the threshold — ending tyranny without breaking the letter of the "
            "boon. This is less a gentle “birth” and more an origin of fierce compassion: love "
            "that refuses to abandon a child devotee."
        ),
        story_hi=(
            "हिरण्यकशिपु का वर ईश्वर को हर वर्ग से बाहर रखता। प्रह्लाद की श्रद्धा ने महल के स्तंभ "
            "की ओर इशारा किया; काठ-पत्थर से नरसिंह फूटे — नर-सिंह, संध्या में, देहरी पर — वर के "
            "अक्षर तोड़े बिना अत्याचार का अंत। यह कोमल “जन्म” कम, प्रचंड करुणा का उद्गम अधिक है: "
            "प्रेम जो बाल भक्त को नहीं छोड़ता।"
        ),
        detail_en=(
            "First movement: ideology that treats categories as cages. Then the knot: devotion "
            "speaks a language cages cannot parse.\n\n"
            "Holi’s Prahlada memory and Narasimha Jayanti moods return here. Temple pillars "
            "sometimes carved with the scene remind visitors that courage can hide in plain sight.\n\n"
            "Read with our fuller Hiranyakashipu katha for the political arc; this page centres the appearance."
        ),
        detail_hi=(
            "पहला चरण: वर्गों को पिंजरा बनाने वाली सोच। फिर भक्ति वह भाषा बोलती है जिसे पिंजरा समझ नहीं पाता।\n\n"
            "यह पृष्ठ प्रादुर्भाव पर केंद्रित है; पूरी राजनीतिक कथा साथ के निबंध में है।"
        ),
        why="Narasimha remembrance teaches that protection may arrive in forms we did not schedule.",
        why_hi="नरसिंह स्मरण सिखाता है — रक्षा ऐसे रूप में आ सकती है जिसकी समय-सारिणी हमने नहीं बनाई।",
        takeaway="When afraid, touch a doorframe or wall at home and whisper one line of trust.",
        devotion=["vishnu-aarti", "vishnu-chalisa"],
        festivals=["holi"],
        temples=["narasimha-jharni-bidar", "simhachalam", "yadagirigutta"],
    ),
    story(
        slug="vitthal-vithoba-origin",
        title="Vitthal’s origin at Pandharpur — the Lord who waited on a brick",
        title_hi="पंढरपुर में विठ्ठल का उद्गम — ईंट पर प्रतीक्षारत प्रभु",
        deity="vitthal",
        hook="A son’s service delayed a saint — so God stood on a brick and waited.",
        hook_hi="पुत्र-सेवा से संत रुके — तो भगवान ईंट पर खड़े प्रतीक्षा करने लगे।",
        story_en=(
            "Varkari tellings say Pundalik was busy serving his parents when Vishnu arrived. "
            "Rather than scold, the Lord stood on a brick (vit) and waited — becoming Vitthal / "
            "Vithoba of Pandharpur, hands on hips, patient as a parent. The origin of this form "
            "is the sanctity of ordinary duty. Abhangs and palkhi processions still walk toward "
            "that waiting kindness."
        ),
        story_hi=(
            "वारकरी कथा कहती है पुंडलिक माता-पिता की सेवा में व्यस्त थे जब विष्णु आए। डाँट के "
            "बजाय प्रभु ईंट (विट) पर खड़े प्रतीक्षा करते रहे — पंढरपुर के विठ्ठल / विठोबा बने, "
            "कमर पर हाथ, माता-पिता-से धैर्यवान। इस रूप का उद्गम साधारण कर्तव्य की पवित्रता है। "
            "अभंग और पालखी आज भी उसी प्रतीक्षा की करुणा की ओर चलती हैं।"
        ),
        detail_en=(
            "First movement: God values the care you give at home. Then the knot: pilgrims "
            "must learn that darshan without kindness to elders is incomplete.\n\n"
            "Pandharpur’s ashadi and kartiki rhythms keep the origin public. At home, one act "
            "of service before aarti echoes Pundalik.\n\n"
            "Related Krishna-Vitthal feelings overlap; this page keeps the Vithoba brick-origin clear."
        ),
        detail_hi=(
            "पहला चरण: भगवान घर की सेवा को महत्व देते हैं। फिर गाँठ: वृद्धों के प्रति करुणा बिना "
            "दर्शन अधूरा।\n\n"
            "आरती से पहले एक सेवा पुंडलिक की याद है।"
        ),
        why="Ashadi Ekadashi pilgrim mood begins with Vitthal’s patient origin — serve someone at home first.",
        why_hi="आषाढ़ी एकादशी का यात्री-भाव विठ्ठल के धैर्य-उद्गम से शुरू होता है — पहले घर में किसी की सेवा करें।",
        takeaway="Do one helpful task for a parent or elder before your evening prayer.",
        devotion=["vitthal-abhang-intro", "krishna-aarti"],
        festivals=["kartik-purnima"],
        temples=["pandharpur-vitthal"],
    ),
    story(
        slug="bhairav-kalabhairav-origin",
        title="Bhairav’s origin — the fierce guardian born of Shiva’s roar",
        title_hi="भैरव का उद्गम — शिव की गर्जना से जन्मा प्रचंड रक्षक",
        deity="bhairav",
        hook="When arrogance needed a boundary, a guardian with a dog appeared.",
        hook_hi="जब अहंकार को सीमा चाहिए थी, कुत्ते संग एक रक्षक प्रकट हुए।",
        story_en=(
            "Shaiva tellings describe Bhairav as arising from Shiva’s fierce energy to curb "
            "cosmic arrogance and guard sacred thresholds — especially time (Kala Bhairava). "
            "His origin is the birth of protective terror that serves devotees who walk honestly "
            "at night roads and temple doors. Dogs as companions remind us that loyalty can look "
            "unpolished and still be holy."
        ),
        story_hi=(
            "शैव कथाएँ भैरव को शिव की प्रचंड ऊर्जा से उत्पन्न बताती हैं — अहंकार थामने और पवित्र "
            "देहरी, विशेषकर काल की रक्षा के लिए (कालभैरव)। उनका उद्गम रक्षक भय का जन्म है जो "
            "ईमानदार राहगीर और मंदिर-द्वार की सेवा करता है। कुत्ता साथ याद दिलाता है — निष्ठा "
            "बिना चमक के भी पवित्र हो सकती है।"
        ),
        detail_en=(
            "First movement: holiness needs a gatekeeper. Then the knot: fear without ethics "
            "becomes superstition; Bhairav bhakti at its best asks for truthfulness and courage.\n\n"
            "Ujjain’s Kal Bhairav and Kashi’s Kaal Bhairav traditions keep this origin vivid. "
            "At home, a Saturday or eighth-day remembrance can be a lamp and a vow to speak "
            "one difficult truth kindly.\n\n"
            "Keep practice AdSense-safe: no harm rituals, no paid “tantra fear” claims — only "
            "guardian devotion."
        ),
        detail_hi=(
            "पहला चरण: पवित्रता को द्वारपाल चाहिए। फिर गाँठ: बिना नीति का भय अंधविश्वास बनता है।\n\n"
            "घर में दीपक और एक कठिन सच कोमलता से बोलने का वचन पर्याप्त हो सकता है।"
        ),
        why="Bhairav remembrance guards time and thresholds — begin evenings with honesty, not panic.",
        why_hi="भैरव स्मरण काल और देहरी की रक्षा करता है — संध्या ईमानदारी से शुरू करें, घबराहट से नहीं।",
        takeaway="Light one lamp near your doorway and commit to one truthful sentence today.",
        devotion=["bhairav-chalisa", "shiva-aarti"],
        festivals=["maha-shivaratri"],
        temples=["kal-bhairav-ujjain", "kaal-bhairav-kashi"],
    ),
    story(
        slug="lakshmi-ocean-birth",
        title="Lakshmi’s birth from the ocean of milk",
        title_hi="क्षीरसागर से लक्ष्मी का प्रादुर्भाव",
        deity="lakshmi",
        hook="When the ocean was churned for amrita, grace arrived wearing lotus and light.",
        hook_hi="अमृत के लिए सागर मथा गया — कृपा कमल और प्रकाश पहनकर आईं।",
        story_en=(
            "During Samudra Manthan, among treasures and terrors, Lakshmi rose from the ocean — "
            "lotus in hand, choosing Vishnu as eternal consort. Her origin teaches that prosperity "
            "is a guest who stays where dharma and generosity live. Diwali nights and Varalakshmi "
            "vrat remember that birth: clean the home, open the door, but do not confuse glitter "
            "with grace."
        ),
        story_hi=(
            "समुद्र मंथन में रत्नों और संकटों के बीच लक्ष्मी सागर से उभरीं — कर में कमल, विष्णु को "
            "नित्य संग चुनतीं। उनका उद्गम सिखाता है: समृद्धि उस घर की अतिथि है जहाँ धर्म और दान "
            "हैं। दीपावली और वरलक्ष्मी व्रत उसी जन्म को याद करते हैं: घर साफ करें, द्वार खोलें, "
            "पर चमक को कृपा मत समझ बैठें।"
        ),
        detail_en=(
            "First movement: shared effort (gods and asuras churning) yields a gift that chooses "
            "righteousness. Then the knot: wealth without character spills away.\n\n"
            "Raja Ravi Varma’s calm Lakshmi images and temple Mahalakshmi shrines keep her ocean "
            "birth in public memory. At home, a coin and a lamp are enough if the heart is clean.\n\n"
            "Companion to the Kurma churning story; here Lakshmi is the centre."
        ),
        detail_hi=(
            "पहला चरण: साझा प्रयास से वह वर आता है जो धर्म चुनता है। फिर गाँठ: चरित्रहीन धन बह "
            "जाता है।\n\n"
            "यहाँ लक्ष्मी केंद्र हैं; कूर्म मंथन की कथा साथ में पढ़ें।"
        ),
        why="Diwali Lakshmi puja and Varalakshmi vrat revisit her ocean birth — invite grace with cleanliness and charity.",
        why_hi="दीपावली लक्ष्मी पूजा और वरलक्ष्मी व्रत सागर-जन्म पर लौटते हैं — स्वच्छता और दान से कृपा बुलाएँ।",
        takeaway="Before lighting lamps, set aside one small amount for someone who needs food.",
        devotion=["lakshmi-aarti", "lakshmi-chalisa", "diwali-lakshmi-puja-katha", "varalakshmi-vrat-katha"],
        festivals=["diwali", "dhanteras", "akshaya-tritiya"],
        temples=["mahalaxmi-kolhapur", "mahalaxmi-mumbai"],
    ),
    story(
        slug="saraswati-vak-origin",
        title="Saraswati’s origin — when speech and learning took a mother’s form",
        title_hi="सरस्वती का उद्गम — जब वाणी और विद्या ने माँ का रूप लिया",
        deity="saraswati",
        hook="Before books, people prayed that words themselves would be kind and true.",
        hook_hi="किताबों से पहले लोग प्रार्थना करते — शब्द स्वयं दयालु और सत्य हों।",
        story_en=(
            "Saraswati is praised as Vak — sacred speech — and as the river-like flow of knowledge. "
            "Puranic images show her arising with veena, book, and swan, white as clarity. Her "
            "“birth” for students is the moment learning becomes reverence: not marks alone, but "
            "the courage to speak carefully. Vasant Panchami keeps that origin on the calendar."
        ),
        story_hi=(
            "सरस्वती वाक् — पवित्र वाणी — और ज्ञान की नदी-सी धारा के रूप में स्तुति पाती हैं। "
            "पौराणिक छवि: वीणा, पुस्तक, हंस, श्वेत स्पष्टता। विद्यार्थी के लिए उनका “जन्म” वह क्षण "
            "है जब पढ़ाई श्रद्धा बनती है: केवल अंक नहीं, सावधानी से बोलने का साहस। वसंत पंचमी उसी "
            "उद्गम को तिथि देती है।"
        ),
        detail_en=(
            "First movement: knowledge as purity of intention. Then the knot: speech that wounds "
            "cannot claim Saraswati even if it is clever.\n\n"
            "Keep notebooks neat on Panchami; place a flower on your study desk. That is origin "
            "practice without expense.\n\n"
            "Avoid miracle claims about exams — AdSense-safe devotion is effort plus prayer."
        ),
        detail_hi=(
            "पहला चरण: ज्ञान नीयत की शुद्धता है। फिर गाँठ: चोट पहुँचाती वाणी सरस्वती नहीं कहलाती।\n\n"
            "पंचमी पर पुस्तकों पर फूल — बिना खर्चे का उद्गम-अभ्यास।"
        ),
        why="Vasant Panchami returns to Saraswati’s origin as learning’s mother — begin studies with one clean page.",
        why_hi="वसंत पंचमी सरस्वती को विद्या की माँ के उद्गम पर लौटाती है — पढ़ाई एक स्वच्छ पृष्ठ से शुरू करें।",
        takeaway="Write one sentence of gratitude in a notebook before studying today.",
        devotion=["saraswati-aarti", "saraswati-chalisa"],
        festivals=["vasant-panchami"],
        temples=["sringeri-sharada", "sharada-maihar"],
    ),
    story(
        slug="kali-born-of-wrath",
        title="Kali’s origin — the Mother who leapt from Durga’s brow",
        title_hi="काली का उद्गम — माँ जो दुर्गा के ललाट से जन्मीं",
        deity="kali",
        hook="When ordinary strength was not enough, a darker compassion stepped forward.",
        hook_hi="जब साधारण बल काफी न रहा, और गहरी करुणा आगे आई।",
        story_en=(
            "In the battle against blood-born demons, Durga’s fury condensed and Kali sprang forth — "
            "garlanded with truth’s severity, dancing on ego’s corpse in iconography that startles "
            "the polite mind. Her origin is not random violence; it is love refusing to let poison "
            "spread. Kali Puja and temple nights in Bengal keep that birth-fire tended with song "
            "and surrender."
        ),
        story_hi=(
            "रक्तबीज जैसे संकट में दुर्गा का क्रोध संघनित हुआ और काली प्रकट हुईं — सत्य की कठोर "
            "माला, अहंकार की छाती पर नृत्य की प्रतिमा जो सभ्य मन को चौंकाती है। उनका उद्गम अंधा "
            "हिंसा नहीं; प्रेम जो विष फैलने नहीं देता। बंगाल की काली पूजा और मंदिर रातें उसी "
            "जन्म-अग्नि को गान और समर्पण से जलाए रखती हैं।"
        ),
        detail_en=(
            "First movement: protection escalates when sweetness alone fails. Then the knot: "
            "devotees must not copy cinematic rage — Kali asks for the death of cruelty inside.\n\n"
            "Kalighat and other Shakti peethas hold her presence. At home, a single red flower "
            "and honest confession of anger can be a safe origin rite.\n\n"
            "Companion to the Raktabija telling; here we stay with how Kali appears."
        ),
        detail_hi=(
            "पहला चरण: जब केवल मिठास असफल हो, रक्षा तीव्र होती है। फिर भक्त सिनेमाई क्रोध न दोहराए।\n\n"
            "घर में एक लाल फूल और क्रोध का ईमानदार स्वीकार सुरक्षित उद्गम हो सकता है।"
        ),
        why="Kali Puja remembers the Mother born of protective wrath — offer surrender, not showmanship.",
        why_hi="काली पूजा रक्षक रोष से जन्मी माँ को याद करती है — समर्पण दें, तमाशा नहीं।",
        takeaway="Name one anger you will not feed today, and bow once in silence.",
        devotion=["kali-aarti", "kali-chalisa", "kali-puja-bengal-katha"],
        festivals=["navaratri", "diwali"],
        temples=["kalighat", "dakshineswar-kali", "tarapith"],
    ),
    story(
        slug="jagannath-neelamadhav-origin",
        title="Jagannath’s origin — from Neelamadhav to the wooden siblings of Puri",
        title_hi="जगन्नाथ का उद्गम — नीलमाधव से पुरी के दारुमय बंधु",
        deity="jagannath",
        hook="A secret hill deity became the Lord of the world — with unfinished arms of mercy.",
        hook_hi="गुप्त पहाड़ी देव जगत् के स्वामी बने — करुणा की अधूरी भुजाओं संग।",
        story_en=(
            "Odisha tellings speak of Neelamadhav worshipped in forest secrecy, then of king "
            "Indradyumna’s quest, Vishwakarma’s carving, and the siblings Jagannath, Balabhadra, "
            "and Subhadra in neem wood — forms left “incomplete” yet complete in grace. Rath Yatra "
            "parades that origin yearly: God who rides with the people. The wooden body teaches "
            "renewal — Nabakalebara — that holiness can be remade with tears and song."
        ),
        story_hi=(
            "ओडिशा कथा नीलमाधव की वन-गुप्त पूजा, फिर इंद्रद्युम्न की खोज, विश्वकर्मा की कारीगरी "
            "और नीम काष्ठ में जगन्नाथ-बलभद्र-सुभद्रा की बात कहती है — रूप “अधूरे” पर कृपा में पूरे। "
            "रथ यात्रा प्रतिवर्ष उसी उद्गम को जन-पथ पर लाती है। दारुमय शरीर नवकलवर सिखाता है — "
            "पवित्रता आँसू और गान से फिर रची जा सकती है।"
        ),
        detail_en=(
            "First movement: a king’s longing for public darshan. Then the knot: the carving "
            "stops at a mysterious moment — and faith accepts the unfinished as sacred.\n\n"
            "Companion to our neem-murti essay; this page centres the origin path to Puri.\n\n"
            "Respect living temple schedules; this is learning, not a replacement for official guidance."
        ),
        detail_hi=(
            "पहला चरण: सार्वजनिक दर्शन की राजा की तड़प। फिर कारीगरी रुकती है — और श्रद्धा अधूरे को "
            "पवित्र मानती है।\n\n"
            "यह पुरी-पथ का उद्गम केंद्रित पृष्ठ है।"
        ),
        why="Rath Yatra returns Jagannath’s origin to the streets — practice sharing space and patience in crowds.",
        why_hi="रथ यात्रा जगन्नाथ के उद्गम को सड़क पर लाती है — भीड़ में धैर्य और स्थान-साझा अभ्यास करें।",
        takeaway="Look at one unfinished project at home and treat it gently as still worthy.",
        devotion=["krishna-aarti", "vishnu-aarti"],
        festivals=["rath-yatra"],
        temples=["jagannath-puri"],
    ),
    story(
        slug="venkateswara-srinivasa-descent",
        title="Srinivasa’s descent — how Venkateswara came to Tirumala",
        title_hi="श्रीनिवास का अवतरण — वेंकटेश्वर तिरुमला कैसे आए",
        deity="venkateswara",
        hook="A Lord who borrowed for a wedding still stands on the hill to clear every sincere debt of worry.",
        hook_hi="विवाह हेतु ऋण लेने वाले प्रभु आज भी पहाड़ी पर खड़े हर चिंता-ऋण उतारते हैं।",
        story_en=(
            "Vaishnava katha of Kali Yuga tells how Vishnu as Srinivasa descended to the Tirumala "
            "hills, won Padmavati’s hand, and accepted Kubera’s loan for the wedding — a debt "
            "devotees help “repay” through offerings. The origin of Venkateswara / Balaji is thus "
            "both romance and responsibility: God who shares human struggle. The hill darshan "
            "remains one of India’s great pilgrim rivers."
        ),
        story_hi=(
            "कलियुग की वैष्णव कथा कहती है विष्णु श्रीनिवास रूप में तिरुमला आए, पद्मावती से विवाह "
            "रचाया, कुबेर से ऋण लिया — जिसे भक्त अर्पण से “चुकाने” में सहभागी होते हैं। वेंकटेश्वर / "
            "बालाजी का उद्गम प्रेम और जिम्मेदारी दोनों है: प्रभु जो मानवीय संघर्ष बाँटते हैं। पहाड़ी "
            "दर्शन भारत की बड़ी यात्री-नदियों में है।"
        ),
        detail_en=(
            "First movement: divine willingness to live under limits. Then the knot: commercial "
            "noise around donations must not erase the inner vow of gratitude.\n\n"
            "Companion pieces cover Kubera’s loan and Padmavati; here the descent-origin is central.\n\n"
            "Follow official temple guidance for visits; this page is home learning."
        ),
        detail_hi=(
            "पहला चरण: सीमाओं में जीने की दिव्य इच्छा। फिर गाँठ: दान के शोर में कृतज्ञता का व्रत न छूटे।\n\n"
            "यहाँ अवतरण-उद्गम केंद्र है।"
        ),
        why="A Tirumala vow often begins with Srinivasa’s descent story — keep promises small enough to fulfill.",
        why_hi="तिरुमला संकल्प अक्सर श्रीनिवास अवतरण से शुरू होता है — वचन इतने छोटे रखें कि पूरे हों।",
        takeaway="Write one financial or personal promise you will keep this month, and offer a silent namaskar.",
        devotion=["venkateswara-aarti", "vishnu-aarti"],
        festivals=["diwali", "akshaya-tritiya"],
        temples=["tirumala-venkateswara", "padmavathi-tiruchanur"],
    ),
    story(
        slug="annapurna-origin-kashi",
        title="Annapurna’s origin — the Mother who fed Shiva and the city of light",
        title_hi="अन्नपूर्णा का उद्गम — माँ जिन्होंने शिव और काशी को अन्न दिया",
        deity="annapurna",
        hook="When the Lord of yoga felt hunger, the Goddess arrived with a ladle of grace.",
        hook_hi="जब योगेश्वर को भूख लगी, देवी करछुल-सी कृपा लेकर आईं।",
        story_en=(
            "A beloved Kashi telling says Shiva once dismissed the world’s food as illusion; "
            "Parvati withdrew, and hunger taught even the ascetic. As Annapurna she returned with "
            "a golden ladle, feeding Shiva and reminding householders that anna is sacred. Her "
            "origin is the birth of kitchen holiness — temples and home stoves as one continuum."
        ),
        story_hi=(
            "काशी की प्रिय कथा कहती है शिव ने कभी अन्न को माया कहा; पार्वती हट गईं, भूख ने तपस्वी "
            "को भी सिखाया। अन्नपूर्णा बनकर स्वर्ण करछुल संग लौटीं, शिव को अन्न दिया, गृहस्थ को "
            "याद दिलाया — अन्न पवित्र है। उनका उद्गम रसोई की पवित्रता का जन्म है — मंदिर और चूल्हा "
            "एक धारा।"
        ),
        detail_en=(
            "First movement: philosophy without compassion empties the plate. Then the knot: "
            "feeding others becomes worship.\n\n"
            "Annapurna Kashi and other annadanam traditions keep this origin practical. At home, "
            "do not waste a grain today.\n\n"
            "Companion to “Annapurna feeds Shiva”; this page names her origin mood for the Annapurna deity hub."
        ),
        detail_hi=(
            "पहला चरण: बिना करुणा का सिद्धांत थाली खाली करता है। फिर दूसरों को खिलाना पूजा बनता है।\n\n"
            "आज एक कण भी व्यर्थ न करें।"
        ),
        why="Kitchen prayers and temple annadanam remember Annapurna’s origin — cook one meal with attention.",
        why_hi="रसोई प्रार्थना और अन्नदान अन्नपूर्णा उद्गम को याद करते हैं — एक भोजन ध्यान से बनाएँ।",
        takeaway="Share or thoughtfully pack leftover food instead of throwing it away tonight.",
        devotion=["annapurna-aarti", "devi-aarti"],
        festivals=["navaratri", "diwali"],
        temples=["annapurna-kashi", "annapurna-temple-indore", "kashi-vishwanath"],
    ),
    story(
        slug="santoshi-mata-origin",
        title="Santoshi Mata’s origin — contentment born for ordinary homes",
        title_hi="संतोषी माता का उद्गम — साधारण घरों के लिए जन्मा संतोष",
        deity="santoshi",
        hook="A Mother who asked for little — fried gram, jaggery, and a peaceful Friday.",
        hook_hi="माँ जिन्होंने कम माँगा — चने, गुड़, और शांत शुक्रवार।",
        story_en=(
            "Modern-popular Hindu devotion tells of Santoshi Mata as the goddess of contentment, "
            "often linked in folk telling to Ganesha’s family grace. Her origin for millions is "
            "the Friday vrat: simple food, simple story, refusal of prideful feasting. Whether "
            "one reads older Puranic lists or newer household katha, the ethical birth is clear — "
            "santosh (contentment) as a deity you can practice in a small flat."
        ),
        story_hi=(
            "आधुनिक-लोक हिंदू भक्ति संतोषी माता को संतोष की देवी कहती है, लोककथा में गणेश-परिवार "
            "की कृपा से जुड़ी। करोड़ों के लिए उनका उद्गम शुक्रवार व्रत है: सादा भोजन, सादी कथा, "
            "अहंकारी भोज से इनकार। पुरानी सूची पढ़ें या घर की नई कथा — नैतिक जन्म स्पष्ट है: "
            "संतोष वह देवता जिसे छोटे घर में भी जिया जा सके।"
        ),
        detail_en=(
            "First movement: spirituality scaled to ordinary budgets. Then the knot: do not "
            "turn the vrat into social competition.\n\n"
            "Keep claims gentle and AdSense-safe — no guaranteed miracles, only disciplined hope.\n\n"
            "Friday katha listening is the living origin rite."
        ),
        detail_hi=(
            "पहला चरण: अध्यात्म साधारण बजट पर। फिर व्रत को दिखावे की होड़ न बनाएँ।\n\n"
            "चमत्कार की गारंटी नहीं — अनुशासित आशा।"
        ),
        why="Friday Santoshi vrat revisits her origin as contentment — keep the meal simple and the speech kind.",
        why_hi="शुक्रवार संतोषी व्रत संतोष के उद्गम पर लौटता है — भोजन सादा, वाणी कोमल रखें।",
        takeaway="Skip one unnecessary purchase this week and note how light that feels.",
        devotion=["santoshi-chalisa", "santoshi-mata-vrat-katha"],
        festivals=["santoshi-mata"],
        temples=["santoshi-mata-jodhpur", "santoshi-mata-delhi"],
    ),
    story(
        slug="brahma-lotus-birth",
        title="Brahma’s birth from the lotus — creator rising from Vishnu’s rest",
        title_hi="कमल से ब्रह्मा का जन्म — विष्णु के विश्राम से उठा स्रष्टा",
        deity="brahma",
        hook="Creation began as a flower opening on the waters of eternity.",
        hook_hi="सृष्टि उस फूल से शुरू हुई जो अनंत जल पर खिला।",
        story_en=(
            "A central telling says Brahma appeared upon the lotus that grew from Vishnu’s navel "
            "as the Lord rested on Shesha. Tasked with creating worlds, Brahma’s origin is "
            "dependency wrapped in dignity — even the creator begins as someone’s child of grace. "
            "Pushkar’s rare Brahma temple keeps this birth in pilgrimage geography, with a reminder "
            "to create without claiming final ownership."
        ),
        story_hi=(
            "केंद्रीय कथा कहती है शेष पर विश्राम करते विष्णु की नाभि-कमल पर ब्रह्मा प्रकट हुए। "
            "लोक रचने का दायित्व पाकर भी उनका उद्गम गरिमा में लिपटी निर्भरता है — स्रष्टा भी कृपा "
            "का बालक है। पुष्कर का दुर्लभ ब्रह्मा मंदिर इस जन्म को तीर्थ-भूगोल में रखता है, याद "
            "दिलाता है: रचो, पर अंतिम स्वामित्व का दावा मत करो।"
        ),
        detail_en=(
            "First movement: creativity as assignment, not ego throne. Then the knot: stories "
            "of Brahma’s pride and lessons appear in other tellings — hold them lightly.\n\n"
            "At home, beginning any new project with a short prayer echoes lotus-birth humility.\n\n"
            "Companion to Vishnu-on-Shesha; here Brahma is the subject."
        ),
        detail_hi=(
            "पहला चरण: रचना असाइनमेंट है, अहंकार का सिंहासन नहीं।\n\n"
            "नया कार्य शुरू करते समय छोटी प्रार्थना कमल-जन्म की नम्रता है।"
        ),
        why="A visit-in-spirit to Pushkar or a creative Saturday can honour Brahma’s lotus birth — start clean.",
        why_hi="पुष्कर की मानसिक यात्रा या रचनात्मक शनिवार ब्रह्मा के कमल-जन्म का सम्मान हो सकता है — स्वच्छ आरंभ करें।",
        takeaway="Begin one creative task today only after tidying the desk for two minutes.",
        devotion=["gayatri-aarti", "gayatri-chalisa", "vishnu-aarti"],
        festivals=["guru-purnima"],
        temples=["brahma-temple-pushkar"],
    ),
    story(
        slug="mangal-graha-origin",
        title="Mangal’s origin — the red planet’s birth in sacred imagination",
        title_hi="मंगल का उद्गम — पवित्र कल्पना में रक्तवर्ण ग्रह का जन्म",
        deity="mangal",
        hook="Earth and fire met in a warrior glow — and Tuesday learned its colour.",
        hook_hi="पृथ्वी और अग्नि योद्धा-ज्योति में मिले — और मंगलवार ने अपना रंग सीखा।",
        story_en=(
            "Folk-astral tellings give Mangal (Mars) origins tied to earth and divine spark — "
            "sometimes linked to Shiva’s energy or Bhumi’s strength — yielding a deity of courage, "
            "land, and disciplined force. His “birth” for householders is Tuesday’s mood: act "
            "bravely, avoid needless quarrel. Temples like Amalner’s Mangal graha shrine keep "
            "that planetary personhood in living worship."
        ),
        story_hi=(
            "लोक-ज्योतिष कथाएँ मंगल को पृथ्वी और दिव्य चिंगारी से जन्म देती हैं — कभी शिव-तेज, "
            "कभी भूमि-बल से जुड़ी — साहस, भूमि और अनुशासित शक्ति के देव। गृहस्थ के लिए उनका "
            "“जन्म” मंगलवार का भाव है: साहस से कर्म, बिना जरूरत के झगड़ा नहीं। अमलगेर जैसे "
            "मंगल ग्रह मंदिर उस ग्रह-व्यक्तित्व को जीवित पूजा में रखते हैं।"
        ),
        detail_en=(
            "First movement: courage as sacred colour. Then the knot: aggression without dharma "
            "is not Mangal’s teaching.\n\n"
            "Keep astrology claims modest for AdSense safety — focus on Tuesday charity and calm strength.\n\n"
            "Amalner and regional Mangal shrines are pilgrimage notes, not medical or fortune guarantees."
        ),
        detail_hi=(
            "पहला चरण: साहस पवित्र रंग है। फिर बिना धर्म की आक्रामकता मंगल की शिक्षा नहीं।\n\n"
            "ज्योतिष दावे संयत रखें — मंगलवार दान और शांत बल पर ध्यान दें।"
        ),
        why="Tuesday Mangal remembrance returns to his fiery origin — choose one brave, non-harmful action.",
        why_hi="मंगलवार स्मरण अग्नि-उद्गम पर लौटता है — एक साहसी, अहिंसक कर्म चुनें।",
        takeaway="On Tuesday, finish one postponed task before noon.",
        devotion=["mangala-gauri-vrat-katha", "hanuman-chalisa"],
        festivals=["hanuman-jayanti"],
        temples=["mangal-dev-grah-amalner"],
    ),
]


def fix_placeholders(items: list[dict]) -> None:
    """Repair any festival placeholders left from drafting."""
    for s in items:
        fests = s.get("relatedFestivals") or []
        # Remove bogus / false entries
        cleaned = [x for x in fests if isinstance(x, str) and x and x != "ashadi" and x != "mangala"]
        if s["slug"] == "vitthal-vithoba-origin" and "kartik-purnima" not in cleaned:
            cleaned = ["kartik-purnima"]
        if s["slug"] == "mangal-graha-origin" and "hanuman-jayanti" not in cleaned:
            cleaned = ["hanuman-jayanti"]
        s["relatedFestivals"] = cleaned


def main() -> None:
    fix_placeholders(NEW)
    data = json.loads(STORIES_PATH.read_text(encoding="utf-8"))
    existing = {s["slug"] for s in data["stories"]}
    existing_deity_origin = {
        s["slug"]
        for s in data["stories"]
        if "origin" in (s.get("tags") or [])
        or any(
            k in s["slug"]
            for k in ("birth", "origin", "appearance", "lingodbhava", "ocean-birth", "descent")
        )
    }

    added = []
    skipped = []
    for s in NEW:
        if s["deity"] in SKIP_DEITIES:
            skipped.append((s["slug"], f"deity {s['deity']} already has strong origin story"))
            continue
        if s["slug"] in existing:
            skipped.append((s["slug"], "slug exists"))
            continue
        data["stories"].append(s)
        added.append(s["slug"])

    STORIES_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Added {len(added)} origin stories:")
    for sl in added:
        print(" ", sl)
    if skipped:
        print("Skipped:")
        for sl, why in skipped:
            print(f"  {sl} ({why})")
    print("Total stories now:", len(data["stories"]))
    print("Note: krishna / ayyappa / sai already covered — not duplicated.")
    _ = existing_deity_origin  # reserved for future audits


if __name__ == "__main__":
    main()
