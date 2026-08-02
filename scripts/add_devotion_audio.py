#!/usr/bin/env python3
"""Attach YouTube audio/video links to aarti, chalisa, and vrat-katha items."""

from __future__ import annotations

import json
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "devotion.json"

# video_id -> label; None means YouTube search fallback
AUDIO: dict[str, tuple[str | None, str]] = {
    "shiva-aarti": ("BhwOproElxU", "Anuradha Paudwal · Om Jai Shiv Omkara"),
    "shiva-chalisa": (None, "Shiv Chalisa full"),
    "vishnu-aarti": ("NE3SWh9_vR4", "Anuradha Paudwal · Om Jai Jagdish Hare"),
    "vishnu-chalisa": ("adLlMH12tTg", "Vishnu Chalisa with lyrics"),
    "krishna-aarti": ("EMO1AT1UQf0", "Hariharan · Aarti Kunj Bihari Ki"),
    "krishna-chalisa": (None, "Krishna Chalisa full"),
    "devi-aarti": ("RY1jmTTjvhI", "Anuradha Paudwal · Jai Ambe Gauri"),
    "durga-chalisa": ("bwPdADAHWtE", "Anuradha Paudwal · Durga Chalisa"),
    "ganesha-aarti": ("x3eVLuHDdfM", "Sadhana Sargam · Sukhkarta Dukhharta"),
    "ganesha-chalisa": ("WyHFSjN0miU", "Anuradha Paudwal · Ganesh Chalisa"),
    "rama-aarti": ("-v8GkdHngD4", "Shri Ramchandra Kripalu Bhajman"),
    "rama-chalisa": ("FQlA6g1HNZk", "Ram Chalisa with lyrics"),
    "hanuman-aarti": ("r7GJ8GoGSD8", "Hariharan · Aarti Kije Hanuman Lala Ki"),
    "hanuman-chalisa": ("AETFvQonfV8", "Hariharan · Gulshan Kumar · Hanuman Chalisa"),
    "ayyappa-aarti": ("-3dse1ajTSA", "Harivarasanam · Sabarimala evening hymn"),
    "ayyappa-chalisa": (None, "Ayyappa Chalisa full"),
    # Vrat Katha — popular YouTube tellings with in-page embed (same as aarti)
    "pradosh-vrat-katha": ("y7IYZhCe4_8", "Pradosh Vrat Katha · Hindi"),
    "ekadashi-vrat-katha": ("zwtFgICr0UI", "Ekadashi Vrat Katha · Hindi"),
    "janmashtami-vrat-katha": ("2iAEl4M0rdw", "Janmashtami Vrat Katha · Hindi"),
    "navaratri-vrat-katha": ("NKAeEbFhlFQ", "Navaratri / Durga Vrat Katha · Hindi"),
    "ganesh-chaturthi-vrat-katha": ("ZYmxGRf1xOk", "Ganesh Chaturthi Vrat Katha"),
    "ram-navami-vrat-katha": ("Pw1z_fF10Wk", "Ram Navami Vrat Katha · Hindi"),
    "hanuman-jayanti-vrat-katha": ("reu6G6LcGXY", "Mangalwar / Hanuman Vrat Katha · Hindi"),
    "ayyappa-mandala-vrat-katha": ("ZTu-NaIAU-8", "Ayyappa / Sabarimala Katha"),
}


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    for item in data["items"]:
        if item.get("type") not in ("aarti", "chalisa", "vrat-katha"):
            continue
        slug = item["slug"]
        vid, label = AUDIO.get(slug, (None, item.get("title", slug)))
        q = urllib.parse.quote(f"{item.get('titleHi', '')} {item.get('title', '')} full")
        search = f"https://www.youtube.com/results?search_query={q}"
        is_vrat = item.get("type") == "vrat-katha"
        if vid:
            item["audioUrl"] = f"https://www.youtube.com/embed/{vid}"
            item["audioWatchUrl"] = f"https://www.youtube.com/watch?v={vid}"
            item["audioLabel"] = label
            item["audioNote"] = (
                "Popular YouTube recording to watch or listen while reading. "
                "Open on YouTube if the player does not load."
                if is_vrat
                else "Popular YouTube recording to listen while reading. "
                "Open on YouTube if the player does not load."
            )
        else:
            item["audioUrl"] = search
            item["audioWatchUrl"] = search
            prefix = "Watch on YouTube" if is_vrat else "Listen on YouTube"
            item["audioLabel"] = f"{prefix} · {label}"
            item["audioNote"] = (
                "Opens YouTube search for popular recordings of this "
                + ("vrat katha" if is_vrat else "hymn")
                + ". Choose any version you prefer."
            )
    disc = data["section"].get("disclaimer", "")
    if "YouTube" not in disc:
        data["section"]["disclaimer"] = (
            disc.rstrip(".")
            + ". Audio/video players and links use popular public YouTube recordings "
            "for convenience; TirthaYatra does not host the media files."
        )
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n = sum(1 for i in data["items"] if i.get("audioUrl"))
    n_vrat = sum(
        1 for i in data["items"] if i.get("type") == "vrat-katha" and i.get("audioUrl")
    )
    print(f"Audio/video attached for {n} items ({n_vrat} vrat kathas).")


if __name__ == "__main__":
    main()
