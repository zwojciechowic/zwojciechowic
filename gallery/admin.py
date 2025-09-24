from django.contrib import admin
from django.utils.html import format_html
from .models import Gallery, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['image', 'media_type', 'order', 'image_preview', 'position_controls']
    readonly_fields = ['media_type', 'image_preview', 'position_controls']
    extra = 0

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:120px; height:80px; object-fit:cover; object-position: center {}%; border: 1px solid #ddd;">',
                obj.image.url, obj.vertical_position or 50
            )
        return ""
    image_preview.short_description = 'Podgląd'
    
    def position_controls(self, obj):
        if obj and obj.id:
            return format_html(
                '<div style="text-align:center;">'
                '<button type="button" onclick="adjustPosition({}, \'up\')" style="display:block; margin:2px auto; padding:5px 10px;">↑</button>'
                '<button type="button" onclick="adjustPosition({}, \'down\')" style="display:block; margin:2px auto; padding:5px 10px;">↓</button>'
                '</div>'
                '<script>'
                'function adjustPosition(id, dir) {{'
                '  fetch(`/admin/adjust-photo-position/${id}/${dir}/`, {{'
                '    method: "POST",'
                '    headers: {{"X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value}}'
                '  }}).then(() => location.reload());'
                '}}'
                '</script>',
                obj.id, obj.id
            )
        return "Zapisz najpierw"
    position_controls.short_description = 'Pozycja'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'photo_count']
    search_fields = ['title']
    inlines = [PhotoInline]
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Zdjęć'