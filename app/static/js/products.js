let isProcessing = false; // Flag to prevent repeated submissions

document.getElementById("Form").addEventListener("submit", function (e) {
    e.preventDefault();

    if (isProcessing) return; // Prevent multiple submissions

    isProcessing = true; // Set processing flag

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
    if (filters.Watches) addProduct("Container_Watches", watchMock);
    if (filters.Necklaces) addProduct("Container_Necklaces", necklaceMock);

    // Add further logic for other filters

    // Reset processing flag
    isProcessing = false;
});

// Mock product templates
const braceletMock = `
    <div class="Product">
        <img src="${imagePaths.bracelet}" alt="Bracelet" onerror="this.src='${imagePaths.placeholder}'">
        <h1>Crystal Bracelet</h1>
        <p class="price">£1,500</p>
    </div>
`;

const earringMock = `
    <div class="Product">
        <img src="${imagePaths.earring}" alt="Earring" onerror="this.src='${imagePaths.placeholder}'">
        <h1>Pearl Earring</h1>
        <p class="price">£799</p>
    </div>
`;

const ringMock = `
    <div class="Product">
        <img src="${imagePaths.ring}" alt="Ring" onerror="this.src='${imagePaths.placeholder}'">
        <h1>Leaf Ring</h1>
        <p class="price">£999</p>
    </div>
`;

const watchMock = `
    <div class="Product">
        <img src="${imagePaths.watch}" alt="Watch" onerror="this.src='${imagePaths.placeholder}'">
        <h1>Luxury Watch</h1>
        <p class="price">£2,500</p>
    </div>
`;

const necklaceMock = `
    <div class="Product">
        <img src="${imagePaths.necklace}" alt="Necklace" onerror="this.src='${imagePaths.placeholder}'">
        <h1>Diamond Necklace</h1>
        <p class="price">£3,000</p>
    </div>
`;


// Helper Functions
function clearContainers() {
    document.querySelectorAll("[id^='Container_']").forEach(container => {
        container.innerHTML = ""; // Clear the contents of the containers
    });
}

function addProduct(containerId, productHTML) {
    const container = document.getElementById(containerId);
    if (container) container.innerHTML += productHTML; // Add new product HTML to the container
}
