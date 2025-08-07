document.addEventListener('DOMContentLoaded', () => {
    
    // Funkcja do inicjalizacji pojedynczej galerii
    function initGallery(galleryElement) {
        console.log('DZIAŁA!');
        
        const slides = galleryElement.querySelectorAll('.slide');
        const dots = galleryElement.querySelectorAll('.dot');
        const prevBtn = galleryElement.querySelector('.prev');
        const nextBtn = galleryElement.querySelector('.next');
        let currentIndex = 0;
    
        if (slides.length === 0) return;
    
        function showSlide(index) {
            if (index >= slides.length) {
                index = 0;
            } else if (index < 0) {
                index = slides.length - 1;
            }
    
            slides.forEach(slide => slide.style.display = 'none');
            dots.forEach(dot => dot.classList.remove('active'));
    
            slides[index].style.display = 'block';
            if (dots[index]) {
                dots[index].classList.add('active');
            }
            
            currentIndex = index;
        }
    
        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => {
                showSlide(currentIndex - 1);
            });
    
            nextBtn.addEventListener('click', () => {
                showSlide(currentIndex + 1);
            });
        }
    
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showSlide(index);
            });
        });
    
        showSlide(0);
    }

    // Znajdź wszystkie galerie na stronie i zainicjuj każdą z nich
    const galleries = document.querySelectorAll('[gallery]');
    galleries.forEach(initGallery);
});