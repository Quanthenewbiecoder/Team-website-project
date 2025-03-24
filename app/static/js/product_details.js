document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-edit-btn");
    const editFormContainer = document.getElementById("edit-form-container");
    const viewDiv = document.getElementById("view-product-info");
    const basketBtn = document.getElementById("add-to-basket");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            const isVisible = editFormContainer.style.display === "block";
            editFormContainer.style.display = isVisible ? "none" : "block";
            viewDiv.style.display = isVisible ? "block" : "none";
            toggleBtn.textContent = isVisible ? "Edit Product" : "Cancel Edit";
        });
    }

    const editForm = document.getElementById("edit-product-form");
    if (editForm) {
        editForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const formData = new FormData(editForm);
            const productId = formData.get("id");

            try {
                const response = await fetch(`/api/products/${productId}`, {
                    method: "PUT",
                    credentials: "include",
                    body: formData
                });

                const data = await response.json();
                if (data.success) {
                    alert("Product updated successfully!");
                    location.reload();
                } else {
                    alert("Update failed: " + data.error);
                }
            } catch (error) {
                console.error("Error updating product:", error);
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
