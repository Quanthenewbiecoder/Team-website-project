document.addEventListener('DOMContentLoaded', function() {
    const trackingForm = document.getElementById('tracking-form');
    if (trackingForm) {
        trackingForm.addEventListener('submit', function(e) {
            const trackingNumber = document.getElementById('tracking-number').value.trim();
            if (!trackingNumber) {
                e.preventDefault();
                showFormError('Please enter a valid tracking number');
            }
        });
    }
    
    const orderDetailsSection = document.getElementById('order-details-section');
    if (orderDetailsSection && orderDetailsSection.getAttribute('data-show') === 'true') {
        orderDetailsSection.classList.add('show');
    }
    
    const copyTrackingBtn = document.getElementById('copy-tracking');
    if (copyTrackingBtn) {
        copyTrackingBtn.addEventListener('click', function() {
            const trackingNumber = this.getAttribute('data-tracking');
            
            navigator.clipboard.writeText(trackingNumber)
                .then(function() {
                    showNotification('Tracking number copied to clipboard!');
                })
                .catch(function() {
                    fallbackCopyToClipboard(trackingNumber);
                });
        });
    }
});

function fallbackCopyToClipboard(text) {
    const tempInput = document.createElement('input');
    tempInput.style.position = 'absolute';
    tempInput.style.left = '-9999px';
    tempInput.value = text;
    document.body.appendChild(tempInput);
    
    tempInput.select();
    document.execCommand('copy');
    
    document.body.removeChild(tempInput);
    
    showNotification('Tracking number copied to clipboard!');
}

function showFormError(message) {
    const errorElement = document.getElementById('form-error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 3000);
    }
}

function showNotification(message, isError = false) {
    const notification = document.createElement('div');
    notification.className = `notification ${isError ? 'error' : 'success'}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function updateOrderStatus(status) {
    const statusElement = document.getElementById('order-status-badge');
    if (statusElement) {
        statusElement.textContent = status;
        
        statusElement.className = 'status-badge';
        switch(status.toLowerCase()) {
            case 'processing':
                statusElement.classList.add('status-processing');
                break;
            case 'shipped':
                statusElement.classList.add('status-shipped');
                break;
            case 'delivered':
                statusElement.classList.add('status-delivered');
                break;
            case 'cancelled':
                statusElement.classList.add('status-cancelled');
                break;
            default:
                statusElement.classList.add('status-default');
        }
    }
}