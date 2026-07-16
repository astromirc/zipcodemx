class AppError(Exception):
    message = "Ha ocurrido un error."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message if message is not None else self.message)


class InvalidCredentialsError(AppError):
    message = "Los datos de acceso son incorrectos. Por favor, verifica tu información."


class InactiveUserError(AppError):
    message = "Tu cuenta está suspendida."
