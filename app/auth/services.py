from sqlmodel import Session

from app.core.security import verify_password

from app.users.models import User
from app.users.services import get_user_by_email

DUMMY_PASSWORD_HASH = "$2b$12$09Zfwqma9ovyIVqXyYM/H.vTc39vwZmG2gNl7c9Lcfxk98P4bn5f."  # noqa: S105


def authenticate_user(*, session: Session, username: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=username)

    if user is None:
        # Verificación simulada para evitar diferencias en tiempos de respuesta
        verify_password(password, DUMMY_PASSWORD_HASH)
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
