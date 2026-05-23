---
trigger: always_on
---

# naming-conventions

## Arquivos e Classes

- O nome do arquivo é o nome da classe em `snake_case`.
- O nome da classe no código segue `PascalCase`.
- Nunca use outros padrões de nomenclatura para arquivos ou classes.

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

## Modelos Pydantic do Schema de Entrada

- Os modelos Pydantic do schema de entrada, declarados no `main.py` do módulo, seguem `PascalCase`.
- Os nomes devem ser descritivos do papel de cada modelo (ex: o schema do payload de busca, o schema dos filtros).
- São classes declarativas e não seguem o padrão de métodos prefixados abaixo.

## Métodos

- Os métodos das classes do pipeline seguem o padrão `[prefixo][Entidade]` em `camelCase`.
- Nunca use `snake_case` para nomes de métodos do pipeline.
- Use os prefixos definidos por classe, conforme a tabela abaixo.

| Classe          | Prefixo obrigatório      | Exemplo                          |
|-----------------|--------------------------|----------------------------------|
| `configuration` | `setup` / `configure`    | `setupBaseUrl()`                 |
| `service`       | `execute` / `process`    | `executeDownload()`              |
| `validator`     | `validate`               | `validateResponse()`             |
| `repository`    | `find` / `save`          | `findCache()`, `saveCache()`     |
| `mapper`        | `map`                    | `mapProduct()`                   |
| `exception`     | *(lançadas diretamente)* | `raise DownloaderException(...)` |

## Pastas e Domínios

- Nomes de domínios e módulos seguem `snake_case` (letras minúsculas e underscores).
- Nomes de etapas são fixos: `downloader`, `extractor`, `output`.
- Nunca renomeie as etapas nem crie etapas com nomes alternativos.
