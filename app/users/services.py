from sqlmodel import Session, select

from app.shared.timezone import now

from .models import User


def get_user_by_email(*, session: Session, email: str) -> User | None:
    email = email.lower().strip()
    stmt = select(User).where(User.email == email)
    return session.exec(stmt).first()


def update_last_login(*, session: Session, user: User) -> None:
    user.last_login = now()
    session.commit()
