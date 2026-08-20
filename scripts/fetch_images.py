#!/usr/bin/env python3
"""
Download Wikimedia Commons images for temples missing local photos.

AdSense / commercial-safe licenses only:
  Public domain, CC0, CC BY, CC BY-SA (any version).
Skip NC, ND-only edge cases we can't use cleanly, GFDL-only, and unknown.

If no suitable file is found after search, leave the temple without a photo.
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
import ssl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA_PATH = ROOT / "data" / "media.json"
TEMPLES = ROOT / "data" / "temples"
OUT = ROOT / "assets" / "temples"
UA = {"User-Agent": "TirthaYatraBot/1.2 (educational pilgrimage guide; TirthaYatraOnline@gmail.com)"}
ctx = ssl.create_default_context()

# Prefer exact filenames first (more reliable than search)
PRIORITY = {
    "kanak-bhawan-ayodhya": ["Kanak_Bhawan_Ayodhya.jpg", "Kanak_Bhawan.jpg", "Ram_Janmabhoomi_Temple.jpg"],
    "shringverpur-prayagraj": ["Shringverpur.jpg", "Shringverpur_Ghat.jpg"],
    "chitrakoot-kamadgiri": ["Kamadgiri_Chitrakoot.jpg", "Chitrakoot_Kamadgiri.jpg", "Chitrakoot.jpg"],
    "gupta-godavari-chitrakoot": ["Gupta_Godavari_Chitrakoot.jpg", "Gupt_Godavari.jpg"],
    "sita-gufa-nashik": ["Sita_Gufa_Nashik.jpg", "Panchavati_Nashik.jpg"],
    "anjanadri-hampi": ["Anjaneya_Temple_Anjanadri.jpg", "Anjanadri_Hill.jpg", "Anjaneyadri.jpg"],
    "kodandarama-hampi": ["Kodanda_Rama_Temple_Hampi.jpg", "Kodandarama_Temple_Hampi.jpg"],
    "dhanushkodi-rama-setu": ["Dhanushkodi.jpg", "Dhanushkodi_Beach.jpg", "Adams_Bridge.jpg"],
    "bhishma-kund-kurukshetra": ["Bhishma_Kund_Kurukshetra.jpg", "Bhishma_Kund.jpg"],
    "pandaveshwar-hastinapur": ["Hastinapur.jpg", "Pandaveshwar_Temple.jpg"],
    "karna-temple-hastinapur": ["Karna_Temple_Hastinapur.jpg", "Hastinapur_Temple.jpg"],
    "barnawa-lakshagriha": ["Barnawa.jpg", "Lakshagriha.jpg"],
    "govardhan-giriraj": ["Govardhan_Hill.jpg", "Giriraj_Govardhan.jpg", "Govardhana_Hill.jpg"],
    "ayodhya-ram-mandir": ["Ram_Mandir_Ayodhya.jpg", "Ayodhya_Ram_Mandir.jpg", "Ram_Janmabhoomi_Temple_Ayodhya.jpg"],
    "bhimashankar": ["Bhimashankar_temple,_Maharashtra.JPG", "Bhimashankar_Temple.jpg", "Bhimashankar_Jyotirlinga.jpg"],
    "ahobilam-narasimha": ["Ahobilam_Temple.jpg", "Lower_Ahobilam.jpg"],
    "moreshwar-morgaon": ["Morgaon_Ganpati.jpg", "Mayureshwar_Temple.jpg"],
    "kalaram-temple-nashik": ["Kalaram_Temple.jpg", "Kalaram_Mandir_Nashik.jpg"],
    "mallikarjuna-srisailam": ["Srisailam_ghat_road.jpg", "Srisailam.jpg", "Mallikarjuna_temple_Srisailam.jpg"],
    "mahakaleshwar-ujjain": ["Mahakaleshwar_Jyotirlinga_Ujjain.jpg", "Mahakaleshwar_temple_Ujjain.jpg", "Ujjain_Mahakal.jpg"],
    "omkareshwar": ["Omkareshwar_Temple_Madhya_Pradesh.jpg", "Omkareshwar.jpg", "Omkareshwar_Mandhata.jpg"],
    "bhimashankar": ["Bhimashankar_Wildlife_Sanctuary_05.jpg", "Bhimashankar_temple.jpg"],
    "kashi-vishwanath": ["Kashi_Vishwanath_Temple_Varanasi.jpg", "Kashi_Vishwanath_corridor_2022.jpg", "New_Vishwanath_Temple.jpg"],
    "trimbakeshwar": ["Trimbakeshwar_Temple.jpg", "Tryambakeshwar_Temple.jpg"],
    "vaidyanath-deoghar": ["Baba_Baidyanath_Temple_Deoghar.jpg", "Baidyanath_Temple.jpg"],
    "nageshwar": ["Nageshvara_Jyotirlinga.jpg", "Nageshwar_temple_Dwarka.jpg"],
    "grishneshwar": ["Grishneshwar_Jyotirlinga_Temple.jpg", "Ghrishneshwar_Temple.jpg"],
    "jagannath-puri": ["Jagannath_Temple_Puri.jpg", "Puri_Jagannath_Temple_Front.jpg"],
    "yamunotri": ["Yamunotri_Temple_Uttarakhand.jpg", "Yamunotri.jpg"],
    "gangotri": ["Gangotri_Temple.jpg", "Gangotri_temple_uttarakhand.jpg"],
    "tungnath": ["Tungnath_Temple.jpg", "Tungnath_temple_chopta.jpg"],
    "tirumala-venkateswara": ["Tirumala_Venkateswara_Temple.jpg", "Tirumala_temple.jpg", "Venkateswara_Temple_Tirumala.jpg"],
    "simhachalam": ["Simhachalam_Temple.jpg", "Simhachalam.jpg"],
    "kanaka-durga-vijayawada": ["Kanaka_Durga_Temple.jpg", "Kanaka_Durga_Temple_Vijayawada.jpg"],
    "guruvayur": ["Guruvayur_Temple.jpg", "Guruvayoor_temple.jpg"],
    "chamundeshwari-mysuru": ["Chamundi_Hills_Temple.jpg", "Chamundeshwari_Temple.jpg"],
    "murudeshwar": ["Murdeshwar_Temple.jpg", "Murudeshwar_Shiva_statue.jpg"],
    "vaishno-devi": ["Vaishno_Devi_Bhawan.jpg", "Mata_Vaishno_Devi.jpg"],
    "pandharpur-vitthal": ["Vithoba_Temple_Pandharpur.jpg", "Pandharpur_Vitthal.jpg"],
    "kalighat": ["Kalighat_Kali_Temple.jpg", "Kalighat_Temple_Kolkata.jpg"],
    "jwalamukhi": ["Jwalamukhi_Temple_Himachal.jpg", "Jwala_Ji_Temple.jpg"],
    "ekambareswarar-kanchipuram": ["Ekambareswarar_Temple_Kanchipuram.jpg", "Ekambaranathar_Temple.jpg"],
    "arunachaleswarar-tiruvannamalai": ["Arunachalesvara_Temple.jpg", "Tiruvannamalai_Temple.jpg"],
    "nataraja-chidambaram": ["Chidambaram_Nataraja_Temple.jpg", "Nataraja_Temple_Chidambaram.jpg"],
    "srikalahasti": ["Srikalahasteeswara_temple.jpg", "Srikalahasti.jpg"],
    "konark-sun-temple": ["Konark_Sun_Temple.jpg", "Konarka_Temple.jpg", "Sun_Temple_Konark.jpg"],
    "lingaraj-bhubaneswar": ["Lingaraj_Temple.jpg", "Lingaraja_Temple_Bhubaneswar.jpg"],
    "kukke-subramanya": ["Kukke_Subramanya_Temple.jpg", "Kukke_Subramanya.jpg"],
    "dharmasthala-manjunatha": ["Dharmasthala_Temple.jpg", "Manjunatha_Temple_Dharmasthala.jpg"],
    "chilkur-balaji": ["Chilkur_Balaji_Temple.jpg", "Chilkur_Balaji.jpg"],
    "karni-mata-deshnok": ["Karni_Mata_Temple.jpg", "Karni_Mata_Deshnoke.jpg"],
    "kalkaji-mandir-delhi": ["Kalkaji_Mandir.jpg", "Kalka_Mandir_Delhi.jpg"],
    "eklingji-udaipur": ["Eklingji_Temple.jpg", "Eklingji.jpg"],
    "raghunath-temple-jammu": ["Raghunath_Temple_Jammu.jpg", "Raghunath_temple.jpg"],
    "shankaracharya-temple": ["Shankaracharya_Temple.jpg", "Shankaracharya_Temple_Srinagar.jpg"],
    "kheer-bhawani": ["Kheer_Bhawani_Temple.jpg", "Kheer_Bhawani.jpg"],
    "saptashrungi": ["Saptashrungi.jpg", "Saptashrungi_Temple.jpg"],
    "mundeshwari-devi": ["Mundeshwari_Temple.jpg", "Mundeshwari_Devi_Temple.jpg"],
    "manakula-vinayagar": ["Manakula_Vinayagar_Temple.jpg", "Manakula_Vinayagar.jpg"],
    "chottanikkara-temple": ["Chottanikkara_Temple.jpg", "Chottanikkara_Bhagavathy_Temple.jpg"],
    "ambalapuzha-krishna": ["Ambalapuzha_Temple.jpg", "Ambalappuzha_Sri_Krishna_Temple.jpg"],
}

SAFE_LICENSE_RE = re.compile(
    r"^(public domain|pd|cc0(\s*1\.0)?|cc[\s-]?by(\s|-sa)?(\s+\d+(\.\d+)?)?)$",
    re.I,
)


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=45) as r:
        return r.read()


def license_ok(short: str) -> bool:
    if not short:
        return False
    s = short.strip().lower().replace("_", " ")
    s = re.sub(r"\s+", " ", s)
    if "nc" in s or "noncommercial" in s or "non-commercial" in s:
        return False
    if "gfdl" in s and "cc" not in s:
        return False
    if "all rights reserved" in s:
        return False
    # ND alone is awkward for reuse; allow BY-ND? Safer skip ND.
    if re.search(r"\bnd\b|no derivatives", s) and "sa" not in s:
        return False
    if s in {"public domain", "pd", "cc0", "cc0 1.0"}:
        return True
    if s.startswith("cc0"):
        return True
    if s.startswith("cc by"):
        return True
    if SAFE_LICENSE_RE.match(s):
        return True
    # Common Commons forms: "CC BY-SA 4.0", "CC BY 3.0"
    if re.match(r"^cc by(-sa)? \d+(\.\d+)?$", s):
        return True
    return False


def api_file_info(filename: str):
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": f"File:{filename}",
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size",
            "iiurlwidth": 1280,
            "format": "json",
        }
    )
    data = json.loads(get(f"https://commons.wikimedia.org/w/api.php?{q}").decode())
    for page in data.get("query", {}).get("pages", {}).values():
        if "imageinfo" not in page:
            return None
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        license_short = meta.get("LicenseShortName", {}).get("value", "") or ""
        if not license_ok(license_short):
            return {"_rejected": True, "filename": filename, "license": license_short}
        artist = re.sub("<[^<]+?>", "", meta.get("Artist", {}).get("value", "Wikimedia contributor"))
        artist = re.sub(r"\s+", " ", artist).strip()[:140]
        width = info.get("width") or 0
        height = info.get("height") or 0
        if width and height and (width < 400 or height < 300):
            return {"_rejected": True, "filename": filename, "license": license_short, "reason": "too small"}
        return {
            "filename": filename,
            "url": info.get("thumburl") or info.get("url"),
            "full_url": info.get("url"),
            "page": "https://commons.wikimedia.org/wiki/File:"
            + urllib.parse.quote(filename.replace(" ", "_")),
            "credit": artist or "Wikimedia Commons",
            "license": license_short or "see Commons",
        }
    return None


def name_tokens(name: str, slug: str) -> list[str]:
    raw = re.sub(r"[^\w\s]", " ", f"{name} {slug.replace('-', ' ')}", flags=re.UNICODE)
    stop = {
        "temple",
        "mandir",
        "shrine",
        "devi",
        "lord",
        "sri",
        "shri",
        "mata",
        "ji",
        "the",
        "and",
        "of",
        "india",
    }
    toks = []
    for t in raw.lower().split():
        if len(t) < 4 or t in stop:
            continue
        toks.append(t)
    # keep distinctive slug parts
    for part in slug.split("-"):
        if len(part) >= 4 and part not in stop and part not in toks:
            toks.append(part)
    return toks[:8]


def title_matches(filename: str, tokens: list[str]) -> bool:
    fn = filename.lower().replace("_", " ").replace("-", " ")
    if not tokens:
        return True
    hits = sum(1 for t in tokens if t in fn)
    return hits >= 1


def search_candidates(term: str, limit: int = 12) -> list[str]:
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": term,
            "srnamespace": 6,
            "srlimit": limit,
            "format": "json",
        }
    )
    data = json.loads(get(f"https://commons.wikimedia.org/w/api.php?{q}").decode())
    out = []
    for hit in data.get("query", {}).get("search", []):
        title = hit["title"].replace("File:", "")
        if not title.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        out.append(title)
    return out


def pick_for_temple(slug: str, name: str, state: str) -> dict | None:
    tokens = name_tokens(name, slug)
    tried = set()

    # 1) Priority filenames
    for fn in PRIORITY.get(slug, []):
        tried.add(fn)
        time.sleep(1.2)
        try:
            info = api_file_info(fn)
        except Exception as ex:
            print("  ERR file", fn, ex)
            time.sleep(3)
            continue
        if info and not info.get("_rejected"):
            return info
        if info and info.get("_rejected"):
            print("  skip license/size", fn, info.get("license"), info.get("reason", ""))

    # 2) Search queries
    queries = [
        f"{name} temple",
        f"{name} {state}" if state else None,
        f"{slug.replace('-', ' ')} temple india",
    ]
    for term in queries:
        if not term:
            continue
        time.sleep(1.2)
        try:
            titles = search_candidates(term)
        except Exception as ex:
            print("  SEARCH FAIL", term, ex)
            time.sleep(3)
            continue
        for title in titles:
            if title in tried:
                continue
            tried.add(title)
            if not title_matches(title, tokens):
                continue
            time.sleep(1.0)
            try:
                info = api_file_info(title)
            except Exception as ex:
                print("  ERR", title, ex)
                time.sleep(2)
                continue
            if info and not info.get("_rejected"):
                return info
            if info and info.get("_rejected"):
                print("  skip", title, info.get("license"), info.get("reason", ""))
    return None


def has_local(media: dict, slug: str) -> bool:
    local_existing = media.get(slug, {}).get("local")
    if not local_existing:
        return False
    path = ROOT / local_existing
    return path.exists() and path.stat().st_size > 2000


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    media = json.loads(MEDIA_PATH.read_text(encoding="utf-8")) if MEDIA_PATH.exists() else {}

    temples = []
    for path in sorted(TEMPLES.glob("*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        temples.append(d)

    # Priority order: PRIORITY keys first, then remaining missing
    ordered = []
    seen = set()
    for slug in PRIORITY:
        for t in temples:
            if t["slug"] == slug and slug not in seen:
                ordered.append(t)
                seen.add(slug)
    for t in temples:
        if t["slug"] not in seen:
            ordered.append(t)
            seen.add(t["slug"])

    added = 0
    skipped = 0
    failed = 0
    for t in ordered:
        slug = t["slug"]
        if has_local(media, slug):
            skipped += 1
            continue
        print("FETCH", slug)
        try:
            chosen = pick_for_temple(slug, t.get("name", slug), t.get("state", ""))
        except Exception as ex:
            print("  FAIL", slug, ex)
            failed += 1
            continue
        if not chosen:
            print("  NONE (left without photo)", slug)
            failed += 1
            continue
        ext = Path(urllib.parse.urlparse(chosen["url"]).path).suffix.lower() or ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
            ext = ".jpg"
        local = OUT / f"{slug}{ext}"
        time.sleep(1.0)
        try:
            local.write_bytes(get(chosen["url"]))
        except Exception:
            time.sleep(2)
            local.write_bytes(get(chosen["full_url"]))
        if local.stat().st_size < 2000:
            local.unlink(missing_ok=True)
            print("  TOO SMALL after download", slug)
            failed += 1
            continue
        chosen["local"] = f"assets/temples/{local.name}"
        media[slug] = {k: v for k, v in chosen.items() if not k.startswith("_")}
        added += 1
        print("  SAVED", slug, local.stat().st_size, chosen.get("license"))
        MEDIA_PATH.write_text(json.dumps(media, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"done: added {added}, already had {skipped}, none/fail {failed}, media total {len(media)}")


if __name__ == "__main__":
    main()
