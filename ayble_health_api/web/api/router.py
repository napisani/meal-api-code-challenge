from fastapi.routing import APIRouter

from ayble_health_api.web.api import docs, meal, user

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(meal.router)
api_router.include_router(user.router)
