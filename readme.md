# Encurtador de URL

Aplicação web feita com Django para encurtar URLs, consultar os links cadastrados e redirecionar pelo código curto. Cada link tem validade padrão de 365 dias, podendo ser estendida para 730 dias.

## Funcionalidades

- Criação de links curtos por meio de uma API JSON.
- Redirecionamento para a URL original usando o código curto.
- Respostas de erro em JSON para links inexistentes ou expirados.
- Página web simples disponível na raiz do projeto (`/`).

## Tecnologias

- Python 3.12 ou superior
- Django 5.2 ou superior (versão limitada pelas dependências em `requirements.txt`)
- Django REST Framework
- PostgreSQL ou SQLite

As dependências Python estão listadas em [`requirements.txt`](./requirements.txt).

## Configuração

Os comandos abaixo consideram que o terminal está na raiz do repositório.

1. Crie e ative um ambiente virtual:

   **Windows (PowerShell):**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Crie o arquivo `.env` a partir do exemplo:

   **Windows (PowerShell):**

   ```powershell
   Copy-Item .env.example .env
   ```

   **Linux:**

   ```bash
   cp .env.example .env
   ```

4. Configure o `.env` com a chave secreta e as credenciais do banco. Para SQLite:

   ```dotenv
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   SECRET_KEY=coloque-aqui-uma-chave-secreta
   ```

   Para PostgreSQL, use `DB_ENGINE=django.db.backends.postgresql` e preencha `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT` com os dados do banco.

   Gere uma chave secreta com:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Copie o valor gerado para `SECRET_KEY`. O `.env` contém configurações privadas e não deve ser compartilhado nem enviado ao controle de versão.

## Desenvolvimento local

O `manage.py` fica dentro do diretório `encurtador_url`. A partir da raiz do repositório:

```bash
cd encurtador_url
python manage.py migrate
python manage.py runserver
```

O servidor de desenvolvimento ficará disponível em <http://127.0.0.1:<PORTA>/>.

## Execução em produção

Em produção, execute o servidor WSGI a partir do diretório `encurtador_url` (o diretório que contém `manage.py` e `config/`). Antes de iniciar:

- Configure o `.env` com uma `SECRET_KEY` exclusiva e os dados do banco de produção.
- Altere `ALLOWED_HOSTS` em `config/settings.py` para incluir o domínio real da aplicação. A configuração atual aceita somente `localhost` e `127.0.0.1`.
- Mantenha `DEBUG = False` e use HTTPS em produção. Recomenda-se colocar o servidor WSGI atrás de um proxy reverso com TLS.
- Aplique as migrações com `python manage.py migrate`.
- Gere os arquivos estáticos após cada atualização do frontend:

  ```bash
  python manage.py collectstatic --noinput
  ```

  O WhiteNoise serve os arquivos coletados junto com a aplicação Waitress/Gunicorn. Não é necessário habilitar `DEBUG` para servir CSS e JavaScript.

### Windows com Waitress

O Waitress está listado em `requirements.txt`. No PowerShell, dentro de `encurtador_url`, inicie o servidor com:

```powershell
waitress-serve --listen=127.0.0.1:<PORTA> config.wsgi:application
```

### Linux com Gunicorn

O Gunicorn está listado em `requirements.txt`. No Linux, dentro de `encurtador_url`, inicie o servidor com:

```bash
gunicorn --workers 3 --bind 127.0.0.1:<PORTA> config.wsgi:application
```

Esses comandos escutam apenas na interface local, apropriado quando há um proxy reverso na mesma máquina. Se o servidor WSGI precisar aceitar conexões diretamente, ajuste o endereço de escuta para `0.0.0.0:<PORTA>` e configure firewall e HTTPS adequadamente.

## Endpoints

### Criar um link curto

`POST /api/v1/encurta_url`

Envie JSON com a URL original:

```json
{
  "url": "https://example.com/minha-pagina"
}
```

Exemplo:

```bash
curl -X POST http://localhost:<PORTA>/api/v1/encurta_url \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://example.com/minha-pagina\"}"
```

Resposta `200`:

```json
{
  "url": "http://localhost:<PORTA>/Ab3xY"
}
```

O código curto tem cinco caracteres. A mesma URL pode ser cadastrada mais de uma vez.

### Redirecionar

`GET /<codigo>`

Ao abrir, por exemplo, `http://localhost:<PORTA>/Ab3xY`, a aplicação redireciona para a URL original se o link ainda estiver válido. Links expirados retornam `410`; códigos não encontrados retornam `404`.

### Página web

A página simples da aplicação está em <http://localhost:<PORTA>/>.

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
