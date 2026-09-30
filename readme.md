# Encurtador de URL

Aplicação web feita com Django para encurtar URLs, consultar os links cadastrados e redirecionar pelo código curto. Cada link tem um prazo de validade padrão de 365 dias podendo ser extendido para 730 dias.

## Funcionalidades

- Criação de links curtos por meio de uma API JSON.
- Redirecionamento para a URL original usando o código curto.
- Respostas de erro em JSON para links inexistentes ou expirados.
- Página web simples disponível em `/index`.

## Tecnologias

- Python 3.12 ou superior
- Django 6.1.1
- Django REST Framework 3.18.1
- Compatível com POSTGRE 8.12
- Compatível com SQLite 3.53

As dependências Python estão listadas em [`requirements.txt`](./requirements.txt).

## Como executar localmente

Os comandos abaixo consideram que o terminal está na raiz do repositório.

1. Crie e ative um ambiente virtual:

   **Windows (PowerShell):**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux/macOS:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Crie o arquivo de ambiente que o Django carrega.:

   **Windows (PowerShell):**

   ```powershell
   Copy-Item ..env.example .env
   ```

   **Linux/macOS:**

   ```bash
   cp .env.example .env
   ```

4. Edite `.env` com uma chave secreta e a configuração do banco de dados. 
- Para desenvolvimento local com POSTGRE, use:

   ```dotenv
   ENGINE=django.db.backends.postgresql
   NAME=nome-da-database
   USER=
   PASSWORD=
   HOST=
   PORT=
   SECRET_KEY=coloque-aqui-uma-chave-secreta
   ```

- Para desenvolvimento local com SQLite, use:

   ```dotenv
   ENGINE=django.db.backends.sqlite3
   NAME=db.sqlite3
   USER=
   PASSWORD=
   HOST=
   PORT=
   SECRET_KEY=coloque-aqui-uma-chave-secreta
   ```

   Gere uma chave secreta com:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Copie o valor gerado para `SECRET_KEY`. O arquivo `.env` contém configurações locais e não deve ser compartilhado.

1. Aplique as migrações e inicie o servidor. O `manage.py` fica dentro de `encurtador_url`, e esse diretório também precisa ser o diretório de trabalho para que as configurações do `.env` sejam carregadas:

   ```bash
   cd encurtador_url
   python manage.py migrate
   python manage.py runserver
   ```

   O servidor estará disponível em <http://127.0.0.1:8000>. A configuração atual aceita `localhost` e `127.0.0.1` como hosts.

## Endpoints

### Criar um link curto

`POST /encurta_url`

Envie JSON com a URL original:

```json
{
  "url": "https://example.com/minha-pagina"
}
```

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/encurta_url \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://example.com/minha-pagina\"}"
```

Resposta `200`:

```json
{
  "url": "http://127.0.0.1:8000/Ab3xY"
}
```

O código curto tem cinco caracteres. Pode ser cadastrada a mesma URL mais de uma vez

### Redirecionar

`GET /<codigo>`

Ao abrir, por exemplo, `http://127.0.0.1:8000/Ab3xY`, a aplicação redireciona para a URL original se o link ainda estiver válido. Links expirados retornam `410`; códigos não encontrados retornam `404`.

### Página web

A página simples da aplicação está em <http://127.0.0.1:8000/index>.

## Erros

As respostas de erro da API usam JSON com `error` e `detail`. Os principais status são:

| Status | Significado |
| --- | --- |
| `404` | Código ou URL não encontrado |
| `410` | Link expirado |
| `422` | Dados ausentes |
| `500` | Falha interna do servidor |

## Testes

Para executar os testes Django:

```bash
cd encurtador_url
python manage.py test
```
