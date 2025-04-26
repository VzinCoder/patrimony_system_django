📦 Sistema de Gerenciamento de Patrimônio
=========================================

Este projeto é uma aplicação web de gerenciamento de patrimônio construída com **Django**.  
Inclui integração com **Stripe** para gerenciamento de pagamentos recorrentes (mensal, semestral e anual).

🚀 Funcionalidades
------------------

* Cadastro e controle de patrimônios
    
* Integração com Stripe para assinaturas:
    
    * Plano Mensal
        
    * Plano Semestral
        
    * Plano Anual
        
* Dashboard com resumo dos patrimônios e status de pagamento
    
* Visualização de dados com gráficos
    

🛠️ Tecnologias utilizadas
--------------------------

* Python 3.x
    
* Django 4.x
    
* Stripe API (Pagamentos)
    
* Tailwind (estilização CSS com Tailwind inline)
    
* Chart.js (biblioteca de gráficos)
    
* HTML, CSS
    

⚙️ Configurações necessárias
----------------------------

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

```env
STRIPE_PUBLISHABLE_KEY=your_publishable_key
STRIPE_SECRET_KEY=your_secret_key
STRIPE_MONTHLY_ID=price_abc123
STRIPE_SEMESTRAL_ID=price_def456
STRIPE_ANNUAL_ID=price_ghi789
STRIPE_WEBHOOK_KEY=your_key_webhook
```

Essas informações são necessárias para que o sistema de pagamento funcione corretamente.

> ⚠️ **Atenção**: Nunca compartilhe seu arquivo `.env` publicamente.

* * *

📝 Criando Planos na Stripe
---------------------------

Antes de utilizar o sistema de assinaturas, é necessário criar os planos na sua conta Stripe:

| Plano | Valor (BRL) | Frequência |
| --- | --- | --- |
| Mensal | R$15 | Todo mês |
| Semestral | R$75 | A cada 6 meses |
| Anual | R$140 | Todo ano |

1. Acesse o [Painel da Stripe](https://dashboard.stripe.com/products).
    
2. Crie um produto para cada tipo de assinatura (Mensal, Semestral e Anual).
    
3. Em cada produto, crie um preço (Price ID) com o valor e a recorrência correta.
    
4. Copie os Price IDs gerados e configure no arquivo `.env`.
    

* * *

🧩 Instalação e uso
-------------------

1. Clone o repositório:
    

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Crie um ambiente virtual:
    

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
    

```bash
pip install -r requirements.txt
```

4. Configure o banco de dados (padrão: SQLite):
    

```bash
python manage.py migrate
```

5. Rode o servidor:
    

```bash
python manage.py runserver
```

* * *

🔔 Configurando Webhook do Stripe localmente
--------------------------------------------

Para testar os eventos de webhook do Stripe no ambiente local, siga os passos:

1. Instale o Stripe CLI:
    
    * [Download Stripe CLI](https://stripe.com/docs/stripe-cli#install)
        
2. Faça login no Stripe CLI:
    

```bash
stripe login
```

3. Rode o servidor Django localmente:
    

```bash
python manage.py runserver
```

4. Em outro terminal, conecte o Stripe CLI ao seu servidor local:
    

```bash
stripe listen --forward-to http://127.0.0.1:porta/subscription/webhook
```

**Importante:**  
A porta pode variar dependendo da configuração local do Django.  
Verifique no terminal qual porta o Django está usando (por padrão é `8000`) e ajuste a URL corretamente.  
Exemplo:

```bash
stripe listen --forward-to http://127.0.0.1:8000/subscription/webhook
```

Isso irá capturar os eventos do Stripe e redirecionar para a sua aplicação local no endpoint `/subscription/webhook`.

* * *

📄 Licença
----------

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
