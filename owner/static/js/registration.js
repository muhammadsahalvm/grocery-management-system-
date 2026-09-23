// ===============================================
// Salam Mart Registration JavaScript
// ===============================================

document.addEventListener("DOMContentLoaded", function () {

    const registerForm = document.getElementById("registerForm");

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");

    const strengthBar = document.querySelector(".strength-bar");
    const strengthText = document.getElementById("strengthText");

    const createBtn = document.querySelector(".login-btn");

    //==========================================
    // PASSWORD TOGGLE
    //==========================================

    const togglePassword = document.querySelector(".togglePassword");

    if (togglePassword) {

        togglePassword.addEventListener("click", function () {

            const icon = this.querySelector("i");

            if (password.type === "password") {

                password.type = "text";

                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");

            } else {

                password.type = "password";

                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");

            }

        });

    }

    //==========================================
    // CONFIRM PASSWORD TOGGLE
    //==========================================

    const toggleConfirm = document.querySelector(".toggleConfirmPassword");

    if (toggleConfirm) {

        toggleConfirm.addEventListener("click", function () {

            const icon = this.querySelector("i");

            if (confirmPassword.type === "password") {

                confirmPassword.type = "text";

                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");

            } else {

                confirmPassword.type = "password";

                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");

            }

        });

    }

    //==========================================
    // PASSWORD STRENGTH
    //==========================================

    password.addEventListener("keyup", function () {

        const value = password.value;

        let strength = 0;

        if (value.length >= 8)
            strength++;

        if (/[A-Z]/.test(value))
            strength++;

        if (/[a-z]/.test(value))
            strength++;

        if (/[0-9]/.test(value))
            strength++;

        if (/[^A-Za-z0-9]/.test(value))
            strength++;

        switch (strength) {

            case 0:
            case 1:

                strengthBar.style.width = "20%";
                strengthBar.style.background = "#dc3545";
                strengthText.innerHTML = "Weak Password";

                break;

            case 2:

                strengthBar.style.width = "40%";
                strengthBar.style.background = "#ff9800";
                strengthText.innerHTML = "Fair Password";

                break;

            case 3:

                strengthBar.style.width = "60%";
                strengthBar.style.background = "#ffc107";
                strengthText.innerHTML = "Medium Password";

                break;

            case 4:

                strengthBar.style.width = "80%";
                strengthBar.style.background = "#4caf50";
                strengthText.innerHTML = "Strong Password";

                break;

            case 5:

                strengthBar.style.width = "100%";
                strengthBar.style.background = "#2f8d46";
                strengthText.innerHTML = "Very Strong Password";

                break;

        }

    });

    //==========================================
    // PASSWORD MATCH
    //==========================================

    const matchMessage = document.createElement("small");

    matchMessage.classList.add("match-text");

    confirmPassword.parentElement.parentElement.appendChild(matchMessage);

    function checkPasswordMatch() {

        if (confirmPassword.value === "") {

            matchMessage.innerHTML = "";

            return true;

        }

        if (password.value === confirmPassword.value) {

            matchMessage.innerHTML = "✔ Passwords Match";

            matchMessage.className = "match-text match-success";

            return true;

        } else {

            matchMessage.innerHTML = "✖ Passwords Do Not Match";

            matchMessage.className = "match-text match-error";

            return false;

        }

    }

    password.addEventListener("keyup", checkPasswordMatch);

    confirmPassword.addEventListener("keyup", checkPasswordMatch);

    //==========================================
    // INPUT ANIMATION
    //==========================================

    const inputs = document.querySelectorAll(".input-box input");

    inputs.forEach(function (input) {

        input.addEventListener("focus", function () {

            this.parentElement.classList.add("active");

        });

        input.addEventListener("blur", function () {

            if (this.value === "") {

                this.parentElement.classList.remove("active");

            }

        });

    });

    //==========================================
    // FORM VALIDATION
    //==========================================

    registerForm.addEventListener("submit", function (e) {

        const name = document.getElementById("name").value.trim();

        const username = document.getElementById("username").value.trim();

        if (name === "") {

            alert("Please enter your name.");

            e.preventDefault();

            return;

        }

        if (username === "") {

            alert("Please enter username.");

            e.preventDefault();

            return;

        }

        if (password.value.length < 8) {

            alert("Password should contain at least 8 characters.");

            e.preventDefault();

            return;

        }

        if (!checkPasswordMatch()) {

            alert("Passwords do not match.");

            e.preventDefault();

            return;

        }

        createBtn.disabled = true;

        createBtn.innerHTML =

            '<i class="fa-solid fa-spinner fa-spin"></i> Creating Account...';

    });

    //==========================================
    // AUTO FOCUS
    //==========================================

    document.getElementById("name").focus();

    //==========================================
    // ENTER KEY SUPPORT
    //==========================================

    document.addEventListener("keydown", function (e) {

        if (e.key === "Enter") {

            registerForm.requestSubmit();

        }

    });

});