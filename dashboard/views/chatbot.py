import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.utils import ProgrammingError, OperationalError

from telecom.huggingface import get_inference_api
from questionarios.models import (
    EstacoesMoveisIndicador,
    TrafegoOriginadoIndicador,
    ReceitasIndicador
)

# Função para processar perguntas sobre os dados de mercado
def process_market_question(question):
    """
    Processa perguntas sobre o mercado usando dados do banco de dados
    e envia para o modelo de IA para elaborar respostas.
    """
    # Preparar contexto com dados do banco de dados
    context = {
        "operadoras": ["Orange", "MTN", "TELECEL"],
        "dados": {}
    }
    
    # Buscar dados para dar contexto à resposta
    try:
        # Estações Móveis/Assinantes
        assinantes = {}
        for operadora in ['orange', 'mtn', 'telecel']:
            try:
                query = EstacoesMoveisIndicador.objects.filter(operadora=operadora).order_by('-ano', '-mes')
                if query.exists():
                    latest = query.first()
                    assinantes[operadora] = {
                        'total': latest.calcular_total_estacoes_moveis(),
                        'pre_pago': latest.afectos_planos_pre_pagos,
                        'pos_pago': latest.afectos_planos_pos_pagos,
                        'ano': latest.ano,
                        'mes': latest.mes
                    }
            except (ProgrammingError, OperationalError):
                # Tabela não existe ou outro erro de banco de dados
                pass
        
        if assinantes:
            context['dados']['assinantes'] = assinantes
        
        # Tráfego
        trafego = {}
        for operadora in ['orange', 'mtn', 'telecel']:
            try:
                query = TrafegoOriginadoIndicador.objects.filter(operadora=operadora).order_by('-ano', '-mes')
                if query.exists():
                    latest = query.first()
                    trafego[operadora] = {
                        'on_net': float(latest.on_net) if hasattr(latest, 'on_net') else 0,
                        'off_net': float(latest.off_net) if hasattr(latest, 'off_net') else 0,
                        'ano': latest.ano,
                        'mes': latest.mes
                    }
            except (ProgrammingError, OperationalError):
                # Tabela não existe ou outro erro de banco de dados
                pass
        
        if trafego:
            context['dados']['trafego'] = trafego
        
        # Receitas
        receitas = {}
        for operadora in ['orange', 'mtn', 'telecel']:
            try:
                query = ReceitasIndicador.objects.filter(operadora=operadora).order_by('-ano', '-mes')
                if query.exists():
                    latest = query.first()
                    receitas[operadora] = {
                        'total': float(latest.calcular_total_receitas()),
                        'retalhistas': float(latest.calcular_total_receitas_retalhistas()),
                        'grossistas': float(latest.calcular_total_receitas_grossistas()),
                        'ano': latest.ano,
                        'mes': latest.mes
                    }
            except (ProgrammingError, OperationalError):
                # Tabela não existe ou outro erro de banco de dados
                pass
        
        if receitas:
            context['dados']['receitas'] = receitas
        
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
    
    # Se não temos dados, informar ao usuário
    if not context['dados']:
        return "Ainda não temos dados suficientes disponíveis no sistema. As tabelas de indicadores podem não ter sido criadas ou estão vazias. Por favor, preencha os questionários para gerar dados de análise."
    
    # Enviar pergunta + contexto para o modelo do Hugging Face
    try:
        model = get_inference_api("google/flan-t5-base")
        prompt = f"""
        Contexto: {json.dumps(context, indent=2)}
        
        Pergunta: {question}
        
        Responda com base nos dados fornecidos no contexto. Se não tiver dados suficientes, 
        indique isso na resposta. Tente sempre encontrar as informações mais relevantes.
        """
        
        response = model(prompt)
        return response[0]['generated_text']
    except Exception as e:
        print(f"Erro na API do Hugging Face: {e}")
        return "Desculpe, estou tendo dificuldades para processar sua pergunta agora. Por favor, tente novamente mais tarde."

@login_required
def chatbot_view(request):
    """
    View principal do chatbot
    """
    messages = request.session.get('chat_messages', [])
    
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '')
        
        if user_message:
            # Adicionar mensagem do usuário ao histórico
            timestamp = timezone.now().strftime('%H:%M')
            messages.append({
                'content': user_message,
                'is_user': True,
                'timestamp': timestamp
            })
            
            # Processar pergunta
            response = process_market_question(user_message)
            
            # Adicionar resposta ao histórico
            messages.append({
                'content': response,
                'is_user': False,
                'timestamp': timezone.now().strftime('%H:%M')
            })
            
            # Limitar o histórico a 10 mensagens
            if len(messages) > 20:
                messages = messages[-20:]
            
            # Salvar no session
            request.session['chat_messages'] = messages
    
    return render(request, 'dashboard/chatbot.html', {'messages': messages})

@csrf_exempt
def chatbot_api(request):
    """
    API para processar perguntas via AJAX
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            
            if not question:
                return JsonResponse({'error': 'Pergunta vazia'}, status=400)
            
            response = process_market_question(question)
            
            return JsonResponse({
                'response': response,
                'timestamp': timezone.now().strftime('%H:%M')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405) 