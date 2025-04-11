document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form.needs-validation');
    
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });

    const numberInputs = form.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.value < 0) {
                this.value = 0;
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

    const decimalInputs = form.querySelectorAll('input[type="text"][step="0.01"]');
    decimalInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9.]/g, '');
            if (this.value.split('.').length > 2) {
                this.value = this.value.replace(/\.+$/, '');
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