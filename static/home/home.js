// Effetto scroll header
window.addEventListener('scroll', function() {
    const header = document.getElementById('main-header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});


function scrollRow(button, amount) {
    const container = button.parentElement;
    const row = container.querySelector('.movie-row');
    row.scrollBy({
        left: amount,
        behavior: 'smooth'
    });
}

// Nascondi le frecce quando non c'è più contenuto da scrollare
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.movie-row');
    const containers = document.querySelectorAll('.movie-row-container');

    function checkScroll() {
        containers.forEach(container => {
            const row = container.querySelector('.movie-row');
            const leftBtn = container.querySelector('.scroll-btn.left');
            const rightBtn = container.querySelector('.scroll-btn.right');

            // Controllo per il pulsante sinistro
            if (row.scrollLeft <= 10) {
                leftBtn.style.display = 'none';
            } else {
                leftBtn.style.display = 'flex';
            }

            // Controllo per il pulsante destro
            if (row.scrollLeft >= row.scrollWidth - row.clientWidth - 10) {
                rightBtn.style.display = 'none';
            } else {
                rightBtn.style.display = 'flex';
            }
        });
    }

    // Controlla lo stato iniziale
    checkScroll();

    // Aggiungi listener per lo scroll
    rows.forEach(row => {
        row.addEventListener('scroll', checkScroll);
    });
});


