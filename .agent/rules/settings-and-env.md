---
trigger: always_on
---

# settings-and-env

## Configuração: Global × Módulo

O projeto separa configuração em dois escopos. Essa separação é uma regra estrutural e não pode ser violada.

- **Configuração global** — pertence à infraestrutura da API como um todo: ambiente de execução, porta, chave de API. Vive na raiz, em `.env` e `shared/config/settings.py`.
- **Configuração de módulo** — pertence às regras operacionais de um módulo específico: comportamento de cache, timeouts, retries, delays. Vive dentro do módulo, em `{modulo}/.env` e `{modulo}/shared/config/settings.py`.

**Princípio:** regras e configurações operacionais de um módulo ficam dentro do módulo. O `.env` e o `settings.py` da raiz são exclusivos para infraestrutura global e nunca devem conter parâmetros operacionais de scraping.

## Regras dos arquivos `.env`

- Nunca versione arquivos `.env` no GitHub.
- Cada ambiente (desenvolvimento, produção) tem seu próprio `.env`.
- Nenhuma classe lê o `.env` diretamente — sempre importa do `settings.py` correspondente ao escopo.

### `.env` da raiz (infraestrutura global)

```
APP_ENV=development
APP_PORT=8000
API_KEY=sua_chave_aqui
```

> `API_KEY` é obrigatória. Se ausente ou vazia, o middleware bloqueará todas as requisições com `401 Unauthorized`.

### `.env` do módulo (configuração operacional)

Contém os parâmetros operacionais do módulo. As variáveis efetivas são definidas pelo próprio módulo. Exemplo:

```
CACHE_ENABLED=true
CACHE_EXPIRATION_MINUTES=1440
HTTP_TIMEOUT_SECONDS=30
HTTP_RETRY_ATTEMPTS=3
HTTP_DELAY_SECONDS=2
```

## Regras dos arquivos `settings.py`

### `shared/config/settings.py` (global)

Lê o `.env` da raiz via `python-dotenv` e expõe as variáveis de infraestrutura global como constantes Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
APP_PORT = int(os.getenv("APP_PORT", 8000))
API_KEY = os.getenv("API_KEY")
```

### `{modulo}/shared/config/settings.py` (módulo)

Carrega explicitamente o `.env` do próprio módulo e expõe sua configuração operacional como constantes Python:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_EXPIRATION_MINUTES = int(os.getenv("CACHE_EXPIRATION_MINUTES", 1440))
HTTP_TIMEOUT_SECONDS = int(os.getenv("HTTP_TIMEOUT_SECONDS", 30))
HTTP_RETRY_ATTEMPTS = int(os.getenv("HTTP_RETRY_ATTEMPTS", 3))
HTTP_DELAY_SECONDS = int(os.getenv("HTTP_DELAY_SECONDS", 2))
```

## Dependências

- O `requirements.txt` da raiz lista as dependências globais do projeto:

```
fastapi
httpx
beautifulsoup4
playwright==1.44.0
python-dotenv
uvicorn
apscheduler
```

- Cada módulo pode declarar um `requirements.txt` próprio com dependências exclusivas.
- O `install.sh` instala as dependências globais, percorre o projeto instalando as dependências de cada módulo e instala os navegadores do Playwright.
- Após instalar as dependências, é obrigatório executar `playwright install chromium` para que módulos com JS rendering funcionem. No ambiente Docker, esse passo já está incluído no `Dockerfile`.
