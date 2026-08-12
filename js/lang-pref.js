/**
 * Hindi / English preference for the Today bar only (localStorage).
 * Page body content always shows both languages — this does not hide .lang-hi / .lang-en.
 * Dispatches `tirthayatra:lang` so the Today bar can refresh labels.
 */
(function () {
  var KEY = "tirthayatra-lang";
  var root = document.documentElement;

  function pageDefault() {
    var body = document.body;
    return (body && body.getAttribute("data-default-lang")) || "hi";
  }

  function current() {
    try {
      var saved = localStorage.getItem(KEY);
      if (saved === "hi" || saved === "en") return saved;
    } catch (e) {}
    return pageDefault();
  }

  function apply(lang) {
    if (lang !== "hi" && lang !== "en") lang = "hi";
    root.setAttribute("data-lang", lang);
    root.classList.toggle("pref-hi", lang === "hi");
    root.classList.toggle("pref-en", lang === "en");
    document.querySelectorAll(".today-bar [data-lang-toggle]").forEach(function (btn) {
      var on = btn.getAttribute("data-lang-toggle") === lang;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    try {
      document.dispatchEvent(
        new CustomEvent("tirthayatra:lang", { detail: { lang: lang } })
      );
    } catch (e) {}
  }

  window.TirthaLang = {
    get: current,
    set: function (lang) {
      try {
        localStorage.setItem(KEY, lang);
      } catch (e) {}
      apply(lang);
    },
    apply: apply,
  };

  apply(current());

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest(".today-bar [data-lang-toggle]");
    if (!btn) return;
    ev.preventDefault();
    ev.stopPropagation();
    var lang = btn.getAttribute("data-lang-toggle");
    if (lang !== "hi" && lang !== "en") return;
    window.TirthaLang.set(lang);
  });
})();
