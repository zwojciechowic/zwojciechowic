from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Gallery, Photo

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

def gallery_widget(request, gallery_id):
    """Widok do wyświetlania galerii jako widget (jeśli potrzebny)"""
    gallery = get_object_or_404(Gallery, id=gallery_id)
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
                    'media_type': photo.media_type,
                    'order': photo.order
                } for photo in photos
            ]
        })
    
    return render(request, 'gallery/widget.html', context)


@staff_member_required
@require_POST
def admin_adjust_photo_position(request, photo_id, direction):
    photo = get_object_or_404(Photo, id=photo_id)
    current_pos = photo.vertical_position or 50
    
    if direction == 'up':
        photo.vertical_position = max(0, current_pos - 15)
    else:
        photo.vertical_position = min(100, current_pos + 15)
    
    photo.save()
    return JsonResponse({'success': True, 'position': photo.vertical_position})