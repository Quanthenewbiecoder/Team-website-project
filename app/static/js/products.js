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
    let isLoggedIn = document.body.getAttribute('data-logged-in') === 'true';

    async function fetchCurrentUser() {
        try {
            const response = await fetch('/api/get-current-user', { credentials: 'include' });
            const data = await response.json();

            if (data.success) {
                currentUserRole = data.user.role;
                console.log("User role:", currentUserRole); 
            }
        } catch (error) {
            console.error("Error fetching user:", error);
        }
    }

    document.addEventListener("DOMContentLoaded", async function () {
        await fetchProducts();
    
        if (filterForm) {
            filterForm.addEventListener("submit", function (event) {
                event.preventDefault();
                applyFilters();
            });
        }
    });

    async function fetchProducts() {
        await fetchCurrentUser();
        
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
    
            if (data.success && Array.isArray(data.products)) {
                allProducts = data.products;
                updateProductList(allProducts); 
            } else {
                console.error("Error fetching products:", data.error || "Invalid data format");
                allProducts = []; 
                
            }
        } catch (error) {
            console.error("Fetch error:", error);
            allProducts = []; 
            
        }

        updateProductList(allProducts);
        loadWishlistStatus(); 
    }    
    
    function updateProductList(products) {
        if (!Array.isArray(products)) {
            console.error("Error: products is not an array.", products);
            products = [];
        }
        
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
    
            if (!imageUrl || imageUrl.trim() === "") {
                imageUrl = "/static/images/default.jpg";
            }
    
            const productElement = document.createElement("div");
            productElement.classList.add("Product");
            productElement.dataset.id = product.id;
            productElement.dataset.type = product.type;
            productElement.dataset.collection = product.collection;
    
            let deleteButtonHTML = "";
            if (currentUserRole === "admin" || currentUserRole === "staff") {
                deleteButtonHTML = `<button class="btn-delete" data-id="${product.id}">Delete</button>`;
            }

            let wishlistButtonHTML = "";
            if (isLoggedIn) {
                wishlistButtonHTML = `
                    <button class="wishlist-btn" data-id="${product.id}" data-name="${product.name}" 
                            data-price="${product.price}" data-image="${imageUrl}">
                        <i class="fas fa-heart"></i>
                    </button>
                `;
            }
    
            productElement.innerHTML = `
                ${deleteButtonHTML}
                ${wishlistButtonHTML}
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
        
        attachProductNavigation();
        attachDeleteEventListeners();
        attachAddToCartEvents();
        attachWishlistEvents();
        loadWishlistStatus(); 
    }    

    async function fetchProductReviews(productId) {
        try {
            const response = await fetch(`/api/products/${productId}/reviews`);
            const reviews = await response.json();
            const reviewsContainer = document.getElementById(`reviews-${productId}`);

            if (reviews.length === 0) {
                reviewsContainer.innerHTML = "<p>No reviews yet.</p>";
                return;
            }

            let reviewsHTML = "<strong>Reviews:</strong><ul>";
            reviews.forEach(review => {
                reviewsHTML += `<li>⭐ ${review.rating}/5 - ${review.review} <em>(${review.created_at})</em></li>`;
            });
            reviewsHTML += "</ul>";

            reviewsContainer.innerHTML = reviewsHTML;
        } catch (error) {
            console.error(`Error loading reviews for product ${productId}:`, error);
            const reviewsContainer = document.getElementById(`reviews-${productId}`);
        }
    }

    async function submitReview(event, productId) {
        event.preventDefault(); 
    
        const reviewText = document.querySelector(`#review-text-${productId}`).value.trim();
        const rating = document.querySelector(`#review-rating-${productId}`).value;
    
        if (!reviewText || !rating) {
            alert("Please enter both a review and a rating.");
            return;
        }
    
        try {
            const response = await fetch(`/products/${productId}/review`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    review: reviewText,
                    rating: rating
                })
            });
    
            if (response.ok) {
                alert("Review submitted successfully!");
                location.reload();
            } else {
                const data = await response.json();
                alert(data.error || "Failed to submit review.");
            }
        } catch (error) {
            console.error("Error submitting review:", error);
            alert("An error occurred while submitting your review.");
        }
    }    

    function attachProductNavigation() {
        document.querySelectorAll(".Product").forEach(product => {
            product.addEventListener("click", function (e) {
                if (e.target.classList.contains("add-btn") || 
                    e.target.classList.contains("wishlist-btn") || 
                    e.target.tagName === "I" || 
                    e.target.classList.contains("btn-delete")) {
                    return;
                }
                
                const productId = this.getAttribute("data-id");
        
                if (!productId || productId.trim() === "") {
                    console.error("Invalid Product ID detected!");
                    return;
                }
                
                window.location.href = `/products/${productId}`;
            });
        });
    }

    function attachDeleteEventListeners() {
        document.querySelectorAll(".btn-delete").forEach(button => {
            button.removeEventListener("click", deleteHandler);
            button.addEventListener("click", deleteHandler);
        });
    }

    function deleteHandler(event) {
        event.stopPropagation(); 
        const productId = event.target.getAttribute("data-id");
        deleteProduct(productId);
    }

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

    function attachAddToCartEvents() {
        document.querySelectorAll('.add-btn').forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                
                const productId = this.getAttribute('data-id');
                const productName = this.getAttribute('data-name');
                const productPrice = this.getAttribute('data-price');
                const productImage = this.closest('.Product').querySelector('img').src;

                addToCart(productId, productName, parseFloat(productPrice), productImage);
            });
        });
    }

    function attachWishlistEvents() {
        document.querySelectorAll('.wishlist-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                const productId = this.getAttribute('data-id');
                const productName = this.getAttribute('data-name');
                const productPrice = this.getAttribute('data-price');
                const productImage = this.getAttribute('data-image');

                toggleWishlistItem(this, productId, productName, productPrice, productImage);
            });
        });
    }

    function toggleWishlistItem(button, id, name, price, image) {
        let wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
        const index = wishlist.findIndex(item => item.id === id);
        
        if (index === -1) {
            wishlist.push({
                id: id,
                name: name,
                price: parseFloat(price),
                image: image
            });
            
            button.classList.add('active');
            showNotification(`${name} added to wishlist`);
        } else {
            wishlist.splice(index, 1);
            button.classList.remove('active');
            showNotification(`${name} removed from wishlist`, 'error');
        }
        
        localStorage.setItem('divineWishlist', JSON.stringify(wishlist));
    }

    function loadWishlistStatus() {
        if (!isLoggedIn) return;
        
        const wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
        const wishlistIds = wishlist.map(item => item.id);
        
        document.querySelectorAll('.wishlist-btn').forEach(button => {
            const productId = button.getAttribute('data-id');
            if (wishlistIds.includes(productId)) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
    }

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

    function showNotification(message, type = '') {
        const notification = document.createElement('div');
        notification.className = `cart-notification ${type}`;
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

    window.toggleFilter = function (header) {
        const content = header.nextElementSibling;
        const arrow = header.querySelector('.arrow');

        content.classList.toggle('show');
        arrow.classList.toggle('rotate');
    };

    if (filterForm) {
        filterForm.addEventListener("submit", function (event) {
            event.preventDefault();
            applyFilters();
        });
    }

    searchInput?.addEventListener("input", debounce(() => applyFilters(), 300));

    function applyFilters() {
        if (!Array.isArray(allProducts)) {
            console.error("Error: allProducts is not an array or is undefined.", allProducts);
            allProducts = [];
        }
    
        if (allProducts.length === 0) {
            showEmptyState();
            return;
        }

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

            if (searchQuery && !productName.includes(searchQuery) && !product.description.toLowerCase().includes(searchQuery)) {
                shouldShow = false;
            }

            if (selectedCollection !== 'None' && productCollection !== selectedCollection.toLowerCase().trim()) {
                shouldShow = false;
            }

            if (checkedTypes.length > 0 && !checkedTypes.includes(productType)) {
                shouldShow = false;
            }

            if (inStockChecked && product.in_stock !== true) {
                shouldShow = false;
            }

            return shouldShow;
        });

        if (sortOption !== 'Recommended') {
            filteredProducts = sortProducts(filteredProducts, sortOption);
        }
        updateProductList(filteredProducts);
    }

    function sortProducts(products, sortOption) {
        if (!Array.isArray(products)) {
            console.error("Error: products is not an array before sorting.", products);
            return [];
        }
    
        let sortedProducts = [...products];
    
        if (sortOption === 'HighLow') {
            sortedProducts.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
        } else if (sortOption === 'LowHigh') {
            sortedProducts.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
        }
    
        return sortedProducts;
    }    

    function showEmptyState() {
        productsGrid.innerHTML = `<div class="empty-state"><div class="empty-icon">🔍</div><h3>No products found</h3><p>Try adjusting your filters or search terms</p></div>`;
    }
    function hideEmptyState() {
        document.querySelector('.empty-state')?.remove();
    }

    function debounce(func, delay) {
        let timeout;
        return function () {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, arguments), delay);
        };
    }

    fetchProducts();
});