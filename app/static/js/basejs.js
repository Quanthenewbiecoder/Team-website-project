window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 80) {
    navbar.classList.add('sticky');
  } else {
    navbar.classList.remove('sticky');
  }
});

window.addEventListener('resize', () => {
  const menu = document.querySelector('.menu');
  if (window.innerWidth > 900 && menu.classList.contains('show')) {
    menu.classList.remove('show');
    document.removeEventListener('click', closeMenuOutside);
  }
});