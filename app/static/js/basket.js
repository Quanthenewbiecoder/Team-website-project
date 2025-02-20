let cartTotal = 0;
let discountApplied = false; 
let discountAmount = 0;

document.addEventListener("DOMContentLoaded", function () {
    updateCartTotal();
});

//update the total price
function updateCartTotal() {
    let totalElement = document.getElementById("order-total");
    let discountedTotal = cartTotal - discountAmount;
    totalElement.innerHTML = `<strong>Total: £${discountedTotal.toFixed(2)}</strong>`;
}


function showPromoPopup() {
    document.getElementById("promo-popup").classList.remove("hidden");
}


function applyPromoCode() {
    let promoCodeInput = document.getElementById("promo-code-input").value.trim();
    let successPopup = document.getElementById("success-popup");
    let errorPopup = document.getElementById("error-popup");

    if (discountApplied) {
        errorPopup.innerText = "Only one discount can be applied per purchase.";
        errorPopup.classList.remove("hidden");
        setTimeout(() => errorPopup.classList.add("hidden"), 2000);
        return;
    }

    if (promoCodeInput === "MothersDay") {
        discountAmount = cartTotal * 0.32; // 32% off
        discountApplied = true;
        successPopup.innerText = "Congratulations! 32% off applied!";
    } else if (promoCodeInput === "Team20") {
        discountAmount = cartTotal * 0.20; // 20% off
        discountApplied = true;
        successPopup.innerText = "Congratulations! 20% off applied!";
    } else {
        errorPopup.innerText = "Invalid promo code!";
        errorPopup.classList.remove("hidden");
        setTimeout(() => errorPopup.classList.add("hidden"), 2000);
        return;
    }

    updateCartTotal();
    successPopup.classList.remove("hidden");
    setTimeout(() => successPopup.classList.add("hidden"), 2000);
    document.getElementById("promo-popup").classList.add("hidden");
}

//for closing popups
document.getElementById("close-popup").addEventListener("click", function () {
    document.getElementById("promo-popup").classList.add("hidden");
});


const updateCartDisplay = (basket) => {
    const orderSummaryList = document.getElementById("order-summary-list");
    const orderTotal = document.getElementById("order-total");
    cartTotal = 0; // Reset total

    orderSummaryList.innerHTML = Object.keys(basket).length ? "" : "<li>Basket is empty</li>";

    Object.entries(basket).forEach(([id, item]) => {
        const itemTotal = item.price * item.quantity;
        cartTotal += itemTotal;

        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <img src="${item.image}" alt="${item.product_name}" class="basket-item-img">
            <span>${item.product_name} - £${itemTotal.toFixed(2)}</span>
            <div class="quantity-controls">
                <button onclick="updateQuantity('${id}', ${item.quantity - 1})">-</button>
                <span class="item-quantity">${item.quantity}</span>
                <button onclick="updateQuantity('${id}', ${item.quantity + 1})">+</button>
            </div>`;
        orderSummaryList.appendChild(listItem);
    });

    updateCartTotal(); // Update total with discount
    document.getElementById("cart-link").innerText = `My Cart (${Object.keys(basket).length} Items)`;
};
