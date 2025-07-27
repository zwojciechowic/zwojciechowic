# main/admin.py
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage, AboutPage, AboutSections
from django.contrib.admin import AdminSite

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

class PuppyAdminForm(forms.ModelForm):
    class Meta:
        model = Puppy
        fields = '__all__'
    
    class Media:
        js = ('js/admin_image_preview.js',)

class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
    
    class Media:
        js = ('js/admin_image_preview.js',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published', 'preview_image']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'preview_image']
    form = BlogPostAdminForm
    
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'slug', 'author', 'is_published')
        }),
        ('Treść', {
            'fields': ('excerpt', 'content', 'featured_image', 'preview_image')
        }),
        ('Daty', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return "Brak zdjęcia"
    preview_image.short_description = "Podgląd"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Jeśli to nowy wpis
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'gender', 'birth_date', 'is_breeding', 'preview_image', 'has_certificate']
    list_filter = ['breed', 'gender', 'is_breeding', 'birth_date']
    search_fields = ['name', 'breed', 'description']
    list_editable = ['is_breeding']
    date_hierarchy = 'birth_date'
    readonly_fields = ['preview_image']
    form = DogAdminForm
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name', 'breed', 'gender', 'birth_date', 'is_breeding')
        }),
        ('Opis i zdjęcie', {
            'fields': ('description', 'photo', 'preview_image')
        }),
        ('Certyfikat', {
            'fields': ('certificate',)
        }),
    )
    
    class Media:
        css = {
            'all': ('css/admin/admin_custom.css',)
        }
        js = ('js/admin_image_preview.js',)

    def preview_image(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />',
                obj.photo.url
            )
        return "Brak zdjęcia"
    preview_image.short_description = "Podgląd"
    
    def has_certificate(self, obj):
        return "Tak" if obj.certificate else "Nie"
    has_certificate.short_description = "Certyfikat"

@admin.register(Puppy)
class PuppyAdmin(admin.ModelAdmin):
    list_display = ['name', 'mother', 'father', 'birth_date', 'gender', 'is_available', 'price', 'preview_image', 'has_certificate']
    list_filter = ['gender', 'is_available', 'birth_date', 'mother', 'father']
    search_fields = ['name', 'mother__name', 'father__name', 'description']
    list_editable = ['is_available', 'price']
    date_hierarchy = 'birth_date'
    readonly_fields = ['preview_image']
    form = PuppyAdminForm
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name', 'mother', 'father', 'birth_date', 'gender')
        }),
        ('Dostępność i cena', {
            'fields': ('is_available', 'price')
        }),
        ('Opis i zdjęcie', {
            'fields': ('description', 'photo', 'preview_image')
        }),
        ('Certyfikat', {
            'fields': ('certificate',)
        }),
    )
    
    class Media:
        css = {
            'all': ('css/admin/admin_custom.css',)
        }
        js = ('js/admin_image_preview.js',)
    
    def preview_image(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />',
                obj.photo.url
            )
        return "Brak zdjęcia"
    preview_image.short_description = "Podgląd"
    
    def has_certificate(self, obj):
        return "Tak" if obj.certificate else "Nie"
    has_certificate.short_description = "Certyfikat"
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['puppy', 'customer_name', 'customer_email', 'customer_phone', 'created_at', 'status']
    list_filter = ['status', 'created_at', 'puppy']
    search_fields = ['customer_name', 'customer_email', 'puppy__name']
    list_editable = ['status']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informacje o rezerwacji', {
            'fields': ('puppy', 'status', 'created_at')
        }),
        ('Dane klienta', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Wiadomość', {
            'fields': ('message',)
        }),
    )
    class Media:
        css = {
            'all': ('css/admin/admin_custom.css',)
        }
        js = ('js/admin_image_preview.js',)
    actions = ['mark_as_confirmed', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"Potwierdzono {queryset.count()} rezerwacji.")
    mark_as_confirmed.short_description = "Potwierdź wybrane rezerwacje"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"Anulowano {queryset.count()} rezerwacji.")
    mark_as_cancelled.short_description = "Anuluj wybrane rezerwacje"

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

# Dodatkowe ustawienia panelu administracyjnego
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

# Jeśli chcesz użyć niestandardowego admin site:
# admin_site = CustomAdminSite(name='hodowla_admin')
# admin_site.register(BlogPost, BlogPostAdmin)
# admin_site.register(Dog, DogAdmin)
# admin_site.register(Puppy, PuppyAdmin)
# admin_site.register(Reservation, ReservationAdmin)
# admin_site.register(ContactMessage, ContactMessageAdmin)

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
    fields = ('main_title', 'top_image', 'quote_text')

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()
    

class HodowlaAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        """Custom dashboard z licznikami"""
        extra_context = extra_context or {}
        extra_context.update({
            'dogs_count': Dog.objects.count(),
            'puppies_count': Puppy.objects.filter(is_available=True).count(),
            'reservations_count': Reservation.objects.filter(status='pending').count(),
            'posts_count': BlogPost.objects.filter(is_published=True).count(),
            'about_exists': AboutPage.objects.exists(),
        })
        return super().index(request, extra_context)

admin.site.__class__ = HodowlaAdminSite