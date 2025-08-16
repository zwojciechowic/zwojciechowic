# models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class BlogPost(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Tytuł')),
        excerpt = models.TextField(max_length=300, blank=True, verbose_name=_('Krótki opis')),
    )
    
    slug = models.SlugField(unique=True, verbose_name=_('URL (slug)'))
    photo_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Galeria zdjęć'),
        related_name='blog_posts'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Autor'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Data utworzenia'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Data aktualizacji'))
    is_published = models.BooleanField(default=True, verbose_name=_('Opublikowane'))
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Wpis na blogu')
        verbose_name_plural = _('Wpisy na blogu')
    
    def __str__(self):
        try:
            title = self.safe_translation_getter('title', any_language=True)
            if title:
                return str(title)
        except:
            pass
        return f"Blog Post #{self.pk}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            title = self.safe_translation_getter('title', any_language=True)
            if title:
                base_slug = slugify(title)
                slug = base_slug
                counter = 1
                while BlogPost.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)
    
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
            f"<h3>{section.safe_translation_getter('title', any_language=True) or ''}</h3>\n{section.safe_translation_getter('content', any_language=True) or ''}" 
            if section.safe_translation_getter('title', any_language=True)
            else section.safe_translation_getter('content', any_language=True) or ''
            for section in self.sections.all()
        ])

class BlogSection(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_("Tytuł sekcji"), max_length=200, blank=True),
        content = models.TextField(_("Treść sekcji")),
    )
    
    blog_post = models.ForeignKey(
        BlogPost, 
        on_delete=models.CASCADE, 
        related_name='sections', 
        verbose_name=_('Wpis na blogu')
    )
    order = models.PositiveIntegerField(_("Kolejność"), default=0)
    
    class Meta:
        ordering = ('order',)
        verbose_name = _("Sekcja wpisu")
        verbose_name_plural = _("Sekcje wpisu")
    
    def __str__(self):
        try:
            blog_title = self.blog_post.safe_translation_getter('title', any_language=True)
            section_title = self.safe_translation_getter('title', any_language=True)
            
            if blog_title and section_title:
                return f"{blog_title} - {section_title}"
            elif blog_title:
                return f"{blog_title} - Sekcja {self.order}"
        except:
            pass
        
        return f"Sekcja #{self.order}"
    
class Dog(TranslatableModel):
    translations = TranslatedFields(
        breed = models.CharField(max_length=100, verbose_name=_('Rasa')),
        description = models.TextField(verbose_name=_('Opis'))
    )
    name = models.CharField(max_length=100, verbose_name=_('Imię'))
    gender = models.CharField(
        max_length=10, 
        choices=[('male', _('Pies')), ('female', _('Suka'))], 
        verbose_name=_('Płeć')
    )
    birth_date = models.DateField(verbose_name=_('Data urodzenia'))
    is_breeding = models.BooleanField(default=False, verbose_name=_('Pies hodowlany'))
    photo_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Galeria zdjęć'),
        related_name='dog_photos'
    )
    certificates_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Galeria certyfikatów'),
        related_name='dog_certificates'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Pies')
        verbose_name_plural = _('Psy')
    
    def __str__(self):
        return self.name
    
    @property
    def main_photo(self):
        if self.photo_gallery:
            return self.photo_gallery.photos.first()
        return None

class Puppy(TranslatableModel):
    translations = TranslatedFields(
        breed = models.CharField(max_length=100, verbose_name=_('Rasa')),
        description = models.TextField(blank=True, verbose_name=_('Opis'))
    )
    
    name = models.CharField(max_length=100, verbose_name=_('Imię'))
    mother_name = models.CharField(
        max_length=100, 
        verbose_name=_('Matka'), 
        blank=True,
        help_text=_('Imię matki - tylko do wyświetlania')
    )
    father_name = models.CharField(
        max_length=100, 
        verbose_name=_('Ojciec'), 
        blank=True,
        help_text=_('Imię ojca - tylko do wyświetlania')
    )
    
    litter = models.CharField(max_length=1, verbose_name=_('Miot'), default='A', help_text=_('Jedna litera oznaczająca miot (A, B, C...)'))
    
    color1 = ColorField(
        default='#FFFFFF',
        verbose_name=_('Kolor 1'),
        help_text=_('Pierwszy kolor')
    )
    color2 = ColorField(
        default='#FFFFFF',
        verbose_name=_('Kolor 2'),
        blank=True,
        help_text=_('Drugi kolor (opcjonalny)')
    )
    
    birth_date = models.DateField(verbose_name=_('Data urodzenia'))
    gender = models.CharField(
        max_length=10, 
        choices=[('male', _('Pies')), ('female', _('Suka'))], 
        verbose_name=_('Płeć')
    )
    photo_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Galeria zdjęć'),
        related_name='puppy_photos'
    )
    certificates_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Galeria certyfikatów'),
        related_name='puppy_certificates'
    )
    is_available = models.BooleanField(default=True, verbose_name=_('Dostępne'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Cena'))
    
    class Meta:
        ordering = ['litter']
        verbose_name = _('Szczeniak')
        verbose_name_plural = _('Szczeniaki')
    
    def __str__(self):
        parent_info = ""
        if self.mother_name and self.father_name:
            parent_info = f" ({self.mother_name} x {self.father_name})"
        elif self.mother_name:
            parent_info = f" (matka: {self.mother_name})"
        elif self.father_name:
            parent_info = f" (ojciec: {self.father_name})"
        
        color_info = ""
        if self.color1:
            color_info = f" - {self.color1}"
            if self.color2:
                color_info += f"/{self.color2}"
        
        return f"{self.litter}-{self.name} - {self.get_gender_display()}{color_info}{parent_info}"
    
    @property
    def main_photo(self):
        if self.photo_gallery:
            return self.photo_gallery.photos.first()
        return None
    
    @property
    def color_display(self):
        if self.color1 and self.color2:
            return f"{self.color1}/{self.color2}"
        elif self.color1:
            return self.color1
        return "Nie określono"

class Reservation(models.Model):
    puppy = models.ForeignKey(Puppy, on_delete=models.CASCADE, verbose_name=_('Szczeniak'))
    customer_name = models.CharField(max_length=100, verbose_name=_('Imię i nazwisko'))
    customer_email = models.EmailField(verbose_name='Email')
    customer_phone = models.CharField(max_length=20, verbose_name=_('Telefon'))
    message = models.TextField(blank=True, verbose_name=_('Wiadomość'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Data zgłoszenia'))
    status = models.CharField(max_length=20, choices=[
        ('pending', _('Oczekuje')),
        ('confirmed', _('Potwierdzone')),
        ('cancelled', _('Anulowane'))
    ], default='pending', verbose_name='Status')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Rezerwacja')
        verbose_name_plural = _('Rezerwacje')
    
    def __str__(self):
        return f"Rezerwacja: {self.puppy.name} - {self.customer_name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Imię i nazwisko'))
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Telefon'))
    subject = models.CharField(max_length=200, verbose_name=_('Temat'))
    message = models.TextField(verbose_name=_('Wiadomość'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Data wysłania'))
    is_read = models.BooleanField(default=False, verbose_name=_('Przeczytane'))
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wiadomość kontaktowa'
        verbose_name_plural = 'Wiadomości kontaktowe'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class AboutPage(TranslatableModel):
    translations = TranslatedFields(
        main_title = models.CharField(_("Główny tytuł"), max_length=200),
        quote_text = models.TextField(_("Tekst cytatu"), blank=True),
    )
    
    top_image = models.ImageField(
        _("Zdjęcie główne"), 
        upload_to='about/',
        blank=True
    )
    certificates_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Galeria certyfikatów'),
        related_name='about_certificates',
        help_text=_('Certyfikaty hodowli, nagrody, dyplomy itp.')
    )

    class Meta:
        verbose_name = _("Strona O nas")
        verbose_name_plural = _("Strona O nas")

    def __str__(self):
        # Próbuj pobrać przetłumaczony tytuł
        try:
            title = self.safe_translation_getter('main_title', any_language=True)
            if title:
                return str(title)
        except:
            pass
        
        # Fallback do zwykłego stringa
        return "Strona O nas"


class AboutSections(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_("Nagłówek H3"), max_length=200, blank=True),
        content = models.TextField(_("Treść paragrafu")),
    )
    
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    order = models.PositiveIntegerField(_("Kolejność"), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _("Sekcja")
        verbose_name_plural = _("Sekcje")

    def __str__(self):
        try:
            title = self.safe_translation_getter('title', any_language=True)
            if title:
                return f"{str(title)} (#{self.order})"
        except:
            pass
        
        # Fallback do zwykłego stringa
        return f"Sekcja {self.order}"
    translations = TranslatedFields(
        title = models.CharField(_("Nagłówek H3"), max_length=200, blank=True),
        content = models.TextField(_("Treść paragrafu")),
    )
    
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    order = models.PositiveIntegerField(_("Kolejność"), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _("Sekcja")
        verbose_name_plural = _("Sekcje")

    def __str__(self):
        title = self.safe_translation_getter('title', any_language=True)
        if title:
            return f"{title} (#{self.order})"
        return f"Sekcja {self.order}"
    translations = TranslatedFields(
        title = models.CharField(_("Nagłówek H3"), max_length=200, blank=True),
        content = models.TextField(_("Treść paragrafu")),
    )
    
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    order = models.PositiveIntegerField(_("Kolejność"), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _("Sekcja")
        verbose_name_plural = _("Sekcje")

    def __str__(self):
        return _("Sekcja %(order)s") % {'order': self.order}