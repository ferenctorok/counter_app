from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from counter_app.database import Base


class Counter(Base):
    """Database model for the counter."""

    __tablename__ = "counter"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
