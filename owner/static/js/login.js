// =========================================
// Salam Mart - Login JavaScript
// =========================================

document.addEventListener("DOMContentLoaded", () => {

    // ============================
    // Password Toggle
    // ============================

    const passwordInput = document.getElementById("password");
    const togglePassword = document.querySelector(".togglePassword");

    if (togglePassword && passwordInput) {

        togglePassword.addEventListener("click", () => {

            const icon = togglePassword.querySelector("i");

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");

            } else {

                passwordInput.type = "password";

                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");

            }

        });

    }

    // ============================
    // Input Focus Animation
    // ============================

    const inputs = document.querySelectorAll(".input-box input");

    inputs.forEach(input => {

        input.addEventListener("focus", () => {

            input.parentElement.classList.add("active");

        });

        input.addEventListener("blur", () => {

            if (input.value.trim() === "") {

                input.parentElement.classList.remove("active");

            }

        });

    });

    // ============================
    // Login Button Loading
    // ============================

    const loginForm = document.getElementById("loginForm");
    const loginBtn = document.querySelector(".login-btn");

    if (loginForm && loginBtn) {

        loginForm.addEventListener("submit", function (e) {

            const username = document
                .getElementById("username")
                .value
                .trim();

            const password = document
                .getElementById("password")
                .value
                .trim();

            // Validation

            if (username === "") {

                e.preventDefault();

                alert("Please enter your username.");

                return;

            }

            if (password === "") {

                e.preventDefault();

                alert("Please enter your password.");

                return;

            }

            loginBtn.disabled = true;

            loginBtn.innerHTML =
                `<i class="fa-solid fa-spinner fa-spin"></i> Logging In...`;

        });

    }

    // ============================
    // Press Enter to Submit
    // ============================

    document.addEventListener("keydown", function (e) {

        if (e.key === "Enter") {

            if (loginForm) {

                loginForm.requestSubmit();

            }

        }

    });

    // ============================
    // Button Hover Effect
    // ============================

    if (loginBtn) {

        loginBtn.addEventListener("mouseenter", () => {

            loginBtn.style.transform = "translateY(-3px)";

        });

        loginBtn.addEventListener("mouseleave", () => {

            loginBtn.style.transform = "translateY(0px)";

        });

    }

    // ============================
    // Auto Focus Username
    // ============================

    const usernameInput = document.getElementById("username");

    if (usernameInput) {

        usernameInput.focus();

    }

});