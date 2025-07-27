// Admin Mobile Hamburger Menu (jak na głównej stronie)
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
        // Usuń stare elementy jeśli istnieją
        const oldToggle = document.getElementById('adminMobileToggle');
        const oldMenu = document.getElementById('adminMobileMenu');
        if (oldToggle) oldToggle.remove();
        if (oldMenu) oldMenu.remove();
        
        // Dodaj przycisk hamburgera
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'adminMobileToggle';
        toggleBtn.className = 'admin-mobile-toggle';
        toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
        document.body.appendChild(toggleBtn);
        
        // Stwórz pełnoekranowe menu
        const mobileMenu = createMobileMenu();
        document.body.appendChild(mobileMenu);
        
        // Event listeners
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            mobileMenu.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        
        // Zamknij przycisk
        const closeBtn = mobileMenu.querySelector('.admin-mobile-close');
        closeBtn.addEventListener('click', function() {
            closeMobileMenu();
        });
        
        // Zamknij po kliknięciu w link
        const navLinks = mobileMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Nie zamykaj od razu - pozwól na nawigację
                setTimeout(() => {
                    closeMobileMenu();
                }, 100);
            });
        });
        
        // Zamknij na ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
                closeMobileMenu();
            }
        });
        
        function closeMobileMenu() {
            mobileMenu.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }
    
    function createMobileMenu() {
        const menu = document.createElement('div');
        menu.id = 'adminMobileMenu';
        menu.className = 'admin-mobile-menu';
        
        menu.innerHTML = `
            <button class="admin-mobile-close">
                <i class="fas fa-times"></i>
            </button>
            
            <div class="admin-mobile-brand">
                <img src="/static/logo/dog-logo.png" alt="Logo">
                <span>Admin Panel</span>
            </div>
            
            <div class="admin-mobile-nav-items">
                <div class="admin-mobile-nav-group">
                    <div class="admin-mobile-nav-title">
                        ⚙️ Panel Główny
                    </div>
                    ${createNavLinks()}
                </div>
                
                <div class="admin-mobile-nav-group">
                    <div class="admin-mobile-nav-title">
                        👤 Użytkownik
                    </div>
                    <a href="/admin/password_change/" class="admin-mobile-nav-link">
                        🔒 Zmień hasło
                    </a>
                    <a href="/admin/logout/" class="admin-mobile-nav-link">
                        🚪 Wyloguj
                    </a>
                </div>
            </div>
        `;
        
        return menu;
    }
    
    function createNavLinks() {
        // Znajdź istniejące linki z oryginalnego navbar
        const originalNavbar = document.querySelector('.admin-modern-navbar');
        if (!originalNavbar) return '';
        
        let linksHTML = '';
        const dropdownLinks = originalNavbar.querySelectorAll('.admin-dropdown-link');
        
        dropdownLinks.forEach(link => {
            const href = link.getAttribute('href');
            const text = link.textContent.trim();
            const addBtn = link.parentNode.querySelector('.admin-dropdown-add-btn');
            
            if (href && text) {
                linksHTML += `
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <a href="${href}" class="admin-mobile-nav-link" style="flex: 1; margin-bottom: 0;">
                            ${text}
                        </a>
                        ${addBtn ? `<a href="${addBtn.getAttribute('href')}" class="admin-mobile-add-btn">+</a>` : ''}
                    </div>
                `;
            }
        });
        
        return linksHTML;
    }
    
    function removeMobileMenu() {
        const toggleBtn = document.getElementById('adminMobileToggle');
        const mobileMenu = document.getElementById('adminMobileMenu');
        
        if (toggleBtn) toggleBtn.remove();
        if (mobileMenu) mobileMenu.remove();
        
        document.body.style.overflow = 'auto';
    }
});