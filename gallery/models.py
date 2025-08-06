from django.db import models

class Gallery(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Galeria #{self.id}"
    
    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerie"

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']