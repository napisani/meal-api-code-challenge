import os

from ayble_health_api.settings import settings


async def create_database() -> None:
    pass


async def drop_database() -> None:
    if settings.db_file.exists():
        os.remove(settings.db_file)
