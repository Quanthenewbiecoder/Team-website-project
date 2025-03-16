document.addEventListener("DOMContentLoaded", function () {
    console.log("Admin Products JS Loaded");

    document.getElementById("product-modal").style.display = "none"; // Ensure modal is hidden initially

    // Add Product Button Listener
    const addProductBtn = document.getElementById("add-product-btn");
    if (addProductBtn) {
        addProductBtn.addEventListener("click", showAddProductModal);
    }

    // Close Modal Button Listener
    const closeModalBtn = document.querySelector(".close-modal");
    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", closeProductModal);
    }

    // Handle Form Submission for Adding Product
    document.getElementById("product-form").addEventListener("submit", function (event) {
        event.preventDefault();
        saveProduct();
    });

    // Attach event listener to all delete buttons
    function attachDeleteEventListeners() {
        document.querySelectorAll(".btn-delete").forEach(button => {
            button.removeEventListener("click", deleteHandler); // Remove old listener first
            button.addEventListener("click", deleteHandler);
        });
    }
    
    function deleteHandler(event) {
        const productId = event.target.getAttribute("data-id");
        deleteProduct(productId);
    }
    
    // Call this function when the page loads and when products are updated
    document.addEventListener("DOMContentLoaded", attachDeleteEventListeners);
    

    // Attach event listener to all edit buttons
    document.querySelectorAll(".btn-edit").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.getAttribute("data-id");
            editProduct(productId);
        });
    });

    // Handle Image Upload Preview
    const fileInput = document.getElementById("product-image-file");
    const previewImage = document.getElementById("preview-image");

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = "block";
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

// Show Add Product Modal
function showAddProductModal() {
    console.log("Opening Add Product Modal");

    document.getElementById("product-modal-title").textContent = "Add Product";
    document.getElementById("product-id").value = "";
    document.getElementById("product-name").value = "";
    document.getElementById("product-price").value = "";
    document.getElementById("product-type").value = "";
    document.getElementById("product-collection").value = "";
    document.getElementById("product-instock").checked = true;
    document.getElementById("product-modal").style.display = "flex";

    // Reset file input and preview
    document.getElementById("product-image-file").value = "";
    document.getElementById("preview-image").style.display = "none";
}

// Show Edit Product Modal
function editProduct(productId) {
    console.log("Editing Product ID:", productId);

    fetch(`/api/products/${productId}`)
    .then(response => response.json())
    .then(product => {
        document.getElementById("product-modal-title").textContent = "Edit Product";
        document.getElementById("product-id").value = productId;
        document.getElementById("product-name").value = product.name;
        document.getElementById("product-price").value = product.price;
        document.getElementById("product-type").value = product.type;
        document.getElementById("product-collection").value = product.collection || "";
        document.getElementById("product-instock").checked = product.in_stock;

        // Display existing image if available
        const previewImage = document.getElementById("preview-image");
        if (product.image_url) {
            previewImage.src = product.image_url;
            previewImage.style.display = "block";
        } else {
            previewImage.style.display = "none";
        }

        document.getElementById("product-modal").style.display = "flex";
    })
    .catch(error => {
        console.error("Error fetching product details:", error);
    });
}

// Close Modal
function closeProductModal() {
    console.log("Closing Product Modal");
    document.getElementById("product-modal").style.display = "none";
}

// Save Product Function (With Image Upload)
function saveProduct() {
    const formData = new FormData();
    const fileInput = document.getElementById("product-image-file").files[0];

    formData.append("name", document.getElementById("product-name").value.trim());
    formData.append("price", parseFloat(document.getElementById("product-price").value.trim()));
    formData.append("type", document.getElementById("product-type").value.trim());
    formData.append("collection", document.getElementById("product-collection").value.trim());
    formData.append("in_stock", document.getElementById("product-instock").checked);

    if (fileInput) {
        formData.append("image", fileInput);
    }

    fetch("/api/products", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Product saved successfully!");
            closeProductModal();
            location.reload();
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error saving product:", error);
    });
}

// Function to delete a product
function deleteProduct(productId) {
    if (!confirm("Are you sure you want to delete this product?")) {
        return;
    }

    // Ask if the user wants to delete the image as well
    const deleteImage = confirm("Would you like to delete the image as well?");

    fetch(`/api/products/${productId}?delete_image=${deleteImage}`, {
        method: "DELETE",
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let message = "Product deleted successfully!";
            if (data.image_deleted) {
                message += " Image was also deleted.";
            } else {
                message += " Image was kept.";
            }
            alert(message);
            location.reload(); // Refresh the page to update product list
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error deleting product:", error);
    });
}
