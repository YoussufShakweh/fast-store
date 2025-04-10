from datetime import datetime
from uuid import UUID

from sqlalchemy import String, false, text, true
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.db.utils import UTC_NOW


class User(Base):
    """
    Authentication user model.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(server_default=true())
    is_superuser: Mapped[bool] = mapped_column(server_default=false())
    last_login: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=UTC_NOW)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=UTC_NOW, server_onupdate=UTC_NOW
    )
