const addToCartButton = document.getElementById("addToCartButton");
const shoppingBag = document.getElementById("shopping-bag");
const closeBagButton = document.getElementById("close-bag");
const itemsAdded = document.getElementById("items-added");
const itemCount = document.getElementById("item-count");
const subtotalAmount = document.getElementById("subtotal-amount");

const exampleItems = [
    { name: "LOVE bracelet, 10 diamonds", price: 17500, details: "White gold, diamonds, Size 20 cm" },
    { name: "LOVE necklace, 2 diamonds", price: 2510, details: "Yellow gold, diamonds" }
];

addToCartButton.addEventListener("click", async () => {
    shoppingBag.classList.remove("hidden");

    for (const item of exampleItems) {
        await fetch("/add_to_basket", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(item),
        });
    }
    updateShoppingBag();
});

closeBagButton.addEventListener("click", () => {
    shoppingBag.classList.add("hidden");
});

async function updateShoppingBag() {
    const response = await fetch("/basket");
    const basket = await response.json();

    itemsAdded.innerHTML = "";
    basket.items.forEach(item => {
        const newItem = document.createElement("li");
        newItem.innerHTML = `
            <div class="item-image"></div>
            <div class="item-details">
                <h3>${item.name}</h3>
                <p>${item.details}</p>
                <p>£${item.price.toLocaleString()}</p>
            </div>
        `;
        itemsAdded.appendChild(newItem);
    });

    itemCount.textContent = basket.items.length;
    subtotalAmount.textContent = `£${basket.subtotal.toLocaleString()} (incl. VAT)`;
}
