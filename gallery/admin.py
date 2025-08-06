# gallery/admin.py - UPROSZCZONY
from django.contrib import admin
from django.utils.html import format_html
from .models import GallerySet, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 5  # 5 pustych pól do dodania zdjęć
    fields = ['image', 'order', 'is_active']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "Brak zdjęcia"
    image_preview.short_description = "Podgląd"

@admin.register(GallerySet)
class GallerySetAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    inlines = [PhotoInline]
    
    def photo_count(self, obj):
        return obj.get_photos().count()
    photo_count.short_description = 'Zdjęć'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'order', 'image_preview', 'is_active', 'created_at']
    list_filter = ['gallery', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    ordering = ['gallery', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "Brak"
    image_preview.short_description = "Podgląd"