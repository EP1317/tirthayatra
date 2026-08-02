# TirthaYatra

Static Indian temple & pilgrimage guide site — mythology, sacred circuits, itineraries, and practical darshan details. Built for later Google AdSense monetisation.

## Quick start

```bash
cd TempleYatra
python3 build.py
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Add a temple

1. Add a summary entry in `data/temples.json`.
2. Create `data/temples/<slug>.json` using the same fields as existing temples.
3. Tag with circuit slugs from `data/circuits.json`.
4. Run `python3 build.py`.

## Structure

- `index.html` — homepage (generated)
- `temples/` — temple guides (generated)
- `circuits/` — circuit hubs (generated)
- `pages/` — About, Contact, Privacy, Disclaimer, Terms
- `assets/temples/` — Wikimedia Commons photos (credited on each page)
- `data/media.json` — image credits + local paths
- `css/main.css` — mythological design system
- `build.py` — static site generator

## Images & maps

Photos are downloaded from **Wikimedia Commons** (Public Domain / Creative Commons) — not scraped from temple websites — and credited on each page. Google Maps embeds use coordinates / place queries on every temple guide.

## Before AdSense

- Contact email: `TirthaYatraOnline@gmail.com`
- Buy a custom domain + HTTPS hosting
- Expand to ~20+ deep temple pages
- Switch comments from localStorage to a moderated service
- Re-verify timings against official trust sites


## Browse by state

- `states/` — one page per Indian state with temples on the site
- `data/state-portals.json` — official government / Devasthan / HRCE links  
  (e.g. [AP Temples](https://www.aptemples.org/en-in/home), TN HR&CE, Telangana Endowments, Karnataka HRI&CE, Rajasthan Devasthan)

```bash
python3 scripts/add_state_temples.py   # add featured temples + attach portal refs
python3 scripts/fetch_images.py        # Wikimedia Commons photos (licensed)
python3 scripts/sync_groups.py
python3 build.py
```

Photos are from Wikimedia Commons only (credited). Government portals are linked for official details — their images are not scraped.

## Circuit membership (source of truth)

Fixed-count circuits are defined in `data/groups.json` and synced by:

```bash
python3 scripts/sync_groups.py
python3 build.py
```

- **Char Dham** = Badrinath, Dwarka, Puri, Rameswaram only (not Kedarnath)
- **Chota Char Dham** = Yamunotri, Gangotri, Kedarnath, Badrinath
- **Panch Kedar** = Kedarnath + four Garhwal Kedars
- Shared temples (e.g. Kedarnath, Badrinath, Jagannath Puri) keep **one** detail file and appear in multiple circuits with the same facts
