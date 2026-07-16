from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def setup_exception_handlers(app: FastAPI) -> None:

    # Errores no controlados (asegura respuesta JSON)
    @app.exception_handler(Exception)
    def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Algo salió mal. Inténtalo de nuevo más tarde."},
        )
