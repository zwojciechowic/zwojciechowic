from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Gallery

def gallery_widget(request, gallery_id):
    """Widok do wyświetlania galerii jako widget"""
    gallery = get_object_or_404(Gallery, id=gallery_id)
    media_files = gallery.media_files.all()
    
    context = {
        'gallery': gallery,
        'media_files': media_files,
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'media_files': [
                {
                    'id': media.id,
                    'url': media.file.url,
                    'media_type': media.media_type,
                    'order': media.order,
                    'thumbnail_url': media.thumbnail.url if media.thumbnail else None,
                } for media in media_files
            ]
        })
    
    return render(request, 'gallery/widget.html', context)