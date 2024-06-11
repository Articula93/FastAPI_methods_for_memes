from pydantic import BaseModel
from typing import Optional
from typing import List
from pydantic import Field
from main_db import*


class DataForUser(BaseModel):
    id_memes: int
    name_memes: str
    description_memes:str

class UpdateMemes(BaseModel):
    data: str
    description_memes: str

def create_data_memes_in_db(memes_in_db):
    data = DataForUser(
                        id_memes=memes_in_db.id_memes,
                        name_memes = memes_in_db.name_memes,
                        description_memes=memes_in_db.description_memes)
    return data

class RequestDataMemes(BaseModel):
    data: str
    description_memes: str

class RequestUpdateMemes(BaseModel):
    data: Optional[str] = Field(None)
    description_memes: Optional[str]  = Field(None)

class ResponceDataMemes(BaseModel):
    success: bool
    error: str | None
    data: DataForUser

class ResponcePaginationMemes(BaseModel):
    success:bool
    error:str
    memes_list:List[DataForUser]
    total: int
    limit: int
    offset: int

class ResponceUpdateUsers(BaseModel):
    success: bool
    error: str | None
    data: UpdateMemes


class ResponseListMemes(BaseModel):
    success: bool
    error: str | None
    items: List[DataForUser]

