#!/usr/bin/env python3
"""Download Wikimedia Commons images for temples missing local photos."""

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
OUT = ROOT / "assets" / "temples"
UA = {"User-Agent": "TirthaYatraBot/1.1 (educational; TirthaYatraOnline@gmail.com)"}
ctx = ssl.create_default_context()

# Prefer exact filenames first (more reliable than search)
PRIORITY = {
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
}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=45) as r:
        return r.read()


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
        artist = re.sub("<[^<]+?>", "", meta.get("Artist", {}).get("value", "Wikimedia contributor"))
        artist = re.sub(r"\s+", " ", artist).strip()[:140]
        return {
            "filename": filename,
            "url": info.get("thumburl") or info.get("url"),
            "full_url": info.get("url"),
            "page": "https://commons.wikimedia.org/wiki/File:"
            + urllib.parse.quote(filename.replace(" ", "_")),
            "credit": artist or "Wikimedia Commons",
            "license": meta.get("LicenseShortName", {}).get("value", "see Commons"),
        }
    return None


def search(term: str):
    q = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": term,
            "srnamespace": 6,
            "srlimit": 10,
            "format": "json",
        }
    )
    data = json.loads(get(f"https://commons.wikimedia.org/w/api.php?{q}").decode())
    for hit in data.get("query", {}).get("search", []):
        title = hit["title"].replace("File:", "")
        if not title.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        info = api_file_info(title)
        time.sleep(1.5)
        if info:
            return info
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    media = json.loads(MEDIA_PATH.read_text(encoding="utf-8")) if MEDIA_PATH.exists() else {}
    added = 0
    for slug, files in PRIORITY.items():
        local_existing = media.get(slug, {}).get("local")
        if local_existing and (ROOT / local_existing).exists() and (ROOT / local_existing).stat().st_size > 2000:
            print("skip", slug)
            continue
        chosen = None
        for fn in files:
            time.sleep(2.0)
            try:
                info = api_file_info(fn)
                print(("OK" if info else "MISS"), slug, fn)
                if info:
                    chosen = info
                    break
            except Exception as ex:
                print("ERR", slug, fn, ex)
                time.sleep(5)
        if not chosen:
            time.sleep(2)
            try:
                chosen = search(slug.replace("-", " ") + " temple india")
                print("SEARCH", slug, chosen["filename"] if chosen else None)
            except Exception as ex:
                print("SEARCH FAIL", slug, ex)
                continue
        if not chosen:
            continue
        ext = Path(urllib.parse.urlparse(chosen["url"]).path).suffix or ".jpg"
        local = OUT / f"{slug}{ext}"
        time.sleep(1.5)
        try:
            local.write_bytes(get(chosen["url"]))
        except Exception:
            time.sleep(2)
            local.write_bytes(get(chosen["full_url"]))
        chosen["local"] = f"assets/temples/{local.name}"
        media[slug] = chosen
        added += 1
        print("SAVED", slug, local.stat().st_size)
        MEDIA_PATH.write_text(json.dumps(media, indent=2, ensure_ascii=False), encoding="utf-8")

    print("added", added, "total", len(media))


if __name__ == "__main__":
    main()
