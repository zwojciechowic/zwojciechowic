// Uproszczony Admin Mobile Menu
document.addEventListener('DOMContentLoaded', function() {
    // Elementy menu
    const mobileMenuToggle = document.getElementById('adminMobileToggle');
    const mobileMenu = document.getElementById('adminMobileMenu');
    const mobileClose = document.getElementById('adminMobileClose');
    const mobileNavLinks = document.querySelectorAll('.admin-mobile-nav-link');

    // Sprawdź czy elementy istnieją
    if (!mobileMenuToggle || !mobileMenu) {
        console.log('Admin mobile menu elements not found');
        return;
    }

    // Otwórz menu mobilne
    mobileMenuToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        mobileMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    // Zamknij menu mobilne
    if (mobileClose) {
        mobileClose.addEventListener('click', function() {
            closeMobileMenu();
        });
    }

    // Zamknij menu po kliknięciu w link
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            setTimeout(() => {
                closeMobileMenu();
            }, 100);
        });
    });

    // Zamknij menu po kliknięciu na tło
    mobileMenu.addEventListener('click', function(e) {
        if (e.target === mobileMenu) {
            closeMobileMenu();
        }
    });

    // Zamknij menu na ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    // Funkcja zamykania menu
    function closeMobileMenu() {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    // Zamknij menu przy zmianie orientacji
    window.addEventListener('orientationchange', function() {
        if (mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });
});