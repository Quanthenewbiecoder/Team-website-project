document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("Search");
    const form = document.getElementById("Form");
    const productContainers = {
        Bracelets: document.getElementById("Container_Bracelet"),
        Earrings: document.getElementById("Container_Earrings"),
        Rings: document.getElementById("Container_Rings"),
        Watches: document.getElementById("Container_Watches"),
        Necklaces: document.getElementById("Container_Necklaces"),
    };

    const products = [
        { name: "Crystal Bracelet", type: "Bracelets", price: 20, img: imagePaths.bracelet },
        { name: "Leaf Earrings", type: "Earrings", price: 15, img: imagePaths.earring },
        { name: "Pearl Ring", type: "Rings", price: 25, img: imagePaths.ring },
        { name: "Stylish Watch", type: "Watches", price: 50, img: imagePaths.watch },
        { name: "Leaf Necklace", type: "Necklaces", price: 30, img: imagePaths.necklace },
    ];

    function displayProducts(filteredProducts) {
        Object.values(productContainers).forEach(container => container.innerHTML = "");
        filteredProducts.forEach(product => {
            const container = productContainers[product.type];
            if (container) {
                const productElement = document.createElement("div");
                productElement.classList.add("Product");
                productElement.innerHTML = `
                    <img src="${product.img}" alt="${product.name}">
                    <h1>${product.name}</h1>
                    <p class="price">$${product.price}</p>
                `;
                container.appendChild(productElement);
            }
        });
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const query = searchInput.value.toLowerCase();
        const filteredProducts = products.filter(product => product.name.toLowerCase().includes(query));
        displayProducts(filteredProducts);
    });
});
