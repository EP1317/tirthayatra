/**
 * TirthaYatra daily Panchang widget (IST).
 * Computed from astronomical approximations — not a reprint of any proprietary almanac.
 */
(function () {
  var root = document.querySelector("[data-panchang]");
  if (!root) return;

  var prefix = root.getAttribute("data-prefix") || "";
  var toggle = root.querySelector("[data-panchang-toggle]");
  var panel = root.querySelector("[data-panchang-panel]");
  var chipDate = root.querySelector("[data-panchang-date]");
  var chipTithi = root.querySelector("[data-panchang-tithi]");
  var chipFest = root.querySelector("[data-panchang-fest]");
  var panelBody = root.querySelector("[data-panchang-body]");

  var TITHI_NAMES = [
    "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी", "सप्तमी",
    "अष्टमी", "नवमी", "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा/अमावस्या"
  ];
  var TITHI_EN = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami",
    "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
  ];
  var NAKSHATRA = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु",
    "पुष्य", "आश्लेषा", "मघा", "पूर्व फाल्गुनी", "उत्तर फाल्गुनी", "हस्त", "चित्रा",
    "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा",
    "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्व भाद्रपद", "उत्तर भाद्रपद", "रेवती"
  ];
  var VARA = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"];
  var VARA_EN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function safeHttpUrl(url) {
    var raw = String(url || "").trim();
    if (!raw || raw.indexOf("\\") !== -1 || /[\u0000-\u001f\u007f]/.test(raw)) {
      return "";
    }
    try {
      var u = new URL(raw, window.location.origin);
      if (u.protocol !== "http:" && u.protocol !== "https:") return "";
      return u.href;
    } catch (err) {
      return "";
    }
  }

  function istParts(d) {
    var fmt = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Kolkata",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      weekday: "short",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
    var parts = {};
    fmt.formatToParts(d).forEach(function (p) {
      if (p.type !== "literal") parts[p.type] = p.value;
    });
    return parts;
  }

  function isoDateIST(d) {
    var p = istParts(d);
    return p.year + "-" + p.month + "-" + p.day;
  }

  function julianDay(y, m, day, hourIST) {
    // hourIST in hours (IST = UTC+5.5)
    var hourUTC = hourIST - 5.5;
    var Y = y;
    var M = m;
    if (M <= 2) {
      Y -= 1;
      M += 12;
    }
    var A = Math.floor(Y / 100);
    var B = 2 - A + Math.floor(A / 4);
    var dayFrac = day + hourUTC / 24;
    return (
      Math.floor(365.25 * (Y + 4716)) +
      Math.floor(30.6001 * (M + 1)) +
      dayFrac +
      B -
      1524.5
    );
  }

  function norm360(x) {
    x = x % 360;
    return x < 0 ? x + 360 : x;
  }

  // Compact Meeus-style sun/moon longitudes (good enough for display; not ritual-grade).
  function sunMoonLong(jd) {
    var T = (jd - 2451545.0) / 36525;
    var L0 = norm360(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
    var M = norm360(357.52911 + 35999.05029 * T - 0.0001537 * T * T);
    var Mr = (M * Math.PI) / 180;
    var C =
      (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(Mr) +
      (0.019993 - 0.000101 * T) * Math.sin(2 * Mr) +
      0.000289 * Math.sin(3 * Mr);
    var sun = norm360(L0 + C);

    var Lp = norm360(218.3164477 + 481267.88123421 * T);
    var D = norm360(297.8501921 + 445267.1114034 * T);
    var Ms = norm360(357.5291092 + 35999.0502909 * T);
    var Mm = norm360(134.9633964 + 477198.8675055 * T);
    var F = norm360(93.272095 + 483202.0175233 * T);
    var toR = Math.PI / 180;
    var lon =
      Lp +
      6.289 * Math.sin(Mm * toR) +
      1.274 * Math.sin((2 * D - Mm) * toR) +
      0.658 * Math.sin(2 * D * toR) +
      0.214 * Math.sin(2 * Mm * toR) +
      0.186 * Math.sin(Ms * toR) +
      0.114 * Math.sin(2 * F * toR) -
      0.059 * Math.sin((2 * D - 2 * Mm) * toR) -
      0.057 * Math.sin((2 * D - Ms - Mm) * toR) +
      0.053 * Math.sin((2 * D + Mm) * toR);
    return { sun: sun, moon: norm360(lon) };
  }

  function lahiriAyanamsa(jd) {
    var T = (jd - 2451545.0) / 36525;
    return 23.85 + 1.397 * T; // approximate Lahiri
  }

  function computePanchang(dateObj) {
    var p = istParts(dateObj);
    var y = +p.year;
    var m = +p.month;
    var day = +p.day;
    // Use ~6:00 IST as a stable “day” snapshot for tithi/nakshatra display
    var jd = julianDay(y, m, day, 6);
    var sm = sunMoonLong(jd);
    var elong = norm360(sm.moon - sm.sun);
    var tithiNum = Math.floor(elong / 12) + 1; // 1..30
    if (tithiNum > 30) tithiNum = 30;
    var paksha = tithiNum <= 15 ? "Shukla" : "Krishna";
    var tithiInPaksha = tithiNum <= 15 ? tithiNum : tithiNum - 15;
    var tithiHi =
      tithiInPaksha === 15
        ? paksha === "Shukla"
          ? "पूर्णिमा"
          : "अमावस्या"
        : TITHI_NAMES[tithiInPaksha - 1];
    var tithiEn =
      tithiInPaksha === 15
        ? paksha === "Shukla"
          ? "Purnima"
          : "Amavasya"
        : TITHI_EN[tithiInPaksha - 1];

    var ayan = lahiriAyanamsa(jd);
    var moonSid = norm360(sm.moon - ayan);
    var nakIndex = Math.floor(moonSid / (360 / 27)) % 27;
    var weekday = new Date(Date.UTC(y, m - 1, day, 0, 0)).getUTCDay();
    // IST calendar date weekday: use formatter
    var wdFmt = new Intl.DateTimeFormat("en-US", {
      timeZone: "Asia/Kolkata",
      weekday: "short",
    }).format(dateObj);
    var wdMap = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    weekday = wdMap[wdFmt] != null ? wdMap[wdFmt] : weekday;

    return {
      iso: isoDateIST(dateObj),
      year: y,
      month: m,
      day: day,
      varaHi: VARA[weekday],
      varaEn: VARA_EN[weekday],
      paksha: paksha,
      pakshaHi: paksha === "Shukla" ? "शुक्ल पक्ष" : "कृष्ण पक्ष",
      tithi: tithiInPaksha,
      tithiFull: tithiNum,
      tithiHi: tithiHi,
      tithiEn: tithiEn,
      nakshatraHi: NAKSHATRA[nakIndex],
      nakshatraEn: NAKSHATRA[nakIndex],
    };
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function matchHighlights(pan, festivals) {
    var out = [];
    var fixed = (festivals && festivals.fixed) || [];
    fixed.forEach(function (f) {
      if (f.date === pan.iso) out.push(f);
    });
    var rules = (festivals && festivals.tithiRules) || [];
    rules.forEach(function (r) {
      if (r.tithi !== pan.tithi) return;
      if (r.paksha && r.paksha !== pan.paksha) return;
      // avoid dup if fixed already named similarly
      var exists = out.some(function (x) {
        return (x.name || "").toLowerCase() === (r.name || "").toLowerCase();
      });
      if (!exists) out.push(r);
    });
    return out;
  }

  function render(pan, festivals) {
    var highlights = matchHighlights(pan, festivals);
    var isFest = highlights.some(function (h) {
      return h.importance === "high";
    });
    var any = highlights.length > 0;

    root.classList.toggle("is-festival", isFest);
    root.classList.toggle("is-observance", any && !isFest);

    var dateLabel =
      pan.day +
      "/" +
      pad(pan.month) +
      " · " +
      pan.varaEn.slice(0, 3);
    if (chipDate) chipDate.textContent = dateLabel;
    if (chipTithi) {
      chipTithi.textContent =
        (pan.paksha === "Shukla" ? "शु" : "कृ") + " · " + pan.tithiHi;
    }
    if (chipFest) {
      if (any) {
        chipFest.hidden = false;
        chipFest.textContent = highlights[0].nameHi || highlights[0].name;
      } else {
        chipFest.hidden = true;
        chipFest.textContent = "";
      }
    }

    var festHtml = "";
    if (any) {
      festHtml =
        '<div class="panchang-fest-list"><p class="panchang-fest-kicker">आज विशेष</p><ul>' +
        highlights
          .map(function (h) {
            return (
              "<li><strong>" +
              escapeHtml(h.nameHi || h.name) +
              "</strong> · " +
              escapeHtml(h.name || "") +
              "</li>"
            );
          })
          .join("") +
        "</ul></div>";
    }

    var ref = (festivals && festivals.referenceLink) || {
      label: "Traditional almanac reference",
      url: "https://thakurprasad.in/",
    };
    var disc =
      (festivals && festivals.disclaimer) ||
      "Indicative panchang for planning. Confirm with your preferred almanac before rituals.";

    if (panelBody) {
      panelBody.innerHTML =
        '<dl class="panchang-facts">' +
        "<div><dt>वार · Weekday</dt><dd>" +
        escapeHtml(pan.varaHi) +
        " · " +
        escapeHtml(pan.varaEn) +
        "</dd></div>" +
        "<div><dt>तिथि · Tithi</dt><dd>" +
        escapeHtml(pan.pakshaHi) +
        " · " +
        escapeHtml(pan.tithiHi) +
        " (" +
        escapeHtml(pan.tithiEn) +
        ")</dd></div>" +
        "<div><dt>नक्षत्र · Nakshatra</dt><dd>" +
        escapeHtml(pan.nakshatraHi) +
        "</dd></div>" +
        "<div><dt>दिनांक · Date (IST)</dt><dd>" +
        escapeHtml(pan.iso) +
        "</dd></div>" +
        "</dl>" +
        festHtml +
        '<p class="panchang-note">' +
        escapeHtml(disc) +
        "</p>" +
        (function () {
          var refUrl = safeHttpUrl(ref && ref.url);
          if (!refUrl) return "";
          return (
            '<p class="panchang-ref"><a href="' +
            escapeHtml(refUrl) +
            '" target="_blank" rel="noopener noreferrer">' +
            escapeHtml(ref.label) +
            " ↗</a></p>"
          );
        })();
    }
  }

  function loadFestivals() {
    return fetch(prefix + "data/festivals.json", { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("festivals missing");
        return r.json();
      })
      .catch(function () {
        return { fixed: [], tithiRules: [] };
      });
  }

  function closePanel() {
    if (!panel) return;
    panel.hidden = true;
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }

  function openPanel() {
    if (!panel) return;
    panel.hidden = false;
    if (toggle) toggle.setAttribute("aria-expanded", "true");
  }

  if (toggle && panel) {
    toggle.addEventListener("click", function (ev) {
      ev.stopPropagation();
      if (panel.hidden) openPanel();
      else closePanel();
    });
    document.addEventListener("click", function (ev) {
      if (!root.contains(ev.target)) closePanel();
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") closePanel();
    });
  }

  var pan = computePanchang(new Date());
  loadFestivals().then(function (fest) {
    render(pan, fest);
  });
})();
