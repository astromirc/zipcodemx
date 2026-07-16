from datetime import datetime
from zoneinfo import ZoneInfo

_DEFAULT_TIMEZONE = ZoneInfo("America/Mexico_City")


def now() -> datetime:
    """Retorna la fecha y hora actual con timezone."""
    return datetime.now(_DEFAULT_TIMEZONE)


def strptime(value: str, fmt: str) -> datetime:
    """Convierte un string a datetime con timezone."""
    return datetime.strptime(value, fmt).replace(tzinfo=_DEFAULT_TIMEZONE)


def strftime(value: datetime, fmt: str) -> str:
    """Convierte un datetime a string con formato."""
    return value.strftime(fmt)
