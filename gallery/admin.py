# gallery/admin.py
from django.contrib import admin
from .models import Gallery, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['image', 'order']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'photo_count']
    inlines = [PhotoInline]
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Zdjęć'