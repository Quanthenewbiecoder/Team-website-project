document.addEventListener('DOMContentLoaded', function() {
    const sliderImages = document.querySelector('.slider-images');
    const images = sliderImages.querySelectorAll('img');
    const totalImages = images.length;
    let currentIndex = 0;

    for (let i = 1; i < totalImages; i++) {
        images[i].style.display = 'none';
    }

    function nextSlide() {
        images[currentIndex].style.display = 'none';
        currentIndex = (currentIndex + 1) % totalImages;
        images[currentIndex].style.display = 'block';
    }

    const slideInterval = setInterval(nextSlide, 4000);

    const popup = document.getElementById('newsletter-popup');
    const closeButton = document.getElementById('close-popup');
    
    setTimeout(() => {
        if (popup) {
            popup.style.display = 'block';
        }
    }, 3000);

    if (closeButton) {
        closeButton.addEventListener('click', function() {
            popup.style.display = 'none';
        });
    }

    const form = document.getElementById('newsletter-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('email').value;

            fetch('/subscriptions/add', {
                method: 'POST',
                body: JSON.stringify({ email: email }),
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (response.ok) {
                    alert('Thank you for subscribing to our newsletter!');
                    popup.style.display = 'none';
                } else {
                    alert('There was an error with your subscription. Please try again.');
                }
            }).catch(error => {
                alert('Error: ' + error);
            });
        });
    }

    const collectionItems = document.querySelectorAll('.collection-item');
    collectionItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (e.target.tagName.toLowerCase() === 'a') {
                return;
            }
            
            const link = this.querySelector('a');
            if (link) {
                window.location.href = link.href;
            }
        });
    });

    window.onclick = function(event) {
        if (event.target === popup) {
            popup.style.display = 'none';
        }
    };
});