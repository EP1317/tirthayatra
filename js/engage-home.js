/** Home countdown to next listed festival + optional local popular note. */
(function () {
  var root = document.querySelector("[data-home-engage]");
  if (!root) return;
  var prefix = root.getAttribute("data-prefix") || "";
  var guideMap = {};
  try {
    guideMap = JSON.parse(root.getAttribute("data-guide-map") || "{}");
  } catch (e) {}

  var out = root.querySelector("[data-countdown]");
  if (!out) return;

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }
  function iso(d) {
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }

  fetch(prefix + "data/festivals.json", { credentials: "same-origin" })
    .then(function (r) {
      return r.ok ? r.json() : { fixed: [] };
    })
    .then(function (data) {
      var today = iso(new Date());
      var upcoming = (data.fixed || [])
        .filter(function (f) {
          return f.date >= today && (f.importance === "high" || guideMap[f.name]);
        })
        .sort(function (a, b) {
          return a.date < b.date ? -1 : 1;
        });
      var next = upcoming[0];
      if (!next) {
        out.innerHTML = "<p>Browse the festival calendar for the season ahead.</p>";
        return;
      }
      var t = new Date(next.date + "T12:00:00");
      var now = new Date();
      var days = Math.max(
        0,
        Math.ceil((t - now) / (24 * 60 * 60 * 1000))
      );
      var slug = guideMap[next.name];
      var href = slug
        ? prefix + "festivals/" + slug + ".html"
        : prefix + "festivals/calendar.html";
      var storyHint = "";
      if (slug === "navaratri") {
        storyHint =
          ' · <a href="' +
          prefix +
          'stories/durga-mahishasura.html">Day-1 Devi story</a>';
      } else if (slug === "diwali") {
        storyHint =
          ' · <a href="' +
          prefix +
          'stories/rama-homecoming-lamps.html">Why lamps?</a>';
      } else if (slug === "janmashtami") {
        storyHint =
          ' · <a href="' +
          prefix +
          'stories/krishna-birth-night.html">Midnight meaning</a>';
      }
      out.innerHTML =
        "<p><strong>" +
        (next.nameHi || next.name) +
        "</strong> · " +
        next.name +
        "</p><p class=\"engage-count\">" +
        (days === 0 ? "Listed today" : days + " day(s) to go") +
        ' · <a href="' +
        href +
        '">Open guide</a>' +
        storyHint +
        ' · <a href="' +
        prefix +
        'festivals/calendar.html">Calendar</a></p>' +
        '<p class="engage-note">Home puja tips &amp; stories — confirm exact tithi with your panchang.</p>';
    })
    .catch(function () {
      out.innerHTML = "<p>Open the festival calendar to see what’s ahead.</p>";
    });
})();
