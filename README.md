# CloudAsset

Sistema web multiusuário para inventário e rastreabilidade de patrimônio corporativo. A aplicação permite cadastrar ativos identificados por RFID, associá-los a categorias, departamentos e fornecedores, acompanhar movimentações e visualizar indicadores operacionais em um dashboard.

O projeto também implementa um modelo SaaS simples: cada usuário recebe um período de teste e o acesso à área protegida é controlado por assinatura, com checkout recorrente via Stripe e atualização de status por webhooks.

## Destaques do projeto

- Aplicação full stack construída com Django e templates server-side.
- Isolamento dos dados por usuário em todas as entidades de negócio.
- CRUD de categorias, departamentos, fornecedores e patrimônios.
- Rastreabilidade de entrada, saída e transferência de ativos.
- Histórico de movimentações com endpoint JSON e paginação.
- Dashboard com métricas operacionais e gráfico de distribuição por categoria.
- Fluxo de assinatura com trial de 7 dias, planos recorrentes e middleware de proteção.
- Interface responsiva com Tailwind CSS, Flowbite, modais, tema claro/escuro e tabelas interativas.
- Busca de fornecedor com HTMX e atualização parcial da página.

## Funcionalidades

### Gestão de patrimônio

- Cadastro de ativo com RFID, nome, categoria, departamento, fornecedor, data de aquisição e status.
- Status disponíveis: ativo, em manutenção, desativado e perdido.
- Validação de RFID único por conta.
- Edição e visualização em modais.
- Exclusão lógica com `is_deleted`, preservando o registro para histórico.
- Registro automático de movimentação inicial ao cadastrar um ativo.
- Registro automático de transferência quando o departamento do ativo é alterado.

### Cadastros auxiliares

Categorias e departamentos possuem nome, descrição e unicidade por usuário. Fornecedores possuem nome, CNPJ, telefone, e-mail e endereço, com regras de unicidade de CNPJ e e-mail por conta.

### Movimentações

O domínio registra três tipos de movimentação: entrada, saída e transferência. O dashboard exibe as dez movimentações mais recentes, enquanto o histórico de cada ativo é disponibilizado por JSON, com paginação de dez registros por página.

### Dashboard e indicadores

O dashboard é calculado exclusivamente com os dados do usuário autenticado e apresenta:

- total de ativos ativos no sistema;
- quantidade de ativos em manutenção;
- ativos ativos sem movimentação há pelo menos seis meses;
- movimentações realizadas nos últimos 30 dias;
- últimas movimentações com data, ativo, tipo e localização;
- gráfico doughnut de distribuição dos ativos por categoria usando Chart.js.

### Assinaturas e pagamentos

O cadastro cria automaticamente uma assinatura trial de sete dias. Os planos pagos são recorrentes e configurados na Stripe:

| Plano | Duração usada pela aplicação | Identificador configurado |
| --- | --- | --- |
| Mensal | 30 dias | `STRIPE_MONTHLY_ID` |
| Semestral | 180 dias | `STRIPE_SEMESTRAL_ID` |
| Anual | 365 dias | `STRIPE_ANNUAL_ID` |

O checkout impede a criação de uma nova assinatura paga quando já existe uma assinatura ativa. O `SubscriptionMiddleware` permite rotas públicas, usuários staff e usuários com assinatura válida; os demais são redirecionados para a página de planos.

### Webhook da Stripe

O endpoint `POST /subscription/webhook` valida a assinatura do evento com `STRIPE_WEBHOOK_KEY` e trata:

- `checkout.session.completed`: cria a assinatura local e associa cliente, plano e assinatura Stripe ao usuário;
- `customer.subscription.updated`: recalcula a duração da assinatura local;
- `customer.subscription.deleted`: marca a assinatura como inativa.

Essa sincronização evita que o acesso dependa somente do retorno visual do checkout no navegador.

## Stack técnica

### Backend

- Python 3.x
- Django 5.1.6
- Django ORM e migrations
- SQLite como banco padrão de desenvolvimento
- Django Authentication e sessões
- `django-environ` para configuração por ambiente
- `django-compressor` para integração de assets
- Stripe Python SDK 11.5.0

### Frontend

- Django Templates com componentes reutilizáveis
- Tailwind CSS 4
- Flowbite 3.1.2 para sidebar, dropdowns e modais
- HTMX para busca assíncrona de fornecedores e renderização do partial `supplier_results.html`
- `simple-datatables` para ordenação, busca e paginação visual das tabelas
- Chart.js para o gráfico do dashboard
- JavaScript vanilla para modais, preenchimento de formulários e tema claro/escuro

> O código não utiliza React, Vue ou uma API REST completa: a interface principal é server-rendered, com endpoints JSON pontuais para o histórico de movimentações e HTMX em interações específicas.

## Arquitetura

```text
patrimony_system_django/
├── asset/          # Ativos, formulário, busca HTMX e histórico JSON
├── category/       # Categorias por usuário
├── department/     # Departamentos por usuário
├── movement/       # Registro de entradas, saídas e transferências
├── supplier/       # Fornecedores e busca por nome/CNPJ
├── subscription/   # Trial, planos, checkout, middleware e webhook Stripe
├── user_auth/      # Cadastro, login e logout
├── templates/      # Layout base, home, dashboard e componentes globais
├── static/         # CSS compilado, JavaScript e bibliotecas frontend locais
├── manage.py
├── requirements.txt
└── package.json
```

O relacionamento central do domínio é:

```text
Usuário
 ├── Assinaturas
 ├── Categorias ──┐
 ├── Departamentos │
 ├── Fornecedores  ├── Patrimônios ─── Movimentações
 └─────────────────┘
```

As queries protegidas filtram pelo usuário autenticado e as migrations adicionam constraints compostas para evitar duplicidade dentro da mesma conta.

## Pré-requisitos

- Python 3.10 ou superior recomendado.
- Node.js e npm para instalar/buildar os assets frontend.
- Uma conta Stripe em modo de teste para validar o checkout.
- Stripe CLI apenas para testar webhooks localmente.

## Instalação local

Clone o projeto e entre na pasta:

```bash
git clone <url-do-repositorio>
cd patrimony_system_django
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate
```

Instale as dependências Python e frontend:

```bash
pip install -r requirements.txt
npm install
```

Crie um arquivo `.env` na raiz antes de executar o Django:

```env
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_MONTHLY_ID=price_...
STRIPE_SEMESTRAL_ID=price_...
STRIPE_ANNUAL_ID=price_...
STRIPE_WEBHOOK_KEY=whsec_...
```

Gere os arquivos CSS e aplique as migrations:

```bash
npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/output.css
python manage.py migrate
python manage.py createsuperuser
```

Inicie a aplicação:

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Para desenvolvimento contínuo de CSS, execute o comando do Tailwind com `--watch` em outro terminal.

## Configuração da Stripe

1. Crie três produtos/preços recorrentes no [Dashboard da Stripe](https://dashboard.stripe.com/test/products).
2. Copie os respectivos Price IDs para as variáveis do `.env`.
3. Use o modo de teste e cartões de teste da Stripe durante o desenvolvimento.
4. Para receber eventos localmente, instale a [Stripe CLI](https://stripe.com/docs/stripe-cli), faça login e encaminhe os eventos:

```bash
stripe login
stripe listen --forward-to http://127.0.0.1:8000/subscription/webhook
```

O comando `stripe listen` exibirá um `whsec_...`; esse valor deve ser usado em `STRIPE_WEBHOOK_KEY`. O endpoint público da aplicação é `/subscription/webhook`.

## Rotas principais

| Método | Rota | Responsabilidade |
| --- | --- | --- |
| `GET` | `/` | Página inicial e planos |
| `GET` | `/auth/register` | Cadastro e criação do trial |
| `GET/POST` | `/auth/login` | Autenticação |
| `GET` | `/dashboard/` | Indicadores e gráfico |
| `GET/POST` | `/asset/` | Listagem e criação/edição de ativos |
| `GET` | `/asset/search-supplier` | Busca HTMX por fornecedor |
| `GET` | `/asset/<id>/movements` | Histórico JSON paginado |
| `GET/POST` | `/category/`, `/department/`, `/supplier/` | CRUD dos cadastros auxiliares |
| `GET` | `/subscription/subscriptions` | Planos disponíveis |
| `POST` | `/subscription/create-checkout-session` | Criação da sessão Stripe Checkout |
| `POST` | `/subscription/webhook` | Sincronização de eventos Stripe |
| `GET` | `/admin/` | Administração Django |

## Segurança e regras de negócio

- Login obrigatório para a área protegida.
- Middleware bloqueia usuários sem assinatura válida.
- Usuários staff podem acessar a área administrativa.
- Dados de categorias, departamentos, fornecedores e ativos são associados ao usuário dono.
- Constraints compostas reforçam unicidade por usuário no banco.
- Formulários usam CSRF token nas operações web.
- Webhook valida a assinatura criptográfica enviada pela Stripe.
- Chaves privadas e Price IDs são lidos do ambiente e não devem ser versionados.

## Testes e manutenção

Execute as verificações padrão do Django:

```bash
python manage.py check
python manage.py test
```

Os testes ficam organizados nos apps. Para uma evolução de produção, é recomendável ampliar a cobertura dos fluxos de autorização entre usuários, checkout duplicado, idempotência de webhooks e expiração de assinaturas.

