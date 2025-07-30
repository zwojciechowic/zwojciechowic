// static/js/admin/photos.js
document.addEventListener('DOMContentLoaded', function() {
    const widgets = document.querySelectorAll('.photos-widget');
    
    widgets.forEach(widget => {
        const fieldName = widget.dataset.field;
        const input = widget.querySelector('.photo-input');
        const container = widget.querySelector('.photos-container');
        const hiddenField = widget.querySelector('.photos-data');
        let photos = [];
        
        // Załaduj istniejące zdjęcia
        loadExistingPhotos();
        
        // Obsługa dodawania nowych plików
        input.addEventListener('change', function(e) {
            Array.from(e.target.files).forEach(file => {
                if (file.type.startsWith('image/')) {
                    addPhoto(file);
                }
            });
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
                        order: parseInt(orderInput.value) || index + 1
                    });
                }
            });
        }
        
        function addPhoto(file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const photo = {
                    url: e.target.result,
                    file: file,
                    order: photos.length + 1
                };
                photos.push(photo);
                renderPhoto(photo, photos.length - 1);
                updateHiddenField();
            };
            reader.readAsDataURL(file);
        }
        
        function renderPhoto(photo, index) {
            const div = document.createElement('div');
            div.className = 'photo-item';
            div.dataset.index = index;
            div.innerHTML = `
                <img src="${photo.url}" style="width: 150px; height: 100px; object-fit: cover;" />
                <span class="remove-photo" onclick="removePhoto(this, '${fieldName}')">×</span>
                <input type="number" value="${photo.order}" min="1" class="order-input" 
                       onchange="updatePhotoOrder(this, '${fieldName}')" />
            `;
            container.appendChild(div);
        }
        
        function setupDragAndDrop() {
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                input.addEventListener(eventName, preventDefaults, false);
            });
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            ['dragenter', 'dragover'].forEach(eventName => {
                input.addEventListener(eventName, () => input.style.background = '#e3f2fd', false);
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                input.addEventListener(eventName, () => input.style.background = '#f0f8ff', false);
            });
            
            input.addEventListener('drop', function(e) {
                const files = e.dataTransfer.files;
                Array.from(files).forEach(file => {
                    if (file.type.startsWith('image/')) {
                        addPhoto(file);
                    }
                });
            });
        }
        
        function updateHiddenField() {
            hiddenField.value = JSON.stringify(photos);
        }
        
        // Zapisz referencje do funkcji dla tego konkretnego widgetu
        widget.removePhoto = function(element) {
            const photoItem = element.closest('.photo-item');
            const index = parseInt(photoItem.dataset.index);
            photos.splice(index, 1);
            photoItem.remove();
            reindexPhotos();
            updateHiddenField();
        };
        
        widget.updateOrder = function(element, newOrder) {
            const photoItem = element.closest('.photo-item');
            const index = parseInt(photoItem.dataset.index);
            photos[index].order = parseInt(newOrder);
            updateHiddenField();
        };
        
        function reindexPhotos() {
            Array.from(container.children).forEach((item, newIndex) => {
                item.dataset.index = newIndex;
                const orderInput = item.querySelector('.order-input');
                orderInput.value = newIndex + 1;
                photos[newIndex].order = newIndex + 1;
            });
        }
    });
});

// Globalne funkcje wywoływane przez onclick
function removePhoto(element, fieldName) {
    const widget = element.closest('.photos-widget');
    if (widget && widget.removePhoto) {
        widget.removePhoto(element);
    }
}

function updatePhotoOrder(element, fieldName) {
    const widget = element.closest('.photos-widget');
    if (widget && widget.updateOrder) {
        widget.updateOrder(element, element.value);
    }
}