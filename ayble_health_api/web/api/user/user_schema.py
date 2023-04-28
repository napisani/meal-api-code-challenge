from typing import Optional

from pydantic import BaseModel, Field



class User(BaseModel):
    id: Optional[int] = Field(default=None,
                              title="The id of the user",
                              example=1)
    first_name: str = Field(default=None,
                            title="The first name of the user",
                            example="Alvin")
    last_name: str = Field(default=None,
                           title="The last name of the user",
                           example="Doe")

    class Config:
        orm_mode = True
