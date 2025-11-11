from unittest.mock import patch
from app.crud import create_categoria_db
import json

MOCK_DB_DATA = {
  'categorias': [
    {'id':10, 'nombre':'prueba'} 
    ],
  'productos': []
}

def test_unit_create_category_logic():
  nombre_cad = "unitary category"
  with patch("app.crud._load_db", 
             return_value=MOCK_DB_DATA.copy()) as mock_load,\
             patch("app.crud._save_db") as mock_save:
            result = create_categoria_db(nombre_cad)
            assert result['nombre'] == nombre_cad
            assert result['id'] == 11
            mock_save.assert_called_once()
            save_data = mock_save.call_args[0][0]

            print("\n---Datos en la DB---")
            print(json.dumps(save_data, indent=4))
            print("-"*20)
            assert any(cat["nombre"] == nombre_cad for cat in save_data["categorias"])
