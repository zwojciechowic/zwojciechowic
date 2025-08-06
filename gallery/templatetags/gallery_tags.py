# gallery/templatetags/gallery_tags.py
from django import template
from ..models import GallerySet

register = template.Library()

@register.inclusion_tag('gallery/widget.html')
def gallery_widget(gallery_id, css_class=''):
    """Template tag do wstawienia galerii"""
    try:
        gallery = GallerySet.objects.get(id=gallery_id, is_active=True)
        photos = gallery.get_photos()
        return {
            'gallery': gallery,
            'photos': photos,
            'css_class': css_class,
        }
    except GallerySet.DoesNotExist:
        return {
            'gallery': None, 
            'photos': [],
            'css_class': css_class,
        }