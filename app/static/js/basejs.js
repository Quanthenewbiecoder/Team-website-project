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

let currentFlow = null;
let userName = null;
let userEmail = null;
let userInquiry = null;
let orderNumber = null;

function closeBubble() {
  const speechBubble = document.getElementById('speech-bubble');
  speechBubble.style.display = 'none'; // Hide the speech bubble
}

// Toggle chat popup
function toggleChat() {
  const popup = document.getElementById('chat-popup');
  popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
}

// Reset chat to initial state
function resetChat() {
  const chatBody = document.getElementById('chat-body');
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
  enableInput(); // Re-enable input field
}

// Enable or disable input field
function enableInput() {
  const input = document.getElementById('user-input');
  input.disabled = false;
  input.placeholder = "Type your message...";
}

function disableInput() {
  const input = document.getElementById('user-input');
  input.disabled = true;
  input.placeholder = "Please select an option above...";
}

// Handle initial options
function handleOption(option) {
  const chatBody = document.getElementById('chat-body');
  currentFlow = option;

  // Clear initial options
  document.getElementById('initial-options').style.display = 'none';

  // Handle selected option
  if (option === 'tracking') {
    chatBody.innerHTML += `<div class="chat-message bot"><span>To track your order, email our support team at support@thedivinejewelry.com.</span></div>`;
    askFollowUp();
  } else if (option === 'returns') {
    chatBody.innerHTML += `<div class="chat-message bot"><span>We do not accept returns, but exchanges are available. Would you like to exchange your product?</span></div>`;
    chatBody.innerHTML += `<div class="chat-options">
      <button onclick="handleExchange(true)">YES</button>
      <button onclick="handleExchange(false)">NO</button>
    </div>`;
    disableInput(); // Disable input during Yes/No prompt
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
      disableInput(); // Disable input during Yes/No prompt
    }, 2000);
  }
}

// Ask to speak to an expert (for "What is your best-selling piece?")
function askToSpeakToExpert() {
  const chatBody = document.getElementById('chat-body');
  chatBody.innerHTML += `<div class="chat-message bot"><span>Would you like to speak to an expert?</span></div>`;
  chatBody.innerHTML += `<div class="chat-options">
    <button onclick="handleExpert(true)">YES</button>
    <button onclick="handleExpert(false)">NO</button>
  </div>`;
  disableInput(); // Disable input during Yes/No prompt
}

// Handle expert option
function handleExpert(wantsExpert) {
  const chatBody = document.getElementById('chat-body');
  if (wantsExpert) {
    askForName();
  } else {
    chatBody.innerHTML += `<div class="chat-message bot"><span>Okay, have a great day!</span></div>`;
  }
  enableInput(); // Re-enable input after Yes/No prompt
}

// Ask for follow-up
function askFollowUp() {
  const chatBody = document.getElementById('chat-body');
  chatBody.innerHTML += `<div class="chat-message bot"><span>Are you happy with this response?</span></div>`;
  chatBody.innerHTML += `<div class="chat-options">
    <button onclick="handleFollowUp(true)">YES</button>
    <button onclick="handleFollowUp(false)">NO</button>
  </div>`;
  disableInput(); // Disable input during Yes/No prompt
}

// Handle follow-up
function handleFollowUp(isHappy) {
  const chatBody = document.getElementById('chat-body');
  if (isHappy) {
    chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you! I'm glad I could assist you. Have a great day!</span></div>`;
  } else {
    if (currentFlow === 'tracking') {
      askForName();
    }
  }
  enableInput(); // Re-enable input after Yes/No prompt
}

// Ask for name
function askForName() {
  const chatBody = document.getElementById('chat-body');
  chatBody.innerHTML += `<div class="chat-message bot"><span>May I have your name, please?</span></div>`;
  enableInput(); // Re-enable input for name
}

// Ask for email
function askForEmail() {
  const chatBody = document.getElementById('chat-body');
  chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you, ${userName}. What is your email?</span></div>`;
  enableInput(); // Re-enable input for email
}

// Ask for inquiry
function askForInquiry() {
  const chatBody = document.getElementById('chat-body');
  chatBody.innerHTML += `<div class="chat-message bot"><span>Please enter your enquiry below.</span></div>`;
  enableInput(); // Re-enable input for inquiry
}

// Ask for order number
function askForOrderNumber() {
  const chatBody = document.getElementById('chat-body');
  chatBody.innerHTML += `<div class="chat-message bot"><span>What is your order number? (Order numbers contain exactly 12 digits.)</span></div>`;
  enableInput(); // Re-enable input for order number
}

// Validate email
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Validate order number (12 digits)
function isValidOrderNumber(orderNumber) {
  const orderNumberRegex = /^\d{12}$/;
  return orderNumberRegex.test(orderNumber);
}

// Handle user input
function handleInput(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
}

// Send message
function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (message) {
    const chatBody = document.getElementById('chat-body');
    chatBody.innerHTML += `<div class="chat-message user"><span>${message}</span></div>`;
    input.value = '';

    // Check if the user is in a valid flow
    if (!currentFlow && !userName && !userEmail && !userInquiry && !orderNumber) {
      chatBody.innerHTML += `<div class="chat-message bot"><span style="color: red;">Please select from the options above or click on 'Other Enquiry' to submit a request. If you need further assistance, select 'Speak to an Agent' to connect with our support team.</span></div>`;
      return; // Stop further processing
    }

    if (!userName) {
      userName = message;
      askForEmail();
    } else if (!userEmail) {
      if (!isValidEmail(message)) {
        chatBody.innerHTML += `<div class="chat-message bot"><span style="color: red;">Invalid email. Please enter a valid email address.</span></div>`;
        return; // Stop further processing
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
          chatBody.innerHTML += `<div class="chat-message bot"><span>Our expert will reach out to you via email shortly. In the meantime, feel free to browse through our collections!.</span></div>`;
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
        return; // Stop further processing
      }
      orderNumber = message;
      saveInquiry(userName, userEmail, `Order Number: ${orderNumber}`);
      chatBody.innerHTML += `<div class="chat-message bot"><span>Thank you for providing your email and order number. Our support team will reach out to you shortly to assist with your exchange or any other support you may need.</span></div>`;
    }
  }
}

// Save inquiry to backend
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

// Handle exchange option
function handleExchange(wantsExchange) {
  const chatBody = document.getElementById('chat-body');
  if (wantsExchange) {
    askForName(); // Fixed: Ask for name first, not order number
  } else {
    chatBody.innerHTML += `<div class="chat-message bot"><span>Okay, have a great day!</span></div>`;
  }
  enableInput(); // Re-enable input after Yes/No prompt
}

// Handle queue option
function handleQueue(wantsQueue) {
  const chatBody = document.getElementById('chat-body');
  if (wantsQueue) {
    askForName();
  } else {
    chatBody.innerHTML += `<div class="chat-message bot"><span>Okay, have a great day!</span></div>`;
  }
  enableInput(); // Re-enable input after Yes/No prompt


}