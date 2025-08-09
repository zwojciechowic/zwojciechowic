# models.py
from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.utils.translation import gettext_lazy as _

class BlogSection(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='sections', verbose_name='Wpis na blogu')
    title = models.CharField("Tytuł sekcji", max_length=200, blank=True)
    title_en = models.CharField("Tytuł sekcji (EN)", max_length=200, blank=True)
    content = models.TextField("Treść sekcji")
    content_en = models.TextField("Treść sekcji (EN)", blank=True)
    order = models.PositiveIntegerField("Kolejność", default=0)
    
    class Meta:
        ordering = ('order',)
        verbose_name = "Sekcja wpisu"
        verbose_name_plural = "Sekcje wpisu"
    
    def __str__(self):
        return f"{self.blog_post.title} - {self.title or 'Sekcja ' + str(self.order)}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tytuł')
    title_en = models.CharField(max_length=200, verbose_name='Tytuł (EN)', blank=True)
    slug = models.SlugField(unique=True, verbose_name='URL (slug)')
    slug_en = models.SlugField(unique=True, verbose_name='URL (slug) (EN)', blank=True)
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Krótki opis')
    excerpt_en = models.TextField(max_length=300, blank=True, verbose_name='Krótki opis (EN)')
    photo_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Galeria zdjęć',
        related_name='blog_posts'
    )
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
    
    def get_title(self, language='pl'):
        """Zwraca tytuł w odpowiednim języku"""
        if language == 'en' and self.title_en:
            return self.title_en
        return self.title
    
    def get_excerpt(self, language='pl'):
        """Zwraca excerpt w odpowiednim języku"""
        if language == 'en' and self.excerpt_en:
            return self.excerpt_en
        return self.excerpt
    
    @property
    def main_photo(self):
        """Pierwsze zdjęcie z galerii jako główne"""
        if self.photo_gallery:
            return self.photo_gallery.photos.first()
        return None
    
    @property
    def content(self):
        """Złączenie wszystkich sekcji w jedną treść dla kompatybilności wstecznej"""
        return "\n\n".join([
            f"<h3>{section.title}</h3>\n{section.content}" if section.title 
            else section.content 
            for section in self.sections.all()
        ])

class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Imię')
    breed = models.CharField(max_length=100, verbose_name='Rasa')
    birth_date = models.DateField(verbose_name='Data urodzenia')
    gender = models.CharField(max_length=10, choices=[('male', 'Pies'), ('female', 'Suka')], verbose_name='Płeć')
    description = models.TextField(verbose_name='Opis')
    description_en = models.TextField(verbose_name='Opis (EN)', blank=True)
    photo_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Galeria zdjęć',
        related_name='dog_photos'
    )
    certificates_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Galeria certyfikatów',
        related_name='dog_certificates'
    )
    is_breeding = models.BooleanField(default=False, verbose_name='Pies hodowlany')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Pies'
        verbose_name_plural = 'Psy'
    
    def __str__(self):
        return self.name
    
    def get_description(self, language='pl'):
        """Zwraca opis w odpowiednim języku"""
        if language == 'en' and self.description_en:
            return self.description_en
        return self.description
    
    @property
    def main_photo(self):
        """Pierwsze zdjęcie z galerii jako główne"""
        if self.photo_gallery:
            return self.photo_gallery.photos.first()
        return None

class Puppy(models.Model):
    name = models.CharField(max_length=100, verbose_name='Imię')
    litter = models.CharField(max_length=1, verbose_name='Miot', default='A', help_text='Jedna litera oznaczająca miot (A, B, C...)')
    
    # Pola kolorów - hex values dla color pickera
    color1 = ColorField(
        default='#FFFFFF',
        verbose_name='Kolor 1',
        help_text='Pierwszy kolor'
    )
    color2 = ColorField(
        default='#FFFFFF',
        verbose_name='Kolor 2',
        blank=True,
        help_text='Drugi kolor (opcjonalny)'
    )
    
    # Pola mother i father jako zwykłe pola tekstowe zamiast ForeignKey
    mother_name = models.CharField(
        max_length=100, 
        verbose_name='Matka', 
        blank=True,
        help_text='Imię matki - tylko do wyświetlania'
    )
    father_name = models.CharField(
        max_length=100, 
        verbose_name='Ojciec', 
        blank=True,
        help_text='Imię ojca - tylko do wyświetlania'
    )
    
    birth_date = models.DateField(verbose_name='Data urodzenia')
    gender = models.CharField(max_length=10, choices=[('male', 'Pies'), ('female', 'Suka')], verbose_name='Płeć')
    description = models.TextField(blank=True, verbose_name='Opis')
    description_en = models.TextField(blank=True, verbose_name='Opis (EN)')
    photo_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Galeria zdjęć',
        related_name='puppy_photos'
    )
    certificates_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Galeria certyfikatów',
        related_name='puppy_certificates'
    )
    is_available = models.BooleanField(default=True, verbose_name='Dostępne')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cena')
    
    class Meta:
        ordering = ['litter', 'name']
        verbose_name = 'Szczeniak'
        verbose_name_plural = 'Szczeniaki'
    
    def __str__(self):
        parent_info = ""
        if self.mother_name and self.father_name:
            parent_info = f" ({self.mother_name} x {self.father_name})"
        elif self.mother_name:
            parent_info = f" (matka: {self.mother_name})"
        elif self.father_name:
            parent_info = f" (ojciec: {self.father_name})"
        
        # Dodanie informacji o kolorach do wyświetlania
        color_info = ""
        if self.color1:
            color_info = f" - {self.color1}"
            if self.color2:
                color_info += f"/{self.color2}"
        
        return f"{self.litter}-{self.name} - {self.get_gender_display()}{color_info}{parent_info}"
    
    def get_description(self, language='pl'):
        """Zwraca opis w odpowiednim języku"""
        if language == 'en' and self.description_en:
            return self.description_en
        return self.description
    
    @property
    def main_photo(self):
        """Pierwsze zdjęcie z galerii jako główne"""
        if self.photo_gallery:
            return self.photo_gallery.photos.first()
        return None
    
    @property
    def color_display(self):
        """Wyświetlanie kolorów w czytelnej formie"""
        if self.color1 and self.color2:
            return f"{self.color1}/{self.color2}"
        elif self.color1:
            return self.color1
        return "Nie określono"

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

class AboutPage(models.Model):
    main_title = models.CharField("Główny tytuł", max_length=200)
    main_title_en = models.CharField("Główny tytuł (EN)", max_length=200, blank=True)
    quote_text = models.TextField("Tekst cytatu", blank=True)
    quote_text_en = models.TextField("Tekst cytatu (EN)", blank=True)
    top_image = models.ImageField(
        "Zdjęcie główne", 
        upload_to='about/',
        blank=True
    )
    certificates_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Galeria certyfikatów',
        related_name='about_certificates',
        help_text='Certyfikaty hodowli, nagrody, dyplomy itp.'
    )

    class Meta:
        verbose_name = "Strona O nas"
        verbose_name_plural = "Strona O nas"

    def __str__(self):
        return "Strona 'O nas'"
    
    def get_main_title(self, language='pl'):
        """Zwraca główny tytuł w odpowiednim języku"""
        if language == 'en' and self.main_title_en:
            return self.main_title_en
        return self.main_title
    
    def get_quote_text(self, language='pl'):
        """Zwraca tekst cytatu w odpowiednim języku"""
        if language == 'en' and self.quote_text_en:
            return self.quote_text_en
        return self.quote_text

class AboutSections(models.Model):
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    title = models.CharField("Nagłówek H3", max_length=200, blank=True)
    title_en = models.CharField("Nagłówek H3 (EN)", max_length=200, blank=True)
    content = models.TextField("Treść paragrafu")
    content_en = models.TextField("Treść paragrafu (EN)", blank=True)
    order = models.PositiveIntegerField("Kolejność", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Sekcja"
        verbose_name_plural = "Sekcje"

    def __str__(self):
        return f"Sekcja {self.order}"
    
    def get_title(self, language='pl'):
        """Zwraca tytuł w odpowiednim języku"""
        if language == 'en' and self.title_en:
            return self.title_en
        return self.title
    
    def get_content(self, language='pl'):
        """Zwraca treść w odpowiednim języku"""
        if language == 'en' and self.content_en:
            return self.content_en
        return self.content