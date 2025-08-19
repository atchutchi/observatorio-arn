from django.db import models
from django.conf import settings
from .base import IndicadorBase

class EstacoesMoveisIndicador(IndicadorBase):
    # Serviços de Mobile Money
    numero_utilizadores = models.IntegerField(verbose_name="Número de Utilizadores", 
                                             help_text="Número total de utilizadores do serviço de Mobile Money",
                                             default=0)
    numero_utilizadores_mulher = models.IntegerField(verbose_name="Utilizadores Mulheres", default=0)
    numero_utilizadores_homem = models.IntegerField(verbose_name="Utilizadores Homens", default=0)

    total_carregamentos = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_carregamentos_mulher = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_carregamentos_homem = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    total_levantamentos = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_levantamentos_mulher = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_levantamentos_homem = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    total_transferencias = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_transferencias_mulher = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_transferencias_homem = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    # Utilizadores de serviço básicos
    sms = models.IntegerField(verbose_name="SMS", default=0)
    mms = models.IntegerField(verbose_name="MMS", null=True, blank=True)
    mobile_tv = models.IntegerField(verbose_name="Mobile TV", null=True, blank=True)
    roaming_internacional_out_parc_roaming_out = models.IntegerField(
        verbose_name="Roaming Internacional Out", default=0)

    # Banda larga (3G + 4G) - Secção 3G
    utilizadores_servico_3g_upgrades = models.IntegerField(
        verbose_name="Utilizadores de serviço de 3G e upgrades", 
        default=0,
        help_text="Utilizadores de serviço de 3G e upgrades"
    )
    utilizadores_acesso_internet_3g = models.IntegerField(
        verbose_name="Utilizadores acesso Internet banda larga (3G)", 
        default=0,
        help_text="Utilizadores de serviço de acesso à Internet em banda larga (3G)"
    )
    utilizadores_3g_placas_box = models.IntegerField(
        verbose_name="3G - Placas (Box)", 
        default=0,
        help_text="dos quais com ligação através de Placas (Box) - 3G"
    )
    utilizadores_3g_placas_usb = models.IntegerField(
        verbose_name="3G - Placas (USB)", 
        default=0,
        help_text="dos quais com ligação através de Placas (USB) - 3G"
    )

    # Banda larga (3G + 4G) - Secção 4G
    utilizadores_servico_4g = models.IntegerField(
        verbose_name="Utilizadores de serviço de 4G", 
        default=0,
        help_text="Utilizadores de serviço de 4G"
    )
    utilizadores_acesso_internet_4g = models.IntegerField(
        verbose_name="Utilizadores acesso Internet banda larga (4G)", 
        default=0,
        help_text="Utilizadores do serviço de acesso à Internet em banda larga (4G)"
    )
    utilizadores_4g_placas_box = models.IntegerField(
        verbose_name="4G - Placas (Box)", 
        default=0,
        help_text="dos quais com ligação através de Placas (Box) - 4G"
    )
    utilizadores_4g_placas_usb = models.IntegerField(
        verbose_name="4G - Placas (USB)", 
        default=0,
        help_text="dos quais com ligação através de Placas (USB) - 4G"
    )

    # Número total de estações móveis activos
    afectos_planos_pos_pagos = models.IntegerField(default=0)
    afectos_planos_pos_pagos_utilizacao = models.IntegerField(default=0)
    afectos_planos_pre_pagos = models.IntegerField(default=0)
    afectos_planos_pre_pagos_utilizacao = models.IntegerField(default=0)
    associados_situacoes_especificas = models.IntegerField(null=True, blank=True)
    outros_residuais = models.IntegerField(null=True, blank=True)

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='estacoes_moveis_criadas')
    atualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='estacoes_moveis_atualizadas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def calcular_total_utilizadores(self):
        return self.numero_utilizadores

    def calcular_total_carregamentos(self):
        return self.total_carregamentos

    def calcular_total_levantamentos(self):
        return self.total_levantamentos

    def calcular_total_transferencias(self):
        return self.total_transferencias

    def calcular_total_3g(self):
        """Calcula o total de utilizadores 3G"""
        return (self.utilizadores_servico_3g_upgrades + 
                self.utilizadores_acesso_internet_3g)

    def calcular_total_4g(self):
        """Calcula o total de utilizadores 4G"""
        return (self.utilizadores_servico_4g + 
                self.utilizadores_acesso_internet_4g)

    def calcular_total_banda_larga(self):
        """Calcula o total de utilizadores banda larga (3G + 4G)"""
        return self.calcular_total_3g() + self.calcular_total_4g()

    def calcular_total_estacoes_moveis(self):
        return (self.afectos_planos_pos_pagos + 
                self.afectos_planos_pre_pagos + 
                (self.associados_situacoes_especificas or 0) + 
                (self.outros_residuais or 0))

    def __str__(self):
        return f"Estações Móveis e Mobile Money - {self.operadora} - {self.ano}/{self.mes}"

    def save(self, *args, **kwargs):
        # Salva no Django
        super().save(*args, **kwargs)
        # Salva no Supabase
        self.save_to_supabase('estacoes_moveis')
        
    def delete(self, *args, **kwargs):
        # Deleta do Supabase
        self.delete_from_supabase('estacoes_moveis')
        # Deleta do Django
        super().delete(*args, **kwargs)

    class Meta:
        unique_together = ('ano', 'mes', 'operadora')
        verbose_name = "Estações Móveis"
        verbose_name_plural = "Estações Móveis"