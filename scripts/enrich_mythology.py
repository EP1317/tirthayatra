#!/usr/bin/env python3
"""
Enrich every temple with structured mythology:
  - mythologySignificance (scriptural / pan-Indian significance)
  - localBeliefs (sthala-purana / regional devotion)
Drawn from widely recorded epic/Puranic and pilgrimage traditions.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLES = ROOT / "data" / "temples"

DISCLAIMER_NOTE = (
    "Accounts summarised from widely cited Puranic, epic, and pilgrimage traditions; "
    "local tellings may differ."
)

# Curated expansions for well-documented shrines (reliable traditional sources).
CURATED: dict[str, dict[str, str]] = {
    "kedarnath": {
        "mythologySignificance": (
            "Kedarnath is counted among the twelve Jyotirlingas — foremost seats where Shiva is "
            "worshipped as a pillar of light (jyoti). In the Mahabharata–linked Garhwal tradition, "
            "the Pandavas sought Shiva after the Kurukshetra war. Shiva, avoiding them in the form "
            "of a bull, submerged into the earth; the hump remaining at Kedarnath became the object "
            "of worship. The Skanda Purana and later Himalayan mahatmya literature celebrate this "
            "landscape as part of Shiva’s Himalayan presence.\n\n"
            "Kedarnath also belongs to the Uttarakhand Chota Char Dham and to the Panch Kedar set. "
            "It is not one of Adi Shankaracharya’s four pan-India Char Dham seats (Badrinath, Dwarka, "
            "Puri, Rameswaram)."
        ),
        "localBeliefs": (
            "Garhwal pilgrims regard the rocky shrine and surrounding peaks as living presence of "
            "Shiva. Adi Shankaracharya is traditionally linked with the temple’s living monastic "
            "framework and a samadhi site nearby. In winter, when snow closes the high shrine, "
            "worship continues at Ukhimath — a seasonal belief that the deity ‘moves’ with the "
            "community.\n\n"
            "Many devotees treat the trek itself as tapasya. Local lore also connects nearby "
            "Panch Kedar temples to different parts of Shiva’s bull-form."
        ),
        "scriptureLinks": [
            "Mahabharata (Pandava–Shiva tradition)",
            "Shiva Purana / Jyotirlinga lists",
            "Skanda Purana Himalayan mahatmya traditions",
        ],
    },
    "somnath": {
        "mythologySignificance": (
            "Somnath is traditionally listed as the first among the twelve Jyotirlingas. Puranic "
            "narrative (especially Chandra–Soma traditions in the Shiva Purana cycle) tells that "
            "the Moon god, cursed and fading, performed penance here; Shiva restored him, and the "
            "place became Somnath — ‘Lord of the Moon’. The Prabhas Khanda traditions of the "
            "Skanda Purana further sanctify the Prabhas coast as a major tirtha."
        ),
        "localBeliefs": (
            "Coastal Gujarat devotion remembers Somnath as a shrine repeatedly rebuilt across "
            "centuries — a symbol of enduring Shaiva faith by the Arabian Sea. Evening aarti by "
            "the shore and the sound-and-light narratives told to pilgrims reinforce the Chandra "
            "penance story in popular memory.\n\n"
            "Nearby Bhalka Tirth is linked in local Krishna-lila geography, so many pilgrims "
            "experience Somnath within a wider Saurashtra sacred circuit."
        ),
        "scriptureLinks": [
            "Shiva Purana (Soma / Chandra penance)",
            "Skanda Purana — Prabhas Khanda traditions",
            "Jyotirlinga pilgrimage lists",
        ],
    },
    "rameswaram": {
        "mythologySignificance": (
            "Rameswaram’s Ramanathaswamy temple is both a Jyotirlinga and a seat of Adi "
            "Shankaracharya’s Char Dham. In the Ramayana tradition, Rama worshipped Shiva here "
            "before (and in some tellings after) the battle with Ravana, installing a lingam on "
            "the seashore. The temple thus joins Shaiva Jyotirlinga theology with the Ramayana’s "
            "geography of exile, devotion, and return."
        ),
        "localBeliefs": (
            "Pilgrims bathe in the temple’s twenty-two theerthams before darshan — a ritual "
            "sequence believed to purify body and mind. Local belief holds that the corridors "
            "and wells mark Rama’s sacred footprint on the island.\n\n"
            "Dress customs (dhoti/veshti, saree) and theertham discipline are treated as part of "
            "respectful approach to Ramanathaswamy. The island is also woven into the wider "
            "Ramayana trail toward Dhanushkodi."
        ),
        "scriptureLinks": [
            "Valmiki Ramayana",
            "Shiva Purana / Jyotirlinga tradition",
            "Skanda Purana Setu–Rameswara mahatmya lore",
        ],
    },
    "badrinath": {
        "mythologySignificance": (
            "Badrinath is the Himalayan Vishnu seat of Adi Shankaracharya’s Char Dham and also "
            "belongs to the Uttarakhand Chota Char Dham. Classical tradition associates the site "
            "with Nar-Narayan meditation and Vishnu’s presence in the Badri forest. "
            "Shankaracharya’s digvijaya narratives credit him with establishing the living "
            "pilgrimage and monastic order connected to the shrine."
        ),
        "localBeliefs": (
            "Garhwal belief holds that the deity ‘resides’ at Badrinath in the open season and "
            "moves to Joshimath for winter worship — a seasonal theology shared with other high "
            "Himalayan dhams. Mana village, Vyas Gufa, and related spots are woven into local "
            "Mahabharata and sage lore.\n\n"
            "Pilgrims often combine Badrinath with Kedarnath, treating the dual Vishnu–Shiva "
            "Himalayan yatra as a complete spiritual circuit."
        ),
        "scriptureLinks": [
            "Vishnu Purana / Nar-Narayan traditions",
            "Skanda Purana Badri mahatmya lore",
            "Shankara digvijaya pilgrimage traditions",
        ],
    },
    "kashi-vishwanath": {
        "mythologySignificance": (
            "Kashi (Varanasi) is praised across Puranas as the city of light where Shiva as "
            "Vishwanath is the eternal lord. The Kashi Vishwanath Jyotirlinga stands at the "
            "spiritual centre of this sacred geography. Texts such as the Kashi Khanda "
            "(Skanda Purana tradition) describe liberation (moksha) associated with dying in "
            "Kashi under Shiva’s grace."
        ),
        "localBeliefs": (
            "Banaras belief treats the Ganga aarti, the lanes to Vishwanath, and the cremation "
            "ghats as a continuous sacred theatre — life, death, and liberation in one city. "
            "Local devotion holds that Vishwanath’s glance frees the soul.\n\n"
            "The expanded temple corridor has become part of contemporary pilgrimage memory, "
            "while older neighbourhood shrines and Annapurna traditions remain woven into "
            "everyday Banarsi faith."
        ),
        "scriptureLinks": [
            "Skanda Purana — Kashi Khanda traditions",
            "Shiva Purana / Jyotirlinga lists",
            "Kashi mahatmya literature",
        ],
    },
    "mahakaleshwar-ujjain": {
        "mythologySignificance": (
            "Mahakaleshwar of Ujjain (Avanti) is a Jyotirlinga celebrated in the Shiva Purana. "
            "The lingam is traditionally described as south-facing (dakshinamukhi), unique among "
            "many Jyotirlinga shrines. Ujjain is also a classical Simhastha Kumbh city, linking "
            "the temple to the wider sacred calendar of riverine India."
        ),
        "localBeliefs": (
            "The pre-dawn Bhasma Aarti — worship with sacred ash — is the living heart of "
            "Mahakal devotion. Locals and pilgrims believe attending this aarti brings fierce "
            "protection and the grace of Mahakala, the lord of time.\n\n"
            "Avanti’s identity as an ancient capital and tirtha deepens the sense that Mahakal "
            "guards both city and cosmos."
        ),
        "scriptureLinks": [
            "Shiva Purana — Mahakala / Avanti traditions",
            "Jyotirlinga pilgrimage lists",
            "Skanda Purana regional mahatmya lore",
        ],
    },
    "omkareshwar": {
        "mythologySignificance": (
            "Omkareshwar, on the Narmada’s Mandhata island, is a Jyotirlinga whose very setting "
            "is read as the sacred syllable Om. Puranic Narmada mahatmya literature praises the "
            "river as purifying; Omkareshwar and nearby Mamleshwar together form the classical "
            "Jyotirlinga complex of this tirtha."
        ),
        "localBeliefs": (
            "Pilgrims circumambulate the island and bathe in the Narmada, believing the river "
            "and the Om-shaped landform amplify Shiva’s presence. Boat crossings and ghats are "
            "part of the lived ritual landscape.\n\n"
            "Local guides often narrate Mandhata’s royal and sage associations alongside the "
            "Jyotirlinga story."
        ),
        "scriptureLinks": [
            "Shiva Purana / Jyotirlinga tradition",
            "Narmada mahatmya literature",
            "Skanda Purana regional traditions",
        ],
    },
    "mallikarjuna-srisailam": {
        "mythologySignificance": (
            "Srisailam’s Mallikarjuna is a Jyotirlinga; the same hill complex venerates "
            "Bhramaramba Devi, counted among the Shakti Peethas. This rare pairing — Shiva and "
            "Shakti on one sacred hill — is celebrated in Andhra Shaiva–Shakta tradition and in "
            "Jyotirlinga / peetha lists alike."
        ),
        "localBeliefs": (
            "Sthala purana tells of Parvati and the devotee-sage Bringi, and of the goddess as "
            "Bhramaramba (the bee-formed mother). Forested Nallamala approaches and Krishna "
            "river geography shape local pilgrimage feeling.\n\n"
            "Devotees treat a single visit as completing both Jyotirlinga and Shakti Peetha "
            "darshan — a belief reinforced by temple ritual pairing of Mallikarjuna and "
            "Bhramaramba."
        ),
        "scriptureLinks": [
            "Shiva Purana / Jyotirlinga lists",
            "Shakti Peetha (Pithanirnaya) traditions",
            "Srisaila sthala purana",
        ],
    },
    "vaidyanath-deoghar": {
        "mythologySignificance": (
            "Baidyanath / Vaidyanath at Deoghar is widely accepted in pilgrimage practice as a "
            "Jyotirlinga. The same sacred complex is associated in Shakti Peetha lists with the "
            "heart of Sati. Thus Deoghar stands at the meeting of Shaiva Jyotirlinga theology "
            "and Shakta peetha geography."
        ),
        "localBeliefs": (
            "The Shravan Bol Bam kanwar yatra — barefoot devotees carrying Ganga water — is the "
            "defining living belief of Deoghar. Locals hold that offering this water to "
            "Baidyanath fulfils vows and heals afflictions (Vaidyanath as ‘lord of physicians’).\n\n"
            "Temple-town culture during Shravan becomes a continuous stream of song, discipline, "
            "and collective devotion."
        ),
        "scriptureLinks": [
            "Shiva Purana / Jyotirlinga pilgrimage tradition",
            "Shakti Peetha lists (heart of Sati)",
            "Regional Santhal Pargana pilgrimage lore",
        ],
    },
    "trimbakeshwar": {
        "mythologySignificance": (
            "Trimbakeshwar near Nashik is a Jyotirlinga linked to Brahmagiri and the sacred "
            "source-region of the Godavari. Puranic Godavari mahatmya and Jyotirlinga lists "
            "place this shrine among Shiva’s twelve radiant forms."
        ),
        "localBeliefs": (
            "The distinctive three-faced lingam tradition and strict ritual norms shape pilgrim "
            "experience. Many combine Trimbakeshwar with Nashik’s Godavari ghats, especially "
            "in Kumbh periods.\n\n"
            "Local belief treats Brahmagiri’s springs and the temple as one continuum of "
            "Godavari’s birth in sacred imagination."
        ),
        "scriptureLinks": [
            "Shiva Purana / Jyotirlinga lists",
            "Godavari mahatmya traditions",
            "Skanda Purana regional lore",
        ],
    },
    "bhimashankar": {
        "mythologySignificance": (
            "Bhimashankar in the Sahyadri is counted among the twelve Jyotirlingas. Regional "
            "Shaiva narrative links the name to Bhima and to Shiva’s triumph in the Tripura / "
            "demon-slaying cycles retained in Deccan oral and textual tradition."
        ),
        "localBeliefs": (
            "Forest sanctuary surroundings make the approach feel like a tapovana. Local "
            "devotees emphasise quiet worship amid the Western Ghats, and monsoon greenery is "
            "itself treated as a blessing of the deity.\n\n"
            "Some Maharashtra pilgrimage circuits pair Bhimashankar with other Jyotirlingas "
            "of the state (Trimbakeshwar, Grishneshwar)."
        ),
        "scriptureLinks": [
            "Shiva Purana / Jyotirlinga lists",
            "Regional Deccan Shaiva sthala lore",
        ],
    },
    "nageshwar": {
        "mythologySignificance": (
            "Nageshwar near Dwarka is counted among the twelve Jyotirlingas. Classical lists "
            "place a Nagesha / Nageshwar form of Shiva in western India; pilgrimage practice "
            "firmly identifies the Dwarka-region shrine for this seat."
        ),
        "localBeliefs": (
            "Gujarat pilgrims almost always combine Nageshwar with Dwarkadhish and often Bet "
            "Dwarka, treating the coastal day as a complete Krishna–Shiva yatra.\n\n"
            "Local belief emphasises protection from poison and fear — resonances of the naga "
            "and Shiva’s nilakantha imagery in popular telling."
        ),
        "scriptureLinks": [
            "Shiva Purana / Jyotirlinga lists",
            "Dwarka–Prabhas regional pilgrimage tradition",
        ],
    },
    "grishneshwar": {
        "mythologySignificance": (
            "Grishneshwar (also Ghushmeshwar in some texts) is the twelfth Jyotirlinga in many "
            "standard yatra lists, standing beside the Ellora caves. The Shiva Purana cycle "
            "retains the Ghushma / Grishneshwar devotion story among Jyotirlinga narratives."
        ),
        "localBeliefs": (
            "Pilgrims often visit Ellora’s rock-cut caves and Grishneshwar on the same day, "
            "reading stone architecture and living lingam worship as one sacred field.\n\n"
            "Local Marathi devotion keeps the shrine intimate despite its pan-Indian "
            "Jyotirlinga status."
        ),
        "scriptureLinks": [
            "Shiva Purana — Ghushmeshwar / Grishneshwar tradition",
            "Jyotirlinga pilgrimage lists",
        ],
    },
    "jagannath-puri": {
        "mythologySignificance": (
            "Puri’s Jagannath temple is the eastern seat of Adi Shankaracharya’s Char Dham. "
            "Jagannath, with Balabhadra and Subhadra, represents a distinctive form of Vishnu–"
            "Krishna devotion rooted in Odisha’s temple culture. Within the same complex, "
            "Goddess Vimala is venerated as a Shakti Peetha (feet of Sati in peetha lists)."
        ),
        "localBeliefs": (
            "Rath Yatra — the deities’ chariot festival — is Odisha’s greatest public theology: "
            "gods come out among the people. Mahaprasad from the temple kitchen is believed to "
            "carry unique sanctity.\n\n"
            "Local identity binds Jagannath to Odia language, arts, and the idea of the lord as "
            "universal ‘Jagannath’ — lord of the world."
        ),
        "scriptureLinks": [
            "Skanda Purana / Purushottama Kshetra traditions",
            "Char Dham pilgrimage tradition",
            "Shakti Peetha lists — Vimala of Puri",
        ],
    },
    "dwarka": {
        "mythologySignificance": (
            "Dwarka is Krishna’s legendary capital after Mathura and the western Char Dham seat. "
            "The Mahabharata and Bhagavata Purana describe Dwarka’s glory and eventual "
            "submersion. The Dwarkadhish temple continues that Vaishnava geography on Gujarat’s "
            "coast."
        ),
        "localBeliefs": (
            "Flag-changing rituals, Gomti Ghat baths, and the boat trip to Bet Dwarka structure "
            "pilgrim belief. Many hold that Krishna still ‘rules’ from Dwarka in a mystical sense.\n\n"
            "Coastal storms and underwater archaeology stories feed popular imagination about "
            "the submerged city, though faith and science remain distinct domains."
        ),
        "scriptureLinks": [
            "Bhagavata Purana",
            "Mahabharata — Dwarka narratives",
            "Char Dham pilgrimage tradition",
        ],
    },
    "kamakhya": {
        "mythologySignificance": (
            "Kamakhya on Nilachal Hill is among the foremost Shakti Peethas. In the Sati–Daksha "
            "narrative retained in Devi and Kalika Purana traditions, the yoni of Sati fell here. "
            "Kamakhya thus stands at the centre of Shakta and Tantric geography in eastern India."
        ),
        "localBeliefs": (
            "Ambubachi Mela marks the goddess’s annual menstrual cycle in local theology — a "
            "rare public sacralising of feminine creative power. During this time the temple "
            "follows special closure and reopening rites.\n\n"
            "Assamese and wider eastern devotees regard Nilachal as a living seat of desire "
            "(kama) transformed into sacred Shakti."
        ),
        "scriptureLinks": [
            "Kalika Purana",
            "Devi Purana / Shakta traditions",
            "Pithanirnaya Shakti Peetha lists",
        ],
    },
    "tirumala-venkateswara": {
        "mythologySignificance": (
            "Tirumala’s Venkateswara (Balaji) is worshipped as Vishnu in Kaliyuga. Venkatachala "
            "mahatmya literature and Vaishnava tradition describe the lord’s residence on the "
            "seven hills (Saptagiri). The shrine is among the most visited Vishnu temples in "
            "the world and the spiritual axis of Andhra pilgrimage."
        ),
        "localBeliefs": (
            "Tonsure (mundan), laddu prasadam, and vow fulfilment (mokku) define lived belief. "
            "Devotees climb or ride to the hills believing Venkateswara grants boons and "
            "relieves debt — a theme in popular Telugu and Tamil devotion.\n\n"
            "TTD administration and seva systems are themselves part of modern sacred order; "
            "pilgrims treat queue discipline as service to the lord."
        ),
        "scriptureLinks": [
            "Venkatachala / Varaha mahatmya traditions",
            "Vaishnava Agamic and Alvar-influenced devotion",
            "Andhra temple sthala purana",
        ],
    },
    "yamunotri": {
        "mythologySignificance": (
            "Yamunotri is the Devi shrine of the Yamuna in the Uttarakhand Chota Char Dham. "
            "Puranic river goddess theology treats Yamuna as sister of Yama and a purifying "
            "tirtha; the Himalayan shrine marks the sacred source-region of that devotion."
        ),
        "localBeliefs": (
            "Pilgrims cook rice in hot springs near the temple as prasadam tradition and regard "
            "the tough trek as offering. Seasonal opening and closing frame the goddess’s "
            "presence in local calendrical belief.\n\n"
            "Yamunotri is consciously distinguished from Adi Shankaracharya’s pan-India Char "
            "Dham in informed pilgrimage teaching."
        ),
        "scriptureLinks": [
            "Puranic Yamuna mahatmya traditions",
            "Uttarakhand Chota Char Dham pilgrimage lore",
        ],
    },
    "gangotri": {
        "mythologySignificance": (
            "Gangotri commemorates Ganga’s descent to earth — a central theme of the Ramayana "
            "and Puranas (Bhagiratha’s penance). The Himalayan temple marks the sacred "
            "geography of Ganga’s appearance in the Chota Char Dham circuit."
        ),
        "localBeliefs": (
            "Gaumukh glacier journeys extend the belief that Ganga’s true ‘mouth’ lies further "
            "in ice and stone. Pilgrims collect Gangajal here for rituals across India.\n\n"
            "Winter closure and the deity’s seasonal seat elsewhere echo other Garhwal dham "
            "practices."
        ),
        "scriptureLinks": [
            "Ramayana — Bhagiratha / Ganga descent",
            "Puranic Ganga mahatmya",
            "Chota Char Dham tradition",
        ],
    },
    "tungnath": {
        "mythologySignificance": (
            "Tungnath is the second of the Panch Kedar. In Garhwal’s Pandava–Shiva bull legend, "
            "different limbs of Shiva’s form are worshipped at five temples; Tungnath is "
            "associated with the arms. It is often described as among the highest Shiva temples."
        ),
        "localBeliefs": (
            "Chopta’s meadows and the short steep climb shape a distinctive Himalayan devotion — "
            "quiet, alpine, and less crowded than Kedarnath. Locals link Chandrashila peak views "
            "with meditative Shaiva mood.\n\n"
            "Winter arrangements and seasonal access are part of lived ritual knowledge."
        ),
        "scriptureLinks": [
            "Garhwal Panch Kedar sthala tradition",
            "Mahabharata-linked Pandava–Shiva lore",
        ],
    },
    "rudranath": {
        "mythologySignificance": (
            "Rudranath is the Panch Kedar seat associated with Shiva’s face (mukha) in the "
            "Garhwal bull-form legend that follows the Pandavas’ search for Shiva after "
            "Kurukshetra. In that widely told Himalayan mahatmya, Shiva dove into the earth as "
            "a bull; different limbs became five Kedars, with Kedarnath holding the hump and "
            "Rudranath the face — hence the fierce Rudra aspect emphasised here.\n\n"
            "The shrine thus joins Mahabharata memory with living Shaiva mountain theology: "
            "Rudra as storm, wildness, and grace in the high Garhwal forests."
        ),
        "localBeliefs": (
            "The demanding trek is itself considered the ‘gate’ to darshan. Shepherds’ paths "
            "and mist-filled valleys feed a local sense of Rudra as wild mountain lord.\n\n"
            "Fewer facilities than famous dhams preserve an austere pilgrimage ethos; many "
            "Garhwal families treat completing Rudranath as a mark of serious Kedara devotion."
        ),
        "scriptureLinks": [
            "Panch Kedar sthala tradition",
            "Mahabharata-linked Garhwal Shaiva lore",
        ],
    },
    "madhyamaheshwar": {
        "mythologySignificance": (
            "Madhyamaheshwar is the Panch Kedar shrine associated with the navel (nabhi) of "
            "Shiva in the distributed bull-form legend of Garhwal. After the Pandavas sought "
            "Shiva’s forgiveness, local mahatmya holds that the mid-body of the submerged bull "
            "remained in this Mandakini valley — ‘Madhya’ Maheshwar, the lord at the centre.\n\n"
            "Together with Kedarnath, Tungnath, Rudranath, and Kalpeshwar, it completes a "
            "five-fold Shaiva body of the Himalaya."
        ),
        "localBeliefs": (
            "Budha Madhyamaheshwar, a higher meadow shrine, is visited by those seeking a still "
            "more remote presence. Local belief treats the valley as a quiet heart of Kedara "
            "kshetra.\n\n"
            "Village hospitality and seasonal herding rhythms frame the pilgrimage; winter "
            "arrangements and pony tracks are part of living ritual knowledge."
        ),
        "scriptureLinks": [
            "Panch Kedar sthala tradition",
            "Garhwal Shaiva oral and mahatmya lore",
        ],
    },
    "kalpeshwar": {
        "mythologySignificance": (
            "Kalpeshwar completes the Panch Kedar, associated with Shiva’s jata (matted hair) "
            "in the Garhwal limb-distribution legend. In the same Pandava–Shiva bull narrative "
            "that sanctifies Kedarnath, the locks of Shiva are said to have remained at "
            "Kalpeshwar in Urgam — a cave-linked seat of matted, ascetic Shiva.\n\n"
            "Puranic Himalayan Shaivism often praises jata as the seat of Ganga’s descent; "
            "local teaching quietly echoes that symbolism at this final Kedar."
        ),
        "localBeliefs": (
            "Often more accessible than higher Kedars, Kalpeshwar is believed by many to remain "
            "approachable longer in the year. Urgam valley lore emphasises a cave-like intimacy "
            "with the deity.\n\n"
            "Completing all five Kedars is a prized vow among Garhwal and plains pilgrims alike; "
            "guides narrate the limb map of Shiva as pilgrims walk from one valley to the next."
        ),
        "scriptureLinks": [
            "Panch Kedar sthala tradition",
            "Garhwal Shaiva pilgrimage lore",
        ],
    },
    "thiruvanaikaval": {
        "mythologySignificance": (
            "Jambukeswarar at Thiruvanaikaval is the water (Appu) element among the Pancha Bhuta "
            "Sthalams of Tamil Shaivism. Tevaram hymns and sthala purana describe an underground "
            "spring beneath the lingam and Parvati’s penance as Akhilandeshwari."
        ),
        "localBeliefs": (
            "The ever-moist lingam is shown as proof of the water element’s living presence. "
            "Paired darshan with Srirangam across the Kaveri is a classic Trichy belief-circuit.\n\n"
            "Strict South Indian dress norms are treated as part of elemental temple discipline."
        ),
        "scriptureLinks": [
            "Tevaram hymns",
            "Pancha Bhuta Shaiva tradition",
            "Tamil sthala purana",
        ],
    },
    "ekambareswarar-kanchipuram": {
        "mythologySignificance": (
            "Ekambareswarar represents the earth (Prithvi) element of the Pancha Bhuta Sthalams. "
            "Kanchipuram’s sthala purana narrates Parvati’s penance under the mango tree and "
            "Shiva’s manifestation as the earth lingam."
        ),
        "localBeliefs": (
            "The ancient mango tree and long temple corridors are touched as blessings. "
            "Kanchi devotees weave Ekambareswarar with Kamakshi and other city shrines into "
            "one temple-town theology.\n\n"
            "Earth-element symbolism is explained to pilgrims as stability and fertility."
        ),
        "scriptureLinks": [
            "Pancha Bhuta tradition",
            "Kanchipuram sthala purana",
            "Tevaram / Tamil Shaiva canon",
        ],
    },
    "arunachaleswarar-tiruvannamalai": {
        "mythologySignificance": (
            "Arunachaleswarar embodies the fire (Agni) element of the Pancha Bhuta. The "
            "Arunachala hill itself is worshipped as a lingam of fire — a theology celebrated "
            "in Tamil Shaiva literature and later in Ramana Maharshi’s association with the hill."
        ),
        "localBeliefs": (
            "Karthigai Deepam — the beacon on the hill — is the year’s climax of fire theology "
            "made visible. Girivalam (circumambulation of Arunachala) is believed to burn karma.\n\n"
            "Ashram culture and classical temple ritual coexist in local sacred life."
        ),
        "scriptureLinks": [
            "Pancha Bhuta / Arunachala tradition",
            "Tamil Shaiva sthala purana",
            "Tevaram hymn landscape",
        ],
    },
    "srikalahasti": {
        "mythologySignificance": (
            "Srikalahasti is the air (Vayu) Sthalam of the Pancha Bhuta. The name recalls the "
            "spider (sri), snake (kala), and elephant (hasti) devotees of local Shaiva legend — "
            "creatures of instinct whose devotion Shiva accepted."
        ),
        "localBeliefs": (
            "Rahu–Ketu dosha remedies and lamp offerings are major living beliefs. The temple’s "
            "nearness to Tirupati makes it a natural stop on Andhra–Tamil pilgrimage loops.\n\n"
            "The lamp flame’s movement inside the sanctum is popularly linked to the air element."
        ),
        "scriptureLinks": [
            "Pancha Bhuta tradition",
            "Srikalahasti sthala purana",
            "South Indian Shaiva lore",
        ],
    },
    "nataraja-chidambaram": {
        "mythologySignificance": (
            "Chidambaram’s Nataraja temple represents space (Akasha) among the Pancha Bhuta. "
            "The Chidambara Rahasyam — the secret of space — and Nataraja’s ananda tandava "
            "(dance of bliss) are central to Tamil Shaiva metaphysics."
        ),
        "localBeliefs": (
            "Seeing the rahasya and witnessing ritual dance theology is a pilgrim’s deep wish. "
            "Dikshitar traditions and temple music keep the dance cosmology alive in sound.\n\n"
            "Space-element teaching is explained as the subtle emptiness in which all forms arise."
        ),
        "scriptureLinks": [
            "Pancha Bhuta / Chidambaram tradition",
            "Tamil Shaiva Agamic and hymn literature",
            "Nataraja theology in Shaiva Siddhanta",
        ],
    },
    "kurukshetra-brahmasarovar": {
        "mythologySignificance": (
            "Kurukshetra is the Mahabharata’s dharma-field. Jyotisar is traditionally identified "
            "with the place of the Bhagavad Gita’s teaching to Arjuna. Brahma Sarovar is a vast "
            "sacred tank praised in regional mahatmya for ancestral rites and eclipse baths."
        ),
        "localBeliefs": (
            "Eclipse-day snans and Gita Jayanti gatherings renew the belief that this land still "
            "echoes Krishna’s words. Museums and marked tirthas help pilgrims map epic memory "
            "onto modern Haryana.\n\n"
            "Local guides narrate tank, banyan, and battlefield traditions as one continuum."
        ),
        "scriptureLinks": [
            "Mahabharata",
            "Bhagavad Gita",
            "Vamana Purana — Kurukshetra mahatmya traditions",
        ],
    },
    "chitrakoot-ramghat": {
        "mythologySignificance": (
            "Chitrakoot is cherished in the Ramayana and later Ramcharitmanas tradition as a "
            "principal forest home of Rama, Sita, and Lakshmana during exile. Ghats, hills, and "
            "caves preserve that epic geography in North Indian devotion."
        ),
        "localBeliefs": (
            "Ramghat aarti, Kamadgiri parikrama, and sites of Bharata’s meeting with Rama "
            "structure local belief. Pilgrims feel the Mandakini landscape as still echoing "
            "Rama’s footsteps.\n\n"
            "Compared with metro temples, Chitrakoot’s quieter rhythm is itself treated as a "
            "spiritual quality."
        ),
        "scriptureLinks": [
            "Valmiki Ramayana",
            "Ramcharitmanas (Tulsidas)",
            "Local Chitrakoot sthala lore",
        ],
    },
    "mount-kailash": {
        "mythologySignificance": (
            "Mount Kailash is revered in Hindu cosmology as Kailasa, the abode of Shiva and "
            "Parvati. The Mahabharata and Puranas celebrate it as a cosmic axis. Jain tradition "
            "associates the region with Rishabhadeva; Tibetan Buddhist and Bon traditions also "
            "hold the mountain sacred — a rare cross-faith geography."
        ),
        "localBeliefs": (
            "Pilgrims perform kora / parikrama rather than summiting — climbing is forbidden and "
            "believed spiritually improper. Lake Manasarovar baths and the multi-day circuit "
            "are the lived rite.\n\n"
            "Altitude, thin air, and silence become part of the belief that one walks the edge "
            "of the human and the divine."
        ),
        "scriptureLinks": [
            "Shiva Purana / Kailasa lore",
            "Mahabharata Himalayan geography",
            "Jain and Tibetan sacred mountain traditions",
        ],
    },
    "pashupatinath": {
        "mythologySignificance": (
            "Pashupatinath in Kathmandu is Nepal’s foremost Shiva temple. Pashupati — ‘Lord of "
            "Beings’ — is an ancient form of Shiva celebrated in Himalayan and pan-Indian Shaiva "
            "devotion. The Bagmati riverside complex is a major cremation and pilgrimage "
            "landscape."
        ),
        "localBeliefs": (
            "Shivaratri draws Himalayan and Indian pilgrims in vast numbers. Local Newar and "
            "Nepali traditions maintain distinctive ritual calendars around the shrine.\n\n"
            "Proximity to Guhyeshwari Shakti Peetha creates a paired Shiva–Shakti belief for "
            "many Kathmandu valley devotees."
        ),
        "scriptureLinks": [
            "Shaiva / Pashupata traditions",
            "Nepalese chronicles and sthala lore",
            "Himalayan Shaiva pilgrimage tradition",
        ],
    },
    "muktinath": {
        "mythologySignificance": (
            "Muktinath in Mustang is a high Himalayan tirtha of liberation (mukti), sacred to "
            "both Hindus and Buddhists. In Shakti Peetha enumerations it is also remembered as "
            "the Gandaki peetha. Vaishnava and Himalayan Buddhist geographies meet here."
        ),
        "localBeliefs": (
            "Bathing under the 108 water spouts and visiting the eternal flame shrine are core "
            "pilgrim acts. Hindus and Buddhists share the precinct with distinct yet coexisting "
            "ritual styles.\n\n"
            "Altitude and wind are read as purifying forces on the path to mukti."
        ),
        "scriptureLinks": [
            "Vaishnava mukti-tirtha tradition",
            "Shakti Peetha (Gandaki) lists",
            "Himalayan Buddhist sacred geography",
        ],
    },
    "guruvayur": {
        "mythologySignificance": (
            "Guruvayurappan is Krishna worshipped in a form cherished across Kerala Vaishnavism. "
            "Temple tradition links the image to ancient consecration narratives involving Guru "
            "(Brihaspati) and Vayu — hence Guruvayur."
        ),
        "localBeliefs": (
            "Strict dress codes, elephant processions, and melam drumming shape belief as "
            "embodied discipline. Offering tulsi and seeing the child-form Krishna are central "
            "wishes.\n\n"
            "Guruvayur is often called the Dwarka of the South in popular Kerala devotion."
        ),
        "scriptureLinks": [
            "Kerala Vaishnava sthala tradition",
            "Bhagavata-inspired Krishna devotion",
            "Guruvayur Devaswom temple lore",
        ],
    },
    "sabarimala": {
        "mythologySignificance": (
            "Sabarimala’s Ayyappa (Dharmasastha) stands at a unique confluence of Shaiva, "
            "Vaishnava, and regional forest-hill traditions of Kerala. The seasonal pilgrimage "
            "is among India’s largest organised acts of vow and austerity."
        ),
        "localBeliefs": (
            "The vrata — black attire, abstinence, and the chant ‘Swamiye Saranam Ayyappa’ — "
            "is the belief system in practice. Mandala–Makaravilakku season structures the year.\n\n"
            "Forest path, eighteen steps, and irumudi kettu bundles are sacred technologies of "
            "approach; rules are taken as Ayyappa’s own command."
        ),
        "scriptureLinks": [
            "Kerala Sastha / Ayyappa tradition",
            "Regional Puranic and folk-epic narratives",
            "Travancore Devaswom pilgrimage order",
        ],
    },
    "vaishno-devi": {
        "mythologySignificance": (
            "Vaishno Devi on Trikuta is worshipped as a form of the Goddess combining Vaishnava "
            "and Shakta resonances in North Indian devotion. Regional mahatmya narrates the "
            "goddess’s pursuit of the devotee-turned-adversary Bhairon and her establishment "
            "in the holy cave — a story that frames the yatra as both refuge and testing.\n\n"
            "The shrine board pilgrimage is among India’s largest Devi yatras, placing Trikuta "
            "alongside pan-Indian Shakta geography even where formal peetha lists differ."
        ),
        "localBeliefs": (
            "The climb from Katra, the holy cave (garbha joon), and the three pindis are the "
            "core of belief. Devotees hold that the Mother calls whom she chooses.\n\n"
            "Bhairavnath temple visit after the main cave is a customary completion of the yatra "
            "in local teaching — gratitude after the Mother’s grace, and closure of the pursuit "
            "story told on the trail."
        ),
        "scriptureLinks": [
            "North Indian Devi / Vaishno tradition",
            "Regional Jammu mahatmya and oral lore",
            "Shrine Board pilgrimage literature",
        ],
    },
    "kalighat": {
        "mythologySignificance": (
            "Kalighat in Kolkata is counted among the great Shakti Peethas. In the Puranic "
            "Sati–Daksha cycle — preserved in Devi and Kalika Purana traditions — Vishnu’s "
            "chakra portions Sati’s body as Shiva carries it in grief; where each part falls, "
            "a peetha arises. Popular 51-peetha lists associate Kalighat with the toes of "
            "Sati’s right foot.\n\n"
            "Kali here is the fierce-compassionate mother of Bengal’s Shakta imagination: "
            "time, death, and protection gathered in one urban tirtha that later gave the "
            "city its colonial-era name, Calcutta / Kolkata."
        ),
        "localBeliefs": (
            "Animal sacrifice traditions (where practised under temple rules), red hibiscus, and "
            "the lane-life around the shrine shape Kalighat’s intense urban sacredness.\n\n"
            "Bengali households treat Kalighat Kali as a city mother — approachable yet "
            "awe-inspiring. Kali Puja night and ordinary Tuesdays/Saturdays both draw vow-keepers "
            "who believe the Mother of Kalighat answers quickly in distress."
        ),
        "scriptureLinks": [
            "Shakti Peetha (Pithanirnaya) tradition",
            "Bengal Shakta / Kali devotion",
            "Kalika Purana–influenced lore",
        ],
    },
    "seetha-amman-nuwara-eliya": {
        "mythologySignificance": (
            "Seetha Amman Temple at Seetha Eliya is linked by Sri Lankan and Indian Ramayana "
            "trail tradition to Sita’s captivity in Lanka. While the Valmiki Ramayana’s geography "
            "is epic rather than modern cartography, living pilgrimage maps this highland site "
            "into Rama–Sita memory."
        ),
        "localBeliefs": (
            "Streamside shrines and ‘footprint’ lore are shown to pilgrims as signs of Sita’s "
            "presence. The cool hill climate becomes part of the emotional landscape of exile.\n\n"
            "Many combine the visit with wider Sri Lanka Ramayana trail stops."
        ),
        "scriptureLinks": [
            "Valmiki Ramayana",
            "Sri Lankan Ramayana trail traditions",
            "Regional sthala lore",
        ],
    },
    "kataragama": {
        "mythologySignificance": (
            "Kataragama is a multi-faith shrine of southern Sri Lanka — Murugan for Hindus, "
            "Kataragama Deviyo for Buddhists, with indigenous resonances. It sits in the wider "
            "Indian Ocean sacred geography that pilgrims also associate with Ramayana Lanka."
        ),
        "localBeliefs": (
            "Fire-walking, processions, and vow offerings define festival belief. Devotees of "
            "different communities share pathways while keeping distinct ritual styles.\n\n"
            "The dry-zone landscape and pilgrimage town rhythm are part of Kataragama’s felt "
            "holiness."
        ),
        "scriptureLinks": [
            "Murugan / Skanda traditions",
            "Sri Lankan Buddhist and Hindu chronicle culture",
            "Indian Ocean pilgrimage routes",
        ],
    },
    "simhachalam": {
        "mythologySignificance": (
            "Simhachalam near Visakhapatnam is dedicated to Varaha Lakshmi Narasimha — a rare "
            "combined form. Vaishnava sthala purana of the Andhra coast narrates Narasimha’s "
            "grace and the hill’s sanctity under successive dynasties."
        ),
        "localBeliefs": (
            "For most of the year the deity is covered in sandal paste; Chandanotsavam reveals "
            "the form — a dramatic annual belief climax.\n\n"
            "Coastal Andhra families treat Simhachalam as a protective Narasimha kshetra for "
            "vows and gratitude."
        ),
        "scriptureLinks": [
            "Andhra Vaishnava sthala purana",
            "Narasimha Purana–influenced devotion",
            "AP temple pilgrimage tradition",
        ],
    },
    "kanaka-durga-vijayawada": {
        "mythologySignificance": (
            "Kanaka Durga on Indrakeeladri overlooks the Krishna. Shakta tradition links the "
            "hill with Durga’s victory over mahishasura-class forces in the Devi Mahatmya "
            "cycle and with regional Andhra mahatmya that place the goddess as guardian of "
            "the river crossing.\n\n"
            "Vijayawada (‘city of victory’) is popularly read through this theology: the "
            "golden (kanaka) mother on the hill confers victory, protection, and prosperity "
            "to the Krishna basin."
        ),
        "localBeliefs": (
            "Dasara celebrations transform the hill into a city-wide festival of the goddess. "
            "River–hill geography is read as Durga’s own seat of victory and protection.\n\n"
            "Local Telugu devotion calls her the golden mother; families climb for Varalakshmi, "
            "Dasara, and ordinary Fridays believing Indrakeeladri answers household vows."
        ),
        "scriptureLinks": [
            "Devi Mahatmya / Durga tradition",
            "Andhra Shakta sthala purana",
            "Regional Krishna-river tirtha lore",
        ],
    },
    "annavaram-satyanarayana": {
        "mythologySignificance": (
            "Annavaram’s Satyanarayana Swamy temple on Ratnagiri hill is dedicated to Vishnu "
            "as Satyanarayana — the lord of truth. Vaishnava vrata literature and Andhra "
            "pilgrimage practice treat the Satyanarayana Vratham as a household and temple "
            "rite for prosperity, gratitude, and fulfilment of vows."
        ),
        "localBeliefs": (
            "Families across Andhra and Telangana travel here specifically to complete "
            "Satyanarayana Vratham with temple priests. The hill setting and Godavari-region "
            "approaches reinforce the sense of a ‘truth-vow’ fulfilled in sacred space.\n\n"
            "Prasadam and vrata katha listening are central to the lived pilgrimage."
        ),
        "scriptureLinks": [
            "Satyanarayana Vratham / Skanda Purana–linked popular tradition",
            "Andhra Vaishnava sthala lore",
            "AP Temples pilgrimage practice",
        ],
    },
    "bhadrachalam": {
        "mythologySignificance": (
            "Bhadrachalam on the Godavari is a major Rama temple of Telangana, woven into "
            "the Ramayana trail of the Deccan. Temple tradition associates the site with "
            "devotion to Rama, Sita, and Lakshmana, and with later historical patronage that "
            "kept Vaishnava worship alive on the riverbank."
        ),
        "localBeliefs": (
            "Vaikuntha Ekadasi and Sri Rama Navami draw huge Godavari-side crowds. Local "
            "belief treats the river bath and Rama darshan as a paired blessing.\n\n"
            "Many pilgrims narrate the story of devotee Bhakta Ramadasu’s association with "
            "the shrine as proof that sincere vow can move both king and deity."
        ),
        "scriptureLinks": [
            "Valmiki Ramayana",
            "Deccan Ramayana trail / temple sthala lore",
            "Bhakta Ramadasu tradition",
        ],
    },
    "chamundeshwari-mysuru": {
        "mythologySignificance": (
            "Chamundeshwari on Chamundi Hill is the tutelary goddess of Mysuru. Shakta "
            "tradition identifies her with Chamunda, the fierce form who slays the demons "
            "Chanda and Munda in the Devi Mahatmya. The hill shrine anchors Mysuru’s royal "
            "and civic sacred geography."
        ),
        "localBeliefs": (
            "Mysuru Dasara centres on the goddess — the royal procession and city festival "
            "are popularly understood as her victory celebrated yearly.\n\n"
            "Local devotees climb or drive the hill for Tuesday/Friday worship and treat "
            "Chamundi as the protecting mother of the city."
        ),
        "scriptureLinks": [
            "Devi Mahatmya (Chamunda narrative)",
            "Mysuru royal / Wodeyar temple tradition",
            "Karnataka Shakta sthala lore",
        ],
    },
    "kanipakam": {
        "mythologySignificance": (
            "Kanipakam’s Varasiddhi Vinayaka is a self-manifest (swayambhu) Ganesha shrine "
            "of the Tirupati region. South Indian Ganesha devotion and Andhra sthala purana "
            "celebrate the growing idol tradition and the tank (kanalu) origin story behind "
            "the place-name."
        ),
        "localBeliefs": (
            "Devotees believe the idol continues to grow and that vows made for obstacles "
            "(vighna) are especially fruitful here. Many combine Kanipakam with Tirumala or "
            "Srikalahasti on the same Andhra loop.\n\n"
            "Abhishekam and laddu-style prasadam customs structure everyday belief."
        ),
        "scriptureLinks": [
            "Andhra Ganesha sthala purana",
            "Skanda / Ganesha Purana–influenced devotion",
            "Tirupati-region pilgrimage practice",
        ],
    },
    "khatushyam": {
        "mythologySignificance": (
            "Khatu Shyam of Rajasthan is worshipped as a form of Krishna–Barbarika "
            "(son of Ghatotkacha) in popular Mahabharata-linked devotion. Folklore holds that "
            "Krishna granted Barbarika worship in Kaliyuga under the name Shyam — making "
            "Khatu a living bridge between epic memory and folk Vaishnavism."
        ),
        "localBeliefs": (
            "Phalguna Mela transforms the small town into one of Rajasthan’s densest "
            "pilgrimages. Devotees offer coconuts, chadars, and songs, believing Shyam Baba "
            "removes impossible obstacles.\n\n"
            "‘Shyam baba ki jai’ processions and village-to-temple walking vows are the "
            "heartbeat of local faith."
        ),
        "scriptureLinks": [
            "Mahabharata-linked Barbarika folklore",
            "Rajasthan folk-Vaishnava tradition",
            "Local Khatu sthala lore",
        ],
    },
    "lepakshi-veerabhadra": {
        "mythologySignificance": (
            "Lepakshi’s Veerabhadra temple is a Vijayanagara masterpiece dedicated to "
            "Veerabhadra — the fierce emanation of Shiva created after Sati’s death at Daksha’s "
            "yajna (a narrative shared with Shakta geography). The site joins Shaiva mythology "
            "with one of South India’s finest mural and sculpture ensembles."
        ),
        "localBeliefs": (
            "The hanging pillar, Nandi, and ceiling paintings are shown as wonders that "
            "confirm divine craftsmanship in popular telling. The name Lepakshi (‘rise, bird’) "
            "is linked in local Ramayana lore to Jatayu.\n\n"
            "Art, myth, and pilgrimage fuse: visitors come for darshan and for the stone "
            "storybook around them."
        ),
        "scriptureLinks": [
            "Shaiva / Daksha–yajna tradition",
            "Vijayanagara temple inscriptions & art history",
            "Local Ramayana (Jatayu) lore",
        ],
    },
    "mookambika-kollur": {
        "mythologySignificance": (
            "Mookambika at Kollur is a powerful coastal Karnataka Devi temple where the "
            "goddess is worshipped in a unique jyotir-linga–associated form with Saraswati–"
            "Lakshmi–Kali resonances. Adi Shankaracharya traditions and Kerala–Karnataka "
            "Shakta devotion both claim deep ties to the shrine."
        ),
        "localBeliefs": (
            "Vidyarambham (initiation into letters) draws parents from Kerala and Karnataka, "
            "who believe the goddess grants speech, learning, and arts. Navaratri is especially "
            "charged.\n\n"
            "Western Ghat approaches and the Sowparnika river frame Kollur as a forest-hill "
            "Devi kshetra rather than a city temple."
        ),
        "scriptureLinks": [
            "Kollur Mookambika sthala purana",
            "Shankara-linked Devi traditions",
            "Kerala–Karnataka Shakta pilgrimage lore",
        ],
    },
    "murudeshwar": {
        "mythologySignificance": (
            "Murudeshwar on the Karnataka coast is dedicated to Shiva. Local Shaiva lore "
            "connects the lingam tradition with Ravana and the Atmalinga narrative of the "
            "Ramayana–Purana interface — a story also told at Gokarna — placing Murudeshwar "
            "in western coastal Shaiva geography."
        ),
        "localBeliefs": (
            "The giant sea-facing Shiva statue and tall gopura have become modern icons of "
            "the pilgrimage; devotees treat the beach-temple complex as an accessible "
            "darshan of coastal Shiva.\n\n"
            "Sunset aarti by the Arabian Sea is a popular lived ritual moment."
        ),
        "scriptureLinks": [
            "Atmalinga / Ravana coastal Shaiva lore",
            "Karnataka temple sthala tradition",
            "Ramayana-linked Deccan Shaiva geography",
        ],
    },
    "pandharpur-vitthal": {
        "mythologySignificance": (
            "Pandharpur’s Vitthal-Rukmini temple is the heart of the Warkari tradition of "
            "Maharashtra. Vitthal is worshipped as a form of Krishna/Vishnu standing on a "
            "brick — a theology sung in the Abhangas of saints from Namdev and Dnyaneshwar "
            "to Tukaram."
        ),
        "localBeliefs": (
            "Ashadhi and Kartiki Ekadashi pilgrimages (wari) — barefoot processions of "
            "palakhis from across Maharashtra — are the living scripture of Pandharpur. "
            "Devotees believe Vitthal waits eternally for the bhakta.\n\n"
            "Standing with hands on hips, the murti’s posture itself is read as welcoming "
            "the weary pilgrim."
        ),
        "scriptureLinks": [
            "Warkari Abhanga literature",
            "Bhagavata-inspired Varkari theology",
            "Pandharpur mahatmya / saint biographies",
        ],
    },
    "salasar-balaji": {
        "mythologySignificance": (
            "Salasar Balaji is a major Hanuman pilgrimage of Rajasthan. Regional tradition "
            "narrates the self-manifestation of the Hanuman image and the spread of Balaji "
            "devotion through Shekhawati villages — situating the shrine in the wider "
            "Ramayana-linked Hanuman theology of North India."
        ),
        "localBeliefs": (
            "Tuesday and Saturday crowds believe Balaji fulfils vows swiftly. Offerings of "
            "chola, ladoo, and flags mark completed mannat (vows).\n\n"
            "The temple town’s growth is itself narrated by locals as Hanuman’s living grace "
            "in the desert belt."
        ),
        "scriptureLinks": [
            "Ramayana Hanuman devotion",
            "Rajasthan folk-Hanuman sthala lore",
            "Shekhawati pilgrimage tradition",
        ],
    },
    "tuljapur-bhavani": {
        "mythologySignificance": (
            "Tulja Bhavani of Tuljapur is one of Maharashtra’s foremost Devi shrines "
            "(Ambabai). Shakta tradition links Bhavani with Durga’s protective and martial "
            "grace; Maratha history further sanctifies her as a goddess of sovereignty and "
            "courage."
        ),
        "localBeliefs": (
            "Navaratri and local jatras fill Tuljapur with vow-fulfilers. Many Maharashtrian "
            "families treat Bhavani as kuladevi (clan goddess).\n\n"
            "Stories of Shivaji’s devotion to Bhavani are retold as proof that political "
            "courage and Devi grace walk together in regional memory."
        ),
        "scriptureLinks": [
            "Devi Mahatmya / Bhavani tradition",
            "Maharashtra Ambabai pilgrimage lore",
            "Maratha–Tuljapur sacred history",
        ],
    },
    "vemulawada": {
        "mythologySignificance": (
            "Vemulawada’s Raja Rajeshwara temple is a principal Shaiva shrine of Telangana. "
            "Regional tradition celebrates Shiva as Rajarajeshwara — lord of lords — with "
            "deep roots in Deccan temple culture and pilgrimage."
        ),
        "localBeliefs": (
            "Devotees flock for kodimundana and special abhishekams, believing the shrine "
            "removes doshas and grants family welfare. The temple tank and complex structure "
            "everyday ritual life.\n\n"
            "Telangana pilgrims often pair Vemulawada with other state Shaiva–Vaishnava seats "
            "on multi-day circuits."
        ),
        "scriptureLinks": [
            "Telangana Shaiva sthala tradition",
            "Deccan temple pilgrimage lore",
            "Local Raja Rajeshwara mahatmya",
        ],
    },
    "yadagirigutta": {
        "mythologySignificance": (
            "Yadagirigutta is dedicated to Lakshmi Narasimha on a Telangana hill. Vaishnava "
            "sthala purana recounts sage Yadarishi’s penance and Narasimha’s grace — placing "
            "the shrine in the wider South Indian Narasimha geography of protection and "
            "fierce compassion."
        ),
        "localBeliefs": (
            "The rebuilt temple complex has become a major state pilgrimage; devotees "
            "believe Narasimha here grants fearlessness and healing. Weekends and festival "
            "days see long queues.\n\n"
            "Hill darshan is treated as a complete family vow destination within Telangana."
        ),
        "scriptureLinks": [
            "Yadagirigutta sthala purana",
            "Narasimha Purana–influenced devotion",
            "Telangana Endowments pilgrimage practice",
        ],
    },
    "amarnath-shakti": {
        "mythologySignificance": (
            "In Shakti Peetha pilgrimage enumerations, Amarnath is remembered as a Himalayan "
            "seat linked to the Sati–Shakti narrative (throat association in some lists; "
            "traditions vary). The same mountain landscape is famous for the ice lingam of "
            "Shiva — so peetha devotion and Amar Katha Shaiva lore meet in one high-altitude "
            "kshetra."
        ),
        "localBeliefs": (
            "Pilgrims on the Amarnath Yatra often hold both Shiva’s ice lingam and the "
            "Goddess’s peetha association in mind. Seasonal access, registered yatra rules, "
            "and weather windows structure safe devotion.\n\n"
            "Local tellings differ on the exact peetha detail; yatra priests and Kashmir "
            "pilgrimage lore remain the practical guides on the ground."
        ),
        "scriptureLinks": [
            "Pithanirnaya / Shakti Peetha lists (traditions vary)",
            "Amar Katha / Himalayan Shaiva tradition",
            "Amarnath Yatra pilgrimage lore",
        ],
    },
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _body_part_from_famous(famous: str) -> str:
    if "—" in famous:
        return famous.split("—", 1)[1].strip()
    return ""


def expand_generic(d: dict) -> tuple[str, str, list]:
    name = d.get("name", "This temple")
    deity = d.get("deity", "the presiding deity")
    loc = d.get("location", "this tirtha")
    tags = set(d.get("tags", []))
    famous = d.get("famousFor", "")
    existing = (d.get("mythology") or "").strip()
    scriptures = list(d.get("scriptureLinks") or [])
    summary = (d.get("summary") or "").strip()

    if "51-shakti-peeth" in tags:
        part = _body_part_from_famous(famous)
        part_clause = (
            f" Tradition in the popular 51-peetha pilgrimage enumeration associates this seat "
            f"with the {part} of Goddess Sati."
            if part
            else ""
        )
        significance = (
            f"The Shakti Peetha cycle rests on the Puranic narrative of Daksha’s yajna, Sati’s "
            f"self-immolation, and Shiva’s grief-stricken tandava. Vishnu’s Sudarshana chakra "
            f"is said to have dismembered Sati’s body; where each portion fell, a peetha of the "
            f"Goddess arose.\n\n"
            f"{name} at {loc} is counted among these seats in widely followed pilgrimage lists."
            f"{part_clause} "
            f"Scriptural enumerations differ (often 51, 52, or 108); Devi / Kalika Purana "
            f"traditions and later Pithanirnaya-style lists underpin how pilgrims map this "
            f"geography today.\n\n"
            f"{deity} is worshipped here as the living Shakti of the peetha — fierce or gentle "
            f"according to local form, yet always as the mother who sanctifies place through "
            f"the Sati–Shiva story."
        )
        local = (
            f"At {name}, priests and elders retell the peetha association"
            + (f" ({part})" if part else "")
            + f" as the reason devotees undertake long journeys for darshan of {deity}. "
            f"Navaratri, local jatras, and family kuladevi vows intensify belief that the "
            f"Goddess of this seat answers specifically here.\n\n"
            f"Offerings, colours of flowers or cloth, and animal-sacrifice customs (where still "
            f"practised under temple rules) vary by region — pilgrims are taught to follow "
            f"only what the local peetha permits.\n\n"
            f"Because peetha lists themselves vary, local tradition at the shrine is treated "
            f"as authoritative for ritual detail, while the pan-Indian Sati narrative supplies "
            f"the shared mythological frame."
        )
        scriptures = [
            "Puranic Sati–Daksha narrative (Devi / Kalika Purana traditions)",
            "Pithanirnaya / Shakti Peetha pilgrimage lists (enumerations vary)",
            "Local peetha sthala purana",
            DISCLAIMER_NOTE,
        ]
        return significance, local, scriptures

    sig_bits = []
    if existing and len(existing) > 80:
        sig_bits.append(existing)
    elif summary:
        sig_bits.append(summary)
    else:
        sig_bits.append(
            f"{name} at {loc} is dedicated to {deity}. "
            f"It occupies a recognised place in regional pilgrimage geography"
            + (f", known especially for {famous}" if famous else "")
            + "."
        )

    extras = []
    if "12-jyotirlinga" in tags:
        extras.append(
            f"In Jyotirlinga tradition drawn from the Shiva Purana cycle, {name} is counted "
            "among the twelve seats where Shiva is worshipped as a pillar of light."
        )
    if "char-dham" in tags:
        extras.append(
            f"{name} belongs to Adi Shankaracharya’s pan-India Char Dham — the four cardinal "
            "pilgrimage seats of Badrinath, Dwarka, Puri, and Rameswaram."
        )
    if "chota-char-dham" in tags:
        extras.append(
            f"Within Uttarakhand pilgrimage, {name} is part of the Chota Char Dham "
            "(Yamunotri–Gangotri–Kedarnath–Badrinath), distinct from the pan-India Char Dham."
        )
    if "panch-kedar" in tags:
        extras.append(
            "As a Panch Kedar shrine, it participates in the Garhwal legend that Shiva’s form "
            "was worshipped in five places after the Pandavas’ search."
        )
    if "pancha-bhuta" in tags:
        extras.append(
            "It is one of the Pancha Bhuta Sthalams of Tamil / South Indian Shaivism, where "
            "Shiva is linked to a fundamental element of nature."
        )
    if "ramayana-trail" in tags:
        extras.append(
            "Local and pan-Indian Ramayana trail devotion connects this place to Rama–Sita–"
            "Lakshmana geography as remembered in epic and regional telling."
        )
    if "mahabharata-sites" in tags:
        extras.append(
            "Mahabharata-linked sacred geography — battlefield, teaching, or Krishna traditions — "
            "frames the significance retained in epic and regional mahatmya."
        )

    joined = " ".join(sig_bits)
    for ex in extras:
        if ex and ex not in joined:
            sig_bits.append(ex)

    if len("\n\n".join(sig_bits)) < 400:
        sig_bits.append(
            f"Classical pilgrimage teaching places {name} within India’s tirtha network: "
            f"a location where devotion to {deity} is believed to ripen vows more readily than "
            f"in ordinary space. Epic, Puranic, and regional mahatmya literature — not a single "
            f"uniform text — sustain this sense of sacred geography."
        )

    significance = "\n\n".join(sig_bits)

    local_bits = []
    if famous:
        local_bits.append(
            f"In popular pilgrimage memory, {name} is especially associated with {famous}. "
            f"Guides and elders retell this identity to first-time visitors as the living "
            f"‘reason’ the tirtha draws crowds."
        )
    local_bits.extend(
        [
            f"Local sthala-purana and priestly teaching at {name} elaborate how {deity} blesses "
            f"devotees who arrive with vows, gratitude, or grief. Festival days intensify these "
            f"beliefs through processions, special alankara, and community feeding where practised.",
            f"Pilgrims commonly link practical customs — dress, queue, prasadam, and parikrama — "
            f"with spiritual fruit. Such customs are living belief: they vary by region and should "
            f"be followed as posted by the temple trust or endowment board.",
        ]
    )
    if "beyond-india" in tags:
        local_bits.append(
            "Because the shrine stands beyond India’s modern borders, local multi-lingual and "
            "sometimes multi-faith customs matter; respectful observance of host-country rules "
            "is part of the pilgrimage ethic."
        )

    local = "\n\n".join(local_bits)

    if not scriptures:
        scriptures = ["Puranic / epic traditions", "Local sthala purana", "Pilgrimage mahatmya lore"]
    if not any(DISCLAIMER_NOTE in s for s in scriptures):
        scriptures = scriptures + [DISCLAIMER_NOTE]

    return significance, local, scriptures


def _ensure_depth(d: dict) -> None:
    """Pad thin curated blurbs so every page has a readable story block."""
    name = d.get("name", "This temple")
    deity = d.get("deity", "the deity")
    sig = d.get("mythologySignificance") or ""
    local = d.get("localBeliefs") or ""
    if len(sig) < 360:
        sig = (
            sig.rstrip()
            + "\n\n"
            + f"Pilgrimage literature treats {name} as a tirtha — a crossing where devotion "
            + f"to {deity} is believed to bear fruit more readily than in ordinary space. "
            + "Accounts summarised here follow widely cited epic, Puranic, and regional "
            + "mahatmya traditions; temple priests remain the guides for ritual detail."
        )
        d["mythologySignificance"] = sig
    if len(local) < 280:
        local = (
            local.rstrip()
            + "\n\n"
            + f"First-time visitors often hear several versions of the same story from "
            + f"pandas, taxi guides, and elderly pilgrims — a reminder that local belief is "
            + f"living conversation, not a single fixed text."
        )
        d["localBeliefs"] = local


def main() -> None:
    updated = 0
    for path in sorted(TEMPLES.glob("*.json")):
        d = load(path)
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
            d["mythology"] = c["mythologySignificance"].split("\n\n")[0]
        else:
            sig, local, scriptures = expand_generic(d)
            d["mythologySignificance"] = sig
            d["localBeliefs"] = local
            d["scriptureLinks"] = scriptures
            d["mythology"] = sig.split("\n\n")[0]
        _ensure_depth(d)
        d["mythology"] = d["mythologySignificance"].split("\n\n")[0]
        d["mythologyDisclaimer"] = (
            "Mythological accounts and local beliefs are drawn from Puranic traditions, epics, "
            "and widely recorded sthala-purana / pilgrimage lore. Versions differ by scripture, "
            "region, and temple tradition. This section is for cultural understanding — not a "
            "claim of historical fact, nor a substitute for guidance from temple priests or "
            "official trusts."
        )
        dump(path, d)
        updated += 1
    print(f"Enriched mythology for {updated} temples.")


if __name__ == "__main__":
    main()
