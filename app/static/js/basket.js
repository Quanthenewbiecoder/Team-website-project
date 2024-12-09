let cartItems = [];
let totalAmount = 0;

function addToCart(itemName, itemPrice) {
    cartItems.push({ name: itemName, price: itemPrice });
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
            ${item.name} - £${item.price.toFixed(2)}
            <button onclick="removeFromCart(${index})">Remove</button>`;
        orderSummaryList.appendChild(listItem);
    });

    orderTotal.innerHTML = `<strong>Total: £${totalAmount.toFixed(2)}</strong>`;
}

function removeFromCart(index) {
    totalAmount -= cartItems[index].price;
    cartItems.splice(index, 1);
    updateCart();
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
        addToCart(name, price);
    })
);
