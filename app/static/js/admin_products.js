document.addEventListener('DOMContentLoaded', function () {
    console.log("Admin Products JS Loaded");
});

// Show Add Product Modal
function showAddProductModal() {
    document.getElementById("product-modal-title").textContent = "Add Product";
    document.getElementById("product-id").value = "";
    document.getElementById("product-name").value = "";
    document.getElementById("product-price").value = "";
    document.getElementById("product-type").value = "";
    document.getElementById("product-collection").value = "";
    document.getElementById("product-image").value = "";
    document.getElementById("product-modal").style.display = "block";
}

// Show Edit Product Modal
function editProduct(productId) {
    fetch(`/api/products/${productId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("product-modal-title").textContent = "Edit Product";
                document.getElementById("product-id").value = data.product.id;
                document.getElementById("product-name").value = data.product.name;
                document.getElementById("product-price").value = data.product.price;
                document.getElementById("product-type").value = data.product.product_type;
                document.getElementById("product-collection").value = data.product.collection;
                document.getElementById("product-image").value = data.product.image_url;
                document.getElementById("product-modal").style.display = "block";
            }
        });
}

// Delete Product
function deleteProduct(productId) {
    if (confirm("Are you sure you want to delete this product?")) {
        fetch(`/api/products/${productId}`, { method: "DELETE" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Product deleted successfully!");
                    location.reload();
                } else {
                    alert("Failed to delete product.");
                }
            });
    }
}

// Handle Form Submission
document.getElementById("product-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const productId = document.getElementById("product-id").value;
    const productData = {
        name: document.getElementById("product-name").value,
        price: document.getElementById("product-price").value,
        product_type: document.getElementById("product-type").value,
        collection: document.getElementById("product-collection").value,
        image_url: document.getElementById("product-image").value
    };

    const method = productId ? "PUT" : "POST";
    const url = productId ? `/api/products/${productId}` : "/api/products";

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(productData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Product saved successfully!");
            location.reload();
        } else {
            alert("Failed to save product.");
        }
    });
});

// Close Modal
function closeProductModal() {
    document.getElementById("product-modal").style.display = "none";
}
