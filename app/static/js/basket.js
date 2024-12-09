const addToCart = async (name, price, image) => {
    const productId = btoa(name).slice(0, 10);
    const data = {
        product_id: productId,
        product_name: name,
        price: price,
        quantity: 1,
        image: image
    };

    try {
        const response = await fetch('/basket/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            updateCartDisplay(result.basket);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

const updateCartDisplay = (basket) => {
    const orderSummaryList = document.getElementById("order-summary-list");
    const orderTotal = document.getElementById("order-total");
    let total = 0;

    orderSummaryList.innerHTML = Object.keys(basket).length ? "" : "<li>Basket is empty</li>";

    Object.entries(basket).forEach(([id, item]) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

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

    orderTotal.innerHTML = `<strong>Total: £${total.toFixed(2)}</strong>`;
    document.getElementById("cart-link").innerText = 
        `My Cart (${Object.keys(basket).length} Items)`;
};

const updateQuantity = async (productId, newQuantity) => {
    if (newQuantity < 1) {
        try {
            const response = await fetch(`/basket/remove/${productId}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                const result = await response.json();
                updateCartDisplay(result.basket);
            }
        } catch (error) {
            console.error('Error:', error);
        }
        return;
    }

    try {
        const response = await fetch('/basket/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: newQuantity
            })
        });

        if (response.ok) {
            const result = await response.json();
            updateCartDisplay(result.basket);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

document.querySelectorAll(".add-btn").forEach(btn => {
    btn.addEventListener("click", event => {
        const name = event.target.dataset.name;
        const price = parseFloat(event.target.dataset.price);
        const image = event.target.closest(".product-card").querySelector("img").src;
        addToCart(name, price, image);
    });
});