from django.contrib import admin
from .models import Gallery, Media

class MediaInline(admin.TabularInline):
    model = Media
    fields = ['file', 'media_type', 'order', 'thumbnail']
    readonly_fields = ['media_type']
    extra = 0

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'media_count', 'images_count', 'videos_count']
    search_fields = ['title']
    inlines = [MediaInline]
    
    def media_count(self, obj):
        return obj.media_files.count()
    media_count.short_description = 'Wszystkich plików'
    
    def images_count(self, obj):
        return obj.media_files.filter(media_type='image').count()
    images_count.short_description = 'Zdjęć'
    
    def videos_count(self, obj):
        return obj.media_files.filter(media_type='video').count()
    videos_count.short_description = 'Wideo'

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'media_type', 'gallery', 'order']
    list_filter = ['media_type', 'gallery']
    search_fields = ['gallery__title']