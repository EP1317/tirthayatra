#!/usr/bin/env python3
"""Generate static TirthaYatra pages from JSON content."""

from __future__ import annotations

import html
import json
import os
import shutil
import time
import urllib.parse
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT_TEMPLES = ROOT / "temples"
OUT_CIRCUITS = ROOT / "circuits"
OUT_PAGES = ROOT / "pages"

MEDIA: dict = {}
GROUPS: dict = {}
STATE_PORTALS: dict = {}
DEITIES: dict = {}
DEVOTION: dict = {}
OUT_STATES = ROOT / "states"
OUT_DEITIES = ROOT / "deities"
OUT_DEVOTION = ROOT / "devotion"
OUT_FESTIVALS = ROOT / "festivals"
OUT_STORIES = ROOT / "stories"

FESTIVAL_GUIDE: dict = {}
STORIES: dict = {}
ENGAGEMENT: dict = {}

# Bump on every build so browsers don't keep stale HTML-linked CSS/JS.
ASSET_VER = str(int(time.time()))

# Canonical production origin (apex redirects to www).
SITE_URL = "https://www.tirthayatraonline.in"


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# Circuits where traditional yatra sequence matters more than A–Z browsing.
PILGRIMAGE_ORDER_CIRCUITS = {
    "12-jyotirlinga",
    "ashtavinayak",
    "char-dham",
    "chota-char-dham",
    "panch-kedar",
}


def circuit_members(circuit_slug: str, temples: list) -> list:
    """Return temples in canonical group order when available.

    Non-sequence circuits (e.g. 51 Shakti Peeth) are sorted A–Z so names like
    Surkanda Devi are findable when browsing under their letter.
    """
    fixed = GROUPS.get("fixed", {}).get(circuit_slug, {})
    order = fixed.get("order") or []
    by_slug = {t["slug"]: t for t in temples}
    if order:
        members = [by_slug[s] for s in order if s in by_slug]
        extras = [
            t
            for t in temples
            if circuit_slug in t.get("tags", []) and t["slug"] not in order
        ]
        members = members + extras
    else:
        members = [t for t in temples if circuit_slug in t.get("tags", [])]
    if circuit_slug not in PILGRIMAGE_ORDER_CIRCUITS:
        members = sorted(members, key=lambda t: t["name"].casefold())
    return members


def validate_fixed_groups(temples: list) -> None:
    fixed = GROUPS.get("fixed", {})
    by_tags: dict[str, set[str]] = {}
    for t in temples:
        for tag in t.get("tags", []):
            by_tags.setdefault(tag, set()).add(t["slug"])
    for slug, meta in fixed.items():
        expected = meta.get("expected")
        order = meta.get("order") or []
        have = by_tags.get(slug, set())
        want = set(order)
        if expected is not None and (len(have) != expected or have != want):
            raise SystemExit(
                f"Group '{slug}' invalid: have {sorted(have)} (n={len(have)}), "
                f"want {sorted(want)} (n={expected})"
            )


YOUTUBE_EMBED_HOSTS = {
    "www.youtube.com",
    "youtube.com",
    "www.youtube-nocookie.com",
    "youtube-nocookie.com",
}


def safe_url(url: str | None, *, allow_mailto: bool = False) -> str:
    """Return url only if scheme/host are safe for href/iframe use; else ''."""
    if not url or not isinstance(url, str):
        return ""
    raw = url.strip()
    if not raw or raw.startswith("//") or "\\" in raw or "\n" in raw or "\r" in raw:
        return ""
    parsed = urlparse(raw)
    scheme = (parsed.scheme or "").lower()
    if scheme == "mailto":
        if not allow_mailto:
            return ""
        addr = parsed.path or ""
        if "@" in addr and all(c not in addr for c in '<>"\''):
            return raw
        return ""
    if scheme in ("http", "https") and parsed.netloc:
        return raw
    return ""


def is_youtube_embed(url: str | None) -> bool:
    raw = safe_url(url)
    if not raw:
        return False
    parsed = urlparse(raw)
    host = (parsed.hostname or "").lower()
    if host not in YOUTUBE_EMBED_HOSTS:
        return False
    path = parsed.path or ""
    return path.startswith("/embed/") and len(path) > len("/embed/")


def e(text) -> str:
    return html.escape(str(text), quote=True)


def media_for(slug: str) -> dict | None:
    return MEDIA.get(slug)


def img_src(slug: str, prefix: str) -> str | None:
    m = media_for(slug)
    if not m:
        return None
    return prefix + m["local"]


def credit_html(slug: str) -> str:
    m = media_for(slug)
    if not m:
        return ""
    page = safe_url(m.get("page"))
    link = (
        f'<a href="{e(page)}" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a>'
        if page
        else "Wikimedia Commons"
    )
    return (
        f'<p class="img-credit">Photo: {e(m.get("credit", "Wikimedia Commons"))} · '
        f"{e(m.get('license', ''))} · {link}</p>"
    )


def thumb_html(slug: str, glyph: str, prefix: str, alt: str = "") -> str:
    src = img_src(slug, prefix)
    if src:
        return (
            f'<div class="temple-thumb">'
            f'<img src="{e(src)}" alt="{e(alt)}" loading="lazy" width="160" height="160" />'
            f"</div>"
        )
    return f'<div class="temple-mark" aria-hidden="true">{e(glyph or "ॐ")}</div>'


def paras_html(text: str) -> str:
    chunks = [c.strip() for c in str(text or "").split("\n\n") if c.strip()]
    if not chunks:
        return ""
    return "".join(f"<p>{e(c)}</p>" for c in chunks)


def sacred_phrase_html(t: dict) -> str:
    phrase = t.get("sacredPhrase")
    if not phrase or not phrase.get("text") or not phrase.get("meaning"):
        return ""
    source = phrase.get("source") or ""
    source_html = f'<p class="sacred-phrase-source">{e(source)}</p>' if source else ""
    return f"""
      <blockquote class="sacred-phrase">
        <p class="sacred-phrase-text">{e(phrase["text"])}</p>
        <p class="sacred-phrase-meaning">{e(phrase["meaning"])}</p>
        {source_html}
      </blockquote>
    """


def mythology_html(t: dict) -> str:
    significance = t.get("mythologySignificance") or t.get("mythology") or ""
    local = t.get("localBeliefs") or ""
    parts = [sacred_phrase_html(t)]
    parts.extend(
        [
            "<h3>Significance in mythology</h3>",
            paras_html(significance),
        ]
    )
    if local:
        parts.append("<h3>Local stories &amp; beliefs</h3>")
        parts.append(paras_html(local))
    return "".join(parts)


def map_embed(t: dict) -> str:
    lat, lng = t.get("lat"), t.get("lng")
    query = t.get("mapQuery") or t.get("name")
    if lat is not None and lng is not None:
        q = f"{lat},{lng}"
    else:
        q = query
    src = (
        "https://maps.google.com/maps?q="
        + urllib.parse.quote(str(q))
        + "&z=14&hl=en&output=embed"
    )
    maps_link = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(
        str(query)
    )
    return f"""
    <div class="map-embed">
      <iframe src="{e(src)}" title="Map of {e(t['name'])}" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
    <p class="map-actions">
      <a class="btn btn-ghost" href="{e(maps_link)}" target="_blank" rel="noopener noreferrer">Open in Google Maps ↗</a>
    </p>
    """


def temple_row(t: dict, href: str, prefix: str, cta: str = "Open →") -> str:
    tags = "".join(f'<span class="tag">{e(x)}</span>' for x in t.get("tagLabels", [])[:3])
    country = t.get("country", "India")
    state = t.get("state", "")
    place = f"{country} · {state}" if state else country
    # No scroll-reveal on rows — long lists stay readable and Ctrl+F / letter-scan works.
    return f"""
    <a class="temple-row" href="{e(href)}">
      {thumb_html(t['slug'], t.get('glyph', 'ॐ'), prefix, t['name'])}
      <div class="temple-row-body">
        <h3>{e(t['name'])}</h3>
        <p class="temple-row-meta">{e(place)} · {e(t['famousFor'])}</p>
        <div class="temple-tags">{tags}</div>
      </div>
      <span class="temple-row-cta">{e(cta)}</span>
    </a>
    """


def state_slug(state_name: str) -> str:
    portal = STATE_PORTALS.get(state_name)
    if portal:
        return portal["slug"]
    return (
        state_name.lower()
        .replace("&", "and")
        .replace(" ", "-")
        .replace("/", "-")
    )


def search_widget(prefix: str = "") -> str:
    """Pill search used in the site nav (left of menu links)."""
    return f"""
<div class="temple-search" data-temple-search data-prefix="{e(prefix)}">
  <div class="temple-search-shell">
    <label class="temple-search-label" for="temple-search-input">
      <svg class="temple-search-icon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
        <circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/>
        <path d="M16.2 16.2L21 21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <span class="visually-hidden">Search temples</span>
    </label>
    <input id="temple-search-input" class="temple-search-input" type="search"
      placeholder="Search temples, deities, states…" autocomplete="off" spellcheck="false"
      data-search-input aria-autocomplete="list" aria-controls="temple-search-results" />
  </div>
  <div id="temple-search-results" class="temple-search-results" data-search-results role="listbox" hidden></div>
</div>
"""


def panchang_widget(prefix: str = "") -> str:
    """Compact daily panchang chip — top-right; updates from visitor's IST date."""
    return f"""
<div class="panchang-widget" data-panchang data-prefix="{e(prefix)}">
  <button type="button" class="panchang-chip" data-panchang-toggle aria-expanded="false" aria-controls="panchang-panel" title="Today's Panchang">
    <span class="panchang-chip-kicker">पंचांग</span>
    <span class="panchang-chip-date" data-panchang-date>…</span>
    <span class="panchang-chip-tithi" data-panchang-tithi></span>
    <span class="panchang-chip-fest" data-panchang-fest hidden></span>
  </button>
  <div id="panchang-panel" class="panchang-panel" data-panchang-panel hidden>
    <p class="panchang-panel-title">आज का पंचांग · Today's Panchang</p>
    <div data-panchang-body></div>
  </div>
</div>
"""


def nav(active: str = "", prefix: str = "", *, show_panchang: bool = False) -> str:
    links = [
        ("index.html", "Home", "home"),
        ("circuits/index.html", "Tirtha Chakra", "circuits"),
        ("deities/index.html", "Devi-Devata", "deities"),
        ("devotion/aarti.html", "Aarti", "aarti"),
        ("devotion/chalisa.html", "Chalisa", "chalisa"),
        ("devotion/vrat-katha.html", "Vrat Katha", "vrat-katha"),
        ("festivals/index.html", "Festivals", "festivals"),
        ("stories/index.html", "Stories", "stories"),
        ("devotion/daily.html", "Today", "daily"),
        ("my-board.html", "My Board", "board"),
        ("states/index.html", "States", "states"),
        ("pages/about.html", "About", "about"),
    ]
    items = []
    for href, label, key in links:
        cls = ' class="active"' if key == active else ""
        items.append(f'<li><a href="{prefix}{href}"{cls}>{label}</a></li>')
    panchang = panchang_widget(prefix) if show_panchang else ""
    return f"""
<header class="site-nav">
  <div class="nav-left">
    <a class="nav-brand" href="{prefix}index.html">TirthaYatra <span>तीर्थयात्रा</span></a>
    {search_widget(prefix)}
  </div>
  <div class="nav-right">
    <button class="nav-toggle" type="button" aria-label="Menu" data-nav-toggle>Menu</button>
    <ul class="nav-links" data-nav-links>
      {''.join(items)}
    </ul>
    {panchang}
  </div>
</header>
"""


def today_bar_html(prefix: str = "") -> str:
    return f"""
<aside class="today-bar" data-today-bar data-prefix="{e(prefix)}">
  <div class="today-bar-inner">
    <div class="today-bar-lead">
      <a class="today-bar-home" href="{prefix}devotion/daily.html">आज · Today</a>
      <div class="today-bar-panchang-wrap">
        <button type="button" class="today-bar-panchang" data-today-panchang-toggle aria-expanded="false" aria-controls="today-panchang-panel" title="आज का पंचांग">
          <span class="today-bar-panchang-kicker">पंचांग</span>
          <span class="today-bar-panchang-line" data-today-panchang-line>…</span>
        </button>
        <div id="today-panchang-panel" class="today-bar-panchang-panel" data-today-panchang-panel hidden></div>
      </div>
      <span class="today-bar-date" data-today-date></span>
    </div>
    <div class="today-bar-links" data-today-links></div>
    <div class="today-bar-tools">
      <div class="lang-toggle" role="group" aria-label="Language">
        <button type="button" class="lang-toggle-btn" data-lang-toggle="hi">हिंदी</button>
        <button type="button" class="lang-toggle-btn" data-lang-toggle="en">EN</button>
      </div>
    </div>
  </div>
</aside>
"""


def footer(prefix: str = "") -> str:
    return f"""
{today_bar_html(prefix)}
<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <p class="footer-brand">TirthaYatra</p>
      <p>Stories, circuits, and practical darshan guides — India, Nepal, Sri Lanka, and the Kailash pilgrimage landscape.</p>
    </div>
    <div class="footer-col footer-col-explore">
      <h3>Explore</h3>
      <div class="footer-explore-grid">
        <a href="{prefix}circuits/12-jyotirlinga.html">12 Jyotirlinga</a>
        <a href="{prefix}festivals/calendar.html">Festival calendar</a>
        <a href="{prefix}circuits/ashtavinayak.html">Ashtavinayak</a>
        <a href="{prefix}festivals/index.html">Festival guides</a>
        <a href="{prefix}circuits/char-dham.html">Char Dham</a>
        <a href="{prefix}stories/index.html">Short stories</a>
        <a href="{prefix}circuits/modern-temples.html">Modern Temples</a>
        <a href="{prefix}devotion/daily.html">Today’s practice</a>
        <a href="{prefix}circuits/beyond-india.html">Beyond India</a>
        <a href="{prefix}my-board.html">My Board</a>
        <a href="{prefix}deities/index.html">By Deity</a>
        <a href="{prefix}devotion/index.html">Aarti · Chalisa · Vrat</a>
        <a href="{prefix}states/index.html">By State</a>
        <a href="{prefix}temples/index.html">All Temples</a>
        <a href="{prefix}pages/creator-kit.html">Share kit · Reels</a>
      </div>
    </div>
    <div class="footer-col">
      <h3>Trust</h3>
      <a href="{prefix}pages/about.html">About</a>
      <a href="{prefix}pages/contact.html">Contact</a>
      <a href="{prefix}pages/feedback.html">Feedback</a>
      <a href="{prefix}pages/privacy.html">Privacy Policy</a>
      <a href="{prefix}pages/disclaimer.html">Disclaimer</a>
      <a href="{prefix}pages/terms.html">Terms</a>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 TirthaYatra. Informational home-devotion &amp; temple guide — not affiliated with any temple trust. Photos via Wikimedia Commons (see credits). Traditional narratives retold for learning; confirm ritual timing with your panchang or family priest.</p>
  </div>
</footer>
<script src="{prefix}js/main.js?v={ASSET_VER}"></script>
<script src="{prefix}js/search.js?v={ASSET_VER}"></script>
<script src="{prefix}js/board.js?v={ASSET_VER}"></script>
<script src="{prefix}js/feedback.js?v={ASSET_VER}"></script>
<script src="{prefix}js/share.js?v={ASSET_VER}"></script>
<script src="{prefix}js/lang-pref.js?v={ASSET_VER}"></script>
<script src="{prefix}js/panchang.js?v={ASSET_VER}"></script>
<script src="{prefix}js/today-bar.js?v={ASSET_VER}"></script>
<script src="{prefix}js/vercel-analytics.js?v={ASSET_VER}"></script>
<script defer src="/_vercel/insights/script.js"></script>
"""


def head(
    title: str,
    description: str,
    prefix: str = "",
    extra: str = "",
    *,
    lang: str = "en",
    canonical_path: str | None = None,
    default_lang: str | None = None,
    og_type: str = "website",
) -> str:
    """Page head with description, Open Graph, and optional Hindi-first default."""
    canon = ""
    if canonical_path:
        loc = sitemap_loc(canonical_path)
        canon = f'<link rel="canonical" href="{e(loc)}" />\n  <meta property="og:url" content="{e(loc)}" />'
    else:
        loc = SITE_URL
    html_lang = "hi" if (default_lang or lang) == "hi" else "en"
    body_default = default_lang or lang or "en"
    return f"""<!DOCTYPE html>
<html lang="{e(html_lang)}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}" />
  <meta name="theme-color" content="#2a160e" />
  <meta property="og:site_name" content="TirthaYatra" />
  <meta property="og:type" content="{e(og_type)}" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(description)}" />
  <meta property="og:locale" content="{"hi_IN" if html_lang == "hi" else "en_IN"}" />
  <meta name="twitter:card" content="summary" />
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <meta http-equiv="Pragma" content="no-cache" />
  {canon}
  <link rel="stylesheet" href="{prefix}css/main.css?v={ASSET_VER}" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6215389980830107"
     crossorigin="anonymous"></script>
  {extra}
</head>
<body data-default-lang="{e(body_default)}">
"""


def list_html(items: list) -> str:
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def nearby_html(items: list, prefix: str) -> str:
    parts = []
    for n in items:
        if n.get("slug"):
            parts.append(
                f'<a class="related-link" href="{prefix}temples/{e(n["slug"])}.html">'
                f'<strong>{e(n["name"])}</strong>{e(n.get("note", ""))}</a>'
            )
        else:
            parts.append(
                f'<div class="related-link"><strong>{e(n["name"])}</strong>{e(n.get("note", ""))}</div>'
            )
    return '<div class="related-strip">' + "".join(parts) + "</div>"


def collage_html(temples: list, prefix: str, limit: int = 9) -> str:
    """Build a photo collage; prefer temples that have local images.

    Uses 9 cells so the 4-column span pattern (tall + wide tiles) fills
    without leaving an empty hole in the masonry grid.
    """
    with_photo = [t for t in temples if img_src(t["slug"], prefix)]
    cells = []
    for i, t in enumerate(with_photo[:limit]):
        src = img_src(t["slug"], prefix)
        cells.append(
            f'<a class="collage-cell collage-cell--{i}" href="{prefix}temples/{e(t["slug"])}.html">'
            f'<img src="{e(src)}" alt="{e(t["name"])}" loading="lazy" />'
            f'<span>{e(t["name"])}</span></a>'
        )
    if not cells:
        return ""
    return f'<div class="collage reveal" aria-label="Temple photo collage">{"".join(cells)}</div>'


def deity_tags_html(t: dict, prefix: str) -> str:
    families = t.get("deityFamilies") or []
    parts = []
    for fam in families:
        meta = DEITIES.get(fam)
        if not meta:
            continue
        parts.append(
            f'<a class="tag" href="{prefix}deities/{e(fam)}.html">{e(meta["nameHi"])} · {e(meta["name"])}</a>'
        )
    return "".join(parts)


def build_temple(t: dict, all_temples: list, circuits_by_slug: dict) -> str:
    prefix = "../"
    tags = "".join(
        f'<a class="tag" href="{prefix}circuits/{e(slug)}.html">{e(label)}</a>'
        for slug, label in zip(t["tags"], t["tagLabels"])
    )
    tags = deity_tags_html(t, prefix) + tags
    scripture = ", ".join(t.get("scriptureLinks", []))
    video = ""
    video_url = safe_url(t.get("videoUrl"))
    if video_url and is_youtube_embed(video_url):
        video = f"""
        <div class="video-embed">
          <iframe src="{e(video_url)}" title="{e(t['name'])} video"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen loading="lazy"></iframe>
        </div>
        <p>{e(t.get('videoNote', ''))}</p>
        """
    elif video_url:
        video = f"""
        <p>{e(t.get('videoNote', 'Watch curated videos for orientation — then verify details on official sites.'))}</p>
        <p><a class="btn btn-ghost" href="{e(video_url)}" target="_blank" rel="noopener noreferrer">Open related videos ↗</a></p>
        """

    official = safe_url(t.get("officialWebsite"))
    official_html = (
        f'<p><a class="official-link" href="{e(official)}" target="_blank" rel="noopener noreferrer">'
        "Official trust / tourism website ↗</a></p>"
        if official
        else ""
    )

    related = []
    for n in t.get("nearby", []):
        if n.get("slug"):
            related.append(n)
    my_deities = set(t.get("deityFamilies") or [])
    for other in all_temples:
        if other["slug"] == t["slug"]:
            continue
        shared_deity = my_deities & set(other.get("deityFamilies") or [])
        shared_circuit = set(other.get("tags", [])) & set(t.get("tags", []))
        if shared_deity or shared_circuit:
            note = other.get("famousFor", "Related shrine")
            if shared_deity and not shared_circuit:
                note = f"Same deity path · {note}"
            related.append({"name": other["name"], "slug": other["slug"], "note": note})
        if len(related) >= 4:
            break

    import build_engage

    post_visit = build_engage.temple_post_visit_loop(
        t,
        prefix=prefix,
        related_html=nearby_html(related[:4], prefix),
        devotion_items=devotion_items(),
        festival_guide=FESTIVAL_GUIDE,
        stories_data=STORIES,
    )
    feedback_block = build_engage.feedback_section_html("temple")

    src = img_src(t["slug"], prefix)
    hero_media = ""
    gallery = ""
    if src:
        hero_media = f"""
        <div class="page-hero-media">
          <img src="{e(src)}" alt="{e(t['name'])}" />
        </div>
        """
        gallery = f"""
        <section class="temple-section" id="gallery">
          <h2>Temple Glimpse</h2>
          <figure class="temple-figure">
            <img src="{e(src)}" alt="{e(t['name'])} — {e(t.get('famousFor', ''))}" loading="lazy" />
            <figcaption>{e(t.get('famousFor', ''))}. {credit_html(t['slug']).replace('<p class="img-credit">', '').replace('</p>', '')}</figcaption>
          </figure>
        </section>
        """

    country = t.get("country", "India")
    body = f"""
{nav('temples', prefix)}
<section class="page-hero page-hero--photo">
  {hero_media}
  <div class="page-hero-inner">
    <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}temples/index.html">Temples</a> · {e(t['name'])}</p>
    <h1>{e(t['name'])}</h1>
    <p class="lede">{e(country)} · {e(t['location'])}</p>
    <p class="lede">{e(t['summary'])}</p>
    <div class="temple-tags" style="margin-top:1rem">{tags}</div>
  </div>
</section>
<div class="temple-layout">
  <article class="temple-main">
    {gallery}

    <section class="temple-section" id="mythology">
      <h2>Mythology &amp; Significance</h2>
      {mythology_html(t)}
      <p><strong>Scriptural &amp; traditional links:</strong> {e(scripture)}</p>
      <p><strong>Known for:</strong> {e(t['famousFor'])}</p>
      <aside class="belief-disclaimer">
        <strong>Disclaimer on stories &amp; beliefs:</strong>
        {e(t.get("mythologyDisclaimer") or (
            "Mythological accounts and local beliefs are drawn from Puranic traditions, epics, "
            "and widely recorded sthala-purana / pilgrimage lore. Versions differ by scripture, "
            "region, and temple tradition. This section is for cultural understanding — not a "
            "claim of historical fact, nor a substitute for guidance from temple priests or official trusts."
        ))}
      </aside>
    </section>

    <section class="temple-section" id="festivals">
      <h2>Important Days, Festivals &amp; Best Time</h2>
      <h3>Festivals &amp; sacred days</h3>
      {list_html(t.get('festivals', []))}
      <div class="fact-grid">
        <div class="fact"><dt>Best time to go</dt><dd>{e(t['bestTime'])}</dd></div>
        <div class="fact"><dt>Climate</dt><dd>{e(t['climate'])}</dd></div>
        <div class="fact"><dt>What to carry</dt><dd>{e(t['whatToCarry'])}</dd></div>
      </div>
    </section>

    <section class="temple-section" id="media">
      <h2>Watch &amp; Learn</h2>
      {video}
    </section>

    <section class="temple-section" id="location">
      <h2>Location on Map</h2>
      <p>Pinpoint the sacred site, then plan your approach from the nearest rail or airport listed below.</p>
      {map_embed(t)}
    </section>

    <section class="temple-section" id="itinerary">
      <h2>Getting There, Stay &amp; Food</h2>
      <div class="fact-grid">
        <div class="fact"><dt>Nearest railway</dt><dd>{e(t['nearestRail'])}</dd></div>
        <div class="fact"><dt>Nearest airport</dt><dd>{e(t['nearestAirport'])}</dd></div>
        <div class="fact"><dt>Local language</dt><dd>{e(t['localLanguage'])}</dd></div>
      </div>
      <h3>Accommodation</h3>
      <p>{e(t['accommodation'])}</p>
      <h3>Local food</h3>
      <p>{e(t['localFood'])}</p>
      <h3>Other food options</h3>
      <p>{e(t['otherFood'])}</p>
    </section>

    <section class="temple-section" id="nearby">
      <h2>Nearby Places &amp; Clubbed Packages</h2>
      <h3>Same-trip places</h3>
      {nearby_html(t.get('nearby', []), prefix)}
      <h3>Suggested packages</h3>
      {list_html(t.get('packages', []))}
    </section>

    <section class="temple-section" id="practical">
      <h2>Practical Darshan Details</h2>
      <div class="fact-grid">
        <div class="fact"><dt>Dress code</dt><dd>{e(t['dressCode'])}</dd></div>
        <div class="fact"><dt>Darshan timings</dt><dd>{e(t['darshanTimings'])}</dd></div>
        <div class="fact"><dt>Special entry / passes</dt><dd>{e(t['specialEntry'])}</dd></div>
        <div class="fact"><dt>Lockers</dt><dd>{e(t['lockers'])}</dd></div>
      </div>
      <h3>Restrictions at gates</h3>
      <p>{e(t['restrictions'])}</p>
      {official_html}
      {state_portal_html(t, prefix)}
    </section>

    <section class="temple-section" id="sources">
      <h2>Sources &amp; Updates</h2>
      <div class="sources">{list_html(t.get('sources', []))}</div>
      {credit_html(t['slug'])}
      <p class="updated">Last updated: {e(t['lastUpdated'])}. {e(t.get('disclaimer', ''))}</p>
    </section>

    {post_visit}

    {feedback_block}
  </article>

  <aside class="temple-aside">
    <nav class="toc">
      <h2>On this page</h2>
      <ol>
        <li><a href="#gallery">Glimpse</a></li>
        <li><a href="#mythology">Mythology</a></li>
        <li><a href="#festivals">Festivals &amp; season</a></li>
        <li><a href="#media">Videos</a></li>
        <li><a href="#location">Map</a></li>
        <li><a href="#itinerary">Travel &amp; food</a></li>
        <li><a href="#nearby">Nearby &amp; packages</a></li>
        <li><a href="#practical">Dress code &amp; timings</a></li>
        <li><a href="#feedback">Feedback</a></li>
      </ol>
    </nav>
    <div class="aside-tags">{tags}</div>
    <p style="margin-top:1.25rem;font-size:0.9rem;color:var(--stone)">
      <strong>{e(t['deity'])}</strong><br />{e(country)} · {e(t['location'])}
    </p>
  </aside>
</div>
{footer(prefix)}
</body>
</html>
"""
    return head(f"{t['name']} — TirthaYatra", t["summary"], prefix) + body


def build_circuit(c: dict, temples: list) -> str:
    prefix = "../"
    members = circuit_members(c["slug"], temples)
    expected = c.get("expected") or GROUPS.get("fixed", {}).get(c["slug"], {}).get("expected")
    rows = [
        temple_row(t, f"{prefix}temples/{t['slug']}.html", prefix, "Open guide →")
        for t in members
    ]
    if not rows:
        rows.append(
            '<p class="comment-empty">More temples for this circuit are being added.</p>'
        )

    if expected:
        title_count = f"{len(members)} of {expected} temples in this complete set"
        if len(members) != expected:
            title_count += " — count mismatch (rebuild required)"
    else:
        title_count = f"{len(members)} guides on this open trail"

    body = f"""
{nav('circuits', prefix)}
<section class="page-hero">
  <div class="page-hero-inner">
    <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}circuits/index.html">Circuits</a> · {e(c['name'])}</p>
    <h1>{e(c['name'])}</h1>
    <p class="lede">{e(c.get('sanskrit', ''))} — {e(c['lede'])}</p>
  </div>
</section>
<div class="circuit-intro">
  <p>{e(c['blurb'])}</p>
  {collage_html(members, prefix)}
</div>
<section class="section">
  <div class="section-head">
    <p class="section-kicker">Temples on this path</p>
    <h2 class="section-title">{e(title_count)}</h2>
    <p class="section-desc">{e(
      "Listed in traditional yatra order."
      if c["slug"] in PILGRIMAGE_ORDER_CIRCUITS
      else "Listed A–Z for easy browsing — search the page for a name (e.g. Surkanda)."
    )}</p>
  </div>
  <div class="temple-list">{''.join(rows)}</div>
  <p style="margin-top:2rem">
    <a class="btn btn-ghost" href="{prefix}temples/index.html">Browse all temples</a>
  </p>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(f"{c['name']} — TirthaYatra", c["lede"], prefix) + body


def build_home(circuits: list, temples: list) -> str:
    import build_engage

    prefix = ""
    tiles = []
    for c in circuits:
        count = sum(1 for t in temples if c["slug"] in t.get("tags", []))
        tiles.append(
            f"""
            <a class="circuit-tile reveal" href="circuits/{e(c['slug'])}.html">
              <p class="circuit-count">{e(c['countLabel'])} · {count} on site</p>
              <h3 class="circuit-name">{e(c['name'])}</h3>
              <p class="circuit-blurb">{e(c['blurb'])}</p>
              <span class="circuit-arrow">Enter circuit →</span>
            </a>
            """
        )

    featured = temples[:8]
    rows = [
        temple_row(t, f"temples/{t['slug']}.html", prefix, "Read guide →")
        for t in featured
    ]
    collage = collage_html(temples, prefix)
    international = [t for t in temples if t.get("country") and t["country"] != "India"]

    body = f"""
{nav('home', prefix, show_panchang=True)}
<section class="hero">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="hero-photo-layer" aria-hidden="true"></div>
  <div class="hero-silhouette" aria-hidden="true"></div>
  <div class="hero-diyas" aria-hidden="true">
    <span class="diya"></span><span class="diya"></span><span class="diya"></span><span class="diya"></span>
  </div>
  <div class="hero-content">
    <h1 class="hero-brand">TirthaYatra<em>पथं पुण्यस्य — the path of sacred journeys</em></h1>
    <p class="hero-line">Temple stories, circuits, and darshan-ready guides.</p>
    <p class="hero-sub">From Jyotirlingas to Ramayana Lanka, Nepal’s Shaiva seats, and Shiva’s Kailasa —<br class="hero-sub-break" /> mythology with maps, photos, and practical gate rules.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="#circuits">Explore sacred circuits</a>
      <a class="btn btn-ghost" href="temples/index.html">Browse temples</a>
    </div>
  </div>
</section>

<section class="section" id="gallery-home">
  <div class="section-head reveal">
    <p class="section-kicker">दृश्य यात्रा · See the path</p>
    <h2 class="section-title">A collage of tirthas</h2>
    <p class="section-desc">Tap any frame to open its full guide — India and beyond.</p>
  </div>
  {collage}
</section>

<section class="section" id="circuits">
  <div class="section-head reveal">
    <p class="section-kicker">तीर्थ चक्र · Sacred circuits</p>
    <h2 class="section-title">Begin with a path, not a list</h2>
    <p class="section-desc">Choose a legendary circuit — then open each temple’s mythology, map, photos, and practical gate rules for respectful visits.</p>
  </div>
  <div class="circuit-grid">
    {''.join(tiles)}
  </div>
</section>

<section class="section-band">
  <div class="section">
    <div class="section-head reveal">
      <p class="section-kicker">Featured guides</p>
      <h2 class="section-title">Temples waiting on your yatra</h2>
      <p class="section-desc">Famous shrines, Tier-2/3 tirthas, and cross-border sacred sites — one clear template everywhere.</p>
    </div>
    <div class="temple-list">{''.join(rows)}</div>
    <p style="margin-top:2rem">
      <a class="btn btn-primary" href="temples/index.html">See all {len(temples)} temple guides</a>
    </p>
  </div>
</section>

<section class="section">
  <div class="section-head reveal">
    <p class="section-kicker">देवता वार · By deity</p>
    <h2 class="section-title">Shiva, Vishnu, Krishna, Devi &amp; more</h2>
    <p class="section-desc">Browse temples by the deity at the centre of worship — including the full Krishna trail of Braj, Dwarka, and beyond.</p>
  </div>
  <div class="circuit-grid">
    {''.join(deity_tiles_home(temples))}
  </div>
  <p style="margin-top:1.5rem">
    <a class="btn btn-primary" href="deities/index.html">All deity paths</a>
  </p>
</section>

<section class="section section-band">
  <div class="section">
    <div class="section-head reveal">
      <p class="section-kicker">भक्ति पाठ · Devotion</p>
      <h2 class="section-title">Aarti · Chalisa · Vrat Katha</h2>
      <p class="section-desc">Home-puja hymns and vow stories for every deity path on TirthaYatra — from Hanuman Chalisa to Shiva Aarti and Navaratri katha.</p>
    </div>
    <div class="circuit-grid">
      <a class="circuit-tile reveal" href="devotion/aarti.html">
        <p class="circuit-count">Aarti</p>
        <h3 class="circuit-name">आरती</h3>
        <p class="circuit-blurb">Lamp hymns for dawn and dusk darshan.</p>
        <span class="circuit-arrow">Open →</span>
      </a>
      <a class="circuit-tile reveal" href="devotion/chalisa.html">
        <p class="circuit-count">Chalisa</p>
        <h3 class="circuit-name">चालीसा</h3>
        <p class="circuit-blurb">Forty-verse praises — Hanuman, Shiva, Devi, and more.</p>
        <span class="circuit-arrow">Open →</span>
      </a>
      <a class="circuit-tile reveal" href="devotion/vrat-katha.html">
        <p class="circuit-count">Vrat Katha</p>
        <h3 class="circuit-name">व्रत कथा</h3>
        <p class="circuit-blurb">Ekadashi, Pradosh, Chaturthi, Navaratri &amp; Mandala stories.</p>
        <span class="circuit-arrow">Open →</span>
      </a>
      <a class="circuit-tile reveal" href="festivals/calendar.html">
        <p class="circuit-count">Festivals</p>
        <h3 class="circuit-name">त्योहार</h3>
        <p class="circuit-blurb">Calendar, home-puja guides, diaspora tips — Shivaratri to Diwali.</p>
        <span class="circuit-arrow">Open calendar →</span>
      </a>
      <a class="circuit-tile reveal" href="stories/index.html">
        <p class="circuit-count">Short stories</p>
        <h3 class="circuit-name">कथा</h3>
        <p class="circuit-blurb">60–90 second myth explainers for first-timers and families.</p>
        <span class="circuit-arrow">Read →</span>
      </a>
      <a class="circuit-tile reveal" href="devotion/daily.html">
        <p class="circuit-count">Daily habit</p>
        <h3 class="circuit-name">आज</h3>
        <p class="circuit-blurb">Today’s aarti + katha + story — for home practice.</p>
        <span class="circuit-arrow">Start →</span>
      </a>
    </div>
    <p style="margin-top:1.5rem">
      <a class="btn btn-primary" href="devotion/index.html">All devotion texts</a>
      <a class="btn btn-ghost" href="festivals/calendar.html" style="margin-left:0.75rem">Festival calendar</a>
      <a class="btn btn-ghost" href="my-board.html" style="margin-left:0.75rem">My Board</a>
    </p>
  </div>
</section>

{build_engage.build_home_engage_band(ENGAGEMENT, FESTIVAL_GUIDE, ASSET_VER, prefix)}

<section class="section">
  <div class="section-head reveal">
    <p class="section-kicker">राज्य वार · By state</p>
    <h2 class="section-title">Explore temples state-wise</h2>
    <p class="section-desc">From Andhra Pradesh’s <a href="https://www.aptemples.org/en-in/home" target="_blank" rel="noopener noreferrer">AP Temples</a> portal to TN HR&CE, Telangana Endowments, Karnataka HRI&CE, Rajasthan Devasthan, and more — browse guides, then verify on official sites.</p>
  </div>
  <div class="circuit-grid">
    {''.join(state_tiles_home(temples))}
  </div>
  <p style="margin-top:1.5rem">
    <a class="btn btn-primary" href="states/index.html">All states</a>
  </p>
</section>

<section class="section">
  <div class="section-head reveal">
    <p class="section-kicker">Beyond borders</p>
    <h2 class="section-title">Nepal · Sri Lanka · Kailash</h2>
    <p class="section-desc">Mythology travels with the epic — Ramayana Lanka, Himalayan Shaiva seats, and the Kailasa parikrama landscape.</p>
  </div>
  <div class="temple-list">
    {''.join(temple_row(t, f"temples/{t['slug']}.html", prefix, "Explore →") for t in international)}
  </div>
  <p style="margin-top:1.5rem">
    <a class="btn btn-ghost" href="circuits/beyond-india.html">Open Beyond India circuit</a>
  </p>
</section>

<section class="section">
  <div class="section-head reveal">
    <p class="section-kicker">Why TirthaYatra</p>
    <h2 class="section-title">One template. Full pilgrimage clarity.</h2>
    <p class="section-desc">Photos, Google Maps, mythology, festivals, travel, food, dress code, timings, and official links — so you keep exploring.</p>
  </div>
  <div class="fact-grid reveal">
    <div class="fact"><dt>Mythology</dt><dd>Story, significance, and scripture links across India and neighbouring sacred lands.</dd></div>
    <div class="fact"><dt>Maps &amp; photos</dt><dd>Licensed imagery and Google Maps pins for clearer trip planning.</dd></div>
    <div class="fact"><dt>Practical</dt><dd>Dress code, timings, special entry, phone/leather rules, official sites.</dd></div>
  </div>
</section>
{footer(prefix)}
</body>
</html>
"""
    # Dedicated vivid landing photo when available; else best temple stills
    hero_path = ROOT / "assets" / "hero-landing.jpg"
    hero_img = "assets/hero-landing.jpg" if hero_path.exists() else None
    if not hero_img:
        for slug in (
            "meenakshi-madurai",
            "murudeshwar",
            "kedarnath",
            "rameswaram",
            "jagannath-puri",
            "tirumala-venkateswara",
        ):
            src = img_src(slug, prefix)
            if src:
                hero_img = src
                break
        if not hero_img and temples:
            hero_img = img_src(temples[0]["slug"], prefix)
    if hero_img:
        body = body.replace(
            '<div class="hero-photo-layer" aria-hidden="true"></div>',
            f'<div class="hero-photo-layer" aria-hidden="true" style="background-image:url(\'{e(hero_img)}\')"></div>',
        )

    # Panchang script is loaded site-wide via footer (Today bar + optional home chip).

    return head(
        "TirthaYatra — Temple & Pilgrimage Guides",
        "Mythology, photos, maps, and practical darshan guides for temples in India, Nepal, Sri Lanka, and Kailash.",
        prefix,
    ) + body


def build_temple_index(temples: list) -> str:
    prefix = "../"
    ordered = sorted(temples, key=lambda t: t["name"].casefold())
    rows = [temple_row(t, f"{t['slug']}.html", prefix) for t in ordered]
    body = f"""
{nav('temples', prefix)}
<section class="page-hero">
  <div class="page-hero-inner">
    <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · Temples</p>
    <h1>All Temple Guides</h1>
    <p class="lede">India and beyond — standardised pages with photos, maps, mythology, itinerary, and darshan practicals. Listed A–Z; use the search bar above to jump to any temple.</p>
  </div>
</section>
<section class="section">
  <div class="temple-list">{''.join(rows)}</div>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head("All Temples — TirthaYatra", "Browse all temple pilgrimage guides on TirthaYatra.", prefix) + body


def build_circuit_index(circuits: list, temples: list) -> str:
    prefix = "../"
    tiles = []
    for c in circuits:
        count = sum(1 for t in temples if c["slug"] in t.get("tags", []))
        tiles.append(
            f"""
            <a class="circuit-tile reveal" href="{e(c['slug'])}.html">
              <p class="circuit-count">{e(c['countLabel'])} · {count} guides</p>
              <h3 class="circuit-name">{e(c['name'])}</h3>
              <p class="circuit-blurb">{e(c['blurb'])}</p>
              <span class="circuit-arrow">Open circuit →</span>
            </a>
            """
        )
    body = f"""
{nav('circuits', prefix)}
<section class="page-hero">
  <div class="page-hero-inner">
    <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · Circuits</p>
    <h1>Sacred Circuits</h1>
    <p class="lede">Jyotirlinga, Shakti Peeth, Char Dham, Ramayana trails, and Beyond India — explore by legendary path.</p>
  </div>
</section>
<section class="section">
  <div class="circuit-grid">{''.join(tiles)}</div>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head("Sacred Circuits — TirthaYatra", "Explore temple circuits and pilgrimage tags.", prefix) + body


def deity_tiles_home(temples: list) -> list[str]:
    order = ["shiva", "vishnu", "krishna", "devi", "ganesha", "rama", "hanuman", "ayyappa"]
    tiles = []
    for fam in order:
        meta = DEITIES.get(fam)
        if not meta:
            continue
        count = sum(1 for t in temples if fam in (t.get("deityFamilies") or []))
        if count == 0:
            continue
        tiles.append(
            f"""
            <a class="circuit-tile reveal" href="deities/{e(fam)}.html">
              <p class="circuit-count">{count} temples</p>
              <h3 class="circuit-name">{e(meta['nameHi'])}</h3>
              <p class="circuit-blurb">{e(meta['name'])} · {e(meta['blurb'][:90])}{'…' if len(meta['blurb']) > 90 else ''}</p>
              <span class="circuit-arrow">Open deity path →</span>
            </a>
            """
        )
    return tiles


def build_deities_index(temples: list) -> str:
    prefix = "../"
    order = ["shiva", "vishnu", "krishna", "devi", "ganesha", "rama", "hanuman", "ayyappa"]
    tiles = []
    for fam in order:
        meta = DEITIES.get(fam)
        if not meta:
            continue
        members = [t for t in temples if fam in (t.get("deityFamilies") or [])]
        if not members:
            continue
        tiles.append(
            f"""
            <a class="circuit-tile reveal" href="{e(fam)}.html">
              <p class="circuit-count">{len(members)} temple guides</p>
              <h3 class="circuit-name">{e(meta['nameHi'])} · {e(meta['name'])}</h3>
              <p class="circuit-blurb">{e(meta['blurb'])}</p>
              <span class="circuit-arrow">Browse →</span>
            </a>
            """
        )
    body = f"""
{nav('deities', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · Deities</p>
  <h1>Temples by Deity</h1>
  <p class="lede">Find Shiva, Vishnu, Krishna, Devi, Ganesha, Rama, Hanuman, and Ayyappa temples in one place. A shrine may appear under more than one path when the complex is shared.</p>
</section>
<section class="section">
  <div class="circuit-grid">{''.join(tiles)}</div>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(
        "Temples by Deity — TirthaYatra",
        "Browse Indian and related temples grouped by deity — Shiva, Vishnu, Krishna, Devi, and more.",
        prefix,
    ) + body


def devotion_items() -> list:
    return list(DEVOTION.get("items") or [])


def devotion_item_row(item: dict, prefix: str) -> str:
    dtype = DEVOTION.get("types", {}).get(item["type"], {})
    deity = DEITIES.get(item.get("deity", ""), {})
    type_label = dtype.get("nameHi") or dtype.get("name") or item["type"]
    deity_label = deity.get("nameHi") or deity.get("name") or item.get("deity", "")
    glyph = (deity.get("nameHi") or "ॐ")[:1]
    audio_tag = ""
    if item.get("audioUrl") or item.get("audioWatchUrl"):
        if item.get("type") == "vrat-katha":
            audio_tag = '<span class="tag tag-audio">Video</span>'
        elif item.get("type") in ("aarti", "chalisa"):
            audio_tag = '<span class="tag tag-audio">Audio</span>'
    return f"""
    <a class="temple-row reveal" href="{prefix}devotion/{e(item['slug'])}.html">
      <div class="temple-mark" aria-hidden="true">{e(glyph)}</div>
      <div class="temple-row-body">
        <h3>{e(item['titleHi'])}</h3>
        <p class="temple-row-meta">{e(item['title'])} · {e(deity_label)}</p>
        <p class="temple-row-summary">{e(item.get('summary', ''))}</p>
        <div class="temple-tags">
          <span class="tag">{e(type_label)}</span>
          <span class="tag">{e(deity_label)}</span>
          {audio_tag}
        </div>
      </div>
      <span class="temple-row-cta">Open →</span>
    </a>
    """


def build_devotion_index() -> str:
    prefix = "../"
    sec = DEVOTION.get("section", {})
    types = DEVOTION.get("types", {})
    items = devotion_items()
    type_tiles = []
    for key in ("aarti", "chalisa", "vrat-katha"):
        meta = types.get(key, {})
        count = sum(1 for i in items if i.get("type") == key)
        type_tiles.append(
            f"""
            <a class="circuit-tile reveal" href="{e(key)}.html">
              <p class="circuit-count">{count} texts</p>
              <h3 class="circuit-name">{e(meta.get('nameHi', key))} · {e(meta.get('name', key))}</h3>
              <p class="circuit-blurb">{e(meta.get('blurb', ''))}</p>
              <span class="circuit-arrow">Browse →</span>
            </a>
            """
        )
    deity_tiles = []
    for fam, meta in DEITIES.items():
        count = sum(1 for i in items if i.get("deity") == fam)
        if not count:
            continue
        deity_tiles.append(
            f"""
            <a class="circuit-tile reveal" href="deity-{e(fam)}.html">
              <p class="circuit-count">{count} texts</p>
              <h3 class="circuit-name">{e(meta['nameHi'])}</h3>
              <p class="circuit-blurb">{e(meta['name'])} — aarti, chalisa &amp; vrat katha</p>
              <span class="circuit-arrow">Open →</span>
            </a>
            """
        )
    rows = [devotion_item_row(i, prefix) for i in items]
    body = f"""
{nav('devotion', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · Devotion</p>
  <p class="section-kicker" style="margin-bottom:0.5rem">{e(sec.get('sanskrit', ''))}</p>
  <h1>{e(sec.get('nameHi', 'भक्ति पाठ'))} · {e(sec.get('name', 'Devotion'))}</h1>
  <p class="lede">{e(sec.get('lede', ''))}</p>
</section>
<section class="section">
  <div class="section-head">
    <p class="section-kicker">By type</p>
    <h2 class="section-title">Aarti · Chalisa · Vrat Katha</h2>
  </div>
  <div class="circuit-grid">{''.join(type_tiles)}</div>
</section>
<section class="section">
  <div class="section-head">
    <p class="section-kicker">By deity</p>
    <h2 class="section-title">Choose your Ishta Devata</h2>
  </div>
  <div class="circuit-grid">{''.join(deity_tiles)}</div>
</section>
<section class="section">
  <div class="section-head">
    <p class="section-kicker">All texts</p>
    <h2 class="section-title">{len(items)} devotion guides</h2>
  </div>
  <div class="temple-list">{''.join(rows)}</div>
  <aside class="belief-disclaimer">
    <strong>Note:</strong> {e(sec.get('disclaimer', ''))}
  </aside>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(
        "Aarti, Chalisa & Vrat Katha — TirthaYatra",
        sec.get("blurb", "Devotional hymns and vow stories"),
        prefix,
    ) + body


def devotion_sangrah_grid(items: list, prefix: str, aria_label: str = "Sangrah") -> str:
    """Pill grid for Aarti / Chalisa / Vrat Katha collections."""
    pills = []
    for item in items:
        label = item.get("sangrahLabel") or item.get("titleHi") or item.get("title")
        pills.append(
            f'<a class="aarti-pill" href="{prefix}devotion/{e(item["slug"])}.html">{e(label)}</a>'
        )
    return (
        f'<div class="aarti-sangrah" role="navigation" aria-label="{e(aria_label)}">'
        f'{"".join(pills)}</div>'
    )


def build_devotion_type_page(type_key: str) -> str:
    prefix = "../"
    meta = DEVOTION["types"][type_key]
    items = [i for i in devotion_items() if i.get("type") == type_key]
    rows = [devotion_item_row(i, prefix) for i in items]
    list_titles = {
        "aarti": ("Full aarti texts", "Open any aarti for complete verses and listen-along audio."),
        "chalisa": ("Full chalisa texts", "Open any chalisa for complete verses and listen-along audio."),
        "vrat-katha": (
            "Full vrat katha texts",
            "Open any vrat katha for the complete story and watch/listen along.",
        ),
    }
    sangrah_labels = {
        "aarti": "Aarti Sangrah",
        "chalisa": "Chalisa Sangrah",
        "vrat-katha": "Vrat Katha Sangrah",
    }
    hidden_titles = {
        "aarti": "Aarti names",
        "chalisa": "Chalisa names",
        "vrat-katha": "Vrat katha names",
    }
    sangrah = ""
    if type_key in sangrah_labels:
        sangrah = f"""
<section class="section aarti-sangrah-section">
  <h2 class="section-title visually-hidden">{e(hidden_titles[type_key])}</h2>
  {devotion_sangrah_grid(items, prefix, sangrah_labels[type_key])}
</section>
"""
    title, desc = list_titles.get(
        type_key, ("All texts", "Browse the full collection below.")
    )
    list_block = f"""
<section class="section aarti-list-section">
  <h2 class="section-title">{e(title)}</h2>
  <p class="section-desc">{e(desc)}</p>
  <div class="temple-list">{''.join(rows)}</div>
</section>
"""
    body = f"""
{nav(type_key, prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · {e(meta['name'])}</p>
  <h1>{e(meta['nameHi'])} · {e(meta['name'])} — {len(items)}</h1>
  <p class="lede">{e(meta.get('lede', ''))}</p>
</section>
{sangrah}
{list_block}
{footer(prefix)}
</body>
</html>
"""
    return head(f"{meta['name']} — TirthaYatra", meta.get("blurb", ""), prefix) + body


def build_devotion_deity_page(fam: str) -> str:
    prefix = "../"
    meta = DEITIES[fam]
    items = [i for i in devotion_items() if i.get("deity") == fam]
    rows = [devotion_item_row(i, prefix) for i in items]
    body = f"""
{nav('devotion', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · {e(meta['name'])}</p>
  <p class="section-kicker" style="margin-bottom:0.5rem">{e(meta.get('sanskrit', ''))}</p>
  <h1>{e(meta['nameHi'])} — Aarti, Chalisa &amp; Vrat Katha</h1>
  <p class="lede">Devotional texts for {e(meta['name'])}. Also explore <a href="{prefix}deities/{e(fam)}.html">{e(meta['name'])} temples</a>.</p>
</section>
<section class="section">
  <div class="temple-list">{''.join(rows)}</div>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(
        f"{meta['name']} Aarti & Chalisa — TirthaYatra",
        f"Aarti, Chalisa and Vrat Katha for {meta['name']}",
        prefix,
    ) + body


def devotion_audio_block(item: dict) -> str:
    """YouTube listen/watch player / link for aarti, chalisa & vrat-katha pages."""
    if item.get("type") not in ("aarti", "chalisa", "vrat-katha"):
        return ""
    audio_url = safe_url(item.get("audioUrl"))
    watch_url = safe_url(item.get("audioWatchUrl")) or audio_url
    if not audio_url and not watch_url:
        return ""
    is_vrat = item.get("type") == "vrat-katha"
    label = item.get("audioLabel") or (
        "Watch on YouTube" if is_vrat else "Listen on YouTube"
    )
    note = item.get("audioNote") or (
        "Popular YouTube recording for watching or listening along. "
        "TirthaYatra does not host the media file."
        if is_vrat
        else "Popular YouTube recording for listening along. "
        "TirthaYatra does not host the audio file."
    )
    player = ""
    if audio_url and is_youtube_embed(audio_url):
        # Prefer privacy-enhanced host; keep original if already nocookie.
        embed_src = audio_url.replace(
            "https://www.youtube.com/embed/",
            "https://www.youtube-nocookie.com/embed/",
        )
        player = f"""
    <div class="video-embed devotion-audio-embed">
      <iframe src="{e(embed_src)}" title="{e(item.get('title', 'Devotion'))} {'video' if is_vrat else 'audio'}"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin"
        allowfullscreen loading="lazy"></iframe>
    </div>"""
    link_href = watch_url or audio_url
    heading = "सुनें · Watch / Listen" if is_vrat else "सुनें · Listen"
    btn = "Open video on YouTube ↗" if is_vrat else "Open audio on YouTube ↗"
    actions = (
        f'<p class="devotion-audio-actions">'
        f'<a class="btn btn-primary" href="{e(link_href)}" target="_blank" rel="noopener noreferrer">{btn}</a>'
        f"</p>"
        if link_href
        else ""
    )
    return f"""
    <div class="devotion-audio">
      <h2>{heading}</h2>
      <p class="devotion-audio-label">{e(label)}</p>
      {player}
      {actions}
      <p class="devotion-audio-note">{e(note)}</p>
    </div>
    """


HINDI_PRIMARY_DEVOTION = {
    "shiva-aarti",
    "shiva-chalisa",
    "lingashtakam",
    "ganga-aarti",
    "sawan-somwar-vrat-katha",
    "mangala-gauri-vrat-katha",
    "nag-panchami-vrat-katha",
    "pradosh-vrat-katha",
    "maha-shivaratri-vrat-katha",
    "hanuman-chalisa",
    "durga-chalisa",
    "ganesha-chalisa",
    "rama-chalisa",
    "krishna-chalisa",
    "vishnu-chalisa",
    "ayyappa-chalisa",
    "lakshmi-chalisa",
    "saraswati-chalisa",
    "santoshi-chalisa",
    "gayatri-chalisa",
    "kali-chalisa",
    "shani-chalisa",
    "bhairav-chalisa",
    "surya-chalisa",
    "ganga-chalisa",
    "vaishno-chalisa",
    "sai-chalisa",
    "devi-aarti",
    "hanuman-aarti",
}


def build_devotion_item(item: dict) -> str:
    prefix = "../"
    dtype = DEVOTION.get("types", {}).get(item["type"], {})
    deity = DEITIES.get(item.get("deity", ""), {})
    verses = "".join(
        f'<div class="devotion-verse"><p>{e(v).replace(chr(10), "<br />")}</p></div>'
        for v in item.get("verses", [])
    )
    temples = []
    for slug in item.get("relatedTemples") or []:
        path = DATA / "temples" / f"{slug}.json"
        if path.exists():
            t = load_json(path)
            temples.append(
                f'<a class="tag" href="{prefix}temples/{e(slug)}.html">{e(t["name"])}</a>'
            )
    temple_block = (
        f'<p class="devotion-related"><strong>Related temples:</strong> {"".join(temples)}</p>'
        if temples
        else ""
    )
    audio_block = devotion_audio_block(item)
    nav_active = item.get("type") if item.get("type") in ("aarti", "chalisa", "vrat-katha") else "aarti"
    import build_engage

    abs_path = f"devotion/{item['slug']}.html"
    hindi_first = (
        item["slug"] in HINDI_PRIMARY_DEVOTION
        or item.get("type") == "chalisa"
        or item.get("deity") == "shiva"
    )
    title_hi = item.get("titleHi") or item.get("title") or item["slug"]
    title_en = item.get("title") or title_hi
    page_title = f"{title_hi} | {title_en} — TirthaYatra" if title_hi != title_en else f"{title_en} — TirthaYatra"
    share_text = f"{title_hi} — TirthaYatra · घर की पूजा के लिए"
    desc = item.get("summary") or title_en
    # Prefer Hindi-leaning description for primary pages
    if hindi_first and item.get("when"):
        desc = f"{title_hi}. {item.get('when')}. {desc}"[:300]

    dev_save = build_engage.save_btn(
        "devotion",
        item["slug"],
        item.get("title") or item["slug"],
        f"{prefix}devotion/{item['slug']}.html",
    )
    share = build_engage.share_bar(
        title=page_title,
        text=share_text,
        url=abs_path,
        kind=item.get("type") or "page",
    )
    dev_feedback = build_engage.feedback_section_html("devotion")
    body = f"""
{nav(nav_active, prefix)}
<section class="page-head">
  <p class="breadcrumb">
    <a href="{prefix}index.html">Home</a> ·
    <a href="{prefix}devotion/{e(item['type'])}.html">{e(dtype.get('name', item['type']))}</a>
  </p>
  <div class="page-tools">{build_engage.lang_toggle()}</div>
  <p class="section-kicker" style="margin-bottom:0.5rem">{e(dtype.get('nameHi', ''))} · {e(deity.get('nameHi', ''))}</p>
  <h1 class="lang-hi">{e(title_hi)}</h1>
  <h1 class="lang-en">{e(title_en)}</h1>
  <p>{dev_save} <a class="btn btn-ghost" href="{prefix}devotion/daily.html">Today’s practice</a>
  <button type="button" class="btn btn-ghost" data-feedback-open data-type="correction">Suggest correction</button></p>
  {share}
</section>
<section class="section devotion-section" data-board-open="devotion" data-slug="{e(item['slug'])}">
  <article class="devotion-article">
    <div class="fact-grid">
      <div class="fact"><dt>Deity</dt><dd><a href="{prefix}devotion/deity-{e(item['deity'])}.html">{e(deity.get('name', item['deity']))}</a></dd></div>
      <div class="fact"><dt>Tradition / author</dt><dd>{e(item.get('author', 'Traditional'))}</dd></div>
      <div class="fact"><dt>When to recite</dt><dd>{e(item.get('when', ''))}</dd></div>
    </div>
    {audio_block if item.get("type") == "vrat-katha" else ""}
    <p class="devotion-summary">{e(item.get('summary', ''))}</p>
    {audio_block if item.get("type") != "vrat-katha" else ""}
    <aside class="belief-disclaimer"><strong>Text note:</strong> Traditional hymn / katha presented for personal learning and home puja. Authors and lineages remain with their traditions; TirthaYatra does not claim copyright over classical verses. Optional YouTube listens belong to their uploaders.</aside>
    <h2>पाठ · Text</h2>
    <div class="devotion-verses">{verses}</div>
    <h2>Meaning · अर्थ</h2>
    <p class="devotion-meaning">{e(item.get('meaning', ''))}</p>
    {temple_block}
    <aside class="belief-disclaimer">
      <strong>Note:</strong>
      {e(DEVOTION.get('section', {}).get('disclaimer', ''))}
    </aside>
    <p class="devotion-actions">
      <a class="btn btn-ghost" href="{prefix}devotion/{e(item['type'])}.html">More {e(dtype.get('name', 'texts'))}</a>
      <a class="btn btn-ghost" href="{prefix}deities/{e(item['deity'])}.html">{e(deity.get('name', 'Deity'))} temples</a>
    </p>
    {dev_feedback}
  </article>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(
        page_title,
        desc,
        prefix,
        lang="hi" if hindi_first else "en",
        canonical_path=abs_path,
        default_lang="hi" if hindi_first else "en",
        og_type="article",
    ) + body


def build_deity_page(fam: str, temples: list) -> str:
    prefix = "../"
    meta = DEITIES[fam]
    members = sorted(
        [t for t in temples if fam in (t.get("deityFamilies") or [])],
        key=lambda t: t["name"],
    )
    rows = [
        temple_row(t, f"{prefix}temples/{t['slug']}.html", prefix, "Open guide →")
        for t in members
    ]
    dev_items = [i for i in devotion_items() if i.get("deity") == fam]
    dev_block = ""
    if dev_items:
        links = "".join(
            f'<a class="tag" href="{prefix}devotion/{e(i["slug"])}.html">{e(i["titleHi"])}</a>'
            for i in dev_items
        )
        dev_block = f"""
        <section class="section">
          <div class="section-head">
            <p class="section-kicker">भक्ति पाठ</p>
            <h2 class="section-title">Aarti · Chalisa · Vrat Katha</h2>
            <p class="section-desc">Recite at home or after darshan — <a href="{prefix}devotion/deity-{e(fam)}.html">all {e(meta['name'])} devotion texts</a>.</p>
          </div>
          <div class="temple-tags" style="justify-content:flex-start;flex-wrap:wrap;gap:0.5rem">{links}</div>
        </section>
        """
    body = f"""
{nav('deities', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}deities/index.html">Deities</a> · {e(meta['name'])}</p>
  <p class="section-kicker" style="margin-bottom:0.5rem">{e(meta.get('sanskrit', ''))}</p>
  <h1>{e(meta['nameHi'])} · {e(meta['name'])} — {len(members)} guides</h1>
  <p class="lede">{e(meta['lede'])}</p>
</section>
{dev_block}
<section class="section">
  <div class="temple-list">{''.join(rows)}</div>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(
        f"{meta['name']} Temples — TirthaYatra",
        meta["blurb"],
        prefix,
    ) + body


def state_tiles_home(temples: list, limit: int = 8) -> list[str]:
    india = [t for t in temples if t.get("country", "India") == "India" and t.get("state")]
    by_state: dict[str, int] = {}
    for t in india:
        by_state[t["state"]] = by_state.get(t["state"], 0) + 1
    top = sorted(by_state.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]
    tiles = []
    for state, count in top:
        portal = STATE_PORTALS.get(state, {})
        blurb = portal.get("portalName", "State temple guides")
        tiles.append(
            f"""
            <a class="circuit-tile reveal" href="states/{e(state_slug(state))}.html">
              <p class="circuit-count">{count} temples</p>
              <h3 class="circuit-name">{e(state)}</h3>
              <p class="circuit-blurb">{e(blurb)}</p>
              <span class="circuit-arrow">Open state →</span>
            </a>
            """
        )
    return tiles


def state_portal_html(t: dict, prefix: str) -> str:
    portal = t.get("statePortal") or STATE_PORTALS.get(t.get("state", ""), {})
    if not portal:
        return ""
    name = portal.get("name") or portal.get("portalName", "State portal")
    url = safe_url(portal.get("url") or portal.get("portalUrl"))
    if not url:
        return ""
    st = t.get("state", "")
    browse = (
        f'<p style="margin-top:0.75rem"><a class="tag" href="{prefix}states/{e(state_slug(st))}.html">More temples in {e(st)}</a></p>'
        if st
        else ""
    )
    return f"""
    <p class="official-link" style="display:block;margin-top:0.75rem">
      State / board reference:
      <a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(name)} ↗</a>
    </p>
    {browse}
    """


def build_states_index(temples: list) -> str:
    prefix = "../"
    india = [t for t in temples if t.get("country", "India") == "India" and t.get("state")]
    by_state: dict[str, list] = {}
    for t in india:
        by_state.setdefault(t["state"], []).append(t)
    tiles = []
    for state in sorted(by_state, key=lambda s: (-len(by_state[s]), s)):
        portal = STATE_PORTALS.get(state, {})
        portal_line = ""
        if portal:
            portal_line = f'<p class="circuit-blurb">Official ref: {e(portal.get("portalName", ""))}</p>'
        tiles.append(
            f"""
            <a class="circuit-tile reveal" href="{e(state_slug(state))}.html">
              <p class="circuit-count">{len(by_state[state])} temples on TirthaYatra</p>
              <h3 class="circuit-name">{e(state)}</h3>
              {portal_line}
              <span class="circuit-arrow">Browse state →</span>
            </a>
            """
        )
    body = f"""
{nav('states', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · States</p>
  <h1>Temples by State</h1>
  <p class="lede">Browse Indian temples state-wise. Each state page links to official government / Devasthan / HRCE portals for verification.</p>
</section>
<section class="section">
  <div class="circuit-grid">{''.join(tiles)}</div>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head("Temples by State — TirthaYatra", "Browse Indian temples grouped by state with official portal references.", prefix) + body


def build_state_page(state: str, temples: list) -> str:
    prefix = "../"
    members = sorted(
        [t for t in temples if t.get("state") == state and t.get("country", "India") == "India"],
        key=lambda t: t["name"],
    )
    portal = STATE_PORTALS.get(state, {})
    portal_block = ""
    portal_url = safe_url(portal.get("portalUrl")) if portal else ""
    if portal and portal_url:
        also = "".join(
            f'<li><a href="{e(u)}" target="_blank" rel="noopener noreferrer">{e(a["name"])} ↗</a></li>'
            for a in portal.get("also", [])
            if (u := safe_url(a.get("url")))
        )
        also_html = f"<ul>{also}</ul>" if also else ""
        portal_block = f"""
        <section class="official-refs" aria-label="Official portals">
          <div class="section-head">
            <p class="section-kicker">Verify before you travel</p>
            <h2 class="section-title">Official sites &amp; tourism links</h2>
            <p class="section-desc">Use these government / trust portals for current darshan rules, tickets, and notices.</p>
          </div>
          <div class="fact-grid">
            <div class="fact">
              <dt>Official state / board portal</dt>
              <dd><a href="{e(portal_url)}" target="_blank" rel="noopener noreferrer">{e(portal['portalName'])} ↗</a></dd>
            </div>
            <div class="fact">
              <dt>Note</dt>
              <dd>{e(portal.get('note', 'Verify darshan details on official channels.'))}</dd>
            </div>
          </div>
          {also_html}
        </section>
        """
    rows = [
        temple_row(t, f"{prefix}temples/{t['slug']}.html", prefix, "Open guide →")
        for t in members
    ]
    body = f"""
{nav('states', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}states/index.html">States</a> · {e(state)}</p>
  <h1>{e(state)} - {len(members)} guides</h1>
</section>
<section class="section">
  <div class="temple-list">{''.join(rows)}</div>
</section>
<section class="section section-band">
  {portal_block if portal_block else '<p class="section-desc">Official portal links will appear here when available for this state.</p>'}
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(f"{state} Temples — TirthaYatra", f"Temple pilgrimage guides in {state}", prefix) + body


def _temple_by_slug(temples: list, slug: str) -> dict | None:
    for t in temples:
        if t.get("slug") == slug:
            return t
    return None


def _festival_dates(fest: dict, festivals_data: dict) -> list[dict]:
    names = set(fest.get("dateNames") or [])
    out = []
    for row in festivals_data.get("fixed") or []:
        if row.get("name") in names:
            out.append(row)
    out.sort(key=lambda r: r.get("date", ""), reverse=True)
    return out


def build_festivals_index(festivals_data: dict) -> str:
    prefix = "../"
    sec = FESTIVAL_GUIDE.get("section", {})
    cards = []
    for fest in FESTIVAL_GUIDE.get("festivals", []):
        dates = _festival_dates(fest, festivals_data)
        next_date = dates[0]["date"] if dates else "—"
        cards.append(
            f"""
            <a class="circuit-tile reveal" href="{prefix}festivals/{e(fest['slug'])}.html">
              <p class="circuit-count">Next listed · {e(next_date)}</p>
              <h3 class="circuit-name">{e(fest.get('nameHi', ''))}</h3>
              <p class="circuit-blurb"><strong>{e(fest['name'])}</strong> — {e(fest.get('summary', ''))}</p>
              <span class="circuit-arrow">Open guide →</span>
            </a>
            """
        )
    body = f"""
{nav('festivals', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · Festivals</p>
  <h1>{e(sec.get('nameHi', 'त्योहार'))} · {e(sec.get('name', 'Festivals'))}</h1>
  <p class="lede">{e(sec.get('lede', ''))}</p>
  <p><a class="btn btn-primary" href="{prefix}festivals/calendar.html">Month calendar · next 30 days</a></p>
</section>
<section class="section">
  <div class="circuit-grid">{''.join(cards)}</div>
  <aside class="belief-disclaimer" style="margin-top:2rem">
    <strong>Note:</strong> {e(sec.get('disclaimer', ''))}
  </aside>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(
        "Festival Guides — TirthaYatra",
        sec.get("lede", "Hindu festivals for home and diaspora"),
        prefix,
    ) + body


def build_festival_detail(fest: dict, festivals_data: dict, temples: list) -> str:
    import build_engage

    prefix = "../"
    fest_save = build_engage.save_btn(
        "festival",
        fest["slug"],
        fest["name"],
        f"{prefix}festivals/{fest['slug']}.html",
    )
    fest_feedback = build_engage.feedback_section_html("festival")
    dates = _festival_dates(fest, festivals_data)
    date_rows = "".join(
        f"<li><strong>{e(r['date'])}</strong> — {e(r.get('nameHi') or r['name'])}</li>"
        for r in dates[:6]
    )
    how_en = "".join(f"<li>{e(x)}</li>" for x in fest.get("howCelebratedEn") or [])
    how_hi = "".join(f"<li>{e(x)}</li>" for x in fest.get("howCelebratedHi") or [])
    regions = "".join(
        f"<li><strong>{e(r['region'])}:</strong> {e(r['notes'])}</li>"
        for r in fest.get("regions") or []
    )
    deity_cards = []
    for ds in fest.get("deityStories") or []:
        deity_cards.append(
            f"""
            <article class="festival-deity-card">
              <h3>{e(ds.get('deityHi', ''))} · {e(ds.get('deity', ''))}</h3>
              <p>{e(ds.get('en', ''))}</p>
              <p class="trail-story-hi">{e(ds.get('hi', ''))}</p>
            </article>
            """
        )
    deity_block = (
        '<h2 class="section-title">Devi–Devata stories · देवी–देवता कथा</h2>'
        f'<div class="festival-deity-grid">{"".join(deity_cards)}</div>'
        if deity_cards
        else ""
    )
    devotion_links = []
    for slug in fest.get("relatedDevotion") or []:
        item = next((i for i in devotion_items() if i.get("slug") == slug), None)
        label = (item.get("titleHi") or item.get("title") or slug) if item else slug
        devotion_links.append(
            f'<a class="tag" href="{prefix}devotion/{e(slug)}.html">{e(label)}</a>'
        )
    temple_links = []
    for slug in fest.get("relatedTemples") or []:
        t = _temple_by_slug(temples, slug)
        if not t:
            continue
        temple_links.append(
            f'<a class="tag" href="{prefix}temples/{e(slug)}.html">{e(t["name"])}</a>'
        )
    devotion_block = (
        '<h2 class="section-title">Related aarti &amp; katha</h2>'
        f'<p class="devotion-related">{"".join(devotion_links)}</p>'
        if devotion_links
        else ""
    )
    temple_block = (
        '<h2 class="section-title">Related temples</h2>'
        f'<p class="devotion-related">{"".join(temple_links)}</p>'
        if temple_links
        else ""
    )
    hindi_first = fest["slug"] in {
        "shravan-sawan",
        "kanwar-yatra",
        "nag-panchami",
        "maha-shivaratri",
        "raksha-bandhan",
        "hartalika-teej",
        "karva-chauth",
        "chhath",
        "navaratri",
        "diwali",
        "janmashtami",
    }
    abs_path = f"festivals/{fest['slug']}.html"
    name_hi = fest.get("nameHi") or fest["name"]
    page_title = (
        f"{name_hi} | {fest['name']} — TirthaYatra"
        if name_hi != fest["name"]
        else f"{fest['name']} — TirthaYatra"
    )
    share = build_engage.share_bar(
        title=page_title,
        text=f"{name_hi} — TirthaYatra festival guide",
        url=abs_path,
        kind="festival",
    )
    # Hindi-first paired blocks
    story_block = ""
    if fest.get("storyEn") or fest.get("storyHi"):
        story_block = f"""
  <h2 class="section-title">कथा · The story</h2>
  {build_engage.lang_p(fest.get('storyEn', ''), fest.get('storyHi', ''))}
"""
    myth_block = ""
    if fest.get("mythologyEn") or fest.get("mythologyHi"):
        myth_block = f"""
  <h2 class="section-title">पौराणिक महत्व · Mythological significance</h2>
  {build_engage.lang_p(fest.get('mythologyEn', ''), fest.get('mythologyHi', ''))}
"""
    body = f"""
{nav('festivals', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}festivals/index.html">Festivals</a> · {e(name_hi)}</p>
  <div class="page-tools">{build_engage.lang_toggle()}</div>
  <h1 class="lang-hi">{e(name_hi)}</h1>
  <h1 class="lang-en">{e(fest['name'])}</h1>
  {build_engage.lang_p(fest.get('summary', ''), fest.get('summaryHi', ''), cls='lede')}
  <p>{fest_save}</p>
  {share}
  <p><a class="btn btn-ghost" href="{prefix}festivals/calendar.html">Open festival calendar</a></p>
</section>
<section class="section festival-section" data-board-open="festival" data-slug="{e(fest['slug'])}">
  <h2 class="section-title">Listed dates</h2>
  <ul class="festival-date-list">{date_rows or '<li>See panchang / local temple calendar</li>'}</ul>
  <h2 class="section-title">अर्थ · Meaning</h2>
  {build_engage.lang_p(fest.get('meaningEn', ''), fest.get('meaningHi', ''))}
  {story_block}
  {myth_block}
  {deity_block}
  <h2 class="section-title">कैसे मनाएँ · How it is celebrated</h2>
  <div class="festival-cols">
    <ul class="lang-en">{how_en}</ul>
    <ul class="lang-hi">{how_hi}</ul>
  </div>
  <h2 class="section-title">प्रवासी समुदाय · For the diaspora</h2>
  {build_engage.lang_p(fest.get('diasporaEn', ''), fest.get('diasporaHi', ''))}
  <ul class="festival-regions">{regions}</ul>
  {devotion_block}
  {temple_block}
  <aside class="belief-disclaimer" style="margin-top:2rem">
    <strong>Note:</strong> {e(FESTIVAL_GUIDE.get('section', {}).get('disclaimer', ''))}
  </aside>
  {fest_feedback}
  <p style="margin-top:1.5rem">
    <a class="btn btn-ghost" href="{prefix}festivals/index.html">All festivals</a>
  </p>
</section>
{footer(prefix)}
</body>
</html>
"""
    desc = fest.get("summaryHi") if hindi_first else fest.get("summary")
    desc = desc or fest.get("summary") or fest["name"]
    return head(
        page_title,
        desc,
        prefix,
        lang="hi" if hindi_first else "en",
        canonical_path=abs_path,
        default_lang="hi" if hindi_first else "en",
        og_type="article",
    ) + body


def sitemap_loc(path: str) -> str:
    """Absolute URL for a site-relative path (no leading slash required)."""
    path = path.lstrip("/")
    if not path or path == "index.html":
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{path}"


def write_today_bar_data() -> None:
    """JSON consumed by js/today-bar.js (survives Vercel data/ prune)."""
    labels: dict[str, str] = {}
    for item in devotion_items():
        labels[item["slug"]] = item.get("titleHi") or item.get("title") or item["slug"]
    for story in STORIES.get("stories") or []:
        labels[story["slug"]] = story.get("titleHi") or story.get("title") or story["slug"]
    payload = {
        "rotation": ENGAGEMENT.get("dailyRotation") or {},
        "labels": labels,
    }
    out = ROOT / "js" / "today-bar-data.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sitemap_url_entry(
    path: str,
    *,
    lastmod: str,
    changefreq: str = "weekly",
    priority: str = "0.5",
    images: list[dict] | None = None,
) -> str:
    parts = [
        "  <url>",
        f"    <loc>{e(sitemap_loc(path))}</loc>",
        f"    <lastmod>{lastmod}</lastmod>",
        f"    <changefreq>{changefreq}</changefreq>",
        f"    <priority>{priority}</priority>",
    ]
    for img in images or []:
        loc = img.get("loc") or ""
        if not loc:
            continue
        parts.append("    <image:image>")
        parts.append(f"      <image:loc>{e(loc)}</image:loc>")
        if img.get("title"):
            parts.append(f"      <image:title>{e(img['title'])}</image:title>")
        if img.get("caption"):
            parts.append(f"      <image:caption>{e(img['caption'])}</image:caption>")
        parts.append("    </image:image>")
    parts.append("  </url>")
    return "\n".join(parts)


def _write_urlset(path: Path, entries: list[str], *, with_images: bool = False) -> None:
    ns = 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
    if with_images:
        ns += '\n        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<urlset {ns}>\n"
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(xml, encoding="utf-8")


def write_sitemap(
    temples: list,
    circuits: list,
    states: list[str],
    *,
    lastmod: str | None = None,
) -> int:
    """Write sitemap index + per-section sitemaps for every public HTML page.

    Returns total URL count across child sitemaps (home counted once).
    """
    from datetime import date

    lastmod = lastmod or date.today().isoformat()
    out_dir = ROOT / "sitemaps"

    # Clear previous child sitemaps so renamed files do not linger.
    if out_dir.exists():
        for old in out_dir.glob("sitemap-*.xml"):
            old.unlink()

    groups: dict[str, list[tuple]] = {
        "core": [],
        "temples": [],
        "devotion": [],
        "festivals": [],
        "stories": [],
        "states": [],
        "circuits": [],
        "deities": [],
        "pages": [],
        "images": [],
    }
    # entry shape: (path, changefreq, priority, lastmod_override|None, images|None)

    def add(
        group: str,
        path: str,
        changefreq: str = "weekly",
        priority: str = "0.5",
        *,
        item_lastmod: str | None = None,
        images: list[dict] | None = None,
    ) -> None:
        groups[group].append((path, changefreq, priority, item_lastmod, images))

    # —— Core hubs ——
    add("core", "index.html", "daily", "1.0")
    add("core", "temples/index.html", "weekly", "0.9")
    add("core", "circuits/index.html", "weekly", "0.8")
    add("core", "deities/index.html", "weekly", "0.8")
    add("core", "states/index.html", "weekly", "0.7")
    add("core", "devotion/index.html", "weekly", "0.8")
    add("core", "devotion/aarti.html", "weekly", "0.8")
    add("core", "devotion/chalisa.html", "weekly", "0.8")
    add("core", "devotion/vrat-katha.html", "weekly", "0.8")
    add("core", "devotion/daily.html", "daily", "0.85")
    add("core", "festivals/index.html", "weekly", "0.8")
    add("core", "festivals/calendar.html", "daily", "0.85")
    add("core", "stories/index.html", "weekly", "0.8")
    add("core", "my-board.html", "monthly", "0.5")

    # —— Individual temples (+ image sitemap entries where licensed photos exist) ——
    for t in temples:
        slug = t["slug"]
        path = f"temples/{slug}.html"
        t_last = t.get("lastUpdated") or lastmod
        add("temples", path, "monthly", "0.7", item_lastmod=t_last)
        media = MEDIA.get(slug) or {}
        local = media.get("local")
        if local and (ROOT / local).exists():
            title = t.get("name") or slug
            caption = t.get("famousFor") or t.get("summary") or title
            add(
                "images",
                path,
                "monthly",
                "0.6",
                item_lastmod=t_last,
                images=[
                    {
                        "loc": sitemap_loc(local),
                        "title": title,
                        "caption": caption[:200],
                    }
                ],
            )

    # —— Devotion items (aarti / chalisa / vrat katha) ——
    for item in devotion_items():
        add("devotion", f"devotion/{item['slug']}.html", "monthly", "0.65")

    for fam in DEITIES:
        if (OUT_DEVOTION / f"deity-{fam}.html").exists() or any(
            i.get("deity") == fam for i in devotion_items()
        ):
            add("devotion", f"devotion/deity-{fam}.html", "monthly", "0.6")

    # —— Festivals ——
    for fest in FESTIVAL_GUIDE.get("festivals", []):
        add("festivals", f"festivals/{fest['slug']}.html", "monthly", "0.75")

    # —— Stories ——
    for story in STORIES.get("stories", []):
        add("stories", f"stories/{story['slug']}.html", "monthly", "0.7")

    # —— States ——
    for state in states:
        add("states", f"states/{state_slug(state)}.html", "monthly", "0.6")

    # —— Circuits ——
    for c in circuits:
        add("circuits", f"circuits/{c['slug']}.html", "monthly", "0.7")

    # —— Deity hubs (every deity page that exists / is defined) ——
    for fam in DEITIES:
        add("deities", f"deities/{fam}.html", "monthly", "0.7")

    # —— Legal / about ——
    for slug in ("about", "contact", "feedback", "privacy", "disclaimer", "terms"):
        add("pages", f"pages/{slug}.html", "yearly", "0.3")

    # Safety net: any public HTML on disk not already listed
    known: set[str] = set()
    for g_entries in groups.values():
        for path, *_rest in g_entries:
            known.add(path)
    public_dirs = (
        OUT_TEMPLES,
        OUT_CIRCUITS,
        OUT_DEITIES,
        OUT_STATES,
        OUT_DEVOTION,
        OUT_FESTIVALS,
        OUT_STORIES,
        OUT_PAGES,
    )
    orphan_group = {
        "temples": "temples",
        "circuits": "circuits",
        "deities": "deities",
        "states": "states",
        "devotion": "devotion",
        "festivals": "festivals",
        "stories": "stories",
        "pages": "pages",
    }
    for folder in public_dirs:
        if not folder.exists():
            continue
        for html_path in sorted(folder.glob("*.html")):
            rel = f"{folder.name}/{html_path.name}"
            if rel in known or html_path.name == "index.html":
                continue
            # Skip known duplicates / redirects not in index
            if folder.name == "temples" and not (DATA / "temples" / f"{html_path.stem}.json").exists():
                continue
            g = orphan_group.get(folder.name, "pages")
            add(g, rel, "monthly", "0.5")
            known.add(rel)

    # Write child sitemaps
    child_files: list[tuple[str, int]] = []
    total_urls = 0
    for name, entries_raw in groups.items():
        if not entries_raw:
            continue
        seen: set[str] = set()
        entries: list[str] = []
        with_images = name == "images"
        for path, changefreq, priority, item_lastmod, images in entries_raw:
            # Images sitemap may repeat temple paths; allow one entry per path there
            key = path if not with_images else f"img:{path}"
            if key in seen:
                continue
            seen.add(key)
            entries.append(
                _sitemap_url_entry(
                    path,
                    lastmod=item_lastmod or lastmod,
                    changefreq=changefreq,
                    priority=priority,
                    images=images,
                )
            )
        if not entries:
            continue
        fname = f"sitemap-{name}.xml"
        _write_urlset(out_dir / fname, entries, with_images=with_images)
        child_files.append((fname, len(entries)))
        total_urls += len(entries)

    # sitemap.xml = index
    index_body = "\n".join(
        "  <sitemap>\n"
        f"    <loc>{e(sitemap_loc(f'sitemaps/{fname}'))}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        "  </sitemap>"
        for fname, _n in child_files
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{index_body}\n"
        "</sitemapindex>\n",
        encoding="utf-8",
    )

    # Also keep a flat combined urlset for tools that expect a single urlset at /sitemap-all.xml
    combined: list[str] = []
    seen_all: set[str] = set()
    for name in (
        "core",
        "temples",
        "devotion",
        "festivals",
        "stories",
        "states",
        "circuits",
        "deities",
        "pages",
    ):
        for path, changefreq, priority, item_lastmod, _images in groups[name]:
            if path in seen_all:
                continue
            seen_all.add(path)
            combined.append(
                _sitemap_url_entry(
                    path,
                    lastmod=item_lastmod or lastmod,
                    changefreq=changefreq,
                    priority=priority,
                )
            )
    _write_urlset(ROOT / "sitemap-all.xml", combined, with_images=False)

    robots_lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {SITE_URL}/sitemap.xml",
        f"Sitemap: {SITE_URL}/sitemap-all.xml",
    ]
    for fname, _n in child_files:
        robots_lines.append(f"Sitemap: {SITE_URL}/sitemaps/{fname}")
    robots_lines.append("")
    (ROOT / "robots.txt").write_text("\n".join(robots_lines), encoding="utf-8")

    print(
        "Sitemaps: "
        + ", ".join(f"{fname} ({n})" for fname, n in child_files)
        + f"; combined {len(combined)}"
    )
    return len(combined)


def build_legal(slug: str, title: str, blocks: list) -> str:
    prefix = "../"
    parts = [f"<h1>{e(title)}</h1>"]
    for h, paras in blocks:
        parts.append(f"<h2>{e(h)}</h2>")
        for p in paras:
            parts.append(f"<p>{p}</p>")
    body = f"""
{nav('about' if slug == 'about' else '', prefix)}
<main class="prose">
{''.join(parts)}
</main>
{footer(prefix)}
</body>
</html>
"""
    return head(f"{title} — TirthaYatra", title, prefix) + body


def main() -> None:
    import build_engage

    global MEDIA, GROUPS, STATE_PORTALS, DEITIES, DEVOTION, FESTIVAL_GUIDE, STORIES, ENGAGEMENT
    OUT_TEMPLES.mkdir(parents=True, exist_ok=True)
    OUT_CIRCUITS.mkdir(parents=True, exist_ok=True)
    OUT_PAGES.mkdir(parents=True, exist_ok=True)
    OUT_STATES.mkdir(parents=True, exist_ok=True)
    OUT_DEITIES.mkdir(parents=True, exist_ok=True)
    OUT_DEVOTION.mkdir(parents=True, exist_ok=True)
    OUT_FESTIVALS.mkdir(parents=True, exist_ok=True)
    OUT_STORIES.mkdir(parents=True, exist_ok=True)

    media_path = DATA / "media.json"
    MEDIA = load_json(media_path) if media_path.exists() else {}
    groups_path = DATA / "groups.json"
    GROUPS = load_json(groups_path) if groups_path.exists() else {}
    portals_path = DATA / "state-portals.json"
    STATE_PORTALS = load_json(portals_path) if portals_path.exists() else {}
    deities_path = DATA / "deities.json"
    DEITIES = load_json(deities_path) if deities_path.exists() else {}
    devotion_path = DATA / "devotion.json"
    DEVOTION = load_json(devotion_path) if devotion_path.exists() else {}
    fest_guide_path = DATA / "festival-guide.json"
    FESTIVAL_GUIDE = load_json(fest_guide_path) if fest_guide_path.exists() else {}
    stories_path = DATA / "stories.json"
    STORIES = load_json(stories_path) if stories_path.exists() else {}
    engage_path = DATA / "engagement.json"
    ENGAGEMENT = load_json(engage_path) if engage_path.exists() else {}
    festivals_dates = (
        load_json(DATA / "festivals.json") if (DATA / "festivals.json").exists() else {}
    )

    circuits = load_json(DATA / "circuits.json")
    index = load_json(DATA / "temples.json")
    validate_fixed_groups(index)
    circuits_by_slug = {c["slug"]: c for c in circuits}

    detailed = []
    for meta in index:
        path = DATA / "temples" / f"{meta['slug']}.json"
        if not path.exists():
            raise SystemExit(f"Missing detail file: {path}")
        detail = load_json(path)
        detail.setdefault("tier", meta.get("tier", ""))
        detail.setdefault("country", meta.get("country", "India"))
        detailed.append(detail)

    # Lightweight search index for client-side temple + devotion search
    search_index = [
        {
            "slug": t["slug"],
            "name": t["name"],
            "location": t.get("location", ""),
            "state": t.get("state", ""),
            "country": t.get("country", "India"),
            "famousFor": t.get("famousFor", ""),
            "tags": t.get("tagLabels", []),
            "deities": [
                DEITIES[f]["name"]
                for f in t.get("deityFamilies", [])
                if f in DEITIES
            ],
            "href": f"temples/{t['slug']}.html",
        }
        for t in index
    ]
    for item in devotion_items():
        deity = DEITIES.get(item.get("deity", {}), {})
        dtype = DEVOTION.get("types", {}).get(item.get("type", ""), {})
        search_index.append(
            {
                "slug": item["slug"],
                "name": f"{item.get('titleHi', '')} {item.get('title', '')}".strip(),
                "location": "",
                "state": "",
                "country": "India",
                "famousFor": item.get("summary", ""),
                "tags": [dtype.get("name", ""), deity.get("name", "")],
                "deities": [deity.get("name", "")] if deity else [],
                "href": f"devotion/{item['slug']}.html",
            }
        )
    (DATA / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8"
    )

    (ROOT / "index.html").write_text(build_home(circuits, index), encoding="utf-8")
    (OUT_TEMPLES / "index.html").write_text(build_temple_index(index), encoding="utf-8")
    (OUT_CIRCUITS / "index.html").write_text(
        build_circuit_index(circuits, index), encoding="utf-8"
    )
    (OUT_STATES / "index.html").write_text(build_states_index(index), encoding="utf-8")
    (OUT_DEITIES / "index.html").write_text(build_deities_index(index), encoding="utf-8")

    if DEVOTION:
        (OUT_DEVOTION / "index.html").write_text(build_devotion_index(), encoding="utf-8")
        for type_key in DEVOTION.get("types", {}):
            (OUT_DEVOTION / f"{type_key}.html").write_text(
                build_devotion_type_page(type_key), encoding="utf-8"
            )
        for fam in DEITIES:
            if any(i.get("deity") == fam for i in devotion_items()):
                (OUT_DEVOTION / f"deity-{fam}.html").write_text(
                    build_devotion_deity_page(fam), encoding="utf-8"
                )
        for item in devotion_items():
            (OUT_DEVOTION / f"{item['slug']}.html").write_text(
                build_devotion_item(item), encoding="utf-8"
            )

    for c in circuits:
        (OUT_CIRCUITS / f"{c['slug']}.html").write_text(
            build_circuit(c, index), encoding="utf-8"
        )

    india_states = sorted(
        {
            t["state"]
            for t in index
            if t.get("country", "India") == "India" and t.get("state")
        }
    )
    for state in india_states:
        (OUT_STATES / f"{state_slug(state)}.html").write_text(
            build_state_page(state, index), encoding="utf-8"
        )

    for fam in DEITIES:
        members = [t for t in index if fam in (t.get("deityFamilies") or [])]
        if members:
            (OUT_DEITIES / f"{fam}.html").write_text(
                build_deity_page(fam, index), encoding="utf-8"
            )

    for t in detailed:
        (OUT_TEMPLES / f"{t['slug']}.html").write_text(
            build_temple(t, index, circuits_by_slug), encoding="utf-8"
        )

    if FESTIVAL_GUIDE.get("festivals"):
        (OUT_FESTIVALS / "index.html").write_text(
            build_festivals_index(festivals_dates), encoding="utf-8"
        )
        (OUT_FESTIVALS / "calendar.html").write_text(
            build_engage.build_festivals_calendar(
                FESTIVAL_GUIDE, ASSET_VER, nav, footer, head
            ),
            encoding="utf-8",
        )
        for fest in FESTIVAL_GUIDE["festivals"]:
            (OUT_FESTIVALS / f"{fest['slug']}.html").write_text(
                build_festival_detail(fest, festivals_dates, index), encoding="utf-8"
            )

    if STORIES.get("stories"):
        (OUT_STORIES / "index.html").write_text(
            build_engage.build_stories_index(STORIES, ASSET_VER, nav, footer, head),
            encoding="utf-8",
        )
        for story in STORIES["stories"]:
            (OUT_STORIES / f"{story['slug']}.html").write_text(
                build_engage.build_story_detail(
                    story, STORIES, ASSET_VER, nav, footer, head
                ),
                encoding="utf-8",
            )

    (OUT_DEVOTION / "daily.html").write_text(
        build_engage.build_daily_practice(
            ENGAGEMENT,
            devotion_items(),
            STORIES,
            ASSET_VER,
            nav,
            footer,
            head,
        ),
        encoding="utf-8",
    )
    (ROOT / "my-board.html").write_text(
        build_engage.build_my_board(
            ENGAGEMENT,
            index,
            FESTIVAL_GUIDE,
            devotion_items(),
            STORIES,
            ASSET_VER,
            nav,
            footer,
            head,
        ),
        encoding="utf-8",
    )

    pages = {
        "about": (
            "About TirthaYatra",
            [
                (
                    "Our purpose",
                    [
                        "TirthaYatra is an independent informational site for home devotion (aarti, chalisa, vrat katha, festival stories) and temple learning across India and related sacred sites in Nepal, Sri Lanka, and the Kailash region.",
                        "We are not a booking engine or guaranteed itinerary planner. Practical temple details can change — verify on official trust or tourism channels before travel.",
                    ],
                ),
                (
                    "Images",
                    [
                        "Temple photographs are sourced from Wikimedia Commons under their stated free licenses (Public Domain / Creative Commons). Each page credits the photographer and license. We do not scrape photos from government temple portals (for example AP Temples, TN HR&CE) because those sites typically retain copyright — we link them for official details instead.",
                    ],
                ),
                (
                    "Official state portals",
                    [
                        'We reference government and Devasthan portals such as <a href="https://www.aptemples.org/en-in/home" target="_blank" rel="noopener noreferrer">AP Temples</a>, TN HR&CE, Telangana Endowments, Karnataka HRI&CE, Rajasthan Devasthan, and temple trusts. TirthaYatra remains independent and unaffiliated.',
                    ],
                ),
                (
                    "Editorial standards",
                    [
                        "We aim for respectful, non-sectarian language. Practical details can change — always reconfirm on official websites before travel. TirthaYatra is not affiliated with any temple trust.",
                    ],
                ),
            ],
        ),
        "contact": (
            "Contact",
            [
                (
                    "Reach us",
                    [
                        'For corrections, image credit updates, or to suggest a temple: <a href="mailto:TirthaYatraOnline@gmail.com">TirthaYatraOnline@gmail.com</a>.',
                        'Prefer a guided form? Use <a href="../pages/feedback.html">Feedback</a> or the Feedback button on any page.',
                    ],
                ),
            ],
        ),
        "feedback": (
            "Feedback &amp; content tips",
            [
                (
                    "Help improve TirthaYatra",
                    [
                        "Use the <strong>Feedback</strong> button (bottom-right on every page) to suggest a correction, add a detail, highlight something useful, ask a question, or share appreciation.",
                        "Choose a type, write a clear note, then <strong>Email to TirthaYatra</strong> so editors can review it. You may also save a personal copy on this device.",
                        "Feedback is for editorial review and is <strong>not published live automatically</strong>. That protects readers from spam and keeps us aligned with advertising and copyright policies.",
                    ],
                ),
                (
                    "What helps most",
                    [
                        "Name the page section (e.g. “Darshan timings”, “Diwali story”).",
                        "For corrections: what is wrong, and what should it say (with a source if you have one).",
                        "For home-puja tips: keep them respectful, non-commercial, and free of hate.",
                    ],
                ),
                (
                    "Direct email",
                    [
                        'You can also write <a href="mailto:TirthaYatraOnline@gmail.com">TirthaYatraOnline@gmail.com</a>.',
                    ],
                ),
            ],
        ),
        "privacy": (
            "Privacy Policy",
            [
                (
                    "Information we collect",
                    [
                        "TirthaYatra is primarily a static informational website for home devotion and temple learning.",
                        "Optional My Board saves, checklists, practice marks, and personal copies of feedback notes may be stored locally in your browser (localStorage) and are not uploaded automatically.",
                        "When you choose <strong>Email to TirthaYatra</strong>, your feedback opens in your email app and is sent to us only if you send that message. We use emailed feedback for editorial review and corrections.",
                        "We use Vercel Web Analytics for aggregated page-view statistics (privacy-friendly, cookieless where supported by the platform).",
                        "Embedded Google Maps and YouTube players may set cookies or similar technologies according to Google’s policies.",
                    ],
                ),
                (
                    "Advertising",
                    [
                        "We do not currently show third-party ads. Before enabling Google AdSense we will update this policy, place ads according to Google’s publisher policies, and avoid ad placement that implies endorsement of rituals or temple trusts.",
                        "Visitor feedback is moderated before any public display. We do not use feedback content to build advertising profiles of religious beliefs. My Board / practice data stays on-device unless a future sync feature is clearly disclosed.",
                    ],
                ),
                (
                    "Copyright &amp; content",
                    [
                        "Short stories on TirthaYatra are original editorial retellings of traditional themes for learning — not verbatim scripture reprints.",
                        "Aarti, Chalisa, and vrat katha texts are traditional materials presented for personal study and home puja; classical authorship remains with their traditions. Wikimedia photos keep their stated licenses. Temple names and logos belong to their trusts.",
                        "Do not scrape or republish our pages as your own scripture edition. Contact us for correction requests.",
                    ],
                ),
                (
                    "Contact",
                    [
                        'Privacy questions: <a href="mailto:TirthaYatraOnline@gmail.com">TirthaYatraOnline@gmail.com</a>.',
                    ],
                ),
            ],
        ),
        "disclaimer": (
            "Disclaimer",
            [
                (
                    "Not official advice",
                    [
                        "Temple timings, dress codes, permits (especially Kailash / Mustang), and road status change frequently. Content is general information only.",
                        "Always verify on official trust, tourism, or authorised operator channels before travel.",
                    ],
                ),
                (
                    "Maps &amp; photos",
                    [
                        "Map pins are approximate. Photos are illustrative and credited to Wikimedia Commons contributors.",
                    ],
                ),
            ],
        ),
        "terms": (
            "Terms of Use",
            [
                (
                    "Acceptance",
                    [
                        "By using TirthaYatra you agree to use the content for lawful, respectful purposes.",
                    ],
                ),
                (
                    "Content &amp; images",
                    [
                        "Text is for personal learning and home puja unless noted. Short stories are original retellings; traditional hymns remain with their lineages. Wikimedia images keep their licenses; temple names and logos belong to their trusts.",
                        "You may not republish TirthaYatra pages as scripture editions, scrape content for competing commercial apps without permission, or use our marks to imply temple-trust affiliation.",
                    ],
                ),
                (
                    "User-stored notes",
                    [
                        "Optional on-device notes and My Board items are your responsibility. Do not store unlawful, hateful, or infringing material. We may remove server-side features in future versions if moderation is required for ads compliance.",
                    ],
                ),
            ],
        ),
    }

    # Creator / share kit — Reels scripts + Search Console checklist (manual steps)
    pages["creator-kit"] = (
        "Share kit · Reels & Search Console",
        [
            (
                "Why this page",
                [
                    "Short links spread TirthaYatra in family WhatsApp groups and Reels bios. Use the exact page URL (not the homepage) so visitors land on the aarti, katha, or story you showed.",
                ],
            ),
            (
                "30–45 second Reel scripts (link in bio)",
                [
                    f"<strong>Bilva leaf:</strong> “तीन दल — एक ॐ। सावन में शिव को बिल्व क्यों?” → end card → {SITE_URL}/stories/bilva-leaf-shiva.html",
                    f"<strong>Neelkanth:</strong> “हलाहल कण्ठ में — नीलकंठ कैसे बने?” → {SITE_URL}/stories/neelkanth-poison.html · temple: {SITE_URL}/temples/neelkanth-mahadev-rishikesh.html",
                    f"<strong>Lingashtakam verse 1:</strong> show text on screen, soft jal sound → {SITE_URL}/devotion/lingashtakam.html",
                    f"<strong>Sawan Somwar:</strong> “सोमवार व्रत कथा — 60 सेकंड सार” → {SITE_URL}/devotion/sawan-somwar-vrat-katha.html",
                    f"<strong>Kanwar / Bol Bam:</strong> “कांवड़ क्यों उठाते हैं?” → {SITE_URL}/festivals/kanwar-yatra.html",
                    f"<strong>Hanuman Chalisa opening:</strong> one doha on screen → {SITE_URL}/devotion/hanuman-chalisa.html",
                ],
            ),
            (
                "WhatsApp share (built into pages)",
                [
                    "On every aarti, chalisa, vrat katha, story, and festival guide, use <strong>WhatsApp</strong> / <strong>Copy link</strong> under the title. Prefers Hindi titles for Sawan and Chalisa pages so family chats feel native.",
                ],
            ),
            (
                "Google Search Console (do this once per property)",
                [
                    "Add property for https://www.tirthayatraonline.in (Domain or URL-prefix).",
                    "Sitemaps → submit <code>https://www.tirthayatraonline.in/sitemap.xml</code> (index of temples, devotion, festivals, stories, images).",
                    "Optional: also submit <code>/sitemap-all.xml</code> if the index is slow to expand.",
                    "Coverage → fix 404s / redirected URLs; watch queries like <em>सावन सोमवार व्रत कथा</em>, <em>कांवड़ यात्रा</em>, <em>लिंगाष्टकम्</em>, <em>[temple] aarti</em>.",
                    "After big content releases (Sawan pack), request indexing on 5–10 hero URLs from the URL Inspection tool.",
                ],
            ),
            (
                "Language tip",
                [
                    "Use the <strong>हिंदी | EN</strong> toggle on guides and stories. Sawan, Kanwar, Chalisa, and Shiva pages default Hindi-first for first-time visitors from Hindi search.",
                ],
            ),
        ],
    )

    for slug, (title, blocks) in pages.items():
        (OUT_PAGES / f"{slug}.html").write_text(
            build_legal(slug, title, blocks), encoding="utf-8"
        )

    write_today_bar_data()
    n_urls = write_sitemap(index, circuits, india_states)
    print(
        f"Built {len(detailed)} temples, {len(circuits)} circuits, "
        f"{len(MEDIA)} images wired, {n_urls} sitemap URLs."
    )
    prune_deploy_artifacts()


def prune_deploy_artifacts() -> None:
    """On Vercel, drop build-only sources from the published static root."""
    if os.environ.get("VERCEL") != "1":
        return
    keep_data = {"search-index.json", "festivals.json"}
    data_dir = DATA
    if data_dir.is_dir():
        for path in data_dir.iterdir():
            if path.is_file() and path.name not in keep_data:
                path.unlink(missing_ok=True)
            elif path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
    for name in ("build.py", "scripts", "README.md", ".git"):
        target = ROOT / name
        if target.is_file():
            target.unlink(missing_ok=True)
        elif target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
    print("Pruned build-only artifacts from Vercel output.")


if __name__ == "__main__":
    main()
