from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Body, status, Response
from typing import Annotated
from fastapi import FastAPI, Path
from fastapi import Form
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse, FileResponse
from fastapi.testclient import TestClient
from main_BaseModel import*
from main_db import*
from minio_client import*
from metadata import*
import requests
import uuid
import os

TOKEN = os.environ.get('minio_token')

app = FastAPI(title="MemesApp + S3",
            description=" API for working with meme collection",
            version="0.0.1",
            terms_of_service="http://example.com/terms/",
            contact={
                "name": "Lapin Ivan",
                "url": "http://example.com/contact/",
                "email": "example@gmail.com",
            },
            license_info={
                "name": "Apache 2.0",
                "identifier": "MIT",
            },
            openapi_tags=tags_metadata)


@app.get("/")
def response_html():
    return FileResponse("adminka.html")


@app.post("/memes",tags=["memes"])
def add_picture(req:RequestDataMemes, response: Response):
    with Session() as session:
        generate_name_memes = str(uuid.uuid4())
        if session.query(Mem).filter(Mem.name_memes == generate_name_memes).first():
            return response.status_code == status.HTTP_400_BAD_REQUEST
        
        res = requests.post("http://localhost:5000/img/add",json={"data":req.data, "name":generate_name_memes}, 
                            headers= {"Autorization":f'Apikey {TOKEN}'})
        print(res.request.headers)
        if res.ok:
            create_memes = Mem()
            create_memes.name_memes = generate_name_memes
            create_memes.description_memes = req.description_memes
            create_memes.format_pictures = req.format_memes

            session.add(create_memes)
            session.commit()
            response.status_code = status.HTTP_200_OK
            return ResponceDataMemes(success = True,error=None, data = create_data_memes_in_db(create_memes))
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponceDataMemes(success = False,error="Ошибка добавления")

@app.get("/memes",tags=["list_memes"])
def list_memes(limit:int, offset:int,response: Response):
    with Session() as session:
        total_memes = session.query(Mem).count()

        list_memes_in_db = session.query(Mem).limit(limit).offset(offset)
        list_memes = []
        for i in list_memes_in_db:
            id_mem = {'name': f"{i.name_memes}"}
            res = requests.get("http://localhost:5000/img/receipt",params=id_mem,headers= {"Autorization":f'Apikey {TOKEN}'})
            list_memes.append(create_data_memes_in_db(i))
            if not res.ok:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return ResponceDataMemes(success = False,error="Такой мем не найден")
            
        response.status_code = status.HTTP_200_OK  
        return ResponcePaginationMemes(success=True, error= None, memes_list=list_memes,total=total_memes,limit=limit,offset=offset)
                
@app.get("/memes_id",tags=["search_for_id"])
def search_memes(id:int,response: Response):
    with Session() as session:
        meme = session.query(Mem).filter(Mem.id_memes == id).first()
        if not meme:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"message": "Мема с таким id не существует"})
        id_mem = {'name': f"{meme.name_memes}"}
        res = requests.get("http://localhost:5000/img/receipt",params=id_mem,headers= {"Autorization":f'Apikey {TOKEN}'})
        print(res.url)
        if res.ok:
            data_res = res.json()
            if data_res["success"]:
                response.status_code = status.HTTP_200_OK  
                return ResponceDataMemes(success=True, data = create_data_memes_in_db(meme, data_res['data']))
            
        response.status_code = status.HTTP_400_BAD_REQUEST   
        return ResponceDataMemes(success = False,error="Такой мем не найден")
        
@app.put("/memes_update",status_code=200,tags=["update_for_id"])
def update_memes(req:RequestUpdateMemes,id: int,response: Response):
    with Session() as session:
        update_memes = session.query(Mem).filter(Mem.id_memes == id).first()
        if not update_memes:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"message": "Мема с таким id не существует"})
        
        if req.description_memes:
            update_memes.description_memes = req.description_memes
        if req.format_memes:
            update_memes.format_pictures = req.format_memes

        if req.data:
            name_mem = {'name': f"{update_memes.name_memes}"}
            res = requests.put("http://localhost:5000/img/update",
                            json={"data":req.data}, 
                            params=name_mem,
                            headers= {"Autorization":f'Apikey {TOKEN}'}) 

            if not res.ok:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return ResponceUpdateMemes(success=True,error="ошибка обновления")
        
        session.commit()
        response.status_code = status.HTTP_200_OK
        return ResponceUpdateMemes(success=True, data=update_data_memes_in_db(update_memes))
    

@app.delete("/memes_delete",tags=["delete_for_id"])
def delete_memes(id: int):
    with Session() as session:
        delete_memes = session.query(Mem).filter(Mem.id_memes == id).first()
        
        if not delete_memes:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"message": "Мем не найден"})   
        else:
            id_mem = {'name': f'{delete_memes.name_memes}'}
            res = requests.delete("http://localhost:5000/img/del",params=id_mem,headers= {"Autorization":f'Apikey {TOKEN}'})
            print(res.url)
            session.delete(delete_memes)
            session.commit()
            if res.ok:
                return JSONResponse(
                        status_code=status.HTTP_201_CREATED, 
                        content={"message": "Мем успешно удален"})
            
