# gallery/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import GallerySet, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3
    fields = ('image', 'title', 'description', 'order', 'is_active', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "Brak zdjęcia"
    preview.short_description = "Podgląd"

@admin.register(GallerySet)
class GallerySetAdmin(admin.ModelAdmin):
    list_display = ('name', 'photos_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    inlines = [PhotoInline]
    
    def photos_count(self, obj):
        return obj.photos.count()
    photos_count.short_description = "Liczba zdjęć"

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'gallery_set', 'order', 'is_active', 'preview')
    list_filter = ('gallery_set', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "Brak zdjęcia"
    preview.short_description = "Podgląd"
