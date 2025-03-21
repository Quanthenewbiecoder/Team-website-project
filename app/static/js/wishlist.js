document.addEventListener('DOMContentLoaded', function() {
    loadWishlist();
    setupEventListeners();
});

function initWishlist() {
    if (!localStorage.getItem('divineWishlist')) {
        localStorage.setItem('divineWishlist', JSON.stringify([]));
    }
}

function loadWishlist() {
    initWishlist();
    const wishlistItems = JSON.parse(localStorage.getItem('divineWishlist')) || [];
    const wishlistGrid = document.getElementById('wishlist-grid');
    const emptyWishlist = document.getElementById('empty-wishlist');
    
    if (wishlistGrid) {
        wishlistGrid.innerHTML = '';
        
        if (wishlistItems.length === 0) {
            if (emptyWishlist) {
                emptyWishlist.style.display = 'block';
            }
            return;
        }
        
        if (emptyWishlist) {
            emptyWishlist.style.display = 'none';
        }
        
        wishlistItems.forEach(item => {
            const wishlistItem = createWishlistItemElement(item);
            wishlistGrid.appendChild(wishlistItem);
        });
    }
}

function createWishlistItemElement(item) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'wishlist-item';
    itemDiv.setAttribute('data-id', item.id);
    
    itemDiv.innerHTML = `
        <img src="${item.image}" alt="${item.name}" onerror="this.src='/static/images/default.jpg';">
        <div class="heart-icon active">
            <i class="fas fa-heart"></i>
        </div>
        <h3>${item.name}</h3>
        <p class="price">£${parseFloat(item.price).toFixed(2)}</p>
        <div class="wishlist-actions">
            <button class="add-to-cart" data-id="${item.id}" data-name="${item.name}" data-price="${item.price}">
                Add to Cart
            </button>
            <button class="remove-from-wishlist" data-id="${item.id}">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    
    return itemDiv;
}

function setupEventListeners() {
    const wishlistGrid = document.getElementById('wishlist-grid');
    const clearWishlistBtn = document.getElementById('clear-wishlist-btn');
    
    if (wishlistGrid) {
        wishlistGrid.addEventListener('click', function(e) {
            const target = e.target;
            
            if (target.classList.contains('add-to-cart') || target.closest('.add-to-cart')) {
                const button = target.classList.contains('add-to-cart') ? target : target.closest('.add-to-cart');
                const id = button.getAttribute('data-id');
                const name = button.getAttribute('data-name');
                const price = parseFloat(button.getAttribute('data-price'));
                const item = document.querySelector(`.wishlist-item[data-id="${id}"]`);
                const image = item.querySelector('img').src;
                
                addToCart(id, name, price, image);
                e.stopPropagation();
            }
            
            if (target.classList.contains('remove-from-wishlist') || target.closest('.remove-from-wishlist')) {
                const button = target.classList.contains('remove-from-wishlist') ? target : target.closest('.remove-from-wishlist');
                const id = button.getAttribute('data-id');
                removeFromWishlist(id);
                e.stopPropagation();
            }
            
            if (target.classList.contains('heart-icon') || target.closest('.heart-icon')) {
                const heartIcon = target.classList.contains('heart-icon') ? target : target.closest('.heart-icon');
                const id = heartIcon.closest('.wishlist-item').getAttribute('data-id');
                removeFromWishlist(id);
                e.stopPropagation(); 
            }
        });
    }
    
    if (clearWishlistBtn) {
        clearWishlistBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to clear your wishlist?')) {
                clearWishlist();
            }
        });
    }
    
    document.querySelectorAll('.wishlist-item').forEach(item => {
        item.addEventListener('click', function(e) {
            if (e.target.tagName === 'BUTTON' || 
                e.target.closest('button') || 
                e.target.classList.contains('heart-icon') || 
                e.target.closest('.heart-icon') ||
                e.target.tagName === 'I') {
                return;
            }
            
            const productId = this.getAttribute('data-id');
            window.location.href = `/products/${productId}`;
        });
    });
}

function addToCart(id, name, price, image) {
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
}

function removeFromWishlist(id) {
    let wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
    
    const itemToRemove = wishlist.find(item => item.id === id);
    
    wishlist = wishlist.filter(item => item.id !== id);
    
    localStorage.setItem('divineWishlist', JSON.stringify(wishlist));
    
    if (itemToRemove) {
        showNotification(`${itemToRemove.name} removed from wishlist`, 'error');
    }
    
    loadWishlist();
}

function clearWishlist() {
    localStorage.setItem('divineWishlist', JSON.stringify([]));
    loadWishlist();
    showNotification('Wishlist has been cleared', 'error');
}

function showNotification(message, type = '') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function updateWishlistCount() {
    const wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
    const count = wishlist.length;
    
    const countBadge = document.querySelector('.wishlist-count');
    if (countBadge) {
        countBadge.textContent = count;
        countBadge.style.display = count > 0 ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initWishlist();
    loadWishlist();
    setupEventListeners();
    updateWishlistCount();
});

window.wishlistFunctions = {
    addToWishlist: function(id, name, price, image) {
        let wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
        
        if (!wishlist.some(item => item.id === id)) {
            wishlist.push({
                id: id,
                name: name,
                price: parseFloat(price),
                image: image
            });
            
            localStorage.setItem('divineWishlist', JSON.stringify(wishlist));
            updateWishlistCount();
            showNotification(`${name} added to wishlist`);
            return true;
        }
        return false;
    },
    
    removeFromWishlist: removeFromWishlist,
    clearWishlist: clearWishlist,
    isInWishlist: function(id) {
        const wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
        return wishlist.some(item => item.id === id);
    }
};