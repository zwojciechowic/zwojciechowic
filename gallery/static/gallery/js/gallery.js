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
        return;
    }
    
    let currentSlide = 0;
    
    function showSlide(index) {
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
        nextBtn.addEventListener('click', nextSlide);
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', prevSlide);
    }
    
    // Event listenery dla wskaźników
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => showSlide(index));
    });
    
    // Obsługa klawiatury
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
    
    // Opcjonalne: automatyczne przewijanie
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
    
    // Uruchom automatyczne przewijanie (opcjonalne)
    // startAutoSlide();
    
    // Obsługa touch/swipe na urządzeniach mobilnych
    let touchStartX = 0;
    let touchEndX = 0;
    
    galleryElement.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    galleryElement.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next slide
                nextSlide();
            } else {
                // Swipe right - prev slide
                prevSlide();
            }
        }
    }
}