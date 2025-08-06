from django import template
from ..models import Gallery

register = template.Library()

@register.inclusion_tag('gallery/gallery.html')
def show_gallery(gallery_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        photos = gallery.photos.all()
        return {'photos': photos}
    except Gallery.DoesNotExist:
        return {'photos': []}