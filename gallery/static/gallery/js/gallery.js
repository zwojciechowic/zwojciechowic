document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript się ładuje!');
    
    function initGallery(galleryElement) {
        console.log('DZIAŁA!');
    }
    
    const galleries = document.querySelectorAll('.gallery');
    console.log('Znalezione galerie:', galleries.length);
    
    for (let i = 0; i < galleries.length; i++) {
        console.log('WYWOŁUJĘ dla galerii nr', i);
        initGallery(galleries[i]);
    }
});