// Navbar functionality
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const header = document.getElementById('main-header');

hamburger.addEventListener('click', function() {
    header.classList.toggle('menu-open');
    navMenu.classList.toggle('active');

    // Cambia icona
    const icon = hamburger.querySelector('i');
    icon.classList.toggle('fa-bars');
    icon.classList.toggle('fa-times');
});

// Chiudi il menu quando si clicca su un link
const navLinks = document.querySelectorAll('#nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', function() {
        header.classList.remove('menu-open');
        navMenu.classList.remove('active');
        hamburger.querySelector('i').classList.remove('fa-times');
        hamburger.querySelector('i').classList.add('fa-bars');
    });
});

// Effetto scroll header
window.addEventListener('scroll', function() {
    if (window.scrollY > 10) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});