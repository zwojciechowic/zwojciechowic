// Obsługa dwujęzycznych pól w panelu administracyjnym Django

(function($) {
    'use strict';

    // Funkcja inicjalizująca dwujęzyczne pola
    function initBilingualFields() {
        // Znajdź wszystkie pola z dwujęzycznymi odpowiednikami
        const bilingualPairs = [
            ['title', 'title_en'],
            ['excerpt', 'excerpt_en'],
            ['description', 'description_en'],
            ['main_title', 'main_title_en'],
            ['quote_text', 'quote_text_en'],
            ['content', 'content_en']
        ];

        bilingualPairs.forEach(pair => {
            const [plField, enField] = pair;
            setupBilingualField(plField, enField);
        });
    }

    // Konfiguracja pojedynczej pary pól
    function setupBilingualField(plFieldName, enFieldName) {
        const plField = $(`#id_${plFieldName}`);
        const enField = $(`#id_${enFieldName}`);
        
        if (plField.length && enField.length) {
            // Utwórz kontener dla obu pól
            const container = createBilingualContainer(plField, enField, plFieldName, enFieldName);
            
            // Zastąp oryginalne pole kontenerem
            plField.closest('.form-row, .field-box').replaceWith(container);
            
            // Ukryj oryginalną sekcję pola angielskiego jeśli istnieje
            enField.closest('.form-row, .field-box').hide();
            
            // Dodaj synchronizację slug jeśli to pole title
            if (plFieldName === 'title') {
                setupSlugSync(plField, enField);
            }
        }
    }

    // Tworzenie kontenera dla dwujęzycznych pól
    function createBilingualContainer(plField, enField, plFieldName, enFieldName) {
        const plLabel = plField.closest('.form-row, .field-box').find('label').first().text() || plField.attr('placeholder') || 'Polski';
        const enLabel = enField.closest('.form-row, .field-box').find('label').first().text() || enField.attr('placeholder') || 'English';
        
        // Klonuj pola aby zachować wszystkie atrybuty
        const plFieldClone = plField.clone().attr('id', `id_${plFieldName}_bilingual_pl`);
        const enFieldClone = enField.clone().attr('id', `id_${enFieldName}_bilingual_en`);
        
        // Dodaj klasy CSS
        plFieldClone.addClass('bilingual-field-pl');
        enFieldClone.addClass('bilingual-field-en');
        
        // Synchronizuj wartości
        plFieldClone.val(plField.val());
        enFieldClone.val(enField.val());
        
        const container = $(`
            <div class="form-row field-${plFieldName}">
                <div>
                    <label class="required">${plLabel}</label>
                    <div class="bilingual-container">
                        <div class="bilingual-field-wrapper language-indicator" data-lang="PL">
                            <label class="bilingual-label">🇵🇱 Polski:</label>
                            <div class="bilingual-field-content"></div>
                        </div>
                        <div class="bilingual-field-wrapper language-indicator" data-lang="EN">
                            <label class="bilingual-label">🇬🇧 English:</label>
                            <div class="bilingual-field-content"></div>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        // Wstaw pola do odpowiednich kontenerów
        container.find('.bilingual-field-wrapper:first .bilingual-field-content').append(plFieldClone);
        container.find('.bilingual-field-wrapper:last .bilingual-field-content').append(enFieldClone);
        
        // Dodaj event listenery dla synchronizacji
        plFieldClone.on('input change', function() {
            plField.val($(this).val()).trigger('change');
        });
        
        enFieldClone.on('input change', function() {
            enField.val($(this).val()).trigger('change');
        });
        
        // Synchronizacja wsteczna
        plField.on('change', function() {
            plFieldClone.val($(this).val());
        });
        
        enField.on('change', function() {
            enFieldClone.val($(this).val());
        });
        
        return container;
    }

    // Synchronizacja slug dla tytułów
    function setupSlugSync(plTitleField, enTitleField) {
        const slugField = $('#id_slug');
        const slugEnField = $('#id_slug_en');
        
        if (slugField.length) {
            // Funkcja tworzenia slug z polskich znaków
            function createSlug(text) {
                const polishChars = {
                    'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
                    'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
                    'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
                    'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
                };
                
                return text
                    .replace(/[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]/g, match => polishChars[match] || match)
                    .toLowerCase()
                    .replace(/[^\w\s-]/g, '')
                    .replace(/[\s_-]+/g, '-')
                    .replace(/^-+|-+$/g, '');
            }
            
            // Auto-generuj slug dla polskiego tytułu
            plTitleField.on('input', function() {
                if (!slugField.val() || slugField.val() === createSlug(plTitleField.val())) {
                    const newSlug = createSlug($(this).val());
                    slugField.val(newSlug);
                }
            });
            
            // Auto-generuj slug_en dla angielskiego tytułu
            if (slugEnField.length) {
                enTitleField.on('input', function() {
                    if (!slugEnField.val() || slugEnField.val() === createSlug(enTitleField.val())) {
                        const newSlug = createSlug($(this).val());
                        slugEnField.val(newSlug);
                    }
                });
            }
        }
    }

    // Obsługa inline formularzy (dla BlogSection, AboutSection)
    function initInlineBilingualFields() {
        // Obsługa istniejących inline formularzy
        $('.inline-group .form-row').each(function() {
            const row = $(this);
            setupInlineRow(row);
        });
        
        // Obsługa nowych inline formularzy (po kliknięciu "Add another")
        $(document).on('formset:added', function(event, $row) {
            setupInlineRow($row);
        });
    }

    function setupInlineRow($row) {
        const titleField = $row.find('input[name$="-title"]');
        const titleEnField = $row.find('input[name$="-title_en"]');
        const contentField = $row.find('textarea[name$="-content"]');
        const contentEnField = $row.find('textarea[name$="-content_en"]');
        
        if (titleField.length && titleEnField.length) {
            createInlineBilingualPair(titleField, titleEnField, 'Tytuł');
        }
        
        if (contentField.length && contentEnField.length) {
            createInlineBilingualPair(contentField, contentEnField, 'Treść');
        }
    }

    function createInlineBilingualPair(plField, enField, labelText) {
        const container = $(`
            <div class="bilingual-inline-container">
                <label>${labelText}</label>
                <div class="bilingual-container">
                    <div class="bilingual-field-wrapper">
                        <label class="bilingual-label">🇵🇱 Polski:</label>
                        <div class="pl-field-container"></div>
                    </div>
                    <div class="bilingual-field-wrapper">
                        <label class="bilingual-label">🇬🇧 English:</label>
                        <div class="en-field-container"></div>
                    </div>
                </div>
            </div>
        `);
        
        // Przenieś pola do nowego kontenera
        container.find('.pl-field-container').append(plField);
        container.find('.en-field-container').append(enField);
        
        // Znajdź i zastąp oryginalny kontener
        const originalContainer = plField.closest('.field-box, td');
        originalContainer.replaceWith(container);
        
        // Ukryj pole angielskie jeśli było w osobnej komórce
        enField.closest('td').hide();
    }

    // Inicjalizacja po załadowaniu DOM
    $(document).ready(function() {
        initBilingualFields();
        initInlineBilingualFields();
        
        // Dodaj przycisk do przełączania widoczności pól angielskich
        addLanguageToggle();
    });

    // Przycisk do pokazywania/ukrywania pól angielskich
    function addLanguageToggle() {
        const toggleButton = $(`
            <div style="margin: 10px 0; padding: 10px; background: #f0f0f0; border-radius: 5px;">
                <button type="button" id="toggle-english-fields" class="button" style="margin-right: 10px;">
                    <span class="toggle-text">Pokaż pola angielskie</span>
                </button>
                <small>Kliknij aby pokazać/ukryć wszystkie pola do wprowadzania treści w języku angielskim</small>
            </div>
        `);
        
        // Wstaw przycisk na początku formularza
        $('.submit-row').before(toggleButton);
        
        let englishFieldsVisible = false;
        
        $('#toggle-english-fields').click(function() {
            englishFieldsVisible = !englishFieldsVisible;
            
            if (englishFieldsVisible) {
                $('.bilingual-field-wrapper:last-child').show();
                $('.collapse').removeClass('collapsed');
                $(this).find('.toggle-text').text('Ukryj pola angielskie');
            } else {
                $('.bilingual-field-wrapper:last-child').hide();
                $('.collapse:not(.collapsed)').addClass('collapsed');
                $(this).find('.toggle-text').text('Pokaż pola angielskie');
            }
        });
        
        // Domyślnie ukryj pola angielskie
        $('.bilingual-field-wrapper:last-child').hide();
    }

})(django.jQuery);