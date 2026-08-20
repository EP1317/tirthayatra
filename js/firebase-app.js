/**
 * Shared Firebase bootstrap for TirthaYatra feedback + admin.
 * Config is public (web SDK); security is Auth + Firestore rules.
 */
(function (global) {
  var CFG = global.TIRTHA_FIREBASE || null;
  var app = null;
  var readyPromise = null;

  function configured() {
    return !!(
      CFG &&
      CFG.enabled &&
      CFG.firebase &&
      CFG.firebase.apiKey &&
      CFG.firebase.apiKey !== "REPLACE_ME" &&
      CFG.firebase.projectId &&
      CFG.firebase.projectId !== "YOUR_PROJECT"
    );
  }

  function adminEmails() {
    return (CFG && CFG.adminEmails) || [];
  }

  function isAdminEmail(email) {
    if (!email) return false;
    var list = adminEmails().map(function (e) {
      return String(e).toLowerCase();
    });
    return list.indexOf(String(email).toLowerCase()) !== -1;
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[src="' + src + '"]');
      if (existing) {
        if (existing.getAttribute("data-loaded") === "1") return resolve();
        existing.addEventListener("load", function () {
          resolve();
        });
        existing.addEventListener("error", reject);
        return;
      }
      var s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = function () {
        s.setAttribute("data-loaded", "1");
        resolve();
      };
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function ensureSdk(needAuth) {
    if (!configured()) {
      return Promise.reject(new Error("Firebase is not configured yet."));
    }
    if (readyPromise) return readyPromise;
    var base = "https://www.gstatic.com/firebasejs/10.14.1/";
    readyPromise = loadScript(base + "firebase-app-compat.js")
      .then(function () {
        return loadScript(base + "firebase-firestore-compat.js");
      })
      .then(function () {
        if (needAuth) return loadScript(base + "firebase-auth-compat.js");
      })
      .then(function () {
        if (!global.firebase) throw new Error("Firebase SDK failed to load.");
        if (!app) {
          app = firebase.apps.length
            ? firebase.app()
            : firebase.initializeApp(CFG.firebase);
        }
        return {
          app: app,
          db: firebase.firestore(),
          auth: needAuth ? firebase.auth() : null,
        };
      });
    return readyPromise;
  }

  function resetReady() {
    readyPromise = null;
  }

  global.TirthaFirebase = {
    configured: configured,
    adminEmails: adminEmails,
    isAdminEmail: isAdminEmail,
    ensureSdk: ensureSdk,
    resetReady: resetReady,
    config: function () {
      return CFG;
    },
  };
})(window);
