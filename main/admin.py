# admin.py
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage, AboutPage, AboutSections, BlogSection
from django.contrib.admin import AdminSite
from parler.admin import TranslatableAdmin

# Konfiguracja panelu administracyjnego
admin.site.site_header = "Hodowla z Wojciechowic - Panel Administracyjny"
admin.site.site_title = "Hodowla z Wojciechowic"
admin.site.index_title = "Zarządzanie treścią"

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
    list_display = ['name', 'breed', 'gender', 'birth_date', 'is_breeding', 'main_photo_preview', 'photos_count', 'certificates_count']
    list_filter = ['gender', 'is_breeding', 'birth_date']
    search_fields = ['translations__name', 'translations__breed', 'translations__description']
    list_editable = ['is_breeding']

    def get_form(self, request, obj=None, **kwargs):
        # 1. Pobierz domyślny formularz, który Django i Parler chcą zbudować.
        form = super().get_form(request, obj, **kwargs)

        # 2. Sprawdź, czy jesteśmy w kontekście języka angielskiego.
        if request.GET.get('language') == 'en':
            # 3. Jeśli tak, usuń z formularza pola, których nie chcemy widzieć.
            #    Używamy pętli i 'try...except', aby uniknąć błędów, jeśli pole już nie istnieje.
            fields_to_hide = ['name', 'gender', 'birth_date', 'is_breeding', 'photo_gallery', 'certificates_gallery']
            for field_name in fields_to_hide:
                try:
                    del form.base_fields[field_name]
                except KeyError:
                    # To normalne, jeśli pole już zostało usunięte lub nie istnieje. Po prostu kontynuuj.
                    pass
        
        # 4. Zwróć zmodyfikowany formularz.
        return form

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
class PuppyAdmin(admin.ModelAdmin):
    form = PuppyAdminForm
    list_display = ['litter', 'name', 'color_display_admin', 'mother_name', 'father_name', 'birth_date', 'gender', 'is_available', 'price', 'main_photo_preview', 'photos_count', 'certificates_count']
    list_filter = ['litter', 'gender', 'is_available', 'birth_date', 'mother_name', 'father_name']
    search_fields = ['name', 'litter', 'mother_name', 'father_name']
    list_editable = ['is_available', 'price']
    
    # Grupowanie po miocie w liście
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('litter', 'name')
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('litter', 'name', 'birth_date', 'gender', 'description')
        }),
        ('Kolory', {
            'fields': ('color1', 'color2'),
            'description': 'Wybierz kolory szczeniaka'
        }),
        ('Rodzice', {
            'fields': ('mother_name', 'father_name'),
            'description': 'Wpisz imiona rodziców - nie będą tworzone nowe rekordy psów w bazie danych'
        }),
        ('Dostępność', {
            'fields': ('is_available', 'price')
        }),
        ('Media', {
            'fields': ('photo_gallery', 'certificates_gallery')
        }),
    )
    
    def color_display_admin(self, obj):
        """Wyświetlanie kolorów w panelu admina z preview"""
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

@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'title', 'order')
    list_editable = ('order',)
    list_filter = ('blog_post',)
    ordering = ('blog_post', 'order')

class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1
    fields = ('order', 'title', 'content')
    ordering = ('order',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published', 'main_photo_preview', 'photos_count', 'sections_count']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'excerpt', 'sections__content', 'sections__title']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    form = BlogPostAdminForm
    inlines = [BlogSectionInline]
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'slug', 'author', 'is_published')
        }),
        ('Opis', {
            'fields': ('excerpt',),
            'description': 'Krótki opis wpisu wyświetlany na liście i w kartach'
        }),
        ('Media', {
            'fields': ('photo_gallery',),
            'description': 'Wybierz istniejącą galerię lub stwórz nową w sekcji "Galerie"'
        }),
        ('Daty', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        # Sekcje treści będą dodawane przez inline poniżej
    )
    
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
    
    def sections_count(self, obj):
        return obj.sections.count()
    sections_count.short_description = "Sekcje"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Jeśli to nowy wpis
            obj.author = request.user
        super().save_model(request, obj, form, change)
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
        """
        Sortuje aplikacje i modele w panelu administracyjnym
        """
        app_list = super().get_app_list(request)
        
        # Sortowanie modeli w aplikacji main
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

@admin.register(AboutSections)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'about_page')
    list_editable = ('order',)
    ordering = ('about_page', 'order')

class AboutSectionInline(admin.TabularInline):
    model = AboutSections
    extra = 1
    fields = ('order', 'title', 'content')
    ordering = ('order',)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    inlines = [AboutSectionInline]
    list_display = ['main_title', 'certificates_count', 'created_info']
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('main_title', 'top_image', 'quote_text')
        }),
        ('Certyfikaty', {
            'fields': ('certificates_gallery',),
            'description': 'Wybierz galerię z certyfikatami hodowli, nagrodami, dyplomami itp.'
        }),
    )
    
    def has_add_permission(self, request):
        return not AboutPage.objects.exists()
    
    def certificates_count(self, obj):
        """Liczba certyfikatów w galerii"""
        if obj.certificates_gallery:
            return obj.certificates_gallery.photos.count()
        return 0
    certificates_count.short_description = "Certyfikaty"
    
    def created_info(self, obj):
        """Informacja o istnieniu strony"""
        return "✓ Skonfigurowana"
    created_info.short_description = "Status"
    
class HodowlaAdminSite(AdminSite):
   def get_app_list(self, request):
       app_list = super().get_app_list(request)
       
       hidden_models = [
           'BlogSection', 'Blog sections', 'Sekcje wpisu',
           'AboutSections', 'About sections', 'Sekcje'
       ]
       
       for app in app_list:
           if app['app_label'] == 'main':
               app['models'] = [
                   model for model in app['models'] 
                   if model['object_name'] not in hidden_models and 
                      model['name'] not in hidden_models
               ]
               
               app['models'].sort(key=lambda x: {
                   'BlogPost': 1,
                   'Blog': 1,
                   'Dog': 2,
                   'Nasze Psy': 2,
                   'Puppy': 3,
                   'Szczenięta': 3,
                   'Reservation': 4,
                   'Rezerwacje': 4,
                   'ContactMessage': 5,
                   'Kontakt': 5,
                   'AboutPage': 6,
                   'Strona O nas': 6
               }.get(x['object_name'], 99))
       
       return app_list

   def index(self, request, extra_context=None):
       extra_context = extra_context or {}
       
       try:
           dogs_count = Dog.objects.count()
           puppies_count = Puppy.objects.filter(is_available=True).count()
           posts_count = BlogPost.objects.filter(is_published=True).count()
           about_exists = AboutPage.objects.exists()
           
           pending_reservations = Reservation.objects.filter(status='pending').count()
           confirmed_reservations = Reservation.objects.filter(status='confirmed').count()
           total_reservations = pending_reservations + confirmed_reservations
           
           total_messages = ContactMessage.objects.count()
           unread_messages = ContactMessage.objects.filter(is_read=False).count()
           
           total_puppies = Puppy.objects.count()
           sold_puppies = total_puppies - puppies_count
           draft_posts = BlogPost.objects.filter(is_published=False).count()
           breeding_dogs = Dog.objects.filter(is_breeding=True).count()
           
           quick_links = format_html('''
           <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
               <h3>🌐 Podgląd strony publicznej:</h3>
               <a href="/" target="_blank" style="margin: 5px; padding: 8px 15px; background: #007cba; color: white; text-decoration: none; border-radius: 3px;">🏠 Strona główna</a>
               <a href="/nasze-psy/" target="_blank" style="margin: 5px; padding: 8px 15px; background: #007cba; color: white; text-decoration: none; border-radius: 3px;">🐕 Nasze psy</a>
               <a href="/szczeniaki/" target="_blank" style="margin: 5px; padding: 8px 15px; background: #007cba; color: white; text-decoration: none; border-radius: 3px;">🐶 Szczeniaki</a>
               <a href="/o-nas/" target="_blank" style="margin: 5px; padding: 8px 15px; background: #007cba; color: white; text-decoration: none; border-radius: 3px;">👥 O nas</a>
               <a href="/kontakt/" target="_blank" style="margin: 5px; padding: 8px 15px; background: #007cba; color: white; text-decoration: none; border-radius: 3px;">📞 Kontakt</a>
               <a href="/hotel/" target="_blank" style="margin: 5px; padding: 8px 15px; background: #007cba; color: white; text-decoration: none; border-radius: 3px;">🏨 Hotel</a>
           </div>
           ''')
           
           extra_context.update({
               'dogs_count': dogs_count,
               'puppies_count': puppies_count,
               'posts_count': posts_count,
               'reservations_count': total_reservations,
               'about_exists': about_exists,
               'messages_count': total_messages,
               'unread_messages': unread_messages,
               'pending_reservations': pending_reservations,
               'confirmed_reservations': confirmed_reservations,
               'sold_puppies': sold_puppies,
               'draft_posts': draft_posts,
               'breeding_dogs': breeding_dogs,
               'quick_links': quick_links,
           })
           
       except Exception as e:
           print(f"Błąd w dashboard: {e}")
           extra_context.update({
               'dogs_count': 0,
               'puppies_count': 0,
               'posts_count': 0,
               'reservations_count': 0,
               'about_exists': False,
               'messages_count': 0,
               'unread_messages': 0,
               'pending_reservations': 0,
               'confirmed_reservations': 0,
               'sold_puppies': 0,
               'draft_posts': 0,
               'breeding_dogs': 0,
               'quick_links': '',
           })
       
       return super().index(request, extra_context)

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

# Zastąp ostatnią linię Twojego pliku admin.py:
admin.site.__class__ = HodowlaAdminSite