---
trigger: always_on
---

# exception-contract

## Regra Geral

- Toda exception lançada em qualquer etapa deve herdar de `BaseApiException`, definida em `shared/exception/base_exception.py`.
- Nunca lance exceções Python genéricas (`Exception`, `ValueError`, etc.) diretamente ao cliente.
- O formato JSON de erro é universal para todos os módulos, domínios e etapas.
- Os códigos de erro específicos de cada módulo são definidos na documentação do próprio módulo.

## Contrato da Classe Base

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

## Formato Universal de Resposta de Erro

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

## Handler Global e Status HTTP

- O `main.py` da raiz registra um handler global que captura qualquer `BaseApiException` e retorna seu `response` com status HTTP `422 Unprocessable Entity`.
- O Pydantic, ao rejeitar um payload com schema inválido na borda da API, também produz status `422`.
- O status `401 Unauthorized` é produzido apenas pelo middleware de segurança quando a `X-API-Key` é inválida ou ausente — não passa pelo contrato de etapas.

## Exceptions por Etapa

- Cada etapa possui seu próprio arquivo `exception/exception.py`.
- Cada `exception.py` de módulo herda de `BaseApiException`.
- Os códigos de erro seguem o padrão `{STAGE_CODIGO_DO_ERRO}` — sempre prefixados pela etapa de origem.
