# dashboard/urls.py
from django.urls import path
from .views import main, analytics, reports, chatbot, export_views

app_name = 'dashboard'

urlpatterns = [
    path('', main.DashboardView.as_view(), name='home'),
    path('analytics/', analytics.AnalyticsView.as_view(), name='analytics'),
    path('reports/', reports.ReportsView.as_view(), name='reports'),
    # Chatbot ARN (novo)
    path('assistant/', chatbot.chatbot_arn_view, name='arn-assistant'),
    path('api/chatbot/', chatbot.ARNChatbotAPIView.as_view(), name='arn-chatbot-api'),
    path('chatbot/history/', chatbot.chat_history_view, name='chat-history'),
    path('chatbot/session/<uuid:session_id>/', chatbot.chat_session_detail, name='chat-session-detail'),
    path('api/chat/feedback/', chatbot.ChatFeedbackAPIView.as_view(), name='chat-feedback'),
    
    # Chatbot antigo (compatibilidade)
    path('chatbot/', chatbot.chatbot_view, name='chatbot'),
    path('api/chatbot-old/', chatbot.chatbot_api, name='chatbot-api-old'),

    # Analytics URLs
    path('analytics/market/', analytics.MarketAnalyticsView.as_view(), name='market-analytics'),
    path('analytics/traffic/', analytics.TrafficAnalyticsView.as_view(), name='traffic-analytics'),
    path('analytics/revenue/', analytics.RevenueAnalyticsView.as_view(), name='revenue-analytics'),
    
    # Relatórios Antigos
    path('reports/export/', reports.ExportReportView.as_view(), name='export-report'),
    
    # ===== NOVOS RELATÓRIOS ARN =====
    path('reports/market/', reports.MarketReportView.as_view(), name='market-report'),
    path('reports/executive/', reports.DashboardExecutiveView.as_view(), name='executive-dashboard'),
    path('reports/comparative/', reports.ComparativeReportView.as_view(), name='comparative-report'),
    path('reports/history/', reports.ReportHistoryView.as_view(), name='report-history'),
    path('reports/generate/', reports.GenerateReportView.as_view(), name='generate-report'),
    
    # APIs para relatórios
    path('api/reports/<str:report_type>/', reports.ReportAPIView.as_view(), name='report-api'),
    
    # ===== EXPORTAÇÃO DE RELATÓRIOS =====
    path('reports/export/<str:report_type>/<str:format_type>/', export_views.ExportReportView.as_view(), name='export-report-new'),
    path('reports/quick-export/', export_views.QuickExportView.as_view(), name='quick-export'),
]
