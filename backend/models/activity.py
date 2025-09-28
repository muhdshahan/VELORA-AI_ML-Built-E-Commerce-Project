""" Setting activity model """

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, String
from backend.db.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    
    # Time spend on product page (in seconds)
    time_spent: Mapped[int] = mapped_column(Integer, default=0)

    # Actions
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # viewed, added_to_cart, purchased