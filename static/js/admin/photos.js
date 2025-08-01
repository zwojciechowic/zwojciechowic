// static/js/admin/photos.js
document.addEventListener('DOMContentLoaded', function() {
    const widgets = document.querySelectorAll('.photos-widget');
    
    widgets.forEach(widget => {
        const fieldName = widget.dataset.field;
        const input = widget.querySelector('.photo-input');
        const container = widget.querySelector('.photos-container');
        const hiddenField = widget.querySelector('.photos-data');
        let photos = [];
        let nextIndex = 0;
        
        // Załaduj istniejące zdjęcia
        loadExistingPhotos();
        
        // Obsługa dodawania nowych plików
        input.addEventListener('change', function(e) {
            console.log('Files selected:', e.target.files.length); // Debug
            handleFiles(e.target.files);
            // Nie resetuj input od razu - zrób to po przetworzeniu
            setTimeout(() => {
                e.target.value = '';
            }, 100);
        });
        
        // Drag & Drop
        setupDragAndDrop();
        
        function loadExistingPhotos() {
            const items = container.querySelectorAll('.photo-item');
            items.forEach((item, index) => {
                const img = item.querySelector('img');
                const orderInput = item.querySelector('.order-input');
                if (img) {
                    photos.push({
                        url: img.src,
                        order: parseInt(orderInput.value) || index + 1,
                        index: index
                    });
                    nextIndex = Math.max(nextIndex, index + 1);
                }
            });
        }
        
        function handleFiles(files) {
            console.log('Processing files:', files.length); // Debug
            Array.from(files).forEach((file, index) => {
                console.log('File', index, ':', file.name, file.type); // Debug
                if (file.type.startsWith('image/')) {
                    addPhoto(file);
                } else {
                    console.log('Skipping non-image file:', file.type);
                }
            });
        }
        
        function addPhoto(file) {
            console.log('Adding photo:', file.name); // Debug
            const reader = new FileReader();
            reader.onload = function(e) {
                console.log('Photo loaded, creating preview'); // Debug
                const photo = {
                    url: e.target.result,
                    file: file,
                    order: photos.length + 1,
                    index: nextIndex++,
                    isNew: true
                };
                photos.push(photo);
                renderPhoto(photo);
                updateHiddenField();
                
                // Przygotuj plik do przesłania
                prepareFileForUpload(file, photo.index);
            };
            reader.onerror = function(e) {
                console.error('Error reading file:', e);
            };
            reader.readAsDataURL(file);
        }
        
        function prepareFileForUpload(file, photoIndex) {
            console.log('prepareFileForUpload called for:', file.name, 'index:', photoIndex);
            
            // Utwórz ukryty input file dla każdego nowego zdjęcia
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.name = `new_photo_${photoIndex}`;
            fileInput.style.display = 'none';
            
            // Stwórz DataTransfer aby przypisać plik do input
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            
            // POPRAWKA: Dodaj do formularza, nie do widget
            const form = widget.closest('form');
            if (form) {
                form.appendChild(fileInput);
                console.log('File input added to form:', fileInput.name);
            } else {
                console.error('Could not find form element');
            }
        }
        
        function renderPhoto(photo) {
            console.log('Rendering photo:', photo.url.substring(0, 50) + '...'); // Debug
            const div = document.createElement('div');
            div.className = 'photo-item';
            div.dataset.index = photo.index;
            div.innerHTML = `
                <img src="${photo.url}" alt="Zdjęcie" style="width: 150px; height: 100px; object-fit: cover; border-radius: 4px;" />
                <span class="remove-photo" onclick="removePhoto(this, '${fieldName}')">×</span>
                <input type="number" value="${photo.order}" min="1" class="order-input" 
                       onchange="updatePhotoOrder(this, '${fieldName}')" />
            `;
            container.appendChild(div);
            console.log('Photo rendered, container now has', container.children.length, 'items');
        }
        
        function setupDragAndDrop() {
            const uploadArea = input.parentElement;
            
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, preventDefaults, false);
            });
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            ['dragenter', 'dragover'].forEach(eventName => {
                uploadArea.addEventListener(eventName, () => {
                    input.style.background = '#e3f2fd';
                    input.style.borderColor = '#1976d2';
                }, false);
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, () => {
                    input.style.background = '#f0f8ff';
                    input.style.borderColor = '#007cba';
                }, false);
            });
            
            uploadArea.addEventListener('drop', function(e) {
                const files = e.dataTransfer.files;
                handleFiles(files);
            });
        }
        
        function updateHiddenField() {
            const photoData = photos.map(photo => ({
                url: photo.url,
                order: photo.order,
                filename: photo.filename || ''
            }));
            hiddenField.value = JSON.stringify(photoData);
        }
        
        // Zapisz referencje do funkcji dla tego konkretnego widgetu
        widget.removePhotoFunction = function(element) {
            const photoItem = element.closest('.photo-item');
            const index = parseInt(photoItem.dataset.index);
            
            // Usuń z tablicy photos
            photos = photos.filter(photo => photo.index !== index);
            
            // Usuń z DOM
            photoItem.remove();
            
            // Przeindeksuj kolejność
            photos.forEach((photo, newIndex) => {
                photo.order = newIndex + 1;
            });
            
            // Aktualizuj numerację w DOM
            Array.from(container.children).forEach((item, domIndex) => {
                const orderInput = item.querySelector('.order-input');
                orderInput.value = domIndex + 1;
            });
            
            updateHiddenField();
        };
        
        widget.updateOrderFunction = function(element) {
            const photoItem = element.closest('.photo-item');
            const index = parseInt(photoItem.dataset.index);
            const newOrder = parseInt(element.value);
            
            // Znajdź zdjęcie i zaktualizuj kolejność
            const photo = photos.find(p => p.index === index);
            if (photo) {
                photo.order = newOrder;
                updateHiddenField();
            }
        };
    });
});

// Globalne funkcje wywoływane przez onclick
function removePhoto(element, fieldName) {
    const widget = element.closest('.photos-widget');
    if (widget && widget.removePhotoFunction) {
        widget.removePhotoFunction(element);
    }
}

function updatePhotoOrder(element, fieldName) {
    const widget = element.closest('.photos-widget');
    if (widget && widget.updateOrderFunction) {
        widget.updateOrderFunction(element);
    }
}