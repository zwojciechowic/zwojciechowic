// static/js/admin_image_preview.js
document.addEventListener('DOMContentLoaded', function() {
    // Funkcja dodawania podglądu zdjęcia
    function addImagePreview(inputField) {
        const previewId = inputField.id + '_preview';
        
        // Usuń istniejący podgląd jeśli istnieje
        const existingPreview = document.getElementById(previewId);
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // Dodaj kontener na podgląd
        const previewDiv = document.createElement('div');
        previewDiv.id = previewId;
        previewDiv.style.marginTop = '10px';
        inputField.parentNode.insertBefore(previewDiv, inputField.nextSibling);
        
        // Obsługa zmiany pliku
        inputField.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const previewContainer = document.getElementById(previewId);
            
            previewContainer.innerHTML = '';
            
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewContainer.innerHTML =
                        '<img src="' + e.target.result + '" ' +
                             'style="max-width: 400px; max-height: 400px; object-fit: cover; border-radius: 4px; display: block;" />';
                };
                
                reader.readAsDataURL(file);
            }
        });
    }

    // Zastosuj podgląd do wszystkich pól zdjęć
    const imageInputs = document.querySelectorAll('input[type="file"][name$="photo"], input[type="file"][name$="featured_image"], input[type="file"][name$="certificate"]');
    imageInputs.forEach(function(input) {
        addImagePreview(input);
    });
});