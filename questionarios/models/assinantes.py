from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import IndicadorBase


class AssinantesIndicador(IndicadorBase):
    """
    Modelo para armazenar indicadores relacionados a assinantes dos serviços de telecomunicações.
    """
    # Assinantes de telefonia móvel
    assinantes_pre_pago = models.IntegerField(
        verbose_name=_("Assinantes pré-pago"),
        help_text=_("Número de assinantes de serviços móveis pré-pagos"),
        null=True, blank=True,
        default=0
    )
    assinantes_pos_pago = models.IntegerField(
        verbose_name=_("Assinantes pós-pago"),
        help_text=_("Número de assinantes de serviços móveis pós-pagos"),
        null=True, blank=True,
        default=0
    )
    
    # Assinantes de telefonia fixa
    assinantes_fixo = models.IntegerField(
        verbose_name=_("Assinantes de telefonia fixa"),
        help_text=_("Número total de assinantes de telefonia fixa"),
        null=True, blank=True,
        default=0
    )
    
    # Assinantes de internet
    assinantes_internet_movel = models.IntegerField(
        verbose_name=_("Assinantes de internet móvel"),
        help_text=_("Número de assinantes de internet móvel"),
        null=True, blank=True,
        default=0
    )
    assinantes_internet_fixa = models.IntegerField(
        verbose_name=_("Assinantes de internet fixa"),
        help_text=_("Número de assinantes de internet fixa"),
        null=True, blank=True,
        default=0
    )
    
    class Meta:
        verbose_name = _("Indicador de Assinantes")
        verbose_name_plural = _("Indicadores de Assinantes") 