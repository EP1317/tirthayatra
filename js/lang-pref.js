/**
 * Hindi / English reading preference (localStorage).
 * Pages with data-default-lang="hi" start Hindi-first until the user toggles.
 * Dispatches `tirthayatra:lang` so the Today bar can refresh labels.
 */
(function () {
  var KEY = "tirthayatra-lang";
  var root = document.documentElement;

  function pageDefault() {
    var body = document.body;
    return (body && body.getAttribute("data-default-lang")) || "en";
  }

  function current() {
    try {
      var saved = localStorage.getItem(KEY);
      if (saved === "hi" || saved === "en") return saved;
    } catch (e) {}
    return pageDefault();
  }

  function apply(lang) {
    if (lang !== "hi" && lang !== "en") lang = "en";
    root.setAttribute("data-lang", lang);
    root.classList.toggle("pref-hi", lang === "hi");
    root.classList.toggle("pref-en", lang === "en");
    document.querySelectorAll("[data-lang-toggle]").forEach(function (btn) {
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
    var btn = ev.target.closest("[data-lang-toggle]");
    if (!btn) return;
    ev.preventDefault();
    ev.stopPropagation();
    var lang = btn.getAttribute("data-lang-toggle");
    if (lang !== "hi" && lang !== "en") return;
    window.TirthaLang.set(lang);
  });
})();
