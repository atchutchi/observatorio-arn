from django.db import models
from django.conf import settings
from .base import IndicadorBase

class TrafegoOriginadoIndicador(IndicadorBase):
    # Tráfego de Dados 3G e upgrade
    trafego_dados_3g_upgrade = models.BigIntegerField(help_text="Em Mbit/s")
    internet_3g = models.BigIntegerField(help_text="Em Mbit")
    internet_3g_placas_modem = models.BigIntegerField(help_text="Em Mbit")
    internet_3g_modem_usb = models.BigIntegerField(help_text="Em Mbit")

    # Tráfego de Dados 4G
    trafego_dados_4g = models.BigIntegerField(help_text="Em Mbit/s")
    internet_4g = models.BigIntegerField(help_text="Em Mbyte (Mo)")
    internet_4g_placas_modem = models.BigIntegerField(help_text="Em Mbyte (Mo)")
    internet_4g_modem_usb = models.BigIntegerField(help_text="Em Mbyte (Mo)")

    # Tráfego de Dados das redes 2G
    trafego_dados_2g = models.BigIntegerField(help_text="Em Sessões")

    # Tráfego de Dados das redes 3G e upgrade
    trafego_dados_3g_upgrade_sessoes = models.BigIntegerField(help_text="Em Sessões")
    internet_3g_sessoes = models.BigIntegerField(help_text="Em Sessões")
    internet_3g_placas_modem_sessoes = models.BigIntegerField(help_text="Em Sessões")
    internet_3g_modem_usb_sessoes = models.BigIntegerField(help_text="Em Sessões")

    # Tráfego de Mensagens
    sms_total = models.BigIntegerField(help_text="Número de mensagens enviadas")
    sms_on_net = models.BigIntegerField()
    sms_off_net = models.BigIntegerField()
    sms_internacional = models.BigIntegerField()
    sms_cedeao = models.BigIntegerField()
    sms_palop = models.BigIntegerField()
    sms_cplp = models.BigIntegerField()
    sms_resto_africa = models.BigIntegerField()
    sms_resto_mundo = models.BigIntegerField()

    # Volume de Tráfegos de Voz
    voz_total = models.BigIntegerField(help_text="Em minutos")
    voz_on_net = models.BigIntegerField(help_text="Em minutos")
    voz_off_net = models.BigIntegerField(help_text="Em minutos")
    voz_telecel = models.BigIntegerField(help_text="Em minutos")
    voz_internacional = models.BigIntegerField(help_text="Em minutos")
    voz_cedeao = models.BigIntegerField(help_text="Em minutos")
    voz_cplp = models.BigIntegerField(help_text="Em minutos")
    voz_palop = models.BigIntegerField(help_text="Em minutos")
    voz_resto_africa = models.BigIntegerField(help_text="Em minutos")
    voz_resto_mundo = models.BigIntegerField(help_text="Em minutos")

    # Número de Comunicações de Voz
    chamadas_total = models.BigIntegerField(help_text="Número de chamadas")
    chamadas_on_net = models.BigIntegerField()
    chamadas_off_net = models.BigIntegerField()
    chamadas_telecel = models.BigIntegerField()
    chamadas_internacional = models.BigIntegerField()
    chamadas_cedeao = models.BigIntegerField()
    chamadas_cplp = models.BigIntegerField()
    chamadas_palop = models.BigIntegerField()
    chamadas_resto_africa = models.BigIntegerField()
    chamadas_resto_mundo = models.BigIntegerField()

    # Campos adicionais
    operador_movel_b = models.BigIntegerField(null=True, blank=True)
    operador_rede_fixa = models.BigIntegerField(null=True, blank=True)
    numeros_curtos = models.BigIntegerField(null=True, blank=True)

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='trafego_originado_criado')
    atualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='trafego_originado_atualizado')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def calcular_total_dados_3g(self):
        return self.trafego_dados_3g_upgrade + self.internet_3g + self.internet_3g_placas_modem + self.internet_3g_modem_usb

    def calcular_total_dados_4g(self):
        return self.trafego_dados_4g + self.internet_4g + self.internet_4g_placas_modem + self.internet_4g_modem_usb

    def calcular_total_sms(self):
        return (self.sms_on_net + self.sms_off_net + self.sms_internacional + 
                self.sms_cedeao + self.sms_palop + self.sms_cplp + 
                self.sms_resto_africa + self.sms_resto_mundo)

    def calcular_total_voz(self):
        return (self.voz_on_net + self.voz_off_net + self.voz_telecel + 
                self.voz_internacional + self.voz_cedeao + self.voz_cplp + 
                self.voz_palop + self.voz_resto_africa + self.voz_resto_mundo)

    def calcular_total_chamadas(self):
        return (self.chamadas_on_net + self.chamadas_off_net + self.chamadas_telecel + 
                self.chamadas_internacional + self.chamadas_cedeao + self.chamadas_cplp + 
                self.chamadas_palop + self.chamadas_resto_africa + self.chamadas_resto_mundo)


    def __str__(self):
        return f"Tráfego Originado - {self.ano}/{self.mes}"

    class Meta:
        unique_together = ('ano', 'mes', 'operadora')