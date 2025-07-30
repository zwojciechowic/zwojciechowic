# admin.py
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, Dog, Puppy, Reservation, ContactMessage, AboutPage, AboutSections
from django.contrib.admin import AdminSite
import json
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

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

# admin.py
from django.contrib import admin
from django.utils.html import format_html
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid

class BasePhotoAdmin(admin.ModelAdmin):
    readonly_fields = ['photos_manager', 'certificates_manager']
    
    class Media:
        css = {'all': ('css/admin/photos.css',)}
        # Usuń JS z Media - dodamy inline
    
    def photos_manager(self, obj):
        return self._render_photo_widget(obj, 'photos', 'Zdjęcia')
    photos_manager.short_description = "Zarządzanie zdjęciami"
    
    def certificates_manager(self, obj):
        return self._render_photo_widget(obj, 'certificates', 'Certyfikaty')
    certificates_manager.short_description = "Zarządzanie certyfikatami"
    
    def _render_photo_widget(self, obj, field_name, label):
        photos = getattr(obj, field_name, []) or []
        
        # JavaScript inline
        js_code = '''
        <script>
        (function() {
            const widget = document.querySelector('.photos-widget[data-field="''' + field_name + '''"]');
            if (!widget) return;
            
            const input = widget.querySelector('.photo-input');
            const container = widget.querySelector('.photos-container');
            const hiddenField = widget.querySelector('.photos-data');
            let photos = [];
            let nextIndex = 0;
            
            // Załaduj istniejące zdjęcia
            const items = container.querySelectorAll('.photo-item');
            items.forEach((item, index) => {
                const img = item.querySelector('img');
                if (img) {
                    photos.push({
                        url: img.src,
                        order: index + 1,
                        index: index
                    });
                    nextIndex = Math.max(nextIndex, index + 1);
                }
            });
            
            // Obsługa nowych plików
            input.addEventListener('change', function(e) {
                Array.from(e.target.files).forEach(file => {
                    if (file.type.startsWith('image/')) {
                        addPhoto(file);
                    }
                });
                e.target.value = '';
            });
            
            function addPhoto(file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const photo = {
                        url: e.target.result,
                        file: file,
                        order: photos.length + 1,
                        index: nextIndex++
                    };
                    photos.push(photo);
                    renderPhoto(photo);
                    updateHiddenField();
                };
                reader.readAsDataURL(file);
            }
            
            function renderPhoto(photo) {
                const div = document.createElement('div');
                div.className = 'photo-item';
                div.dataset.index = photo.index;
                div.innerHTML = `
                    <img src="${photo.url}" style="width: 150px; height: 100px; object-fit: cover; border-radius: 4px;" />
                    <span class="remove-photo" onclick="removePhoto''' + field_name + '''(${photo.index})">×</span>
                    <input type="text" value="${photo.order}" class="order-input" style="width: 30px; height: 30px; text-align: center; border: 1px solid #ddd; border-radius: 4px; font-size: 12px;" />
                `;
                container.appendChild(div);
            }
            
            function updateHiddenField() {
                hiddenField.value = JSON.stringify(photos);
            }
            
            // Globalna funkcja usuwania
            window['removePhoto''' + field_name + ''''] = function(index) {
                photos = photos.filter(p => p.index !== index);
                const item = container.querySelector(`[data-index="${index}"]`);
                if (item) item.remove();
                updateHiddenField();
            };
        })();
        </script>
        '''
        
        html = f'''
        <div class="photos-widget" data-field="{field_name}">
            <h4>{label}</h4>
            <input type="file" multiple accept="image/*" class="photo-input" 
                   style="width: 100%; padding: 10px; border: 2px dashed #007cba; border-radius: 6px; background: #f0f8ff; cursor: pointer; margin-bottom: 15px;" />
            <p style="margin: 10px 0; color: #666; font-size: 12px;">
                Wybierz wiele zdjęć naraz. Możesz je przeciągnąć i upuścić tutaj.
            </p>
            <div class="photos-container" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px;">
        '''
        
        for i, photo in enumerate(photos):
            html += f'''
                <div class="photo-item" data-index="{i}" style="position: relative; border: 1px solid #ddd; border-radius: 6px; padding: 10px; background: white;">
                    <img src="{photo.get('url', '')}" style="width: 150px; height: 100px; object-fit: cover; border-radius: 4px; display: block; margin-bottom: 8px;" />
                    <span class="remove-photo" onclick="removePhoto{field_name}({i})" style="position: absolute; top: 5px; right: 5px; background: #dc3545; color: white; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; font-size: 16px; line-height: 25px; text-align: center; font-weight: bold;">×</span>
                    <input type="text" value="{i+1}" class="order-input" style="width: 30px; height: 30px; text-align: center; border: 1px solid #ddd; border-radius: 4px; font-size: 12px;" />
                </div>
            '''
        
        html += f'''
            </div>
            <input type="hidden" name="{field_name}_data" class="photos-data" />
        </div>
        {js_code}
        '''
        return format_html(html)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Obsługa zdjęć
        self._save_photos(request, obj, 'photos')
        # Obsługa certyfikatów
        self._save_photos(request, obj, 'certificates')
    
    def _save_photos(self, request, obj, field_name):
        # Pobierz istniejące zdjęcia
        existing_photos = getattr(obj, field_name, []) or []
        
        # Sprawdź czy są nowe pliki przesłane przez JavaScript
        new_photos = []
        for key, file in request.FILES.items():
            if key.startswith('new_photo_') and file.content_type.startswith('image/'):
                filename = f"{field_name}/{obj._meta.model_name}_{obj.pk}_{uuid.uuid4().hex[:8]}_{file.name}"
                saved_file = default_storage.save(filename, ContentFile(file.read()))
                new_photos.append({
                    'url': default_storage.url(saved_file),
                    'filename': saved_file,
                    'order': len(existing_photos) + len(new_photos) + 1
                })
        
        # Połącz istniejące z nowymi
        all_photos = existing_photos + new_photos
        
        # Sprawdź dane z hidden field (może zawierać info o usuniętych zdjęciach)
        photos_data = request.POST.get(f'{field_name}_data')
        if photos_data:
            try:
                client_photos = json.loads(photos_data)
                # Jeśli klient przesłał dane, użyj ich do określenia kolejności
                if client_photos:
                    # Sortuj według kolejności z klienta
                    all_photos.sort(key=lambda x: next((p['order'] for p in client_photos if p['url'] == x['url']), 999))
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Zapisz zaktualizowane zdjęcia
        setattr(obj, field_name, all_photos)
        obj.save(update_fields=[field_name])

@admin.register(Dog)
class DogAdmin(BasePhotoAdmin):
    list_display = ['name', 'breed', 'gender', 'birth_date', 'is_breeding', 'main_photo', 'photos_count', 'certificates_count']
    list_filter = ['breed', 'gender', 'is_breeding', 'birth_date']
    search_fields = ['name', 'breed', 'description']
    list_editable = ['is_breeding']
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name', 'breed', 'gender', 'birth_date', 'is_breeding', 'description')
        }),
        ('Zdjęcia', {
            'fields': ('photos_manager',),
            'classes': ('wide',)
        }),
        ('Certyfikaty', {
            'fields': ('certificates_manager',),
            'classes': ('wide',)
        }),
    )
    
    def main_photo(self, obj):
        if obj.photos and len(obj.photos) > 0:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />', 
                             obj.photos[0].get('url', ''))
        return "Brak"
    main_photo.short_description = "Główne zdjęcie"
    
    def photos_count(self, obj):
        return len(obj.photos) if obj.photos else 0
    photos_count.short_description = "Zdjęcia"
    
    def certificates_count(self, obj):
        return len(obj.certificates) if obj.certificates else 0
    certificates_count.short_description = "Certyfikaty"

@admin.register(Puppy)
class PuppyAdmin(BasePhotoAdmin):
    list_display = ['name', 'mother', 'father', 'birth_date', 'gender', 'is_available', 'price', 'main_photo', 'photos_count', 'certificates_count']
    list_filter = ['gender', 'is_available', 'birth_date']
    search_fields = ['name', 'mother__name', 'father__name']
    list_editable = ['is_available', 'price']
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name', 'mother', 'father', 'birth_date', 'gender', 'description')
        }),
        ('Dostępność', {
            'fields': ('is_available', 'price')
        }),
        ('Zdjęcia', {
            'fields': ('photos_manager',),
            'classes': ('wide',)
        }),
        ('Certyfikaty', {
            'fields': ('certificates_manager',),
            'classes': ('wide',)
        }),
    )
    
    def main_photo(self, obj):
        if obj.photos and len(obj.photos) > 0:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />', 
                             obj.photos[0].get('url', ''))
        return "Brak"
    main_photo.short_description = "Główne zdjęcie"
    
    def photos_count(self, obj):
        return len(obj.photos) if obj.photos else 0
    photos_count.short_description = "Zdjęcia"
    
    def certificates_count(self, obj):
        return len(obj.certificates) if obj.certificates else 0
    certificates_count.short_description = "Certyfikaty"

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