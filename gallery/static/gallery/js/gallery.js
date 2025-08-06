// DZIAŁAJĄCY JAVASCRIPT
document.addEventListener('DOMContentLoaded', function() {
    console.log('Gallery JS loaded');
    
    const galleries = document.querySelectorAll('.gallery-widget');
    console.log('Found galleries:', galleries.length);
    
    galleries.forEach(gallery => {
        const slides = gallery.querySelectorAll('.gallery-slide');
        const indicators = gallery.querySelectorAll('.gallery-indicator');
        const prevBtn = gallery.querySelector('.gallery-prev');
        const nextBtn = gallery.querySelector('.gallery-next');
        
        console.log('Gallery slides:', slides.length);
        
        if (slides.length <= 1) {
            if (prevBtn) prevBtn.style.display = 'none';
            if (nextBtn) nextBtn.style.display = 'none';
            return;
        }
        
        let currentSlide = 0;
        
        function showSlide(index) {
            console.log('Showing slide:', index);
            
            // Ukryj wszystkie
            slides.forEach(slide => {
                slide.classList.remove('active');
            });
            indicators.forEach(indicator => {
                indicator.classList.remove('active');
            });
            
            // Pokaż aktywny
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
        
        // WAŻNE: Event listenery
        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Next clicked');
                nextSlide();
            });
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Prev clicked');
                prevSlide();
            });
        }
        
        // Wskaźniki
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Indicator clicked:', index);
                showSlide(index);
            });
        });
        
        // Pokaż pierwszy slide
        showSlide(0);
    });
});