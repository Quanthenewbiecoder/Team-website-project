document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('newsletter-popup');
    const closeButton = document.getElementById('close-popup');
    
    if (popup) {
        popup.style.display = 'block';
    }

    // Close popup when clicking the X button
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            popup.style.display = 'none';
        });
    }

    // Newsletter form submission
    const form = document.getElementById('newsletter-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;

            fetch('/subscribe-newsletter', {
                method: 'POST',
                body: JSON.stringify({ email: email }),
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (response.ok) {
                    alert('Thank you for subscribing to our newsletter!');
                    popup.style.display = 'none';
                } else {
                    alert('There was an error with your subscription. Please try again.');
                }
            }).catch(error => {
                alert('Error: ' + error);
            });
        });
    }

    // Close popup when clicking outside
    window.onclick = function(event) {
        if (event.target === popup) {
            popup.style.display = 'none';
        }
    };
});
