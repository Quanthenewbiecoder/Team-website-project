document.addEventListener('DOMContentLoaded', function () {
    console.log("Admin Products JS Loaded");

    // Ensure modal is hidden initially
    document.getElementById("product-modal").style.display = "none";

    // Add event listener for Add Product button
    const addProductBtn = document.getElementById("add-product-btn");
    if (addProductBtn) {
        addProductBtn.addEventListener("click", function () {
            showAddProductModal();
        });
    }

    // Add event listener for close button
    const closeModalBtn = document.querySelector(".close-modal");
    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", function () {
            closeProductModal();
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
    document.getElementById("product-image").value = "";
    document.getElementById("product-modal").style.display = "flex";  // Use 'flex' to center it
}

// Close Modal
function closeProductModal() {
    console.log("Closing Product Modal");
    document.getElementById("product-modal").style.display = "none";
}
