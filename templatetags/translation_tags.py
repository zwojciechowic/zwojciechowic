# templatetags/translation_tags.py

from django import template
from django.utils.translation import get_language
from django.utils.safestring import mark_safe

register = template.Library()

def get_translated_field(obj, field_name, language=None):
    """
    Zwraca wartość pola w odpowiednim języku.
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

@register.simple_tag
def translated_field(obj, field_name, language=None):
    """
    Template tag do pobierania przetłumaczonego pola.
    
    Użycie:
    {% translated_field blog_post "title" %}
    {% translated_field blog_post "title" "en" %}
    """
    return get_translated_field(obj, field_name, language)

@register.simple_tag
def translated_content(obj, language=None):
    """
    Template tag do pobierania pełnej treści z sekcjami.
    
    Użycie:
    {% translated_content blog_post %}
    {% translated_content about_page "en" %}
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
    
    return mark_safe("\n\n".join(sections_content))

@register.filter
def translate_field(obj, field_name):
    """
    Filter do tłumaczenia pola bazując na aktualnym języku.
    
    Użycie:
    {{ blog_post|translate_field:"title" }}
    {{ dog|translate_field:"description" }}
    """
    return get_translated_field(obj, field_name)

@register.simple_tag
def get_language_code():
    """
    Zwraca aktualny kod języka.
    
    Użycie:
    {% get_language_code as current_lang %}
    """
    return get_language()

@register.simple_tag
def is_english():
    """
    Sprawdza czy aktualny język to angielski.
    
    Użycie:
    {% is_english as is_en %}
    {% if is_en %}English content{% endif %}
    """
    return get_language().startswith('en')

@register.simple_tag
def field_exists(obj, field_name):
    """
    Sprawdza czy obiekt ma określone pole.
    
    Użycie:
    {% field_exists blog_post "title_en" as has_en_title %}
    """
    return hasattr(obj, field_name)

@register.inclusion_tag('admin/bilingual_field_widget.html', takes_context=True)
def bilingual_field_widget(context, field_name, label=""):
    """
    Inclusion tag dla wyświetlania dwujęzycznego widgetu w szablonach.
    
    Użycie:
    {% bilingual_field_widget "title" "Tytuł" %}
    """
    obj = context.get('object') or context.get('instance')
    
    if not obj:
        return {}
    
    pl_value = getattr(obj, field_name, '')
    en_value = getattr(obj, f"{field_name}_en", '')
    
    return {
        'field_name': field_name,
        'label': label or field_name.title(),
        'pl_value': pl_value,
        'en_value': en_value,
        'current_language': get_language(),
    }

@register.simple_tag
def translate_choice(choices, value, language=None):
    """
    Tłumaczy wartość wyboru z listy choices.
    Przydatne dla pól z choices jak gender, status itp.
    
    Użycie:
    {% translate_choice DOG_GENDER_CHOICES dog.gender %}
    """
    if language is None:
        language = get_language()
    
    for choice_value, choice_label in choices:
        if choice_value == value:
            # Tu można dodać mapowanie tłumaczeń dla choices
            # Na razie zwraca oryginalną etykietę
            return choice_label
    
    return value

# Template tag do generowania linków językowych
@register.simple_tag(takes_context=True)
def language_url(context, language_code):
    """
    Generuje URL dla tej samej strony w innym języku.
    
    Użycie:
    {% language_url "en" as english_url %}
    <a href="{{ english_url }}">English</a>
    """
    request = context['request']
    current_path = request.get_full_path()
    
    # Usuń obecny prefix językowy z URL
    path_parts = current_path.split('/')
    if len(path_parts) > 1 and path_parts[1] in ['pl', 'en']:
        path_parts[1] = language_code
    else:
        path_parts.insert(1, language_code)
    
    return '/'.join(path_parts)

@register.simple_tag
def get_available_languages():
    """
    Zwraca listę dostępnych języków.
    
    Użycie:
    {% get_available_languages as languages %}
    {% for lang in languages %}...{% endfor %}
    """
    from django.conf import settings
    return getattr(settings, 'LANGUAGES', [('pl', 'Polski'), ('en', 'English')])

# Przykład szablonu do inclusion_tag bilingual_field_widget:
"""
<!-- templates/admin/bilingual_field_widget.html -->
<div class="bilingual-widget">
    <div class="field-wrapper">
        <label>🇵🇱 {{ label }} (Polski):</label>
        <div class="field-value">{{ pl_value|default:"Brak tłumaczenia" }}</div>
    </div>
    <div class="field-wrapper">
        <label>🇬🇧 {{ label }} (English):</label>
        <div class="field-value">{{ en_value|default:"No translation" }}</div>
    </div>
</div>
"""