from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tytuł')
    slug = models.SlugField(unique=True, verbose_name='URL (slug)')
    content = models.TextField(verbose_name='Treść')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Krótki opis')
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name='Zdjęcie główne')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data utworzenia')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')
    is_published = models.BooleanField(default=True, verbose_name='Opublikowane')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wpis na blogu'
        verbose_name_plural = 'Wpisy na blogu'
    
    def __str__(self):
        return self.title

class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Imię')
    breed = models.CharField(max_length=100, verbose_name='Rasa')
    birth_date = models.DateField(verbose_name='Data urodzenia')
    gender = models.CharField(max_length=10, choices=[('male', 'Pies'), ('female', 'Suka')], verbose_name='Płeć')
    description = models.TextField(verbose_name='Opis')
    photo = models.ImageField(upload_to='dogs/', verbose_name='Zdjęcie')
    is_breeding = models.BooleanField(default=False, verbose_name='Pies hodowlany')
    certificate = models.ImageField(upload_to='certificates/', blank=True, null=True, verbose_name='Certyfikat')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Pies'
        verbose_name_plural = 'Psy'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dog_detail', kwargs={'pk': self.pk})

class Puppy(models.Model):
    name = models.CharField(max_length=100, verbose_name='Imię')
    mother = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='puppies_as_mother', verbose_name='Matka')
    father = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='puppies_as_father', verbose_name='Ojciec')
    birth_date = models.DateField(verbose_name='Data urodzenia')
    gender = models.CharField(max_length=10, choices=[('male', 'Pies'), ('female', 'Suka')], verbose_name='Płeć')
    description = models.TextField(blank=True, verbose_name='Opis')
    photo = models.ImageField(upload_to='puppies/', verbose_name='Zdjęcie')
    is_available = models.BooleanField(default=True, verbose_name='Dostępne')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena')
    
    class Meta:
        ordering = ['-birth_date']
        verbose_name = 'Szczeniak'
        verbose_name_plural = 'Szczeniaki'
    
    def __str__(self):
        return f"{self.name} - {self.get_gender_display()}"

class Reservation(models.Model):
    puppy = models.ForeignKey(Puppy, on_delete=models.CASCADE, verbose_name='Szczeniak')
    customer_name = models.CharField(max_length=100, verbose_name='Imię i nazwisko')
    customer_email = models.EmailField(verbose_name='Email')
    customer_phone = models.CharField(max_length=20, verbose_name='Telefon')
    message = models.TextField(blank=True, verbose_name='Wiadomość')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data zgłoszenia')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Oczekuje'),
        ('confirmed', 'Potwierdzone'),
        ('cancelled', 'Anulowane')
    ], default='pending', verbose_name='Status')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rezerwacja'
        verbose_name_plural = 'Rezerwacje'
    
    def __str__(self):
        return f"Rezerwacja: {self.puppy.name} - {self.customer_name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Imię i nazwisko')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    subject = models.CharField(max_length=200, verbose_name='Temat')
    message = models.TextField(verbose_name='Wiadomość')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data wysłania')
    is_read = models.BooleanField(default=False, verbose_name='Przeczytane')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wiadomość kontaktowa'
        verbose_name_plural = 'Wiadomości kontaktowe'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
