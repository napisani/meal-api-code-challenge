from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ayble_health_api.business.food import FoodType
from ayble_health_api.db.base import Base
from ayble_health_api.db.models.user_model import UserModel


class MealPortionModel(Base):
    __tablename__ = "meal_portion"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    food_type: Mapped[FoodType] = mapped_column(Enum(FoodType))
    portion_size_cups: Mapped[float] = mapped_column()
    meal_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey("meal.id"),
                                         index=True)
    meal: Mapped['MealModel'] = relationship('MealModel', uselist=False)


class MealModel(Base):
    __tablename__ = "meal"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at = mapped_column(DateTime,
                               default=datetime.utcnow,
                               nullable=False)
    portions: Mapped[MealPortionModel] = relationship("MealPortionModel",
                                                      back_populates="meal")
    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey("user.id"),
                                         index=True)
    user: Mapped[UserModel] = relationship(UserModel, uselist=False)
