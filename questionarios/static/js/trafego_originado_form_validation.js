document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(event) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('input[required], select[required]');
        
        requiredFields.forEach(function(field) {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('is-invalid');
            } else {
                field.classList.remove('is-invalid');
            }
        });

        const numberFields = form.querySelectorAll('input[type="number"]');
        numberFields.forEach(function(field) {
            if (field.value && parseInt(field.value) < 0) {
                isValid = false;
                field.classList.add('is-invalid');
                alert('Os valores numéricos não podem ser negativos.');
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Por favor, preencha todos os campos obrigatórios corretamente.');
        }
    });

    // Validação em tempo real
    const numberInputs = form.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.value < 0) {
                this.classList.add('is-invalid');
                let feedbackElement = this.nextElementSibling;
                if (!feedbackElement || !feedbackElement.classList.contains('invalid-feedback')) {
                    feedbackElement = document.createElement('div');
                    feedbackElement.classList.add('invalid-feedback');
                    this.parentNode.insertBefore(feedbackElement, this.nextSibling);
                }
                feedbackElement.textContent = 'O valor não pode ser negativo.';
            } else {
                this.classList.remove('is-invalid');
                let feedbackElement = this.nextElementSibling;
                if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
                    feedbackElement.textContent = '';
                }
            }
        });
    });

    // Função para formatar números grandes
    function formatLargeNumber(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    // Aplicar formatação aos campos numéricos
    const largeNumberInputs = form.querySelectorAll('.large-number');
    largeNumberInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value) {
                const formattedValue = formatLargeNumber(this.value);
                this.value = formattedValue;
            }
        });

        input.addEventListener('focus', function() {
            this.value = this.value.replace(/\./g, '');
        });
    });
});