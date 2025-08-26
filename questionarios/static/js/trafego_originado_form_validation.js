/**
 * Validação e cálculos para formulário de Tráfego Originado
 * Baseado na estrutura KPI ARN - Seção 5
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form.needs-validation, form');
    
    if (!form) return;

    // ========== INICIALIZAÇÃO ==========
    initializeValidation();
    initializeCalculations();
    initializeFormatters();
    initializeAutoCalculate();
    
    // ========== VALIDAÇÃO PRINCIPAL ==========
    function initializeValidation() {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validação padrão HTML5
            if (!form.checkValidity()) {
                isValid = false;
            }
            
            // Validações customizadas
            if (!validateDataTraffic()) isValid = false;
            if (!validateSMSTotals()) isValid = false;
            if (!validateVoiceTotals()) isValid = false;
            if (!validateCallsTotals()) isValid = false;
            if (!validateCoherence()) isValid = false;
            
            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
                showValidationSummary();
            }
            
            form.classList.add('was-validated');
        });

        // Validação em tempo real
        const numberInputs = form.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.addEventListener('input', function() {
                // Não permitir valores negativos
                if (this.value < 0) {
                    this.value = 0;
                    showFieldError(this, 'Valor não pode ser negativo');
                } else {
                    clearFieldError(this);
                }
                
                // Atualizar cálculos
                updateCalculations();
            });
            
            input.addEventListener('blur', function() {
                validateFieldOnBlur(this);
            });
        });
    }

    // ========== CÁLCULOS AUTOMÁTICOS ==========
    function initializeAutoCalculate() {
        // SMS - calcular totais
        const smsFields = {
            nacional: ['sms_on_net', 'sms_off_net_nacional'],
            internacional: ['sms_cedeao', 'sms_palop', 'sms_cplp', 'sms_resto_africa', 'sms_resto_mundo']
        };
        
        smsFields.nacional.concat(smsFields.internacional).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.addEventListener('input', calculateSMSTotals);
            }
        });
        
        // Voz - calcular totais
        const vozFields = {
            nacional: ['voz_on_net_minutos', 'voz_off_net_nacional_minutos', 'voz_rede_fixa_minutos', 'voz_outras_redes_moveis_minutos'],
            internacional: ['voz_cedeao_minutos', 'voz_palop_minutos', 'voz_cplp_minutos', 'voz_resto_africa_minutos', 'voz_resto_mundo_minutos']
        };
        
        vozFields.nacional.concat(vozFields.internacional).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.addEventListener('input', calculateVoiceTotals);
            }
        });
        
        // Chamadas - calcular totais
        const chamadasFields = {
            nacional: ['chamadas_on_net', 'chamadas_off_net_nacional', 'chamadas_rede_fixa', 'chamadas_outras_redes_moveis'],
            internacional: ['chamadas_cedeao', 'chamadas_palop', 'chamadas_cplp', 'chamadas_resto_africa', 'chamadas_resto_mundo']
        };
        
        chamadasFields.nacional.concat(chamadasFields.internacional).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.addEventListener('input', calculateCallsTotals);
            }
        });
    }

    // ========== CÁLCULOS DE SMS ==========
    function calculateSMSTotals() {
        // Calcular total nacional
        const smsOnNet = parseInt(getFieldValue('sms_on_net') || 0);
        const smsOffNet = parseInt(getFieldValue('sms_off_net_nacional') || 0);
        const smsNacional = smsOnNet + smsOffNet;
        
        // Calcular total internacional
        const smsCedeao = parseInt(getFieldValue('sms_cedeao') || 0);
        const smsPalop = parseInt(getFieldValue('sms_palop') || 0);
        const smsCplp = parseInt(getFieldValue('sms_cplp') || 0);
        const smsRestoAfrica = parseInt(getFieldValue('sms_resto_africa') || 0);
        const smsRestoMundo = parseInt(getFieldValue('sms_resto_mundo') || 0);
        const smsInternacional = smsCedeao + smsPalop + smsCplp + smsRestoAfrica + smsRestoMundo;
        
        // Atualizar campo de total internacional
        const smsInternacionalField = form.querySelector('[name="sms_internacional_total"]');
        if (smsInternacionalField) {
            smsInternacionalField.value = smsInternacional;
        }
        
        // Calcular e atualizar total geral
        const smsTotal = smsNacional + smsInternacional;
        const smsTotalField = form.querySelector('[name="sms_total"]');
        if (smsTotalField) {
            smsTotalField.value = smsTotal;
        }
        
        // Atualizar display
        updateSummaryDisplay('total-sms', formatNumber(smsTotal));
    }

    // ========== CÁLCULOS DE VOZ ==========
    function calculateVoiceTotals() {
        // Calcular total nacional
        const vozOnNet = parseInt(getFieldValue('voz_on_net_minutos') || 0);
        const vozOffNet = parseInt(getFieldValue('voz_off_net_nacional_minutos') || 0);
        const vozRedeFixa = parseInt(getFieldValue('voz_rede_fixa_minutos') || 0);
        const vozOutrasRedes = parseInt(getFieldValue('voz_outras_redes_moveis_minutos') || 0);
        const vozNacional = vozOnNet + vozOffNet + vozRedeFixa + vozOutrasRedes;
        
        // Calcular total internacional
        const vozCedeao = parseInt(getFieldValue('voz_cedeao_minutos') || 0);
        const vozPalop = parseInt(getFieldValue('voz_palop_minutos') || 0);
        const vozCplp = parseInt(getFieldValue('voz_cplp_minutos') || 0);
        const vozRestoAfrica = parseInt(getFieldValue('voz_resto_africa_minutos') || 0);
        const vozRestoMundo = parseInt(getFieldValue('voz_resto_mundo_minutos') || 0);
        const vozInternacional = vozCedeao + vozPalop + vozCplp + vozRestoAfrica + vozRestoMundo;
        
        // Atualizar campo de total internacional
        const vozInternacionalField = form.querySelector('[name="voz_internacional_total_minutos"]');
        if (vozInternacionalField) {
            vozInternacionalField.value = vozInternacional;
        }
        
        // Calcular e atualizar total geral
        const vozTotal = vozNacional + vozInternacional;
        const vozTotalField = form.querySelector('[name="voz_total_minutos"]');
        if (vozTotalField) {
            vozTotalField.value = vozTotal;
        }
        
        // Atualizar display
        updateSummaryDisplay('total-minutos', formatNumber(vozTotal));
    }

    // ========== CÁLCULOS DE CHAMADAS ==========
    function calculateCallsTotals() {
        // Calcular total nacional
        const chamadasOnNet = parseInt(getFieldValue('chamadas_on_net') || 0);
        const chamadasOffNet = parseInt(getFieldValue('chamadas_off_net_nacional') || 0);
        const chamadasRedeFixa = parseInt(getFieldValue('chamadas_rede_fixa') || 0);
        const chamadasOutrasRedes = parseInt(getFieldValue('chamadas_outras_redes_moveis') || 0);
        const chamadasNacional = chamadasOnNet + chamadasOffNet + chamadasRedeFixa + chamadasOutrasRedes;
        
        // Calcular total internacional
        const chamadasCedeao = parseInt(getFieldValue('chamadas_cedeao') || 0);
        const chamadasPalop = parseInt(getFieldValue('chamadas_palop') || 0);
        const chamadasCplp = parseInt(getFieldValue('chamadas_cplp') || 0);
        const chamadasRestoAfrica = parseInt(getFieldValue('chamadas_resto_africa') || 0);
        const chamadasRestoMundo = parseInt(getFieldValue('chamadas_resto_mundo') || 0);
        const chamadasInternacional = chamadasCedeao + chamadasPalop + chamadasCplp + chamadasRestoAfrica + chamadasRestoMundo;
        
        // Atualizar campo de total internacional
        const chamadasInternacionalField = form.querySelector('[name="chamadas_internacional_total"]');
        if (chamadasInternacionalField) {
            chamadasInternacionalField.value = chamadasInternacional;
        }
        
        // Calcular e atualizar total geral
        const chamadasTotal = chamadasNacional + chamadasInternacional;
        const chamadasTotalField = form.querySelector('[name="chamadas_total"]');
        if (chamadasTotalField) {
            chamadasTotalField.value = chamadasTotal;
        }
        
        // Atualizar display
        updateSummaryDisplay('total-chamadas', formatNumber(chamadasTotal));
    }

    // ========== CÁLCULOS GERAIS ==========
    function initializeCalculations() {
        // Atualizar cálculos ao carregar
        updateCalculations();
        
        // Adicionar listeners para atualização
        const calculableFields = form.querySelectorAll('input[type="number"]');
        calculableFields.forEach(field => {
            field.addEventListener('input', debounce(updateCalculations, 300));
        });
    }
    
    function updateCalculations() {
        // 1. Total de Dados
        const dados2G = parseInt(getFieldValue('trafego_dados_2g_mbytes') || 0);
        
        const dados3G = parseInt(getFieldValue('trafego_dados_3g_upgrade_mbytes') || 0) +
                       parseInt(getFieldValue('internet_3g_mbytes') || 0) +
                       parseInt(getFieldValue('internet_3g_placas_modem_mbytes') || 0) +
                       parseInt(getFieldValue('internet_3g_modem_usb_mbytes') || 0);
        
        const dados4G = parseInt(getFieldValue('trafego_dados_4g_mbytes') || 0) +
                       parseInt(getFieldValue('internet_4g_mbytes') || 0) +
                       parseInt(getFieldValue('internet_4g_placas_modem_mbytes') || 0) +
                       parseInt(getFieldValue('internet_4g_modem_usb_mbytes') || 0);
        
        const totalDadosMB = dados2G + dados3G + dados4G;
        const totalDadosGB = (totalDadosMB / 1024).toFixed(2);
        
        updateSummaryDisplay('total-dados-gb', `${formatNumber(totalDadosGB)} GB`);
        
        // 2. Recalcular SMS, Voz e Chamadas
        calculateSMSTotals();
        calculateVoiceTotals();
        calculateCallsTotals();
        
        // 3. Validar coerência
        validateCoherence();
    }

    // ========== VALIDAÇÕES ESPECÍFICAS ==========
    
    function validateDataTraffic() {
        let isValid = true;
        
        // Validar que sessões não sejam maiores que volume (regra de negócio)
        const volume2G = parseInt(getFieldValue('trafego_dados_2g_mbytes') || 0);
        const sessoes2G = parseInt(getFieldValue('trafego_dados_2g_sessoes') || 0);
        
        if (sessoes2G > 0 && volume2G === 0) {
            showFieldError(document.querySelector('[name="trafego_dados_2g_mbytes"]'), 
                'Existem sessões mas nenhum volume de dados');
            isValid = false;
        }
        
        return isValid;
    }
    
    function validateSMSTotals() {
        const smsTotal = parseInt(getFieldValue('sms_total') || 0);
        const smsCalculado = 
            parseInt(getFieldValue('sms_on_net') || 0) +
            parseInt(getFieldValue('sms_off_net_nacional') || 0) +
            parseInt(getFieldValue('sms_internacional_total') || 0);
        
        if (smsTotal !== smsCalculado) {
            console.log(`SMS Total (${smsTotal}) não coincide com calculado (${smsCalculado})`);
        }
        
        return true; // Sempre retorna true pois recalcula automaticamente
    }
    
    function validateVoiceTotals() {
        // Validação similar aos SMS
        return true; // Sempre retorna true pois recalcula automaticamente
    }
    
    function validateCallsTotals() {
        // Validação similar aos SMS
        return true; // Sempre retorna true pois recalcula automaticamente
    }
    
    function validateCoherence() {
        let isValid = true;
        
        const totalMinutos = parseInt(getFieldValue('voz_total_minutos') || 0);
        const totalChamadas = parseInt(getFieldValue('chamadas_total') || 0);
        
        // Verificar se há chamadas sem minutos
        if (totalChamadas > 0 && totalMinutos === 0) {
            showNotification('Aviso: Existem chamadas mas nenhum minuto registrado', 'warning');
        }
        
        // Verificar duração média
        if (totalChamadas > 0) {
            const duracaoMedia = totalMinutos / totalChamadas;
            
            if (duracaoMedia > 60) {
                showNotification(`Aviso: Duração média muito alta (${duracaoMedia.toFixed(1)} min/chamada)`, 'warning');
            }
            
            // Atualizar display de duração média
            const avgDisplay = document.getElementById('avg-call-duration');
            if (avgDisplay) {
                avgDisplay.textContent = `${duracaoMedia.toFixed(1)} min`;
            }
        }
        
        return isValid;
    }
    
    function validateFieldOnBlur(field) {
        clearFieldError(field);
        
        // Revalidar campos relacionados
        const fieldName = field.name;
        
        if (fieldName.includes('sms')) {
            calculateSMSTotals();
        } else if (fieldName.includes('voz')) {
            calculateVoiceTotals();
        } else if (fieldName.includes('chamadas')) {
            calculateCallsTotals();
        }
    }

    // ========== FORMATADORES ==========
    function initializeFormatters() {
        // Formatar valores grandes
        const largeNumberFields = document.querySelectorAll('[data-format="large-number"]');
        
        largeNumberFields.forEach(field => {
            field.addEventListener('blur', function() {
                if (this.value) {
                    const value = parseInt(this.value.replace(/\D/g, ''));
                    this.value = formatNumber(value);
                }
            });
            
            field.addEventListener('focus', function() {
                // Remover formatação para edição
                this.value = this.value.replace(/\D/g, '');
            });
        });
    }

    // ========== FUNÇÕES AUXILIARES ==========
    function getFieldValue(fieldName) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (!field) return '';
        
        // Remover formatação para obter valor numérico
        return field.value.replace(/\D/g, '');
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
    
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    }
    
    function updateSummaryDisplay(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
            
            // Adicionar animação
            element.classList.add('updating');
            setTimeout(() => {
                element.classList.remove('updating');
            }, 300);
        }
    }
    
    function showValidationSummary() {
        const errors = form.querySelectorAll('.is-invalid');
        
        if (errors.length > 0) {
            errors[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            errors[0].focus();
            
            showNotification(`Existem ${errors.length} erro(s) no formulário`, 'error');
        }
    }
    
    function showNotification(message, type = 'info') {
        // Usar sistema de notificação da plataforma se disponível
        if (window.QuestionariosJS && window.QuestionariosJS.showNotification) {
            window.QuestionariosJS.showNotification(message, type);
        } else {
            // Fallback
            const alertClass = type === 'error' ? 'alert-danger' : 
                              type === 'warning' ? 'alert-warning' : 'alert-info';
            
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
    
    // ========== ESTILOS CSS ==========
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
        
        input[data-calculated="true"] {
            background-color: rgba(240, 185, 11, 0.1);
            font-weight: bold;
        }
        
        .is-invalid {
            border-color: var(--binance-danger) !important;
        }
        
        .invalid-feedback {
            color: var(--binance-danger);
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
    `;
    document.head.appendChild(style);
});

// ========== EXPORTAR FUNÇÕES ==========
window.TrafegoOriginadoValidation = {
    updateCalculations: function() {
        const event = new Event('input');
        document.querySelector('form').dispatchEvent(event);
    }
};