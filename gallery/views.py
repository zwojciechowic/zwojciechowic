# gallery/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Gallery

def gallery_widget(request, gallery_id):
    """Widok do wyświetlania galerii jako widget (jeśli potrzebny)"""
    gallery = get_object_or_404(Gallery, id=gallery_id, is_active=True)
    photos = gallery.photos.all()
    
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