// related-animal-click.js - Wersja z debugiem
document.addEventListener('DOMContentLoaded', function() {
    console.log('🐕 Related animal script loaded');
    
    const relatedAnimalLinks = document.querySelectorAll('.related-animal-info a');
    console.log('🔍 Found related animal links:', relatedAnimalLinks.length);
    
    relatedAnimalLinks.forEach((link, index) => {
        console.log(`🔗 Setting up link ${index + 1}:`, link.href);
        
        link.addEventListener('click', function(e) {
            console.log('🖱️ Link clicked!', this.href);
            
            // Zapobiegnij natychmiastowemu przejściu
            e.preventDefault();
            e.stopPropagation();
            
            // Dodaj klasę clicked do linku
            this.classList.add('clicked');
            console.log('✅ Added clicked class');
            
            // Zapisz docelowy URL
            const targetUrl = this.href;
            
            // Wizualny feedback w konsoli
            console.log('⏱️ Waiting 700ms before redirect...');
            
            // Po opóźnieniu przejdź do linku
            setTimeout(() => {
                console.log('🚀 Redirecting to:', targetUrl);
                window.location.href = targetUrl;
            }, 700);
            
            // Usuń klasę po czasie (dla bezpieczeństwa)
            setTimeout(() => {
                this.classList.remove('clicked');
                console.log('🧹 Removed clicked class');
            }, 1400);
        });
        
        // Dodaj hover listener dla debugowania
        link.addEventListener('mouseenter', function() {
            console.log('👆 Mouse entered link');
        });
        
        link.addEventListener('mouseleave', function() {
            console.log('👋 Mouse left link');
        });
    });
});