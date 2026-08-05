(function () {
  var widgets = document.querySelectorAll("[data-temple-search]");
  if (!widgets.length) return;

  var cache = null;
  var loading = null;
  var primaryInput = null;

  function prefixOf(el) {
    return el.getAttribute("data-prefix") || "";
  }

  function indexUrl(prefix) {
    return prefix + "data/search-index.json";
  }

  function loadIndex(prefix) {
    if (cache) return Promise.resolve(cache);
    if (loading) return loading;
    loading = fetch(indexUrl(prefix), { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("search index missing");
        return r.json();
      })
      .then(function (data) {
        cache = data;
        loading = null;
        return cache;
      })
      .catch(function () {
        loading = null;
        cache = [];
        return cache;
      });
    return loading;
  }

  function normalize(s) {
    return String(s || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function scoreItem(item, q) {
    var name = normalize(item.name);
    var loc = normalize(item.location);
    var state = normalize(item.state);
    var country = normalize(item.country);
    var famous = normalize(item.famousFor);
    var tags = normalize((item.tags || []).join(" "));
    var deities = normalize((item.deities || []).join(" "));
    var slug = normalize(item.slug);
    if (name === q) return 100;
    if (name.indexOf(q) === 0) return 90;
    if (name.indexOf(q) !== -1) return 80;
    if (slug.indexOf(q) !== -1) return 70;
    if (state.indexOf(q) !== -1 || loc.indexOf(q) !== -1) return 60;
    if (deities.indexOf(q) !== -1) return 50;
    if (famous.indexOf(q) !== -1 || tags.indexOf(q) !== -1 || country.indexOf(q) !== -1)
      return 40;
    var parts = q.split(/\s+/).filter(Boolean);
    if (parts.length > 1) {
      var blob = [name, loc, state, famous, tags, deities, slug].join(" ");
      if (parts.every(function (p) { return blob.indexOf(p) !== -1; })) return 55;
    }
    return 0;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** Allow only relative site paths like temples/foo.html (no schemes / //). */
  function safeRelativeHref(prefix, href) {
    var raw = String(href || "").trim();
    if (!raw || /^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(raw) || raw.indexOf("//") === 0) {
      return "";
    }
    if (
      raw.indexOf("\\") !== -1 ||
      raw.indexOf("..") !== -1 ||
      /[\u0000-\u001f\u007f]/.test(raw)
    ) {
      return "";
    }
    if (!/^[a-zA-Z0-9._/-]+\.html$/.test(raw)) return "";
    var p = String(prefix || "");
    if (p && !/^(?:\.\.\/)+$/.test(p)) return "";
    return p + raw;
  }

  function render(widget, items, q) {
    var box = widget.querySelector("[data-search-results]");
    if (!box) return;
    if (!q) {
      box.hidden = true;
      box.innerHTML = "";
      return;
    }
    if (!items.length) {
      box.hidden = false;
      box.innerHTML =
        '<p class="temple-search-empty">No temples match “' +
        escapeHtml(q) +
        '”. Try a city, state, or deity name.</p>';
      return;
    }
    var prefix = prefixOf(widget);
    box.hidden = false;
    box.innerHTML = items
      .map(function (item) {
        var href = safeRelativeHref(prefix, item.href);
        if (!href) return "";
        var meta = [item.state || item.country, item.famousFor]
          .filter(Boolean)
          .join(" · ");
        var tags = (item.tags || [])
          .slice(0, 2)
          .map(function (t) {
            return '<span class="tag">' + escapeHtml(t) + "</span>";
          })
          .join("");
        return (
          '<a class="temple-search-hit" role="option" href="' +
          escapeHtml(href) +
          '"><strong>' +
          escapeHtml(item.name) +
          "</strong><span>" +
          escapeHtml(meta) +
          "</span><span class=\"temple-search-hit-tags\">" +
          tags +
          "</span></a>"
        );
      })
      .filter(Boolean)
      .join("");
  }

  function bind(widget) {
    var input = widget.querySelector("[data-search-input]");
    var box = widget.querySelector("[data-search-results]");
    if (!input || !box) return;
    if (!primaryInput) primaryInput = input;

    var timer = null;

    function run() {
      var q = normalize(input.value).trim();
      if (q.length < 2) {
        render(widget, [], "");
        return;
      }
      loadIndex(prefixOf(widget)).then(function (data) {
        var ranked = data
          .map(function (item) {
            return { item: item, score: scoreItem(item, q) };
          })
          .filter(function (x) {
            return x.score > 0;
          })
          .sort(function (a, b) {
            return b.score - a.score || a.item.name.localeCompare(b.item.name);
          })
          .slice(0, 8)
          .map(function (x) {
            return x.item;
          });
        render(widget, ranked, input.value.trim());
      });
    }

    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(run, 120);
    });
    input.addEventListener("focus", function () {
      if (normalize(input.value).trim().length >= 2) run();
    });
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") {
        input.blur();
        render(widget, [], "");
      }
      if (ev.key === "Enter") {
        var first = box.querySelector(".temple-search-hit");
        if (first) {
          ev.preventDefault();
          window.location.href = first.getAttribute("href");
        }
      }
    });
    document.addEventListener("click", function (ev) {
      if (!widget.contains(ev.target)) render(widget, [], "");
    });
  }

  widgets.forEach(bind);

  document.addEventListener("keydown", function (ev) {
    var key = (ev.key || "").toLowerCase();
    var mod = ev.metaKey || ev.ctrlKey;
    if (mod && key === "k") {
      ev.preventDefault();
      if (primaryInput) {
        primaryInput.focus();
        primaryInput.select();
      }
    }
  });
})();
