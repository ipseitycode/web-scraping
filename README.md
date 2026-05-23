# web-scraping-api

[![Playlist YouTube - web-scraping-api](https://img.youtube.com/vi/AhOOZfWk51g/maxresdefault.jpg)](https://youtube.com/playlist?list=PLz9bzqrAthDlqWNLfrcVzUaakjcm68NKc&si=s1dAcm8KCyNzkb6b)


## 📋 Descrição

**web-scraping-api** é uma **API de web scraping profissional, modular e escalável**, desenvolvida em Python com FastAPI. Seu contrato é simples: recebe um `POST` com os parâmetros de busca e retorna os dados extraídos em JSON limpo e padronizado.

Diferente de uma API focada em um único alvo, o projeto foi desenhado como uma **plataforma genérica de scraping**, capaz de hospedar diversos **domínios de interesse** (marketplace, news, business, etc.) e, dentro de cada domínio, múltiplos **módulos-alvo** (mercadolivre, olx, shopee, e assim por diante). Cada módulo é completamente isolado, segue exatamente a mesma estrutura interna e pode ser desenvolvido, validado e revisado **por agentes de IA orquestrados sob um conjunto rígido de regras**.


## 🎯 Proposta

O projeto tem três propósitos principais:

1. **Servir como API de produção** — uma única instância atende raspagens de N alvos diferentes via endpoints padronizados (`POST /web-scraping/{dominio}/{modulo}`).
2. **Servir como esqueleto agêntico** — toda a estrutura do projeto (pastas, classes, contratos, naming conventions) está documentada em arquivos de regras (`.agent/rules/`) que orientam agentes de IA na criação automática de novos módulos.
3. **Compartilhar com a comunidade dev** — divulgar o resultado de meses de estudo aplicado em Python, arquitetura de software e orquestração de agentes de IA, deixando uma base pronta para qualquer dev que queira estudar, estender ou usar.


## 🧱 Arquitetura

O projeto é organizado em **5 níveis hierárquicos**:

```
Projeto (web-scraping-api)
└── Domínio (marketplace, news, business, ...)
    └── Módulo / Alvo (mercadolivre, olx, shopee, ...)
        └── Etapa (downloader, extractor, output)
            └── Classe (service, validator, mapper, transfer, ...)
```

**Regra estrutural fundamental:** todos os módulos, independente do domínio, seguem **exatamente a mesma estrutura de pastas, etapas e classes**. O que muda entre módulos é exclusivamente o código dentro de cada classe, adaptado às regras de negócio e ao HTML do site alvo.

### Pipeline universal de 3 etapas

| Etapa        | Responsabilidade |
|--------------|------------------|
| `downloader` | Buscar o conteúdo bruto na fonte (HTTP / browser headless), com retry, delay, paginação e cache |
| `extractor`  | Aplicar seletores CSS sobre o conteúdo bruto e extrair os campos crus do DOM |
| `output`     | Mapear, validar, filtrar, limitar e projetar os dados, devolvendo o JSON final |

Cada etapa tem seu próprio `service`, `validator`, `transfer` e `exception`. As etapas **nunca se comunicam diretamente entre si** — o `main.py` do módulo é o único orquestrador.

### Descoberta automática de módulos

O `main.py` da raiz não conhece módulos específicos. Ele varre o projeto buscando `main.py` e `jobs.py` dentro dos módulos e registra os routers e jobs automaticamente. **Para adicionar um novo módulo, basta criá-lo na estrutura padrão — nenhuma linha do código raiz precisa ser tocada.**


## 🤖 Fluxo Agêntico

A maior aposta do projeto é que **grande parte do trabalho de criação de um novo módulo seja feita por agentes de IA**, não escrita à mão.

Em `.agent/rules/` ficam **19 arquivos de regras** que descrevem, sem ambiguidade, todos os contratos do projeto: estrutura de pastas, naming conventions, contratos de cada etapa, schemas de transfer, contratos de exception, regras de cache, regras de segurança, etc.

Em `.agent/skills/` ficam os **agentes responsáveis pelo ciclo de vida de um módulo**:

| Agente | Função |
|--------|--------|
| `agent-creator`   | Cria o módulo completo a partir do `MAP.md` e das regras |
| `agent-validator` | Valida se o módulo respeita todos os contratos definidos |
| `agent-broker`    | Coordena o fluxo entre os demais agentes |

O fluxo recomendado para criação de um módulo está em `devtools/docs/ROADMAP.md` e divide o trabalho em três blocos:

1. **Planejamento** — identidade, objetivo, dados desejados e fonte
2. **Exploração** — script descartável que valida hipóteses de acesso, paginação, seletores e dados
3. **Definição** — consolidação no `MAP.md` do módulo, que serve de input para o agente criador

> O `MAP.md` é o documento que une o "o quê" e o "como" de um módulo. Com ele pronto, o agente criador consegue gerar todo o módulo seguindo as regras.


## 📦 Módulos Inclusos

| Domínio       | Módulo         | Status |
|---------------|----------------|--------|
| `marketplace` | `mercadolivre` | ✅ **Funcional** (na data do commit). Usa Playwright + BeautifulSoup, paginação por offset, hard cap de 500 itens, cache de 24h e contratos completos de filtros / projeção / limite |
| `marketplace` | `olx`          | ⚠️ **Demonstrativo**. Não está em paridade funcional com o `mercadolivre`. Foi incluído exclusivamente para **documentar o fluxo completo de criação de um módulo via IA**, do `ROADMAP.md` ao deploy em VPS, com toda a jornada registrada na playlist do YouTube |

> Sites mudam o HTML com frequência. O Mercado Livre estava funcional na data do commit; revisões dos seletores podem ser necessárias com o tempo. O `validator` do extractor detecta a quebra e lança exception com código específico.


## 🛠️ Tecnologias

| Tecnologia | Papel |
|------------|-------|
| Python 3 | Linguagem base |
| FastAPI | Exposição de endpoints HTTP |
| Pydantic | Validação do payload de entrada |
| HTTPX | Cliente HTTP para sites estáticos |
| BeautifulSoup | Parsing de HTML |
| Playwright | Browser headless para sites com JS rendering |
| APScheduler | Jobs agendados (ex: limpeza de cache) |
| python-dotenv | Variáveis de ambiente |
| Uvicorn | Servidor ASGI |
| Docker | Containerização para deploy em VPS |


## 🚀 Como Usar

### Instalação local

```bash
# clonar o repositório
git clone https://github.com/ipseitycode/web-scraping.git
cd web-scraping

# criar e ativar venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# instalar dependências (raiz + módulos + chromium do playwright)
bash install.sh
```

Configure o `.env` da raiz:

```env
APP_ENV=development
APP_PORT=8000
API_KEY=sua_chave_aqui
```

Configure também o `.env` de cada módulo (ex: `marketplace/mercadolivre/.env`) com as variáveis operacionais (`CACHE_ENABLED`, `CACHE_EXPIRATION_MINUTES`, `HTTP_TIMEOUT_SECONDS`, `HTTP_RETRY_ATTEMPTS`, `HTTP_DELAY_SECONDS`).

Suba a API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Deploy via Docker

```bash
docker build -t web-scraping-api .
docker run -p 8000:8000 --env-file .env web-scraping-api
```

### Exemplo de requisição

```http
POST http://localhost:8000/web-scraping/marketplace/mercadolivre
Content-Type: application/json
X-API-Key: sua_chave_aqui

{
  "query": "notebook",
  "filters": {
    "price_min": 1200,
    "price_max": 3000,
    "free_shipping": true,
    "min_rating": 4.0,
    "has_discount": true
  },
  "fields": ["title", "price", "url", "shipping"],
  "limit": 20
}
```

> O contrato exato de cada módulo (campos disponíveis, filtros suportados, projeção) está documentado no `MAP.md` da pasta do módulo.


## 📚 Documentação

Toda a documentação técnica do projeto fica em `devtools/docs/`:

- **`devtools/docs/visao-geral.md`** — documento mestre. Cobre arquitetura, contratos de cada etapa, regras estruturais, fluxo completo do POST ao JSON, regras de negócio e instruções para adicionar novos módulos e domínios.
- **`devtools/docs/ROADMAP.md`** — passo a passo (Planejamento → Exploração → Definição) para criar um módulo do zero, pronto para ser consumido por um agente de IA.
- **`{dominio}/{modulo}/MAP.md`** — documento de scraping de cada módulo. Detalha identidade, dados, fonte, seletores, paginação, cache, exceptions e contrato de payload.

Para entender o projeto **na prática**, a playlist no YouTube traz mais de **5 horas de gravação** comentando tudo:

🎥 **[Playlist completa no YouTube](https://youtube.com/playlist?list=PLz9bzqrAthDlqWNLfrcVzUaakjcm68NKc&si=s1dAcm8KCyNzkb6b)**

A playlist cobre, na ordem:

1. Visão geral do projeto (arquitetura, FastAPI, papel da IA na orquestração)
2. Apresentação do `MAP.md` do Mercado Livre
3. Teste do módulo `mercadolivre` em produção
4. Fluxo agêntico na teoria (regras, agentes, ciclo de criação de módulos)
5. Criação completa do módulo `olx` na prática — do `ROADMAP.md` ao deploy em VPS, com IA fazendo o trabalho pesado


## 👤 Autor

**Cauan Gomes**

- GitHub: [@ipseitycode](https://github.com/ipseitycode)
- YouTube: [Playlist do projeto](https://youtube.com/playlist?list=PLz9bzqrAthDlqWNLfrcVzUaakjcm68NKc&si=s1dAcm8KCyNzkb6b)
- Linkedin: [Perfil do Linkedin](https://www.linkedin.com/in/ipseitycode/)


## ⚖️ Considerações Legais

Este projeto respeita o arquivo `robots.txt` dos sites alvo e foi desenvolvido em conformidade com a LGPD. A responsabilidade pelo uso ético dos dados coletados é integralmente do consumidor da API.