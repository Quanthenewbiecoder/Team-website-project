document.addEventListener("DOMContentLoaded", function () {
    console.log("Admin Products JS Loaded");

    document.getElementById("product-modal").style.display = "none";

    const addProductBtn = document.getElementById("add-product-btn");
    if (addProductBtn) {
        addProductBtn.addEventListener("click", showAddProductModal);
    }

    const closeModalBtn = document.querySelector(".close-modal");
    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", closeProductModal);
    }

    document.getElementById("product-form").addEventListener("submit", function (event) {
        event.preventDefault();
        saveProduct();
    });

    // Handle Image Upload Preview
    const fileInput = document.getElementById("product-image-file");
    const previewImage = document.getElementById("preview-image");

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
            alert("Product added successfully!");
            closeProductModal();
            location.reload();
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error adding product:", error);
    });
}
