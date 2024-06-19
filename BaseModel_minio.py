from fastapi import HTTPException
from pydantic import BaseModel,EmailStr, field_validator, model_validator
from typing import Optional
from typing import List
from pydantic import Field


class RequestAddImg(BaseModel):
    name: str
    data: str

class RequestUpdatePictures(BaseModel):
    name: str
    data: str


class ReceiptDataPictures(BaseModel):
    data: str

class PicturesFromBucket(BaseModel):
    name: str
    data: str


def create_data_pictures(data_pictures):
    data = ReceiptDataPictures(data=data_pictures.data)
    return data

def data_pictures_from_bucket(data_pictures):
    data = PicturesFromBucket(name=data_pictures.name, data=data_pictures.data)
    return data
     


class ResponceDataPictures(BaseModel):
    success: bool
    error: str | None
    data: str


class ResponcePaginationPictures(BaseModel):
    success:bool
    error:str
    picture_list:List[PicturesFromBucket]