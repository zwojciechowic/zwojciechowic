# gallery/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import GallerySet

def gallery_widget(request, gallery_id):
    """Widok do wyświetlania galerii jako widget (jeśli potrzebny)"""
    gallery = get_object_or_404(GallerySet, id=gallery_id, is_active=True)
    photos = gallery.get_photos()
    
    context = {
        'gallery': gallery,
        'photos': photos,
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'photos': [
                {
                    'id': photo.id,
                    'url': photo.image.url,
                    'order': photo.order
                } for photo in photos
            ]
        })
    
    return render(request, 'gallery/widget.html', context)