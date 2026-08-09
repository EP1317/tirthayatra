#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append high-search myth stories (India + diaspora) to stories.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def S(**kw):
    return kw


NEW = [
    S(
        slug="samudra-manthan-kurma",
        title="Samudra Manthan — churning the ocean of milk",
        titleHi="समुद्र मंथन — क्षीरसागर और कूर्म अवतार",
        readSeconds=95,
        deity="vishnu",
        tags=["first-timer", "family", "ritual-why"],
        hook="Gods and asuras pulled one serpent — and the ocean gave poison, treasure, and amrita.",
        hookHi="देव और असुर ने एक नाग खींचा — सागर ने विष, रत्न और अमृत दिए।",
        whyRitual="Remembered in Vishnu temples, Southeast Asian reliefs (Angkor), and Neelkanth / Mohini tellings — cooperation, greed, and grace in one cosmic labour.",
        whyRitualHi="विष्णु मंदिरों, अंगकोर जैसी मूर्तिकला, और नीलकंठ–मोहिनी कथाओं में स्मृत — सहयोग, लोभ और कृपा का एक मंथन।",
        storyEn="When the gods lost their strength, Vishnu counselled a daring plan: churn the ocean of milk for amrita, the nectar of immortality — but only with the asuras’ help. Mount Mandara became the churning rod; Vasuki the serpent the rope. The mountain sank; Vishnu as Kurma, the great tortoise, bore it on his back. Asuras held Vasuki’s hoods, gods the tail, and the sea turned. First rose halahal poison — Shiva held it in his throat as Neelkanth. Then treasures emerged: the wish-cow, the horse Uchchaihshravas, the jewel Kaustubha, Lakshmi herself, and at last Dhanvantari with the pot of amrita. Dispute flared. Vishnu as Mohini distributed the nectar so dharma would not drown in endless war. The myth is beloved from India to Cambodia because it shows creation itself as a shared struggle — and warns that immortality without justice burns the worlds twice.",
        storyHi="जब देव दुर्बल हुए, विष्णु जी ने कहा — अमृत हेतु क्षीरसागर मथो, पर असुरों संग। मंदराचल मंथन-दंडा बना; वासुकि रस्सी। पर्वत डूबा तो विष्णु जी कूर्म रूप में पीठ पर थामे। असुर फन, देव पूँछ — सागर हिला। पहले हलाहल उठा; शिव जी ने कंठ में धर नीलकंठ कहलाए। फिर रत्न निकले — कामधेनु, उच्चैःश्रवा, कौस्तुभ, स्वयं लक्ष्मी जी, और अंत में धन्वंतरि जी अमृत-कलश संग। विवाद उठा। विष्णु जी मोहिनी रूप से अमृत बाँटे ताकि अधर्म अमर न हो। भारत से कंबोडिया तक प्रिय कथा — सृष्टि सहयोग है, और बिना न्याय अमरत्व लोक जलाता है।",
        takeaway="When a task feels too heavy alone, remember Kurma — steady support under the mountain of effort.",
        relatedDevotion=["vishnu-aarti", "lakshmi-aarti", "shiva-aarti"],
        relatedFestivals=["diwali", "maha-shivaratri"],
        relatedTemples=["tirumala-venkateswara", "padmanabhaswamy-thiruvananthapuram", "jagannath-puri", "kashi-vishwanath"],
    ),
    S(
        slug="krishna-makhan-chor",
        title="Krishna the butter thief",
        titleHi="कृष्ण जी मक्खन चोर",
        readSeconds=75,
        deity="krishna",
        tags=["family", "first-timer", "festival"],
        hook="The whole of Braj knew — the pot was empty because love had climbed the rafters.",
        hookHi="पूरा ब्रज जानता — मटकी खाली इसलिए कि प्रेम ने शहतीर चढ़ाई थी।",
        whyRitual="Janmashtami and Bal Gopal worship remember the child who stole butter — and stole hearts. Diaspora temples stage ‘makhan chor’ plays for children every year.",
        whyRitualHi="जन्माष्टमी और बाल गोपाल पूजा इसी बाल-लीला की स्मृति हैं। प्रवासी मंदिरों में बच्चों के ‘मक्खन चोर’ नाटक हर वर्ष होते हैं।",
        storyEn="In Gokul and Vrindavan, Yashoda and the gopis hung pots of fresh butter high from the ceiling. Yet each morning the pots were lighter. Footprints of curd, a flute’s giggle, friends boosted on shoulders — Bal Krishna and the cowherd boys had raided the stores again. When Yashoda caught him, his mouth was smeared white; his eyes wide with mischief that was never cruelty. The ‘theft’ is read as grace: the Lord takes what is offered in affection, and leaves the house richer in joy. Mothers still tie a tiny pot above the cradle of Laddu Gopal — inviting the same sweet trespass.",
        storyHi="गोकुल–वृंदावन में यशोदा जी और गोपियाँ मक्खन की मटकी ऊँची टाँगतीं। प्रातः फिर हल्की। दही के पदचिह्न, मुरली की हँसी, कंधों पर चढ़े सखा — बाल कृष्ण जी फिर लूट ले गए। जब यशोदा जी ने पकड़ा, मुँह सफेद, आँखें शरारत से भरी — क्रूरता नहीं। ‘चोरी’ कृपा है: प्रभु स्नेह से अर्पित लेते हैं और घर आनंद से भरते हैं। माताएँ लड्डू गोपाल के पालने पर छोटी मटकी बाँधती हैं — वही मीठी अतिक्रमण की न्योता।",
        takeaway="Offer a spoon of butter or milk sweets to Bal Gopal — laugh once like Braj before the day turns serious.",
        relatedDevotion=["krishna-aarti", "krishna-chalisa", "janmashtami-vrat-katha"],
        relatedFestivals=["janmashtami"],
        relatedTemples=["banke-bihari-vrindavan", "iskcon-vrindavan", "krishna-janmabhoomi-mathura", "guruvayur"],
    ),
    S(
        slug="krishna-virat-roop",
        title="Krishna reveals the Vishwarupa",
        titleHi="कृष्ण जी का विश्वरूप",
        readSeconds=90,
        deity="krishna",
        tags=["first-timer", "challenge"],
        hook="On the chariot at Kurukshetra, a friend became the sky that held every world.",
        hookHi="कुरुक्षेत्र के रथ पर सखा वह आकाश बन गए जिसमें सब लोक समाए।",
        whyRitual="Gita Jayanti and Bhagavad Gita path remember Chapter 11 — when teaching became vision. One of the most searched Krishna moments on YouTube worldwide.",
        whyRitualHi="गीता जयंती और भगवद्गीता पाठ अध्याय ११ याद करते हैं — जब उपदेश दर्शन बना। यूट्यूब पर सर्वाधिक खोजी कृष्ण घड़ियों में।",
        storyEn="Arjuna’s despair had already heard of the soul and of duty. Still he asked to see the truth behind his charioteer. Krishna granted divine sight. Then Arjuna beheld the Vishwarupa — countless faces and eyes, suns and weapons, gods and time itself devouring the armies that would fall. Terror and awe shook him; he saw that the war was already held within a larger order. He bowed, begged to see again the gentle human form of his friend, and received it. The vision does not glorify violence; it places finite fear inside infinite being — so courage can return without hatred.",
        storyHi="अर्जुन जी का शोक आत्मा और कर्तव्य सुन चुका था। फिर भी उन्होंने रथी के सत्य का दर्शन माँगा। कृष्ण जी ने दिव्य दृष्टि दी। तब विश्वरूप दिखा — अनगिनत मुख–नेत्र, सूर्य–शस्त्र, देव और काल जो आने वाली सेनाओं को ग्रसे हुए। भय और विस्मय से अर्जुन काँपे; समझे युद्ध किसी विशाल व्यवस्था में पहले से समाया है। झुके, फिर सखा का सौम्य नर रूप माँगा — और पाया। दर्शन हिंसा का गुणगान नहीं; परिमित भय को अनंत सत्ता में रखता है — ताकि द्वेष बिना साहस लौटे।",
        takeaway="Read or hear Gita Chapter 11 once — then look at one hard duty with a wider sky behind it.",
        relatedDevotion=["krishna-aarti", "vishnu-aarti", "bhagavad-gita-kurukshetra"],
        relatedFestivals=["janmashtami"],
        relatedTemples=["kurukshetra-brahmasarovar", "iskcon-vrindavan", "dwarka", "jagannath-puri"],
    ),
    S(
        slug="narasimha-hiranyakashipu",
        title="Narasimha and the end of Hiranyakashipu",
        titleHi="नरसिंह जी और हिरण्यकशिपु का अंत",
        readSeconds=90,
        deity="vishnu",
        tags=["festival", "family", "first-timer"],
        hook="Neither day nor night, neither indoors nor out — the boon had a gap, and devotion walked through it.",
        hookHi="न दिन न रात, न घर न बाहर — वर में दरार थी, भक्ति उसी से निकली।",
        whyRitual="Told at Holi with Prahlad’s fire story, and in Narasimha temples at Ahobilam and Yadagirigutta — the Lord who protects a child’s faith against a tyrant’s pride.",
        whyRitualHi="होली पर प्रह्लाद कथा संग, और नरसिंह मंदिरों में — बालक की भक्ति रक्षक प्रभु की गाथा।",
        storyEn="Hiranyakashipu’s boon seemed perfect: death not by man or beast, not by day or night, not indoors or outdoors, not by weapon. Drunk on safety, he demanded worship of himself alone. His son Prahlad would only name Vishnu. Rage filled the palace. At twilight — neither day nor night — on the palace threshold — neither in nor out — Vishnu appeared as Narasimha, man-lion, and ended the tyranny with claws that were not a forged weapon. The story is fierce because tyranny was fierce; its heart is the child who would not trade truth for fear.",
        storyHi="हिरण्यकशिपु का वर लगभग पूर्ण था — न नर न पशु, न दिन न रात, न घर न बाहर, न शस्त्र। अहंकार में उसने केवल अपनी पूजा माँगी। पुत्र प्रह्लाद केवल विष्णु नाम जपे। संध्या में — न दिन न रात — देहली पर — न भीतर न बाहर — विष्णु जी नरसिंह रूप आए; नखों से अधर्म का अंत किया। कथा उग्र है क्योंकि अत्याचार उग्र था; हृदय वह बालक है जिसने भय से सत्य नहीं बेचा।",
        takeaway="When fear demands a false worship — of ego, money, or silence — remember Prahlad’s single name.",
        relatedDevotion=["vishnu-aarti", "prahlad-holika"],
        relatedFestivals=["holi"],
        relatedTemples=["yadagirigutta", "simhachalam", "ahobilam-proxy", "tirumala-venkateswara"],
    ),
    S(
        slug="lakshman-rekha",
        title="The Lakshman Rekha",
        titleHi="लक्ष्मण रेखा",
        readSeconds=80,
        deity="rama",
        tags=["family", "first-timer"],
        hook="One line in the dust — and a kingdom’s sorrow waited just beyond it.",
        hookHi="धूल में एक रेखा — और उसके पार एक राज्य का शोक खड़ा था।",
        whyRitual="A household saying across India and the diaspora: ‘Don’t cross the Lakshman Rekha’ — a mythic warning about boundaries, trust, and the cost of a broken vow-line.",
        whyRitualHi="भारत और प्रवास में कहावत — ‘लक्ष्मण रेखा मत लाँघो’ — सीमा, विश्वास और टूटी मर्यादा की चेतावनी।",
        storyEn="In the forest hermitage, Rama left to chase a golden deer — Maricha’s illusion — at Sita’s request. Lakshmana stayed as guard. Sita, hearing what she thought was Rama’s cry, urged Lakshmana to go. Torn between duty to brother and duty to sister-in-law, he drew a protective line around the hut and begged her not to step beyond it. After he left, Ravana came as a mendicant. When Sita crossed the line to offer alms, the circle’s protection broke and she was seized. Tellings differ in detail; the enduring lesson is not blame of Sita — it is how deception hunts the moment a sacred boundary is treated lightly.",
        storyHi="वन में राम जी स्वर्ण मृग — मारीच माया — के पीछे गए। लक्ष्मण जी रक्षक रहे। सीता जी को राम की पुकार-सी सुनाई दी; उन्होंने लक्ष्मण को भेजा। कर्तव्य द्वन्द्व में लक्ष्मण जी ने कुटीर चारों ओर रक्षा-रेखा खींची — पार न जाएँ। उनके जाते ही रावण भिक्षुक वेश में आया। जब सीता जी भिक्षा हेतु रेखा लाँघी, रक्षा टूटी और हरण हुआ। विवरण भिन्न; शिक्षा सीता दोष नहीं — छल उसी क्षण टूटता है जब पवित्र सीमा हल्की लगे।",
        takeaway="Name one healthy boundary in your week — and keep it without cruelty.",
        relatedDevotion=["rama-aarti", "rama-chalisa", "ram-navami-vrat-katha"],
        relatedFestivals=["dussehra", "diwali"],
        relatedTemples=["ayodhya-ram-mandir", "bhadrachalam", "rameswaram", "chitrakoot-ramghat"],
    ),
    S(
        slug="ahalya-rama",
        title="Ahalya and Rama’s grace",
        titleHi="अहल्या और राम जी की कृपा",
        readSeconds=80,
        deity="rama",
        tags=["first-timer", "family"],
        hook="A stone waited in the ashram dust — until a footfall of compassion woke her.",
        hookHi="आश्रम धूल में एक शिला प्रतीक्षा कर रही थी — करुणा के चरण से जागी।",
        whyRitual="Recited in Ramayana path and temple storytelling; searched widely as ‘Ahalya uddhar’ — liberation through the Lord’s glance and touch of grace.",
        whyRitualHi="रामायण पाठ और मंदिर कथा में — ‘अहल्या उद्धार’ के रूप में खोजित; प्रभु कृपा से मुक्ति।",
        storyEn="Ahalya, wife of sage Gautama, was cursed to become stone — tellings vary on Indra’s deceit and her share of error. Years of still penance followed in the ashram. When young Rama walked the path with Vishvamitra toward Mithila, his feet touched the stone (or his glance fell upon her). The curse lifted; Ahalya rose restored, offered hospitality, and blessed the journey that would lead to Sita. The story is treasured because it frames Rama not only as warrior-king but as restorer — dignity returned without public shame.",
        storyHi="अहल्या, गौतम मुनि की पत्नी, शिला बन शापित रहीं — इंद्र छल और दोष-भाग की कथाएँ भिन्न। वर्षों तपःशिला। जब युवक राम जी विश्वामित्र संग मिथिला गए, चरण/दृष्टि पड़ी — शाप टूटा। अहल्या उठ खड़ी हुईं, आतिथ्य दिया, उस यात्रा को आशीष दी जो सीता तक ले गई। कथा प्रिय है क्योंकि राम केवल योद्धा नहीं — प्रतिष्ठा लौटाने वाले करुणासिंधु हैं।",
        takeaway="Offer one quiet kindness to someone stuck in old shame — restoration over spectacle.",
        relatedDevotion=["rama-aarti", "rama-chalisa"],
        relatedFestivals=["ram-navami"],
        relatedTemples=["ayodhya-ram-mandir", "bhadrachalam", "mithila-janakpur"],
    ),
    S(
        slug="ganesha-vyasa-mahabharata",
        title="Ganesha writes the Mahabharata",
        titleHi="गणेश जी महाभारत लिखते हैं",
        readSeconds=85,
        deity="ganesha",
        tags=["first-timer", "family", "challenge"],
        hook="Vyasa would speak only if the scribe never stopped — so Ganesha broke a tusk for ink and speed.",
        hookHi="व्यास बोलते यदि लेखक न रुके — गणेश जी ने वेग हेतु दंत तोड़ा।",
        whyRitual="A top search among students and writers: Ganesha as patron of letters. Reminds why new books, exams, and ledgers begin with his name.",
        whyRitualHi="छात्र–लेखकों की बड़ी खोज — विद्या के अधिष्ठाता गणेश। इसीलिए नयी पुस्तक, परीक्षा, खाता गणेश नाम से।",
        storyEn="Sage Vyasa had conceived the vast Mahabharata and needed a scribe equal to its flood. He asked Ganesha. Ganesha agreed on one condition: the dictation must never pause. Vyasa agreed on his own: Ganesha must understand each verse before writing. When the stylus broke under the torrent of verse, Ganesha snapped off his own tusk and wrote on — Ekadanta, the one-tusked lord. The epic was born from unbroken attention. The myth crowns buddhi over haste: wisdom that keeps writing even when the tool fails.",
        storyHi="व्यास जी के पास महाभारत का सागर था; लेखक चाहिए था। गणेश जी राजी — शर्त: लेखन न रुके। व्यास की शर्त: लिखने से पूर्व श्लोक समझें। वेग में शैली टूटी तो गणेश जी ने अपना दंत तोड़ लिखा — एकदंत। महाकाव्य अखंड ध्यान से जन्मा। कथा बुद्धि को जल्दबाजी पर मुकुट पहनाती है — औजार टूटे तो भी ज्ञान लिखता रहे।",
        takeaway="Before a hard writing or study block, whisper a Ganesha prayer — then work without checking the phone mid-flow.",
        relatedDevotion=["ganesha-aarti", "ganesha-chalisa", "ganesh-chaturthi-vrat-katha"],
        relatedFestivals=["ganesh-chaturthi"],
        relatedTemples=["siddhivinayak-mumbai", "moreshwar-morgaon", "kanipakam", "chintamani-theur"],
    ),
    S(
        slug="matsya-manu",
        title="Matsya and Manu — the fish who saved the world",
        titleHi="मत्स्य अवतार और मनु — मछली जिसने जगत बचाया",
        readSeconds=85,
        deity="vishnu",
        tags=["first-timer", "family"],
        hook="A tiny fish asked for shelter — and grew until only the flood could match it.",
        hookHi="छोटी मछली ने शरण माँगी — बढ़ती गई जब तक प्रलय उसके बराबर न हुआ।",
        whyRitual="Matsya Jayanti and dashavatara panels in temples abroad introduce Vishnu’s first avatar — conservation, warning, and a boat of seeds for a new age.",
        whyRitualHi="मत्स्य जयंती और दशावतार पट्टों में प्रथम अवतार — रक्षा, चेतावनी, और नये युग के बीज की नाव।",
        storyEn="King Manu found a small fish that begged protection from larger jaws. He moved it from pot to pond to river to sea as it grew divine. The fish — Vishnu as Matsya — warned of a coming deluge and told Manu to build a ship, gather seeds, sages, and the seven rishis. When the waters rose, Matsya towed the vessel to safety through the storm, restoring knowledge for the next cycle of the world. Flood myths worldwide echo this shape; in Hindu telling, divinity wears the form of what we are asked to save.",
        storyHi="राजा मनु को छोटी मछली मिली — बड़ी मछलियों से रक्षा माँगी। घड़े से सरोवर, नदी, सागर — बढ़ती दिव्य मत्स्य। वह विष्णु जी मत्स्य अवतार थे; प्रलय की चेतावनी दी — नाव बनाओ, बीज, मुनि, सप्तर्षि संग रखो। जल उछला तो मत्स्य ने नौका खींच सुरक्षित की; ज्ञान अगले कल्प हेतु बचा। विश्व की प्रलय कथाओं की छाया; यहाँ दिव्यता उसी रूप में आती है जिसकी रक्षा हमें सौंपी गई।",
        takeaway="Protect one small living thing or skill this week — the ‘tiny fish’ that may carry tomorrow.",
        relatedDevotion=["vishnu-aarti"],
        relatedFestivals=[],
        relatedTemples=["tirumala-venkateswara", "rameswaram", "padmanabhaswamy-thiruvananthapuram", "jagannath-puri"],
    ),
    S(
        slug="varaha-earth",
        title="Varaha lifts the Earth",
        titleHi="वराह अवतार — पृथ्वी का उद्धार",
        readSeconds=80,
        deity="vishnu",
        tags=["first-timer", "ritual-why"],
        hook="When the world sank into the cosmic dark, a boar’s tusk became the horizon again.",
        hookHi="जब धरती गहरे अंधकार में डूबी, वराह के दंत ने क्षितिज लौटाया।",
        whyRitual="Varaha Jayanti and temple icons (Khajuraho to South Indian vimanas) celebrate the Earth restored — ecology as devotion avant la lettre.",
        whyRitualHi="वराह जयंती और मंदिर मूर्तियों में — धरती का उद्धार; पर्यावरण भक्ति का प्राचीन रूप।",
        storyEn="The demon Hiranyaksha dragged the Earth (Bhudevi) into the cosmic waters. Vishnu took the form of Varaha, a gigantic boar, dove into the depths, fought the asura, and raised the Earth upon his tusk, setting her again upon the waters of space. Artists carve the moment as tenderness as much as triumph — the planet held carefully, not conquered. In an age of climate anxiety, the myth returns as prayer: the ground beneath us is divine and worth the dive.",
        storyHi="असुर हिरण्याक्ष ने पृथ्वी (भूदेवी) को रसातल खींचा। विष्णु जी विशाल वराह बने, गहराई में गए, असुर से जूझे, दंत पर धरती उठा अंतरिक्ष जल पर पुनः टिकाई। शिल्प में यह क्षण विजय जितना कोमल भी है — ग्रह सावधानी से थामा, रौंदा नहीं। जलवायु चिंता के युग में कथा प्रार्थना बनती है: पैर तले भूमि दिव्य है, गोता लगाने योग्य।",
        takeaway="Touch the soil or a houseplant with thanks — Bhudevi under Varaha’s care.",
        relatedDevotion=["vishnu-aarti"],
        relatedFestivals=[],
        relatedTemples=["tirumala-venkateswara", "srirangam-ranganathaswamy", "badrinath", "jagannath-puri"],
    ),
    S(
        slug="shravan-kumar",
        title="Shravan Kumar — the son who carried his parents",
        titleHi="श्रवण कुमार — माता–पिता को कंधे पर उठाने वाला पुत्र",
        readSeconds=85,
        deity="rama",
        tags=["family", "first-timer"],
        hook="A bamboo sling, two blind parents, and a journey cut short by a king’s arrow.",
        hookHi="बाँस की काँवर, अंधे माता–पिता, और राजा के बाण से टूटी यात्रा।",
        whyRitual="Among India’s most searched ideal-son stories; told on days of pitru devotion and in Ramayana context — Dasharatha’s sorrow that later shapes Rama’s exile.",
        whyRitualHi="भारत की सर्वाधिक खोजी आदर्श-पुत्र कथाओं में; पितृ-स्मृति और रामायण संदर्भ — दशरथ शोक जो राम वनवास तक छाया है।",
        storyEn="Shravan Kumar carried his blind parents in a shoulder-sling (kanwar) on pilgrimage to sacred waters. At a riverside he filled a pot; King Dasharatha, hunting by sound, mistook the splash for a deer and loosed an arrow. Shravan fell. Dying, he asked only that the king take water to his parents and confess. Their grief cursed Dasharatha to die longing for his own son — a thread that later tightens when Rama leaves for the forest. The story is loved not for tragedy alone but for seva: carrying the old is itself a tirtha.",
        storyHi="श्रवण कुमार ने अंधे माता–पिता को काँवर में उठा तीर्थ यात्रा की। नदी पर जल भरते दशरथ ने छप–छप सुन मृग समझ बाण मारा। श्रवण गिरे; मरते हुए कहा — जल माता–पिता को दो और सत्य कहो। उनके शोक ने दशरथ को शाप दिया — पुत्र-वियोग में मृत्यु। वही सूत्र बाद में राम वनवास पर कसता है। कथा केवल दुख नहीं — सेवा: वृद्ध को उठाना स्वयं तीर्थ है।",
        takeaway="Call or help a parent or elder today — one small ‘kanwar’ of care.",
        relatedDevotion=["rama-aarti", "rama-chalisa"],
        relatedFestivals=[],
        relatedTemples=["ayodhya-ram-mandir", "chitrakoot-ramghat", "rameswaram", "gangotri"],
    ),
    S(
        slug="bhishma-pratigya",
        title="Bhishma’s terrible vow",
        titleHi="भीष्म प्रतिज्ञा",
        readSeconds=90,
        deity="krishna",
        tags=["challenge", "first-timer"],
        hook="A prince gave up the throne and marriage — and the heavens named him Bhishma, the Terrible.",
        hookHi="राजकुमार ने सिंहासन और विवाह त्यागे — स्वर्ग ने उन्हें भीष्म कहा।",
        whyRitual="Bhishma Ashtami and Mahabharata tellings keep this vow alive; diaspora seekers search ‘Bhishma pratigya’ as the gold standard of kept word.",
        whyRitualHi="भीष्माष्टमी और महाभारत कथा में जीवित; प्रवास में ‘भीष्म प्रतिज्ञा’ वचन-पालन का मानक खोज।",
        storyEn="Devavrata, son of Shantanu and Ganga, saw his father love the fisher-maiden Satyavati, whose father demanded that her sons inherit the throne. To clear the path, Devavrata vowed lifelong brahmacharya and renounced kingship for himself and any offspring. The gods cried ‘Bhishma!’ — for the vow was dreadful in its cost. He kept it through palace intrigue and war, becoming the grandsire who could not die until he willed, lying on arrows at Kurukshetra teaching dharma to the victors. The myth asks what a kept promise costs — and whether silence for another’s desire can become both glory and tragedy.",
        storyHi="देवव्रत, शांतनु–गंगा पुत्र, ने पिता का सत्यवती प्रेम देखा; उसके पिता ने माँगा — सिंहासन उसके पुत्रों का हो। मार्ग साफ करने देवव्रत ने आजीवन ब्रह्मचर्य और राजत्याग की प्रतिज्ञा की। देवताओं ने कहा ‘भीष्म!’ — मूल्य भयंकर था। उन्होंने उसे निभाया; कुरुक्षेत्र में शरशय्या पर विजेताओं को धर्म सिखाया। कथा पूछती है — निभाया वचन क्या मोल लेता है, और दूसरे की चाह हेतु मौन कभी महिमा कभी त्रासदी कब बनता है।",
        takeaway="Keep one small promise today exactly — practice for the large ones.",
        relatedDevotion=["krishna-aarti", "vishnu-aarti"],
        relatedFestivals=[],
        relatedTemples=["kurukshetra-brahmasarovar", "gangotri", "badrinath", "kashi-vishwanath"],
    ),
    S(
        slug="kali-raktabija",
        title="Kali and the demon Raktabija",
        titleHi="काली जी और रक्तबीज असुर",
        readSeconds=85,
        deity="devi",
        tags=["festival", "first-timer"],
        hook="Every drop of his blood became a clone — until the Mother drank the battlefield dry of fear.",
        hookHi="रक्त की प्रत्येक बूँद से नया असुर — तब माँ ने रण का भय पी लिया।",
        whyRitual="Told in Devi Mahatmya cycles during Navaratri and Kali Puja; high search for ‘Kali Raktabija’ among devotees and diaspora goddess festivals.",
        whyRitualHi="देवी माहात्म्य, नवरात्रि और काली पूजा में; ‘काली रक्तबीज’ भक्तों और प्रवासी देवी उत्सवों की बड़ी खोज।",
        storyEn="Raktabija had a boon: every drop of his blood that touched the earth would birth another demon like him. Ordinary battle multiplied the enemy. Then Kali manifested in her fierce compassion — stretching her tongue across the field, she drank the falling blood before it seeded new rage, and destroyed the horde. The image is fierce; the meaning is psychological as much as mythic: some afflictions reproduce when fought carelessly; wisdom contains the leak. After victory, Shiva is said to have calmed her — fury returning to peace when the work is done.",
        storyHi="रक्तबीज को वर था — भूमि पर गिरी रक्त-बूँद से उसके जैसा असुर जन्मे। साधारण युद्ध शत्रु बढ़ाता। तब काली जी प्रकट हुईं — जिह्वा फैला रक्त भूमि पर गिरने से पहले पान किया, सेना का अंत किया। रूप उग्र; अर्थ मानसिक भी — कुछ क्लेश लापरवाह संघर्ष से फैलते हैं; विवेक रिसाव रोकता है। विजय बाद शिव ने शांत किया — कार्य पूर्ण होने पर रोष शांति में लौटे।",
        takeaway="On a hard day, name the ‘blood drop’ habit that multiplies stress — contain it once before it clones.",
        relatedDevotion=["kali-aarti", "devi-aarti", "navaratri-vrat-katha"],
        relatedFestivals=["navaratri"],
        relatedTemples=["kalighat", "dakshineswar-kali", "kamakhya", "vaishno-devi"],
    ),
    S(
        slug="putana-krishna",
        title="Krishna and the demoness Putana",
        titleHi="कृष्ण जी और पूतना",
        readSeconds=75,
        deity="krishna",
        tags=["family", "first-timer", "festival"],
        hook="She came as a nurse with poisoned milk — the infant drank, and fear itself failed.",
        hookHi="विषैले दूध संग धाय बन आई — शिशु ने पिया, और भय हार गया।",
        whyRitual="A staple of Bal Krishna cartoons and Janmashtami children’s programmes in India and abroad — the baby who protects the cradle.",
        whyRitualHi="बाल कृष्ण कार्टून और जन्माष्टमी बाल कार्यक्रमों की मुख्य कथा — पालना रक्षक शिशु।",
        storyEn="Kamsa sent Putana to kill the prophesied child. She smeared poison on her breast and entered Gokul as a beautiful nurse. When she offered milk to infant Krishna, he drank — and with the milk drew out her life and her asura form. She fell enormous and dead; the villagers cut and burned the body, and the air smelled strangely sweet — even her end purified by contact with the Lord. The tale comforts parents: grace can meet danger at the cradle’s edge.",
        storyHi="कंस ने पूतना को बालक मारने भेजा। उसने स्तन पर विष लगाया, सुंदर धाय बन गोकुल घुसी। बाल कृष्ण जी ने दूध संग उसका प्राण और असुर रूप खींच लिया। वह विशाल गिर मरी; गोपों ने दाह किया — स्पर्श से अंत भी शुद्ध-सा गंधाया। कथा माता–पिता को सांत्वना देती है: पालने की दहलीज पर भी कृपा खतरे से मिल सकती है।",
        takeaway="Rock a cradle or light a lamp for a child in your life — protectiveness as prayer.",
        relatedDevotion=["krishna-aarti", "janmashtami-vrat-katha"],
        relatedFestivals=["janmashtami"],
        relatedTemples=["krishna-janmabhoomi-mathura", "banke-bihari-vrindavan", "iskcon-vrindavan", "guruvayur"],
    ),
    S(
        slug="narakasura-krishna",
        title="Krishna and the defeat of Narakasura",
        titleHi="कृष्ण जी और नरकासुर वध",
        readSeconds=80,
        deity="krishna",
        tags=["festival", "family", "first-timer"],
        hook="Sixteen thousand imprisoned lights — and a dawn that became Naraka Chaturdashi.",
        hookHi="सोलह हज़ार क़ैद ज्योतियाँ — और वह प्रभात जो नरक चतुर्दशी बना।",
        whyRitual="Naraka Chaturdashi / Chhoti Diwali remembers this victory: oil bath, lamps, and the end of a tyrant who stole freedom. Huge pre-Diwali search spike in India and diaspora.",
        whyRitualHi="नरक चतुर्दशी / छोटी दीपावली — तेल स्नान, दीप, और स्वतंत्रता हरण करने वाले असुर का अंत। दीपावली पूर्व बड़ी खोज।",
        storyEn="Narakasura of Pragjyotisha seized heavenly treasures and imprisoned many women. Krishna, with Satyabhama in many tellings, rode to war, slew the demon, and freed the captives. Tradition says the earth felt relief at dawn — hence the ritual oil bath and lamps that push back ‘naraka’ (misery) before the main Diwali night. The myth pairs with Rama’s lamps: one story of homecoming, one of liberation from a dungeon of greed.",
        storyHi="प्राग्ज्योतिष के नरकासुर ने स्वर्गीय रत्न हरे, अनेक स्त्रियों को क़ैद किया। कृष्ण जी — कई कथाओं में सत्यभामा संग — युद्ध कर असुर का वध किया, बन्दियों को मुक्त किया। परंपरा कहती है पृथ्वी ने प्रभात में राहत ली — इसलिए दीपावली से पूर्व तेल स्नान और दीप जो ‘नरक’ (दुर्गति) पीछे धकेलते हैं। कथा राम-दीपों की बहन: एक घर वापसी, एक लालच-कारागार से मुक्ति।",
        takeaway="On Chhoti Diwali morning, oil lamp or shower with intention — wash one resentment before the feast.",
        relatedDevotion=["krishna-aarti", "lakshmi-aarti"],
        relatedFestivals=["diwali", "dhanteras"],
        relatedTemples=["dwarka", "banke-bihari-vrindavan", "tirumala-venkateswara", "jagannath-puri"],
    ),
    S(
        slug="sita-swayamvara-bow",
        title="Rama breaks Shiva’s bow",
        titleHi="राम जी शिव धनुष तोड़ते हैं",
        readSeconds=80,
        deity="rama",
        tags=["festival", "family", "first-timer"],
        hook="In Janaka’s hall the bow that none could string became a bridge to Sita.",
        hookHi="जनक सभा में जो धनुष कोई न चढ़ा सका — वह सीता तक सेतु बना।",
        whyRitual="Ram Navami dramas and wedding blessings recall the swayamvara — strength that serves partnership, not display. Popular in diaspora Ramayana plays.",
        whyRitualHi="राम नवमी नाटक और विवाह आशीष में स्वयंवर स्मृत — बल प्रदर्शन नहीं, साझेदारी हेतु। प्रवासी रामलीला में लोकप्रिय।",
        storyEn="King Janaka vowed that Sita would marry only the one who could string the great bow of Shiva. Princes failed; the bow would not bend. Rama, guided by Vishvamitra, lifted it with calm ease — and as he drew the string, the bow broke with a thunder that shook the hall. Sita garlanded him. The moment is less about muscle than about adhikara: the right to protect and walk with Shakti when the time and grace align.",
        storyHi="जनक ने प्रतिज्ञा की — जो शिव धनुष चढ़ाए वही सीता वर। राजकुमार हारे; धनुष न झुका। राम जी विश्वामित्र संग शांत भाव से उठाए — प्रत्यंचा चढ़ाते धनुष गर्जना संग टूटा। सीता जी ने जयमाल पहनाई। क्षण पेशीबल का नहीं, अधिकार का है — जब समय और कृपा संग हों तो शक्ति संग चलने का अधिकार।",
        takeaway="Before a commitment (work or relationship), ask if your strength is for partnership — then act cleanly.",
        relatedDevotion=["rama-aarti", "rama-chalisa", "ram-navami-vrat-katha"],
        relatedFestivals=["ram-navami"],
        relatedTemples=["ayodhya-ram-mandir", "mithila-janakpur", "bhadrachalam", "rameswaram"],
    ),
]


def main():
    stories_path = ROOT / "data" / "stories.json"
    data = json.loads(stories_path.read_text(encoding="utf-8"))
    existing = {s["slug"] for s in data["stories"]}
    # fix bad temple refs
    for s in NEW:
        s["relatedTemples"] = [t for t in s["relatedTemples"] if t != "ahobilam-proxy"]
        if s["slug"] == "narasimha-hiranyakashipu":
            s["relatedTemples"] = ["yadagirigutta", "simhachalam", "tirumala-venkateswara", "jagannath-puri"]
        # relatedDevotion story slugs shouldn't be in devotion - fix virat
        if s["slug"] == "krishna-virat-roop":
            s["relatedDevotion"] = ["krishna-aarti", "vishnu-aarti"]
        if s["slug"] == "narasimha-hiranyakashipu":
            s["relatedDevotion"] = ["vishnu-aarti"]

    added = []
    for s in NEW:
        if s["slug"] in existing:
            # replace to allow updates
            data["stories"] = [x for x in data["stories"] if x["slug"] != s["slug"]]
        data["stories"].append(s)
        added.append(s["slug"])

    stories_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    eng_path = ROOT / "data" / "engagement.json"
    eng = json.loads(eng_path.read_text(encoding="utf-8"))
    rot = eng.setdefault("dailyRotation", {})
    story_rot = list(rot.get("story") or [])
    for slug in added:
        if slug not in story_rot:
            story_rot.append(slug)
    rot["story"] = story_rot

    # freshen social proof with new hits
    eng["socialProof"]["mostLoved"].insert(
        1,
        {
            "type": "story",
            "slug": "krishna-makhan-chor",
            "label": "Kids’ favourite",
            "blurb": "Makhan chor — the butter thief of Braj.",
        },
    )
    # dedupe mostLoved by slug keep first
    seen = set()
    cleaned = []
    for item in eng["socialProof"]["mostLoved"]:
        key = (item.get("type"), item.get("slug"))
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
    eng["socialProof"]["mostLoved"] = cleaned[:6]

    eng["socialProof"]["firstTimers"].insert(
        0,
        {
            "type": "story",
            "slug": "samudra-manthan-kurma",
            "label": "Epic classic",
            "blurb": "Ocean churning — Kurma, poison, amrita.",
        },
    )
    seen = set()
    cleaned = []
    for item in eng["socialProof"]["firstTimers"]:
        key = (item.get("type"), item.get("slug"))
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
    eng["socialProof"]["firstTimers"] = cleaned[:6]

    eng_path.write_text(json.dumps(eng, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Stories total: {len(data['stories'])}")
    print("Added/updated:", ", ".join(added))


if __name__ == "__main__":
    main()
