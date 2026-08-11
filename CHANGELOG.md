# Changelog

All notable changes to **TirthaYatra** are documented here.

This project follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

| Bump | When |
|------|------|
| **MAJOR** | Breaking site structure or removed public URLs without redirects |
| **MINOR** | New features / content areas (festivals, stories, practice, etc.) |
| **PATCH** | Fixes, copy edits, small UI/security hardenings |

The current version is in [`VERSION`](./VERSION). Released versions should also be git tags (`v0.3.0`, etc.) so any earlier build can be checked out or promoted on Vercel.

## [0.5.3] - 2026-08-11

### Added
- **Sawan / Shravan month pack** for monsoon Shiva devotion:
  - Festival guides: Sawan/Shravan, Kanwar Yatra (Bol Bam), Nag Panchami
  - Stories: bilva leaf, kanwar–Ganga, Parvati’s tapasya, Naga ornament, rudraksha tears
  - Vrat kathas: Sawan Somwar, Mangala Gauri, Nag Panchami (original TirthaYatra retellings)
  - Aarti/stotra: Lingashtakam; engagement checklist + 4-Monday challenge
  - Temples: Neelkanth Mahadev (Rishikesh), Baba Garibnath (Muzaffarpur), Pura Mahadev (Baghpat) — with Commons photos
  - 2026 calendar markers for Sawan start/Somwars/Shivaratri/Nag Panchami (North India reference; confirm local panchang)

## [0.5.2] - 2026-08-10

### Added
- **Split sitemaps for every public page** — `sitemap.xml` is now a sitemap index pointing to section files under `/sitemaps/`:
  - temples (283), devotion (49), festivals (29), stories (36), states (29), circuits (11), deities (9), core hubs, legal pages
  - **image sitemap** for 231 temples with Wikimedia photos
- Combined flat fallback at `/sitemap-all.xml`; `robots.txt` lists the index and all child sitemaps

## [0.5.1] - 2026-08-09

### Added
- **Temple content enrichment** for thin / newly added pages: longer mythology openings, sacred phrases, nearby temple links, state-aware climate/best-time/food/language, deity-aware festivals
- **Wikimedia Commons photos** for **231 / 283** temples — Public Domain / CC0 / CC BY / CC BY-SA only (AdSense-safe); **52** left without a photo where no clear licensed match was found

## [0.5.0] - 2026-08-09

### Added
- **~125 high-search / high-footfall temples** (site **158 → 283** total), prioritizing Google/YouTube popularity and reported pilgrim visitors
- **20 Indian states/UTs at ≥10 famous temples**; new coverage for Sikkim, Manipur, Arunachal Pradesh, Puducherry
- Approximate visitor / search signals in `famousFor` (editorial estimates from public pilgrimage reporting — not paid rankings)
- State portals for newly covered regions; Northeast states listed with fewer entries where fewer major Hindu tirthas exist

## [0.4.2] - 2026-08-09

### Added
- **15 high-search short stories** (India + diaspora / YouTube favourites): Samudra Manthan–Kurma, Makhan Chor, Vishwarupa, Narasimha, Lakshman Rekha, Ahalya, Ganesha writes Mahabharata, Matsya–Manu, Varaha, Shravan Kumar, Bhishma Pratigya, Kali–Raktabija, Putana, Narakasura, Sita swayamvara bow (36 stories total)
- Daily rotation and editor picks updated

## [0.4.1] - 2026-08-09

### Fixed
- **Vrat Katha videos** — added YouTube watch/listen embeds for all 7 new kathas (Satyanarayan, Karva Chauth, Chhath, Teej, Vat Savitri, Maha Shivaratri, Ahoi Ashtami); player shown first on vrat pages; privacy-enhanced YouTube embeds

## [0.4.0] - 2026-08-09

### Added
- **16 high-search festival guides** (India + diaspora): Karva Chauth, Chhath, Ram Navami, Hanuman Jayanti, Vasant Panchami, Akshaya Tritiya, Guru Purnima, Govardhan Puja, Jagannath Rath Yatra, Onam, Ugadi, Vaisakhi/Vishu/Puthandu, Dhanteras, Kartik Purnima, Hartalika Teej, Vat Savitri
- **7 new vrat kathas** as original TirthaYatra retellings (AdSense/copyright-safe): Karva Chauth, Chhath, Satyanarayan, Teej, Vat Savitri, Maha Shivaratri, Ahoi Ashtami
- Calendar dates for Onam, Ugadi, Teej, Vat Savitri/Purnima, Dhanteras, Ahoi Ashtami, Kartik Purnima; Chhath date corrected off Kartik Purnima day
- Festival/devotion disclaimers clarified for original retellings vs classical hymns

## [0.3.1] - 2026-08-07

### Added
- **12 popular short stories** often searched / retold online: Govardhan, Kaliya, Bhagavad Gita at Kurukshetra, Ganga avatarana, Vamana–Bali, Sudama, Savitri–Satyavan, Markandeya, Dhruva, Shabari, Ganesha–Chandra curse, Mohini–amrita (21 stories total)
- Stories index / daily rotation / editor picks updated for the new set

## [0.3.0] - 2026-08-07

Home-devotion engagement (calendar, practice, My Board, feedback).

### Added
- **Festival calendar** — month view, next 30 days, shareable plain-text cards (`festivals/calendar.html`)
- **Short stories** — myth explainers with story / why-ritual / takeaway (`stories/`, `data/stories.json`)
- **Today’s practice** — IST-rotated aarti + katha + story and streak-light challenges (`devotion/daily.html`)
- **My Board** — localStorage saves, Diwali/Navaratri checklists (`my-board.html`, `js/board.js`)
- **Home engagement band** — festival countdown, editor picks / first-timers / family-friendly
- **Feedback loop** — correction / add-detail / highlight / tip via email + optional on-device copy (`js/feedback.js`, `pages/feedback.html`)
- **Temple post-visit loop** — related aarti, festivals, stories, ask/feedback CTAs
- Compact **Explore** footer as a two-column link grid
- This **CHANGELOG** and **VERSION** file for ongoing versioning

### Changed
- Story bodies rewritten as real myth narratives (removed “foreign reader / page intent” meta copy)
- Privacy / Terms / About updated for on-device board data, moderated feedback, and copyright notes
- Nav links for Stories, Today, My Board

### Security / policy
- Feedback is emailed for editorial review and **not** auto-published (AdSense-friendlier UGC stance)
- Social proof labeled as editorial picks; on-device “opened often” is local-only, not fabricated traffic

## [0.2.0] - 2026-08-05

### Added
- Expanded **festival guides** (Shivaratri, Holi, Dussehra, Lohri, Sankranti, Pongal, Gudi Padwa, Raksha Bandhan, Ganesh Chaturthi, Bhai Dooj, plus richer Diwali / Navaratri / Janmashtami)
- Festival story, mythology, and Devi–Devata sections
- Security hardenings: CSP / HSTS / framing headers, `safe_url` + YouTube host checks, deploy prune, privacy alignment for Vercel Analytics

### Removed
- **Epic Trails** (story maps) — removed from nav, build, and sitemap for now

## [0.1.0] - 2026-08-04

### Added
- Initial TirthaYatra static site: temples, circuits, deities, devotion (aarti / chalisa / vrat katha)
- Client IST panchang, search, Vercel hosting, sitemap / robots, Web Analytics
- First festival guide set (Diwali, Navaratri, Janmashtami)

---

## Versioning workflow

1. Change code / content as usual; run `python3 build.py` before committing generated HTML when needed.
2. Update [`VERSION`](./VERSION) and add a section under **Unreleased** or a dated version in this file.
3. Commit locally: `git commit …`
4. Optional: `git tag vX.Y.Z` after the release commit.
5. Deploy: `git push origin main` (and `git push --tags` if tagged).
6. Rollback live site: promote an older Vercel deployment, and/or check out / revert to an earlier git tag or commit.
