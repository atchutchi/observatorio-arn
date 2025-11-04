# 🌍 Observatório do Mercado de Telecomunicações da Guiné-Bissau

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.1.0-orange.svg)](CHANGELOG.md)

Uma plataforma web moderna para monitoramento e análise do mercado de telecomunicações da Guiné-Bissau, permitindo visualizar dados estatísticos das operadoras e tendências do setor.

---

## ✨ Características Principais

- 📊 **Dashboard Analítico**: Visualizações interativas de dados do mercado de telecomunicações
- 📝 **Questionários KPI**: Sistema de coleta de dados via questionários padronizados ARN
- 🤖 **Chatbot Inteligente**: Assistente virtual com IA para esclarecimento de dúvidas
- 🔐 **Autenticação Segura**: Login com Google OAuth e sistema tradicional
- ☁️ **Integração Supabase**: Armazenamento híbrido (local + cloud)
- 🧠 **AI/ML**: Integração com Hugging Face para processamento de linguagem natural
- 💰 **Gestão de Tarifários**: Módulo para gerenciamento de tarifários das operadoras
- 📈 **Análise de Mercado**: Módulos de análise comparativa e relatórios
- 📡 **Estações Móveis**: Monitoramento de cobertura territorial
- 🌐 **Tráfego de Dados**: Análise de tráfego (originado, terminado, roaming)
- 💼 **Indicadores Económicos**: Receitas, emprego e investimentos no setor
- 🏥 **Health Monitoring**: Endpoints de monitoramento para produção

---

## 🚀 Tecnologias Utilizadas

### Backend
- **Framework**: Django 4.2.11 LTS
- **Linguagem**: Python 3.9+
- **API**: Django REST Framework
- **Auth**: Django AllAuth + Google OAuth

### Frontend
- **Framework CSS**: Bootstrap 5
- **Gráficos**: Chart.js
- **Icons**: Font Awesome

### Banco de Dados
- **Desenvolvimento**: SQLite 3
- **Produção**: PostgreSQL 12+

### Cloud & IA
- **Storage**: Supabase
- **AI/ML**: Hugging Face Transformers
- **Chatbot**: BlenderBot 400M

### DevOps
- **Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Container**: Docker + Docker Compose
- **Deploy**: Heroku, Railway, AWS, VPS

---

## ⚡ Quickstart

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/observatorio-arn.git
cd observatorio-arn

# Configure e execute
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # Configure suas variáveis
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Acesse:** http://127.0.0.1:8000

📖 **Documentação completa:** [QUICKSTART.md](QUICKSTART.md) | [SETUP.md](SETUP.md)

---

## 🐳 Docker (Recomendado)

```bash
# Configure
cp env.example .env

# Execute
docker-compose up

# Migrations (novo terminal)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

**Acesse:** http://localhost:8000

---

## 📋 Versão 1.1.0 - Novidades

### ✅ Atualizações
- ✨ Django 3.2 → 4.2.11 LTS (suporte até 2026)
- 🔒 Configurações de segurança avançadas
- 🏥 Health check endpoints
- 🐳 Containerização com Docker
- 📚 Documentação completa

### 🔐 Segurança
- HTTPS/SSL redirect em produção
- Content Security Policy (CSP)
- CSRF protection avançada
- Session security aprimorada
- Cookies seguros (HttpOnly, SameSite)

### 📊 Monitoramento
- `GET /health/` - Status básico
- `GET /health/detailed/` - Status completo
- `GET /health/ready/` - Readiness probe
- `GET /health/alive/` - Liveness probe

Veja o [CHANGELOG.md](CHANGELOG.md) para detalhes completos.

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | Guia rápido (5 minutos) |
| [SETUP.md](SETUP.md) | Instalação detalhada |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Guia de deploy (Heroku, AWS, VPS) |
| [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) | Migração Django 3.2 → 4.2 |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de mudanças |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Resumo técnico |
| [TEMPLATES_REVIEW_SUMMARY.md](TEMPLATES_REVIEW_SUMMARY.md) | ⭐ Revisão de templates |
| [TEMPLATES_STANDARDIZATION_PLAN.md](TEMPLATES_STANDARDIZATION_PLAN.md) | Plano de padronização |

---

## 🏗️ Tecnologias Atualizadas (v1.1.0)

| Tecnologia | Versão | Status |
|------------|--------|--------|
| Django | 4.2.11 LTS | ✅ |
| Python | 3.9+ | ✅ |
| django-allauth | 0.61.1 | ✅ |
| supabase | 2.3.4 | ✅ |
| huggingface-hub | 0.20.3 | ✅ |
| transformers | 4.37.2 | ✅ |
| PostgreSQL | 12+ | ✅ |

## User Stories

### Utilizadores Regulares
- **Como** utilizador público, **posso** visualizar estatísticas gerais sobre o mercado de telecomunicações, **para** entender as tendências do setor.
- **Como** utilizador público, **posso** interagir com o chatbot, **para** obter respostas às minhas dúvidas sobre o setor.
- **Como** utilizador público, **posso** ver gráficos comparativos entre operadoras, **para** escolher a melhor empresa para meus serviços.

### Utilizadores Autenticados
- **Como** utilizador autenticado, **posso** inserir novos dados de questionários, **para** contribuir com informações atualizadas.
- **Como** utilizador autenticado, **posso** visualizar relatórios detalhados, **para** realizar análises aprofundadas do mercado.

### Administradores
- **Como** administrador, **posso** gerir tarifários de voz, **para** manter a base de dados sempre atualizada.
- **Como** administrador, **posso** criar novos utilizadores e atribuir permissões, **para** controlar o acesso ao sistema.
- **Como** administrador, **posso** monitorar a sincronização com o Supabase, **para** garantir a integridade dos dados.
- **Como** administrador, **posso** ver logs de atividades, **para** auditar as ações realizadas no sistema.

## Configuração de Ambiente

### Pré-requisitos

- Python 3.7+
- Pip (gerenciador de pacotes Python)
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Conta no Supabase para sincronização de dados (opcional, mas recomendado)

### Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/observatorio-telecom-gb.git
   cd observatorio-telecom-gb
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```
   DEBUG=True
   SECRET_KEY=sua-chave-secreta
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database
   DATABASE_URL=sqlite:///db.sqlite3
   
   # Supabase
   SUPABASE_URL=sua-url-supabase
   SUPABASE_KEY=sua-chave-supabase
   
   # Hugging Face
   HUGGINGFACE_TOKEN=seu-token-huggingface
   
   # Google Auth
   GOOGLE_CLIENT_ID=seu-client-id-google
   GOOGLE_CLIENT_SECRET=seu-client-secret-google
   ```

5. Aplique as migrações:
   ```
   python manage.py migrate
   ```

6. Crie um superusuário:
   ```
   python manage.py createsuperuser
   ```

7. Execute o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

8. Acesse o site em `http://localhost:8000`

## Integração com Supabase

Para configurar a integração com Supabase:

1. Instale a biblioteca Supabase:
   ```
   pip install supabase
   ```

2. Configure as tabelas no Supabase:
   ```
   python manage.py setup_supabase
   ```

3. Este comando verificará se as tabelas necessárias existem no Supabase e fornecerá instruções para criar aquelas que não existem.

## Troubleshooting

| Problema | Solução |
|----------|---------|
| URLs não encontradas (NoReverseMatch) | Verifique se o namespace está correto nos URLs. Foi corrigido um problema onde o `app_name = 'questionarios'` estava faltando. |
| Erro na migração com JSON_VALID | Este erro ocorre com SQLite em versões mais antigas. Atualize o SQLite ou use PostgreSQL para desenvolvimento. |
| Modelos não aparecem no Admin | Verifique se os modelos estão registrados em `admin.py` com o decorator `@admin.register`. |
| Erro ao conectar com o Supabase | Verifique as credenciais no arquivo `.env` e se a biblioteca Supabase foi instalada corretamente. |
| Tarifário Voz não aparece no Admin | Foi adicionado o registro dos modelos `TarifarioVozOrangeIndicador` e `TarifarioVozMTNIndicador` ao arquivo `admin.py`. |
| Dados não sincronizam com Supabase | Execute `python manage.py setup_supabase` para verificar a configuração das tabelas e siga as instruções para criar manualmente as tabelas necessárias. |

## Database Schema

### Models Principais

#### Base
- **IndicadorBase** (Modelo Abstrato)
  - `ano`: IntegerField
  - `mes`: IntegerField
  - `operadora`: CharField (choices: orange, telecel, telecel)

#### Tarifários
- **TarifarioVozOrangeIndicador**
  - Campos para tarifas de Internet USB Pré-pago
  - Campos para tarifas de Internet USB/BOX Residencial
  - Campos para tarifas de Subscrição mensal Residencial
  - Campos para tarifas de comunicação On-net e Off-net
  - Campos para tarifas internacionais (zonas 1-6)
  - Campos de metadados (criado_por, data_criacao, etc.)

- **TarifarioVozMTNIndicador**
  - Campos para equipamentos Huawei
  - Campos para pacotes diários, semanais e mensais
  - Campos para pacotes Y'ello Night
  - Campos para pacotes ilimitados
  - Campos de metadados (criado_por, data_criacao, etc.)

#### Estações Móveis
- **EstacoesMoveisIndicador**
  - Informações sobre estações móveis das operadoras
  - Distribuição regional e tecnológica

#### Tráfego
- **TrafegoOriginadoIndicador**
  - Dados sobre tráfego originado por operadora
  - Estatísticas por tipo de tráfego e destino

- **TrafegoTerminadoIndicador**
  - Dados sobre tráfego terminado por operadora
  - Estatísticas por tipo de tráfego e origem

- **TrafegoRoamingInternacionalIndicador**
  - Dados sobre roaming internacional
  - Estatísticas por país e tipo de serviço

- **TrafegoInternetIndicador**
  - Estatísticas de tráfego de internet
  - Distribuição por tecnologia e velocidade

#### Outros Indicadores
- **LBIIndicador**
  - Indicadores de LBI (Large Bandwidth Internet)

- **InternetFixoIndicador**
  - Estatísticas de internet fixa
  - Distribuição por tecnologia e região

- **ReceitasIndicador**
  - Dados financeiros sobre receitas das operadoras
  - Categorização por tipo de serviço

- **EmpregoIndicador**
  - Dados sobre emprego no setor de telecomunicações
  - Estatísticas por gênero e tipo de emprego

- **InvestimentoIndicador**
  - Dados sobre investimentos no setor
  - Categorização por tipo de investimento e região

### Integração com Supabase

Todos os modelos possuem os métodos:
- `save_to_supabase(table_name)`: Salva os dados do modelo no Supabase
- `delete_from_supabase(table_name)`: Remove os dados do modelo no Supabase

Os signals `post_save` e `post_delete` estão configurados para sincronizar automaticamente com o Supabase.

## Estrutura do Projeto

- **home**: Aplicação para a página inicial
- **dashboard**: Aplicação para visualizações e análises de dados
- **questionarios**: Aplicação para gerenciamento de questionários e indicadores
- **templates**: Templates HTML base
- **static**: Arquivos estáticos (CSS, JS, imagens)
- **media**: Arquivos enviados pelos usuários

## Desenvolvimento Futuro

### Planejado para as próximas versões:

1. **Melhorias no Chatbot**
   - Treinamento com dados específicos do mercado de telecomunicações da Guiné-Bissau
   - Integração com mais fontes de dados para respostas mais precisas

2. **Expansão de Análises**
   - Módulos adicionais para análise preditiva usando técnicas de IA
   - Dashboards personalizáveis para utilizadores

3. **Autenticação e Segurança**
   - Implementação de autenticação de dois fatores
   - Auditoria mais detalhada de ações dos utilizadores

4. **Internacionalização**
   - Suporte a múltiplos idiomas (incluindo crioulo guineense)
   - Adaptação para diferentes fusos horários

5. **API RESTful**
   - Desenvolvimento de API pública para acesso a dados não-sensíveis
   - Documentação interativa com Swagger/OpenAPI

6. **Mobile App**
   - Desenvolvimento de aplicativo móvel complementar
   - Notificações push para atualizações importantes

7. **Integração com Sistemas Governamentais**
   - Conexões com sistemas da ARN (Autoridade Reguladora Nacional)
   - Intercâmbio de dados com outros órgãos relevantes

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das mudanças (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Créditos

### Equipe de Desenvolvimento
- **Coordenação**: ARN (Autoridade Reguladora Nacional) da Guiné-Bissau
- **Desenvolvimento Backend**: Equipe de TI da ARN
- **Design e Frontend**: Consultores contratados
- **Análise de Dados**: Departamento de Estatística da ARN

### Tecnologias e Serviços
- **Supabase**: Serviço de banco de dados e armazenamento
- **Hugging Face**: Modelos de IA para o chatbot
- **Bootstrap**: Framework CSS para o frontend
- **Chart.js**: Biblioteca para visualização de dados
- **Django**: Framework web para Python

### Agradecimentos Especiais
- Às operadoras de telecomunicações da Guiné-Bissau pela colaboração na coleta de dados
- À comunidade open-source pelas ferramentas e bibliotecas utilizadas

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Para dúvidas ou informações, entre em contato: contato@observatoriotelecom.gb 