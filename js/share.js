/**
 * WhatsApp / native share / copy-link for devotion, stories, festivals.
 */
(function () {
  function closestShareRoot(el) {
    return el.closest("[data-share]");
  }

  function payload(root) {
    var title = root.getAttribute("data-share-title") || document.title;
    var text = root.getAttribute("data-share-text") || "";
    var url = resolveShareUrl(root.getAttribute("data-share-url"));
    return { title: title, text: text, url: url };
  }

  function resolveShareUrl(raw) {
    var canon = document.querySelector('link[rel="canonical"]');
    if (canon && canon.getAttribute("href")) {
      try {
        return new URL(canon.getAttribute("href"), window.location.origin).href;
      } catch (e) {}
    }
    if (!raw) return window.location.href;
    var s = String(raw).trim();
    try {
      if (/^https?:\/\//i.test(s)) return s;
      // Resolve from site root so nested pages don't become /stories/stories/...
      return new URL("/" + s.replace(/^\/+/, ""), window.location.origin).href;
    } catch (e) {
      return window.location.href;
    }
  }

  function toast(root, msg) {
    var note = root.querySelector("[data-share-note]");
    if (!note) return;
    note.hidden = false;
    note.textContent = msg;
    window.clearTimeout(note._t);
    note._t = window.setTimeout(function () {
      note.hidden = true;
    }, 2200);
  }

  function copyText(str) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(str);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = str;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (err) {
        reject(err);
      }
      document.body.removeChild(ta);
    });
  }

  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest("[data-share-action]");
    if (!btn) return;
    var root = closestShareRoot(btn);
    if (!root) return;
    ev.preventDefault();
    var action = btn.getAttribute("data-share-action");
    var p = payload(root);
    var message = (p.text ? p.text + "\n\n" : "") + p.url;

    if (action === "whatsapp") {
      window.open(
        "https://wa.me/?text=" + encodeURIComponent(message),
        "_blank",
        "noopener,noreferrer"
      );
      return;
    }

    if (action === "copy") {
      copyText(message).then(
        function () {
          toast(root, "Link copied — paste in WhatsApp / chat");
        },
        function () {
          toast(root, "Could not copy — long-press the address bar");
        }
      );
      return;
    }

    if (action === "native") {
      if (navigator.share) {
        navigator
          .share({ title: p.title, text: p.text, url: p.url })
          .catch(function () {});
      } else {
        copyText(message).then(function () {
          toast(root, "Link copied");
        });
      }
    }
  });
})();
