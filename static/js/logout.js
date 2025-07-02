document.addEventListener("DOMContentLoaded", () => {
  const logoutButton = document.getElementById("logout-btn");

  if (logoutButton) {
    logoutButton.addEventListener("click", async (event) => {
      event.preventDefault();

      try {
        const response = await fetch("/logout", {
          method: "POST",
        });

        const data = await response.json();

        if (response.ok) {
          if (data.redirect) {
            window.location.href = data.redirect;
          } else {
            window.location.href = "/";
          }
        } else {
          alert(data.error || "Logout failed. Please try again.");
        }
      } catch (error) {
        console.error("An error occurred during logout:", error);
        alert("An error occurred during logout. Please check the console.");
      }
    });
  }
});
