document.addEventListener('DOMContentLoaded', function() {
    const successMessage = document.querySelector('.forgot-flash-message.success');
    const errorMessage = document.querySelector('.forgot-flash-message.danger, .forgot-flash-message.error');
    
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `password-reset-notification ${type}`;
        
        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
        
        notification.innerHTML = `
            <i class="fas ${icon}"></i>
            <div class="notification-message">${message}</div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 4000);
    }
    
    if (successMessage) {
        showNotification(successMessage.textContent, 'success');
    }
    
    if (errorMessage) {
        showNotification(errorMessage.textContent, 'error');
    }
    
    const forgotPasswordForm = document.querySelector('.forgot-password-form');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            
            if (!email) {
                e.preventDefault();
                showNotification('Please enter your email address', 'error');
                return;
            }
            
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showNotification('Please enter a valid email address', 'error');
                return;
            }
        });
    }
});