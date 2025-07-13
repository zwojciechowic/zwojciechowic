from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage
from .forms import ReservationForm, ContactForm

def home(request):
    """Strona główna z blogami"""
    posts = BlogPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 6)  # 6 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Najnowsze szczeniaki dla sekcji "Dostępne szczenięta"
    available_puppies = Puppy.objects.filter(is_available=True)[:3]
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'available_puppies': available_puppies
    })

def blog_detail(request, slug):
    """Szczegóły wpisu na blogu"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'blog_detail.html', {'post': post})

def about(request):
    """Strona o nas"""
    return render(request, 'about.html')

def dogs(request):
    """Strona nasze psy"""
    breeding_dogs = Dog.objects.filter(is_breeding=True)
    other_dogs = Dog.objects.filter(is_breeding=False)
    return render(request, 'dogs.html', {
        'breeding_dogs': breeding_dogs,
        'other_dogs': other_dogs
    })

def puppies(request):
    """Strona szczeniaki"""
    available_puppies = Puppy.objects.filter(is_available=True)
    return render(request, 'puppies.html', {
        'puppies': available_puppies,
        'favicon': 'logo/puppy-logo.ico'
    })

def reservations(request):
    """Strona rezerwacji"""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rezerwacja została wysłana pomyślnie!')
            return redirect('reservations')
    else:
        form = ReservationForm()
    
    available_puppies = Puppy.objects.filter(is_available=True)
    return render(request, 'reservations.html', {
        'form': form,
        'available_puppies': available_puppies
    })

def contact(request):
    """Strona kontakt"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wiadomość została wysłana pomyślnie!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})