/** Render My Board page from localStorage + embedded catalog. */
(function () {
  var root = document.querySelector("[data-my-board-page]");
  if (!root || !window.TirthaBoard) return;

  var catalog = { temples: {}, festivals: {}, devotion: {}, stories: {}, checklists: {} };
  try {
    catalog = JSON.parse(root.getAttribute("data-catalog") || "{}");
  } catch (e) {}

  var prefix = root.getAttribute("data-prefix") || "";

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function resolve(type, slug) {
    var map = catalog[type] || {};
    var hit = map[slug];
    if (hit) return hit;
    var state = window.TirthaBoard.load();
    var metaKey =
      type === "temples"
        ? "temple:" + slug
        : type === "festivals"
          ? "festival:" + slug
          : type === "devotion"
            ? "devotion:" + slug
            : type === "stories"
              ? "story:" + slug
              : type.replace(/s$/, "") + ":" + slug;
    var meta = (state.meta || {})[metaKey];
    if (meta) return meta;
    return { title: slug, href: "#" };
  }

  function renderList(el, typeKey, itemType, folder) {
    if (!el) return;
    var state = window.TirthaBoard.load();
    var slugs = state[typeKey] || [];
    if (!slugs.length) {
      el.innerHTML = '<p class="comment-empty">Nothing saved yet — tap “Save to My Board” on a guide.</p>';
      return;
    }
    el.innerHTML = slugs
      .map(function (slug) {
        var info = resolve(typeKey, slug);
        var href = info.href || prefix + folder + "/" + slug + ".html";
        return (
          '<div class="board-item"><a href="' +
          escapeHtml(href) +
          '"><strong>' +
          escapeHtml(info.title || slug) +
          '</strong></a><button type="button" class="btn btn-ghost" data-save="' +
          itemType +
          '" data-slug="' +
          escapeHtml(slug) +
          '" data-title="' +
          escapeHtml(info.title || slug) +
          '" data-href="' +
          escapeHtml(href) +
          '" data-label="Save to My Board">Remove</button></div>'
        );
      })
      .join("");
  }

  function renderFestivalChecklists() {
    var host = root.querySelector("[data-board-checklists]");
    if (!host) return;
    var saved = window.TirthaBoard.load().festivals || [];
    var map = catalog.checklists || {};
    var blocks = [];
    saved.forEach(function (festSlug) {
      var info = map[festSlug];
      if (!info || !(info.items || []).length) return;
      var presetId = info.presetId || festSlug;
      var title = info.titleHi || info.title || festSlug;
      var festName = info.festivalName || festSlug;
      var href = info.href || "festivals/" + festSlug + ".html";
      blocks.push(
        '<div class="board-checklist" data-board-checklist-for="' +
          escapeHtml(festSlug) +
          '">' +
          "<h3>" +
          escapeHtml(title) +
          '</h3><p class="engage-note"><a href="' +
          escapeHtml(href) +
          '">' +
          escapeHtml(festName) +
          " guide →</a></p>" +
          '<div data-checklist-preset="' +
          escapeHtml(presetId) +
          '" data-items="' +
          escapeHtml(JSON.stringify(info.items || [])) +
          '"></div></div>'
      );
    });
    if (!blocks.length) {
      host.innerHTML =
        '<p class="comment-empty">No festival checklists yet. Save a festival (Diwali, Holi, Navaratri…) and its checklist appears here. <a href="festivals/checklists.html">Browse all checklists</a>.</p>';
      return;
    }
    host.innerHTML = blocks.join("");
    if (window.TirthaBoard.initChecklistWidgets) {
      window.TirthaBoard.initChecklistWidgets(host);
    }
  }

  function render() {
    renderList(root.querySelector("[data-board-temples]"), "temples", "temple", "temples");
    renderList(root.querySelector("[data-board-festivals]"), "festivals", "festival", "festivals");
    renderList(root.querySelector("[data-board-devotion]"), "devotion", "devotion", "devotion");
    renderList(root.querySelector("[data-board-stories]"), "stories", "story", "stories");
    renderFestivalChecklists();

    var localPop = root.querySelector("[data-board-local-popular]");
    if (localPop) {
      var opens = window.TirthaBoard.load().opens || {};
      var ranked = Object.keys(opens)
        .map(function (k) {
          return { k: k, n: opens[k] };
        })
        .sort(function (a, b) {
          return b.n - a.n;
        })
        .slice(0, 5);
      if (!ranked.length) {
        localPop.innerHTML =
          '<p class="comment-empty">Open a few guides — your on-device favourites will appear here.</p>';
      } else {
        localPop.innerHTML = ranked
          .map(function (r) {
            return (
              "<li>" +
              escapeHtml(r.k) +
              " · opened " +
              r.n +
              "× on this device</li>"
            );
          })
          .join("");
      }
    }

    if (window.TirthaBoard && typeof window.TirthaBoard.load === "function") {
      /* refresh save button labels after list rebuild */
      document.querySelectorAll("[data-save]").forEach(function (btn) {
        var type = btn.getAttribute("data-save");
        var slug = btn.getAttribute("data-slug");
        if (!type || !slug) return;
        var on = window.TirthaBoard.isSaved(type, slug);
        btn.setAttribute("aria-pressed", on ? "true" : "false");
        if (btn.closest(".board-item")) {
          btn.textContent = "Remove";
        } else {
          btn.textContent = on ? "Saved ✓" : btn.getAttribute("data-label") || "Save to My Board";
        }
      });
    }
  }

  root.addEventListener("click", function (ev) {
    if (ev.target.closest("[data-save]")) {
      setTimeout(render, 0);
    }
  });

  render();
})();
