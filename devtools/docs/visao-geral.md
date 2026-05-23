# web-scraping-api — Documentação Técnica

## Visão Geral

O `web-scraping-api` é uma API de web scraping profissional, modular e escalável desenvolvida em Python. Seu contrato central é baseado em requisição e resposta: recebe um POST com os parâmetros de busca e retorna os dados extraídos em JSON limpo e padronizado. O projeto não possui interface gráfica e não tem responsabilidade sobre o que o consumidor faz com os dados retornados.

O sistema é classificado como API (`-api`) e não como sistema (`-sys`) porque sua essência é expor endpoints HTTP que recebem requisições e retornam respostas estruturadas em JSON. A persistência definitiva dos dados é responsabilidade do sistema consumidor. O único armazenamento que a API mantém é um cache local e temporário, exclusivamente para evitar requisições externas repetidas.

---

## Tecnologias Utilizadas

| Tecnologia     | Papel no projeto |
|----------------|------------------|
| Python         | Linguagem base de todo o projeto |
| FastAPI        | Framework para expor os endpoints HTTP da API |
| Pydantic       | Validação do schema do payload HTTP de entrada (acompanha o FastAPI) |
| HTTPX          | Cliente HTTP para requisições em sites estáticos |
| BeautifulSoup  | Parsing de HTML e extração de dados do DOM |
| Playwright     | Automação de navegador para sites que dependem de JavaScript |
| APScheduler    | Agendamento de tarefas recorrentes (jobs) dos módulos |
| python-dotenv  | Leitura de variáveis de ambiente dos arquivos `.env` |
| Uvicorn        | Servidor ASGI para rodar o FastAPI em produção |
| Docker         | Containerização da aplicação para deploy em VPS |

---

## Formas de Acionamento

A API é acionada exclusivamente via POST HTTP. Toda requisição deve incluir o header de autenticação `X-API-Key`.

```
POST http://{host}/web-scraping/{dominio}/{modulo}
Content-Type: application/json
X-API-Key: {sua_chave}

{
    "query": "{termo de busca}",
    "filters": { ... },
    "fields": [ ... ],
    "limit": 20
}
```

> `query` é o único campo sempre obrigatório. Os campos opcionais aceitos no payload (`filters`, `fields`, `limit` e outros) e o comportamento de cada um são definidos pelo schema de entrada do módulo de destino, declarado no `main.py` do módulo. Consulte a seção **`main.py` do Módulo — O Orquestrador**.

Requisições sem o header `X-API-Key` ou com chave inválida recebem resposta `401 Unauthorized` antes de chegar a qualquer módulo.

---

## Hierarquia Conceitual do Projeto

O projeto é organizado em cinco níveis hierárquicos:

1. **Projeto** — `web-scraping-api`: raiz de tudo.
2. **Pacote / Domínio** — agrupa módulos de um mesmo domínio de interesse.
3. **Módulo / Alvo** — representa um site ou fonte específica dentro de um domínio.
4. **Etapa** — `downloader`, `extractor`, `output`: as três fases universais e obrigatórias do pipeline de scraping.
5. **Classe** — `service`, `validator`, `exception`, etc.: a lógica interna de cada etapa.

A lógica estrutural é universal: todos os módulos, independente do domínio, seguem exatamente a mesma estrutura de pastas, etapas e classes. O que muda entre módulos é exclusivamente o código dentro de cada classe, adaptado às regras de negócio e à estrutura do site alvo.

---

## Estrutura Completa de Pastas

Todo diretório do projeto deve conter um arquivo `__init__.py` vazio. Isso é obrigatório para que o Python reconheça cada pasta como um pacote importável. Nenhum diretório pode existir sem ele.

```
web-scraping-api/
│
├── shared/                          # Recursos globais compartilhados entre todos os domínios
│   ├── __init__.py
│   ├── base/                        # Classes abstratas — contratos universais de cada etapa
│   │   ├── __init__.py
│   │   ├── base_downloader.py
│   │   ├── base_extractor.py
│   │   └── base_output.py
│   ├── config/                      # Configuração de infraestrutura global da API
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── exception/                   # Contrato global de erro padronizado
│   │   ├── __init__.py
│   │   └── base_exception.py
│   └── security/                    # Segurança global da API
│       ├── __init__.py
│       └── api_key_middleware.py
│
├── {dominio}/
│   ├── __init__.py
│   └── {modulo}/
│       ├── __init__.py
│       ├── downloader/
│       │   ├── __init__.py
│       │   ├── configuration/
│       │   │   ├── __init__.py
│       │   │   └── configuration.py
│       │   ├── exception/
│       │   │   ├── __init__.py
│       │   │   └── exception.py
│       │   ├── repository/
│       │   │   ├── __init__.py
│       │   │   └── repository.py
│       │   ├── service/
│       │   │   ├── __init__.py
│       │   │   └── service.py
│       │   ├── transfer/
│       │   │   ├── __init__.py
│       │   │   └── request_transfer.py
│       │   └── validator/
│       │       ├── __init__.py
│       │       └── validator.py
│       │
│       ├── extractor/
│       │   ├── __init__.py
│       │   ├── exception/
│       │   │   ├── __init__.py
│       │   │   └── exception.py
│       │   ├── service/
│       │   │   ├── __init__.py
│       │   │   └── service.py
│       │   ├── transfer/
│       │   │   ├── __init__.py
│       │   │   └── request_transfer.py
│       │   └── validator/
│       │       ├── __init__.py
│       │       └── validator.py
│       │
│       ├── output/
│       │   ├── __init__.py
│       │   ├── exception/
│       │   │   ├── __init__.py
│       │   │   └── exception.py
│       │   ├── mapper/
│       │   │   ├── __init__.py
│       │   │   └── mapper.py
│       │   ├── service/
│       │   │   ├── __init__.py
│       │   │   └── service.py
│       │   ├── transfer/
│       │   │   ├── __init__.py
│       │   │   └── response_transfer.py
│       │   └── validator/
│       │       ├── __init__.py
│       │       └── validator.py
│       │
│       ├── shared/                  # Recursos internos exclusivos do módulo
│       │   ├── __init__.py
│       │   ├── config/
│       │   │   ├── __init__.py
│       │   │   └── settings.py
│       │   └── infra/
│       │       ├── __init__.py
│       │       └── cache/
│       │           ├── __init__.py
│       │           └── cleaner.py
│       │
│       ├── .env                     # Configuração operacional do módulo
│       ├── jobs.py                  # Tarefas agendadas do módulo (opcional)
│       ├── main.py                  # Orquestrador do pipeline do módulo
│       ├── MAP.md                   # Documentação técnica de scraping do módulo
│       └── requirements.txt         # Dependências exclusivas do módulo (opcional)
│
├── .env                             # Configuração de infraestrutura global
├── Dockerfile
├── install.sh
├── main.py                          # Ponto de entrada global da aplicação
└── requirements.txt                 # Dependências globais do projeto
```

---

## Configuração: Global × Módulo

O projeto separa configuração em dois escopos. Essa separação é uma regra estrutural e não pode ser violada.

- **Configuração global** — pertence à infraestrutura da API como um todo: ambiente de execução, porta, chave de API. Vive na raiz, em `.env` e `shared/config/settings.py`.
- **Configuração de módulo** — pertence às regras operacionais de um módulo específico: comportamento de cache, timeouts, retries, delays. Vive dentro do módulo, em `{modulo}/.env` e `{modulo}/shared/config/settings.py`.

**Princípio:** regras de um módulo ficam dentro do módulo. O `.env` e o `settings.py` da raiz são exclusivos para infraestrutura global e nunca devem conter parâmetros operacionais de scraping. Cada módulo carrega e expõe sua própria configuração de forma isolada.

---

## Arquivos da Raiz do Projeto

### `main.py` (raiz)

Ponto de entrada global da aplicação. Tem responsabilidades fixas e nenhuma lógica de negócio ou regra de domínio:

1. Instanciar o `FastAPI` com um `lifespan` que gerencia o agendador de tarefas.
2. Registrar o middleware de segurança.
3. Registrar o handler global de exceções da API.
4. **Descobrir e registrar automaticamente** os routers e os jobs de todos os módulos.

O `main.py` da raiz **não conhece módulos específicos** e **não é editado quando um novo módulo é adicionado**. Ele varre o projeto em busca de arquivos `main.py` e `jobs.py` dentro dos módulos e os registra de forma genérica.

```python
import importlib
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from shared.security.api_key_middleware import ApiKeyMiddleware
from shared.exception.base_exception import BaseApiException

_ROOT = Path(__file__).parent
_EXCLUDED = {"shared", "venv", ".venv", "node_modules"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    for path in _ROOT.glob("*/*/jobs.py"):
        rel = path.relative_to(_ROOT)
        if rel.parts[0] not in _EXCLUDED:
            module_path = rel.with_suffix("").as_posix().replace("/", ".")
            module = importlib.import_module(module_path)
            if hasattr(module, "register_jobs"):
                module.register_jobs(scheduler)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(ApiKeyMiddleware)


@app.exception_handler(BaseApiException)
async def handle_api_exception(request: Request, exc: BaseApiException):
    return JSONResponse(status_code=422, content=exc.response)


for _path in _ROOT.glob("*/*/main.py"):
    _rel = _path.relative_to(_ROOT)
    if _rel.parts[0] not in _EXCLUDED:
        _module_path = _rel.with_suffix("").as_posix().replace("/", ".")
        _module = importlib.import_module(_module_path)
        if hasattr(_module, "router"):
            app.include_router(_module.router, prefix="/web-scraping")
```

> **Consequência prática:** para adicionar um novo módulo ao projeto, basta criá-lo na estrutura padrão expondo um objeto `router` em seu `main.py`. A descoberta é automática — nenhuma linha do `main.py` da raiz precisa ser alterada.

### `.env` (raiz)

Arquivo de configuração de infraestrutura global. Nunca deve ser versionado no GitHub. Cada ambiente (desenvolvimento, produção) tem seu próprio `.env`.

```
APP_ENV=development
APP_PORT=8000
API_KEY=sua_chave_aqui
```

> `API_KEY` é obrigatória. Se ausente ou vazia, o middleware bloqueará todas as requisições com `401`. Variáveis operacionais de scraping (cache, timeouts) **não** ficam aqui — ver configuração de módulo.

### `Dockerfile`

Arquivo de containerização da aplicação. Utiliza a imagem oficial do Playwright para garantir que o Chromium esteja disponível no ambiente de produção. Obrigatório para deploy em VPS.

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `install.sh`

Script de instalação para ambiente local. Instala as dependências globais, percorre o projeto instalando as dependências declaradas por cada módulo e instala os navegadores do Playwright.

```bash
#!/bin/bash
set -e

echo "Installing root dependencies..."
pip install -r requirements.txt

echo "Installing module dependencies..."
find . -name "requirements.txt" -not -path "./requirements.txt" | while read req; do
    echo "  -> $req"
    pip install -r "$req"
done

echo "Installing Playwright browsers..."
playwright install chromium

echo "Done."
```

### `requirements.txt` (raiz)

Lista as dependências globais do projeto.

```
fastapi
httpx
beautifulsoup4
playwright==1.44.0
python-dotenv
uvicorn
apscheduler
```

> Cada módulo pode declarar um `requirements.txt` próprio com dependências exclusivas, instalado automaticamente pelo `install.sh`. O `Pydantic` acompanha o FastAPI e não precisa ser listado. Após `pip install -r requirements.txt`, é obrigatório executar `playwright install chromium`; no Docker esse passo já está no `Dockerfile`.

---

## Pasta `shared/` Global

A `shared/` global contém exclusivamente o que é relevante para o projeto inteiro, independente de qualquer domínio. Nenhuma lógica de negócio específica de um módulo deve existir aqui.

### `shared/base/`

Classes abstratas que definem os contratos obrigatórios de cada etapa. Qualquer módulo que implemente um downloader, extractor ou output deve herdar da respectiva classe base. Se o método abstrato obrigatório não for implementado, o Python lança erro automaticamente antes da execução.

As classes base encapsulam comportamentos universais — como retry e logging — no método público. O módulo implementa apenas o método interno (`_fetch`, `_extract` ou `_process`), contendo exclusivamente a lógica específica do site alvo. O método público da classe base nunca é sobrescrito.

```python
# shared/base/base_downloader.py
import time
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseDownloader(ABC):

    def __init__(self, retry_attempts: int, delay_seconds: int):
        self.__retry_attempts = retry_attempts
        self.__delay_seconds = delay_seconds

    def executeDownload(self, request):
        # retry automático com delay entre tentativas — lógica universal
        ...

    @abstractmethod
    def _fetch(self, request):
        # implementado pelo módulo: faz a requisição HTTP de fato
        pass
```

```python
# shared/base/base_extractor.py
class BaseExtractor(ABC):
    def executeExtraction(self, raw_content):
        # logging universal
        ...

    @abstractmethod
    def _extract(self, raw_content):
        # implementado pelo módulo: aplica os seletores no conteúdo bruto
        pass
```

```python
# shared/base/base_output.py
class BaseOutput(ABC):
    def executeOutput(self, raw_data):
        # logging universal
        ...

    @abstractmethod
    def _process(self, raw_data):
        # implementado pelo módulo: converte dados brutos em ResponseTransfer
        pass
```

> O construtor de `BaseDownloader` recebe os parâmetros de retry e delay. O `service` do downloader os repassa a partir da configuração do módulo. `BaseExtractor` e `BaseOutput` não possuem construtor.

### `shared/config/settings.py`

Lê o `.env` da raiz e expõe as variáveis de infraestrutura global como constantes Python. Nenhuma parte do sistema lê o `.env` diretamente — sempre importa de `settings.py`.

```python
import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
APP_PORT = int(os.getenv("APP_PORT", 8000))
API_KEY = os.getenv("API_KEY")
```

### `shared/exception/base_exception.py`

Define o contrato global do JSON de erro. Todas as exceptions específicas das etapas herdam dessa classe base, garantindo que qualquer erro retornado pela API sempre siga o mesmo formato, independente de qual domínio, módulo ou etapa o gerou.

```python
class BaseApiException(Exception):
    def __init__(self, code: str, message: str, stage: str, domain: str, target: str):
        super().__init__(message)
        self.code = code
        self.stage = stage
        self.domain = domain
        self.target = target
        self.response = {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "stage": stage,
                "domain": domain,
                "target": target
            }
        }
```

O handler global de exceções, registrado no `main.py` da raiz, captura qualquer `BaseApiException` e retorna seu `response` com status HTTP `422 Unprocessable Entity`.

### `shared/security/api_key_middleware.py`

Middleware global de autenticação. Intercepta toda requisição recebida pela API antes de chegar a qualquer módulo. Valida o header `X-API-Key` contra o valor definido em `settings.py`. Nenhum módulo conhece ou depende deste arquivo.

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from shared.config.settings import API_KEY


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")

        if not api_key or api_key != API_KEY:
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Invalid or missing API key."
                    }
                }
            )

        return await call_next(request)
```

**Regras do middleware:**
- Toda requisição sem o header `X-API-Key` ou com chave incorreta retorna `401`.
- O middleware não conhece domínios, módulos ou rotas. Valida apenas a chave.
- A chave é única e global para toda a API. Não há controle de acesso por módulo ou domínio.
- A `API_KEY` nunca tem valor padrão no código. Se ausente no `.env`, todas as requisições são bloqueadas.

---

## `main.py` do Módulo — O Orquestrador

O `main.py` dentro de cada módulo é o arquivo mais importante do módulo. Atua como um controller: recebe a requisição, orquestra todas as etapas em sequência e retorna o JSON final ao cliente.

**Responsabilidades do `main.py` do módulo:**
1. Definir os schemas Pydantic de entrada da API e declarar o objeto `router` do FastAPI, descoberto e registrado automaticamente pelo `main.py` da raiz. A rota declarada segue o padrão `/{dominio}/{modulo}` (o prefixo `/web-scraping` é aplicado no registro).
2. Receber o payload do POST já validado pelo schema Pydantic de entrada.
3. Instanciar o `RequestTransfer` do downloader e populá-lo com os dados do payload.
4. Consultar o cache antes de iniciar o pipeline.
5. Acionar o `downloader` e capturar seu retorno.
6. Passar o retorno do `downloader` para o `extractor`.
7. Passar o retorno do `extractor` para o `output`.
8. Gravar o resultado completo no cache e retornar o JSON final ao cliente.

**Regra fundamental:** as etapas nunca se comunicam diretamente entre si. O `main.py` do módulo é o único intermediário. O retorno de uma etapa vai para o `main.py`, que então passa para a próxima etapa. Isso garante isolamento total entre as etapas.

```
POST recebido → Middleware valida X-API-Key
     ↓
Pydantic valida o schema do payload (definido no main.py do módulo)
     ↓
main.py popula o RequestTransfer
     ↓
Consulta ao cache
     ↓ (cache miss)
Downloader → retorna conteúdo bruto para o main.py
     ↓
Extractor → recebe o bruto, retorna dados extraídos para o main.py
     ↓
Output → recebe os extraídos, retorna dados limpos para o main.py
     ↓
main.py grava no cache, aplica filtros/projeção e retorna ao cliente
```

### Schema de Entrada do Módulo

O `main.py` do módulo, como controller, é o único arquivo que conhece e declara o **contrato de entrada da API**. Os schemas Pydantic do payload — o schema raiz da busca, o schema dos filtros e, quando há projeção, o `AllowedField` — são definidos no próprio `main.py` do módulo. O FastAPI valida automaticamente o corpo do POST contra esse schema antes de o controller executar qualquer lógica; campos não previstos, tipos inválidos ou valores fora das restrições são rejeitados com `422` pelo próprio Pydantic.

> **Distinção crítica — schema de entrada × `transfer`:** são camadas diferentes, com responsabilidades diferentes, e não devem ser confundidas.
> - O **schema de entrada** usa Pydantic, é declarado no `main.py` do módulo e valida o que o consumidor externo envia no corpo do POST. É a borda da API.
> - O **`transfer`** é o DTO interno do pipeline. É uma classe Python pura. Transporta dados entre as etapas. Nunca usa Pydantic.
>
> O `main.py` do módulo recebe o payload validado e, a partir dele, popula o `RequestTransfer`. O Pydantic nunca cruza a fronteira interna do pipeline; os transfers nunca aparecem na borda HTTP.

---

## As Três Etapas do Pipeline

### Etapa 1 — Downloader

**Responsabilidade única:** comunicação com o mundo externo. Faz a requisição HTTP, lida com headers, user-agent, paginação, delays e retries. Não sabe nada sobre o conteúdo que recebe. Apenas traz o HTML ou JSON bruto. Se o site bloquear, é aqui que o erro acontece.

#### Classes do Downloader

**`configuration/configuration.py`**
Define todas as configurações necessárias para a requisição do módulo: URL base, headers HTTP, user-agent, timeout, limites de raspagem e demais parâmetros de acesso. É a primeira coisa que o `service` instancia. A escolha entre HTTPX e Playwright é definida aqui. Os valores específicos são definidos pelo módulo.

**`service/service.py`**
Orquestra a etapa. Instancia a `configuration`, executa a requisição (incluindo paginação, quando aplicável) usando HTTPX ou Playwright conforme definido pelo módulo, e retorna o conteúdo bruto. Herda de `BaseDownloader` e implementa `_fetch(request)`. Repassa os parâmetros de retry e delay à classe base a partir da configuração do módulo. Nunca implementa parsing ou transformação de dados.

**`validator/validator.py`**
Valida se a resposta recebida é utilizável antes de passar para o extractor. Verifica condições como resposta vazia, bloqueio ou captcha. Se inválida, lança a exception. Método principal: `validateResponse(response)`.

**`repository/repository.py`**
Consulta e grava no cache local do módulo. Antes de qualquer requisição externa, verifica se já existe resultado recente em cache para a mesma chave. A estratégia de chave de cache é definida pelo módulo. Métodos principais: `findCache(key)` e `saveCache(key, data)`.

**`transfer/request_transfer.py`**
DTO interno de entrada do downloader. Transporta os parâmetros da requisição de forma estruturada entre o `main.py` e a etapa. Classe Python pura com atributos privados, getters e setters, sem dependência de bibliotecas externas.

```python
class RequestTransfer:
    def __init__(self):
        self.__query = None
        self.__domain = None
        self.__target = None
        self.__filters = {}

    def getQuery(self): return self.__query
    def setQuery(self, query: str): self.__query = query

    def getDomain(self): return self.__domain
    def setDomain(self, domain: str): self.__domain = domain

    def getTarget(self): return self.__target
    def setTarget(self, target: str): self.__target = target

    def getFilters(self): return self.__filters
    def setFilters(self, filters: dict): self.__filters = filters
```

**`exception/exception.py`**
Erros específicos do downloader. Herda de `BaseApiException`. Os códigos de erro são definidos pelo módulo.

---

### Etapa 2 — Extractor

**Responsabilidade única:** ler o conteúdo bruto recebido do downloader e localizar os campos de interesse. Conhece a estrutura do HTML ou JSON do site alvo. Não limpa, não formata, não valida semanticamente — apenas extrai os campos no estado bruto em que estão. Os campos extraídos e os seletores utilizados são definidos pelo módulo.

#### Classes do Extractor

**`service/service.py`**
Orquestra a etapa. Recebe o conteúdo bruto do `main.py`, aplica os seletores específicos do site alvo e coleta os campos de interesse de cada item encontrado. Retorna os dados brutos extraídos para o `main.py`. Herda de `BaseExtractor` e implementa `_extract(raw_content)`. Nunca limpa, converte tipos ou transforma os dados — essa responsabilidade pertence ao output.

**`validator/validator.py`**
Valida se os campos obrigatórios foram extraídos antes de seguir para o output. Quando o site alvo muda seu HTML e os seletores param de funcionar, este validator detecta a condição e lança exception com código específico. Os campos obrigatórios são definidos pelo módulo. Método principal: `validateExtraction(data)`.

**`transfer/request_transfer.py`**
DTO interno de transporte dos dados extraídos brutos. Carrega os campos no estado exato em que foram encontrados no conteúdo, sem nenhum tratamento. Os atributos correspondem aos campos definidos pelo módulo. Classe Python pura com atributos privados, getters e setters.

**`exception/exception.py`**
Erros específicos do extractor. Herda de `BaseApiException`. Os códigos de erro são definidos pelo módulo.

---

### Etapa 3 — Output

**Responsabilidade única:** receber os dados extraídos brutos, transformá-los em dados limpos, tipados e padronizados, montar a coleção final de resultados e aplicar filtros e projeção de campos antes de retornar ao cliente. Remove sujeira, converte tipos, preenche campos ausentes com `null` e garante que a saída sempre segue o contrato definido pelo módulo.

#### Classes do Output

**`service/service.py`**
Orquestra a etapa. Recebe os dados brutos do `main.py`, utiliza o `mapper` para converter cada item e o `validator` para garantir o schema final. Retorna a coleção de `ResponseTransfer` pronta para serialização. Herda de `BaseOutput` e implementa `_process(raw_data)`.

O `service` do output também concentra a aplicação de **filtros** e **projeção de campos** sobre a coleção de resultados — operações que ocorrem após o mapeamento. Como essa lógica opera sobre o resultado já serializado, ela pode ser exposta como função(ões) auxiliar(es) no próprio arquivo do `service`, reutilizável tanto no caminho de pipeline executado quanto no caminho de cache hit.

**`mapper/mapper.py`**
Converte o `RequestTransfer` do extractor em `ResponseTransfer`. Aplica todas as transformações campo a campo (limpeza, conversão de tipo, normalização) conforme as regras definidas pelo módulo. Método principal: `mapProduct(raw)` ou equivalente conforme a entidade alvo.

**`validator/validator.py`**
Valida o `ResponseTransfer` final antes de retornar ao cliente. Garante que os campos obrigatórios estão presentes e os tipos estão corretos. Os campos obrigatórios são definidos pelo módulo. Método principal: `validateOutput(transfer)`.

**`transfer/response_transfer.py`**
DTO interno de saída do pipeline. Carrega os dados limpos, tipados e prontos para serialização. Classe Python pura com atributos privados, getters e setters. Implementa o método `toJson()`, que serializa o transfer em dicionário. Os atributos, seus getters/setters e o `toJson()` são definidos pelo módulo conforme o contrato de saída estabelecido em sua documentação.

**`exception/exception.py`**
Erros específicos do output. Herda de `BaseApiException`. Os códigos de erro são definidos pelo módulo.

---

## Tabela de Classes por Etapa

| Classe                       | Downloader | Extractor | Output |
|------------------------------|------------|-----------|--------|
| `configuration`              | Sim        | Não       | Não    |
| `service`                    | Sim        | Sim       | Sim    |
| `validator`                  | Sim        | Sim       | Sim    |
| `repository`                 | Sim        | Não       | Não    |
| `transfer/request_transfer`  | Sim        | Sim       | Não    |
| `transfer/response_transfer` | Não        | Não       | Sim    |
| `mapper`                     | Não        | Não       | Sim    |
| `exception`                  | Sim        | Sim       | Sim    |

---

## Filtros, Projeção e Limite

Além de `query`, o schema de entrada de um módulo pode aceitar campos opcionais que moldam a resposta sem alterar o scraping:

- **`filters`** — critérios que removem itens do conjunto de resultados (ex: faixa de preço, atributos booleanos).
- **`limit`** — teto inteiro positivo para o número de itens retornados.
- **`fields`** — lista de campos a projetar; quando omitida, todos os campos do contrato de saída são retornados.

Esses campos são declarados e validados pelos schemas Pydantic de entrada, no `main.py` do módulo, e aplicados pelo `output` sobre o resultado já mapeado. A ordem de aplicação é fixa: **filtros → limite → projeção**.

**Regra do `AllowedField`:** todo módulo que suportar o campo `fields` no payload deve declarar explicitamente um `AllowedField` — um `Literal` tipado com os campos permitidos para projeção — no `main.py` do módulo, junto aos demais schemas Pydantic de entrada. O Pydantic usa esse `Literal` para validar os valores de `fields` na borda da API, rejeitando com `422` qualquer campo não declarado. A projeção em si é responsabilidade do `output`, aplicada após filtros e limite.

**Relação com o cache:** o cache armazena sempre o **resultado completo e não-filtrado** do pipeline. Filtros, limite e projeção são aplicados na montagem da resposta — tanto no caminho de cache hit quanto no de pipeline executado. Isso permite que a mesma entrada de cache atenda requisições com filtros diferentes. Os campos aceitos, seus tipos e seus efeitos são definidos pelo módulo em sua documentação.

---

## Cache

O cache é responsabilidade do **downloader**, gerenciado pelo seu `repository`. Antes de qualquer requisição externa, o repository verifica se já existe resultado recente para a mesma chave de cache.

O cache é armazenado localmente no módulo em `shared/infra/cache/`, em arquivos JSON no disco. Cada entrada guarda um timestamp de gravação, usado para calcular a expiração contra o TTL configurado. Não há dependência de serviços externos como Redis.

**Fluxo do cache:**
```
main.py aciona o repository do downloader
     ↓
repository verifica o cache local
     ↓ (hit — resultado recente encontrado)
retorna o resultado completo sem executar o pipeline
     ↓ (miss — cache expirado ou inexistente)
executa o pipeline completo (downloader → extractor → output)
     ↓
repository grava o resultado completo no cache
     ↓
main.py aplica filtros/limite/projeção e retorna o JSON ao cliente
```

**Limpeza de cache (`shared/infra/cache/cleaner.py`):** rotina de housekeeping que remove do disco as entradas de cache expiradas ou corrompidas. É executada de forma agendada (ver seção **Tarefas Agendadas**), não no caminho de uma requisição.

> A estratégia de chave de cache (quais parâmetros a compõem) e o TTL padrão são definidos pelo módulo. O comportamento do cache (habilitado/desabilitado e expiração) é controlado pela configuração do módulo.

---

## Tarefas Agendadas (`jobs.py`)

Um módulo pode declarar tarefas recorrentes — por exemplo, a limpeza periódica do cache. Para isso, expõe um arquivo `jobs.py` na raiz do módulo com uma função `register_jobs(scheduler)`:

```python
from {dominio}.{modulo}.shared.infra.cache.cleaner import clean_expired_cache

def register_jobs(scheduler):
    scheduler.add_job(clean_expired_cache, "cron", hour=3)
```

O `main.py` da raiz, em seu `lifespan`, cria um único `AsyncIOScheduler`, descobre automaticamente todos os `jobs.py` dos módulos e chama o `register_jobs` de cada um, passando o scheduler compartilhado. O agendador é iniciado no startup e encerrado no shutdown da aplicação.

`jobs.py` é **opcional**: um módulo sem tarefas agendadas simplesmente não o declara. O `main.py` da raiz nunca é editado para isso — a descoberta é genérica.

---

## Contrato de Resposta de Sucesso

O envelope de resposta é universal para todos os módulos:

```json
{
    "success": true,
    "domain": "{dominio}",
    "target": "{modulo}",
    "query": "{termo buscado}",
    "total": 48,
    "cached": false,
    "results": [
        { ... }
    ]
}
```

- `cached` indica se o resultado veio do cache (`true`) ou do pipeline executado (`false`).
- `total` representa o número de itens em `results` após filtros, limite e projeção.
- O schema de cada objeto dentro de `results` é definido pelo módulo, conforme seu contrato de saída.

---

## Contrato de Resposta de Erro

Toda exception lançada em qualquer etapa herda de `BaseApiException` e produz um JSON de erro universal. O handler global converte essa exception em resposta HTTP `422`.

```json
{
    "success": false,
    "error": {
        "code": "{STAGE_CODIGO_DO_ERRO}",
        "message": "{mensagem descritiva}",
        "stage": "{downloader | extractor | output}",
        "domain": "{dominio}",
        "target": "{modulo}"
    }
}
```

Casos de erro especiais:
- **`401 Unauthorized`** — produzido pelo middleware de segurança quando a `X-API-Key` é inválida ou ausente. Não passa pelo contrato de etapas.
- **`422 Unprocessable Entity`** — produzido tanto pelo Pydantic (payload com schema inválido) quanto pelo handler global de `BaseApiException` (erro em qualquer etapa do pipeline).

> Os códigos de erro específicos de cada etapa seguem o padrão `{STAGE_CODIGO_DO_ERRO}` — sempre prefixados pela etapa de origem — e são definidos na documentação do próprio módulo.

---

## `shared/` Local do Módulo

Cada módulo possui sua própria pasta `shared/` para recursos internos compartilhados entre suas etapas. Nenhum conteúdo da `shared/` local de um módulo deve ser acessado por outro módulo ou pelo projeto global.

```
{modulo}/
└── shared/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    └── infra/
        ├── __init__.py
        └── cache/
            ├── __init__.py
            └── cleaner.py
```

### `{modulo}/shared/config/settings.py`

Carrega o `.env` do módulo e expõe as variáveis operacionais como constantes Python. É o equivalente, em escopo de módulo, do `settings.py` global. Carrega explicitamente o `.env` localizado na raiz do próprio módulo:

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

### `{modulo}/.env`

Configuração operacional do módulo. Não versionado no GitHub. Exemplo de variáveis:

```
CACHE_ENABLED=true
CACHE_EXPIRATION_MINUTES=1440
HTTP_TIMEOUT_SECONDS=30
HTTP_RETRY_ATTEMPTS=3
HTTP_DELAY_SECONDS=2
```

> As variáveis efetivas de cada módulo são definidas pelo próprio módulo. Nenhuma classe do módulo lê o `.env` diretamente — sempre importa do `settings.py` do módulo.

### `{modulo}/shared/infra/`

Infraestrutura interna do módulo. Contém a pasta `cache/`, com a rotina de limpeza (`cleaner.py`) e os arquivos JSON de cache gerados em tempo de execução.

---

## Nomenclatura

### Arquivos e Classes

O nome do arquivo é o nome da classe em `snake_case`. O nome da classe no código segue `PascalCase`.

| Arquivo                | Classe             |
|------------------------|--------------------|
| `service.py`           | `Service`          |
| `validator.py`         | `Validator`        |
| `configuration.py`     | `Configuration`    |
| `repository.py`        | `Repository`       |
| `mapper.py`            | `Mapper`           |
| `request_transfer.py`  | `RequestTransfer`  |
| `response_transfer.py` | `ResponseTransfer` |
| `base_downloader.py`   | `BaseDownloader`   |
| `base_exception.py`    | `BaseApiException` |

> Os modelos Pydantic do schema de entrada, definidos no `main.py` do módulo, também seguem `PascalCase`, com nomes descritivos do papel de cada modelo (ex: o schema do payload de busca, o schema dos filtros).

### Métodos

Os métodos das classes do pipeline seguem o padrão `[prefixo][Entidade]` em `camelCase`:

| Classe          | Prefixo                  | Exemplo                          |
|-----------------|--------------------------|----------------------------------|
| `configuration` | `setup` / `configure`    | `setupBaseUrl()`                 |
| `service`       | `execute` / `process`    | `executeDownload()`              |
| `validator`     | `validate`               | `validateResponse()`             |
| `repository`    | `find` / `save`          | `findCache()`, `saveCache()`     |
| `mapper`        | `map`                    | `mapProduct()`                   |
| `exception`     | *(lançadas diretamente)* | `raise DownloaderException(...)` |

> Os modelos Pydantic do schema de entrada são declarativos e não seguem esse padrão de métodos.

### Pastas e Domínios

- Nomes de domínios e módulos seguem `snake_case` (letras minúsculas e underscores).
- Nomes de etapas são fixos: `downloader`, `extractor`, `output`. Nunca renomeie as etapas nem crie etapas alternativas.

---

## Fluxo Completo — do POST ao JSON

1. O cliente envia um `POST` para `/web-scraping/{dominio}/{modulo}` com o header `X-API-Key` e o payload de busca.
2. O middleware `ApiKeyMiddleware` valida a chave. Se inválida ou ausente, retorna `401` imediatamente.
3. O FastAPI valida o corpo do POST contra o schema Pydantic de entrada definido no `main.py` do módulo. Se inválido, retorna `422`.
4. O `main.py` do módulo recebe o payload validado e instancia o `RequestTransfer` do downloader, populando-o com os dados do payload.
5. O `main.py` aciona o `repository` do downloader para consultar o cache.
6. **Cache hit:** o `main.py` aplica filtros, limite e projeção sobre o resultado completo em cache e retorna o envelope com `cached: true`, sem executar o pipeline.
7. **Cache miss:** o `main.py` aciona o `service` do downloader.
8. O downloader lê a `configuration`, executa a requisição (com paginação, retries e delays), valida a resposta com o `validator` e retorna o conteúdo bruto ao `main.py`.
9. O `main.py` passa o conteúdo bruto para o `service` do extractor.
10. O extractor aplica os seletores, extrai os campos brutos, valida com o `validator` e retorna os `RequestTransfer` populados ao `main.py`.
11. O `main.py` passa os dados extraídos para o `service` do output.
12. O output usa o `mapper` para converter os dados brutos em `ResponseTransfer` e o `validator` para garantir o schema final, retornando a coleção ao `main.py`.
13. O `main.py` serializa cada `ResponseTransfer` via `toJson()` e grava o resultado completo no cache via `repository`.
14. O `main.py` aplica filtros, limite e projeção e retorna o envelope de sucesso com `cached: false` ao cliente.

---

## Regras de Negócio

- Toda requisição deve conter o header `X-API-Key` com a chave válida configurada no `.env` da raiz.
- Toda vez que um módulo for acionado, é obrigatório verificar o cache antes de iniciar o pipeline.
- As etapas nunca se comunicam diretamente entre si. O `main.py` do módulo é o único intermediário.
- A lógica de cada módulo é completamente isolada. Nenhum módulo acessa pastas ou classes de outro módulo. A única dependência cruzada permitida é o uso das classes base e da configuração global em `shared/`.
- Os schemas Pydantic de entrada, declarados no `main.py` do módulo, validam o payload na borda da API; os `transfer` (classes puras) transportam dados dentro do pipeline. As duas camadas nunca se misturam.
- Toda exception lançada em qualquer etapa segue o contrato de `BaseApiException` e resulta em resposta `422`.
- O cache armazena sempre o resultado completo e não-filtrado; filtros, limite e projeção são aplicados na montagem da resposta.
- Regras e configurações operacionais de um módulo ficam dentro do módulo. O `.env` e o `settings.py` da raiz são exclusivos para infraestrutura global.
- Todos os módulos seguem exatamente a mesma estrutura de pastas, etapas e classes. O que muda entre módulos é exclusivamente a implementação interna de cada classe.
- Todo diretório do projeto deve conter um `__init__.py` vazio.
- A responsabilidade de persistir definitivamente os dados retornados é do sistema consumidor, não da API.
- O projeto respeita o arquivo `robots.txt` dos sites alvo e segue as diretrizes da LGPD.

---

## Desafios de Confiabilidade

- **Evasão de bloqueio de IP:** uso de proxies residenciais rotativos quando necessário. Configurado na `configuration` do downloader do módulo.
- **Resolução de captcha:** integração com serviços especializados quando necessário, na etapa de downloader.
- **Mudança de estrutura do site:** quando o site alvo altera seu HTML, o extractor para de funcionar. O `validator` do extractor detecta a condição e lança exception com código específico do módulo.
- **Rate limiting:** delays configuráveis entre requisições, definidos na configuração do módulo.
- **Conformidade legal:** respeito ao `robots.txt` dos sites alvo e conformidade com a LGPD.

---

## Como Adicionar um Novo Módulo

1. Criar a pasta do novo alvo dentro do domínio correspondente.
2. Replicar exatamente a estrutura de pastas e classes definida neste documento, incluindo um `__init__.py` vazio em cada pasta.
3. Documentar o módulo: contrato de entrada, contrato de saída, seletores, paginação, estratégia de cache e códigos de exception.
4. Implementar cada classe das três etapas, herdando das respectivas classes base em `shared/base/`.
5. Definir os schemas Pydantic do payload no `main.py` do módulo.
6. Adaptar a `configuration` com os parâmetros de acesso do novo site.
7. Adaptar o `service` do extractor com os seletores específicos do novo site.
8. Adaptar o `mapper` do output com as regras de normalização do novo site.
9. Criar o `.env` e o `settings.py` do módulo com sua configuração operacional.
10. Declarar o objeto `router` no `main.py` do módulo, com a rota `/{dominio}/{modulo}`.
11. Opcionalmente, declarar um `jobs.py` com `register_jobs(scheduler)` para tarefas agendadas.
12. Opcionalmente, declarar um `requirements.txt` do módulo com dependências exclusivas.

> Não é necessário editar o `main.py` da raiz: o router e os jobs do novo módulo são descobertos e registrados automaticamente.

---

## Como Adicionar um Novo Domínio

1. Criar a pasta do novo domínio na raiz do projeto com um `__init__.py` vazio.
2. Criar os módulos dentro do domínio seguindo a mesma hierarquia universal.
3. Todos os módulos do novo domínio seguem exatamente a mesma estrutura definida neste documento.
