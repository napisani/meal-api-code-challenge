from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ayble_health_api.business.food import FoodType
from ayble_health_api.db.dao.meal_dao import MealDAO
from ayble_health_api.db.dao.user_dao import UserDAO
from ayble_health_api.db.models.meal_model import MealModel
from ayble_health_api.db.models.user_model import UserModel
from ayble_health_api.web.api.meal.meal_schema import Meal, MealPortion


@pytest.fixture(scope='function')
@pytest.mark.anyio
async def test_user(
        dbsession: AsyncSession) -> AsyncGenerator[UserModel, None]:
    user_dao = UserDAO(dbsession)
    user = await user_dao.create_user(first_name="Chloe", last_name="Doe")
    yield user


@pytest.fixture(scope='function')
@pytest.mark.anyio
async def test_meal(
        test_user: UserModel,
        dbsession: AsyncSession) -> AsyncGenerator[MealModel, None]:
    meal_dao = MealDAO(dbsession)
    portions = [
        meal_dao.construct_portion(food_type=FoodType.WHEAT,
                                   portion_size_cups=1.0),
        meal_dao.construct_portion(food_type=FoodType.VEGGIE,
                                   portion_size_cups=2.5)
    ]
    meal = await meal_dao.create_meal(portions=portions, user=test_user)
    yield meal


@pytest.mark.anyio
async def test_add_meal_with_two_valid_portions(client: AsyncClient,
                                                fastapi_app: FastAPI,
                                                test_user: UserModel) -> None:
    """
    given a valid user and two valid portions, 
    add a meal and assert that the meal was added successfully
    """
    url = fastapi_app.url_path_for("add_meal")
    meal = Meal(user_id=test_user.id,
                portions=[
                    MealPortion(food_type=FoodType.WHEAT,
                                portion_size_cups=1.0),
                    MealPortion(food_type=FoodType.VEGGIE,
                                portion_size_cups=1.5)
                ])
    response = await client.post(url, json=meal.dict(exclude_none=True))
    assert response.status_code == status.HTTP_200_OK
    saved_meal = Meal(**response.json())
    assert saved_meal.user_id == meal.user_id
    assert len(saved_meal.portions) == len(meal.portions)
    for input, saved in zip(meal.portions, saved_meal.portions):
        assert input.food_type == saved.food_type
        assert input.portion_size_cups == saved.portion_size_cups


@pytest.mark.anyio
async def test_add_meal_with_invalid_user(client: AsyncClient,
                                          fastapi_app: FastAPI) -> None:
    """
    given an invalid user, assert that the meal was not added and a 404 was returned
    """
    url = fastapi_app.url_path_for("add_meal")
    meal = Meal(user_id=999,
                portions=[
                    MealPortion(food_type=FoodType.WHEAT,
                                portion_size_cups=1.0),
                ])
    response = await client.post(url, json=meal.dict(exclude_none=True))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_add_meal_with_invalid_portion_size_increment(
        client: AsyncClient, fastapi_app: FastAPI,
        test_user: UserModel) -> None:
    """
    given a portion with an invalid portion size (not an increment of .5 cups), 
    assert that a bad input response is returned 
    """
    url = fastapi_app.url_path_for("add_meal")
    meal = Meal(user_id=test_user.id,
                portions=[
                    MealPortion(food_type=FoodType.WHEAT,
                                portion_size_cups=1.5),
                ])
    meal_json = meal.dict(exclude_none=True)
    meal_json['portions'][0]['portion_size_cups'] = 1.3
    response = await client.post(url, json=meal_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_add_meal_with_invalid_portion_size_above_max(
        client: AsyncClient, fastapi_app: FastAPI,
        test_user: UserModel) -> None:
    """
    given a portion with an invalid portion size (greater than 10 cups), 
    assert that a bad input response is returned 
    """
    url = fastapi_app.url_path_for("add_meal")
    meal = Meal(user_id=test_user.id,
                portions=[
                    MealPortion(food_type=FoodType.WHEAT,
                                portion_size_cups=1.5),
                ])
    meal_json = meal.dict(exclude_none=True)
    meal_json['portions'][0]['portion_size_cups'] = 11
    response = await client.post(url, json=meal_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_update_meal_portion_with_valid_portion(
        client: AsyncClient, fastapi_app: FastAPI, test_user: UserModel,
        test_meal: MealModel) -> None:
    """
    given a valid meal, valid user and valid portion, 
    assert that the portion was updated successfully
    """
    existing_portion = test_meal.portions[0] # type: ignore
    url = fastapi_app.url_path_for("update_meal_portion",
                                   meal_portion_id=existing_portion.id)
    portion = MealPortion(food_type=FoodType.WHEAT, portion_size_cups=4.5)
    response = await client.put(url, json=portion.dict(exclude_none=True))
    assert response.status_code == status.HTTP_200_OK
    saved_portion = MealPortion(**response.json())
    assert saved_portion.food_type == portion.food_type
    assert saved_portion.portion_size_cups == portion.portion_size_cups


@pytest.mark.anyio
async def test_update_meal_portion_with_invalid_portion_size_increment(
        client: AsyncClient, fastapi_app: FastAPI, test_user: UserModel,
        test_meal: MealModel) -> None:
    """
    given a valid meal, valid user and an invalid portion, 
    assert that an unprocessable entity response is returned 
    """
    existing_portion = test_meal.portions[0] # type: ignore
    url = fastapi_app.url_path_for("update_meal_portion",
                                   meal_portion_id=existing_portion.id)
    portion = MealPortion(food_type=FoodType.WHEAT, portion_size_cups=4.5)
    portion_json = portion.dict(exclude_none=True)
    portion_json['portion_size_cups'] = 4.3
    response = await client.put(url, json=portion_json)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
