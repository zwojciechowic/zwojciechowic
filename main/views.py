# main/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.paginator import Paginator
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage, AboutPage
from .forms import ReservationForm, ContactForm, PuppyReservationForm

def home(request):
    """Strona główna z blogami"""
    posts = BlogPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 6)  # 6 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Najnowsze szczeniaki dla sekcji "Dostępne szczenięta"
    available_puppies = Puppy.objects.filter(is_available=True)[:3]

    featured_dogs = Dog.objects.filter(is_breeding=True)[:2]
    
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'available_puppies': available_puppies,
        'featured_dogs': featured_dogs
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

def dog_detail(request, pk):
    """Szczegółowa strona psa"""
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'dog_detail.html', {
        'dog': dog
    })

def puppies(request):
    """Strona szczeniaki"""
    available_puppies = Puppy.objects.filter(is_available=True)
    return render(request, 'puppies.html', {
        'puppies': available_puppies,
        'favicon': 'logo/puppy-logo.ico',
        'favicon_png': 'logo/puppy-logo.png'
    })

def puppy_detail(request, pk):
    """Szczegółowa strona szczenięcia z formularzem rezerwacji"""
    puppy = get_object_or_404(Puppy, pk=pk)
    
    if request.method == 'POST' and puppy.is_available:
        form = PuppyReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.puppy = puppy
            reservation.save()
            messages.success(request, f'Rezerwacja szczenięcia {puppy.name} została wysłana pomyślnie!')
            return redirect('puppy_detail', pk=puppy.pk)
    else:
        form = PuppyReservationForm()
    
    return render(request, 'puppy_detail.html', {
        'puppy': puppy,
        'form': form
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

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Pobierz dane z formularza
            name = form.cleaned_data['name'].strip()
            email = form.cleaned_data['email'].strip()
            phone = form.cleaned_data['phone'].strip() if form.cleaned_data['phone'] else ''
            subject = form.cleaned_data['subject'].strip()
            message = form.cleaned_data['message'].strip()
            
            # Przygotuj treść e-maila
            email_subject = f"Nowa wiadomość z formularza kontaktowego: {subject}"
            email_message = f"""Nowa wiadomość z formularza kontaktowego na stronie hodowli:

                Imię i nazwisko: {name}
                Email: {email}
                Telefon: {phone if phone else 'Nie podano'}
                Temat: {subject}

                Wiadomość:
                {message}

                ---
                Ta wiadomość została wysłana automatycznie z formularza kontaktowego.
                """
            
            try:
                email = EmailMessage(
                    subject=email_subject,
                    body=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=['zwojciechowic@gmail.com'],
                )
                email.send()
                
                messages.success(request, 'Wiadomość została wysłana pomyślnie!')
                return redirect('contact')
                
            except Exception as e:
                messages.error(request, 'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.')
                print(f"Błąd wysyłania e-maila: {e}")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def about(request):
    about_page = AboutPage.objects.first()
    return render(request, 'about.html', {'about': about_page})

def admin_dashboard_context(request):
    """Context processor dla dashboard admin"""
    if request.path.startswith('/admin/'):
        return {
            'dogs_count': Dog.objects.count(),
            'puppies_count': Puppy.objects.filter(is_available=True).count(),
            'reservations_count': Reservation.objects.filter(status='pending').count(),
            'posts_count': BlogPost.objects.filter(is_published=True).count(),
            'about_exists': AboutPage.objects.exists(),
        }
    return {}

def hotel(request):
    """Strona hotelu - już wkrótce"""
    return render(request, 'hotel.html')

def handle_additional_photos_upload(request, instance):
    """
    Obsługuje upload dodatkowych zdjęć z formularza administracyjnego
    """
    uploaded_files = request.FILES.getlist('additional_photos_files')
    additional_photos_data = request.POST.get('additional_photos_data', '[]')
    
    try:
        photos_data = json.loads(additional_photos_data)
    except (json.JSONDecodeError, TypeError):
        photos_data = []
    
    # Obsługa nowych plików
    for file in uploaded_files:
        if file.content_type.startswith('image/'):
            # Zapisz plik
            filename = f"additional_photos/{instance._meta.model_name}_{instance.pk}_{file.name}"
            saved_file = default_storage.save(filename, ContentFile(file.read()))
            
            # Dodaj do danych
            photos_data.append({
                'url': default_storage.url(saved_file),
                'order': len(photos_data) + 1,
                'filename': saved_file
            })
    
    # Sortuj według kolejności
    photos_data.sort(key=lambda x: x.get('order', 0))
    
    return photos_data

# Alternatywnie - dodaj do admin.py w metodzie save_model bardziej zaawansowaną obsługę:

def save_model(self, request, obj, form, change):
    # Najpierw zapisz obiekt
    super().save_model(request, obj, form, change)
    
    # Obsługa dodatkowych zdjęć
    additional_photos_data = request.POST.get('additional_photos_data')
    if additional_photos_data:
        try:
            import json
            photos_data = json.loads(additional_photos_data)
            
            # Sprawdź czy są nowe pliki do uploadu
            uploaded_files = request.FILES.getlist('additional_photos_files')
            for file in uploaded_files:
                if file.content_type.startswith('image/'):
                    # Zapisz plik do odpowiedniego katalogu
                    from django.core.files.storage import default_storage
                    from django.core.files.base import ContentFile
                    import uuid
                    
                    filename = f"additional_photos/{obj._meta.model_name}_{obj.pk}_{uuid.uuid4().hex[:8]}_{file.name}"
                    saved_file = default_storage.save(filename, ContentFile(file.read()))
                    
                    # Dodaj do photos_data
                    photos_data.append({
                        'url': default_storage.url(saved_file),
                        'order': len(photos_data) + 1,
                        'filename': saved_file
                    })
            
            # Sortuj i zapisz
            photos_data.sort(key=lambda x: x.get('order', 0))
            obj.additional_photos = photos_data
            obj.save(update_fields=['additional_photos'])
            
        except (json.JSONDecodeError, TypeError):
            pass