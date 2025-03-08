document.addEventListener("DOMContentLoaded", function () {
    const productsGrid = document.getElementById("products-grid");
    if (!productsGrid) {
        console.error("Error: Element with ID 'products-grid' not found.");
        return;
    }

    const searchInput = document.getElementById("Search");
    const filterForm = document.getElementById("Form");
    const searchQueryParam = new URLSearchParams(window.location.search).get('query');

    if (searchQueryParam) {
        console.log("Using server-filtered results for query:", searchQueryParam);
        attachAddToCartEvents();
        return;
    }

    let allProducts = []; 

    async function fetchProducts() {
        try {
            const response = await fetch('/api/products');
            allProducts = await response.json();
            renderProducts(allProducts);
        } catch (error) {
            console.error('Error loading products:', error);
        }
    }

    function renderProducts(products) {
        productsGrid.innerHTML = "";
    
        if (products.length === 0) {
            showEmptyState();
            return;
        }
    
        products.forEach(product => {
            //  Remove any extra 'static/' from the path
            let correctedImageURL = product.image_url.replace(/\s/g, "_");
    
            const productDiv = document.createElement("div");
            productDiv.classList.add("Product");
            productDiv.setAttribute("data-id", product.id);
            productDiv.setAttribute("data-type", product.type);
            productDiv.setAttribute("data-collection", product.collection);
    
            productDiv.innerHTML = `
                <img src="${correctedImageURL}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p class="price">£${product.price.toFixed(2)}</p>
                <p class="desc">${product.description}</p>
                <button class="add-btn" data-id="${product.id}" data-name="${product.name}" data-price="${product.price}">
                    Add to Cart
                </button>
            `;
    
            productsGrid.appendChild(productDiv);
        });
    
        attachAddToCartEvents();
    }
       

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

    async function addToCart(id, name, price, image) {
        try {
            let cart = JSON.parse(sessionStorage.getItem('divinecart') || '{}');

            if (cart[id]) {
                cart[id].quantity += 1;
            } else {
                cart[id] = {
                    name: name,
                    price: price,
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

    if (filterForm) {
        filterForm.addEventListener("submit", function(event) {
            event.preventDefault();
            applyFilters(); //  This ensures dynamic filtering without page reload
        });
    }    

    searchInput?.addEventListener("input", debounce(function () {
        applyFilters();
    }, 300));

    function applyFilters() {
        const searchQuery = searchInput.value.toLowerCase();
        const selectedCollection = document.querySelector('input[name="collections"]:checked')?.value || 'None';
        
        const checkedTypes = [];
        document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
            checkedTypes.push(checkbox.value.toLowerCase());
        });
    
        const sortOption = document.querySelector('input[name="sort"]:checked')?.value || 'Recommended';
    
        const inStockChecked = document.querySelector('#InStock')?.checked || false;
    
        const filteredProducts = allProducts.filter(product => {
            const productName = product.name.toLowerCase();
            const productType = product.type?.toLowerCase() || '';
            const productCollection = product.collection?.toLowerCase() || '';
    
            let shouldShow = true;
    
            //  Search Query Filtering
            if (searchQuery && !productName.includes(searchQuery)) {
                shouldShow = false;
            }
    
            //  Collection Filtering
            if (selectedCollection !== 'None' && productCollection !== selectedCollection.toLowerCase()) {
                shouldShow = false;
            }
    
            //  Product Type Filtering
            if (checkedTypes.length > 0 && !checkedTypes.includes(productType)) {
                shouldShow = false;
            }
    
            //  In-Stock Filtering
            if (inStockChecked && product.in_stock !== true) {
                shouldShow = false;
            }
    
            return shouldShow;
        });
    
        console.log("Filtered Products:", filteredProducts); // 🔥 Debugging Log
    
        //  Apply sorting before rendering
        if (sortOption !== 'Recommended') {
            sortProducts(filteredProducts, sortOption);
        } else {
            renderProducts(filteredProducts);
        }
    
        //  Show/hide "no results found" message
        if (filteredProducts.length === 0) {
            showEmptyState();
        } else {
            hideEmptyState();
        }
    }
    

    function sortProducts(products, sortOption) {
        products.sort((a, b) => {
            const priceA = parseFloat(a.price);
            const priceB = parseFloat(b.price);
    
            return sortOption === 'HighLow' ? priceB - priceA : priceA - priceB;
        });
    
        renderProducts(products); //  Ensure rendering updates after sorting
    }   

    function showEmptyState() {
        if (!document.querySelector('.empty-state')) {
            const emptyState = document.createElement('div');
            emptyState.className = 'empty-state';
            emptyState.innerHTML = `
                <div class="empty-icon">🔍</div>
                <h3>No products found</h3>
                <p>Try adjusting your filters or search terms</p>
            `;
            productsGrid.appendChild(emptyState);
        }
    }

    function hideEmptyState() {
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }
    }

    function toggleMenu() {
        const menu = document.getElementById("mobile-menu");
        if (menu) {
            menu.classList.toggle("show");
        } else {
            console.error("Error: Element with ID 'mobile-menu' not found.");
        }
    }     

    function debounce(func, delay) {
        let timeout;
        return function () {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, arguments), delay);
        };
    }

    window.toggleFilter = function(header) {
        const content = header.nextElementSibling;
        const arrow = header.querySelector('.arrow');

        content.classList.toggle('show');
        arrow.classList.toggle('rotate');
    };

    fetchProducts();
});