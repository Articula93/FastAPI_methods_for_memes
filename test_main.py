
from fastapi.testclient import TestClient
import main as web_app


client = TestClient(web_app.app)

def test_post_mem():
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
    assert data['total'] >=0
    assert data['limit'] == 5
    assert data['offset'] == 20


def test_get_id_mem():
    response = client.post("/memes",json={"data":"qwertySDF","description_memes":"просто какой то текст","format_memes":"jpeg"})
    assert response.status_code == 200
    data = response.json()
    response = client.get("/memes_id?id="+ str(data["data"]["id_memes"]))
    assert response.status_code == 200
    data =  response.json() 

    assert data['success'] == True
    assert data['error'] == None
    assert data['data']['id_memes'] > 0
    assert data['data']['description_memes'] == "просто какой то текст"
    assert data['data']['data'] == "qwertySDF"


def test_put_mem():
    response = client.post("/memes",json={"data":"qwertySDF","description_memes":"просто какой то текст","format_memes":"jpeg"})
    assert response.status_code == 200
    data = response.json()
    response = client.put("/memes_update?id="+ str(data["data"]["id_memes"]),json={"data":"dGVzdAas==!asdf","description_memes":"Обновленный какой то текст22","format_memes":"PNG"})
    assert response.status_code == 200
    data =  response.json() 
    assert data['success'] == True
    assert data['error'] == None
    assert data['data']['description_memes'] == "Обновленный какой то текст22"
    assert data['data']['format_memes'] == "PNG"

def test_delete_mem():
    response = client.post("/memes",json={"data":"qwertySDF","description_memes":"просто какой то текст","format_memes":"jpeg"})
    assert response.status_code == 200
    data = response.json()
    response = client.delete("/memes_delete?id=" + str(data["data"]["id_memes"]))
    assert response.status_code == 201
    assert response.json() == {"message": "Мем успешно удален"}
    response = client.get("/memes_id?id="+ str(data["data"]["id_memes"]))
    assert response.status_code == 404

                               