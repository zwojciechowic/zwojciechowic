from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.paginator import Paginator
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage, AboutPage
from .forms import ReservationForm, ContactForm

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