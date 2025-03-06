document.addEventListener('DOMContentLoaded', function() {
    // Setup form submission
    const trackingForm = document.getElementById('tracking-form');
    if (trackingForm) {
        trackingForm.addEventListener('submit', function(e) {
            // Form validation is handled by the server
            const trackingNumber = document.getElementById('tracking-number').value.trim();
            if (!trackingNumber) {
                e.preventDefault();
                showFormError('Please enter a valid tracking number');
            }
        });
    }
    
    // Check if order details should be shown (based on server-side data)
    const orderDetailsSection = document.getElementById('order-details-section');
    if (orderDetailsSection && orderDetailsSection.getAttribute('data-show') === 'true') {
        orderDetailsSection.classList.add('show');
    }
    
    // Copy tracking number to clipboard functionality
    const copyTrackingBtn = document.getElementById('copy-tracking');
    if (copyTrackingBtn) {
        copyTrackingBtn.addEventListener('click', function() {
            const trackingNumber = this.getAttribute('data-tracking');
            navigator.clipboard.writeText(trackingNumber).then(function() {
                showNotification('Tracking number copied to clipboard!');
            }, function() {
                showNotification('Failed to copy tracking number', true);
            });
        });
    }
});

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
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${isError ? 'error' : 'success'}`;
    notification.textContent = message;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Show notification (with animation)
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Hide and remove notification after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Function to update the order status in the UI
function updateOrderStatus(status) {
    const statusElement = document.getElementById('order-status-badge');
    if (statusElement) {
        statusElement.textContent = status;
        
        // Update color based on status
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