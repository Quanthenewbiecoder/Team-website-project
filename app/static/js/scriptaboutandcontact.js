function toggleMenu(event) {
  const navbarLinks = document.querySelector('.navbar ul');
  const searchBar = document.querySelector('.search-bar');
  navbarLinks.classList.toggle('show');
  searchBar.classList.toggle('show'); 


  if (navbarLinks.classList.contains('show') || searchBar.classList.contains('show')) {
    document.addEventListener('click', closeMenuOnClickOutside);
  } else {
    document.removeEventListener('click', closeMenuOnClickOutside);
  }

  event.stopPropagation(); 
}

function closeMenuOnClickOutside(event) {
  const navbarLinks = document.querySelector('.navbar ul');
  const searchBar = document.querySelector('.search-bar');
  const hamburger = document.querySelector('.hamburger');

  if (!navbarLinks.contains(event.target) && !hamburger.contains(event.target) && !searchBar.contains(event.target)) {
    navbarLinks.classList.remove('show');
    searchBar.classList.remove('show');
    document.removeEventListener('click', closeMenuOnClickOutside);
  }
}

function openPopup(img) {
const popupOverlay = document.querySelector('.popup-overlay');
const popupImage = document.getElementById('popup-image');
popupImage.src = img.src;
popupOverlay.style.display = 'flex';
}

function closePopup() {
const popupOverlay = document.querySelector('.popup-overlay');
popupOverlay.style.display = 'none';
}

window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 500) {
    navbar.classList.add('sticky');
  } else {
    navbar.classList.remove('sticky');
  }
});


var	testim = document.getElementById("testim"),
		testimDots = Array.prototype.slice.call(document.getElementById("testim-dots").children),
    testimContent = Array.prototype.slice.call(document.getElementById("testim-content").children),
    testimLeftArrow = document.getElementById("left-arrow"),
    testimRightArrow = document.getElementById("right-arrow"),
    testimSpeed = 4500,
    currentSlide = 0,
    currentActive = 0,
    testimTimer,
		touchStartPos,
		touchEndPos,
		touchPosDiff,
		ignoreTouch = 30;
;

window.onload = function() {


    function playSlide(slide) {
        for (var k = 0; k < testimDots.length; k++) {
            testimContent[k].classList.remove("active");
            testimContent[k].classList.remove("inactive");
            testimDots[k].classList.remove("active");
        }

        if (slide < 0) {
            slide = currentSlide = testimContent.length-1;
        }

        if (slide > testimContent.length - 1) {
            slide = currentSlide = 0;
        }

        if (currentActive != currentSlide) {
            testimContent[currentActive].classList.add("inactive");            
        }
        testimContent[slide].classList.add("active");
        testimDots[slide].classList.add("active");

        currentActive = currentSlide;
    
        clearTimeout(testimTimer);
        testimTimer = setTimeout(function() {
            playSlide(currentSlide += 1);
        }, testimSpeed)
    }

    testimLeftArrow.addEventListener("click", function() {
        playSlide(currentSlide -= 1);
    })

    testimRightArrow.addEventListener("click", function() {
        playSlide(currentSlide += 1);
    })    

    for (var l = 0; l < testimDots.length; l++) {
        testimDots[l].addEventListener("click", function() {
            playSlide(currentSlide = testimDots.indexOf(this));
        })
    }

    playSlide(currentSlide);

    
    document.addEventListener("keyup", function(e) {
        switch (e.keyCode) {
            case 37:
                testimLeftArrow.click();
                break;
                
            case 39:
                testimRightArrow.click();
                break;

            case 39:
                testimRightArrow.click();
                break;

            default:
                break;
        }
    })
		
		testim.addEventListener("touchstart", function(e) {
				touchStartPos = e.changedTouches[0].clientX;
		})
	
		testim.addEventListener("touchend", function(e) {
				touchEndPos = e.changedTouches[0].clientX;
			
				touchPosDiff = touchStartPos - touchEndPos;
			
				console.log(touchPosDiff);
				console.log(touchStartPos);	
				console.log(touchEndPos);	

			
				if (touchPosDiff > 0 + ignoreTouch) {
						testimLeftArrow.click();
				} else if (touchPosDiff < 0 - ignoreTouch) {
						testimRightArrow.click();
				} else {
					return;
				}
			
		})
}

function openPopup(img) {
  const popupOverlay = document.getElementById('popup-overlay');
  const popupImage = document.getElementById('popup-image');
  
  if (popupOverlay && popupImage) {
      popupImage.src = img.src;
      popupOverlay.style.display = 'flex';
      
      document.body.style.overflow = 'hidden';
  }
}

function closePopup() {
  const popupOverlay = document.getElementById('popup-overlay');
  
  if (popupOverlay) {
      popupOverlay.style.display = 'none';
      
      document.body.style.overflow = 'auto';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const popupOverlay = document.getElementById('popup-overlay');
  
  if (popupOverlay) {
      popupOverlay.addEventListener('click', function(event) {
          if (event.target === popupOverlay) {
              closePopup();
          }
      });
  }
  
  const cardImages = document.querySelectorAll('.card img');
  cardImages.forEach(img => {
      img.addEventListener('click', function() {
          openPopup(this);
      });
  });
});