document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("toggle-edit-btn");
    const editForm = document.getElementById("edit-form-container");
    const viewDiv = document.getElementById("view-product-info");

    if (editBtn) {
        editBtn.addEventListener("click", function () {
            const isVisible = editForm.style.display === "block";
            editForm.style.display = isVisible ? "none" : "block";
            viewDiv.style.display = isVisible ? "block" : "none";
            editBtn.textContent = isVisible ? "Edit Product" : "Cancel Edit";
        });
    }

    const editFormElem = document.getElementById("edit-product-form");
    if (editFormElem) {
        editFormElem.addEventListener("submit", async function (e) {
            e.preventDefault();

            const productId = document.getElementById("product-id").value;

            const updatedData = {
                name: document.getElementById("product-name").value,
                type: document.getElementById("product-type").value,
                price: parseFloat(document.getElementById("product-price").value),
                collection: document.getElementById("product-collection").value,
                description: document.getElementById("product-description").value,
                in_stock: document.getElementById("product-stock").checked,
            };

            try {
                const response = await fetch(`/api/products/${productId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                    body: JSON.stringify(updatedData),
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    alert("Product updated successfully!");
                    location.reload();
                } else {
                    alert("Update failed: " + data.error);
                }
            } catch (err) {
                console.error("Error updating product:", err);
                alert("An error occurred while updating the product.");
            }
        });
    }

    if (basketBtn) {
        basketBtn.addEventListener("click", function () {
            const id = this.dataset.id;
            const name = this.dataset.name;
            const price = parseFloat(this.dataset.price);
            const image = this.dataset.image;

            addToCart(id, name, price, image);
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
});
