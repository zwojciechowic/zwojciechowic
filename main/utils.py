# utils.py - Pomocnicze funkcje dla obsługi tłumaczeń

from django.utils.translation import get_language

def get_translated_field(obj, field_name, language=None):
    """
    Zwraca wartość pola w odpowiednim języku.
    
    Args:
        obj: Obiekt modelu
        field_name: Nazwa pola bazowego (np. 'title')
        language: Kod języka ('pl' lub 'en'). Jeśli None, użyje aktualnego języka.
    
    Returns:
        str: Wartość pola w odpowiednim języku lub wartość domyślna
    """
    if language is None:
        language = get_language()
    
    # Mapowanie kodów języków Django na sufiksy pól
    lang_map = {
        'pl': '',           # Pola bez sufiksu to wersja polska
        'pl-pl': '',        
        'en': '_en',        # Pola z _en to wersja angielska
        'en-us': '_en',
        'en-gb': '_en',
    }
    
    suffix = lang_map.get(language.lower(), '')
    
    # Nazwa pola z odpowiednim sufiksem
    translated_field_name = f"{field_name}{suffix}"
    
    # Sprawdź czy pole istnieje
    if hasattr(obj, translated_field_name):
        value = getattr(obj, translated_field_name)
        
        # Jeśli pole tłumaczenia jest puste, wróć do wersji domyślnej
        if not value and suffix:
            value = getattr(obj, field_name, '')
        
        return value
    
    # Fallback do oryginalnego pola
    return getattr(obj, field_name, '')

def get_translated_content(obj, language=None):
    """
    Zwraca pełną treść dla obiektów z sekcjami (BlogPost, AboutPage).
    
    Args:
        obj: Obiekt BlogPost lub AboutPage
        language: Kod języka
    
    Returns:
        str: Skonkatenowana treść wszystkich sekcji
    """
    if not hasattr(obj, 'sections'):
        return ''
    
    if language is None:
        language = get_language()
    
    sections_content = []
    
    for section in obj.sections.all():
        title = get_translated_field(section, 'title', language)
        content = get_translated_field(section, 'content', language)
        
        if title:
            sections_content.append(f"<h3>{title}</h3>")
        if content:
            sections_content.append(content)
    
    return "\n\n".join(sections_content)

# Mixiny dla modeli
class TranslatableModelMixin:
    """
    Mixin dla modeli z polami tłumaczalnymi.
    Dodaje metody get_FIELD_NAME do automatycznego zwracania wartości w odpowiednim języku.
    """
    
    TRANSLATABLE_FIELDS = []  # Lista pól do przetłumaczenia - należy zdefiniować w modelu
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_translation_methods()
    
    def _add_translation_methods(self):
        """Automatycznie dodaje metody get_FIELD_NAME dla każdego pola tłumaczalnego"""
        for field_name in self.TRANSLATABLE_FIELDS:
            if not hasattr(self, f'get_{field_name}'):
                setattr(self, f'get_{field_name}', 
                       lambda language=None, fn=field_name: get_translated_field(self, fn, language))

# Template tags dla łatwego użycia w szablonach
def register_translation_tags():
    """
    Funkcja do zarejestrowania custom template tags.
    Umieść w pliku templatetags/translation_tags.py:
    """
    template_tags_code = '''
from django import template
from django.utils.translation import get_language
from ..utils import get_translated_field, get_translated_content

register = template.Library()

@register.simple_tag
def translated_field(obj, field_name, language=None):
    """Template tag do pobierania przetłumaczonego pola"""
    return get_translated_field(obj, field_name, language)

@register.simple_tag
def translated_content(obj, language=None):
    """Template tag do pobierania pełnej treści z sekcjami"""
    return get_translated_content(obj, language)

@register.filter
def translate_field(obj, field_name):
    """Filter do tłumaczenia pola based on current language"""
    return get_translated_field(obj, field_name)

# Przykład użycia w szablonie:
# {% load translation_tags %}
# 
# {% translated_field blog_post "title" %}
# {% translated_field blog_post "title" "en" %}
# {{ blog_post|translate_field:"description" }}
# {% translated_content blog_post %}
'''
    return template_tags_code

# Funkcje pomocnicze dla API/JSON responses
def serialize_translatable_object(obj, translatable_fields, language=None):
    """
    Serializuje obiekt z polami tłumaczalnymi do słownika.
    
    Args:
        obj: Obiekt do serializacji
        translatable_fields: Lista pól tłumaczalnych
        language: Kod języka
    
    Returns:
        dict: Słownik z przetłumaczonymi polami
    """
    result = {}
    
    for field in translatable_fields:
        result[field] = get_translated_field(obj, field, language)
    
    return result

# Context processor dla szablonów
def translation_context_processor(request):
    """
    Context processor dodający funkcje tłumaczeniowe do kontekstu szablonów.
    
    Dodaj do TEMPLATES['OPTIONS']['context_processors'] w settings.py:
    'myapp.utils.translation_context_processor'
    """
    return {
        'get_translated_field': get_translated_field,
        'get_translated_content': get_translated_content,
        'current_language': get_language(),
    }

# Przykłady użycia w views.py:
"""
from django.shortcuts import render
from django.utils.translation import get_language
from .models import BlogPost
from .utils import get_translated_field

def blog_post_detail(request, slug):
    language = get_language()
    
    # Znajdź wpis po odpowiednim slug
    if language.startswith('en'):
        try:
            post = BlogPost.objects.get(slug_en=slug)
        except BlogPost.DoesNotExist:
            post = BlogPost.objects.get(slug=slug)
    else:
        post = BlogPost.objects.get(slug=slug)
    
    # Pobierz przetłumaczone dane
    context = {
        'post': post,
        'title': get_translated_field(post, 'title', language),
        'excerpt': get_translated_field(post, 'excerpt', language),
        'content': get_translated_content(post, language),
    }
    
    return render(request, 'blog/post_detail.html', context)
"""