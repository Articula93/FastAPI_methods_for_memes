from minio import Minio
import io
from BaseModel_minio import*
import base64
import random
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, Body, status, Response


app = FastAPI()

client = Minio("localhost:9000",access_key="minioadmin",secret_key="minioadmin",secure=False)

def put_store(name, stream):
    client = Minio("localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure = False
    )

    if client.bucket_exists("my-bucket-memes"):
        print("my-bucket-memes exists")
    else:
        client.make_bucket("my-bucket-memes")

    return client.put_object( "my-bucket-memes",name, stream, length=-1, part_size=10*1024*1024)

def to_stream(data):
    result = base64.b64decode(data)
    return io.BytesIO(result)


@app.post("/img/add")
async def add_img(req: RequestAddImg):
    stream = to_stream(req.data)
    put_store(req.name,stream)


# @app.get("/img/receipt")
# async def receipt_img(name: str):
#     objects = client.list_objects("my-bucket-memes", prefix=f"{name}/prefix/")
#     return ResponceDataPictures(success = True,error="",data=objects)

@app.get("/img/receipt")
async def receipt_img(name: str):
    print('receipt_img')
    try:
        response = client.get_object("my-bucket-memes", f"{name}")
        result =  ResponceDataPictures(success = True,error="",data=base64.b64encode(response.data).decode("utf-8"))
        response.close()
        response.release_conn()
    except:
        result =ResponceDataPictures(success= False, error="Такого имени не существует", data = " ")
    # print(responce.data)
    # result = client.stat_object("my-bucket-memes", f"{name}")
    # print('result',result)
    
   
    return result

@app.delete("/img/del")
async def delete_img(name: str):
    client.remove_object("my-bucket-memes", f"{name}")
  
@app.put("/img/update")
def update_picture(req:RequestUpdatePictures,name: str):
    client.remove_object("my-bucket-memes", f"{name}")
    stream = to_stream(req.data)
    put_store(req.name,stream)

# @app.get("/img/list")
# def list_memes(offset: int,length: int):
#     try:
#         response = client.get_object(
#             "my-bucket-memes", "my-object", f"{offset}, {length}")
#     finally:
#         response.close()
#         response.release_conn()
#     return ResponcePaginationPictures(success = True,error="",data = response)


# def add_pictures():
#     file = open("D:\Учеба\картинки\images.jpg", "rb")
#     client.put_object("my-bucket-memes","my-object-mem", file, length=-1,part_size=10*1024*1024)
#     file.close()

# test=add_pictures()

