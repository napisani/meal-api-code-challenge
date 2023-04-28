from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ayble_health_api.db.dependencies import get_db_session
from ayble_health_api.db.models.user_model import UserModel


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(self, first_name: str, last_name: str) -> UserModel:
        """
        Creates a user in the database

        :param first_name: the first name of the user 
        :param last_name: the last name of the user 
        :return: the created user
        """
        user = UserModel(first_name=first_name, last_name=last_name)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user(self, user_id: int) -> Optional[UserModel]:
        """
        Gets a user from the database

        :param user_id: the id of the user to get
        :return: the user
        """
        user = await self.session.get(UserModel, user_id)
        return user
