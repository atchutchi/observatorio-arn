from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/api/', views.ChatbotAPIView.as_view(), name='chatbot_api'),
    path('chatbot/', views.chatbot_page_view, name='chatbot_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('operadoras/', views.operadoras, name='operadoras'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('sobre/', views.sobre, name='sobre'),
    path('profile/', views.profile, name='profile'),
] 