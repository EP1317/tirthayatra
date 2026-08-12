"""Engagement pages: calendar, stories, daily practice, my board, home bands."""

from __future__ import annotations

import html
import json
import urllib.parse
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def e(text) -> str:
    return html.escape("" if text is None else str(text), quote=True)


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def guide_name_map(festival_guide: dict) -> dict[str, str]:
    """Map festivals.json fixed[].name -> festival-guide slug."""
    out: dict[str, str] = {}
    for fest in festival_guide.get("festivals") or []:
        for name in fest.get("dateNames") or []:
            out[name] = fest["slug"]
    return out


def feedback_section_html(kind: str = "page") -> str:
    """Inline feedback CTA — opens site-wide panel; local copies listed on-device."""
    return f"""
    <section class="temple-section feedback-inline" id="feedback" data-feedback-inline data-kind="{e(kind)}">
      <h2>Feedback · सुधार</h2>
      <p>Help us validate this page: suggest a <strong>correction</strong>, <strong>add a detail</strong>, or <strong>highlight</strong> something useful for home puja readers.</p>
      <p class="comments-note">Feedback is emailed to TirthaYatra for editorial review. It is <strong>not published live automatically</strong> (safer for quality and ads policy). You can also keep a personal copy on this device.</p>
      <div class="feedback-inline-actions">
        <button type="button" class="btn btn-primary" data-feedback-open data-type="correction">Suggest a correction</button>
        <button type="button" class="btn btn-ghost" data-feedback-open data-type="add-detail">Add a detail</button>
        <button type="button" class="btn btn-ghost" data-feedback-open data-type="highlight">Highlight something</button>
        <button type="button" class="btn btn-ghost" data-feedback-open data-type="tip">Leave a tip</button>
      </div>
      <h3 class="engage-subhead">Your notes on this page</h3>
      <div data-feedback-inline-list></div>
    </section>
    """


def save_btn(type_: str, slug: str, title: str, href: str, label: str = "Save to My Board") -> str:
    return (
        f'<button type="button" class="btn btn-ghost save-btn" data-save="{e(type_)}" '
        f'data-slug="{e(slug)}" data-title="{e(title)}" data-href="{e(href)}" '
        f'data-label="{e(label)}">{e(label)}</button>'
    )


def lang_toggle() -> str:
    return (
        '<div class="lang-toggle" role="group" aria-label="Language">'
        '<button type="button" class="lang-toggle-btn" data-lang-toggle="hi">हिंदी</button>'
        '<button type="button" class="lang-toggle-btn" data-lang-toggle="en">EN</button>'
        "</div>"
    )


def share_bar(
    *,
    title: str,
    text: str,
    url: str,
    kind: str = "page",
) -> str:
    """WhatsApp-friendly share / copy strip for devotion, stories, festivals."""
    kind_hi = {
        "aarti": "आरती",
        "chalisa": "चालीसा",
        "vrat-katha": "व्रत कथा",
        "story": "कथा",
        "festival": "त्योहार",
        "page": "पेज",
    }.get(kind, "पेज")
    return f"""
<div class="share-bar" data-share data-share-title="{e(title)}" data-share-text="{e(text)}" data-share-url="{e(url)}">
  <p class="share-bar-label">Share this {e(kind_hi)} · परिवार संग बाँटें</p>
  <div class="share-bar-actions">
    <button type="button" class="btn btn-primary" data-share-action="whatsapp">WhatsApp</button>
    <button type="button" class="btn btn-ghost" data-share-action="copy">Copy link</button>
    <button type="button" class="btn btn-ghost" data-share-action="native">Share…</button>
  </div>
  <p class="share-bar-note engage-note" data-share-note hidden></p>
</div>
"""


def lang_p(en: str, hi: str, *, cls: str = "") -> str:
    """Paired EN/HI paragraphs for language preference."""
    extra = f" {cls}" if cls else ""
    parts = []
    if hi:
        parts.append(f'<p class="lang-hi{extra}">{e(hi)}</p>')
    if en:
        parts.append(f'<p class="lang-en{extra}">{e(en)}</p>')
    return "\n".join(parts)


def engagement_href(prefix: str, type_: str, slug: str) -> str:
    if type_ == "festival":
        return f"{prefix}festivals/{slug}.html"
    if type_ == "story":
        return f"{prefix}stories/{slug}.html"
    if type_ == "devotion":
        return f"{prefix}devotion/{slug}.html"
    if type_ == "temple":
        return f"{prefix}temples/{slug}.html"
    return prefix


def social_cards(items: list, prefix: str) -> str:
    cards = []
    for it in items:
        href = engagement_href(prefix, it["type"], it["slug"])
        cards.append(
            f"""
            <a class="circuit-tile reveal" href="{e(href)}">
              <p class="circuit-count">{e(it.get('label', ''))}</p>
              <h3 class="circuit-name">{e(it['slug'].replace('-', ' ').title())}</h3>
              <p class="circuit-blurb">{e(it.get('blurb', ''))}</p>
              <span class="circuit-arrow">Open →</span>
            </a>
            """
        )
    return "".join(cards)


def build_home_engage_band(
    engagement: dict, festival_guide: dict, asset_ver: str, prefix: str = ""
) -> str:
    sp = engagement.get("socialProof") or {}
    gmap = json.dumps(guide_name_map(festival_guide), ensure_ascii=False)
    return f"""
<section class="section section-band" id="home-engage" data-home-engage data-prefix="{e(prefix)}" data-guide-map="{e(gmap)}">
  <div class="section">
    <div class="section-head reveal">
      <p class="section-kicker">घर की साधना · For home devotion</p>
      <h2 class="section-title">Come back for meaning — not an itinerary</h2>
      <p class="section-desc">Festival countdowns, short stories, and daily aarti/katha for puja at home. Editorial picks — not paid ads, not fabricated rankings.</p>
    </div>
    <div class="engage-countdown reveal" data-countdown>
      <p>Loading next festival…</p>
    </div>
    <div class="engage-cta-row reveal">
      <a class="btn btn-primary" href="{prefix}devotion/daily.html">Today’s practice</a>
      <a class="btn btn-ghost" href="{prefix}festivals/calendar.html">Festival calendar</a>
      <a class="btn btn-ghost" href="{prefix}stories/index.html">Short stories</a>
      <a class="btn btn-ghost" href="{prefix}my-board.html">My Board</a>
    </div>
    <h3 class="engage-subhead">Editor picks this season</h3>
    <div class="circuit-grid">{social_cards(sp.get('mostLoved') or [], prefix)}</div>
    <h3 class="engage-subhead">Best for first-timers</h3>
    <div class="circuit-grid">{social_cards(sp.get('firstTimers') or [], prefix)}</div>
    <h3 class="engage-subhead">Family-friendly reading</h3>
    <div class="circuit-grid">{social_cards(sp.get('familyFriendly') or [], prefix)}</div>
    <p class="engage-legal">{e(sp.get('note', ''))}</p>
  </div>
</section>
<script src="{prefix}js/engage-home.js?v={e(asset_ver)}"></script>
"""


def build_festivals_calendar(festival_guide: dict, asset_ver: str, nav: Callable, footer: Callable, head: Callable) -> str:
    prefix = "../"
    gmap = guide_name_map(festival_guide)
    body = f"""
{nav('festivals', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}festivals/index.html">Festivals</a> · Calendar</p>
  <h1>त्योहार कैलेंडर · Festival calendar</h1>
  <p class="lede">Month view and the next 30 days — for home puja planning and seasonal reading. Share a plain-text card with family abroad. Dates are listed guides; confirm tithi with your panchang.</p>
</section>
<section class="section festival-calendar" data-festival-calendar data-prefix="{e(prefix)}" data-guide-map="{e(json.dumps(gmap, ensure_ascii=False))}">
  <div class="cal-toolbar">
    <button type="button" class="btn btn-ghost" data-cal-prev>← Prev</button>
    <h2 class="cal-label" data-cal-label>Month</h2>
    <button type="button" class="btn btn-ghost" data-cal-next-btn>Next →</button>
  </div>
  <div data-cal-month></div>
  <h2 class="section-title">Next 30 days</h2>
  <div class="cal-next-grid" data-cal-next></div>
  <div class="cal-share-box" data-cal-share hidden>
    <h3>Shareable card</h3>
    <p class="engage-note">Plain text you can paste into WhatsApp / email. No images copied from third parties.</p>
    <textarea rows="5" data-share-text readonly></textarea>
    <button type="button" class="btn btn-primary" data-share-copy>Copy text</button>
  </div>
  <aside class="belief-disclaimer" style="margin-top:2rem">
    <strong>Note:</strong> Informational calendar only. Regional observance can differ by a day. Not an itinerary planner.
  </aside>
  <p style="margin-top:1.5rem">
    <a class="btn btn-ghost" href="{prefix}festivals/index.html">All festival guides</a>
  </p>
</section>
{footer(prefix)}
<script src="{prefix}js/calendar.js?v={asset_ver}"></script>
</body>
</html>
"""
    return head(
        "Festival Calendar — TirthaYatra",
        "Month view and next 30 days of Hindu festivals for home puja and diaspora families.",
        prefix,
    ) + body


def build_stories_index(stories_data: dict, asset_ver: str, nav: Callable, footer: Callable, head: Callable) -> str:
    prefix = "../"
    sec = stories_data.get("section") or {}
    tiles = []
    for s in stories_data.get("stories") or []:
        tags = " · ".join(s.get("tags") or [])
        tiles.append(
            f"""
            <a class="circuit-tile reveal" href="{prefix}stories/{e(s['slug'])}.html">
              <p class="circuit-count">~{e(str(s.get('readSeconds', 70)))} sec · {e(tags)}</p>
              <h3 class="circuit-name">{e(s.get('titleHi', ''))}</h3>
              <p class="circuit-blurb"><strong>{e(s['title'])}</strong> — {e(s.get('hook', ''))}</p>
              <span class="circuit-arrow">Read story →</span>
            </a>
            """
        )
    body = f"""
{nav('stories', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · Stories</p>
  <h1>{e(sec.get('nameHi', 'कथा'))} · {e(sec.get('name', 'Short Stories'))}</h1>
  <p class="lede">{e(sec.get('lede', ''))}</p>
</section>
<section class="section">
  <div class="circuit-grid">{''.join(tiles)}</div>
  <aside class="belief-disclaimer" style="margin-top:2rem">
    <strong>Copyright &amp; learning use:</strong> {e(sec.get('disclaimer', ''))}
  </aside>
</section>
{footer(prefix)}
</body>
</html>
"""
    return head(
        "Short Stories — TirthaYatra",
        sec.get("lede", "Short myth explainers for home devotion"),
        prefix,
    ) + body


HINDI_PRIMARY_STORY_TAGS = {"sawan"}
HINDI_PRIMARY_STORY_SLUGS = {
    "bilva-leaf-shiva",
    "kanwar-ganga-shiva",
    "parvati-sawan-tapasya",
    "naga-shiva-ornament",
    "rudraksha-tears-shiva",
    "neelkanth-poison",
    "ganga-avatarana",
    "markandeya-shiva",
}


def build_story_detail(
    story: dict,
    stories_data: dict,
    asset_ver: str,
    nav: Callable,
    footer: Callable,
    head: Callable,
) -> str:
    prefix = "../"
    sec = stories_data.get("section") or {}
    rel_dev = "".join(
        f'<a class="tag" href="{prefix}devotion/{e(s)}.html">{e(s.replace("-", " "))}</a>'
        for s in story.get("relatedDevotion") or []
    )
    rel_fest = "".join(
        f'<a class="tag" href="{prefix}festivals/{e(s)}.html">{e(s.replace("-", " "))}</a>'
        for s in story.get("relatedFestivals") or []
    )
    rel_tmp = "".join(
        f'<a class="tag" href="{prefix}temples/{e(s)}.html">{e(s.replace("-", " "))}</a>'
        for s in story.get("relatedTemples") or []
    )
    href = f"{prefix}stories/{story['slug']}.html"
    abs_path = f"stories/{story['slug']}.html"
    hindi_first = story["slug"] in HINDI_PRIMARY_STORY_SLUGS or bool(
        set(story.get("tags") or []) & HINDI_PRIMARY_STORY_TAGS
    )
    default_lang = "hi" if hindi_first else "en"
    title_hi = story.get("titleHi") or story["title"]
    share_text = (
        f"{title_hi} — TirthaYatra short story for home puja"
        if hindi_first
        else f"{story['title']} — short story for home puja · TirthaYatra"
    )
    page_title = (
        f"{title_hi} | {story['title']} — TirthaYatra"
        if story.get("titleHi")
        else f"{story['title']} — TirthaYatra"
    )
    desc = story.get("hookHi") or story.get("hook") or story["title"]
    body = f"""
{nav('stories', prefix)}
<article class="section story-article" data-board-open="story" data-slug="{e(story['slug'])}">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}stories/index.html">Stories</a> · {e(title_hi)}</p>
  <div class="page-tools">{lang_toggle()}</div>
  <p class="section-kicker">~{e(str(story.get('readSeconds', 70)))} second read · home puja</p>
  <h1><span class="lang-hi">{e(title_hi)}</span><span class="lang-en title-en-sep"> · {e(story['title'])}</span></h1>
  {lang_p(story.get('hook', ''), story.get('hookHi', ''), cls='lede')}
  <p>{save_btn('story', story['slug'], story['title'], href)}</p>
  {share_bar(title=page_title, text=share_text, url=abs_path, kind='story')}
  <h2 class="section-title">कथा · The story</h2>
  {lang_p(story.get('storyEn', ''), story.get('storyHi', ''))}
  <h2 class="section-title">क्यों · Why this ritual</h2>
  {lang_p(story.get('whyRitual', ''), story.get('whyRitualHi', ''))}
  <h2 class="section-title">Takeaway for home</h2>
  <p class="lang-en">{e(story.get('takeaway', ''))}</p>
  <h2 class="section-title">Continue</h2>
  <p class="devotion-related">{rel_dev}{rel_fest}{rel_tmp}</p>
  <aside class="belief-disclaimer" style="margin-top:2rem">
    <strong>Note:</strong> {e(sec.get('disclaimer', ''))}
  </aside>
  {feedback_section_html('story')}
</article>
{footer(prefix)}
</body>
</html>
"""
    return head(
        page_title,
        desc,
        prefix,
        lang=default_lang,
        canonical_path=abs_path,
        default_lang=default_lang,
    ) + body


def build_daily_practice(
    engagement: dict,
    devotion_items: list,
    stories_data: dict,
    asset_ver: str,
    nav: Callable,
    footer: Callable,
    head: Callable,
) -> str:
    prefix = "../"
    rotation = engagement.get("dailyRotation") or {}
    challenges = engagement.get("challenges") or []
    by_slug = {i["slug"]: i for i in devotion_items}
    story_titles = {s["slug"]: s["title"] for s in stories_data.get("stories") or []}

    ch_html = []
    for ch in challenges:
        dslug = ch.get("devotionSlug")
        dtitle = by_slug.get(dslug, {}).get("titleHi") or by_slug.get(dslug, {}).get("title") or dslug
        link = f'{prefix}devotion/{e(dslug)}.html' if dslug else "#"
        story_link = ""
        if ch.get("storySlug"):
            story_link = f' · <a href="{prefix}stories/{e(ch["storySlug"])}.html">Related story</a>'
        days = int(ch.get("days") or 1)
        marks = "".join(
            f'<button type="button" class="btn btn-ghost" data-challenge-mark="{e(ch["id"])}" data-day="{i}">Mark day {i+1}</button> '
            for i in range(days)
        )
        ch_html.append(
            f"""
            <article class="daily-challenge">
              <h3>{e(ch.get('titleHi', ''))} · {e(ch['title'])}</h3>
              <p>{e(ch.get('blurb', ''))}</p>
              <p><a class="btn btn-primary" href="{link}">{e(dtitle)}</a>{story_link}</p>
              <p class="engage-note" data-challenge-progress="{e(ch['id'])}"></p>
              <p>{marks}</p>
            </article>
            """
        )

    body = f"""
{nav('daily', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="{prefix}index.html">Home</a> · <a href="{prefix}devotion/index.html">Devotion</a> · Today</p>
  <h1>आज की साधना · Today’s practice</h1>
  <p class="lede">One aarti, one short katha, one 60–90 second story — rotated by IST date. Built for home puja and vrat days, not travel itineraries. Progress stays on this device.</p>
  <p class="engage-note">Date: <strong data-daily-date></strong></p>
</section>
<section class="section" data-daily-practice data-prefix="{e(prefix)}" data-rotation="{e(json.dumps(rotation, ensure_ascii=False))}">
  <div class="daily-grid" data-daily-slots></div>
  <p style="margin-top:1.25rem">
    <button type="button" class="btn btn-primary" data-daily-done>Mark today’s practice done</button>
  </p>
  <p class="engage-note" data-daily-done-note hidden>Nice — see you tomorrow for a fresh rotation.</p>
  <h2 class="section-title">Progressive devotion (streak-light)</h2>
  <p class="section-desc">No points, no public leaderboard — just gentle continuity on this browser.</p>
  {''.join(ch_html)}
  <aside class="belief-disclaimer" style="margin-top:2rem">
    <strong>Privacy:</strong> Marks are stored in your browser only (localStorage). We do not upload devotion streaks. Email / WhatsApp digests are not enabled in this demo.
  </aside>
</section>
{footer(prefix)}
<script src="{prefix}js/daily.js?v={asset_ver}"></script>
</body>
</html>
"""
    # story_titles unused but kept for future labels — silence via _
    _ = story_titles
    return head(
        "Today’s Practice — TirthaYatra",
        "Daily aarti, vrat katha, and short story for home devotion.",
        prefix,
    ) + body


def build_my_board(
    engagement: dict,
    temples: list,
    festival_guide: dict,
    devotion_items: list,
    stories_data: dict,
    asset_ver: str,
    nav: Callable,
    footer: Callable,
    head: Callable,
) -> str:
    prefix = ""
    catalog = {
        "temples": {
            t["slug"]: {"title": t["name"], "href": f"temples/{t['slug']}.html"}
            for t in temples
        },
        "festivals": {
            f["slug"]: {"title": f["name"], "href": f"festivals/{f['slug']}.html"}
            for f in festival_guide.get("festivals") or []
        },
        "devotion": {
            i["slug"]: {
                "title": i.get("titleHi") or i.get("title") or i["slug"],
                "href": f"devotion/{i['slug']}.html",
            }
            for i in devotion_items
        },
        "stories": {
            s["slug"]: {"title": s["title"], "href": f"stories/{s['slug']}.html"}
            for s in stories_data.get("stories") or []
        },
    }
    presets = engagement.get("checklistPresets") or {}
    checklist_html = []
    for pid, preset in presets.items():
        checklist_html.append(
            f"""
            <div class="board-checklist">
              <h3>{e(preset.get('title', pid))}</h3>
              <div data-checklist-preset="{e(pid)}" data-items="{e(json.dumps(preset.get('items') or [], ensure_ascii=False))}"></div>
            </div>
            """
        )

    body = f"""
{nav('board', prefix)}
<section class="page-head">
  <p class="breadcrumb"><a href="index.html">Home</a> · My Board</p>
  <h1>मेरा पट्टा · My Board</h1>
  <p class="lede">Saved temples, festivals, aartis, and stories on this device. Diwali / Navaratri home checklists included. Nothing is synced to a server in this demo.</p>
</section>
<section class="section" data-my-board-page data-prefix="{e(prefix)}" data-catalog="{e(json.dumps(catalog, ensure_ascii=False))}">
  <h2 class="section-title">Saved festivals</h2>
  <div class="board-list" data-board-festivals></div>
  <h2 class="section-title">Saved aarti &amp; katha</h2>
  <div class="board-list" data-board-devotion></div>
  <h2 class="section-title">Saved stories</h2>
  <div class="board-list" data-board-stories></div>
  <h2 class="section-title">Temples I want to read / visit later</h2>
  <div class="board-list" data-board-temples></div>
  <h2 class="section-title">Home checklists</h2>
  {''.join(checklist_html)}
  <h2 class="section-title">Opened often on this device</h2>
  <p class="engage-note">Honest local count only — not a public “most read” claim for advertising.</p>
  <ul data-board-local-popular></ul>
  <aside class="belief-disclaimer" style="margin-top:2rem">
    <strong>AdSense / privacy:</strong> My Board uses localStorage only. Clear site data to erase saves. If ads are enabled later, we will not use religious belief profiling; see Privacy Policy.
  </aside>
</section>
{footer(prefix)}
<script src="js/my-board-page.js?v={asset_ver}"></script>
</body>
</html>
"""
    return head(
        "My Board — TirthaYatra",
        "Your saved aartis, festivals, stories, and home checklists (on this device).",
        prefix,
    ) + body


def temple_post_visit_loop(
    t: dict,
    *,
    prefix: str,
    related_html: str,
    devotion_items: list,
    festival_guide: dict,
    stories_data: dict,
) -> str:
    """Related aarti, nearest festival guide, similar temples, ask link."""
    families = t.get("deityFamilies") or []
    deity = (t.get("deity") or "").lower()
    aartis = []
    for item in devotion_items:
        if item.get("type") != "aarti":
            continue
        if item.get("deity") in families or item.get("deity") in deity:
            aartis.append(item)
        if len(aartis) >= 3:
            break
    if not aartis:
        aartis = [i for i in devotion_items if i.get("type") == "aarti"][:2]

    aarti_links = "".join(
        f'<a class="tag" href="{prefix}devotion/{e(a["slug"])}.html">{e(a.get("titleHi") or a["title"])}</a>'
        for a in aartis
    )

    fest_links = []
    for fest in festival_guide.get("festivals") or []:
        for slug in fest.get("relatedTemples") or []:
            if slug == t["slug"]:
                fest_links.append(fest)
                break
    if not fest_links:
        # deity-based soft match via related devotion overlap
        for fest in (festival_guide.get("festivals") or [])[:3]:
            fest_links.append(fest)
    fest_html = "".join(
        f'<a class="tag" href="{prefix}festivals/{e(f["slug"])}.html">{e(f["name"])}</a>'
        for f in fest_links[:3]
    )

    story_html = ""
    for s in stories_data.get("stories") or []:
        if t["slug"] in (s.get("relatedTemples") or []) or (
            families and s.get("deity") in families
        ):
            story_html = f'<a class="tag" href="{prefix}stories/{e(s["slug"])}.html">{e(s["title"])}</a>'
            break

    ask = "mailto:TirthaYatraOnline@gmail.com?subject=" + urllib.parse.quote(
        "Question about " + t["name"]
    )
    save = save_btn(
        "temple",
        t["slug"],
        t["name"],
        f"{prefix}temples/{t['slug']}.html",
        "Save temple to My Board",
    )

    return f"""
    <section class="temple-section" id="related">
      <h2>Continue at home · आगे की साधना</h2>
      <p>Not a travel itinerary — related aarti, festival guides, stories, and similar temples for reading and puja.</p>
      <p>{save}</p>
      <h3>Related aarti</h3>
      <p class="devotion-related">{aarti_links or "—"}</p>
      <h3>Related festivals</h3>
      <p class="devotion-related">{fest_html or "—"}</p>
      <h3>Short story</h3>
      <p class="devotion-related">{story_html or f'<a class="tag" href="{prefix}stories/index.html">Browse stories</a>'}</p>
      <h3>Similar temples</h3>
      {related_html}
      <h3>Ask or correct</h3>
      <p>
        <button type="button" class="btn btn-primary" data-feedback-open data-type="question">Send feedback on this temple</button>
        <a class="btn btn-ghost" href="{ask}">Email directly</a>
      </p>
      <p class="engage-note">Corrections and respectful questions help us improve guides. Not a booking service. Feedback is reviewed before any public use.</p>
      <p style="margin-top:1rem">
        <a class="btn btn-ghost" href="{prefix}devotion/daily.html">Today’s practice</a>
        <a class="btn btn-ghost" href="{prefix}my-board.html">My Board</a>
      </p>
    </section>
    """
