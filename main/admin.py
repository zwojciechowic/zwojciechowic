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

    def get_fieldsets(self, request, obj = ...):
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
    list_display = ['litter', 'name', 'color_display_admin', 'mother_name', 'father_name', 'birth_date', 'gender', 'is_available', 'price', 'main_photo_preview', 'photos_count', 'certificates_count']
    list_filter = ['litter', 'gender', 'is_available', 'birth_date']
    search_fields = ['name', 'litter', 'mother_name', 'father_name', 'translations__breed', 'translations__description']
    list_editable = ['is_available', 'price']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if request.GET.get('language') == 'en':
            fields_to_hide = ['name', 'mother_name', 'father_name', 'litter', 'color1', 'color2', 'birth_date', 'gender', 'is_available', 'price', 'photo_gallery', 'certificates_gallery']
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
                (_('Psi rodzice'), {
                    'fields': ('mother_name', 'father_name'),
                }),
                ('Media', {
                    'fields': ('photo_gallery', 'certificates_gallery')
                }),
            )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('litter')
    
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
    list_display = ['title', 'author', 'created_at', 'is_published', 'main_photo_preview', 'photos_count', 'sections_count']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['translations__title', 'translations__excerpt', 'sections__translations__content', 'sections__translations__title']
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BlogSectionInline]
    
    # Pola wymagane dla wszystkich języków
    fields_basic = ['title', 'slug', 'author', 'is_published']
    fields_content = ['excerpt']
    fields_media = ['photo_gallery']
    fields_meta = ['created_at', 'updated_at']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        if request.GET.get('language'):
            current_lang = request.GET.get('language')
            available_languages = [lang[0] for lang in settings.LANGUAGES]
            main_language = available_languages[0] if available_languages else 'pl'
            if current_lang != main_language:
                fields_to_hide = ['slug', 'photo_gallery', 'author', 'is_published', 'created_at', 'updated_at']
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
        return qs.select_related('author', 'photo_gallery').prefetch_related('sections')

class HodowlaAdminSite(admin.AdminSite):
    site_header = _("Panel administracyjny Hodowli")
    site_title = _("Hodowla Admin")
    index_title = _("Witaj w panelu administracyjnym")
    
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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Dane nadawcy', {
            'fields': ('name', 'email', 'phone', 'created_at')
        }),
        ('Wiadomość', {
            'fields': ('subject', 'message', 'is_read')
        }),
    )
    class Media:
        css = {
            'all': ('css/admin/admin_custom.css',)
        }
        js = ('js/admin_image_preview.js',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"Oznaczono {queryset.count()} wiadomości jako przeczytane.")
    mark_as_read.short_description = "Oznacz jako przeczytane"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"Oznaczono {queryset.count()} wiadomości jako nieprzeczytane.")
    mark_as_unread.short_description = "Oznacz jako nieprzeczytane"

class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        for app in app_list:
            if app['app_label'] == 'main':
                app['models'].sort(key=lambda x: {
                    'BlogPost': 1,
                    'Dog': 2,
                    'Puppy': 3,
                    'Reservation': 4,
                    'ContactMessage': 5
                }.get(x['object_name'], 99))
        
        return app_list

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

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('puppy', 'customer_name', 'customer_email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'puppy__name')
    readonly_fields = ('created_at',)
    list_editable = ('status',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Dane rezerwacji', {
            'fields': ('puppy', 'status', 'created_at')
        }),
        ('Dane klienta', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'message')
        }),
    )

admin.site.__class__ = HodowlaAdminSite