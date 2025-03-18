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
        <img src="${item.image}" alt="${item.name}">
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
            }
            
            if (target.classList.contains('remove-from-wishlist') || target.closest('.remove-from-wishlist')) {
                const button = target.classList.contains('remove-from-wishlist') ? target : target.closest('.remove-from-wishlist');
                const id = button.getAttribute('data-id');
                removeFromWishlist(id);
            }
            
            if (target.classList.contains('heart-icon') || target.closest('.heart-icon')) {
                const heartIcon = target.classList.contains('heart-icon') ? target : target.closest('.heart-icon');
                const id = heartIcon.closest('.wishlist-item').getAttribute('data-id');
                removeFromWishlist(id);
            }
        });
    }
    
    document.querySelectorAll('.button-heart').forEach(heartBtn => {
        heartBtn.addEventListener('click', function() {
            const productCard = this.closest('.card, .Product');
            if (!productCard) return;
            
            const id = productCard.getAttribute('data-id');
            const name = productCard.querySelector('h3').textContent;
            const priceText = productCard.querySelector('.price').textContent;
            const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
            const image = productCard.querySelector('img').src;
            
            this.classList.toggle('is-active');
            
            if (this.classList.contains('is-active')) {
                addToWishlist(id, name, price, image);
            } else {
                removeFromWishlist(id);
            }
        });
    });
}

function addToCart(id, name, price, image) {
    let cart = JSON.parse(sessionStorage.getItem('divinecart') || '{}');
    
    if (cart[id]) {
        cart[id].quantity += 1;
    } else {
        cart[id] = {
            product_name: name,
            price: parseFloat(price),
            quantity: 1,
            image: image
        };
    }
    
    sessionStorage.setItem('divinecart', JSON.stringify(cart));
    
    showNotification(`${name} added to cart`);
}

function addToWishlist(id, name, price, image) {
    const wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
    
    if (!wishlist.some(item => item.id === id)) {
        wishlist.push({
            id: id,
            name: name,
            price: price,
            image: image
        });
        
        localStorage.setItem('divineWishlist', JSON.stringify(wishlist));
        showNotification(`${name} added to wishlist`);
    }
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

function initHeartIcons() {
    const wishlist = JSON.parse(localStorage.getItem('divineWishlist')) || [];
    const wishlistIds = wishlist.map(item => item.id);
    
    document.querySelectorAll('.card, .Product').forEach(product => {
        const id = product.getAttribute('data-id');
        const heartIcon = product.querySelector('.button-heart');
        
        if (heartIcon && wishlistIds.includes(id)) {
            heartIcon.classList.add('is-active');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    initWishlist();
    loadWishlist();
    setupEventListeners();
    initHeartIcons();
});