from django import template
from ..models import Gallery

register = template.Library()

# Zmieniamy definicję tagu, dodając drugi, opcjonalny argument
@register.inclusion_tag('gallery/gallery.html')
def show_gallery(gallery_id, extra_classes=""):
    """
    Tag szablonu do wyświetlania galerii zdjęć.
    
    Użycie:
    {% show_gallery gallery.id %}
    {% show_gallery gallery.id "moja-klasa-css" %}
    """
    try:
        gallery = Gallery.objects.prefetch_related('photos').get(id=gallery_id)
        photos = gallery.photos.all()
    except Gallery.DoesNotExist:
        gallery = None
        photos = []
        
    return {
        'gallery': gallery,
        'photos': photos,
        'extra_classes': extra_classes, # Przekazujemy klasy do szablonu
    }