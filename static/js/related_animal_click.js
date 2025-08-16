_// related-animal-click.js - obsługa kliknięcia
document.addEventListener('DOMContentLoaded', function() {
    const relatedAnimalElements = document.querySelectorAll('.related-animal-info .text-muted');
    
    relatedAnimalElements.forEach(element => {
        element.addEventListener('click', function(e) {
            // Dodaj klasę clicked
            this.classList.add('clicked');
            
            // Usuń klasę po 1.4s (0.7s opóźnienie + 0.7s trwanie)
            setTimeout(() => {
                this.classList.remove('clicked');
            }, 1400);
            
            // Opcjonalnie: zapobiegnij domyślnemu zachowaniu linku na 0.7s
            e.preventDefault();
            
            // Po opóźnieniu przejdź do linku (jeśli to link)
            const link = this.closest('a');
            if (link) {
                setTimeout(() => {
                    if (!e.defaultPrevented) {
                        window.location.href = link.href;
                    }
                }, 700);
            }
        });
    });
});