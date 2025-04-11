# dashboard/views/reports.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, Count, Avg
import csv

from questionarios.models import (
   EstacoesMoveisIndicador,
   TrafegoOriginadoIndicador, 
   TrafegoTerminadoIndicador,
   TrafegoRoamingInternacionalIndicador,
   LBIIndicador,
   TrafegoInternetIndicador,
   InternetFixoIndicador,
   TarifarioVozMTNIndicador,
   TarifarioVozOrangeIndicador,
   ReceitasIndicador,
   EmpregoIndicador,
   InvestimentoIndicador
)

class ReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
   template_name = 'dashboard/reports.html'
   
   def test_func(self):
       return self.request.user.is_staff
   
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       year = self.request.GET.get('year', timezone.now().year)
       
       context.update({
           'estacoes_moveis': self.get_mobile_stats(year),
           'trafego': self.get_traffic_stats(year),
           'internet': self.get_internet_stats(year),
           'receitas': self.get_revenue_stats(year),
           'anos_disponiveis': self.get_available_years(),
           'ano_selecionado': year
       })
       return context

   def get_mobile_stats(self, year):
       estacoes = EstacoesMoveisIndicador.objects.filter(ano=year)
       return {
           'total_assinantes': estacoes.aggregate(total=Sum('total_assinantes')),
           'por_operadora': {
               'mtn': estacoes.filter(operadora='MTN').aggregate(
                   total=Sum('total_assinantes')
               ),
               'orange': estacoes.filter(operadora='ORANGE').aggregate(
                   total=Sum('total_assinantes')
               )
           },
           'crescimento': self.calcular_crescimento(EstacoesMoveisIndicador, year, 'total_assinantes')
       }

   def get_traffic_stats(self, year):
       trafego_terminado = TrafegoTerminadoIndicador.objects.filter(ano=year)
       trafego_originado = TrafegoOriginadoIndicador.objects.filter(ano=year)
       
       return {
           'onnet': {
               'mtn': trafego_originado.filter(operadora='MTN').aggregate(
                   total=Sum('chamadas_on_net')
               ),
               'orange': trafego_originado.filter(operadora='ORANGE').aggregate(
                   total=Sum('chamadas_on_net')
               )
           },
           'offnet': {
               'mtn': trafego_originado.filter(operadora='MTN').aggregate(
                   total=Sum('chamadas_off_net')
               ),
               'orange': trafego_originado.filter(operadora='ORANGE').aggregate(
                   total=Sum('chamadas_off_net')
               )
           },
           'internacional': {
               'entrada': trafego_terminado.aggregate(
                   total=Sum('chamadas_internacionais')
               ),
               'saida': trafego_originado.aggregate(
                   total=Sum('chamadas_internacionais')
               )
           }
       }

   def get_internet_stats(self, year):
       return {
           '3g': LBIIndicador.objects.filter(
               ano=year, 
               tecnologia='3G'
           ).aggregate(total=Sum('total_assinantes')),
           '4g': LBIIndicador.objects.filter(
               ano=year, 
               tecnologia='4G'
           ).aggregate(total=Sum('total_assinantes')),
           'trafego': TrafegoInternetIndicador.objects.filter(
               ano=year
           ).aggregate(total=Sum('trafego_total'))
       }

   def get_revenue_stats(self, year):
       receitas = ReceitasIndicador.objects.filter(ano=year)
       return {
           'total': receitas.aggregate(total=Sum('receita_total')),
           'por_operadora': {
               'mtn': receitas.filter(operadora='MTN').aggregate(
                   total=Sum('receita_total')
               ),
               'orange': receitas.filter(operadora='ORANGE').aggregate(
                   total=Sum('receita_total')
               )
           },
           'crescimento': self.calcular_crescimento(ReceitasIndicador, year, 'receita_total')
       }

   def get_available_years(self):
       years = set()
       models = [
           EstacoesMoveisIndicador,
           TrafegoOriginadoIndicador,
           ReceitasIndicador
       ]
       for model in models:
           years.update(model.objects.values_list('ano', flat=True).distinct())
       return sorted(years, reverse=True)

   def calcular_crescimento(self, model, year, field):
       ano_atual = model.objects.filter(ano=year).aggregate(total=Sum(field))['total'] or 0
       ano_anterior = model.objects.filter(ano=year-1).aggregate(total=Sum(field))['total'] or 0
       
       if ano_anterior == 0:
           return 0
       return ((ano_atual - ano_anterior) / ano_anterior) * 100

class ExportReportView(LoginRequiredMixin, UserPassesTestMixin, View):
   def test_func(self):
       return self.request.user.is_staff
   
   def get(self, request, *args, **kwargs):
       year = request.GET.get('year', timezone.now().year)
       report_type = request.GET.get('type', 'completo')
       
       response = HttpResponse(content_type='text/csv')
       response['Content-Disposition'] = f'attachment; filename="relatorio_mercado_{year}_{report_type}.csv"'
       
       writer = csv.writer(response)
       self.write_report(writer, year, report_type)
       
       return response
       
   def write_report(self, writer, year, report_type):
       if report_type == 'estacoes':
           self.write_mobile_report(writer, year)
       elif report_type == 'trafego':
           self.write_traffic_report(writer, year)
       else:
           self.write_full_report(writer, year)
           
   def write_mobile_report(self, writer, year):
       writer.writerow(['Relatório de Estações Móveis', year])
       writer.writerow(['Operadora', 'Total Assinantes', 'Quota de Mercado (%)'])
       
       estacoes = EstacoesMoveisIndicador.objects.filter(ano=year)
       total = estacoes.aggregate(total=Sum('total_assinantes'))['total'] or 0
       
       for operadora in ['MTN', 'ORANGE']:
           subtotal = estacoes.filter(operadora=operadora).aggregate(
               total=Sum('total_assinantes')
           )['total'] or 0
           
           writer.writerow([
               operadora,
               subtotal,
               round(subtotal/total * 100, 2) if total > 0 else 0
           ])
           
   def write_traffic_report(self, writer, year):
       writer.writerow(['Relatório de Tráfego', year])
       writer.writerow(['Tipo', 'MTN', 'Orange', 'Total'])
       
       trafego = TrafegoOriginadoIndicador.objects.filter(ano=year)
       
       # On-Net
       onnet_mtn = trafego.filter(operadora='MTN').aggregate(
           total=Sum('chamadas_on_net')
       )['total'] or 0
       onnet_orange = trafego.filter(operadora='ORANGE').aggregate(
           total=Sum('chamadas_on_net')
       )['total'] or 0
       
       writer.writerow([
           'Tráfego On-Net',
           onnet_mtn,
           onnet_orange,
           onnet_mtn + onnet_orange
       ])
       
       # Continue with Off-Net and International traffic...
           
   def write_full_report(self, writer, year):
       self.write_mobile_report(writer, year)
       writer.writerow([])  # Empty row for separation
       self.write_traffic_report(writer, year)