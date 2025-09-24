from django.contrib import admin
from django.utils.html import format_html
from .models import Gallery, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['image', 'media_type', 'order', 'vertical_position', 'visual_editor']
    readonly_fields = ['media_type', 'visual_editor']
    extra = 0

    def visual_editor(self, obj):
        if obj and obj.image:
            return format_html('''
                <div id="visual-editor-{}" style="width: 200px; position: relative; margin: 10px 0;">
                    <div style="width: 200px; height: 150px; border: 2px solid #ddd; position: relative; overflow: hidden; background: #f5f5f5;">
                        <img id="preview-img-{}" src="{}" 
                             style="width: 200px; height: 267px; object-fit: cover; object-position: center {}%; position: absolute; cursor: grab;">
                        <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px; background: red; border-top: 2px dashed red; z-index: 10;"></div>
                        <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 2px; background: red; border-bottom: 2px dashed red; z-index: 10;"></div>
                    </div>
                    <input type="hidden" id="position-input-{}" value="{}">
                    <div style="text-align: center; margin-top: 5px; font-size: 12px;">
                        Pozycja: <span id="position-value-{}">{}</span>%
                    </div>
                </div>
                <script>
                (function() {{
                    const img = document.getElementById('preview-img-{}');
                    const input = document.getElementById('position-input-{}');
                    const valueSpan = document.getElementById('position-value-{}');
                    const fieldInput = document.querySelector('input[name*="vertical_position"][value="{}"]');
                    
                    let isDragging = false;
                    let startY = 0;
                    let startPosition = {};
                    
                    img.addEventListener('mousedown', function(e) {{
                        isDragging = true;
                        startY = e.clientY;
                        startPosition = parseInt(input.value);
                        img.style.cursor = 'grabbing';
                        e.preventDefault();
                    }});
                    
                    document.addEventListener('mousemove', function(e) {{
                        if (!isDragging) return;
                        
                        const deltaY = e.clientY - startY;
                        const sensitivity = 0.5;
                        let newPosition = startPosition - (deltaY * sensitivity);
                        
                        newPosition = Math.max(0, Math.min(100, newPosition));
                        
                        input.value = Math.round(newPosition);
                        valueSpan.textContent = Math.round(newPosition);
                        img.style.objectPosition = `center ${{newPosition}}%`;
                        
                        if (fieldInput) {{
                            fieldInput.value = Math.round(newPosition);
                        }}
                    }});
                    
                    document.addEventListener('mouseup', function() {{
                        if (isDragging) {{
                            isDragging = false;
                            img.style.cursor = 'grab';
                        }}
                    }});
                }})();
                </script>
            ''', 
            obj.id, obj.id, obj.image.url, obj.vertical_position or 50, obj.id, 
            obj.vertical_position or 50, obj.id, obj.vertical_position or 50,
            obj.id, obj.id, obj.id, obj.vertical_position or 50, obj.vertical_position or 50)
        return ""
    visual_editor.short_description = 'Edytor wizualny'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'photo_count']
    search_fields = ['title']
    inlines = [PhotoInline]
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Zdjęć'