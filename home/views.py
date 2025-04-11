from django.shortcuts import render
from django.db.models import Sum, Count, Avg, Max, F, DecimalField
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from decimal import Decimal

from .models import Operadora, DadoEstatistico, TipoServico
from .chatbot import Chatbot
from questionarios.models import (
    AssinantesIndicador, ReceitasIndicador, InvestimentoIndicador
)
import logging

logger = logging.getLogger(__name__)

# Initialize chatbot instance (can be global if state is managed via session)
chatbot_instance = Chatbot()

# Helper function to get latest year with data for a model
def get_latest_year(model):
    return model.objects.aggregate(latest_year=Max('ano')).get('latest_year')

def index(request):
    # Fetch basic stats for the homepage cards
    total_operadoras = Operadora.objects.filter(ativo=True).count()
    servicos = TipoServico.objects.all()
    
    # Placeholder data for other cards until specific logic is defined
    total_questionarios = 13 # Count of distinct indicator types managed
    total_relatorios = 4 # Placeholder
    
    context = {
        'total_operadoras': total_operadoras,
        'servicos': servicos,
        'total_questionarios': total_questionarios,
        'total_relatorios': total_relatorios,
    }
    return render(request, 'home/index.html', context)

@login_required
def dashboard(request):
    # Totals for dashboard cards
    total_operadoras = Operadora.objects.filter(ativo=True).count()
    total_servicos = TipoServico.objects.count()
    total_indicadores_count = 13 # Static count for now

    # --- Calculate Key Metrics --- 
    latest_year_assinantes = get_latest_year(AssinantesIndicador)
    latest_year_investimento = get_latest_year(InvestimentoIndicador)
    
    total_assinantes_geral = 0
    if latest_year_assinantes:
        assinantes_agg = AssinantesIndicador.objects.filter(ano=latest_year_assinantes).aggregate(
            total_sum=Sum( 
                Coalesce(F('assinantes_pre_pago'), 0) + 
                Coalesce(F('assinantes_pos_pago'), 0) + 
                Coalesce(F('assinantes_fixo'), 0) 
            )
        )
        total_assinantes_geral = assinantes_agg.get('total_sum') or 0
        
    total_investimento_geral = Decimal('0.00') # Use Decimal
    if latest_year_investimento:
        investimento_agg = InvestimentoIndicador.objects.filter(ano=latest_year_investimento).aggregate(
             total_sum=Sum(
                 Coalesce(F('servicos_telecomunicacoes'), Decimal('0.0')) + 
                 Coalesce(F('servicos_internet'), Decimal('0.0')) + 
                 Coalesce(F('servicos_telecomunicacoes_incorporeo'), Decimal('0.0')) + 
                 Coalesce(F('servicos_internet_incorporeo'), Decimal('0.0'))
             , output_field=DecimalField())
        )
        total_investimento_geral = investimento_agg.get('total_sum') or Decimal('0.00')

    # Placeholder for other metrics
    market_share_leader = "Orange (Exemplo)"
    market_share_value = "49.3% (Exemplo)"
    avg_qos = "4.0/5 (Exemplo)"

    context = {
        'total_operadoras': total_operadoras,
        'total_servicos': total_servicos,
        'total_indicadores': total_indicadores_count,
        'total_assinantes_geral': total_assinantes_geral,
        'latest_year_assinantes': latest_year_assinantes,
        'total_investimento_geral': total_investimento_geral,
        'latest_year_investimento': latest_year_investimento,
        'market_share_leader': market_share_leader,
        'market_share_value': market_share_value,
        'avg_qos': avg_qos,
        'is_dashboard': True # Flag for active link styling
    }
    return render(request, 'home/dashboard.html', context)

def estatisticas(request):
    """View para a página de estatísticas."""
    context = {
        'title': 'Estatísticas',
        'page': 'estatisticas'
    }
    return render(request, 'home/estatisticas.html', context)

@login_required
def operadoras(request):
    operadoras_list = Operadora.objects.filter(ativo=True)
    operadoras_data = []
    latest_year = get_latest_year(AssinantesIndicador)

    for op in operadoras_list:
        assinantes_count = 0
        if latest_year:
            agg = AssinantesIndicador.objects.filter(operadora=op.codigo, ano=latest_year).aggregate(
                 total_sum=Sum( 
                    Coalesce(F('assinantes_pre_pago'), 0) + 
                    Coalesce(F('assinantes_pos_pago'), 0) + 
                    Coalesce(F('assinantes_fixo'), 0) 
                )
            )
            assinantes_count = agg.get('total_sum') or 0
            
        operadoras_data.append({
            'nome': op.nome,
            'descricao': op.descricao,
            'logo_url': op.logo.url if op.logo else '/static/img/default-logo.png',
            'assinantes': assinantes_count, 
            'servicos': "Móvel, Internet, TV", # Placeholder - needs dynamic logic
            'ativo_desde': 2005 # Placeholder
        })

    # Placeholder data for comparison table
    comparativo_data = [
        {'operadora': 'Orange', 'assinantes': 750000, 'market_share': '49.3%', 'cobertura': '87%', 'qualidade': '4.2/5', 'licenca': 2030},
        {'operadora': 'MTN', 'assinantes': 650000, 'market_share': '42.8%', 'cobertura': '82%', 'qualidade': '3.8/5', 'licenca': 2029},
        {'operadora': 'Guinetel', 'assinantes': 120000, 'market_share': '7.9%', 'cobertura': '45%', 'qualidade': '3.2/5', 'licenca': 2027},
    ]
    
    context = {
        'operadoras': operadoras_data,
        'comparativo_data': comparativo_data # Pass placeholder data
    }
    return render(request, 'home/operadoras.html', context)

def relatorios(request):
    """View para a página de relatórios."""
    context = {
        'title': 'Relatórios',
        'page': 'relatorios',
        'relatorios': [
            {'titulo': 'Relatório Anual 2024', 'data': '15/01/2025', 'tipo': 'PDF'},
            {'titulo': 'Relatório Trimestral Q3-2024', 'data': '15/10/2024', 'tipo': 'XLSX'},
            {'titulo': 'Análise de Mercado 2023-2024', 'data': '30/06/2024', 'tipo': 'PDF'}
        ]
    }
    return render(request, 'home/relatorios.html', context)

def sobre(request):
    """View para a página sobre."""
    context = {
        'title': 'Sobre',
        'page': 'sobre'
    }
    return render(request, 'home/sobre.html', context)

def profile(request):
    """View para a página de perfil do usuário."""
    context = {
        'title': 'Perfil',
        'page': 'profile'
    }
    return render(request, 'home/profile.html', context)

def chatbot(request):
    """View para a página do chatbot."""
    context = {
        'title': 'Chatbot',
        'page': 'chatbot'
    }
    return render(request, 'home/chatbot.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotAPIView(View):
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            session_id = request.session.get('chatbot_session_id')
            
            if not user_message:
                return JsonResponse({"error": "Mensagem não fornecida."}, status=400)
                
            session_id = chatbot_instance.get_session_id(session_id)
            request.session['chatbot_session_id'] = session_id
            
            if user_message.lower().strip() == "/reset":
                 chatbot_instance.reset_conversation(session_id)
                 response_data = {
                     "message": "A conversa foi reiniciada.",
                     "session_id": session_id,
                     "status": "success"
                 }
            else:
                response_data = chatbot_instance.get_response(user_message, session_id)
            
            request.session.modified = True 
            
            return JsonResponse(response_data)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados JSON inválidos."}, status=400)
        except Exception as e:
            logger.error(f"Erro na API do Chatbot: {e}", exc_info=True)
            return JsonResponse({"error": "Erro interno no servidor."}, status=500)

def chatbot_page_view(request):
    context = {}
    return render(request, 'home/chatbot.html', context) 