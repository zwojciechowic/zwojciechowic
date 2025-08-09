# Generated migration to fix slug_en field
from django.db import migrations, models
from django.utils.text import slugify

def populate_slug_en(apps, schema_editor):
    """
    Wypełnia puste slug_en wartościami na podstawie slug lub title
    """
    BlogPost = apps.get_model('main', 'BlogPost')
    
    for post in BlogPost.objects.all():
        if not post.slug_en:  # Jeśli slug_en jest pusty
            if post.title_en:
                # Jeśli istnieje title_en, użyj go do stworzenia slug_en
                base_slug = slugify(post.title_en)
            else:
                # Jeśli nie ma title_en, użyj slug + '-en'
                base_slug = f"{post.slug}-en"
            
            # Upewnij się, że slug jest unikalny
            slug_en = base_slug
            counter = 1
            while BlogPost.objects.filter(slug_en=slug_en).exists():
                slug_en = f"{base_slug}-{counter}"
                counter += 1
            
            post.slug_en = slug_en
            post.save()

def reverse_populate_slug_en(apps, schema_editor):
    """
    Operacja odwrotna - usuwa wypełnione slug_en (na wypadek rollback)
    """
    BlogPost = apps.get_model('main', 'BlogPost')
    BlogPost.objects.update(slug_en=None)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_aboutpage_main_title_en_aboutpage_quote_text_en_and_more'),
    ]

    operations = [
        # Krok 1: Wypełnij puste slug_en
        migrations.RunPython(
            populate_slug_en,
            reverse_populate_slug_en,
        ),
        
        # Krok 2: Zmień pole na non-nullable i unique
        migrations.AlterField(
            model_name='blogpost',
            name='slug_en',
            field=models.SlugField(unique=True, verbose_name='URL (slug) (EN)', blank=True),
        ),
    ]