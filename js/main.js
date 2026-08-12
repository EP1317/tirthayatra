(function () {
  // Shuffle story (and any) grids marked for per-visit variety
  document.querySelectorAll("[data-shuffle-children]").forEach(function (grid) {
    var nodes = Array.prototype.slice.call(grid.children);
    if (nodes.length < 2) return;
    for (var i = nodes.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = nodes[i];
      nodes[i] = nodes[j];
      nodes[j] = tmp;
    }
    nodes.forEach(function (el) {
      grid.appendChild(el);
    });
  });

  var toggle = document.querySelector("[data-nav-toggle]");
  var links = document.querySelector("[data-nav-links]");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  var reveals = document.querySelectorAll(".reveal");
  if (!reveals.length || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) {
      el.classList.add("visible");
    });
    return;
  }

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  reveals.forEach(function (el) {
    io.observe(el);
  });
})();
