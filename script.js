document.addEventListener("DOMContentLoaded", () => {
  const loginButton = document.getElementById("loginButton");
  const logoutBtn = document.getElementById("logoutBtn");

  // LOGIN PAGE
  if (loginButton) {
    loginButton.addEventListener("click", () => {
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();
      const errorMsg = document.getElementById("errorMsg");
      const validationMsg = document.getElementById("validationMsg");

      errorMsg.classList.add("hidden");
      validationMsg.classList.add("hidden");

      if (!username || !password) {
        validationMsg.classList.remove("hidden");
        return;
      }

      if (username === "valid_user" && password === "valid_pass") {
        localStorage.setItem("isLoggedIn", "true");
        localStorage.setItem("username", username);
        window.location.href = "dashboard.html";
      } else {
        errorMsg.classList.remove("hidden");
      }
    });
  }

  // DASHBOARD PAGE
  if (logoutBtn) {
    const isLoggedIn = localStorage.getItem("isLoggedIn");
    const user = localStorage.getItem("username");
    if (isLoggedIn !== "true") {
      window.location.href = "index.html";
      return;
    }
    document.getElementById("userName").textContent = user;
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("username");
      window.location.href = "index.html";
    });
  }
});
