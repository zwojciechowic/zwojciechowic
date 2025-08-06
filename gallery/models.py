# gallery/models.py - UPROSZCZONY
from django.db import models

class GallerySet(models.Model):
    """Zestaw zdjęć - bez zbędnego syfu"""
    name = models.CharField(max_length=100, help_text="Tylko nazwa do identyfikacji")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_photos(self):
        """Zwraca wszystkie zdjęcia z tego zestawu"""
        return self.photos.filter(is_active=True).order_by('order')
    
    def __str__(self):
        return f"{self.name} ({self.get_photos().count()} zdjęć)"
    
    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerie"

class Photo(models.Model):
    """Pojedyncze zdjęcie - BEZ tytułów i opisów"""
    gallery = models.ForeignKey(GallerySet, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/', help_text="Po prostu wrzuć zdjęcie")
    order = models.PositiveIntegerField(default=0, help_text="Kolejność (0, 1, 2...)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Zdjęcie #{self.order} z {self.gallery.name}"
    
    class Meta:
        ordering = ['order', 'created_at']