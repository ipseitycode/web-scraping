# ROADMAP — Criação de Módulo de Scraping

---

## BLOCO 1 — PLANEJAMENTO

> O que pode ser definido antes de qualquer contato com a fonte.

### ETAPA 1 — IDENTIDADE

1. Defina o nome do módulo (slug, minúsculo, sem espaços)
2. Defina o domínio pai (ex: marketplace, imóveis, vagas, notícias)
3. Defina a entidade alvo (o que está sendo coletado: produto, empresa, anúncio, etc.)

---

### ETAPA 2 — OBJETIVO

1. Determine por que essa raspagem está sendo feita
2. Determine qual problema de negócio ela resolve
3. Determine quem vai consumir os dados (sistema externo, dashboard, uso interno, etc.)

---

### ETAPA 3 — DADOS DESEJADOS (rascunho)

> Ainda não confirmados — lista do que se espera extrair com base no conhecimento prévio da fonte.

1. Liste os campos que deseja extrair
2. Para cada campo, defina:
   - Tipo esperado (`string`, `float`, `int`, `bool`)
   - Se é obrigatório ou opcional
   - Descrição do que representa
   - Exemplo de valor esperado

---

### ETAPA 4 — FONTE (observação manual)

1. Identifique o site ou plataforma de origem
2. Identifique o tipo de página que será raspada (listagem, detalhe, busca, etc.)
3. Identifique a URL base
4. Registre hipóteses iniciais sobre paginação e padrão de acesso (a confirmar no Bloco 2)

---

## BLOCO 2 — EXPLORAÇÃO

> Script simples usado como ferramenta de descoberta. O objetivo não é entregar código limpo, mas responder às perguntas que o Bloco 1 não conseguiu.

### ETAPA 5 — SCRIPT DE EXPLORAÇÃO

Crie um script básico que acesse a fonte e tente extrair os dados desejados. Durante a execução, registre:

1. **Acesso:**
   - A página exige autenticação?
   - O conteúdo é renderizado por JS ou está no HTML estático?
   - Há detecção de bot? Quais sintomas?

2. **Paginação:**
   - Como a URL muda entre páginas?
   - Qual o padrão de offset, cursor ou parâmetro?
   - Qual é a condição real de fim de resultados?

3. **Seletores:**
   - Os campos desejados existem no DOM?
   - Quais seletores os identificam?
   - Algum campo desejado não existe ou aparece de forma inconsistente?

4. **Dados:**
   - Os valores extraídos batem com o esperado?
   - Há campos que precisam de normalização antes de usar?
   - Algum campo do rascunho deve ser descartado?

---

## BLOCO 3 — DEFINIÇÃO DO MÓDULO

> Com base no que foi descoberto no Bloco 2, define-se tudo que será implementado no módulo.

### ETAPA 6 — DADOS ESPERADOS (confirmados)

1. Atualize a lista de campos com base no que foi possível extrair
2. Para cada campo, defina:
   - Tipo (`string`, `float`, `int`, `bool`)
   - Se é obrigatório ou não
   - Descrição final
   - Exemplo de valor real
3. Documente campos descartados e o motivo
4. Documente campos retornados como string bruta e de quem é a responsabilidade de normalizar

---

### ETAPA 7 — ACESSO

1. Defina se requer autenticação e qual o tipo (sessão, token, cookie, etc.)
2. Defina o cliente HTTP que será usado (`requests`, `httpx`, `playwright`, etc.)
3. Se usar browser headless, defina:
   - `user_agent`
   - `viewport`
   - `locale` e `timezone`
   - `launch_args` relevantes
   - Selector de espera antes do parse (`wait_for_selector`)
4. Documente as medidas de contorno de detecção de bot adotadas

---

### ETAPA 8 — SELETORES

1. Para cada campo confirmado, defina:
   - O seletor CSS (ou XPath) do elemento
   - O método de extração (`.get_text()`, `.get('href')`, atributo específico, etc.)
   - O tratamento do valor extraído (conversão de tipo, strip, substituição, etc.)
   - O comportamento quando o elemento está ausente (`null`, valor padrão, descarte do item)
2. Identifique o seletor do container de cada item (elemento que envolve um registro)

---

### ETAPA 9 — PAGINAÇÃO

1. Defina a estratégia de paginação (offset numérico, cursor, próxima página, etc.)
2. Documente o padrão de URL ou parâmetro para cada página
3. Defina a condição de parada do loop (timeout, página vazia, sem mais resultados, etc.)
4. Defina o hard cap de itens (limite máximo de raspagem independente de paginação)

---

### ETAPA 10 — OPERACIONAL

1. Defina o delay entre requisições (`HTTP_DELAY_SECONDS`)
2. Defina o número de retries em caso de falha (`HTTP_RETRY_ATTEMPTS`)
3. Defina o timeout de requisição (`HTTP_TIMEOUT_SECONDS`)
4. Documente onde essas configurações ficam (`.env`, `settings.py`, constante hardcoded, etc.)

---

### ETAPA 11 — CACHE

1. Determine se cache será utilizado
2. Defina a estratégia de chave de cache (como identificar unicamente uma consulta)
3. Defina o conteúdo armazenado (resultado bruto, filtrado, truncado, etc.)
4. Defina o TTL de leitura (`CACHE_EXPIRATION_MINUTES`)
5. Defina a localização física dos arquivos de cache
6. Defina a política de limpeza (rotina agendada, critério de expiração do disco, etc.)

---

### ETAPA 12 — CONTRATO DE ENTRADA

1. Defina o schema do payload aceito pelo módulo
2. Para cada campo do payload, defina:
   - Tipo e se é obrigatório
   - Comportamento quando ausente
3. Defina os filtros disponíveis e o efeito de cada um sobre os dados
4. Defina se há suporte a projeção de campos (`fields`) e quais campos são projetáveis
5. Defina se há suporte a limite de itens na resposta (`limit`) e seu comportamento em relação ao hard cap
6. Defina o comportamento em relação a campos desconhecidos no payload (rejeitar, ignorar)
7. Documente um exemplo de payload completo

---

### ETAPA 13 — EXCEPTIONS

1. Liste todas as exceptions possíveis por etapa (downloader, extractor, output)
2. Para cada exception, defina:
   - Código identificador
   - Etapa onde ocorre
   - Condição de disparo
   - Comportamento (interrompe a requisição com erro, ou descarta o item e continua)

---

> O MAP final do módulo é o documento que consolida tudo definido no Bloco 3, com o Bloco 1 como contexto.