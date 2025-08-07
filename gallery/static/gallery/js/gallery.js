document.addEventListener('DOMContentLoaded', () => {
    
    // Funkcja do inicjalizacji pojedynczej galerii
    function initGallery(galleryElement) {
        const slides = galleryElement.querySelectorAll('.slide');
        const dots = galleryElement.querySelectorAll('.dot');
        const prevBtn = galleryElement.querySelector('.prev');
        const nextBtn = galleryElement.querySelector('.next');
        let currentIndex = 0;

        if (slides.length === 0) return; // Nie rób nic, jeśli nie ma slajdów

        function showSlide(index) {
            // Upewnij się, że indeks jest w poprawnym zakresie
            if (index >= slides.length) {
                index = 0;
            } else if (index < 0) {
                index = slides.length - 1;
            }

            // Ukryj wszystkie slajdy i usuń klasę 'active' z kropek
            slides.forEach(slide => slide.style.display = 'none');
            dots.forEach(dot => dot.classList.remove('active'));

            // Pokaż wybrany slajd i aktywuj kropkę
            slides[index].style.display = 'block';
            if (dots[index]) {
                dots[index].classList.add('active');
            }
            
            currentIndex = index;
        }

        // Dodaj event listenery do przycisków
        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => {
                showSlide(currentIndex - 1);
            });
    
            nextBtn.addEventListener('click', () => {
                showSlide(currentIndex + 1);
            });
        }

        // Dodaj event listenery do kropek
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showSlide(index);
            });
        });

        // Pokaż pierwszy slajd na starcie
        showSlide(0);
    }

    const galleries = document.querySelectorAll('.gallery');
    console.log('Znalezione galerie:', galleries.length);
    
    for (let i = 0; i < galleries.length; i++) {
        console.log('WYWOŁUJĘ dla galerii nr', i);
        initGallery(galleries[i]);
    }
});