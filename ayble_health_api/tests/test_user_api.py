import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from ayble_health_api.web.api.user.user_schema import User


@pytest.mark.anyio
async def test_add_valid_user(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    given a valid user, ensure that the user is saved and a success response is returned
    """
    url = fastapi_app.url_path_for("create_user")
    user = User(first_name="Alvin", last_name="Doe")
    response = await client.post(url, json=user.dict(exclude_none=True))
    assert response.status_code == status.HTTP_200_OK
    saved_user = User(**response.json())
    assert saved_user.first_name == user.first_name
    assert saved_user.last_name == user.last_name
