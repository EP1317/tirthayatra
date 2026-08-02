(function () {
  const root = document.querySelector("#comments");
  if (!root) return;

  const slug = root.getAttribute("data-temple");
  const form = root.querySelector("[data-comment-form]");
  const list = root.querySelector("[data-comment-list]");
  const key = "tirthayatra-comments:" + slug;

  function load() {
    try {
      return JSON.parse(localStorage.getItem(key) || "[]");
    } catch (e) {
      return [];
    }
  }

  function save(items) {
    localStorage.setItem(key, JSON.stringify(items));
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function render() {
    const items = load();
    if (!items.length) {
      list.innerHTML =
        '<p class="comment-empty">No pilgrim notes yet — be the first to leave a respectful tip.</p>';
      return;
    }
    list.innerHTML = items
      .map(function (c) {
        return (
          '<article class="comment-item">' +
          "<header><span class=\"author\">" +
          escapeHtml(c.name || "Anonymous") +
          " · " +
          escapeHtml(String(c.rating)) +
          "/5</span><span class=\"date\">" +
          escapeHtml(c.date) +
          "</span></header>" +
          "<p>" +
          escapeHtml(c.body) +
          "</p></article>"
        );
      })
      .join("");
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    const data = new FormData(form);
    const name = String(data.get("name") || "").trim() || "Anonymous";
    const body = String(data.get("body") || "").trim();
    const rating = String(data.get("rating") || "5");
    if (!body) return;

    const blocked = /(https?:\/\/|buy now|crypto|casino)/i;
    if (blocked.test(body)) {
      alert("Please keep notes spam-free and without promotional links.");
      return;
    }

    const items = load();
    items.unshift({
      name: name.slice(0, 60),
      body: body.slice(0, 800),
      rating: rating,
      date: new Date().toLocaleDateString("en-IN", {
        year: "numeric",
        month: "short",
        day: "numeric",
      }),
    });
    save(items.slice(0, 40));
    form.reset();
    render();
  });

  render();
})();
