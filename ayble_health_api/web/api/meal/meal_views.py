from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ayble_health_api.db.dao.meal_dao import MealDAO
from ayble_health_api.db.dao.user_dao import UserDAO
from ayble_health_api.db.dependencies import get_db_session
from ayble_health_api.web.api.meal.meal_schema import Meal, MealPortion

router = APIRouter()



@router.post("/meal")
async def add_meal(
    meal: Meal, session: AsyncSession = Depends(get_db_session)) -> Meal:
    meal_dao = MealDAO(session)
    user_dao = UserDAO(session)
    user = await user_dao.get_user(meal.user_id)
    if not user:
        raise HTTPException(status_code=404,
                            detail=f"User not found with id: {meal.user_id}")

    portions = [
        meal_dao.construct_portion(food_type=portion.food_type,
                                   portion_size_cups=portion.portion_size_cups)
        for portion in meal.portions
    ]
    added_meal = await meal_dao.create_meal(portions, user)
    await session.commit()
    return Meal.from_orm(added_meal)


@router.put("/meal-portion/{meal_portion_id}")
async def update_meal_portion(
    meal_portion_id: int,
    meal_portion: MealPortion,
    session: AsyncSession = Depends(get_db_session)
) -> MealPortion:
    meal_dao = MealDAO(session)
    meal_portion_model = meal_dao.construct_portion(
        food_type=meal_portion.food_type,
        portion_size_cups=meal_portion.portion_size_cups)
    existing_portion = await meal_dao.get_meal_portion(meal_portion_id)
    if not existing_portion:
        raise HTTPException(status_code=404,
                            detail=f"Meal portion not found with id: {meal_portion_id}")
    updated_portion = await meal_dao.update_meal_portion(
        existing_portion, meal_portion_model)
    await session.commit()
    return MealPortion.from_orm(updated_portion)
