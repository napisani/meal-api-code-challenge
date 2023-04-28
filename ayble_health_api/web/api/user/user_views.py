from ayble_health_api.web.api.user.user_schema import User
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ayble_health_api.db.dao.user_dao import UserDAO 
from ayble_health_api.db.dependencies import get_db_session

router = APIRouter()
@router.post("/user")
async def create_user(
    user: User, session: AsyncSession = Depends(get_db_session)) -> User:
    user_dao = UserDAO(session)
    added_user = await user_dao.create_user(user.first_name, user.last_name)
    await session.commit()
    return User.from_orm(added_user)

