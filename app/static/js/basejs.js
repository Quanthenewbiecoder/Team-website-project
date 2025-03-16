document.addEventListener("DOMContentLoaded", function() {
  const hamburger = document.querySelector('.hamburger');
  const menu = document.querySelector('.menu');
  
  if (hamburger) {
      hamburger.addEventListener('click', function(e) {
          e.stopPropagation();
          menu.classList.toggle('show');
      });
  }
  
  document.addEventListener('click', function(e) {
      if (menu && menu.classList.contains('show') && 
          !menu.contains(e.target) && 
          !hamburger.contains(e.target)) {
          menu.classList.remove('show');
      }
  });
  
  window.addEventListener('scroll', function() {
      const navbar = document.querySelector('.navbar');
      if (window.scrollY > 80) {
          navbar.classList.add('sticky');
      } else {
          navbar.classList.remove('sticky');
      }
  });
  
  window.addEventListener('resize', function() {
      if (window.innerWidth > 900 && menu.classList.contains('show')) {
          menu.classList.remove('show');
      }
  });

  const addToCartButtons = document.querySelectorAll(".add-btn");
  if (addToCartButtons.length > 0) {
      addToCartButtons.forEach(button => {
          button.addEventListener("click", addToCart);
      });
  }
  
  const closePopup = document.getElementById("close-popup");
  const shoppingBagPopup = document.getElementById("shopping-bag-popup");
  if (closePopup && shoppingBagPopup) {
      closePopup.addEventListener("click", function() {
          shoppingBagPopup.style.display = "none";
      });
  }
});

function addToCart() {
  const cartCountElement = document.getElementById("cart-count");
  const subtotalElement = document.getElementById("subtotal-price");
  const cartItems = document.getElementById("cart-items");
  const shoppingBagPopup = document.getElementById("shopping-bag-popup");
  
  if (cartCountElement) {
      let cartCount = parseInt(cartCountElement.textContent) || 0;
      cartCount++;
      cartCountElement.textContent = cartCount;
  }
  
  if (subtotalElement) {
      let subtotal = parseFloat(subtotalElement.textContent.replace('£', '')) || 0;
      subtotal += 6250;
      subtotalElement.textContent = `£${subtotal}`;
  }
  
  if (cartItems) {
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
  }
  
  if (shoppingBagPopup) {
      shoppingBagPopup.style.display = "block";
  }
}

function removeItem(element) {
  const cartCountElement = document.getElementById("cart-count");
  const subtotalElement = document.getElementById("subtotal-price");
  
  if (cartCountElement) {
      let cartCount = parseInt(cartCountElement.textContent) || 0;
      if (cartCount > 0) cartCount--;
      cartCountElement.textContent = cartCount;
  }
  
  if (subtotalElement) {
      let subtotal = parseFloat(subtotalElement.textContent.replace('£', '')) || 0;
      subtotal -= 6250;
      if (subtotal < 0) subtotal = 0;
      subtotalElement.textContent = `£${subtotal}`;
  }
  
  if (element.parentElement) {
      element.parentElement.remove();
  }
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

let currentFlow = null;
let userName = null;
let userEmail = null;
let userInquiry = null;
let orderNumber = null;

function closeBubble() {
  const speechBubble = document.getElementById('speech-bubble');
  if (speechBubble) {
      speechBubble.style.display = 'none';
  }
}

function toggleChat() {
  const popup = document.getElementById('chat-popup');
  if (popup) {
      popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
  }
}

function resetChat() {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  chatBody.innerHTML = `
    <div class="chat-message bot"><span>Hello! I'm Divine AI. How can I assist you today?</span></div>
    <div class="chat-options" id="initial-options">
      <button onclick="handleOption('tracking')">Tracking my order</button>
      <button onclick="handleOption('returns')">Do you offer returns?</button>
      <button onclick="handleOption('best-selling')">What is your best-selling piece?</button>
      <button onclick="handleOption('other')">Other enquiry</button>
      <button onclick="handleOption('agent')">Speak to an agent</button>
    </div>
  `;
  userName = null;
  userEmail = null;
  userInquiry = null;
  orderNumber = null;
  enableInput();
}

function enableInput() {
  const input = document.getElementById('user-input');
  if (input) {
      input.disabled = false;
      input.placeholder = "Type your message...";
  }
}

function disableInput() {
  const input = document.getElementById('user-input');
  if (input) {
      input.disabled = true;
      input.placeholder = "Please select an option above...";
  }
}

function handleOption(option) {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  const initialOptions = document.getElementById('initial-options');
  if (initialOptions) {
      initialOptions.style.display = 'none';
  }
  
  currentFlow = option;

  if (option === 'tracking') {
      chatBody.innerHTML += `<div class="chat-message bot"><span>To track your order, email our support team at support@thedivinejewelry.com.</span></div>`;
      askFollowUp();
  } else if (option === 'returns') {
      chatBody.innerHTML += `<div class="chat-message bot"><span>We do not accept returns, but exchanges are available. Would you like to exchange your product?</span></div>`;
      chatBody.innerHTML += `<div class="chat-options">
          <button onclick="handleExchange(true)">YES</button>
          <button onclick="handleExchange(false)">NO</button>
      </div>`;
      disableInput();
  } else if (option === 'best-selling') {
      chatBody.innerHTML += `<div class="chat-message bot"><span>The Pearl Collection is known to be our best-selling line due to its timeless elegance, exquisite craftsmanship, and luxurious appeal.</span></div>`;
      askToSpeakToExpert();
  } else if (option === 'other') {
      askForName();
  } else if (option === 'agent') {
      chatBody.innerHTML += `<div class="chat-message bot"><span>Connecting you to an agent now…</span></div>`;
      setTimeout(() => {
          chatBody.innerHTML += `<div class="chat-message bot"><span>All our agents are currently assisting other customers at the moment. Would you like to join the queue and wait for the next available agent?</span></div>`;
          chatBody.innerHTML += `<div class="chat-options">
              <button onclick="handleQueue(true)">YES</button>
              <button onclick="handleQueue(false)">NO</button>
          </div>`;
          disableInput();
      }, 2000);
  }
}

function askToSpeakToExpert() {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  chatBody.innerHTML += `<div class="chat-message bot"><span>Would you like to speak to an expert?</span></div>`;
  chatBody.innerHTML += `<div class="chat-options">
      <button onclick="handleExpert(true)">YES</button>
      <button onclick="handleExpert(false)">NO</button>
  </div>`;
  disableInput();
}

function handleExpert(wantsExpert) {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  if (wantsExpert) {
      askForName();
  } else {
      chatBody.innerHTML += `<div class="chat-message bot"><span>Okay, have a great day!</span></div>`;
  }
  enableInput();
}

function askFollowUp() {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  chatBody.innerHTML += `<div class="chat-message bot"><span>Are you happy with this response?</span></div>`;
  chatBody.innerHTML += `<div class="chat-options">
      <button onclick="handleFollowUp(true)">YES</button>
      <button onclick="handleFollowUp(false)">NO</button>
  </div>`;
  disableInput();
}

function handleFollowUp(isHappy) {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  if (isHappy) {
      chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you! I'm glad I could assist you. Have a great day!</span></div>`;
  } else {
      if (currentFlow === 'tracking') {
          askForName();
      }
  }
  enableInput();
}

function askForName() {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  chatBody.innerHTML += `<div class="chat-message bot"><span>May I have your name, please?</span></div>`;
  enableInput();
}

function askForEmail() {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you, ${userName}. What is your email?</span></div>`;
  enableInput();
}

function askForInquiry() {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  chatBody.innerHTML += `<div class="chat-message bot"><span>Please enter your enquiry below.</span></div>`;
  enableInput();
}

function askForOrderNumber() {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  chatBody.innerHTML += `<div class="chat-message bot"><span>What is your order number? (Order numbers contain exactly 12 digits.)</span></div>`;
  enableInput();
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function isValidOrderNumber(orderNumber) {
  const orderNumberRegex = /^\d{12}$/;
  return orderNumberRegex.test(orderNumber);
}

function handleInput(event) {
  if (event.key === 'Enter') {
      sendMessage();
  }
}

function sendMessage() {
  const input = document.getElementById('user-input');
  const chatBody = document.getElementById('chat-body');
  if (!input || !chatBody) return;
  
  const message = input.value.trim();
  if (!message) return;
  
  chatBody.innerHTML += `<div class="chat-message user"><span>${message}</span></div>`;
  input.value = '';

  if (!currentFlow && !userName && !userEmail && !userInquiry && !orderNumber) {
      chatBody.innerHTML += `<div class="chat-message bot"><span style="color: red;">Please select from the options above or click on 'Other Enquiry' to submit a request. If you need further assistance, select 'Speak to an Agent' to connect with our support team.</span></div>`;
      return;
  }

  if (!userName) {
      userName = message;
      askForEmail();
  } else if (!userEmail) {
      if (!isValidEmail(message)) {
          chatBody.innerHTML += `<div class="chat-message bot"><span style="color: red;">Invalid email. Please enter a valid email address.</span></div>`;
          return;
      }
      userEmail = message;
      if (currentFlow === 'other') {
          askForInquiry();
      } else if (currentFlow === 'returns') {
          askForOrderNumber();
      } else if (currentFlow === 'best-selling' || currentFlow === 'agent') {
          if (currentFlow === 'agent') {
              chatBody.innerHTML += `<div class="chat-message bot"><span>You are No. 2 in our queue. An agent will reach out to you via email. Thank you for your patience.</span></div>`;
          } else {
              chatBody.innerHTML += `<div class="chat-message bot"><span>Our expert will reach out to you via email shortly. In the meantime, feel free to browse through our collections!</span></div>`;
          }
      } else if (currentFlow === 'tracking') {
          chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you for providing your email. Our support team will reach out to you via email with live tracking details for your order.</span></div>`;
      }
  } else if (!userInquiry && currentFlow === 'other') {
      userInquiry = message;
      saveInquiry(userName, userEmail, userInquiry);
      chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you for providing your email and enquiry. Our AI expert will reach out to you via email shortly.</span></div>`;
  } else if (!orderNumber && currentFlow === 'returns') {
      if (!isValidOrderNumber(message)) {
          chatBody.innerHTML += `<div class="chat-message bot"><span style="color: red;">Invalid order number. Order numbers must contain exactly 12 digits.</span></div>`;
          return;
      }
      orderNumber = message;
      saveInquiry(userName, userEmail, `Order Number: ${orderNumber}`);
      chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you for providing your email and order number. Our support team will reach out to you shortly to assist with your exchange or any other support you may need.</span></div>`;
  }
}

function saveInquiry(name, email, inquiry) {
  fetch('/save-inquiry', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email, inquiry }),
  })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error('Error:', error));
}

function handleExchange(wantsExchange) {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  if (wantsExchange) {
      askForName();
  } else {
      chatBody.innerHTML += `<div class="chat-message bot"><span>Okay, have a great day!</span></div>`;
  }
  enableInput();
}

function handleQueue(wantsQueue) {
  const chatBody = document.getElementById('chat-body');
  if (!chatBody) return;
  
  if (wantsQueue) {
      askForName();
  } else {
      chatBody.innerHTML += `<div class="chat-message bot"><span>Okay, have a great day!</span></div>`;
  }
  enableInput();
}