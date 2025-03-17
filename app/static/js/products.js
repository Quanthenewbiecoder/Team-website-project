document.addEventListener("DOMContentLoaded", function () {
    const productsGrid = document.getElementById("products-grid");
    if (!productsGrid) {
        console.error("Error: Element with ID 'products-grid' not found.");
        return;
    }

    const searchInput = document.getElementById("Search");
    const filterForm = document.getElementById("Form");
    let allProducts = [];
    let currentUserRole = null;

    async function fetchCurrentUser() {
        try {
            const response = await fetch('/api/get-current-user', { credentials: 'include' });
            const data = await response.json();

            if (data.success) {
                currentUserRole = data.user.role;
                console.log("User role:", currentUserRole); // Debugging
            }
        } catch (error) {
            console.error("Error fetching user:", error);
        }
    }

    // Fetch and display products
    async function fetchProducts() {
        await fetchCurrentUser();
        
        try {
            const response = await fetch('/api/products');
            const data = await response.json();

            if (data.success) {
                allProducts = data.products;
                updateProductList(allProducts); // Show all products initially
            } else {
                console.error("Error fetching products:", data.error);
            }
        } catch (error) {
            console.error("Fetch error:", error);
        }
    }
    
    // Update product list in UI
    function updateProductList(products) {
        productsGrid.innerHTML = "";
    
        if (products.length === 0) {
            showEmptyState();
            return;
        }
    
        products.forEach(product => {
            let imageUrl = product.image_url;
    
            if (!imageUrl.startsWith("/static/images/")) {
                imageUrl = `/static/images/${imageUrl.split('/').pop()}`;
            }
    
            // Fallback image if missing
            if (!imageUrl || imageUrl.trim() === "") {
                imageUrl = "/static/images/default.jpg";
            }
    
            const productElement = document.createElement("div");
            productElement.classList.add("Product");
            productElement.dataset.id = product.id;
            productElement.dataset.type = product.type;
            productElement.dataset.collection = product.collection;
    
            // Only show delete button if user is admin/staff
            let deleteButtonHTML = "";
            if (currentUserRole === "admin" || currentUserRole === "staff") {
                deleteButtonHTML = `<button class="btn-delete" data-id="${product.id}">Delete</button>`;
            }
    
            productElement.innerHTML = `
                ${deleteButtonHTML}
                <img src="${imageUrl}" alt="${product.name}" onerror="this.src='/static/images/default.jpg';">
                <h3>${product.name}</h3>
                <p class="price">£${parseFloat(product.price).toFixed(2)}</p>
                <p class="desc">${product.description}</p>
                <button class="add-btn" data-id="${product.id}" data-name="${product.name}" data-price="${product.price}">
                    Add to Cart
                </button>
            `;
    
            productsGrid.appendChild(productElement);
        });
    
        attachDeleteEventListeners();
        attachAddToCartEvents();
    }    

    // Attach delete button event listeners
    function attachDeleteEventListeners() {
        document.querySelectorAll(".btn-delete").forEach(button => {
            button.removeEventListener("click", deleteHandler);
            button.addEventListener("click", deleteHandler);
        });
    }

    // Function to handle product deletion
    function deleteHandler(event) {
        const productId = event.target.getAttribute("data-id");
        deleteProduct(productId);
    }

    // Function to delete a product
    async function deleteProduct(productId) {
        if (!confirm("Are you sure you want to delete this product?")) return;
        const deleteImage = confirm("Would you like to delete the image as well?");
        
        try {
            const response = await fetch(`/api/products/${productId}?delete_image=${deleteImage}`, {
                method: "DELETE",
                credentials: "include",
            });

            const data = await response.json();

            if (response.status === 401) {
                alert("You must be logged in to delete products.");
                window.location.href = "/login";
                return;
            }

            if (response.status === 403) {
                alert("You do not have permission to delete this product.");
                return;
            }

            if (data.success) {
                alert("Product deleted successfully!");
                fetchProducts();
            } else {
                alert("Error: " + data.error);
            }
        } catch (error) {
            console.error("Error deleting product:", error);
        }
    }

    // Attach "Add to Cart" button events
    function attachAddToCartEvents() {
        document.querySelectorAll('.add-btn').forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault();
                const productId = this.getAttribute('data-id');
                const productName = this.getAttribute('data-name');
                const productPrice = this.getAttribute('data-price');
                const productImage = this.closest('.Product').querySelector('img').src;

                addToCart(productId, productName, parseFloat(productPrice), productImage);
            });
        });
    }

    // Function to add item to cart
    function addToCart(id, name, price, image) {
        try {
            let cart = JSON.parse(sessionStorage.getItem('divinecart') || '{}');

            if (cart[id]) {
                cart[id].quantity += 1;
            } else {
                cart[id] = {
                    name: name,
                    price: parseFloat(price),
                    quantity: 1,
                    image: image
                };
            }

            sessionStorage.setItem('divinecart', JSON.stringify(cart));
            showNotification(`${name} added to cart`);
        } catch (error) {
            console.error('Error adding to cart:', error);
        }
    }

    // Function to show notification when adding to cart
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

    // Toggle filter dropdown
    window.toggleFilter = function (header) {
        const content = header.nextElementSibling;
        const arrow = header.querySelector('.arrow');

        content.classList.toggle('show');
        arrow.classList.toggle('rotate');
    };

    // Apply filters when form is submitted
    if (filterForm) {
        filterForm.addEventListener("submit", function (event) {
            event.preventDefault();
            applyFilters();
        });
    }

    // Search filter triggers dynamically
    searchInput?.addEventListener("input", debounce(() => applyFilters(), 300));

    // Function to apply filters
    function applyFilters() {
        if (allProducts.length === 0) return;

        const searchQuery = searchInput.value.toLowerCase().trim();
        const selectedCollection = document.querySelector('input[name="collections"]:checked')?.value || 'None';

        const checkedTypes = [];
        document.querySelectorAll('input[name="Bracelets"]:checked, input[name="Earrings"]:checked, input[name="Rings"]:checked, input[name="Watches"]:checked, input[name="Necklaces"]:checked')
            .forEach(checkbox => {
                checkedTypes.push(checkbox.value.toLowerCase());
            });

        const sortOption = document.querySelector('input[name="sort"]:checked')?.value || 'Recommended';
        const inStockChecked = document.querySelector('#InStock')?.checked || false;

        let filteredProducts = allProducts.filter(product => {
            const productName = product.name.toLowerCase();
            const productType = product.type?.toLowerCase() || '';
            const productCollection = product.collection?.toLowerCase() || '';

            let shouldShow = true;

            // Search Query Filtering (searches both name and description)
            if (searchQuery && !productName.includes(searchQuery) && !product.description.toLowerCase().includes(searchQuery)) {
                shouldShow = false;
            }

            // Collection Filtering
            if (selectedCollection !== 'None' && productCollection !== selectedCollection.toLowerCase().trim()) {
                shouldShow = false;
            }

            // Product Type Filtering
            if (checkedTypes.length > 0 && !checkedTypes.includes(productType)) {
                shouldShow = false;
            }

            // In-Stock Filtering
            if (inStockChecked && product.in_stock !== true) {
                shouldShow = false;
            }

            return shouldShow;
        });

        // If no filters are selected, show all products
        if (sortOption !== 'Recommended') {
            filteredProducts = sortProducts(filteredProducts, sortOption);
        }
        updateProductList(filteredProducts);
        

        // Show/hide "no results found" message
        if (filteredProducts.length === 0) {
            showEmptyState();
        } else {
            hideEmptyState();
        }
    }

    // Function to sort products
    function sortProducts(products, sortOption) {
        products.sort((a, b) => {
            const priceA = parseFloat(a.price);
            const priceB = parseFloat(b.price);
            return sortOption === 'HighLow' ? priceB - priceA : priceA - priceB;
        });

        updateProductList(products);
    }

    // Show or hide empty state
    function showEmptyState() {
        productsGrid.innerHTML = `<div class="empty-state"><div class="empty-icon">🔍</div><h3>No products found</h3><p>Try adjusting your filters or search terms</p></div>`;
    }
    function hideEmptyState() {
        document.querySelector('.empty-state')?.remove();
    }

    // Debounce function
    function debounce(func, delay) {
        let timeout;
        return function () {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, arguments), delay);
        };
    }

    fetchProducts();
});