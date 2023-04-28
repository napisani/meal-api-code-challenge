from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ayble_health_api.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
