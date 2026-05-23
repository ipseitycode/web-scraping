# Scraping Map — `mercadolivre`

## 1. Identidade

- **Nome do módulo:** mercadolivre
- **Domínio pai:** marketplace
- **Entidade alvo:** Produtos listados na busca do Mercado Livre

## 2. Objetivo

- **Por que estamos raspando isso?** Coletar dados de produtos disponíveis no Mercado Livre com base em uma query de busca, retornando as informações estruturadas em JSON.
- **Qual problema de negócio resolve?** Permite que sistemas consumidores obtenham dados atualizados de produtos e preços do Mercado Livre sem depender de uma API oficial, que é limitada e paga.
- **Quem vai consumir esses dados?** Sistemas externos via POST HTTP, dashboards desenvolvidos como produtos derivados, e uso interno da software house para análise de mercado e precificação.

## 3. Dados esperados

| Campo            | Tipo   | Obrigatório | Descrição |
|------------------|--------|-------------|-----------|
| `title`          | string | Sim         | Nome completo do produto conforme anunciado |
| `price`          | float  | Sim         | Preço atual do produto (ex: `1629.00`) |
| `currency`       | string | Sim         | Moeda do preço — sempre `"BRL"`, hardcoded no `ResponseTransfer` |
| `url`            | string | Sim         | Link direto para o anúncio no Mercado Livre |
| `rating`         | float  | Não         | Avaliação média do produto (0.0 a 5.0) — `null` quando ausente no DOM |
| `price_original` | float  | Não         | Preço original antes do desconto — `null` quando não há desconto |
| `installments`   | string | Não         | Texto bruto das parcelas (ex: `"10x R$ 162,90 sem juros"`) — `null` quando ausente |
| `shipping`       | string | Não         | Texto bruto do frete (ex: `"Frete grátis"`, `"Chegará grátis amanhã"`) — `null` quando ausente |
| `seller`         | string | Não         | Nome do vendedor — `null` quando ausente no DOM |

> **Campos removidos:** `condition` e `sales` não aparecem de forma confiável no DOM da listagem e foram excluídos do contrato de saída desta versão.

> **Sobre `installments` e `shipping`:** retornados como string bruta. A normalização (ex: extrair número de parcelas e valor) é responsabilidade do sistema consumidor.

> **Sobre os campos obrigatórios:** itens cujo mapeamento não produza `title`, `price`, `currency` e `url` são **descartados individualmente** pelo `output` (ver seção 9). A requisição não falha por causa de um item incompleto.

## 4. Fonte

- **Site/plataforma:** Mercado Livre Brasil
- **Tipo de página:** Listagem de resultados de busca
- **URL base:** `https://lista.mercadolivre.com.br`
- **Padrão de acesso:**
  - Primeira página: `https://lista.mercadolivre.com.br/{query}_NoIndex_True`
  - Páginas seguintes: `https://lista.mercadolivre.com.br/{query}_Desde_{offset}_NoIndex_True`
  - A `query` tem os espaços substituídos por hífen antes de compor a URL.

---

## 5. Acesso

- **Requer autenticação?** Não
- **Requer JS rendering?** **Sim** — o DOM da listagem é montado via JavaScript. Utiliza **Playwright** (Chromium headless) + BeautifulSoup.
- **Selector de espera:** `a.poly-component__title` — aguardado via `wait_for_selector` antes de fazer o parse do HTML. O timeout é o `HTTP_TIMEOUT_SECONDS` da configuração do módulo (padrão 30s).
- **Cliente HTTP:** definido na `configuration` via `client_type = "playwright"`.

### Configuração do navegador (`downloader/configuration/configuration.py`)

| Parâmetro     | Valor |
|---------------|-------|
| `base_url`    | `https://lista.mercadolivre.com.br` |
| `client_type` | `playwright` |
| `user_agent`  | Chrome 124 / Windows NT 10.0 / x64 |
| `viewport`    | `1366 x 768` |
| `locale`      | `pt-BR` |
| `timezone`    | `America/Sao_Paulo` |
| `launch_args` | `--disable-blink-features=AutomationControlled`, `--no-sandbox`, `--disable-dev-shm-usage` |
| `max_items`   | `500` (hard cap de raspagem) |

### Contorno de detecção de bot

O Mercado Livre aplica detecção de automação. As medidas atuais, todas no downloader:

- Sufixo `_NoIndex_True` em todas as URLs de listagem.
- `launch_args` com `--disable-blink-features=AutomationControlled`.
- `user_agent`, `viewport`, `locale` e `timezone` realistas no contexto do navegador.
- Header `Accept-Language` explícito (`pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7`).
- Script de inicialização que sobrescreve `navigator.webdriver` para `undefined`.

> Estas medidas podem precisar de revisão caso o Mercado Livre reforce a detecção.

---

## 6. Seletores CSS

| Campo            | Seletor                                                                 | Extração |
|------------------|-------------------------------------------------------------------------|----------|
| card             | `li.ui-search-layout__item`                                             | Container de cada produto |
| `title`          | `a.poly-component__title`                                               | `.get_text(strip=True)` |
| `price`          | `span.andes-money-amount__fraction`                                     | `.get_text(strip=True)` → float |
| `url`            | `a.poly-component__title`                                               | `.get('href')` |
| `rating`         | `span.poly-component__review-compacted` → `span.poly-phrase-label`     | `.get_text(strip=True)` → float. `null` se bloco ausente |
| `price_original` | `s.andes-money-amount--previous` → `span.andes-money-amount__fraction` | `.get_text(strip=True)` → float. `null` se tag ausente |
| `installments`   | `span.poly-price__installments`                                         | `.get_text(separator=' ', strip=True)`. `null` se ausente |
| `shipping`       | `div.poly-component__shipping` ou `div.poly-component__shipping-v2`    | `.get_text(separator=' ', strip=True)`. `null` se ausente |
| `seller`         | `span.poly-component__seller`                                           | `.find(string=True, recursive=False).strip()`. `null` se ausente |

---

## 7. Operacional

- **Estratégia de paginação:**
  - Primeira página: sem offset (`_NoIndex_True`)
  - Segunda página: offset `49`
  - Páginas seguintes: incremento de `48` por página (`49`, `97`, `145`, ...)
  - Loop interrompido quando: (a) `wait_for_selector('a.poly-component__title')` lançar `TimeoutError`, ou (b) a estimativa `len(html_pages) * 48` atingir o hard cap

- **Hard cap de raspagem:** `500` itens. Constante hardcoded em `downloader/configuration/configuration.py` (`__max_items`), exposta via `setupMaxItems()`. **Não usa variável de ambiente** — regras do módulo ficam dentro do módulo. A paginação interrompe antecipadamente quando a estimativa atinge o cap; o cache é truncado para no máximo 500 itens antes de ser gravado. Para alterar o valor, editar a classe e reiniciar.
- **Rate limit / delay:** delay entre páginas e entre retries, configurável via `HTTP_DELAY_SECONDS` no `.env` do módulo (padrão 2s).
- **Retries:** o downloader herda o retry automático de `BaseDownloader`, com `HTTP_RETRY_ATTEMPTS` tentativas (padrão 3).

### Cache

- **Localização:** `shared/infra/cache/`, um arquivo JSON por chave.
- **Chave de cache:** `mercadolivre_{query-normalizada}` — a query é normalizada em minúsculas, com espaços convertidos em hífen.
- **Conteúdo:** o cache armazena o resultado **completo, não-filtrado**, já truncado no hard cap de 500 itens. Filtros, `limit` e `fields` são aplicados na resposta, não no cache.
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
| `filters` | objeto                  | Não         | Critérios de filtragem (ver abaixo) |
| `fields`  | lista de string         | Não         | Projeção de campos (ver abaixo) |
| `limit`   | inteiro positivo (`>0`) | Não         | Teto de itens na resposta |

Filtros, `limit` e projeção são aplicados pelo `output` após o scraping, tanto no caminho fresh quanto no cache hit. A ordem de aplicação é fixa: **filtros → limit → projeção**.

### Filtros (`filters`)

| Filtro          | Tipo    | Efeito |
|-----------------|---------|--------|
| `price_min`     | float   | Exclui produtos com `price` abaixo do valor |
| `price_max`     | float   | Exclui produtos com `price` acima do valor |
| `free_shipping` | bool    | Quando `true`, mantém apenas produtos cujo `shipping` contém `"grátis"` (case-insensitive). Quando `false` ou omitido, não filtra |
| `min_rating`    | float   | Exclui produtos com `rating` abaixo do valor **ou** com `rating == null` |
| `has_discount`  | bool    | Quando `true`, mantém apenas produtos com `price_original != null`. Quando `false` ou omitido, não filtra |
| `seller`        | string  | Mantém apenas produtos cujo `seller` **contém** o valor passado como substring (case-insensitive via `casefold`). Termos curtos ou genéricos podem casar com mais de um vendedor. Produtos com `seller == null` são excluídos |

> Filtros desconhecidos são rejeitados pelo Pydantic com HTTP 422.
> `condition` **não** está disponível como filtro — campo excluído do contrato de saída (seção 3).

### Limite de itens (`limit`)

Campo opcional inteiro positivo. Aplicado **depois dos filtros e antes da projeção**.

- Omitido → retorna até o hard cap do módulo (500 itens — ver seção 7).
- `limit ≤ hard cap` → retorna até `limit` itens.
- `limit > hard cap` → retorna até o hard cap (cap silencioso, sem erro).
- `limit ≤ 0` → rejeitado pelo Pydantic com HTTP 422.

Quando combinado com filtros que removem muitos itens, a resposta pode ter **menos** que `limit` — `limit` é um teto sobre o conjunto filtrado, não um número garantido.

### Projeção (`fields`)

Lista opcional. Quando omitida, retorna todos os campos da seção 3. Valores permitidos:
`title`, `price`, `currency`, `url`, `rating`, `price_original`, `installments`, `shipping`, `seller`.

É possível filtrar ou limitar por um campo que não esteja em `fields`.

### Exemplo de payload

```json
{
  "query": "notebook",
  "filters": {
    "price_min": 1200,
    "price_max": 3000,
    "free_shipping": true,
    "min_rating": 4.0,
    "has_discount": true,
    "seller": "Magazine Luiza"
  },
  "fields": ["title", "price", "url", "shipping"],
  "limit": 20
}
```

---

## 9. Exceptions

Todas herdam de `BaseApiException`. As exceptions de **downloader** e **extractor** interrompem a requisição e retornam HTTP 422 ao cliente. As exceptions de **output** têm comportamento diferente (ver nota abaixo).

| Código                        | Etapa      | Quando ocorre |
|--------------------------------|-----------|----------------|
| `DOWNLOADER_EMPTY_RESPONSE`    | downloader | A resposta do alvo veio vazia (nenhuma página coletada) |
| `EXTRACTOR_SELECTOR_NOT_FOUND` | extractor  | Nenhum campo pôde ser extraído — seletores possivelmente quebrados pela mudança do HTML do site |
| `OUTPUT_MISSING_TITLE`         | output     | Item sem `title` após o mapeamento |
| `OUTPUT_MISSING_PRICE`         | output     | Item sem `price` após o mapeamento |
| `OUTPUT_MISSING_CURRENCY`      | output     | Item sem `currency` após o mapeamento |
| `OUTPUT_MISSING_URL`           | output     | Item sem `url` após o mapeamento |

> **Comportamento das exceptions de `output`:** o `validator` do output lança `OUTPUT_MISSING_*` por item. O `service` do output **captura essas exceptions, registra um warning e descarta o item inválido**, seguindo com os demais. Ou seja, exceptions de output **não chegam ao cliente** — funcionam como um filtro de integridade item a item. Apenas downloader e extractor produzem o erro 422.

---

> **Versão:** 1.3
> **Última atualização:** 2026-05-17
> **Observações:** Módulo piloto do projeto. Utiliza Playwright por necessidade de JS rendering. Os seletores CSS devem ser revisados caso o Mercado Livre altere a estrutura do HTML — detecção feita pelo `validator` do extractor via exception `EXTRACTOR_SELECTOR_NOT_FOUND`.
>
> **Histórico:**
> - v1.1 — adicionou `filters` e `fields` aplicados pelo `output` sem alterar o scraping nem o cache.
> - v1.2 — adicionou hard cap de raspagem (constante `__max_items=500` em `Configuration`, sem env var) e campo `limit` no payload.
> - v1.3 — config operacional movida para o `.env`/`settings.py` do módulo; documentadas a configuração do navegador, as medidas de contorno de detecção de bot, a limpeza agendada de cache (`jobs.py` + `cleaner.py`), o contrato de entrada Pydantic e a tabela consolidada de exceptions com o comportamento de descarte item a item do `output`.