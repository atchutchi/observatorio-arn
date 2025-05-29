"""
Script seguro para testar configurações de email usando apenas variáveis de ambiente
NUNCA hardcode credenciais neste arquivo!
"""
import os
import django
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'observatorio.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_settings():
    """Testa as configurações de e-mail usando apenas variáveis de ambiente."""
    
    # Verificar se as variáveis de ambiente estão configuradas
    required_vars = ['EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Erro: Variáveis de ambiente não configuradas: {', '.join(missing_vars)}")
        print("\nPara configurar, adicione ao arquivo .env:")
        print("EMAIL_HOST_USER=seu_email@arn.gw")
        print("EMAIL_HOST_PASSWORD=sua_senha_app")
        print("EMAIL_HOST=smtp.gmail.com")
        print("EMAIL_PORT=587")
        print("EMAIL_USE_TLS=True")
        return
    
    # Configurações vêm apenas do .env
    print("=== Configurações de E-mail ===")
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"Host: {os.getenv('EMAIL_HOST', 'smtp.gmail.com')}")
    print(f"Port: {os.getenv('EMAIL_PORT', '587')}")
    print(f"TLS: {os.getenv('EMAIL_USE_TLS', 'True')}")
    print(f"Username: {os.getenv('EMAIL_HOST_USER', 'NÃO CONFIGURADO')}")
    print(f"Password: {'✓ Configurado' if os.getenv('EMAIL_HOST_PASSWORD') else '❌ Não configurado'}")
    print(f"From Email: {os.getenv('DEFAULT_FROM_EMAIL', os.getenv('EMAIL_HOST_USER'))}")
    print("============================")
    
    # E-mail de destino
    recipient = input("Digite o e-mail para receber o teste: ")
    
    try:
        print("\n📧 Enviando e-mail de teste...")
        result = send_mail(
            subject='Teste de configuração de e-mail - Observatório ARN',
            message='Este é um e-mail de teste do sistema Observatório ARN. '
                   'Se você está recebendo esta mensagem, a configuração de e-mail foi bem-sucedida!',
            from_email=os.getenv('DEFAULT_FROM_EMAIL', os.getenv('EMAIL_HOST_USER')),
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        if result:
            print(f"\n✅ Sucesso! E-mail enviado para {recipient}")
            print("Verifique sua caixa de entrada (e também a pasta de spam).")
        else:
            print("\n❌ Falha: O e-mail não foi enviado. Verifique as configurações.")
            
    except Exception as e:
        print(f"\n❌ Erro ao enviar e-mail: {e}")
        print("\n💡 Dicas:")
        print("1. Verifique se as credenciais estão corretas no arquivo .env")
        print("2. Se usando Gmail, ative 'Senhas de app' em vez da senha normal")
        print("3. Verifique se o 2FA está configurado na conta Google")
        
if __name__ == "__main__":
    test_email_settings() 