from pydantic import BaseModel
from typing import Optional
from typing import List
from pydantic import Field, field_validator
from fastapi import HTTPException
from main_db import*


class DataForUser(BaseModel):
    id_memes: int
    description_memes:str
    data: str | None = None

class UpdateMemes(BaseModel):
    description_memes: str
    format_memes: str

def update_data_memes_in_db(update_in_db):
    data = UpdateMemes(description_memes=update_in_db.description_memes,format_memes=update_in_db.format_pictures)
    return data

def create_data_memes_in_db(memes_in_db, img=None):
    data = DataForUser(
                        id_memes=memes_in_db.id_memes,
                        description_memes=memes_in_db.description_memes, 
                        data=img)
    return data

class RequestDataMemes(BaseModel):
    data: str
    description_memes: str
    format_memes: str

    @field_validator("format_memes")
    def format_validator(cls, value):
        format_file = ['PNG','JPEG','GIF','TIFF','EPS','SVG','RAW','PSD','CDR','PDF','AI']
        value = value.upper()
        if value not in format_file:
            raise HTTPException(status_code = 422, detail ="Error format")
        return value


class RequestUpdateMemes(BaseModel):
    data: str | None
    description_memes: str
    format_memes: str

    @field_validator("data")
    def existence_data(cls, value):
        if value:
            value = value.strip()
            if not value:
                raise HTTPException(status_code=422, detail="enter the data")
        return value
        
    @field_validator("description_memes")
    def existence_description_memes(cls, value):
        if value:
            value = value.strip()
            if not value:
                raise HTTPException(status_code=422, detail="enter the description_memes")
        return value
        
    @field_validator("format_memes")
    def existence_format_memes(cls, value):
        if value:
            value = value.strip()
            if not value:
                raise HTTPException(status_code=422, detail="enter the format_memes") 
        return value

class ResponceDataMemes(BaseModel):
    success: bool
    error: str | None = None
    data: DataForUser | None = None

class ResponcePaginationMemes(BaseModel):
    success:bool
    error:str | None = None
    memes_list:List[DataForUser]
    total: int
    limit: int
    offset: int

class ResponceUpdateMemes(BaseModel):
    success: bool
    error: str | None = None
    data: UpdateMemes | None = None


class ResponseListMemes(BaseModel):
    success: bool
    error: str | None
    items: List[DataForUser]

