document.addEventListener("DOMContentLoaded", () => {
  // --- Tab Switching Logic ---
  const navLinks = document.querySelectorAll(".account-nav-link");
  const contentPanels = document.querySelectorAll(".account-panel");
  url = "http://127.0.0.1:5000"

  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();

      const targetPanelId = link.getAttribute("data-tab");
      const targetPanel = document.getElementById(targetPanelId);

      navLinks.forEach((navLink) => navLink.classList.remove("active"));
      contentPanels.forEach((panel) => panel.classList.remove("active"));

      link.classList.add("active");
      if (targetPanel) {
        targetPanel.classList.add("active");
      }
    });
  });

  // --- API and Data Handling Logic ---
  const profileForm = document.getElementById("profile-form");
  const fullNameInput = document.getElementById("fullName");
  const emailInput = document.getElementById("email");
  const phoneInput = document.getElementById("phone");

  // Fetch Account Details from the Backend
  const fetchAccountDetails = async () => {
    try {
      const response = await fetch(`${url}/account/details`);
      if (!response.ok) {
        throw new Error("Failed to fetch account details");
      }
      const data = await response.json();

      fullNameInput.value = data.fullName || "";
      emailInput.value = data.email || "";
      phoneInput.value = data.phone || "";
    } catch (error) {
      console.error("Error fetching account details:", error);
    }
  };

  // Handle Profile Update Form Submission
  profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const updatedData = {
      fullName: fullNameInput.value,
      phone: phoneInput.value,
    };

    try {
      const response = await fetch(`${url}/account/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedData),
      });

      if (!response.ok) {
        throw new Error("Failed to update profile");
      }

      alert("Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error);
      alert("Could not update profile. Please try again.");
    }
  });

  fetchAccountDetails();
});
