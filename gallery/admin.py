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
                        <div id="visible-area-{}" style="position: absolute; top: 0; left: 0; right: 0; height: 150px; border-top: 2px dashed red; border-bottom: 2px dashed red; z-index: 10; pointer-events: none;"></div>
                        <div id="top-overlay-{}" style="position: absolute; top: -117px; left: 0; right: 0; height: 117px; background: rgba(0,0,0,0.5); z-index: 5; pointer-events: none;"></div>
                        <div id="bottom-overlay-{}" style="position: absolute; bottom: -117px; left: 0; right: 0; height: 117px; background: rgba(0,0,0,0.5); z-index: 5; pointer-events: none;"></div>
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
                    
                    // reszta JS...
                }})();
                </script>
            ''', 
            obj.id,                    # 1 - visual-editor-{}
            obj.id,                    # 2 - preview-img-{}  
            obj.image.url,             # 3 - src="{}"
            obj.vertical_position or 50, # 4 - object-position center {}%
            obj.id,                    # 5 - visible-area-{}
            obj.id,                    # 6 - top-overlay-{}
            obj.id,                    # 7 - bottom-overlay-{}
            obj.id,                    # 8 - position-input-{}
            obj.vertical_position or 50, # 9 - value="{}"
            obj.id,                    # 10 - position-value-{}
            obj.vertical_position or 50, # 11 - span content {}%
            obj.id,                    # 12 - preview-img-{} w JS
            obj.id,                    # 13 - position-input-{} w JS
            obj.id,                    # 14 - position-value-{} w JS
            obj.vertical_position or 50, # 15 - value="{}" w JS
            obj.vertical_position or 50) # 16 - startPosition = {}
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