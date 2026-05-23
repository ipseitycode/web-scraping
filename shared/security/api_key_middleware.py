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