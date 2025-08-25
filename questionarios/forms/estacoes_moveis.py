from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from ..models.estacoes_moveis import EstacoesMoveisIndicador


class EstacoesMoveisForm(forms.ModelForm):
    class Meta:
        model = EstacoesMoveisIndicador
        fields = [
            # Informações básicas
            'operadora', 'ano', 'mes',
            
            # Estações móveis ativas
            'afectos_planos_pos_pagos',
            'afectos_planos_pos_pagos_utilizacao',
            'afectos_planos_pre_pagos',
            'afectos_planos_pre_pagos_utilizacao',
            'associados_situacoes_especificas',
            'outros_residuais',
            
            # Utilizadores de serviços
            'sms',
            'mms',
            'mobile_tv',
            'roaming_internacional_out_parc_roaming_out',
            
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
            
            # Mobile Money
            'numero_utilizadores',
            'numero_utilizadores_mulher',
            'numero_utilizadores_homem',
            'total_carregamentos',
            'total_carregamentos_mulher',
            'total_carregamentos_homem',
            'total_levantamentos',
            'total_levantamentos_mulher',
            'total_levantamentos_homem',
            'total_transferencias',
            'total_transferencias_mulher',
            'total_transferencias_homem',
            
            # Linhas alugadas
            'linhas_64kbit',
            'linhas_128kbit',
            'linhas_256kbit',
            'linhas_512kbit',
            'linhas_1mbit',
            'linhas_maior_2mbit',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes Bootstrap a todos os campos
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'