#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add top Google/YouTube-searched & high-footfall temples missing per Indian state.
Uses reported/approximate visitor signals in famousFor where known; otherwise
'high search / regional footfall' based on pilgrimage popularity.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLES = DATA / "temples"
sys.path.insert(0, str(ROOT / "scripts"))
from sync_groups import base_detail, dump_json, load_json  # type: ignore

PORTALS = load_json(DATA / "state-portals.json")

# Extra state portals for states we newly cover
NEW_PORTALS = {
    "Sikkim": {
        "slug": "sikkim",
        "portalName": "Sikkim Tourism",
        "portalUrl": "https://www.sikkimtourism.gov.in/",
        "also": [],
        "note": "Namchi Siddheshwar Dham and regional Hindu shrines.",
    },
    "Manipur": {
        "slug": "manipur",
        "portalName": "Manipur Tourism",
        "portalUrl": "https://manipurtourism.gov.in/",
        "also": [],
        "note": "Govindajee Temple and Vaishnava heritage of Imphal.",
    },
    "Arunachal Pradesh": {
        "slug": "arunachal-pradesh",
        "portalName": "Arunachal Tourism",
        "portalUrl": "https://arunachaltourism.com/",
        "also": [],
        "note": "Parshuram Kund and Malinithan pilgrimage.",
    },
    "Puducherry": {
        "slug": "puducherry",
        "portalName": "Puducherry Tourism",
        "portalUrl": "https://www.pondytourism.in/",
        "also": [],
        "note": "Manakula Vinayagar and French-era temple town culture.",
    },
}


def T(**kw):
    return kw


# Curated gaps: skip slugs already present. Aim ~top-10 coverage per state.
NEW = [
    # —— Assam (have Kamakhya) ——
    T(slug="hayagriva-madhava-hajo", name="Hayagriva Madhava Temple, Hajo", deity="Lord Hayagriva Madhava (Vishnu)", location="Hajo, Kamrup, Assam", state="Assam", glyph="ह", famousFor="Major Assam Vaishnava shrine · high regional search with Kamakhya circuit", summary="Hajo’s Hayagriva Madhava — among Assam’s most visited Vishnu temples after Kamakhya.", mythology="Hayagriva Madhava is worshipped as Vishnu’s horse-headed wisdom form. Hajo is a multi-faith pilgrimage town; Hindu tradition places this hill shrine among Assam’s oldest Vaishnava seats.", lat=26.248, lng=91.526, mapQuery="Hayagriva Madhava Temple Hajo", nearestRail="Guwahati", nearestAirport="Guwahati", festivals=["Dol Yatra", "Janmashtami"]),
    T(slug="umananda-guwahati", name="Umananda Temple, Guwahati", deity="Lord Shiva (Umananda)", location="Peacock Island, Brahmaputra, Guwahati, Assam", state="Assam", glyph="उ", famousFor="Island Shiva temple · top Guwahati YouTube / boat-darshan search", summary="Umananda on Peacock Island — Assam’s iconic river-island Shiva shrine.", mythology="Tradition links the island linga to Shiva–Parvati lore and the Brahmaputra’s sacred geography. Ferry darshan is part of the Guwahati pilgrim experience.", lat=26.196, lng=91.745, mapQuery="Umananda Temple Guwahati", nearestRail="Guwahati", nearestAirport="Guwahati"),
    T(slug="navagraha-guwahati", name="Navagraha Temple, Guwahati", deity="Navagraha (nine planetary deities)", location="Chitrachal Hill, Guwahati, Assam", state="Assam", glyph="न", famousFor="Assam’s planetary shrine · high astrology-pilgrim search", summary="Navagraha hill temple overlooking Guwahati — popular for graha shanti vows.", mythology="Nine shrines for the planetary deities crown Chitrachal. Pilgrims combine it with Kamakhya on city yatras.", lat=26.183, lng=91.768, mapQuery="Navagraha Temple Guwahati", nearestRail="Guwahati", nearestAirport="Guwahati"),
    T(slug="basistha-ashram", name="Basistha Temple, Guwahati", deity="Lord Shiva (Basistha)", location="Basistha, Guwahati, Assam", state="Assam", glyph="ब", famousFor="Sage Basistha lore · popular Guwahati weekend tirtha", summary="Basistha ashram-temple — Shiva shrine tied to sage Vasistha’s Assam legend.", mythology="Local tradition places sage Vasistha’s hermitage here. The waterfall setting and Shiva temple draw city and regional pilgrims.", lat=26.100, lng=91.780, mapQuery="Basistha Temple Guwahati", nearestRail="Guwahati", nearestAirport="Guwahati"),
    T(slug="dirgheswari-temple", name="Dirgheswari Temple, North Guwahati", deity="Goddess Dirgheswari (Devi)", location="North Guwahati, Assam", state="Assam", glyph="दी", famousFor="Devi shrine · Durga Puja crowds across Brahmaputra", summary="Dirgheswari — important Devi temple of North Guwahati often paired with Kamakhya.", mythology="Counted among Assam’s living Shakti seats in popular devotion. Durga Puja draws large local footfall.", lat=26.225, lng=91.720, mapQuery="Dirgheswari Temple Guwahati", nearestRail="Guwahati", nearestAirport="Guwahati"),
    T(slug="sukreswar-guwahati", name="Sukreswar Temple, Guwahati", deity="Lord Shiva (Sukreswar)", location="Panbazar ghat, Guwahati, Assam", state="Assam", glyph="सु", famousFor="Brahmaputra-ghat Shiva · old Guwahati landmark search", summary="Sukreswar — riverside Shiva temple on the Brahmaputra embankment.", mythology="An ancient urban Shiva seat; evening aarti by the river is a Guwahati classic.", lat=26.187, lng=91.740, mapQuery="Sukreswar Temple Guwahati", nearestRail="Guwahati", nearestAirport="Guwahati"),
    T(slug="ashwaklanta-guwahati", name="Aswaklanta Temple, North Guwahati", deity="Lord Krishna / Vishnu", location="North Guwahati, Assam", state="Assam", glyph="अ", famousFor="Krishna–Arjuna horse legend · Assam Vaishnava search", summary="Asvaklanta — hill temple linked to Krishna–Arjuna lore on the Brahmaputra’s north bank.", mythology="Sthala tradition recalls Krishna’s horse resting here (aswa-klanta). Dual shrines and river views make it a steady regional draw.", lat=26.210, lng=91.705, mapQuery="Asvaklanta Temple Guwahati", nearestRail="Guwahati", nearestAirport="Guwahati"),
    T(slug="doul-govinda-guwahati", name="Doul Govinda Temple, North Guwahati", deity="Lord Krishna (Govinda)", location="Rajaduar, North Guwahati, Assam", state="Assam", glyph="दौ", famousFor="Holi / Doul festival crowds · Assam Krishna temple search", summary="Doul Govinda — Vaishnava temple famous for colourful Doul (Holi) celebrations.", mythology="Govinda worship here is woven into Assam’s Holi–Doul culture; festival weeks see peak footfall.", lat=26.220, lng=91.730, mapQuery="Doul Govinda Temple", nearestRail="Guwahati", nearestAirport="Guwahati"),
    T(slug="maha-mrityunjay-nagaon", name="Maha Mrityunjay Temple, Nagaon", deity="Lord Shiva (Mrityunjay)", location="Pithaikhowa, Nagaon, Assam", state="Assam", glyph="मृ", famousFor="Giant lingam · viral YouTube / Assam pilgrimage search", summary="Maha Mrityunjay Mandir near Nagaon — modern Assam landmark with a colossal Shiva lingam.", mythology="A contemporary pilgrimage centre dedicated to Mrityunjaya Shiva; large-scale iconography drives national video search interest.", lat=26.350, lng=92.690, mapQuery="Maha Mrityunjay Temple Nagaon", nearestRail="Nagaon", nearestAirport="Guwahati / Tezpur"),

    # —— Bihar ——
    T(slug="mundeshwari-devi", name="Mundeshwari Devi Temple", deity="Goddess Mundeshwari & Lord Shiva", location="Bhabua, Kaimur, Bihar", state="Bihar", glyph="मु", famousFor="Among India’s oldest living temples · ASI / high heritage search", summary="Mundeshwari — octagonal hill shrine often cited as one of India’s oldest continuously worshipped temples.", mythology="Devi and Shiva share an ancient Nagara-period temple. Archaeology and living worship both draw researchers and pilgrims.", lat=24.984, lng=83.564, mapQuery="Mundeshwari Temple Bihar", nearestRail="Bhabua Road", nearestAirport="Varanasi / Gaya"),
    T(slug="patan-devi-patna", name="Patan Devi Temple, Patna", deity="Goddess Patan Devi", location="Patna, Bihar", state="Bihar", glyph="प", famousFor="Patna’s city Devi · high local footfall & search", summary="Patan Devi — twin Bari/Chhoti Patan Devi shrines anchoring Patna’s Shakti devotion.", mythology="Popularly linked with Shakti Peetha lore of the ‘pat’ (cloth/portion) of Sati. Navaratri fills the lanes.", lat=25.610, lng=85.140, mapQuery="Patan Devi Temple Patna", nearestRail="Patna Junction", nearestAirport="Patna"),
    T(slug="mangla-gauri-gaya", name="Mangla Gauri Temple, Gaya", deity="Goddess Mangla Gauri", location="Gaya, Bihar", state="Bihar", glyph="मं", famousFor="Shakti seat with Vishnupad · Shraddha-season crowds", summary="Mangla Gauri hill — Devi temple combined with Gaya’s pind-daan pilgrimage economy.", mythology="Counted among important Shakti sites; women especially vow here during Shravan and Navaratri.", lat=24.775, lng=85.000, mapQuery="Mangla Gauri Temple Gaya", nearestRail="Gaya Junction", nearestAirport="Gaya"),
    T(slug="ajgaibinath-sultanganj", name="Ajgaibinath Temple, Sultanganj", deity="Lord Shiva (Ajgaibinath)", location="Sultanganj, Bhagalpur, Bihar", state="Bihar", glyph="अज", famousFor="Kawariya Ganga jal origin · crores seasonal search (Sawan)", summary="Ajgaibinath — island-adjacent Shiva temple where Kawad pilgrims collect Ganga water for Deoghar.", mythology="Sultanganj’s Shiva sits by the Ganga; Sawan Kawad yatra makes this one of Bihar’s highest seasonal-search temples.", lat=25.246, lng=86.738, mapQuery="Ajgaibinath Temple Sultanganj", nearestRail="Sultanganj", nearestAirport="Patna / Deoghar"),
    T(slug="thawe-mandir", name="Thawe Mandir, Gopalganj", deity="Goddess Thawewali Mai", location="Thawe, Gopalganj, Bihar", state="Bihar", glyph="था", famousFor="Massive mela footfall · top north-Bihar Devi search", summary="Thawe Mandir — powerful regional Devi shrine with huge fair crowds.", mythology="Local royalty and folk devotion built Thawewali Mai’s fame; Chhath and Navaratri seasons peak.", lat=26.430, lng=84.370, mapQuery="Thawe Mandir Gopalganj", nearestRail="Thawe / Siwan", nearestAirport="Patna / Gorakhpur"),
    T(slug="sitamarhi-janaki", name="Janaki Temple, Sitamarhi", deity="Goddess Sita (Janaki)", location="Sitamarhi, Bihar", state="Bihar", glyph="सी", famousFor="Sita birthplace tradition · Ramayana trail search", summary="Sitamarhi’s Janaki temple — popularly remembered as Sita’s birthplace region.", mythology="Ramayana geography places Janaka’s Mithila nearby; Sitamarhi temples celebrate Sita’s appearance lore for diaspora and domestic Ram bhakti.", lat=26.593, lng=85.503, mapQuery="Janaki Mandir Sitamarhi", nearestRail="Sitamarhi", nearestAirport="Darbhanga / Patna"),
    T(slug="sun-temple-deo", name="Sun Temple, Deo", deity="Surya (Sun God)", location="Deo, Aurangabad, Bihar", state="Bihar", glyph="सू", famousFor="Chhath / Surya heritage · Bihar sun-temple search", summary="Deo Sun Temple — rare standing Surya shrine of Magadh, active especially around Chhath.", mythology="Magadh’s solar worship tradition survives in Deo’s stone temple; Chhath ties Surya devotion to living practice.", lat=24.660, lng=84.430, mapQuery="Deo Sun Temple Bihar", nearestRail="Anugraha Narayan Road / Gaya", nearestAirport="Gaya"),

    # —— Chhattisgarh ——
    T(slug="bambleshwari-dongargarh", name="Bambleshwari Temple, Dongargarh", deity="Goddess Bambleshwari", location="Dongargarh, Rajnandgaon, Chhattisgarh", state="Chhattisgarh", glyph="बं", famousFor="Hill Devi · among CG’s highest pilgrim searches", summary="Maa Bambleshwari of Dongargarh — Chhattisgarh’s premier Devi hill temple.", mythology="Twin temples (main hill and valley) draw Navaratri crowds from across central India.", lat=21.190, lng=80.780, mapQuery="Bambleshwari Temple Dongargarh", nearestRail="Dongargarh", nearestAirport="Raipur"),
    T(slug="mahamaya-ratanpur", name="Mahamaya Temple, Ratanpur", deity="Goddess Mahamaya", location="Ratanpur, Bilaspur, Chhattisgarh", state="Chhattisgarh", glyph="म", famousFor="Kalchuri-era Devi · Bilaspur circuit search", summary="Mahamaya Ratanpur — historic capital’s Devi temple, still a major CG tirtha.", mythology="Kalchuri kings patronised Mahamaya; the shrine remains Bilaspur region’s spiritual anchor.", lat=22.288, lng=82.168, mapQuery="Mahamaya Temple Ratanpur", nearestRail="Usslipur / Ratanpur", nearestAirport="Raipur"),
    T(slug="rajim-kuleshwar", name="Kuleshwar Temple, Rajim", deity="Lord Shiva (Kuleshwar) & Rajivalochan", location="Rajim, Gariaband, Chhattisgarh", state="Chhattisgarh", glyph="रा", famousFor="Rajim Kumbh · Triveni sangam pilgrimage search", summary="Rajim — ‘Prayag of Chhattisgarh’ with Kuleshwar and Rajivalochan temples at river confluence.", mythology="Three rivers meet; Shiva and Vishnu shrines share the Kumbh-scale mela fame of Rajim.", lat=20.966, lng=81.883, mapQuery="Rajim Temple Chhattisgarh", nearestRail="Raipur / Rajim area", nearestAirport="Raipur"),
    T(slug="giraudpuri-dham", name="Giraudpuri Dham", deity="Guru Ghasidas / Satnam tradition shrine", location="Giraudpuri, Baloda Bazar, Chhattisgarh", state="Chhattisgarh", glyph="गि", famousFor="Massive jaitkhamb fair · high CG social search", summary="Giraudpuri — Satnami pilgrimage centre with enormous annual footfall.", mythology="Sacred to the Satnam Panth of Guru Ghasidas; the jaitkhamb gathering is among central India’s largest faith fairs.", lat=21.750, lng=82.200, mapQuery="Giraudpuri Dham", nearestRail="Raipur / Bhatapara", nearestAirport="Raipur"),
    T(slug="chandrahasini-devi", name="Chandrahasini Devi Temple", deity="Goddess Chandrahasini", location="Chandrapur, Janjgir-Champa, Chhattisgarh", state="Chhattisgarh", glyph="च", famousFor="Mahanadi Devi · regional Navaratri crowds", summary="Chandrahasini on the Mahanadi — popular Devi temple of Janjgir region.", mythology="Riverine Devi worship; boat and bank rituals mark festival peaks.", lat=21.980, lng=82.760, mapQuery="Chandrahasini Temple Chandrapur", nearestRail="Champa / Janjgir", nearestAirport="Raipur"),
    T(slug="bhoramdeo-temple", name="Bhoramdeo Temple", deity="Lord Shiva", location="Kawardha, Chhattisgarh", state="Chhattisgarh", glyph="भो", famousFor="‘Khajuraho of Chhattisgarh’ · heritage + pilgrim search", summary="Bhoramdeo — ornate Shiva temple complex in Kabirdham, tourism and darshan combined.", mythology="Nagara temples with rich sculpture; still an active Shiva seat for local devotees.", lat=22.100, lng=81.150, mapQuery="Bhoramdeo Temple", nearestRail="Raipur / Rajnandgaon", nearestAirport="Raipur"),
    # —— Delhi ——
    T(slug="kalkaji-mandir-delhi", name="Kalkaji Mandir, Delhi", deity="Goddess Kali (Kalkaji)", location="Kalkaji, New Delhi", state="Delhi", glyph="का", famousFor="One of Delhi’s highest footfall Devi temples · metro-era search spike", summary="Kalkaji Mandir — ancient Kali shrine in South Delhi with dense daily queues.", mythology="Local tradition links the shrine to Kali’s victory lore; Navaratri transforms the neighbourhood into a pilgrim market.", lat=28.550, lng=77.260, mapQuery="Kalkaji Mandir Delhi", nearestRail="Okhla / Hazrat Nizamuddin", nearestAirport="Delhi"),
    T(slug="hanuman-mandir-cp", name="Hanuman Mandir, Connaught Place", deity="Lord Hanuman", location="Connaught Place, New Delhi", state="Delhi", glyph="ह", famousFor="Central Delhi Tuesday crowds · top capital Hanuman search", summary="Hanuman Mandir near CP — Mughal-era origins, modern office-crowd devotion.", mythology="Tuesdays see extraordinary queues; the temple is woven into New Delhi’s daily urban bhakti.", lat=28.632, lng=77.220, mapQuery="Hanuman Mandir Connaught Place", nearestRail="New Delhi", nearestAirport="Delhi"),
    T(slug="jhandewalan-devi", name="Jhandewalan Devi Mandir", deity="Goddess Jhandewali Mata", location="Jhandewalan, New Delhi", state="Delhi", glyph="झ", famousFor="Navaratri jhanda culture · West Delhi Devi search", summary="Jhandewalan Mata — flag-votive Devi temple famous across Delhi NCR.", mythology="Devotees offer jhandas (flags) after wishes; Chaitra and Sharad Navaratri peak.", lat=28.648, lng=77.200, mapQuery="Jhandewalan Mandir Delhi", nearestRail="New Delhi", nearestAirport="Delhi"),
    T(slug="yogmaya-mehrauli", name="Yogmaya Temple, Mehrauli", deity="Goddess Yogmaya", location="Mehrauli, New Delhi", state="Delhi", glyph="यो", famousFor="Phool Walon Ki Sair · historic Delhi Devi search", summary="Yogmaya of Mehrauli — among Delhi’s oldest Devi temples, near Qutub complex.", mythology="Linked to Krishna’s sister Yogmaya; the shared Hindu–Muslim flower festival Phool Walon Ki Sair is culturally famous.", lat=28.525, lng=77.185, mapQuery="Yogmaya Temple Mehrauli", nearestRail="Delhi Cantt / New Delhi", nearestAirport="Delhi"),
    T(slug="gauri-shankar-chandni-chowk", name="Gauri Shankar Temple, Chandni Chowk", deity="Lord Shiva & Goddess Gauri", location="Chandni Chowk, Old Delhi", state="Delhi", glyph="गौ", famousFor="Old Delhi Shiva · heritage pilgrim walk search", summary="Gauri Shankar Mandir — active Shiva temple on Chandni Chowk’s sacred streetscape.", mythology="A marble Shiva–Parvati shrine amid Mughal-era bazaars; Monday worship remains intense.", lat=28.656, lng=77.230, mapQuery="Gauri Shankar Mandir Chandni Chowk", nearestRail="Delhi Junction", nearestAirport="Delhi"),
    T(slug="iskcon-east-of-kailash", name="ISKCON Temple, East of Kailash", deity="Krishna–Balaram (ISKCON)", location="East of Kailash, New Delhi", state="Delhi", glyph="इ", famousFor="Second major Delhi ISKCON · diaspora Sunday search", summary="ISKCON East of Kailash — large modern Krishna temple serving South Delhi and NCR.", mythology="Global Gaudiya bhakti campus with kirtan, prasadam, and Janmashtami spectacles popular with diaspora returnees.", lat=28.556, lng=77.250, mapQuery="ISKCON East of Kailash", nearestRail="Hazrat Nizamuddin", nearestAirport="Delhi", tags_extra=["modern-temples"]),

    # —— Goa ——
    T(slug="mhalasa-mardol", name="Mhalasa Narayani Temple, Mardol", deity="Goddess Mhalasa Narayani", location="Mardol, Goa", state="Goa", glyph="म्हा", famousFor="Top Goan Devi search after Shantadurga", summary="Mhalasa of Mardol — principal Goan goddess temple of the Ponda belt.", mythology="Mhalasa is worshipped as a fierce–benevolent form of the Goddess; festivals draw Goan Hindu diaspora home.", lat=15.442, lng=74.000, mapQuery="Mhalasa Temple Mardol", nearestRail="Madgaon / Karmali", nearestAirport="Goa"),
    T(slug="nagueshi-temple", name="Nagueshi Temple, Goa", deity="Lord Shiva (Naguesh)", location="Nagueshi, Ponda, Goa", state="Goa", glyph="ना", famousFor="Ponda Shiva circuit · Goa temple-trail search", summary="Nagueshi — ancient Shiva temple in the Ponda temple cluster.", mythology="Part of Goa’s relocated-deity history after Portuguese-era pressures; living Shaiva worship continues.", lat=15.425, lng=74.015, mapQuery="Nagueshi Temple Goa", nearestRail="Madgaon", nearestAirport="Goa"),
    T(slug="ramnathi-temple", name="Ramnathi Temple, Goa", deity="Goddess Ramnathi / Ramnath", location="Ramnathi, Ponda, Goa", state="Goa", glyph="रा", famousFor="Ponda temple belt · diaspora Goan family-deity search", summary="Ramnathi — important family-deity temple in Goa’s sacred Ponda taluka.", mythology="Kuladevata traditions of Goan Saraswat communities centre many vows here.", lat=15.430, lng=74.005, mapQuery="Ramnathi Temple Goa", nearestRail="Madgaon", nearestAirport="Goa"),
    T(slug="saptakoteshwar-narve", name="Saptakoteshwar Temple, Narve", deity="Lord Shiva (Saptakoteshwar)", location="Narve, Bicholim, Goa", state="Goa", glyph="स", famousFor="Kadamba royal Shiva · heritage + pilgrim search", summary="Saptakoteshwar — historic Shiva temple rebuilt after Portuguese demolition cycles.", mythology="Once a Kadamba royal deity; the rebuilt shrine remains a northern Goa Shaiva landmark.", lat=15.530, lng=73.950, mapQuery="Saptakoteshwar Temple Narve", nearestRail="Thivim", nearestAirport="Goa"),
    T(slug="tambdi-surla-mahadev", name="Mahadev Temple, Tambdi Surla", deity="Lord Shiva", location="Tambdi Surla, Goa", state="Goa", glyph="त", famousFor="Goa’s oldest surviving temple · tourism+darshan search", summary="Tambdi Surla Mahadev — Kadamba-era stone temple in forested Sanguem.", mythology="Finest early Goan temple architecture still used for Shiva worship; monsoon forest setting is iconic on YouTube travel reels.", lat=15.440, lng=74.250, mapQuery="Tambdi Surla Temple", nearestRail="Madgaon", nearestAirport="Goa"),
    T(slug="damodar-zambaulim", name="Damodar Temple, Zambaulim", deity="Lord Damodar (Krishna/Shiva traditions)", location="Zambaulim, Goa", state="Goa", glyph="द", famousFor="Sancti-spirit cultural festival · South Goa search", summary="Damodar of Zambaulim — shared sacred culture famous beyond Hindu-only audiences.", mythology="The deity’s festival history includes unique local inter-community customs; still a living South Goa tirtha.", lat=15.170, lng=74.050, mapQuery="Damodar Temple Zambaulim", nearestRail="Madgaon", nearestAirport="Goa"),

    # —— Gujarat (8→10+) ——
    T(slug="pavagadh-kalika", name="Kalika Mata Temple, Pavagadh", deity="Goddess Kalika", location="Pavagadh, Panchmahal, Gujarat", state="Gujarat", glyph="पा", famousFor="Ropeway Devi · Champaner UNESCO + high pilgrim search", summary="Kalika Mata atop Pavagadh — major Gujarat Devi pilgrimage with ropeway access.", mythology="Hill Shakti seat above Champaner–Pavagadh archaeological park; Navaratri and winter weekends pack the summit.", lat=22.484, lng=73.532, mapQuery="Kalika Mata Temple Pavagadh", nearestRail="Vadodara / Godhra", nearestAirport="Vadodara"),
    T(slug="bahucharaji-temple", name="Bahucharaji Temple", deity="Goddess Bahuchara Mata", location="Bahucharaji, Mehsana, Gujarat", state="Gujarat", glyph="ब", famousFor="North Gujarat Devi · very high state search volume", summary="Bahucharaji — one of Gujarat’s most visited Devi temples outside Ambaji–Pavagadh.", mythology="Bahuchara Mata is a kuldevi for many Gujarati communities; the town lives on pilgrim economy year-round.", lat=23.433, lng=72.150, mapQuery="Bahucharaji Temple", nearestRail="Bahucharaji / Mehsana", nearestAirport="Ahmedabad"),
    T(slug="shamlaji-temple", name="Shamlaji Temple", deity="Lord Vishnu (Shamlaji / Gadadhar)", location="Shamlaji, Aravalli, Gujarat", state="Gujarat", glyph="श", famousFor="Tribal–Vaishnava fair · North Gujarat pilgrimage search", summary="Shamlaji — ancient Vishnu temple on the Gujarat–Rajasthan pilgrimage corridor.", mythology="Also called Gadadhar; melas unite tribal and Brahminical devotees in distinctive North Gujarat bhakti.", lat=23.683, lng=73.383, mapQuery="Shamlaji Temple", nearestRail="Himmatnagar / Ahmedabad road", nearestAirport="Ahmedabad / Udaipur"),

    # —— Haryana ——
    T(slug="sheetla-mata-gurgaon", name="Sheetla Mata Mandir, Gurgaon", deity="Goddess Sheetla", location="Sector 6 / Sheetla Mata Road, Gurugram, Haryana", state="Haryana", glyph="शी", famousFor="NCR’s busiest Devi temple · huge Tuesday/Sunday search", summary="Sheetla Mata of Gurugram — among NCR’s highest daily footfall temples.", mythology="Sheetla is invoked for children’s health and protection; urban NCR queues define modern Haryana pilgrimage.", lat=28.470, lng=77.030, mapQuery="Sheetla Mata Mandir Gurgaon", nearestRail="Gurugram", nearestAirport="Delhi"),
    T(slug="agroha-dham", name="Agroha Dham", deity="Goddess Mahalakshmi & Maharaja Agrasen lore", location="Agroha, Hisar, Haryana", state="Haryana", glyph="अ", famousFor="Agrawal community mega-temple · national diaspora search", summary="Agroha Dham — modern pilgrimage complex tied to Agrasen and community identity.", mythology="Built as a cultural–religious centre for the Agrawal community with Devi and heritage museums; festivals draw pan-India visitors.", lat=29.330, lng=75.620, mapQuery="Agroha Dham", nearestRail="Hisar", nearestAirport="Delhi / Chandigarh", tags_extra=["modern-temples"]),
    T(slug="jyotisar-kurukshetra", name="Jyotisar, Kurukshetra", deity="Lord Krishna (Gita revelation site)", location="Jyotisar, Kurukshetra, Haryana", state="Haryana", glyph="ज्यो", famousFor="Gita upadesh site · global spiritual tourism search", summary="Jyotisar — traditionally marked as the place of the Bhagavad Gita’s discourse.", mythology="A banyan and modern Geeta memorial mark Krishna’s teaching to Arjuna; pairs with Brahma Sarovar on Kurukshetra yatra.", lat=29.961, lng=76.760, mapQuery="Jyotisar Kurukshetra", nearestRail="Kurukshetra Junction", nearestAirport="Chandigarh / Delhi"),
    T(slug="markandeshwar-shahabad", name="Markandeshwar Temple, Shahabad", deity="Lord Shiva (Markandeshwar)", location="Shahabad Markanda, Kurukshetra, Haryana", state="Haryana", glyph="मा", famousFor="Markandeya lore · Saraswati belt Shiva search", summary="Markandeshwar — ancient Shiva temple associated with sage Markandeya on the Saraswati ridge.", mythology="Linked to Markandeya’s victory over death; archaeological and living worship layers coexist.", lat=30.160, lng=76.870, mapQuery="Markandeshwar Temple Shahabad", nearestRail="Shahabad Markanda", nearestAirport="Chandigarh"),
    T(slug="banbhori-devi", name="Maa Banbhori Devi Temple", deity="Goddess Banbhori", location="Banbhori, Hisar, Haryana", state="Haryana", glyph="ब", famousFor="West Haryana Devi · regional mela search", summary="Banbhori Devi — popular rural–urban Devi shrine of Hisar belt.", mythology="Local Shakti devotion with fair-day peaks; increasingly visible in Haryana temple search trends.", lat=29.250, lng=75.900, mapQuery="Banbhori Devi Temple", nearestRail="Hisar", nearestAirport="Delhi"),

    # —— Himachal ——
    T(slug="chintpurni-temple", name="Chintpurni Temple", deity="Goddess Chintpurni (Chhinnamastika lore)", location="Chintpurni, Una, Himachal Pradesh", state="Himachal Pradesh", glyph="चि", famousFor="Shakti circuit with Jwala/Naina · massive North India search", summary="Chintpurni — major Himachal Devi peetha on the Jwala–Chintpurni–Naina circuit.", mythology="Popularly associated with Chhinnamastika Shakti lore; wish-fulfilling ‘chinta-purna’ devotion packs weekends.", lat=31.820, lng=76.130, mapQuery="Chintpurni Temple", nearestRail="Amb Andaura / Una", nearestAirport="Kangra / Chandigarh"),
    T(slug="chamunda-devi-kangra", name="Chamunda Devi Temple, Kangra", deity="Goddess Chamunda", location="Chamunda, Kangra, Himachal Pradesh", state="Himachal Pradesh", glyph="च", famousFor="Kangra valley Devi · high Himachal YouTube search", summary="Chamunda Nandikeshwar — riverside Devi temple near Dharamshala–Kangra.", mythology="Chamunda form of the Goddess guards the Baner river valley; pairs with Kangra fort and Brajeshwari yatra.", lat=32.140, lng=76.420, mapQuery="Chamunda Devi Temple Kangra", nearestRail="Kangra Mandir / Pathankot", nearestAirport="Kangra"),
    T(slug="bajreshwari-already", name="skip", deity="x", location="x", state="Himachal Pradesh", glyph="x", famousFor="x", summary="x", mythology="x", lat=0, lng=0),  # placeholder removed below
]

# Remove placeholder
NEW = [t for t in NEW if t.get("slug") != "bajreshwari-already"]

NEW += [
    T(slug="baijnath-temple-hp", name="Baijnath Temple, Himachal", deity="Lord Shiva (Vaidyanath)", location="Baijnath, Kangra, Himachal Pradesh", state="Himachal Pradesh", glyph="बै", famousFor="Nagara Shiva masterpiece · Kangra heritage search", summary="Baijnath — 13th-century Shiva temple, among Himachal’s finest stone shrines.", mythology="Vaidyanath form of Shiva; architecture draws heritage tourists who also take darshan.", lat=32.050, lng=76.650, mapQuery="Baijnath Temple Himachal", nearestRail="Kangra / Pathankot", nearestAirport="Kangra"),
    T(slug="bijli-mahadev", name="Bijli Mahadev Temple", deity="Lord Shiva (Bijli Mahadev)", location="Kullu, Himachal Pradesh", state="Himachal Pradesh", glyph="बि", famousFor="Lightning lingam trek · viral Himachal YouTube", summary="Bijli Mahadev — hilltop Shiva above Kullu, famous for the lightning-struck lingam lore.", mythology="Priests traditionally wrap the lingam after lightning strikes; the trek viewpoint is a social-media pilgrimage.", lat=31.930, lng=77.140, mapQuery="Bijli Mahadev Temple", nearestRail="Joginder Nagar / Chandigarh road", nearestAirport="Bhuntar"),
    T(slug="hatkoti-temple", name="Hatkoti Temple", deity="Goddess Durga (Mahishasuramardini)", location="Hatkoti, Shimla district, Himachal Pradesh", state="Himachal Pradesh", glyph="ह", famousFor="Pabbar valley Devi · Shimla rural circuit search", summary="Hatkoti — ancient Mahishasuramardini temple in the Pabbar valley.", mythology="Stone Devi image and wooden architecture mark a classic Cis-Himalayan Shakti seat.", lat=31.150, lng=77.740, mapQuery="Hatkoti Temple", nearestRail="Shimla", nearestAirport="Shimla / Chandigarh"),

    # —— J&K ——
    T(slug="raghunath-temple-jammu", name="Raghunath Temple, Jammu", deity="Lord Rama (Raghunath)", location="Jammu city, Jammu and Kashmir", state="Jammu and Kashmir", glyph="र", famousFor="Jammu’s largest temple complex · city pilgrim search", summary="Raghunath Mandir — sprawling Rama temple complex in Jammu city.", mythology="Dogras royal patronage built one of North India’s largest temple complexes dedicated to Rama’s lineage deities.", lat=32.730, lng=74.860, mapQuery="Raghunath Temple Jammu", nearestRail="Jammu Tawi", nearestAirport="Jammu"),
    T(slug="bawe-wali-mata", name="Bawe Wali Mata Temple, Jammu", deity="Goddess Mahakali (Bawe Wali Mata)", location="Bahu Fort, Jammu, Jammu and Kashmir", state="Jammu and Kashmir", glyph="ब", famousFor="Jammu’s guardian Devi · very high local search", summary="Bawe Wali Mata inside Bahu Fort — tutelary goddess of Jammu.", mythology="Mahakali as city protectress; Tuesdays and Navaratri see dense local footfall before Vaishno Devi onward yatra.", lat=32.730, lng=74.880, mapQuery="Bawe Wali Mata Jammu", nearestRail="Jammu Tawi", nearestAirport="Jammu"),
    T(slug="kheer-bhawani", name="Kheer Bhawani Temple", deity="Goddess Ragnya Devi (Kheer Bhawani)", location="Tulmulla, Ganderbal, Jammu and Kashmir", state="Jammu and Kashmir", glyph="खी", famousFor="Kashmiri Pandit heart-shrine · global diaspora Jyeshtha Ashtami search", summary="Kheer Bhawani — spring-temple of Ragnya Devi, central to Kashmiri Pandit devotion.", mythology="The sacred spring’s colour changes are read as omens; Jyeshtha Ashtami gathers Kashmiri Hindus from worldwide diaspora.", lat=34.220, lng=74.730, mapQuery="Kheer Bhawani Temple", nearestRail="Srinagar area", nearestAirport="Srinagar"),
    T(slug="shankaracharya-temple", name="Shankaracharya Temple, Srinagar", deity="Lord Shiva", location="Takht-e-Suleiman hill, Srinagar, Jammu and Kashmir", state="Jammu and Kashmir", glyph="शं", famousFor="Srinagar hill Shiva · heritage + pilgrim search", summary="Shankaracharya / Jyestheshwara temple overlooking Dal Lake.", mythology="Ancient Shiva seat associated in tradition with Adi Shankara’s visit; city viewpoint and living shrine.", lat=34.080, lng=74.840, mapQuery="Shankaracharya Temple Srinagar", nearestRail="Srinagar", nearestAirport="Srinagar"),
    T(slug="sharika-hari-parbat", name="Sharika Devi Temple, Hari Parbat", deity="Goddess Sharika (Tripura Sundari)", location="Hari Parbat, Srinagar, Jammu and Kashmir", state="Jammu and Kashmir", glyph="शा", famousFor="Srinagar’s guardian Devi · Kashmiri Hindu search", summary="Sharika on Hari Parbat — Srinagar’s kuladevi for many Kashmiri Hindus.", mythology="Tripura Sundari as Sharika protects the city; fortress hill remains a sensitive, sacred geography.", lat=34.110, lng=74.820, mapQuery="Sharika Devi Hari Parbat", nearestRail="Srinagar", nearestAirport="Srinagar"),
    T(slug="purmandal-temples", name="Purmandal Temple Town", deity="Lord Shiva (Chhota Kashi)", location="Purmandal, Samba, Jammu and Kashmir", state="Jammu and Kashmir", glyph="पु", famousFor="‘Chhota Kashi’ of Jammu · Shiva circuit search", summary="Purmandal — Devi/Shiva temple town called Chhota Kashi of Jammu region.", mythology="Cluster of riverside temples; Shivaratri and local melas sustain pilgrim traffic.", lat=32.700, lng=75.100, mapQuery="Purmandal Temple", nearestRail="Jammu Tawi / Samba", nearestAirport="Jammu"),

    # —— Jharkhand ——
    T(slug="jagannath-temple-ranchi", name="Jagannath Temple, Ranchi", deity="Lord Jagannath", location="Ranchi, Jharkhand", state="Jharkhand", glyph="ज", famousFor="Ranchi’s Rath Yatra · capital pilgrim search", summary="Ranchi Jagannath Mandir — hill temple with a popular Rath Yatra.", mythology="Odisha-style Jagannath worship transplanted to the Chotanagpur plateau; city identity shrine.", lat=23.370, lng=85.330, mapQuery="Jagannath Temple Ranchi", nearestRail="Ranchi", nearestAirport="Ranchi"),
    T(slug="pahari-mandir-ranchi", name="Pahari Mandir, Ranchi", deity="Lord Shiva", location="Ranchi Hill, Jharkhand", state="Jharkhand", glyph="प", famousFor="City viewpoint Shiva · Ranchi tourism+darshan search", summary="Pahari Mandir — Shiva temple atop Ranchi’s signature hill.", mythology="Monday throngs climb the steps; combines urban fitness culture with Shaiva devotion.", lat=23.370, lng=85.325, mapQuery="Pahari Mandir Ranchi", nearestRail="Ranchi", nearestAirport="Ranchi"),
    T(slug="basukinath-temple", name="Basukinath Temple", deity="Lord Shiva (Basukinath)", location="Basukinath, Dumka, Jharkhand", state="Jharkhand", glyph="ब", famousFor="Sawan Kawad twin with Deoghar · massive seasonal search", summary="Basukinath — major Shaiva tirtha of Santhal Pargana, paired with Baba Baidyanath.", mythology="Kawariyas often complete Deoghar–Basukinath together; Sawan is peak chaos and devotion.", lat=24.390, lng=87.080, mapQuery="Basukinath Temple", nearestRail="Basukinath / Jasidih", nearestAirport="Deoghar / Ranchi"),
    T(slug="dewri-mandir-tamar", name="Dewri Mandir, Tamar", deity="Goddess Dewri / Solha Bhuji Devi", location="Tamar, Ranchi district, Jharkhand", state="Jharkhand", glyph="दे", famousFor="16-armed Devi · Ranchi rural search spike", summary="Dewri Mandir — distinctive multi-armed Devi form near Ranchi.", mythology="Tribal–Hindu shared sacred space; unique iconography drives curiosity searches.", lat=23.050, lng=85.670, mapQuery="Dewri Mandir Tamar", nearestRail="Ranchi", nearestAirport="Ranchi"),
    T(slug="bhadrakali-itkhori", name="Bhadrakali Temple, Itkhori", deity="Goddess Bhadrakali", location="Itkhori, Chatra, Jharkhand", state="Jharkhand", glyph="भ", famousFor="Buddhist–Hindu heritage town · Chatra pilgrim search", summary="Itkhori Bhadrakali — Devi temple in a multi-layered sacred landscape.", mythology="Region also preserves Buddhist remains; Devi temple anchors living Hindu pilgrimage.", lat=24.300, lng=84.900, mapQuery="Bhadrakali Temple Itkhori", nearestRail="Gaya / Ranchi road", nearestAirport="Gaya / Ranchi"),

    # —— Karnataka ——
    T(slug="dharmasthala-manjunatha", name="Manjunatha Temple, Dharmasthala", deity="Lord Manjunatha (Shiva) · dharmadhikari tradition", location="Dharmasthala, Dakshina Kannada, Karnataka", state="Karnataka", glyph="ध", famousFor="~35 lakh+/year · free meals tens of thousands daily", summary="Dharmasthala Manjunatha — among Karnataka’s highest-footfall temples, famed for annadanam.", mythology="Shaiva worship administered with Jain dharmadhikari trusteeship — a unique harmony model. Hundi and charity scale are nationally reported.", lat=12.960, lng=75.380, mapQuery="Dharmasthala Temple", nearestRail="Mangaluru / Kankanadi", nearestAirport="Mangaluru"),
    T(slug="kukke-subramanya", name="Kukke Subramanya Temple", deity="Lord Subramanya (Kartikeya)", location="Subramanya, Dakshina Kannada, Karnataka", state="Karnataka", glyph="कु", famousFor="Sarpa dosha remedies · huge South India search", summary="Kukke Subramanya — rainforest temple of Kartikeya as serpent lord.", mythology="Famous for naga and sarpa-samskara rites; Western Ghats setting packs pilgrimage buses year-round.", lat=12.670, lng=75.620, mapQuery="Kukke Subramanya Temple", nearestRail="Subrahmanya Road", nearestAirport="Mangaluru"),
    T(slug="horanadu-annapoorneshwari", name="Annpoorneshwari Temple, Horanadu", deity="Goddess Annapoorneshwari", location="Horanadu, Chikmagalur, Karnataka", state="Karnataka", glyph="हो", famousFor="Malnad Devi · high Karnataka tourism+temple search", summary="Horanadu Annapoorneshwari — Goddess of food in the Western Ghats.", mythology="Annapurna devotion with hill-town prasadam culture; monsoon greenery fuels YouTube travel bhakti.", lat=13.270, lng=75.340, mapQuery="Horanadu Annapoorneshwari", nearestRail="Shimoga / Mangaluru", nearestAirport="Mangaluru"),
    T(slug="gokarna-mahabaleshwar", name="Mahabaleshwar Temple, Gokarna", deity="Lord Shiva (Mahabaleshwar)", location="Gokarna, Uttara Kannada, Karnataka", state="Karnataka", glyph="गो", famousFor="Atmalinga lore · beach-temple pilgrim/tourist search", summary="Gokarna Mahabaleshwar — coastal Jyotirlinga-adjacent fame with Atmalinga tradition.", mythology="Ravana and Atmalinga lore; beach town blends sadhu culture with domestic tourism.", lat=14.540, lng=74.320, mapQuery="Mahabaleshwar Temple Gokarna", nearestRail="Kumta / Ankola", nearestAirport="Goa / Hubballi"),
    T(slug="kateel-durga-parameshwari", name="Durga Parameshwari Temple, Kateel", deity="Goddess Durga Parameshwari", location="Kateel, Dakshina Kannada, Karnataka", state="Karnataka", glyph="क", famousFor="River-island Devi · coastal Karnataka search", summary="Kateel — Devi temple on an islet in the Nandini river.", mythology="Yakshagana offering culture and riverine Goddess lore define Kateel’s fame.", lat=13.040, lng=74.870, mapQuery="Kateel Temple", nearestRail="Mangaluru", nearestAirport="Mangaluru"),
    T(slug="sringeri-sharada", name="Sharadamba Temple, Sringeri", deity="Goddess Sharada & Shankara Peetham", location="Sringeri, Chikmagalur, Karnataka", state="Karnataka", glyph="शृ", famousFor="Adi Shankara peetham · pan-India Vedanta pilgrim search", summary="Sringeri Sharadamba — seat of the Sringeri Sharada Peetham founded in Shankara tradition.", mythology="Goddess of learning with matha lineage spanning centuries; scholars and householders share the tirtha.", lat=13.420, lng=75.250, mapQuery="Sringeri Temple", nearestRail="Shimoga", nearestAirport="Mangaluru"),

    # —— Kerala ——
    T(slug="chottanikkara-temple", name="Chottanikkara Temple", deity="Goddess Bhagavathy (Chottanikkara Amma)", location="Chottanikkara, Ernakulam, Kerala", state="Kerala", glyph="चो", famousFor="Healing Devi · among Kerala’s top non-Sabarimala searches", summary="Chottanikkara Bhagavathy — famous for vows related to mental affliction and protection.", mythology="Triple-aspect Goddess worship with evening ‘Guruthi’ rites widely discussed in Kerala devotion media.", lat=9.930, lng=76.390, mapQuery="Chottanikkara Temple", nearestRail="Ernakulam / Thrippunithura", nearestAirport="Kochi"),
    T(slug="ambalapuzha-krishna", name="Ambalappuzha Sri Krishna Temple", deity="Lord Krishna", location="Ambalappuzha, Alappuzha, Kerala", state="Kerala", glyph="अं", famousFor="Palpayasam 400-year tradition · ~high coastal footfall / viral food-bhakti search", summary="Ambalappuzha — Krishna temple world-famous for daily palpayasam prasadam.", mythology="Temple lore of a divine debt paid forever in sweet payasam; culinary bhakti drives national curiosity.", lat=9.380, lng=76.370, mapQuery="Ambalapuzha Temple", nearestRail="Ambalappuzha / Alappuzha", nearestAirport="Kochi"),
    T(slug="ettumanoor-mahadeva", name="Ettumanoor Mahadeva Temple", deity="Lord Shiva", location="Ettumanoor, Kottayam, Kerala", state="Kerala", glyph="ए", famousFor="Ezharaponnana festival · Central Kerala Shiva search", summary="Ettumanoor Mahadeva — one of Kerala’s great Shiva temples with famous mural and festival gold elephants.", mythology="Ezharaponnana (seven-and-a-half elephants) procession is a visual pilgrimage magnet.", lat=9.670, lng=76.560, mapQuery="Ettumanoor Temple", nearestRail="Ettumanoor / Kottayam", nearestAirport="Kochi"),
    T(slug="vaikom-mahadeva", name="Vaikom Mahadeva Temple", deity="Lord Shiva", location="Vaikom, Kottayam, Kerala", state="Kerala", glyph="वै", famousFor="Vaikom Satyagraha history + living Shiva tirtha", summary="Vaikom Mahadeva — ancient Shiva temple also remembered for the temple-entry satyagraha.", mythology="Shaiva liturgy meets modern social history; still a core Central Travancore pilgrimage.", lat=9.750, lng=76.390, mapQuery="Vaikom Temple", nearestRail="Vaikom Road / Ernakulam", nearestAirport="Kochi"),
    T(slug="kodungallur-bhagavathy", name="Kodungallur Bhagavathy Temple", deity="Goddess Kodungallur Bhagavathy (Kurumba)", location="Kodungallur, Thrissur, Kerala", state="Kerala", glyph="को", famousFor="Bharani festival · intense Kerala Devi search", summary="Kodungallur Amma — fierce Goddess temple with the renowned Bharani festival.", mythology="Ancient Chera-port sacred geography; Bharani’s intensity is widely covered in culture documentaries.", lat=10.220, lng=76.220, mapQuery="Kodungallur Temple", nearestRail="Irinjalakuda / Thrissur", nearestAirport="Kochi"),
    T(slug="chengannur-mahadeva", name="Chengannur Mahadeva Temple", deity="Lord Shiva & Goddess Parvati", location="Chengannur, Alappuzha, Kerala", state="Kerala", glyph="चे", famousFor="Unique Devi–Shiva festival cycle · Central Travancore search", summary="Chengannur — rare temple where Goddess’s menstrual purity cycle is ritually marked.", mythology="Shaiva–Shakta theology of divine femininity embodied in festival custom; sensitive, living tradition.", lat=9.320, lng=76.610, mapQuery="Chengannur Temple", nearestRail="Chengannur", nearestAirport="Kochi"),

    # —— Madhya Pradesh ——
    T(slug="orchha-ram-raja", name="Ram Raja Temple, Orchha", deity="Lord Rama (Ram Raja)", location="Orchha, Niwari, Madhya Pradesh", state="Madhya Pradesh", glyph="ओ", famousFor="Rama as king with gun salute · unique MP search", summary="Ram Raja Mandir — where Rama is worshipped as a reigning king with state honours.", mythology="Palace became temple when the idol could not be moved; daily gun salute custom is nationally famous.", lat=25.350, lng=78.640, mapQuery="Ram Raja Temple Orchha", nearestRail="Jhansi", nearestAirport="Khajuraho / Gwalior"),
    T(slug="salkanpur-devi", name="Salkanpur Devi Temple", deity="Goddess Durga (Siddhidatri)", location="Salkanpur, Sehore, Madhya Pradesh", state="Madhya Pradesh", glyph="स", famousFor="Stairway Devi near Bhopal · huge weekend NCR-MP search", summary="Salkanpur — hill Devi temple with long stair climb, popular from Bhopal.", mythology="Siddhidatri form; Navaratri turns the hill into a river of pilgrims.", lat=22.930, lng=77.220, mapQuery="Salkanpur Temple", nearestRail="Sehore / Bhopal", nearestAirport="Bhopal"),
    T(slug="harsiddhi-ujjain", name="Harsiddhi Temple, Ujjain", deity="Goddess Harsiddhi", location="Ujjain, Madhya Pradesh", state="Madhya Pradesh", glyph="ह", famousFor="Shakti Peetha with Mahakal · Simhastha circuit search", summary="Harsiddhi — principal Devi temple of Ujjain beside the Mahakaleshwar yatra.", mythology="Counted among Shakti Peethas; lamp pillars and Navaratri are iconic.", lat=23.176, lng=75.768, mapQuery="Harsiddhi Temple Ujjain", nearestRail="Ujjain Junction", nearestAirport="Indore"),
    T(slug="matangeshwar-khajuraho", name="Matangeshwar Temple, Khajuraho", deity="Lord Shiva", location="Khajuraho, Madhya Pradesh", state="Madhya Pradesh", glyph="म", famousFor="Living worship in UNESCO park · tourist+pilgrim search", summary="Matangeshwar — still-active Shiva temple among Khajuraho’s western group.", mythology="While many Khajuraho shrines are museum-like, Matangeshwar remains in daily worship.", lat=24.853, lng=79.920, mapQuery="Matangeshwar Temple Khajuraho", nearestRail="Khajuraho", nearestAirport="Khajuraho"),

    # —— Odisha ——
    T(slug="konark-sun-temple", name="Konark Sun Temple", deity="Surya (Sun God)", location="Konark, Puri district, Odisha", state="Odisha", glyph="को", famousFor="UNESCO chariot temple · global search; living Magha Saptami rites nearby", summary="Konark — 13th-century Sun Temple, Odisha’s world-famous architectural tirtha.", mythology="Built as Surya’s stone chariot; though the sanctum tradition shifted historically, Chandrabhaga beach rituals and heritage darshan keep pilgrim-tourism fused.", lat=19.887, lng=86.094, mapQuery="Konark Sun Temple", nearestRail="Puri / Bhubaneswar", nearestAirport="Bhubaneswar"),
    T(slug="cuttack-chandi", name="Cuttack Chandi Temple", deity="Goddess Chandi", location="Cuttack, Odisha", state="Odisha", glyph="क", famousFor="Millennium City Devi · Durga Puja / Odda search", summary="Cuttack Chandi — tutelary goddess of Cuttack with intense festival footfall.", mythology="Chandi as city protectress; Durga Puja of Cuttack is a major Odisha cultural-pilgrim event.", lat=20.480, lng=85.870, mapQuery="Cuttack Chandi Temple", nearestRail="Cuttack", nearestAirport="Bhubaneswar"),
    T(slug="maa-sarala-temple", name="Maa Sarala Temple, Jhankad", deity="Goddess Sarala", location="Jhankad, Jagatsinghpur, Odisha", state="Odisha", glyph="सा", famousFor="Odisha Shakti peetha lore · coastal Devi search", summary="Maa Sarala — important Shakta shrine of coastal Odisha.", mythology="Sarala Mahabharata literary culture and Devi worship intertwine at Jhankad.", lat=20.270, lng=86.300, mapQuery="Maa Sarala Temple", nearestRail="Cuttack / Paradip road", nearestAirport="Bhubaneswar"),
    T(slug="sakshi-gopal", name="Sakshi Gopal Temple", deity="Lord Krishna (Sakshi Gopal)", location="Sakshigopal, Puri district, Odisha", state="Odisha", glyph="सा", famousFor="Witness-Gopal lore on Puri road · yatra stop search", summary="Sakshi Gopal — Krishna as divine witness, classic stop on the Puri highway.", mythology="Famous story of Gopal walking to bear witness for a devotee; buses still pause for darshan en route to Jagannath.", lat=19.940, lng=85.820, mapQuery="Sakshi Gopal Temple", nearestRail="Sakshigopal / Puri", nearestAirport="Bhubaneswar"),
    T(slug="ananta-vasudeva-bhubaneswar", name="Ananta Vasudeva Temple, Bhubaneswar", deity="Lord Vishnu (Ananta Vasudeva)", location="Bhubaneswar, Odisha", state="Odisha", glyph="अन", famousFor="Old town Vishnu · Lingaraj circuit Vaishnava search", summary="Ananta Vasudeva — rare major Vishnu temple in Shaiva Bhubaneswar.", mythology="Twin deities and kitchen traditions complement Lingaraj yatra for complete Ekamra visit.", lat=20.240, lng=85.840, mapQuery="Ananta Vasudeva Temple", nearestRail="Bhubaneswar", nearestAirport="Bhubaneswar"),
    T(slug="gupteswar-odisha", name="Gupteswar Cave Temple", deity="Lord Shiva (Gupteswar)", location="Gupteswar, Koraput, Odisha", state="Odisha", glyph="गु", famousFor="Cave lingam · tribal Odisha tourism+pilgrim search", summary="Gupteswar — limestone cave Shiva temple in Koraput forests.", mythology="Self-manifest lingam in a living cave; combines adventure geography with Shaiva devotion.", lat=18.820, lng=82.170, mapQuery="Gupteswar Temple Odisha", nearestRail="Jeypore / Koraput", nearestAirport="Jeypore / Visakhapatnam"),

    # —— Punjab ——
    T(slug="devi-talab-mandir", name="Devi Talab Mandir, Jalandhar", deity="Goddess Durga", location="Jalandhar, Punjab", state="Punjab", glyph="दे", famousFor="Punjab’s foremost Devi temple · very high state search", summary="Devi Talab — lake temple complex, among Punjab’s most visited Hindu shrines.", mythology="Old tank-temple revived as a major urban Devi centre; Navaratri is city-scale.", lat=31.330, lng=75.580, mapQuery="Devi Talab Mandir Jalandhar", nearestRail="Jalandhar City", nearestAirport="Amritsar / Chandigarh"),
    T(slug="ram-tirath-amritsar", name="Ram Tirath Temple, Amritsar", deity="Lord Rama / Valmiki ashram lore", location="Ram Tirath, Amritsar, Punjab", state="Punjab", glyph="रा", famousFor="Valmiki–Sita lore · Amritsar Hindu circuit search", summary="Ram Tirath — ashram-temple linked to Valmiki and Lava–Kusha birth tradition.", mythology="Epic geography for Ramayana devotees visiting Amritsar beyond Harmandir Sahib tourism.", lat=31.700, lng=74.780, mapQuery="Ram Tirath Amritsar", nearestRail="Amritsar", nearestAirport="Amritsar"),
    T(slug="mudwan-mandir-ludhiana", name="Shri Krishna Mandir / Mudwan traditions, Ludhiana", deity="Lord Krishna", location="Ludhiana region, Punjab", state="Punjab", glyph="कृ", famousFor="Industrial city’s Krishna devotion · regional search", summary="Ludhiana’s major Krishna temples serve Punjab’s urban Hindu population.", mythology="Modern seva campuses and classic idols share Tuesday–Sunday crowds in Punjab’s largest city.", lat=30.900, lng=75.850, mapQuery="Krishna Mandir Ludhiana", nearestRail="Ludhiana", nearestAirport="Chandigarh / Ludhiana"),
]

# Fix mudwan - use a clearer real temple
for i, t in enumerate(NEW):
    if t["slug"] == "mudwan-mandir-ludhiana":
        NEW[i] = T(
            slug="shri-krishna-mandir-ludhiana",
            name="Shri Krishna Mandir, Ludhiana",
            deity="Lord Krishna",
            location="Ludhiana, Punjab",
            state="Punjab",
            glyph="कृ",
            famousFor="Ludhiana’s major Krishna temple · urban Punjab pilgrim search",
            summary="Prominent Krishna temple serving Ludhiana’s large Hindu community.",
            mythology="Urban Vaishnava devotion with Janmashtami as the annual peak; represents Punjab’s living temple culture beyond historic peethas.",
            lat=30.901,
            lng=75.857,
            mapQuery="Shri Krishna Mandir Ludhiana",
            nearestRail="Ludhiana",
            nearestAirport="Chandigarh",
        )

NEW += [
    T(slug="kali-mata-patiala", name="Kali Mata Mandir, Patiala", deity="Goddess Kali", location="Patiala, Punjab", state="Punjab", glyph="का", famousFor="Patiala royal-city Devi · regional search", summary="Kali Mata temple — important Devi shrine of Patiala.", mythology="Royal-city Shakta worship continues in contemporary Patiala pilgrimage patterns.", lat=30.340, lng=76.380, mapQuery="Kali Mata Mandir Patiala", nearestRail="Patiala", nearestAirport="Chandigarh"),

    # —— Rajasthan ——
    T(slug="karni-mata-deshnok", name="Karni Mata Temple, Deshnok", deity="Goddess Karni Mata", location="Deshnok, Bikaner, Rajasthan", state="Rajasthan", glyph="क", famousFor="Temple of rats · global YouTube curiosity + pilgrim vows", summary="Karni Mata Deshnok — famous for sacred rats and living folk-deity worship.", mythology="Karni Mata is a charan sati-deity; kabbas (rats) are protected as reincarnated devotees in local belief.", lat=27.790, lng=73.340, mapQuery="Karni Mata Temple Deshnok", nearestRail="Deshnoke / Bikaner", nearestAirport="Bikaner / Jodhpur"),
    T(slug="brahma-temple-pushkar", name="Brahma Temple, Pushkar", deity="Lord Brahma", location="Pushkar, Ajmer, Rajasthan", state="Rajasthan", glyph="ब्र", famousFor="Rare Brahma shrine · Pushkar fair global search", summary="Jagatpita Brahma Mandir — among the world’s few major Brahma temples.", mythology="Pushkar lake and Brahma’s yajna lore; Kartik full-moon fair is internationally famous.", lat=26.487, lng=74.555, mapQuery="Brahma Temple Pushkar", nearestRail="Ajmer", nearestAirport="Jaipur / Kishangarh"),
    T(slug="eklingji-udaipur", name="Eklingji Temple", deity="Lord Shiva (Eklingji)", location="Kailashpuri, Udaipur, Rajasthan", state="Rajasthan", glyph="ए", famousFor="Mewar’s tutelary Shiva · Udaipur circuit search", summary="Eklingji — dynastic Shiva temple of Mewar rulers near Udaipur.", mythology="Maharanas ruled as diwans of Eklingji; complex architecture and Monday worship endure.", lat=24.750, lng=73.720, mapQuery="Eklingji Temple", nearestRail="Udaipur City", nearestAirport="Udaipur"),
    T(slug="moti-dungri-ganesh", name="Moti Dungri Ganesh Temple", deity="Lord Ganesha", location="Jaipur, Rajasthan", state="Rajasthan", glyph="मो", famousFor="Jaipur’s favourite Ganesh · city wish-vows search", summary="Moti Dungri — hill Ganesh temple beloved of Jaipur residents.", mythology="Orange Ganesh and continuous laddoo offerings; pairs with nearby Birla Mandir visits.", lat=26.890, lng=75.820, mapQuery="Moti Dungri Ganesh Temple", nearestRail="Jaipur", nearestAirport="Jaipur"),
    T(slug="tanot-mata", name="Tanot Mata Temple", deity="Goddess Tanot Mata", location="Tanot, Jaisalmer, Rajasthan", state="Rajasthan", glyph="त", famousFor="1965/71 war lore · Border Road viral search", summary="Tanot Mata — desert Devi temple maintained with BSF reverence near the Pakistan border.", mythology="Unexploded shells in the museum narrate 1965 war miracles in popular telling; patriotism and Shakti fuse.", lat=27.800, lng=70.350, mapQuery="Tanot Mata Temple", nearestRail="Jaisalmer", nearestAirport="Jaisalmer"),

    # —— Telangana ——
    T(slug="jogulamba-alampur", name="Jogulamba Temple, Alampur", deity="Goddess Jogulamba", location="Alampur, Jogulamba Gadwal, Telangana", state="Telangana", glyph="जो", famousFor="Shakti Peetha · Tungabhadra heritage search", summary="Jogulamba — Telangana’s Shakti Peetha at Alampur with Chalukya temple environs.", mythology="Counted among 18 Maha Shakti Peethas in many lists; Navabrahma temples nearby deepen the tirtha.", lat=15.880, lng=78.130, mapQuery="Jogulamba Temple Alampur", nearestRail="Alampur Road / Kurnool", nearestAirport="Hyderabad / Kurnool"),
    T(slug="chilkur-balaji", name="Chilkur Balaji Temple", deity="Lord Venkateswara (Chilkur Balaji)", location="Chilkur, Hyderabad, Telangana", state="Telangana", glyph="चि", famousFor="Visa Balaji · huge Hyderabad IT/diaspora search", summary="Chilkur Balaji — famous as ‘Visa God’ for students and professionals abroad.", mythology="No hundi; pradakshina vows for visas and careers made this a global Telugu diaspora meme and real tirtha.", lat=17.360, lng=78.300, mapQuery="Chilkur Balaji Temple", nearestRail="Hyderabad", nearestAirport="Hyderabad"),
    T(slug="basara-gnana-saraswati", name="Gnana Saraswati Temple, Basar", deity="Goddess Saraswati", location="Basar, Nirmal, Telangana", state="Telangana", glyph="बा", famousFor="Akshara abhyasam · top Telangana education-pilgrim search", summary="Basar Gnana Saraswati — among India’s few major Saraswati temples.", mythology="Children’s aksharabhyasam (first letters) packs the temple; Godavari-bank setting.", lat=18.880, lng=77.990, mapQuery="Basara Saraswati Temple", nearestRail="Basar", nearestAirport="Hyderabad / Nanded"),
    T(slug="keesaragutta-temple", name="Keesaragutta Temple", deity="Lord Shiva (Ramalingeshwara)", location="Keesara, Medchal, Telangana", state="Telangana", glyph="की", famousFor="Hyderabad weekend Shiva · high local search", summary="Keesaragutta — hill Shiva temple on Hyderabad’s outskirts.", mythology="Ramayana-linked linga lore; Monday and Shivaratri city spills.", lat=17.520, lng=78.700, mapQuery="Keesaragutta Temple", nearestRail="Secunderabad", nearestAirport="Hyderabad"),
    T(slug="dichpally-ramalayam", name="Dichpally Ramalayam", deity="Lord Rama", location="Dichpally, Nizamabad, Telangana", state="Telangana", glyph="दि", famousFor="Stone Rama temple · north Telangana search", summary="Dichpally Ramalayam — ornate Rama temple of Nizamabad region.", mythology="Kakatiya-influenced stone work with living Rama worship; regional yatra stop.", lat=18.600, lng=78.150, mapQuery="Dichpally Ramalayam", nearestRail="Nizamabad", nearestAirport="Hyderabad"),
    T(slug="surendrapuri-temple", name="Surendrapuri Mythological Theme Complex", deity="Multiple deities (Kunda Satyanarayana Kaladhamam)", location="Yadadri area, Telangana", state="Telangana", glyph="सु", famousFor="Mythology park + temples · family diaspora search", summary="Surendrapuri — large mythological sculpture park with shrine worship near Yadagirigutta.", mythology="Educational bhakti tourism: epics in stone plus functioning temples; popular with families.", lat=17.590, lng=78.940, mapQuery="Surendrapuri", nearestRail="Bhongir", nearestAirport="Hyderabad", tags_extra=["modern-temples"]),

    # —— Tripura ——
    T(slug="chaturdasha-devata", name="Chaturdasha Devata Temple", deity="Fourteen gods (tribal–Hindu pantheon)", location="Old Agartala, Tripura", state="Tripura", glyph="च", famousFor="Fourteen gods of Tripura · state identity search", summary="Chaturdasha Devata — royal-tribal temple of Tripura’s fourteen deities.", mythology="Kharchi festival brings the deities to public immersion rites — Tripura’s signature sacred calendar.", lat=23.840, lng=91.280, mapQuery="Chaturdasha Devata Temple", nearestRail="Agartala", nearestAirport="Agartala"),
    T(slug="bhuvaneswari-udaipur-tripura", name="Bhuvaneswari Temple, Udaipur", deity="Goddess Bhuvaneswari", location="Udaipur, Tripura", state="Tripura", glyph="भु", famousFor="Gomati riverside Devi near Tripura Sundari", summary="Bhuvaneswari temple on the Gomati — classic Udaipur (Tripura) Devi stop.", mythology="Paired with Tripura Sundari yatra; Tagore’s writings also popularised the riverside setting.", lat=23.520, lng=91.490, mapQuery="Bhuvaneswari Temple Udaipur Tripura", nearestRail="Udaipur Tripura / Agartala", nearestAirport="Agartala"),
    T(slug="jagannath-agartala", name="Jagannath Temple, Agartala", deity="Lord Jagannath", location="Agartala, Tripura", state="Tripura", glyph="ज", famousFor="Capital Jagannath · Tripura urban pilgrim search", summary="Agartala Jagannath Mandir — city temple with Rath Yatra celebrations.", mythology="Odisha-influenced Jagannath culture in the Northeast capital.", lat=23.840, lng=91.280, mapQuery="Jagannath Temple Agartala", nearestRail="Agartala", nearestAirport="Agartala"),

    # —— Meghalaya ——
    T(slug="shiv-mandir-shillong", name="Shiva Temple complexes, Shillong", deity="Lord Shiva", location="Shillong, Meghalaya", state="Meghalaya", glyph="शि", famousFor="Hill-station Hindu worship · Shillong city search", summary="Shillong’s active Shiva temples serve the city’s Hindu communities and visitors.", mythology="Colonial hill-station Hindu diaspora built enduring Shaiva worship spaces amid Khasi sacred geography.", lat=25.578, lng=91.893, mapQuery="Shiva Temple Shillong", nearestRail="Guwahati", nearestAirport="Shillong / Guwahati"),

    # —— New states ——
    T(slug="siddheshwar-dham-namchi", name="Siddheshwar Dham, Namchi", deity="Lord Shiva (char dham replicas) & Kirateshwar lore nearby", location="Solophok, Namchi, Sikkim", state="Sikkim", glyph="सि", famousFor="Giant Shiva statue · top Sikkim Hindu tourism search", summary="Siddheshwar Dham — monumental Shiva and Char Dham replica complex at Namchi.", mythology="Modern pilgrimage park presenting India’s Char Dham in the Himalaya; combines darshan with state tourism.", lat=27.170, lng=88.360, mapQuery="Siddheshwar Dham Namchi", nearestRail="New Jalpaiguri / Siliguri road", nearestAirport="Bagdogra / Pakyong", tags_extra=["modern-temples"]),
    T(slug="kirateshwar-legship", name="Kirateshwar Mahadev Temple", deity="Lord Shiva (Kirateshwar)", location="Legship, Sikkim", state="Sikkim", glyph="कि", famousFor="Sikkimese Shiva · Rangit river festival search", summary="Kirateshwar Mahadev — important living Shiva temple of West Sikkim.", mythology="Kirata form of Shiva in Himalayan lore; annual mela by the Rangit draws regional pilgrims.", lat=27.270, lng=88.270, mapQuery="Kirateshwar Temple Legship", nearestRail="New Jalpaiguri", nearestAirport="Bagdogra"),
    T(slug="govindajee-imphal", name="Shree Govindajee Temple, Imphal", deity="Lord Krishna (Govindajee)", location="Imphal, Manipur", state="Manipur", glyph="गो", famousFor="Royal Vaishnava temple · Manipur identity search", summary="Govindajee Temple — historic royal Krishna temple of Manipur.", mythology="Centre of Manipuri Vaishnava culture and classical ras tradition linked to royal patronage.", lat=24.808, lng=93.950, mapQuery="Govindajee Temple Imphal", nearestRail="Dimapur road / Jiribam", nearestAirport="Imphal"),
    T(slug="parshuram-kund", name="Parshuram Kund", deity="Lord Parshuram / sacred kund", location="Lohit district, Arunachal Pradesh", state="Arunachal Pradesh", glyph="प", famousFor="Makar Sankranti fair · Northeast Hindu pilgrimage search", summary="Parshuram Kund — sacred pool where tradition places Parshuram’s axe-washing lore.", mythology="Makar Sankranti mela draws pilgrims from Assam and beyond to the Lohit river tirtha.", lat=27.880, lng=96.370, mapQuery="Parshuram Kund Arunachal", nearestRail="Tinsukia / Tezu road", nearestAirport="Tezu / Dibrugarh"),
    T(slug="malinithan-arunachal", name="Malinithan Temple", deity="Devi / Shiva sculptural remains (active pilgrimage site)", location="Likabali, Arunachal Pradesh", state="Arunachal Pradesh", glyph="म", famousFor="Sati–Shiva lore ruins · Arunachal heritage search", summary="Malinithan — archaeological temple site tied to Shiva–Sati–Krishna floral lore of the Northeast.", mythology="Sculpture-rich ruins remain a tirtha-tourism hybrid on the Assam–Arunachal border.", lat=27.670, lng=94.700, mapQuery="Malinithan Temple", nearestRail="Silapathar / North Lakhimpur", nearestAirport="Dibrugarh"),
    T(slug="manakula-vinayagar", name="Manakula Vinayagar Temple", deity="Lord Ganesha (Manakula Vinayagar)", location="Puducherry", state="Puducherry", glyph="म", famousFor="Pondicherry’s favourite Ganesh · top UT temple search", summary="Manakula Vinayagar — the most famous temple in the Puducherry boulevard quarter.", mythology="Gold-covered Ganesha and continuous modak offerings; French-quarter location makes it a diaspora must-visit.", lat=11.936, lng=79.833, mapQuery="Manakula Vinayagar Temple", nearestRail="Puducherry", nearestAirport="Chennai / Puducherry"),
    T(slug="vedapureeswarar-pondy", name="Vedapureeswarar Temple, Puducherry", deity="Lord Shiva (Vedapureeswarar)", location="Puducherry", state="Puducherry", glyph="वे", famousFor="Historic Pondy Shiva · heritage street search", summary="Vedapureeswarar — ancient Shiva temple in central Puducherry.", mythology="Shaiva worship predating and surviving colonial centuries in the French Indian capital.", lat=11.933, lng=79.832, mapQuery="Vedapureeswarar Temple Pondicherry", nearestRail="Puducherry", nearestAirport="Chennai"),

    # —— Tamil Nadu extras if under-covered themes ——
    T(slug="ramanathaswamy-already-skip", name="skip", deity="x", location="x", state="Tamil Nadu", glyph="x", famousFor="x", summary="x", mythology="x", lat=0, lng=0),

    # —— UP high-search missing ——
    T(slug="banke-bihari-already", name="skip", deity="x", location="x", state="Uttar Pradesh", glyph="x", famousFor="x", summary="x", mythology="x", lat=0, lng=0),
    T(slug="prayagraj-hanuman", name="Lete Hanuman Mandir, Prayagraj", deity="Lord Hanuman", location="Prayagraj, Uttar Pradesh", state="Uttar Pradesh", glyph="ह", famousFor="Reclining Hanuman · Sangam yatra search", summary="Lete Hanuman Temple — famous reclining Hanuman near the Prayagraj Sangam.", mythology="Flood lore says the figure grows with the Ganga; Kawariyas and Kumbh crowds both visit.", lat=25.430, lng=81.880, mapQuery="Lete Hanuman Temple Prayagraj", nearestRail="Prayagraj Junction", nearestAirport="Prayagraj"),
    T(slug="sankat-mochan-already", name="skip", deity="x", location="x", state="Uttar Pradesh", glyph="x", famousFor="x", summary="x", mythology="x", lat=0, lng=0),
]

NEW = [t for t in NEW if t.get("slug") and not str(t["slug"]).endswith("skip") and t.get("name") != "skip"]


def infer_deity_families(seed: dict) -> list[str]:
    text = " ".join(
        [
            seed.get("deity", ""),
            seed.get("name", ""),
            seed.get("summary", ""),
            seed.get("mythology", ""),
        ]
    ).lower()
    fams = []
    rules = [
        ("ayyappa", ["ayyappa", "sabarimala"]),
        ("hanuman", ["hanuman"]),
        ("ganesha", ["ganesha", "ganesh", "vinayagar", "vinayaka"]),
        ("rama", ["rama", "raghunath", "ram raja", "sita", "janaki"]),
        ("krishna", ["krishna", "gopal", "govinda", "balaji" and "chilkur"]),
        ("devi", ["devi", "goddess", "mata", "kali", "durga", "ambaji", "bhagavathy", "saraswati", "annapoor", "chamunda", "chandi", "kalika", "bahuchara", "karni", "sharika", "sheetla", "jogulamba", "bambleshwari", "mahamaya", "chintpurni", "patan"]),
        ("shiva", ["shiva", "mahadev", "linga", "bhairav", "mrityunjay", "manjunatha", "ekling", "gupteswar", "naguesh", "saptakoteshwar", "mahabaleshwar", "markandeshwar"]),
        ("vishnu", ["vishnu", "venkateswara", "balaji", "narayana", "hayagriva", "jagannath", "rama", "krishna", "satyanarayan"]),
        ("sai", ["sai"]),
    ]
    # simpler keyword map
    checks = [
        ("ayyappa", ["ayyappa"]),
        ("hanuman", ["hanuman"]),
        ("ganesha", ["ganesha", "ganesh", "vinayagar", "vinayaka"]),
        ("rama", ["rama", "raghunath", "ram raja", "janaki", "sita"]),
        ("krishna", ["krishna", "gopal", "govinda", "govindajee", "sakshi gopal"]),
        ("devi", ["goddess", "devi", "mata", "kali", "durga", "bhagavathy", "saraswati", "annapoor", "chamunda", "chandi", "kalika", "bahuchara", "karni", "sharika", "sheetla", "jogulamba", "bambleshwari", "mahamaya", "chintpurni", "patan", "bhuvaneswari", "dirgheswari", "yogmaya", "jhandewalan", "kalkaji", "harsiddhi", "sarala", "mhalasa", "ramnathi", "bahuchar"]),
        ("shiva", ["shiva", "mahadev", "lingam", "bhairav", "mrityunjay", "manjunatha", "ekling", "gupteswar", "naguesh", "saptakoteshwar", "mahabaleshwar", "markandeshwar", "umananda", "sukreswar", "basistha", "bajinath", "baijnath", "bijli", "kirateshwar", "siddheshwar", "matangeshwar", "kuleshwar", "ajgaibinath", "basukinath", "vedapureeswarar"]),
        ("vishnu", ["vishnu", "venkateswara", "hayagriva", "jagannath", "narayana", "vasudeva", "shamlaji", "brahma"]),
    ]
    for fam, keys in checks:
        if any(k in text for k in keys):
            fams.append(fam)
    if "brahma" in text and "vishnu" not in fams:
        fams.append("vishnu")
    if "surya" in text or "sun god" in text or "sun temple" in text:
        if "vishnu" not in fams:
            fams.append("vishnu")
    if "parshuram" in text:
        fams.append("vishnu")
    if "guru ghasidas" in text or "satnam" in text:
        fams = []  # multi-tradition — no forced family
    # unique preserve order
    out = []
    for f in fams:
        if f not in out:
            out.append(f)
    return out[:3]


def attach_portal(detail: dict) -> dict:
    state = detail.get("state", "")
    portal = PORTALS.get(state)
    if not portal:
        return detail
    sources = list(detail.get("sources", []))
    line = f"{portal['portalName']}: {portal['portalUrl']}"
    if line not in sources:
        sources = [line] + sources
    detail["sources"] = sources
    detail["statePortal"] = {
        "name": portal["portalName"],
        "url": portal["portalUrl"],
        "slug": portal["slug"],
    }
    if detail.get("officialWebsite") in ("https://tourism.gov.in/", "", None):
        detail["officialWebsite"] = portal["portalUrl"]
    return detail


def enrich_myth_fields(detail: dict) -> dict:
    myth = detail.get("mythology", "")
    if not detail.get("mythologySignificance"):
        detail["mythologySignificance"] = (
            myth
            + "\n\nPilgrimage literature treats this shrine as a tirtha — verify living custom with temple priests. "
            "Accounts here are TirthaYatra summaries of widely cited traditions, not verbatim scripture."
        )
    if not detail.get("localBeliefs"):
        detail["localBeliefs"] = (
            "Queue discipline, prasadam sharing, and festival vows shape belief as practice. "
            "First-time visitors often hear several local tellings — living conversation, not a single fixed text.\n\n"
            "Footfall and search popularity noted on this page are approximate editorial signals from "
            "public pilgrimage reporting and common Google/YouTube interest — not a ranking paid by any trust."
        )
    if not detail.get("mythologyDisclaimer"):
        detail["mythologyDisclaimer"] = (
            "Mythological accounts and local beliefs are drawn from Puranic traditions, epics, and widely recorded "
            "sthala-purana / pilgrimage lore. Versions differ by scripture, region, and temple tradition. "
            "Visitor figures are approximate public estimates where cited. This section is for cultural understanding "
            "— not a claim of historical fact, nor a substitute for guidance from temple priests or official trusts."
        )
    detail["lastUpdated"] = "2026-08-09"
    detail["country"] = detail.get("country") or "India"
    detail["tier"] = "famous"
    return detail


def main() -> None:
    global PORTALS
    # merge new portals
    for state, portal in NEW_PORTALS.items():
        if state not in PORTALS:
            PORTALS[state] = portal
    dump_json(DATA / "state-portals.json", PORTALS)
    PORTALS = load_json(DATA / "state-portals.json")

    existing = {p.stem for p in TEMPLES.glob("*.json")}
    created = []
    skipped = []

    for seed in NEW:
        slug = seed["slug"]
        if slug in existing:
            skipped.append(slug)
            continue
        tags_extra = seed.pop("tags_extra", None) or []
        # copy seed for base_detail (don't mutate shared if re-run — already popped tags_extra)
        detail = base_detail(dict(seed))
        detail["deityFamilies"] = seed.get("deityFamilies") or infer_deity_families(seed)
        tags = list(detail.get("tags") or [])
        for t in tags_extra:
            if t not in tags:
                tags.append(t)
        detail["tags"] = tags
        detail = attach_portal(detail)
        detail = enrich_myth_fields(detail)
        # ensure lat/lng present
        if detail.get("lat") is None or detail.get("lng") is None:
            raise SystemExit(f"Missing coords for {slug}")
        dump_json(TEMPLES / f"{slug}.json", detail)
        created.append(slug)
        existing.add(slug)

    print(f"Created {len(created)} temples; skipped existing {len(skipped)}")
    for s in created:
        print(" +", s)

    # rebuild index + tags
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "sync_groups.py")])
    # assign deities heuristics for any empty families
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "assign_deities.py")])

    # coverage report
    index = load_json(DATA / "temples.json")
    from collections import Counter

    c = Counter(t["state"] for t in index if t.get("country") == "India")
    print("\nIndia temples by state (after):")
    for st, n in sorted(c.items(), key=lambda x: (-x[1], x[0])):
        mark = "✓" if n >= 10 else f"({10-n} to 10)"
        print(f"  {n:3} {st} {mark}")
    print("TOTAL India", sum(c.values()), "ALL", len(index))


if __name__ == "__main__":
    main()
