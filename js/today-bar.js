/**
 * Sticky "Today" bar — today's aarti / katha / story (IST rotation).
 */
(function () {
  var bar = document.querySelector("[data-today-bar]");
  if (!bar) return;

  var prefix = bar.getAttribute("data-prefix") || "";
  var dismissKey = "tirthayatra-today-bar-dismiss";

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

  function render(data) {
    var iso = istIso(new Date());
    var rot = (data && data.rotation) || {};
    var labels = (data && data.labels) || {};
    var aarti = pick(rot.aarti, iso);
    var katha = pick(rot.katha, iso);
    var story = pick(rot.story, iso);

    var links = bar.querySelector("[data-today-links]");
    if (!links) return;

    var parts = [];
    if (aarti) {
      parts.push(
        '<a class="today-bar-link" href="' +
          hrefFor("aarti", aarti) +
          '"><span class="today-bar-kicker">आरती</span> ' +
          labelFor(labels, aarti) +
          "</a>"
      );
    }
    if (katha) {
      parts.push(
        '<a class="today-bar-link" href="' +
          hrefFor("katha", katha) +
          '"><span class="today-bar-kicker">कथा</span> ' +
          labelFor(labels, katha) +
          "</a>"
      );
    }
    if (story) {
      parts.push(
        '<a class="today-bar-link" href="' +
          hrefFor("story", story) +
          '"><span class="today-bar-kicker">कहानी</span> ' +
          labelFor(labels, story) +
          "</a>"
      );
    }
    links.innerHTML = parts.join('<span class="today-bar-sep" aria-hidden="true">·</span>');

    var dateEl = bar.querySelector("[data-today-date]");
    if (dateEl) dateEl.textContent = iso;

    try {
      if (sessionStorage.getItem(dismissKey) === iso) {
        bar.setAttribute("hidden", "");
        document.documentElement.classList.remove("has-today-bar");
      } else {
        bar.removeAttribute("hidden");
        document.documentElement.classList.add("has-today-bar");
      }
    } catch (e) {
      bar.removeAttribute("hidden");
      document.documentElement.classList.add("has-today-bar");
    }
  }

  var dismiss = bar.querySelector("[data-today-dismiss]");
  if (dismiss) {
    dismiss.addEventListener("click", function () {
      try {
        sessionStorage.setItem(dismissKey, istIso(new Date()));
      } catch (e) {}
      bar.setAttribute("hidden", "");
      document.documentElement.classList.remove("has-today-bar");
    });
  }

  // Prefer build-time JSON; fall back to inline payload
  var inline = document.getElementById("today-bar-data");
  if (inline && inline.textContent) {
    try {
      render(JSON.parse(inline.textContent));
      return;
    } catch (e) {}
  }

  fetch(prefix + "js/today-bar-data.json", { credentials: "same-origin" })
    .then(function (r) {
      return r.ok ? r.json() : null;
    })
    .then(function (data) {
      if (data) render(data);
    })
    .catch(function () {});
})();
