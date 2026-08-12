/**
 * Sticky "Today" bar — panchang + today's aarti / katha / story (IST).
 * Always visible (no dismiss). Respects Hindi/EN preference from lang-pref.js.
 */
(function () {
  var bar = document.querySelector("[data-today-bar]");
  if (!bar) return;

  var prefix = bar.getAttribute("data-prefix") || "";
  document.documentElement.classList.add("has-today-bar");
  bar.removeAttribute("hidden");

  var practiceData = null;
  var lastPan = null;
  var lastFestivals = null;

  function lang() {
    if (window.TirthaLang && typeof window.TirthaLang.get === "function") {
      return window.TirthaLang.get();
    }
    var d = document.documentElement.getAttribute("data-lang");
    return d === "hi" || d === "en" ? d : "en";
  }

  function istIso(d) {
    return new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Kolkata",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }).format(d);
  }

  function dayIndex(iso) {
    var parts = iso.split("-").map(Number);
    return Math.floor(Date.UTC(parts[0], parts[1] - 1, parts[2]) / 86400000);
  }

  function pick(list, iso) {
    if (!list || !list.length) return null;
    return list[dayIndex(iso) % list.length];
  }

  function labelFor(catalog, slug) {
    if (!slug) return "";
    if (catalog && catalog[slug]) return catalog[slug];
    return slug.replace(/-/g, " ");
  }

  function hrefFor(kind, slug) {
    if (!slug) return "#";
    if (kind === "story") return prefix + "stories/" + slug + ".html";
    return prefix + "devotion/" + slug + ".html";
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  var KICKERS = {
    hi: { aarti: "आरती", katha: "कथा", story: "कहानी" },
    en: { aarti: "Aarti", katha: "Katha", story: "Story" },
  };

  function renderPractice(data) {
    if (data) practiceData = data;
    data = practiceData;
    if (!data) return;

    var iso = istIso(new Date());
    var rot = data.rotation || {};
    var labels = data.labels || {};
    var aarti = pick(rot.aarti, iso);
    var katha = pick(rot.katha, iso);
    var story = pick(rot.story, iso);
    var L = lang() === "hi" ? KICKERS.hi : KICKERS.en;

    var links = bar.querySelector("[data-today-links]");
    if (!links) return;

    var parts = [];
    if (aarti) {
      parts.push(
        '<a class="today-bar-link" href="' +
          hrefFor("aarti", aarti) +
          '"><span class="today-bar-kicker">' +
          L.aarti +
          "</span> " +
          escapeHtml(labelFor(labels, aarti)) +
          "</a>"
      );
    }
    if (katha) {
      parts.push(
        '<a class="today-bar-link" href="' +
          hrefFor("katha", katha) +
          '"><span class="today-bar-kicker">' +
          L.katha +
          "</span> " +
          escapeHtml(labelFor(labels, katha)) +
          "</a>"
      );
    }
    if (story) {
      parts.push(
        '<a class="today-bar-link" href="' +
          hrefFor("story", story) +
          '"><span class="today-bar-kicker">' +
          L.story +
          "</span> " +
          escapeHtml(labelFor(labels, story)) +
          "</a>"
      );
    }
    links.innerHTML = parts.join(
      '<span class="today-bar-sep" aria-hidden="true">·</span>'
    );

    var dateEl = bar.querySelector("[data-today-date]");
    if (dateEl) dateEl.textContent = iso;

    var home = bar.querySelector(".today-bar-home");
    if (home) {
      home.textContent = lang() === "hi" ? "आज" : "Today";
    }
  }

  function renderPanchang(pan, festivals) {
    if (pan) lastPan = pan;
    if (festivals) lastFestivals = festivals;
    pan = lastPan;
    festivals = lastFestivals;
    var line = bar.querySelector("[data-today-panchang-line]");
    var panel = bar.querySelector("[data-today-panchang-panel]");
    var kicker = bar.querySelector(".today-bar-panchang-kicker");
    var TP = window.TirthaPanchang;
    if (!pan || !line) return;

    var hi = lang() === "hi";
    if (kicker) kicker.textContent = hi ? "पंचांग" : "Panchang";

    var highlights =
      TP && TP.matchHighlights
        ? TP.matchHighlights(pan, festivals || { fixed: [], tithiRules: [] })
        : [];
    var festLabel = "";
    if (highlights.length > 0) {
      festLabel = hi
        ? highlights[0].nameHi || highlights[0].name || ""
        : highlights[0].name || highlights[0].nameHi || "";
    }

    var short = hi
      ? pan.varaHi +
        " · " +
        (pan.paksha === "Shukla" ? "शु" : "कृ") +
        " " +
        pan.tithiHi +
        (festLabel ? " · " + festLabel : "")
      : pan.varaEn +
        " · " +
        (pan.paksha === "Shukla" ? "Shukla" : "Krishna") +
        " " +
        pan.tithiEn +
        (festLabel ? " · " + festLabel : "");
    line.textContent = short;
    line.title = hi
      ? pan.pakshaHi + " " + pan.tithiHi + " · " + pan.nakshatraHi + " · " + pan.iso
      : pan.paksha + " " + pan.tithiEn + " · " + pan.nakshatraEn + " · " + pan.iso;

    var toggle = bar.querySelector("[data-today-panchang-toggle]");
    if (toggle) {
      toggle.title = hi ? "आज का पंचांग" : "Today’s Panchang";
    }

    if (!panel) return;
    var festHtml = "";
    if (highlights.length) {
      festHtml =
        '<div class="today-bar-panchang-fest"><strong>' +
        (hi ? "आज विशेष" : "Today’s highlights") +
        "</strong><ul>" +
        highlights
          .map(function (h) {
            var primary = hi
              ? h.nameHi || h.name
              : h.name || h.nameHi;
            var secondary = hi ? h.name : h.nameHi;
            return (
              "<li>" +
              escapeHtml(primary || "") +
              (secondary && secondary !== primary
                ? " · " + escapeHtml(secondary)
                : "") +
              "</li>"
            );
          })
          .join("") +
        "</ul></div>";
    }
    panel.innerHTML =
      '<p class="today-bar-panchang-title">' +
      (hi ? "आज का पंचांग" : "Today’s Panchang") +
      "</p>" +
      '<dl class="today-bar-panchang-facts">' +
      "<div><dt>" +
      (hi ? "वार" : "Weekday") +
      "</dt><dd>" +
      escapeHtml(pan.varaHi) +
      " · " +
      escapeHtml(pan.varaEn) +
      "</dd></div>" +
      "<div><dt>" +
      (hi ? "तिथि" : "Tithi") +
      "</dt><dd>" +
      escapeHtml(hi ? pan.pakshaHi : pan.paksha) +
      " · " +
      escapeHtml(hi ? pan.tithiHi : pan.tithiEn) +
      "</dd></div>" +
      "<div><dt>" +
      (hi ? "नक्षत्र" : "Nakshatra") +
      "</dt><dd>" +
      escapeHtml(hi ? pan.nakshatraHi : pan.nakshatraEn) +
      "</dd></div>" +
      "<div><dt>" +
      (hi ? "दिनांक (IST)" : "Date (IST)") +
      "</dt><dd>" +
      escapeHtml(pan.iso) +
      "</dd></div>" +
      "</dl>" +
      festHtml +
      '<p class="today-bar-panchang-note">' +
      (hi
        ? "संकेतात्मक पंचांग — विधि से पहले अपने पंचांग से मिलाएँ।"
        : "Indicative panchang — confirm with your local almanac before observances.") +
      "</p>" +
      '<p><a class="today-bar-cal-link" href="' +
      prefix +
      'festivals/calendar.html">' +
      (hi ? "त्योहार कैलेंडर →" : "Festival calendar →") +
      "</a></p>";
  }

  function refreshLang() {
    renderPractice(practiceData);
    if (lastPan) renderPanchang(lastPan, lastFestivals);
  }

  function bindPanchangToggle() {
    var toggle = bar.querySelector("[data-today-panchang-toggle]");
    var panel = bar.querySelector("[data-today-panchang-panel]");
    if (!toggle || !panel) return;
    toggle.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var open = panel.hasAttribute("hidden");
      if (open) {
        panel.removeAttribute("hidden");
        toggle.setAttribute("aria-expanded", "true");
      } else {
        panel.setAttribute("hidden", "");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("click", function (ev) {
      if (ev.target.closest("[data-lang-toggle]")) return;
      if (!bar.contains(ev.target)) {
        panel.setAttribute("hidden", "");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") {
        panel.setAttribute("hidden", "");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  function loadPracticeData() {
    var inline = document.getElementById("today-bar-data");
    if (inline && inline.textContent) {
      try {
        renderPractice(JSON.parse(inline.textContent));
        return;
      } catch (e) {}
    }
    fetch(prefix + "js/today-bar-data.json", { credentials: "same-origin" })
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (data) {
        if (data) renderPractice(data);
      })
      .catch(function () {});
  }

  function loadPanchang() {
    var TP = window.TirthaPanchang;
    if (!TP || !TP.compute) return;
    var pan = TP.compute(new Date());
    fetch(prefix + "data/festivals.json", { credentials: "same-origin" })
      .then(function (r) {
        return r.ok ? r.json() : { fixed: [], tithiRules: [] };
      })
      .catch(function () {
        return { fixed: [], tithiRules: [] };
      })
      .then(function (fest) {
        renderPanchang(pan, fest);
      });
  }

  document.addEventListener("tirthayatra:lang", refreshLang);

  bindPanchangToggle();
  loadPracticeData();
  loadPanchang();
})();
