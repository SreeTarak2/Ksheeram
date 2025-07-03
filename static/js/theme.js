document.addEventListener("DOMContentLoaded", () => {
  const themeToggleCheckbox = document.getElementById("theme-toggle-checkbox");
  const rootElement = document.documentElement;

  if (!themeToggleCheckbox) {
    const savedTheme = localStorage.getItem("theme") || "dark";
    rootElement.setAttribute("data-theme", savedTheme);
    return;
  }

  const applyTheme = (theme) => {
    rootElement.setAttribute("data-theme", theme);
    themeToggleCheckbox.checked = theme === "dark";
  };

  const handleThemeChange = () => {
    const isDark = themeToggleCheckbox.checked;
    const newTheme = isDark ? "dark" : "light";
    applyTheme(newTheme);
    localStorage.setItem("theme", newTheme);
  };

  themeToggleCheckbox.addEventListener("change", handleThemeChange);

  const savedTheme = localStorage.getItem("theme") || "dark";
  applyTheme(savedTheme);

  const currentPagePath = window.location.pathname;
  const navLinks = document.querySelectorAll(".main-nav .nav-link");

  navLinks.forEach((link) => {
    const linkPath = new URL(link.href).pathname;
    if (currentPagePath === linkPath) {
      link.classList.add("active");
    }
  });

  document.getElementById("hamburger").addEventListener("click", function () {
    document.querySelector(".main-nav").classList.toggle("show");
  });
});
