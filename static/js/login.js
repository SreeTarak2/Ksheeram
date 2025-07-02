document.addEventListener("DOMContentLoaded", () => {
  // Elements for Role Selection and Forms
  const roleSelection = document.getElementById("login-role-selection");
  const buyerLoginFormContainer = document.getElementById(
    "buyer-login-form-container"
  );
  const sellerLoginFormContainer = document.getElementById(
    "seller-login-form-container"
  );

  const buyerLoginBtn = document.getElementById("buyer-login-btn");
  const sellerLoginBtn = document.getElementById("seller-login-btn");

  const buyerLoginForm = document.getElementById("buyer-login-form");
  const sellerLoginForm = document.getElementById("seller-login-form");

  const backLinks = document.querySelectorAll(".modal-back-link");
  const findFarmsBtn = document.querySelector("#open-login-modal-btn");

  // Handlers to switch between role selection and login forms
  buyerLoginBtn.addEventListener("click", () => {
    roleSelection.classList.add("hidden");
    buyerLoginFormContainer.classList.remove("hidden");
  });
  //find farm button
  findFarmsBtn.addEventListener("click", (e) => {
    e.preventDefault()
    document.getElementById("login-modal").classList.add("active");
  });

  sellerLoginBtn.addEventListener("click", () => {
    roleSelection.classList.add("hidden");
    sellerLoginFormContainer.classList.remove("hidden");
  });

  backLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      buyerLoginFormContainer.classList.add("hidden");
      sellerLoginFormContainer.classList.add("hidden");
      roleSelection.classList.remove("hidden");
    });
  });

  // Helper to show error messages inline in the form
  const showFormError = (form, message) => {
    const errorDiv = form.querySelector(".form-error-message");
    if (errorDiv) {
      errorDiv.textContent = message;
      errorDiv.style.display = "block";
    }
  };

  const hideFormError = (form) => {
    const errorDiv = form.querySelector(".form-error-message");
    if (errorDiv) {
      errorDiv.style.display = "none";
    }
  };

  const showSuccessMessage = (form, message) => {
    const successDiv = form.querySelector(".form-success-message");
    if (successDiv) {
      successDiv.textContent = message;
      successDiv.style.display = "block";
    }
  };

  // Buyer Login Form Submission
  buyerLoginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("login-buyer-email").value;
    const password = document.getElementById("login-buyer-password").value;

    hideFormError(buyerLoginForm);

    if (!email || !password) {
      showFormError(
        buyerLoginForm,
        "Please enter both email/username and password."
      );
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/login/buyer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        showSuccessMessage(buyerLoginForm, data.message);
        if (data.redirect) {
          window.location.href = data.redirect;
        }
      } else {
        showFormError(
          buyerLoginForm,
          data.error || "Login failed. Please check your credentials."
        );
      }
    } catch (error) {
      console.error("Error:", error);
      showFormError(buyerLoginForm, "An error occurred during login.");
    }
  });

  // Seller Login Form Submission
  sellerLoginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("login-seller-email").value;
    const password = document.getElementById("login-seller-password").value;

    hideFormError(sellerLoginForm);

    if (!email || !password) {
      showFormError(
        sellerLoginForm,
        "Please enter both store ID/email and password."
      );
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/login/seller", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        showSuccessMessage(sellerLoginForm, data.message);
        if (data.redirect) {
          window.location.href = data.redirect;
        }
      } else {
        showFormError(
          sellerLoginForm,
          data.error || "Login failed. Please check your credentials."
        );
      }
    } catch (error) {
      console.error("Error:", error);
      showFormError(sellerLoginForm, "An error occurred during login.");
    }
  });
});
