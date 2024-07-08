from minio import Minio
import io
from BaseModel_minio import*
import base64
import random
from fastapi import FastAPI,Request,Depends,Header
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, Body, status, Response
from typing_extensions import Annotated
from fastapi.testclient import TestClient
import os
from main import*

app = FastAPI()

LOGIN = os.environ.get('minio_access_key')
PASSWORD = os.environ.get('minio_secret_key')
TOKEN = os.environ.get('minio_token')


client = Minio("localhost:9000",access_key=LOGIN,secret_key=PASSWORD,secure=False)

def put_store(name, stream):
    client = Minio("localhost:9000",
        access_key=LOGIN,
        secret_key=PASSWORD,
        secure = False
    )

    if client.bucket_exists("my-bucket-memes"):
        print("my-bucket-memes exists")
    else:
        client.make_bucket("my-bucket-memes")

    return client.put_object( "my-bucket-memes",name, stream, length=-1, part_size=10*1024*1024)

def to_stream(data):
    b = bytes(data, 'utf-8')
    byte_string = io.BytesIO(b)
    return byte_string


@app.middleware("http")
async def validate_access_token(request: Request, call_next):
    response = await call_next(request)
    access_token = request.headers.get('Autorization').split()
    print(access_token)
   
    if len(access_token) < 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='authorization failed'
        )
   
    valid_token = access_token[1]

    if valid_token == TOKEN:
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid access token'
        )

@app.post("/img/add")
async def add_img(req: RequestAddImg,response: Response):
    try:
        stream = to_stream(req.data)
        put_store(req.name,stream)
        response.status_code = status.HTTP_200_OK
        result = ResponceResultImg(success= True, error="мем добавлен")
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result = ResponceResultImg(success= False, error="мем не добавлен")
        
    return result

@app.get("/img/receipt")
async def receipt_img(name: str,response: Response):
   
    try:
        response = client.get_object("my-bucket-memes", f"{name}")
        response.status_code = status.HTTP_200_OK
        result =  ResponceDataPictures(success = True,error="",data=response.data)
        response.close()
        response.release_conn()
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result = ResponceDataPictures(success= False, error="Такого имени не существует")

    return result

@app.delete("/img/del")
async def delete_img(name: str,response: Response):
   
    try:
        client.remove_object("my-bucket-memes", f"{name}")
        response.status_code = status.HTTP_200_OK
        result =  ResponceDeletePictures(success = True,error="Мем успешно удален",data=name)
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result = ResponceDeletePictures(success= False, error="Такого имени не существует")

    return result

  
@app.put("/img/update")
def update_picture(req:RequestUpdatePictures,name: str,response: Response):
 
    try:
        client.remove_object("my-bucket-memes", f"{name}")
        stream = to_stream(req.data)
        put_store(name,stream)
        response.status_code = status.HTTP_200_OK
        result = ResponceResultImg(success= True, error="мем успешно обновлен")
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        result = ResponceResultImg(success= False, error="мем не обновлен")
        
    return result
    







