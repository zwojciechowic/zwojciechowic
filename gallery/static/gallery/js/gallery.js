// ULTRA PROSTY JAVASCRIPT
document.addEventListener('DOMContentLoaded', function() {
    const galleries = document.querySelectorAll('.simple-gallery');
    
    galleries.forEach(gallery => {
        const slides = gallery.querySelectorAll('.gallery-slide');
        const dots = gallery.querySelectorAll('.dot');
        const prevBtn = gallery.querySelector('.gallery-prev');
        const nextBtn = gallery.querySelector('.gallery-next');
        
        if (slides.length <= 1) return;
        
        let current = 0;
        
        function showSlide(n) {
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            slides[n].classList.add('active');
            dots[n].classList.add('active');
            current = n;
        }
        
        function nextSlide() {
            const next = (current + 1) % slides.length;
            showSlide(next);
        }
        
        function prevSlide() {
            const prev = (current - 1 + slides.length) % slides.length;
            showSlide(prev);
        }
        
        if (nextBtn) nextBtn.onclick = nextSlide;
        if (prevBtn) prevBtn.onclick = prevSlide;
        
        dots.forEach((dot, index) => {
            dot.onclick = () => showSlide(index);
        });
    });
});