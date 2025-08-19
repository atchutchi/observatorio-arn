from django import forms
from ..models.estacoes_moveis import EstacoesMoveisIndicador

class EstacoesMoveisForm(forms.ModelForm):
    class Meta:
        model = EstacoesMoveisIndicador
        fields = [
            # Dados básicos
            'ano', 'mes', 'operadora',
            
            # Mobile Money
            'numero_utilizadores', 'numero_utilizadores_mulher', 'numero_utilizadores_homem',
            'total_carregamentos', 'total_carregamentos_mulher', 'total_carregamentos_homem',
            'total_levantamentos', 'total_levantamentos_mulher', 'total_levantamentos_homem',
            'total_transferencias', 'total_transferencias_mulher', 'total_transferencias_homem',
            
            # Utilizadores de serviço básicos
            'sms', 'mms', 'mobile_tv', 'roaming_internacional_out_parc_roaming_out',
            
            # Banda larga 3G
            'utilizadores_servico_3g_upgrades',
            'utilizadores_acesso_internet_3g',
            'utilizadores_3g_placas_box',
            'utilizadores_3g_placas_usb',
            
            # Banda larga 4G
            'utilizadores_servico_4g',
            'utilizadores_acesso_internet_4g',
            'utilizadores_4g_placas_box',
            'utilizadores_4g_placas_usb',
            
            # Estações móveis ativas
            'afectos_planos_pos_pagos', 'afectos_planos_pos_pagos_utilizacao',
            'afectos_planos_pre_pagos', 'afectos_planos_pre_pagos_utilizacao',
            'associados_situacoes_especificas', 'outros_residuais'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona a classe form-control para todos os campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Select)):
                field.widget.attrs['class'] = 'form-control'
                
        # Configurações específicas dos campos
        self.fields['ano'].widget.attrs.update({'class': 'form-control'})
        self.fields['mes'].widget.attrs.update({'class': 'form-control'})
        self.fields['operadora'].widget.attrs.update({'class': 'form-control'})
        
        # Adiciona placeholders e configurações especiais
        numero_fields = [
            'numero_utilizadores', 'numero_utilizadores_mulher', 'numero_utilizadores_homem',
            'sms', 'mms', 'mobile_tv', 'roaming_internacional_out_parc_roaming_out',
            'utilizadores_servico_3g_upgrades', 'utilizadores_acesso_internet_3g',
            'utilizadores_3g_placas_box', 'utilizadores_3g_placas_usb',
            'utilizadores_servico_4g', 'utilizadores_acesso_internet_4g',
            'utilizadores_4g_placas_box', 'utilizadores_4g_placas_usb',
            'afectos_planos_pos_pagos', 'afectos_planos_pos_pagos_utilizacao',
            'afectos_planos_pre_pagos', 'afectos_planos_pre_pagos_utilizacao',
            'associados_situacoes_especificas', 'outros_residuais'
        ]
        
        for field_name in numero_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'placeholder': '0',
                    'min': '0'
                })
        
        # Campos decimais (valores monetários)
        decimal_fields = [
            'total_carregamentos', 'total_carregamentos_mulher', 'total_carregamentos_homem',
            'total_levantamentos', 'total_levantamentos_mulher', 'total_levantamentos_homem',
            'total_transferencias', 'total_transferencias_mulher', 'total_transferencias_homem'
        ]
        
        for field_name in decimal_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'placeholder': '0.00',
                    'step': '0.01',
                    'min': '0'
                })