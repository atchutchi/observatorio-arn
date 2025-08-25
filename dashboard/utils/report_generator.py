"""
Sistema de Geração de Relatórios ARN
Baseado na configuração YAML fornecida
"""
import json
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg, Max, Min
from django.utils import timezone
from questionarios.models import (
    EstacoesMoveisIndicador, AssinantesIndicador, ReceitasIndicador,
    TrafegoOriginadoIndicador, TrafegoTerminadoIndicador,
    TrafegoRoamingInternacionalIndicador, LBIIndicador,
    TrafegoInternetIndicador, InternetFixoIndicador,
    InvestimentoIndicador, EmpregoIndicador
)

class ARNReportGenerator:
    """Gerador principal de relatórios ARN"""
    
    # Mapeamento de modelos por fonte de dados
    DATA_SOURCES = {
        'estacoes_moveis': EstacoesMoveisIndicador,
        'assinantes': AssinantesIndicador,
        'trafego_originado': TrafegoOriginadoIndicador,
        'trafego_terminado': TrafegoTerminadoIndicador,
        'trafego_roaming': TrafegoRoamingInternacionalIndicador,
        'lbi': LBIIndicador,
        'trafego_internet': TrafegoInternetIndicador,
        'internet_fixo': InternetFixoIndicador,
        'receitas': ReceitasIndicador,
        'investimentos': InvestimentoIndicador,
        'empregos': EmpregoIndicador,
    }
    
    # Configuração de cores para operadoras
    OPERATOR_COLORS = {
        'TELECEL': '#DC3545',
        'ORANGE': '#FF6600',
        'TELECEL': '#DC3545',
    }
    
    def __init__(self, year=None, quarter=None):
        self.year = year or timezone.now().year
        self.quarter = quarter
        self.report_data = {}
        
    def generate_market_report(self):
        """Gera relatório completo do mercado"""
        return {
            'panorama_geral': self.get_market_overview(),
            'trafego_voz': self.get_voice_traffic_analysis(),
            'mobile_money': self.get_mobile_money_analysis(),
            'banda_larga': self.get_broadband_analysis(),
            'receitas': self.get_revenue_analysis(),
        }
    
    def get_market_overview(self):
        """Panorama geral do mercado"""
        # Assinantes
        assinantes_data = AssinantesIndicador.objects.filter(ano=self.year)
        
        total_assinantes = assinantes_data.aggregate(
            total=Sum('assinantes_activos')
        )['total'] or 0
        
        # Crescimento
        previous_year_data = AssinantesIndicador.objects.filter(ano=self.year-1)
        previous_total = previous_year_data.aggregate(
            total=Sum('assinantes_activos')
        )['total'] or 0
        
        growth_rate = 0
        if previous_total > 0:
            growth_rate = ((total_assinantes - previous_total) / previous_total) * 100
        
        # Quota de mercado por operadora
        market_share = {}
        for operadora in ['ORANGE', 'TELECEL']:
            operadora_total = assinantes_data.filter(operadora=operadora).aggregate(
                total=Sum('assinantes_activos')
            )['total'] or 0
            
            if total_assinantes > 0:
                market_share[operadora] = (operadora_total / total_assinantes) * 100
            else:
                market_share[operadora] = 0
        
        # Taxa de penetração (assumindo população de 2M)
        penetration_rate = (total_assinantes / 2000000) * 100 if total_assinantes else 0
        
        return {
            'total_assinantes': total_assinantes,
            'crescimento_percentual': round(growth_rate, 2),
            'market_share': market_share,
            'taxa_penetracao': round(penetration_rate, 2),
            'dados_por_operadora': [
                {
                    'operadora': item.operadora,
                    'assinantes': item.assinantes_activos,
                    'percentual': market_share.get(item.operadora, 0)
                }
                for item in assinantes_data.values('operadora').annotate(
                    assinantes_activos=Sum('assinantes_activos')
                )
            ]
        }
    
    def get_voice_traffic_analysis(self):
        """Análise de tráfego de voz"""
        trafego_originado = TrafegoOriginadoIndicador.objects.filter(ano=self.year)
        
        # Volume total por operadora
        traffic_by_operator = {}
        total_traffic = 0
        
        for operadora in ['ORANGE', 'TELECEL']:
            op_data = trafego_originado.filter(operadora=operadora)
            
            on_net = op_data.aggregate(total=Sum('chamadas_on_net'))['total'] or 0
            off_net = op_data.aggregate(total=Sum('chamadas_off_net'))['total'] or 0
            international = op_data.aggregate(total=Sum('chamadas_internacionais'))['total'] or 0
            
            operator_total = on_net + off_net + international
            total_traffic += operator_total
            
            traffic_by_operator[operadora] = {
                'on_net': on_net,
                'off_net': off_net,
                'internacional': international,
                'total': operator_total
            }
        
        # Distribuição por tipo
        total_on_net = sum(op['on_net'] for op in traffic_by_operator.values())
        total_off_net = sum(op['off_net'] for op in traffic_by_operator.values())
        total_international = sum(op['internacional'] for op in traffic_by_operator.values())
        
        distribution = {}
        if total_traffic > 0:
            distribution = {
                'on_net': round((total_on_net / total_traffic) * 100, 1),
                'off_net': round((total_off_net / total_traffic) * 100, 1),
                'internacional': round((total_international / total_traffic) * 100, 1),
            }
        
        return {
            'volume_total': total_traffic,
            'por_operadora': traffic_by_operator,
            'distribuicao_percentual': distribution,
            'evolucao_mensal': self.get_monthly_evolution('trafego_originado')
        }
    
    def get_mobile_money_analysis(self):
        """Análise Mobile Money - dados simulados baseados no exemplo"""
        # Esta implementação seria baseada em dados reais quando disponíveis
        return {
            'carregamentos': {
                'valor_fcfa': 173891000000,
                'numero_transacoes': 45000000,
                'crescimento': 152
            },
            'levantamentos': {
                'valor_fcfa': 174564000000,
                'numero_transacoes': 38000000,
                'crescimento': 235
            },
            'transferencias': {
                'valor_fcfa': 96460000000,
                'numero_transacoes': 12000000,
                'crescimento': 465
            },
            'distribuicao_genero': {
                'mulher': 45,
                'homem': 55
            }
        }
    
    def get_broadband_analysis(self):
        """Análise de banda larga móvel"""
        lbi_data = LBIIndicador.objects.filter(ano=self.year)
        internet_data = TrafegoInternetIndicador.objects.filter(ano=self.year)
        
        # Assinantes por tecnologia
        tech_3g = lbi_data.filter(tecnologia='3G').aggregate(
            total=Sum('total_assinantes')
        )['total'] or 0
        
        tech_4g = lbi_data.filter(tecnologia='4G').aggregate(
            total=Sum('total_assinantes')
        )['total'] or 0
        
        # Tráfego de dados
        traffic_data = internet_data.aggregate(
            download_nacional=Sum('trafego_nacional_download'),
            upload_nacional=Sum('trafego_nacional_upload'),
            download_internacional=Sum('trafego_internacional_download'),
            upload_internacional=Sum('trafego_internacional_upload')
        )
        
        return {
            'assinantes_por_tecnologia': {
                '3G': tech_3g,
                '4G': tech_4g,
                '5G': 0  # Placeholder para futuro
            },
            'trafego_dados': traffic_data,
            'taxa_penetracao_dados': self.calculate_data_penetration(tech_3g + tech_4g)
        }
    
    def get_revenue_analysis(self):
        """Análise de receitas"""
        receitas_data = ReceitasIndicador.objects.filter(ano=self.year)
        
        # Volume de negócios por operadora
        revenue_by_operator = {}
        total_revenue = 0
        
        for operadora in ['ORANGE', 'TELECEL']:
            op_revenue = receitas_data.filter(operadora=operadora).aggregate(
                total=Sum('receita_total')
            )['total'] or 0
            
            revenue_by_operator[operadora] = op_revenue
            total_revenue += op_revenue
        
        # Quota de receitas
        revenue_share = {}
        if total_revenue > 0:
            for operadora, revenue in revenue_by_operator.items():
                revenue_share[operadora] = round((revenue / total_revenue) * 100, 1)
        
        # Evolução anual
        evolution_data = self.get_revenue_evolution()
        
        return {
            'volume_total': total_revenue,
            'por_operadora': revenue_by_operator,
            'quota_receitas': revenue_share,
            'evolucao_anual': evolution_data,
            'crescimento_percentual': self.calculate_revenue_growth()
        }
    
    def get_monthly_evolution(self, data_source):
        """Evolução mensal de um indicador"""
        if data_source not in self.DATA_SOURCES:
            return []
        
        model = self.DATA_SOURCES[data_source]
        
        evolution = []
        for month in range(1, 13):
            monthly_data = model.objects.filter(
                ano=self.year,
                mes=month
            ).aggregate(
                total=Sum('total_assinantes') if hasattr(model, 'total_assinantes') 
                      else Sum('chamadas_on_net')  # Default field
            )
            
            evolution.append({
                'mes': month,
                'valor': monthly_data['total'] or 0
            })
        
        return evolution
    
    def get_revenue_evolution(self):
        """Evolução das receitas nos últimos 5 anos"""
        years = range(self.year - 4, self.year + 1)
        evolution = []
        
        for year in years:
            yearly_revenue = ReceitasIndicador.objects.filter(
                ano=year
            ).aggregate(total=Sum('receita_total'))['total'] or 0
            
            evolution.append({
                'ano': year,
                'receita': yearly_revenue
            })
        
        return evolution
    
    def calculate_data_penetration(self, total_subscribers):
        """Calcula taxa de penetração de dados"""
        # Assumindo população de 2 milhões
        population = 2000000
        return round((total_subscribers / population) * 100, 2) if total_subscribers else 0
    
    def calculate_revenue_growth(self):
        """Calcula crescimento de receita anual"""
        current_revenue = ReceitasIndicador.objects.filter(
            ano=self.year
        ).aggregate(total=Sum('receita_total'))['total'] or 0
        
        previous_revenue = ReceitasIndicador.objects.filter(
            ano=self.year - 1
        ).aggregate(total=Sum('receita_total'))['total'] or 0
        
        if previous_revenue > 0:
            return round(((current_revenue - previous_revenue) / previous_revenue) * 100, 2)
        return 0
    
    def generate_dashboard_data(self):
        """Gera dados para o dashboard executivo"""
        market_data = self.get_market_overview()
        traffic_data = self.get_voice_traffic_analysis()
        revenue_data = self.get_revenue_analysis()
        
        return {
            'kpis_principais': {
                'total_assinantes': {
                    'valor': market_data['total_assinantes'],
                    'variacao': f"+{market_data['crescimento_percentual']}%",
                    'cor': 'verde' if market_data['crescimento_percentual'] > 0 else 'vermelho'
                },
                'taxa_penetracao': {
                    'valor': f"{market_data['taxa_penetracao']}%",
                    'variacao': '+2pp',  # Placeholder
                    'cor': 'azul'
                },
                'volume_trafego': {
                    'valor': f"{traffic_data['volume_total'] / 1000000:.1f}M min",
                    'variacao': '+28%',  # Placeholder
                    'cor': 'verde'
                },
                'receita_total': {
                    'valor': f"{revenue_data['volume_total'] / 1000000:.0f}M FCFA",
                    'variacao': f"+{revenue_data['crescimento_percentual']}%",
                    'cor': 'verde' if revenue_data['crescimento_percentual'] > 0 else 'vermelho'
                }
            },
            'market_share': market_data['market_share'],
            'tendencia_mensal': traffic_data['evolucao_mensal']
        }
    
    def generate_comparative_report(self):
        """Relatório comparativo entre operadoras"""
        market_data = self.get_market_overview()
        traffic_data = self.get_voice_traffic_analysis()
        revenue_data = self.get_revenue_analysis()
        
        comparison = []
        for operadora in ['ORANGE', 'TELECEL']:
            assinantes = next((item['assinantes'] for item in market_data['dados_por_operadora'] 
                             if item['operadora'] == operadora), 0)
            
            comparison.append({
                'operadora': operadora,
                'assinantes': assinantes,
                'market_share': f"{market_data['market_share'].get(operadora, 0):.1f}%",
                'trafego_voz': traffic_data['por_operadora'].get(operadora, {}).get('total', 0),
                'receitas': revenue_data['por_operadora'].get(operadora, 0)
            })
        
        return comparison
    
    def export_to_json(self, data):
        """Exporta dados para JSON"""
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)
    
    def get_chart_config(self, chart_type, data):
        """Configuração padrão para gráficos"""
        base_config = {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {
                    'labels': {
                        'color': '#F0F0F0',
                        'usePointStyle': True,
                        'family': 'Inter'
                    }
                }
            }
        }
        
        if chart_type == 'line':
            base_config['scales'] = {
                'x': {
                    'grid': {'color': '#474D57'},
                    'ticks': {'color': '#F0F0F0', 'font': {'family': 'Inter'}}
                },
                'y': {
                    'grid': {'color': '#474D57'},
                    'ticks': {'color': '#F0F0F0', 'font': {'family': 'Inter'}}
                }
            }
        
        return base_config
