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
                    showFormError('Order not found. Please check your details.');
                }
            })
            .catch(error => console.error('ERROR: Fetch Failed', error));
    });
});

function displayOrderDetails(order) {
    console.log("DEBUG: Displaying Order Details", order);

    const orderDetailsSection = document.getElementById('order-details-section');
    const orderDetails = document.getElementById('order-details');

    if (!orderDetailsSection || !orderDetails) {
        console.error("ERROR: Order details elements not found!");
        return;
    }

    // Make sure the section is visible
    orderDetailsSection.style.display = 'block';

    // Ensure guest_order_id is used if _id is missing
    const trackingId = order.guest_order_id || order._id || "Unknown ID";

    // Convert MongoDB date format
    const createdAt = order.created_at ? new Date(order.created_at.$date).toLocaleString() : "N/A";

    orderDetails.innerHTML = `
        <h2>Order Details</h2>
        <p><strong>Order ID:</strong> ${trackingId}</p>
        <p><strong>Status:</strong> ${order.status}</p>
        <p><strong>Total Price:</strong> £${order.total_price.toFixed(2)}</p>
        <p><strong>Order Date:</strong> ${createdAt}</p>
        <h4>Items:</h4>
        <ul>
            ${order.items.length > 0 
                ? order.items.map(item => `
                    <li>${item.product_name} - £${item.price.toFixed(2)} x${item.quantity}</li>
                `).join('')
                : '<li>No items in this order.</li>'}
        </ul>
    `;

    console.log("DEBUG: Order details updated successfully.");
}

// Function to show error message
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
