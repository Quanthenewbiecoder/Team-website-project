document.addEventListener('DOMContentLoaded', function() {
    loadCartData();
    
    setupFormFormatting();
    
    setupFormSubmission();
    
    setupTrackingCopy();
});

function loadCartData() {
    const orderItems = document.getElementById('order-items');
    const cartTotal = document.getElementById('cart-total');
    const emptyCartMessage = document.querySelector('.empty-cart-message');
    const cartDataInput = document.getElementById('cart-data');
    
    const cartDataString = sessionStorage.getItem('divinecart');
    
    if (!cartDataString || cartDataString === '{}') {
        if (emptyCartMessage) {
            emptyCartMessage.style.display = 'block';
        }
        if (cartTotal) {
            cartTotal.textContent = '£0.00';
        }
        return;
    }
    
    const cartData = JSON.parse(cartDataString);
    
    if (cartDataInput) {
        cartDataInput.value = cartDataString;
    }
    
    if (emptyCartMessage) {
        emptyCartMessage.style.display = 'none';
    }
    
    if (!orderItems || !cartTotal) return;
    
    orderItems.innerHTML = '';
    
    let total = 0;
    
    Object.entries(cartData).forEach(([id, item]) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.innerHTML = `
            <img src="${item.image}" alt="${item.name}" class="item-image">
            <div class="item-details">
                <p class="item-name">${item.name}</p>
                <p class="item-price">£${item.price.toFixed(2)} <span class="item-quantity">x${item.quantity}</span></p>
            </div>
        `;
        
        orderItems.appendChild(itemElement);
    });
    
    cartTotal.textContent = `£${total.toFixed(2)}`;
}

function setupFormFormatting() {
    const cardNumberInput = document.getElementById('card-number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = '';
            
            for(let i = 0; i < value.length; i++) {
                if(i > 0 && i % 4 === 0) {
                    formattedValue += ' ';
                }
                formattedValue += value[i];
            }
            
            e.target.value = formattedValue;
        });
    }

    const expiryInput = document.getElementById('expiry');
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length >= 2) {
                value = value.slice(0,2) + '/' + value.slice(2);
            }
            
            e.target.value = value;
        });
    }

    const cvvInput = document.getElementById('cvv');
    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '');
        });
    }
}

function setupFormSubmission() {
    const paymentForm = document.querySelector('.payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const cardNumber = document.getElementById('card-number').value.replace(/\s/g, '');
            const expiry = document.getElementById('expiry').value;
            const cvv = document.getElementById('cvv').value;
            
            if (cardNumber.length !== 16) {
                alert('Please enter a valid 16-digit card number');
                return;
            }
            
            if (!expiry.match(/^(0[1-9]|1[0-2])\/([0-9]{2})$/)) {
                alert('Please enter a valid expiry date (MM/YY)');
                return;
            }
            
            if (cvv.length !== 3) {
                alert('Please enter a valid 3-digit CVV');
                return;
            }
            
            sessionStorage.removeItem('divinecart');
            
            this.submit();
        });
    }
}

function setupTrackingCopy() {
    const copyTrackingBtn = document.getElementById('copy-tracking');
    
    if (copyTrackingBtn) {
        copyTrackingBtn.addEventListener('click', function() {
            const trackingNumber = this.getAttribute('data-tracking');
            
            navigator.clipboard.writeText(trackingNumber)
                .then(() => {
                    showCopyConfirmation(this);
                })
                .catch(() => {
                    fallbackCopyToClipboard(trackingNumber, this);
                });
        });
    }
}

function fallbackCopyToClipboard(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopyConfirmation(button);
        } else {
            showCopyError();
        }
    } catch (err) {
        showCopyError();
    }
    
    document.body.removeChild(textArea);
}

function showCopyConfirmation(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i> Copied!';
    button.classList.add('copy-success');
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.classList.remove('copy-success');
    }, 2000);
}

function showCopyError() {
    const notification = document.createElement('div');
    notification.className = 'copy-notification error';
    notification.textContent = 'Failed to copy. Please try again.';
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