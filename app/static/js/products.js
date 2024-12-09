document.getElementById("Form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Extract form data
    const formData = new FormData(e.target);
    const filters = Object.fromEntries(formData.entries());

    console.log("Filters Applied:", filters);

    // Clear previous results
    clearContainers();

    // Apply filters and display products (mock implementation here)
    if (filters.Bracelets) addProduct("Container_Bracelet", braceletMock);
    if (filters.Earrings) addProduct("Container_Earrings", earringMock);
    if (filters.Rings) addProduct("Container_Rings", ringMock);
    // Add further logic for other filters
});

// Mock product templates
const braceletMock = `
    <div class="Product">
        <img src="static/images/bracelet.jpg" alt="Bracelet">
        <h1>Crystal Bracelet</h1>
        <p class="price">£1,500</p>
    </div>
`;

const earringMock = `
    <div class="Product">
        <img src="static/images/earring.jpg" alt="Earring">
        <h1>Pearl Earring</h1>
        <p class="price">£799</p>
    </div>
`;

const ringMock = `
    <div class="Product">
        <img src="static/images/ring.jpg" alt="Ring">
        <h1>Leaf Ring</h1>
        <p class="price">£999</p>
    </div>
`;

// Helper Functions
function clearContainers() {
    document.querySelectorAll("[id^='Container_']").forEach(container => {
        container.innerHTML = "";
    });
}

function addProduct(containerId, productHTML) {
    const container = document.getElementById(containerId);
    if (container) container.innerHTML += productHTML;
}
