from fastapi.testclient import TestClient
import minio_client as web_app

client = TestClient(web_app.app)


def test_add_memes():
    response = client.post("/img/add",headers={"Autorization": f"Apikey {web_app.TOKEN}"},
                           json={"name":"image_001","data":"qwertySDF"})
    assert response.status_code == 200
    assert response.json() == {"success":True,"error":"мем добавлен"}

def test_receipt_memes():
    response = client.get("/img/receipt?name=image_0001",headers={"Autorization": f"Apikey {web_app.TOKEN}"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "error":"","data":"qwertySDF"}

def test_delete_memes():
    response = client.delete("/img/del?name=image_0001",headers={"Autorization": f"Apikey {web_app.TOKEN}"})
    assert response.status_code == 200
    assert response.json() == {"success":True, "error":"Мем успешно удален","data":"image_0001"}

def test_update_memes():
    response = client.put("/img/update?name=image_0001",headers={"Autorization": f"Apikey {web_app.TOKEN}"},
                           json={"data":"qwertySDF"})
    assert response.status_code == 200
    assert response.json() == {"success":True, "error":"мем успешно обновлен"}
