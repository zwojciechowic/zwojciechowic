// Gallery Widget JavaScript - Fixed
document.addEventListener('DOMContentLoaded', function() {
    // Inicjalizuj wszystkie galerie na stronie
    const galleries = document.querySelectorAll('.gallery-widget');
    
    galleries.forEach(gallery => {
        initGallery(gallery);
    });
});

function initGallery(galleryElement) {
    const slides = galleryElement.querySelectorAll('.gallery-slide');
    const indicators = galleryElement.querySelectorAll('.gallery-indicator');
    const prevBtn = galleryElement.querySelector('.gallery-prev');
    const nextBtn = galleryElement.querySelector('.gallery-next');
    
    if (slides.length <= 1) {
        // Ukryj przyciski jeśli jest tylko jedno zdjęcie lub mniej
        if (prevBtn) prevBtn.style.display = 'none';
        if (nextBtn) nextBtn.style.display = 'none';
        if (galleryElement.querySelector('.gallery-indicators')) {
            galleryElement.querySelector('.gallery-indicators').style.display = 'none';
        }
        return;
    }
    
    let currentSlide = 0;
    
    function showSlide(index) {
        // Sprawdź czy index jest prawidłowy
        if (index < 0) index = slides.length - 1;
        if (index >= slides.length) index = 0;
        
        // Ukryj wszystkie slajdy
        slides.forEach(slide => slide.classList.remove('active'));
        indicators.forEach(indicator => indicator.classList.remove('active'));
        
        // Pokaż wybrany slajd
        if (slides[index]) {
            slides[index].classList.add('active');
        }
        if (indicators[index]) {
            indicators[index].classList.add('active');
        }
        
        currentSlide = index;
    }
    
    function nextSlide() {
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }
    
    function prevSlide() {
        const prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }
    
    // Event listenery dla przycisków
    if (nextBtn) {
        nextBtn.addEventListener('click', (e) => {
            e.preventDefault();
            nextSlide();
        });
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', (e) => {
            e.preventDefault();
            prevSlide();
        });
    }
    
    // Event listenery dla wskaźników
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', (e) => {
            e.preventDefault();
            showSlide(index);
        });
    });
    
    // Obsługa klawiatury (tylko gdy galeria jest w fokusie)
    galleryElement.setAttribute('tabindex', '0');
    galleryElement.addEventListener('keydown', (e) => {
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                prevSlide();
                break;
            case 'ArrowRight':
                e.preventDefault();
                nextSlide();
                break;
        }
    });
    
    // Obsługa touch/swipe na urządzeniach mobilnych
    let touchStartX = 0;
    let touchEndX = 0;
    let touchStartY = 0;
    let touchEndY = 0;
    
    galleryElement.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }, { passive: true });
    
    galleryElement.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].clientX;
        touchEndY = e.changedTouches[0].clientY;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diffX = touchStartX - touchEndX;
        const diffY = touchStartY - touchEndY;
        
        // Sprawdź czy to poziomy swipe (bardziej poziomy niż pionowy)
        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > swipeThreshold) {
            if (diffX > 0) {
                // Swipe left - next slide
                nextSlide();
            } else {
                // Swipe right - prev slide
                prevSlide();
            }
        }
    }
    
    // Opcjonalne: automatyczne przewijanie (odkomentuj jeśli chcesz)
    /*
    let autoSlideInterval;
    
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 5000); // 5 sekund
    }
    
    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }
    
    // Zatrzymaj automatyczne przewijanie podczas hover
    galleryElement.addEventListener('mouseenter', stopAutoSlide);
    galleryElement.addEventListener('mouseleave', startAutoSlide);
    
    // Uruchom automatyczne przewijanie
    startAutoSlide();
    */
    
    // Upewnij się że pierwszy slide jest aktywny
    showSlide(0);
}