from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token

from app.shared.dependencies import Session
from app.users.services import update_last_login

from .models import Token
from .services import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    session: Session,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Los datos de acceso son incorrectos. "
                "Por favor, verifica tu información."
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está bloqueada.",
        )

    update_last_login(session=session, user=user)
    token = create_access_token(user.id)

    return Token(access_token=token)
