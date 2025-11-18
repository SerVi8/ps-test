from fastapi.testclient import TestClient
from app.main import app
import time
import json

client = TestClient(app)

def test_e2e_full_producto_lifecycle():
  prod_nombre = f"E2E Producto {int(time.time())}"
  response_get_initial = client.get("/productos")
  initial_list = response_get_initial.json()
  initial_count = len(initial_list)
  print("\n E2E Lista inicial de porductos")
  print(json.dumps(initial_list, indent=2))
  print(f"Numero de porductos: {initial_count}")

  # Crear un nueva producto

  response_post = client.post("/productos", 
                         params={
                           "nombre": prod_nombre,
                           "categoria_id": 1
                           })
  assert response_post.status_code == 200
  producto_creado = response_post.json()
  producto_creado_id = producto_creado["id"]
  print(f"\n{"-" * 10} E2E Producto creado {"-" * 10}" )
  print(json.dumps(producto_creado, indent=2))
  print("-" * 30)

  # Verificar lista de productos actual despues del POST

  response_get_final = client.get("/productos")
  lista_final = response_get_final.json()
  print(f"\n{"-" * 10} E2E Lista final de productos {"-" * 10}" )
  print(json.dumps(lista_final, indent=2))
  print("-" * 30)
  assert len(lista_final) == (initial_count + 1)
  assert any(p["nombre"] == prod_nombre for p in lista_final)

  initial_count = len(lista_final)

  # Actualizacion de producto
  
  nuevo_nombre_prod = f"E2E Update {int(time.time())}"
  response_put = client.put(f"/productos/{producto_creado_id}", 
                         params={
                           "nombre": nuevo_nombre_prod
                           })
  assert response_put.status_code == 200
  
  response_get_update = client.get("/productos")
  lista_final = response_get_update.json()
  print(f"\n{"-" * 10} E2E Lista actualizada de productos {"-" * 10}" )
  print(json.dumps(lista_final, indent=2))
  print("-" * 30)
  assert any(c["nombre"] == nuevo_nombre_prod for c in lista_final)
  

  # Eliminar producto
  response_delete = client.delete(f"/productos/{producto_creado_id}")
  
  assert response_delete.status_code == 200
  
  # Verificar lista de productos actual despues del Delete

  response_get_final = client.get("/productos")
  lista_final = response_get_final.json()
  print(f"\n{"-" * 10} E2E Lista final de productos {"-" * 10}" )
  print(json.dumps(lista_final, indent=2))
  print("-" * 30)
  assert len(lista_final) == (initial_count - 1)

