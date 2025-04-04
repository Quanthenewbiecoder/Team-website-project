document.addEventListener('DOMContentLoaded', function () {
    loadCartData();
    setupFormFormatting();
    setupFormSubmission();
    setupTrackingCopy();
    setupBillingAddressToggle();
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
        cardNumberInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = '';

            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formattedValue += ' ';
                }
                formattedValue += value[i];
            }

            e.target.value = formattedValue;
        });
    }

    const expiryInput = document.getElementById('expiry');
    if (expiryInput) {
        expiryInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2);
            }

            e.target.value = value;
        });
    }

    const cvvInput = document.getElementById('cvv');
    if (cvvInput) {
        cvvInput.addEventListener('input', function (e) {
            e.target.value = e.target.value.replace(/\D/g, '');
        });
    }
}


function setupFormSubmission() {
    const paymentForm = document.querySelector('.payment-form');

    if (paymentForm) {
        paymentForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const cartDataString = sessionStorage.getItem('divinecart');
            if (!cartDataString || cartDataString === '{}') {
                alert('Your cart is empty!');
                return;
            }

            const cartData = JSON.parse(cartDataString);
            let totalPrice = 0;
            let items = [];

            Object.entries(cartData).forEach(([id, item]) => {
                totalPrice += item.price * item.quantity;
                items.push({
                    product_name: item.name,
                    quantity: item.quantity,
                    price: item.price
                });
            });

            const formData = new FormData(this);
            
            const guestEmailInput = document.getElementById('guest-email');
            const guestEmail = guestEmailInput ? guestEmailInput.value.trim() : formData.get('email');

            let userId = null;
            try {
                const response = await fetch('/api/get-current-user');
                const userData = await response.json();

                if (userData.success && userData.user) {
                    userId = userData.user.email;  
                }
            } catch (error) {
                console.error("Error fetching user data:", error);
            }

            console.log(`DEBUG: userId from API → ${userId}`);
            console.log(`DEBUG: guestEmail from form → ${guestEmail}`);

            if (!userId && !guestEmail) {
                alert('Please provide an email to continue.');
                return;
            }

            const orderData = {
                user_id: userId,
                guest_email: guestEmail,
                total_price: totalPrice,
                items: items,
                shipping_info: {
                    full_name: formData.get('full_name'),
                    phone: formData.get('phone'),
                    address_line1: formData.get('address_line1'),
                    address_line2: formData.get('address_line2'),
                    city: formData.get('city'),
                    postcode: formData.get('postcode'),
                    country: formData.get('country')
                }
            };

            if (!formData.get('billing_same')) {
                orderData.billing_info = {
                    address_line1: formData.get('billing_address_line1'),
                    address_line2: formData.get('billing_address_line2'),
                    city: formData.get('billing_city'),
                    postcode: formData.get('billing_postcode'),
                    country: formData.get('billing_country')
                };
            }

            console.log("DEBUG: Sending Order Data →", JSON.stringify(orderData, null, 2));

            fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(orderData)
            })
            .then(response => response.json())
            .then(data => {
                console.log("DEBUG: API Response →", data);

                if (data.success) {
                    alert('Payment successful! Your order has been placed.');
                    sessionStorage.removeItem('divinecart');

                    window.location.href = `/payment/success/${data.tracking_number}`;
                } else {
                    alert('Error processing your order. Please try again.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}


function setupTrackingCopy() {
    const copyTrackingBtn = document.getElementById('copy-tracking');

    if (copyTrackingBtn) {
        copyTrackingBtn.addEventListener('click', function () {
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


function setupBillingAddressToggle() {
    const billingSameCheckbox = document.getElementById('billing-same');
    const billingAddressContainer = document.getElementById('billing-address-container');
    
    if (billingSameCheckbox && billingAddressContainer) {
        billingSameCheckbox.addEventListener('change', function() {
            if (this.checked) {
                billingAddressContainer.style.display = 'none';
                document.querySelectorAll('#billing-address-container input, #billing-address-container select').forEach(input => {
                    input.removeAttribute('required');
                });
            } else {
                billingAddressContainer.style.display = 'block';
                document.querySelectorAll('#billing-address-container input, #billing-address-container select').forEach(input => {
                    if (input.id !== 'billing-address-line2') {
                        input.setAttribute('required', 'required');
                    }
                });
            }
        });
        
        billingSameCheckbox.dispatchEvent(new Event('change'));
    }
}