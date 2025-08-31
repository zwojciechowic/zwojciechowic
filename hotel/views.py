from django.shortcuts import render, redirect
from django.contrib import messages
from gallery.models import Gallery
from .models import Booking, FAQ
from .forms import BookingForm

def hotel_home(request):
    gallery = Gallery.objects.filter(title__icontains='hotel').first()
    if not gallery:
        gallery = Gallery.objects.first()
    
    faqs = FAQ.objects.all()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rezerwacja została wysłana!')
            return redirect('hotel:home')
    else:
        form = BookingForm()
    
    context = {
        'gallery': gallery,
        'photos': gallery.photos.all() if gallery else [],
        'form': form,
        'faqs': faqs,
    }
    
    return render(request, 'hotel/home.html', context)