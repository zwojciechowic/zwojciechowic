from django import template
from django.utils.safestring import mark_safe
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
        return {'gallery': None, 'photos': []}

@register.simple_tag
def gallery_by_name(name, css_class=''):
    """Template tag do wstawienia galerii po nazwie"""
    try:
        gallery = GallerySet.objects.get(name=name, is_active=True)
        photos = gallery.get_photos()
        return mark_safe(f'''
            <div class="gallery-widget {css_class}" data-gallery-id="{gallery.id}">
                <!-- Galeria będzie załadowana przez JavaScript -->
            </div>
        ''')
    except GallerySet.DoesNotExist:
        return ''