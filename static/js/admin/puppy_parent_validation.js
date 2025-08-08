document.addEventListener('DOMContentLoaded', function() {
    // Walidacja dla matki
    const motherSelect = document.getElementById('id_mother');
    const motherNameInput = document.getElementById('id_mother_name');
    
    // Walidacja dla ojca
    const fatherSelect = document.getElementById('id_father');
    const fatherNameInput = document.getElementById('id_father_name');
    
    function validateParentFields(selectField, textField, parentName) {
        if (!selectField || !textField) return;
        
        function updateFields() {
            if (selectField.value && textField.value) {
                // Oba pola wypełnione - wyświetl ostrzeżenie
                textField.style.border = '2px solid #dc3545';
                selectField.style.border = '2px solid #dc3545';
                
                // Dodaj komunikat ostrzeżenia jeśli nie istnieje
                let warningId = `warning-${parentName}`;
                if (!document.getElementById(warningId)) {
                    let warning = document.createElement('div');
                    warning.id = warningId;
                    warning.style.color = '#dc3545';
                    warning.style.fontSize = '12px';
                    warning.style.marginTop = '5px';
                    warning.innerHTML = `⚠️ Wypełniono oba pola dla ${parentName}. Wybierz TYLKO jedno.`;
                    textField.parentNode.appendChild(warning);
                }
            } else {
                // Usunij ostrzeżenia
                textField.style.border = '';
                selectField.style.border = '';
                let warning = document.getElementById(`warning-${parentName}`);
                if (warning) warning.remove();
            }
        }
        
        selectField.addEventListener('change', updateFields);
        textField.addEventListener('input', updateFields);
        
        // Sprawdź na starcie
        updateFields();
    }
    
    // Zastosuj walidację
    validateParentFields(motherSelect, motherNameInput, 'matki');
    validateParentFields(fatherSelect, fatherNameInput, 'ojca');
});