document.addEventListener('DOMContentLoaded', function() {
    function initGallery(galleryElement) {
        const slides = galleryElement.querySelectorAll('.slide');
        const dots = galleryElement.querySelectorAll('.dot');
        const prevBtn = galleryElement.querySelector('.prev');
        const nextBtn = galleryElement.querySelector('.next');
        let currentIndex = 0;
 
        if (slides.length === 0) return;
 
        function showSlide(index) {
            if (index >= slides.length) index = 0;
            else if (index < 0) index = slides.length - 1;
 
            slides.forEach(slide => slide.style.display = 'none');
            dots.forEach(dot => dot.classList.remove('active'));
 
            slides[index].style.display = 'block';
            if (dots[index]) dots[index].classList.add('active');
            
            currentIndex = index;
        }
 
        if (prevBtn) prevBtn.addEventListener('click', () => showSlide(currentIndex - 1));
        if (nextBtn) nextBtn.addEventListener('click', () => showSlide(currentIndex + 1));
 
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => showSlide(index));
        });
 
        showSlide(0);
    }
 
    const galleries = document.querySelectorAll('.gallery');
    galleries.forEach(gallery => initGallery(gallery));
 });