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
    list_display = ['name', 'breed', 'gender', 'birth_date', 'is_breeding', 'preview_image', 'has_certificate', 'additional_photos_count']
    list_filter = ['breed', 'gender', 'is_breeding', 'birth_date']
    search_fields = ['name', 'breed', 'description']
    list_editable = ['is_breeding']
    date_hierarchy = 'birth_date'
    readonly_fields = ['preview_image', 'additional_photos_manager']
    form = DogAdminForm
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name', 'breed', 'gender', 'birth_date', 'is_breeding')
        }),
        ('Opis i zdjęcie główne', {
            'fields': ('description', 'photo', 'preview_image')
        }),
        ('Dodatkowe zdjęcia', {
            'fields': ('additional_photos_manager',),
            'classes': ('multiple-photos-section',)
        }),
        ('Certyfikat', {
            'fields': ('certificate',)
        }),
    )
    
    class Media:
        css = {
            'all': ('css/admin/admin_custom.css', 'css/admin/multiple_photos.css')
        }
        js = ('js/admin_image_preview.js', 'js/multiple_photos.js')

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
    
    def additional_photos_count(self, obj):
        return len(obj.additional_photos) if obj.additional_photos else 0
    additional_photos_count.short_description = "Dodatkowe zdjęcia"
    
    def additional_photos_manager(self, obj):
        html = '''
        <div class="multiple-photos-widget">
            <div class="upload-section">
                <input type="file" id="additional_photos_input" multiple accept="image/*" 
                       style="width: 100%; padding: 10px; border: 2px dashed #007cba; border-radius: 6px; background: #f0f8ff; cursor: pointer;" />
                <p style="margin: 10px 0; color: #666; font-size: 12px;">
                    Wybierz wiele zdjęć naraz. Możesz je przeciągnąć i upuścić tutaj.
                </p>
            </div>
            <div id="additional-photos-container">
        '''
        
        if obj.additional_photos:
            for i, photo_data in enumerate(obj.additional_photos):
                html += f'''
                <div class="photo-item" data-index="{i}">
                    <img src="{photo_data.get('url', '')}" style="width: 150px; height: 100px; object-fit: cover;" />
                    <span class="remove-photo" onclick="removePhoto({i})">×</span>
                    <input type="number" value="{photo_data.get('order', i+1)}" min="1" class="order-input" 
                           onchange="updatePhotoOrder({i}, this.value)" />
                </div>
                '''
        
        html += '''
            </div>
            <input type="hidden" name="additional_photos_data" id="additional_photos_data" />
        </div>
        '''
        
        return format_html(html)
    additional_photos_manager.short_description = "Zarządzanie dodatkowymi zdjęciami"

    def save_model(self, request, obj, form, change):
        # Najpierw zapisz obiekt
        super().save_model(request, obj, form, change)
        
        # Obsługa dodatkowych zdjęć
        additional_photos_data = request.POST.get('additional_photos_data')
        if additional_photos_data:
            try:
                import json
                photos_data = json.loads(additional_photos_data)
                
                # Sprawdź czy są nowe pliki do uploadu
                uploaded_files = request.FILES.getlist('additional_photos_files')
                for file in uploaded_files:
                    if file.content_type.startswith('image/'):
                        # Zapisz plik do odpowiedniego katalogu
                        from django.core.files.storage import default_storage
                        from django.core.files.base import ContentFile
                        import uuid
                        
                        filename = f"additional_photos/{obj._meta.model_name}_{obj.pk}_{uuid.uuid4().hex[:8]}_{file.name}"
                        saved_file = default_storage.save(filename, ContentFile(file.read()))
                        
                        # Dodaj do photos_data
                        photos_data.append({
                            'url': default_storage.url(saved_file),
                            'order': len(photos_data) + 1,
                            'filename': saved_file
                        })
                
                # Sortuj i zapisz
                photos_data.sort(key=lambda x: x.get('order', 0))
                obj.additional_photos = photos_data
                obj.save(update_fields=['additional_photos'])
                
            except (json.JSONDecodeError, TypeError):
                pass

@admin.register(Puppy)
class PuppyAdmin(admin.ModelAdmin):
    list_display = ['name', 'mother', 'father', 'birth_date', 'gender', 'is_available', 'price', 'preview_image', 'has_certificate', 'additional_photos_count']
    list_filter = ['gender', 'is_available', 'birth_date', 'mother', 'father']
    search_fields = ['name', 'mother__name', 'father__name', 'description']
    list_editable = ['is_available', 'price']
    date_hierarchy = 'birth_date'
    readonly_fields = ['preview_image', 'additional_photos_manager']
    form = PuppyAdminForm
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name', 'mother', 'father', 'birth_date', 'gender')
        }),
        ('Dostępność i cena', {
            'fields': ('is_available', 'price')
        }),
        ('Opis i zdjęcie główne', {
            'fields': ('description', 'photo', 'preview_image')
        }),
        ('Dodatkowe zdjęcia', {
            'fields': ('additional_photos_manager',),
            'classes': ('multiple-photos-section',)
        }),
        ('Certyfikat', {
            'fields': ('certificate',)
        }),
    )
    
    class Media:
        css = {
            'all': ('css/admin/admin_custom.css', 'css/admin/multiple_photos.css')
        }
        js = ('js/admin_image_preview.js', 'js/multiple_photos.js')
    
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
    
    def additional_photos_count(self, obj):
        return len(obj.additional_photos) if obj.additional_photos else 0
    additional_photos_count.short_description = "Dodatkowe zdjęcia"
    
    def additional_photos_manager(self, obj):
        html = '''
        <div class="multiple-photos-widget">
            <div class="upload-section">
                <input type="file" id="additional_photos_input" multiple accept="image/*" 
                       style="width: 100%; padding: 10px; border: 2px dashed #007cba; border-radius: 6px; background: #f0f8ff; cursor: pointer;" />
                <p style="margin: 10px 0; color: #666; font-size: 12px;">
                    Wybierz wiele zdjęć naraz. Możesz je przeciągnąć i upuścić tutaj.
                </p>
            </div>
            <div id="additional-photos-container">
        '''
        
        if obj.additional_photos:
            for i, photo_data in enumerate(obj.additional_photos):
                html += f'''
                <div class="photo-item" data-index="{i}">
                    <img src="{photo_data.get('url', '')}" style="width: 150px; height: 100px; object-fit: cover;" />
                    <span class="remove-photo" onclick="removePhoto({i})">×</span>
                    <input type="number" value="{photo_data.get('order', i+1)}" min="1" class="order-input" 
                           onchange="updatePhotoOrder({i}, this.value)" />
                </div>
                '''
        
        html += '''
            </div>
            <input type="hidden" name="additional_photos_data" id="additional_photos_data" />
        </div>
        '''
        
        return format_html(html)
    additional_photos_manager.short_description = "Zarządzanie dodatkowymi zdjęciami"

    def save_model(self, request, obj, form, change):
        # Najpierw zapisz obiekt
        super().save_model(request, obj, form, change)
        
        # Obsługa dodatkowych zdjęć
        additional_photos_data = request.POST.get('additional_photos_data')
        if additional_photos_data:
            try:
                import json
                photos_data = json.loads(additional_photos_data)
                
                # Sprawdź czy są nowe pliki do uploadu
                uploaded_files = request.FILES.getlist('additional_photos_files')
                for file in uploaded_files:
                    if file.content_type.startswith('image/'):
                        # Zapisz plik do odpowiedniego katalogu
                        from django.core.files.storage import default_storage
                        from django.core.files.base import ContentFile
                        import uuid
                        
                        filename = f"additional_photos/{obj._meta.model_name}_{obj.pk}_{uuid.uuid4().hex[:8]}_{file.name}"
                        saved_file = default_storage.save(filename, ContentFile(file.read()))
                        
                        # Dodaj do photos_data
                        photos_data.append({
                            'url': default_storage.url(saved_file),
                            'order': len(photos_data) + 1,
                            'filename': saved_file
                        })
                
                # Sortuj i zapisz
                photos_data.sort(key=lambda x: x.get('order', 0))
                obj.additional_photos = photos_data
                obj.save(update_fields=['additional_photos'])
                
            except (json.JSONDecodeError, TypeError):
                pass
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
    fields = ('main_title', 'top_image', 'quote_text')

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()
    
class HodowlaAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        """Custom dashboard z licznikami - ulepszona wersja"""
        extra_context = extra_context or {}
        
        try:
            dogs_count = Dog.objects.count()
            puppies_count = Puppy.objects.filter(is_available=True).count()
            posts_count = BlogPost.objects.filter(is_published=True).count()
            about_exists = AboutPage.objects.exists()
            
            # Liczniki rezerwacji
            pending_reservations = Reservation.objects.filter(status='pending').count()
            confirmed_reservations = Reservation.objects.filter(status='confirmed').count()
            total_reservations = pending_reservations + confirmed_reservations
            
            # Liczniki wiadomości kontaktowych
            total_messages = ContactMessage.objects.count()
            unread_messages = ContactMessage.objects.filter(is_read=False).count()
            
            # Dodatkowe statystyki (opcjonalnie)
            total_puppies = Puppy.objects.count()
            sold_puppies = total_puppies - puppies_count
            draft_posts = BlogPost.objects.filter(is_published=False).count()
            breeding_dogs = Dog.objects.filter(is_breeding=True).count()
            
            extra_context.update({
                # Podstawowe dane dla kart
                'dogs_count': dogs_count,
                'puppies_count': puppies_count,
                'posts_count': posts_count,
                'reservations_count': total_reservations,
                'about_exists': about_exists,
                
                # Dane dla wiadomości
                'messages_count': total_messages,
                'unread_messages': unread_messages,
                
                # Dodatkowe szczegóły
                'pending_reservations': pending_reservations,
                'confirmed_reservations': confirmed_reservations,
                'sold_puppies': sold_puppies,
                'draft_posts': draft_posts,
                'breeding_dogs': breeding_dogs,
            })
            
        except Exception as e:
            # W przypadku błędu (np. przy pierwszym uruchomieniu bez migracji)
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
            })
        
        return super().index(request, extra_context)

# Zastąp ostatnią linię Twojego pliku admin.py:
admin.site.__class__ = HodowlaAdminSite