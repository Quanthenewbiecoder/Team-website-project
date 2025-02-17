let isProcessing = false; // Flag to prevent repeated submissions
let braceletNames = ["Pearl bracelet", "Crystal bracelet", "Leaf bracelet"];
let braceletPrice = ["£1,500","£1,100","£1,250"]
let productDescription = ["A finely crafted bracelet made with the finest pearls","A luxurious bracelet made with the finest quartz", "A metallic masterpiece made of stainless steel"]


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
    if (filters.Bracelets) {
        for (let i = 0; i < braceletNames.length; i++) {
            addProduct(braceletMock(i));
        }
    }
    if (filters.Earrings) addProduct(earringMock);
    if (filters.Rings) addProduct(ringMock);
    if (filters.Watches) addProduct(watchMock);
    if (filters.Necklaces) addProduct(necklaceMock);

    // Add further logic for other filters

    // Reset processing flag
    isProcessing = false;
});

// Mock product templates
function braceletMock(i){ 
    return `
    <div class="Product">
        <img src="${imagePaths.bracelet}" alt="Bracelet" onerror="this.src='${imagePaths.placeholder}'">
        <h1>, ${braceletNames[i]}</h1>
        <p class="price">,${braceletPrice[i]} </p>
        <p>, ${productDescription[i]}</p>
    </div>
    `;
}

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

function addProduct(productHTML) {
    var container = document.createElement("div");
    container.innerHTML += productHTML;  // Add new product HTML to the container
    const productDisplay = document.getElementById("product_display")
    productDisplay.appendChild(container)
    
}
