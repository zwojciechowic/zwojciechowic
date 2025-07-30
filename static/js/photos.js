// static/js/admin/photos.js
document.addEventListener('DOMContentLoaded', function() {
    const widgets = document.querySelectorAll('.photos-widget');
    
    widgets.forEach(widget => {
        const input = widget.querySelector('.photo-input');
        const container = widget.querySelector('.photos-container');
        const hiddenField = widget.querySelector('.photos-data');
        let photos = [];
        
        // Załaduj istniejące zdjęcia
        loadExistingPhotos();
        
        // Obsługa nowych plików
        input.addEventListener('change', e => {
            Array.from(e.target.files).forEach(addPhoto);
        });
        
        function loadExistingPhotos() {
            const items = container.querySelectorAll('.photo-item');
            items.forEach((item, index) => {
                const img = item.querySelector('img');
                if (img) {
                    photos.push({
                        url: img.src,
                        order: index
                    });
                }
            });
        }
        
        function addPhoto(file) {
            const reader = new FileReader();
            reader.onload = e => {
                const photo = {
                    url: e.target.result,
                    file: file,
                    order: photos.length
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
            div.innerHTML = `
                <img src="${photo.url}" />
                <button type="button" onclick="removePhoto(${index})">×</button>
                <input type="number" value="${index + 1}" min="1" onchange="updateOrder(${index}, this.value)" />
            `;
            container.appendChild(div);
        }
        
        window.removePhoto = function(index) {
            photos.splice(index, 1);
            container.children[index].remove();
            updateIndices();
            updateHiddenField();
        };
        
        window.updateOrder = function(index, newOrder) {
            const photo = photos[index];
            photos.splice(index, 1);
            photos.splice(newOrder - 1, 0, photo);
            reRender();
            updateHiddenField();
        };
        
        function updateIndices() {
            Array.from(container.children).forEach((item, index) => {
                const removeBtn = item.querySelector('button');
                const orderInput = item.querySelector('input');
                removeBtn.setAttribute('onclick', `removePhoto(${index})`);
                orderInput.setAttribute('onchange', `updateOrder(${index}, this.value)`);
                orderInput.value = index + 1;
            });
        }
        
        function reRender() {
            container.innerHTML = '';
            photos.forEach((photo, index) => renderPhoto(photo, index));
        }
        
        function updateHiddenField() {
            hiddenField.value = JSON.stringify(photos.map(p => ({
                url: p.url,
                order: p.order
            })));
        }
    });
});