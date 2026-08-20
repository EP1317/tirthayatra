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

  var state = {
    items: [],
    filter: "new",
    api: null,
    user: null,
    gateDetail: "",
    rejecting: false,
  };

  function setGate(mode, detail) {
    var gate = $("[data-admin-gate]");
    var app = $("[data-admin-app]");
    if (!gate || !app) return;
    if (mode === "app") {
      gate.hidden = true;
      app.hidden = false;
      return;
    }
    gate.hidden = false;
    app.hidden = true;
    if (detail) state.gateDetail = detail;
    var msg = $("[data-admin-gate-msg]");
    if (msg && state.gateDetail) msg.textContent = state.gateDetail;
  }

  function allowedHint() {
    var list = (window.TirthaFirebase && window.TirthaFirebase.adminEmails()) || [];
    return list.length ? list.join(", ") : "TirthaYatraOnline@gmail.com";
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

  function googleProvider() {
    var provider = new firebase.auth.GoogleAuthProvider();
    provider.setCustomParameters({ prompt: "select_account" });
    provider.addScope("email");
    return provider;
  }

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
            '<p class="admin-empty">Could not load feedback (' +
            escapeHtml(err && err.code ? err.code : "error") +
            "). Check Firestore rules and that Google Auth is enabled.</p>";
        }
      });
  }

  function onAuth(user) {
    state.user = user;
    var userEl = $("[data-admin-user]");
    if (!user) {
      if (userEl) userEl.textContent = "";
      // Keep rejection / error text if we just blocked a non-admin.
      if (!state.gateDetail) {
        state.gateDetail =
          "Sign in with Google using " +
          allowedHint() +
          " to open the editorial feedback inbox.";
      }
      setGate("gate");
      return;
    }

    if (!window.TirthaFirebase.isAdminEmail(user.email)) {
      state.rejecting = true;
      state.gateDetail =
        "Signed in as " +
        user.email +
        ", but only these admin emails can open the inbox: " +
        allowedHint() +
        ". Click Sign in again and choose the allowlisted account.";
      setGate("gate");
      if (userEl) userEl.textContent = "Blocked: " + user.email;
      state.api.auth.signOut().finally(function () {
        state.rejecting = false;
      });
      return;
    }

    state.gateDetail = "";
    if (userEl) userEl.textContent = "Signed in as " + user.email;
    setGate("app");
    loadItems();
  }

  function boot() {
    if (!window.TirthaFirebase || !window.TirthaFirebase.configured()) {
      state.gateDetail =
        "Firebase is not enabled yet. Fill data/firebase-public.json, deploy firestore.rules, then rebuild.";
      setGate("gate");
      var btn = $("[data-admin-signin]");
      if (btn) btn.disabled = true;
      return;
    }

    var allowEl = $("[data-admin-allowlist]");
    if (allowEl) allowEl.textContent = "Allowed admin: " + allowedHint();

    window.TirthaFirebase
      .ensureSdk(true)
      .then(function (api) {
        state.api = api;
        return api.auth.getRedirectResult().catch(function (err) {
          if (err && err.code && err.code !== "auth/redirect-cancelled-by-user") {
            state.gateDetail =
              "Google sign-in failed (" +
              err.code +
              "). Try again, or use a different browser profile.";
            setGate("gate");
          }
        });
      })
      .then(function () {
        state.api.auth.onAuthStateChanged(onAuth);
      })
      .catch(function (err) {
        console.warn(err);
        state.gateDetail =
          "Could not load Firebase. Check config, network, and that Authentication → Google is enabled.";
        setGate("gate");
      });
  }

  function startSignIn() {
    if (!state.api) return;
    state.gateDetail = "Opening Google sign-in… choose " + allowedHint();
    setGate("gate");
    var provider = googleProvider();
    // Prefer popup; fall back to redirect if popup blocked.
    state.api.auth
      .signInWithPopup(provider)
      .catch(function (err) {
        console.warn("popup sign-in failed", err);
        if (
          err &&
          (err.code === "auth/popup-blocked" ||
            err.code === "auth/popup-closed-by-user" ||
            err.code === "auth/cancelled-popup-request")
        ) {
          state.gateDetail = "Popup blocked or closed — redirecting to Google…";
          setGate("gate");
          return state.api.auth.signInWithRedirect(provider);
        }
        state.gateDetail =
          "Google sign-in failed" +
          (err && err.code ? " (" + err.code + ")" : "") +
          ". Confirm Authentication → Google is enabled and Authorized domains include www.tirthayatraonline.in.";
        setGate("gate");
      });
  }

  root.addEventListener("click", function (ev) {
    var signIn = ev.target.closest("[data-admin-signin]");
    if (signIn) {
      ev.preventDefault();
      startSignIn();
      return;
    }
    var signOut = ev.target.closest("[data-admin-signout]");
    if (signOut) {
      ev.preventDefault();
      state.gateDetail =
        "Signed out. Sign in with Google using " + allowedHint() + ".";
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

  boot();
})();
