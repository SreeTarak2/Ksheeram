document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const roleSelection = document.getElementById("register-role-selection");
  const buyerFormContainer = document.getElementById("buyer-register-form-container");
  const sellerFormContainer = document.getElementById("seller-register-form-container");

  const buyerRegisterBtn = document.getElementById("buyer-register-btn");
  const sellerRegisterBtn = document.getElementById("seller-register-btn");

  const buyerRegisterForm = document.getElementById("buyer-register-form");
  const sellerRegisterForm = document.getElementById("seller-register-form");

  const backLinks = document.querySelectorAll(".modal-back-link");

  // Helpers to show/hide messages
  const showFormError = (form, message) => {
    const errorDiv = form.querySelector(".form-error-message");
    if (errorDiv) {
      errorDiv.textContent = message;
      errorDiv.style.display = "block";
    }
  };

  const showSuccessMessage = (form, message) => {
    const successDiv = form.querySelector(".form-success-message");
    if (successDiv) {
      successDiv.textContent = message;
      successDiv.style.display = "block";
    }
  };

  const clearMessages = (form) => {
    const errorDiv = form.querySelector(".form-error-message");
    const successDiv = form.querySelector(".form-success-message");
    if (errorDiv) {
      errorDiv.style.display = "none";
      errorDiv.textContent = "";
    }
    if (successDiv) {
      successDiv.style.display = "none";
      successDiv.textContent = "";
    }
  };

  // Role switch handlers
  buyerRegisterBtn.addEventListener("click", () => {
    clearMessages(sellerRegisterForm);
    roleSelection.classList.add("hidden");
    buyerFormContainer.classList.remove("hidden");
  });

  sellerRegisterBtn.addEventListener("click", () => {
    clearMessages(buyerRegisterForm);
    roleSelection.classList.add("hidden");
    sellerFormContainer.classList.remove("hidden");
  });

  backLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      clearMessages(buyerRegisterForm);
      clearMessages(sellerRegisterForm);
      buyerFormContainer.classList.add("hidden");
      sellerFormContainer.classList.add("hidden");
      roleSelection.classList.remove("hidden");
    });
  });

  // Buyer Registration Handler
  buyerRegisterForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fullName = document.getElementById("reg-buyer-name").value;
    const email = document.getElementById("reg-buyer-email").value;
    const phone = document.getElementById("reg-buyer-phone").value;
    const password = document.getElementById("reg-buyer-password").value;
    const confirmPassword = document.getElementById("reg-buyer-confirm-password").value;

    clearMessages(buyerRegisterForm);

    if (!fullName || !email || !phone || !password || !confirmPassword) {
      showFormError(buyerRegisterForm, "Please fill in all fields.");
      return;
    }

    if (password !== confirmPassword) {
      showFormError(buyerRegisterForm, "Passwords do not match.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/register/buyer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials:"include",
        body: JSON.stringify({ fullName, email, phone, password }),
      });

      const data = await res.json();

      if (res.ok) {
        showSuccessMessage(buyerRegisterForm, data.message);
        if (data.redirect) {
          setTimeout(()=>{
            window.location.href = data.redirect;
          } , 300);
        }
      } else {
        showFormError(buyerRegisterForm, data.error || "Registration failed.");
      }
    } catch (error) {
      console.error("Error:", error);
      showFormError(buyerRegisterForm, "An error occurred during registration.");
    }
  });

  // Seller Registration Handler
  sellerRegisterForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const storeName = document.getElementById("reg-seller-store").value;
    const email = document.getElementById("reg-seller-email").value;
    const phone = document.getElementById("reg-seller-phone").value;
    const password = document.getElementById("reg-seller-password").value;
    const confirmPassword = document.getElementById("reg-seller-confirm-password").value;

    clearMessages(sellerRegisterForm);

    if (!storeName || !email || !phone || !password || !confirmPassword) {
      showFormError(sellerRegisterForm, "Please fill in all fields.");
      return;
    }

    if (password !== confirmPassword) {
      showFormError(sellerRegisterForm, "Passwords do not match.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/register/seller", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials:"include",
        body: JSON.stringify({ storeName, email, phone, password }),
      });

      const data = await res.json();

      if (res.ok) {
        showSuccessMessage(sellerRegisterForm, data.message);
        if (data.redirect) {
          setTimeout(()=>{
            window.location.href = data.redirect;
          },300);
        }
      } else {
        showFormError(sellerRegisterForm, data.error || "Registration failed.");
      }
    } catch (error) {
      console.error("Error:", error);
      showFormError(sellerRegisterForm, "An error occurred during registration.");
    }
  });
});
