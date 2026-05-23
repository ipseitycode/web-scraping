---
trigger: always_on
---

# security

## Autenticação via API Key

Toda requisição recebida pela API deve conter o header `X-API-Key` com a chave configurada no `.env` da raiz. A validação é feita pelo middleware global `ApiKeyMiddleware`, localizado em `shared/security/api_key_middleware.py`.

## Comportamento do Middleware

- Intercepta toda requisição antes de chegar a qualquer módulo ou rota.
- Lê o header `X-API-Key` da requisição.
- Compara contra o valor de `API_KEY` exposto por `shared/config/settings.py`.
- Se o header estiver ausente ou a chave for inválida, retorna imediatamente `401 Unauthorized` com o seguinte corpo:

```json
{
    "success": false,
    "error": {
        "code": "UNAUTHORIZED",
        "message": "Invalid or missing API key."
    }
}
```

- Se a chave for válida, a requisição segue normalmente para o router do módulo.

## Implementação

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

## Regras

- A chave é única e global para toda a API. Não há controle de acesso por módulo ou domínio.
- Nenhum módulo conhece ou depende do middleware. O isolamento é total.
- Nenhuma lógica de autenticação deve existir fora de `shared/security/`.
- O middleware é registrado no `main.py` da raiz via `app.add_middleware(ApiKeyMiddleware)`, sempre antes do registro dos routers.
- A `API_KEY` nunca deve ter valor padrão no código. Se não estiver no `.env`, todas as requisições serão bloqueadas.
