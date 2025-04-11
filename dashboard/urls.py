# dashboard/urls.py
from django.urls import path
from .views import main, analytics, reports
from .views.chatbot import chatbot_view, chatbot_api

app_name = 'dashboard'

urlpatterns = [
    path('', main.DashboardView.as_view(), name='home'),
    path('analytics/', analytics.AnalyticsView.as_view(), name='analytics'),
    path('reports/', reports.ReportsView.as_view(), name='reports'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('api/chatbot/', chatbot_api, name='chatbot-api'),

    path('analytics/market/', analytics.MarketAnalyticsView.as_view(), name='market-analytics'),
    path('analytics/traffic/', analytics.TrafficAnalyticsView.as_view(), name='traffic-analytics'),
    path('analytics/revenue/', analytics.RevenueAnalyticsView.as_view(), name='revenue-analytics'),
    path('reports/export/', reports.ExportReportView.as_view(), name='export-report'),
]
