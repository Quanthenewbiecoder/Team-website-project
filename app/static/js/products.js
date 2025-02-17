document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("Search");
    const form = document.getElementById("Form");
    const productContainers = {
        Bracelets: document.getElementById("Container_Bracelet"),
        Earrings: document.getElementById("Container_Earrings"),
        Rings: document.getElementById("Container_Rings"),
        Watches: document.getElementById("Container_Watches"),
        Necklaces: document.getElementById("Container_Necklaces"),
    };

    const products = [
        { name: "Ethereal Harmony", type: "Bracelets", price: 200, img: imagePaths.bracelet, collection: "Crystal", description: "A captivating blend of elegance and serenity."},
        { name: "Nature's Grace", type: "Earrings", price: 150, img: imagePaths.earring, collection: "Leaf", description: "Masterfully crafted to embody the delicate beauty of nature, featuring intricately detailed leaf designs that capture the essence of a serene forest." },
        { name: "Luminous Pearl", type: "Rings", price: 250, img: imagePaths.ring, collection: "Pearl", description: "This ring, with its natural iridescence, catches the light beautifully, creating a mesmerizing glow that draws the eye."},
        { name: "Midnight Elegance", type: "Watches", price: 1500, img: imagePaths.watch, collection: "None", description: "This striking timepiece seamlessly blends modern sophistication with timeless charm, creating a versatile accessory that's perfect for any occasion."},
        { name: "Forest Whisper", type: "Necklaces", price: 300, img: imagePaths.necklace, collection: "Leaf", description: "Meticulously crafted to showcase it's fine details, from the veins to the subtle textures, creating a lifelike representation of nature's artistry."},
    ];

    var collectionFilter = ""
    function collectionType(){
        var collections = document.getElementsByName("collections")
        for (i = 0; i < collections.length; i++){
            if(collections[i].checked){
                collectionFilter = collections[i].value
            }
        }
    }

    function displayProducts(filteredProducts) {
        Object.values(productContainers).forEach(container => container.innerHTML = "");
        filteredProducts.forEach(product => {
            const container = productContainers[product.type];
            collectionType();

            if (document.getElementById(product.type).checked && collectionFilter === "None") {
                const productElement = document.createElement("div");
                productElement.classList.add("Product");
                productElement.innerHTML = `
                    <img src="${product.img}" alt="${product.name}">
                    <h1>${product.name}</h1>
                    <p class="price">£ ${product.price}</p>
                    <p>${product.description}</p>
                `;
                container.appendChild(productElement);
            }
            else if (document.getElementById(product.type).checked && collectionFilter === product.collection){
                const productElement = document.createElement("div");
                productElement.classList.add("Product");
                productElement.innerHTML = `
                    <img src="${product.img}" alt="${product.name}">
                    <h1>${product.name}</h1>
                    <p class="price">£ ${product.price}</p>
                    <p>${product.description}</p>
                `;
                container.appendChild(productElement); 
            }
            else if (document.getElementById(product.type).checked && collectionFilter === product.collection){
                const productElement = document.createElement("div");
                productElement.classList.add("Product");
                productElement.innerHTML = `
                    <img src="${product.img}" alt="${product.name}">
                    <h1>${product.name}</h1>
                    <p class="price">£ ${product.price}</p>
                    <p>${product.description}</p>
                `;
                container.appendChild(productElement);
            }
            else if (document.getElementById(product.type).checked && collectionFilter === product.collection){ 
                const productElement = document.createElement("div");
                productElement.classList.add("Product");
                productElement.innerHTML = `
                    <img src="${product.img}" alt="${product.name}">
                    <h1>${product.name}</h1>
                    <p class="price">£ ${product.price}</p>
                    <p>${product.description}</p>
                `;
                container.appendChild(productElement);
            }
            console.log(product.type)
            console.log(product.collection)
        });
    }

    function emptyContainers() {
        //remove the products as they dont get removed automatically when filtered due to how this code is setup
        document.getElementById("Container_Bracelet").innerHTML = ""
        document.getElementById("Container_Earrings").innerHTML = ""
        document.getElementById("Container_Rings").innerHTML = ""
        document.getElementById("Container_Watches").innerHTML = ""
        document.getElementById("Container_Necklaces").innerHTML = ""

    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const query = searchInput.value.toLowerCase();
        const filteredProducts = products.filter(product => product.name.toLowerCase().includes(query));
        emptyContainers() 
        displayProducts(filteredProducts);
    });
});
