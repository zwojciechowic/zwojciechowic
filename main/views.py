# main/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.paginator import Paginator
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage, AboutPage
from .forms import ReservationForm, ContactForm, PuppyReservationForm
from django.db.models import Count
from collections import OrderedDict
from collections import defaultdict
from django.db.models import Count, Q

def home(request):
    """Strona główna z najnowszymi wpisami, psami i szczeniakami"""
    # Pobierz najnowsze wpisy blogowe
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # Pobierz wybrane psy hodowlane
    featured_dogs = Dog.objects.filter(is_breeding=True)[:2]
    
    # Pobierz dostępne szczenięta (maksymalnie 3)
    available_puppies = Puppy.objects.filter(is_available=True).order_by('litter', 'name')[:3]
    
    context = {
        'latest_posts': latest_posts,
        'featured_dogs': featured_dogs,
        'available_puppies': available_puppies,
        'page_obj': latest_posts,  # Dla kompatybilności z szablonem
    }
    
    return render(request, 'index.html', context)
def blog_detail(request, slug):
    """Szczegóły wpisu na blogu z nawigacją karuzeli (pętla)"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Pobierz wszystkie opublikowane wpisy w kolejności chronologicznej
    all_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    # Znajdź indeks aktualnego wpisu
    current_index = None
    for i, p in enumerate(all_posts):
        if p.id == post.id:
            current_index = i
            break
    
    # Logika karuzeli - jeśli jesteśmy na końcu, idź na początek i odwrotnie
    if current_index is not None:
        total_posts = len(all_posts)
        
        # Poprzedni wpis (z pętlą)
        prev_index = (current_index - 1) % total_posts
        previous_post = all_posts[prev_index]
        
        # Następny wpis (z pętlą) 
        next_index = (current_index + 1) % total_posts
        next_post = all_posts[next_index]
    else:
        # Fallback gdyby coś poszło nie tak
        previous_post = None
        next_post = None
    
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
    }
    
    return render(request, 'blog_detail.html', context)
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
    """Strona szczeniaki z grupowaniem po miotach"""
    all_puppies = Puppy.objects.all().order_by('litter', 'name')
    
    # Grupowanie szczeniąt po miotach
    puppies_by_litter = defaultdict(lambda: {
        'puppies': [],
        'total_count': 0,
        'available_count': 0
    })
    
    for puppy in all_puppies:
        puppies_by_litter[puppy.litter]['puppies'].append(puppy)
        puppies_by_litter[puppy.litter]['total_count'] += 1
        if puppy.is_available:
            puppies_by_litter[puppy.litter]['available_count'] += 1
    
    # Sortowanie miotów alfabetycznie
    puppies_by_litter = dict(sorted(puppies_by_litter.items()))
    
    return render(request, 'puppies.html', {
        'puppies_by_litter': puppies_by_litter,
        'favicon': 'logo/puppy-logo.ico',
        'favicon_png': 'logo/puppy-logo.png'
    })
def puppy_detail(request, pk):
    """Szczegółowa strona szczenięcia z formularzem rezerwacji"""
    puppy = get_object_or_404(Puppy, pk=pk)
    
    # Pobierz innych szczeniąt z tego samego miotu
    litter_siblings = Puppy.objects.filter(
        litter=puppy.litter, 
        is_available=True
    ).exclude(pk=puppy.pk).order_by('name')
    
    if request.method == 'POST' and puppy.is_available:
        form = PuppyReservationForm(request.POST)
        if form.is_valid():
            # Zapisz rezerwację do bazy danych
            reservation = form.save(commit=False)
            reservation.puppy = puppy
            reservation.message = f"Rezerwacja złożona przez formularz na stronie szczenięcia {puppy.name}"
            reservation.save()
            
            # Przygotuj dane do e-maila
            customer_name = form.cleaned_data['customer_name']
            customer_email = form.cleaned_data['customer_email']
            customer_phone = form.cleaned_data['customer_phone']
            
            # Wyślij e-mail z powiadomieniem o rezerwacji
            email_subject = f"Nowa rezerwacja szczenięcia: {puppy.name} z miotu {puppy.litter}"
            email_message = f"""Nowa rezerwacja szczenięcia została złożona:

SZCZENIAK:
Imię: {puppy.name}
Miot: {puppy.litter}
Płeć: {puppy.get_gender_display()}
Cena: {puppy.price} zł
Rodzice: {puppy.mother_name} x {puppy.father_name}

DANE KLIENTA:
Imię i nazwisko: {customer_name}
E-mail: {customer_email}
Telefon: {customer_phone}

---
Rezerwacja została automatycznie zapisana w systemie.
ID rezerwacji: {reservation.id}
Data złożenia: {reservation.created_at.strftime('%d.%m.%Y %H:%M')}

Aby potwierdzić lub odrzucić rezerwację, zaloguj się do panelu administracyjnego.
"""
            
            try:
                from django.core.mail import EmailMessage
                from django.conf import settings
                
                email = EmailMessage(
                    subject=email_subject,
                    body=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=['zwojciechowic@gmail.com'],
                )
                email.send()
                
                messages.success(request, f'Rezerwacja szczenięcia {puppy.name} z miotu {puppy.litter} została wysłana pomyślnie! Skontaktujemy się z Tobą wkrótce.')
                
            except Exception as e:
                messages.warning(request, f'Rezerwacja została zapisana, ale wystąpił problem z wysyłką e-maila. Skontaktujemy się z Tobą wkrótce.')
                print(f"Błąd wysyłania e-maila rezerwacji: {e}")
            
            return redirect('puppy_detail', pk=puppy.pk)
    else:
        form = PuppyReservationForm()
    
    return render(request, 'puppy_detail.html', {
        'puppy': puppy,
        'form': form,
        'litter_siblings': litter_siblings
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
            
            # ZAPISZ WIADOMOŚĆ DO BAZY DANYCH
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                is_read=False  # Domyślnie jako nieprzeczytana
            )
            
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
ID wiadomości w systemie: {contact_message.id}
"""
            
            try:
                email_obj = EmailMessage(
                    subject=email_subject,
                    body=email_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=['zwojciechowic@gmail.com'],
                )
                email_obj.send()
                
                messages.success(request, 'Wiadomość została wysłana pomyślnie!')
                return redirect('contact')
                
            except Exception as e:
                # Nawet jeśli wysyłka maila się nie powiedzie, wiadomość jest już zapisana w bazie
                messages.warning(request, 'Wiadomość została zapisana, ale wystąpił problem z wysyłką e-maila. Skontaktujemy się z Tobą wkrótce.')
                print(f"Błąd wysyłania e-maila: {e}")
                return redirect('contact')
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