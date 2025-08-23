from django.contrib import admin
from .models import Gallery, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['image', 'media_type', 'order']
    readonly_fields = ['media_type']
    extra = 0

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'photo_count']
    search_fields = ['title']
    inlines = [PhotoInline]
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Zdjęć'