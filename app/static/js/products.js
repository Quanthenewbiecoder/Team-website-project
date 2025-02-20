document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("Search");
    const form = document.getElementById("Form");
    const productsContainer = document.querySelector(".products-container");
    let allProducts = []; // Store all products globally

    //  Fetch products from Flask API once
    async function fetchProducts() {
        try {
            const response = await fetch("/api/products"); // Fetch products from API
            allProducts = await response.json(); // Store globally
            displayProducts(allProducts); // Display all products initially
        } catch (error) {
            console.error("Error fetching products:", error);
        }
    }

    //  Display products dynamically
    function displayProducts(products) {
        // Clear previous products before adding new ones
        document.querySelectorAll(".product-card").forEach(card => card.remove());

        products.forEach(product => {
            const productElement = document.createElement("div");
            productElement.classList.add("product-card");
            productElement.setAttribute("data-type", product.type);
            productElement.setAttribute("data-collection", product.collection);
            productElement.setAttribute("data-instock", product.in_stock);

            productElement.innerHTML = `
                <img src="${product.image_url}" alt="${product.name}">
                <h1>${product.name}</h1>
                <p class="price">£${product.price}</p>
                <p>${product.description}</p>
            `;
            productsContainer.appendChild(productElement);
        });
    }

    //  Apply filters based on user selection
    function applyFilters() {
        let filteredProducts = [...allProducts]; // Copy the array

        const query = searchInput.value.toLowerCase();
        const selectedSort = document.querySelector('input[name="sort"]:checked')?.value;
        const selectedCollection = document.querySelector('input[name="collections"]:checked')?.value;
        const inStockChecked = document.getElementById("InStock").checked;
        const newChecked = document.getElementById("New").checked;
        const onSaleChecked = document.getElementById("OnSale").checked;

        //  Filter by search query (name)
        if (query) {
            filteredProducts = filteredProducts.filter(product =>
                product.name.toLowerCase().includes(query)
            );
        }

        //  Filter by collection
        if (selectedCollection && selectedCollection !== "None") {
            filteredProducts = filteredProducts.filter(product =>
                product.collection === selectedCollection
            );
        }

        //  Filter by stock availability
        if (inStockChecked) {
            filteredProducts = filteredProducts.filter(product => product.in_stock);
        }

        //  Filter by "New" - Assuming "New" means products with a certain property (e.g., collection is recent)
        if (newChecked) {
            filteredProducts = filteredProducts.filter(product => product.collection === "New");
        }

        //  Filter by "On Sale" - Assuming sale items have a specific flag (modify this as needed)
        if (onSaleChecked) {
            filteredProducts = filteredProducts.filter(product => product.collection === "OnSale");
        }

        //  Filter by Product Type (Checkbox Selection)
        const selectedTypes = [];
        document.querySelectorAll('input[name="Bracelets"]:checked, input[name="Earrings"]:checked, input[name="Rings"]:checked, input[name="Watches"]:checked, input[name="Necklaces"]:checked').forEach(checkbox => {
            selectedTypes.push(checkbox.value);
        });

        if (selectedTypes.length > 0) {
            filteredProducts = filteredProducts.filter(product =>
                selectedTypes.includes(product.type)
            );
        }

        //  Sorting logic
        if (selectedSort === "HighLow") {
            filteredProducts.sort((a, b) => b.price - a.price);
        } else if (selectedSort === "LowHigh") {
            filteredProducts.sort((a, b) => a.price - b.price);
        }

        // Display filtered products
        displayProducts(filteredProducts);
    }

    //  Event Listener for form submission (filters and sorting)
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        applyFilters();
    });

    fetchProducts(); // Load products on page load
});
