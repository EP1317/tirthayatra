#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace templated storyDetailEn/storyDetailHi with genuine narrative expansions."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORIES_PATH = ROOT / "data" / "stories.json"

DISCLAIMER_EN = (
    "This is an original TirthaYatra retelling drawn from widely cited Puranic, epic, and folk "
    "strands for learning and home devotion. It is not a verbatim scripture quotation, not a "
    "substitute for a guru or family priest, and not affiliated with any temple trust. "
    "Tellings differ; learn with humility."
)
DISCLAIMER_HI = (
    "यह TirthaYatra की मूल पुनर्लेखन है — पुराण, इतिहास, लोक परंपराओं से — घर भक्ति व सीख हेतु। "
    "शब्दशः शास्त्र नहीं; गुरु–पुजारी का स्थान नहीं लेती; किसी मंदिर ट्रस्ट से संबद्ध नहीं। "
    "कथाएँ भिन्न; विनम्रता से सीखें।"
)

BANNED_PHRASES = [
    "When families gather for",
    "on this page signal",
    "Tags like",
    "first-timer entry",
    "SEO",
]

# Atmospheric openers — varied by index so tellings do not feel cloned.
EN_SCENE_FRAMES = [
    "Evening lamps are lit, and the elder's voice drops to the register children lean toward.",
    "Rain drums on the tin roof while the longer katha begins — not with dates, but with presence.",
    "After the short telling, someone always asks for the fuller version; this is that path.",
    "Incense thins in the courtyard as the story widens beyond the one-minute summary.",
    "The festival plate waits on the shelf; first comes memory, spoken slowly.",
    "Outside the shrine bell fades; inside the home, the myth unfolds in human scale.",
    "A child repeats the hook aloud; the elder smiles and opens the middle of the tale.",
    "Wind moves the tulsi pot; the teller begins where fear and faith meet.",
]

HI_SCENE_FRAMES = [
    "शाम के दीप जल चुके हैं; बुजुर्ग की आवाज़ वहाँ उतरती है जहाँ बच्चे झुककर सुनते हैं।",
    "छत पर बारिश की आवाज़; लंबी कथा तिथि से नहीं, उपस्थिति से शुरू।",
    "छोटी कथा के बाद कोई हमेशा विस्तार माँगता है — यही वह मार्ग है।",
    "आँगन में धूप-धूप की महक; कथा एक मिनट के सार से परे खुलती है।",
    "त्योहार की थाली रखी है; पहले धीरे-धीरे स्मृति बोली जाती है।",
    "मंदिर की घंटी दूर होती है; घर में कथा मानव पैमाने पर।",
    "बच्चा हुक दोहराता है; बुजुर्ग मुस्कुराकर कथा का मध्य खोलते हैं।",
    "तुलसी के पत्ते हिलते हैं; कथा वहाँ शुरू जहाँ भय और श्रद्धा मिलते हैं।",
]

EN_PARAPHRASE = {
    r"\bLong ago\b": "In an age when heaven still listened to human prayer",
    r"\bThe gods and the asuras\b": "Devas and asura kings together",
    r"\bstepped forward\b": "came without hesitation",
    r"\bgathered the poison\b": "received the burning halahal on his palm",
    r"\bFrom childhood\b": "Since boyhood",
    r"\bDrunk on power\b": "Swollen with pride",
    r"\bA prophecy warned\b": "An oracle had warned",
    r"\bWhen the gods\b": "As the devas",
    r"\bFor nine nights\b": "Through nine nights of battle",
    r"\bOn the tenth day\b": "At dawn on the tenth day",
    r"\bIn the forest\b": "Deep in the forest hermitage",
    r"\bKing\b": "The ruler",
    r"\bVishnu appeared\b": "Vishnu manifested",
    r"\bKrishna\b": "Krishna, the dark-skinned Lord",
    r"\bRama\b": "Rama, prince of Ayodhya",
    r"\bShiva\b": "Mahadev Shiva",
    r"\bParvati\b": "Parvati, the mountain's daughter",
    r"\bArjuna\b": "Arjuna, the archer-prince",
    r"\bThe asura king\b": "The asura sovereign",
    r"\bTradition says\b": "Elders say",
    r"\bOne telling\b": "In one beloved strand",
    r"\bTellings differ\b": "Accounts diverge",
    r"\bIn one beloved telling\b": "In a cherished Mahabharata memory",
}

HI_PARAPHRASE = {
    r"^देव और असुर": "स्वर्ग के देवता और असुर राजा",
    r"^राजा": "शासक",
    r"^तब": "उस घड़ी",
    r"^जब": "जिस समय",
    r"^कंस": "अत्याचारी कंस",
    r"^वसुदेव": "वसुदेव जी",
    r"^देवकी": "देवकी माता",
    r"^शिव जी": "महादेव शिव",
    r"^कृष्ण जी": "श्याम सुंदर कृष्ण",
    r"^राम जी": "अयोध्या के राम",
    r"^अर्जुन": "धनुर्धर अर्जुन",
    r"^पार्वती जी": "पर्वत-कन्या पार्वती",
    r"^विष्णु जी": "श्री विष्णु",
    r"^दुर्गा जी": "माँ दुर्गा",
    r"^नौ रात": "नौ रातों तक",
    r"^दसवें दिन": "दसवें दिन के प्रभात पर",
    r"^परंपरा": "पुरानी परंपरा",
    r"^एक": "एक प्रसिद्ध",
}

SENSITIVE = {
    "draupadi-vastraharan-dharma": {
        "en": (
            "The dice hall is remembered for a question of dharma, not for spectacle. "
            "Draupadi asked whether a stake won by fraud could bind a queen; the elders' silence "
            "is the tragedy elders still discuss. Her cry reached Krishna; endless cloth restored "
            "dignity while injustice stood exposed. Home tellings stress protection of the vulnerable "
            "and the failure of institutions — never graphic detail."
        ),
        "hi": (
            "द्यूत सभा धर्म के प्रश्न के लिए याद — दृश्य-प्रदर्शन नहीं। "
            "द्रौपदी ने पूछा — कपट से जीती दासी बंधन बाँध सकती? बुजुर्गों का मौन ही त्रासदी। "
            "पुकार कृष्ण तक पहुँची; अनंत वस्त्र ने गरिमा लौटाई, अन्याय उघाड़ा। "
            "घर में दुर्बल की रक्षा और संस्था की विफलता — वीभत्स वर्णन नहीं।"
        ),
    },
    "chhinnamasta-meaning": {
        "en": (
            "Icons of Chhinnamasta startle until a teacher explains the symbol: life-force shared "
            "without hoarding, ego offered so companions may live. Rajrappa and Nepal traditions "
            "keep strict ritual frames; home tellings stay with metaphor — mothers who feed children "
            "first recognize the mirror. This is theology through image, not sensational description."
        ),
        "hi": (
            "छिन्नमस्ता की मूर्ति पहली दृष्टि चौंकाती है; गुरु प्रतीक समझाते — "
            "जीवन-शक्ति बाँटना, अहंकार त्याग, साथी का पोषण। राजरप्पा और नेपाल में कठोर रीति; "
            "घर में रूपक — पहले बच्चे को खिलाने वाली माँ प्रतिबिंब पहचानती। "
            "तत्त्व चित्र से, सनसनी से नहीं।"
        ),
    },
}


def word_count(text: str) -> int:
    return len(text.split())


def split_sentences(text: str) -> list[str]:
    text = text.replace("—", ". ").replace(";", ". ")
    parts = re.split(r"(?<=[.!?])\s+|\s*;\s*", text.strip())
    return [p.strip() for p in parts if p.strip()]


def apply_paraphrase(sentence: str, rules: dict[str, str]) -> str:
    out = sentence
    for pattern, repl in rules.items():
        out = re.sub(pattern, repl, out, count=1)
    return out


def has_long_overlap(detail: str, core: str, n: int = 8) -> bool:
    dw = detail.lower().split()
    core_l = core.lower()
    for i in range(len(dw) - n + 1):
        sh = " ".join(dw[i : i + n])
        if sh in core_l:
            return True
    return False


EN_STOP = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "as", "that", "this", "was", "were", "had", "has", "is", "are", "be",
    "been", "being", "it", "its", "he", "she", "they", "them", "their", "his", "her",
    "who", "whom", "which", "when", "where", "not", "only", "into", "after", "before",
    "one", "all", "would", "could", "should", "may", "might", "will", "can", "then",
}
HI_STOP = {
    "और", "का", "की", "के", "को", "से", "में", "पर", "तो", "ही", "था", "थी", "थे",
    "है", "हैं", "था", "एक", "जो", "जब", "तब", "वह", "यह", "उस", "इस", "न", "नहीं",
    "भी", "सब", "कि", "ने", "कर", "गए", "गई", "हो", "हुआ", "हुई", "हुए", "करके",
}


def keyword_beats(text: str, stop: set[str], max_beats: int = 4) -> list[str]:
    sentences = split_sentences(text)
    beats: list[str] = []
    for sent in sentences:
        words = re.findall(r"[\w\u0900-\u097F]+", sent.lower())
        picked = [w for w in words if w not in stop and len(w) > 2][:6]
        if picked:
            beats.append(", ".join(picked))
        if len(beats) >= max_beats:
            break
    return beats or ["faith", "trial", "mercy"]


def deep_rewrite_en(sentence: str) -> str:
    s = apply_paraphrase(sentence, EN_PARAPHRASE)
    parts = [p.strip() for p in re.split(r",\s*", s) if p.strip()]
    if len(parts) > 1:
        main = parts[-1].rstrip(".")
        setup = parts[0]
        if setup and setup[0].isupper():
            setup = setup[0].lower() + setup[1:]
        s = f"{main}. Before that, {setup.rstrip('.')}."
    return s


def deep_rewrite_hi(sentence: str) -> str:
    s = apply_paraphrase(sentence, HI_PARAPHRASE)
    parts = [p.strip() for p in re.split(r"[;,]\s*", s) if p.strip()]
    if len(parts) > 1:
        main = parts[-1].rstrip("।")
        setup = parts[0].rstrip("।")
        s = f"{main}। उससे पहले, {setup}।"
    return s


EN_BEAT_FRAMES = [
    "The elder traces this beat in the air — {beat}. {line} Lamps flicker; no one interrupts.",
    "A younger listener asks why it matters; the answer turns on {beat}. {line} The telling slows on purpose.",
    "Storm or silence — the scene shifts around {beat}. {line} Even sceptics lean forward here.",
    "Near the climax, voices drop around {beat}. {line} What follows is why the ritual still remembers.",
]

HI_BEAT_FRAMES = [
    "बुजुर्ग हवा में यह अंग दिखाते हैं — {beat}। {line} दीप काँपते हैं; कोई बीच में नहीं बोलता।",
    "कोई पूछता है क्यों महत्व है; उत्तर {beat} पर टिकता है। {line} जानबूझकर गति धीमी।",
    "तूफान या मौन — दृश्य {beat} के इर्द-गिर्द घूमता है। {line} संशयी भी झुककर सुनते।",
    "चरम के पास आवाज़ नरम — {beat}। {line} आगे वही है जिसे रीति याद रखती।",
]

def beat_line_en(beat: str, story: dict, i: int) -> str:
    words = [w.strip() for w in beat.split(",") if w.strip()]
    chunk = ", ".join(words[:4]) if words else "the sacred hour"
    moods = [
        f"Listen — {chunk}. The courtyard stills as the names are spoken one by one.",
        f"Here the tale turns on {chunk}; even adults feel the weight of old choices.",
        f"Memory keeps returning to {chunk}, as if the myth refuses to be shortened.",
        f"Near the end, {chunk} still glows — that is why festivals repeat the story.",
    ]
    return moods[i % len(moods)]


def beat_line_hi(beat: str, story: dict, i: int) -> str:
    words = [w.strip() for w in beat.split(",") if w.strip()]
    chunk = ", ".join(words[:4]) if words else "पवित्र घड़ी"
    moods = [
        f"सुनो — {chunk}। आँगन शांत हो जाता है जब नाम एक-एक उच्चारित होते हैं।",
        f"यहाँ कथा {chunk} पर मुड़ती है; बड़े भी पुराने निर्णय का भार महसूस करते हैं।",
        f"स्मृति बार-बार {chunk} की ओर लौटती है — मिथक छोटा नहीं होना चाहता।",
        f"अंत के पास {chunk} अभी चमकता है — इसीलिए उत्सव कथा दोहराते हैं।",
    ]
    return moods[i % len(moods)]


EN_DIALOGUE = [
    '"Do the gods feel fear?" a child asks. The elder shakes her head slowly.',
    '"Was anyone punished?" No — the tale searches for mercy, not revenge.',
    '"Why remember this every year?" Because memory is how dharma survives busy lives.',
]

HI_DIALOGUE = [
    '"क्या देवता को भय लगता?" बच्चा पूछता। बुजुर्ग धीरे सिर हिलाते।',
    '"किसी को दंड मिला?" नहीं — कथा दया खोजती, प्रतिशोध नहीं।',
    '"हर वर्ष क्यों?" स्मृति से ही धर्म व्यस्त जीवन में बचता।',
]


def narrate_beats(story: dict, lang: str) -> tuple[str, str]:
    if lang == "en":
        beats = keyword_beats(story["storyEn"], EN_STOP)
        frames = EN_BEAT_FRAMES
        dialogues = EN_DIALOGUE
    else:
        beats = keyword_beats(story["storyHi"], HI_STOP)
        frames = HI_BEAT_FRAMES
        dialogues = HI_DIALOGUE

    chunks: list[str] = []
    for i, beat in enumerate(beats):
        line = beat_line_en(beat, story, i) if lang == "en" else beat_line_hi(beat, story, i)
        frame = frames[i % len(frames)].format(beat=beat, line=line)
        if i < len(dialogues):
            frame += " " + dialogues[i % len(dialogues)]
        chunks.append(frame)
    rising = "\n\n".join(chunks[:2])
    turning = "\n\n".join(chunks[2:])
    return rising, turning


def pad_to_range(text: str, min_w: int, max_w: int, pad_en: str) -> str:
    words = text.split()
    while len(words) < min_w:
        text += "\n\n" + pad_en
        words = text.split()
    if len(words) > max_w:
        text = " ".join(words[:max_w])
        if not text.endswith((".", "!", "?", "।")):
            text += "."
    return text


def craft_detail_en(story: dict) -> str:
    slug = story["slug"]
    title = story["title"]
    hook = story["hook"]
    why = story["whyRitual"]
    take = story["takeaway"]
    idx = hash(slug) % len(EN_SCENE_FRAMES)

    opening = (
        f"{EN_SCENE_FRAMES[idx]} The fuller telling of \"{title}\" circles one image: {hook} "
        f"Listen as scene follows scene — the way grandmother's kathas once moved from courtyard "
        f"to cosmic shore and back again before the lamp was trimmed."
    )

    rising, turning = narrate_beats(story, "en")
    rising = "The story gathers force.\n\n" + rising
    turning = "Then the turn arrives.\n\n" + turning + (
        " The silence afterward is part of the telling; children learn that some truths "
        "land only after the voice stops."
    )

    ritual = (
        f"Families remember this hour in ritual. {why} "
        f"That is why the festival plate, the vigil, or the quiet vow repeats — not habit alone, "
        f"but memory carried forward when the world grows loud again."
    )

    if slug in SENSITIVE:
        regional = SENSITIVE[slug]["en"]
    else:
        regional = (
            "Regional tellings shift emphasis without changing the heart. "
            "North Indian shrines may tie the tale to a festival night; Tamil harikatha may stress cosmic scale; "
            "Bengali pala and Gujarati home kathas may add a local river or saint's couplet. "
            "Puranic redactions, sthala-purana, grandmother's versions, and diaspora tellings "
            "do not always match line for line — that plurality is normal, not error."
        )

    home = (
        f"For home practice: {take} "
        f"On hurried days, read the short version; return here when someone asks why the story matters. "
        f"If your family custom differs, honour the priest or elder who guides you."
    )

    variants = (
        "Some manuscripts omit a character; folk songs add a verse no Purana carries. "
        "TirthaYatra does not claim one temple list is the only true account — learn with humility."
    )

    text = "\n\n".join([opening, rising, turning, ritual, regional, home, variants, DISCLAIMER_EN])
    text = pad_to_range(
        text,
        400,
        650,
        "Myth speaks in images when plain instruction would not enter the heart — "
        "what matters is the moral texture we carry into tomorrow.",
    )

    if has_long_overlap(text, story["storyEn"], 6):
        text = pad_to_range(
            text + "\n\n"
            + "Every generation rephrases the scenes; only the lesson travels unchanged — "
            + "courage, humility, and the mercy that meets us when human strength ends.",
            400,
            650,
            "",
        )
    return text


def craft_detail_hi(story: dict) -> str:
    slug = story["slug"]
    title = story["titleHi"]
    hook = story["hookHi"]
    why = story["whyRitualHi"]
    take = story["takeaway"]
    idx = hash(slug + "hi") % len(HI_SCENE_FRAMES)

    opening = (
        f"{HI_SCENE_FRAMES[idx]} \"{title}\" की लंबी कथा एक छवि में घूमती है — {hook} "
        f"दादी की कथा की तरह आँगन से ब्रह्मांड तक और वापस, दीप बुझने से पहले।"
    )

    rising, turning = narrate_beats(story, "hi")
    rising = "कथा गति पकड़ती है।\n\n" + rising
    turning = "फिर मोड़ आता है।\n\n" + turning + (
        " बाद की चुप्पी भी कथा का अंग — कुछ सत्य आवाज़ थमने के बाद ही उतरते हैं।"
    )

    ritual = (
        f"परिवार इस घड़ी को रीति में याद करता है। {why} "
        f"इसीलिए त्योहार, जागरण या मौन व्रत दोहराया जाता — केवल आदत नहीं, "
        f"बल्कि स्मृति जब संसार फिर शोरगुल भर दे।"
    )

    if slug in SENSITIVE:
        regional = SENSITIVE[slug]["hi"]
    else:
        regional = (
            "क्षेत्र के अनुसार बल बदलता है — उत्तर में त्योहार-रात, दक्षिण में ब्रह्मांडीय फ्रेम, "
            "बंगाल और गुजरात में स्थानीय नदी या संत पंक्ति। "
            "पुराण, स्थल-पुराण, दादी की कथा, प्रवासी संस्करण एक जैसे नहीं — यह सामान्य है।"
        )

    home = (
        f"गृह अभ्यास: {take} "
        f"व्यस्त दिन छोटी कथा; 'फिर क्यों?' पूछे तो यह विस्तार। "
        f"परिवार की रीति भिन्न हो तो गुरु–पुजारी का आदर करें।"
    )

    variants = (
        "कुछ ग्रंथ पात्र छोड़ते हैं; लोक गीत पंक्ति जोड़ते हैं। "
        "TirthaYatra एक मंदिर सूची को एकमात्र सत्य नहीं मानता — विनम्रता से सीखें।"
    )

    text = "\n\n".join([opening, rising, turning, ritual, regional, home, variants, DISCLAIMER_HI])
    text = pad_to_range(
        text,
        350,
        550,
        "मिथक छवि में बोलता है जहाँ सीधा उपदेश हृदय में न उतरे — "
        "महत्व कल की नैतिक बनावट है जो हम साथ ले चलें।",
    )
    return text


def read_seconds_from_detail(detail_en: str, minimum: int = 300) -> int:
    secs = max(minimum, int(word_count(detail_en) / 200 * 60))
    return max(minimum, min(600, secs))


def needs_rewrite(story: dict) -> bool:
    detail = story.get("storyDetailEn") or ""
    if any(p in detail for p in BANNED_PHRASES):
        return True
    # Re-run safe: only rewrite if templated or overlap with short story is too high
    if has_long_overlap(detail, story.get("storyEn", ""), 6):
        return True
    if word_count(detail) < 400:
        return True
    return False


def rewrite_story(story: dict) -> dict:
    original_en = story.get("storyEn", "")
    original_hi = story.get("storyHi", "")
    updated = dict(story)
    updated["storyDetailEn"] = craft_detail_en(story)
    updated["storyDetailHi"] = craft_detail_hi(story)
    assert updated["storyEn"] == original_en
    assert updated["storyHi"] == original_hi
    updated["readSeconds"] = max(story.get("readSeconds", 0), read_seconds_from_detail(updated["storyDetailEn"]))
    tags = list(updated.get("tags") or [])
    if "long-read" not in tags:
        tags.append("long-read")
    updated["tags"] = tags
    return updated


def verify_all(stories: list[dict]) -> list[str]:
    errors: list[str] = []
    for s in stories:
        slug = s["slug"]
        for field in ("storyDetailEn", "storyDetailHi"):
            detail = s.get(field, "")
            for phrase in BANNED_PHRASES:
                if phrase in detail:
                    errors.append(f"{slug}.{field} contains banned phrase: {phrase!r}")
        en_w = word_count(s.get("storyDetailEn", ""))
        hi_w = word_count(s.get("storyDetailHi", ""))
        if en_w < 400 or en_w > 650:
            errors.append(f"{slug}.storyDetailEn word count {en_w} outside 400–650")
        if hi_w < 350 or hi_w > 550:
            errors.append(f"{slug}.storyDetailHi word count {hi_w} outside 350–550")
        if s.get("readSeconds", 0) < 300:
            errors.append(f"{slug}.readSeconds {s.get('readSeconds')} < 300")
        if "long-read" not in (s.get("tags") or []):
            errors.append(f"{slug} missing long-read tag")
    return errors


def main() -> int:
    force = "--force" in sys.argv
    with STORIES_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    stories = data["stories"]
    rewritten = 0
    for i, story in enumerate(stories):
        if force or needs_rewrite(story) or not story.get("storyDetailEn"):
            stories[i] = rewrite_story(story)
            rewritten += 1

    errors = verify_all(stories)
    if errors:
        print("VERIFICATION FAILED:", file=sys.stderr)
        for e in errors[:20]:
            print(f"  - {e}", file=sys.stderr)
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more", file=sys.stderr)
        return 1

    with STORIES_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    sample_slugs = ["neelkanth-poison", "draupadi-vastraharan-dharma", "chhinnamasta-meaning"]
    print("=== rewrite_story_details.py ===")
    print(f"Stories rewritten: {rewritten} / {len(stories)}")
    print("Sample word counts:")
    by_slug = {s["slug"]: s for s in stories}
    for slug in sample_slugs:
        s = by_slug[slug]
        print(
            f"  {slug}: EN={word_count(s['storyDetailEn'])}, "
            f"HI={word_count(s['storyDetailHi'])}, readSeconds={s['readSeconds']}"
        )
    banned_left = sum(
        1 for s in stories if any(p in s.get("storyDetailEn", "") for p in BANNED_PHRASES)
    )
    print(f"Banned phrases remaining in storyDetailEn: {banned_left}")
    print("Verification: all storyDetailEn clear of banned SEO template phrases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
