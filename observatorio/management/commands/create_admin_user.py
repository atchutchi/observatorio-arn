from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError
import os

class Command(BaseCommand):
    help = 'Cria usuário administrador usando variáveis de ambiente seguras'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nome de usuário do administrador',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email do administrador',
        )
        parser.add_argument(
            '--interactive',
            action='store_true',
            help='Modo interativo para inserir dados',
        )

    def handle(self, *args, **options):
        if options['interactive']:
            username = input('Username: ')
            email = input('Email: ')
            password = input('Password: ')
        else:
            # Usar variáveis de ambiente ou argumentos
            username = options.get('username') or os.getenv('ADMIN_USERNAME')
            email = options.get('email') or os.getenv('ADMIN_EMAIL')
            password = os.getenv('ADMIN_PASSWORD')
            
            if not all([username, email, password]):
                self.stdout.write(
                    self.style.ERROR(
                        'Configure as variáveis de ambiente ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD '
                        'ou use --interactive para inserir dados manualmente.'
                    )
                )
                return
        
        try:
            # Verificar se o usuário já existe
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuário "{username}" já existe!')
                )
                
                # Perguntar se quer atualizar
                if options['interactive']:
                    update = input('Atualizar senha? (s/N): ').lower() == 's'
                    if update:
                        user = User.objects.get(username=username)
                        user.set_password(password)
                        user.email = email
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Usuário "{username}" atualizado com sucesso!')
                        )
                return
            
            # Criar novo usuário
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Superuser "{username}" criado com sucesso!\n'
                    f'📧 Email: {email}\n'
                    f'🔑 Acesse em: http://127.0.0.1:8000/admin/'
                )
            )
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao criar usuário: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro inesperado: {e}')
            )
