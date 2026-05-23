# Scraping Map — `olx`

## 1. Identidade

- **Nome do módulo:** olx
- **Domínio pai:** marketplace
- **Entidade alvo:** Produtos listados na busca da OLX

## 2. Objetivo

- **Por que estamos raspando isso?** Coletar dados de produtos disponíveis na OLX com base em uma query de busca, retornando as informações estruturadas em JSON.
- **Qual problema de negócio resolve?** Permite que sistemas consumidores obtenham dados atualizados de produtos e preços da OLX sem depender de uma API oficial, que é limitada e paga.
- **Quem vai consumir esses dados?** Sistemas externos via POST HTTP, dashboards desenvolvidos como produtos derivados, e uso interno da software house para análise de mercado e precificação.

## 3. Dados esperados

| Campo          | Tipo            | Obrigatório | Descrição |
|----------------|-----------------|-------------|-----------|
| `title`        | string          | Sim         | Título do anúncio conforme exibido |
| `price`        | string          | Sim         | Preço bruto conforme exibido (ex: `"R$ 600"`) |
| `url`          | string          | Sim         | Link direto para o anúncio na OLX |
| `location`     | string          | Não         | Cidade e bairro do anunciante — `null` quando ausente no DOM |
| `date`         | string          | Não         | Data bruta de publicação (ex: `"Hoje, 14:41"` / `"20 de mai, 19:36"`) — `null` quando ausente |
| `image`        | string          | Não         | URL da imagem principal do anúncio — `null` quando ausente |
| `installments` | string          | Não         | Texto bruto das parcelas (ex: `"em até3x de R$ 200,00sem juros"`) — `null` quando ausente |
| `badges`       | lista de string | Não         | Badges do anúncio — `null` quando ausente |
| `image_count`  | int             | Não         | Quantidade de fotos no anúncio — `null` quando ausente |

> **Campos obrigatórios:** itens cujo mapeamento não produza `title`, `price` e `url` são **descartados individualmente** pelo `output` (ver seção 9). A requisição não falha por causa de um item incompleto.

> **Sobre `price`:** retornado como string bruta (`"R$ 600"`). Conversão para float é responsabilidade do sistema consumidor.

> **Sobre `installments`:** retornado como string bruta sem espaços entre os tokens (ex: `"em até3x de R$ 266,67sem juros"`). Normalização é responsabilidade do sistema consumidor.

> **Sobre `badges`:** aparece apenas em anúncios com integração ao sistema de pagamento/entrega da OLX. Valores conhecidos: `"Frete grátis"`, `"Entrega Fácil"`, `"Pague Online"`, `"Parcele sem juros"`, `"Aceita trocas"`, `"Reduziu o preço"`.

## 4. Fonte

- **Site/plataforma:** OLX Brasil
- **Tipo de página:** Listagem de resultados de busca
- **URL base:** `https://www.olx.com.br`
- **Padrão de acesso:**
  - Primeira página: `https://www.olx.com.br/{estado}?q={query}`
  - Páginas seguintes: `https://www.olx.com.br/{estado}?q={query}&o={pagina}`
  - Exemplo: `https://www.olx.com.br/estado-ba?q=celular&o=2`

---

## 5. Acesso

- **Requer autenticação?** Não
- **Requer JS rendering?** **Sim** — requisição com `requests` retornou HTTP 403. Utiliza **Playwright** (Chromium headless) + BeautifulSoup.
- **Selector de espera:** `section.olx-adcard` — aguardado via `wait_for_selector` antes de fazer o parse do HTML. O timeout é o `HTTP_TIMEOUT_SECONDS` da configuração do módulo (padrão 30s).
- **Cliente HTTP:** definido na `configuration` via `client_type = "playwright"`.

### Configuração do navegador (`downloader/configuration/configuration.py`)

| Parâmetro     | Valor |
|---------------|-------|
| `base_url`    | `https://www.olx.com.br` |
| `client_type` | `playwright` |
| `user_agent`  | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36` |
| `viewport`    | `1366 x 768` |
| `locale`      | `pt-BR` |
| `timezone`    | `America/Sao_Paulo` |
| `launch_args` | `--disable-blink-features=AutomationControlled`, `--no-sandbox`, `--disable-dev-shm-usage` |
| `max_items`   | `200` (hard cap de raspagem) |

### Contorno de detecção de bot

A OLX aplica detecção de automação. As medidas atuais, todas no downloader:

- `launch_args` com `--disable-blink-features=AutomationControlled`.
- `user_agent`, `viewport`, `locale` e `timezone` realistas no contexto do navegador.
- Script de inicialização que sobrescreve `navigator.webdriver` para `undefined`.

> Estas medidas podem precisar de revisão caso a OLX reforce a detecção.

---

## 6. Seletores CSS

| Campo          | Seletor                                 | Extração |
|----------------|-----------------------------------------|----------|
| card           | `section.olx-adcard`                    | Container de cada anúncio |
| `title`        | `h2.olx-adcard__title`                  | `.get_text(strip=True)` |
| `price`        | `h3.olx-adcard__price`                  | `.get_text(strip=True)` |
| `url`          | `a[data-testid="adcard-link"]`          | `.get('href')` |
| `location`     | `p.olx-adcard__location`                | `.get_text(strip=True)`. `null` se ausente |
| `date`         | `p.olx-adcard__date`                    | `.get_text(strip=True)`. `null` se ausente |
| `image`        | `.olx-adcard__media img`                | `.get('src')`. `null` se ausente |
| `installments` | `[data-testid="adcard-price-info"]`     | `.get_text(strip=True)`. `null` se ausente |
| `badges`       | `.olx-adcard__badges div`               | lista de `.get_text(strip=True)`. `null` se ausente |
| `image_count`  | `.olx-adcard__carousel--bullet`         | `len()` dos elementos encontrados. `null` se ausente |

---

## 7. Operacional

- **Estratégia de paginação:**
  - Primeira página: sem parâmetro de offset (`/{estado}?q={query}`)
  - Páginas seguintes: parâmetro `&o=N`, incremento de `+1` por página
  - Loop interrompido quando: (a) `wait_for_selector('section.olx-adcard')` lançar `TimeoutError`, ou (b) a página retornar zero cards

- **Hard cap de raspagem:** `200` itens. Constante hardcoded em `downloader/configuration/configuration.py` (`__max_items`), exposta via `setupMaxItems()`. **Não usa variável de ambiente** — regras do módulo ficam dentro do módulo. Para alterar o valor, editar a classe e reiniciar.
- **Rate limit / delay:** delay entre páginas e entre retries, configurável via `HTTP_DELAY_SECONDS` no `.env` do módulo (padrão 2s).
- **Retries:** o downloader herda o retry automático de `BaseDownloader`, com `HTTP_RETRY_ATTEMPTS` tentativas (padrão 3).

### Cache

- **Localização:** `shared/infra/cache/`, um arquivo JSON por chave.
- **Chave de cache:** `olx_{estado}_{query-normalizada}` — a query é normalizada em minúsculas, com espaços convertidos em hífen. Exemplo: `olx_estado-ba_celular`.
- **Conteúdo:** o cache armazena o resultado **completo, não-filtrado**, já truncado no hard cap de 200 itens. Filtros, `limit` e `fields` são aplicados na resposta, não no cache.
- **TTL:** `CACHE_EXPIRATION_MINUTES` no `.env` do módulo (padrão 1440 min = 24h). A expiração é verificada na leitura, comparando o `_timestamp` gravado.
- **Habilitar/desabilitar:** `CACHE_ENABLED` no `.env` do módulo.

### Limpeza agendada de cache

- O módulo expõe um `jobs.py` com `register_jobs(scheduler)`, que agenda a rotina `clean_expired_cache` (`shared/infra/cache/cleaner.py`) via cron, diariamente às 3h.
- O `cleaner` remove arquivos de cache com mais de **48 horas**, além de arquivos ilegíveis ou sem timestamp válido.
- Esse limite de 48h é independente do TTL de leitura (24h): a leitura já ignora cache expirado; a limpeza apenas faz a faxina do disco.

---

## 8. Contrato de entrada — payload HTTP

O schema do payload é validado por Pydantic e declarado no `main.py` do módulo (`SearchPayload`). Campos desconhecidos no objeto raiz ou em `filters` são rejeitados com HTTP 422 (`extra='forbid'` nos filtros).

| Campo     | Tipo                    | Obrigatório | Descrição |
|-----------|-------------------------|-------------|-----------|
| `query`   | string                  | Sim         | Termo de busca |
| `estado`  | string                  | Não         | Slug do estado (ex: `"estado-ba"`). Padrão: `"brasil"` |
| `filters` | objeto                  | Não         | Critérios de filtragem (ver abaixo) |
| `fields`  | lista de string         | Não         | Projeção de campos (ver abaixo) |
| `limit`   | inteiro positivo (`>0`) | Não         | Teto de itens na resposta |

Filtros, `limit` e projeção são aplicados pelo `output` após o scraping, tanto no caminho fresh quanto no cache hit. A ordem de aplicação é fixa: **filtros → limit → projeção**.

### Filtros (`filters`)

| Filtro             | Tipo   | Efeito |
|--------------------|--------|--------|
| `price_min`        | float  | Exclui produtos cujo `price` normalizado seja inferior ao valor |
| `price_max`        | float  | Exclui produtos cujo `price` normalizado seja superior ao valor |
| `has_installments` | bool   | Quando `true`, mantém apenas produtos com `installments != null` |
| `location`         | string | Mantém apenas produtos cujo `location` contenha o valor como substring (case-insensitive) |

> Filtros desconhecidos são rejeitados pelo Pydantic com HTTP 422.

> Filtros `price_min` e `price_max` requerem normalização interna do campo `price` (remoção de `"R$ "` e conversão para float) antes da comparação. Essa normalização ocorre apenas na camada de filtragem — o campo `price` continua sendo retornado como string bruta na resposta.

### Limite de itens (`limit`)

Campo opcional inteiro positivo. Aplicado **depois dos filtros e antes da projeção**.

- Omitido → retorna até o hard cap do módulo (200 itens — ver seção 7).
- `limit ≤ hard cap` → retorna até `limit` itens.
- `limit > hard cap` → retorna até o hard cap (cap silencioso, sem erro).
- `limit ≤ 0` → rejeitado pelo Pydantic com HTTP 422.

Quando combinado com filtros que removem muitos itens, a resposta pode ter **menos** que `limit` — `limit` é um teto sobre o conjunto filtrado, não um número garantido.

### Projeção (`fields`)

Lista opcional. Quando omitida, retorna todos os campos da seção 3. Valores permitidos:
`title`, `price`, `url`, `location`, `date`, `image`, `installments`, `badges`, `image_count`.

É possível filtrar ou limitar por um campo que não esteja em `fields`.

### Exemplo de payload

```json
{
  "query": "celular",
  "estado": "estado-ba",
  "filters": {
    "price_max": 1000,
    "has_installments": true,
    "location": "Salvador"
  },
  "fields": ["title", "price", "url", "location"],
  "limit": 50
}
```

---

## 9. Exceptions

Todas herdam de `BaseApiException`. As exceptions de **downloader** e **extractor** interrompem a requisição e retornam HTTP 422 ao cliente. As exceptions de **output** têm comportamento diferente (ver nota abaixo).

| Código                         | Etapa      | Quando ocorre |
|--------------------------------|------------|---------------|
| `DOWNLOADER_EMPTY_RESPONSE`    | downloader | Nenhuma página coletada (timeout em todas as tentativas) |
| `EXTRACTOR_SELECTOR_NOT_FOUND` | extractor  | Nenhum card encontrado — seletores possivelmente quebrados pela mudança do HTML do site |
| `OUTPUT_MISSING_TITLE`         | output     | Item sem `title` após o mapeamento |
| `OUTPUT_MISSING_PRICE`         | output     | Item sem `price` após o mapeamento |
| `OUTPUT_MISSING_URL`           | output     | Item sem `url` após o mapeamento |

> **Comportamento das exceptions de `output`:** o `validator` do output lança `OUTPUT_MISSING_*` por item. O `service` do output **captura essas exceptions, registra um warning e descarta o item inválido**, seguindo com os demais. Exceptions de output **não chegam ao cliente** — funcionam como um filtro de integridade item a item. Apenas downloader e extractor produzem o erro 422.

---

> **Versão:** 1.0
> **Última atualização:** 2026-05-22
> **Observações:** Os seletores CSS devem ser revisados caso a OLX altere a estrutura do HTML — detecção feita pelo `validator` do extractor via exception `EXTRACTOR_SELECTOR_NOT_FOUND`.