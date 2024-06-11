from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Body, status, Response
from typing import Annotated
from fastapi import Form
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse, FileResponse
import base64
from main_BaseModel import*
from main_db import*
import random

app = FastAPI()


@app.get("/")
def response_html():
    return FileResponse("adminka.html")


@app.post("/memes")
def add_picture(req:RequestDataMemes):
    with Session() as session:
       
        data  = req.data
        decode_data = base64.b64decode(data)
        generate_name_memes = f"{base64.urlsafe_b64encode(random.randbytes(30))}"
        file = open(generate_name_memes, "wb")
        file.write(decode_data)
        file.close()
        create_memes = MemesList()
        create_memes.name_memes = generate_name_memes
        create_memes.description_memes = req.description_memes

        session.add(create_memes)
        session.commit()


        return ResponceDataMemes(success = True,error="", data = create_data_memes_in_db(create_memes))


@app.get("/memes")
def list_memes(limit: int, offset: int):
    
    with Session() as session:

        total_memes = session.query(MemesList).filter(MemesList.id_memes).count()

        list_memes_in_db = session.query(MemesList).order_by(MemesList.id_memes.desc()).limit(limit).offset(offset)
        list_memes = []
        for i in list_memes_in_db:
            list_memes.append(create_data_memes_in_db(i))
        return ResponcePaginationMemes(success=True, error= "", memes_list=list_memes,total=total_memes,limit=limit,offset=offset)
    
@app.get("/memes_id")
def search_memes(id:int):
    with Session() as session:
        id_memes = session.query(MemesList).filter(MemesList.id_memes == id).first()
        if not id_memes:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"message": "Мема с таким id не существует"})
        
        return ResponceDataMemes(success = True,error="",data=create_data_memes_in_db(id_memes))
        
@app.put("/memes_update")
def search_memes(req:RequestUpdateMemes,id: int):
    with Session() as session:
        if not req.data and not req.description_memes:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    content={"error": "ОДНО ИЗ ПОЛЕЙ ДОЛЖНО БЫТЬ ЗАПОЛЕННО data, description_memes"})
        
        update_memes = session.query(MemesList).filter(MemesList.id_memes == id).first()
        if not update_memes:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"message": "Мема с таким id не существует"})
        else:
            update_memes.name_memes = req.data
            update_memes.description_memes = req.description_memes
            session.commit()
            new_data_memes = UpdateMemes(data=req.data,description_memes=req.description_memes)
            return JSONResponse(
            status_code=status.HTTP_201_CREATED, 
            content= ResponceUpdateUsers(success = True,error="",data = new_data_memes))

@app.delete("/memes_delete")
def delete_memes(id: int):
    with Session() as session:
        delete_memes = session.query(MemesList).filter(MemesList.id_memes == id).delete()
        session.commit()

        if not delete_memes:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"message": "Мем не найден"})   
        else:
            return JSONResponse(
                    status_code=status.HTTP_201_CREATED, 
                    content={"message": "Мем успешно удален"})