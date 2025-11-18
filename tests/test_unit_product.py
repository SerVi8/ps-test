from unittest.mock import patch
from app.crud import create_producto_db
import json

MOCK_DB_DATA = {
  'categorias': [
    {
      "id": 1,
      "nombre": "Celulares"
    }
  ],
  'productos': [
    {
      'id':10, 
      'nombre':'IPhone 15',      
      "categoria_id": 1
    }   
  ]
}

def test_unit_create_product_logic():
  nombre_product = "unitary product"
  category_id = 1
  with patch("app.crud._load_db", 
             return_value=MOCK_DB_DATA.copy()) as mock_load,\
             patch("app.crud._save_db") as mock_save:
            result = create_producto_db(nombre_product, category_id)
            assert result['nombre'] == nombre_product
            assert result['id'] == 11
            mock_save.assert_called_once()
            save_data = mock_save.call_args[0][0]

            print("\n---Datos en la DB---")
            print(json.dumps(save_data, indent=4))
            print("-"*20)
            assert any(p["nombre"] == nombre_product for p in save_data["productos"])
