/** Render My Board page from localStorage + embedded catalog. */
(function () {
  var root = document.querySelector("[data-my-board-page]");
  if (!root || !window.TirthaBoard) return;

  var catalog = { temples: {}, festivals: {}, devotion: {}, stories: {} };
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
    var meta = (state.meta || {})[type.replace(/s$/, "") + ":" + slug];
    if (type === "temples") meta = (state.meta || {})["temple:" + slug];
    if (type === "festivals") meta = (state.meta || {})["festival:" + slug];
    if (type === "devotion") meta = (state.meta || {})["devotion:" + slug];
    if (type === "stories") meta = (state.meta || {})["story:" + slug];
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

  function render() {
    renderList(root.querySelector("[data-board-temples]"), "temples", "temple", "temples");
    renderList(root.querySelector("[data-board-festivals]"), "festivals", "festival", "festivals");
    renderList(root.querySelector("[data-board-devotion]"), "devotion", "devotion", "devotion");
    renderList(root.querySelector("[data-board-stories]"), "stories", "story", "stories");

    root.querySelectorAll("[data-checklist-preset]").forEach(function (box) {
      var id = box.getAttribute("data-checklist-preset");
      var items;
      try {
        items = JSON.parse(box.getAttribute("data-items") || "[]");
      } catch (e) {
        items = [];
      }
      var flags = window.TirthaBoard.checklistState(id, items);
      box.innerHTML = items
        .map(function (label, i) {
          return (
            '<label class="board-check"><input type="checkbox" data-check-id="' +
            escapeHtml(id) +
            '" data-check-i="' +
            i +
            '"' +
            (flags[i] ? " checked" : "") +
            " /> " +
            escapeHtml(label) +
            "</label>"
          );
        })
        .join("");
    });

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
  }

  root.addEventListener("change", function (ev) {
    var input = ev.target.closest("input[data-check-id]");
    if (!input) return;
    var id = input.getAttribute("data-check-id");
    var i = Number(input.getAttribute("data-check-i"));
    var box = root.querySelector('[data-checklist-preset="' + id + '"]');
    var len = box ? box.querySelectorAll("input").length : 0;
    window.TirthaBoard.setChecklistItem(id, i, input.checked, len);
  });

  root.addEventListener("click", function (ev) {
    if (ev.target.closest("[data-save]")) {
      setTimeout(render, 0);
    }
  });

  render();
})();
