// static/js/admin_image_preview.js
django.jQuery(document).ready(function($) {
    // Funkcja dodawania podglądu zdjęcia
    function addImagePreview(inputField) {
        const previewId = inputField.attr('id') + '_preview';
        
        // Usuń istniejący podgląd jeśli istnieje
        $('#' + previewId).remove();
        
        // Dodaj kontener na podgląd
        inputField.after(
            '<div id="' + previewId + '" style="margin-top: 10px;"></div>'
        );
        
        // Obsługa zmiany pliku
        inputField.on('change', function(e) {
            const file = e.target.files[0];
            const previewContainer = $('#' + previewId);
            
            previewContainer.empty();
            
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const imgHtml = 
                        '<div style="border: 2px solid #ddd; border-radius: 8px; padding: 10px; background: white; display: inline-block;">' +
                            '<img src="' + e.target.result + '" ' +
                                 'style="max-width: 200px; max-height: 200px; object-fit: cover; border-radius: 4px; display: block;" />' +
                            '<p style="margin: 8px 0 0 0; font-size: 12px; color: #666; text-align: center;">Podgląd zdjęcia</p>' +
                        '</div>';
                    previewContainer.html(imgHtml);
                };
                
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Zastosuj podgląd do wszystkich pól zdjęć
    $('input[type="file"][name$="photo"], input[type="file"][name$="featured_image"], input[type="file"][name$="certificate"]').each(function() {
        addImagePreview($(this));
    });
    
    // Dla dynamicznie dodawanych pól (inlines)
    $(document).on('DOMNodeInserted', function(e) {
        $(e.target).find('input[type="file"][name$="photo"], input[type="file"][name$="featured_image"], input[type="file"][name$="certificate"]').each(function() {
            if (!$(this).data('preview-added')) {
                addImagePreview($(this));
                $(this).data('preview-added', true);
            }
        });
    });
});