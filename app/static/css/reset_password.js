document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const passwordMatchMessage = document.getElementById('password-match-message');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    const resetForm = document.getElementById('reset-password-form');
    
    if (!passwordInput || !confirmPasswordInput || !passwordMatchMessage || !strengthBar || !strengthText || !resetForm) {
        console.error('Required elements not found on page');
        return;
    }
    
    const successMessage = document.querySelector('.reset-flash-message.success');
    const errorMessage = document.querySelector('.reset-flash-message.danger, .reset-flash-message.error');
    
    if (successMessage) {
        showNotification(successMessage.textContent, 'success');
    }
    
    if (errorMessage) {
        showNotification(errorMessage.textContent, 'error');
    }
    
    passwordInput.addEventListener('input', function() {
        checkPasswordStrength(this.value);
        checkPasswordsMatch();
    });
    
    confirmPasswordInput.addEventListener('input', checkPasswordsMatch);
    
    resetForm.addEventListener('submit', function(e) {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        if (!isPasswordValid(password)) {
            e.preventDefault();
            showNotification('Please make sure your password meets all requirements', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            e.preventDefault();
            showNotification('Passwords do not match', 'error');
            return;
        }
    });
    
    function checkPasswordStrength(password) {
        strengthBar.className = '';
        
        if (!password) {
            strengthBar.style.width = '0';
            strengthText.textContent = 'Password strength';
            return;
        }
        
        let strength = 0;
        let feedback = '';
        
        if (password.length >= 8) {
            strength += 1;
        }
        
        if (/[A-Z]/.test(password)) strength += 1;
        if (/[a-z]/.test(password)) strength += 1;
        if (/[0-9]/.test(password)) strength += 1;
        if (/[^A-Za-z0-9]/.test(password)) strength += 1;
        
        // Determine strength level and update UI
        if (strength <= 2) {
            strengthBar.className = 'weak';
            feedback = 'Weak password';
        } else if (strength === 3) {
            strengthBar.className = 'medium';
            feedback = 'Medium strength password';
        } else if (strength === 4) {
            strengthBar.className = 'strong';
            feedback = 'Strong password';
        } else if (strength === 5) {
            strengthBar.className = 'very-strong';
            feedback = 'Very strong password';
        }
        
        strengthText.textContent = feedback;
    }
    
    function checkPasswordsMatch() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        if (!confirmPassword) {
            passwordMatchMessage.textContent = '';
            passwordMatchMessage.className = 'match-message';
            return;
        }
        
        if (password === confirmPassword) {
            passwordMatchMessage.textContent = 'Passwords match';
            passwordMatchMessage.className = 'match-message success';
        } else {
            passwordMatchMessage.textContent = 'Passwords do not match';
            passwordMatchMessage.className = 'match-message error';
        }
    }
    
    function isPasswordValid(password) {
        if (password.length < 8) return false;
        
        if (!/[A-Z]/.test(password)) return false;
        
        if (!/[a-z]/.test(password)) return false;
        
        if (!/[0-9]/.test(password)) return false;
        
        if (!/[^A-Za-z0-9]/.test(password)) return false;
        
        return true;
    }
    
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
});