from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ayble_health_api.business.food import FoodType
from ayble_health_api.db.dependencies import get_db_session
from ayble_health_api.db.models.meal_model import MealModel, MealPortionModel
from ayble_health_api.db.models.user_model import UserModel


class MealDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    def construct_portion(self, food_type: FoodType, 
                          portion_size_cups: float) -> MealPortionModel:
        """
        Constructs a MealPortionModel from the given 
        parameters without adding it to the database
        :param food_type: the type of food in this portion
        :param portion_size_cups: the size of this portion in cups
        """

        return MealPortionModel(food_type=food_type,
                                portion_size_cups=portion_size_cups)

    async def create_meal(self, portions: List[MealPortionModel],
                          user: UserModel) -> MealModel:
        """
        Creates a meal in the database

        :param portions: the list of food portions included in this meal
        :param user: the user who ate this meal
        :return: the created meal
        """
        meal = MealModel(portions=portions, user=user)
        self.session.add(meal)
        await self.session.flush()
        return meal

    async def get_meal_portion(self,
                               portion_id: int) -> Optional[MealPortionModel]:
        """
        Gets a meal portion from the database

        :param portion_id: the id of the portion to get
        :return: the meal portion
        """
        meal_portion = await self.session.get(MealPortionModel, portion_id)
        return meal_portion


    async def update_meal_portion(
            self, existing_meal_portion: MealPortionModel,
            portion_with_updates: MealPortionModel) -> MealPortionModel:
        """
        Updates a meal portion in the database

        :param existing_meal_portion: the existing meal portion
        :param portion_with_updates: the portion with the updated values
        :return: the updated meal portion
        """
        existing_meal_portion.food_type = portion_with_updates.food_type
        existing_meal_portion.portion_size_cups = portion_with_updates.portion_size_cups
        await self.session.flush()
        return existing_meal_portion 
