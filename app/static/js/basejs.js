window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 80) {
    navbar.classList.add('sticky');
  } else {
    navbar.classList.remove('sticky');
  }
});

window.addEventListener('resize', () => {
  const menu = document.querySelector('.menu');
  if (window.innerWidth > 900 && menu.classList.contains('show')) {
    menu.classList.remove('show');
    document.removeEventListener('click', closeMenuOutside);
  }
});

// Shopping bag pop-up functionality
let cartCount = 1;
let subtotal = 6250;

document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-btn");
    const closePopup = document.getElementById("close-popup");
    const shoppingBagPopup = document.getElementById("shopping-bag-popup");
    
    addToCartButtons.forEach(button => {
        button.addEventListener("click", addItem);
    });
    
    if (closePopup) {
        closePopup.addEventListener("click", function () {
            shoppingBagPopup.style.display = "none";
        });
    }
});

function addItem() {
    cartCount++;
    subtotal += 6250;

    document.getElementById("cart-count").textContent = cartCount;
    document.getElementById("subtotal-price").textContent = `£${subtotal}`;

    let cartItems = document.getElementById("cart-items");
    let newItem = document.createElement("div");
    newItem.classList.add("cart-item");
    newItem.innerHTML = `
        <img src="/static/images/love_bracelet.png" alt="Love Bracelet" class="product-image">
        <div class="product-details">
            <h3>LOVE BRACELET, MEDIUM MODEL</h3>
            <p>White gold</p>
            <p><strong>£6,250</strong></p>
            <p>Size: 20 CM</p>
        </div>
        <span class="remove-item" onclick="removeItem(this)">&times;</span>
    `;
    cartItems.appendChild(newItem);

    document.getElementById("shopping-bag-popup").style.display = "block";
}

function removeItem(element) {
    let itemPrice = 6250;
    cartCount--;
    subtotal -= itemPrice;

    document.getElementById("cart-count").textContent = cartCount;
    document.getElementById("subtotal-price").textContent = `£${subtotal}`;

    element.parentElement.remove();
}


function openPopup(img) {
  const popupOverlay = document.querySelector('.popup-overlay');
  const popupImage = document.getElementById('popup-image');
  if (popupOverlay && popupImage) {
    popupImage.src = img.src;
    popupOverlay.style.display = 'flex';
  }
}

function closePopup() {
  const popupOverlay = document.querySelector('.popup-overlay');
  if (popupOverlay) {
    popupOverlay.style.display = 'none';
  }
}