(function () {
  const toggle = document.querySelector("[data-nav-toggle]");
  const links = document.querySelector("[data-nav-links]");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  const reveals = document.querySelectorAll(".reveal");
  if (!reveals.length || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) {
      el.classList.add("visible");
    });
    return;
  }

  const io = new IntersectionObserver(
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
