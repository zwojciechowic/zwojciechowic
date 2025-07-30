// static/js/multiple_photos.js
document.addEventListener('DOMContentLoaded', function() {
    let photosData = [];
    let nextOrder = 1;

    function initializeMultiplePhotos() {
        const fileInput = document.getElementById('additional_photos_input');
        const container = document.getElementById('additional-photos-container');
        
        if (!fileInput) return;

        // Wczytaj istniejące zdjęcia
        loadExistingPhotos();

        // Obsługa wyboru nowych plików
        fileInput.addEventListener('change', function(e) {
            handleFileSelection(e.target.files);
        });

        // Obsługa drag & drop
        setupDragAndDrop();
    }

    function loadExistingPhotos() {
        const container = document.getElementById('additional-photos-container');
        if (!container) return;

        const photoItems = container.querySelectorAll('.photo-item');
        photoItems.forEach((item, index) => {
            const img = item.querySelector('img');
            const orderInput = item.querySelector('.order-input');
            const removeBtn = item.querySelector('.remove-photo');

            if (img && orderInput) {
                photosData.push({
                    url: img.src,
                    order: parseInt(orderInput.value) || index + 1,
                    index: index
                });

                // Obsługa zmiany kolejności
                orderInput.addEventListener('change', function() {
                    updatePhotoOrder(index, parseInt(this.value));
                });

                // Obsługa usuwania
                removeBtn.addEventListener('click', function() {
                    removePhoto(index);
                });
            }
        });

        nextOrder = Math.max(...photosData.map(p => p.order), 0) + 1;
    }

    function handleFileSelection(files) {
        Array.from(files).forEach(file => {
            if (file.type.startsWith('image/')) {
                addPhotoPreview(file);
            }
        });
    }

    function addPhotoPreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const photoData = {
                url: e.target.result,
                file: file,
                order: nextOrder++,
                index: photosData.length
            };

            photosData.push(photoData);
            renderPhoto(photoData);
        };
        reader.readAsDataURL(file);
    }

    function renderPhoto(photoData) {
        const container = document.getElementById('additional-photos-container');
        if (!container) return;

        const photoDiv = document.createElement('div');
        photoDiv.className = 'photo-item';
        photoDiv.dataset.index = photoData.index;

        photoDiv.innerHTML = `
            <img src="${photoData.url}" alt="Zdjęcie ${photoData.order}" />
            <span class="remove-photo" onclick="removePhoto(${photoData.index})">×</span>
            <input type="number" value="${photoData.order}" min="1" class="order-input" 
                   onchange="updatePhotoOrder(${photoData.index}, this.value)" />
        `;

        container.appendChild(photoDiv);
    }

    function removePhoto(index) {
        // Usuń z tablicy
        photosData = photosData.filter(photo => photo.index !== index);
        
        // Usuń z DOM
        const photoItem = document.querySelector(`.photo-item[data-index="${index}"]`);
        if (photoItem) {
            photoItem.remove();
        }

        // Aktualizuj ukryte pole
        updateHiddenField();
    }

    function updatePhotoOrder(index, newOrder) {
        const photo = photosData.find(p => p.index === index);
        if (photo) {
            photo.order = parseInt(newOrder);
            updateHiddenField();
        }
    }

    function updateHiddenField() {
        // Sortuj zdjęcia według kolejności
        const sortedPhotos = photosData.sort((a, b) => a.order - b.order);
        
        // Utwórz ukryte pole z danymi JSON
        let hiddenField = document.getElementById('additional_photos_data');
        if (!hiddenField) {
            hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.id = 'additional_photos_data';
            hiddenField.name = 'additional_photos_data';
            document.querySelector('form').appendChild(hiddenField);
        }

        const photoUrls = sortedPhotos.map(photo => ({
            url: photo.url,
            order: photo.order
        }));

        hiddenField.value = JSON.stringify(photoUrls);
    }

    function setupDragAndDrop() {
        const fileInput = document.getElementById('additional_photos_input');
        if (!fileInput) return;

        const uploadArea = fileInput.parentElement;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            uploadArea.classList.add('dragover');
        }

        function unhighlight(e) {
            uploadArea.classList.remove('dragover');
        }

        uploadArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFileSelection(files);
        }
    }

    // Globalne funkcje dla onclick handlers
    window.removePhoto = removePhoto;
    window.updatePhotoOrder = updatePhotoOrder;

    // Inicjalizacja
    initializeMultiplePhotos();

    // Obsługa formularza przed wysłaniem
    document.querySelector('form').addEventListener('submit', function() {
        updateHiddenField();
    });
});