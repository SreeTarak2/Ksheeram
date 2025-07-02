document.addEventListener("DOMContentLoaded", () => {

  // --- Scroll to Top Button ---
  const scrollTopBtn = document.querySelector(".scroll-top-btn");
  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      scrollTopBtn.classList.add("visible");
    } else {
      scrollTopBtn.classList.remove("visible");
    }
  });

  // --- Modal Management ---
  const loginBtn = document.getElementById("login-btn");
  const signupBtn = document.getElementById("signup-btn");
  const loginModal = document.getElementById("login-modal");
  const registerModal = document.getElementById("register-modal");
  const allModals = document.querySelectorAll(".modal-overlay");

  const openModal = (modal) => modal?.classList.add("active");
  const closeModal = (modal) => modal?.classList.remove("active");

  loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    openModal(loginModal);
  });
  signupBtn.addEventListener("click", (e) => {
    e.preventDefault();
    openModal(registerModal);
  });

  allModals.forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (
        e.target === modal ||
        e.target.classList.contains("modal-close-btn")
      ) {
        closeModal(modal);
      }
    });
  });

  // Switch between modals
  document
    .getElementById("switch-to-register")
    .addEventListener("click", (e) => {
      e.preventDefault();
      closeModal(loginModal);
      openModal(registerModal);
    });
  document.getElementById("switch-to-login").addEventListener("click", (e) => {
    e.preventDefault();
    closeModal(registerModal);
    openModal(loginModal);
  });

  // --- Modal Form Navigation (Role Selection) ---
  const setupRoleInteractions = (modal) => {
    const roleSelectionContainer = modal.querySelector(".modal-form-container");
    modal.querySelectorAll(".modal-btn-role").forEach((button) => {
      button.addEventListener("click", (e) => {
        const role = e.target.dataset.role;
        const modalType = modal.id.split("-")[0];
        const formContainer = modal.querySelector(
          `#${role}-${modalType}-form-container`
        );
        if (formContainer) {
          roleSelectionContainer.classList.add("hidden");
          formContainer.classList.remove("hidden");
        }
      });
    });
    modal.querySelectorAll(".modal-back-link").forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        link.closest(".modal-form-container").classList.add("hidden");
        roleSelectionContainer.classList.remove("hidden");
      });
    });
  };
  setupRoleInteractions(loginModal);
  setupRoleInteractions(registerModal);
});