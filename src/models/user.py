from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import String, false, func, text, true
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class User(Base):
    """
    Authentication user model.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String(254), index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(server_default=true())
    is_superuser: Mapped[bool] = mapped_column(server_default=false())
    last_login: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=datetime.now(timezone.utc)
    )
