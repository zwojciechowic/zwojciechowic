from django.db import models

class Gallery(models.Model):
    title = models.CharField("Nazwa galerii", max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Jeśli nie podano tytułu, ustaw domyślny
        if not self.title:
            if not self.pk:  # Nowa galeria
                # Sprawdź ile już jest galerii żeby nadać kolejny numer
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

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/')
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']