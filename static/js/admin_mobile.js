// Admin Mobile Hamburger Menu
document.addEventListener('DOMContentLoaded', function() {
    // Sprawdź czy jesteśmy na mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // Initialize mobile menu tylko na mobile
    if (isMobile()) {
        initMobileMenu();
    }
    
    // Reinitialize po zmianie rozmiaru okna
    window.addEventListener('resize', function() {
        if (isMobile() && !document.getElementById('adminMobileToggle')) {
            initMobileMenu();
        } else if (!isMobile()) {
            removeMobileMenu();
        }
    });
    
    function initMobileMenu() {
        // Dodaj przycisk hamburgera jeśli nie istnieje
        if (!document.getElementById('adminMobileToggle')) {
            const toggleBtn = document.createElement('button');
            toggleBtn.id = 'adminMobileToggle';
            toggleBtn.className = 'admin-mobile-toggle';
            toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
            document.body.appendChild(toggleBtn);
        }
        
        // Dodaj overlay jeśli nie istnieje
        if (!document.getElementById('adminMobileOverlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'adminMobileOverlay';
            overlay.className = 'admin-mobile-overlay';
            document.body.appendChild(overlay);
        }
        
        const navbar = document.querySelector('.admin-modern-navbar');
        const toggleBtn = document.getElementById('adminMobileToggle');
        const overlay = document.getElementById('adminMobileOverlay');
        
        if (!navbar || !toggleBtn || !overlay) return;
        
        // Event listeners
        toggleBtn.addEventListener('click', function() {
            navbar.classList.add('mobile-active');
            overlay.classList.add('active');
            overlay.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
        
        // Zamknij po kliknięciu w overlay
        overlay.addEventListener('click', function() {
            closeMobileMenu();
        });
        
        // Zamknij po kliknięciu w link
        const navLinks = navbar.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                closeMobileMenu();
            });
        });
        
        // Zamknij na ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navbar.classList.contains('mobile-active')) {
                closeMobileMenu();
            }
        });
        
        function closeMobileMenu() {
            navbar.classList.remove('mobile-active');
            overlay.classList.remove('active');
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
            document.body.style.overflow = 'auto';
        }
    }
    
    function removeMobileMenu() {
        const toggleBtn = document.getElementById('adminMobileToggle');
        const overlay = document.getElementById('adminMobileOverlay');
        
        if (toggleBtn) toggleBtn.remove();
        if (overlay) overlay.remove();
        
        const navbar = document.querySelector('.admin-modern-navbar');
        if (navbar) {
            navbar.classList.remove('mobile-active');
            navbar.style.transform = ''; // Reset transform
        }
        
        document.body.style.overflow = 'auto';
    }
});