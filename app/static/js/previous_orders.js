document.addEventListener('DOMContentLoaded', function () {
    console.log("DEBUG: JavaScript Loaded");

    const trackingForm = document.getElementById('tracking-form');

    if (!trackingForm) {
        console.error("ERROR: Tracking form not found!");
        return;
    }

    trackingForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const trackingNumber = document.getElementById('tracking-number').value.trim();
        const guestEmail = document.getElementById('guest-email').value.trim();

        console.log("DEBUG: Tracking Number:", trackingNumber);
        console.log("DEBUG: Guest Email:", guestEmail);

        if (!trackingNumber && !guestEmail) {
            showFormError('Please enter a tracking number or email.');
            return;
        }

        let url = `/api/orders/track?tracking=${trackingNumber}`;
        if (guestEmail) {
            url += `&guest_email=${guestEmail}`;
        }

        console.log("DEBUG: Fetching from URL:", url);

        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log("DEBUG: API Response", data);

                if (data.success && data.order) {
                    displayOrderDetails(data.order);
                } else {
                    showFormError(data.error || 'Order not found. Please check your details.');
                }
            })
            .catch(error => console.error('ERROR: Fetch Failed', error));
    });
});

// Function to parse MongoDB date format
function parseMongoDate(dateObj) {
    if (!dateObj) return "N/A";

    // Handle MongoDB's extended JSON format
    let dateStr = dateObj.$date || dateObj;

    let parsedDate = new Date(dateStr);
    return isNaN(parsedDate.getTime()) ? "N/A" : parsedDate.toLocaleString();
}

// Function to display order details
function displayOrderDetails(order) {
    console.log("DEBUG: Displaying Order Details", order);

    const orderDetailsSection = document.getElementById('order-details-section');
    const orderDetails = document.getElementById('order-details');

    if (!orderDetailsSection || !orderDetails) {
        console.error("ERROR: Order details elements not found!");
        return;
    }

    orderDetailsSection.style.display = 'block';

    const createdAt = parseMongoDate(order.created_at);
    const trackingId = order.user_order_id || order.guest_order_id || order._id || "Unknown ID"; // Supports both user & guest orders
    const totalPrice = order.total_price ? order.total_price.toFixed(2) : "0.00";

    console.log("DEBUG: Order Items:", order.items);

    let itemsHTML = "";
    if (Array.isArray(order.items) && order.items.length > 0) {
        itemsHTML = order.items.map(item => `
            <li>
                <strong>${item.product_name}</strong> - 
                £${item.price.toFixed(2)} x${item.quantity}
            </li>
        `).join('');
    } else {
        itemsHTML = "<li>No items found.</li>";
    }

    // Added Order Type (Guest or Registered User)
    const orderType = order.user_order_id ? "Registered User" : "Guest Order";

    orderDetails.innerHTML = `
        <h2>Order Details</h2>
        <p><strong>Tracking Number:</strong> ${trackingId}</p>
        <p><strong>Order Type:</strong> ${orderType}</p> 
        <p><strong>Status:</strong> ${order.status}</p>
        <p><strong>Total Price:</strong> £${totalPrice}</p>
        <p><strong>Order Date:</strong> ${createdAt}</p>
        <h4>Items:</h4>
        <ul id="order-items-list">${itemsHTML}</ul>
    `;

    console.log("DEBUG: Order details updated successfully.");
}

// Function to show form errors
function showFormError(message) {
    const errorElement = document.getElementById('form-error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';

        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 3000);
    }
}

// Function to copy tracking number to clipboard
document.addEventListener('click', function (event) {
    if (event.target.id === "copy-tracking" || event.target.closest("#copy-tracking")) {
        const trackingNumber = event.target.dataset.tracking || event.target.closest("#copy-tracking").dataset.tracking;

        if (!trackingNumber) {
            console.error("ERROR: No tracking number found to copy.");
            return;
        }

        navigator.clipboard.writeText(trackingNumber).then(() => {
            showNotification("Tracking number copied!", "success");
        }).catch(err => {
            console.error("ERROR: Failed to copy tracking number", err);
        });
    }
});

// Function to show notifications
function showNotification(message, type = "success") {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);
    setTimeout(() => {
        notification.classList.add("show");
    }, 100);

    setTimeout(() => {
        notification.classList.remove("show");
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 2500);
}
