/**
 * TirthaYatra feedback — private editorial inbox (Firestore).
 * Notes are NEVER published live automatically (AdSense / UGC-safe).
 * Optional: save a personal copy in localStorage on this device.
 * Mailto remains a fallback if Firebase is not configured.
 */
(function () {
  var EMAIL = "TirthaYatraOnline@gmail.com";
  var STORE_KEY = "tirthayatra-feedback-v1";
  var RATE_KEY = "tirthayatra-feedback-rate";
  var RATE_MS = 45000;
  var TYPES = [
    { id: "correction", label: "Correction", hint: "Something inaccurate or outdated" },
    { id: "add-detail", label: "Add detail", hint: "Useful info we should include" },
    { id: "highlight", label: "Highlight", hint: "A point worth featuring" },
    { id: "tip", label: "Home / visit tip", hint: "Practical note for others (reviewed before any public use)" },
    { id: "question", label: "Question", hint: "Ask about this page" },
    { id: "appreciation", label: "Appreciation", hint: "What helped you" },
  ];

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function loadAll() {
    try {
      return JSON.parse(localStorage.getItem(STORE_KEY) || "[]");
    } catch (e) {
      return [];
    }
  }

  function saveAll(items) {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(items.slice(0, 80)));
    } catch (e) {}
  }

  function pageMeta() {
    var title = document.title.replace(/\s*[—–-]\s*TirthaYatra.*$/i, "").trim();
    var path = window.location.pathname || "/";
    var kind = "page";
    if (path.indexOf("/temples/") !== -1) kind = "temple";
    else if (path.indexOf("/festivals/") !== -1) kind = "festival";
    else if (path.indexOf("/stories/") !== -1) kind = "story";
    else if (path.indexOf("/devotion/") !== -1) kind = "devotion";
    return { title: title || "TirthaYatra", path: path, href: window.location.href, kind: kind };
  }

  function spammy(text) {
    return /(https?:\/\/|www\.|buy now|crypto|casino|viagra|loan\s*approved)/i.test(text);
  }

  function rateLimited() {
    try {
      var last = parseInt(localStorage.getItem(RATE_KEY) || "0", 10);
      return last && Date.now() - last < RATE_MS;
    } catch (e) {
      return false;
    }
  }

  function markRate() {
    try {
      localStorage.setItem(RATE_KEY, String(Date.now()));
    } catch (e) {}
  }

  function firebaseReady() {
    return window.TirthaFirebase && window.TirthaFirebase.configured();
  }

  function ensureUi() {
    if (document.querySelector("[data-feedback-root]")) return;

    var typeOptions = TYPES.map(function (t) {
      return (
        '<option value="' +
        escapeHtml(t.id) +
        '">' +
        escapeHtml(t.label) +
        " — " +
        escapeHtml(t.hint) +
        "</option>"
      );
    }).join("");

    var primaryLabel = firebaseReady() ? "Send feedback" : "Email to TirthaYatra";

    var wrap = document.createElement("div");
    wrap.setAttribute("data-feedback-root", "1");
    wrap.innerHTML =
      '<button type="button" class="feedback-fab" data-feedback-open aria-haspopup="dialog">' +
      "Feedback" +
      "</button>" +
      '<div class="feedback-backdrop" data-feedback-backdrop hidden></div>' +
      '<div class="feedback-panel" data-feedback-panel role="dialog" aria-modal="true" aria-labelledby="feedback-title" hidden>' +
      '<div class="feedback-panel-head">' +
      '<h2 id="feedback-title">Improve this page</h2>' +
      '<button type="button" class="feedback-close" data-feedback-close aria-label="Close">×</button>' +
      "</div>" +
      '<p class="feedback-lede">Suggest a correction, add a detail, or highlight something useful. Notes go to TirthaYatra editors only — they are <strong>not published live automatically</strong> (content quality and ad-policy safety).</p>' +
      '<p class="feedback-page" data-feedback-page-label></p>' +
      '<form class="feedback-form" data-feedback-form>' +
      '<label class="feedback-hp" aria-hidden="true">Company<input name="company" tabindex="-1" autocomplete="off" /></label>' +
      '<label>Type<select name="type" required>' +
      typeOptions +
      "</select></label>" +
      '<label>Your name <span class="opt">(optional)</span><input name="name" maxlength="60" autocomplete="name" placeholder="Name" /></label>' +
      '<label>Email <span class="opt">(optional, for follow-up)</span><input name="email" type="email" maxlength="120" autocomplete="email" placeholder="you@example.com" /></label>' +
      '<label>Your note<textarea name="body" required maxlength="1200" rows="5" placeholder="What should we correct, add, or highlight? Be specific — section name, timing, story detail…"></textarea></label>' +
      '<div class="feedback-actions">' +
      '<button type="submit" class="btn btn-primary" data-feedback-submit>' +
      escapeHtml(primaryLabel) +
      "</button>" +
      '<button type="button" class="btn btn-ghost" data-feedback-local>Save copy on this device</button>' +
      "</div>" +
      '<p class="feedback-status" data-feedback-status hidden></p>' +
      "</form>" +
      '<div class="feedback-local">' +
      "<h3>Your notes on this page (this device)</h3>" +
      '<div data-feedback-local-list></div>' +
      "</div>" +
      "</div>";
    document.body.appendChild(wrap);
  }

  function openPanel(presetType) {
    ensureUi();
    var panel = document.querySelector("[data-feedback-panel]");
    var backdrop = document.querySelector("[data-feedback-backdrop]");
    var meta = pageMeta();
    var label = document.querySelector("[data-feedback-page-label]");
    if (label) {
      label.textContent = "Page: " + meta.title + " · " + meta.path;
    }
    var form = document.querySelector("[data-feedback-form]");
    if (form && presetType) {
      var sel = form.querySelector('[name="type"]');
      if (sel) sel.value = presetType;
    }
    if (panel) panel.hidden = false;
    if (backdrop) backdrop.hidden = false;
    document.body.classList.add("feedback-open");
    renderLocal();
    var ta = form && form.querySelector('[name="body"]');
    if (ta) ta.focus();
  }

  function closePanel() {
    var panel = document.querySelector("[data-feedback-panel]");
    var backdrop = document.querySelector("[data-feedback-backdrop]");
    if (panel) panel.hidden = true;
    if (backdrop) backdrop.hidden = true;
    document.body.classList.remove("feedback-open");
  }

  function collect(form) {
    var data = new FormData(form);
    var meta = pageMeta();
    return {
      type: String(data.get("type") || "tip"),
      name: String(data.get("name") || "").trim().slice(0, 60),
      email: String(data.get("email") || "").trim().slice(0, 120),
      body: String(data.get("body") || "").trim().slice(0, 1200),
      company: String(data.get("company") || "").trim(),
      pageTitle: meta.title.slice(0, 200),
      path: meta.path.slice(0, 300),
      href: meta.href.slice(0, 500),
      kind: meta.kind.slice(0, 40),
      date: new Date().toISOString(),
    };
  }

  function typeLabel(id) {
    for (var i = 0; i < TYPES.length; i++) {
      if (TYPES[i].id === id) return TYPES[i].label;
    }
    return id;
  }

  function buildMailto(item) {
    var subject = encodeURIComponent(
      "[TirthaYatra feedback] " + typeLabel(item.type) + " · " + item.pageTitle
    );
    var lines = [
      "Type: " + typeLabel(item.type),
      "Page: " + item.pageTitle,
      "URL: " + item.href,
      "Path: " + item.path,
      "Kind: " + item.kind,
      "Name: " + (item.name || "(not given)"),
      "Email: " + (item.email || "(not given)"),
      "",
      "Note:",
      item.body,
      "",
      "— Sent via TirthaYatra feedback form (for editorial review)",
    ];
    var body = encodeURIComponent(lines.join("\n")).slice(0, 1800);
    return "mailto:" + EMAIL + "?subject=" + subject + "&body=" + body;
  }

  function setStatus(msg, ok) {
    var el = document.querySelector("[data-feedback-status]");
    if (!el) return;
    el.hidden = false;
    el.textContent = msg;
    el.classList.toggle("ok", !!ok);
  }

  function renderLocal() {
    var list = document.querySelector("[data-feedback-local-list]");
    if (!list) return;
    var meta = pageMeta();
    var items = loadAll().filter(function (x) {
      return x.path === meta.path;
    });
    if (!items.length) {
      list.innerHTML =
        '<p class="comment-empty">No local copies on this page yet.</p>';
      return;
    }
    list.innerHTML = items
      .map(function (c) {
        var tag = c.sent ? " · sent for review" : c.emailed ? " · emailed" : " · local only";
        return (
          '<article class="feedback-item">' +
          "<header><span>" +
          escapeHtml(typeLabel(c.type)) +
          tag +
          '</span><span class="date">' +
          escapeHtml((c.date || "").slice(0, 10)) +
          "</span></header>" +
          "<p>" +
          escapeHtml(c.body) +
          "</p></article>"
        );
      })
      .join("");
  }

  function persist(item, flags) {
    var all = loadAll();
    item.emailed = !!(flags && flags.emailed);
    item.sent = !!(flags && flags.sent);
    all.unshift(item);
    saveAll(all);
    renderLocal();
    renderInlineLists();
  }

  function renderInlineLists() {
    document.querySelectorAll("[data-feedback-inline-list]").forEach(function (list) {
      var path = list.getAttribute("data-path") || pageMeta().path;
      var items = loadAll().filter(function (x) {
        return x.path === path;
      });
      if (!items.length) {
        list.innerHTML =
          '<p class="comment-empty">Your notes for this page appear here on this device after you save or send.</p>';
        return;
      }
      list.innerHTML = items
        .map(function (c) {
          var tag = c.sent ? " · sent for review" : c.emailed ? " · emailed" : " · saved locally";
          return (
            '<article class="feedback-item">' +
            "<header><span>" +
            escapeHtml(typeLabel(c.type)) +
            tag +
            "</span></header><p>" +
            escapeHtml(c.body) +
            "</p></article>"
          );
        })
        .join("");
    });
  }

  function validateItem(item) {
    if (item.company) {
      setStatus("Could not send. Please try again.", false);
      return false;
    }
    if (!item.body || item.body.length < 3) {
      setStatus("Please write a short note first.", false);
      return false;
    }
    if (spammy(item.body)) {
      setStatus("Please keep notes spam-free and without promotional links.", false);
      return false;
    }
    if (rateLimited()) {
      setStatus("Please wait a moment before sending another note.", false);
      return false;
    }
    return true;
  }

  function submitToFirestore(item, submitBtn) {
    if (!window.TirthaFirebase) {
      return Promise.reject(new Error("Firebase helper missing"));
    }
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending…";
    }
    return window.TirthaFirebase.ensureSdk(false).then(function (api) {
      var payload = {
        type: item.type,
        name: item.name || "",
        email: item.email || "",
        body: item.body,
        pageTitle: item.pageTitle,
        path: item.path,
        href: item.href,
        kind: item.kind,
        status: "new",
        adminNote: "",
        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        ua: String(navigator.userAgent || "").slice(0, 180),
      };
      return api.db.collection("feedback").add(payload);
    });
  }

  document.addEventListener("click", function (ev) {
    var openBtn = ev.target.closest("[data-feedback-open]");
    if (openBtn) {
      ev.preventDefault();
      var preset =
        openBtn.getAttribute("data-type") ||
        openBtn.getAttribute("data-feedback-open") ||
        "";
      if (preset === "true" || preset === "1") preset = "";
      openPanel(preset);
      return;
    }
    if (ev.target.closest("[data-feedback-close], [data-feedback-backdrop]")) {
      closePanel();
      return;
    }
    var localBtn = ev.target.closest("[data-feedback-local]");
    if (localBtn) {
      ev.preventDefault();
      var form = document.querySelector("[data-feedback-form]");
      if (!form) return;
      var item = collect(form);
      if (!validateItem(item)) return;
      persist(item, {});
      setStatus(
        firebaseReady()
          ? "Saved on this device. Use “Send feedback” so editors receive it."
          : "Saved on this device. Use “Email to TirthaYatra” so editors can review it.",
        true
      );
    }
  });

  document.addEventListener("submit", function (ev) {
    var form = ev.target.closest("[data-feedback-form]");
    if (!form) return;
    ev.preventDefault();
    var item = collect(form);
    if (!validateItem(item)) return;
    var submitBtn = form.querySelector("[data-feedback-submit]");

    if (!firebaseReady()) {
      persist(item, { emailed: true });
      markRate();
      setStatus("Opening your email app… Editors review before anything goes public.", true);
      window.location.href = buildMailto(item);
      return;
    }

    submitToFirestore(item, submitBtn)
      .then(function () {
        markRate();
        persist(item, { sent: true });
        form.querySelector('[name="body"]').value = "";
        setStatus(
          "Thank you — your note reached TirthaYatra editors. It will not appear on the site automatically.",
          true
        );
      })
      .catch(function (err) {
        console.warn("feedback send failed", err);
        setStatus(
          "Could not send right now. You can retry, or email " + EMAIL + ".",
          false
        );
      })
      .finally(function () {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Send feedback";
        }
      });
  });

  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") closePanel();
  });

  ensureUi();
  renderInlineLists();
})();
