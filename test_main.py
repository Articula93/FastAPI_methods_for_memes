
from fastapi.testclient import TestClient
import main as web_app


client = TestClient(web_app.app)

def test_post_memes():
    response = client.post("/memes",json={"data":"qwertySDF","description_memes":"просто какой то текст","format_memes":"jpeg"})
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['error'] == None
    assert data['data']['id_memes'] > 0
    assert data['data']['description_memes'] == "просто какой то текст"
    assert data['data']['data'] == None
  
def test_get_memes():
    response = client.get("/memes?limit=5&offset=20")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['error'] == None
    for i in  data['memes_list']:
        assert i['id_memes'] > 0
        assert i['description_memes'] == "просто какой то текст"
        assert i['data'] == None
    assert data['total'] > 0
    assert data['limit'] > 0
    assert data['offset'] > 1


def test_get_id_memes():
    response = client.get("/memes_id?id=34")
    assert response.status_code == 200
    data =  response.json() 

    assert data['success'] == True
    assert data['error'] == None
    assert data['data']['id_memes'] > 0
    assert data['data']['description_memes'] == "Обновленный какой то текст22"
    assert data['data']['data'] == "dGVzdAas==!asdf"


def test_put_memes():
    response = client.put("/memes_update?id=37",json={"data":"dGVzdAas==!asdf","description_memes":"Обновленный какой то текст22","format_memes":"PNG"})
    assert response.status_code == 200
    data =  response.json() 
    assert data['success'] == True
    assert data['error'] == None
    assert data['data']['description_memes'] == "Обновленный какой то текст22"
    assert data['data']['format_memes'] == "PNG"

def test_delete_memes():
    response = client.delete("/memes_delete?id=53")
    assert response.status_code == 201
    assert response.json() == {"message": "Мем успешно удален"}
                               