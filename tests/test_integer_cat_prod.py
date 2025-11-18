""" from fastapi.testclient import TestClient
from app.main import app
from app import crud
import json

client = TestClient(app)
def setup_function():
  data_init = {
    "categorias":[{"id":1, "nombre":"electroinca"}],
    "productos": [{
      "id": 1,
      "nombre": "Smartphone",
      "categoria_id": 1
    }]
  }
  crud._save_db(data_init)
  print("Datos de prueba restaurados.")
  print(json.dumps(data_init, indent=2))
  print("- "*20)

def test_itegration_create_cat_and_prod():
  response_cat = client.post(
    "/categorias", 
    params= {
      "nombre":"Celulares"
    })
  assert response_cat.status_code == 200
  category_created =response_cat.json()
  category_id = category_created['id']

  response_prod = client.post(
    "/productos",
    params = {
      "nombre":"iPhone 13",
      "id": category_id
      })
  assert response_prod.status_code == 200
  product_create = response_prod.json()
  final_category = client.get("/categorias").json()
  assert any(cat['id'] == category_id for cat in final_category)

  final_data_db = crud._load_db()
  print("Estado final de la DB")
  print(json.dumps(final_data_db, indent=2))
  print("- "*20)

  assert product_create["nombre"] == "iPhone 13"
  assert product_create["categoria_id"] == category_id

 """