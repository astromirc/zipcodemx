from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token

from app.shared.dependencies import Session
from app.shared.errors import InactiveUserError, InvalidCredentialsError
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
        raise InvalidCredentialsError()

    if not user.is_active:
        raise InactiveUserError()

    update_last_login(session=session, user=user)
    token = create_access_token(user.id)

    return Token(access_token=token)
