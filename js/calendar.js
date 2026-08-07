/**
 * Festival calendar — month grid, next 30 days, shareable plain-text cards.
 */
(function () {
  var root = document.querySelector("[data-festival-calendar]");
  if (!root) return;

  var prefix = root.getAttribute("data-prefix") || "";
  var guideMap = {};
  try {
    guideMap = JSON.parse(root.getAttribute("data-guide-map") || "{}");
  } catch (e) {
    guideMap = {};
  }

  var monthEl = root.querySelector("[data-cal-month]");
  var nextEl = root.querySelector("[data-cal-next]");
  var labelEl = root.querySelector("[data-cal-label]");
  var prevBtn = root.querySelector("[data-cal-prev]");
  var nextBtn = root.querySelector("[data-cal-next-btn]");
  var shareBox = root.querySelector("[data-cal-share]");

  var cursor = new Date();
  cursor.setDate(1);
  cursor.setHours(12, 0, 0, 0);
  var fixed = [];

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function iso(d) {
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function guideHref(name) {
    var slug = guideMap[name];
    return slug ? prefix + "festivals/" + slug + ".html" : "";
  }

  function eventsOn(dayIso) {
    return fixed.filter(function (f) {
      return f.date === dayIso;
    });
  }

  function renderMonth() {
    if (!monthEl || !labelEl) return;
    var y = cursor.getFullYear();
    var m = cursor.getMonth();
    labelEl.textContent = cursor.toLocaleString("en-IN", {
      month: "long",
      year: "numeric",
    });
    var firstDow = new Date(y, m, 1).getDay();
    var daysInMonth = new Date(y, m + 1, 0).getDate();
    var html =
      '<div class="cal-dow">' +
      ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        .map(function (d) {
          return "<span>" + d + "</span>";
        })
        .join("") +
      "</div><div class=\"cal-grid\">";
    for (var i = 0; i < firstDow; i++) html += '<div class="cal-cell cal-empty"></div>';
    for (var day = 1; day <= daysInMonth; day++) {
      var d = new Date(y, m, day, 12);
      var id = iso(d);
      var evs = eventsOn(id);
      var cls = "cal-cell" + (evs.length ? " cal-has" : "");
      html += '<div class="' + cls + '" data-iso="' + id + '">';
      html += '<span class="cal-daynum">' + day + "</span>";
      evs.slice(0, 2).forEach(function (ev) {
        var href = guideHref(ev.name);
        var label = escapeHtml(ev.nameHi || ev.name);
        if (href) {
          html +=
            '<a class="cal-pill" href="' +
            escapeHtml(href) +
            '">' +
            label +
            "</a>";
        } else {
          html += '<span class="cal-pill cal-pill-muted">' + label + "</span>";
        }
      });
      if (evs.length > 2) {
        html += '<span class="cal-more">+' + (evs.length - 2) + "</span>";
      }
      html += "</div>";
    }
    html += "</div>";
    monthEl.innerHTML = html;
  }

  function renderNext30() {
    if (!nextEl) return;
    var start = new Date();
    start.setHours(12, 0, 0, 0);
    var end = new Date(start);
    end.setDate(end.getDate() + 30);
    var startIso = iso(start);
    var endIso = iso(end);
    var upcoming = fixed
      .filter(function (f) {
        return f.date >= startIso && f.date <= endIso;
      })
      .sort(function (a, b) {
        return a.date < b.date ? -1 : 1;
      });
    if (!upcoming.length) {
      nextEl.innerHTML =
        '<p class="comment-empty">No listed festivals in the next 30 days — browse all guides below.</p>';
      return;
    }
    nextEl.innerHTML = upcoming
      .map(function (ev) {
        var href = guideHref(ev.name);
        var title = escapeHtml(ev.nameHi || ev.name);
        var en = escapeHtml(ev.name);
        var shareBtn =
          '<button type="button" class="btn btn-ghost cal-share-btn" data-share-fest' +
          ' data-name="' +
          escapeHtml(ev.name) +
          '" data-name-hi="' +
          escapeHtml(ev.nameHi || "") +
          '" data-date="' +
          escapeHtml(ev.date) +
          '" data-href="' +
          escapeHtml(href || prefix + "festivals/index.html") +
          '">Share card</button>';
        var link = href
          ? '<a class="cal-next-title" href="' +
            escapeHtml(href) +
            '">' +
            title +
            " · " +
            en +
            "</a>"
          : '<span class="cal-next-title">' + title + " · " + en + "</span>";
        return (
          '<article class="cal-next-card">' +
          '<p class="cal-next-date">' +
          escapeHtml(ev.date) +
          "</p>" +
          link +
          shareBtn +
          "</article>"
        );
      })
      .join("");
  }

  function shareText(name, nameHi, date, href) {
    var abs =
      href && href.indexOf("http") === 0
        ? href
        : window.location.origin +
          "/" +
          String(href || "").replace(/^\.\.\//, "").replace(/^\//, "");
    return (
      (nameHi ? nameHi + " · " : "") +
      name +
      "\nDate (listed): " +
      date +
      "\nMeaning & home puja tips: " +
      abs +
      "\n— TirthaYatra (informational; confirm with your panchang)"
    );
  }

  root.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-share-fest]");
    if (!btn) return;
    var text = shareText(
      btn.getAttribute("data-name"),
      btn.getAttribute("data-name-hi"),
      btn.getAttribute("data-date"),
      btn.getAttribute("data-href")
    );
    if (shareBox) {
      shareBox.hidden = false;
      shareBox.querySelector("[data-share-text]").value = text;
    }
    if (navigator.share) {
      navigator.share({ text: text }).catch(function () {});
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "Copied ✓";
        setTimeout(function () {
          btn.textContent = "Share card";
        }, 1600);
      });
    }
  });

  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      cursor.setMonth(cursor.getMonth() - 1);
      renderMonth();
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      cursor.setMonth(cursor.getMonth() + 1);
      renderMonth();
    });
  }

  var copyBtn = root.querySelector("[data-share-copy]");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      var ta = root.querySelector("[data-share-text]");
      if (!ta) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(ta.value).then(function () {
          copyBtn.textContent = "Copied ✓";
        });
      } else {
        ta.select();
        document.execCommand("copy");
        copyBtn.textContent = "Copied ✓";
      }
    });
  }

  fetch(prefix + "data/festivals.json", { credentials: "same-origin" })
    .then(function (r) {
      if (!r.ok) throw new Error("missing");
      return r.json();
    })
    .then(function (data) {
      fixed = data.fixed || [];
      renderMonth();
      renderNext30();
    })
    .catch(function () {
      if (monthEl) {
        monthEl.innerHTML =
          '<p class="comment-empty">Could not load festival dates.</p>';
      }
    });
})();
