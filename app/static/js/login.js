document.addEventListener('DOMContentLoaded', function() {
    // Check if we have a success message to display
    const successMessage = document.querySelector('.login-flash-message.success');
    if (successMessage) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'login-success-notification';
        notification.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <div>
                <div class="login-message">${successMessage.textContent}</div>
                <div class="login-redirect">Redirecting you...</div>
            </div>
        `;
        
        // Add to body
        document.body.appendChild(notification);
        
        // Show the notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Hide after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Additional form validation can be added here
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!email || !password) {
                e.preventDefault();
                
                // Create error notification
                const notification = document.createElement('div');
                notification.className = 'login-success-notification';
                notification.style.backgroundColor = '#d32f2f';
                notification.innerHTML = `
                    <i class="fas fa-exclamation-circle"></i>
                    <div>
                        <div class="login-message">Please fill in all required fields</div>
                    </div>
                `;
                
                // Add to body
                document.body.appendChild(notification);
                
                // Show the notification
                setTimeout(() => {
                    notification.classList.add('show');
                }, 100);
                
                // Hide after 3 seconds
                setTimeout(() => {
                    notification.classList.remove('show');
                    setTimeout(() => {
                        notification.remove();
                    }, 300);
                }, 3000);
            }
        });
    }
});