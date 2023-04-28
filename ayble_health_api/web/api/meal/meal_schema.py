from typing import List, Optional

from pydantic import BaseModel, Field, validator

from ayble_health_api.business.food import FoodType


class MealPortion(BaseModel):
    id: Optional[int] = Field(default=None,
                              title="The id of the meal portion",
                              example=1)

    food_type: FoodType = Field(
        default=None,
        title="The type of food in this portion of the meal",
        example=str(FoodType.MEAT))

    portion_size_cups: float = Field(
        default=None,
        title="The size of this portion in cups",
        description="Only increments of 0.5 cups, no more than 10 cups",
        gt=0,
        le=10,
        example=1.5)

    @validator('portion_size_cups')
    def portion_size_is_in_correct_increments(cls, portion_size_cups: float) -> float:
        if portion_size_cups % 0.5 != 0:
            raise ValueError('portion size must be in increments of 0.5 cups')
        return portion_size_cups

    class Config:
        orm_mode = True


class Meal(BaseModel):
    id: Optional[int] = Field(default=None,
                              title="The id of the meal",
                              example=1)
    portions: List[MealPortion] = Field(
        default=None, title="The portions of food in this meal")

    user_id: int = Field(default=None,
                         title="The id of the user who ate this meal")

    class Config:
        orm_mode = True
