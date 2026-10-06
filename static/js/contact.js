/**
 * Client-side validation and interactive feedback for contact form.
 */
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contact-form");
    if (!form) return;

    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const messageInput = document.getElementById("message");
    const submitBtn = document.getElementById("submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnSpinner = submitBtn.querySelector(".btn-spinner");

    const nameError = document.getElementById("name-error");
    const emailError = document.getElementById("email-error");
    const messageError = document.getElementById("message-error");

    const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

    function validate() {
        let isValid = true;

        // Name
        if (!nameInput.value.trim() || nameInput.value.trim().length < 2) {
            nameError.textContent = "Please enter your name (at least 2 characters).";
            nameInput.classList.add("input-invalid");
            isValid = false;
        } else {
            nameError.textContent = "";
            nameInput.classList.remove("input-invalid");
        }

        // Email
        if (!emailRegex.test(emailInput.value.trim())) {
            emailError.textContent = "Please enter a valid email address.";
            emailInput.classList.add("input-invalid");
            isValid = false;
        } else {
            emailError.textContent = "";
            emailInput.classList.remove("input-invalid");
        }

        // Message
        if (!messageInput.value.trim() || messageInput.value.trim().length < 5) {
            messageError.textContent = "Message must be at least 5 characters long.";
            messageInput.classList.add("input-invalid");
            isValid = false;
        } else {
            messageError.textContent = "";
            messageInput.classList.remove("input-invalid");
        }

        return isValid;
    }

    form.addEventListener("submit", (e) => {
        if (!validate()) {
            e.preventDefault();
            return;
        }

        // Visual feedback during submission
        if (btnText && btnSpinner) {
            btnText.setAttribute("hidden", "true");
            btnSpinner.removeAttribute("hidden");
            submitBtn.setAttribute("disabled", "true");
        }
    });

    // Real-time clearance of validation errors on input
    [nameInput, emailInput, messageInput].forEach(inp => {
        inp?.addEventListener("input", () => {
            inp.classList.remove("input-invalid");
            const errSpan = document.getElementById(`${inp.id}-error`);
            if (errSpan) errSpan.textContent = "";
        });
    });
});
