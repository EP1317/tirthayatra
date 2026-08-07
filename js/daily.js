/**
 * Daily habit: tithi chip + rotating aarti / katha / story + challenge check-ins.
 */
(function () {
  var root = document.querySelector("[data-daily-practice]");
  if (!root) return;

  var prefix = root.getAttribute("data-prefix") || "";
  var rotation = { aarti: [], katha: [], story: [] };
  try {
    rotation = JSON.parse(root.getAttribute("data-rotation") || "{}");
  } catch (e) {}

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function istIso(d) {
    var fmt = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Kolkata",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
    return fmt.format(d);
  }

  function dayIndex(iso) {
    var parts = iso.split("-").map(Number);
    var utc = Date.UTC(parts[0], parts[1] - 1, parts[2]);
    return Math.floor(utc / 86400000);
  }

  function pick(list, iso) {
    if (!list || !list.length) return null;
    return list[dayIndex(iso) % list.length];
  }

  function hrefFor(kind, slug) {
    if (!slug) return "#";
    if (kind === "story") return prefix + "stories/" + slug + ".html";
    return prefix + "devotion/" + slug + ".html";
  }

  var iso = istIso(new Date());
  var aarti = pick(rotation.aarti, iso);
  var katha = pick(rotation.katha, iso);
  var story = pick(rotation.story, iso);

  var slots = root.querySelector("[data-daily-slots]");
  if (slots) {
    var cards = [
      {
        kicker: "आज की आरती · Today's aarti",
        slug: aarti,
        kind: "aarti",
        cta: "Open aarti",
      },
      {
        kicker: "व्रत कथा · Short katha",
        slug: katha,
        kind: "katha",
        cta: "Open katha",
      },
      {
        kicker: "कथा · 60–90 sec story",
        slug: story,
        kind: "story",
        cta: "Read story",
      },
    ];
    slots.innerHTML = cards
      .map(function (c) {
        if (!c.slug) return "";
        var href = hrefFor(c.kind === "story" ? "story" : "devotion", c.slug);
        var label = c.slug.replace(/-/g, " ");
        return (
          '<article class="daily-card">' +
          '<p class="daily-kicker">' +
          c.kicker +
          "</p>" +
          "<h3>" +
          label +
          "</h3>" +
          '<a class="btn btn-primary" href="' +
          href +
          '">' +
          c.cta +
          "</a>" +
          "</article>"
        );
      })
      .join("");
  }

  var dateEl = root.querySelector("[data-daily-date]");
  if (dateEl) dateEl.textContent = iso + " (IST)";

  var doneBtn = root.querySelector("[data-daily-done]");
  var doneNote = root.querySelector("[data-daily-done-note]");
  function refreshDone() {
    if (!window.TirthaBoard || !doneBtn) return;
    var done = window.TirthaBoard.isDailyDone(iso);
    doneBtn.disabled = done;
    doneBtn.textContent = done ? "Marked for today ✓" : "Mark today’s practice done";
    if (doneNote) {
      doneNote.hidden = !done;
    }
  }
  if (doneBtn) {
    doneBtn.addEventListener("click", function () {
      if (!window.TirthaBoard) return;
      window.TirthaBoard.markDaily(iso);
      refreshDone();
    });
    refreshDone();
  }

  root.querySelectorAll("[data-challenge-mark]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!window.TirthaBoard) return;
      var id = btn.getAttribute("data-challenge-mark");
      var day = Number(btn.getAttribute("data-day") || "0");
      var prog = window.TirthaBoard.markChallengeDay(id, day);
      var wrap = root.querySelector('[data-challenge-progress="' + id + '"]');
      if (wrap) {
        wrap.textContent = prog.done.length + " day(s) marked on this device";
      }
      btn.textContent = "Marked ✓";
    });
  });

  root.querySelectorAll("[data-challenge-progress]").forEach(function (el) {
    if (!window.TirthaBoard) return;
    var id = el.getAttribute("data-challenge-progress");
    var prog = window.TirthaBoard.challengeProgress(id);
    el.textContent = (prog.done || []).length
      ? prog.done.length + " day(s) marked on this device"
      : "No days marked yet";
  });
})();
