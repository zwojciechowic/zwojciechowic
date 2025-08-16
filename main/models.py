# models.py
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class BlogPost(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(
            max_length=200, 
            verbose_name=_('Tytuł'),
            blank=True,
            help_text=_('Tytuł wpisu na blogu')
        ),
        excerpt=models.TextField(
            max_length=300, 
            blank=True, 
            verbose_name=_('Krótki opis'),
            help_text=_('Krótki opis wpisu wyświetlany na liście')
        ),
    )
    
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('URL (slug)'),
        help_text=_('URL przyjazny dla SEO (zostanie wygenerowany automatycznie jeśli pusty)')
    )
    photo_gallery = models.ForeignKey(
        'gallery.Gallery', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_('Galeria zdjęć'),
        related_name='blog_posts'
    )
    
    # NOWE POLE - powiązanie z psem
    related_dog = models.ForeignKey(
        'Dog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Powiązany pies'),
        help_text=_('Wybierz psa, którego dotyczy ten wpis'),
        related_name='blog_posts'
    )
    
    # NOWE POLE - powiązanie ze szczeniakiem
    related_puppy = models.ForeignKey(
        'Puppy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Powiązany szczeniak'),
        help_text=_('Wybierz szczeniaka, którego dotyczy ten wpis'),
        related_name='blog_posts'
    )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name=_('Autor')
    )
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Data aktualizacji')
    )
    is_published = models.BooleanField(
        default=True, 
        verbose_name=_('Opublikowane')
    )
    
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
        return f"Blog Post #{self.pk}" if self.pk else "Nowy wpis"
    
    def clean(self):
        """Walidacja modelu"""
        from django.core.exceptions import ValidationError
        from django.conf import settings
        
        # Sprawdź czy nie wybrano jednocześnie psa i szczeniaka
        if self.related_dog and self.related_puppy:
            raise ValidationError(_('Nie możesz wybrać jednocześnie psa i szczeniaka. Wybierz tylko jeden.'))
        
        # Sprawdź czy istnieje tytuł w jakimkolwiek języku
        if self.pk:  # Tylko dla istniejących obiektów
            has_title = False
            for lang_code, lang_name in settings.LANGUAGES:
                try:
                    translation = self.get_translation(lang_code)
                    if translation.title and translation.title.strip():
                        has_title = True
                        break
                except:
                    continue
            
            if not has_title:
                raise ValidationError(_('Wpis musi mieć tytuł w przynajmniej jednym języku'))
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            title = None
            try:
                title = self.safe_translation_getter('title', any_language=True)
            except:
                pass
            
            if title and title.strip():
                base_slug = slugify(title)
                if base_slug:  # Sprawdź czy slug nie jest pusty
                    slug = base_slug
                    counter = 1
                    while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    self.slug = slug
                else:
                    # Fallback slug jeśli title nie może być przekonwertowany na slug
                    import uuid
                    self.slug = f"post-{str(uuid.uuid4())[:8]}"
            else:
                # Fallback slug jeśli brak tytułu
                import uuid
                self.slug = f"post-{str(uuid.uuid4())[:8]}"
        
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
        sections = []
        for section in self.sections.all():
            section_title = section.safe_translation_getter('title', any_language=True)
            section_content = section.safe_translation_getter('content', any_language=True)
            
            if section_title and section_content:
                sections.append(f"<h3>{section_title}</h3>\n{section_content}")
            elif section_content:
                sections.append(section_content)
        
        return "\n\n".join(sections)
    
    @property
    def get_related_animal(self):
        """Zwraca powiązanego psa lub szczeniaka"""
        if self.related_dog:
            return self.related_dog
        elif self.related_puppy:
            return self.related_puppy
        return None
    
    @property
    def get_related_animal_type(self):
        """Zwraca typ powiązanego zwierzęcia"""
        if self.related_dog:
            return 'dog'
        elif self.related_puppy:
            return 'puppy'
        return None
    
class BlogSection(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(
            _("Tytuł sekcji"), 
            max_length=200, 
            blank=True,
            help_text=_('Opcjonalny tytuł sekcji')
        ),
        content=models.TextField(
            _("Treść sekcji"),
            blank=True,  # Dodano blank=True dla większej elastyczności
            help_text=_('Treść sekcji wpisu')
        ),
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
        unique_together = ['blog_post', 'order']  # Zapobiega duplikatom kolejności
    
    def __str__(self):
        try:
            blog_title = self.blog_post.safe_translation_getter('title', any_language=True)
            section_title = self.safe_translation_getter('title', any_language=True)
            
            if blog_title and section_title:
                return f"{blog_title} - {section_title}"
            elif blog_title:
                return f"{blog_title} - Sekcja {self.order + 1}"
            else:
                return f"Sekcja {self.order + 1}"
        except:
            return f"Sekcja #{self.order + 1}"  

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
    
    # ZMODYFIKOWANE POLA - relacje z psami + tekstowe alternatywy
    mother = models.ForeignKey(
        'Dog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Matka (z bazy)'),
        help_text=_('Wybierz matkę z istniejących psów w bazie'),
        related_name='puppy_children_as_mother'
    )
    mother_name_custom = models.CharField(
        max_length=100, 
        verbose_name=_('Matka (imię własne)'), 
        blank=True,
        help_text=_('Imię matki - jeśli nie ma jej w bazie psów')
    )
    
    father = models.ForeignKey(
        'Dog',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Ojciec (z bazy)'),
        help_text=_('Wybierz ojca z istniejących psów w bazie'),
        related_name='puppy_children_as_father'
    )
    father_name_custom = models.CharField(
        max_length=100, 
        verbose_name=_('Ojciec (imię własne)'), 
        blank=True,
        help_text=_('Imię ojca - jeśli nie ma go w bazie psów')
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
    
    def clean(self):
        """Walidacja modelu"""
        from django.core.exceptions import ValidationError
        
        # Sprawdź czy nie wybrano jednocześnie psa z bazy i wpisano imię własne dla matki
        if self.mother and self.mother_name_custom:
            raise ValidationError({
                'mother_name_custom': _('Nie można jednocześnie wybrać matki z bazy i wpisać własnego imienia. Wybierz tylko jedną opcję.')
            })
        
        # Sprawdź czy nie wybrano jednocześnie psa z bazy i wpisano imię własne dla ojca
        if self.father and self.father_name_custom:
            raise ValidationError({
                'father_name_custom': _('Nie można jednocześnie wybrać ojca z bazy i wpisać własnego imienia. Wybierz tylko jedną opcję.')
            })
    
    def __str__(self):
        parent_info = ""
        mother_display = self.get_mother_display()
        father_display = self.get_father_display()
        
        if mother_display and father_display:
            parent_info = f" ({mother_display} x {father_display})"
        elif mother_display:
            parent_info = f" (matka: {mother_display})"
        elif father_display:
            parent_info = f" (ojciec: {father_display})"
        
        color_info = ""
        if self.color1:
            color_info = f" - {self.color1}"
            if self.color2:
                color_info += f"/{self.color2}"
        
        return f"{self.litter}-{self.name} - {self.get_gender_display()}{color_info}{parent_info}"
    
    # NOWE WŁAŚCIWOŚCI I METODY
    def get_mother_display(self):
        """Zwraca wyświetlaną nazwę matki (z bazy lub własną)"""
        if self.mother:
            return self.mother.name
        elif self.mother_name_custom:
            return self.mother_name_custom
        return ""
    
    def get_father_display(self):
        """Zwraca wyświetlaną nazwę ojca (z bazy lub własną)"""
        if self.father:
            return self.father.name
        elif self.father_name_custom:
            return self.father_name_custom
        return ""
    
    def get_mother_link_data(self):
        """Zwraca dane do generowania linku dla matki"""
        if self.mother:
            return {
                'name': self.mother.name,
                'has_link': True,
                'dog_id': self.mother.pk,
                'breed': self.mother.breed if hasattr(self.mother, 'breed') else ''
            }
        elif self.mother_name_custom:
            return {
                'name': self.mother_name_custom,
                'has_link': False,
                'dog_id': None,
                'breed': ''
            }
        return None
    
    def get_father_link_data(self):
        """Zwraca dane do generowania linku dla ojca"""
        if self.father:
            return {
                'name': self.father.name,
                'has_link': True,
                'dog_id': self.father.pk,
                'breed': self.father.breed if hasattr(self.father, 'breed') else ''
            }
        elif self.father_name_custom:
            return {
                'name': self.father_name_custom,
                'has_link': False,
                'dog_id': None,
                'breed': ''
            }
        return None
    
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
    
    # DEPRECATED PROPERTIES - dla kompatybilności wstecznej
    @property
    def mother_name(self):
        """Kompatybilność wsteczna - zwraca wyświetlaną nazwę matki"""
        return self.get_mother_display()
    
    @property
    def father_name(self):
        """Kompatybilność wsteczna - zwraca wyświetlaną nazwę ojca"""
        return self.get_father_display()

class Reservation(TranslatableModel):
    translations = TranslatedFields(
        message=models.TextField(
            blank=True, 
            verbose_name=_('Wiadomość'),
            help_text=_('Dodatkowa wiadomość od klienta')
        ),
    )
    
    puppy = models.ForeignKey(
        Puppy, 
        on_delete=models.CASCADE, 
        verbose_name=_('Szczeniak')
    )
    customer_name = models.CharField(
        max_length=100, 
        verbose_name=_('Imię i nazwisko')
    )
    customer_email = models.EmailField(
        verbose_name=_('Email')
    )
    customer_phone = models.CharField(
        max_length=20, 
        verbose_name=_('Telefon')
    )
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name=_('Data zgłoszenia')
    )
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', _('Oczekuje')),
            ('confirmed', _('Potwierdzone')),
            ('cancelled', _('Anulowane'))
        ], 
        default='pending', 
        verbose_name=_('Status')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Rezerwacja')
        verbose_name_plural = _('Rezerwacje')
    
    def __str__(self):
        return f"{_('Rezerwacja')}: {self.puppy.name} - {self.customer_name}"
class ContactMessage(TranslatableModel):
    translations = TranslatedFields(
        subject=models.CharField(
            max_length=200, 
            verbose_name=_('Temat'),
            help_text=_('Temat wiadomości')
        ),
        message=models.TextField(
            verbose_name=_('Wiadomość'),
            help_text=_('Treść wiadomości kontaktowej')
        ),
    )
    
    name = models.CharField(
        max_length=100, 
        verbose_name=_('Imię i nazwisko')
    )
    email = models.EmailField(
        verbose_name=_('Email')
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name=_('Telefon')
    )
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name=_('Data wysłania')
    )
    is_read = models.BooleanField(
        default=False, 
        verbose_name=_('Przeczytane')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Wiadomość kontaktowa')
        verbose_name_plural = _('Wiadomości kontaktowe')
    
    def __str__(self):
        try:
            subject = self.safe_translation_getter('subject', any_language=True)
            if subject:
                return f"{self.name} - {subject}"
        except:
            pass
        return f"{self.name} - {_('Wiadomość kontaktowa')}"


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