---
trigger: always_on
---

# downloader-stage

## Responsabilidade

O downloader tem responsabilidade única: comunicação com o mundo externo. Faz a requisição HTTP, lida com headers, user-agent, paginação, delays e retries. Não sabe nada sobre o conteúdo que recebe. Apenas traz o HTML ou JSON bruto.

> O schema HTTP do payload de entrada (Pydantic) **não** é uma classe do downloader. Ele é declarado no `main.py` do módulo — ver `request-schema.md`.

## Classes

### `configuration/configuration.py`
- Define todas as configurações necessárias para a requisição do módulo: URL base, headers HTTP, user-agent, timeout, limites de raspagem e demais parâmetros de acesso.
- É a primeira coisa que o `service` instancia.
- Os valores específicos de cada configuração são definidos pelo módulo.
- A escolha entre HTTPX e Playwright é definida aqui.
- A configuração de proxies residenciais rotativos, quando necessária, também é definida aqui.

### `service/service.py`
- Orquestra a etapa.
- Instancia a `configuration`, executa a requisição (incluindo paginação, quando aplicável) usando HTTPX ou Playwright conforme definido pelo módulo, e retorna o conteúdo bruto.
- Herda de `BaseDownloader` e implementa `_fetch(request)`.
- Repassa os parâmetros de retry e delay à classe base a partir da configuração do módulo.
- Nunca implementa lógica de parsing ou transformação de dados.

### `validator/validator.py`
- Valida se a resposta recebida é utilizável antes de passar para o extractor.
- Verifica condições como resposta vazia, bloqueio ou captcha.
- Se inválida, aciona a exception.
- Método principal: `validateResponse(response)`.

### `repository/repository.py`
- Consulta e grava no cache local do módulo.
- Antes de qualquer requisição externa, verifica se já existe resultado recente em cache para a mesma chave.
- A estratégia de chave de cache é definida pelo módulo.
- Métodos principais: `findCache(key)` e `saveCache(key, data)`.

### `transfer/request_transfer.py`
- DTO interno de entrada do downloader.
- Transporta os parâmetros da requisição de forma estruturada entre o `main.py` e a etapa.
- Implementado como classe Python pura com atributos privados, getters e setters, sem dependência de bibliotecas externas.

### `exception/exception.py`
- Contém os erros específicos do downloader.
- Herda de `BaseApiException`.
- Os códigos de erro são definidos pelo módulo.

## Tabela de Classes

| Classe                       | Presente no Downloader |
|------------------------------|------------------------|
| `configuration`              | Sim                    |
| `service`                    | Sim                    |
| `validator`                  | Sim                    |
| `repository`                 | Sim                    |
| `transfer/request_transfer`  | Sim                    |
| `transfer/response_transfer` | Não                    |
| `mapper`                     | Não                    |
