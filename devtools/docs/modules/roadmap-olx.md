# ROADMAP — Módulo `olx`

---

## BLOCO 1 — PLANEJAMENTO

### ETAPA 1 — IDENTIDADE

1. **Nome do módulo:** `olx`
2. **Domínio pai:** marketplace
3. **Entidade alvo:** produto

---

### ETAPA 2 — OBJETIVO

1. **Por que:** Coletar dados de produtos disponíveis na OLX com base em uma query de busca, retornando as informações estruturadas em JSON.
2. **Problema de negócio:** Permite que sistemas consumidores obtenham dados atualizados de produtos e preços da OLX sem depender de uma API oficial, que é limitada e paga.
3. **Consumidores:** Sistemas externos via POST HTTP, dashboards desenvolvidos como produtos derivados, e uso interno da software house para análise de mercado e precificação.

---

### ETAPA 3 — DADOS DESEJADOS (rascunho)

| Campo          | Tipo            | Obrigatório | Descrição                             | Exemplo                              |
|----------------|-----------------|-------------|---------------------------------------|--------------------------------------|
| `title`        | string          | Sim         | Título do anúncio                     | `"Celular Samsung Galaxy A13"`       |
| `price`        | string          | Sim         | Preço do produto                      | `"R$ 600"`                           |
| `url`          | string          | Sim         | Link direto para o anúncio            | `"https://ba.olx.com.br/..."`        |
| `location`     | string          | Não         | Cidade e bairro do anunciante         | `"Salvador, Brotas"`                 |
| `date`         | string          | Não         | Data de publicação do anúncio         | `"Hoje, 14:41"` / `"20 de mai"`      |
| `image`        | string          | Não         | URL da imagem principal               | `"https://img.olx.com.br/..."`       |
| `installments` | string          | Não         | Texto bruto das parcelas              | `"em até 3x de R$ 200,00 sem juros"` |
| `badges`       | lista de string | Não         | Badges do anúncio (frete, pagamento)  | `["Frete grátis"]`                   |
| `image_count`  | int             | Não         | Quantidade de fotos no anúncio        | `5`                                  |

---

### ETAPA 4 — FONTE (observação manual)

1. **Site:** OLX Brasil — `https://www.olx.com.br`
2. **Tipo de página:** Listagem de resultados de busca
3. **URL base:** `https://www.olx.com.br/{estado-slug}?q={query}`
   - Exemplo: `https://www.olx.com.br/estado-ba?q=celular`
4. **Hipótese de paginação:** Parâmetro `&o=N` incrementando de 1 em 1 a partir da página 2.
   - Página 1: `https://www.olx.com.br/estado-ba?q=celular`
   - Página 2: `https://www.olx.com.br/estado-ba?q=celular&o=2`
   - Página 3: `https://www.olx.com.br/estado-ba?q=celular&o=3`

---

## BLOCO 2 — EXPLORAÇÃO

### ETAPA 5 — SCRIPT DE EXPLORAÇÃO

**1. Acesso:**
- Autenticação: **não requerida**
- JS rendering: **sim** — requisição com `requests` retornou HTTP 403. Playwright com Chromium headless resolveu o acesso.
- Detecção de bot: **presente** — sintoma foi 403 imediato com cliente HTTP simples. Contornável com Playwright + configuração de browser realista.

**2. Paginação:**
- A URL muda via parâmetro `&o=N` a partir da página 2.
- Incremento de `+1` por página confirmado.
- Condição de fim: `TimeoutError` no `wait_for_selector` ou página retornando zero cards.

**3. Seletores:**
- Todos os campos desejados existem no DOM.
- `badges` inicialmente retornou `null` — seletor original `.olx-adcard__badges span` estava errado. Inspeção do DOM revelou que os elementos são `div`, não `span`. Seletor corrigido para `.olx-adcard__badges div`.
- `badges` aparece apenas em anúncios com integração ao sistema de pagamento/entrega da OLX. Anúncios de pessoa física simples retornam `null`.
- `installments` retornou string concatenada sem espaços (`"em até3x de R$ 266,67sem juros"`) — normalização necessária.

**4. Dados:**
- Todos os valores extraídos batem com o esperado.
- `installments` precisa de normalização (responsabilidade do consumidor).
- Nenhum campo do rascunho foi descartado.

---

## BLOCO 3 — DEFINIÇÃO DO MÓDULO

### ETAPA 6 — DADOS ESPERADOS (confirmados)

| Campo          | Tipo            | Obrigatório | Descrição                            | Exemplo de valor real                    |
|----------------|-----------------|-------------|--------------------------------------|------------------------------------------|
| `title`        | string          | Sim         | Título do anúncio                    | `"Celular Samsung Galaxy A13"`           |
| `price`        | string          | Sim         | Preço bruto conforme exibido         | `"R$ 600"`                               |
| `url`          | string          | Sim         | Link direto para o anúncio           | `"https://ba.olx.com.br/grande-salvador/celulares/celular-samsung-galaxy-a13-1503759377"` |
| `location`     | string          | Não         | Cidade e bairro                      | `"Salvador, Brotas"`                     |
| `date`         | string          | Não         | Data bruta de publicação             | `"Hoje, 14:41"` / `"20 de mai, 19:36"`  |
| `image`        | string          | Não         | URL da imagem principal              | `"https://img.olx.com.br/thumbs700x500/62/622658161812909.webp"` |
| `installments` | string          | Não         | Texto bruto das parcelas             | `"em até3x de R$ 200,00sem juros"`       |
| `badges`       | lista de string | Não         | Badges do anúncio                    | `["Entrega Fácil", "Pague Online", "Parcele sem juros"]` |
| `image_count`  | int             | Não         | Quantidade de fotos no anúncio       | `5`                                      |

> **Campos obrigatórios:** itens sem `title`, `price` ou `url` são descartados individualmente. A requisição não falha por causa de um item incompleto.

> **Sobre `installments`:** retornado como string bruta sem espaços entre os tokens (ex: `"em até3x de R$ 266,67sem juros"`). Normalização é responsabilidade do consumidor.

> **Sobre `badges`:** aparece apenas em anúncios com integração ao sistema de pagamento/entrega da OLX. Podem retornam `null`. Valores conhecidos: `"Frete grátis"`, `"Entrega Fácil"`, `"Pague Online"`, `"Parcele sem juros"`, `"Aceita trocas"`, `"Reduziu o preço"`.

> **Sobre `price`:** retornado como string bruta (`"R$ 600"`). Conversão para float é responsabilidade do consumidor.

---

### ETAPA 7 — ACESSO

- **Autenticação:** não requerida
- **Cliente:** Playwright (Chromium headless)

**Configuração do navegador:**

| Parâmetro           | Valor |
|---------------------|-------|
| `user_agent`        | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36` |
| `viewport`          | `1366 x 768` |
| `locale`            | `pt-BR` |
| `timezone`          | `America/Sao_Paulo` |
| `launch_args`       | `--disable-blink-features=AutomationControlled`, `--no-sandbox`, `--disable-dev-shm-usage` |
| `wait_for_selector` | `section.olx-adcard` |

**Medidas de contorno de detecção de bot:**
- `launch_args` com `--disable-blink-features=AutomationControlled`
- Script de inicialização que sobrescreve `navigator.webdriver` para `undefined`
- `user_agent`, `viewport`, `locale` e `timezone` realistas no contexto do navegador

---

### ETAPA 8 — SELETORES

| Campo          | Seletor                                 | Extração                          | Ausente       |
|----------------|-----------------------------------------|-----------------------------------|---------------|
| container      | `section.olx-adcard`                    | Container de cada anúncio         | —             |
| `title`        | `h2.olx-adcard__title`                  | `.get_text(strip=True)`           | descarta item |
| `price`        | `h3.olx-adcard__price`                  | `.get_text(strip=True)`           | descarta item |
| `url`          | `a[data-testid="adcard-link"]`          | `.get('href')`                    | descarta item |
| `location`     | `p.olx-adcard__location`                | `.get_text(strip=True)`           | `null`        |
| `date`         | `p.olx-adcard__date`                    | `.get_text(strip=True)`           | `null`        |
| `image`        | `.olx-adcard__media img`                | `.get('src')`                     | `null`        |
| `installments` | `[data-testid="adcard-price-info"]`     | `.get_text(strip=True)`           | `null`        |
| `badges`       | `.olx-adcard__badges div`               | lista de `.get_text(strip=True)`  | `null`        |
| `image_count`  | `.olx-adcard__carousel--bullet`         | `len()` dos elementos encontrados | `null`        |

---

### ETAPA 9 — PAGINAÇÃO

- **Estratégia:** offset numérico via parâmetro `&o=N`
- **Padrão de URL:**
  - Página 1: `/{estado}?q={query}`
  - Páginas seguintes: `/{estado}?q={query}&o={pagina}`
  - Incremento: `+1` por página
- **Condição de parada:** `TimeoutError` no `wait_for_selector('section.olx-adcard')` ou página retornando zero cards
- **Hard cap:** `500` itens

---

### ETAPA 10 — OPERACIONAL

| Parâmetro              | Valor padrão | Onde fica        |
|------------------------|--------------|------------------|
| `HTTP_DELAY_SECONDS`   | `2s`         | `.env` do módulo |
| `HTTP_RETRY_ATTEMPTS`  | `3`          | `.env` do módulo |
| `HTTP_TIMEOUT_SECONDS` | `30s`        | `.env` do módulo |

---

### ETAPA 11 — CACHE

- **Utilizar cache:** sim
- **Chave de cache:** `olx_{estado}_{query-normalizada}` — query em minúsculas, espaços convertidos em hífen
  - Exemplo: `olx_estado-ba_celular`
- **Conteúdo armazenado:** resultado completo, não filtrado, truncado no hard cap de 200 itens
- **TTL de leitura:** `1440` min (24h) — `CACHE_EXPIRATION_MINUTES` no `.env`
- **Localização:** `shared/infra/cache/`
- **Limpeza:** rotina agendada diária às 3h — remove arquivos com mais de 48h, arquivos ilegíveis ou sem timestamp válido

---

### ETAPA 12 — CONTRATO DE ENTRADA

| Campo     | Tipo            | Obrigatório | Comportamento quando ausente       |
|-----------|-----------------|-------------|------------------------------------|
| `query`   | string          | Sim         | HTTP 422                           |
| `estado`  | string          | Não         | Padrão: `brasil`                   |
| `filters` | objeto          | Não         | Sem filtragem                      |
| `fields`  | lista de string | Não         | Retorna todos os campos            |
| `limit`   | inteiro (`>0`)  | Não         | Retorna até o hard cap (200 itens) |

**Filtros disponíveis (`filters`):**

| Filtro             | Tipo  | Efeito |
|--------------------|-------|--------|
| `price_min`        | float | Exclui produtos cujo `price` normalizado seja inferior ao valor |
| `price_max`        | float | Exclui produtos cujo `price` normalizado seja superior ao valor |
| `has_installments` | bool  | Quando `true`, mantém apenas produtos com `installments != null` |
| `location`         | string| Mantém apenas produtos cujo `location` contenha o valor como substring (case-insensitive) |

> Campos desconhecidos no payload são rejeitados com HTTP 422.

> Filtros `price_min` e `price_max` requerem normalização interna do campo `price` (remoção de `"R$ "` e conversão para float) antes da comparação. Essa normalização ocorre apenas na camada de filtragem — o campo `price` continua sendo retornado como string bruta na resposta.

> Filtros, `limit` e projeção são aplicados após o scraping. Ordem: **filtros → limit → projeção**.

**Exemplo de payload:**

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

### ETAPA 13 — EXCEPTIONS

| Código                         | Etapa      | Quando ocorre                                            | Comportamento                               |
|--------------------------------|------------|----------------------------------------------------------|---------------------------------------------|
| `DOWNLOADER_EMPTY_RESPONSE`    | downloader | Nenhuma página coletada (timeout em todas as tentativas) | Interrompe — HTTP 422 ao cliente            |
| `EXTRACTOR_SELECTOR_NOT_FOUND` | extractor  | Nenhum card encontrado — seletores possivelmente quebrados | Interrompe — HTTP 422 ao cliente          |
| `OUTPUT_MISSING_TITLE`         | output     | Item sem `title` após mapeamento                         | Descarta o item, registra warning, continua |
| `OUTPUT_MISSING_PRICE`         | output     | Item sem `price` após mapeamento                         | Descarta o item, registra warning, continua |
| `OUTPUT_MISSING_URL`           | output     | Item sem `url` após mapeamento                           | Descarta o item, registra warning, continua |

> Exceptions de `output` não chegam ao cliente — funcionam como filtro de integridade item a item. Apenas `downloader` e `extractor` produzem HTTP 422.