/**
 * Validação e cálculos para formulário de Estações Móveis
 * Baseado na estrutura KPI ARN
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form.needs-validation, form');
    
    if (!form) return;

    // ========== INICIALIZAÇÃO ==========
    initializeValidation();
    initializeCalculations();
    initializeFormatters();
    initializeAutoSave();
    
    // ========== VALIDAÇÃO PRINCIPAL ==========
    function initializeValidation() {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validação padrão HTML5
            if (!form.checkValidity()) {
                isValid = false;
            }
            
            // Validações customizadas
            if (!validateMobileMoney()) isValid = false;
            if (!validateBandaLarga()) isValid = false;
            if (!validateEstacoesMoveisLogica()) isValid = false;
            
            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
                showValidationSummary();
            }
            
            form.classList.add('was-validated');
        });

        // Validação em tempo real para campos numéricos
        const numberInputs = form.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.addEventListener('input', function() {
                // Não permitir valores negativos
                if (this.value < 0) {
                    this.value = 0;
                    showFieldError(this, 'Valor não pode ser negativo');
                }
                
                // Atualizar cálculos
                updateCalculations();
            });
            
            input.addEventListener('blur', function() {
                validateFieldOnBlur(this);
            });
        });

        // Validação em tempo real para campos decimais (Mobile Money)
        const decimalInputs = form.querySelectorAll('[name*="carregamentos"], [name*="levantamentos"], [name*="transferencias"]');
        decimalInputs.forEach(input => {
            input.addEventListener('input', function() {
                // Formatar para aceitar apenas números e ponto decimal
                let value = this.value.replace(/[^0-9.]/g, '');
                
                // Permitir apenas um ponto decimal
                const parts = value.split('.');
                if (parts.length > 2) {
                    value = parts[0] + '.' + parts.slice(1).join('');
                }
                
                // Limitar a 2 casas decimais
                if (parts[1] && parts[1].length > 2) {
                    value = parts[0] + '.' + parts[1].substring(0, 2);
                }
                
                this.value = value;
                updateCalculations();
            });
        });
    }

    // ========== VALIDAÇÕES ESPECÍFICAS ==========
    
    // 1. Validação de Mobile Money
    function validateMobileMoney() {
        let isValid = true;
        const errors = [];
        
        // Obter valores
        const totalUtilizadores = parseInt(getFieldValue('numero_utilizadores') || 0);
        const utilizadoresMulher = parseInt(getFieldValue('numero_utilizadores_mulher') || 0);
        const utilizadoresHomem = parseInt(getFieldValue('numero_utilizadores_homem') || 0);
        
        // Validar soma de gêneros
        if ((utilizadoresMulher + utilizadoresHomem) > totalUtilizadores) {
            errors.push('Soma de utilizadores por gênero excede o total');
            showFieldError(document.querySelector('[name="numero_utilizadores_homem"]'), 
                'Soma por gênero excede total');
            isValid = false;
        }
        
        // Validar carregamentos
        const totalCarregamentos = parseFloat(getFieldValue('total_carregamentos') || 0);
        const carregamentosMulher = parseFloat(getFieldValue('total_carregamentos_mulher') || 0);
        const carregamentosHomem = parseFloat(getFieldValue('total_carregamentos_homem') || 0);
        
        if (Math.abs((carregamentosMulher + carregamentosHomem) - totalCarregamentos) > 0.01) {
            errors.push('Soma de carregamentos por gênero não coincide com total');
            showFieldError(document.querySelector('[name="total_carregamentos_homem"]'), 
                'Soma não coincide com total');
            isValid = false;
        }
        
        // Validar levantamentos
        const totalLevantamentos = parseFloat(getFieldValue('total_levantamentos') || 0);
        const levantamentosMulher = parseFloat(getFieldValue('total_levantamentos_mulher') || 0);
        const levantamentosHomem = parseFloat(getFieldValue('total_levantamentos_homem') || 0);
        
        if (Math.abs((levantamentosMulher + levantamentosHomem) - totalLevantamentos) > 0.01) {
            errors.push('Soma de levantamentos por gênero não coincide com total');
            showFieldError(document.querySelector('[name="total_levantamentos_homem"]'), 
                'Soma não coincide com total');
            isValid = false;
        }
        
        // Validar transferências
        const totalTransferencias = parseFloat(getFieldValue('total_transferencias') || 0);
        const transferenciasMulher = parseFloat(getFieldValue('total_transferencias_mulher') || 0);
        const transferenciasHomem = parseFloat(getFieldValue('total_transferencias_homem') || 0);
        
        if (Math.abs((transferenciasMulher + transferenciasHomem) - totalTransferencias) > 0.01) {
            errors.push('Soma de transferências por gênero não coincide com total');
            showFieldError(document.querySelector('[name="total_transferencias_homem"]'), 
                'Soma não coincide com total');
            isValid = false;
        }
        
        if (errors.length > 0) {
            console.log('Erros Mobile Money:', errors);
        }
        
        return isValid;
    }
    
    // 2. Validação de Banda Larga (3G/4G)
    function validateBandaLarga() {
        let isValid = true;
        
        // Validar 3G
        const acesso3G = parseInt(getFieldValue('utilizadores_acesso_internet_3g') || 0);
        const placasBox3G = parseInt(getFieldValue('utilizadores_3g_placas_box') || 0);
        const placasUSB3G = parseInt(getFieldValue('utilizadores_3g_placas_usb') || 0);
        
        if ((placasBox3G + placasUSB3G) > acesso3G && acesso3G > 0) {
            showFieldError(document.querySelector('[name="utilizadores_3g_placas_usb"]'), 
                'Total de placas 3G excede utilizadores de internet 3G');
            isValid = false;
        }
        
        // Validar 4G
        const acesso4G = parseInt(getFieldValue('utilizadores_acesso_internet_4g') || 0);
        const placasBox4G = parseInt(getFieldValue('utilizadores_4g_placas_box') || 0);
        const placasUSB4G = parseInt(getFieldValue('utilizadores_4g_placas_usb') || 0);
        
        if ((placasBox4G + placasUSB4G) > acesso4G && acesso4G > 0) {
            showFieldError(document.querySelector('[name="utilizadores_4g_placas_usb"]'), 
                'Total de placas 4G excede utilizadores de internet 4G');
            isValid = false;
        }
        
        return isValid;
    }
    
    // 3. Validação de Estações Móveis
    function validateEstacoesMoveisLogica() {
        let isValid = true;
        
        // Validar utilizações não excedem totais
        const posPageos = parseInt(getFieldValue('afectos_planos_pos_pagos') || 0);
        const posPagosUtilizacao = parseInt(getFieldValue('afectos_planos_pos_pagos_utilizacao') || 0);
        
        if (posPagosUtilizacao > posPageos) {
            showFieldError(document.querySelector('[name="afectos_planos_pos_pagos_utilizacao"]'), 
                'Utilização não pode exceder total de pós-pagos');
            isValid = false;
        }
        
        const prePageos = parseInt(getFieldValue('afectos_planos_pre_pagos') || 0);
        const prePagosUtilizacao = parseInt(getFieldValue('afectos_planos_pre_pagos_utilizacao') || 0);
        
        if (prePagosUtilizacao > prePageos) {
            showFieldError(document.querySelector('[name="afectos_planos_pre_pagos_utilizacao"]'), 
                'Utilização não pode exceder total de pré-pagos');
            isValid = false;
        }
        
        return isValid;
    }
    
    // ========== CÁLCULOS EM TEMPO REAL ==========
    function initializeCalculations() {
        // Atualizar cálculos ao carregar
        updateCalculations();
        
        // Adicionar listeners para atualização
        const calculableFields = form.querySelectorAll('input[type="number"], input[type="text"]');
        calculableFields.forEach(field => {
            field.addEventListener('input', debounce(updateCalculations, 300));
        });
    }
    
    function updateCalculations() {
        // 1. Total de Estações Móveis
        const totalEstacoes = 
            parseInt(getFieldValue('afectos_planos_pos_pagos') || 0) +
            parseInt(getFieldValue('afectos_planos_pre_pagos') || 0) +
            parseInt(getFieldValue('associados_situacoes_especificas') || 0) +
            parseInt(getFieldValue('outros_residuais') || 0);
        
        updateSummaryDisplay('total-estacoes', formatNumber(totalEstacoes));
        
        // 2. Total Banda Larga (máximo entre 3G e 4G, pois pode haver sobreposição)
        const total3G = parseInt(getFieldValue('utilizadores_servico_3g_upgrades') || 0);
        const total4G = parseInt(getFieldValue('utilizadores_servico_4g') || 0);
        const totalBandaLarga = Math.max(total3G + total4G, 
            parseInt(getFieldValue('utilizadores_acesso_internet_3g') || 0) + 
            parseInt(getFieldValue('utilizadores_acesso_internet_4g') || 0));
        
        updateSummaryDisplay('total-banda-larga', formatNumber(totalBandaLarga));
        
        // 3. Total Mobile Money
        const totalMobileMoney = parseInt(getFieldValue('numero_utilizadores') || 0);
        updateSummaryDisplay('total-mobile-money', formatNumber(totalMobileMoney));
        
        // 4. Total Linhas Alugadas
        const totalLinhas = 
            parseInt(getFieldValue('linhas_64kbit') || 0) +
            parseInt(getFieldValue('linhas_128kbit') || 0) +
            parseInt(getFieldValue('linhas_256kbit') || 0) +
            parseInt(getFieldValue('linhas_512kbit') || 0) +
            parseInt(getFieldValue('linhas_1mbit') || 0) +
            parseInt(getFieldValue('linhas_maior_2mbit') || 0);
        
        updateSummaryDisplay('total-linhas', formatNumber(totalLinhas));
        
        // Atualizar indicadores visuais
        updateVisualIndicators();
    }
    
    // ========== FORMATADORES ==========
    function initializeFormatters() {
        // Formatar valores grandes (milhões/bilhões)
        const largeNumberFields = [
            'afectos_planos_pre_pagos',
            'afectos_planos_pre_pagos_utilizacao',
            'numero_utilizadores',
            'numero_utilizadores_mulher',
            'numero_utilizadores_homem',
            'sms',
            'roaming_internacional_out_parc_roaming_out',
            'utilizadores_servico_3g_upgrades',
            'utilizadores_servico_4g'
        ];
        
        largeNumberFields.forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.addEventListener('blur', function() {
                    if (this.value) {
                        // Formatar com separadores de milhares
                        const value = parseInt(this.value.replace(/\D/g, ''));
                        this.value = formatNumber(value);
                    }
                });
                
                field.addEventListener('focus', function() {
                    // Remover formatação para edição
                    this.value = this.value.replace(/\D/g, '');
                });
            }
        });
        
        // Formatar valores monetários (Mobile Money)
        const moneyFields = document.querySelectorAll('[name*="carregamentos"], [name*="levantamentos"], [name*="transferencias"]');
        moneyFields.forEach(field => {
            field.addEventListener('blur', function() {
                if (this.value) {
                    const value = parseFloat(this.value);
                    this.value = formatMoney(value);
                }
            });
            
            field.addEventListener('focus', function() {
                // Remover formatação para edição
                this.value = this.value.replace(/[^\d.]/g, '');
            });
        });
    }
    
    // ========== AUTO-SAVE ==========
    function initializeAutoSave() {
        let saveTimeout;
        const formId = form.id || 'estacoes-moveis-form';
        
        // Carregar dados salvos se existirem
        loadSavedData();
        
        // Salvar a cada mudança
        form.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                saveFormData();
                showSaveIndicator();
            }, 2000);
        });
        
        // Limpar dados salvos ao submeter com sucesso
        form.addEventListener('submit', function() {
            if (form.checkValidity()) {
                clearSavedData();
            }
        });
    }
    
    function saveFormData() {
        const formData = {};
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            if (input.name) {
                formData[input.name] = input.value;
            }
        });
        
        localStorage.setItem('estacoes_moveis_draft', JSON.stringify(formData));
    }
    
    function loadSavedData() {
        const savedData = localStorage.getItem('estacoes_moveis_draft');
        
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                
                // Perguntar se deseja restaurar
                if (confirm('Dados não salvos foram encontrados. Deseja restaurá-los?')) {
                    Object.keys(data).forEach(key => {
                        const field = form.querySelector(`[name="${key}"]`);
                        if (field) {
                            field.value = data[key];
                        }
                    });
                    
                    updateCalculations();
                    showNotification('Dados restaurados com sucesso', 'info');
                } else {
                    clearSavedData();
                }
            } catch (e) {
                console.error('Erro ao carregar dados salvos:', e);
                clearSavedData();
            }
        }
    }
    
    function clearSavedData() {
        localStorage.removeItem('estacoes_moveis_draft');
    }
    
    // ========== FUNÇÕES AUXILIARES ==========
    function getFieldValue(fieldName) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        return field ? field.value.replace(/\D/g, '') : '';
    }
    
    function showFieldError(field, message) {
        if (!field) return;
        
        field.classList.add('is-invalid');
        
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback d-block';
            field.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    }
    
    function clearFieldError(field) {
        if (!field) return;
        
        field.classList.remove('is-invalid');
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }
    
    function validateFieldOnBlur(field) {
        clearFieldError(field);
        
        // Revalidar campos relacionados
        if (field.name.includes('3g')) {
            validateBandaLarga();
        } else if (field.name.includes('4g')) {
            validateBandaLarga();
        } else if (field.name.includes('utilizadores') || 
                   field.name.includes('carregamentos') || 
                   field.name.includes('levantamentos') || 
                   field.name.includes('transferencias')) {
            validateMobileMoney();
        } else if (field.name.includes('planos')) {
            validateEstacoesMoveisLogica();
        }
    }
    
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    }
    
    function formatMoney(value) {
        return value.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
    
    function updateSummaryDisplay(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
            
            // Adicionar animação de atualização
            element.classList.add('updating');
            setTimeout(() => {
                element.classList.remove('updating');
            }, 300);
        }
    }
    
    function updateVisualIndicators() {
        // Adicionar classes de estado baseadas nos valores
        const totalEstacoes = parseInt(document.getElementById('total-estacoes')?.textContent.replace(/\D/g, '') || 0);
        const totalMobileMoney = parseInt(document.getElementById('total-mobile-money')?.textContent.replace(/\D/g, '') || 0);
        
        // Indicar quando há valores significativos
        if (totalEstacoes > 1000000) {
            document.getElementById('total-estacoes')?.classList.add('text-success', 'fw-bold');
        }
        
        if (totalMobileMoney > 100000) {
            document.getElementById('total-mobile-money')?.classList.add('text-info', 'fw-bold');
        }
    }
    
    function showValidationSummary() {
        const errors = form.querySelectorAll('.is-invalid');
        
        if (errors.length > 0) {
            // Scroll para o primeiro erro
            errors[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            errors[0].focus();
            
            showNotification(`Existem ${errors.length} erro(s) no formulário`, 'error');
        }
    }
    
    function showSaveIndicator() {
        const indicator = document.getElementById('save-indicator') || createSaveIndicator();
        indicator.style.display = 'block';
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 2000);
    }
    
    function createSaveIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'save-indicator';
        indicator.className = 'position-fixed top-0 end-0 m-3 badge bg-success';
        indicator.innerHTML = '<i class="fas fa-check me-1"></i>Rascunho salvo';
        indicator.style.display = 'none';
        indicator.style.zIndex = '9999';
        document.body.appendChild(indicator);
        return indicator;
    }
    
    function showNotification(message, type = 'info') {
        // Usar sistema de notificação da plataforma se disponível
        if (window.QuestionariosJS && window.QuestionariosJS.showNotification) {
            window.QuestionariosJS.showNotification(message, type);
        } else {
            // Fallback para alert
            const alertClass = type === 'error' ? 'alert-danger' : 'alert-info';
            const alert = document.createElement('div');
            alert.className = `alert ${alertClass} position-fixed top-0 start-50 translate-middle-x mt-3`;
            alert.style.zIndex = '9999';
            alert.innerHTML = `
                <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                ${message}
            `;
            document.body.appendChild(alert);
            
            setTimeout(() => {
                alert.remove();
            }, 4000);
        }
    }
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // ========== ESTILOS CSS PARA ANIMAÇÕES ==========
    const style = document.createElement('style');
    style.textContent = `
        .total-summary-item {
            padding: 1rem;
            border-radius: 8px;
            background: var(--binance-dark);
            border: 1px solid var(--binance-border);
            transition: all 0.3s ease;
        }
        
        .total-summary-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .total-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--binance-yellow);
            margin: 0;
        }
        
        .total-value.updating {
            animation: pulse 0.3s ease;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .is-invalid {
            border-color: var(--binance-danger) !important;
        }
        
        .invalid-feedback {
            color: var(--binance-danger);
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        
        #save-indicator {
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
});

// ========== EXPORTAR FUNÇÕES PARA USO EXTERNO ==========
window.EstacoesMoveisValidation = {
    updateCalculations: function() {
        // Permitir atualização externa dos cálculos
        const event = new Event('input');
        document.querySelector('form').dispatchEvent(event);
    }
};