from django import template
from ..models import Gallery

register = template.Library()

@register.inclusion_tag('gallery/gallery.html')
def show_gallery(gallery_id):
    try:
        # Użycie prefetch_related jest dobrą praktyką dla optymalizacji zapytań
        gallery = Gallery.objects.prefetch_related('photos').get(id=gallery_id)
        photos = gallery.photos.all()
    except Gallery.DoesNotExist:
        # Eleganckie obsłużenie przypadku, gdy galeria nie istnieje
        photos = []
        
    return {'photos': photos}