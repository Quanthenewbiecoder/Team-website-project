document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const emailInput = document.getElementById("email").value.trim();
            const passwordInput = document.getElementById("password").value.trim();

            if (!emailInput || !passwordInput) {
                alert("Please fill in all fields.");
                return;
            }

            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: emailInput, password: passwordInput })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Store user_email in localStorage after successful login
                    localStorage.setItem('user_email', data.user_email);
                    
                    alert("Login successful!");
                    window.location.href = "/dashboard"; // Redirect user
                } else {
                    alert("Invalid email or password.");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});
