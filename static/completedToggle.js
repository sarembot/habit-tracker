// Toggle Check/Ex for complete/incomplete habits in table
document.addEventListener("DOMContentLoaded", function () {
  const btns = document.querySelectorAll(".habit-btn");

  btns.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const form = this.closest("form");

      // Add the CSRF token to request
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      // Send data to server and wait for response
      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => response.json()) // Parse the JSON response
        .then((data) => {
          // Only update the symbol after server confirms the change
          this.textContent = data.status ? "✔️" : "❌";
        })
        .catch((error) => {
          console.error("Error:", error);
          // Optionally, you could add error handling here
        });
    });
  });
});
