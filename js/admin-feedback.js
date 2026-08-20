/**
 * TirthaYatra admin feedback inbox — Google Auth + Firestore.
 * Private editorial triage only. Never renders visitor notes on public pages.
 */
(function () {
  var STATUSES = ["new", "reviewed", "done", "spam"];
  var root = document.querySelector("[data-admin-feedback]");
  if (!root) return;

  function escapeHtml(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function $(sel) {
    return root.querySelector(sel);
  }

  function setGate(mode, detail) {
    var gate = $("[data-admin-gate]");
    var app = $("[data-admin-app]");
    if (!gate || !app) return;
    if (mode === "app") {
      gate.hidden = true;
      app.hidden = false;
    } else {
      gate.hidden = false;
      app.hidden = true;
      var msg = $("[data-admin-gate-msg]");
      if (msg && detail) msg.textContent = detail;
    }
  }

  function typeLabel(id) {
    var map = {
      correction: "Correction",
      "add-detail": "Add detail",
      highlight: "Highlight",
      tip: "Tip",
      question: "Question",
      appreciation: "Appreciation",
    };
    return map[id] || id || "—";
  }

  function fmtDate(ts) {
    if (!ts) return "—";
    try {
      var d = ts.toDate ? ts.toDate() : new Date(ts);
      return d.toISOString().slice(0, 16).replace("T", " ");
    } catch (e) {
      return "—";
    }
  }

  var state = { items: [], filter: "new", api: null, user: null };

  function renderList() {
    var host = $("[data-admin-list]");
    if (!host) return;
    var items = state.items.filter(function (row) {
      if (state.filter === "all") return true;
      return row.status === state.filter;
    });
    if (!items.length) {
      host.innerHTML = '<p class="admin-empty">No feedback in this filter.</p>';
      return;
    }
    host.innerHTML = items
      .map(function (row) {
        var opts = STATUSES.map(function (s) {
          return (
            '<option value="' +
            s +
            '"' +
            (row.status === s ? " selected" : "") +
            ">" +
            s +
            "</option>"
          );
        }).join("");
        return (
          '<article class="admin-card" data-id="' +
          escapeHtml(row.id) +
          '">' +
          '<header class="admin-card-head">' +
          "<div><strong>" +
          escapeHtml(typeLabel(row.type)) +
          '</strong> · <span class="admin-muted">' +
          escapeHtml(fmtDate(row.createdAt)) +
          "</span></div>" +
          '<span class="admin-badge">' +
          escapeHtml(row.status || "new") +
          "</span></header>" +
          '<p class="admin-page"><a href="' +
          escapeHtml(row.href || "#") +
          '" target="_blank" rel="noopener noreferrer">' +
          escapeHtml(row.pageTitle || row.path || "Page") +
          "</a><br /><code>" +
          escapeHtml(row.path || "") +
          "</code></p>" +
          '<p class="admin-note-body">' +
          escapeHtml(row.body || "") +
          "</p>" +
          '<p class="admin-meta">From: ' +
          escapeHtml(row.name || "—") +
          " · " +
          escapeHtml(row.email || "no email") +
          " · " +
          escapeHtml(row.kind || "") +
          "</p>" +
          '<div class="admin-actions">' +
          "<label>Status <select data-status>" +
          opts +
          "</select></label>" +
          '<label>Admin note <input type="text" maxlength="500" data-admin-note value="' +
          escapeHtml(row.adminNote || "") +
          '" placeholder="Internal note (optional)" /></label>' +
          '<button type="button" class="btn btn-primary" data-save>Save</button>' +
          "</div></article>"
        );
      })
      .join("");
  }

  function loadItems() {
    var host = $("[data-admin-list]");
    if (host) host.innerHTML = '<p class="admin-empty">Loading…</p>';
    return state.api.db
      .collection("feedback")
      .orderBy("createdAt", "desc")
      .limit(150)
      .get()
      .then(function (snap) {
        state.items = snap.docs.map(function (doc) {
          var d = doc.data() || {};
          return {
            id: doc.id,
            type: d.type,
            name: d.name,
            email: d.email,
            body: d.body,
            pageTitle: d.pageTitle,
            path: d.path,
            href: d.href,
            kind: d.kind,
            status: d.status || "new",
            adminNote: d.adminNote || "",
            createdAt: d.createdAt,
          };
        });
        renderList();
      })
      .catch(function (err) {
        console.warn(err);
        if (host) {
          host.innerHTML =
            '<p class="admin-empty">Could not load feedback. Check Firestore rules and that your Google account is allowlisted.</p>';
        }
      });
  }

  function onAuth(user) {
    state.user = user;
    if (!user) {
      setGate("gate", "Sign in with Google to open the editorial feedback inbox.");
      $("[data-admin-user]").textContent = "";
      return;
    }
    if (!window.TirthaFirebase.isAdminEmail(user.email)) {
      state.api.auth.signOut();
      setGate(
        "gate",
        "Signed in as " +
          user.email +
          ", but this account is not on the admin allowlist."
      );
      return;
    }
    $("[data-admin-user]").textContent = "Signed in as " + user.email;
    setGate("app");
    loadItems();
  }

  function boot() {
    if (!window.TirthaFirebase || !window.TirthaFirebase.configured()) {
      setGate(
        "gate",
        "Firebase is not enabled yet. Fill data/firebase-public.json (enabled: true + web config), deploy firestore.rules, then rebuild."
      );
      $("[data-admin-signin]").disabled = true;
      return;
    }
    window.TirthaFirebase
      .ensureSdk(true)
      .then(function (api) {
        state.api = api;
        api.auth.onAuthStateChanged(onAuth);
      })
      .catch(function (err) {
        console.warn(err);
        setGate("gate", "Could not load Firebase. Check config and network/CSP.");
      });
  }

  root.addEventListener("click", function (ev) {
    var signIn = ev.target.closest("[data-admin-signin]");
    if (signIn) {
      ev.preventDefault();
      if (!state.api) return;
      var provider = new firebase.auth.GoogleAuthProvider();
      provider.setCustomParameters({ prompt: "select_account" });
      // Redirect avoids COOP/popup blockers on some browsers.
      state.api.auth.signInWithRedirect(provider);
      return;
    }
    var signOut = ev.target.closest("[data-admin-signout]");
    if (signOut) {
      ev.preventDefault();
      if (state.api) state.api.auth.signOut();
      return;
    }
    var save = ev.target.closest("[data-save]");
    if (save) {
      ev.preventDefault();
      var card = save.closest(".admin-card");
      if (!card || !state.api) return;
      var id = card.getAttribute("data-id");
      var status = card.querySelector("[data-status]").value;
      var note = card.querySelector("[data-admin-note]").value.slice(0, 500);
      save.disabled = true;
      state.api.db
        .collection("feedback")
        .doc(id)
        .update({
          status: status,
          adminNote: note,
          updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
        })
        .then(function () {
          var row = state.items.find(function (x) {
            return x.id === id;
          });
          if (row) {
            row.status = status;
            row.adminNote = note;
          }
          renderList();
        })
        .catch(function (err) {
          console.warn(err);
          alert("Could not save. Check Firestore rules / admin email.");
        })
        .finally(function () {
          save.disabled = false;
        });
    }
  });

  root.addEventListener("change", function (ev) {
    if (ev.target.matches("[data-admin-filter]")) {
      state.filter = ev.target.value;
      renderList();
    }
  });

  // Finish redirect sign-in if present.
  if (window.TirthaFirebase && window.TirthaFirebase.configured()) {
    window.TirthaFirebase.ensureSdk(true).then(function (api) {
      state.api = api;
      return api.auth.getRedirectResult().catch(function () {});
    }).finally(boot);
  } else {
    boot();
  }
})();
