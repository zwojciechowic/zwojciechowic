from django.db import models
import os

class Gallery(models.Model):
    title = models.CharField("Nazwa galerii", max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.title:
            if not self.pk:
                count = Gallery.objects.count() + 1
                self.title = f"Galeria #{count}"
            else:
                self.title = f"Galeria #{self.pk}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerie"

class Media(models.Model):
    MEDIA_TYPES = (
        ('image', 'Zdjęcie'),
        ('video', 'Wideo'),
    )
    
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='gallery/')  # Zmiana z ImageField na FileField
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES, editable=False)
    order = models.PositiveIntegerField(default=1)
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Automatyczne określanie typu na podstawie rozszerzenia
        if self.file:
            file_extension = os.path.splitext(self.file.name)[1].lower()
            
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
            video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v']
            
            if file_extension in image_extensions:
                self.media_type = 'image'
            elif file_extension in video_extensions:
                self.media_type = 'video'
            else:
                raise ValueError(f"Nieobsługiwany format pliku: {file_extension}")
        
        super().save(*args, **kwargs)
    
    @property
    def is_image(self):
        return self.media_type == 'image'
    
    @property
    def is_video(self):
        return self.media_type == 'video'
    
    def __str__(self):
        return f"{self.gallery.title} - {self.get_media_type_display()}"
    
    class Meta:
        ordering = ['order']
        verbose_name = "Plik multimedialny"
        verbose_name_plural = "Pliki multimedialne"

# Zachowaj kompatybilność z poprzednim kodem
Photo = Media