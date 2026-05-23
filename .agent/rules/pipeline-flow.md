---
trigger: always_on
---

# pipeline-flow

## Acionamento

A API é acionada exclusivamente via POST HTTP. Toda requisição deve conter o header `X-API-Key` com a chave válida configurada no `.env` da raiz. Requisições sem o header ou com chave inválida são rejeitadas com `401 Unauthorized` antes de chegar a qualquer módulo.

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

## Responsabilidades do `main.py` do Módulo

O `main.py` dentro de cada módulo é o único orquestrador do pipeline. Ele deve obrigatoriamente:

1. Definir os schemas Pydantic de entrada da API e declarar o objeto `router` do FastAPI, com a rota `/{dominio}/{modulo}`. O router é descoberto e registrado automaticamente pelo `main.py` da raiz.
2. Receber o payload do POST já validado pelo schema Pydantic de entrada.
3. Instanciar o `RequestTransfer` do downloader e populá-lo com os dados do payload.
4. Consultar o cache antes de iniciar o pipeline.
5. Acionar o `downloader` e capturar seu retorno.
6. Passar o retorno do `downloader` para o `extractor`.
7. Passar o retorno do `extractor` para o `output`.
8. Gravar o resultado completo no cache e retornar o JSON final ao cliente.

## Isolamento entre Etapas

- As etapas nunca se comunicam diretamente entre si.
- O `main.py` do módulo é o único intermediário entre etapas.
- O retorno de uma etapa vai para o `main.py`, que então repassa para a próxima etapa.
- Nunca permita que o downloader chame o extractor, ou que o extractor chame o output diretamente.

## Fluxo Obrigatório

```
POST recebido
     ↓
Middleware valida X-API-Key
     ↓ (inválida) → 401 Unauthorized
     ↓ (válida)
Pydantic valida o schema do payload (definido no main.py do módulo)
     ↓ (inválido) → 422 Unprocessable Entity
     ↓ (válido)
main.py popula o RequestTransfer
     ↓
Consulta ao cache
     ↓ (cache hit) → aplica filtros/limite/projeção e retorna, sem executar o pipeline
     ↓ (cache miss)
Downloader → retorna conteúdo bruto para o main.py
     ↓
Extractor → recebe o bruto, retorna dados extraídos para o main.py
     ↓
Output → recebe os extraídos, retorna dados limpos para o main.py
     ↓
Repository grava o resultado completo no cache
     ↓
main.py aplica filtros/limite/projeção e retorna ao cliente
```

## Fluxo Completo — Passo a Passo

1. O cliente envia um `POST` para `/web-scraping/{dominio}/{modulo}` com o header `X-API-Key` e o payload de busca.
2. O middleware `ApiKeyMiddleware` valida a chave. Se inválida ou ausente, retorna `401` imediatamente.
3. O FastAPI valida o corpo do POST contra o schema Pydantic de entrada definido no `main.py` do módulo. Se inválido, retorna `422`.
4. O `main.py` do módulo recebe o payload validado e instancia o `RequestTransfer`, populando-o com os dados do payload.
5. O `main.py` aciona o `repository` do downloader para consultar o cache.
6. **Cache hit:** aplica filtros, limite e projeção sobre o resultado completo em cache e retorna o envelope com `cached: true`, sem executar o pipeline.
7. **Cache miss:** o `main.py` aciona o `service` do downloader.
8. O downloader lê a `configuration`, executa a requisição, valida a resposta com o `validator` e retorna o conteúdo bruto ao `main.py`.
9. O `main.py` passa o conteúdo bruto para o `service` do extractor.
10. O extractor aplica os seletores, extrai os campos brutos, valida com o `validator` e retorna os `RequestTransfer` populados ao `main.py`.
11. O `main.py` passa os dados extraídos para o `service` do output.
12. O output usa o `mapper` para converter os dados brutos em `ResponseTransfer`, valida com o `validator` e retorna a coleção ao `main.py`.
13. O `main.py` serializa cada `ResponseTransfer` via `toJson()` e grava o resultado completo no cache.
14. O `main.py` aplica filtros, limite e projeção e retorna o envelope de sucesso com `cached: false` ao cliente.
