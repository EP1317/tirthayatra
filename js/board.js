/**
 * TirthaYatra My Board — local-first saves, checklists, light streaks, open counts.
 * Nothing is sent to a server (AdSense / privacy friendly — localStorage only).
 */
(function () {
  var KEY = "tirthayatra-board-v1";

  function empty() {
    return {
      temples: [],
      festivals: [],
      devotion: [],
      stories: [],
      checklists: {},
      challenges: {},
      opens: {},
      dailyDone: {},
    };
  }

  function load() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || "null");
      if (!raw || typeof raw !== "object") return empty();
      return Object.assign(empty(), raw);
    } catch (e) {
      return empty();
    }
  }

  function save(state) {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* quota / private mode */
    }
  }

  function bucketFor(type) {
    if (type === "temple") return "temples";
    if (type === "festival") return "festivals";
    if (type === "devotion") return "devotion";
    if (type === "story") return "stories";
    return null;
  }

  function isSaved(type, slug) {
    var b = bucketFor(type);
    if (!b) return false;
    return load()[b].indexOf(slug) !== -1;
  }

  function toggle(type, slug, meta) {
    var b = bucketFor(type);
    if (!b || !slug) return false;
    var state = load();
    var arr = state[b];
    var i = arr.indexOf(slug);
    if (i === -1) {
      arr.unshift(slug);
      if (arr.length > 80) arr.length = 80;
      if (meta && meta.title) {
        state.meta = state.meta || {};
        state.meta[type + ":" + slug] = {
          title: String(meta.title).slice(0, 120),
          href: String(meta.href || "").slice(0, 200),
        };
      }
    } else {
      arr.splice(i, 1);
    }
    save(state);
    return i === -1;
  }

  function recordOpen(type, slug) {
    if (!type || !slug) return;
    var state = load();
    var k = type + ":" + slug;
    state.opens[k] = (state.opens[k] || 0) + 1;
    save(state);
  }

  function challengeProgress(id) {
    var state = load();
    return state.challenges[id] || { done: [], started: null };
  }

  function markChallengeDay(id, dayIndex) {
    var state = load();
    var c = state.challenges[id] || { done: [], started: new Date().toISOString().slice(0, 10) };
    if (c.done.indexOf(dayIndex) === -1) c.done.push(dayIndex);
    state.challenges[id] = c;
    save(state);
    return c;
  }

  function checklistState(presetId, items) {
    var state = load();
    var existing = state.checklists[presetId];
    if (!existing && presetId === "shravan-sawan" && state.checklists.sawan) {
      existing = state.checklists.sawan;
    }
    if (!existing) {
      // Do not persist until the user ticks a box (avoids filling storage with every preset).
      return (items || []).map(function () {
        return false;
      });
    }
    while (existing.length < (items || []).length) existing.push(false);
    return existing;
  }

  function setChecklistItem(presetId, index, value, len) {
    var state = load();
    var arr = state.checklists[presetId] || [];
    while (arr.length < len) arr.push(false);
    arr[index] = !!value;
    state.checklists[presetId] = arr;
    save(state);
  }

  function markDaily(iso) {
    var state = load();
    state.dailyDone[iso] = true;
    save(state);
  }

  function isDailyDone(iso) {
    return !!load().dailyDone[iso];
  }

  window.TirthaBoard = {
    load: load,
    save: save,
    isSaved: isSaved,
    toggle: toggle,
    recordOpen: recordOpen,
    challengeProgress: challengeProgress,
    markChallengeDay: markChallengeDay,
    checklistState: checklistState,
    setChecklistItem: setChecklistItem,
    markDaily: markDaily,
    isDailyDone: isDailyDone,
  };

  function syncButtons(root) {
    (root || document)
      .querySelectorAll("[data-save]")
      .forEach(function (btn) {
        var type = btn.getAttribute("data-save");
        var slug = btn.getAttribute("data-slug");
        if (!type || !slug) return;
        var on = isSaved(type, slug);
        btn.setAttribute("aria-pressed", on ? "true" : "false");
        btn.textContent = on ? "Saved ✓" : btn.getAttribute("data-label") || "Save to My Board";
      });
  }

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-save]");
    if (!btn) return;
    ev.preventDefault();
    var type = btn.getAttribute("data-save");
    var slug = btn.getAttribute("data-slug");
    var title = btn.getAttribute("data-title") || slug;
    var href = btn.getAttribute("data-href") || "";
    var on = toggle(type, slug, { title: title, href: href });
    btn.setAttribute("aria-pressed", on ? "true" : "false");
    btn.textContent = on ? "Saved ✓" : btn.getAttribute("data-label") || "Save to My Board";
  });

  var openEl = document.querySelector("[data-board-open]");
  if (openEl) {
    recordOpen(
      openEl.getAttribute("data-board-open"),
      openEl.getAttribute("data-slug")
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      syncButtons();
      initChecklistWidgets(document);
    });
  } else {
    syncButtons();
    initChecklistWidgets(document);
  }

  function initChecklistWidgets(scope) {
    (scope || document).querySelectorAll("[data-checklist-preset]").forEach(function (box) {
      if (box.getAttribute("data-checklist-ready") === "1") return;
      var id = box.getAttribute("data-checklist-preset");
      var items;
      try {
        items = JSON.parse(box.getAttribute("data-items") || "[]");
      } catch (err) {
        items = [];
      }
      if (!id || !items.length) return;
      var flags = checklistState(id, items);
      box.innerHTML = items
        .map(function (label, i) {
          return (
            '<label class="board-check"><input type="checkbox" data-check-id="' +
            id.replace(/"/g, "") +
            '" data-check-i="' +
            i +
            '"' +
            (flags[i] ? " checked" : "") +
            " /> " +
            String(label)
              .replace(/&/g, "&amp;")
              .replace(/</g, "&lt;")
              .replace(/>/g, "&gt;") +
            "</label>"
          );
        })
        .join("");
      box.setAttribute("data-checklist-ready", "1");
    });
  }

  document.addEventListener("change", function (ev) {
    var input = ev.target.closest("input[data-check-id]");
    if (!input) return;
    var id = input.getAttribute("data-check-id");
    var i = Number(input.getAttribute("data-check-i"));
    var box = document.querySelector('[data-checklist-preset="' + id + '"]');
    var len = box ? box.querySelectorAll("input").length : 0;
    setChecklistItem(id, i, input.checked, len);
  });

  window.TirthaBoard.initChecklistWidgets = initChecklistWidgets;
})();
