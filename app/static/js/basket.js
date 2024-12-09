let cartItems = [];
let totalAmount = 0;

function addToCart(itemName, itemPrice, itemImage) {
    const existingItemIndex = cartItems.findIndex((item) => item.name === itemName);
    if (existingItemIndex !== -1) {
        cartItems[existingItemIndex].quantity += 1;
    } else {
        cartItems.push({ name: itemName, price: itemPrice, image: itemImage, quantity: 1 });
    }
    totalAmount += itemPrice;
    updateCart();
    updateOrderSummary();
}

function updateCart() {
    document.getElementById("cart-link").innerText = `My Cart (${cartItems.length} Items)`;
}

function updateOrderSummary() {
    const orderSummaryList = document.getElementById("order-summary-list");
    const orderTotal = document.getElementById("order-total");

    orderSummaryList.innerHTML = cartItems.length ? "" : "<li>Basket is empty</li>";

    cartItems.forEach((item, index) => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}" class="basket-item-img">
            <span>${item.name} - £${(item.price * item.quantity).toFixed(2)}</span>
            <div class="quantity-controls">
                <button onclick="decreaseQuantity(${index})">-</button>
                <span class="item-quantity">${item.quantity}</span>
                <button onclick="increaseQuantity(${index})">+</button>
            </div>`;
        orderSummaryList.appendChild(listItem);
    });

    orderTotal.innerHTML = `<strong>Total: £${totalAmount.toFixed(2)}</strong>`;
}

function increaseQuantity(index) {
    cartItems[index].quantity += 1;
    totalAmount += cartItems[index].price;
    updateOrderSummary();
}

function decreaseQuantity(index) {
    if (cartItems[index].quantity > 1) {
        cartItems[index].quantity -= 1;
        totalAmount -= cartItems[index].price;
    } else {
        totalAmount -= cartItems[index].price;
        cartItems.splice(index, 1);
    }
    updateOrderSummary();
}

function showPromoPopup() {
    document.getElementById("promo-popup").classList.remove("hidden");
}

function closePopup() {
    document.getElementById("promo-popup").classList.add("hidden");
}

function applyPromoCode() {
    const code = document.getElementById("promo-code-input").value;
    if (code === "TEAM20") {
        showMessage("success-popup");
        totalAmount *= 0.8;
        updateOrderSummary();
    } else {
        showMessage("error-popup");
    }
}

function showMessage(popupId) {
    const popup = document.getElementById(popupId);
    popup.classList.remove("hidden");
    setTimeout(() => {
        popup.classList.add("hidden");
    }, 6000);
}

document.getElementById("close-popup").addEventListener("click", closePopup);

document.querySelectorAll(".add-btn").forEach((btn) =>
    btn.addEventListener("click", (event) => {
        const name = event.target.dataset.name;
        const price = parseFloat(event.target.dataset.price);
        const image = event.target.closest(".product-card").querySelector("img").src;
        addToCart(name, price, image);
    })
);