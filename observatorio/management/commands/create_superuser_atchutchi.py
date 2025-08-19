from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Cria o superuser atchutchi específico solicitado'

    def handle(self, *args, **options):
        username = 'atchutchi'
        email = 'abboss40@gmail.com'
        password = 'admin123'
        
        try:
            # Verifica se o usuário já existe
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuário "{username}" já existe!')
                )
                return
            
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'Email "{email}" já está em uso!')
                )
                return
            
            # Cria o superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" criado com sucesso!\n'
                    f'Email: {email}\n'
                    f'Senha: {password}\n'
                    f'Acesse: http://127.0.0.1:8000/admin/ ou http://127.0.0.1:8000/accounts/login/'
                )
            )
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar superuser: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro inesperado: {e}')
            ) 