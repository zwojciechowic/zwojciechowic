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
import random

def home(request):
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    featured_dogs = Dog.objects.filter(is_breeding=True).order_by('name')[:2]
    
    puppies_by_litter = defaultdict(list)
    available_puppies_all = Puppy.objects.filter(is_available=True).select_related('mother', 'father', 'photo_gallery')

    for puppy in available_puppies_all:
        puppies_by_litter[puppy.litter].append(puppy)

    selected_puppies = []
    litter_keys = list(puppies_by_litter.keys())
    random.shuffle(litter_keys)

    for litter in litter_keys[:3]:
        puppies_in_litter = puppies_by_litter[litter]
        selected_puppy = random.choice(puppies_in_litter)
        selected_puppies.append(selected_puppy)

    if len(selected_puppies) < 3:
        remaining_puppies = [p for p in available_puppies_all if p not in selected_puppies]
        additional_count = min(3 - len(selected_puppies), len(remaining_puppies))
        if additional_count > 0:
            additional_puppies = random.sample(remaining_puppies, additional_count)
            selected_puppies.extend(additional_puppies)
    
    context = {
        'latest_posts': latest_posts,
        'featured_dogs': featured_dogs,
        'available_puppies': selected_puppies,
        'page_obj': latest_posts,
    }
    
    return render(request, 'index.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    all_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    current_index = None
    for i, p in enumerate(all_posts):
        if p.id == post.id:
            current_index = i
            break
    
    if current_index is not None:
        total_posts = len(all_posts)
        
        prev_index = (current_index - 1) % total_posts
        previous_post = all_posts[prev_index]
        
        next_index = (current_index + 1) % total_posts
        next_post = all_posts[next_index]
    else:
        previous_post = None
        next_post = None
    
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
    }
    
    return render(request, 'blog_detail.html', context)

def about(request):
    return render(request, 'about.html')

def dogs(request):
    breeding_dogs = Dog.objects.filter(is_breeding=True).order_by('name')
    other_dogs = Dog.objects.filter(is_breeding=False).order_by('name')
    return render(request, 'dogs.html', {
        'breeding_dogs': breeding_dogs,
        'other_dogs': other_dogs
    })

def dog_detail(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'dog_detail.html', {
        'dog': dog
    })

def puppies(request):
    all_puppies = Puppy.objects.all().order_by('litter', 'name')
    
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
    
    puppies_by_litter = dict(sorted(puppies_by_litter.items()))
    
    return render(request, 'puppies.html', {
        'puppies_by_litter': puppies_by_litter,
        'favicon': 'logo/puppy-logo.ico',
        'favicon_png': 'logo/puppy-logo.png'
    })

def puppy_detail(request, pk):
    puppy = get_object_or_404(Puppy, pk=pk)
    
    litter_siblings = Puppy.objects.filter(
        litter=puppy.litter, 
        is_available=True
    ).exclude(pk=puppy.pk).order_by('name')
    
    if request.method == 'POST' and puppy.is_available:
        form = PuppyReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.puppy = puppy
            reservation.message = f"Rezerwacja złożona przez formularz na stronie szczenięcia {puppy.name}"
            reservation.save()
            
            customer_name = form.cleaned_data['customer_name']
            customer_email = form.cleaned_data['customer_email']
            customer_phone = form.cleaned_data['customer_phone']
            
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
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            
            message_text = form.cleaned_data.get('message', '').strip()
            if message_text:
                reservation.message = message_text
                reservation.save()
            
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
            contact_message = form.save()
            
            subject_text = form.cleaned_data.get('subject', '').strip()
            message_text = form.cleaned_data.get('message', '').strip()
            
            if subject_text:
                contact_message.subject = subject_text
            if message_text:
                contact_message.message = message_text
            
            contact_message.is_read = False
            contact_message.save()
            
            name = contact_message.name
            email = contact_message.email
            phone = contact_message.phone if contact_message.phone else 'Nie podano'
            
            email_subject = f"Nowa wiadomość z formularza kontaktowego: {subject_text}"
            email_message = f"""Nowa wiadomość z formularza kontaktowego na stronie hodowli:

Imię i nazwisko: {name}
Email: {email}
Telefon: {phone}
Temat: {subject_text}

Wiadomość:
{message_text}

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
                messages.warning(request, 'Wiadomość została zapisana, ale wystąpił problem z wysyłką e-maila. Skontaktujemy się z Tobą wkrótce.')
                print(f"Błąd wysyłania e-maila: {e}")
                return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def about(request):
    about_page = AboutPage.objects.first()
    return render(request, 'about.html', {'about': about_page})

def hotel(request):
    from hotel.views import hotel_home
    return hotel_home(request)