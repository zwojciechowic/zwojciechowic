# admin.py
from django import forms
from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage, AboutPage, AboutSections, BlogSection
from django.contrib.admin import AdminSite
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Hodowla z Wojciechowic - Panel Administracyjny")
admin.site.site_title = _("Hodowla z Wojciechowic")
admin.site.index_title = _("Zarządzanie treścią")

class DogAdminForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'
    
    class Media:
        js = ('js/admin_image_preview.js',)

class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
    
    class Media:
        js = ('js/admin_image_preview.js',)

@admin.register(Dog)
class DogAdmin(TranslatableAdmin):
    list_display = ['name', 'breed', 'gender', 'birth_date', 'is_breeding']
    list_filter = ['gender', 'is_breeding', 'birth_date']
    search_fields = ['name', 'translations__breed', 'translations__description']
    list_editable = ['is_breeding']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if request.GET.get('language') == 'en':
            fields_to_hide = ['name', 'gender', 'birth_date', 'is_breeding', 'photo_gallery', 'certificates_gallery']
            for field_name in fields_to_hide:
                try:
                    del form.base_fields[field_name]
                except KeyError:
                    pass
        
        return form

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

    def main_photo_preview(self, obj):
        main_photo_obj = obj.main_photo
        if main_photo_obj and main_photo_obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />', 
                             main_photo_obj.image.url)
        return "Brak"
    main_photo_preview.short_description = "Główne zdjęcie"
    
    def photos_count(self, obj):
        if obj.photo_gallery:
            return obj.photo_gallery.photos.count()
        return 0
    photos_count.short_description = "Zdjęcia"
    
    def certificates_count(self, obj):
        if obj.certificates_gallery:
            return obj.certificates_gallery.photos.count()
        return 0
    certificates_count.short_description = "Certyfikaty"

class ColorWidget(forms.TextInput):
    """Custom widget dla color pickera"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'type': 'color',
            'style': 'width: 60px; height: 40px; border: none; cursor: pointer;'
        })

class PuppyAdminForm(forms.ModelForm):
    class Meta:
        model = Puppy
        fields = '__all__'
        widgets = {
            'color1': ColorWidget(),
            'color2': ColorWidget(),
        }

@admin.register(Puppy)
class PuppyAdmin(TranslatableAdmin):
    list_display = ['litter', 'name', 'color_display_admin', 'get_mother_display', 'get_father_display', 'birth_date', 'gender', 'is_available', 'price', 'main_photo_preview', 'photos_count', 'certificates_count']
    list_filter = ['litter', 'gender', 'is_available', 'birth_date', 'mother', 'father']
    search_fields = ['name', 'litter', 'mother_name_custom', 'father_name_custom', 'mother__name', 'father__name', 'translations__breed', 'translations__description']
    list_editable = ['is_available', 'price']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if request.GET.get('language') == 'en':
            fields_to_hide = ['name', 'mother', 'mother_name_custom', 'father', 'father_name_custom', 'litter', 'color1', 'color2', 'birth_date', 'gender', 'is_available', 'price', 'photo_gallery', 'certificates_gallery']
            for field_name in fields_to_hide:
                try:
                    del form.base_fields[field_name]
                except KeyError:
                    pass
        
        return form
    
    def get_fieldsets(self, request, obj=None):
        if request.GET.get('language') == 'en':
            return (
                (_('Podstawowe informacje'), {
                    'fields': ('breed', 'description')
                }),
            )
        else:
            return (
                (_('Podstawowe informacje'), {
                    'fields': ('litter', 'name', 'breed', 'description', 'birth_date', 'gender', 'is_available', 'price')
                }),
                (_('Kolory szczeniaka'), {
                    'fields': ('color1', 'color2'),
                }),
                (_('Rodzice szczeniaka'), {
                    'fields': (
                        ('mother', 'mother_name_custom'),
                        ('father', 'father_name_custom')
                    ),
                    'description': _(
                        'Możesz wybrać rodzica z bazy psów LUB wpisać imię psa spoza bazy. '
                        'Nie można jednocześnie wybrać psa z bazy i wpisać imienia własnego. '
                        'Jeśli wybierzesz psa z bazy, na stronie pojawi się link do jego profilu.'
                    )
                }),
                ('Media', {
                    'fields': ('photo_gallery', 'certificates_gallery')
                }),
            )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('mother', 'father').order_by('litter')
    
    def get_mother_display(self, obj):
        """Wyświetlanie matki w liście adminów"""
        mother_data = obj.get_mother_link_data()
        if mother_data:
            if mother_data['has_link']:
                return format_html(
                    '<a href="/admin/main/dog/{}/change/" title="Przejdź do profilu" style="color: #007cba; text-decoration: none;">🔗 {}</a>',
                    mother_data['dog_id'],
                    mother_data['name']
                )
            else:
                return format_html(
                    '<span style="color: #666;" title="Pies spoza bazy">📝 {}</span>',
                    mother_data['name']
                )
        return "-"
    get_mother_display.short_description = _("Matka")
    get_mother_display.admin_order_field = 'mother__name'
    
    def get_father_display(self, obj):
        """Wyświetlanie ojca w liście adminów"""
        father_data = obj.get_father_link_data()
        if father_data:
            if father_data['has_link']:
                return format_html(
                    '<a href="/admin/main/dog/{}/change/" title="Przejdź do profilu" style="color: #007cba; text-decoration: none;">🔗 {}</a>',
                    father_data['dog_id'],
                    father_data['name']
                )
            else:
                return format_html(
                    '<span style="color: #666;" title="Pies spoza bazy">📝 {}</span>',
                    father_data['name']
                )
        return "-"
    get_father_display.short_description = _("Ojciec")
    get_father_display.admin_order_field = 'father__name'
    
    def color_display_admin(self, obj):
        colors_html = ""
        if obj.color1:
            colors_html += f'<span style="background-color: {obj.color1}; width: 20px; height: 20px; display: inline-block; border: 1px solid #ccc; margin-right: 5px; vertical-align: middle;"></span>'
        if obj.color2:
            colors_html += f'<span style="background-color: {obj.color2}; width: 20px; height: 20px; display: inline-block; border: 1px solid #ccc; margin-right: 5px; vertical-align: middle;"></span>'
        
        if colors_html:
            return format_html(colors_html + f' {obj.color_display}')
        return "Nie określono"
    color_display_admin.short_description = "Kolory"
    
    def main_photo_preview(self, obj):
        main_photo_obj = obj.main_photo
        if main_photo_obj and main_photo_obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />', 
                             main_photo_obj.image.url)
        return "Brak"
    main_photo_preview.short_description = "Główne zdjęcie"
    
    def photos_count(self, obj):
        if obj.photo_gallery:
            return obj.photo_gallery.photos.count()
        return 0
    photos_count.short_description = "Zdjęcia"
    
    def certificates_count(self, obj):
        if obj.certificates_gallery:
            return obj.certificates_gallery.photos.count()
        return 0
    certificates_count.short_description = "Certyfikaty"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Dostosowanie wyboru psów dla rodziców"""
        if db_field.name == "mother":
            kwargs["queryset"] = Dog.objects.filter(gender='female').select_related().order_by('name')
            kwargs["empty_label"] = _("-- Wybierz matkę z bazy --")
        elif db_field.name == "father":
            kwargs["queryset"] = Dog.objects.filter(gender='male').select_related().order_by('name')
            kwargs["empty_label"] = _("-- Wybierz ojca z bazy --")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }
        js = [
            'admin/js/jquery.init.js',
            'admin/js/core.js',
        ]

class BlogSectionInline(TranslatableTabularInline):
    model = BlogSection
    extra = 1
    fields = ('order', 'title', 'content')
    ordering = ('order',)
    classes = ['collapse']

@admin.register(BlogSection)
class BlogSectionAdmin(TranslatableAdmin):
    list_display = ('blog_post_title', 'title', 'order')
    list_editable = ('order',)
    list_filter = ('blog_post',)
    ordering = ('blog_post', 'order')
    
    def blog_post_title(self, obj):
        try:
            return obj.blog_post.safe_translation_getter('title', any_language=True) or f"Post #{obj.blog_post.pk}"
        except:
            return f"Post #{obj.blog_post.pk}"
    blog_post_title.short_description = _("Wpis na blogu")

@admin.register(BlogPost)
class BlogPostAdmin(TranslatableAdmin):
    list_display = ['title', 'author', 'get_related_animal_display', 'created_at', 'is_published', 'main_photo_preview', 'photos_count', 'sections_count']
    list_filter = ['is_published', 'created_at', 'author', 'related_dog', 'related_puppy']
    search_fields = ['translations__title', 'translations__excerpt', 'sections__translations__content', 'sections__translations__title', 'related_dog__name', 'related_puppy__name']
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BlogSectionInline]
    
    # Pola wymagane dla wszystkich języków
    fields_basic = ['title', 'slug', 'author', 'is_published']
    fields_content = ['excerpt']
    fields_media = ['photo_gallery']
    fields_relations = ['related_dog', 'related_puppy']
    fields_meta = ['created_at', 'updated_at']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if request.GET.get('language'):
            current_lang = request.GET.get('language')
            available_languages = [lang[0] for lang in settings.LANGUAGES]
            main_language = available_languages[0] if available_languages else 'pl'
            if current_lang != main_language:
                fields_to_hide = ['slug', 'photo_gallery', 'author', 'is_published', 'created_at', 'updated_at', 'related_dog', 'related_puppy']
                for field_name in fields_to_hide:
                    try:
                        del form.base_fields[field_name]
                    except KeyError:
                        pass
        
        return form
    
    def get_fieldsets(self, request, obj=None):
        """Różne zestawy pól dla głównego języka i tłumaczeń"""
        current_language = request.GET.get('language')
        
        # Sprawdź czy to jest tryb tłumaczenia na inny język niż główny
        if current_language and obj:
            available_languages = [lang[0] for lang in settings.LANGUAGES]
            main_language = available_languages[0] if available_languages else 'pl'
            if current_language != main_language:
                return (
                    (_('Tłumaczenie na język: {}').format(current_language.upper()), {
                        'fields': ('title', 'excerpt'),
                        'description': _('Przetłumacz tytuł i opis na wybrany język')
                    }),
                )
        
        # Standardowe pola dla głównego języka lub nowego wpisu
        return (
            (_('Podstawowe informacje'), {
                'fields': ('title', 'slug', 'author', 'is_published'),
                'description': _('Slug zostanie wygenerowany automatycznie z tytułu jeśli pozostanie pusty')
            }),
            (_('Opis'), {
                'fields': ('excerpt',),
                'description': _('Krótki opis wpisu wyświetlany na liście i w kartach')
            }),
            (_('Powiązania'), {
                'fields': ('related_dog', 'related_puppy'),
                'description': _('Wybierz psa LUB szczeniaka (nie oba jednocześnie). Zostanie wyświetlony link w karcie wpisu.')
            }),
            (_('Media'), {
                'fields': ('photo_gallery',),
                'description': _('Wybierz istniejącą galerię lub stwórz nową w sekcji "Galerie"')
            }),
            (_('Informacje systemowe'), {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
                'description': _('Automatycznie generowane daty')
            }),
        )
    
    def get_related_animal_display(self, obj):
        """Wyświetla powiązane zwierzę w liście adminów"""
        if obj.related_dog:
            return format_html(
                '<span style="color: #2196F3;"><i class="fas fa-dog"></i> {}</span>',
                obj.related_dog.name
            )
        elif obj.related_puppy:
            return format_html(
                '<span style="color: #FF6B6B;"><i class="fas fa-heart"></i> {} ({})</span>',
                obj.related_puppy.name,
                f"Miot {obj.related_puppy.litter}" if obj.related_puppy.litter else "Szczeniak"
            )
        return "-"
    get_related_animal_display.short_description = _('Powiązany pies')
    get_related_animal_display.admin_order_field = 'related_dog__name'
    
    def main_photo_preview(self, obj):
        """Podgląd głównego zdjęcia"""
        main_photo_obj = obj.main_photo
        if main_photo_obj and main_photo_obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" alt="{}" />', 
                main_photo_obj.image.url,
                _("Podgląd zdjęcia")
            )
        return _("Brak")
    main_photo_preview.short_description = _("Główne zdjęcie")
    
    def photos_count(self, obj):
        """Liczba zdjęć w galerii"""
        if obj.photo_gallery:
            return obj.photo_gallery.photos.count()
        return 0
    photos_count.short_description = _("Zdjęcia")
    
    def sections_count(self, obj):
        """Liczba sekcji wpisu"""
        return obj.sections.count()
    sections_count.short_description = _("Sekcje")
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Popraw wyświetlanie w selectach dla powiązanych zwierząt"""
        if db_field.name == "related_dog":
            kwargs["queryset"] = Dog.objects.select_related().order_by('name')
            kwargs["empty_label"] = _("Brak powiązania z psem")
        elif db_field.name == "related_puppy":
            kwargs["queryset"] = Puppy.objects.select_related().order_by('litter', 'name')
            kwargs["empty_label"] = _("Brak powiązania ze szczeniakiem")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        """Zapisywanie modelu z automatycznym przypisaniem autora"""
        if not change:  # Jeśli to nowy wpis
            obj.author = request.user
        
        # Upewnij się, że slug istnieje przed zapisaniem
        if not obj.slug:
            if hasattr(obj, '_current_language'):
                # Jesteśmy w kontekście tłumaczenia
                title = getattr(obj, 'title', None)
                if title:
                    from django.utils.text import slugify
                    import uuid
                    base_slug = slugify(title) or f"post-{str(uuid.uuid4())[:8]}"
                    slug = base_slug
                    counter = 1
                    while BlogPost.objects.filter(slug=slug).exclude(pk=obj.pk).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    obj.slug = slug
            else:
                # Fallback slug
                import uuid
                obj.slug = f"post-{str(uuid.uuid4())[:8]}"
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optymalizacja zapytań"""
        qs = super().get_queryset(request)
        return qs.select_related('author', 'photo_gallery', 'related_dog', 'related_puppy').prefetch_related('sections')
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }
        js = [
            'admin/js/jquery.init.js',
            'admin/js/core.js',
        ]

class AboutSectionInline(TranslatableTabularInline):
    model = AboutSections
    extra = 1
    fields = ('order', 'title', 'content')
    ordering = ('order',)

@admin.register(AboutSections)
class AboutSectionAdmin(TranslatableAdmin):
    list_display = ('title', 'order', 'about_page')
    list_editable = ('order',)
    ordering = ('about_page', 'order')

@admin.register(AboutPage)
class AboutPageAdmin(TranslatableAdmin):
    inlines = [AboutSectionInline]
    list_display = ['main_title', 'certificates_count', 'created_info']
    
    fieldsets = (
        (_('Podstawowe informacje'), {
            'fields': ('main_title', 'top_image', 'quote_text')
        }),
        (_('Certyfikaty'), {
            'fields': ('certificates_gallery',),
            'description': _('Wybierz galerię z certyfikatami hodowli, nagrodami, dyplomami itp.')
        }),
    )
    
    def has_add_permission(self, request):
        return not AboutPage.objects.exists()
    
    def certificates_count(self, obj):
        """Liczba certyfikatów w galerii"""
        if obj.certificates_gallery:
            return obj.certificates_gallery.photos.count()
        return 0
    certificates_count.short_description = _("Certyfikaty")
    
    def created_info(self, obj):
        """Informacja o istnieniu strony"""
        return _("✓ Skonfigurowana")
    created_info.short_description = _("Status")

@admin.register(ContactMessage)
class ContactMessageAdmin(TranslatableAdmin):
    list_display = ['name', 'email', 'subject_display', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'translations__subject', 'translations__message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if request.GET.get('language') == 'en':
            fields_to_hide = ['name', 'email', 'phone', 'created_at', 'is_read']
            for field_name in fields_to_hide:
                try:
                    del form.base_fields[field_name]
                except KeyError:
                    pass
        
        return form
    
    def get_fieldsets(self, request, obj=None):
        """Różne zestawy pól dla głównego języka i tłumaczeń"""
        current_language = request.GET.get('language')
        
        # Sprawdź czy to jest tryb tłumaczenia na inny język niż główny
        if current_language and obj:
            available_languages = [lang[0] for lang in settings.LANGUAGES]
            main_language = available_languages[0] if available_languages else 'pl'
            if current_language != main_language:
                return (
                    (_('Tłumaczenie na język: {}').format(current_language.upper()), {
                        'fields': ('subject', 'message'),
                        'description': _('Przetłumacz temat i treść wiadomości na wybrany język')
                    }),
                )
        
        # Standardowe pola dla głównego języka lub nowej wiadomości
        return (
            (_('Dane nadawcy'), {
                'fields': ('name', 'email', 'phone', 'created_at')
            }),
            (_('Wiadomość'), {
                'fields': ('subject', 'message', 'is_read')
            }),
        )
    
    def subject_display(self, obj):
        """Wyświetlenie tematu z obsługą tłumaczeń"""
        try:
            subject = obj.safe_translation_getter('subject', any_language=True)
            if subject:
                return str(subject)
        except:
            pass
        return _("Brak tematu")
    subject_display.short_description = _('Temat')
    
    class Media:
        css = {
            'all': ('css/admin/admin_custom.css',)
        }
        js = ('js/admin_image_preview.js',)
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, _("Oznaczono %(count)d wiadomości jako przeczytane.") % {'count': queryset.count()})
    mark_as_read.short_description = _("Oznacz jako przeczytane")
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, _("Oznaczono %(count)d wiadomości jako nieprzeczytane.") % {'count': queryset.count()})
    mark_as_unread.short_description = _("Oznacz jako nieprzeczytane")

@admin.register(Reservation)
class ReservationAdmin(TranslatableAdmin):
    # ZMIENIONA LISTA KOLUMN
    list_display = ('puppy_name_display', 'contact_display', 'status', 'created_at_display')
    
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'puppy__name', 'translations__message')
    readonly_fields = ('created_at',)
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    
    # NOWE METODY WYŚWIETLANIA
    def puppy_name_display(self, obj):
        """Wyświetla tylko imię szczeniaka"""
        if obj.puppy and hasattr(obj.puppy, 'name'):
            return obj.puppy.name
        return "Nieznane"
    puppy_name_display.short_description = "Imię"
    puppy_name_display.admin_order_field = 'puppy__name'
    
    def contact_display(self, obj):
        """Wyświetla email i/lub telefon"""
        contact_info = []
        
        if obj.customer_email and obj.customer_email.strip():
            contact_info.append(obj.customer_email.strip())
        
        if obj.customer_phone and obj.customer_phone.strip():
            contact_info.append(obj.customer_phone.strip())
        
        if contact_info:
            return '<br>'.join(contact_info)
        
        # Jeśli brak kontaktu, pokaż imię
        if obj.customer_name and obj.customer_name.strip():
            return obj.customer_name.strip()
        
        return "Brak kontaktu"
    contact_display.short_description = "Kontakt"
    contact_display.allow_tags = True  # Pozwala na HTML (dla <br>)
    
    def created_at_display(self, obj):
        """Formatuje datę zgłoszenia"""
        if obj.created_at:
            return obj.created_at.strftime('%d.%m.%Y, %H:%M')
        return "-"
    created_at_display.short_description = "Z kiedy"
    created_at_display.admin_order_field = 'created_at'
    
    # CSS DO WĘŻSZYCH KOLUMN
    class Media:
        css = {
            'all': ('admin/css/custom_reservation_admin.css',)
        }
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if request.GET.get('language') == 'en':
            fields_to_hide = ['puppy', 'customer_name', 'customer_email', 'customer_phone', 'created_at', 'status']
            for field_name in fields_to_hide:
                try:
                    del form.base_fields[field_name]
                except KeyError:
                    pass
        
        return form
    
    def get_fieldsets(self, request, obj=None):
        """Różne zestawy pól dla głównego języka i tłumaczeń"""
        current_language = request.GET.get('language')
        
        # Sprawdź czy to jest tryb tłumaczenia na inny język niż główny
        if current_language and obj:
            available_languages = [lang[0] for lang in settings.LANGUAGES]
            main_language = available_languages[0] if available_languages else 'pl'
            if current_language != main_language:
                return (
                    (_('Tłumaczenie na język: {}').format(current_language.upper()), {
                        'fields': ('message',),
                        'description': _('Przetłumacz wiadomość klienta na wybrany język')
                    }),
                )
        
        # Standardowe pola dla głównego języka lub nowej rezerwacji
        return (
            (_('Dane rezerwacji'), {
                'fields': ('puppy', 'status', 'created_at')
            }),
            (_('Dane klienta'), {
                'fields': ('customer_name', 'customer_email', 'customer_phone', 'message')
            }),
        )

# CUSTOM ADMIN SITE Z DASHBOARD CONTEXT
class CustomAdminSite(admin.AdminSite):
    site_header = _("Panel administracyjny Hodowli")
    site_title = _("Hodowla Admin")
    index_title = _("Panel Hodowli z Wojciechowic")
    
    def index(self, request, extra_context=None):
        """
        Nadpisuje domyślny widok dashboard z danymi kontekstowymi
        """
        # Importuj modele lokalnie żeby uniknąć circular imports
        from .models import Dog, Puppy, Reservation, BlogPost, ContactMessage, AboutPage
        
        extra_context = extra_context or {}
        
        # Dodaj wszystkie dane potrzebne w template
        extra_context.update({
            'dogs_count': Dog.objects.count(),
            'puppies_count': Puppy.objects.filter(is_available=True).count(),
            'reservations_count': Reservation.objects.filter(status='pending').count(),
            'posts_count': BlogPost.objects.filter(is_published=True).count(),
            'messages_count': ContactMessage.objects.count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'about_exists': AboutPage.objects.exists(),
        })
        
        return super().index(request, extra_context)
    
    def get_app_list(self, request, app_label=None):
        """Customizacja listy aplikacji i modeli"""
        app_list = super().get_app_list(request, app_label)
        
        hidden_models = [
            'BlogSection', 'Blog sections', 'Sekcje wpisu',
            'AboutSections', 'About sections', 'Sekcje'
        ]
        
        for app in app_list:
            if app['app_label'] == 'main':
                # Filtruj ukryte modele
                app['models'] = [
                    model for model in app['models'] 
                    if model['object_name'] not in hidden_models and 
                        model['name'] not in hidden_models
                ]
                
                # Sortuj modele w określonej kolejności
                model_order = {
                    'BlogPost': 1,
                    'Dog': 2,
                    'Puppy': 3,
                    'Reservation': 4,
                    'ContactMessage': 5,
                    'AboutPage': 6
                }
                
                app['models'].sort(key=lambda x: model_order.get(x['object_name'], 99))
        
        return app_list

# Zastąp domyślny admin site naszym custom site
admin.site.__class__ = CustomAdminSite