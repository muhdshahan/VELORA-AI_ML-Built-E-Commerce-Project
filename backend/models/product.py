""" Setting product model """

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from backend.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    category: Mapped[str] = mapped_column(Integer, index=True)
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float, default=0.0)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[str] = mapped_column(String(300))