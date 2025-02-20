document.addEventListener("DOMContentLoaded", function () {
    function toggleFilter(header) {
        const content = header.nextElementSibling;
        const arrow = header.querySelector('.arrow');
        content.classList.toggle('show');
        arrow.classList.toggle('rotate');
    }
    
    window.toggleFilter = toggleFilter;

    const searchSection = document.querySelector('.filter-section:first-child .filter-content');
    const searchArrow = document.querySelector('.filter-section:first-child .arrow');
    if (searchSection && searchArrow) {
        searchSection.classList.add('show');
        searchArrow.classList.add('rotate');
    }

    const searchInput = document.getElementById("Search");
    const filterForm = document.getElementById("Form");
    const productsGrid = document.getElementById("products-grid");
    const productCards = document.querySelectorAll(".Product");
    
    document.querySelectorAll('.add-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const isLoggedIn = document.body.getAttribute('data-logged-in') === 'true';
            
            if (!isLoggedIn) {
                window.location.href = '/login?redirect=products';
                return;
            }
            
            const productId = this.getAttribute('data-id');
            const productName = this.getAttribute('data-name');
            const productPrice = this.getAttribute('data-price');
            const productImage = this.closest('.Product').querySelector('img').src;
            
            addToCart(productId, productName, parseFloat(productPrice), productImage);
        });
    });
    
    async function addToCart(id, name, price, image) {
        try {
            const response = await fetch('/basket/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: id,
                    product_name: name,
                    price: price,
                    quantity: 1,
                    image: image
                })
            });
            
            if (response.ok) {
                showNotification(`${name} added to cart`);
            }
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
    
    filterForm.addEventListener("submit", function(event) {
        event.preventDefault();
        applyFilters();
    });
    
    searchInput.addEventListener("input", debounce(function() {
        applyFilters();
    }, 300));
    
    function applyFilters() {
        const searchQuery = searchInput.value.toLowerCase();
        const selectedCollectionRadio = document.querySelector('input[name="collections"]:checked');
        const selectedCollection = selectedCollectionRadio ? selectedCollectionRadio.value : 'None';
        
        const checkedTypes = [];
        document.querySelectorAll('input[type="checkbox"][id="Bracelets"], input[type="checkbox"][id="Earrings"], input[type="checkbox"][id="Rings"], input[type="checkbox"][id="Watches"], input[type="checkbox"][id="Necklaces"]').forEach(checkbox => {
            if (checkbox.checked) {
                let type = checkbox.id.toLowerCase();
                if (type === 'earrings') type = 'earring';
                if (type === 'bracelets') type = 'bracelet';
                if (type === 'rings') type = 'ring';
                if (type === 'watches') type = 'watch';
                if (type === 'necklaces') type = 'necklace'; 
                checkedTypes.push(type);
            }
        });
        
        const sortOption = document.querySelector('input[name="sort"]:checked').value;
        
        const inStockOnly = document.getElementById('InStock').checked;
        const newOnly = document.getElementById('New').checked;
        const onSaleOnly = document.getElementById('OnSale').checked;
        
        productCards.forEach(product => {
            const productName = product.querySelector('h3').textContent.toLowerCase();
            const productType = product.getAttribute('data-type');
            const productCollection = product.getAttribute('data-collection');
            
            let shouldShow = true;
            
            if (searchQuery && !productName.includes(searchQuery)) {
                shouldShow = false;
            }
            
            if (selectedCollection !== 'None' && productCollection !== selectedCollection.toLowerCase()) {
                shouldShow = false;
            }
            
            if (checkedTypes.length > 0 && !checkedTypes.includes(productType)) {
                shouldShow = false;
            }
            
            product.style.display = shouldShow ? 'flex' : 'none';
        });
        
        if (sortOption !== 'Recommended') {
            sortProducts(sortOption);
        }
        
        const visibleProducts = Array.from(productCards).filter(p => p.style.display !== 'none');
        if (visibleProducts.length === 0) {
            showEmptyState();
        } else {
            hideEmptyState();
        }
    }
    
    function sortProducts(sortOption) {
        const products = Array.from(productCards).filter(p => p.style.display !== 'none');
        
        products.sort((a, b) => {
            const priceA = parseFloat(a.querySelector('.price').textContent.replace('£', ''));
            const priceB = parseFloat(b.querySelector('.price').textContent.replace('£', ''));
            
            if (sortOption === 'HighLow') {
                return priceB - priceA;
            } else if (sortOption === 'LowHigh') {
                return priceA - priceB;
            }
            return 0;
        });
        
        products.forEach(product => {
            productsGrid.appendChild(product);
        });
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
    
    function debounce(func, delay) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), delay);
        };
    }
    
    applyFilters();
});