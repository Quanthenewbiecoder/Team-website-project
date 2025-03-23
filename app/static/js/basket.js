let cartItems = {};
let cartTotal = 0;
let discountApplied = false; 
let discountAmount = 0;

document.addEventListener("DOMContentLoaded", function() {
    loadCartFromStorage();
    
    updateCartDisplay();
    
    attachAddToCartListeners();
    
    initPromoCode();
});

function loadCartFromStorage() {
    const savedCart = sessionStorage.getItem('divinecart');
    if (savedCart) {
        cartItems = JSON.parse(savedCart);
        calculateCartTotal();
    }
}

function saveCartToStorage() {
    sessionStorage.setItem('divinecart', JSON.stringify(cartItems));
}

function calculateCartTotal() {
    cartTotal = 0;
    Object.values(cartItems).forEach(item => {
        cartTotal += item.price * item.quantity;
    });
}

function updateCartDisplay() {
    const orderSummaryList = document.getElementById("order-summary-list");
    const orderTotal = document.getElementById("order-total");
    const cartLink = document.getElementById("cart-link");
    const emptyCartMessage = document.getElementById("empty-cart-message");
    
    if (!orderSummaryList) return;
    
    const itemCount = Object.keys(cartItems).length;
    
    if (cartLink) {
        cartLink.innerText = `My Cart (${itemCount} Items)`;
    }
    
    orderSummaryList.innerHTML = "";
    
    if (itemCount === 0) {
        orderSummaryList.innerHTML = "<li>Your basket is empty</li>";
        orderTotal.innerHTML = "<strong>Total: £0.00</strong>";
        if (emptyCartMessage) {
            emptyCartMessage.style.display = "block";
        }
        return;
    }
    
    if (emptyCartMessage) {
        emptyCartMessage.style.display = "none";
    }
    
    Object.entries(cartItems).forEach(([id, item]) => {
        const listItem = document.createElement("li");
        
        listItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}" class="basket-item-img">
            <div class="item-details">
                <span class="item-name">${item.name}</span>
                <span class="item-price">£${(item.price * item.quantity).toFixed(2)}</span>
            </div>
            <div class="quantity-controls">
                <button onclick="updateQuantity('${id}', ${item.quantity - 1})">-</button>
                <span class="item-quantity">${item.quantity}</span>
                <button onclick="updateQuantity('${id}', ${item.quantity + 1})">+</button>
                <button class="remove-item" data-id="${id}">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        
        orderSummaryList.appendChild(listItem);
    });
    
    let finalTotal = cartTotal - discountAmount;
    orderTotal.innerHTML = `<strong>Total: £${finalTotal.toFixed(2)}</strong>`;
}

function attachAddToCartListeners() {
    const addButtons = document.querySelectorAll('.add-btn');
    
    if (addButtons.length > 0) {
        addButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                const productId = this.getAttribute('data-id');
                const productName = this.getAttribute('data-name');
                const productPrice = parseFloat(this.getAttribute('data-price'));
                const productImage = this.closest('.Product')?.querySelector('img')?.src || 
                                    this.closest('.product-card')?.querySelector('img')?.src;
                
                addToCart(productId, productName, productPrice, productImage);
            });
        });
    }
}

function addToCart(id, name, price, image) {
    if (cartItems[id]) {
        cartItems[id].quantity += 1;
    } else {
        cartItems[id] = {
            name: name,
            price: price,
            quantity: 1,
            image: image
        };
    }
    
    calculateCartTotal();
    saveCartToStorage();
    showNotification(`${name} added to your basket`);
    updateCartDisplay();
}

function updateQuantity(id, newQuantity) {
    if (newQuantity <= 0) {
        removeItem(id);
        return;
    }
    
    if (cartItems[id]) {
        cartItems[id].quantity = newQuantity;
        calculateCartTotal();
        saveCartToStorage();
        updateCartDisplay();
    }
}

function removeItem(id) {
    console.log("Removing item with ID:", id); // Debug log
    
    if (cartItems[id]) {
        const itemName = cartItems[id].name;
        delete cartItems[id];
        calculateCartTotal();
        saveCartToStorage();
        updateCartDisplay();
        showNotification(`${itemName} removed from your basket`);
    } else {
        console.log("Item with ID not found in cart:", id); // Debug log
    }
}

function clearCart() {
    cartItems = {};
    cartTotal = 0;
    discountApplied = false;
    discountAmount = 0;
    saveCartToStorage();
    updateCartDisplay();
    showNotification("Your basket has been cleared");
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
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
    }, 2000);
}

function initPromoCode() {
    const promoButton = document.querySelector('.btn-primary[onclick="showPromoPopup()"]');
    const closePopup = document.getElementById('close-popup');
    
    if (promoButton) {
        promoButton.addEventListener('click', showPromoPopup);
    }
    
    if (closePopup) {
        closePopup.addEventListener('click', function() {
            document.getElementById('promo-popup').classList.add('hidden');
        });
    }
}

function showPromoPopup() {
    const popup = document.getElementById('promo-popup');
    if (popup) {
        popup.classList.remove('hidden');
    }
}

function applyPromoCode() {
    const promoCodeInput = document.getElementById('promo-code-input').value.trim();
    const successPopup = document.getElementById('success-popup');
    const errorPopup = document.getElementById('error-popup');
    
    if (discountApplied) {
        showError("Only one discount can be applied per purchase.");
        return;
    }
    
    if (promoCodeInput === "DIVINE20") {
        discountAmount = cartTotal * 0.20;
        discountApplied = true;
        showSuccess("Congratulations! 20% discount applied!");
    } else if (promoCodeInput === "WELCOME10") {
        discountAmount = cartTotal * 0.10;
        discountApplied = true;
        showSuccess("Welcome discount of 10% applied!");
    } else {
        showError("Invalid promo code. Please try again.");
        return;
    }
    
    updateCartDisplay();
    document.getElementById('promo-popup').classList.add('hidden');
}

function showSuccess(message) {
    showNotification(message);
}

function showError(message) {
    const notification = document.createElement('div');
    notification.className = 'cart-notification error';
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
    }, 2000);
}

window.updateQuantity = updateQuantity;
window.removeItem = removeItem;
window.clearCart = clearCart;
window.showPromoPopup = showPromoPopup;
window.applyPromoCode = applyPromoCode;