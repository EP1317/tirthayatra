"""Shared Article / FAQ JSON-LD and FAQ HTML for TirthaYatra pages."""

from __future__ import annotations

import html

SITE_URL = "https://www.tirthayatraonline.in"
ORG_ID = f"{SITE_URL}/#organization"


def _esc(text) -> str:
    return html.escape("" if text is None else str(text), quote=True)


def sitemap_abs(path: str) -> str:
    path = (path or "").lstrip("/")
    if not path or path == "index.html":
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{path}"


def clip_text(text: str, limit: int = 280) -> str:
    raw = " ".join(str(text or "").split())
    if len(raw) <= limit:
        return raw
    return raw[: limit - 1].rstrip() + "…"


def faq_page_ld(faqs: list[tuple[str, str]]) -> dict | None:
    entities = []
    for q, a in faqs:
        q, a = (q or "").strip(), (a or "").strip()
        if not q or not a:
            continue
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    if not entities:
        return None
    return {"@type": "FAQPage", "mainEntity": entities}


def article_ld(
    *,
    headline: str,
    description: str,
    url: str,
    language: str = "hi",
    date_modified: str | None = None,
    about: list | None = None,
) -> dict:
    node = {
        "@type": "Article",
        "headline": clip_text(headline, 110),
        "description": clip_text(description, 300),
        "inLanguage": language,
        "isAccessibleForFree": True,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {
            "@type": "Organization",
            "name": "TirthaYatra",
            "url": f"{SITE_URL}/",
        },
        "publisher": {
            "@type": "Organization",
            "@id": ORG_ID,
            "name": "TirthaYatra",
            "url": f"{SITE_URL}/",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/assets/icons/logo-512.png",
            },
        },
    }
    if date_modified:
        node["dateModified"] = date_modified
    if about:
        node["about"] = about
    return node


def json_ld_graph(*nodes: dict | None) -> dict:
    cleaned = [n for n in nodes if n]
    return {"@context": "https://schema.org", "@graph": cleaned}


def faq_section_html(
    faqs: list[tuple[str, str]],
    *,
    title: str = "Common questions · सामान्य प्रश्न",
) -> str:
    items = []
    for q, a in faqs:
        q, a = (q or "").strip(), (a or "").strip()
        if not q or not a:
            continue
        items.append(
            f'<details class="faq-item"><summary>{_esc(q)}</summary>'
            f"<p>{_esc(a)}</p></details>"
        )
    if not items:
        return ""
    return (
        f'<section class="faq-block temple-section" id="faq">'
        f"<h2>{_esc(title)}</h2>"
        f'{"".join(items)}'
        f"</section>"
    )


def related_stories_html(stories: list[dict], prefix: str) -> str:
    if not stories:
        return ""
    links = "".join(
        f'<a class="related-link" href="{prefix}stories/{_esc(s["slug"])}.html">'
        f'<strong>{_esc(s.get("titleHi") or s.get("title") or s["slug"])}</strong>'
        f'{_esc(s.get("hookHi") or s.get("hook") or "")}</a>'
        for s in stories[:6]
    )
    return f"""
    <section class="temple-section" id="related-stories">
      <h2>Related stories · संबंधित कथा</h2>
      <p class="section-desc">Short myth explainers linked to this tirtha — useful for home puja and Search discovery.</p>
      <div class="related-strip">{links}</div>
    </section>
    """
