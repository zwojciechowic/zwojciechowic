from django.db import models
from django.urls import reverse

class GallerySet(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa galerii")
    description = models.TextField(blank=True, verbose_name="Opis")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktywna")
    
    class Meta:
        verbose_name = "Zbiór zdjęć"
        verbose_name_plural = "Zbiory zdjęć"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_photos(self):
        return self.photos.filter(is_active=True).order_by('order', 'id')

class Photo(models.Model):
    gallery_set = models.ForeignKey(GallerySet, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/%Y/%m/', verbose_name="Zdjęcie")
    title = models.CharField(max_length=200, blank=True, verbose_name="Tytuł")
    description = models.TextField(blank=True, verbose_name="Opis")
    order = models.PositiveIntegerField(default=0, verbose_name="Kolejność")
    is_active = models.BooleanField(default=True, verbose_name="Aktywne")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.title or f"Zdjęcie {self.id}"